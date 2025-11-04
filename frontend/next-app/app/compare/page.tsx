"use client";
import { useState } from 'react';
import { useRouter } from 'next/navigation';
import Header from '../../src/components/Header';
import BirthDetailsForm, { BirthDetails } from '../../src/components/BirthDetailsForm';
import SouthIndianChart from '../../src/components/SouthIndianChart';
import { calculateChart } from '../../src/lib/api';
import { calculateAshtakoot, type AshtakootResult } from '../../src/lib/ashtakoot';
import styles from './page.module.css';

export default function ComparePage() {
  const router = useRouter();
  const [chart1, setChart1] = useState<{details: BirthDetails; data: any} | null>(null);
  const [chart2, setChart2] = useState<{details: BirthDetails; data: any} | null>(null);
  const [loading, setLoading] = useState<1 | 2 | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (chartNum: 1 | 2, details: BirthDetails) => {
    setLoading(chartNum);
    setError(null);

    try {
      const dateTime = `${details.date}T${details.time}:00Z`;
      
      const data = await calculateChart({
        date_time: dateTime,
        latitude: details.latitude,
        longitude: details.longitude,
        altitude: 0,
        ayanamsa_type: details.ayanamsa_type,
        house_system: details.house_system,
      });

      if (chartNum === 1) {
        setChart1({ details, data });
      } else {
        setChart2({ details, data });
      }
    } catch (e: any) {
      setError(`Failed to calculate Chart ${chartNum}: ${e?.message || String(e)}`);
    } finally {
      setLoading(null);
    }
  };

  const getAshtakootResults = (): AshtakootResult | null => {
    if (!chart1 || !chart2) return null;

    try {
      return calculateAshtakoot(chart1.data, chart2.data);
    } catch (error) {
      console.error('Ashtakoot calculation error:', error);
      return null;
    }
  };

  const calculateCompatibility = (): { score: number; notes: string[] } => {
    if (!chart1 || !chart2) return { score: 0, notes: [] };

    const notes: string[] = [];
    let score = 0;

    // Compare ascendants
    const asc1 = chart1.data.houses?.ascendant?.sign_num || 0;
    const asc2 = chart2.data.houses?.ascendant?.sign_num || 0;
    
    if (asc1 && asc2) {
      const ascDiff = Math.abs(asc1 - asc2);
      if (ascDiff === 0) {
        score += 15;
        notes.push('✅ Same ascendant - excellent compatibility');
      } else if (ascDiff === 4 || ascDiff === 8) {
        score += 10;
        notes.push('✅ Ascendants in trine - good compatibility');
      } else if (ascDiff === 6) {
        score += 5;
        notes.push('⚠️ Opposite ascendants - challenging but balanced');
      }
    }

    // Compare Moon signs
    const moon1Sign = chart1.data.planetary_positions?.Moon?.sign_num || 0;
    const moon2Sign = chart2.data.planetary_positions?.Moon?.sign_num || 0;
    
    if (moon1Sign && moon2Sign) {
      const moonDiff = Math.abs(moon1Sign - moon2Sign);
      if (moonDiff === 0) {
        score += 20;
        notes.push('💑 Same Moon sign - emotional harmony');
      } else if (moonDiff === 4 || moonDiff === 8) {
        score += 15;
        notes.push('💑 Moon signs in trine - emotional understanding');
      } else if (moonDiff === 6) {
        score += 5;
        notes.push('⚠️ Opposite Moon signs - needs effort');
      }
    }

    // Compare Venus positions (love & relationships)
    const venus1 = chart1.data.planetary_positions?.Venus?.sign_num || 0;
    const venus2 = chart2.data.planetary_positions?.Venus?.sign_num || 0;
    
    if (venus1 && venus2) {
      const venusDiff = Math.abs(venus1 - venus2);
      if (venusDiff === 0 || venusDiff === 4 || venusDiff === 8) {
        score += 15;
        notes.push('❤️ Venus compatibility - similar love languages');
      }
    }

    // Compare Mars positions (energy & passion)
    const mars1 = chart1.data.planetary_positions?.Mars?.sign_num || 0;
    const mars2 = chart2.data.planetary_positions?.Mars?.sign_num || 0;
    
    if (mars1 && mars2) {
      const marsDiff = Math.abs(mars1 - mars2);
      if (marsDiff === 0 || marsDiff === 4 || marsDiff === 8) {
        score += 10;
        notes.push('⚡ Mars compatibility - similar energy levels');
      }
    }

    // Sun sign compatibility
    const sun1 = chart1.data.planetary_positions?.Sun?.sign_num || 0;
    const sun2 = chart2.data.planetary_positions?.Sun?.sign_num || 0;
    
    if (sun1 && sun2) {
      const sunDiff = Math.abs(sun1 - sun2);
      if (sunDiff === 0) {
        score += 10;
        notes.push('☀️ Same Sun sign - similar life paths');
      } else if (sunDiff === 4 || sunDiff === 8) {
        score += 8;
        notes.push('☀️ Sun signs in trine - compatible personalities');
      }
    }

    // Jupiter compatibility (growth & wisdom)
    const jup1 = chart1.data.planetary_positions?.Jupiter?.sign_num || 0;
    const jup2 = chart2.data.planetary_positions?.Jupiter?.sign_num || 0;
    
    if (jup1 && jup2) {
      const jupDiff = Math.abs(jup1 - jup2);
      if (jupDiff === 0 || jupDiff === 4 || jupDiff === 8) {
        score += 10;
        notes.push('🌟 Jupiter compatibility - shared values');
      }
    }

    // Saturn compatibility (responsibility & commitment)
    const sat1 = chart1.data.planetary_positions?.Saturn?.sign_num || 0;
    const sat2 = chart2.data.planetary_positions?.Saturn?.sign_num || 0;
    
    if (sat1 && sat2) {
      const satDiff = Math.abs(sat1 - sat2);
      if (satDiff === 0 || satDiff === 4 || satDiff === 8) {
        score += 10;
        notes.push('⏳ Saturn compatibility - similar commitments');
      }
    }

    return { score, notes };
  };

  const compatibility = chart1 && chart2 ? calculateCompatibility() : null;
  const ashtakoot = getAshtakootResults();

  return (
    <>
      <Header />
      <main className={styles.container}>
        <div className={styles.header}>
          <h1>Chart Comparison</h1>
          <p>Compare two birth charts for synastry and compatibility analysis</p>
          <button onClick={() => router.push('/')} className={styles.backBtn}>
            ← Back to Calculator
          </button>
        </div>

        {error && (
          <div className={styles.error}>
            <strong>Error:</strong> {error}
          </div>
        )}

        <div className={styles.formsGrid}>
          {/* Chart 1 */}
          <div className={styles.formSection}>
            <h2>Person 1</h2>
            <BirthDetailsForm
              onSubmit={(details) => handleSubmit(1, details)}
              loading={loading === 1}
            />
          </div>

          {/* Chart 2 */}
          <div className={styles.formSection}>
            <h2>Person 2</h2>
            <BirthDetailsForm
              onSubmit={(details) => handleSubmit(2, details)}
              loading={loading === 2}
            />
          </div>
        </div>

        {/* Compatibility Score */}
        {compatibility && (
          <div className={styles.compatibilitySection}>
            <h2>Compatibility Analysis</h2>
            
            <div className={styles.scoreCard}>
              <div className={styles.scoreCircle}>
                <div className={styles.scoreValue}>{compatibility.score}</div>
                <div className={styles.scoreLabel}>out of 100</div>
              </div>
              
              <div className={styles.scoreDescription}>
                {compatibility.score >= 75 && (
                  <>
                    <h3>Excellent Compatibility! 🎉</h3>
                    <p>Strong harmonious connection with great potential</p>
                  </>
                )}
                {compatibility.score >= 50 && compatibility.score < 75 && (
                  <>
                    <h3>Good Compatibility 👍</h3>
                    <p>Positive connection with some areas to work on</p>
                  </>
                )}
                {compatibility.score >= 30 && compatibility.score < 50 && (
                  <>
                    <h3>Moderate Compatibility ⚖️</h3>
                    <p>Challenges present but can work with effort</p>
                  </>
                )}
                {compatibility.score < 30 && (
                  <>
                    <h3>Challenging Compatibility ⚠️</h3>
                    <p>Significant differences that need understanding</p>
                  </>
                )}
              </div>
            </div>

            <div className={styles.notesSection}>
              <h3>Detailed Analysis</h3>
              <ul className={styles.notesList}>
                {compatibility.notes.map((note, idx) => (
                  <li key={idx}>{note}</li>
                ))}
              </ul>
            </div>
          </div>
        )}

        {/* Ashtakoot Matching (36 Points) */}
        {ashtakoot && (
          <div className={styles.ashtakootSection}>
            <h2>🔮 Ashtakoot Matching (Traditional 36-Point System)</h2>
            
            <div className={styles.ashtakootScore}>
              <div className={styles.mainScore}>
                <div className={styles.scoreCircle}>
                  <div className={styles.scoreValue}>{ashtakoot.total}</div>
                  <div className={styles.scoreLabel}>out of 36</div>
                </div>
                <div className={styles.percentage}>{ashtakoot.percentage.toFixed(1)}%</div>
                <div className={`${styles.compatibilityBadge} ${styles[ashtakoot.compatibility.toLowerCase().replace(' ', '')]}`}>
                  {ashtakoot.compatibility}
                </div>
              </div>
              
              <div className={styles.recommendation}>
                <h3>Recommendation</h3>
                <p>{ashtakoot.recommendation}</p>
              </div>
            </div>

            <div className={styles.ashtakootDetails}>
              <div className={styles.kootaGrid}>
                {/* Varna */}
                <div className={styles.kootaCard}>
                  <div className={styles.kootaHeader}>
                    <h4>1. Varna (Caste)</h4>
                    <span className={styles.kootaScore}>
                      {ashtakoot.varna.points}/{ashtakoot.varna.maxPoints}
                    </span>
                  </div>
                  <p>{ashtakoot.varna.description}</p>
                </div>

                {/* Vashya */}
                <div className={styles.kootaCard}>
                  <div className={styles.kootaHeader}>
                    <h4>2. Vashya (Attraction)</h4>
                    <span className={styles.kootaScore}>
                      {ashtakoot.vashya.points}/{ashtakoot.vashya.maxPoints}
                    </span>
                  </div>
                  <p>{ashtakoot.vashya.description}</p>
                </div>

                {/* Tara */}
                <div className={styles.kootaCard}>
                  <div className={styles.kootaHeader}>
                    <h4>3. Tara (Birth Star)</h4>
                    <span className={styles.kootaScore}>
                      {ashtakoot.tara.points}/{ashtakoot.tara.maxPoints}
                    </span>
                  </div>
                  <p>{ashtakoot.tara.description}</p>
                </div>

                {/* Yoni */}
                <div className={styles.kootaCard}>
                  <div className={styles.kootaHeader}>
                    <h4>4. Yoni (Physical)</h4>
                    <span className={styles.kootaScore}>
                      {ashtakoot.yoni.points}/{ashtakoot.yoni.maxPoints}
                    </span>
                  </div>
                  <p>{ashtakoot.yoni.description}</p>
                </div>

                {/* Graha Maitri */}
                <div className={styles.kootaCard}>
                  <div className={styles.kootaHeader}>
                    <h4>5. Graha Maitri (Mental)</h4>
                    <span className={styles.kootaScore}>
                      {ashtakoot.graha_maitri.points}/{ashtakoot.graha_maitri.maxPoints}
                    </span>
                  </div>
                  <p>{ashtakoot.graha_maitri.description}</p>
                </div>

                {/* Gana */}
                <div className={styles.kootaCard}>
                  <div className={styles.kootaHeader}>
                    <h4>6. Gana (Temperament)</h4>
                    <span className={styles.kootaScore}>
                      {ashtakoot.gana.points}/{ashtakoot.gana.maxPoints}
                    </span>
                  </div>
                  <p>{ashtakoot.gana.description}</p>
                </div>

                {/* Bhakoot */}
                <div className={styles.kootaCard}>
                  <div className={styles.kootaHeader}>
                    <h4>7. Bhakoot (Rasi)</h4>
                    <span className={styles.kootaScore}>
                      {ashtakoot.bhakoot.points}/{ashtakoot.bhakoot.maxPoints}
                    </span>
                  </div>
                  <p>{ashtakoot.bhakoot.description}</p>
                </div>

                {/* Nadi */}
                <div className={`${styles.kootaCard} ${ashtakoot.nadi.points === 0 ? styles.critical : ''}`}>
                  <div className={styles.kootaHeader}>
                    <h4>8. Nadi (Health/Genes) ⚠️</h4>
                    <span className={styles.kootaScore}>
                      {ashtakoot.nadi.points}/{ashtakoot.nadi.maxPoints}
                    </span>
                  </div>
                  <p>{ashtakoot.nadi.description}</p>
                  {ashtakoot.nadi.points === 0 && (
                    <div className={styles.criticalWarning}>
                      <strong>⚠️ IMPORTANT:</strong> Nadi dosha is considered very serious in traditional matching.
                      Please consult an experienced astrologer for exceptions and remedies.
                    </div>
                  )}
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Charts Display */}
        {(chart1 || chart2) && (
          <div className={styles.chartsGrid}>
            {chart1 && (
              <div className={styles.chartCard}>
                <h3>{chart1.details.locationName}</h3>
                <p className={styles.chartDate}>
                  {chart1.details.date} {chart1.details.time}
                </p>
                <div className={styles.chartDisplay}>
                  <SouthIndianChart data={chart1.data} size={450} />
                </div>
                <div className={styles.chartInfo}>
                  <p><strong>Ascendant:</strong> {chart1.data.houses?.ascendant?.sign}</p>
                  <p><strong>Moon:</strong> {chart1.data.planetary_positions?.Moon?.sign}</p>
                  <p><strong>Sun:</strong> {chart1.data.planetary_positions?.Sun?.sign}</p>
                </div>
              </div>
            )}

            {chart2 && (
              <div className={styles.chartCard}>
                <h3>{chart2.details.locationName}</h3>
                <p className={styles.chartDate}>
                  {chart2.details.date} {chart2.details.time}
                </p>
                <div className={styles.chartDisplay}>
                  <SouthIndianChart data={chart2.data} size={450} />
                </div>
                <div className={styles.chartInfo}>
                  <p><strong>Ascendant:</strong> {chart2.data.houses?.ascendant?.sign}</p>
                  <p><strong>Moon:</strong> {chart2.data.planetary_positions?.Moon?.sign}</p>
                  <p><strong>Sun:</strong> {chart2.data.planetary_positions?.Sun?.sign}</p>
                </div>
              </div>
            )}
          </div>
        )}
      </main>
    </>
  );
}
