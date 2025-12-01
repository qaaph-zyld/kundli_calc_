"use client";
import React, { useEffect, useState } from 'react';
import { Card, CardHeader, CardBody } from './ui/Card';
import Button from './ui/Button';
import Input from './ui/Input';
import Select from './ui/Select';
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

  // Option arrays for Select components
  const timezoneOptions = [
    { value: 'UTC', label: 'UTC' },
    { value: 'Asia/Kolkata', label: 'IST (India)' },
    { value: 'America/New_York', label: 'EST (New York)' },
    { value: 'America/Los_Angeles', label: 'PST (Los Angeles)' },
    { value: 'Europe/London', label: 'GMT (London)' },
    { value: 'Europe/Belgrade', label: 'CET (Belgrade)' },
  ];

  const ayanamsaOptions = [
    { value: 'lahiri', label: 'Lahiri (Most Common)' },
    { value: 'raman', label: 'Raman' },
    { value: 'krishnamurti', label: 'Krishnamurti (KP)' },
    { value: 'yukteshwar', label: 'Yukteshwar' },
  ];

  const houseSystemOptions = [
    { value: 'P', label: 'Placidus' },
    { value: 'K', label: 'Koch' },
    { value: 'E', label: 'Equal House' },
    { value: 'W', label: 'Whole Sign' },
  ];

  return (
    <form onSubmit={handleSubmit} className={styles.form}>
      <div className={styles.grid}>
        {/* Date and Time Card */}
        <Card variant="default" padding="md">
          <CardHeader title="Birth Date & Time" subtitle="Enter the exact birth details" />
          <CardBody>
            <div className={styles.row}>
              <Input
                id="date"
                type="date"
                label="Date"
                value={formData.date}
                onChange={(e) => handleChange('date', e.target.value)}
                disabled={loading}
                required
                error={errors.date}
                fullWidth
              />
              <Input
                id="time"
                type="time"
                label="Time (24h)"
                value={formData.time}
                onChange={(e) => handleChange('time', e.target.value)}
                disabled={loading}
                required
                error={errors.time}
                fullWidth
              />
            </div>
          </CardBody>
        </Card>

        {/* Location Card */}
        <Card variant="default" padding="md">
          <CardHeader title="Birth Location" subtitle="Where were you born?" />
          <CardBody>
            <div className={styles.group}>
              <Input
                id="locationName"
                type="text"
                label="Location Name"
                placeholder="City, Country"
                value={formData.locationName}
                onChange={(e) => handleChange('locationName', e.target.value)}
                disabled={loading}
                required
                error={errors.locationName || geoError || undefined}
                fullWidth
              />
              <div className={styles.inlineActions}>
                <Button 
                  type="button" 
                  variant="secondary" 
                  size="sm"
                  onClick={handleResolvePlace} 
                  disabled={loading || geoLoading}
                  isLoading={geoLoading}
                >
                  🔍 Search
                </Button>
                <Button 
                  type="button" 
                  variant="ghost" 
                  size="sm"
                  onClick={handleDetectTimezone} 
                  disabled={loading || geoLoading}
                >
                  🌐 Detect Timezone
                </Button>
              </div>
            </div>

            <div className={styles.row}>
              <Input
                id="latitude"
                type="number"
                label="Latitude"
                placeholder="44.531346"
                value={formData.latitude.toString()}
                onChange={(e) => handleChange('latitude', parseFloat(e.target.value) || 0)}
                disabled={loading}
                required
                error={errors.latitude}
                fullWidth
              />
              <Input
                id="longitude"
                type="number"
                label="Longitude"
                placeholder="19.206766"
                value={formData.longitude.toString()}
                onChange={(e) => handleChange('longitude', parseFloat(e.target.value) || 0)}
                disabled={loading}
                required
                error={errors.longitude}
                fullWidth
              />
            </div>

            <Select
              id="timezone"
              label="Timezone"
              options={timezoneOptions}
              value={formData.timezone}
              onChange={(e) => handleChange('timezone', e.target.value)}
              disabled={loading}
              fullWidth
            />
          </CardBody>
        </Card>

        {/* Calculation Settings Card */}
        <Card variant="default" padding="md">
          <CardHeader title="Settings" subtitle="Calculation preferences" />
          <CardBody>
            <div className={styles.row}>
              <Select
                id="ayanamsa"
                label="Ayanamsa"
                options={ayanamsaOptions}
                value={formData.ayanamsa_type}
                onChange={(e) => handleChange('ayanamsa_type', e.target.value)}
                disabled={loading}
                fullWidth
              />
              <Select
                id="houseSystem"
                label="House System"
                options={houseSystemOptions}
                value={formData.house_system}
                onChange={(e) => handleChange('house_system', e.target.value)}
                disabled={loading}
                fullWidth
              />
            </div>
          </CardBody>
        </Card>
      </div>

      <div className={styles.actions}>
        <Button 
          type="submit" 
          variant="primary" 
          size="lg"
          disabled={loading} 
          isLoading={loading}
          fullWidth
        >
          {loading ? 'Calculating...' : '✨ Generate Kundli'}
        </Button>
      </div>
    </form>
  );
}
