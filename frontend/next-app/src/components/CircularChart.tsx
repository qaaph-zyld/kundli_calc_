'use client';

import React, { useMemo } from 'react';

interface PlanetPosition {
  longitude: number;
  sign_num?: number;
  sign?: string;
}

interface CircularChartProps {
  planets: Record<string, PlanetPosition>;
  ascendant?: number;
  size?: number;
  showDegrees?: boolean;
  title?: string;
}

const SIGNS = [
  "Aries", "Taurus", "Gemini", "Cancer", 
  "Leo", "Virgo", "Libra", "Scorpio",
  "Sagittarius", "Capricorn", "Aquarius", "Pisces"
];

const SIGN_SYMBOLS = ["♈", "♉", "♊", "♋", "♌", "♍", "♎", "♏", "♐", "♑", "♒", "♓"];

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
  Uranus: "♅",
  Neptune: "♆",
  Pluto: "♇",
};

const PLANET_COLORS: Record<string, string> = {
  Sun: "#FFD700",
  Moon: "#C0C0C0",
  Mars: "#FF4444",
  Mercury: "#00AA00",
  Jupiter: "#FFD700",
  Venus: "#FF69B4",
  Saturn: "#4169E1",
  Rahu: "#666666",
  Ketu: "#999999",
};

export default function CircularChart({
  planets,
  ascendant = 0,
  size = 400,
  showDegrees = true,
  title = "Birth Chart"
}: CircularChartProps) {
  const center = size / 2;
  const outerRadius = size / 2 - 20;
  const signRadius = outerRadius - 30;
  const planetRadius = signRadius - 40;
  const innerRadius = planetRadius - 40;

  // Calculate planet positions on the wheel
  const planetPositions = useMemo(() => {
    const positions: { planet: string; angle: number; lon: number }[] = [];
    
    for (const [planet, data] of Object.entries(planets)) {
      const lon = typeof data === 'number' ? data : data.longitude;
      // Convert longitude to angle (0° Aries at top, going clockwise)
      // Adjust for ascendant to put it on the left (9 o'clock position)
      const angle = (lon - ascendant + 90) * (Math.PI / 180);
      positions.push({ planet, angle, lon });
    }
    
    // Handle overlapping planets
    positions.sort((a, b) => a.angle - b.angle);
    
    return positions;
  }, [planets, ascendant]);

  // Generate sign segments
  const signSegments = useMemo(() => {
    const segments = [];
    
    for (let i = 0; i < 12; i++) {
      const startAngle = ((i * 30) - ascendant + 90) * (Math.PI / 180);
      const endAngle = startAngle + (30 * Math.PI / 180);
      
      // Arc path
      const x1 = center + outerRadius * Math.cos(startAngle);
      const y1 = center + outerRadius * Math.sin(startAngle);
      const x2 = center + outerRadius * Math.cos(endAngle);
      const y2 = center + outerRadius * Math.sin(endAngle);
      const x3 = center + signRadius * Math.cos(endAngle);
      const y3 = center + signRadius * Math.sin(endAngle);
      const x4 = center + signRadius * Math.cos(startAngle);
      const y4 = center + signRadius * Math.sin(startAngle);
      
      // Sign symbol position (middle of segment)
      const midAngle = startAngle + (15 * Math.PI / 180);
      const symbolRadius = (outerRadius + signRadius) / 2;
      const symbolX = center + symbolRadius * Math.cos(midAngle);
      const symbolY = center + symbolRadius * Math.sin(midAngle);
      
      segments.push({
        index: i,
        sign: SIGNS[i],
        symbol: SIGN_SYMBOLS[i],
        path: `M ${x1} ${y1} A ${outerRadius} ${outerRadius} 0 0 1 ${x2} ${y2} L ${x3} ${y3} A ${signRadius} ${signRadius} 0 0 0 ${x4} ${y4} Z`,
        symbolX,
        symbolY,
        color: i % 2 === 0 ? '#f8f9fa' : '#e9ecef',
      });
    }
    
    return segments;
  }, [ascendant, center, outerRadius, signRadius]);

  return (
    <div style={{ textAlign: 'center' }}>
      {title && <h3 style={{ marginBottom: '0.5rem', color: '#374151' }}>{title}</h3>}
      
      <svg width={size} height={size} viewBox={`0 0 ${size} ${size}`}>
        {/* Background */}
        <circle cx={center} cy={center} r={outerRadius} fill="#fff" stroke="#d1d5db" strokeWidth="2" />
        
        {/* Sign segments */}
        {signSegments.map((seg) => (
          <g key={seg.index}>
            <path d={seg.path} fill={seg.color} stroke="#adb5bd" strokeWidth="1" />
            <text
              x={seg.symbolX}
              y={seg.symbolY}
              textAnchor="middle"
              dominantBaseline="middle"
              fontSize="16"
              fill="#495057"
            >
              {seg.symbol}
            </text>
          </g>
        ))}
        
        {/* Inner circle */}
        <circle cx={center} cy={center} r={innerRadius} fill="#fff" stroke="#dee2e6" strokeWidth="1" />
        
        {/* Planets */}
        {planetPositions.map(({ planet, angle, lon }, idx) => {
          const x = center + planetRadius * Math.cos(angle);
          const y = center + planetRadius * Math.sin(angle);
          const symbol = PLANET_SYMBOLS[planet] || planet.charAt(0);
          const color = PLANET_COLORS[planet] || '#333';
          
          // Calculate degree in sign
          const degInSign = lon % 30;
          
          return (
            <g key={planet}>
              {/* Planet symbol */}
              <circle cx={x} cy={y} r="16" fill="white" stroke={color} strokeWidth="2" />
              <text
                x={x}
                y={y}
                textAnchor="middle"
                dominantBaseline="middle"
                fontSize="14"
                fontWeight="bold"
                fill={color}
              >
                {symbol}
              </text>
              
              {/* Degree label */}
              {showDegrees && (
                <text
                  x={x}
                  y={y + 22}
                  textAnchor="middle"
                  fontSize="9"
                  fill="#6b7280"
                >
                  {degInSign.toFixed(1)}°
                </text>
              )}
            </g>
          );
        })}
        
        {/* Ascendant marker */}
        <g transform={`rotate(${-ascendant + 90}, ${center}, ${center})`}>
          <line
            x1={center + signRadius}
            y1={center}
            x2={center + outerRadius + 10}
            y2={center}
            stroke="#dc2626"
            strokeWidth="3"
          />
          <text
            x={center + outerRadius + 15}
            y={center + 4}
            fontSize="12"
            fontWeight="bold"
            fill="#dc2626"
          >
            Asc
          </text>
        </g>
        
        {/* Center info */}
        <text
          x={center}
          y={center - 10}
          textAnchor="middle"
          fontSize="11"
          fill="#6b7280"
        >
          Asc: {SIGNS[Math.floor(ascendant / 30)]}
        </text>
        <text
          x={center}
          y={center + 5}
          textAnchor="middle"
          fontSize="10"
          fill="#9ca3af"
        >
          {(ascendant % 30).toFixed(1)}°
        </text>
      </svg>
      
      {/* Planet Legend */}
      <div style={{
        display: 'flex',
        flexWrap: 'wrap',
        justifyContent: 'center',
        gap: '0.5rem',
        marginTop: '0.75rem',
        fontSize: '0.8rem',
      }}>
        {planetPositions.map(({ planet, lon }) => (
          <span
            key={planet}
            style={{
              padding: '2px 8px',
              backgroundColor: '#f3f4f6',
              borderRadius: '4px',
              color: PLANET_COLORS[planet] || '#333',
            }}
          >
            {PLANET_SYMBOLS[planet] || planet.charAt(0)} {SIGNS[Math.floor(lon / 30)]} {(lon % 30).toFixed(0)}°
          </span>
        ))}
      </div>
    </div>
  );
}
