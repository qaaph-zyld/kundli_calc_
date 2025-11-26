/**
 * Multi-language Translation System
 * Supports English, Hindi, and Sanskrit
 */

export type Language = 'en' | 'hi' | 'sa';

export interface TranslationSet {
  // Navigation
  home: string;
  chart: string;
  analysis: string;
  compatibility: string;
  muhurta: string;
  settings: string;
  
  // Planets
  planets: {
    sun: string;
    moon: string;
    mars: string;
    mercury: string;
    jupiter: string;
    venus: string;
    saturn: string;
    rahu: string;
    ketu: string;
  };
  
  // Signs
  signs: {
    aries: string;
    taurus: string;
    gemini: string;
    cancer: string;
    leo: string;
    virgo: string;
    libra: string;
    scorpio: string;
    sagittarius: string;
    capricorn: string;
    aquarius: string;
    pisces: string;
  };
  
  // Houses
  houses: {
    h1: string;
    h2: string;
    h3: string;
    h4: string;
    h5: string;
    h6: string;
    h7: string;
    h8: string;
    h9: string;
    h10: string;
    h11: string;
    h12: string;
  };
  
  // Nakshatras
  nakshatras: string[];
  
  // UI Elements
  ui: {
    calculate: string;
    export: string;
    save: string;
    load: string;
    date: string;
    time: string;
    place: string;
    birthDetails: string;
    chartType: string;
    analysis: string;
    predictions: string;
    compatibility: string;
    dasha: string;
    transit: string;
    yoga: string;
    strength: string;
    auspicious: string;
    inauspicious: string;
    favorable: string;
    unfavorable: string;
    strong: string;
    weak: string;
    benefic: string;
    malefic: string;
  };
  
  // Panchang
  panchang: {
    tithi: string;
    nakshatra: string;
    yoga: string;
    karana: string;
    weekday: string;
    sunrise: string;
    sunset: string;
    rahuKalam: string;
    gulika: string;
    yamagandam: string;
    abhijit: string;
    shukla: string;
    krishna: string;
  };
  
  // Compatibility
  kootas: {
    varna: string;
    vashya: string;
    tara: string;
    yoni: string;
    grahaMaitri: string;
    gana: string;
    bhakoot: string;
    nadi: string;
  };
  
  // Common terms
  terms: {
    ascendant: string;
    descendant: string;
    midheaven: string;
    nadir: string;
    degree: string;
    minute: string;
    retrograde: string;
    exalted: string;
    debilitated: string;
    own: string;
    friend: string;
    enemy: string;
    neutral: string;
  };
}

export const translations: Record<Language, TranslationSet> = {
  en: {
    home: 'Home',
    chart: 'Chart',
    analysis: 'Analysis',
    compatibility: 'Compatibility',
    muhurta: 'Muhurta',
    settings: 'Settings',
    
    planets: {
      sun: 'Sun',
      moon: 'Moon',
      mars: 'Mars',
      mercury: 'Mercury',
      jupiter: 'Jupiter',
      venus: 'Venus',
      saturn: 'Saturn',
      rahu: 'Rahu',
      ketu: 'Ketu'
    },
    
    signs: {
      aries: 'Aries',
      taurus: 'Taurus',
      gemini: 'Gemini',
      cancer: 'Cancer',
      leo: 'Leo',
      virgo: 'Virgo',
      libra: 'Libra',
      scorpio: 'Scorpio',
      sagittarius: 'Sagittarius',
      capricorn: 'Capricorn',
      aquarius: 'Aquarius',
      pisces: 'Pisces'
    },
    
    houses: {
      h1: '1st House (Self)',
      h2: '2nd House (Wealth)',
      h3: '3rd House (Siblings)',
      h4: '4th House (Home)',
      h5: '5th House (Children)',
      h6: '6th House (Enemies)',
      h7: '7th House (Marriage)',
      h8: '8th House (Death)',
      h9: '9th House (Fortune)',
      h10: '10th House (Career)',
      h11: '11th House (Gains)',
      h12: '12th House (Loss)'
    },
    
    nakshatras: [
      'Ashwini', 'Bharani', 'Krittika', 'Rohini', 'Mrigashira', 'Ardra',
      'Punarvasu', 'Pushya', 'Ashlesha', 'Magha', 'Purva Phalguni', 'Uttara Phalguni',
      'Hasta', 'Chitra', 'Swati', 'Vishakha', 'Anuradha', 'Jyeshtha',
      'Mula', 'Purva Ashadha', 'Uttara Ashadha', 'Shravana', 'Dhanishta', 'Shatabhisha',
      'Purva Bhadrapada', 'Uttara Bhadrapada', 'Revati'
    ],
    
    ui: {
      calculate: 'Calculate',
      export: 'Export',
      save: 'Save',
      load: 'Load',
      date: 'Date',
      time: 'Time',
      place: 'Place',
      birthDetails: 'Birth Details',
      chartType: 'Chart Type',
      analysis: 'Analysis',
      predictions: 'Predictions',
      compatibility: 'Compatibility',
      dasha: 'Dasha',
      transit: 'Transit',
      yoga: 'Yoga',
      strength: 'Strength',
      auspicious: 'Auspicious',
      inauspicious: 'Inauspicious',
      favorable: 'Favorable',
      unfavorable: 'Unfavorable',
      strong: 'Strong',
      weak: 'Weak',
      benefic: 'Benefic',
      malefic: 'Malefic'
    },
    
    panchang: {
      tithi: 'Tithi',
      nakshatra: 'Nakshatra',
      yoga: 'Yoga',
      karana: 'Karana',
      weekday: 'Weekday',
      sunrise: 'Sunrise',
      sunset: 'Sunset',
      rahuKalam: 'Rahu Kalam',
      gulika: 'Gulika Kalam',
      yamagandam: 'Yamagandam',
      abhijit: 'Abhijit Muhurta',
      shukla: 'Shukla Paksha',
      krishna: 'Krishna Paksha'
    },
    
    kootas: {
      varna: 'Varna',
      vashya: 'Vashya',
      tara: 'Tara',
      yoni: 'Yoni',
      grahaMaitri: 'Graha Maitri',
      gana: 'Gana',
      bhakoot: 'Bhakoot',
      nadi: 'Nadi'
    },
    
    terms: {
      ascendant: 'Ascendant',
      descendant: 'Descendant',
      midheaven: 'Midheaven',
      nadir: 'Nadir',
      degree: 'Degree',
      minute: 'Minute',
      retrograde: 'Retrograde',
      exalted: 'Exalted',
      debilitated: 'Debilitated',
      own: 'Own Sign',
      friend: 'Friendly',
      enemy: 'Enemy',
      neutral: 'Neutral'
    }
  },
  
  hi: {
    home: 'होम',
    chart: 'कुंडली',
    analysis: 'विश्लेषण',
    compatibility: 'मिलान',
    muhurta: 'मुहूर्त',
    settings: 'सेटिंग्स',
    
    planets: {
      sun: 'सूर्य',
      moon: 'चंद्र',
      mars: 'मंगल',
      mercury: 'बुध',
      jupiter: 'गुरु',
      venus: 'शुक्र',
      saturn: 'शनि',
      rahu: 'राहु',
      ketu: 'केतु'
    },
    
    signs: {
      aries: 'मेष',
      taurus: 'वृषभ',
      gemini: 'मिथुन',
      cancer: 'कर्क',
      leo: 'सिंह',
      virgo: 'कन्या',
      libra: 'तुला',
      scorpio: 'वृश्चिक',
      sagittarius: 'धनु',
      capricorn: 'मकर',
      aquarius: 'कुंभ',
      pisces: 'मीन'
    },
    
    houses: {
      h1: 'प्रथम भाव (तनु)',
      h2: 'द्वितीय भाव (धन)',
      h3: 'तृतीय भाव (भ्रातृ)',
      h4: 'चतुर्थ भाव (मातृ)',
      h5: 'पंचम भाव (पुत्र)',
      h6: 'षष्ठ भाव (शत्रु)',
      h7: 'सप्तम भाव (विवाह)',
      h8: 'अष्टम भाव (मृत्यु)',
      h9: 'नवम भाव (भाग्य)',
      h10: 'दशम भाव (कर्म)',
      h11: 'एकादश भाव (लाभ)',
      h12: 'द्वादश भाव (व्यय)'
    },
    
    nakshatras: [
      'अश्विनी', 'भरणी', 'कृत्तिका', 'रोहिणी', 'मृगशिरा', 'आर्द्रा',
      'पुनर्वसु', 'पुष्य', 'आश्लेषा', 'मघा', 'पूर्वाफाल्गुनी', 'उत्तराफाल्गुनी',
      'हस्त', 'चित्रा', 'स्वाति', 'विशाखा', 'अनुराधा', 'ज्येष्ठा',
      'मूल', 'पूर्वाषाढ़ा', 'उत्तराषाढ़ा', 'श्रवण', 'धनिष्ठा', 'शतभिषा',
      'पूर्वाभाद्रपद', 'उत्तराभाद्रपद', 'रेवती'
    ],
    
    ui: {
      calculate: 'गणना करें',
      export: 'निर्यात',
      save: 'सहेजें',
      load: 'लोड',
      date: 'तारीख',
      time: 'समय',
      place: 'स्थान',
      birthDetails: 'जन्म विवरण',
      chartType: 'कुंडली प्रकार',
      analysis: 'विश्लेषण',
      predictions: 'भविष्यवाणी',
      compatibility: 'मिलान',
      dasha: 'दशा',
      transit: 'गोचर',
      yoga: 'योग',
      strength: 'बल',
      auspicious: 'शुभ',
      inauspicious: 'अशुभ',
      favorable: 'अनुकूल',
      unfavorable: 'प्रतिकूल',
      strong: 'बलवान',
      weak: 'दुर्बल',
      benefic: 'शुभ',
      malefic: 'पाप'
    },
    
    panchang: {
      tithi: 'तिथि',
      nakshatra: 'नक्षत्र',
      yoga: 'योग',
      karana: 'करण',
      weekday: 'वार',
      sunrise: 'सूर्योदय',
      sunset: 'सूर्यास्त',
      rahuKalam: 'राहु काल',
      gulika: 'गुलिक काल',
      yamagandam: 'यमगंड',
      abhijit: 'अभिजित मुहूर्त',
      shukla: 'शुक्ल पक्ष',
      krishna: 'कृष्ण पक्ष'
    },
    
    kootas: {
      varna: 'वर्ण',
      vashya: 'वश्य',
      tara: 'तारा',
      yoni: 'योनि',
      grahaMaitri: 'ग्रह मैत्री',
      gana: 'गण',
      bhakoot: 'भकूट',
      nadi: 'नाड़ी'
    },
    
    terms: {
      ascendant: 'लग्न',
      descendant: 'अस्त',
      midheaven: 'मध्य आकाश',
      nadir: 'पाताल',
      degree: 'अंश',
      minute: 'कला',
      retrograde: 'वक्री',
      exalted: 'उच्च',
      debilitated: 'नीच',
      own: 'स्वराशि',
      friend: 'मित्र',
      enemy: 'शत्रु',
      neutral: 'सम'
    }
  },
  
  sa: {
    home: 'गृहम्',
    chart: 'जन्मपत्रिका',
    analysis: 'विश्लेषणम्',
    compatibility: 'मेलापकम्',
    muhurta: 'मुहूर्तः',
    settings: 'विन्यासः',
    
    planets: {
      sun: 'सूर्यः',
      moon: 'चन्द्रः',
      mars: 'मङ्गलः',
      mercury: 'बुधः',
      jupiter: 'बृहस्पतिः',
      venus: 'शुक्रः',
      saturn: 'शनैश्चरः',
      rahu: 'राहुः',
      ketu: 'केतुः'
    },
    
    signs: {
      aries: 'मेषः',
      taurus: 'वृषभः',
      gemini: 'मिथुनम्',
      cancer: 'कर्कटः',
      leo: 'सिंहः',
      virgo: 'कन्या',
      libra: 'तुला',
      scorpio: 'वृश्चिकः',
      sagittarius: 'धनुः',
      capricorn: 'मकरः',
      aquarius: 'कुम्भः',
      pisces: 'मीनः'
    },
    
    houses: {
      h1: 'प्रथमभावः (तनुभावः)',
      h2: 'द्वितीयभावः (धनभावः)',
      h3: 'तृतीयभावः (सहजभावः)',
      h4: 'चतुर्थभावः (सुखभावः)',
      h5: 'पञ्चमभावः (पुत्रभावः)',
      h6: 'षष्ठभावः (रिपुभावः)',
      h7: 'सप्तमभावः (कलत्रभावः)',
      h8: 'अष्टमभावः (आयुर्भावः)',
      h9: 'नवमभावः (धर्मभावः)',
      h10: 'दशमभावः (कर्मभावः)',
      h11: 'एकादशभावः (लाभभावः)',
      h12: 'द्वादशभावः (व्ययभावः)'
    },
    
    nakshatras: [
      'अश्विनी', 'भरणी', 'कृत्तिका', 'रोहिणी', 'मृगशीर्षम्', 'आर्द्रा',
      'पुनर्वसु', 'पुष्यः', 'आश्लेषा', 'मघा', 'पूर्वाफल्गुनी', 'उत्तराफल्गुनी',
      'हस्तः', 'चित्रा', 'स्वाती', 'विशाखा', 'अनुराधा', 'ज्येष्ठा',
      'मूलम्', 'पूर्वाषाढा', 'उत्तराषाढा', 'श्रवणः', 'धनिष्ठा', 'शतभिषक्',
      'पूर्वाभाद्रपदा', 'उत्तराभाद्रपदा', 'रेवती'
    ],
    
    ui: {
      calculate: 'गणयतु',
      export: 'निर्गमः',
      save: 'रक्षतु',
      load: 'आनयतु',
      date: 'तिथिः',
      time: 'कालः',
      place: 'स्थानम्',
      birthDetails: 'जन्मविवरणम्',
      chartType: 'चक्रप्रकारः',
      analysis: 'विश्लेषणम्',
      predictions: 'फलादेशः',
      compatibility: 'मेलापकम्',
      dasha: 'दशा',
      transit: 'गोचरः',
      yoga: 'योगः',
      strength: 'बलम्',
      auspicious: 'शुभम्',
      inauspicious: 'अशुभम्',
      favorable: 'अनुकूलम्',
      unfavorable: 'प्रतिकूलम्',
      strong: 'बलवान्',
      weak: 'दुर्बलः',
      benefic: 'शुभग्रहः',
      malefic: 'पापग्रहः'
    },
    
    panchang: {
      tithi: 'तिथिः',
      nakshatra: 'नक्षत्रम्',
      yoga: 'योगः',
      karana: 'करणम्',
      weekday: 'वारः',
      sunrise: 'सूर्योदयः',
      sunset: 'सूर्यास्तः',
      rahuKalam: 'राहुकालः',
      gulika: 'गुलिककालः',
      yamagandam: 'यमघण्टः',
      abhijit: 'अभिजित्मुहूर्तः',
      shukla: 'शुक्लपक्षः',
      krishna: 'कृष्णपक्षः'
    },
    
    kootas: {
      varna: 'वर्णः',
      vashya: 'वश्यम्',
      tara: 'तारा',
      yoni: 'योनिः',
      grahaMaitri: 'ग्रहमैत्री',
      gana: 'गणः',
      bhakoot: 'भकूटम्',
      nadi: 'नाडी'
    },
    
    terms: {
      ascendant: 'लग्नम्',
      descendant: 'अस्तलग्नम्',
      midheaven: 'मध्यललितम्',
      nadir: 'पातालम्',
      degree: 'अंशः',
      minute: 'कला',
      retrograde: 'वक्री',
      exalted: 'उच्चस्थः',
      debilitated: 'नीचस्थः',
      own: 'स्वक्षेत्रे',
      friend: 'मित्रम्',
      enemy: 'शत्रुः',
      neutral: 'समः'
    }
  }
};

// Translation hook/context helper
export function getTranslation(lang: Language): TranslationSet {
  return translations[lang] || translations.en;
}

// Planet name translator
export function translatePlanet(planet: string, lang: Language): string {
  const t = translations[lang].planets;
  const key = planet.toLowerCase() as keyof typeof t;
  return t[key] || planet;
}

// Sign name translator
export function translateSign(sign: string, lang: Language): string {
  const t = translations[lang].signs;
  const key = sign.toLowerCase() as keyof typeof t;
  return t[key] || sign;
}

// Nakshatra translator
export function translateNakshatra(index: number, lang: Language): string {
  const nakshatras = translations[lang].nakshatras;
  return nakshatras[index] || translations.en.nakshatras[index];
}
