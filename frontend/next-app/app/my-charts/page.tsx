"use client";
import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '../../src/contexts/AuthContext';
import { getUserCharts, deleteChart, SavedChart } from '../../src/lib/supabase/charts';
import Header from '../../src/components/Header';
import styles from './page.module.css';

export default function MyChartsPage() {
  const router = useRouter();
  const { user, loading: authLoading } = useAuth();
  const [charts, setCharts] = useState<SavedChart[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [deletingId, setDeletingId] = useState<string | null>(null);

  useEffect(() => {
    if (!authLoading && !user) {
      router.push('/');
      return;
    }

    if (user) {
      loadCharts();
    }
  }, [user, authLoading, router]);

  const loadCharts = async () => {
    setLoading(true);
    setError(null);
    
    const { data, error: err } = await getUserCharts();
    
    if (err) {
      setError(err.message || 'Failed to load charts');
    } else {
      setCharts(data || []);
    }
    
    setLoading(false);
  };

  const handleDelete = async (chartId: string) => {
    if (!confirm('Are you sure you want to delete this chart?')) {
      return;
    }

    setDeletingId(chartId);
    const { error: err } = await deleteChart(chartId);
    
    if (err) {
      alert('Failed to delete chart: ' + err.message);
    } else {
      setCharts(charts.filter(c => c.id !== chartId));
    }
    
    setDeletingId(null);
  };

  const handleView = (chart: SavedChart) => {
    // Store chart in sessionStorage and navigate to home
    sessionStorage.setItem('viewChart', JSON.stringify(chart));
    router.push('/');
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  if (authLoading || loading) {
    return (
      <>
        <Header />
        <main className={styles.container}>
          <div className={styles.loading}>
            <div className={styles.spinner}></div>
            <p>Loading your charts...</p>
          </div>
        </main>
      </>
    );
  }

  return (
    <>
      <Header />
      <main className={styles.container}>
        <div className={styles.header}>
          <h1>My Saved Charts</h1>
          <button onClick={() => router.push('/')} className={styles.newChartBtn}>
            ➕ Generate New Chart
          </button>
        </div>

        {error && (
          <div className={styles.error}>
            <strong>Error:</strong> {error}
          </div>
        )}

        {charts.length === 0 ? (
          <div className={styles.empty}>
            <div className={styles.emptyIcon}>📊</div>
            <h2>No saved charts yet</h2>
            <p>Generate your first kundli chart and save it to see it here!</p>
            <button onClick={() => router.push('/')} className={styles.emptyBtn}>
              Generate Your First Chart
            </button>
          </div>
        ) : (
          <div className={styles.grid}>
            {charts.map((chart) => (
              <div key={chart.id} className={styles.card}>
                <div className={styles.cardHeader}>
                  <h3>{chart.title}</h3>
                  <span className={styles.date}>
                    {formatDate(chart.created_at)}
                  </span>
                </div>

                <div className={styles.cardBody}>
                  <div className={styles.details}>
                    <div className={styles.detailItem}>
                      <span className={styles.label}>📅 Date:</span>
                      <span>{chart.birth_details.date}</span>
                    </div>
                    <div className={styles.detailItem}>
                      <span className={styles.label}>🕐 Time:</span>
                      <span>{chart.birth_details.time}</span>
                    </div>
                    <div className={styles.detailItem}>
                      <span className={styles.label}>📍 Location:</span>
                      <span>{chart.birth_details.locationName}</span>
                    </div>
                    <div className={styles.detailItem}>
                      <span className={styles.label}>🔆 Ascendant:</span>
                      <span className={styles.highlight}>
                        {chart.chart_data?.houses?.ascendant?.sign || 'N/A'}
                      </span>
                    </div>
                  </div>

                  {/* Chart Preview */}
                  <div className={styles.preview}>
                    <div className={styles.previewBadge}>
                      Rasi Chart
                    </div>
                  </div>
                </div>

                <div className={styles.cardActions}>
                  <button
                    onClick={() => handleView(chart)}
                    className={styles.viewBtn}
                  >
                    👁️ View Chart
                  </button>
                  <button
                    onClick={() => handleDelete(chart.id)}
                    className={styles.deleteBtn}
                    disabled={deletingId === chart.id}
                  >
                    {deletingId === chart.id ? '⏳' : '🗑️'} Delete
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </main>
    </>
  );
}
