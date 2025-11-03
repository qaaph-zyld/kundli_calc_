/**
 * Classical Vedic Astrology Interpretations
 * Based on: BPHS (Brihat Parashara Hora Shastra), Phaladeepika, Saravali
 * 
 * These are traditional interpretations from classical texts,
 * adapted for modern digital presentation.
 */

// Planet in Sign Interpretations
export const PLANET_IN_SIGN: Record<string, Record<string, string>> = {
  Sun: {
    Aries: "Strong leadership qualities, pioneering spirit, natural authority. Confident and ambitious in career pursuits.",
    Taurus: "Stable nature, materialistic tendencies. Success through persistent efforts. Strong value for tradition.",
    Gemini: "Intellectual pursuits, communication skills. Multiple interests and versatile nature. Good for writing.",
    Cancer: "Emotional depth, nurturing nature. Family-oriented. May face ego-emotion conflicts.",
    Leo: "Exalted position. Royal qualities, natural charisma, leadership abilities. Success in authority positions.",
    Virgo: "Analytical mind, attention to detail. Service-oriented nature. Health consciousness.",
    Libra: "Debilitated position. Diplomatic nature, artistic inclinations. Relationship-focused, may lack confidence.",
    Scorpio: "Intense personality, transformative experiences. Research-oriented, secretive nature.",
    Sagittarius: "Philosophical mind, spiritual inclinations. Teaching abilities, love for truth and justice.",
    Capricorn: "Disciplined approach, practical mindset. Ambitious career goals, respect for authority.",
    Aquarius: "Humanitarian values, unconventional thinking. Scientific temperament, social consciousness.",
    Pisces: "Spiritual nature, compassionate heart. Imaginative mind, may lack practicality."
  },
  Moon: {
    Aries: "Quick emotions, impulsive nature. Dynamic mind, pioneering instincts.",
    Taurus: "Exalted position. Emotional stability, strong memory. Materialistic comforts, artistic nature.",
    Gemini: "Versatile mind, changing emotions. Good communication, intellectual pursuits.",
    Cancer: "Own sign. Strong intuition, deep emotions. Nurturing nature, attached to family and home.",
    Leo: "Emotional confidence, creative mind. Need for recognition, generous heart.",
    Virgo: "Analytical emotions, health-conscious. Practical mind, service-oriented.",
    Libra: "Balanced emotions, diplomatic nature. Artistic inclinations, relationship-focused.",
    Scorpio: "Debilitated position. Deep emotions, secretive nature. Intense feelings, transformative experiences.",
    Sagittarius: "Optimistic mind, philosophical nature. Love for truth, spiritual inclinations.",
    Capricorn: "Practical emotions, disciplined mind. Ambitious nature, emotional restraint.",
    Aquarius: "Humanitarian feelings, unconventional thinking. Friendly nature, social causes.",
    Pisces: "Compassionate heart, spiritual mind. Imaginative nature, psychic abilities."
  },
  Mars: {
    Aries: "Own sign. Strong courage, leadership abilities. Athletic nature, pioneering spirit.",
    Taurus: "Persistent efforts, strong determination. Materialistic pursuits, fixed nature.",
    Gemini: "Quick mind, sharp communication. Argumentative nature, technical skills.",
    Cancer: "Debilitated position. Emotional energy, may lack courage. Indirect actions.",
    Leo: "Powerful energy, leadership in action. Commanding nature, athletic abilities.",
    Virgo: "Analytical approach to action. Technical skills, attention to detail in work.",
    Libra: "Diplomatic actions, balanced energy. May lack decisive nature, artistic pursuits.",
    Scorpio: "Own sign. Intense energy, transformative power. Research abilities, secretive actions.",
    Sagittarius: "Philosophical actions, righteous energy. Athletic nature, love for adventure.",
    Capricorn: "Exalted position. Disciplined energy, organized actions. Ambitious pursuits, career success.",
    Aquarius: "Unconventional actions, humanitarian efforts. Technical skills, scientific pursuits.",
    Pisces: "Spiritual actions, compassionate energy. May lack direction, imaginative pursuits."
  },
  Mercury: {
    Aries: "Quick thinking, sharp intellect. Direct communication, pioneering ideas.",
    Taurus: "Practical intelligence, stable thoughts. Business acumen, materialistic thinking.",
    Gemini: "Own sign. Brilliant intellect, versatile mind. Excellent communication, multiple talents.",
    Cancer: "Emotional intelligence, intuitive mind. Good memory, imaginative thinking.",
    Leo: "Creative intelligence, confident communication. Leadership in intellectual pursuits.",
    Virgo: "Exalted and own sign. Analytical brilliance, perfect discrimination. Technical excellence, attention to detail.",
    Libra: "Balanced thinking, diplomatic communication. Artistic intellect, relationship wisdom.",
    Scorpio: "Deep analytical mind, research abilities. Secretive communication, strategic thinking.",
    Sagittarius: "Philosophical mind, teaching abilities. Ethical thinking, spiritual wisdom.",
    Capricorn: "Practical intelligence, organized thinking. Business mind, disciplined approach.",
    Aquarius: "Scientific mind, innovative thinking. Humanitarian intellect, unconventional ideas.",
    Pisces: "Debilitated position. Imaginative mind, spiritual thinking. May lack discrimination, scattered thoughts."
  },
  Jupiter: {
    Aries: "Philosophical leadership, ethical actions. Teaching abilities, spiritual courage.",
    Taurus: "Practical wisdom, material prosperity. Strong value system, stable knowledge.",
    Gemini: "Intellectual wisdom, teaching through communication. Multiple knowledge streams.",
    Cancer: "Exalted position. Compassionate wisdom, nurturing teacher. Family prosperity, spiritual emotions.",
    Leo: "Confident wisdom, royal knowledge. Teaching with authority, spiritual leadership.",
    Virgo: "Analytical wisdom, practical knowledge. Service-oriented teaching, health consciousness.",
    Libra: "Balanced wisdom, diplomatic knowledge. Legal matters, relationship counseling.",
    Scorpio: "Deep wisdom, transformative knowledge. Research in spirituality, occult understanding.",
    Sagittarius: "Own sign. Pure philosophical wisdom, spiritual teacher. Ethical nature, love for truth.",
    Capricorn: "Debilitated position. Practical but limited wisdom. Cautious approach, may lack faith.",
    Aquarius: "Humanitarian wisdom, scientific spirituality. Unconventional knowledge, social teaching.",
    Pisces: "Own sign. Spiritual wisdom, compassionate teacher. Mystical knowledge, universal love."
  },
  Venus: {
    Aries: "Passionate love, impulsive relationships. Creative energy, pioneering in arts.",
    Taurus: "Own sign. Strong sensual nature, love for luxury. Artistic talents, material comforts.",
    Gemini: "Intellectual love, versatile relationships. Communication in arts, multiple interests.",
    Cancer: "Nurturing love, emotional relationships. Family comfort, artistic home.",
    Leo: "Dramatic love, creative expression. Luxury loving, royal artistic taste.",
    Virgo: "Debilitated position. Analytical love, practical relationships. Service through beauty, critical of art.",
    Libra: "Own sign and exalted. Perfect harmony in love, balanced relationships. Artistic excellence, diplomatic charm.",
    Scorpio: "Intense love, passionate relationships. Deep artistic expression, transformative beauty.",
    Sagittarius: "Philosophical love, spiritual relationships. Teaching through arts, ethical values.",
    Capricorn: "Practical love, stable relationships. Disciplined artistic pursuit, traditional values.",
    Aquarius: "Unconventional love, friendly relationships. Humanitarian arts, social beauty.",
    Pisces: "Exalted position. Spiritual love, compassionate relationships. Mystical arts, universal beauty."
  },
  Saturn: {
    Aries: "Debilitated position. Restricted energy, delayed actions. Patient leadership needed.",
    Taurus: "Persistent efforts, stable work. Material success through patience, practical discipline.",
    Gemini: "Disciplined communication, serious thinking. Slow but steady learning.",
    Cancer: "Emotional restraint, family responsibilities. Patient nurturing, karmic home matters.",
    Leo: "Authority challenges, ego discipline. Patient in creative pursuits, delayed recognition.",
    Virgo: "Analytical discipline, perfect organization. Service through hard work, health through routine.",
    Libra: "Exalted position. Balanced justice, diplomatic discipline. Success in law, patient relationships.",
    Scorpio: "Deep transformation, intense discipline. Research through patience, occult mastery.",
    Sagittarius: "Philosophical discipline, spiritual maturity. Patient teaching, ethical responsibilities.",
    Capricorn: "Own sign. Perfect discipline, organized efforts. Career success, material achievement through patience.",
    Aquarius: "Own sign. Social discipline, humanitarian responsibilities. Scientific patience, unconventional maturity.",
    Pisces: "Spiritual discipline, compassionate responsibilities. Patient mysticism, karmic lessons."
  }
};

// House Significations
export const HOUSE_MEANINGS: Record<number, string> = {
  1: "Personality, physical body, self-expression, overall vitality. Your approach to life and first impressions.",
  2: "Wealth, family, speech, accumulated resources. Your values, food habits, and early childhood.",
  3: "Courage, siblings, short travels, communication skills. Hobbies, neighbors, and mental strength.",
  4: "Mother, home, property, emotional foundation. Education, vehicles, inner peace, and happiness.",
  5: "Children, creativity, intelligence, speculation. Romance, past-life merit (poorva punya), and education.",
  6: "Enemies, diseases, debts, service, daily routine. Obstacles, competition, and maternal relatives.",
  7: "Marriage, partnerships, business relationships. Spouse, public image, and long-distance travel.",
  8: "Longevity, transformation, inheritance, occult knowledge. Death, sudden events, and hidden matters.",
  9: "Father, dharma, fortune, higher education. Religion, long journeys, spiritual teachers (Guru).",
  10: "Career, social status, authority, achievements. Father's influence, profession, and public recognition.",
  11: "Gains, income, friendships, aspirations. Elder siblings, social networks, and fulfillment of desires.",
  12: "Losses, expenses, liberation (moksha), foreign lands. Isolation, spirituality, bed pleasures, and hospitals."
};

// Ascendant Sign Characteristics
export const ASCENDANT_TRAITS: Record<string, string> = {
  Aries: "Dynamic, courageous, pioneering, impulsive. Natural leaders with athletic build. Quick to act, independent nature.",
  Taurus: "Stable, practical, sensual, persistent. Strong build, love for comfort. Patient but stubborn when opposed.",
  Gemini: "Intellectual, versatile, communicative, restless. Youthful appearance, quick learner. May lack consistency.",
  Cancer: "Emotional, nurturing, intuitive, protective. Sensitive nature, strong family bonds. Fluctuating moods.",
  Leo: "Confident, charismatic, creative, proud. Regal bearing, natural authority. Generous but ego-sensitive.",
  Virgo: "Analytical, perfectionist, practical, health-conscious. Detail-oriented, service-minded. May be overly critical.",
  Libra: "Diplomatic, balanced, artistic, relationship-oriented. Charming personality, seeks harmony. May be indecisive.",
  Scorpio: "Intense, mysterious, transformative, magnetic. Penetrating gaze, strong willpower. Secretive and passionate.",
  Sagittarius: "Optimistic, philosophical, adventurous, honest. Athletic build, love for freedom. Blunt but well-meaning.",
  Capricorn: "Disciplined, ambitious, responsible, practical. Serious demeanor, career-focused. Patient and determined.",
  Aquarius: "Unconventional, humanitarian, intellectual, independent. Unique perspective, socially conscious. Can seem detached.",
  Pisces: "Compassionate, spiritual, imaginative, sensitive. Dreamy eyes, artistic nature. May lack boundaries."
};

// Dasha Period Interpretations
export const DASHA_EFFECTS: Record<string, string> = {
  Sun: "Focus on authority, father, government matters. Period of recognition, leadership opportunities. Ego development and self-confidence. Potential for career advancement in authoritative roles.",
  Moon: "Focus on emotions, mother, public matters. Period of emotional development and family concerns. Mind and mental peace important. Good for public relations and nurturing activities.",
  Mars: "Focus on courage, energy, property matters. Period of action and achievement through efforts. May face conflicts or surgery. Good for real estate, siblings, and athletic pursuits.",
  Mercury: "Focus on intellect, communication, business. Period of learning and skill development. Good for education, writing, and commercial activities. May travel frequently.",
  Jupiter: "Focus on wisdom, children, spirituality. Period of expansion and grace. Good for education, teaching, and spiritual growth. Blessings from teachers and father.",
  Venus: "Focus on love, luxury, creativity. Period of comfort and artistic pursuits. Marriage prospects improve. Good for relationships, arts, and material pleasures.",
  Saturn: "Focus on discipline, hard work, responsibilities. Period of karmic lessons and patience. May face delays and obstacles. Success through sustained effort and maturity.",
  Rahu: "Focus on material desires, foreign matters. Period of unconventional experiences and sudden changes. Good for technology, foreign connections. May face confusion or deception.",
  Ketu: "Focus on spirituality, detachment, mysticism. Period of spiritual growth and letting go. May face losses in material matters. Good for meditation and occult studies."
};

// Nakshatra Characteristics (simplified - 27 nakshatras)
export const NAKSHATRA_TRAITS: Record<string, string> = {
  Ashwini: "Healing abilities, swift actions, pioneering spirit. Horse energy - speed and healing.",
  Bharani: "Transformation, creativity, nurturing. Bearer of life - creation and destruction cycles.",
  Krittika: "Sharp intellect, cutting through illusions, purification. Fire energy - burning away impurities.",
  Rohini: "Beauty, fertility, growth. Moon's favorite nakshatra - creativity and material growth.",
  Mrigashira: "Searching nature, curiosity, gentleness. Deer energy - seeking knowledge.",
  Ardra: "Transformation through storms, emotional depth. Thunder and lightning - dramatic changes.",
  Punarvasu: "Renewal, return to source, optimistic. Bow and quiver - spiritual archer.",
  Pushya: "Nourishing, supporting, spiritual teaching. Most auspicious nakshatra - spiritual nourishment.",
  Ashlesha: "Hypnotic abilities, kundalini energy, mysticism. Serpent energy - coiled wisdom.",
  Magha: "Ancestral connections, royal qualities, tradition. Throne room - honoring ancestors.",
  'Purva Phalguni': "Enjoyment, creativity, procreation. Hammock or bed - rest and pleasure.",
  'Uttara Phalguni': "Service, agreements, partnerships. Back legs of bed - support and contracts.",
  Hasta: "Skillful hands, craftsmanship, manifestation. Hand - creating through skill.",
  Chitra: "Beauty, artistry, brilliant light. Pearl or shining jewel - creating beautiful things.",
  Swati: "Independence, flexibility, trade. Sword blown by wind - moving freely.",
  Vishakha: "Determined purpose, achievement focus. Triumphal arch - goal-oriented success.",
  Anuradha: "Devotion, friendship, balance. Lotus flower - rising above difficulties through devotion.",
  Jyeshtha: "Leadership, protection, seniority. Umbrella or earring - protecting others.",
  Mula: "Root investigation, deep inquiry, transformation. Bunch of roots - getting to the foundation.",
  'Purva Ashadha': "Invincibility, optimism, purification. Elephant tusk - undefeated strength.",
  'Uttara Ashadha': "Victory, permanent achievement, integrity. Elephant tusk or planks - lasting success.",
  Shravana: "Listening, learning, connection. Ear - learning through listening.",
  Dhanishtha: "Wealth, music, adaptability. Drum - creating rhythm and prosperity.",
  Shatabhisha: "Healing, secrecy, mysticism. Hundred physicians - healing through unconventional means.",
  'Purva Bhadrapada': "Transformation, intensity, mystical fire. Funeral cot - transformative spiritual fire.",
  'Uttara Bhadrapada': "Deep wisdom, kundalini rising, depth. Back legs of funeral cot - bringing rain of wisdom.",
  Revati: "Nourishment, completion, spiritual journey. Drum for marking time - safe journeys."
};

/**
 * Generate interpretation for planet in house
 */
export function interpretPlanetInHouse(planet: string, house: number): string {
  const interpretations: Record<string, Record<number, string>> = {
    Sun: {
      1: "Strong self-confidence, leadership abilities. Father's influence on personality. Natural authority and vitality.",
      2: "Wealth through government or father. Strong family values. Authoritative speech.",
      3: "Courageous nature, leadership among siblings. Father's influence on courage. May have ego conflicts with siblings.",
      4: "Happy home life through authority. Government property benefits. Father's influence on emotions.",
      5: "Intelligent children, leadership in creative pursuits. Good for speculation with care.",
      6: "Victory over enemies through authority. May face ego issues with servants/employees.",
      7: "Authoritative spouse or partner. Government connections through marriage. Leadership in partnerships.",
      8: "Interest in occult and authority matters. Father's health concerns. Inheritance from father.",
      9: "Strongly blessed by father and fortune. Government favor. Philosophical leadership.",
      10: "Exalted house. Career in government or authority positions. Fame and recognition.",
      11: "Gains through government. Influential friendships. Elder sibling may be authoritative.",
      12: "Expenses on father or government matters. Foreign government connections. Spiritual authority."
    },
    Moon: {
      1: "Emotional nature, changeable personality. Mother's influence strong. Intuitive approach to life.",
      2: "Wealth through mother or public. Good speech and memory. Family-oriented values.",
      3: "Emotional courage, close to siblings. Mental strength through mother. Frequent short travels.",
      4: "Exalted house. Very happy with mother. Comfortable home life. Emotional peace and contentment.",
      5: "Emotionally attached to children. Creative imagination. Intuitive intelligence.",
      6: "Emotional health issues. Mother's health concerns. Service through nurturing.",
      7: "Emotional spouse, public partnerships. Marriage brings happiness. Partner may be motherly.",
      8: "Deep emotions, interest in mysticism. Mother's transformation. Inheritance from mother.",
      9: "Blessed by mother, spiritual emotions. Fortune through women. Intuitive dharma.",
      10: "Public career, popularity. Mother's influence on profession. Emotional achievements.",
      11: "Gains through women or public. Emotional fulfillment of desires. Elder sibling may be caring.",
      12: "Spiritual emotions, losses through women. Foreign mother connections. Bed pleasures."
    }
    // Add more planets as needed
  };

  const planetInterp = interpretations[planet];
  if (planetInterp && planetInterp[house]) {
    return planetInterp[house];
  }

  return `${planet} in ${house}${house === 1 ? 'st' : house === 2 ? 'nd' : house === 3 ? 'rd' : 'th'} house influences matters of ${HOUSE_MEANINGS[house]}`;
}

/**
 * Generate overall chart summary
 */
export function generateChartSummary(chartData: any): {
  ascendant: string;
  strengths: string[];
  challenges: string[];
  lifeTheme: string;
} {
  const ascSign = chartData?.houses?.ascendant?.sign || 'Unknown';
  
  return {
    ascendant: ASCENDANT_TRAITS[ascSign] || 'Unique individual with special karmic path.',
    strengths: [
      'Natural talents indicated by strong planetary placements',
      'Fortunate areas shown by benefic influences',
      'Areas of easy growth and success'
    ],
    challenges: [
      'Areas requiring effort and patience',
      'Karmic lessons to be learned',
      'Obstacles that promote growth'
    ],
    lifeTheme: `With ${ascSign} ascendant, your life journey focuses on ${ascSign === 'Aries' ? 'leadership and pioneering new paths' : ascSign === 'Taurus' ? 'building stability and material security' : ascSign === 'Gemini' ? 'communication and versatile learning' : ascSign === 'Cancer' ? 'emotional security and nurturing others' : ascSign === 'Leo' ? 'creative self-expression and leadership' : ascSign === 'Virgo' ? 'service, health, and perfection' : ascSign === 'Libra' ? 'balance, relationships, and harmony' : ascSign === 'Scorpio' ? 'transformation and deep understanding' : ascSign === 'Sagittarius' ? 'wisdom, truth, and higher learning' : ascSign === 'Capricorn' ? 'discipline, career, and achievement' : ascSign === 'Aquarius' ? 'innovation and humanitarian service' : 'spiritual growth and compassion'}.`
  };
}
