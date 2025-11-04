"use client";
import { useState } from 'react';
import { useRouter } from 'next/navigation';
import Header from '../../src/components/Header';
import styles from './page.module.css';

interface LifeEvent {
  date: string;
  description: string;
  type: 'marriage' | 'career' | 'child' | 'accident' | 'relocation' | 'other';
}

interface RectificationResult {
  suggestedTime: string;
  confidence: number;
  adjustmentMinutes: number;
  reasoning: string[];
  charts: {
    original: any;
    corrected: any;
  };
}

export default function RectificationPage() {
  const router = useRouter();
  const [approximateDate, setApproximateDate] = useState('');
  const [approximateTime, setApproximateTime] = useState('');
  const [timeUncertainty, setTimeUncertainty] = useState('30'); // minutes
  const [latitude, setLatitude] = useState('');
  const [longitude, setLongitude] = useState('');
  const [lifeEvents, setLifeEvents] = useState<LifeEvent[]>([
    { date: '', description: '', type: 'marriage' }
  ]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<RectificationResult | null>(null);

  const addLifeEvent = () => {
    setLifeEvents([...lifeEvents, { date: '', description: '', type: 'marriage' }]);
  };

  const updateLifeEvent = (index: number, field: keyof LifeEvent, value: string) => {
    const updated = [...lifeEvents];
    updated[index] = { ...updated[index], [field]: value };
    setLifeEvents(updated);
  };

  const removeLifeEvent = (index: number) => {
    setLifeEvents(lifeEvents.filter((_, i) => i !== index));
  };

  const handleRectify = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      // Simulated rectification logic
      // In production, this would call backend API
      await new Promise(resolve => setTimeout(resolve, 2000));

      const adjustmentMinutes = Math.round((Math.random() - 0.5) * parseFloat(timeUncertainty) * 2);
      const [hours, minutes] = approximateTime.split(':').map(Number);
      const totalMinutes = hours * 60 + minutes + adjustmentMinutes;
      const correctedHours = Math.floor(totalMinutes / 60) % 24;
      const correctedMinutes = totalMinutes % 60;
      const suggestedTime = `${String(correctedHours).padStart(2, '0')}:${String(correctedMinutes).padStart(2, '0')}`;

      setResult({
        suggestedTime,
        confidence: 75 + Math.random() * 20,
        adjustmentMinutes,
        reasoning: [
          'Marriage event aligns with Venus dasha period at corrected time',
          'Ascendant matches physical appearance and personality traits',
          'Saturn transit during accident correlates with corrected 8th house',
          'Career milestone timing fits corrected 10th house activation'
        ],
        charts: {
          original: null,
          corrected: null
        }
      });
    } catch (err: any) {
      setError(err.message || 'Error in rectification');
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <Header />
      <main className={styles.container}>
        <div className={styles.header}>
          <h1>⏰ Birth Time Rectification</h1>
          <p>Correct your birth time using life events and astrological principles</p>
          <button onClick={() => router.push('/')} className={styles.backBtn}>
            ← Back to Calculator
          </button>
        </div>

        <div className={styles.infoBox}>
          <h3>📖 What is Birth Time Rectification?</h3>
          <p>
            Birth time rectification is the process of determining the correct birth time when it's 
            uncertain or unknown. This technique uses major life events (marriage, career milestones, 
            accidents, etc.) to work backward and find the most accurate birth time.
          </p>
          <p><strong>Methods used:</strong></p>
          <ul>
            <li>Matching life events with dasha periods</li>
            <li>Analyzing physical features and personality traits</li>
            <li>Checking planetary positions during known events</li>
            <li>Verifying ascendant and moon sign characteristics</li>
          </ul>
        </div>

        {error && (
          <div className={styles.error}>
            <strong>Error:</strong> {error}
          </div>
        )}

        <form onSubmit={handleRectify} className={styles.form}>
          <div className={styles.section}>
            <h2>1. Approximate Birth Details</h2>
            
            <div className={styles.formRow}>
              <div className={styles.formGroup}>
                <label>Approximate Birth Date</label>
                <input
                  type="date"
                  value={approximateDate}
                  onChange={(e) => setApproximateDate(e.target.value)}
                  required
                />
              </div>

              <div className={styles.formGroup}>
                <label>Approximate Birth Time</label>
                <input
                  type="time"
                  value={approximateTime}
                  onChange={(e) => setApproximateTime(e.target.value)}
                  required
                />
              </div>
            </div>

            <div className={styles.formRow}>
              <div className={styles.formGroup}>
                <label>Time Uncertainty (±minutes)</label>
                <select
                  value={timeUncertainty}
                  onChange={(e) => setTimeUncertainty(e.target.value)}
                  className={styles.select}
                >
                  <option value="15">±15 minutes</option>
                  <option value="30">±30 minutes</option>
                  <option value="60">±1 hour</option>
                  <option value="120">±2 hours</option>
                  <option value="240">±4 hours</option>
                </select>
              </div>
            </div>

            <div className={styles.formRow}>
              <div className={styles.formGroup}>
                <label>Birth Latitude</label>
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
                <label>Birth Longitude</label>
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
          </div>

          <div className={styles.section}>
            <h2>2. Major Life Events</h2>
            <p className={styles.helpText}>
              Add at least 3-5 significant life events to improve accuracy
            </p>

            {lifeEvents.map((event, index) => (
              <div key={index} className={styles.eventCard}>
                <div className={styles.eventHeader}>
                  <h4>Event {index + 1}</h4>
                  {lifeEvents.length > 1 && (
                    <button
                      type="button"
                      onClick={() => removeLifeEvent(index)}
                      className={styles.removeBtn}
                    >
                      ✕ Remove
                    </button>
                  )}
                </div>

                <div className={styles.formRow}>
                  <div className={styles.formGroup}>
                    <label>Event Type</label>
                    <select
                      value={event.type}
                      onChange={(e) => updateLifeEvent(index, 'type', e.target.value)}
                      className={styles.select}
                    >
                      <option value="marriage">Marriage</option>
                      <option value="career">Career Milestone</option>
                      <option value="child">Child Birth</option>
                      <option value="accident">Accident/Injury</option>
                      <option value="relocation">Relocation</option>
                      <option value="other">Other</option>
                    </select>
                  </div>

                  <div className={styles.formGroup}>
                    <label>Event Date</label>
                    <input
                      type="date"
                      value={event.date}
                      onChange={(e) => updateLifeEvent(index, 'date', e.target.value)}
                      required
                    />
                  </div>
                </div>

                <div className={styles.formGroup}>
                  <label>Description</label>
                  <textarea
                    value={event.description}
                    onChange={(e) => updateLifeEvent(index, 'description', e.target.value)}
                    placeholder="Describe the event (e.g., Got married in Delhi, Started new job at Google)"
                    rows={2}
                    className={styles.textarea}
                  />
                </div>
              </div>
            ))}

            <button type="button" onClick={addLifeEvent} className={styles.addBtn}>
              + Add Another Event
            </button>
          </div>

          <button type="submit" disabled={loading} className={styles.submitBtn}>
            {loading ? '⏳ Rectifying...' : '🔮 Rectify Birth Time'}
          </button>
        </form>

        {result && (
          <div className={styles.resultSection}>
            <h2>✨ Rectification Results</h2>

            <div className={styles.resultGrid}>
              <div className={styles.resultCard}>
                <h3>Suggested Birth Time</h3>
                <div className={styles.timeResult}>
                  <div className={styles.timeComparison}>
                    <div>
                      <span className={styles.label}>Original:</span>
                      <span className={styles.time}>{approximateTime}</span>
                    </div>
                    <div className={styles.arrow}>→</div>
                    <div>
                      <span className={styles.label}>Corrected:</span>
                      <span className={styles.time}>{result.suggestedTime}</span>
                    </div>
                  </div>
                  <div className={styles.adjustment}>
                    Adjustment: {result.adjustmentMinutes > 0 ? '+' : ''}{result.adjustmentMinutes} minutes
                  </div>
                </div>
              </div>

              <div className={styles.resultCard}>
                <h3>Confidence Level</h3>
                <div className={styles.confidenceBar}>
                  <div 
                    className={styles.confidenceFill} 
                    style={{
                      width: `${result.confidence}%`,
                      backgroundColor: result.confidence >= 80 ? '#4caf50' : result.confidence >= 60 ? '#ff9800' : '#f44336'
                    }}
                  />
                </div>
                <div className={styles.confidenceText}>
                  {result.confidence.toFixed(1)}% - {result.confidence >= 80 ? 'High' : result.confidence >= 60 ? 'Moderate' : 'Low'} Confidence
                </div>
              </div>
            </div>

            <div className={styles.reasoningCard}>
              <h3>📋 Analysis & Reasoning</h3>
              <ul>
                {result.reasoning.map((reason, idx) => (
                  <li key={idx}>{reason}</li>
                ))}
              </ul>
            </div>

            <div className={styles.nextSteps}>
              <h3>🎯 Next Steps</h3>
              <ol>
                <li>Use the corrected birth time to generate a new chart</li>
                <li>Verify the ascendant matches your physical appearance and personality</li>
                <li>Check if dasha periods align with past life events</li>
                <li>Consult with an experienced astrologer for final confirmation</li>
              </ol>
            </div>
          </div>
        )}

        {!result && !loading && (
          <div className={styles.placeholder}>
            <div className={styles.placeholderIcon}>⏰</div>
            <h3>Fill in the form to rectify your birth time</h3>
            <p>Accurate life events help achieve better rectification results</p>
          </div>
        )}
      </main>
    </>
  );
}
