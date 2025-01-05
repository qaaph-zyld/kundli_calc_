import React from 'react';
import { render, screen } from '@testing-library/react';
import KundliChart from '../KundliChart';

// Mock D3 since it manipulates DOM directly
jest.mock('d3', () => ({
  select: () => ({
    selectAll: () => ({
      remove: jest.fn(),
    }),
    append: () => ({
      attr: () => ({
        attr: jest.fn(),
        style: jest.fn(),
      }),
    }),
  }),
}));

describe('KundliChart Component', () => {
  const mockPlanets = [
    {
      name: 'Sun',
      longitude: 45,
      house: 1,
      retrograde: false,
    },
    {
      name: 'Moon',
      longitude: 90,
      house: 2,
      retrograde: false,
    },
  ];

  const mockHouses = [
    {
      number: 1,
      startDegree: 0,
      endDegree: 30,
      sign: 'Aries',
    },
    {
      number: 2,
      startDegree: 30,
      endDegree: 60,
      sign: 'Taurus',
    },
  ];

  it('renders chart title', () => {
    render(
      <KundliChart
        planets={mockPlanets}
        houses={mockHouses}
      />
    );
    
    expect(screen.getByText(/Kundli Chart/i)).toBeInTheDocument();
  });

  it('renders with custom dimensions', () => {
    const { container } = render(
      <KundliChart
        planets={mockPlanets}
        houses={mockHouses}
        width={800}
        height={800}
      />
    );
    
    const svg = container.querySelector('svg');
    expect(svg).toHaveAttribute('width', '800');
    expect(svg).toHaveAttribute('height', '800');
  });

  it('updates when props change', () => {
    const { rerender } = render(
      <KundliChart
        planets={mockPlanets}
        houses={mockHouses}
      />
    );

    const newPlanets = [
      ...mockPlanets,
      {
        name: 'Mars',
        longitude: 120,
        house: 3,
        retrograde: true,
      },
    ];

    rerender(
      <KundliChart
        planets={newPlanets}
        houses={mockHouses}
      />
    );

    // Since we're mocking D3, we can only verify that the component re-renders
    expect(screen.getByText(/Kundli Chart/i)).toBeInTheDocument();
  });
});
