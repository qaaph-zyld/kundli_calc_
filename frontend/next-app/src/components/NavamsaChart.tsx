"use client";
import React from 'react';

interface Planet { name: string; sign?: string; sign_num?: number; longitude: number; navamsa_sign?: number; }

interface ChartData { planetary_positions?: Record<string, any>; houses?: any; divisional_charts?: any; }

interface NavamsaChartProps {
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
 * Calculate Navamsa (D9) position
 * Each sign is divided into 9 parts of 3°20' each
 * Formula: ((sign_num - 1) * 9 + floor(longitude_in_sign / 3.333)) % 12 + 1
 */
function calculateNavamsaSign(signNum: number, longitude: number): number {
  // Get longitude within the sign (0-30 degrees)
  const longitudeInSign = longitude % 30;
  
  // Each navamsa is 3°20' (3.333 degrees)
  const navamsaPart = Math.floor(longitudeInSign / 3.333333);
  
  // Calculate navamsa sign
  const navamsaSign = ((signNum - 1) * 9 + navamsaPart) % 12 + 1;
  
  return navamsaSign;
}

/**
 * Navamsa Chart Component (D9 Divisional Chart)
 * Used for marriage, relationships, and spiritual path analysis
 */
export default function NavamsaChart({ data, size = 600 }: NavamsaChartProps) {
  const padding = 40;
  const chartSize = size - padding * 2;
  const cellSize = chartSize / 4;
  const degToSign = (deg: number) => Math.floor((((deg % 360) + 360) % 360) / 30) + 1;

  // Calculate Navamsa ascendant: prefer backend D9 cusp[0], fallback to rasi-derived
  const d9: any = (data as any)?.divisional_charts?.D9;
  const navamsaAscendantSign = (() => {
    if (d9?.house_cusps && Array.isArray(d9.house_cusps) && d9.house_cusps.length > 0) {
      const cusp0 = parseFloat(String(d9.house_cusps[0]));
      if (Number.isFinite(cusp0)) return degToSign(cusp0);
    }
    const rasiAscVal: any = (data as any)?.houses?.ascendant;
    const ascDeg = parseFloat(String(rasiAscVal ?? 0));
    const signNum = degToSign(ascDeg);
    return calculateNavamsaSign(signNum, ascDeg % 30);
  })();

  // Calculate Navamsa positions: prefer backend D9 planetary_positions, fallback to compute
  const planetsWithNavamsa = React.useMemo(() => {
    const out: Record<number, Planet[]> = {};
    const backend = d9?.planetary_positions;
    if (backend) {
      Object.entries(backend).forEach(([name, p]: any) => {
        const lon = parseFloat(String(p?.longitude ?? 0));
        const navSign = degToSign(lon);
        const houseNum = ((navSign - navamsaAscendantSign + 12) % 12) + 1;
        if (!out[houseNum]) out[houseNum] = [];
        out[houseNum].push({ name, longitude: lon, navamsa_sign: navSign });
      });
      return out;
    }
    if (data?.planetary_positions) {
      Object.entries(data.planetary_positions).forEach(([name, p]: any) => {
        const lon = parseFloat(String(p?.longitude ?? 0));
        const signNum = typeof p?.sign_num === 'number' ? p.sign_num : degToSign(lon);
        const navSign = calculateNavamsaSign(signNum, lon % 30);
        const houseNum = ((navSign - navamsaAscendantSign + 12) % 12) + 1;
        if (!out[houseNum]) out[houseNum] = [];
        out[houseNum].push({ name, longitude: lon, navamsa_sign: navSign });
      });
    }
    return out;
  }, [data, d9, navamsaAscendantSign]);

  // Map zodiac sign to standard South Indian layout (fixed signs)
  const getSignPosition = (signNum: number): { row: number; col: number } => {
    const positions = [
      { row: 1, col: 1 }, // 1 Aries
      { row: 2, col: 1 }, // 2 Taurus
      { row: 2, col: 2 }, // 3 Gemini
      { row: 3, col: 2 }, // 4 Cancer
      { row: 3, col: 1 }, // 5 Leo
      { row: 3, col: 0 }, // 6 Virgo
      { row: 2, col: 0 }, // 7 Libra
      { row: 1, col: 0 }, // 8 Scorpio
      { row: 0, col: 0 }, // 9 Sagittarius
      { row: 0, col: 1 }, // 10 Capricorn
      { row: 0, col: 2 }, // 11 Aquarius
      { row: 1, col: 2 }, // 12 Pisces
    ];
    return positions[(signNum - 1 + 12) % 12];
  };

  const getHouseNumber = (signNum: number): number => {
    return ((signNum - navamsaAscendantSign + 12) % 12) + 1;
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
    const planetsInHouse = planetsWithNavamsa[houseNum] || [];
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
          fill={isAscendant ? '#e8f5e9' : '#ffffff'}
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
            fill="#4caf50"
          >
            D9 As
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
                  fill="#2e7d32"
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
          <text
            x={x + cellSize / 2}
            y={y + cellSize / 2}
            fontSize="14"
            fontWeight="bold"
            textAnchor="middle"
            fill="#666"
          >
            Navamsa (D9)
          </text>
        )}
      </g>
    );
  };

  return (
    <div className="navamsa-chart">
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
          Navamsa Chart (D9) - Marriage & Spirituality
        </text>

        {/* Render all cells in 4x3 grid */}
        {[0, 1, 2, 3].map(row => 
          [0, 1, 2].map(col => renderCell(row, col))
        )}

        {/* Legend */}
        <g transform={`translate(${padding}, ${size - 25})`}>
          <text fontSize="11" fill="#666">
            D9 As = Navamsa Ascendant | Each sign divided into 9 parts (3°20')
          </text>
        </g>
      </svg>
    </div>
  );
}
