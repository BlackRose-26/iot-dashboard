import { test, expect } from '@playwright/test'
import { randomUUID } from 'node:crypto'
import fs from 'node:fs/promises'

// Visual regression capture for the CSS-to-Tailwind conversion. Runs only when VISUAL_LABEL is
// set (for example "before" or "after"); compare the two folders with scripts/compare-visual.py.
const label = process.env.VISUAL_LABEL
test.skip(!label, 'Set VISUAL_LABEL to capture screenshots.')
test.describe.configure({ mode: 'serial' })

const out = `../docs/ui-review/visual/${label}`
const sizes = {
  desktop: { width: 1440, height: 900 },
  phone: { width: 390, height: 844 },
}

async function shoot(page, name) {
  await page.waitForLoadState('networkidle')
  await expect(page.locator('.page-loading')).toHaveCount(0)
  await page.evaluate(() => document.fonts.ready)
  await page.screenshot({ path: `${out}/${name}.png`, fullPage: true, animations: 'disabled' })
}

async function adminLogin(context) {
  const page = await context.newPage()
  await page.goto('/admin/login')
  await page.getByLabel('Username', { exact: true }).fill('admin')
  await page.getByLabel('Password', { exact: true }).fill(process.env.STACK_TEST_PASSWORD)
  await page.getByRole('button', { name: 'Sign in', exact: true }).click()
  await expect(page).toHaveURL(/\/admin\/overview$/)
  const csrf = (await (await page.request.get('/api/admin/session')).json()).csrf
  return { page, csrf }
}

test('capture player and admin pages', async ({ browser }) => {
  test.setTimeout(240000)
  await fs.mkdir(out, { recursive: true })
  const staffContext = await browser.newContext({ viewport: sizes.desktop })
  const { page: staff, csrf } = await adminLogin(staffContext)
  const headers = { 'X-CSRF-Token': csrf }
  const { qrPath } = await (await staff.request.get('/api/admin/snapshot')).json()

  // One finished round (so the leaderboard exists) and one waiting player.
  async function register(context, nickname) {
    const page = await context.newPage()
    await page.goto('/scan')
    const origin = new URL(page.url()).origin
    expect(
      (
        await page.request.post('/api/player/entry', {
          data: { qrContent: origin + qrPath, method: 'upload' },
          headers: { Origin: origin },
        })
      ).status(),
    ).toBe(200)
    await page.goto('/register')
    await page.getByLabel(/^Nickname/).fill(nickname)
    await page
      .getByLabel(/^Student ID/)
      .fill(`DUMMY-${nickname.replace(/\W/g, '').toUpperCase()}`)
    await page.getByRole('checkbox').check()
    await page.getByRole('button', { name: 'Let’s stack' }).click()
    await expect(page).toHaveURL(/\/ticket$/)
    return page
  }

  for (const [size, viewport] of Object.entries(sizes)) {
    const context = await browser.newContext({ viewport })
    await context.addInitScript(() => {
      try {
        sessionStorage.setItem('smb-robot-greeted', '1')
      } catch {
        // ignore
      }
    })
    const page = await context.newPage()
    for (const [name, path] of [
      ['home', '/'],
      ['about', '/about'],
      ['contact', '/contact'],
      ['reenter', '/reenter#short'],
      ['register-gate', '/register'],
    ]) {
      await page.goto(path)
      await shoot(page, `player-${size}-${name}`)
    }
    await context.close()
  }

  const finisher = await browser.newContext({ viewport: sizes.phone })
  const finished = await register(finisher, 'Visual Winner')
  await staff.request.post('/api/admin/simulator/ready', { headers })
  await staff.request.post('/api/admin/queue/call-next', {
    headers: { ...headers, 'Idempotency-Key': randomUUID() },
  })
  await staff.request.post('/api/admin/simulator/start', { headers })
  await staff.request.post('/api/admin/simulator/win', { headers })
  await finished.goto('/ticket')
  await shoot(finished, 'player-phone-ticket-finished')
  await finished.goto('/leaderboard/acs-day')
  await shoot(finished, 'player-phone-leaderboard')
  await finished.setViewportSize(sizes.desktop)
  await finished.goto('/leaderboard/acs-day')
  await shoot(finished, 'player-desktop-leaderboard')

  const waiterContext = await browser.newContext({ viewport: sizes.phone })
  const waiter = await register(waiterContext, 'Visual Waiter')
  await shoot(waiter, 'player-phone-ticket-waiting')
  await waiter.setViewportSize(sizes.desktop)
  await shoot(waiter, 'player-desktop-ticket-waiting')

  const adminPages = [
    'overview',
    'analytics',
    'queue',
    'sessions',
    'machines',
    'settings',
    'question-review',
  ]
  for (const [variant, viewport, theme] of [
    ['desktop-light', sizes.desktop, 'light'],
    ['desktop-dark', sizes.desktop, 'dark'],
    ['phone-light', sizes.phone, 'light'],
  ]) {
    const context = await browser.newContext({ viewport })
    await context.addInitScript((value) => {
      try {
        localStorage.setItem('smb-admin-theme', value)
      } catch {
        // ignore
      }
    }, theme)
    const loginPage = await context.newPage()
    await loginPage.goto('/admin/login')
    await shoot(loginPage, `admin-${variant}-login`)
    await loginPage.close()
    const { page } = await adminLogin(context)
    for (const name of adminPages) {
      await page.goto(`/admin/${name}`)
      await shoot(page, `admin-${variant}-${name}`)
    }
    await context.close()
  }
  await finisher.close()
  await waiterContext.close()
  await staffContext.close()
})
