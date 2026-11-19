import { defineConfig } from '@playwright/test'
export default defineConfig({
  testDir: './e2e',
  fullyParallel: false,
  workers: 1,
  use: {
    baseURL: process.env.STACK_TEST_URL || 'http://127.0.0.1:5174',
    ...(process.env.STACK_TEST_BROWSER_PATH
      ? { launchOptions: { executablePath: process.env.STACK_TEST_BROWSER_PATH } }
      : { channel: process.env.STACK_TEST_BROWSER || 'msedge' }),
    headless: true,
    viewport: { width: 1440, height: 1000 },
    reducedMotion: 'reduce',
    screenshot: 'only-on-failure',
  },
  reporter: [['list'], ['json', { outputFile: '../docs/ui-review/browser-tests.json' }]],
})
