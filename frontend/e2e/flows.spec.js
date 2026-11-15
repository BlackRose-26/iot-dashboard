import { test, expect } from '@playwright/test'
import AxeBuilder from '@axe-core/playwright'

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
  await expect(first.getByText('You’re next. Get ready to stack.')).toBeVisible()
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
    for (const route of ['overview', 'analytics', 'queue', 'sessions', 'machines']) {
      await page.goto(`/admin/${route}`)
      await expect(page.locator('html')).toHaveAttribute('data-admin-theme', theme)
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
