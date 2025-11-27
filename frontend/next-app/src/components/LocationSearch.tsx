'use client';

import React, { useState, useEffect, useCallback } from 'react';

interface LocationResult {
  city: string;
  state: string;
  country: string;
  latitude: number;
  longitude: number;
  timezone: string;
  utc_offset: number;
  display_name: string;
}

interface LocationSearchProps {
  onSelect: (location: LocationResult) => void;
  placeholder?: string;
}

export default function LocationSearch({ onSelect, placeholder = "Search city..." }: LocationSearchProps) {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState<LocationResult[]>([]);
  const [loading, setLoading] = useState(false);
  const [showDropdown, setShowDropdown] = useState(false);

  const searchLocations = useCallback(async (searchQuery: string) => {
    if (searchQuery.length < 2) {
      setResults([]);
      return;
    }

    setLoading(true);
    try {
      const response = await fetch(
        `http://localhost:8000/api/v1/location/search?q=${encodeURIComponent(searchQuery)}&limit=5`
      );
      
      if (response.ok) {
        const data = await response.json();
        setResults(data.results || []);
        setShowDropdown(true);
      }
    } catch (error) {
      console.error('Location search error:', error);
      // Fallback to manual data for common cities
      const fallback = getFallbackResults(searchQuery);
      setResults(fallback);
      setShowDropdown(fallback.length > 0);
    } finally {
      setLoading(false);
    }
  }, []);

  // Debounce search
  useEffect(() => {
    const timer = setTimeout(() => {
      if (query) {
        searchLocations(query);
      }
    }, 300);

    return () => clearTimeout(timer);
  }, [query, searchLocations]);

  const handleSelect = (location: LocationResult) => {
    setQuery(location.display_name || `${location.city}, ${location.country}`);
    setShowDropdown(false);
    onSelect(location);
  };

  return (
    <div style={{ position: 'relative', width: '100%' }}>
      <input
        type="text"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        onFocus={() => results.length > 0 && setShowDropdown(true)}
        placeholder={placeholder}
        style={{
          width: '100%',
          padding: '0.75rem 1rem',
          fontSize: '1rem',
          border: '1px solid #d1d5db',
          borderRadius: '8px',
          outline: 'none',
        }}
      />
      
      {loading && (
        <div style={{
          position: 'absolute',
          right: '12px',
          top: '50%',
          transform: 'translateY(-50%)',
          color: '#6b7280',
        }}>
          ⏳
        </div>
      )}

      {showDropdown && results.length > 0 && (
        <div
          style={{
            position: 'absolute',
            top: '100%',
            left: 0,
            right: 0,
            backgroundColor: 'white',
            border: '1px solid #d1d5db',
            borderRadius: '8px',
            marginTop: '4px',
            boxShadow: '0 4px 6px -1px rgba(0,0,0,0.1)',
            zIndex: 1000,
            maxHeight: '300px',
            overflowY: 'auto',
          }}
        >
          {results.map((result, index) => (
            <div
              key={index}
              onClick={() => handleSelect(result)}
              style={{
                padding: '0.75rem 1rem',
                cursor: 'pointer',
                borderBottom: index < results.length - 1 ? '1px solid #f3f4f6' : 'none',
              }}
              onMouseEnter={(e) => {
                e.currentTarget.style.backgroundColor = '#f9fafb';
              }}
              onMouseLeave={(e) => {
                e.currentTarget.style.backgroundColor = 'white';
              }}
            >
              <div style={{ fontWeight: 500 }}>
                {result.city}{result.state ? `, ${result.state}` : ''}
              </div>
              <div style={{ fontSize: '0.85rem', color: '#6b7280' }}>
                {result.country} • {result.latitude.toFixed(4)}°, {result.longitude.toFixed(4)}°
              </div>
              <div style={{ fontSize: '0.8rem', color: '#9ca3af' }}>
                Timezone: {result.timezone} (UTC{result.utc_offset >= 0 ? '+' : ''}{result.utc_offset})
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

// Fallback data for common cities when API is unavailable
function getFallbackResults(query: string): LocationResult[] {
  const cities: LocationResult[] = [
    { city: "Delhi", state: "Delhi", country: "India", latitude: 28.6139, longitude: 77.2090, timezone: "Asia/Kolkata", utc_offset: 5.5, display_name: "New Delhi, Delhi, India" },
    { city: "Mumbai", state: "Maharashtra", country: "India", latitude: 19.0760, longitude: 72.8777, timezone: "Asia/Kolkata", utc_offset: 5.5, display_name: "Mumbai, Maharashtra, India" },
    { city: "Bangalore", state: "Karnataka", country: "India", latitude: 12.9716, longitude: 77.5946, timezone: "Asia/Kolkata", utc_offset: 5.5, display_name: "Bangalore, Karnataka, India" },
    { city: "Chennai", state: "Tamil Nadu", country: "India", latitude: 13.0827, longitude: 80.2707, timezone: "Asia/Kolkata", utc_offset: 5.5, display_name: "Chennai, Tamil Nadu, India" },
    { city: "Kolkata", state: "West Bengal", country: "India", latitude: 22.5726, longitude: 88.3639, timezone: "Asia/Kolkata", utc_offset: 5.5, display_name: "Kolkata, West Bengal, India" },
    { city: "Hyderabad", state: "Telangana", country: "India", latitude: 17.3850, longitude: 78.4867, timezone: "Asia/Kolkata", utc_offset: 5.5, display_name: "Hyderabad, Telangana, India" },
    { city: "Pune", state: "Maharashtra", country: "India", latitude: 18.5204, longitude: 73.8567, timezone: "Asia/Kolkata", utc_offset: 5.5, display_name: "Pune, Maharashtra, India" },
    { city: "Jaipur", state: "Rajasthan", country: "India", latitude: 26.9124, longitude: 75.7873, timezone: "Asia/Kolkata", utc_offset: 5.5, display_name: "Jaipur, Rajasthan, India" },
    { city: "London", state: "", country: "United Kingdom", latitude: 51.5074, longitude: -0.1278, timezone: "Europe/London", utc_offset: 0, display_name: "London, United Kingdom" },
    { city: "New York", state: "New York", country: "USA", latitude: 40.7128, longitude: -74.0060, timezone: "America/New_York", utc_offset: -5, display_name: "New York, NY, USA" },
    { city: "Los Angeles", state: "California", country: "USA", latitude: 34.0522, longitude: -118.2437, timezone: "America/Los_Angeles", utc_offset: -8, display_name: "Los Angeles, CA, USA" },
    { city: "Tokyo", state: "", country: "Japan", latitude: 35.6762, longitude: 139.6503, timezone: "Asia/Tokyo", utc_offset: 9, display_name: "Tokyo, Japan" },
    { city: "Singapore", state: "", country: "Singapore", latitude: 1.3521, longitude: 103.8198, timezone: "Asia/Singapore", utc_offset: 8, display_name: "Singapore" },
    { city: "Dubai", state: "", country: "UAE", latitude: 25.2048, longitude: 55.2708, timezone: "Asia/Dubai", utc_offset: 4, display_name: "Dubai, UAE" },
    { city: "Sydney", state: "NSW", country: "Australia", latitude: -33.8688, longitude: 151.2093, timezone: "Australia/Sydney", utc_offset: 10, display_name: "Sydney, NSW, Australia" },
    { city: "Loznica", state: "Serbia", country: "Serbia", latitude: 44.5333, longitude: 19.2261, timezone: "Europe/Belgrade", utc_offset: 1, display_name: "Loznica, Serbia" },
    { city: "Belgrade", state: "", country: "Serbia", latitude: 44.7866, longitude: 20.4489, timezone: "Europe/Belgrade", utc_offset: 1, display_name: "Belgrade, Serbia" },
  ];

  const lowerQuery = query.toLowerCase();
  return cities.filter(c => 
    c.city.toLowerCase().includes(lowerQuery) ||
    c.country.toLowerCase().includes(lowerQuery) ||
    c.state.toLowerCase().includes(lowerQuery)
  ).slice(0, 5);
}
