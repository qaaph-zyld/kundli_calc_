'use client';

import React, { useState, useMemo } from 'react';

const SIGNS = ["Ari", "Tau", "Gem", "Can", "Leo", "Vir", "Lib", "Sco", "Sag", "Cap", "Aqu", "Pis"];
const MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];

// Simplified ephemeris calculation (mean motion approximation)
// For production, use actual ephemeris data from backend
const DAILY_MOTION: Record<string, number> = {
  Sun: 0.9856,
  Moon: 13.1764,
  Mars: 0.524,
  Mercury: 1.383,
  Jupiter: 0.0831,
  Venus: 1.2,
  Saturn: 0.0335,
  Rahu: -0.0529,
};

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
};

const AYANAMSA = 24.17;

interface EphemerisViewProps {
  year?: number;
  month?: number;
}

export default function EphemerisView({ 
  year = new Date().getFullYear(),
  month = new Date().getMonth()
}: EphemerisViewProps) {
  const [selectedYear, setSelectedYear] = useState(year);
  const [selectedMonth, setSelectedMonth] = useState(month);
  const [selectedPlanet, setSelectedPlanet] = useState<string | null>(null);

  const daysInMonth = new Date(selectedYear, selectedMonth + 1, 0).getDate();

  const ephemerisData = useMemo(() => {
    const data: { day: number; positions: Record<string, { lon: number; sign: string; deg: number }> }[] = [];
    
    for (let day = 1; day <= daysInMonth; day++) {
      const date = new Date(selectedYear, selectedMonth, day);
      const daysSinceRef = (date.getTime() - REFERENCE_DATE.getTime()) / (1000 * 60 * 60 * 24);
      
      const positions: Record<string, { lon: number; sign: string; deg: number }> = {};
      
      for (const [planet, refPos] of Object.entries(REFERENCE_POSITIONS)) {
        const motion = DAILY_MOTION[planet] || 0;
        let tropical = (refPos + motion * daysSinceRef) % 360;
        if (tropical < 0) tropical += 360;
        
        let sidereal = (tropical - AYANAMSA + 360) % 360;
        const signIndex = Math.floor(sidereal / 30);
        const degree = sidereal % 30;
        
        positions[planet] = {
          lon: sidereal,
          sign: SIGNS[signIndex],
          deg: degree,
        };
      }
      
      data.push({ day, positions });
    }
    
    return data;
  }, [selectedYear, selectedMonth, daysInMonth]);

  const formatDeg = (deg: number) => {
    const d = Math.floor(deg);
    const m = Math.floor((deg - d) * 60);
    return `${d}°${m.toString().padStart(2, '0')}'`;
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
        flexWrap: 'wrap',
        gap: '0.5rem',
      }}>
        <h3 style={{ margin: 0, fontSize: '1.1rem', fontWeight: 600 }}>
          📅 Ephemeris
        </h3>
        
        <div style={{ display: 'flex', gap: '0.5rem' }}>
          <select
            value={selectedMonth}
            onChange={(e) => setSelectedMonth(Number(e.target.value))}
            style={{
              padding: '0.25rem 0.5rem',
              borderRadius: '4px',
              border: '1px solid #d1d5db',
            }}
          >
            {MONTHS.map((m, i) => (
              <option key={i} value={i}>{m}</option>
            ))}
          </select>
          
          <select
            value={selectedYear}
            onChange={(e) => setSelectedYear(Number(e.target.value))}
            style={{
              padding: '0.25rem 0.5rem',
              borderRadius: '4px',
              border: '1px solid #d1d5db',
            }}
          >
            {Array.from({ length: 21 }, (_, i) => 2015 + i).map((y) => (
              <option key={y} value={y}>{y}</option>
            ))}
          </select>
        </div>
      </div>

      {/* Planet filter */}
      <div style={{
        display: 'flex',
        gap: '0.25rem',
        marginBottom: '0.75rem',
        flexWrap: 'wrap',
      }}>
        <button
          onClick={() => setSelectedPlanet(null)}
          style={{
            padding: '0.25rem 0.5rem',
            fontSize: '0.75rem',
            borderRadius: '4px',
            border: '1px solid #d1d5db',
            backgroundColor: selectedPlanet === null ? '#3b82f6' : 'white',
            color: selectedPlanet === null ? 'white' : '#374151',
            cursor: 'pointer',
          }}
        >
          All
        </button>
        {Object.keys(REFERENCE_POSITIONS).map((planet) => (
          <button
            key={planet}
            onClick={() => setSelectedPlanet(planet)}
            style={{
              padding: '0.25rem 0.5rem',
              fontSize: '0.75rem',
              borderRadius: '4px',
              border: '1px solid #d1d5db',
              backgroundColor: selectedPlanet === planet ? '#3b82f6' : 'white',
              color: selectedPlanet === planet ? 'white' : '#374151',
              cursor: 'pointer',
            }}
          >
            {planet}
          </button>
        ))}
      </div>

      {/* Ephemeris table */}
      <div style={{ overflowX: 'auto' }}>
        <table style={{
          width: '100%',
          fontSize: '0.75rem',
          borderCollapse: 'collapse',
        }}>
          <thead>
            <tr style={{ backgroundColor: '#f3f4f6' }}>
              <th style={{ padding: '0.5rem', textAlign: 'left', borderBottom: '1px solid #e5e7eb' }}>Day</th>
              {(selectedPlanet ? [selectedPlanet] : Object.keys(REFERENCE_POSITIONS)).map((planet) => (
                <th key={planet} style={{ padding: '0.5rem', textAlign: 'center', borderBottom: '1px solid #e5e7eb' }}>
                  {planet}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {ephemerisData.map(({ day, positions }) => (
              <tr key={day} style={{ 
                backgroundColor: day % 2 === 0 ? '#f9fafb' : 'white',
              }}>
                <td style={{ padding: '0.4rem 0.5rem', borderBottom: '1px solid #f3f4f6', fontWeight: 500 }}>
                  {day}
                </td>
                {(selectedPlanet ? [selectedPlanet] : Object.keys(REFERENCE_POSITIONS)).map((planet) => {
                  const pos = positions[planet];
                  return (
                    <td key={planet} style={{ 
                      padding: '0.4rem 0.5rem', 
                      textAlign: 'center',
                      borderBottom: '1px solid #f3f4f6',
                    }}>
                      <span style={{ fontWeight: 500 }}>{pos.sign}</span>
                      {' '}
                      <span style={{ color: '#6b7280' }}>{formatDeg(pos.deg)}</span>
                    </td>
                  );
                })}
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <div style={{
        marginTop: '0.75rem',
        padding: '0.5rem',
        backgroundColor: '#fef3c7',
        borderRadius: '6px',
        fontSize: '0.75rem',
        color: '#92400e',
      }}>
        ⚠️ Approximate positions (mean motion). For precise ephemeris, connect to Swiss Ephemeris backend.
      </div>
    </div>
  );
}
