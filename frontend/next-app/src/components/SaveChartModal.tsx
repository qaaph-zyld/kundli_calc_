"use client";
import React, { useState } from 'react';
import { saveChart } from '../lib/supabase/charts';
import { BirthDetails } from './BirthDetailsForm';
import styles from './SaveChartModal.module.css';

interface SaveChartModalProps {
  isOpen: boolean;
  onClose: () => void;
  birthDetails: BirthDetails;
  chartData: any;
  onSaved?: () => void;
}

export default function SaveChartModal({
  isOpen,
  onClose,
  birthDetails,
  chartData,
  onSaved,
}: SaveChartModalProps) {
  const [title, setTitle] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState(false);

  if (!isOpen) return null;

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setLoading(true);

    try {
      const { data, error } = await saveChart(title, birthDetails, chartData);
      
      if (error) {
        setError(error.message || 'Failed to save chart');
      } else {
        setSuccess(true);
        setTimeout(() => {
          onSaved?.();
          onClose();
          setTitle('');
          setSuccess(false);
        }, 1500);
      }
    } catch (err: any) {
      setError(err.message || 'An error occurred');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className={styles.overlay} onClick={onClose}>
      <div className={styles.modal} onClick={(e) => e.stopPropagation()}>
        <button className={styles.closeBtn} onClick={onClose}>×</button>
        
        <h2>Save Chart</h2>
        <p className={styles.subtitle}>Give your chart a memorable name</p>

        {error && <div className={styles.error}>{error}</div>}
        {success && <div className={styles.success}>Chart saved successfully!</div>}

        <form onSubmit={handleSubmit}>
          <div className={styles.formGroup}>
            <label htmlFor="title">Chart Title</label>
            <input
              id="title"
              type="text"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              placeholder="e.g., My Birth Chart, John's Kundli"
              required
              disabled={loading || success}
              autoFocus
            />
            <small>
              {birthDetails.locationName} • {birthDetails.date} {birthDetails.time}
            </small>
          </div>

          <div className={styles.actions}>
            <button 
              type="button" 
              onClick={onClose}
              className={styles.cancelBtn}
              disabled={loading || success}
            >
              Cancel
            </button>
            <button 
              type="submit" 
              className={styles.saveBtn}
              disabled={loading || success}
            >
              {loading ? 'Saving...' : success ? 'Saved!' : 'Save Chart'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
