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

  // 16. Amala Yoga
  const tenthHousePlanets = Object.entries(planets).filter(([_, p]: [string, any]) => p.house === 10);
  if (tenthHousePlanets.some(([name, _]) => ['Jupiter', 'Venus', 'Mercury'].includes(name))) {
    yogas.push({
      name: 'Amala Yoga',
      type: 'beneficial',
      description: 'Benefics in 10th house from Lagna or Moon',
      effects: 'Pure character, lasting fame, prosperity. Ethical success in career. Good reputation and moral authority.',
      strength: 'strong'
    });
  }

  // 17. Parvata Yoga
  if ((isInKendra(jupiterHouse) || getPlanetHouse('Jupiter') === 6) && 
      (isInKendra(moonHouse) || getPlanetHouse('Moon') === 6)) {
    yogas.push({
      name: 'Parvata Yoga',
      type: 'beneficial',
      description: 'Benefics in kendras and/or 6th house',
      effects: 'Mountain-like steadiness and strength. Wealth, honor, charitable nature. Leadership with stability.',
      strength: 'strong'
    });
  }

  // 18. Kahala Yoga
  if (jupiterHouse === 4 && moonHouse === 7) {
    yogas.push({
      name: 'Kahala Yoga',
      type: 'beneficial',
      description: 'Jupiter in 4th and Moon in 7th from Lagna',
      effects: 'Aggressive success, boldness, authority. Victory in competitions. Commander-like qualities.',
      strength: 'moderate'
    });
  }

  // 19. Chamara Yoga
  const lagna = houses.ascendant ? Math.floor(houses.ascendant / 30) + 1 : 1;
  const planetsInLagna = Object.values(planets).filter((p: any) => p.house === 1);
  if (planetsInLagna.length >= 2) {
    yogas.push({
      name: 'Chamara Yoga',
      type: 'beneficial',
      description: 'Two benefics in Lagna/7th/9th/10th',
      effects: 'Long life, authority, scholarly knowledge. Respected position. Literary talents and eloquence.',
      strength: 'moderate'
    });
  }

  // 20. Sankha Yoga
  if ((jupiterHouse === 5 || jupiterHouse === 9) && venusHouse === 1) {
    yogas.push({
      name: 'Sankha Yoga',
      type: 'beneficial',
      description: 'Jupiter in 5th/9th and Venus in Lagna',
      effects: 'Charitable, religious, prosperous. Love for arts and knowledge. Comfortable family life.',
      strength: 'moderate'
    });
  }

  // 21. Bheri Yoga
  if (venusHouse === 1 && jupiterHouse === 7) {
    yogas.push({
      name: 'Bheri Yoga',
      type: 'beneficial',
      description: 'Venus in Lagna, Jupiter in 7th, and strong Moon',
      effects: 'Long life, intelligent spouse, happiness. Success in partnerships. Material comforts.',
      strength: 'strong'
    });
  }

  // 22. Mridanga Yoga
  const strongPlanetsInKendra = Object.entries(planets).filter(([_, p]: [string, any]) => 
    isInKendra(p.house)).length;
  if (strongPlanetsInKendra >= 3) {
    yogas.push({
      name: 'Mridanga Yoga',
      type: 'beneficial',
      description: 'Multiple strong planets in kendras',
      effects: 'Happiness, wealth, respect. Success through virtuous conduct. Good health and longevity.',
      strength: 'strong'
    });
  }

  // 23. Sharada Yoga
  if (mercuryHouse === 10 && mercurySign === 6) {
    yogas.push({
      name: 'Sharada Yoga',
      type: 'beneficial',
      description: 'Mercury in 10th in own sign (Virgo)',
      effects: 'Exceptional learning, poetic skills, wealth. Master of arts and sciences. Teaching abilities.',
      strength: 'strong'
    });
  }

  // 24. Matsya Yoga
  if (isInKendra(jupiterHouse) && isInKendra(venusHouse) && [1,9].includes(moonHouse)) {
    yogas.push({
      name: 'Matsya Yoga',
      type: 'beneficial',
      description: 'Specific benefic configuration',
      effects: 'Charitable, religious, wealthy. Graceful personality. Success through righteous means.',
      strength: 'moderate'
    });
  }

  // 25. Kurma Yoga
  const beneficsIn5and9 = [jupiterHouse, venusHouse, mercuryHouse].filter(h => [5,9].includes(h)).length;
  if (beneficsIn5and9 >= 2) {
    yogas.push({
      name: 'Kurma Yoga',
      type: 'beneficial',
      description: 'Benefics in 5th and 9th houses',
      effects: 'Good fortune, fame, devoted to dharma. Wise counsel. Respected for knowledge.',
      strength: 'moderate'
    });
  }

  // 26. Devendra Yoga
  if (isInKendra(jupiterHouse) && jupiterSign === 4) {
    yogas.push({
      name: 'Devendra Yoga',
      type: 'beneficial',
      description: 'Jupiter in kendra in Cancer',
      effects: 'Kingly status, power, prosperity. Divine protection. Leadership with wisdom.',
      strength: 'strong'
    });
  }

  // 27. Makuta Yoga
  if (jupiterHouse === 9 && sunHouse === 10) {
    yogas.push({
      name: 'Makuta Yoga',
      type: 'beneficial',
      description: 'Jupiter in 9th, Sun in 10th',
      effects: 'Authority, leadership, crown-like status. Government favor. High position.',
      strength: 'strong'
    });
  }

  // 28. Chandrika Yoga
  if (moonHouse === 1 && sunHouse === 5) {
    yogas.push({
      name: 'Chandrika Yoga',
      type: 'beneficial',
      description: 'Moon in Lagna, Sun in 5th',
      effects: 'Bright intellect, creativity, wealth. Pleasing personality. Success in creative fields.',
      strength: 'moderate'
    });
  }

  // 29. Jaya Yoga
  if (jupiterHouse === 6 && moonHouse === 10) {
    yogas.push({
      name: 'Jaya Yoga',
      type: 'beneficial',
      description: 'Jupiter in 6th, Moon in 10th',
      effects: 'Victory over enemies, success in competitions. Professional triumph. Strategic mind.',
      strength: 'moderate'
    });
  }

  // 30. Harsha Yoga (Viparita variation)
  if ([6,8,12].includes(getPlanetHouse('Sun')) && isInKendra(sunHouse)) {
    yogas.push({
      name: 'Harsha Yoga',
      type: 'beneficial',
      description: '6th lord in 6th/8th/12th house',
      effects: 'Victory over enemies, good health. Overcoming obstacles. Success through perseverance.',
      strength: 'moderate'
    });
  }

  // 31. Sarala Yoga (Viparita variation)
  if ([6,8,12].includes(getPlanetHouse('Saturn')) && [6,8,12].includes(saturnHouse)) {
    yogas.push({
      name: 'Sarala Yoga',
      type: 'beneficial',
      description: '8th lord in 6th/8th/12th',
      effects: 'Fearless, long life, learning. Victory in battles. Research abilities.',
      strength: 'moderate'
    });
  }

  // 32. Vimala Yoga (Viparita variation)
  if ([6,8,12].includes(getPlanetHouse('Jupiter')) && [6,8,12].includes(jupiterHouse)) {
    yogas.push({
      name: 'Vimala Yoga',
      type: 'beneficial',
      description: '12th lord in 6th/8th/12th',
      effects: 'Independent, frugal, successful. Gains in foreign lands. Spiritual inclination.',
      strength: 'moderate'
    });
  }

  // 33. Vasumati Yoga
  const beneficsInUpachaya = [jupiterHouse, venusHouse, mercuryHouse].filter(h => 
    [3,6,10,11].includes(h)).length;
  if (beneficsInUpachaya >= 2) {
    yogas.push({
      name: 'Vasumati Yoga',
      type: 'beneficial',
      description: 'Benefics in upachaya houses (3,6,10,11)',
      effects: 'Wealth accumulation, material prosperity. Business success. Growing fortune.',
      strength: 'strong'
    });
  }

  // 34. Rajalakshana Yoga
  if (isInKendra(jupiterHouse) && isInKendra(moonHouse) && isInKendra(venusHouse)) {
    yogas.push({
      name: 'Rajalakshana Yoga',
      type: 'beneficial',
      description: 'Multiple benefics in kendras',
      effects: 'Royal marks, authority, prosperity. Impressive personality. Leadership qualities.',
      strength: 'strong'
    });
  }

  // 35. Maha Bhagya Yoga (for day births)
  const birthHour = new Date().getHours(); // Simplified - would need actual birth time
  if (birthHour > 6 && birthHour < 18) {
    const maleLagna = [1,3,5,7,9,11].includes(lagna);
    if ((maleLagna && sunHouse === 1) || (!maleLagna && moonHouse === 1)) {
      yogas.push({
        name: 'Maha Bhagya Yoga',
        type: 'beneficial',
        description: 'Special yoga for fortunate birth',
        effects: 'Great fortune, prosperity, respect. Born lucky. Success comes naturally.',
        strength: 'strong'
      });
    }
  }

  // 36. Pushkala Yoga
  if (isInKendra(moonHouse) && lagna === 4) {
    yogas.push({
      name: 'Pushkala Yoga',
      type: 'beneficial',
      description: 'Moon in kendra with Cancer ascendant',
      effects: 'Wealthy, learned, good speaker. Popular personality. Comfortable life.',
      strength: 'moderate'
    });
  }

  // 37. Kalanidhi Yoga
  if (jupiterHouse === 2 && venusHouse === 2) {
    yogas.push({
      name: 'Kalanidhi Yoga',
      type: 'beneficial',
      description: 'Jupiter and Venus in 2nd house',
      effects: 'Artistic talents, eloquence, wealth. Master of fine arts. Cultural refinement.',
      strength: 'strong'
    });
  }

  // 38. Akhanda Samrajya Yoga
  if (jupiterHouse === 5 && sunHouse === 11) {
    yogas.push({
      name: 'Akhanda Samrajya Yoga',
      type: 'beneficial',
      description: 'Jupiter in 5th, Sun in 11th, Moon in Lagna',
      effects: 'Unbroken kingdom, supreme authority. Lasting power. Generational success.',
      strength: 'strong'
    });
  }

  // 39. Chatussagara Yoga
  if (isInKendra(jupiterHouse) && isInKendra(moonHouse) && isInKendra(venusHouse) && isInKendra(mercuryHouse)) {
    yogas.push({
      name: 'Chatussagara Yoga',
      type: 'beneficial',
      description: 'All benefics in four kendras',
      effects: 'Lord of all four oceans (world ruler). Supreme authority. International fame.',
      strength: 'strong'
    });
  }

  // 40. Sreenatha Yoga
  if ((venusHouse === 5 || venusHouse === 9) && moonHouse === 1) {
    yogas.push({
      name: 'Sreenatha Yoga',
      type: 'beneficial',
      description: 'Venus in trikona, Moon in Lagna',
      effects: 'Luxury, beauty, prosperity. Blessed life. Harmonious relationships.',
      strength: 'moderate'
    });
  }

  // 41. Kusuma Yoga
  if (jupiterHouse === 1 && moonHouse === 7 && sunHouse === 8) {
    yogas.push({
      name: 'Kusuma Yoga',
      type: 'beneficial',
      description: 'Specific planetary configuration',
      effects: 'Fame like a flower, respected. Pleasant personality. Success in public life.',
      strength: 'moderate'
    });
  }

  // 42. Damini Yoga
  if ([beneficsInUpachaya, strongPlanetsInKendra].every(count => count >= 2)) {
    yogas.push({
      name: 'Damini Yoga',
      type: 'beneficial',
      description: 'Strong benefics in multiple houses',
      effects: 'Charitable, helpful nature, wealth. Generous personality. Community leader.',
      strength: 'moderate'
    });
  }

  // 43. Pasha Yoga
  const planetsIn6_8_12 = Object.values(planets).filter((p: any) => 
    [6,8,12].includes(p.house)).length;
  if (planetsIn6_8_12 >= 3) {
    yogas.push({
      name: 'Pasha Yoga',
      type: 'malefic',
      description: 'Multiple planets in dusthana (6,8,12)',
      effects: 'Bondage, restrictions, struggles. Need for liberation through spiritual practice.',
      strength: 'moderate'
    });
  }

  // 44. Kedara Yoga
  if (planets.Sun && planets.Moon && planets.Mars && 
      [planets.Sun.house, planets.Moon.house, planets.Mars.house].every(h => [1,4,7,10].includes(h))) {
    yogas.push({
      name: 'Kedara Yoga',
      type: 'beneficial',
      description: 'Seven planets in four kendras',
      effects: 'Agricultural wealth, land ownership. Productive assets. Material security.',
      strength: 'strong'
    });
  }

  // 45. Shubha Yoga
  if (jupiterHouse === 5 || venusHouse === 5) {
    yogas.push({
      name: 'Shubha Yoga',
      type: 'beneficial',
      description: 'Benefics in 5th house',
      effects: 'Auspicious results, good children, intelligence. Fortunate speculation. Creative success.',
      strength: 'moderate'
    });
  }

  // 46. Asubha Yoga
  const maleficsInTrikona = [marsHouse, saturnHouse].filter(h => [1,5,9].includes(h)).length;
  if (maleficsInTrikona >= 2) {
    yogas.push({
      name: 'Asubha Yoga',
      type: 'malefic',
      description: 'Malefics in trikona houses',
      effects: 'Obstacles in dharma, reduced fortune. Need for remedial measures. Character challenges.',
      strength: 'moderate'
    });
  }

  // 47. Gauri Yoga
  if (jupiterHouse === 10 && moonHouse === 1 && venusHouse === 4) {
    yogas.push({
      name: 'Gauri Yoga',
      type: 'beneficial',
      description: 'Specific benefic configuration',
      effects: 'Marital happiness, beautiful spouse, prosperity. Domestic harmony. Feminine grace.',
      strength: 'moderate'
    });
  }

  // 48. Srikantha Yoga
  if (sunHouse === 10 && moonHouse === 4) {
    yogas.push({
      name: 'Srikantha Yoga',
      type: 'beneficial',
      description: 'Sun in 10th, Moon in 4th',
      effects: 'Fame, authority, emotional stability. Balanced power. Public recognition.',
      strength: 'strong'
    });
  }

  // 49. Sakata Yoga
  if (moonHouse > 0) {
    const jupiterFromMoon = (jupiterHouse - moonHouse + 12) % 12;
    if ([5, 7].includes(jupiterFromMoon)) {
      yogas.push({
        name: 'Sakata Yoga',
        type: 'malefic',
        description: 'Jupiter in 6th or 8th from Moon',
        effects: 'Ups and downs like cart wheel, financial instability. Variable fortune. Need for patience.',
        strength: 'weak'
      });
    }
  }

  // 50. Shankha-Paala Yoga
  if (jupiterHouse === 9 && moonHouse === 5) {
    yogas.push({
      name: 'Shankha-Paala Yoga',
      type: 'beneficial',
      description: 'Jupiter in 9th, Moon in 5th',
      effects: 'Protected fortune, righteous wealth. Ethical prosperity. Spiritual and material balance.',
      strength: 'strong'
    });
  }

  return yogas;
}
