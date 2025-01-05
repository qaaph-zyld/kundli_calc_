import React, { useEffect, useRef } from 'react';
import { Box, Paper, Typography } from '@mui/material';
import * as d3 from 'd3';

interface Planet {
  name: string;
  longitude: number;
  house: number;
  retrograde: boolean;
}

interface House {
  number: number;
  startDegree: number;
  endDegree: number;
  sign: string;
}

interface KundliChartProps {
  planets: Planet[];
  houses: House[];
  width?: number;
  height?: number;
}

const KundliChart: React.FC<KundliChartProps> = ({
  planets,
  houses,
  width = 600,
  height = 600,
}) => {
  const svgRef = useRef<SVGSVGElement>(null);

  useEffect(() => {
    if (!svgRef.current) return;

    // Clear previous chart
    d3.select(svgRef.current).selectAll('*').remove();

    const svg = d3.select(svgRef.current)
      .attr('width', width)
      .attr('height', height);

    const radius = Math.min(width, height) / 2;
    const centerX = width / 2;
    const centerY = height / 2;

    // Create chart background
    const chartGroup = svg.append('g')
      .attr('transform', `translate(${centerX}, ${centerY})`);

    // Draw outer circle
    chartGroup.append('circle')
      .attr('r', radius)
      .attr('fill', 'none')
      .attr('stroke', '#000')
      .attr('stroke-width', 2);

    // Draw house divisions
    const houseAngle = 360 / 12;
    houses.forEach((house, i) => {
      const angle = i * houseAngle;
      const radians = (angle - 90) * Math.PI / 180;
      const x2 = radius * Math.cos(radians);
      const y2 = radius * Math.sin(radians);

      // Draw house lines
      chartGroup.append('line')
        .attr('x1', 0)
        .attr('y1', 0)
        .attr('x2', x2)
        .attr('y2', y2)
        .attr('stroke', '#000')
        .attr('stroke-width', 1);

      // Add house numbers
      const textRadius = radius * 0.85;
      const textX = textRadius * Math.cos(radians);
      const textY = textRadius * Math.sin(radians);

      chartGroup.append('text')
        .attr('x', textX)
        .attr('y', textY)
        .attr('text-anchor', 'middle')
        .attr('dominant-baseline', 'middle')
        .text(house.number.toString());
    });

    // Place planets
    planets.forEach((planet) => {
      const houseIndex = planet.house - 1;
      const baseAngle = houseIndex * houseAngle;
      const planetAngle = baseAngle + (planet.longitude % 30) * (houseAngle / 30);
      const radians = (planetAngle - 90) * Math.PI / 180;
      
      const planetRadius = radius * 0.7;
      const x = planetRadius * Math.cos(radians);
      const y = planetRadius * Math.sin(radians);

      // Planet symbol
      chartGroup.append('circle')
        .attr('cx', x)
        .attr('cy', y)
        .attr('r', 5)
        .attr('fill', planet.retrograde ? '#ff4444' : '#4444ff');

      // Planet label
      chartGroup.append('text')
        .attr('x', x)
        .attr('y', y - 10)
        .attr('text-anchor', 'middle')
        .attr('dominant-baseline', 'middle')
        .text(planet.name);
    });

  }, [planets, houses, width, height]);

  return (
    <Paper elevation={3} sx={{ p: 2, m: 2 }}>
      <Typography variant="h6" gutterBottom align="center">
        Kundli Chart
      </Typography>
      <Box sx={{ display: 'flex', justifyContent: 'center' }}>
        <svg ref={svgRef}></svg>
      </Box>
    </Paper>
  );
};

export default KundliChart;
