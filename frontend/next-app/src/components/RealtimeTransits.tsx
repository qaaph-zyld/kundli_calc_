'use client';

import React, { useState, useEffect } from 'react';

const SIGNS = [
  "Aries", "Taurus", "Gemini", "Cancer", 
  "Leo", "Virgo", "Libra", "Scorpio",
  "Sagittarius", "Capricorn", "Aquarius", "Pisces"
];

const PLANET_SYMBOLS: Record<string, string> = {
  Sun: "☉",
  Moon: "☽",
  Mars: "♂",
  Mercury: "☿",
  Jupiter: "♃",
  Venus: "♀",
  Saturn: "♄",
  Rahu: "☊",
  Ketu: "☋",
};

// Approximate mean daily motions (degrees per day)
const DAILY_MOTION: Record<string, number> = {
  Sun: 0.9856,
  Moon: 13.1764,
  Mars: 0.524,
  Mercury: 1.383,
  Jupiter: 0.0831,
  Venus: 1.2,
  Saturn: 0.0335,
  Rahu: -0.0529,
  Ketu: -0.0529,
};

// Reference positions (approximate for current epoch)
const REFERENCE_DATE = new Date('2024-01-01T00:00:00Z');
const REFERENCE_POSITIONS: Record<string, number> = {
  Sun: 280.0,
  Moon: 45.0,
  Mars: 265.0,
  Mercury: 260.0,
  Jupiter: 33.0,
  Venus: 230.0,
  Saturn: 330.0,
  Rahu: 20.0,
  Ketu: 200.0,
};

// Lahiri ayanamsa approximation
const AYANAMSA = 24.17;

interface TransitPosition {
  planet: string;
  longitude: number;
  sign: string;
  degree: number;
  retrograde: boolean;
}

export default function RealtimeTransits() {
  const [transits, setTransits] = useState<TransitPosition[]>([]);
  const [lastUpdate, setLastUpdate] = useState<Date>(new Date());

  const calculateTransits = () => {
    const now = new Date();
    const daysSinceRef = (now.getTime() - REFERENCE_DATE.getTime()) / (1000 * 60 * 60 * 24);
    
    const positions: TransitPosition[] = [];
    
    for (const [planet, refPos] of Object.entries(REFERENCE_POSITIONS)) {
      const motion = DAILY_MOTION[planet] || 0;
      let tropical = (refPos + motion * daysSinceRef) % 360;
      if (tropical < 0) tropical += 360;
      
      // Convert to sidereal
      let sidereal = (tropical - AYANAMSA + 360) % 360;
      
      const signIndex = Math.floor(sidereal / 30);
      const degree = sidereal % 30;
      
      // Approximate retrograde (simplified)
      const isRetrograde = planet === 'Rahu' || planet === 'Ketu' || 
        (planet === 'Mercury' && Math.sin(daysSinceRef * 0.05) > 0.8) ||
        (planet === 'Venus' && Math.sin(daysSinceRef * 0.01) > 0.9);
      
      positions.push({
        planet,
        longitude: sidereal,
        sign: SIGNS[signIndex],
        degree,
        retrograde: isRetrograde,
      });
    }
    
    // Sort by natural order
    const order = ['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn', 'Rahu', 'Ketu'];
    positions.sort((a, b) => order.indexOf(a.planet) - order.indexOf(b.planet));
    
    setTransits(positions);
    setLastUpdate(now);
  };

  useEffect(() => {
    calculateTransits();
    
    // Update every minute
    const interval = setInterval(calculateTransits, 60000);
    
    return () => clearInterval(interval);
  }, []);

  const formatDegree = (deg: number) => {
    const d = Math.floor(deg);
    const m = Math.floor((deg - d) * 60);
    return `${d}°${m}'`;
  };

  return (
    <div style={{
      backgroundColor: 'white',
      borderRadius: '12px',
      padding: '1rem',
      boxShadow: '0 1px 3px rgba(0,0,0,0.1)',
    }}>
      <div style={{
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        marginBottom: '1rem',
      }}>
        <h3 style={{ margin: 0, fontSize: '1.1rem', fontWeight: 600 }}>
          🌍 Current Transits
        </h3>
        <span style={{ fontSize: '0.75rem', color: '#6b7280' }}>
          Updated: {lastUpdate.toLocaleTimeString()}
        </span>
      </div>

      <div style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(3, 1fr)',
        gap: '0.5rem',
      }}>
        {transits.map((t) => (
          <div
            key={t.planet}
            style={{
              padding: '0.5rem',
              backgroundColor: '#f9fafb',
              borderRadius: '8px',
              textAlign: 'center',
            }}
          >
            <div style={{ fontSize: '1.5rem' }}>
              {PLANET_SYMBOLS[t.planet]}
              {t.retrograde && <span style={{ fontSize: '0.7rem', color: '#dc2626' }}>ℜ</span>}
            </div>
            <div style={{ fontWeight: 500, fontSize: '0.85rem' }}>
              {t.planet}
            </div>
            <div style={{ fontSize: '0.8rem', color: '#374151' }}>
              {t.sign}
            </div>
            <div style={{ fontSize: '0.75rem', color: '#6b7280' }}>
              {formatDegree(t.degree)}
            </div>
          </div>
        ))}
      </div>

      <div style={{
        marginTop: '0.75rem',
        padding: '0.5rem',
        backgroundColor: '#fef3c7',
        borderRadius: '6px',
        fontSize: '0.75rem',
        color: '#92400e',
      }}>
        ⚠️ Approximate positions (mean motion). For precise calculations, use the chart calculator.
      </div>
    </div>
  );
}
