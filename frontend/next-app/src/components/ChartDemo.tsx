"use client";
import { useState } from 'react';
import { API_BASE, calculateChart } from '../lib/api';
import BirthDetailsForm, { BirthDetails } from './BirthDetailsForm';
import SouthIndianChart from './SouthIndianChart';
import SaveChartModal from './SaveChartModal';
import { useAuth } from '../contexts/AuthContext';
import styles from './ChartDemo.module.css';

export default function ChartDemo() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<any | null>(null);
  const [birthDetails, setBirthDetails] = useState<BirthDetails | null>(null);
  const [showRawData, setShowRawData] = useState(false);
  const [showSaveModal, setShowSaveModal] = useState(false);
  const { user } = useAuth();

  async function handleFormSubmit(details: BirthDetails) {
    setLoading(true);
    setError(null);
    setResult(null);
    setBirthDetails(details);
    
    try {
      // Combine date and time into ISO format
      const dateTime = `${details.date}T${details.time}:00Z`;
      
      const data = await calculateChart({
        date_time: dateTime,
        latitude: details.latitude,
        longitude: details.longitude,
        altitude: 0,
        ayanamsa_type: details.ayanamsa_type,
        house_system: details.house_system,
      });
      setResult(data);
    } catch (e: any) {
      setError(e?.message || String(e));
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className={styles.container}>
      <header className={styles.header}>
        <h1>Kundli Calculator</h1>
        <p>Generate your Vedic astrology birth chart (South Indian style)</p>
        <code className={styles.apiInfo}>API: {API_BASE}</code>
      </header>

      {/* Birth Details Form */}
      <section className={styles.formSection}>
        <BirthDetailsForm onSubmit={handleFormSubmit} loading={loading} />
      </section>

      {/* Error Display */}
      {error && (
        <div className={styles.errorBox}>
          <strong>Error:</strong> {error}
        </div>
      )}

      {/* Chart Display */}
      {result && (
        <section className={styles.resultSection}>
          <div className={styles.resultHeader}>
            <h2>Your Birth Chart</h2>
            <div className={styles.headerActions}>
              {user && (
                <button 
                  onClick={() => setShowSaveModal(true)}
                  className={styles.saveBtn}
                >
                  💾 Save Chart
                </button>
              )}
              <button 
                onClick={() => setShowRawData(!showRawData)}
                className={styles.toggleBtn}
              >
                {showRawData ? 'Hide' : 'Show'} Raw Data
              </button>
            </div>
          </div>

          {/* South Indian Chart Visualization */}
          <div className={styles.chartContainer}>
            <SouthIndianChart data={result} size={600} />
          </div>

          {/* Chart Summary */}
          <div className={styles.summary}>
            <div className={styles.summaryCard}>
              <h3>Ascendant (Lagna)</h3>
              <p className={styles.highlight}>{result?.houses?.ascendant?.sign || 'N/A'}</p>
              <p className={styles.detail}>{result?.houses?.ascendant?.longitude?.toFixed(2)}°</p>
            </div>

            <div className={styles.summaryCard}>
              <h3>Ayanamsa</h3>
              <p className={styles.highlight}>{result?.ayanamsa_type || 'N/A'}</p>
              <p className={styles.detail}>{result?.ayanamsa_value?.toFixed(2)}°</p>
            </div>

            <div className={styles.summaryCard}>
              <h3>Planets</h3>
              <p className={styles.highlight}>{Object.keys(result?.planetary_positions || {}).length}</p>
              <p className={styles.detail}>Calculated</p>
            </div>
          </div>

          {/* Raw Data Toggle */}
          {showRawData && (
            <div className={styles.rawDataSection}>
              <h3>Raw Chart Data</h3>
              <div className={styles.dataGrid}>
                <div>
                  <h4>Houses</h4>
                  <pre>{JSON.stringify(result?.houses, null, 2)}</pre>
                </div>
                <div>
                  <h4>Planetary Positions</h4>
                  <pre>{JSON.stringify(result?.planetary_positions, null, 2)}</pre>
                </div>
              </div>
            </div>
          )}
        </section>
      )}

      {/* Save Chart Modal */}
      {birthDetails && result && (
        <SaveChartModal
          isOpen={showSaveModal}
          onClose={() => setShowSaveModal(false)}
          birthDetails={birthDetails}
          chartData={result}
          onSaved={() => {
            // Could add a toast notification here
            console.log('Chart saved successfully!');
          }}
        />
      )}
    </div>
  );
}
