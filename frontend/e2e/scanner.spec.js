import { test, expect } from '@playwright/test'
import AxeBuilder from '@axe-core/playwright'
import fs from 'node:fs/promises'

async function qrFixtures(browser) {
  const context = await browser.newContext()
  const page = await context.newPage()
  await page.goto('/admin/login')
  await page.getByLabel('Username', { exact: true }).fill('admin')
  await page.getByLabel('Password', { exact: true }).fill(process.env.STACK_TEST_PASSWORD)
  await page.getByRole('button', { name: 'Sign in', exact: true }).click()
  await expect(page).toHaveURL(/\/admin\/overview$/)
  await page.getByRole('button', { name: 'Registration QR' }).click()
  const canvas = page.getByRole('dialog').locator('canvas')
  const good = Buffer.from(
    await canvas.evaluate((element) => element.toDataURL('image/png').split(',')[1]),
    'base64',
  )
  const link = await page.getByRole('link', { name: 'Test player entry' }).getAttribute('href')
  await page.getByLabel('Event website address').fill('https://other.example')
  await expect(page.getByRole('link', { name: 'Test player entry' })).toHaveAttribute(
    'href',
    /^https:\/\/other.example/,
  )
  await canvas.evaluate(
    () => new Promise((resolve) => requestAnimationFrame(() => requestAnimationFrame(resolve))),
  )
  const foreign = Buffer.from(
    await canvas.evaluate((element) => element.toDataURL('image/png').split(',')[1]),
    'base64',
  )
  await fs.writeFile('../docs/ui-review/scanner-test-foreign.png', foreign)
  await fs.writeFile('../docs/ui-review/scanner-test-good.png', good)
  await context.close()
  return { good, foreign, link }
}
test('scanner uses real image decoding, rejects unrelated images, and does not trust a pasted QR link', async ({
  browser,
  page,
}) => {
  const { foreign, link } = await qrFixtures(browser)
  await page.setViewportSize({ width: 390, height: 844 })
  await page.goto(link)
  await expect(page.getByRole('button', { name: 'Use camera', exact: true })).toBeVisible()
  await expect(page.getByRole('button', { name: 'Upload QR image', exact: true })).toBeVisible()
  expect((await (await page.request.get('/api/player/context')).json()).canRegister).toBe(false)
  await page.screenshot({ path: '../docs/ui-review/scanner-phone.png', fullPage: true })
  expect(await page.locator('svg').count()).toBe(0)
  expect(await page.evaluate(() => document.documentElement.scrollWidth)).toBe(390)
  expect(
    (await new AxeBuilder({ page }).withTags(['wcag2a', 'wcag2aa', 'wcag21aa']).analyze())
      .violations,
  ).toEqual([])
  const input = page.getByLabel('QR code image', { exact: true })
  await input.setInputFiles({
    name: 'notes.txt',
    mimeType: 'text/plain',
    buffer: Buffer.from('not a QR image'),
  })
  await expect(page.getByRole('alert')).toContainText('Choose a PNG, JPG or WebP')
  const blank = await page.screenshot()
  await input.setInputFiles({ name: 'no-code.png', mimeType: 'image/png', buffer: blank })
  await expect(page.getByRole('alert')).toContainText('No readable QR code')
  await page.setViewportSize({ width: 1440, height: 1000 })
  await page.goto('/scan')
  await page.screenshot({ path: '../docs/ui-review/scanner-desktop.png', fullPage: true })
  const request = page.waitForRequest(
    (r) => r.url().endsWith('/api/player/entry') && r.method() === 'POST',
  )
  // A registered game token remains valid when its printed hostname differs.
  await input.setInputFiles({ name: 'game-qr.png', mimeType: 'image/png', buffer: foreign })
  expect((await request).postDataJSON()).toEqual({ qrContent: link, method: 'upload' })
  await expect(page).toHaveURL(/\/register$/)
})

test('camera API decodes a synthetic live stream and releases it after detection', async ({
  browser,
}) => {
  const { good } = await qrFixtures(browser)
  const context = await browser.newContext()
  await context.addInitScript((png) => {
    Object.defineProperty(navigator.mediaDevices, 'getUserMedia', {
      configurable: true,
      value: async () => {
        const image = new Image()
        image.src = `data:image/png;base64,${png}`
        await image.decode()
        const canvas = document.createElement('canvas')
        canvas.width = canvas.height = 640
        const ctx = canvas.getContext('2d')
        const stream = canvas.captureStream(8)
        const draw = () => {
          ctx.fillStyle = 'white'
          ctx.fillRect(0, 0, 640, 640)
          ctx.drawImage(image, 0, 0, 640, 640)
        }
        const timer = setInterval(draw, 100)
        draw()
        window.__cameraStopped = 0
        for (const track of stream.getTracks()) {
          const stop = track.stop.bind(track)
          track.stop = () => {
            window.__cameraStopped++
            clearInterval(timer)
            stop()
          }
        }
        return stream
      },
    })
  }, good.toString('base64'))
  const page = await context.newPage()
  await page.goto('/scan')
  const request = page.waitForRequest(
    (r) => r.url().endsWith('/api/player/entry') && r.method() === 'POST',
  )
  await page.getByRole('button', { name: 'Use camera', exact: true }).click()
  expect((await request).postDataJSON().method).toBe('camera')
  await expect(page).toHaveURL(/\/register$/)
  expect(await page.evaluate(() => window.__cameraStopped)).toBeGreaterThan(0)
  await context.close()
})

test('camera permission failure leaves image upload available', async ({ page }) => {
  await page.addInitScript(() => {
    Object.defineProperty(navigator.mediaDevices, 'getUserMedia', {
      configurable: true,
      value: async () => {
        throw new DOMException('Denied for test', 'NotAllowedError')
      },
    })
  })
  await page.goto('/scan')
  await page.getByRole('button', { name: 'Use camera', exact: true }).click()
  await expect(page.getByRole('alert')).toContainText('camera could not open')
  await expect(page.getByRole('button', { name: 'Upload QR image', exact: true })).toBeEnabled()
})

test('cancelled camera permission does not block upload and a late stream is stopped', async ({
  browser,
}) => {
  const { good } = await qrFixtures(browser)
  const context = await browser.newContext()
  await context.addInitScript(() => {
    Object.defineProperty(navigator.mediaDevices, 'getUserMedia', {
      configurable: true,
      value: () =>
        new Promise((resolve) => {
          window.__resolveCamera = () => {
            const canvas = document.createElement('canvas')
            canvas.width = canvas.height = 320
            const stream = canvas.captureStream(8)
            window.__lateStopped = 0
            for (const track of stream.getTracks()) {
              const stop = track.stop.bind(track)
              track.stop = () => {
                window.__lateStopped++
                stop()
              }
            }
            resolve(stream)
          }
        }),
    })
  })
  const page = await context.newPage()
  const errors = []
  page.on('pageerror', (error) => errors.push(error.message))
  await page.goto('/scan')
  await page.getByRole('button', { name: 'Use camera', exact: true }).click()
  await expect.poll(() => page.evaluate(() => typeof window.__resolveCamera)).toBe('function')
  await page.getByRole('button', { name: 'Cancel camera', exact: true }).click()
  await page
    .getByLabel('QR code image', { exact: true })
    .setInputFiles({ name: 'game-qr.png', mimeType: 'image/png', buffer: good })
  await expect(page).toHaveURL(/\/register$/)
  await page.evaluate(() => window.__resolveCamera())
  await expect.poll(() => page.evaluate(() => window.__lateStopped)).toBeGreaterThan(0)
  await page.evaluate(() => new Promise((resolve) => setTimeout(resolve, 100)))
  expect(errors).toEqual([])
  await context.close()
})
