/**
 * Dosha Detection System
 * Doshas are afflictions in the birth chart that create challenges
 * Based on: Traditional Vedic Astrology texts
 */

export interface Dosha {
  name: string;
  severity: 'mild' | 'moderate' | 'severe';
  description: string;
  effects: string;
  remedies: string[];
}

/**
 * Detect doshas in a birth chart
 */
export function detectDoshas(chartData: any): Dosha[] {
  const doshas: Dosha[] = [];
  
  if (!chartData?.planetary_positions || !chartData?.houses) {
    return doshas;
  }

  const planets = chartData.planetary_positions;
  
  const getPlanetHouse = (planetName: string): number => {
    return planets[planetName]?.house || 0;
  };

  const getPlanetSign = (planetName: string): number => {
    return planets[planetName]?.sign_num || 0;
  };

  // 1. Mangal Dosha (Mars Dosha / Kuja Dosha)
  const marsHouse = getPlanetHouse('Mars');
  const mangalDoshaHouses = [1, 2, 4, 7, 8, 12];
  
  if (mangalDoshaHouses.includes(marsHouse)) {
    const severity = [1, 7, 8].includes(marsHouse) ? 'severe' : 
                     [2, 12].includes(marsHouse) ? 'moderate' : 'mild';
    
    doshas.push({
      name: 'Mangal Dosha (Kuja Dosha)',
      severity,
      description: `Mars in ${marsHouse}${marsHouse === 1 ? 'st' : marsHouse === 2 ? 'nd' : marsHouse === 3 ? 'rd' : 'th'} house creates Manglik condition`,
      effects: 'May cause delays or challenges in marriage, potential for conflicts in relationships. Can affect marital harmony and partner\'s health. Strong will and aggressive nature in personal matters.',
      remedies: [
        'Marry another Manglik person (dosha cancels out)',
        'Perform Kuja Shanti puja',
        'Fast on Tuesdays',
        'Chant Mars mantras (Om Angarakaya Namaha)',
        'Donate red lentils, red clothes on Tuesdays',
        'Visit Hanuman temple on Tuesdays',
        'Wear red coral (Moonga) gemstone after consultation'
      ]
    });
  }

  // 2. Kala Sarpa Dosha (Serpent Time Dosha)
  const rahuHouse = getPlanetHouse('Rahu');
  const ketuHouse = getPlanetHouse('Ketu');
  
  // Check if all planets are hemmed between Rahu and Ketu
  if (rahuHouse && ketuHouse) {
    const allPlanetsInBetween = ['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn']
      .every(planet => {
        const house = getPlanetHouse(planet);
        const rahuToKetu = rahuHouse < ketuHouse;
        if (rahuToKetu) {
          return house > rahuHouse && house < ketuHouse;
        } else {
          return house > rahuHouse || house < ketuHouse;
        }
      });

    if (allPlanetsInBetween) {
      doshas.push({
        name: 'Kala Sarpa Dosha',
        severity: 'severe',
        description: 'All planets hemmed between Rahu and Ketu axis',
        effects: 'Obstacles and delays in life, mental anxiety, disturbed sleep with snake dreams. Sudden ups and downs. Success comes after struggle. May affect family peace and progress.',
        remedies: [
          'Perform Kala Sarpa Dosha Nivaran puja',
          'Visit Srikalahasti temple (Andhra Pradesh) or Kukke Subramanya (Karnataka)',
          'Chant Rahu-Ketu mantras',
          'Feed birds and animals regularly',
          'Donate to snake-related causes',
          'Perform Naga Pratishtha puja',
          'Observe Nag Panchami fasting'
        ]
      });
    }
  }

  // 3. Pitra Dosha (Ancestral Affliction)
  const sun9th = getPlanetHouse('Sun') === 9;
  const saturn9th = getPlanetHouse('Saturn') === 9;
  const rahu9th = getPlanetHouse('Rahu') === 9;
  
  if (sun9th || saturn9th || rahu9th) {
    doshas.push({
      name: 'Pitra Dosha',
      severity: rahu9th ? 'severe' : saturn9th ? 'moderate' : 'mild',
      description: 'Affliction to 9th house (house of father and ancestors)',
      effects: 'Issues related to father, ancestors not at peace. Obstacles in progeny, delayed marriage. Financial difficulties. Need to clear ancestral karmic debts.',
      remedies: [
        'Perform Pitra Dosha Nivaran puja',
        'Perform Shraddha rituals sincerely',
        'Feed Brahmins on Amavasya (New Moon)',
        'Donate to orphanages and old-age homes',
        'Plant Peepal tree and water it regularly',
        'Chant Pitra Gayatri mantra',
        'Offer water to Peepal tree on Saturdays',
        'Feed crows (considered ancestors\' representatives)'
      ]
    });
  }

  // 4. Grahan Dosha (Eclipse Dosha)
  const sunSign = getPlanetSign('Sun');
  const moonSign = getPlanetSign('Moon');
  const rahuSign = getPlanetSign('Rahu');
  const ketuSign = getPlanetSign('Ketu');

  if ((sunSign === rahuSign || sunSign === ketuSign) || (moonSign === rahuSign || moonSign === ketuSign)) {
    doshas.push({
      name: 'Grahan Dosha (Eclipse Dosha)',
      severity: 'moderate',
      description: 'Sun or Moon conjunct with Rahu/Ketu (eclipse condition)',
      effects: 'Mental confusion, health issues, relationship challenges. Lack of clarity in decision-making. Issues with parents or authority figures.',
      remedies: [
        'Chant Surya or Chandra mantras daily',
        'Donate during eclipses',
        'Perform Grahan Dosha Shanti puja',
        'Worship Lord Shiva regularly',
        'Offer water to Sun at sunrise',
        'Donate white items for Moon affliction, copper for Sun'
      ]
    });
  }

  // 5. Shrapit Dosha (Cursed Combination)
  const saturnSign = getPlanetSign('Saturn');
  if (saturnSign === rahuSign) {
    doshas.push({
      name: 'Shrapit Dosha',
      severity: 'severe',
      description: 'Saturn and Rahu together (cursed yoga)',
      effects: 'Indicates curse from previous life. Multiple obstacles, delays in all matters. Mental stress and sudden setbacks. Need for spiritual remedies.',
      remedies: [
        'Perform Shrapit Dosha Nivaran puja',
        'Visit Shani temples on Saturdays',
        'Chant Hanuman Chalisa daily',
        'Donate black items on Saturdays',
        'Help the needy and disabled',
        'Practice patience and karma yoga'
      ]
    });
  }

  // 6. Kemdrum Dosha (Lunar Affliction)
  // Already checked in yogas, but adding here for completeness
  const moonHouse = getPlanetHouse('Moon');
  const moonHasNeighbors = Object.values(planets).some((p: any) => {
    const diff = Math.abs(p.house - moonHouse);
    return diff === 1 && p.house !== moonHouse;
  });
  
  if (!moonHasNeighbors && moonHouse > 0) {
    doshas.push({
      name: 'Kemdrum Dosha',
      severity: 'moderate',
      description: 'Moon isolated without planets on either side',
      effects: 'Lack of mental peace, financial struggles, lack of support from others. Emotional isolation and poverty yoga.',
      remedies: [
        'Worship Lord Shiva and Goddess Parvati',
        'Chant Moon mantras (Om Chandraya Namaha)',
        'Donate white items on Mondays',
        'Wear Pearl gemstone after consultation',
        'Practice meditation for mental peace',
        'Strengthen Moon through charity and kindness'
      ]
    });
  }

  // 7. Nadi Dosha (For Marriage Compatibility)
  // This would need partner's chart, but we can note if Moon is in certain nakshatras
  doshas.push({
    name: 'Nadi Dosha (Marriage Compatibility Check Needed)',
    severity: 'mild',
    description: 'Affects marriage compatibility when both partners have same Nadi',
    effects: 'Can cause health issues, progeny problems, or lack of harmony if present in marriage matching.',
    remedies: [
      'Perform Nadi Dosha Nivaran puja before marriage',
      'Check with astrologer for severity level',
      'Perform compatibility rituals',
      'Some exceptions may cancel this dosha'
    ]
  });

  return doshas;
}

/**
 * Calculate overall dosha severity score
 */
export function calculateDoshaScore(doshas: Dosha[]): {
  score: number; // 0-100, where 0 is worst, 100 is best
  level: 'excellent' | 'good' | 'moderate' | 'challenging' | 'severe';
} {
  if (doshas.length === 0) {
    return { score: 100, level: 'excellent' };
  }

  const severityPoints = { mild: 10, moderate: 20, severe: 35 };
  const totalDeduction = doshas.reduce((sum, dosha) => sum + severityPoints[dosha.severity], 0);
  const score = Math.max(0, 100 - totalDeduction);

  let level: 'excellent' | 'good' | 'moderate' | 'challenging' | 'severe';
  if (score >= 80) level = 'excellent';
  else if (score >= 60) level = 'good';
  else if (score >= 40) level = 'moderate';
  else if (score >= 20) level = 'challenging';
  else level = 'severe';

  return { score, level };
}
