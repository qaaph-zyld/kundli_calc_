"""
Chart Interpretation Methodology
================================

A systematic approach to reading Vedic charts based on classical principles.
This follows the traditional Parashara system taught by masters.

"First understand the WHOLE, then analyze the PARTS"
"""

from dataclasses import dataclass
from typing import Dict, List, Optional

# =============================================================================
# THE 10-STEP CHART READING METHODOLOGY
# =============================================================================

INTERPRETATION_STEPS = """
╔══════════════════════════════════════════════════════════════════════════════╗
║                    SYSTEMATIC CHART INTERPRETATION                            ║
║                      (Parashara Method - 10 Steps)                           ║
╚══════════════════════════════════════════════════════════════════════════════╝

STEP 1: ASCENDANT ANALYSIS (Lagna Vichar)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
The Lagna is the FOUNDATION of the entire chart. It represents:
• Physical body and constitution
• Overall life direction and personality
• How the world perceives you
• Starting point for all house calculations

Check:
□ Sign rising - element, modality, nature
□ Degree of Lagna - early/middle/late
□ Lagna lord - sign, house, dignity, aspects
□ Planets in 1st house
□ Aspects to Lagna and Lagna lord
□ Navamsa Lagna - inner nature, destiny

Example Analysis:
- Gemini Lagna → Mercury ruled, Air sign, Dual nature
- Mercury in 12th → Lagna lord in house of loss/spirituality
- Strong Mercury → intellectual, communicative, adaptable
- Weak Mercury → scattered, nervous, indecisive


STEP 2: MOON ANALYSIS (Chandra Vichar)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Moon is the MIND - equally important as Lagna.

Check:
□ Moon sign (Rashi) - emotional nature
□ Moon nakshatra - deeper psychological patterns
□ Moon house - where mind focuses
□ Moon dignity - exalted/debilitated/own
□ Planets conjunct Moon - mental influences
□ Moon's paksha - waxing (strong) or waning (weak)

Key Points:
- Strong Moon = emotional stability, good memory, public success
- Weak Moon = mental anxiety, mood swings, mother issues
- Moon determines Vimshottari Dasha starting point


STEP 3: SUN ANALYSIS (Surya Vichar)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Sun is the SOUL and VITALITY.

Check:
□ Sun sign - core identity, ego expression
□ Sun house - area of life seeking recognition
□ Sun dignity - confidence level
□ Sun aspects - authority figures, father
□ Combustion - planets too close to Sun

Key Points:
- Strong Sun = leadership, confidence, father blessing
- Weak Sun = low vitality, ego issues, government troubles
- Sun in 10th/1st = natural leadership


STEP 4: YOGA IDENTIFICATION (Yoga Vichar)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Yogas are planetary combinations that modify results.

Priority Yogas to Check:
□ Pancha Mahapurusha Yogas (5 great person yogas)
  - Hamsa (Jupiter in kendra in own/exalted)
  - Malavya (Venus in kendra in own/exalted)
  - Bhadra (Mercury in kendra in own/exalted)
  - Ruchaka (Mars in kendra in own/exalted)
  - Shasha (Saturn in kendra in own/exalted)

□ Raja Yogas (power combinations)
  - Kendra-Trikona lord conjunction/exchange
  - 9th + 10th lord connection
  - 5th + 9th lord connection

□ Dhana Yogas (wealth combinations)
  - 2nd + 11th lord connection
  - 5th + 9th lord with 2nd/11th

□ Negative Yogas
  - Kemadruma (Moon isolated)
  - Shakata (Jupiter 6/8 from Moon)
  - Daridra (poverty yogas)


STEP 5: HOUSE ANALYSIS (Bhava Vichar)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Analyze each house for specific life areas.

For Each Important House, Check:
□ Sign in house - quality of that life area
□ House lord - where results manifest
□ Planets in house - energies active there
□ Aspects to house - external influences
□ Karaka (significator) condition

House Priority by Query:
- Career: 10th, 2nd, 11th, 6th
- Marriage: 7th, 2nd, 4th, Venus
- Children: 5th, Jupiter, 9th
- Health: 1st, 6th, 8th, Sun
- Wealth: 2nd, 11th, 5th, 9th
- Spirituality: 9th, 12th, 5th, Jupiter


STEP 6: PLANETARY STRENGTH (Bala Vichar)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Assess the strength of key planets.

Quick Strength Assessment:
□ Dignity (exalted → debilitated)
□ House placement (kendra > trikona > upachaya > dusthana)
□ Aspects received (benefic vs malefic)
□ Combustion (too close to Sun)
□ Retrograde status
□ Nakshatra lord strength
□ Navamsa position (vargottama = strong)

Shadbala Components (if calculating):
1. Sthana Bala (positional)
2. Dig Bala (directional)
3. Kala Bala (temporal)
4. Chesta Bala (motional)
5. Naisargika Bala (natural)
6. Drik Bala (aspectual)


STEP 7: DIVISIONAL CHARTS (Varga Vichar)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Confirm D1 findings in relevant vargas.

Key Divisional Charts:
□ D9 (Navamsa) - MOST IMPORTANT
  - Marriage, dharma, fortune
  - Confirms or denies D1 promise
  - Check: Navamsa Lagna, 7th house, Venus/Jupiter

□ D10 (Dasamsa) - Career
  - Professional success and status
  - Check: 10th house, Saturn, Sun, Mercury

□ D4 (Chaturthamsa) - Property
  - Fixed assets, vehicles, happiness
  - Check: 4th house, Moon, Venus

□ D7 (Saptamsa) - Children
  - Progeny and creativity
  - Check: 5th house, Jupiter

□ D12 (Dwadasamsa) - Parents
  - Father (9th), Mother (4th)


STEP 8: DASHA ANALYSIS (Dasha Vichar)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Timing is everything - when will results manifest?

Vimshottari Dasha Analysis:
□ Current Mahadasha lord
  - Its strength in D1 and D9
  - Houses it rules
  - Houses it occupies
  - Planets it's conjunct/aspected by

□ Current Antardasha lord
  - Same analysis as above
  - Relationship with Mahadasha lord

□ Pratyantara (sub-sub) for fine timing

Dasha Interpretation Rules:
- Planet gives results of houses it RULES
- Planet gives results of house it OCCUPIES
- Planet gives results of planets it's CONJUNCT
- Strong planet = good results in its dasha
- Weak planet = struggles in its dasha


STEP 9: TRANSIT ANALYSIS (Gochara Vichar)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Current planetary positions affecting the chart.

Key Transits to Watch:
□ Saturn transit (2.5 years per sign)
  - Sade Sati (7.5 year Saturn over Moon)
  - Saturn return (age 29-30, 58-60)
  - Saturn over natal planets

□ Jupiter transit (1 year per sign)
  - Jupiter return (every 12 years)
  - Jupiter over Lagna/Moon
  - Jupiter aspecting key houses

□ Rahu-Ketu transit (1.5 years per sign)
  - Nodal return (every 18 years)
  - Rahu/Ketu over natal positions


STEP 10: SYNTHESIS & PREDICTION (Phaladesha)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Bring it all together for final judgment.

Synthesis Rules:
□ Multiple factors confirming = STRONG prediction
□ Mixed factors = MODERATE prediction
□ Single factor alone = WEAK prediction

Always Consider:
- Dasha activating the yoga/combination
- Transit supporting the dasha
- Divisional charts confirming
- Overall chart strength (strong vs weak chart)

Final Questions:
1. What is the PROMISE of the chart? (natal potential)
2. WHEN will it manifest? (dasha + transit)
3. HOW MUCH will manifest? (strength assessment)
4. What OBSTACLES exist? (afflictions, dusthana lords)
"""

# =============================================================================
# SPECIFIC LIFE AREA ANALYSIS
# =============================================================================

CAREER_ANALYSIS = """
╔══════════════════════════════════════════════════════════════════════════════╗
║                           CAREER ANALYSIS                                     ║
╚══════════════════════════════════════════════════════════════════════════════╝

PRIMARY FACTORS:
━━━━━━━━━━━━━━━━
1. 10th House (Karma Bhava)
   - Sign in 10th = nature of career
   - Planets in 10th = career activators
   - 10th lord placement = where career manifests

2. 10th Lord Analysis
   - Strength of 10th lord
   - House placement of 10th lord
   - Conjunctions and aspects

3. D10 (Dasamsa) Chart
   - 10th house in D10
   - Lagna lord in D10
   - Position of D1 10th lord in D10

CAREER INDICATORS BY PLANET:
━━━━━━━━━━━━━━━━━━━━━━━━━━━
Sun strong: Government, politics, medicine, administration
Moon strong: Public dealing, hospitality, nursing, psychology
Mars strong: Military, police, surgery, engineering, sports
Mercury strong: Business, writing, IT, accounting, teaching
Jupiter strong: Law, education, finance, consulting, religion
Venus strong: Arts, entertainment, luxury goods, hospitality
Saturn strong: Mining, labor, construction, agriculture, service
Rahu strong: Foreign, technology, unconventional, research
Ketu strong: Spiritual, healing, research, investigation

10TH HOUSE SIGN CAREERS:
━━━━━━━━━━━━━━━━━━━━━━━━
Aries 10th: Pioneering, leadership, military, sports
Taurus 10th: Banking, arts, agriculture, beauty
Gemini 10th: Communication, media, trading, writing
Cancer 10th: Real estate, food, nurturing professions
Leo 10th: Government, entertainment, management
Virgo 10th: Healthcare, service, analysis, editing
Libra 10th: Law, diplomacy, arts, partnerships
Scorpio 10th: Research, investigation, occult, transformation
Sagittarius 10th: Education, law, publishing, travel
Capricorn 10th: Corporate, government, traditional business
Aquarius 10th: Technology, social work, innovation
Pisces 10th: Healing, arts, spirituality, charity
"""

MARRIAGE_ANALYSIS = """
╔══════════════════════════════════════════════════════════════════════════════╗
║                          MARRIAGE ANALYSIS                                    ║
╚══════════════════════════════════════════════════════════════════════════════╝

PRIMARY FACTORS:
━━━━━━━━━━━━━━━━
1. 7th House (Kalatra Bhava)
   - Sign = type of spouse
   - Planets = energies in marriage
   - 7th lord = marriage destiny

2. Venus (for males) / Jupiter (for females)
   - Natural significator of spouse
   - Strength and placement crucial

3. Navamsa (D9) Chart
   - 7th house in D9
   - D9 Lagna = inner self in relationship
   - Venus/Jupiter in D9

SPOUSE CHARACTERISTICS BY 7TH SIGN:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Aries 7th: Independent, assertive, athletic spouse
Taurus 7th: Beautiful, sensual, stable spouse
Gemini 7th: Intellectual, communicative spouse
Cancer 7th: Nurturing, emotional, family-oriented spouse
Leo 7th: Proud, generous, dramatic spouse
Virgo 7th: Practical, service-oriented, critical spouse
Libra 7th: Balanced, artistic, diplomatic spouse
Scorpio 7th: Intense, transformative, secretive spouse
Sagittarius 7th: Philosophical, adventurous spouse
Capricorn 7th: Mature, ambitious, traditional spouse
Aquarius 7th: Unconventional, friendly, detached spouse
Pisces 7th: Spiritual, artistic, sacrificing spouse

TIMING OF MARRIAGE:
━━━━━━━━━━━━━━━━━━
- Dasha of 7th lord or Venus
- Transit Jupiter aspecting 7th house
- Transit Saturn forming relationship with 7th
- Age indicated by 7th lord (count from Lagna)

MARRIAGE OBSTACLES:
━━━━━━━━━━━━━━━━━━
- Malefics in 7th house
- 7th lord in dusthana (6, 8, 12)
- Venus combust or debilitated
- Mangal Dosha (Mars in 1, 2, 4, 7, 8, 12)
- Saturn aspect on 7th house/lord
"""

HEALTH_ANALYSIS = """
╔══════════════════════════════════════════════════════════════════════════════╗
║                           HEALTH ANALYSIS                                     ║
╚══════════════════════════════════════════════════════════════════════════════╝

PRIMARY FACTORS:
━━━━━━━━━━━━━━━━
1. Lagna & Lagna Lord
   - Physical constitution
   - Overall vitality

2. 6th House (Disease)
   - Types of illness
   - Enemies and obstacles

3. 8th House (Longevity)
   - Chronic conditions
   - Transformation and death

4. Sun (Vitality)
   - Life force, heart, eyes
   - Father's health influence

5. Moon (Mind & Fluids)
   - Mental health
   - Bodily fluids, emotions

BODY PARTS BY SIGN:
━━━━━━━━━━━━━━━━━━━
Aries: Head, brain, face
Taurus: Throat, neck, thyroid
Gemini: Shoulders, arms, lungs
Cancer: Chest, breast, stomach
Leo: Heart, spine, upper back
Virgo: Intestines, nervous system
Libra: Kidneys, lower back, skin
Scorpio: Reproductive organs, bladder
Sagittarius: Hips, thighs, liver
Capricorn: Knees, bones, joints
Aquarius: Ankles, calves, circulation
Pisces: Feet, lymphatic system

DISEASE INDICATORS:
━━━━━━━━━━━━━━━━━━
- Malefics in 6th = chronic disease
- 6th lord in Lagna = health issues
- Weak Lagna lord = low immunity
- Saturn afflicting Moon = depression
- Mars afflicting = inflammation, surgery
- Rahu/Ketu = mysterious ailments
"""

# =============================================================================
# PRACTICAL INTERPRETATION EXAMPLES
# =============================================================================


def get_interpretation_guide() -> str:
    """Return the complete interpretation methodology"""
    return INTERPRETATION_STEPS


def get_career_guide() -> str:
    """Return career analysis guide"""
    return CAREER_ANALYSIS


def get_marriage_guide() -> str:
    """Return marriage analysis guide"""
    return MARRIAGE_ANALYSIS


def get_health_guide() -> str:
    """Return health analysis guide"""
    return HEALTH_ANALYSIS
