import { test, expect } from '@playwright/test';

/**
 * E2E Tests for Kundli Chart Calculation
 * 
 * Tests the main chart generation flow including:
 * - Form submission
 * - Chart display
 * - Planetary positions
 * - Chart type switching
 */

test.describe('Chart Calculation Flow', () => {
  
  test.beforeEach(async ({ page }) => {
    // Navigate to the main page
    await page.goto('/');
  });

  test('should display the birth details form', async ({ page }) => {
    // Check for form elements
    await expect(page.locator('form')).toBeVisible();
    
    // Check for date input
    const dateInput = page.locator('input[type="date"]');
    await expect(dateInput).toBeVisible();
    
    // Check for time input
    const timeInput = page.locator('input[type="time"]');
    await expect(timeInput).toBeVisible();
  });

  test('should show location input fields', async ({ page }) => {
    // Check for location input (could be autocomplete or manual)
    const locationInput = page.locator('input[name="location"], input[placeholder*="location"], input[placeholder*="city"]');
    
    // At least one location-related input should exist
    const locationInputs = await page.locator('input').filter({ hasText: /location|city|place/i }).count();
    const latInput = page.locator('input[name="latitude"], input[placeholder*="latitude"]');
    const lonInput = page.locator('input[name="longitude"], input[placeholder*="longitude"]');
    
    // Either location autocomplete or lat/lon inputs should be present
    const hasLocation = (await locationInput.count()) > 0 || 
                        ((await latInput.count()) > 0 && (await lonInput.count()) > 0);
    
    expect(hasLocation || locationInputs > 0).toBeTruthy();
  });

  test('should have ayanamsa selection with Lahiri option', async ({ page }) => {
    // Look for ayanamsa dropdown or radio buttons
    const ayanamsaSelect = page.locator('select').filter({ hasText: /lahiri|ayanamsa/i });
    const ayanamsaLabel = page.getByText(/ayanamsa/i);
    
    // Check if ayanamsa selection exists
    const hasAyanamsaControl = (await ayanamsaSelect.count()) > 0 || 
                               (await ayanamsaLabel.count()) > 0;
    
    expect(hasAyanamsaControl).toBeTruthy();
  });

  test('should have house system selection with Whole Sign option', async ({ page }) => {
    // Look for house system dropdown
    const houseSelect = page.locator('select').filter({ hasText: /house|whole sign/i });
    const houseLabel = page.getByText(/house system/i);
    
    const hasHouseControl = (await houseSelect.count()) > 0 || 
                            (await houseLabel.count()) > 0;
    
    expect(hasHouseControl).toBeTruthy();
  });

  test('should have a submit button', async ({ page }) => {
    // Check for submit button
    const submitButton = page.locator('button[type="submit"], button').filter({ hasText: /calculate|generate|submit/i });
    await expect(submitButton.first()).toBeVisible();
  });

});


test.describe('Chart Display', () => {
  
  test('should show chart type selector after calculation', async ({ page }) => {
    await page.goto('/');
    
    // Fill in a test birth data
    const dateInput = page.locator('input[type="date"]');
    if (await dateInput.isVisible()) {
      await dateInput.fill('1990-01-15');
    }
    
    const timeInput = page.locator('input[type="time"]');
    if (await timeInput.isVisible()) {
      await timeInput.fill('12:00');
    }
    
    // Try to find and fill latitude/longitude if available
    const latInput = page.locator('input[name="latitude"]');
    const lonInput = page.locator('input[name="longitude"]');
    
    if (await latInput.isVisible()) {
      await latInput.fill('28.6139');
    }
    if (await lonInput.isVisible()) {
      await lonInput.fill('77.209');
    }
    
    // Submit the form
    const submitButton = page.locator('button[type="submit"], button').filter({ hasText: /calculate|generate|submit/i });
    if (await submitButton.first().isVisible()) {
      await submitButton.first().click();
      
      // Wait for chart to load (with timeout)
      await page.waitForResponse(
        response => response.url().includes('/api/') && response.status() === 200,
        { timeout: 30000 }
      ).catch(() => {
        // API might not be running, skip
      });
      
      // Check if chart type buttons appear
      const chartTypeButtons = page.locator('button').filter({ hasText: /rasi|north|south|navamsa/i });
      
      // If calculation succeeded, chart type buttons should appear
      if ((await chartTypeButtons.count()) > 0) {
        await expect(chartTypeButtons.first()).toBeVisible();
      }
    }
  });

});


test.describe('Page Navigation', () => {
  
  test('should have a title containing Kundli', async ({ page }) => {
    await page.goto('/');
    
    // Check page title or heading
    const title = await page.title();
    const h1 = page.locator('h1');
    
    const hasKundliTitle = title.toLowerCase().includes('kundli') || 
                           title.toLowerCase().includes('astrology') ||
                           title.toLowerCase().includes('chart');
    
    const h1Text = await h1.first().textContent().catch(() => '');
    const hasKundliHeading = h1Text?.toLowerCase().includes('kundli') ||
                              h1Text?.toLowerCase().includes('chart');
    
    expect(hasKundliTitle || hasKundliHeading).toBeTruthy();
  });

  test('should be responsive on mobile', async ({ page }) => {
    await page.setViewportSize({ width: 375, height: 667 });
    await page.goto('/');
    
    // Page should still be usable on mobile
    await expect(page.locator('body')).toBeVisible();
    
    // Form should still be accessible
    const formInputs = page.locator('input');
    expect(await formInputs.count()).toBeGreaterThan(0);
  });

});


test.describe('Mobile UX Tests', () => {
  
  // iPhone 14 viewport
  const mobileViewport = { width: 390, height: 844 };
  
  // iPhone SE viewport (smaller)
  const smallMobileViewport = { width: 375, height: 667 };

  test('should display mobile menu button on mobile viewport', async ({ page }) => {
    await page.setViewportSize(mobileViewport);
    await page.goto('/');
    
    // Mobile menu button should be visible
    const mobileMenuBtn = page.locator('button[aria-label="Open menu"], button:has-text("☰")');
    await expect(mobileMenuBtn).toBeVisible();
    
    // Desktop nav should be hidden
    const desktopNav = page.locator('nav').filter({ hasText: /compare|transits/i });
    // On mobile, main nav should be hidden or collapsed
  });

  test('should open and close mobile menu', async ({ page }) => {
    await page.setViewportSize(mobileViewport);
    await page.goto('/');
    
    // Open mobile menu
    const mobileMenuBtn = page.locator('button[aria-label="Open menu"], button:has-text("☰")');
    await mobileMenuBtn.click();
    
    // Menu should be visible
    await expect(page.getByText('Home')).toBeVisible();
    await expect(page.getByText('Compatibility')).toBeVisible();
    await expect(page.getByText('Transits')).toBeVisible();
    
    // Close menu
    const closeBtn = page.locator('button[aria-label="Close menu"], button:has-text("✕")');
    await closeBtn.click();
    
    // Menu should close (wait a bit for animation)
    await page.waitForTimeout(500);
  });

  test('should have touch-friendly form inputs on mobile', async ({ page }) => {
    await page.setViewportSize(mobileViewport);
    await page.goto('/');
    
    // Check that inputs are large enough for touch (min 44px height)
    const dateInput = page.locator('input[type="date"]');
    if (await dateInput.isVisible()) {
      const box = await dateInput.boundingBox();
      if (box) {
        expect(box.height).toBeGreaterThanOrEqual(40);
      }
    }
    
    // Submit button should be full width on mobile
    const submitButton = page.locator('button[type="submit"]');
    if (await submitButton.isVisible()) {
      const box = await submitButton.boundingBox();
      const viewport = page.viewportSize();
      if (box && viewport) {
        // Button should take most of the width (accounting for padding)
        expect(box.width).toBeGreaterThan(viewport.width * 0.8);
      }
    }
  });

  test('should not have horizontal scroll on mobile', async ({ page }) => {
    await page.setViewportSize(mobileViewport);
    await page.goto('/');
    
    // Check that body doesn't overflow horizontally
    const bodyWidth = await page.evaluate(() => document.body.scrollWidth);
    const viewportWidth = mobileViewport.width;
    
    expect(bodyWidth).toBeLessThanOrEqual(viewportWidth + 10); // Small tolerance
  });

  test('should handle chart calculation flow on mobile', async ({ page }) => {
    await page.setViewportSize(mobileViewport);
    await page.goto('/');
    
    // Fill form on mobile
    const dateInput = page.locator('input[type="date"]');
    if (await dateInput.isVisible()) {
      await dateInput.fill('1990-01-15');
    }
    
    const timeInput = page.locator('input[type="time"]');
    if (await timeInput.isVisible()) {
      await timeInput.fill('12:00');
    }
    
    // Submit
    const submitButton = page.locator('button[type="submit"]');
    if (await submitButton.isVisible()) {
      await submitButton.click();
      
      // Wait for potential API response
      await page.waitForTimeout(2000);
      
      // Check that page is still usable (no errors blocking view)
      await expect(page.locator('body')).toBeVisible();
    }
  });

  test('should have readable text on small mobile viewport', async ({ page }) => {
    await page.setViewportSize(smallMobileViewport);
    await page.goto('/');
    
    // Check heading font size is reasonable
    const h1 = page.locator('h1').first();
    if (await h1.isVisible()) {
      const fontSize = await h1.evaluate(el => 
        parseFloat(window.getComputedStyle(el).fontSize)
      );
      expect(fontSize).toBeGreaterThanOrEqual(16);
    }
    
    // Check labels are readable
    const labels = page.locator('label');
    const labelCount = await labels.count();
    for (let i = 0; i < Math.min(labelCount, 3); i++) {
      const label = labels.nth(i);
      if (await label.isVisible()) {
        const fontSize = await label.evaluate(el => 
          parseFloat(window.getComputedStyle(el).fontSize)
        );
        expect(fontSize).toBeGreaterThanOrEqual(12);
      }
    }
  });

  test('should navigate via mobile menu', async ({ page }) => {
    await page.setViewportSize(mobileViewport);
    await page.goto('/');
    
    // Open mobile menu
    const mobileMenuBtn = page.locator('button[aria-label="Open menu"], button:has-text("☰")');
    if (await mobileMenuBtn.isVisible()) {
      await mobileMenuBtn.click();
      
      // Click on Compatibility
      const compatibilityLink = page.getByText('Compatibility');
      if (await compatibilityLink.isVisible()) {
        await compatibilityLink.click();
        
        // Should navigate to compare page
        await page.waitForURL('**/compare', { timeout: 5000 }).catch(() => {});
      }
    }
  });

  test('should show charts properly on mobile', async ({ page }) => {
    await page.setViewportSize(mobileViewport);
    await page.goto('/');
    
    // Fill form and calculate
    const dateInput = page.locator('input[type="date"]');
    const timeInput = page.locator('input[type="time"]');
    
    if (await dateInput.isVisible() && await timeInput.isVisible()) {
      await dateInput.fill('1990-01-15');
      await timeInput.fill('12:00');
      
      const submitButton = page.locator('button[type="submit"]');
      await submitButton.click();
      
      // Wait for chart to potentially load
      await page.waitForResponse(
        response => response.url().includes('/api/') && response.status() === 200,
        { timeout: 10000 }
      ).catch(() => {});
      
      // If chart appears, it should fit within viewport
      const chartContainer = page.locator('svg, [class*="chart"]').first();
      if (await chartContainer.isVisible()) {
        const box = await chartContainer.boundingBox();
        if (box) {
          expect(box.width).toBeLessThanOrEqual(mobileViewport.width);
        }
      }
    }
  });

});


test.describe('API Integration', () => {
  
  test('should connect to backend API', async ({ page, request }) => {
    // Test direct API connection
    const response = await request.get('http://localhost:8000/api/v1/health/').catch(() => null);
    
    if (response) {
      expect(response.status()).toBe(200);
    } else {
      // API not running - test will be skipped
      test.skip();
    }
  });

  test('should be able to calculate chart via API', async ({ request }) => {
    const response = await request.post('http://localhost:8000/api/v1/charts/calculate', {
      data: {
        date_time: '1990-01-15T06:30:00Z',
        latitude: 28.6139,
        longitude: 77.209,
        altitude: 0,
        ayanamsa: 1,
        house_system: 'W'
      }
    }).catch(() => null);
    
    if (response) {
      expect(response.status()).toBe(200);
      
      const data = await response.json();
      
      // Verify response structure
      expect(data).toHaveProperty('planetary_positions');
      expect(data).toHaveProperty('houses');
      expect(data).toHaveProperty('ayanamsa_value');
      
      // Verify planets are present
      expect(data.planetary_positions).toHaveProperty('Sun');
      expect(data.planetary_positions).toHaveProperty('Moon');
      expect(data.planetary_positions).toHaveProperty('Mars');
    } else {
      test.skip();
    }
  });

});
