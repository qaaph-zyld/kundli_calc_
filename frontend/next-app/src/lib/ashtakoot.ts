/**
 * Ashtakoot Matching System (36-Point Compatibility)
 * Traditional Vedic Astrology Marriage Compatibility
 * Based on: Classical texts - Muhurta Chintamani, Brihat Samhita
 */

export interface AshtakootResult {
  varna: { points: number; maxPoints: 1; description: string };
  vashya: { points: number; maxPoints: 2; description: string };
  tara: { points: number; maxPoints: 3; description: string };
  yoni: { points: number; maxPoints: 4; description: string };
  graha_maitri: { points: number; maxPoints: 5; description: string };
  gana: { points: number; maxPoints: 6; description: string };
  bhakoot: { points: number; maxPoints: 7; description: string };
  nadi: { points: number; maxPoints: 8; description: string };
  total: number;
  percentage: number;
  compatibility: 'Excellent' | 'Very Good' | 'Good' | 'Average' | 'Poor';
  recommendation: string;
}

// Nakshatra to various attributes mapping
const NAKSHATRA_DATA = {
  varna: ['Brahmin', 'Brahmin', 'Kshatriya', 'Kshatriya', 'Kshatriya', 'Vaishya', 'Vaishya', 'Vaishya', 'Brahmin',
          'Kshatriya', 'Kshatriya', 'Kshatriya', 'Vaishya', 'Vaishya', 'Shudra', 'Shudra', 'Shudra', 'Brahmin',
          'Brahmin', 'Kshatriya', 'Vaishya', 'Vaishya', 'Vaishya', 'Shudra', 'Shudra', 'Shudra', 'Shudra'],
  
  vashya: ['Quadruped', 'Quadruped', 'Quadruped', 'Quadruped', 'Human', 'Quadruped', 'Human', 'Reptile', 'Feline',
           'Rat', 'Rat', 'Quadruped', 'Human', 'Human', 'Quadruped', 'Quadruped', 'Quadruped', 'Insect',
           'Human', 'Human', 'Human', 'Waterborne', 'Waterborne', 'Quadruped', 'Quadruped', 'Quadruped', 'Waterborne'],
  
  yoni: ['Horse', 'Elephant', 'Sheep', 'Serpent', 'Dog', 'Cat', 'Rat', 'Cow', 'Buffalo',
         'Tiger', 'Deer', 'Deer', 'Monkey', 'Mongoose', 'Mongoose', 'Monkey', 'Lion',
         'Horse', 'Elephant', 'Sheep', 'Serpent', 'Dog', 'Cat', 'Rat', 'Cow', 'Buffalo', 'Tiger'],
  
  gana: ['Deva', 'Manushya', 'Manushya', 'Rakshasa', 'Manushya', 'Rakshasa', 'Manushya', 'Rakshasa', 'Rakshasa',
         'Deva', 'Manushya', 'Manushya', 'Rakshasa', 'Deva', 'Deva', 'Rakshasa', 'Rakshasa', 'Deva',
         'Manushya', 'Manushya', 'Rakshasa', 'Rakshasa', 'Rakshasa', 'Deva', 'Deva', 'Manushya', 'Manushya'],
  
  nadi: ['Adi', 'Madhya', 'Antya', 'Adi', 'Madhya', 'Antya', 'Adi', 'Madhya', 'Antya',
         'Adi', 'Madhya', 'Antya', 'Adi', 'Madhya', 'Antya', 'Adi', 'Madhya', 'Antya',
         'Adi', 'Madhya', 'Antya', 'Adi', 'Madhya', 'Antya', 'Adi', 'Madhya', 'Antya']
};

const YONI_COMPATIBILITY = [
  [4, 2, 3, 3, 2, 2, 2, 3, 3, 1, 2, 2, 3, 1, 1, 3, 0, 4, 2, 3, 3, 2, 2, 2, 3, 3, 1], // Horse
  [2, 4, 3, 3, 2, 3, 2, 3, 3, 2, 3, 3, 2, 2, 2, 2, 1, 2, 4, 3, 3, 2, 3, 2, 3, 3, 2], // Elephant
  [3, 3, 4, 2, 3, 1, 2, 3, 3, 0, 2, 2, 1, 2, 2, 1, 2, 3, 3, 4, 2, 3, 1, 2, 3, 3, 0], // Sheep
  [3, 3, 2, 4, 2, 2, 1, 3, 3, 2, 2, 2, 0, 2, 2, 0, 2, 3, 3, 2, 4, 2, 2, 1, 3, 3, 2], // Serpent
  [2, 2, 3, 2, 4, 2, 1, 3, 2, 2, 3, 3, 2, 2, 2, 2, 2, 2, 2, 3, 2, 4, 2, 1, 3, 2, 2], // Dog
  [2, 3, 1, 2, 2, 4, 0, 3, 2, 2, 3, 3, 2, 2, 2, 2, 2, 2, 3, 1, 2, 2, 4, 0, 3, 2, 2], // Cat
  [2, 2, 2, 1, 1, 0, 4, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 0, 4, 2, 1, 2], // Rat
  [3, 3, 3, 3, 3, 3, 2, 4, 3, 2, 3, 3, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 2, 4, 3, 2], // Cow
  [3, 3, 3, 3, 2, 2, 1, 3, 4, 0, 2, 2, 1, 2, 2, 1, 2, 3, 3, 3, 3, 2, 2, 1, 3, 4, 0], // Buffalo
  [1, 2, 0, 2, 2, 2, 2, 2, 0, 4, 1, 1, 0, 1, 1, 0, 2, 1, 2, 0, 2, 2, 2, 2, 2, 0, 4], // Tiger
  [2, 3, 2, 2, 3, 3, 2, 3, 2, 1, 4, 4, 2, 2, 2, 2, 2, 2, 3, 2, 2, 3, 3, 2, 3, 2, 1], // Deer
  [2, 3, 2, 2, 3, 3, 2, 3, 2, 1, 4, 4, 2, 2, 2, 2, 2, 2, 3, 2, 2, 3, 3, 2, 3, 2, 1], // Deer
  [3, 2, 1, 0, 2, 2, 2, 2, 1, 0, 2, 2, 4, 2, 2, 4, 2, 3, 2, 1, 0, 2, 2, 2, 2, 1, 0], // Monkey
  [1, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 4, 4, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 1], // Mongoose
  [1, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 4, 4, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 1], // Mongoose
  [3, 2, 1, 0, 2, 2, 2, 2, 1, 0, 2, 2, 4, 2, 2, 4, 2, 3, 2, 1, 0, 2, 2, 2, 2, 1, 0], // Monkey
  [0, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 4, 0, 1, 2, 2, 2, 2, 2, 2, 2, 2], // Lion
  [4, 2, 3, 3, 2, 2, 2, 3, 3, 1, 2, 2, 3, 1, 1, 3, 0, 4, 2, 3, 3, 2, 2, 2, 3, 3, 1], // Horse
  [2, 4, 3, 3, 2, 3, 2, 3, 3, 2, 3, 3, 2, 2, 2, 2, 1, 2, 4, 3, 3, 2, 3, 2, 3, 3, 2], // Elephant
  [3, 3, 4, 2, 3, 1, 2, 3, 3, 0, 2, 2, 1, 2, 2, 1, 2, 3, 3, 4, 2, 3, 1, 2, 3, 3, 0], // Sheep
  [3, 3, 2, 4, 2, 2, 1, 3, 3, 2, 2, 2, 0, 2, 2, 0, 2, 3, 3, 2, 4, 2, 2, 1, 3, 3, 2], // Serpent
  [2, 2, 3, 2, 4, 2, 1, 3, 2, 2, 3, 3, 2, 2, 2, 2, 2, 2, 2, 3, 2, 4, 2, 1, 3, 2, 2], // Dog
  [2, 3, 1, 2, 2, 4, 0, 3, 2, 2, 3, 3, 2, 2, 2, 2, 2, 2, 3, 1, 2, 2, 4, 0, 3, 2, 2], // Cat
  [2, 2, 2, 1, 1, 0, 4, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 0, 4, 2, 1, 2], // Rat
  [3, 3, 3, 3, 3, 3, 2, 4, 3, 2, 3, 3, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 2, 4, 3, 2], // Cow
  [3, 3, 3, 3, 2, 2, 1, 3, 4, 0, 2, 2, 1, 2, 2, 1, 2, 3, 3, 3, 3, 2, 2, 1, 3, 4, 0], // Buffalo
  [1, 2, 0, 2, 2, 2, 2, 2, 0, 4, 1, 1, 0, 1, 1, 0, 2, 1, 2, 0, 2, 2, 2, 2, 2, 0, 4]  // Tiger
];

/**
 * Calculate Ashtakoot compatibility between two charts
 */
export function calculateAshtakoot(
  chart1: any,
  chart2: any
): AshtakootResult {
  const moon1Nakshatra = getMoonNakshatra(chart1);
  const moon2Nakshatra = getMoonNakshatra(chart2);
  
  if (!moon1Nakshatra || !moon2Nakshatra) {
    throw new Error('Moon nakshatra not found in charts');
  }

  const nak1Index = moon1Nakshatra - 1;
  const nak2Index = moon2Nakshatra - 1;

  // 1. Varna (Caste) - 1 point
  const varna = calculateVarna(nak1Index, nak2Index);

  // 2. Vashya (Mutual Attraction) - 2 points
  const vashya = calculateVashya(nak1Index, nak2Index);

  // 3. Tara (Birth Star) - 3 points
  const tara = calculateTara(nak1Index, nak2Index);

  // 4. Yoni (Sexual Compatibility) - 4 points
  const yoni = calculateYoni(nak1Index, nak2Index);

  // 5. Graha Maitri (Planetary Friendship) - 5 points
  const grahaMaitri = calculateGrahaMaitri(chart1, chart2);

  // 6. Gana (Temperament) - 6 points
  const gana = calculateGana(nak1Index, nak2Index);

  // 7. Bhakoot (Rasi) - 7 points
  const bhakoot = calculateBhakoot(chart1, chart2);

  // 8. Nadi (Health/Genetics) - 8 points
  const nadi = calculateNadi(nak1Index, nak2Index);

  const total = varna.points + vashya.points + tara.points + yoni.points +
                grahaMaitri.points + gana.points + bhakoot.points + nadi.points;
  
  const percentage = (total / 36) * 100;

  let compatibility: 'Excellent' | 'Very Good' | 'Good' | 'Average' | 'Poor';
  let recommendation: string;

  if (percentage >= 80) {
    compatibility = 'Excellent';
    recommendation = 'Outstanding match! This union is highly favorable for a happy and prosperous married life.';
  } else if (percentage >= 60) {
    compatibility = 'Very Good';
    recommendation = 'Very good compatibility. This match is recommended and will likely lead to a harmonious relationship.';
  } else if (percentage >= 40) {
    compatibility = 'Good';
    recommendation = 'Good compatibility. With understanding and effort, this relationship can thrive.';
  } else if (percentage >= 25) {
    compatibility = 'Average';
    recommendation = 'Average compatibility. Some challenges may arise, but they can be overcome with commitment.';
  } else {
    compatibility = 'Poor';
    recommendation = 'Below average compatibility. This match may face significant challenges. Consultation with an experienced astrologer is recommended.';
  }

  return {
    varna,
    vashya,
    tara,
    yoni,
    graha_maitri: grahaMaitri,
    gana,
    bhakoot,
    nadi,
    total,
    percentage,
    compatibility,
    recommendation
  };
}

function getMoonNakshatra(chart: any): number | null {
  const moon = chart?.planetary_positions?.Moon;
  if (!moon) return null;
  
  // Calculate nakshatra from longitude
  // Each nakshatra is 13°20' (13.333°)
  const longitude = moon.longitude;
  const nakshatra = Math.floor(longitude / 13.333333) + 1;
  return nakshatra;
}

function calculateVarna(nak1: number, nak2: number): { points: number; maxPoints: 1; description: string } {
  const varna1 = NAKSHATRA_DATA.varna[nak1];
  const varna2 = NAKSHATRA_DATA.varna[nak2];
  
  const varnaOrder = { 'Brahmin': 4, 'Kshatriya': 3, 'Vaishya': 2, 'Shudra': 1 };
  const v1 = varnaOrder[varna1 as keyof typeof varnaOrder];
  const v2 = varnaOrder[varna2 as keyof typeof varnaOrder];
  
  const points = v1 >= v2 ? 1 : 0;
  
  return {
    points,
    maxPoints: 1,
    description: points === 1 
      ? `Compatible varnas (${varna1} - ${varna2}). Spiritual and intellectual compatibility is good.`
      : `Varna mismatch (${varna1} - ${varna2}). May indicate different spiritual aspirations.`
  };
}

function calculateVashya(nak1: number, nak2: number): { points: number; maxPoints: 2; description: string } {
  const vashya1 = NAKSHATRA_DATA.vashya[nak1];
  const vashya2 = NAKSHATRA_DATA.vashya[nak2];
  
  let points = 0;
  if (vashya1 === vashya2) {
    points = 2;
  } else if (
    (vashya1 === 'Human' && vashya2 === 'Human') ||
    (vashya1 === 'Quadruped' && vashya2 === 'Quadruped')
  ) {
    points = 2;
  } else if (
    (vashya1 === 'Human' || vashya2 === 'Human') &&
    (vashya1 === 'Quadruped' || vashya2 === 'Quadruped')
  ) {
    points = 1;
  }
  
  return {
    points,
    maxPoints: 2,
    description: points === 2
      ? `Strong mutual attraction (${vashya1} - ${vashya2}). Natural control and influence over each other.`
      : points === 1
      ? `Moderate attraction (${vashya1} - ${vashya2}). Some level of mutual influence exists.`
      : `Weak attraction (${vashya1} - ${vashya2}). May struggle to influence each other positively.`
  };
}

function calculateTara(nak1: number, nak2: number): { points: number; maxPoints: 3; description: string } {
  const count = ((nak2 - nak1 + 27) % 27) + 1;
  const remainder = count % 9;
  
  // Janma (1), Sampat (2), Vipat (3), Kshema (4), Pratyak (5), Sadhana (6), Vadha (7), Mitra (8), Param Mitra (9)
  const favorableTaras = [1, 2, 4, 6, 8, 9];
  const points = favorableTaras.includes(remainder) ? 3 : 0;
  
  const taraNames = ['', 'Janma', 'Sampat', 'Vipat', 'Kshema', 'Pratyak', 'Sadhana', 'Vadha', 'Mitra', 'Param Mitra'];
  
  return {
    points,
    maxPoints: 3,
    description: points === 3
      ? `Favorable tara (${taraNames[remainder]}). Mutual well-being and prosperity indicated.`
      : `Unfavorable tara (${taraNames[remainder]}). May face obstacles in well-being.`
  };
}

function calculateYoni(nak1: number, nak2: number): { points: number; maxPoints: 4; description: string } {
  const yoni1 = NAKSHATRA_DATA.yoni[nak1];
  const yoni2 = NAKSHATRA_DATA.yoni[nak2];
  
  const yoniList = ['Horse', 'Elephant', 'Sheep', 'Serpent', 'Dog', 'Cat', 'Rat', 'Cow', 'Buffalo',
                    'Tiger', 'Deer', 'Deer', 'Monkey', 'Mongoose', 'Mongoose', 'Monkey', 'Lion',
                    'Horse', 'Elephant', 'Sheep', 'Serpent', 'Dog', 'Cat', 'Rat', 'Cow', 'Buffalo', 'Tiger'];
  
  const yoni1Index = yoniList.indexOf(yoni1);
  const yoni2Index = yoniList.indexOf(yoni2);
  
  const points = YONI_COMPATIBILITY[yoni1Index][yoni2Index];
  
  return {
    points,
    maxPoints: 4,
    description: points === 4
      ? `Excellent yoni match (${yoni1} - ${yoni2}). Perfect sexual and biological compatibility.`
      : points >= 2
      ? `Good yoni match (${yoni1} - ${yoni2}). Satisfactory physical compatibility.`
      : `Poor yoni match (${yoni1} - ${yoni2}). May face challenges in physical relationship.`
  };
}

function calculateGrahaMaitri(chart1: any, chart2: any): { points: number; maxPoints: 5; description: string } {
  const moon1Sign = chart1?.planetary_positions?.Moon?.sign_num;
  const moon2Sign = chart2?.planetary_positions?.Moon?.sign_num;
  
  if (!moon1Sign || !moon2Sign) {
    return { points: 0, maxPoints: 5, description: 'Moon sign not found' };
  }
  
  // Sign lords
  const signLords = [1, 2, 3, 4, 5, 3, 2, 1, 6, 7, 7, 6]; // Mars, Venus, Mercury, Moon, Sun, Mercury, Venus, Mars, Jupiter, Saturn, Saturn, Jupiter
  const lord1 = signLords[(moon1Sign - 1) % 12];
  const lord2 = signLords[(moon2Sign - 1) % 12];
  
  // Planetary friendships (simplified)
  const friendships = {
    1: [5, 1, 6], // Sun friends: Sun, Mars, Jupiter
    2: [3, 7, 2], // Moon friends: Mercury, Saturn, Moon
    3: [5, 2, 3], // Mars friends: Sun, Moon, Mars
    4: [5, 3, 4], // Mercury friends: Sun, Mercury, Venus
    5: [5, 4, 6], // Jupiter friends: Sun, Moon, Jupiter
    6: [3, 7, 4], // Venus friends: Mercury, Saturn, Venus
    7: [3, 2, 7]  // Saturn friends: Mercury, Venus, Saturn
  };
  
  let points = 0;
  if (lord1 === lord2) {
    points = 5;
  } else if (friendships[lord1 as keyof typeof friendships]?.includes(lord2)) {
    points = 4;
  } else {
    points = 1;
  }
  
  return {
    points,
    maxPoints: 5,
    description: points >= 4
      ? 'Excellent planetary friendship. Mental compatibility and understanding are strong.'
      : points >= 2
      ? 'Moderate planetary friendship. Some mental harmony exists.'
      : 'Weak planetary friendship. May face mental incompatibility.'
  };
}

function calculateGana(nak1: number, nak2: number): { points: number; maxPoints: 6; description: string } {
  const gana1 = NAKSHATRA_DATA.gana[nak1];
  const gana2 = NAKSHATRA_DATA.gana[nak2];
  
  let points = 0;
  if (gana1 === gana2) {
    points = 6;
  } else if (
    (gana1 === 'Deva' && gana2 === 'Manushya') ||
    (gana1 === 'Manushya' && gana2 === 'Deva')
  ) {
    points = 6;
  } else if (
    (gana1 === 'Manushya' && gana2 === 'Rakshasa') ||
    (gana1 === 'Rakshasa' && gana2 === 'Manushya')
  ) {
    points = 3;
  } else {
    points = 0; // Deva - Rakshasa
  }
  
  return {
    points,
    maxPoints: 6,
    description: points === 6
      ? `Perfect temperament match (${gana1} - ${gana2}). Similar nature and behavior.`
      : points === 3
      ? `Moderate temperament match (${gana1} - ${gana2}). Some behavioral differences.`
      : `Poor temperament match (${gana1} - ${gana2}). Significant behavioral conflicts possible.`
  };
}

function calculateBhakoot(chart1: any, chart2: any): { points: number; maxPoints: 7; description: string } {
  const moon1Sign = chart1?.planetary_positions?.Moon?.sign_num;
  const moon2Sign = chart2?.planetary_positions?.Moon?.sign_num;
  
  if (!moon1Sign || !moon2Sign) {
    return { points: 0, maxPoints: 7, description: 'Moon sign not found' };
  }
  
  const diff = Math.abs(moon1Sign - moon2Sign);
  
  // Signs in 2-12, 5-9, 6-8 positions are inauspicious
  if (diff === 1 || diff === 11 || diff === 4 || diff === 8 || diff === 5 || diff === 7) {
    return {
      points: 0,
      maxPoints: 7,
      description: 'Unfavorable rasi position. May affect health, wealth, or progeny.'
    };
  }
  
  return {
    points: 7,
    maxPoints: 7,
    description: 'Favorable rasi position. Good for health, wealth, and children.'
  };
}

function calculateNadi(nak1: number, nak2: number): { points: number; maxPoints: 8; description: string } {
  const nadi1 = NAKSHATRA_DATA.nadi[nak1];
  const nadi2 = NAKSHATRA_DATA.nadi[nak2];
  
  const points = nadi1 !== nadi2 ? 8 : 0;
  
  return {
    points,
    maxPoints: 8,
    description: points === 8
      ? `Different nadis (${nadi1} - ${nadi2}). Good genetic compatibility and healthy progeny indicated.`
      : `Same nadi (${nadi1}). Nadi dosha present - may affect health of progeny. Remedies should be performed.`
  };
}
