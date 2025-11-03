"use client";
import { useState, useEffect, useRef } from 'react';
import { API_BASE, calculateChart } from '../lib/api';
import BirthDetailsForm, { BirthDetails } from './BirthDetailsForm';
import SouthIndianChart from './SouthIndianChart';
import NavamsaChart from './NavamsaChart';
import DivisionalChart from './DivisionalChart';
import SaveChartModal from './SaveChartModal';
import { useAuth } from '../contexts/AuthContext';
import { exportChartWithImage } from '../lib/pdfExport';
import styles from './ChartDemo.module.css';

type ChartType = 'rasi' | 'navamsa' | 'd2' | 'd3' | 'd10' | 'd12';

export default function ChartDemo() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<any | null>(null);
  const [birthDetails, setBirthDetails] = useState<BirthDetails | null>(null);
  const [showRawData, setShowRawData] = useState(false);
  const [showSaveModal, setShowSaveModal] = useState(false);
  const [chartType, setChartType] = useState<ChartType>('rasi');
  const [exportingPDF, setExportingPDF] = useState(false);
  const chartRef = useRef<HTMLDivElement>(null);
  const { user} = useAuth();

  // Check if viewing a saved chart from sessionStorage
  useEffect(() => {
    const savedChartData = sessionStorage.getItem('viewChart');
    if (savedChartData) {
      try {
        const chart = JSON.parse(savedChartData);
        setBirthDetails(chart.birth_details);
        setResult(chart.chart_data);
        sessionStorage.removeItem('viewChart');
      } catch (err) {
        console.error('Error loading saved chart:', err);
      }
    }
  }, []);

  const handleExportPDF = async () => {
    if (!chartRef.current || !birthDetails || !result) return;

    setExportingPDF(true);
    try {
      await exportChartWithImage(chartRef.current, {
        birthDetails,
        chartData: result,
        title: `Kundli Chart - ${birthDetails.locationName}`,
      });
    } catch (err) {
      console.error('PDF export failed:', err);
      alert('Failed to export PDF. Please try again.');
    } finally {
      setExportingPDF(false);
    }
  };

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
              <button 
                onClick={handleExportPDF}
                className={styles.pdfBtn}
                disabled={exportingPDF}
              >
                {exportingPDF ? '⏳' : '📄'} {exportingPDF ? 'Exporting...' : 'Export PDF'}
              </button>
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

          {/* Chart Type Switcher */}
          <div className={styles.chartSwitcher}>
            <button
              className={`${styles.switcherBtn} ${chartType === 'rasi' ? styles.active : ''}`}
              onClick={() => setChartType('rasi')}
            >
              Rasi (D1)
            </button>
            <button
              className={`${styles.switcherBtn} ${chartType === 'd2' ? styles.active : ''}`}
              onClick={() => setChartType('d2')}
            >
              Hora (D2)
            </button>
            <button
              className={`${styles.switcherBtn} ${chartType === 'd3' ? styles.active : ''}`}
              onClick={() => setChartType('d3')}
            >
              Drekkana (D3)
            </button>
            <button
              className={`${styles.switcherBtn} ${chartType === 'navamsa' ? styles.active : ''}`}
              onClick={() => setChartType('navamsa')}
            >
              Navamsa (D9)
            </button>
            <button
              className={`${styles.switcherBtn} ${chartType === 'd10' ? styles.active : ''}`}
              onClick={() => setChartType('d10')}
            >
              Dasamsa (D10)
            </button>
            <button
              className={`${styles.switcherBtn} ${chartType === 'd12' ? styles.active : ''}`}
              onClick={() => setChartType('d12')}
            >
              Dwadasamsa (D12)
            </button>
          </div>

          {/* Chart Visualization */}
          <div className={styles.chartContainer} ref={chartRef}>
            {chartType === 'rasi' && <SouthIndianChart data={result} size={600} />}
            {chartType === 'navamsa' && <NavamsaChart data={result} size={600} />}
            {chartType === 'd2' && <DivisionalChart data={result} size={600} division={2} />}
            {chartType === 'd3' && <DivisionalChart data={result} size={600} division={3} />}
            {chartType === 'd10' && <DivisionalChart data={result} size={600} division={10} />}
            {chartType === 'd12' && <DivisionalChart data={result} size={600} division={12} />}
          </div>

          {/* Chart Info */}
          <div className={styles.chartInfo}>
            <p>
              {chartType === 'rasi' && '📊 Rasi Chart (D1) - Birth chart showing planetary positions at time of birth'}
              {chartType === 'd2' && '💰 Hora Chart (D2) - Wealth, prosperity, and material gains'}
              {chartType === 'd3' && '👫 Drekkana Chart (D3) - Siblings, courage, and mental strength'}
              {chartType === 'navamsa' && '💑 Navamsa Chart (D9) - Marriage, relationships, and spiritual path'}
              {chartType === 'd10' && '💼 Dasamsa Chart (D10) - Career, profession, and public life'}
              {chartType === 'd12' && '👨‍👩‍👧‍👦 Dwadasamsa Chart (D12) - Parents, ancestry, and past life karma'}
            </p>
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
