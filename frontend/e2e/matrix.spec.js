import { test, expect } from '@playwright/test'
import { randomUUID } from 'node:crypto'

test('Matrix device protocol completes a 15-point game and updates the player and charts', async ({
  page,
  browser,
  playwright,
}) => {
  test.skip(
    process.env.STACK_TEST_RULESET !== 'matrix-v1',
    'Run with STACK_TEST_RULESET=matrix-v1 and a disposable database.',
  )
  await page.goto('/admin/login')
  await page.getByLabel('Username', { exact: true }).fill('admin')
  await page.getByLabel('Password', { exact: true }).fill(process.env.STACK_TEST_PASSWORD)
  await page.getByRole('button', { name: 'Sign in', exact: true }).click()
  await expect(page).toHaveURL(/\/admin\/overview$/)
  await expect(page.getByText('Matrix v1', { exact: true }).first()).toBeVisible()
  const snapshot = await (await page.request.get('/api/admin/snapshot')).json()
  expect(snapshot.game.code).toBe('matrix-v1')
  await page.getByRole('button', { name: 'Registration QR' }).click()
  const qrImage = Buffer.from(
    await page
      .getByRole('dialog')
      .locator('canvas')
      .evaluate((element) => element.toDataURL('image/png').split(',')[1]),
    'base64',
  )
  await page.getByRole('button', { name: 'Close dialog' }).click()
  const playerContext = await browser.newContext()
  const player = await playerContext.newPage()
  const device = await playwright.request.newContext({
    baseURL: process.env.STACK_TEST_URL,
    extraHTTPHeaders: { 'X-Device-Token': 'disposable-browser-device-token' },
  })
  try {
    await player.goto('/scan')
    await player
      .getByLabel('QR code image', { exact: true })
      .setInputFiles({ name: 'game-qr.png', mimeType: 'image/png', buffer: qrImage })
    await expect(player).toHaveURL(/\/register$/)
    await expect(player.getByText('15 levels', { exact: true })).toBeVisible()
    await expect(player.getByText('15 points', { exact: true })).toBeVisible()
    await player.getByLabel(/^Nickname/).fill('Matrix Tester')
    await player.getByLabel(/^Student ID/).fill('SYNTHETIC-MATRIX-01')
    await player.getByRole('checkbox').check()
    await player.getByRole('button', { name: 'Let’s stack' }).click()
    await expect(player).toHaveURL(/\/ticket$/)
    const bootId = randomUUID()
    // Like fresh firmware: discover the current lineage first, because an
    // earlier spec may already have registered a boot in this database.
    const enrollment = await device.get('/api/device/enrollment')
    expect(enrollment.status()).toBe(200)
    const { currentBootId } = await enrollment.json()
    expect(
      (
        await device.post('/api/device/boot', {
          data: { bootId, previousBootId: currentBootId, storageId: randomUUID(), uptimeMs: 0 },
        })
      ).status(),
    ).toBe(200)
    // Device-only identity; student ID is never part of command/result evidence.
    const headers = { 'X-Device-Boot-Id': bootId }
    expect(
      (
        await device.post('/api/device/heartbeat', {
          headers,
          data: { state: 'ready', firmware: 'synthetic-matrix-browser-test' },
        })
      ).status(),
    ).toBe(200)
    const auth = await (await page.request.get('/api/admin/session')).json()
    const called = await page.request.post('/api/admin/queue/call-next', {
      headers: { 'X-CSRF-Token': auth.csrf, 'Idempotency-Key': randomUUID() },
    })
    expect(called.status()).toBe(200)
    const command = (await (await device.get('/api/device/commands', { headers })).json())
      .commands[0]
    expect(command.rules.levels).toBe(15)
    expect(JSON.stringify(command)).not.toContain('SYNTHETIC-MATRIX')
    const packet = {
      sessionId: command.sessionId,
      commandId: command.id,
      expectedRevision: command.expectedRevision,
    }
    expect(
      (
        await device.post('/api/device/journal', {
          headers,
          data: { ...packet, eventId: randomUUID(), sequence: 1, uptimeMs: 0, phase: 'reserved' },
        })
      ).status(),
    ).toBe(200)
    expect(
      (
        await device.post('/api/device/journal', {
          headers,
          data: {
            ...packet,
            eventId: randomUUID(),
            sequence: 2,
            uptimeMs: 0,
            phase: 'started',
            roundBootId: bootId,
            startUptimeMs: 0,
          },
        })
      ).status(),
    ).toBe(200)
    let clock = 0
    const placements = Array.from({ length: 15 }, (_, i) => {
      clock += (i === 0 ? 60 : 50) * 5 + 5
      return { candidate_x: 5, candidate_width: 6, overlap_width: 6, locked_at_ms: clock }
    })
    // Real elapsed time must cover the submitted trace; never forge a server clock.
    await new Promise((resolve) => setTimeout(resolve, clock + 100))
    const terminal = {
      ...packet,
      eventId: randomUUID(),
      sequence: 3,
      uptimeMs: clock,
      phase: 'terminal',
      roundBootId: bootId,
      startUptimeMs: 0,
      terminal: {
        terminalId: randomUUID(),
        rulesHash: command.rulesHash,
        outcome: 'win',
        durationMs: clock,
        placements,
      },
    }
    const result = await device.post('/api/device/journal', { headers, data: terminal })
    expect(result.status()).toBe(200)
    expect((await result.json()).score).toBe(15)
    expect((await device.post('/api/device/journal', { headers, data: terminal })).status()).toBe(
      200,
    )
    await expect
      .poll(
        async () => (await (await player.request.get('/api/player/context')).json()).ticket.status,
      )
      .toBe('completed')
    const completed = await (await player.request.get('/api/player/context')).json()
    expect(completed.ticket.score).toBe(15)
    expect(completed.notifications).toHaveLength(1)
    await player.goto('/ticket')
    await player.getByRole('link', { name: 'View the leaderboard' }).click()
    await expect(player.getByText('Matrix Tester').first()).toBeVisible()
    expect((await player.request.get('/api/admin/snapshot')).status()).toBe(401)
    await page.goto('/admin/sessions')
    await expect(page.getByText('Matrix Tester')).toBeVisible()
    await expect(page.getByText('Matrix v1', { exact: false }).first()).toBeVisible()
    const analytics = await (
      await page.request.get('/api/admin/analytics?source=device&period=event_to_date')
    ).json()
    expect(analytics.levels).toHaveLength(15)
    expect(analytics.summary.highest_score).toBe(15)
    await page.screenshot({ path: '../docs/ui-review/matrix-device-completed.png', fullPage: true })
  } finally {
    await device.dispose()
    await playerContext.close()
  }
})
