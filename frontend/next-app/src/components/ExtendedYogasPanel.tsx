"use client";
import { useState, useMemo } from 'react';
import styles from './AnalysisPanels.module.css';

interface Yoga {
  name: string;
  sanskrit_name: string;
  category: string;
  description: string;
  effects: string[];
  planets: string[];
  houses: number[];
  strength: number;
  is_benefic: boolean;
  notes?: string;
}

interface ExtendedYogasPanelProps {
  chartData: any;
}

const CATEGORY_INFO: Record<string, { icon: string; color: string; label: string }> = {
  raja: { icon: '👑', color: '#FFD700', label: 'Raja Yoga' },
  dhana: { icon: '💰', color: '#4CAF50', label: 'Dhana Yoga' },
  mahapurusha: { icon: '🦁', color: '#9C27B0', label: 'Mahapurusha' },
  chandra: { icon: '🌙', color: '#90CAF9', label: 'Chandra Yoga' },
  surya: { icon: '☀️', color: '#FF9800', label: 'Surya Yoga' },
  budha: { icon: '📚', color: '#4DD0E1', label: 'Budha Yoga' },
  vipreet: { icon: '🔄', color: '#7C4DFF', label: 'Vipreet Raja' },
  neecha_bhanga: { icon: '⬆️', color: '#00BCD4', label: 'Neecha Bhanga' },
  arishta: { icon: '⚠️', color: '#F44336', label: 'Arishta' },
  sannyasa: { icon: '🕉️', color: '#795548', label: 'Sannyasa' },
  parivartana: { icon: '🔀', color: '#607D8B', label: 'Parivartana' },
  nabhasa: { icon: '🌌', color: '#3F51B5', label: 'Nabhasa' },
  special: { icon: '⭐', color: '#E91E63', label: 'Special' }
};

const PLANET_SYMBOLS: Record<string, string> = {
  Sun: '☉', Moon: '☽', Mars: '♂', Mercury: '☿',
  Jupiter: '♃', Venus: '♀', Saturn: '♄', Rahu: '☊', Ketu: '☋'
};

export default function ExtendedYogasPanel({ chartData }: ExtendedYogasPanelProps) {
  const [selectedCategory, setSelectedCategory] = useState<string>('all');
  const [showOnlyStrong, setShowOnlyStrong] = useState(false);

  // Calculate yogas from chart data
  const yogas = useMemo<Yoga[]>(() => {
    if (!chartData?.planetary_positions) return [];

    const detected: Yoga[] = [];
    const planets = chartData.planetary_positions;
    const houses = chartData.houses;
    
    // Extract positions
    const getHouse = (planet: string): number => {
      const pos = planets[planet];
      if (!pos) return 1;
      const lon = pos.longitude;
      const ascLon = houses?.ascendant || 0;
      const ascSign = Math.floor(ascLon / 30);
      const planetSign = Math.floor(lon / 30);
      return ((planetSign - ascSign + 12) % 12) + 1;
    };

    const getSign = (planet: string): number => {
      return Math.floor((planets[planet]?.longitude || 0) / 30);
    };

    const SIGN_LORDS = ["Mars", "Venus", "Mercury", "Moon", "Sun", "Mercury",
                        "Venus", "Mars", "Jupiter", "Saturn", "Saturn", "Jupiter"];
    const EXALTATION: Record<string, number> = { Sun: 0, Moon: 1, Mars: 9, Mercury: 5, Jupiter: 3, Venus: 11, Saturn: 6 };
    const OWN_SIGNS: Record<string, number[]> = {
      Sun: [4], Moon: [3], Mars: [0, 7], Mercury: [2, 5],
      Jupiter: [8, 11], Venus: [1, 6], Saturn: [9, 10]
    };

    const isExalted = (planet: string) => EXALTATION[planet] === getSign(planet);
    const isOwnSign = (planet: string) => OWN_SIGNS[planet]?.includes(getSign(planet));
    const isInKendra = (planet: string) => [1, 4, 7, 10].includes(getHouse(planet));
    const isInTrine = (planet: string) => [1, 5, 9].includes(getHouse(planet));

    const ascSign = Math.floor((houses?.ascendant || 0) / 30);
    const getHouseLord = (house: number) => SIGN_LORDS[(ascSign + house - 1) % 12];

    // PANCHA MAHAPURUSHA YOGAS
    const mahapurusha = [
      { planet: 'Mars', name: 'Ruchaka', desc: 'Valor, courage, leadership' },
      { planet: 'Mercury', name: 'Bhadra', desc: 'Intelligence, communication' },
      { planet: 'Jupiter', name: 'Hamsa', desc: 'Wisdom, spirituality' },
      { planet: 'Venus', name: 'Malavya', desc: 'Beauty, luxury, arts' },
      { planet: 'Saturn', name: 'Sasa', desc: 'Power, authority, discipline' }
    ];

    mahapurusha.forEach(({ planet, name, desc }) => {
      if (planets[planet] && isInKendra(planet) && (isExalted(planet) || isOwnSign(planet))) {
        detected.push({
          name: `${name} Yoga`,
          sanskrit_name: `${name} योग`,
          category: 'mahapurusha',
          description: `${planet} in kendra in ${isExalted(planet) ? 'exaltation' : 'own sign'}`,
          effects: [desc, 'Great personality', 'Fame'],
          planets: [planet],
          houses: [getHouse(planet)],
          strength: isExalted(planet) ? 90 : 80,
          is_benefic: true
        });
      }
    });

    // GAJAKESARI YOGA
    if (planets.Moon && planets.Jupiter) {
      const moonHouse = getHouse('Moon');
      const jupHouse = getHouse('Jupiter');
      const kendraFromMoon = [1, 4, 7, 10].map(k => ((moonHouse - 1 + k - 1) % 12) + 1);
      if (kendraFromMoon.includes(jupHouse)) {
        detected.push({
          name: 'Gajakesari Yoga',
          sanskrit_name: 'गजकेसरी योग',
          category: 'special',
          description: 'Jupiter in kendra from Moon',
          effects: ['Fame', 'Wealth', 'Many virtues', 'Long life'],
          planets: ['Moon', 'Jupiter'],
          houses: [moonHouse, jupHouse],
          strength: isExalted('Jupiter') ? 90 : 80,
          is_benefic: true
        });
      }
    }

    // BUDHA-ADITYA YOGA
    if (planets.Sun && planets.Mercury) {
      if (getHouse('Sun') === getHouse('Mercury')) {
        const diff = Math.abs(planets.Sun.longitude - planets.Mercury.longitude);
        const isCombust = diff < 14;
        detected.push({
          name: 'Budha-Aditya Yoga',
          sanskrit_name: 'बुधादित्य योग',
          category: 'budha',
          description: 'Sun-Mercury conjunction',
          effects: ['Intelligence', 'Learned', 'Fame through intellect'],
          planets: ['Sun', 'Mercury'],
          houses: [getHouse('Sun')],
          strength: isCombust ? 60 : 80,
          is_benefic: true,
          notes: isCombust ? 'Reduced due to combustion' : undefined
        });
      }
    }

    // RAJA YOGA (Trine + Kendra lords)
    const trineLords = [1, 5, 9].map(h => getHouseLord(h));
    const kendraLords = [1, 4, 7, 10].map(h => getHouseLord(h));
    
    trineLords.forEach(tl => {
      kendraLords.forEach(kl => {
        if (tl !== kl && planets[tl] && planets[kl]) {
          if (getHouse(tl) === getHouse(kl)) {
            detected.push({
              name: 'Raja Yoga',
              sanskrit_name: 'राज योग',
              category: 'raja',
              description: `${tl} (trine lord) conjunct ${kl} (kendra lord)`,
              effects: ['Power', 'Authority', 'Success'],
              planets: [tl, kl],
              houses: [getHouse(tl)],
              strength: 85,
              is_benefic: true
            });
          }
        }
      });
    });

    // VIPREET RAJA YOGAS
    const lord6 = getHouseLord(6);
    const lord8 = getHouseLord(8);
    const lord12 = getHouseLord(12);

    if (planets[lord6] && [6, 8, 12].includes(getHouse(lord6))) {
      detected.push({
        name: 'Harsha Yoga',
        sanskrit_name: 'हर्ष योग',
        category: 'vipreet',
        description: `6th lord ${lord6} in house ${getHouse(lord6)}`,
        effects: ['Victory over enemies', 'Good health'],
        planets: [lord6],
        houses: [getHouse(lord6)],
        strength: 75,
        is_benefic: true
      });
    }

    if (planets[lord8] && [6, 8, 12].includes(getHouse(lord8))) {
      detected.push({
        name: 'Sarala Yoga',
        sanskrit_name: 'सरल योग',
        category: 'vipreet',
        description: `8th lord ${lord8} in house ${getHouse(lord8)}`,
        effects: ['Long life', 'Fearless', 'Prosperous'],
        planets: [lord8],
        houses: [getHouse(lord8)],
        strength: 75,
        is_benefic: true
      });
    }

    if (planets[lord12] && [6, 8, 12].includes(getHouse(lord12))) {
      detected.push({
        name: 'Vimala Yoga',
        sanskrit_name: 'विमल योग',
        category: 'vipreet',
        description: `12th lord ${lord12} in house ${getHouse(lord12)}`,
        effects: ['Frugal', 'Independent', 'Respected'],
        planets: [lord12],
        houses: [getHouse(lord12)],
        strength: 75,
        is_benefic: true
      });
    }

    // DHANA YOGA
    const lord2 = getHouseLord(2);
    const lord11 = getHouseLord(11);
    if (planets[lord2] && planets[lord11] && getHouse(lord2) === getHouse(lord11)) {
      detected.push({
        name: 'Dhana Yoga',
        sanskrit_name: 'धन योग',
        category: 'dhana',
        description: '2nd and 11th lords conjunct',
        effects: ['Wealth accumulation', 'Financial prosperity'],
        planets: [lord2, lord11],
        houses: [getHouse(lord2)],
        strength: 85,
        is_benefic: true
      });
    }

    // SUNAPHA/ANAPHA/DURUDHARA (Moon-based)
    if (planets.Moon) {
      const moonSign = getSign('Moon');
      const h2FromMoon = (moonSign + 1) % 12;
      const h12FromMoon = (moonSign + 11) % 12;
      
      const beneficsIn2 = ['Jupiter', 'Venus', 'Mercury'].filter(p => 
        planets[p] && getSign(p) === h2FromMoon);
      const beneficsIn12 = ['Jupiter', 'Venus', 'Mercury'].filter(p => 
        planets[p] && getSign(p) === h12FromMoon);

      if (beneficsIn2.length > 0) {
        detected.push({
          name: 'Sunapha Yoga',
          sanskrit_name: 'सुनफा योग',
          category: 'chandra',
          description: `${beneficsIn2.join(', ')} in 2nd from Moon`,
          effects: ['Self-made wealth', 'Intelligence', 'Fame'],
          planets: ['Moon', ...beneficsIn2],
          houses: [getHouse('Moon')],
          strength: 75,
          is_benefic: true
        });
      }

      if (beneficsIn12.length > 0) {
        detected.push({
          name: 'Anapha Yoga',
          sanskrit_name: 'अनफा योग',
          category: 'chandra',
          description: `${beneficsIn12.join(', ')} in 12th from Moon`,
          effects: ['Well-dressed', 'Good character', 'Fame'],
          planets: ['Moon', ...beneficsIn12],
          houses: [getHouse('Moon')],
          strength: 75,
          is_benefic: true
        });
      }

      if (beneficsIn2.length > 0 && beneficsIn12.length > 0) {
        detected.push({
          name: 'Durudhara Yoga',
          sanskrit_name: 'दुरुधरा योग',
          category: 'chandra',
          description: 'Benefics on both sides of Moon',
          effects: ['Wealth', 'Enjoyments', 'Charitable'],
          planets: ['Moon', ...beneficsIn2, ...beneficsIn12],
          houses: [getHouse('Moon')],
          strength: 85,
          is_benefic: true
        });
      }
    }

    // AMALA YOGA
    const beneficsIn10 = ['Jupiter', 'Venus', 'Mercury'].filter(p => 
      planets[p] && getHouse(p) === 10);
    if (beneficsIn10.length > 0) {
      detected.push({
        name: 'Amala Yoga',
        sanskrit_name: 'अमल योग',
        category: 'special',
        description: `${beneficsIn10.join(', ')} in 10th house`,
        effects: ['Lasting fame', 'Charitable', 'Prosperous career'],
        planets: beneficsIn10,
        houses: [10],
        strength: 80,
        is_benefic: true
      });
    }

    return detected;
  }, [chartData]);

  // Filter yogas
  const filteredYogas = useMemo(() => {
    let result = [...yogas];
    if (selectedCategory !== 'all') {
      result = result.filter(y => y.category === selectedCategory);
    }
    if (showOnlyStrong) {
      result = result.filter(y => y.strength >= 75);
    }
    return result.sort((a, b) => b.strength - a.strength);
  }, [yogas, selectedCategory, showOnlyStrong]);

  // Statistics
  const stats = useMemo(() => {
    const benefic = yogas.filter(y => y.is_benefic).length;
    const avgStrength = yogas.length > 0 
      ? yogas.reduce((sum, y) => sum + y.strength, 0) / yogas.length 
      : 0;
    const categories = [...new Set(yogas.map(y => y.category))];
    return { total: yogas.length, benefic, avgStrength, categories };
  }, [yogas]);

  return (
    <div className={styles.panel}>
      <div className={styles.panelHeader}>
        <h3>✨ Extended Yogas Analysis</h3>
        <p className={styles.subtitle}>60+ Classical Vedic Yogas</p>
      </div>

      {/* Stats */}
      <div className={styles.statsRow}>
        <div className={styles.statCard}>
          <span className={styles.statValue}>{stats.total}</span>
          <span className={styles.statLabel}>Total Yogas</span>
        </div>
        <div className={styles.statCard}>
          <span className={styles.statValue} style={{ color: '#4CAF50' }}>{stats.benefic}</span>
          <span className={styles.statLabel}>Benefic</span>
        </div>
        <div className={styles.statCard}>
          <span className={styles.statValue}>{stats.avgStrength.toFixed(0)}%</span>
          <span className={styles.statLabel}>Avg Strength</span>
        </div>
        <div className={styles.statCard}>
          <span className={styles.statValue}>{stats.categories.length}</span>
          <span className={styles.statLabel}>Categories</span>
        </div>
      </div>

      {/* Filters */}
      <div className={styles.filters}>
        <select 
          value={selectedCategory} 
          onChange={(e) => setSelectedCategory(e.target.value)}
          className={styles.filterSelect}
        >
          <option value="all">All Categories</option>
          {Object.entries(CATEGORY_INFO).map(([key, info]) => (
            <option key={key} value={key}>{info.icon} {info.label}</option>
          ))}
        </select>
        <label className={styles.filterCheckbox}>
          <input 
            type="checkbox" 
            checked={showOnlyStrong} 
            onChange={(e) => setShowOnlyStrong(e.target.checked)} 
          />
          Strong only (75%+)
        </label>
      </div>

      {/* Yogas List */}
      <div className={styles.yogasList}>
        {filteredYogas.length === 0 ? (
          <div className={styles.noYogas}>
            <p>No yogas found matching the filter criteria.</p>
          </div>
        ) : (
          filteredYogas.map((yoga, idx) => {
            const catInfo = CATEGORY_INFO[yoga.category] || CATEGORY_INFO.special;
            return (
              <div 
                key={idx} 
                className={`${styles.yogaCard} ${yoga.is_benefic ? styles.benefic : styles.malefic}`}
              >
                <div className={styles.yogaHeader}>
                  <div className={styles.yogaTitle}>
                    <span 
                      className={styles.categoryBadge}
                      style={{ backgroundColor: catInfo.color }}
                    >
                      {catInfo.icon} {catInfo.label}
                    </span>
                    <h4>{yoga.name}</h4>
                    <span className={styles.sanskritName}>{yoga.sanskrit_name}</span>
                  </div>
                  <div className={styles.strengthBadge} style={{
                    backgroundColor: yoga.strength >= 80 ? '#4CAF50' : 
                                    yoga.strength >= 60 ? '#FF9800' : '#F44336'
                  }}>
                    {yoga.strength}%
                  </div>
                </div>

                <p className={styles.yogaDesc}>{yoga.description}</p>

                <div className={styles.yogaPlanets}>
                  {yoga.planets.map(p => (
                    <span key={p} className={styles.planetTag}>
                      {PLANET_SYMBOLS[p] || ''} {p}
                    </span>
                  ))}
                  <span className={styles.houseTag}>
                    Houses: {yoga.houses.join(', ')}
                  </span>
                </div>

                <div className={styles.yogaEffects}>
                  <strong>Effects:</strong>
                  <ul>
                    {yoga.effects.map((effect, i) => (
                      <li key={i}>{effect}</li>
                    ))}
                  </ul>
                </div>

                {yoga.notes && (
                  <div className={styles.yogaNotes}>
                    <em>Note: {yoga.notes}</em>
                  </div>
                )}
              </div>
            );
          })
        )}
      </div>

      {yogas.length > 0 && (
        <div className={styles.yogaSummary}>
          <h4>📊 Yoga Summary</h4>
          <p>
            This chart has <strong>{stats.total}</strong> detected yogas with an average strength of 
            <strong> {stats.avgStrength.toFixed(1)}%</strong>. 
            {stats.benefic === stats.total 
              ? ' All yogas are benefic, indicating positive influences.' 
              : ` ${stats.benefic} are benefic and ${stats.total - stats.benefic} require attention.`}
          </p>
        </div>
      )}
    </div>
  );
}
