"use client";
import { useState, useMemo } from 'react';
import styles from './AnalysisPanels.module.css';

interface DashaTimelineProps {
  chartData: any;
  birthDatetime: string;
}

interface DashaPeriod {
  planet: string;
  startDate: Date;
  endDate: Date;
  years: number;
  isCurrent: boolean;
}

const PLANET_SYMBOLS: Record<string, string> = {
  Sun: '☉', Moon: '☽', Mars: '♂', Mercury: '☿',
  Jupiter: '♃', Venus: '♀', Saturn: '♄', Rahu: '☊', Ketu: '☋'
};

const PLANET_COLORS: Record<string, string> = {
  Sun: '#FF9800', Moon: '#90CAF9', Mars: '#F44336', Mercury: '#4CAF50',
  Jupiter: '#FFC107', Venus: '#E91E63', Saturn: '#607D8B', Rahu: '#9C27B0', Ketu: '#795548'
};

// Vimshottari Dasha periods
const VIMSHOTTARI_PERIODS: Record<string, number> = {
  Ketu: 7, Venus: 20, Sun: 6, Moon: 10, Mars: 7,
  Rahu: 18, Jupiter: 16, Saturn: 19, Mercury: 17
};

const VIMSHOTTARI_SEQUENCE = ['Ketu', 'Venus', 'Sun', 'Moon', 'Mars', 'Rahu', 'Jupiter', 'Saturn', 'Mercury'];

// Yogini Dasha periods
const YOGINI_PERIODS: Record<string, { years: number; planet: string }> = {
  Mangala: { years: 1, planet: 'Moon' },
  Pingala: { years: 2, planet: 'Sun' },
  Dhanya: { years: 3, planet: 'Jupiter' },
  Bhramari: { years: 4, planet: 'Mars' },
  Bhadrika: { years: 5, planet: 'Mercury' },
  Ulka: { years: 6, planet: 'Saturn' },
  Siddha: { years: 7, planet: 'Venus' },
  Sankata: { years: 8, planet: 'Rahu' }
};

const YOGINI_SEQUENCE = ['Mangala', 'Pingala', 'Dhanya', 'Bhramari', 'Bhadrika', 'Ulka', 'Siddha', 'Sankata'];

export default function DashaTimeline({ chartData, birthDatetime }: DashaTimelineProps) {
  const [activeSystem, setActiveSystem] = useState<'vimshottari' | 'yogini' | 'comparison'>('vimshottari');
  const [showDetails, setShowDetails] = useState<string | null>(null);

  const birthDate = useMemo(() => new Date(birthDatetime), [birthDatetime]);
  const now = new Date();

  // Get Moon's nakshatra for dasha calculation
  const moonNakshatra = useMemo(() => {
    const moonLon = chartData?.planetary_positions?.Moon?.longitude || 0;
    return Math.floor(moonLon / (360 / 27));
  }, [chartData]);

  // Calculate Vimshottari Dasha
  const vimshottariDashas = useMemo<DashaPeriod[]>(() => {
    const nakLords = ['Ketu', 'Venus', 'Sun', 'Moon', 'Mars', 'Rahu', 'Jupiter', 'Saturn', 'Mercury'];
    const startingLord = nakLords[moonNakshatra % 9];
    
    // Calculate balance at birth
    const moonLon = chartData?.planetary_positions?.Moon?.longitude || 0;
    const nakSpan = 360 / 27;
    const posInNak = moonLon % nakSpan;
    const balance = 1 - (posInNak / nakSpan);
    
    // Build sequence starting from birth nakshatra lord
    const startIdx = VIMSHOTTARI_SEQUENCE.indexOf(startingLord);
    const sequence = [...VIMSHOTTARI_SEQUENCE.slice(startIdx), ...VIMSHOTTARI_SEQUENCE.slice(0, startIdx)];
    
    const periods: DashaPeriod[] = [];
    let currentDate = new Date(birthDate);
    
    sequence.forEach((planet, idx) => {
      const fullYears = VIMSHOTTARI_PERIODS[planet];
      const years = idx === 0 ? fullYears * balance : fullYears;
      const endDate = new Date(currentDate);
      endDate.setFullYear(endDate.getFullYear() + Math.floor(years));
      endDate.setMonth(endDate.getMonth() + Math.round((years % 1) * 12));
      
      const isCurrent = currentDate <= now && now < endDate;
      
      periods.push({
        planet,
        startDate: new Date(currentDate),
        endDate,
        years,
        isCurrent
      });
      
      currentDate = new Date(endDate);
    });
    
    return periods;
  }, [chartData, birthDate, moonNakshatra]);

  // Calculate Yogini Dasha
  const yoginiDashas = useMemo(() => {
    const startIdx = (moonNakshatra + 3) % 8; // Offset by 3
    const sequence = [...YOGINI_SEQUENCE.slice(startIdx), ...YOGINI_SEQUENCE.slice(0, startIdx)];
    
    const moonLon = chartData?.planetary_positions?.Moon?.longitude || 0;
    const nakSpan = 360 / 27;
    const posInNak = moonLon % nakSpan;
    const balance = 1 - (posInNak / nakSpan);
    
    const periods: { yogini: string; planet: string; startDate: Date; endDate: Date; years: number; isCurrent: boolean }[] = [];
    let currentDate = new Date(birthDate);
    
    sequence.forEach((yogini, idx) => {
      const { years: fullYears, planet } = YOGINI_PERIODS[yogini];
      const years = idx === 0 ? fullYears * balance : fullYears;
      const endDate = new Date(currentDate);
      endDate.setFullYear(endDate.getFullYear() + Math.floor(years));
      endDate.setMonth(endDate.getMonth() + Math.round((years % 1) * 12));
      
      const isCurrent = currentDate <= now && now < endDate;
      
      periods.push({
        yogini,
        planet,
        startDate: new Date(currentDate),
        endDate,
        years,
        isCurrent
      });
      
      currentDate = new Date(endDate);
    });
    
    return periods;
  }, [chartData, birthDate, moonNakshatra]);

  // Current dashas
  const currentVimshottari = vimshottariDashas.find(d => d.isCurrent);
  const currentYogini = yoginiDashas.find(d => d.isCurrent);

  // Format date
  const formatDate = (date: Date) => {
    return date.toLocaleDateString('en-US', { month: 'short', year: 'numeric' });
  };

  // Calculate progress percentage
  const getProgress = (start: Date, end: Date): number => {
    const total = end.getTime() - start.getTime();
    const elapsed = now.getTime() - start.getTime();
    return Math.min(100, Math.max(0, (elapsed / total) * 100));
  };

  return (
    <div className={styles.panel}>
      <div className={styles.panelHeader}>
        <h3>📅 Dasha Timeline</h3>
        <p className={styles.subtitle}>Planetary period systems comparison</p>
      </div>

      {/* Current Dasha Summary */}
      <div className={styles.currentDashaRow}>
        <div className={styles.currentDashaCard}>
          <span className={styles.dashaLabel}>Vimshottari Mahadasha</span>
          <div className={styles.dashaValue}>
            <span className={styles.dashaSymbol} style={{ color: PLANET_COLORS[currentVimshottari?.planet || 'Sun'] }}>
              {PLANET_SYMBOLS[currentVimshottari?.planet || 'Sun']}
            </span>
            <span>{currentVimshottari?.planet || 'N/A'}</span>
          </div>
          <span className={styles.dashaDate}>
            {currentVimshottari && `Until ${formatDate(currentVimshottari.endDate)}`}
          </span>
        </div>
        <div className={styles.currentDashaCard}>
          <span className={styles.dashaLabel}>Yogini Dasha</span>
          <div className={styles.dashaValue}>
            <span className={styles.dashaSymbol} style={{ color: PLANET_COLORS[currentYogini?.planet || 'Moon'] }}>
              {PLANET_SYMBOLS[currentYogini?.planet || 'Moon']}
            </span>
            <span>{currentYogini?.yogini || 'N/A'}</span>
          </div>
          <span className={styles.dashaDate}>
            {currentYogini && `Until ${formatDate(currentYogini.endDate)}`}
          </span>
        </div>
      </div>

      {/* System Tabs */}
      <div className={styles.tabNav}>
        <button 
          className={`${styles.tab} ${activeSystem === 'vimshottari' ? styles.active : ''}`}
          onClick={() => setActiveSystem('vimshottari')}
        >
          Vimshottari (120 yr)
        </button>
        <button 
          className={`${styles.tab} ${activeSystem === 'yogini' ? styles.active : ''}`}
          onClick={() => setActiveSystem('yogini')}
        >
          Yogini (36 yr)
        </button>
        <button 
          className={`${styles.tab} ${activeSystem === 'comparison' ? styles.active : ''}`}
          onClick={() => setActiveSystem('comparison')}
        >
          Compare
        </button>
      </div>

      {/* Vimshottari Timeline */}
      {activeSystem === 'vimshottari' && (
        <div className={styles.timeline}>
          <div className={styles.timelineHeader}>
            <h4>Vimshottari Mahadasha (120-year cycle)</h4>
            <p>Based on Moon's nakshatra at birth</p>
          </div>
          <div className={styles.timelinePeriods}>
            {vimshottariDashas.map((period, idx) => (
              <div 
                key={idx}
                className={`${styles.periodBar} ${period.isCurrent ? styles.current : ''}`}
                style={{ 
                  flex: period.years,
                  backgroundColor: period.isCurrent ? PLANET_COLORS[period.planet] : `${PLANET_COLORS[period.planet]}40`
                }}
                onClick={() => setShowDetails(showDetails === `vim-${idx}` ? null : `vim-${idx}`)}
              >
                <span className={styles.periodLabel}>
                  {PLANET_SYMBOLS[period.planet]} {period.planet}
                </span>
                <span className={styles.periodYears}>{period.years.toFixed(1)}y</span>
                
                {showDetails === `vim-${idx}` && (
                  <div className={styles.periodDetails}>
                    <p><strong>{period.planet} Mahadasha</strong></p>
                    <p>Start: {formatDate(period.startDate)}</p>
                    <p>End: {formatDate(period.endDate)}</p>
                    <p>Duration: {period.years.toFixed(2)} years</p>
                    {period.isCurrent && (
                      <div className={styles.progressBar}>
                        <div 
                          className={styles.progressFill}
                          style={{ width: `${getProgress(period.startDate, period.endDate)}%` }}
                        />
                      </div>
                    )}
                  </div>
                )}
              </div>
            ))}
          </div>
          
          {/* Current Period Details */}
          {currentVimshottari && (
            <div className={styles.currentDetails}>
              <h4>Current: {currentVimshottari.planet} Mahadasha</h4>
              <div className={styles.progressSection}>
                <div className={styles.progressInfo}>
                  <span>{formatDate(currentVimshottari.startDate)}</span>
                  <span>{getProgress(currentVimshottari.startDate, currentVimshottari.endDate).toFixed(1)}% complete</span>
                  <span>{formatDate(currentVimshottari.endDate)}</span>
                </div>
                <div className={styles.largeProgress}>
                  <div 
                    className={styles.progressFill}
                    style={{ 
                      width: `${getProgress(currentVimshottari.startDate, currentVimshottari.endDate)}%`,
                      backgroundColor: PLANET_COLORS[currentVimshottari.planet]
                    }}
                  />
                </div>
              </div>
              <div className={styles.periodEffects}>
                <h5>Period Significations:</h5>
                <p>{getDashaSignifications(currentVimshottari.planet)}</p>
              </div>
            </div>
          )}
        </div>
      )}

      {/* Yogini Timeline */}
      {activeSystem === 'yogini' && (
        <div className={styles.timeline}>
          <div className={styles.timelineHeader}>
            <h4>Yogini Dasha (36-year cycle)</h4>
            <p>Faster cycle - useful for timing events</p>
          </div>
          <div className={styles.timelinePeriods}>
            {yoginiDashas.map((period, idx) => (
              <div 
                key={idx}
                className={`${styles.periodBar} ${period.isCurrent ? styles.current : ''}`}
                style={{ 
                  flex: period.years,
                  backgroundColor: period.isCurrent ? PLANET_COLORS[period.planet] : `${PLANET_COLORS[period.planet]}40`
                }}
                onClick={() => setShowDetails(showDetails === `yog-${idx}` ? null : `yog-${idx}`)}
              >
                <span className={styles.periodLabel}>
                  {PLANET_SYMBOLS[period.planet]} {period.yogini}
                </span>
                <span className={styles.periodYears}>{period.years.toFixed(1)}y</span>
                
                {showDetails === `yog-${idx}` && (
                  <div className={styles.periodDetails}>
                    <p><strong>{period.yogini} ({period.planet})</strong></p>
                    <p>Start: {formatDate(period.startDate)}</p>
                    <p>End: {formatDate(period.endDate)}</p>
                    <p>Duration: {period.years.toFixed(2)} years</p>
                  </div>
                )}
              </div>
            ))}
          </div>

          {/* Yogini Legend */}
          <div className={styles.yoginiLegend}>
            <h5>Yogini Deities:</h5>
            <div className={styles.legendGrid}>
              {Object.entries(YOGINI_PERIODS).map(([yogini, data]) => (
                <div key={yogini} className={styles.legendItem}>
                  <span style={{ color: PLANET_COLORS[data.planet] }}>{PLANET_SYMBOLS[data.planet]}</span>
                  <span>{yogini}</span>
                  <span className={styles.legendPlanet}>({data.planet})</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* Comparison View */}
      {activeSystem === 'comparison' && (
        <div className={styles.comparison}>
          <div className={styles.comparisonTable}>
            <table>
              <thead>
                <tr>
                  <th>System</th>
                  <th>Total Cycle</th>
                  <th>Current Period</th>
                  <th>Ends</th>
                  <th>Best For</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td><strong>Vimshottari</strong></td>
                  <td>120 years</td>
                  <td>
                    <span style={{ color: PLANET_COLORS[currentVimshottari?.planet || 'Sun'] }}>
                      {PLANET_SYMBOLS[currentVimshottari?.planet || 'Sun']} {currentVimshottari?.planet}
                    </span>
                  </td>
                  <td>{currentVimshottari && formatDate(currentVimshottari.endDate)}</td>
                  <td>Major life events</td>
                </tr>
                <tr>
                  <td><strong>Yogini</strong></td>
                  <td>36 years</td>
                  <td>
                    <span style={{ color: PLANET_COLORS[currentYogini?.planet || 'Moon'] }}>
                      {PLANET_SYMBOLS[currentYogini?.planet || 'Moon']} {currentYogini?.yogini}
                    </span>
                  </td>
                  <td>{currentYogini && formatDate(currentYogini.endDate)}</td>
                  <td>Short-term timing</td>
                </tr>
              </tbody>
            </table>
          </div>

          <div className={styles.comparisonNote}>
            <h5>💡 Understanding Dasha Systems</h5>
            <ul>
              <li><strong>Vimshottari:</strong> Most widely used, covers entire life span. Good for major predictions.</li>
              <li><strong>Yogini:</strong> Faster 36-year cycle, repeats ~3 times in life. Good for event timing.</li>
              <li><strong>Best practice:</strong> Use both systems together - Vimshottari for theme, Yogini for timing.</li>
            </ul>
          </div>
        </div>
      )}

      <div className={styles.dashaFooter}>
        <p>
          <strong>Note:</strong> Dasha results are modified by the strength and placement of the ruling planet. 
          Sub-periods (Antardasha) provide more specific timing within each major period.
        </p>
      </div>
    </div>
  );
}

function getDashaSignifications(planet: string): string {
  const significations: Record<string, string> = {
    Sun: 'Authority, father, government, health vitality, soul purpose, leadership roles.',
    Moon: 'Mind, mother, emotions, public life, travel, changes, mental peace.',
    Mars: 'Energy, courage, siblings, property, conflicts, surgery, competition.',
    Mercury: 'Communication, business, education, intellect, writing, nervous system.',
    Jupiter: 'Wisdom, children, wealth, spirituality, teachers, expansion, luck.',
    Venus: 'Relationships, marriage, arts, luxury, vehicles, comfort, beauty.',
    Saturn: 'Discipline, hard work, delays, karma, old age, structure, chronic issues.',
    Rahu: 'Worldly desires, foreign elements, unconventional, obsession, technology.',
    Ketu: 'Spirituality, detachment, past karma, liberation, losses, mysticism.'
  };
  return significations[planet] || 'General influences based on planet\'s nature.';
}
