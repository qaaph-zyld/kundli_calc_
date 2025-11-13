"use client";
import React, { useState } from 'react';
import styles from './BirthDetailsForm.module.css';

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
  const [formData, setFormData] = useState<BirthDetails>({
    date: '1990-10-09',
    time: '07:10',
    latitude: 44.5333,
    longitude: 19.2333,
    timezone: 'UTC',
    locationName: 'Loznica, Serbia',
    ayanamsa_type: 'lahiri',
    house_system: 'W',
  });

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
            {errors.locationName && <span className={styles.error}>{errors.locationName}</span>}
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
