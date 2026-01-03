// playwright.config.js
// @ts-check
const { defineConfig, devices } = require('@playwright/test');

/**
 * @see https://playwright.dev/docs/test-configuration
 */
module.exports = defineConfig({
  testDir: './tests', // Look for tests in the 'tests' directory
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: 'list',
  use: {
    trace: 'on-first-retry',
    baseURL: 'http://localhost:4200',
  },
  projects: [
    {
      name: 'firefox',
      use: {
        ...devices['Desktop Firefox'],
        headless: false, // Ensure the browser window is visible
      },
    },
  ],
  webServer: {
    command: 'npm run dev',
    url: 'http://localhost:4200',
    timeout: 120 * 1000,
    reuseExistingServer: !process.env.CI,
  },
});
