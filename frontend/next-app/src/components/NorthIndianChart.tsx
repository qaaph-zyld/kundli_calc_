"use client";
import React, { useState } from 'react';

interface Planet {
  name: string;
  sign: string;
  sign_num: number;
  longitude: number;
  house?: number;
}

interface ChartData {
  planetary_positions?: Record<string, Planet>;
  houses?: {
    ascendant: { sign: string; sign_num: number; longitude: number };
  };
}

interface NorthIndianChartProps {
  data: ChartData;
  size?: number;
}

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

const ZODIAC_SIGNS = [
  'Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo',
  'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces'
];

/**
 * North Indian Chart (Diamond Style)
 * Houses are fixed, signs rotate based on ascendant
 */
export default function NorthIndianChart({ data, size = 600 }: NorthIndianChartProps) {
  const [hoveredHouse, setHoveredHouse] = useState<number | null>(null);
  
  const padding = 40;
  const chartSize = size - padding * 2;
  const centerX = size / 2;
  const centerY = size / 2;
  const diamondSize = chartSize * 0.8;

  // Get ascendant sign number
  const ascendantSignNum = data?.houses?.ascendant?.sign_num || 1;

  // Calculate which sign is in which house
  const getSignInHouse = (houseNum: number): number => {
    // House 1 has ascendant sign, house 2 has next sign, etc.
    return ((ascendantSignNum - 1 + (houseNum - 1)) % 12) + 1;
  };

  // Group planets by house
  const planetsByHouse: Record<number, Planet[]> = {};
  if (data?.planetary_positions) {
    Object.entries(data.planetary_positions).forEach(([name, planet]) => {
      const houseNum = planet.house || 0;
      if (houseNum > 0) {
        if (!planetsByHouse[houseNum]) planetsByHouse[houseNum] = [];
        planetsByHouse[houseNum].push({ ...planet, name });
      }
    });
  }

  // Diamond house positions (clockwise from top)
  const housePositions = [
    { house: 1, cx: centerX, cy: centerY - diamondSize / 2, label: 'Asc' },       // Top
    { house: 2, cx: centerX + diamondSize / 4, cy: centerY - diamondSize / 4 },   // Top-right
    { house: 3, cx: centerX + diamondSize / 2, cy: centerY },                      // Right
    { house: 4, cx: centerX + diamondSize / 4, cy: centerY + diamondSize / 4 },   // Bottom-right
    { house: 5, cx: centerX, cy: centerY + diamondSize / 2 },                      // Bottom
    { house: 6, cx: centerX - diamondSize / 4, cy: centerY + diamondSize / 4 },   // Bottom-left
    { house: 7, cx: centerX - diamondSize / 2, cy: centerY },                      // Left
    { house: 8, cx: centerX - diamondSize / 4, cy: centerY - diamondSize / 4 },   // Top-left
    { house: 9, cx: centerX - diamondSize / 6, cy: centerY - diamondSize / 6 },   // Inner top-left
    { house: 10, cx: centerX + diamondSize / 6, cy: centerY - diamondSize / 6 },  // Inner top-right
    { house: 11, cx: centerX + diamondSize / 6, cy: centerY + diamondSize / 6 },  // Inner bottom-right
    { house: 12, cx: centerX - diamondSize / 6, cy: centerY + diamondSize / 6 },  // Inner bottom-left
  ];

  // Diamond path (outer houses)
  const diamondPath = `
    M ${centerX} ${centerY - diamondSize / 2}
    L ${centerX + diamondSize / 2} ${centerY}
    L ${centerX} ${centerY + diamondSize / 2}
    L ${centerX - diamondSize / 2} ${centerY}
    Z
  `;

  // Inner diamond (houses 9-12)
  const innerDiamondPath = `
    M ${centerX} ${centerY - diamondSize / 6}
    L ${centerX + diamondSize / 6} ${centerY}
    L ${centerX} ${centerY + diamondSize / 6}
    L ${centerX - diamondSize / 6} ${centerY}
    Z
  `;

  return (
    <div>
      <svg
        width={size}
        height={size}
        viewBox={`0 0 ${size} ${size}`}
        style={{ border: '2px solid #1976d2', borderRadius: '8px' }}
      >
        {/* Background */}
        <rect width={size} height={size} fill="#fafafa" />

        {/* Title */}
        <text
          x={centerX}
          y={25}
          fontSize="18"
          fontWeight="bold"
          textAnchor="middle"
          fill="#333"
        >
          North Indian Chart (Diamond Style)
        </text>

        {/* Outer Diamond */}
        <path
          d={diamondPath}
          fill="white"
          stroke="#333"
          strokeWidth="2"
        />

        {/* Inner Diamond */}
        <path
          d={innerDiamondPath}
          fill="white"
          stroke="#333"
          strokeWidth="2"
        />

        {/* Diagonal lines */}
        <line x1={centerX - diamondSize / 2} y1={centerY} x2={centerX + diamondSize / 2} y2={centerY} stroke="#333" strokeWidth="1" />
        <line x1={centerX} y1={centerY - diamondSize / 2} x2={centerX} y2={centerY + diamondSize / 2} stroke="#333" strokeWidth="1" />

        {/* Render houses */}
        {housePositions.map(({ house, cx, cy, label }) => {
          const signNum = getSignInHouse(house);
          const signName = ZODIAC_SIGNS[signNum - 1];
          const planets = planetsByHouse[house] || [];
          const isAscendant = house === 1;
          const isHovered = hoveredHouse === house;

          return (
            <g key={house}>
              {/* House highlight on hover */}
              {isHovered && (
                <circle
                  cx={cx}
                  cy={cy}
                  r={diamondSize / 8}
                  fill="rgba(25, 118, 210, 0.1)"
                />
              )}

              {/* House number */}
              <text
                x={cx}
                y={cy - 35}
                fontSize="10"
                textAnchor="middle"
                fill="#999"
              >
                H{house}
              </text>

              {/* Sign name */}
              <text
                x={cx}
                y={cy - 20}
                fontSize="12"
                fontWeight={isAscendant ? 'bold' : 'normal'}
                textAnchor="middle"
                fill={isAscendant ? '#1976d2' : '#666'}
              >
                {signName.slice(0, 3)}
                {isAscendant && ' (Asc)'}
              </text>

              {/* Planets in house */}
              {planets.map((planet, idx) => (
                <g key={planet.name}>
                  <text
                    x={cx - 20}
                    y={cy + idx * 18}
                    fontSize="16"
                    fill="#d32f2f"
                    onMouseEnter={() => setHoveredHouse(house)}
                    onMouseLeave={() => setHoveredHouse(null)}
                    style={{ cursor: 'pointer' }}
                  >
                    {PLANET_SYMBOLS[planet.name] || planet.name.slice(0, 2)}
                  </text>
                  <text
                    x={cx}
                    y={cy + idx * 18}
                    fontSize="11"
                    fill="#333"
                  >
                    {planet.name}
                  </text>
                </g>
              ))}

              {/* Hover info */}
              {isHovered && planets.length > 0 && (
                <g>
                  <rect
                    x={cx + 50}
                    y={cy - 30}
                    width="150"
                    height={30 + planets.length * 20}
                    fill="white"
                    stroke="#1976d2"
                    strokeWidth="1"
                    rx="4"
                  />
                  <text x={cx + 60} y={cy - 10} fontSize="12" fontWeight="bold" fill="#333">
                    {signName} ({house}th House)
                  </text>
                  {planets.map((p, i) => (
                    <text key={i} x={cx + 60} y={cy + 10 + i * 20} fontSize="11" fill="#666">
                      {p.name}: {p.longitude.toFixed(2)}°
                    </text>
                  ))}
                </g>
              )}
            </g>
          );
        })}

        {/* Legend */}
        <text x={padding} y={size - 15} fontSize="11" fill="#666">
          Ascendant: {data?.houses?.ascendant?.sign || 'N/A'} | Fixed houses, rotating signs
        </text>
      </svg>
    </div>
  );
}
