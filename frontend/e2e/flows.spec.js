import { test, expect } from '@playwright/test'
import AxeBuilder from '@axe-core/playwright'
import { randomUUID } from 'node:crypto'

test.describe.configure({ mode: 'serial' })
const errors = []
let entryPath
let qrImage
let foreignQrImage
async function login(page) {
  page.on('pageerror', (e) => errors.push(e.message))
  await page.goto('/admin/login')
  await page.getByLabel('Username', { exact: true }).fill('admin')
  await page.getByLabel('Password', { exact: true }).fill(process.env.STACK_TEST_PASSWORD)
  await page.getByRole('button', { name: 'Sign in', exact: true }).click()
  await expect(page).toHaveURL(/\/admin\/overview$/)
}
async function screenshot(page, name) {
  await expect(page.getByRole('main')).toBeVisible()
  await expect(page.locator('.page-loading')).toHaveCount(0)
  await page.screenshot({ path: `../docs/ui-review/access-${name}.png`, fullPage: true })
}
async function join(page, name, id) {
  await page.goto('/scan')
  await page
    .getByLabel('QR code image', { exact: true })
    .setInputFiles({ name: 'game-qr.png', mimeType: 'image/png', buffer: qrImage })
  await expect(page).toHaveURL(/\/register$/)
  await page.getByLabel(/^Nickname/).fill(name)
  await page.getByLabel(/^Student ID/).fill(id)
  await page.getByRole('checkbox').check()
  await page.getByRole('button', { name: 'Let’s stack' }).click()
  await expect(page).toHaveURL(/\/ticket$/)
}

test('admin login protects dashboard and QR-only registration', async ({ page }) => {
  await page.goto('/admin/queue')
  await expect(page).toHaveURL(/\/admin\/login$/)
  expect((await page.request.get('/api/admin/snapshot')).status()).toBe(401)
  await screenshot(page, 'login-light')
  await page.getByRole('button', { name: 'Switch to dark mode' }).click()
  await screenshot(page, 'login-dark')
  await page.goto('/register')
  await expect(page.getByRole('heading', { name: 'Your game starts with a scan.' })).toBeVisible()
  expect(await page.locator('a[href^="/admin"]').count()).toBe(0)
  await login(page)
  const snapshot = await (await page.request.get('/api/admin/snapshot')).json()
  entryPath = snapshot.qrPath
  await page.getByRole('button', { name: 'Registration QR' }).click()
  await expect(page.getByRole('dialog').locator('canvas')).toBeVisible()
  qrImage = Buffer.from(
    await page
      .getByRole('dialog')
      .locator('canvas')
      .evaluate((element) => element.toDataURL('image/png').split(',')[1]),
    'base64',
  )
  expect(
    await page.getByRole('link', { name: 'Test player entry' }).getAttribute('href'),
  ).toContain(entryPath)
  await page.getByLabel('Event website address').fill('https://other.example')
  await expect(page.getByRole('link', { name: 'Test player entry' })).toHaveAttribute(
    'href',
    new RegExp('^https://other.example/'),
  )
  foreignQrImage = Buffer.from(
    await page
      .getByRole('dialog')
      .locator('canvas')
      .evaluate((element) => element.toDataURL('image/png').split(',')[1]),
    'base64',
  )
  await page.getByLabel('Event website address').fill(new URL(page.url()).origin)
  await page.getByRole('button', { name: 'Close dialog' }).click()
  await screenshot(page, 'overview-dark')
  await page.getByRole('button', { name: 'Switch to light mode' }).click()
  await screenshot(page, 'overview-light')
  await page.getByRole('button', { name: 'Sign out' }).click()
  await expect(page).toHaveURL(/\/admin\/login$/)
})

test('two independent phones queue in order, receive win/loss, and unlock leaderboards', async ({
  browser,
}) => {
  const adminContext = await browser.newContext()
  const one = await browser.newContext({ viewport: { width: 390, height: 844 } })
  const two = await browser.newContext({ viewport: { width: 360, height: 800 } })
  const admin = await adminContext.newPage()
  const first = await one.newPage()
  const second = await two.newPage()
  first.on('pageerror', (e) => errors.push(e.message))
  second.on('pageerror', (e) => errors.push(e.message))
  await login(admin)
  await first.goto(entryPath)
  await expect(first.getByRole('button', { name: 'Use camera', exact: true })).toBeVisible()
  expect((await (await first.request.get('/api/player/context')).json()).canRegister).toBe(false)
  await first
    .getByLabel('QR code image', { exact: true })
    .setInputFiles({ name: 'game-qr.png', mimeType: 'image/png', buffer: qrImage })
  await expect(first).toHaveURL(/\/register$/)
  await screenshot(first, 'registration-phone')
  await first.getByRole('button', { name: 'Let’s stack' }).click()
  await expect(first.getByLabel(/^Nickname/)).toBeFocused()
  await join(first, 'First Player', 'DUMMY-BROWSER-0001')
  await join(second, 'Second Player', 'DUMMY-BROWSER-0002')
  await expect(
    first.getByText('You’re first in line. Wait for the operator to call you.'),
  ).toBeVisible()
  await expect(second.getByText('1 player ahead of you')).toBeVisible()
  await first.reload()
  await expect(first.getByText('Hey, First Player.')).toBeVisible()
  expect((await first.request.get('/api/admin/snapshot')).status()).toBe(401)
  expect((await first.request.get('/api/player/leaderboard')).status()).toBe(403)
  expect(await first.locator('a[href^="/admin"]').count()).toBe(0)
  expect(await first.content()).not.toContain('DUMMY-BROWSER-0001')
  expect(await first.evaluate(() => Object.keys(localStorage))).toEqual(['smb-admin-theme'])
  await screenshot(first, 'waiting-phone')
  await admin.goto('/admin/machines')
  await admin.getByRole('button', { name: 'Set simulator ready' }).click()
  await admin.goto('/admin/queue')
  await expect(admin.getByRole('button', { name: 'Call next player' })).toBeEnabled()
  await admin.getByRole('button', { name: 'Call next player' }).click()
  await expect(first.getByRole('heading', { name: 'It’s your turn.' })).toBeVisible()
  await screenshot(first, 'called-phone')
  await admin.goto('/admin/machines')
  await admin.getByRole('button', { name: 'Start test round' }).click()
  await expect(first.getByRole('heading', { name: 'Make it count.' })).toBeVisible()
  await admin.getByRole('button', { name: 'Finish: win' }).click()
  await expect(first.getByRole('alert')).toContainText('You won! Congratulations.')
  await screenshot(first, 'win-phone')
  await first.getByRole('link', { name: 'View the leaderboard' }).click()
  await expect(first.getByText('Every player, one best stack.')).toBeVisible()
  await screenshot(first, 'leaderboard-phone')
  await admin.goto('/admin/queue')
  await admin.getByRole('button', { name: 'Call next player' }).click()
  await admin.goto('/admin/machines')
  await admin.getByRole('button', { name: 'Start test round' }).click()
  await admin.getByRole('button', { name: 'Finish: loss' }).click()
  await expect(second.getByRole('alert')).toContainText('Game finished. Thanks for playing!')
  await screenshot(second, 'loss-phone')
  await second.getByRole('link', { name: 'View the leaderboard' }).click()
  await expect(second.getByText('Second Player', { exact: true }).first()).toBeVisible()
  expect(await second.evaluate(() => document.documentElement.scrollWidth)).toBe(360)
  for (const page of [first, second]) {
    const results = await new AxeBuilder({ page })
      .withTags(['wcag2a', 'wcag2aa', 'wcag21aa'])
      .analyze()
    expect(results.violations).toEqual([])
  }
  await adminContext.close()
  await one.close()
  await two.close()
})

test('admin screens have neutral light and dark modes and accessible phone navigation', async ({
  page,
}) => {
  test.setTimeout(90000)
  await login(page)
  const violations = []
  for (const theme of ['light', 'dark']) {
    if ((await page.locator('html').getAttribute('data-admin-theme')) !== theme)
      await page.getByRole('button', { name: `Switch to ${theme} mode` }).click()
    for (const route of ['overview', 'analytics', 'queue', 'sessions', 'machines', 'settings']) {
      await page.goto(`/admin/${route}`)
      await expect(page.locator('html')).toHaveAttribute('data-admin-theme', theme)
      expect(
        await page.locator('body').evaluate((element) => getComputedStyle(element).fontFamily),
      ).toContain('Open Sans Variable')
      await screenshot(page, `${route}-${theme}`)
      const results = await new AxeBuilder({ page })
        .withTags(['wcag2a', 'wcag2aa', 'wcag21aa'])
        .analyze()
      violations.push(
        ...results.violations.map((v) => ({
          theme,
          route,
          id: v.id,
          nodes: v.nodes.map((n) => n.target),
        })),
      )
    }
  }
  await page.reload()
  await expect(page.locator('html')).toHaveAttribute('data-admin-theme', 'dark')
  await page.setViewportSize({ width: 360, height: 800 })
  await page.getByRole('button', { name: 'Open navigation' }).click()
  await page.getByRole('link', { name: 'Sessions', exact: true }).click()
  expect(await page.evaluate(() => document.documentElement.scrollWidth)).toBe(360)
  await screenshot(page, 'admin-dark-phone')
  expect(violations).toEqual([])
  expect(errors).toEqual([])
})

test('boot-bound device fence enables an audited unstarted release in the admin UI', async ({
  page,
  browser,
}) => {
  await login(page)
  const playerContext = await browser.newContext({ viewport: { width: 390, height: 844 } })
  try {
    const player = await playerContext.newPage()
    await join(player, 'Recovery Guest', 'DUMMY-BROWSER-RECOVERY')
    const bootId = randomUUID()
    const deviceHeaders = {
      'X-Device-Token': process.env.STACK_DEVICE_TOKEN,
      'X-Device-Boot-Id': bootId,
    }
    const registered = await page.request.post('/api/device/boot', {
      headers: deviceHeaders,
      data: { bootId, storageId: randomUUID(), previousBootId: null, uptimeMs: 0 },
    })
    expect(registered.status()).toBe(200)
    expect(
      (
        await page.request.post('/api/device/heartbeat', {
          headers: deviceHeaders,
          data: { state: 'ready', firmware: 'synthetic-browser-recovery' },
        })
      ).status(),
    ).toBe(200)
    await page.goto('/admin/queue')
    await page.getByRole('button', { name: 'Call next player' }).click()
    await expect(player.getByText(/It’s your turn/)).toBeVisible()
    const command = (
      await (await page.request.get('/api/device/commands', { headers: deviceHeaders })).json()
    ).commands[0]
    expect(
      (
        await page.request.post('/api/device/journal', {
          headers: deviceHeaders,
          data: {
            eventId: randomUUID(),
            sequence: 1,
            uptimeMs: 100,
            sessionId: command.sessionId,
            commandId: command.id,
            expectedRevision: command.expectedRevision,
            phase: 'reserved',
          },
        })
      ).status(),
    ).toBe(200)
    await page.goto('/admin/machines')
    await expect(page.getByText(bootId, { exact: true })).toBeVisible()
    await page.getByRole('button', { name: 'Request device stop', exact: true }).click()
    await page.getByLabel('Reason for this decision').fill('Synthetic browser recovery check')
    await page.getByRole('button', { name: 'Confirm decision' }).click()
    await expect(page.getByRole('dialog')).toHaveCount(0)
    await expect(page.getByRole('button', { name: 'Release unstarted round' })).toHaveCount(0)
    const fence = (
      await (await page.request.get('/api/device/commands', { headers: deviceHeaders })).json()
    ).commands[0]
    expect(fence.type).toBe('fence')
    expect(
      (
        await page.request.post('/api/device/journal', {
          headers: deviceHeaders,
          data: {
            eventId: randomUUID(),
            sequence: 2,
            uptimeMs: 200,
            sessionId: fence.sessionId,
            commandId: fence.id,
            expectedRevision: fence.expectedRevision,
            phase: 'fenced_unstarted',
          },
        })
      ).status(),
    ).toBe(200)
    await expect(page.getByRole('button', { name: 'Release unstarted round' })).toBeVisible()
    for (const theme of ['light', 'dark']) {
      if ((await page.locator('html').getAttribute('data-admin-theme')) !== theme)
        await page.getByRole('button', { name: `Switch to ${theme} mode` }).click()
      const recoveryCard = page.locator('section').filter({
        has: page.getByRole('heading', { name: 'Device recovery', exact: true }),
      })
      // These utilities override the legacy card padding, proving the Vite CSS
      // pipeline and layer order work in the real browser, not just in JSX.
      await expect(recoveryCard).toHaveCSS('padding', '28px')
      await expect(recoveryCard).toHaveCSS('margin-top', '24px')
      await screenshot(page, `device-recovery-${theme}`)
      expect(
        (await new AxeBuilder({ page }).withTags(['wcag2a', 'wcag2aa', 'wcag21aa']).analyze())
          .violations,
      ).toEqual([])
    }
    await page.setViewportSize({ width: 360, height: 800 })
    expect(await page.evaluate(() => document.documentElement.scrollWidth)).toBe(360)
    await screenshot(page, 'device-recovery-phone')
    await page.getByRole('button', { name: 'Release unstarted round' }).click()
    await page
      .getByLabel('Reason for this decision')
      .fill('Reviewed saved never-started fence receipt')
    await page.getByRole('button', { name: 'Confirm decision' }).click()
    await expect(page.getByText(bootId, { exact: true })).toHaveCount(0)
    await expect(page.locator('.toast')).toBeVisible()
    const toastWidth = await page
      .locator('.toast')
      .evaluate((element) => element.getBoundingClientRect().width)
    expect(toastWidth).toBeGreaterThanOrEqual(320)
    expect(toastWidth).toBeLessThanOrEqual(336)
    await expect
      .poll(
        async () => (await (await player.request.get('/api/player/context')).json()).ticket.status,
      )
      .toBe('expired')
    const snapshot = await (await page.request.get('/api/admin/snapshot')).json()
    expect(snapshot.currentPlayer).toBeNull()
    expect(snapshot.machineState).toBe('offline')
    expect(
      (await (await player.request.get('/api/player/context')).json()).notifications,
    ).toHaveLength(0)
  } finally {
    await playerContext.close()
  }
})

test('Player didn’t come stops and releases an unstarted no-show in one click', async ({
  page,
  browser,
}) => {
  await login(page)
  const playerContext = await browser.newContext({ viewport: { width: 390, height: 844 } })
  try {
    const player = await playerContext.newPage()
    await join(player, 'No Show Guest', 'DUMMY-BROWSER-NOSHOW')
    const bootId = randomUUID()
    const deviceHeaders = {
      'X-Device-Token': process.env.STACK_DEVICE_TOKEN,
      'X-Device-Boot-Id': bootId,
    }
    // Like fresh firmware: continue the current lineage registered by earlier specs.
    const { currentBootId } = await (
      await page.request.get('/api/device/enrollment', { headers: deviceHeaders })
    ).json()
    expect(
      (
        await page.request.post('/api/device/boot', {
          headers: deviceHeaders,
          data: { bootId, storageId: randomUUID(), previousBootId: currentBootId, uptimeMs: 0 },
        })
      ).status(),
    ).toBe(200)
    expect(
      (
        await page.request.post('/api/device/heartbeat', {
          headers: deviceHeaders,
          data: { state: 'ready', firmware: 'synthetic-browser-noshow' },
        })
      ).status(),
    ).toBe(200)
    await page.goto('/admin/queue')
    await page.getByRole('button', { name: 'Call next player' }).click()
    await expect(player.getByText(/within about 3 minutes/)).toBeVisible()
    const reserve = (
      await (await page.request.get('/api/device/commands', { headers: deviceHeaders })).json()
    ).commands[0]
    const journal = (sequence, command, phase) =>
      page.request.post('/api/device/journal', {
        headers: deviceHeaders,
        data: {
          eventId: randomUUID(),
          sequence,
          uptimeMs: sequence * 100,
          sessionId: command.sessionId,
          commandId: command.id,
          expectedRevision: command.expectedRevision,
          phase,
        },
      })
    expect((await journal(1, reserve, 'reserved')).status()).toBe(200)

    await page.getByRole('button', { name: /Player didn.t come/ }).click()
    await page.getByRole('button', { name: 'Stop and release' }).click()
    await expect(page.getByText(/Waiting for the cabinet to confirm/)).toBeVisible()
    // The simulated cabinet confirms the round never started; the UI then releases on its own.
    let fence
    await expect
      .poll(async () => {
        fence = (
          await (await page.request.get('/api/device/commands', { headers: deviceHeaders })).json()
        ).commands[0]
        return fence?.type
      })
      .toBe('fence')
    expect((await journal(2, fence, 'fenced_unstarted')).status()).toBe(200)
    await expect(page.locator('.toast')).toContainText('no score')
    await expect
      .poll(
        async () => (await (await player.request.get('/api/player/context')).json()).ticket.status,
      )
      .toBe('expired')
    const snapshot = await (await page.request.get('/api/admin/snapshot')).json()
    expect(snapshot.currentPlayer).toBeNull()
    expect(
      (await (await player.request.get('/api/player/context')).json()).notifications,
    ).toHaveLength(0)
  } finally {
    await playerContext.close()
  }
})

test('operator re-entry QR restores a lost ticket on a new phone exactly once', async ({
  page,
  browser,
}) => {
  await login(page)
  const oldContext = await browser.newContext({ viewport: { width: 390, height: 844 } })
  const newContext = await browser.newContext({ viewport: { width: 390, height: 844 } })
  try {
    const oldPhone = await oldContext.newPage()
    await join(oldPhone, 'Lost Phone Guest', 'DUMMY-BROWSER-REENTRY')
    const before = (await (await oldPhone.request.get('/api/player/context')).json()).ticket

    await page.goto('/admin/queue')
    await page.getByLabel('Find a player to restore').fill('Lost Phone')
    const issued = page.waitForResponse(
      (r) =>
        /\/api\/admin\/players\/[^/]+\/reentry$/.test(r.url()) && r.request().method() === 'POST',
    )
    await page.getByRole('button', { name: 'Show re-entry QR for Lost Phone Guest' }).click()
    const { path } = await (await issued).json()
    const dialog = page.getByRole('dialog')
    await expect(dialog.locator('canvas')).toBeVisible()
    await expect(dialog).toContainText('works once')
    expect(await dialog.textContent()).not.toContain(path.split('#')[1])

    // The new phone has no cookie for this player; the code rides in the fragment only.
    const newPhone = await newContext.newPage()
    const sent = []
    newPhone.on('request', (request) => sent.push(request.url()))
    await newPhone.goto(path)
    await expect(newPhone).toHaveURL(/\/ticket$/)
    const after = (await (await newPhone.request.get('/api/player/context')).json()).ticket
    expect(after.nickname).toBe('Lost Phone Guest')
    expect(after.status).toBe(before.status)
    expect(sent.some((url) => url.includes(path.split('#')[1]))).toBe(false)
    expect(
      (await (await oldPhone.request.get('/api/player/context')).json()).ticket ?? null,
    ).toBeNull()

    // A second scan of the same QR is refused with a clear message.
    const again = await (await browser.newContext()).newPage()
    await again.goto(path)
    await expect(again.getByText(/expired or was already used/)).toBeVisible()
    await again.context().close()
    await page.getByRole('button', { name: 'Done' }).click()
    await expect(dialog).toBeHidden()
    expect(errors).toEqual([])
  } finally {
    await oldContext.close()
    await newContext.close()
  }
})

test('administrator creates an operator who runs the line without admin-only tools', async ({
  page,
  browser,
}) => {
  await login(page)
  await page.goto('/admin/settings')
  await page.getByLabel('New operator username').fill('booth-e2e')
  await page.getByRole('button', { name: 'Add operator' }).click()
  const dialog = page.getByRole('dialog')
  await expect(dialog).toContainText('Password for booth-e2e')
  const password = (await dialog.getByText(/^[a-z2-9]{4}(-[a-z2-9]{4}){3}$/).textContent()).trim()
  expect(password).toMatch(/^[a-z2-9]{4}(-[a-z2-9]{4}){3}$/)
  await dialog.getByRole('button', { name: 'Done' }).click()
  await expect(page.getByRole('list', { name: 'Staff accounts' })).toContainText('booth-e2e')

  const operatorContext = await browser.newContext()
  try {
    const operator = await operatorContext.newPage()
    operator.on('pageerror', (e) => errors.push(e.message))
    await operator.goto('/admin/login')
    await operator.getByLabel('Username', { exact: true }).fill('booth-e2e')
    await operator.getByLabel('Password', { exact: true }).fill(password)
    await operator.getByRole('button', { name: 'Sign in', exact: true }).click()
    await expect(operator).toHaveURL(/\/admin\/overview$/)
    await expect(operator.getByLabel('Signed in as booth-e2e, operator')).toHaveText('OP')

    await operator.goto('/admin/queue')
    await expect(operator.getByRole('button', { name: 'Call next player' })).toBeVisible()
    await expect(operator.getByText('Player lost their ticket?')).toBeVisible()
    await expect(operator.getByRole('heading', { name: 'Development simulator' })).toHaveCount(0)
    await operator.goto('/admin/settings')
    await expect(operator.getByText('Staff accounts')).toHaveCount(0)
    await expect(operator.getByRole('link', { name: 'Review questions' })).toHaveCount(0)
    await operator.goto('/admin/question-review')
    await expect(operator.getByRole('heading', { name: 'Administrators only' })).toBeVisible()
    expect((await operator.request.get('/api/admin/staff')).status()).toBe(403)

    // Switching the account off signs the operator out.
    await page.getByRole('button', { name: 'Switch off booth-e2e' }).click()
    await expect(page.locator('.toast')).toContainText('booth-e2e is switched off')
    expect((await operator.request.get('/api/admin/snapshot')).status()).toBe(401)
    expect(errors).toEqual([])
  } finally {
    await operatorContext.close()
  }
})

test('player site: header, About, Contact and the sticky robot chat', async ({ browser }) => {
  const axe = (page) =>
    new AxeBuilder({ page }).withTags(['wcag2a', 'wcag2aa', 'wcag21aa']).analyze()
  const desktop = await browser.newContext({ viewport: { width: 1440, height: 900 } })
  const wide = await desktop.newPage()
  wide.on('pageerror', (e) => errors.push(e.message))
  await wide.goto('/')
  const nav = wide.getByRole('navigation', { name: 'Main' })
  await expect(nav.getByRole('link', { name: 'Home' })).toHaveClass(/active/)
  await expect(wide.getByRole('button', { name: 'Use camera', exact: true })).toBeInViewport()
  await expect(wide.getByLabel('Live line status')).toBeInViewport()
  await expect(wide.getByRole('button', { name: 'Open Stack Intelligence' })).toBeInViewport()
  expect((await axe(wide)).violations).toEqual([])
  await wide.screenshot({ path: '../docs/ui-review/site-home-desktop.png' })

  // The robot opens from the hero button, answers, and closes back to the icon.
  await wide.getByRole('button', { name: 'Ask the robot' }).click()
  const chat = wide.getByRole('dialog', { name: 'Stack Intelligence' })
  await chat.getByRole('button', { name: 'How do I play?' }).click()
  await expect(chat.getByRole('log')).toContainText('Press the big button')
  await expect(chat.getByRole('log')).toContainText('Game rules')
  await chat.getByLabel('Ask Stack Intelligence a question').fill('my id is 2021-12345')
  await chat.getByRole('button', { name: 'Send question' }).click()
  await expect(chat.getByRole('log')).toContainText('Please don’t share your student ID here')
  expect((await axe(wide)).violations).toEqual([])
  await wide.screenshot({ path: '../docs/ui-review/site-chat-open-desktop.png' })

  // The conversation survives moving to About and Contact.
  await nav.getByRole('link', { name: 'About' }).click()
  await expect(wide.getByRole('heading', { level: 1 })).toContainText('A carnival stacker')
  await expect(chat.getByRole('log')).toContainText('Press the big button')
  await wide.getByRole('button', { name: 'Close chat' }).click()
  await expect(chat).toHaveCount(0)
  expect((await axe(wide)).violations).toEqual([])
  await wide
    .getByRole('navigation', { name: 'Main' })
    .getByRole('link', { name: 'Contact' })
    .click()
  await expect(wide.getByRole('heading', { level: 1 })).toContainText('Need a hand?')
  expect((await axe(wide)).violations).toEqual([])
  await wide.screenshot({ path: '../docs/ui-review/site-contact-desktop.png' })
  await desktop.close()

  const phone = await browser.newContext({ viewport: { width: 390, height: 844 } })
  try {
    const page = await phone.newPage()
    page.on('pageerror', (e) => errors.push(e.message))
    await page.goto('/scan')
    await expect(page.getByRole('button', { name: 'Use camera', exact: true })).toBeVisible()
    await page.getByRole('button', { name: 'Menu' }).click()
    await expect(page.getByRole('navigation', { name: 'Main' })).toBeVisible()
    await page.getByRole('button', { name: 'Menu' }).click()
    await page.screenshot({ path: '../docs/ui-review/site-home-phone.png', fullPage: true })
    expect((await axe(page)).violations).toEqual([])

    await join(page, 'Robot Guest', 'DUMMY-BROWSER-ROBOT')
    await page.getByRole('button', { name: 'Ask the robot' }).click()
    const phoneChat = page.getByRole('dialog', { name: 'Stack Intelligence' })
    await phoneChat.getByRole('button', { name: 'When is my turn?' }).click()
    await expect(phoneChat.getByRole('log')).toContainText(/You’re (#\d+|next)/)
    expect((await axe(page)).violations).toEqual([])
    await page.screenshot({ path: '../docs/ui-review/site-ticket-chat-phone.png' })
    expect(errors).toEqual([])
  } finally {
    await phone.close()
  }
})

test('motion: animations play by default and switch off with reduce motion', async ({
  browser,
}) => {
  const animation = (locator) =>
    locator.evaluate((element) => getComputedStyle(element).animationName)
  const moving = await browser.newContext({ reducedMotion: 'no-preference' })
  try {
    const page = await moving.newPage()
    await page.goto('/')
    const launcher = page.getByRole('button', { name: 'Open Stack Intelligence' })
    expect(await animation(launcher)).toBe('pop-in')
    expect(await animation(page.getByRole('heading', { level: 1 }))).toBe('fade-up')
    await launcher.click()
    expect(await animation(page.getByRole('dialog', { name: 'Stack Intelligence' }))).toBe(
      'panel-in',
    )
  } finally {
    await moving.close()
  }
  const still = await browser.newContext({ reducedMotion: 'reduce' })
  try {
    const page = await still.newPage()
    await page.goto('/')
    expect(await animation(page.getByRole('button', { name: 'Open Stack Intelligence' }))).toBe(
      'none',
    )
    expect(await animation(page.getByRole('heading', { level: 1 }))).toBe('none')
  } finally {
    await still.close()
  }
})
