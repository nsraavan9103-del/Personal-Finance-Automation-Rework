import { test, expect } from '@playwright/test';

test.describe('Personal Finance Dashboard', () => {
  test.beforeEach(async ({ page }) => {
    // Capture console logs for debugging
    page.on('console', msg => console.log('BROWSER CONSOLE:', msg.text()));
    page.on('pageerror', err => console.log('BROWSER ERROR:', err.message));
    
    // Capture network responses for debugging
    page.on('response', response => {
      if (response.url().includes('/api/')) {
        console.log(`API RESPONSE: ${response.status()} ${response.url()}`);
      }
    });
    
    await page.goto('/');
    await page.waitForLoadState('networkidle');
  });

  test('should load the dashboard with header', async ({ page }) => {
    await expect(page.locator('h1')).toContainText('Personal Finance Dashboard');
  });

  test('should show file upload component', async ({ page }) => {
    await expect(page.locator('text=Drag and drop')).toBeVisible();
  });

  test('should show tab navigation', async ({ page }) => {
    // Check for the tab buttons specifically
    await expect(page.locator('button:has-text("Expenses (Debits)")')).toBeVisible();
    await expect(page.locator('button:has-text("Payments (Credits)")')).toBeVisible();
  });

  test('should upload CSV and show transactions', async ({ page }) => {
    // Create a test CSV file
    const csvContent = `Date,Details,Amount,Debit/Credit
15 Jan 2024,STARBUCKS,25.50,Debit
16 Jan 2024,SALARY,5000.00,Credit
17 Jan 2024,UBER,45.00,Debit`;

    // Upload the CSV
    const fileInput = page.locator('input[type="file"]');
    await fileInput.setInputFiles({
      name: 'test.csv',
      mimeType: 'text/csv',
      buffer: Buffer.from(csvContent)
    });

    // Click the upload button to submit the form
    await page.click('button:has-text("Upload Statement")');

    // Wait for upload to complete and transactions to appear
    await page.waitForSelector('text=STARBUCKS', { timeout: 30000 });
    
    // Verify Debit transactions are displayed on Expenses tab (default)
    await expect(page.locator('text=STARBUCKS').first()).toBeVisible();
    await expect(page.locator('text=UBER').first()).toBeVisible();
    
    // Verify amounts for Debit transactions
    await expect(page.locator('text=25.50').first()).toBeVisible();
    await expect(page.locator('text=45.00').first()).toBeVisible();
  });

  test('should switch between Expenses and Payments tabs', async ({ page }) => {
    // Upload CSV first
    const csvContent = `Date,Details,Amount,Debit/Credit
15 Jan 2024,STARBUCKS,25.50,Debit
16 Jan 2024,SALARY,5000.00,Credit`;

    const fileInput = page.locator('input[type="file"]');
    await fileInput.setInputFiles({
      name: 'test.csv',
      mimeType: 'text/csv',
      buffer: Buffer.from(csvContent)
    });

    // Click the upload button to submit the form
    await page.click('button:has-text("Upload Statement")');

    await page.waitForSelector('text=STARBUCKS', { timeout: 30000 });

    // Click Payments tab
    await page.click('button:has-text("Payments (Credits)")');
    await expect(page.locator('text=SALARY').first()).toBeVisible();
    await expect(page.locator('text=5000.00').first()).toBeVisible();

    // Click Expenses tab
    await page.click('button:has-text("Expenses (Debits)")');
    await expect(page.locator('text=STARBUCKS').first()).toBeVisible();
    await expect(page.locator('text=25.50').first()).toBeVisible();
  });

  test('should show expense summary', async ({ page }) => {
    const csvContent = `Date,Details,Amount,Debit/Credit
15 Jan 2024,STARBUCKS,25.50,Debit
17 Jan 2024,UBER,45.00,Debit`;

    const fileInput = page.locator('input[type="file"]');
    await fileInput.setInputFiles({
      name: 'test.csv',
      mimeType: 'text/csv',
      buffer: Buffer.from(csvContent)
    });

    // Click the upload button to submit the form
    await page.click('button:has-text("Upload Statement")');

    await page.waitForSelector('text=STARBUCKS', { timeout: 30000 });
    
    // Check for summary section
    await expect(page.locator('text=Expense Summary')).toBeVisible({ timeout: 10000 });
  });

  test('should show category management', async ({ page }) => {
    const csvContent = `Date,Details,Amount,Debit/Credit
15 Jan 2024,STARBUCKS,25.50,Debit`;

    const fileInput = page.locator('input[type="file"]');
    await fileInput.setInputFiles({
      name: 'test.csv',
      mimeType: 'text/csv',
      buffer: Buffer.from(csvContent)
    });

    // Click the upload button to submit the form
    await page.click('button:has-text("Upload Statement")');

    await page.waitForSelector('text=STARBUCKS', { timeout: 30000 });
    
    // Check for category dropdown or management - use first() to avoid strict mode violation
    await expect(page.locator('text=Categories').first()).toBeVisible({ timeout: 10000 });
  });
});