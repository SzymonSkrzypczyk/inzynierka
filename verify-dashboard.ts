import { test, expect } from '@playwright/test';

test('dashboard renders with data', async ({ page }) => {
  page.on('console', msg => console.log('BROWSER CONSOLE:', msg.text()));
  page.on('pageerror', err => console.log('BROWSER ERROR:', err.message));

  await page.goto('http://localhost:3000');

  // Wait for the hero panel to be visible
  await expect(page.locator('.hero-panel')).toBeVisible();

  // Wait for data to load - check if Kp value is not 0.00
  await page.waitForFunction(() => {
    const kpElement = document.querySelector('.font-display-lg');
    return kpElement && kpElement.textContent !== '0.00';
  }, { timeout: 10000 });

  // Additional wait for charts to animate/render
  await page.waitForTimeout(5000);

  await page.screenshot({ path: '/home/jules/verification/screenshots/dashboard_retry.png', fullPage: true });

  // Check for presence of Kp bars
  const bars = await page.locator('.kp-bar').count();
  console.log(`Found ${bars} Kp bars`);

  // Check for presence of canvas elements (Chart.js)
  const canvases = await page.locator('canvas').count();
  console.log(`Found ${canvases} Chart.js canvases`);
});
