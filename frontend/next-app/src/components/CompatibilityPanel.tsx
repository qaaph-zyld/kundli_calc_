"use client";
import { useState, useMemo } from 'react';
import styles from './AnalysisPanels.module.css';

interface CompatibilityPanelProps {
  chartData?: any;
}

const NAKSHATRAS = [
  "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra",
  "Punarvasu", "Pushya", "Ashlesha", "Magha", "Purva Phalguni", "Uttara Phalguni",
  "Hasta", "Chitra", "Swati", "Vishakha", "Anuradha", "Jyeshtha",
  "Mula", "Purva Ashadha", "Uttara Ashadha", "Shravana", "Dhanishta", "Shatabhisha",
  "Purva Bhadrapada", "Uttara Bhadrapada", "Revati"
];

const SIGNS = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
               "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"];

const NAKSHATRA_NADI = [
  "Aadi", "Madhya", "Antya", "Aadi", "Madhya", "Antya",
  "Aadi", "Madhya", "Antya", "Aadi", "Madhya", "Antya",
  "Aadi", "Madhya", "Antya", "Aadi", "Madhya", "Antya",
  "Aadi", "Madhya", "Antya", "Aadi", "Madhya", "Antya",
  "Aadi", "Madhya", "Antya"
];

const NAKSHATRA_GANA = [
  "Deva", "Manushya", "Rakshasa", "Manushya", "Deva", "Rakshasa",
  "Deva", "Deva", "Rakshasa", "Rakshasa", "Manushya", "Manushya",
  "Deva", "Rakshasa", "Deva", "Rakshasa", "Deva", "Rakshasa",
  "Rakshasa", "Manushya", "Manushya", "Deva", "Rakshasa", "Rakshasa",
  "Manushya", "Manushya", "Deva"
];

export default function CompatibilityPanel({ chartData }: CompatibilityPanelProps) {
  const [boyMoonLon, setBoyMoonLon] = useState<number>(chartData?.planetary_positions?.Moon?.longitude || 0);
  const [girlMoonLon, setGirlMoonLon] = useState<number>(90); // Default: Cancer
  const [showDetails, setShowDetails] = useState(false);

  // Calculate compatibility
  const compatibility = useMemo(() => {
    const boyNak = Math.floor(boyMoonLon / (360 / 27));
    const girlNak = Math.floor(girlMoonLon / (360 / 27));
    const boySign = Math.floor(boyMoonLon / 30);
    const girlSign = Math.floor(girlMoonLon / 30);

    const kootas = [];
    let totalPoints = 0;

    // 1. Varna (1 point)
    const varnaPoints = checkVarna(boySign, girlSign);
    totalPoints += varnaPoints;
    kootas.push({
      name: 'Varna',
      maxPoints: 1,
      obtained: varnaPoints,
      description: varnaPoints === 1 ? 'Compatible' : 'Boy\'s varna is lower'
    });

    // 2. Vashya (2 points)
    const vashyaPoints = checkVashya(boySign, girlSign);
    totalPoints += vashyaPoints;
    kootas.push({
      name: 'Vashya',
      maxPoints: 2,
      obtained: vashyaPoints,
      description: vashyaPoints >= 1.5 ? 'Good control' : 'Needs adjustment'
    });

    // 3. Tara (3 points)
    const taraPoints = checkTara(boyNak, girlNak);
    totalPoints += taraPoints;
    kootas.push({
      name: 'Tara',
      maxPoints: 3,
      obtained: taraPoints,
      description: taraPoints >= 2 ? 'Favorable destiny' : 'Some challenges'
    });

    // 4. Yoni (4 points)
    const yoniPoints = checkYoni(boyNak, girlNak);
    totalPoints += yoniPoints;
    kootas.push({
      name: 'Yoni',
      maxPoints: 4,
      obtained: yoniPoints,
      description: yoniPoints >= 3 ? 'Physical compatibility' : 'Differences in nature'
    });

    // 5. Graha Maitri (5 points)
    const maitriPoints = checkGrahaMaitri(boySign, girlSign);
    totalPoints += maitriPoints;
    kootas.push({
      name: 'Graha Maitri',
      maxPoints: 5,
      obtained: maitriPoints,
      description: maitriPoints >= 4 ? 'Friendly lords' : 'Lord compatibility low'
    });

    // 6. Gana (6 points)
    const ganaPoints = checkGana(boyNak, girlNak);
    totalPoints += ganaPoints;
    kootas.push({
      name: 'Gana',
      maxPoints: 6,
      obtained: ganaPoints,
      description: ganaPoints >= 5 ? 'Temperament match' : 'Different temperaments'
    });

    // 7. Bhakoot (7 points)
    const bhakootPoints = checkBhakoot(boySign, girlSign);
    totalPoints += bhakootPoints;
    kootas.push({
      name: 'Bhakoot',
      maxPoints: 7,
      obtained: bhakootPoints,
      description: bhakootPoints >= 5 ? 'Harmonious' : 'Bhakoot Dosha present'
    });

    // 8. Nadi (8 points)
    const nadiPoints = checkNadi(boyNak, girlNak);
    totalPoints += nadiPoints;
    kootas.push({
      name: 'Nadi',
      maxPoints: 8,
      obtained: nadiPoints,
      description: nadiPoints === 8 ? 'Different Nadi - Excellent' : 'Same Nadi - Dosha'
    });

    const percentage = (totalPoints / 36) * 100;

    // Doshas
    const doshas = [];
    if (nadiPoints === 0) {
      doshas.push({
        name: 'Nadi Dosha',
        severity: 'high',
        description: 'Same Nadi may affect progeny and health'
      });
    }
    if (bhakootPoints === 0) {
      doshas.push({
        name: 'Bhakoot Dosha',
        severity: 'high',
        description: '6-8 or 2-12 relationship between signs'
      });
    }

    // Recommendation
    let recommendation = '';
    if (totalPoints >= 28) {
      recommendation = 'Excellent match! Highly recommended.';
    } else if (totalPoints >= 21) {
      recommendation = 'Good match. Compatible for marriage.';
    } else if (totalPoints >= 18) {
      recommendation = 'Average. Consider remedies.';
    } else {
      recommendation = 'Below average. Strong remedies needed.';
    }

    return {
      totalPoints,
      maxPoints: 36,
      percentage,
      kootas,
      doshas,
      recommendation,
      boyDetails: {
        nakshatra: NAKSHATRAS[boyNak],
        sign: SIGNS[boySign],
        nadi: NAKSHATRA_NADI[boyNak],
        gana: NAKSHATRA_GANA[boyNak]
      },
      girlDetails: {
        nakshatra: NAKSHATRAS[girlNak],
        sign: SIGNS[girlSign],
        nadi: NAKSHATRA_NADI[girlNak],
        gana: NAKSHATRA_GANA[girlNak]
      }
    };
  }, [boyMoonLon, girlMoonLon]);

  return (
    <div className={styles.panel}>
      <div className={styles.panelHeader}>
        <h3>💑 Compatibility Analysis (Ashtakoot)</h3>
        <p className={styles.subtitle}>Traditional 36-point matching system</p>
      </div>

      {/* Input Section */}
      <div className={styles.currentDashaRow}>
        <div className={styles.currentDashaCard}>
          <span className={styles.dashaLabel}>Boy's Moon</span>
          <select
            value={Math.floor(boyMoonLon / 30)}
            onChange={(e) => setBoyMoonLon(parseInt(e.target.value) * 30 + 15)}
            className={styles.filterSelect}
            style={{ marginTop: '8px' }}
          >
            {SIGNS.map((sign, idx) => (
              <option key={sign} value={idx}>{sign}</option>
            ))}
          </select>
          <p style={{ fontSize: '0.8rem', marginTop: '4px', color: '#9e9e9e' }}>
            {compatibility.boyDetails.nakshatra}
          </p>
        </div>
        <div className={styles.currentDashaCard}>
          <span className={styles.dashaLabel}>Girl's Moon</span>
          <select
            value={Math.floor(girlMoonLon / 30)}
            onChange={(e) => setGirlMoonLon(parseInt(e.target.value) * 30 + 15)}
            className={styles.filterSelect}
            style={{ marginTop: '8px' }}
          >
            {SIGNS.map((sign, idx) => (
              <option key={sign} value={idx}>{sign}</option>
            ))}
          </select>
          <p style={{ fontSize: '0.8rem', marginTop: '4px', color: '#9e9e9e' }}>
            {compatibility.girlDetails.nakshatra}
          </p>
        </div>
      </div>

      {/* Score Display */}
      <div className={styles.transitScore}>
        <div 
          className={styles.scoreCircle}
          style={{
            background: `conic-gradient(${compatibility.percentage >= 70 ? '#4CAF50' : compatibility.percentage >= 50 ? '#FFC107' : '#F44336'} ${compatibility.percentage}%, rgba(255,255,255,0.1) 0%)`
          }}
        >
          <div className={styles.scoreInner}>
            <span className={styles.scoreValue}>{compatibility.totalPoints}</span>
            <span className={styles.scoreLabel}>/ 36 points</span>
          </div>
        </div>
        <div className={styles.scoreDetails}>
          <h4>{compatibility.percentage.toFixed(0)}% Compatible</h4>
          <p>{compatibility.recommendation}</p>
          {compatibility.doshas.length > 0 && (
            <p style={{ color: '#F44336' }}>
              ⚠️ {compatibility.doshas.length} dosha(s) detected
            </p>
          )}
        </div>
      </div>

      {/* Koota Details */}
      <div className={styles.tableContainer}>
        <table className={styles.kpTable}>
          <thead>
            <tr>
              <th>Koota</th>
              <th>Max</th>
              <th>Score</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            {compatibility.kootas.map((koota) => (
              <tr key={koota.name}>
                <td className={styles.planetCell}>{koota.name}</td>
                <td>{koota.maxPoints}</td>
                <td>
                  <strong>{koota.obtained}</strong>
                </td>
                <td>
                  <span className={`${styles.resultBadge} ${
                    koota.obtained >= koota.maxPoints * 0.6 ? styles.good : styles.challenging
                  }`}>
                    {koota.obtained >= koota.maxPoints * 0.6 ? '✓' : '✗'} {koota.description}
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Detailed Analysis */}
      <button 
        className={styles.tab}
        onClick={() => setShowDetails(!showDetails)}
        style={{ marginTop: '16px' }}
      >
        {showDetails ? 'Hide' : 'Show'} Detailed Analysis
      </button>

      {showDetails && (
        <div className={styles.comparison}>
          <div className={styles.comparisonTable}>
            <table>
              <thead>
                <tr>
                  <th>Attribute</th>
                  <th>Boy</th>
                  <th>Girl</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td>Moon Sign</td>
                  <td>{compatibility.boyDetails.sign}</td>
                  <td>{compatibility.girlDetails.sign}</td>
                </tr>
                <tr>
                  <td>Nakshatra</td>
                  <td>{compatibility.boyDetails.nakshatra}</td>
                  <td>{compatibility.girlDetails.nakshatra}</td>
                </tr>
                <tr>
                  <td>Nadi</td>
                  <td>{compatibility.boyDetails.nadi}</td>
                  <td>{compatibility.girlDetails.nadi}</td>
                </tr>
                <tr>
                  <td>Gana</td>
                  <td>{compatibility.boyDetails.gana}</td>
                  <td>{compatibility.girlDetails.gana}</td>
                </tr>
              </tbody>
            </table>
          </div>

          {/* Doshas */}
          {compatibility.doshas.length > 0 && (
            <div className={styles.sadeSatiAlert + ' ' + styles.peak}>
              <span className={styles.alertIcon}>⚠️</span>
              <div className={styles.alertContent}>
                <h4>Doshas Detected</h4>
                {compatibility.doshas.map((dosha, idx) => (
                  <p key={idx}><strong>{dosha.name}:</strong> {dosha.description}</p>
                ))}
                <details>
                  <summary>Remedies</summary>
                  <ul>
                    <li>Nadi Dosha: Nadi Nivarana Pooja, donation of gold</li>
                    <li>Bhakoot Dosha: Matching other factors, specific mantras</li>
                    <li>General: Consult with qualified astrologer</li>
                  </ul>
                </details>
              </div>
            </div>
          )}

          <div className={styles.comparisonNote}>
            <h5>💡 Understanding Ashtakoot</h5>
            <ul>
              <li><strong>18+ points:</strong> Minimum for marriage consideration</li>
              <li><strong>21+ points:</strong> Good compatibility</li>
              <li><strong>28+ points:</strong> Excellent match</li>
              <li><strong>Nadi Dosha:</strong> Most serious - affects health & progeny</li>
              <li><strong>Bhakoot Dosha:</strong> Affects harmony & prosperity</li>
            </ul>
          </div>
        </div>
      )}
    </div>
  );
}

// Helper functions for koota calculations
function checkVarna(boySign: number, girlSign: number): number {
  const varnaMap: Record<number, number> = {
    0: 2, 1: 1, 2: 0, 3: 3, 4: 2, 5: 1, 6: 0, 7: 3, 8: 2, 9: 1, 10: 0, 11: 3
  };
  return varnaMap[boySign] >= varnaMap[girlSign] ? 1 : 0;
}

function checkVashya(boySign: number, girlSign: number): number {
  // Simplified
  if (boySign === girlSign) return 2;
  return 1;
}

function checkTara(boyNak: number, girlNak: number): number {
  const count1 = (boyNak - girlNak + 27) % 27;
  const tara1 = (count1 % 9) + 1;
  const count2 = (girlNak - boyNak + 27) % 27;
  const tara2 = (count2 % 9) + 1;
  const badTaras = [3, 5, 7];
  
  if (!badTaras.includes(tara1) && !badTaras.includes(tara2)) return 3;
  if (!badTaras.includes(tara1) || !badTaras.includes(tara2)) return 1.5;
  return 0;
}

function checkYoni(boyNak: number, girlNak: number): number {
  // Simplified - same nakshatra group = 4, otherwise proportional
  if (boyNak === girlNak) return 4;
  if (Math.abs(boyNak - girlNak) <= 2) return 3;
  return 2;
}

function checkGrahaMaitri(boySign: number, girlSign: number): number {
  const lords = ["Mars", "Venus", "Mercury", "Moon", "Sun", "Mercury",
                 "Venus", "Mars", "Jupiter", "Saturn", "Saturn", "Jupiter"];
  const boyLord = lords[boySign];
  const girlLord = lords[girlSign];
  
  if (boyLord === girlLord) return 5;
  
  const friends: Record<string, string[]> = {
    Sun: ["Moon", "Mars", "Jupiter"],
    Moon: ["Sun", "Mercury"],
    Mars: ["Sun", "Moon", "Jupiter"],
    Mercury: ["Sun", "Venus"],
    Jupiter: ["Sun", "Moon", "Mars"],
    Venus: ["Mercury", "Saturn"],
    Saturn: ["Mercury", "Venus"]
  };
  
  if (friends[boyLord]?.includes(girlLord) || friends[girlLord]?.includes(boyLord)) return 4;
  return 2;
}

function checkGana(boyNak: number, girlNak: number): number {
  const boyGana = NAKSHATRA_GANA[boyNak];
  const girlGana = NAKSHATRA_GANA[girlNak];
  
  if (boyGana === girlGana) return 6;
  if ((boyGana === "Deva" && girlGana === "Manushya") ||
      (boyGana === "Manushya" && girlGana === "Deva")) return 5;
  if (boyGana === "Rakshasa" || girlGana === "Rakshasa") return 0;
  return 3;
}

function checkBhakoot(boySign: number, girlSign: number): number {
  const diff = Math.abs(boySign - girlSign);
  const adjustedDiff = diff > 6 ? 12 - diff : diff;
  
  // 2-12, 6-8 are problematic
  if (adjustedDiff === 1 || adjustedDiff === 5) return 0;
  if (adjustedDiff === 0 || adjustedDiff === 4) return 7;
  return 3;
}

function checkNadi(boyNak: number, girlNak: number): number {
  const boyNadi = NAKSHATRA_NADI[boyNak];
  const girlNadi = NAKSHATRA_NADI[girlNak];
  return boyNadi !== girlNadi ? 8 : 0;
}
