"use client";
import React from 'react';

interface Planet {
  name: string;
  sign: string;
  sign_num: number;
  longitude: number;
  house: number;
}

interface ChartData {
  planetary_positions?: Record<string, Planet>;
  houses?: {
    ascendant: { sign: string; sign_num: number };
    [key: string]: any;
  };
}

interface SouthIndianChartProps {
  data: ChartData;
  size?: number;
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

/**
 * South Indian Chart Component
 * 
 * Layout (counter-clockwise from ascendant):
 *     12 | 1  | 2
 *     ---+----+---
 *     11 | As | 3
 *     ---+----+---
 *     10 | 9  | 4
 *     ---+----+---
 *      8 | 7  | 6
 *        5
 */
export default function SouthIndianChart({ data, size = 600 }: SouthIndianChartProps) {
  const padding = 40;
  const chartSize = size - padding * 2;
  const cellSize = chartSize / 4;

  // Get ascendant sign number (1-12, where 1=Aries)
  const ascendantSignNum = data?.houses?.ascendant?.sign_num || 1;

  // Group planets by house
  const planetsByHouse = React.useMemo(() => {
    const houses: Record<number, Planet[]> = {};
    if (data?.planetary_positions) {
      Object.entries(data.planetary_positions).forEach(([name, planet]) => {
        const houseNum = planet.house || planet.sign_num;
        if (!houses[houseNum]) houses[houseNum] = [];
        houses[houseNum].push({ ...planet, name });
      });
    }
    return houses;
  }, [data]);

  // Map zodiac sign to position in South Indian chart
  // In South Indian chart, signs are fixed, not houses
  // Sign 1 (Aries) is always in position 2 (top-center-right)
  const getSignPosition = (signNum: number): { row: number; col: number } => {
    // Positions in South Indian chart (counter-clockwise from top-right)
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

  // Get house number from sign number based on ascendant
  const getHouseNumber = (signNum: number): number => {
    return ((signNum - ascendantSignNum + 12) % 12) + 1;
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
    const planetsInHouse = planetsByHouse[houseNum] || [];
    const isAscendant = houseNum === 1;

    // For center cell (row 1, col 1), show ascendant sign
    const isCenter = row === 1 && col === 1;

    return (
      <g key={`cell-${row}-${col}`}>
        {/* Cell rectangle */}
        <rect
          x={x}
          y={y}
          width={cellSize}
          height={cellSize}
          fill={isAscendant ? '#fffacd' : '#ffffff'}
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
            fontSize="16"
            fontWeight="bold"
            textAnchor="middle"
            fill="#d32f2f"
          >
            As
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
                  fill="#1976d2"
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
                {/* Planet degree */}
                <text
                  x={x + cellSize - 8}
                  y={y + 50 + idx * 20}
                  fontSize="10"
                  textAnchor="end"
                  fill="#666"
                >
                  {planet.longitude.toFixed(1)}°
                </text>
              </g>
            ))}
          </g>
        )}

        {/* Center cell - show chart title */}
        {isCenter && (
          <text
            x={x + cellSize / 2}
            y={y + cellSize / 2}
            fontSize="14"
            fontWeight="bold"
            textAnchor="middle"
            fill="#666"
          >
            Birth Chart
          </text>
        )}
      </g>
    );
  };

  return (
    <div className="south-indian-chart">
      <svg
        width={size}
        height={size}
        viewBox={`0 0 ${size} ${size}`}
        style={{ border: '1px solid #ddd', borderRadius: '8px' }}
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
          South Indian Chart (Rasi)
        </text>

        {/* Render all cells in 4x3 grid */}
        {[0, 1, 2, 3].map(row => 
          [0, 1, 2].map(col => renderCell(row, col))
        )}

        {/* Legend */}
        <g transform={`translate(${padding}, ${size - 25})`}>
          <text fontSize="11" fill="#666">
            As = Ascendant | Numbers = Houses | Symbols = Planets
          </text>
        </g>
      </svg>
    </div>
  );
}
