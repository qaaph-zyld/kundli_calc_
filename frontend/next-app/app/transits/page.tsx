"use client";
import { useState } from 'react';
import { useRouter } from 'next/navigation';
import Header from '../../src/components/Header';
import { API_BASE } from '../../src/lib/api';
import styles from './page.module.css';

interface TransitData {
  transit_date: string;
  planetary_positions: any;
  aspects: string[];
  predictions: string[];
}

export default function TransitsPage() {
  const router = useRouter();
  const [birthDate, setBirthDate] = useState('');
  const [birthTime, setBirthTime] = useState('');
  const [latitude, setLatitude] = useState('');
  const [longitude, setLongitude] = useState('');
  const [transitDate, setTransitDate] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [transitData, setTransitData] = useState<TransitData | null>(null);

  const handleCalculate = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      const response = await fetch(`${API_BASE}/transits`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          birth_datetime: `${birthDate}T${birthTime}:00Z`,
          transit_date: transitDate,
          latitude: parseFloat(latitude),
          longitude: parseFloat(longitude),
        }),
      });

      if (!response.ok) {
        throw new Error('Failed to calculate transits');
      }

      const data = await response.json();
      setTransitData(data);
    } catch (err: any) {
      setError(err.message || 'Error calculating transits');
    } finally {
      setLoading(false);
    }
  };

  const getCurrentTransits = () => {
    const today = new Date().toISOString().split('T')[0];
    setTransitDate(today);
  };

  return (
    <>
      <Header />
      <main className={styles.container}>
        <div className={styles.header}>
          <h1>🌍 Transit Calculations</h1>
          <p>Analyze current and future planetary transits and their effects</p>
          <button onClick={() => router.push('/')} className={styles.backBtn}>
            ← Back to Calculator
          </button>
        </div>

        {error && (
          <div className={styles.error}>
            <strong>Error:</strong> {error}
          </div>
        )}

        <div className={styles.formSection}>
          <h2>Birth Details & Transit Date</h2>
          <form onSubmit={handleCalculate} className={styles.form}>
            <div className={styles.formRow}>
              <div className={styles.formGroup}>
                <label>Birth Date</label>
                <input
                  type="date"
                  value={birthDate}
                  onChange={(e) => setBirthDate(e.target.value)}
                  required
                />
              </div>

              <div className={styles.formGroup}>
                <label>Birth Time</label>
                <input
                  type="time"
                  value={birthTime}
                  onChange={(e) => setBirthTime(e.target.value)}
                  required
                />
              </div>
            </div>

            <div className={styles.formRow}>
              <div className={styles.formGroup}>
                <label>Latitude</label>
                <input
                  type="number"
                  step="0.0001"
                  value={latitude}
                  onChange={(e) => setLatitude(e.target.value)}
                  placeholder="28.6139"
                  required
                />
              </div>

              <div className={styles.formGroup}>
                <label>Longitude</label>
                <input
                  type="number"
                  step="0.0001"
                  value={longitude}
                  onChange={(e) => setLongitude(e.target.value)}
                  placeholder="77.2090"
                  required
                />
              </div>
            </div>

            <div className={styles.formRow}>
              <div className={styles.formGroup}>
                <label>Transit Date</label>
                <div className={styles.dateInputGroup}>
                  <input
                    type="date"
                    value={transitDate}
                    onChange={(e) => setTransitDate(e.target.value)}
                    required
                  />
                  <button
                    type="button"
                    onClick={getCurrentTransits}
                    className={styles.todayBtn}
                  >
                    Today
                  </button>
                </div>
              </div>
            </div>

            <button type="submit" disabled={loading} className={styles.submitBtn}>
              {loading ? '⏳ Calculating...' : '🔮 Calculate Transits'}
            </button>
          </form>
        </div>

        {transitData && (
          <div className={styles.resultsSection}>
            <h2>Transit Analysis for {transitData.transit_date}</h2>

            <div className={styles.transitGrid}>
              {/* Current Planetary Positions */}
              <div className={styles.transitCard}>
                <h3>📍 Current Planetary Positions</h3>
                <div className={styles.planetList}>
                  {transitData.planetary_positions && Object.entries(transitData.planetary_positions).map(([planet, data]: [string, any]) => (
                    <div key={planet} className={styles.planetItem}>
                      <span className={styles.planetName}>{planet}</span>
                      <span className={styles.planetSign}>{data.sign}</span>
                      <span className={styles.planetDegree}>{data.longitude?.toFixed(2)}°</span>
                    </div>
                  ))}
                </div>
              </div>

              {/* Important Aspects */}
              {transitData.aspects && transitData.aspects.length > 0 && (
                <div className={styles.transitCard}>
                  <h3>⭐ Important Aspects</h3>
                  <ul className={styles.aspectsList}>
                    {transitData.aspects.map((aspect, idx) => (
                      <li key={idx}>{aspect}</li>
                    ))}
                  </ul>
                </div>
              )}

              {/* Transit Predictions */}
              {transitData.predictions && transitData.predictions.length > 0 && (
                <div className={styles.transitCard}>
                  <h3>🔮 Transit Effects & Predictions</h3>
                  <ul className={styles.predictionsList}>
                    {transitData.predictions.map((pred, idx) => (
                      <li key={idx}>{pred}</li>
                    ))}
                  </ul>
                </div>
              )}
            </div>

            <div className={styles.infoBox}>
              <h4>📝 About Transits</h4>
              <p>
                Transits are the current positions of planets in the sky and how they interact with 
                your birth chart. They indicate upcoming opportunities, challenges, and life events.
              </p>
              <ul>
                <li><strong>Saturn Transits:</strong> Long-term lessons, career changes, responsibilities</li>
                <li><strong>Jupiter Transits:</strong> Growth, expansion, opportunities, blessings</li>
                <li><strong>Rahu-Ketu Transits:</strong> Karmic events, sudden changes, spiritual evolution</li>
                <li><strong>Mars Transits:</strong> Energy, action, conflicts, quick events</li>
                <li><strong>Sun/Moon Transits:</strong> Daily and monthly influences on mood and energy</li>
              </ul>
            </div>
          </div>
        )}

        {!transitData && !loading && (
          <div className={styles.placeholder}>
            <div className={styles.placeholderIcon}>🌟</div>
            <h3>Enter your birth details to see transit analysis</h3>
            <p>Transits show how current planetary positions affect your birth chart</p>
          </div>
        )}
      </main>
    </>
  );
}
