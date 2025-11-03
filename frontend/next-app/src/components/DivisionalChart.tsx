"use client";
import React from 'react';

interface Planet {
  name: string;
  sign: string;
  sign_num: number;
  longitude: number;
}

interface ChartData {
  planetary_positions?: Record<string, Planet>;
  houses?: {
    ascendant: { sign: string; sign_num: number; longitude: number };
  };
}

interface DivisionalChartProps {
  data: ChartData;
  size?: number;
  division: 2 | 3 | 7 | 10 | 12; // D2, D3, D7, D10, D12
}

const ZODIAC_SIGNS = [
  'Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo',
  'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces'
];

const PLANET_SYMBOLS: Record<string, string> = {
  'Sun': '☉',
  'Moon': '☽',
  'Mars': '♂',
  'Mercury': '☿',
  'Jupiter': '♃',
  'Venus': '♀',
  'Saturn': '♄',
  'Rahu': '☊',
  'Ketu': '☋',
};

const DIVISION_INFO: Record<number, { name: string; purpose: string; color: string }> = {
  2: { name: 'Hora (D2)', purpose: 'Wealth & Prosperity', color: '#ff9800' },
  3: { name: 'Drekkana (D3)', purpose: 'Siblings & Courage', color: '#9c27b0' },
  7: { name: 'Saptamsa (D7)', purpose: 'Children & Creativity', color: '#00bcd4' },
  10: { name: 'Dasamsa (D10)', purpose: 'Career & Profession', color: '#4caf50' },
  12: { name: 'Dwadasamsa (D12)', purpose: 'Parents & Ancestry', color: '#f44336' },
};

/**
 * Calculate divisional chart position
 * Formula varies by division type
 */
function calculateDivisionalSign(signNum: number, longitude: number, division: number): number {
  const longitudeInSign = longitude % 30;
  const partSize = 30 / division;
  const part = Math.floor(longitudeInSign / partSize);
  
  // Different formulas for different divisions
  let divisionalSign: number;
  
  switch (division) {
    case 2: // Hora (D2)
      // First 15° = same sign, last 15° = 7th from sign
      divisionalSign = part === 0 ? signNum : ((signNum + 6) % 12) + 1;
      break;
      
    case 3: // Drekkana (D3)
      // Each 10° = +0, +4, +8 signs
      divisionalSign = ((signNum - 1 + part * 4) % 12) + 1;
      break;
      
    case 7: // Saptamsa (D7)
      // Standard formula
      divisionalSign = (((signNum - 1) * 7 + part) % 12) + 1;
      break;
      
    case 10: // Dasamsa (D10)
      // Standard formula
      divisionalSign = (((signNum - 1) * 10 + part) % 12) + 1;
      break;
      
    case 12: // Dwadasamsa (D12)
      // Each sign divided into 12 parts of 2.5°
      divisionalSign = (((signNum - 1) * 12 + part) % 12) + 1;
      break;
      
    default:
      divisionalSign = signNum;
  }
  
  return divisionalSign;
}

export default function DivisionalChart({ data, size = 600, division }: DivisionalChartProps) {
  const padding = 40;
  const chartSize = size - padding * 2;
  const cellSize = chartSize / 4;
  const info = DIVISION_INFO[division];

  // Calculate divisional ascendant
  const rasiAscendant = data?.houses?.ascendant;
  const divisionalAscendantSign = rasiAscendant 
    ? calculateDivisionalSign(rasiAscendant.sign_num, rasiAscendant.longitude, division)
    : 1;

  // Calculate divisional positions for all planets
  const planetsWithDivisional = React.useMemo(() => {
    if (!data?.planetary_positions) return {};
    
    const result: Record<number, Planet[]> = {};
    
    Object.entries(data.planetary_positions).forEach(([name, planet]) => {
      const divisionalSign = calculateDivisionalSign(planet.sign_num, planet.longitude, division);
      const houseNum = ((divisionalSign - divisionalAscendantSign + 12) % 12) + 1;
      
      if (!result[houseNum]) result[houseNum] = [];
      result[houseNum].push({
        ...planet,
        name,
      });
    });
    
    return result;
  }, [data, divisionalAscendantSign, division]);

  // Map zodiac sign to position in South Indian chart
  const getSignPosition = (signNum: number): { row: number; col: number } => {
    const positions = [
      { row: 0, col: 2 }, // 1: Aries
      { row: 1, col: 2 }, // 2: Taurus
      { row: 2, col: 2 }, // 3: Gemini
      { row: 3, col: 2 }, // 4: Cancer
      { row: 3, col: 1 }, // 5: Leo
      { row: 3, col: 0 }, // 6: Virgo
      { row: 2, col: 0 }, // 7: Libra
      { row: 1, col: 0 }, // 8: Scorpio
      { row: 0, col: 0 }, // 9: Sagittarius
      { row: 0, col: 1 }, // 10: Capricorn
      { row: 1, col: 1 }, // 11: Aquarius
      { row: 2, col: 1 }, // 12: Pisces
    ];
    return positions[(signNum - 1 + 12) % 12];
  };

  const getHouseNumber = (signNum: number): number => {
    return ((signNum - divisionalAscendantSign + 12) % 12) + 1;
  };

  // Render a single cell
  const renderCell = (row: number, col: number) => {
    const x = padding + col * cellSize;
    const y = padding + row * cellSize;

    // Find which sign is in this position
    let signNum = 0;
    for (let i = 1; i <= 12; i++) {
      const pos = getSignPosition(i);
      if (pos.row === row && pos.col === col) {
        signNum = i;
        break;
      }
    }

    if (signNum === 0) return null;

    const houseNum = getHouseNumber(signNum);
    const planetsInHouse = planetsWithDivisional[houseNum] || [];
    const isAscendant = houseNum === 1;
    const isCenter = row === 1 && col === 1;

    return (
      <g key={`cell-${row}-${col}`}>
        {/* Cell rectangle */}
        <rect
          x={x}
          y={y}
          width={cellSize}
          height={cellSize}
          fill={isAscendant ? `${info.color}15` : '#ffffff'}
          stroke="#333"
          strokeWidth="2"
        />

        {/* Sign label */}
        <text
          x={x + 8}
          y={y + 18}
          fontSize="14"
          fontWeight={isAscendant ? 'bold' : 'normal'}
          fill="#666"
        >
          {ZODIAC_SIGNS[signNum - 1].slice(0, 3)}
        </text>

        {/* House number */}
        <text
          x={x + cellSize - 8}
          y={y + 18}
          fontSize="12"
          textAnchor="end"
          fill="#999"
        >
          H{houseNum}
        </text>

        {/* Ascendant marker */}
        {isAscendant && (
          <text
            x={x + cellSize / 2}
            y={y + 35}
            fontSize="14"
            fontWeight="bold"
            textAnchor="middle"
            fill={info.color}
          >
            D{division} As
          </text>
        )}

        {/* Planets in this house */}
        {planetsInHouse.length > 0 && (
          <g>
            {planetsInHouse.map((planet, idx) => (
              <g key={planet.name}>
                {/* Planet symbol */}
                <text
                  x={x + 8}
                  y={y + 50 + idx * 20}
                  fontSize="18"
                  fill={info.color}
                >
                  {PLANET_SYMBOLS[planet.name] || planet.name.slice(0, 2)}
                </text>
                {/* Planet name */}
                <text
                  x={x + 30}
                  y={y + 50 + idx * 20}
                  fontSize="12"
                  fill="#333"
                >
                  {planet.name}
                </text>
              </g>
            ))}
          </g>
        )}

        {/* Center cell - show chart title */}
        {isCenter && (
          <>
            <text
              x={x + cellSize / 2}
              y={y + cellSize / 2 - 5}
              fontSize="14"
              fontWeight="bold"
              textAnchor="middle"
              fill="#666"
            >
              {info.name}
            </text>
            <text
              x={x + cellSize / 2}
              y={y + cellSize / 2 + 12}
              fontSize="11"
              textAnchor="middle"
              fill="#999"
            >
              {info.purpose}
            </text>
          </>
        )}
      </g>
    );
  };

  return (
    <div className="divisional-chart">
      <svg
        width={size}
        height={size}
        viewBox={`0 0 ${size} ${size}`}
        style={{ border: `2px solid ${info.color}`, borderRadius: '8px' }}
      >
        {/* Background */}
        <rect width={size} height={size} fill="#fafafa" />

        {/* Title */}
        <text
          x={size / 2}
          y={25}
          fontSize="18"
          fontWeight="bold"
          textAnchor="middle"
          fill="#333"
        >
          {info.name} - {info.purpose}
        </text>

        {/* Render all cells in 4x3 grid */}
        {[0, 1, 2, 3].map(row => 
          [0, 1, 2].map(col => renderCell(row, col))
        )}

        {/* Legend */}
        <g transform={`translate(${padding}, ${size - 25})`}>
          <text fontSize="11" fill="#666">
            D{division} As = {info.name} Ascendant | Divisional chart for {info.purpose}
          </text>
        </g>
      </svg>
    </div>
  );
}
