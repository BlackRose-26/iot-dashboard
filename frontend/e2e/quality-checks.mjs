// Manual synthetic resilience companion, not part of the normal spec discovery.
import { chromium } from '@playwright/test'
import { createInterface } from 'node:readline'
const lines = createInterface({ input: process.stdin })
const iterator = lines[Symbol.asyncIterator]()
const read = async () => JSON.parse((await iterator.next()).value)
const report = (value) => process.stdout.write(`${JSON.stringify(value)}\n`)
let browser
try {
  const config = await read()
  browser = await chromium.launch({ executablePath: config.browser, headless: true })
  const pages = []
  const contexts = []
  const errors = []
  for (let index = 0; index < config.cookies.length; index += 5) {
    await Promise.all(
      config.cookies.slice(index, index + 5).map(async (cookies, offset) => {
        const context = await browser.newContext({ viewport: { width: 390, height: 844 } })
        contexts[index + offset] = context
        await context.addCookies(cookies)
        const page = await context.newPage()
        page.on('pageerror', (error) => errors.push(error.message))
        await page.goto(`${config.url}/ticket`, { waitUntil: 'domcontentloaded' })
        await page.getByText(/Live updates/).waitFor({ timeout: 60000 })
        pages[index + offset] = page
      }),
    )
  }
  report({ stage: 'ready', clients: pages.length })
  while (true) {
    const command = await read()
    if (command.action === 'observe') {
      const latencies = await Promise.all(
        pages.map(async (page) => {
          await page.getByText(command.text, { exact: true }).waitFor({ timeout: 60000 })
          return Date.now() - command.startedAt
        }),
      )
      report({ stage: 'observed', latencies, browserErrors: errors.length })
    } else if (command.action === 'one') {
      // Keep the oldest player for a process-restart recovery check.
      while (contexts.length > 1) await contexts.pop().close()
      pages.splice(1)
      report({ stage: 'one' })
    } else if (command.action === 'live') {
      await pages[0].getByText(/Live updates/).waitFor({ timeout: 60000 })
      report({ stage: 'live' })
    } else if (command.action === 'close') break
    else throw new Error('Unknown synthetic check command')
  }
} catch (error) {
  report({ stage: 'error', message: error.message })
  process.exitCode = 1
} finally {
  await browser?.close()
  lines.close()
}
