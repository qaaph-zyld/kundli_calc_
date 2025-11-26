"use client";
import { useState, useMemo } from 'react';
import styles from './AnalysisPanels.module.css';

interface MuhurtaPanelProps {
  chartData: any;
  birthDatetime?: string;
}

const WEEKDAYS = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
const WEEKDAY_LORDS = ['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn'];

const PLANET_COLORS: Record<string, string> = {
  Sun: '#FF9800', Moon: '#90CAF9', Mars: '#F44336', Mercury: '#4CAF50',
  Jupiter: '#FFC107', Venus: '#E91E63', Saturn: '#607D8B', Rahu: '#9C27B0', Ketu: '#795548'
};

const NAKSHATRA_NAMES = [
  "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra",
  "Punarvasu", "Pushya", "Ashlesha", "Magha", "Purva Phalguni", "Uttara Phalguni",
  "Hasta", "Chitra", "Swati", "Vishakha", "Anuradha", "Jyeshtha",
  "Mula", "Purva Ashadha", "Uttara Ashadha", "Shravana", "Dhanishta", "Shatabhisha",
  "Purva Bhadrapada", "Uttara Bhadrapada", "Revati"
];

const TITHI_NAMES = [
  "Pratipada", "Dwitiya", "Tritiya", "Chaturthi", "Panchami",
  "Shashthi", "Saptami", "Ashtami", "Navami", "Dashami",
  "Ekadashi", "Dwadashi", "Trayodashi", "Chaturdashi", "Purnima/Amavasya"
];

const YOGA_NAMES = [
  "Vishkumbha", "Priti", "Ayushman", "Saubhagya", "Shobhana",
  "Atiganda", "Sukarma", "Dhriti", "Shula", "Ganda",
  "Vriddhi", "Dhruva", "Vyaghata", "Harshana", "Vajra",
  "Siddhi", "Vyatipata", "Variyan", "Parigha", "Shiva",
  "Siddha", "Sadhya", "Shubha", "Shukla", "Brahma",
  "Indra", "Vaidhriti"
];

// Rahu Kalam segments by day (1-8)
const RAHU_KALAM = [8, 2, 7, 5, 6, 4, 3]; // Sun=8th, Mon=2nd, etc.

export default function MuhurtaPanel({ chartData, birthDatetime }: MuhurtaPanelProps) {
  const [selectedDate, setSelectedDate] = useState(new Date());
  const [activeTab, setActiveTab] = useState<'panchang' | 'muhurta' | 'choghadiya'>('panchang');

  // Calculate Panchang
  const panchang = useMemo(() => {
    const sunLon = chartData?.planetary_positions?.Sun?.longitude || 0;
    const moonLon = chartData?.planetary_positions?.Moon?.longitude || 0;
    
    // Tithi
    const diff = (moonLon - sunLon + 360) % 360;
    const tithiNum = Math.floor(diff / 12) + 1;
    const paksha = tithiNum <= 15 ? 'Shukla' : 'Krishna';
    const tithiName = TITHI_NAMES[(tithiNum - 1) % 15];
    
    // Nakshatra
    const nakIdx = Math.floor(moonLon / (360 / 27));
    const nakPada = Math.floor((moonLon % (360 / 27)) / (360 / 27 / 4)) + 1;
    
    // Yoga
    const combined = (sunLon + moonLon) % 360;
    const yogaIdx = Math.floor(combined / (360 / 27));
    
    // Karana
    const karanaNum = Math.floor(diff / 6) % 11;
    const karanaNames = ["Bava", "Balava", "Kaulava", "Taitila", "Gara", "Vanija", "Vishti"];
    const karana = karanaNames[karanaNum % 7];
    
    // Weekday
    const weekdayIdx = selectedDate.getDay();
    
    return {
      weekday: WEEKDAYS[weekdayIdx],
      weekdayLord: WEEKDAY_LORDS[weekdayIdx],
      tithi: {
        name: tithiName,
        number: tithiNum,
        paksha
      },
      nakshatra: {
        name: NAKSHATRA_NAMES[nakIdx],
        pada: nakPada,
        lord: getNakshatraLord(nakIdx)
      },
      yoga: {
        name: YOGA_NAMES[yogaIdx],
        quality: getYogaQuality(yogaIdx)
      },
      karana,
      moonSign: getSignName(moonLon),
      sunSign: getSignName(sunLon)
    };
  }, [chartData, selectedDate]);

  // Calculate Muhurtas
  const muhurtas = useMemo(() => {
    const sunrise = new Date(selectedDate);
    sunrise.setHours(6, 0, 0, 0); // Approximate
    
    const sunset = new Date(selectedDate);
    sunset.setHours(18, 0, 0, 0);
    
    const dayDuration = (sunset.getTime() - sunrise.getTime()) / 1000;
    const muhurtaDuration = dayDuration / 15; // 15 muhurtas in day
    
    const dayMuhurtas = [];
    for (let i = 0; i < 15; i++) {
      const start = new Date(sunrise.getTime() + i * muhurtaDuration * 1000);
      const end = new Date(start.getTime() + muhurtaDuration * 1000);
      
      dayMuhurtas.push({
        number: i + 1,
        name: getMuhurtaName(i + 1),
        start: formatTime(start),
        end: formatTime(end),
        quality: getMuhurtaQuality(i + 1),
        isAbhijit: i === 7 // 8th muhurta
      });
    }
    
    return dayMuhurtas;
  }, [selectedDate]);

  // Calculate Choghadiya
  const choghadiyas = useMemo(() => {
    const sunrise = new Date(selectedDate);
    sunrise.setHours(6, 0, 0, 0);
    
    const sunset = new Date(selectedDate);
    sunset.setHours(18, 0, 0, 0);
    
    const dayDuration = (sunset.getTime() - sunrise.getTime()) / 1000;
    const chogDuration = dayDuration / 8;
    
    const types = [
      { name: 'Udveg', quality: 'avoid', lord: 'Mars' },
      { name: 'Char', quality: 'good', lord: 'Venus' },
      { name: 'Labh', quality: 'excellent', lord: 'Mercury' },
      { name: 'Amrit', quality: 'excellent', lord: 'Moon' },
      { name: 'Kaal', quality: 'avoid', lord: 'Saturn' },
      { name: 'Shubh', quality: 'good', lord: 'Jupiter' },
      { name: 'Rog', quality: 'avoid', lord: 'Sun' }
    ];
    
    const weekdayOrder = [
      [0, 1, 2, 3, 4, 5, 6, 0],
      [3, 4, 5, 6, 0, 1, 2, 3],
      [6, 0, 1, 2, 3, 4, 5, 6],
      [1, 2, 3, 4, 5, 6, 0, 1],
      [5, 6, 0, 1, 2, 3, 4, 5],
      [2, 3, 4, 5, 6, 0, 1, 2],
      [4, 5, 6, 0, 1, 2, 3, 4]
    ];
    
    const weekday = selectedDate.getDay();
    const order = weekdayOrder[weekday];
    
    return order.map((typeIdx, i) => {
      const start = new Date(sunrise.getTime() + i * chogDuration * 1000);
      const end = new Date(start.getTime() + chogDuration * 1000);
      const type = types[typeIdx];
      
      return {
        ...type,
        start: formatTime(start),
        end: formatTime(end),
        period: i + 1
      };
    });
  }, [selectedDate]);

  // Calculate Rahu Kalam
  const rahuKalam = useMemo(() => {
    const sunrise = new Date(selectedDate);
    sunrise.setHours(6, 0, 0, 0);
    
    const sunset = new Date(selectedDate);
    sunset.setHours(18, 0, 0, 0);
    
    const dayDuration = (sunset.getTime() - sunrise.getTime()) / 1000;
    const segmentDuration = dayDuration / 8;
    
    const weekday = selectedDate.getDay();
    const segment = RAHU_KALAM[weekday];
    
    const start = new Date(sunrise.getTime() + (segment - 1) * segmentDuration * 1000);
    const end = new Date(start.getTime() + segmentDuration * 1000);
    
    return {
      start: formatTime(start),
      end: formatTime(end)
    };
  }, [selectedDate]);

  return (
    <div className={styles.panel}>
      <div className={styles.panelHeader}>
        <h3>🕉️ Panchang & Muhurta</h3>
        <p className={styles.subtitle}>Daily Hindu almanac and auspicious times</p>
      </div>

      {/* Date Selector */}
      <div className={styles.filters}>
        <input
          type="date"
          value={selectedDate.toISOString().split('T')[0]}
          onChange={(e) => setSelectedDate(new Date(e.target.value))}
          className={styles.filterSelect}
        />
      </div>

      {/* Tabs */}
      <div className={styles.tabNav}>
        <button
          className={`${styles.tab} ${activeTab === 'panchang' ? styles.active : ''}`}
          onClick={() => setActiveTab('panchang')}
        >
          📅 Panchang
        </button>
        <button
          className={`${styles.tab} ${activeTab === 'muhurta' ? styles.active : ''}`}
          onClick={() => setActiveTab('muhurta')}
        >
          ⏰ Muhurta
        </button>
        <button
          className={`${styles.tab} ${activeTab === 'choghadiya' ? styles.active : ''}`}
          onClick={() => setActiveTab('choghadiya')}
        >
          🔔 Choghadiya
        </button>
      </div>

      {/* Panchang Tab */}
      {activeTab === 'panchang' && (
        <div className={styles.timeline}>
          {/* Main Panchang Display */}
          <div className={styles.statsRow}>
            <div className={styles.statCard}>
              <span className={styles.statLabel}>Weekday</span>
              <span className={styles.statValue}>{panchang.weekday}</span>
              <span style={{ color: PLANET_COLORS[panchang.weekdayLord] }}>
                {panchang.weekdayLord}
              </span>
            </div>
            <div className={styles.statCard}>
              <span className={styles.statLabel}>Tithi</span>
              <span className={styles.statValue}>{panchang.tithi.name}</span>
              <span>{panchang.tithi.paksha} Paksha</span>
            </div>
            <div className={styles.statCard}>
              <span className={styles.statLabel}>Nakshatra</span>
              <span className={styles.statValue}>{panchang.nakshatra.name}</span>
              <span>Pada {panchang.nakshatra.pada}</span>
            </div>
            <div className={styles.statCard}>
              <span className={styles.statLabel}>Yoga</span>
              <span className={styles.statValue}>{panchang.yoga.name}</span>
              <span className={panchang.yoga.quality === 'benefic' ? styles.beneficRow : ''}>
                {panchang.yoga.quality}
              </span>
            </div>
          </div>

          {/* Additional Info */}
          <div className={styles.currentDetails}>
            <div className={styles.rpGrid}>
              <div className={styles.rpCard}>
                <h4>Karana</h4>
                <span className={styles.rpValue}>{panchang.karana}</span>
              </div>
              <div className={styles.rpCard}>
                <h4>Moon Sign</h4>
                <span className={styles.rpValue}>{panchang.moonSign}</span>
              </div>
              <div className={styles.rpCard}>
                <h4>Sun Sign</h4>
                <span className={styles.rpValue}>{panchang.sunSign}</span>
              </div>
            </div>
          </div>

          {/* Inauspicious Times */}
          <div className={styles.sadeSatiAlert + ' ' + styles.peak}>
            <span className={styles.alertIcon}>⚠️</span>
            <div className={styles.alertContent}>
              <h4>Rahu Kalam (Avoid new beginnings)</h4>
              <p>{rahuKalam.start} - {rahuKalam.end}</p>
            </div>
          </div>
        </div>
      )}

      {/* Muhurta Tab */}
      {activeTab === 'muhurta' && (
        <div className={styles.timeline}>
          <div className={styles.tableContainer}>
            <table className={styles.kpTable}>
              <thead>
                <tr>
                  <th>#</th>
                  <th>Muhurta</th>
                  <th>Time</th>
                  <th>Quality</th>
                </tr>
              </thead>
              <tbody>
                {muhurtas.map((m) => (
                  <tr key={m.number} className={m.isAbhijit ? styles.beneficRow : ''}>
                    <td>{m.number}</td>
                    <td>
                      {m.name}
                      {m.isAbhijit && <span className={styles.resultBadge + ' ' + styles.good}> ★ ABHIJIT</span>}
                    </td>
                    <td>{m.start} - {m.end}</td>
                    <td>
                      <span className={`${styles.resultBadge} ${m.quality === 'good' ? styles.good : m.quality === 'bad' ? styles.challenging : ''}`}>
                        {m.quality}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          <div className={styles.comparisonNote}>
            <h5>💡 Abhijit Muhurta</h5>
            <p>The 8th muhurta (midday period) is called Abhijit - the most auspicious time for starting any new venture, except on Wednesdays when it's inauspicious.</p>
          </div>
        </div>
      )}

      {/* Choghadiya Tab */}
      {activeTab === 'choghadiya' && (
        <div className={styles.timeline}>
          <div className={styles.predictionCategories}>
            {choghadiyas.map((c, idx) => (
              <div 
                key={idx} 
                className={styles.predictionCard}
                style={{ 
                  borderLeft: `4px solid ${c.quality === 'excellent' ? '#4CAF50' : c.quality === 'good' ? '#FFC107' : '#F44336'}`
                }}
              >
                <div className={styles.predictionHeader}>
                  <span className={styles.predictionIcon}>
                    {c.quality === 'excellent' ? '✨' : c.quality === 'good' ? '👍' : '⚠️'}
                  </span>
                  <h4>{c.name}</h4>
                  <span className={`${styles.outlookBadge} ${c.quality === 'avoid' ? styles.cautious : styles.positive}`}>
                    {c.quality === 'excellent' ? '★' : c.quality === 'good' ? '✓' : '✗'}
                  </span>
                </div>
                <p className={styles.predictionText}>
                  <strong>{c.start} - {c.end}</strong>
                </p>
                <p className={styles.predictionText}>
                  Lord: <span style={{ color: PLANET_COLORS[c.lord] }}>{c.lord}</span>
                </p>
                <p className={styles.predictionText}>
                  {getChoghadiyaMeaning(c.name)}
                </p>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

// Helper functions
function formatTime(date: Date): string {
  return date.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit', hour12: true });
}

function getSignName(longitude: number): string {
  const signs = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
                 "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"];
  return signs[Math.floor(longitude / 30)];
}

function getNakshatraLord(nakIdx: number): string {
  const lords = ["Ketu", "Venus", "Sun", "Moon", "Mars", "Rahu",
                 "Jupiter", "Saturn", "Mercury"];
  return lords[nakIdx % 9];
}

function getYogaQuality(yogaIdx: number): string {
  const malefic = [0, 5, 8, 9, 12, 16, 18, 26];
  return malefic.includes(yogaIdx) ? 'malefic' : 'benefic';
}

function getMuhurtaName(num: number): string {
  const names = [
    "Rudra", "Ahi", "Mitra", "Pitru", "Vasu", "Vara", "Vishwadeva", "Abhijit",
    "Vidhi", "Satmukhi", "Puruhuta", "Vahini", "Naktanakara", "Varuna", "Aryama"
  ];
  return names[num - 1] || `Muhurta ${num}`;
}

function getMuhurtaQuality(num: number): string {
  const goodMuhurtas = [3, 4, 5, 7, 8, 10, 11, 13, 15];
  const badMuhurtas = [1, 2, 6, 9, 14];
  if (goodMuhurtas.includes(num)) return 'good';
  if (badMuhurtas.includes(num)) return 'bad';
  return 'neutral';
}

function getChoghadiyaMeaning(name: string): string {
  const meanings: Record<string, string> = {
    'Amrit': 'Excellent for all auspicious work, marriage, business',
    'Labh': 'Good for financial matters, starting business, gains',
    'Shubh': 'Auspicious for religious ceremonies, important work',
    'Char': 'Good for travel, movement, short journeys',
    'Udveg': 'Avoid - may cause anxiety, conflict',
    'Kaal': 'Avoid - inauspicious for new beginnings',
    'Rog': 'Avoid - may affect health matters'
  };
  return meanings[name] || '';
}
