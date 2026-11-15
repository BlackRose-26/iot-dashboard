import { chromium } from '@playwright/test'
import fs from 'node:fs/promises'
const browser = await chromium.launch({ channel: 'msedge', headless: true })
const page = await browser.newPage()
await page.goto('http://127.0.0.1:5173/admin/overview')
await page.waitForLoadState('networkidle')
await page.evaluate(() => document.fonts.ready)
const data = await page.evaluate(() => {
  const icon = document.querySelector('.brand-mark .fa-symbol')
  const style = getComputedStyle(icon, '::before')
  const glyph = style.content.replaceAll('"', '')
  const canvas = document.createElement('canvas')
  canvas.width = 64
  canvas.height = 64
  const ctx = canvas.getContext('2d')
  ctx.fillStyle = '#dfff00'
  ctx.beginPath()
  ctx.roundRect(0, 0, 64, 64, 18)
  ctx.fill()
  ctx.font = `900 36px ${getComputedStyle(icon).fontFamily}`
  ctx.textAlign = 'center'
  ctx.textBaseline = 'middle'
  ctx.fillStyle = '#111313'
  ctx.fillText(glyph, 32, 34)
  return canvas.toDataURL('image/png').split(',')[1]
})
await fs.writeFile('public/favicon.png', Buffer.from(data, 'base64'))
await browser.close()
console.log('Created raster favicon from the standard Font Awesome layer-group glyph.')
