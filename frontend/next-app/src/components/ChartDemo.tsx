"use client";
import { useState } from 'react';
import { API_BASE, calculateChart } from '../lib/api';
import BirthDetailsForm, { BirthDetails } from './BirthDetailsForm';
import SouthIndianChart from './SouthIndianChart';

export default function ChartDemo() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<any | null>(null);
  const [showRawData, setShowRawData] = useState(false);

  async function handleFormSubmit(details: BirthDetails) {
    setLoading(true);
    setError(null);
    setResult(null);
    
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
    <div className="chart-demo-container">
      <header className="chart-demo-header">
        <h1>Kundli Calculator</h1>
        <p>Generate your Vedic astrology birth chart (South Indian style)</p>
        <code className="api-info">API: {API_BASE}</code>
      </header>

      {/* Birth Details Form */}
      <section className="form-section">
        <BirthDetailsForm onSubmit={handleFormSubmit} loading={loading} />
      </section>

      {/* Error Display */}
      {error && (
        <div className="error-box">
          <strong>Error:</strong> {error}
        </div>
      )}

      {/* Chart Display */}
      {result && (
        <section className="result-section">
          <div className="result-header">
            <h2>Your Birth Chart</h2>
            <button 
              onClick={() => setShowRawData(!showRawData)}
              className="toggle-data-btn"
            >
              {showRawData ? 'Hide' : 'Show'} Raw Data
            </button>
          </div>

          {/* South Indian Chart Visualization */}
          <div className="chart-container">
            <SouthIndianChart data={result} size={600} />
          </div>

          {/* Chart Summary */}
          <div className="chart-summary">
            <div className="summary-card">
              <h3>Ascendant (Lagna)</h3>
              <p className="highlight">{result?.houses?.ascendant?.sign || 'N/A'}</p>
              <p className="detail">{result?.houses?.ascendant?.longitude?.toFixed(2)}°</p>
            </div>

            <div className="summary-card">
              <h3>Ayanamsa</h3>
              <p className="highlight">{result?.ayanamsa_type || 'N/A'}</p>
              <p className="detail">{result?.ayanamsa_value?.toFixed(2)}°</p>
            </div>

            <div className="summary-card">
              <h3>Planets</h3>
              <p className="highlight">{Object.keys(result?.planetary_positions || {}).length}</p>
              <p className="detail">Calculated</p>
            </div>
          </div>

          {/* Raw Data Toggle */}
          {showRawData && (
            <div className="raw-data-section">
              <h3>Raw Chart Data</h3>
              <div className="data-grid">
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

      <style jsx>{`
        .chart-demo-container {
          max-width: 1200px;
          margin: 0 auto;
          padding: 20px;
        }

        .chart-demo-header {
          text-align: center;
          margin-bottom: 40px;
        }

        .chart-demo-header h1 {
          font-size: 32px;
          margin: 0 0 8px 0;
          color: #333;
        }

        .chart-demo-header p {
          font-size: 16px;
          color: #666;
          margin: 0 0 16px 0;
        }

        .api-info {
          display: inline-block;
          background: #f5f5f5;
          padding: 4px 12px;
          border-radius: 4px;
          font-size: 12px;
          color: #666;
        }

        .form-section {
          margin-bottom: 40px;
        }

        .error-box {
          background: #ffebee;
          border: 1px solid #ef5350;
          border-radius: 8px;
          padding: 16px;
          margin-bottom: 24px;
          color: #c62828;
        }

        .result-section {
          margin-top: 40px;
        }

        .result-header {
          display: flex;
          justify-content: space-between;
          align-items: center;
          margin-bottom: 24px;
        }

        .result-header h2 {
          margin: 0;
          font-size: 24px;
          color: #333;
        }

        .toggle-data-btn {
          background: #f5f5f5;
          border: 1px solid #ccc;
          border-radius: 4px;
          padding: 8px 16px;
          cursor: pointer;
          font-size: 14px;
          transition: background 0.2s;
        }

        .toggle-data-btn:hover {
          background: #e0e0e0;
        }

        .chart-container {
          display: flex;
          justify-content: center;
          margin: 32px 0;
          padding: 20px;
          background: white;
          border-radius: 8px;
          box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }

        .chart-summary {
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
          gap: 16px;
          margin: 32px 0;
        }

        .summary-card {
          background: white;
          border: 1px solid #ddd;
          border-radius: 8px;
          padding: 20px;
          text-align: center;
        }

        .summary-card h3 {
          margin: 0 0 12px 0;
          font-size: 14px;
          font-weight: 600;
          color: #666;
          text-transform: uppercase;
        }

        .summary-card .highlight {
          margin: 0 0 4px 0;
          font-size: 24px;
          font-weight: bold;
          color: #1976d2;
        }

        .summary-card .detail {
          margin: 0;
          font-size: 14px;
          color: #999;
        }

        .raw-data-section {
          margin-top: 40px;
          padding: 24px;
          background: #fafafa;
          border: 1px solid #ddd;
          border-radius: 8px;
        }

        .raw-data-section h3 {
          margin: 0 0 16px 0;
          font-size: 18px;
          color: #333;
        }

        .data-grid {
          display: grid;
          grid-template-columns: 1fr 1fr;
          gap: 16px;
        }

        .data-grid h4 {
          margin: 0 0 8px 0;
          font-size: 14px;
          color: #666;
        }

        .data-grid pre {
          background: white;
          border: 1px solid #ddd;
          border-radius: 4px;
          padding: 16px;
          overflow: auto;
          max-height: 400px;
          font-size: 12px;
        }

        @media (max-width: 768px) {
          .chart-demo-header h1 {
            font-size: 24px;
          }

          .data-grid {
            grid-template-columns: 1fr;
          }

          .result-header {
            flex-direction: column;
            align-items: flex-start;
            gap: 12px;
          }
        }
      `}</style>
    </div>
  );
}
