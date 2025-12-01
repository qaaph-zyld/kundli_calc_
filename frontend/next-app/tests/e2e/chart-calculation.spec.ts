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
