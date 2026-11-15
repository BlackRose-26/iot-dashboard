import { chromium } from '@playwright/test'
import fs from 'node:fs/promises'
import path from 'node:path'
const pass = process.argv[2] || '01'
const width = Number(process.argv[3] || 1440)
const height = Number(process.argv[4] || 1000)
const directory = path.resolve('../docs/ui-review', `pass-${pass}-${width}`)
await fs.mkdir(directory, { recursive: true })
const browser = await chromium.launch({ channel: 'msedge', headless: true })
const page = await browser.newPage({ viewport: { width, height }, reducedMotion: 'reduce' })
const errors = []
page.on('pageerror', (e) => errors.push(e.message))
const routes = [
  ['overview', '/admin/overview'],
  ['analytics', '/admin/analytics'],
  ['queue', '/admin/queue'],
  ['sessions', '/admin/sessions'],
  ['machine', '/admin/machines'],
  ['leaderboard', '/leaderboard/acs-day'],
  ['registration', '/register/acs-day/cabinet-01'],
  ['ticket', '/ticket'],
]
const results = []
for (const [name, route] of routes) {
  await page.goto(`http://127.0.0.1:5173${route}`)
  await page.waitForLoadState('networkidle')
  await page.evaluate(() => document.fonts.ready)
  const metrics = await page.evaluate(() => ({
    scrollWidth: document.documentElement.scrollWidth,
    width: window.innerWidth,
    title: document.title,
    headings: [...document.querySelectorAll('h1')].map((h) => h.textContent),
    brokenImages: [...document.images].filter((i) => !i.complete || i.naturalWidth === 0).length,
  }))
  await page.screenshot({ path: path.join(directory, `${name}.png`), fullPage: true })
  results.push({ page: name, ...metrics, overflow: metrics.scrollWidth > width })
}
await fs.writeFile(
  path.join(directory, 'results.json'),
  JSON.stringify({ pass, width, height, errors, pages: results }, null, 2),
)
console.log(JSON.stringify({ pass, width, errors, pages: results }, null, 2))
await browser.close()
if (errors.length || results.some((r) => r.overflow || r.brokenImages)) process.exitCode = 1
