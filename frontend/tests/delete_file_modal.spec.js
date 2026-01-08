import { test, expect } from '@playwright/test'

test.describe('DeleteFileModal', () => {
  test.beforeEach(async ({ page }) => {
    // Set a dummy auth token in localStorage BEFORE navigating to the page
    await page.goto('/');
    await page.evaluate(() => {
      localStorage.setItem('token', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IlRlc3QgVXNlciIsImlhdCI6MTUxNjIzOTAyMn0.dummy_signature');
    });
    // Now navigate to the page
    await page.goto('/');

    // Mock the API calls
    await page.route('**/api/v1/drive/files', async route => {
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({
          files: [{ id: '1', name: 'test_file.txt', mimeType: 'text/plain' }],
          connected: true
        }),
      })
    })

    await page.route('**/api/v1/drive/files/*', async route => {
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({ message: 'File deleted successfully' }),
      })
    })
  })

  test('should open and close the delete modal when cancel is clicked', async ({ page }) => {
    // Click the delete button
    await page.click('button:has-text("Delete")')

    // Check if the modal is visible
    await expect(page.locator('.modal-title')).toHaveText('Confirm Deletion');
    await expect(page.locator('.modal-body strong')).toHaveText('test_file.txt');

    // Click the cancel button
    await page.click('button:has-text("Cancel")')

    // Check if the modal is no longer visible
    await expect(page.locator('.modal-overlay')).not.toBeVisible();
  })

  test('should open and close the delete modal when confirm is clicked', async ({ page }) => {
    // Click the delete button
    await page.click('button:has-text("Delete")')

    // Check if the modal is visible
    await expect(page.locator('.modal-title')).toHaveText('Confirm Deletion');
    await expect(page.locator('.modal-body strong')).toHaveText('test_file.txt');

    // Click the delete button on the modal (confirm)
    await page.locator('.modal-footer button:has-text("Delete")').click();

    // Check if the modal is no longer visible
    await expect(page.locator('.modal-overlay')).not.toBeVisible();
  })
})
