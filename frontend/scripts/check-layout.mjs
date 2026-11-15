import { chromium } from '@playwright/test'
const browser = await chromium.launch({ channel: 'msedge', headless: true })
const page = await browser.newPage({ viewport: { width: 390, height: 844 } })
await page.goto('http://127.0.0.1:5173/admin/sessions')
await page.waitForLoadState('networkidle')
console.log(
  JSON.stringify(
    await page.evaluate(() =>
      [...document.querySelectorAll('body *')]
        .filter(
          (n) =>
            n.getBoundingClientRect().right > window.innerWidth + 1 &&
            getComputedStyle(n).position !== 'absolute',
        )
        .map((n) => ({
          tag: n.tagName,
          class: n.className,
          right: n.getBoundingClientRect().right,
          width: n.getBoundingClientRect().width,
        }))
        .slice(0, 18),
    ),
    null,
    2,
  ),
)
console.log(
  JSON.stringify(
    await page.evaluate(() => ({
      doc: document.documentElement.scrollWidth,
      body: document.body.scrollWidth,
      els: [
        ...document.querySelectorAll(
          '.app-shell,header,.scope-bar,main,.page-heading,.page-actions,.sessions-card,.table-tools,.table-scroll,footer,.sr-only',
        ),
      ].map((n) => ({
        class: n.className,
        rect: n.getBoundingClientRect().toJSON(),
        scroll: n.scrollWidth,
        overflow: getComputedStyle(n).overflow,
        width: getComputedStyle(n).width,
        position: getComputedStyle(n).position,
      })),
    })),
    null,
    2,
  ),
)
await browser.close()
