/**
 * Planetary Strength Calculations (Shadbala System)
 * Based on: BPHS (Brihat Parashara Hora Shastra), Sarvartha Chintamani
 * 
 * Shadbala = Six-fold strength system
 * 1. Sthana Bala (Positional Strength)
 * 2. Dig Bala (Directional Strength)
 * 3. Kala Bala (Temporal Strength)
 * 4. Chesta Bala (Motional Strength)
 * 5. Naisargika Bala (Natural Strength)
 * 6. Drik Bala (Aspectual Strength)
 */

export interface PlanetaryStrength {
  planet: string;
  totalStrength: number; // in Rupas
  percentage: number;
  strength: 'Very Weak' | 'Weak' | 'Average' | 'Strong' | 'Very Strong';
  details: {
    sthanaBala: number;
    digBala: number;
    kalaBala: number;
    chestaBala: number;
    naisargikaBala: number;
    drikBala: number;
  };
  minimumRequired: number;
  interpretation: string;
}

export interface SpecialPoints {
  brighaBindu: {
    longitude: number;
    sign: string;
    signNum: number;
    house: number;
    description: string;
  };
  gulika: {
    longitude: number;
    sign: string;
    signNum: number;
    house: number;
    description: string;
  };
  mandi: {
    longitude: number;
    sign: string;
    signNum: number;
    house: number;
    description: string;
  };
  bhavaLagna: {
    longitude: number;
    sign: string;
    signNum: number;
    description: string;
  };
  horaLagna: {
    longitude: number;
    sign: string;
    signNum: number;
    description: string;
  };
}

const ZODIAC_SIGNS = [
  'Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo',
  'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces'
];

// Minimum required strength for each planet (in Rupas)
const MINIMUM_STRENGTH = {
  Sun: 390,
  Moon: 360,
  Mars: 300,
  Mercury: 420,
  Jupiter: 390,
  Venus: 330,
  Saturn: 300
};

// Natural strength values
const NAISARGIKA_VALUES = {
  Sun: 60,
  Moon: 51.43,
  Mars: 17.14,
  Mercury: 25.70,
  Jupiter: 34.28,
  Venus: 42.85,
  Saturn: 8.57
};

/**
 * Calculate comprehensive planetary strength
 */
export function calculatePlanetaryStrength(chartData: any): PlanetaryStrength[] {
  const strengths: PlanetaryStrength[] = [];
  
  if (!chartData?.planetary_positions || !chartData?.houses) {
    return strengths;
  }

  const planets = ['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn'];
  
  for (const planetName of planets) {
    const planet = chartData.planetary_positions[planetName];
    if (!planet) continue;

    const sthanaBala = calculateSthanaBala(planet, chartData);
    const digBala = calculateDigBala(planet, chartData);
    const kalaBala = calculateKalaBala(planet, chartData);
    const chestaBala = calculateChestaBala(planet);
    const naisargikaBala = NAISARGIKA_VALUES[planetName as keyof typeof NAISARGIKA_VALUES];
    const drikBala = calculateDrikBala(planet, chartData);

    const totalStrength = sthanaBala + digBala + kalaBala + chestaBala + naisargikaBala + drikBala;
    const minRequired = MINIMUM_STRENGTH[planetName as keyof typeof MINIMUM_STRENGTH];
    const percentage = (totalStrength / minRequired) * 100;

    let strength: 'Very Weak' | 'Weak' | 'Average' | 'Strong' | 'Very Strong';
    if (percentage >= 150) strength = 'Very Strong';
    else if (percentage >= 110) strength = 'Strong';
    else if (percentage >= 90) strength = 'Average';
    else if (percentage >= 60) strength = 'Weak';
    else strength = 'Very Weak';

    const interpretation = getStrengthInterpretation(planetName, strength, percentage);

    strengths.push({
      planet: planetName,
      totalStrength,
      percentage,
      strength,
      details: {
        sthanaBala,
        digBala,
        kalaBala,
        chestaBala,
        naisargikaBala,
        drikBala
      },
      minimumRequired: minRequired,
      interpretation
    });
  }

  return strengths;
}

function calculateSthanaBala(planet: any, chartData: any): number {
  // Simplified Sthana Bala calculation
  // Based on: Uchcha Bala (exaltation), Saptavargaja Bala, etc.
  
  let bala = 0;
  const signNum = planet.sign_num;
  
  // Exaltation points
  const exaltationSigns: Record<number, number> = {
    1: 1,   // Sun in Aries
    2: 2,   // Moon in Taurus
    3: 10,  // Mars in Capricorn
    4: 6,   // Mercury in Virgo
    5: 4,   // Jupiter in Cancer
    6: 12,  // Venus in Pisces
    7: 7    // Saturn in Libra
  };

  // Debilitation points
  const debilitationSigns: Record<number, number> = {
    1: 7,   // Sun in Libra
    2: 8,   // Moon in Scorpio
    3: 4,   // Mars in Cancer
    4: 12,  // Mercury in Pisces
    5: 10,  // Jupiter in Capricorn
    6: 6,   // Venus in Virgo
    7: 1    // Saturn in Aries
  };

  // Get planet number (1-7 for Sun-Saturn)
  const planetNum = ['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn'].indexOf(planet.name) + 1;
  
  if (exaltationSigns[planetNum] === signNum) {
    bala += 60; // Maximum Uchcha Bala
  } else if (debilitationSigns[planetNum] === signNum) {
    bala += 0; // Minimum Uchcha Bala
  } else {
    bala += 30; // Average Uchcha Bala
  }

  // Own sign strength
  const ownSigns: Record<string, number[]> = {
    Sun: [5],
    Moon: [4],
    Mars: [1, 8],
    Mercury: [3, 6],
    Jupiter: [9, 12],
    Venus: [2, 7],
    Saturn: [10, 11]
  };

  if (ownSigns[planet.name]?.includes(signNum)) {
    bala += 30;
  }

  return bala;
}

function calculateDigBala(planet: any, chartData: any): number {
  // Directional strength
  // Sun & Mars: 10th house, Jupiter & Mercury: 1st house
  // Moon & Venus: 4th house, Saturn: 7th house
  
  const house = planet.house || 1;
  const planetName = planet.name;
  
  let maxBala = 60;
  let idealHouse = 1;
  
  if (planetName === 'Sun' || planetName === 'Mars') {
    idealHouse = 10;
  } else if (planetName === 'Jupiter' || planetName === 'Mercury') {
    idealHouse = 1;
  } else if (planetName === 'Moon' || planetName === 'Venus') {
    idealHouse = 4;
  } else if (planetName === 'Saturn') {
    idealHouse = 7;
  }
  
  const diff = Math.abs(house - idealHouse);
  const bala = maxBala - (diff * 10);
  
  return Math.max(0, bala);
}

function calculateKalaBala(planet: any, chartData: any): number {
  // Temporal strength - simplified
  // Includes Nathonnatha Bala, Paksha Bala, Tribhaga Bala, etc.
  
  let bala = 30; // Base temporal strength
  
  // Day/Night strength
  const isNocturnal = ['Moon', 'Mars', 'Saturn'].includes(planet.name);
  // Assuming daytime for simplification
  if (!isNocturnal) {
    bala += 15;
  }
  
  return bala;
}

function calculateChestaBala(planet: any): number {
  // Motional strength
  // Based on retrograde motion, speed, etc.
  
  let bala = 30; // Base motional strength
  
  // Retrograde planets have special chesta bala
  if (planet.is_retrograde) {
    bala += 30;
  }
  
  // Speed consideration (simplified)
  const speed = Math.abs(planet.speed || 0);
  if (speed > 0.5) {
    bala += 15;
  }
  
  return Math.min(60, bala); // Max 60
}

function calculateDrikBala(planet: any, chartData: any): number {
  // Aspectual strength - simplified
  // Based on aspects from benefics and malefics
  
  let bala = 0;
  
  // Base drik bala
  bala = 20;
  
  // Add more based on aspects (would need complex calculation)
  // Simplified version
  
  return bala;
}

function getStrengthInterpretation(planet: string, strength: string, percentage: number): string {
  const interpretations: Record<string, Record<string, string>> = {
    Sun: {
      'Very Strong': 'Excellent vitality, strong father figure, authority, and self-confidence. Leadership abilities shine.',
      'Strong': 'Good health, confidence, and recognition. Positive relationship with father and authority.',
      'Average': 'Moderate vitality and confidence. Balanced ego and self-expression.',
      'Weak': 'Reduced confidence, health issues possible. Father relationship may be challenging.',
      'Very Weak': 'Low vitality, weak ego, health problems. Struggles with authority and recognition.'
    },
    Moon: {
      'Very Strong': 'Excellent mental strength, emotional stability, good memory. Strong mother bond.',
      'Strong': 'Good emotional health, intuition, and mental peace. Positive mind and relationships.',
      'Average': 'Balanced emotions and mental state. Moderate intuition and memory.',
      'Weak': 'Emotional instability, weak mind, memory issues. Mother relationship challenges.',
      'Very Weak': 'Mental anxiety, emotional disorders, poor memory. Weak mother bond.'
    },
    Mars: {
      'Very Strong': 'Excellent courage, energy, and drive. Strong willpower and athletic abilities.',
      'Strong': 'Good courage, determination, and physical strength. Ability to overcome obstacles.',
      'Average': 'Moderate energy and courage. Balanced assertiveness.',
      'Weak': 'Low energy, weak courage, lack of drive. Accidents prone.',
      'Very Weak': 'Cowardice, low vitality, chronic weakness. Blood-related disorders possible.'
    },
    Mercury: {
      'Very Strong': 'Brilliant intellect, excellent communication, business acumen. Quick learner.',
      'Strong': 'Good intelligence, analytical skills, effective communication. Business success.',
      'Average': 'Moderate intellect and communication abilities. Balanced reasoning.',
      'Weak': 'Poor communication, weak intellect, learning difficulties. Speech problems.',
      'Very Weak': 'Mental disorders, severe speech problems, learning disabilities. Poor business sense.'
    },
    Jupiter: {
      'Very Strong': 'Excellent wisdom, spiritual knowledge, prosperity. Great teacher and guide.',
      'Strong': 'Good wisdom, ethical values, children, and prosperity. Spiritual growth.',
      'Average': 'Moderate wisdom and prosperity. Balanced spiritual interests.',
      'Weak': 'Lack of wisdom, financial issues, children problems. Weak dharma.',
      'Very Weak': 'Ignorance, severe financial problems, childlessness possible. Lack of grace.'
    },
    Venus: {
      'Very Strong': 'Excellent artistic talents, luxury, beautiful spouse. Strong romantic life.',
      'Strong': 'Good relationships, comforts, arts, and beauty. Happy married life.',
      'Average': 'Moderate comforts and relationships. Balanced sensual nature.',
      'Weak': 'Relationship problems, lack of comforts, poor artistic sense. Marital issues.',
      'Very Weak': 'Severe relationship problems, poverty, lack of beauty. Marital discord.'
    },
    Saturn: {
      'Very Strong': 'Excellent discipline, patience, longevity. Success through hard work.',
      'Strong': 'Good discipline, responsibility, and practical wisdom. Career stability.',
      'Average': 'Moderate discipline and patience. Balanced karma and lessons.',
      'Weak': 'Lack of discipline, delays, obstacles. Chronic problems and fears.',
      'Very Weak': 'Severe obstacles, chronic diseases, extreme delays. Karmic suffering.'
    }
  };

  return interpretations[planet]?.[strength] || 'Planetary strength affects overall life results.';
}

/**
 * Calculate special points in the chart
 */
export function calculateSpecialPoints(chartData: any): SpecialPoints {
  const ascendant = chartData?.houses?.ascendant?.longitude || 0;
  const moon = chartData?.planetary_positions?.Moon?.longitude || 0;
  const sun = chartData?.planetary_positions?.Sun?.longitude || 0;
  
  // Brighu Bindu (Destiny Point)
  // Calculated as: (Rahu longitude + Moon longitude) / 2
  const rahu = chartData?.planetary_positions?.Rahu?.longitude || 0;
  const brighaBinduLong = ((rahu + moon) / 2) % 360;
  
  // Gulika (Son of Saturn - Malefic point)
  // Simplified calculation based on day of week and ascendant
  // In actual practice, calculated from sunrise time
  const gulikaLong = (ascendant + 120) % 360;
  
  // Mandi (Another son of Saturn)
  // Similar to Gulika but different calculation
  const mandiLong = (ascendant + 240) % 360;
  
  // Bhava Lagna (House  Cusp Ascendant)
  const bhavaLagnaLong = (ascendant + sun - moon + 360) % 360;
  
  // Hora Lagna (Wealth Point)
  const horaLagnaLong = (ascendant + (sun - moon) / 2 + 360) % 360;

  return {
    brighaBindu: {
      longitude: brighaBinduLong,
      sign: ZODIAC_SIGNS[Math.floor(brighaBinduLong / 30)],
      signNum: Math.floor(brighaBinduLong / 30) + 1,
      house: calculateHouseFromLongitude(brighaBinduLong, ascendant),
      description: 'Destiny Point (Brighu Bindu) - Shows karmic destiny, important life events, and key turning points. Strong influence on life path and major decisions.'
    },
    gulika: {
      longitude: gulikaLong,
      sign: ZODIAC_SIGNS[Math.floor(gulikaLong / 30)],
      signNum: Math.floor(gulikaLong / 30) + 1,
      house: calculateHouseFromLongitude(gulikaLong, ascendant),
      description: 'Gulika (Son of Saturn) - Malefic point indicating obstacles, delays, and karmic debts. Shows areas of life requiring patience and hard work.'
    },
    mandi: {
      longitude: mandiLong,
      sign: ZODIAC_SIGNS[Math.floor(mandiLong / 30)],
      signNum: Math.floor(mandiLong / 30) + 1,
      house: calculateHouseFromLongitude(mandiLong, ascendant),
      description: 'Mandi (Saturn\'s agent) - Another malefic point indicating chronic issues, fears, and restrictions. Shows areas requiring discipline and perseverance.'
    },
    bhavaLagna: {
      longitude: bhavaLagnaLong,
      sign: ZODIAC_SIGNS[Math.floor(bhavaLagnaLong / 30)],
      signNum: Math.floor(bhavaLagnaLong / 30) + 1,
      description: 'Bhava Lagna (House Ascendant) - Shows physical body strength and overall vitality. Important for health and longevity analysis.'
    },
    horaLagna: {
      longitude: horaLagnaLong,
      sign: ZODIAC_SIGNS[Math.floor(horaLagnaLong / 30)],
      signNum: Math.floor(horaLagnaLong / 30) + 1,
      description: 'Hora Lagna (Wealth Point) - Indicates wealth potential, financial gains, and material prosperity. Important for financial analysis.'
    }
  };
}

function calculateHouseFromLongitude(longitude: number, ascendant: number): number {
  const diff = ((longitude - ascendant + 360) % 360);
  return Math.floor(diff / 30) + 1;
}

/**
 * Get overall chart strength summary
 */
export function getChartStrengthSummary(strengths: PlanetaryStrength[]): {
  averageStrength: number;
  strongestPlanet: string;
  weakestPlanet: string;
  overallRating: string;
  recommendations: string[];
} {
  if (strengths.length === 0) {
    return {
      averageStrength: 0,
      strongestPlanet: 'None',
      weakestPlanet: 'None',
      overallRating: 'Unknown',
      recommendations: []
    };
  }

  const avgPercentage = strengths.reduce((sum, s) => sum + s.percentage, 0) / strengths.length;
  
  const sorted = [...strengths].sort((a, b) => b.percentage - a.percentage);
  const strongestPlanet = sorted[0].planet;
  const weakestPlanet = sorted[sorted.length - 1].planet;

  let overallRating: string;
  if (avgPercentage >= 120) overallRating = 'Excellent';
  else if (avgPercentage >= 100) overallRating = 'Very Good';
  else if (avgPercentage >= 85) overallRating = 'Good';
  else if (avgPercentage >= 70) overallRating = 'Average';
  else overallRating = 'Weak';

  const recommendations: string[] = [];
  
  const weakPlanets = strengths.filter(s => s.strength === 'Weak' || s.strength === 'Very Weak');
  weakPlanets.forEach(p => {
    recommendations.push(`Strengthen ${p.planet} through gemstones, mantras, and charitable actions.`);
  });

  if (recommendations.length === 0) {
    recommendations.push('Overall planetary strength is good. Maintain spiritual practices.');
  }

  return {
    averageStrength: avgPercentage,
    strongestPlanet,
    weakestPlanet,
    overallRating,
    recommendations
  };
}
