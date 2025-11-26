"use client";
import { useState, useMemo } from 'react';
import styles from './AnalysisPanels.module.css';

interface TransitDashboardProps {
  chartData: any;
  currentTransits?: Record<string, number>;
}

const PLANET_SYMBOLS: Record<string, string> = {
  Sun: '☉', Moon: '☽', Mars: '♂', Mercury: '☿',
  Jupiter: '♃', Venus: '♀', Saturn: '♄', Rahu: '☊', Ketu: '☋'
};

const SIGNS = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
               "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"];

// Gochara benefic houses from Moon
const GOCHARA_BENEFIC: Record<string, number[]> = {
  Sun: [3, 6, 10, 11],
  Moon: [1, 3, 6, 7, 10, 11],
  Mars: [3, 6, 11],
  Mercury: [2, 4, 6, 8, 10, 11],
  Jupiter: [2, 5, 7, 9, 11],
  Venus: [1, 2, 3, 4, 5, 8, 9, 11, 12],
  Saturn: [3, 6, 11],
  Rahu: [3, 6, 10, 11],
  Ketu: [3, 6, 10, 11]
};

interface GocharaResult {
  planet: string;
  transitSign: number;
  houseFromMoon: number;
  isBenefic: boolean;
  effects: string[];
}

interface SadeSatiStatus {
  isActive: boolean;
  phase: 'rising' | 'peak' | 'setting' | null;
  intensity: string;
  affectedHouses: number[];
}

export default function TransitDashboard({ chartData, currentTransits }: TransitDashboardProps) {
  const [activeView, setActiveView] = useState<'gochara' | 'sadesati' | 'predictions'>('gochara');

  // Get natal Moon sign
  const natalMoonSign = useMemo(() => {
    const moonLon = chartData?.planetary_positions?.Moon?.longitude || 0;
    return Math.floor(moonLon / 30);
  }, [chartData]);

  // Simulate current transits (in real app, would fetch from ephemeris)
  const transits = useMemo(() => {
    // Use provided transits or simulate approximate current positions
    if (currentTransits) return currentTransits;
    
    // Approximate Nov 2024 positions (for demo)
    return {
      Sun: 240,      // Scorpio
      Moon: 60,      // Gemini (changes daily)
      Mars: 95,      // Cancer
      Mercury: 255,  // Sagittarius
      Jupiter: 55,   // Taurus
      Venus: 280,    // Capricorn
      Saturn: 330,   // Pisces
      Rahu: 20,      // Aries
      Ketu: 200      // Libra
    };
  }, [currentTransits]);

  // Calculate Gochara results
  const gocharaResults = useMemo<GocharaResult[]>(() => {
    const results: GocharaResult[] = [];
    
    Object.entries(transits).forEach(([planet, lon]) => {
      const transitSign = Math.floor(lon / 30);
      const houseFromMoon = ((transitSign - natalMoonSign + 12) % 12) + 1;
      const beneficHouses = GOCHARA_BENEFIC[planet] || [];
      const isBenefic = beneficHouses.includes(houseFromMoon);
      
      const effects = getTransitEffects(planet, houseFromMoon, isBenefic);
      
      results.push({
        planet,
        transitSign,
        houseFromMoon,
        isBenefic,
        effects
      });
    });
    
    return results;
  }, [transits, natalMoonSign]);

  // Calculate Sade Sati status
  const sadeSati = useMemo<SadeSatiStatus>(() => {
    const saturnSign = Math.floor(transits.Saturn / 30);
    const houseFromMoon = ((saturnSign - natalMoonSign + 12) % 12) + 1;
    
    if (houseFromMoon === 12) {
      return { isActive: true, phase: 'rising', intensity: 'Light', affectedHouses: [12, 1] };
    } else if (houseFromMoon === 1) {
      return { isActive: true, phase: 'peak', intensity: 'Heavy', affectedHouses: [12, 1, 2] };
    } else if (houseFromMoon === 2) {
      return { isActive: true, phase: 'setting', intensity: 'Medium', affectedHouses: [1, 2, 3] };
    }
    
    return { isActive: false, phase: null, intensity: 'None', affectedHouses: [] };
  }, [transits, natalMoonSign]);

  // Overall transit score
  const transitScore = useMemo(() => {
    const benefic = gocharaResults.filter(r => r.isBenefic).length;
    const total = gocharaResults.length;
    const percentage = (benefic / total) * 100;
    
    let status = 'Mixed';
    if (percentage >= 70) status = 'Excellent';
    else if (percentage >= 55) status = 'Good';
    else if (percentage >= 40) status = 'Challenging';
    else status = 'Difficult';
    
    return { benefic, total, percentage, status };
  }, [gocharaResults]);

  return (
    <div className={styles.panel}>
      <div className={styles.panelHeader}>
        <h3>🌍 Transit Analysis (Gochara)</h3>
        <p className={styles.subtitle}>Current planetary transits from natal Moon</p>
      </div>

      {/* Sade Sati Alert */}
      {sadeSati.isActive && (
        <div className={`${styles.sadeSatiAlert} ${styles[sadeSati.phase || 'rising']}`}>
          <div className={styles.alertIcon}>🪐</div>
          <div className={styles.alertContent}>
            <h4>Sade Sati Active - {sadeSati.phase?.toUpperCase()} Phase</h4>
            <p>
              Saturn is transiting {sadeSati.phase === 'rising' ? '12th' : sadeSati.phase === 'peak' ? '1st' : '2nd'} 
              from your natal Moon. Intensity: <strong>{sadeSati.intensity}</strong>
            </p>
            <details>
              <summary>Remedies</summary>
              <ul>
                <li>Worship Lord Hanuman on Saturdays</li>
                <li>Recite Shani Stotram or Hanuman Chalisa</li>
                <li>Donate black sesame, iron, mustard oil</li>
                <li>Help the elderly and disabled</li>
                <li>Practice patience and discipline</li>
              </ul>
            </details>
          </div>
        </div>
      )}

      {/* Transit Score */}
      <div className={styles.transitScore}>
        <div className={styles.scoreCircle} style={{
          background: `conic-gradient(
            ${transitScore.percentage >= 60 ? '#4CAF50' : transitScore.percentage >= 40 ? '#FF9800' : '#F44336'} 
            ${transitScore.percentage * 3.6}deg, 
            #e0e0e0 0deg
          )`
        }}>
          <div className={styles.scoreInner}>
            <span className={styles.scoreValue}>{transitScore.percentage.toFixed(0)}%</span>
            <span className={styles.scoreLabel}>{transitScore.status}</span>
          </div>
        </div>
        <div className={styles.scoreDetails}>
          <p><strong>{transitScore.benefic}</strong> of {transitScore.total} planets in favorable transit</p>
          <p>Natal Moon: <strong>{SIGNS[natalMoonSign]}</strong></p>
        </div>
      </div>

      {/* View Tabs */}
      <div className={styles.tabNav}>
        <button 
          className={`${styles.tab} ${activeView === 'gochara' ? styles.active : ''}`}
          onClick={() => setActiveView('gochara')}
        >
          Gochara Table
        </button>
        <button 
          className={`${styles.tab} ${activeView === 'sadesati' ? styles.active : ''}`}
          onClick={() => setActiveView('sadesati')}
        >
          Sade Sati
        </button>
        <button 
          className={`${styles.tab} ${activeView === 'predictions' ? styles.active : ''}`}
          onClick={() => setActiveView('predictions')}
        >
          Predictions
        </button>
      </div>

      {/* Gochara Table */}
      {activeView === 'gochara' && (
        <div className={styles.tableContainer}>
          <table className={styles.transitTable}>
            <thead>
              <tr>
                <th>Planet</th>
                <th>Transit Sign</th>
                <th>House from Moon</th>
                <th>Result</th>
                <th>Effects</th>
              </tr>
            </thead>
            <tbody>
              {gocharaResults.map((result) => (
                <tr key={result.planet} className={result.isBenefic ? styles.beneficRow : styles.maleficRow}>
                  <td className={styles.planetCell}>
                    <span className={styles.planetSymbol}>{PLANET_SYMBOLS[result.planet]}</span>
                    {result.planet}
                  </td>
                  <td>{SIGNS[result.transitSign]}</td>
                  <td className={styles.houseCell}>{result.houseFromMoon}</td>
                  <td>
                    <span className={`${styles.resultBadge} ${result.isBenefic ? styles.good : styles.challenging}`}>
                      {result.isBenefic ? '✓ Favorable' : '⚠ Challenging'}
                    </span>
                  </td>
                  <td className={styles.effectsCell}>
                    {result.effects.slice(0, 2).join(', ')}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {/* Sade Sati Details */}
      {activeView === 'sadesati' && (
        <div className={styles.sadeSatiDetails}>
          <div className={styles.sadeSatiCard}>
            <h4>What is Sade Sati?</h4>
            <p>
              Sade Sati (साढ़े साती) is a 7.5 year period when Saturn transits through the 12th, 1st, and 2nd houses 
              from natal Moon. It occurs approximately every 29.5 years.
            </p>
          </div>

          <div className={styles.phaseCards}>
            <div className={`${styles.phaseCard} ${sadeSati.phase === 'rising' ? styles.activePhase : ''}`}>
              <h5>🌅 Rising Phase</h5>
              <p>Saturn in 12th from Moon</p>
              <p className={styles.phaseEffect}>Expenses increase, hidden enemies, need for introspection</p>
              <span className={styles.duration}>~2.5 years</span>
            </div>
            <div className={`${styles.phaseCard} ${sadeSati.phase === 'peak' ? styles.activePhase : ''}`}>
              <h5>🔝 Peak Phase</h5>
              <p>Saturn on natal Moon</p>
              <p className={styles.phaseEffect}>Most intense - mental stress, career challenges, health</p>
              <span className={styles.duration}>~2.5 years</span>
            </div>
            <div className={`${styles.phaseCard} ${sadeSati.phase === 'setting' ? styles.activePhase : ''}`}>
              <h5>🌅 Setting Phase</h5>
              <p>Saturn in 2nd from Moon</p>
              <p className={styles.phaseEffect}>Financial pressures, family matters, gradual relief</p>
              <span className={styles.duration}>~2.5 years</span>
            </div>
          </div>

          <div className={styles.currentStatus}>
            <h4>Your Status</h4>
            {sadeSati.isActive ? (
              <div className={styles.activeStatus}>
                <span className={styles.statusIcon}>🪐</span>
                <p>
                  You are currently in the <strong>{sadeSati.phase}</strong> phase of Sade Sati.
                  <br />Intensity: <strong>{sadeSati.intensity}</strong>
                </p>
              </div>
            ) : (
              <div className={styles.inactiveStatus}>
                <span className={styles.statusIcon}>✓</span>
                <p>Sade Sati is <strong>not active</strong> for your chart.</p>
              </div>
            )}
          </div>
        </div>
      )}

      {/* Predictions */}
      {activeView === 'predictions' && (
        <div className={styles.predictions}>
          <div className={styles.predictionCategories}>
            {[
              { area: 'Career', icon: '💼', planets: ['Saturn', 'Sun', 'Jupiter'] },
              { area: 'Relationships', icon: '💑', planets: ['Venus', 'Moon'] },
              { area: 'Finances', icon: '💰', planets: ['Jupiter', 'Venus'] },
              { area: 'Health', icon: '🏥', planets: ['Sun', 'Mars', 'Saturn'] }
            ].map(category => {
              const relevantResults = gocharaResults.filter(r => 
                category.planets.includes(r.planet));
              const favorable = relevantResults.filter(r => r.isBenefic).length;
              const outlook = favorable >= relevantResults.length / 2 ? 'positive' : 'cautious';
              
              return (
                <div key={category.area} className={styles.predictionCard}>
                  <div className={styles.predictionHeader}>
                    <span className={styles.predictionIcon}>{category.icon}</span>
                    <h4>{category.area}</h4>
                    <span className={`${styles.outlookBadge} ${styles[outlook]}`}>
                      {outlook === 'positive' ? '✓' : '⚠'}
                    </span>
                  </div>
                  <div className={styles.predictionPlanets}>
                    {relevantResults.map(r => (
                      <div key={r.planet} className={`${styles.miniTransit} ${r.isBenefic ? styles.good : styles.bad}`}>
                        <span>{PLANET_SYMBOLS[r.planet]}</span>
                        <span>{r.planet}</span>
                        <span>H{r.houseFromMoon}</span>
                      </div>
                    ))}
                  </div>
                  <p className={styles.predictionText}>
                    {outlook === 'positive' 
                      ? `Favorable period for ${category.area.toLowerCase()} matters.`
                      : `Exercise caution in ${category.area.toLowerCase()} decisions.`}
                  </p>
                </div>
              );
            })}
          </div>
        </div>
      )}

      <div className={styles.transitFooter}>
        <p>
          <strong>Note:</strong> Transit analysis shows current planetary positions from your natal Moon. 
          Results are modified by individual chart strength, dasha periods, and other factors.
        </p>
      </div>
    </div>
  );
}

function getTransitEffects(planet: string, house: number, isBenefic: boolean): string[] {
  const effectsMap: Record<string, { benefic: string[]; malefic: string[] }> = {
    Sun: { 
      benefic: ['Authority', 'Recognition', 'Vitality'], 
      malefic: ['Ego conflicts', 'Health issues'] 
    },
    Moon: { 
      benefic: ['Emotional peace', 'Public favor'], 
      malefic: ['Mental stress', 'Mood swings'] 
    },
    Mars: { 
      benefic: ['Energy', 'Courage', 'Victory'], 
      malefic: ['Conflicts', 'Accidents', 'Anger'] 
    },
    Mercury: { 
      benefic: ['Intelligence', 'Communication', 'Business'], 
      malefic: ['Confusion', 'Wrong decisions'] 
    },
    Jupiter: { 
      benefic: ['Wisdom', 'Expansion', 'Children'], 
      malefic: ['Overconfidence', 'Legal issues'] 
    },
    Venus: { 
      benefic: ['Love', 'Luxury', 'Arts'], 
      malefic: ['Relationship issues', 'Overspending'] 
    },
    Saturn: { 
      benefic: ['Discipline', 'Long-term gains'], 
      malefic: ['Delays', 'Hard work', 'Restrictions'] 
    },
    Rahu: { 
      benefic: ['Material gains', 'Innovation'], 
      malefic: ['Confusion', 'Illusions'] 
    },
    Ketu: { 
      benefic: ['Spirituality', 'Liberation'], 
      malefic: ['Losses', 'Detachment'] 
    }
  };

  const effects = effectsMap[planet] || { benefic: [], malefic: [] };
  return isBenefic ? effects.benefic : effects.malefic;
}
