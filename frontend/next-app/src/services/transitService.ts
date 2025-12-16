/**
 * Transit Service - Fetches real-time planetary positions
 * Uses the backend API for accurate ephemeris calculations
 */

const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8000/api/v1';

export interface TransitPositions {
  Sun: number;
  Moon: number;
  Mars: number;
  Mercury: number;
  Jupiter: number;
  Venus: number;
  Saturn: number;
  Rahu: number;
  Ketu: number;
}

export interface TransitAnalysis {
  success: boolean;
  analysis: {
    gochara_results: Array<{
      planet: string;
      transit_sign: number;
      house_from_moon: number;
      is_benefic: boolean;
      vedha_blocked: boolean;
    }>;
    sade_sati: {
      is_active: boolean;
      phase: string | null;
      intensity: string;
    };
    overall_score: number;
    predictions: string[];
  };
}

/**
 * Fetch current planetary positions from backend
 */
export async function getCurrentTransits(): Promise<TransitPositions> {
  try {
    // Get current datetime
    const now = new Date().toISOString();
    
    // Calculate current chart to get transit positions
    const response = await fetch(`${API_BASE}/charts/calculate`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        date_time: now,
        latitude: 0,  // Geocentric positions
        longitude: 0,
        ayanamsa: 1,  // Lahiri
        house_system: 'W'
      })
    });

    if (!response.ok) {
      throw new Error('Failed to fetch transit positions');
    }

    const data = await response.json();
    const positions: TransitPositions = {
      Sun: 0, Moon: 0, Mars: 0, Mercury: 0,
      Jupiter: 0, Venus: 0, Saturn: 0, Rahu: 0, Ketu: 0
    };

    // Extract longitudes from response
    Object.entries(data.planetary_positions || {}).forEach(([planet, info]: [string, any]) => {
      if (planet in positions) {
        positions[planet as keyof TransitPositions] = parseFloat(info.longitude);
      }
    });

    return positions;
  } catch (error) {
    console.error('Error fetching transits:', error);
    // Return approximate current positions as fallback (Dec 2024)
    return {
      Sun: 265,      // Sagittarius
      Moon: 120,     // Leo (approximate)
      Mars: 95,      // Cancer
      Mercury: 270,  // Sagittarius
      Jupiter: 55,   // Taurus
      Venus: 300,    // Capricorn
      Saturn: 340,   // Pisces
      Rahu: 15,      // Aries
      Ketu: 195      // Libra
    };
  }
}

/**
 * Analyze transits for a natal chart
 */
export async function analyzeTransits(
  natalMoonSign: number,
  natalPlanets: Record<string, number>,
  currentPositions: TransitPositions
): Promise<TransitAnalysis | null> {
  try {
    const response = await fetch(`${API_BASE}/transits/analyze`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        natal_moon_sign: natalMoonSign,
        natal_planets: natalPlanets,
        current_positions: currentPositions,
        datetime: new Date().toISOString()
      })
    });

    if (!response.ok) {
      return null;
    }

    return await response.json();
  } catch (error) {
    console.error('Error analyzing transits:', error);
    return null;
  }
}

/**
 * Check Sade Sati status
 */
export async function checkSadeSati(
  natalMoonSign: number,
  saturnLongitude: number
): Promise<{ isActive: boolean; phase: string | null; intensity: string }> {
  try {
    const response = await fetch(`${API_BASE}/transits/sade-sati`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        natal_moon_sign: natalMoonSign,
        current_saturn_longitude: saturnLongitude
      })
    });

    if (!response.ok) {
      throw new Error('Failed to check Sade Sati');
    }

    const data = await response.json();
    return {
      isActive: data.is_active || false,
      phase: data.phase || null,
      intensity: data.intensity || 'None'
    };
  } catch (error) {
    console.error('Error checking Sade Sati:', error);
    // Calculate locally as fallback
    const saturnSign = Math.floor(saturnLongitude / 30);
    const houseFromMoon = ((saturnSign - natalMoonSign + 12) % 12) + 1;
    
    if (houseFromMoon === 12) {
      return { isActive: true, phase: 'rising', intensity: 'Light' };
    } else if (houseFromMoon === 1) {
      return { isActive: true, phase: 'peak', intensity: 'Heavy' };
    } else if (houseFromMoon === 2) {
      return { isActive: true, phase: 'setting', intensity: 'Medium' };
    }
    return { isActive: false, phase: null, intensity: 'None' };
  }
}
