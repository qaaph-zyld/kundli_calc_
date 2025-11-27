'use client';

import React, { useState, useEffect } from 'react';

interface FamousChart {
  key: string;
  name: string;
  birth_date: string;
  birth_place: string;
  latitude?: number;
  longitude?: number;
  timezone?: number;
  category: string;
  description: string;
}

interface FamousChartsPanelProps {
  onSelectChart?: (chart: FamousChart) => void;
}

const CATEGORIES = [
  { id: 'all', label: 'All' },
  { id: 'Politics', label: '🏛️ Politics' },
  { id: 'Science', label: '🔬 Science' },
  { id: 'Spiritual', label: '🕉️ Spiritual' },
  { id: 'Entertainment', label: '🎬 Entertainment' },
  { id: 'Sports', label: '⚽ Sports' },
  { id: 'Business', label: '💼 Business' },
];

export default function FamousChartsPanel({ onSelectChart }: FamousChartsPanelProps) {
  const [charts, setCharts] = useState<FamousChart[]>([]);
  const [selectedCategory, setSelectedCategory] = useState('all');
  const [searchQuery, setSearchQuery] = useState('');
  const [loading, setLoading] = useState(false);
  const [selectedChart, setSelectedChart] = useState<FamousChart | null>(null);

  const fetchCharts = async (category?: string) => {
    setLoading(true);
    try {
      const url = category && category !== 'all'
        ? `http://localhost:8000/api/v1/famous-charts/list?category=${category}`
        : 'http://localhost:8000/api/v1/famous-charts/list';
      
      const response = await fetch(url);
      if (response.ok) {
        const data = await response.json();
        setCharts(data);
      }
    } catch (error) {
      console.error('Error fetching famous charts:', error);
      // Use fallback data
      setCharts(FALLBACK_CHARTS);
    } finally {
      setLoading(false);
    }
  };

  const fetchChartDetails = async (key: string) => {
    try {
      const response = await fetch(`http://localhost:8000/api/v1/famous-charts/${key}`);
      if (response.ok) {
        const data = await response.json();
        setSelectedChart(data);
        if (onSelectChart) {
          onSelectChart(data);
        }
      }
    } catch (error) {
      console.error('Error fetching chart details:', error);
    }
  };

  useEffect(() => {
    fetchCharts(selectedCategory);
  }, [selectedCategory]);

  const filteredCharts = searchQuery
    ? charts.filter(c => 
        c.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
        c.description.toLowerCase().includes(searchQuery.toLowerCase())
      )
    : charts;

  const formatDate = (dateStr: string) => {
    try {
      const date = new Date(dateStr);
      return date.toLocaleDateString('en-IN', {
        day: 'numeric',
        month: 'short',
        year: 'numeric',
      });
    } catch {
      return dateStr;
    }
  };

  return (
    <div style={{
      backgroundColor: 'white',
      borderRadius: '12px',
      padding: '1rem',
      boxShadow: '0 1px 3px rgba(0,0,0,0.1)',
    }}>
      <h3 style={{ margin: '0 0 1rem', fontSize: '1.1rem', fontWeight: 600 }}>
        ⭐ Famous Charts
      </h3>

      {/* Search */}
      <input
        type="text"
        placeholder="Search by name..."
        value={searchQuery}
        onChange={(e) => setSearchQuery(e.target.value)}
        style={{
          width: '100%',
          padding: '0.5rem 0.75rem',
          borderRadius: '6px',
          border: '1px solid #d1d5db',
          marginBottom: '0.75rem',
          fontSize: '0.9rem',
        }}
      />

      {/* Category filter */}
      <div style={{
        display: 'flex',
        gap: '0.25rem',
        marginBottom: '0.75rem',
        flexWrap: 'wrap',
      }}>
        {CATEGORIES.map((cat) => (
          <button
            key={cat.id}
            onClick={() => setSelectedCategory(cat.id)}
            style={{
              padding: '0.25rem 0.5rem',
              fontSize: '0.75rem',
              borderRadius: '4px',
              border: '1px solid #d1d5db',
              backgroundColor: selectedCategory === cat.id ? '#3b82f6' : 'white',
              color: selectedCategory === cat.id ? 'white' : '#374151',
              cursor: 'pointer',
            }}
          >
            {cat.label}
          </button>
        ))}
      </div>

      {/* Charts list */}
      {loading ? (
        <div style={{ textAlign: 'center', padding: '2rem', color: '#6b7280' }}>
          Loading...
        </div>
      ) : (
        <div style={{
          maxHeight: '400px',
          overflowY: 'auto',
        }}>
          {filteredCharts.length === 0 ? (
            <div style={{ textAlign: 'center', padding: '2rem', color: '#6b7280' }}>
              No charts found
            </div>
          ) : (
            <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
              {filteredCharts.map((chart) => (
                <div
                  key={chart.key}
                  onClick={() => fetchChartDetails(chart.key)}
                  style={{
                    padding: '0.75rem',
                    borderRadius: '8px',
                    border: '1px solid #e5e7eb',
                    cursor: 'pointer',
                    backgroundColor: selectedChart?.key === chart.key ? '#eff6ff' : 'white',
                    transition: 'background-color 0.15s',
                  }}
                  onMouseEnter={(e) => {
                    if (selectedChart?.key !== chart.key) {
                      e.currentTarget.style.backgroundColor = '#f9fafb';
                    }
                  }}
                  onMouseLeave={(e) => {
                    if (selectedChart?.key !== chart.key) {
                      e.currentTarget.style.backgroundColor = 'white';
                    }
                  }}
                >
                  <div style={{ 
                    display: 'flex', 
                    justifyContent: 'space-between',
                    alignItems: 'flex-start',
                  }}>
                    <div>
                      <div style={{ fontWeight: 600, fontSize: '0.95rem' }}>
                        {chart.name}
                      </div>
                      <div style={{ fontSize: '0.8rem', color: '#6b7280' }}>
                        {chart.description}
                      </div>
                    </div>
                    <span style={{
                      fontSize: '0.7rem',
                      padding: '0.15rem 0.4rem',
                      backgroundColor: '#f3f4f6',
                      borderRadius: '4px',
                      color: '#4b5563',
                    }}>
                      {chart.category}
                    </span>
                  </div>
                  <div style={{
                    marginTop: '0.5rem',
                    fontSize: '0.75rem',
                    color: '#9ca3af',
                  }}>
                    📅 {formatDate(chart.birth_date)} • 📍 {chart.birth_place}
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      )}

      {/* Selected chart details */}
      {selectedChart && (
        <div style={{
          marginTop: '1rem',
          padding: '0.75rem',
          backgroundColor: '#f0fdf4',
          borderRadius: '8px',
          fontSize: '0.85rem',
        }}>
          <div style={{ fontWeight: 600, marginBottom: '0.5rem' }}>
            Selected: {selectedChart.name}
          </div>
          <div style={{ color: '#374151' }}>
            <div>📅 {formatDate(selectedChart.birth_date)}</div>
            <div>📍 {selectedChart.birth_place}</div>
            {selectedChart.latitude && (
              <div>🌐 {selectedChart.latitude.toFixed(4)}°N, {selectedChart.longitude?.toFixed(4)}°E</div>
            )}
            {selectedChart.timezone !== undefined && (
              <div>🕐 UTC{selectedChart.timezone >= 0 ? '+' : ''}{selectedChart.timezone}</div>
            )}
          </div>
          <button
            onClick={() => onSelectChart && onSelectChart(selectedChart)}
            style={{
              marginTop: '0.5rem',
              padding: '0.5rem 1rem',
              backgroundColor: '#10b981',
              color: 'white',
              border: 'none',
              borderRadius: '6px',
              cursor: 'pointer',
              fontSize: '0.85rem',
              fontWeight: 500,
            }}
          >
            Load This Chart
          </button>
        </div>
      )}
    </div>
  );
}

// Fallback data when API is unavailable
const FALLBACK_CHARTS: FamousChart[] = [
  { key: "narendra_modi", name: "Narendra Modi", birth_date: "1950-09-17T11:00:00", birth_place: "Vadnagar, Gujarat, India", category: "Politics", description: "Prime Minister of India" },
  { key: "mahatma_gandhi", name: "Mahatma Gandhi", birth_date: "1869-10-02T07:12:00", birth_place: "Porbandar, Gujarat, India", category: "Politics", description: "Father of the Indian Nation" },
  { key: "albert_einstein", name: "Albert Einstein", birth_date: "1879-03-14T11:30:00", birth_place: "Ulm, Germany", category: "Science", description: "Theoretical Physicist" },
  { key: "swami_vivekananda", name: "Swami Vivekananda", birth_date: "1863-01-12T06:33:00", birth_place: "Kolkata, India", category: "Spiritual", description: "Hindu monk, key figure in Vedanta" },
  { key: "sachin_tendulkar", name: "Sachin Tendulkar", birth_date: "1973-04-24T16:15:00", birth_place: "Mumbai, India", category: "Sports", description: "Cricket Legend" },
  { key: "amitabh_bachchan", name: "Amitabh Bachchan", birth_date: "1942-10-11T16:00:00", birth_place: "Allahabad, India", category: "Entertainment", description: "Bollywood Actor" },
  { key: "steve_jobs", name: "Steve Jobs", birth_date: "1955-02-24T19:15:00", birth_place: "San Francisco, USA", category: "Business", description: "Co-founder of Apple" },
  { key: "elon_musk", name: "Elon Musk", birth_date: "1971-06-28T07:00:00", birth_place: "Pretoria, South Africa", category: "Business", description: "CEO of Tesla and SpaceX" },
];
