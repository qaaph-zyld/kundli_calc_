"use client";
import { useState } from 'react';
import { API_BASE, calculateChart } from '../lib/api';

export default function ChartDemo() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<any | null>(null);

  async function onRun() {
    setLoading(true);
    setError(null);
    setResult(null);
    try {
      const data = await calculateChart({
        date_time: '1990-10-09T07:10:00Z',
        latitude: 44.531346,
        longitude: 19.206766,
        altitude: 0,
        ayanamsa_type: 'lahiri',
        house_system: 'P',
      });
      setResult(data);
    } catch (e: any) {
      setError(e?.message || String(e));
    } finally {
      setLoading(false);
    }
  }

  return (
    <div style={{ border: '1px solid #ddd', borderRadius: 8, padding: 16 }}>
      <div style={{ display: 'flex', gap: 8, alignItems: 'center' }}>
        <button onClick={onRun} disabled={loading} style={{ padding: '8px 12px' }}>
          {loading ? 'Calculating…' : 'Calculate Sample Chart'}
        </button>
        <code style={{ color: '#666' }}>API: {API_BASE}</code>
      </div>

      {error && (
        <p style={{ color: '#b00020', marginTop: 12 }}>Error: {error}</p>
      )}

      {result && (
        <div style={{ marginTop: 16 }}>
          <h3 style={{ margin: '8px 0' }}>Result</h3>
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 12 }}>
            <div>
              <h4>Ayanamsa</h4>
              <pre style={{ whiteSpace: 'pre-wrap' }}>{JSON.stringify(result.ayanamsa_value, null, 2)}</pre>
            </div>
            <div>
              <h4>Ascendant</h4>
              <pre style={{ whiteSpace: 'pre-wrap' }}>{JSON.stringify(result?.houses?.ascendant, null, 2)}</pre>
            </div>
          </div>
          <div>
            <h4>Planets (first 6)</h4>
            <pre style={{ maxHeight: 240, overflow: 'auto', background: '#fafafa', padding: 8 }}>
              {JSON.stringify(Object.fromEntries(Object.entries(result.planetary_positions || {}).slice(0, 6)), null, 2)}
            </pre>
          </div>
        </div>
      )}
    </div>
  );
}
