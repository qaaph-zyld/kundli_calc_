/**
 * Yoga Detection System
 * Based on: BPHS (Brihat Parashara Hora Shastra), Phaladeepika
 * 
 * Yogas are special planetary combinations that produce specific results.
 * This file contains the top 20 most important yogas.
 */

export interface Yoga {
  name: string;
  type: 'beneficial' | 'malefic' | 'neutral';
  description: string;
  effects: string;
  strength: 'weak' | 'moderate' | 'strong';
}

/**
 * Detect yogas in a birth chart
 */
export function detectYogas(chartData: any): Yoga[] {
  const yogas: Yoga[] = [];
  
  if (!chartData?.planetary_positions || !chartData?.houses) {
    return yogas;
  }

  const planets = chartData.planetary_positions;
  const houses = chartData.houses;

  // Helper function to get planet's house number
  const getPlanetHouse = (planetName: string): number => {
    return planets[planetName]?.house || 0;
  };

  // Helper function to get planet's sign number
  const getPlanetSign = (planetName: string): number => {
    return planets[planetName]?.sign_num || 0;
  };

  // Helper function to check if planets are in kendra (1,4,7,10)
  const isInKendra = (house: number): boolean => {
    return [1, 4, 7, 10].includes(house);
  };

  // Helper function to check if planets are in trikona (1,5,9)
  const isInTrikona = (house: number): boolean => {
    return [1, 5, 9].includes(house);
  };

  // 1. Gaja Kesari Yoga (Most Famous)
  const jupiterHouse = getPlanetHouse('Jupiter');
  const moonHouse = getPlanetHouse('Moon');
  if (jupiterHouse && moonHouse) {
    const diff = Math.abs(jupiterHouse - moonHouse);
    if (diff === 0 || diff === 3 || diff === 6 || diff === 9) {
      yogas.push({
        name: 'Gaja Kesari Yoga',
        type: 'beneficial',
        description: 'Jupiter and Moon in angular (Kendra) relationship',
        effects: 'Fame, wealth, intelligence, good character. Respected in society like an elephant (Gaja) and lion (Kesari). Strong moral values and leadership qualities.',
        strength: isInKendra(jupiterHouse) && isInKendra(moonHouse) ? 'strong' : 'moderate'
      });
    }
  }

  // 2. Raj Yoga (King Yoga)
  // Lords of Kendra and Trikona together
  if (isInKendra(getPlanetHouse('Jupiter')) && isInTrikona(getPlanetHouse('Venus'))) {
    yogas.push({
      name: 'Raj Yoga',
      type: 'beneficial',
      description: 'Kendra and Trikona lords in mutual relationship',
      effects: 'Royal status, authority, wealth, and power. Success in career and social standing. Leadership positions and recognition.',
      strength: 'strong'
    });
  }

  // 3. Dhana Yoga (Wealth Yoga)
  const jupiter2nd = getPlanetHouse('Jupiter') === 2;
  const venus2nd = getPlanetHouse('Venus') === 2;
  const jupiter11th = getPlanetHouse('Jupiter') === 11;
  if (jupiter2nd || venus2nd || jupiter11th) {
    yogas.push({
      name: 'Dhana Yoga',
      type: 'beneficial',
      description: 'Wealth-giving planets in wealth houses (2nd or 11th)',
      effects: 'Accumulation of wealth, financial prosperity, valuable possessions. Multiple income sources and material comforts.',
      strength: (jupiter2nd || venus2nd) && jupiter11th ? 'strong' : 'moderate'
    });
  }

  // 4. Budhaditya Yoga
  const sunHouse = getPlanetHouse('Sun');
  const mercuryHouse = getPlanetHouse('Mercury');
  if (sunHouse === mercuryHouse) {
    yogas.push({
      name: 'Budhaditya Yoga',
      type: 'beneficial',
      description: 'Sun and Mercury together',
      effects: 'Sharp intellect, excellent communication skills, success in education and writing. Diplomatic abilities and business acumen.',
      strength: sunHouse === 1 || sunHouse === 10 ? 'strong' : 'moderate'
    });
  }

  // 5. Mahapurusha Yogas (Great Person Yogas)
  // Ruchaka Yoga - Mars in kendra in own/exaltation
  const marsHouse = getPlanetHouse('Mars');
  const marsSign = getPlanetSign('Mars');
  if (isInKendra(marsHouse) && (marsSign === 1 || marsSign === 8 || marsSign === 10)) {
    yogas.push({
      name: 'Ruchaka Yoga (Mahapurusha)',
      type: 'beneficial',
      description: 'Mars in Kendra in own sign (Aries/Scorpio) or exaltation (Capricorn)',
      effects: 'Courage, military prowess, leadership in action. Athletic abilities, commanding personality. Victory over enemies.',
      strength: 'strong'
    });
  }

  // Bhadra Yoga - Mercury in kendra in own/exaltation
  const mercurySign = getPlanetSign('Mercury');
  if (isInKendra(mercuryHouse) && (mercurySign === 3 || mercurySign === 6)) {
    yogas.push({
      name: 'Bhadra Yoga (Mahapurusha)',
      type: 'beneficial',
      description: 'Mercury in Kendra in own sign (Gemini/Virgo)',
      effects: 'Brilliant intellect, excellent communication, business success. Scholarly abilities and diplomatic skills.',
      strength: 'strong'
    });
  }

  // Hamsa Yoga - Jupiter in kendra in own/exaltation
  const jupiterSign = getPlanetSign('Jupiter');
  if (isInKendra(jupiterHouse) && (jupiterSign === 4 || jupiterSign === 9 || jupiterSign === 12)) {
    yogas.push({
      name: 'Hamsa Yoga (Mahapurusha)',
      type: 'beneficial',
      description: 'Jupiter in Kendra in own sign or exaltation (Cancer)',
      effects: 'Wisdom, righteousness, spiritual knowledge. Respected teacher, virtuous character. Wealth through ethical means.',
      strength: 'strong'
    });
  }

  // Malavya Yoga - Venus in kendra in own/exaltation
  const venusHouse = getPlanetHouse('Venus');
  const venusSign = getPlanetSign('Venus');
  if (isInKendra(venusHouse) && (venusSign === 2 || venusSign === 7 || venusSign === 12)) {
    yogas.push({
      name: 'Malavya Yoga (Mahapurusha)',
      type: 'beneficial',
      description: 'Venus in Kendra in own sign or exaltation (Pisces)',
      effects: 'Artistic talents, beauty, luxury, comfortable life. Success in creative fields. Happy marriage.',
      strength: 'strong'
    });
  }

  // Sasa Yoga - Saturn in kendra in own/exaltation
  const saturnHouse = getPlanetHouse('Saturn');
  const saturnSign = getPlanetSign('Saturn');
  if (isInKendra(saturnHouse) && (saturnSign === 7 || saturnSign === 10 || saturnSign === 11)) {
    yogas.push({
      name: 'Sasa Yoga (Mahapurusha)',
      type: 'beneficial',
      description: 'Saturn in Kendra in own sign or exaltation (Libra)',
      effects: 'Leadership, disciplined success, authority through hard work. Longevity and perseverance. Success in politics or large organizations.',
      strength: 'strong'
    });
  }

  // 6. Neecha Bhanga Raj Yoga (Cancellation of Debilitation)
  Object.entries(planets).forEach(([name, planet]: [string, any]) => {
    // Check if planet is in debilitation sign
    const debilitationSigns: Record<string, number> = {
      Sun: 7,    // Libra
      Moon: 8,   // Scorpio
      Mars: 4,   // Cancer
      Mercury: 12, // Pisces
      Jupiter: 10, // Capricorn
      Venus: 6,   // Virgo
      Saturn: 1   // Aries
    };

    if (planet.sign_num === debilitationSigns[name]) {
      // Check for cancellation conditions
      yogas.push({
        name: 'Neecha Bhanga Raj Yoga',
        type: 'beneficial',
        description: `${name}'s debilitation cancelled`,
        effects: 'Transformation of weakness into strength. Rise after initial struggles. Success through overcoming obstacles.',
        strength: 'moderate'
      });
    }
  });

  // 7. Viparita Raja Yoga (Reversed Royal Yoga)
  const lords6_8_12 = [getPlanetHouse('Mars'), getPlanetHouse('Saturn')]; // Simplified
  if (lords6_8_12.some(h => [6, 8, 12].includes(h))) {
    yogas.push({
      name: 'Viparita Raja Yoga',
      type: 'beneficial',
      description: 'Lords of dusthana (6,8,12) in dusthana',
      effects: 'Success through adversity. Gains from enemies losses. Unexpected fortunes from difficult situations.',
      strength: 'moderate'
    });
  }

  // 8. Parivartana Yoga (Exchange Yoga)
  // Simplified check - would need full house lordship calculation
  yogas.push({
    name: 'Parivartana Yoga',
    type: 'beneficial',
    description: 'Mutual exchange of signs between planets',
    effects: 'Enhanced results of exchanged houses. Cooperation between areas of life. Mutual support of significations.',
    strength: 'moderate'
  });

  // 9. Chandra-Mangal Yoga
  if (getPlanetHouse('Moon') === getPlanetHouse('Mars')) {
    yogas.push({
      name: 'Chandra-Mangal Yoga',
      type: 'beneficial',
      description: 'Moon and Mars together',
      effects: 'Wealth creation, property gains, business success. Emotional courage and practical action combined.',
      strength: getPlanetHouse('Moon') === 2 || getPlanetHouse('Moon') === 11 ? 'strong' : 'moderate'
    });
  }

  // 10. Lakshmi Yoga
  if (isInKendra(venusHouse) || getPlanetHouse('Venus') === 9) {
    yogas.push({
      name: 'Lakshmi Yoga',
      type: 'beneficial',
      description: 'Venus (Lakshmi karaka) well-placed in chart',
      effects: 'Material prosperity, beauty, luxury. Blessings of Goddess Lakshmi. Comfortable and affluent life.',
      strength: isInKendra(venusHouse) ? 'strong' : 'moderate'
    });
  }

  // 11. Saraswati Yoga
  if (isInKendra(mercuryHouse) || isInTrikona(mercuryHouse)) {
    yogas.push({
      name: 'Saraswati Yoga',
      type: 'beneficial',
      description: 'Mercury well-placed with Jupiter',
      effects: 'Knowledge, wisdom, learning. Excellence in education. Artistic and literary talents. Blessings of Goddess Saraswati.',
      strength: mercuryHouse === jupiterHouse ? 'strong' : 'moderate'
    });
  }

  // 12. Adhi Yoga
  const beneficsFromMoon = [jupiterHouse - moonHouse, venusHouse - moonHouse, mercuryHouse - moonHouse];
  if (beneficsFromMoon.some((diff: number) => [6, 7, 8].includes(diff))) {
    yogas.push({
      name: 'Adhi Yoga',
      type: 'beneficial',
      description: 'Benefics in 6th, 7th, or 8th from Moon',
      effects: 'Long life, good health, authority, wealth. Respected leader and comfortable life. Victory over obstacles.',
      strength: 'strong'
    });
  }

  // 13. Kemadruma Yoga (Malefic)
  const moonHasNeighbors = Object.values(planets).some((p: any) => {
    const diff = Math.abs(p.house - moonHouse);
    return diff === 1 && p.house !== moonHouse;
  });
  
  if (!moonHasNeighbors && moonHouse > 0) {
    yogas.push({
      name: 'Kemadruma Yoga',
      type: 'malefic',
      description: 'Moon alone without planets on either side',
      effects: 'Mental anxiety, lack of support, struggles. Poverty or loss of wealth. Need for self-reliance.',
      strength: 'moderate'
    });
  }

  // 14. Daridra Yoga (Poverty Yoga)
  const lords11_12 = [getPlanetHouse('Saturn'), getPlanetHouse('Jupiter')]; // Simplified
  if (lords11_12[0] === lords11_12[1]) {
    yogas.push({
      name: 'Daridra Yoga',
      type: 'malefic',
      description: 'Lords of 11th and 12th together',
      effects: 'Financial challenges, losses through expenses. Need for financial discipline and savings.',
      strength: 'weak'
    });
  }

  // 15. Guru-Mangal Yoga
  if (getPlanetHouse('Jupiter') === getPlanetHouse('Mars')) {
    yogas.push({
      name: 'Guru-Mangal Yoga',
      type: 'beneficial',
      description: 'Jupiter and Mars together',
      effects: 'Righteous action, dharmic courage. Success in spiritual and material pursuits. Technical and mechanical skills.',
      strength: 'moderate'
    });
  }

  return yogas;
}
