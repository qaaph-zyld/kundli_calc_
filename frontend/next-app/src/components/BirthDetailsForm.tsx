"use client";
import React, { useEffect, useState } from 'react';
import styles from './BirthDetailsForm.module.css';
import { resolvePlace, timezoneFromCoords } from '../lib/api';

export interface BirthDetails {
  date: string; // YYYY-MM-DD
  time: string; // HH:MM
  latitude: number;
  longitude: number;
  timezone: string;
  locationName: string;
  ayanamsa_type: string;
  house_system: string;
}

interface BirthDetailsFormProps {
  onSubmit: (details: BirthDetails) => void;
  loading?: boolean;
}

export default function BirthDetailsForm({ onSubmit, loading = false }: BirthDetailsFormProps) {
  const [formData, setFormData] = useState<BirthDetails>(() => {
    if (typeof window !== 'undefined') {
      try {
        const saved = localStorage.getItem('birthDetails');
        if (saved) return JSON.parse(saved);
      } catch {}
    }
    return {
      date: '1990-10-09',
      time: '08:10',
      latitude: 44.5333,
      longitude: 19.2333,
      timezone: 'UTC',
      locationName: 'Loznica, Serbia',
      ayanamsa_type: 'lahiri',
      house_system: 'W',
    };
  });

  useEffect(() => {
    try { localStorage.setItem('birthDetails', JSON.stringify(formData)); } catch {}
  }, [formData]);

  const [geoLoading, setGeoLoading] = useState(false);
  const [geoError, setGeoError] = useState<string | null>(null);

  const [errors, setErrors] = useState<Partial<Record<keyof BirthDetails, string>>>({});

  const validate = (): boolean => {
    const newErrors: Partial<Record<keyof BirthDetails, string>> = {};

    if (!formData.date) newErrors.date = 'Date is required';
    if (!formData.time) newErrors.time = 'Time is required';
    if (formData.latitude < -90 || formData.latitude > 90) {
      newErrors.latitude = 'Latitude must be between -90 and 90';
    }
    if (formData.longitude < -180 || formData.longitude > 180) {
      newErrors.longitude = 'Longitude must be between -180 and 180';
    }
    if (!formData.locationName) newErrors.locationName = 'Location name is required';

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (validate()) {
      onSubmit(formData);
    }
  };

  const handleChange = (field: keyof BirthDetails, value: string | number) => {
    setFormData(prev => ({ ...prev, [field]: value }));
    // Clear error for this field
    if (errors[field]) {
      setErrors(prev => ({ ...prev, [field]: undefined }));
    }
  };

  const handleResolvePlace = async () => {
    if (!formData.locationName) { setGeoError('Enter a location name'); return; }
    setGeoError(null); setGeoLoading(true);
    try {
      const res = await resolvePlace(formData.locationName);
      const tz = await timezoneFromCoords(res.latitude, res.longitude);
      setFormData(prev => ({
        ...prev,
        latitude: res.latitude,
        longitude: res.longitude,
        timezone: tz.timezone,
        locationName: res.display_name,
      }));
    } catch (e: any) {
      setGeoError(e?.message || String(e));
    } finally { setGeoLoading(false); }
  };

  const handleDetectTimezone = async () => {
    setGeoError(null); setGeoLoading(true);
    try {
      const tz = await timezoneFromCoords(formData.latitude, formData.longitude);
      setFormData(prev => ({ ...prev, timezone: tz.timezone }));
    } catch (e: any) {
      setGeoError(e?.message || String(e));
    } finally { setGeoLoading(false); }
  };

  return (
    <form onSubmit={handleSubmit} className={styles.form}>
      <div className={styles.grid}>
        {/* Date and Time */}
        <div className={styles.section}>
          <h3>Birth Date & Time</h3>
          <div className={styles.row}>
            <div className={styles.group}>
              <label htmlFor="date">Date *</label>
              <input
                id="date"
                type="date"
                value={formData.date}
                onChange={(e) => handleChange('date', e.target.value)}
                disabled={loading}
                required
              />
              {errors.date && <span className={styles.error}>{errors.date}</span>}
            </div>

            <div className={styles.group}>
              <label htmlFor="time">Time (24h) *</label>
              <input
                id="time"
                type="time"
                value={formData.time}
                onChange={(e) => handleChange('time', e.target.value)}
                disabled={loading}
                required
              />
              {errors.time && <span className={styles.error}>{errors.time}</span>}
            </div>
          </div>
        </div>

        {/* Location */}
        <div className={styles.section}>
          <h3>Birth Location</h3>
          <div className={styles.group}>
            <label htmlFor="locationName">Location Name *</label>
            <input
              id="locationName"
              type="text"
              placeholder="City, Country"
              value={formData.locationName}
              onChange={(e) => handleChange('locationName', e.target.value)}
              disabled={loading}
              required
            />
            <div className={styles.inlineActions}>
              <button type="button" onClick={handleResolvePlace} disabled={loading || geoLoading} className={styles.btnSecondary}>Search</button>
              <button type="button" onClick={handleDetectTimezone} disabled={loading || geoLoading} className={styles.btnTertiary}>Detect Timezone</button>
            </div>
            {errors.locationName && <span className={styles.error}>{errors.locationName}</span>}
            {geoError && <span className={styles.error}>{geoError}</span>}
          </div>

          <div className={styles.row}>
            <div className={styles.group}>
              <label htmlFor="latitude">Latitude *</label>
              <input
                id="latitude"
                type="number"
                step="0.000001"
                min="-90"
                max="90"
                placeholder="44.531346"
                value={formData.latitude}
                onChange={(e) => handleChange('latitude', parseFloat(e.target.value))}
                disabled={loading}
                required
              />
              {errors.latitude && <span className={styles.error}>{errors.latitude}</span>}
            </div>

            <div className={styles.group}>
              <label htmlFor="longitude">Longitude *</label>
              <input
                id="longitude"
                type="number"
                step="0.000001"
                min="-180"
                max="180"
                placeholder="19.206766"
                value={formData.longitude}
                onChange={(e) => handleChange('longitude', parseFloat(e.target.value))}
                disabled={loading}
                required
              />
              {errors.longitude && <span className={styles.error}>{errors.longitude}</span>}
            </div>
          </div>

          <div className={styles.group}>
            <label htmlFor="timezone">Timezone</label>
            <select
              id="timezone"
              value={formData.timezone}
              onChange={(e) => handleChange('timezone', e.target.value)}
              disabled={loading}
            >
              <option value="UTC">UTC</option>
              <option value="Asia/Kolkata">IST (India)</option>
              <option value="America/New_York">EST (New York)</option>
              <option value="America/Los_Angeles">PST (Los Angeles)</option>
              <option value="Europe/London">GMT (London)</option>
              <option value="Europe/Belgrade">CET (Belgrade)</option>
            </select>
          </div>
        </div>

        {/* Calculation Settings */}
        <div className={styles.section}>
          <h3>Settings</h3>
          <div className={styles.row}>
            <div className={styles.group}>
              <label htmlFor="ayanamsa">Ayanamsa</label>
              <select
                id="ayanamsa"
                value={formData.ayanamsa_type}
                onChange={(e) => handleChange('ayanamsa_type', e.target.value)}
                disabled={loading}
              >
                <option value="lahiri">Lahiri (Most Common)</option>
                <option value="raman">Raman</option>
                <option value="krishnamurti">Krishnamurti (KP)</option>
                <option value="yukteshwar">Yukteshwar</option>
              </select>
            </div>

            <div className={styles.group}>
              <label htmlFor="houseSystem">House System</label>
              <select
                id="houseSystem"
                value={formData.house_system}
                onChange={(e) => handleChange('house_system', e.target.value)}
                disabled={loading}
              >
                <option value="P">Placidus</option>
                <option value="K">Koch</option>
                <option value="E">Equal House</option>
                <option value="W">Whole Sign</option>
              </select>
            </div>
          </div>
        </div>
      </div>

      <div className={styles.actions}>
        <button type="submit" disabled={loading} className={styles.btnPrimary}>
          {loading ? 'Calculating...' : 'Generate Kundli'}
        </button>
      </div>
    </form>
  );
}
