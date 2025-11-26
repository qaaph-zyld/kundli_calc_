"use client";
import { useState, useEffect, useMemo } from 'react';
import styles from './AnalysisPanels.module.css';

interface KPPosition {
  degree: number;
  sign: string;
  sign_lord: string;
  nakshatra: string;
  star_lord: string;
  sub_lord: string;
  sub_sub_lord: string;
}

interface RulingPlanets {
  weekday_lord: string;
  moon_sign_lord: string;
  moon_star_lord: string;
  moon_sub_lord: string;
  asc_sign_lord: string;
  asc_star_lord: string;
  asc_sub_lord: string;
  strong_rp: string[];
}

interface KPData {
  planet_positions: Record<string, KPPosition>;
  cuspal_positions: Record<string, KPPosition>;
  planets_by_house: Record<string, string[]>;
  ruling_planets: RulingPlanets;
}

interface KPSystemPanelProps {
  chartData: any;
  birthDatetime?: string;
}

// Planet symbols
const PLANET_SYMBOLS: Record<string, string> = {
  Sun: '☉', Moon: '☽', Mars: '♂', Mercury: '☿',
  Jupiter: '♃', Venus: '♀', Saturn: '♄', Rahu: '☊', Ketu: '☋'
};

export default function KPSystemPanel({ chartData, birthDatetime }: KPSystemPanelProps) {
  const [activeTab, setActiveTab] = useState<'planets' | 'cusps' | 'rp' | 'significators'>('planets');
  const [kpData, setKpData] = useState<KPData | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Calculate KP data locally (since we have the calculations in backend)
  const calculatedKP = useMemo(() => {
    if (!chartData?.planetary_positions) return null;

    const positions: Record<string, KPPosition> = {};
    const NAKSHATRAS = [
      "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra",
      "Punarvasu", "Pushya", "Ashlesha", "Magha", "Purva Phalguni", "Uttara Phalguni",
      "Hasta", "Chitra", "Swati", "Vishakha", "Anuradha", "Jyeshtha",
      "Mula", "Purva Ashadha", "Uttara Ashadha", "Shravana", "Dhanishta", "Shatabhisha",
      "Purva Bhadrapada", "Uttara Bhadrapada", "Revati"
    ];
    const NAK_LORDS = ["Ketu", "Venus", "Sun", "Moon", "Mars", "Rahu", "Jupiter", "Saturn", "Mercury"];
    const SIGNS = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", 
                   "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"];
    const SIGN_LORDS = ["Mars", "Venus", "Mercury", "Moon", "Sun", "Mercury",
                        "Venus", "Mars", "Jupiter", "Saturn", "Saturn", "Jupiter"];

    Object.entries(chartData.planetary_positions).forEach(([planet, data]: [string, any]) => {
      const lon = data.longitude;
      const sign = Math.floor(lon / 30);
      const nakIdx = Math.floor(lon / (360 / 27));
      const starLord = NAK_LORDS[nakIdx % 9];
      
      // Sub lord calculation (simplified)
      const nakSpan = 13.333333;
      const posInNak = lon % nakSpan;
      const subIdx = Math.floor((posInNak / nakSpan) * 9);
      const lordOrder = [...NAK_LORDS.slice(NAK_LORDS.indexOf(starLord)), 
                         ...NAK_LORDS.slice(0, NAK_LORDS.indexOf(starLord))];
      const subLord = lordOrder[subIdx % 9];
      const subSubLord = lordOrder[(subIdx + 1) % 9];

      positions[planet] = {
        degree: lon,
        sign: SIGNS[sign],
        sign_lord: SIGN_LORDS[sign],
        nakshatra: NAKSHATRAS[nakIdx],
        star_lord: starLord,
        sub_lord: subLord,
        sub_sub_lord: subSubLord
      };
    });

    // Calculate cuspal positions
    const cusps: Record<string, KPPosition> = {};
    if (chartData.houses?.cusps) {
      chartData.houses.cusps.forEach((cusp: number, idx: number) => {
        const sign = Math.floor(cusp / 30);
        const nakIdx = Math.floor(cusp / (360 / 27));
        const starLord = NAK_LORDS[nakIdx % 9];
        const nakSpan = 13.333333;
        const posInNak = cusp % nakSpan;
        const subIdx = Math.floor((posInNak / nakSpan) * 9);
        const lordOrder = [...NAK_LORDS.slice(NAK_LORDS.indexOf(starLord)), 
                           ...NAK_LORDS.slice(0, NAK_LORDS.indexOf(starLord))];

        cusps[String(idx + 1)] = {
          degree: cusp,
          sign: SIGNS[sign],
          sign_lord: SIGN_LORDS[sign],
          nakshatra: NAKSHATRAS[nakIdx],
          star_lord: starLord,
          sub_lord: lordOrder[subIdx % 9],
          sub_sub_lord: lordOrder[(subIdx + 1) % 9]
        };
      });
    }

    // Ruling planets (for current moment - simplified)
    const now = new Date();
    const weekdays = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"];
    const weekdayLord = weekdays[now.getDay() === 0 ? 0 : now.getDay()];
    
    const moonPos = positions["Moon"];
    const rp: RulingPlanets = {
      weekday_lord: weekdayLord,
      moon_sign_lord: moonPos?.sign_lord || "",
      moon_star_lord: moonPos?.star_lord || "",
      moon_sub_lord: moonPos?.sub_lord || "",
      asc_sign_lord: cusps["1"]?.sign_lord || "",
      asc_star_lord: cusps["1"]?.star_lord || "",
      asc_sub_lord: cusps["1"]?.sub_lord || "",
      strong_rp: []
    };

    // Find strong ruling planets (appearing multiple times)
    const allRp = [rp.weekday_lord, rp.moon_sign_lord, rp.moon_star_lord, 
                   rp.moon_sub_lord, rp.asc_sign_lord, rp.asc_star_lord, rp.asc_sub_lord];
    const rpCounts: Record<string, number> = {};
    allRp.forEach(p => { rpCounts[p] = (rpCounts[p] || 0) + 1; });
    rp.strong_rp = Object.entries(rpCounts)
      .sort((a, b) => b[1] - a[1])
      .map(([p]) => p)
      .filter(p => p);

    return {
      planet_positions: positions,
      cuspal_positions: cusps,
      planets_by_house: {},
      ruling_planets: rp
    };
  }, [chartData]);

  if (!calculatedKP) {
    return (
      <div className={styles.panel}>
        <div className={styles.panelHeader}>
          <h3>🎯 KP System</h3>
        </div>
        <p className={styles.noData}>No chart data available</p>
      </div>
    );
  }

  return (
    <div className={styles.panel}>
      <div className={styles.panelHeader}>
        <h3>🎯 KP (Krishnamurti Paddhati) System</h3>
        <p className={styles.subtitle}>Sublord-based precision astrology</p>
      </div>

      {/* Tab Navigation */}
      <div className={styles.tabNav}>
        <button 
          className={`${styles.tab} ${activeTab === 'planets' ? styles.active : ''}`}
          onClick={() => setActiveTab('planets')}
        >
          Planets
        </button>
        <button 
          className={`${styles.tab} ${activeTab === 'cusps' ? styles.active : ''}`}
          onClick={() => setActiveTab('cusps')}
        >
          Cusps
        </button>
        <button 
          className={`${styles.tab} ${activeTab === 'rp' ? styles.active : ''}`}
          onClick={() => setActiveTab('rp')}
        >
          Ruling Planets
        </button>
        <button 
          className={`${styles.tab} ${activeTab === 'significators' ? styles.active : ''}`}
          onClick={() => setActiveTab('significators')}
        >
          Significators
        </button>
      </div>

      {/* Planet Positions Table */}
      {activeTab === 'planets' && (
        <div className={styles.tableContainer}>
          <table className={styles.kpTable}>
            <thead>
              <tr>
                <th>Planet</th>
                <th>Degree</th>
                <th>Sign</th>
                <th>Sign Lord</th>
                <th>Star Lord</th>
                <th>Sub Lord</th>
                <th>S-S Lord</th>
              </tr>
            </thead>
            <tbody>
              {Object.entries(calculatedKP.planet_positions).map(([planet, pos]) => (
                <tr key={planet}>
                  <td className={styles.planetCell}>
                    <span className={styles.planetSymbol}>{PLANET_SYMBOLS[planet] || ''}</span>
                    {planet}
                  </td>
                  <td>{pos.degree.toFixed(2)}°</td>
                  <td>{pos.sign}</td>
                  <td className={styles.lordCell}>{pos.sign_lord}</td>
                  <td className={styles.starLord}>{pos.star_lord}</td>
                  <td className={styles.subLord}>{pos.sub_lord}</td>
                  <td className={styles.subSubLord}>{pos.sub_sub_lord}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {/* Cuspal Positions Table */}
      {activeTab === 'cusps' && (
        <div className={styles.tableContainer}>
          <table className={styles.kpTable}>
            <thead>
              <tr>
                <th>Cusp</th>
                <th>Degree</th>
                <th>Sign</th>
                <th>Sign Lord</th>
                <th>Star Lord</th>
                <th>Sub Lord</th>
                <th>S-S Lord</th>
              </tr>
            </thead>
            <tbody>
              {Object.entries(calculatedKP.cuspal_positions).map(([cusp, pos]) => (
                <tr key={cusp}>
                  <td className={styles.cuspCell}>House {cusp}</td>
                  <td>{pos.degree.toFixed(2)}°</td>
                  <td>{pos.sign}</td>
                  <td className={styles.lordCell}>{pos.sign_lord}</td>
                  <td className={styles.starLord}>{pos.star_lord}</td>
                  <td className={styles.subLord}>{pos.sub_lord}</td>
                  <td className={styles.subSubLord}>{pos.sub_sub_lord}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {/* Ruling Planets */}
      {activeTab === 'rp' && (
        <div className={styles.rpSection}>
          <div className={styles.rpGrid}>
            <div className={styles.rpCard}>
              <h4>📅 Day Lord</h4>
              <p className={styles.rpValue}>{calculatedKP.ruling_planets.weekday_lord}</p>
            </div>
            <div className={styles.rpCard}>
              <h4>☽ Moon Sign Lord</h4>
              <p className={styles.rpValue}>{calculatedKP.ruling_planets.moon_sign_lord}</p>
            </div>
            <div className={styles.rpCard}>
              <h4>⭐ Moon Star Lord</h4>
              <p className={styles.rpValue}>{calculatedKP.ruling_planets.moon_star_lord}</p>
            </div>
            <div className={styles.rpCard}>
              <h4>◉ Moon Sub Lord</h4>
              <p className={styles.rpValue}>{calculatedKP.ruling_planets.moon_sub_lord}</p>
            </div>
            <div className={styles.rpCard}>
              <h4>🌅 Asc Sign Lord</h4>
              <p className={styles.rpValue}>{calculatedKP.ruling_planets.asc_sign_lord}</p>
            </div>
            <div className={styles.rpCard}>
              <h4>⭐ Asc Star Lord</h4>
              <p className={styles.rpValue}>{calculatedKP.ruling_planets.asc_star_lord}</p>
            </div>
            <div className={styles.rpCard}>
              <h4>◉ Asc Sub Lord</h4>
              <p className={styles.rpValue}>{calculatedKP.ruling_planets.asc_sub_lord}</p>
            </div>
          </div>

          <div className={styles.strongRp}>
            <h4>🏆 Strong Ruling Planets (by frequency)</h4>
            <div className={styles.rpTags}>
              {calculatedKP.ruling_planets.strong_rp.map((planet, idx) => (
                <span key={planet} className={`${styles.rpTag} ${idx === 0 ? styles.primary : ''}`}>
                  {PLANET_SYMBOLS[planet] || ''} {planet}
                </span>
              ))}
            </div>
            <p className={styles.rpNote}>
              Planets appearing multiple times are stronger ruling planets for timing events
            </p>
          </div>
        </div>
      )}

      {/* Significators */}
      {activeTab === 'significators' && (
        <div className={styles.sigSection}>
          <div className={styles.sigExplanation}>
            <h4>ABCD Significator System</h4>
            <div className={styles.sigLegend}>
              <div><strong>A:</strong> Planets in star of occupants of the house</div>
              <div><strong>B:</strong> Planets occupying the house</div>
              <div><strong>C:</strong> Planets in star of house owner</div>
              <div><strong>D:</strong> Owner of the house (Sign Lord of cusp)</div>
            </div>
          </div>

          <div className={styles.sigGrid}>
            {[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12].map(house => {
              const cusp = calculatedKP.cuspal_positions[String(house)];
              return (
                <div key={house} className={styles.sigCard}>
                  <h5>House {house}</h5>
                  <div className={styles.sigDetails}>
                    <div className={styles.sigRow}>
                      <span className={styles.sigLabel}>D (Owner):</span>
                      <span className={styles.sigValue}>{cusp?.sign_lord}</span>
                    </div>
                    <div className={styles.sigRow}>
                      <span className={styles.sigLabel}>Star Lord:</span>
                      <span className={styles.sigValue}>{cusp?.star_lord}</span>
                    </div>
                    <div className={styles.sigRow}>
                      <span className={styles.sigLabel}>Sub Lord:</span>
                      <span className={styles.sigValue}>{cusp?.sub_lord}</span>
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      )}

      <div className={styles.kpFooter}>
        <p>
          <strong>Usage:</strong> In KP, events are timed when the ruling planets match the significators of relevant houses.
          Sub lord of a cusp determines whether the house promises positive results.
        </p>
      </div>
    </div>
  );
}
