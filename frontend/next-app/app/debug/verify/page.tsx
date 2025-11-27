import React from 'react';

async function fetchVerification() {
  const res = await fetch('http://localhost:8000/api/v1/debug/verify', {
    cache: 'no-store',
  });

  if (!res.ok) {
    throw new Error(`Failed to fetch /api/v1/debug/verify: ${res.status}`);
  }

  return res.json();
}

export default async function DebugVerifyPage() {
  const data = await fetchVerification();
  const summary = data.summary || { passed: [], failed: [], all_passed: false };
  const results = data.results || {};

  return (
    <main style={{ padding: '1.5rem', maxWidth: 960, margin: '0 auto', fontFamily: 'system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif' }}>
      <h1 style={{ fontSize: '1.8rem', fontWeight: 700, marginBottom: '0.75rem' }}>
        Debug Verification Dashboard
      </h1>
      <p style={{ marginBottom: '1.25rem', color: '#555' }}>
        Live summary of backend calculation modules (Phase 5 & 6). This runs against the
        hard-coded test birth data (Oct 9 1990, Loznica) and sample planets.
      </p>

      <section
        style={{
          border: '1px solid #e2e8f0',
          borderRadius: 8,
          padding: '1rem 1.25rem',
          marginBottom: '1.5rem',
          background: summary.all_passed ? '#f0fff4' : '#fffaf0',
        }}
      >
        <h2 style={{ fontSize: '1.2rem', fontWeight: 600, marginBottom: '0.5rem' }}>Summary</h2>
        <p style={{ margin: 0 }}>
          Overall status:{' '}
          <strong style={{ color: summary.all_passed ? '#15803d' : '#b91c1c' }}>
            {summary.all_passed ? 'ALL PASSED' : 'SOME TESTS FAILED'}
          </strong>
        </p>
        <p style={{ margin: '0.5rem 0 0' }}>
          Passed modules: {summary.passed?.length || 0} • Failed modules: {summary.failed?.length || 0}
        </p>
      </section>

      <section>
        <h2 style={{ fontSize: '1.2rem', fontWeight: 600, marginBottom: '0.75rem' }}>Module Status</h2>
        <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
          {Object.entries(results).map(([key, value]: [string, any]) => {
            const status = value?.status || 'unknown';
            const isPass = status === 'pass';
            const isFail = status === 'fail';

            return (
              <details
                key={key}
                style={{
                  border: '1px solid #e5e7eb',
                  borderRadius: 6,
                  padding: '0.5rem 0.75rem',
                  background: '#ffffff',
                }}
              >
                <summary
                  style={{
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'space-between',
                    cursor: 'pointer',
                    listStyle: 'none',
                  }}
                >
                  <span style={{ fontWeight: 500 }}>{key}</span>
                  <span
                    style={{
                      fontSize: '0.85rem',
                      padding: '0.15rem 0.5rem',
                      borderRadius: 999,
                      backgroundColor: isPass ? '#dcfce7' : isFail ? '#fee2e2' : '#e5e7eb',
                      color: isPass ? '#15803d' : isFail ? '#b91c1c' : '#374151',
                    }}
                  >
                    {status.toUpperCase()}
                  </span>
                </summary>
                <pre
                  style={{
                    marginTop: '0.5rem',
                    fontSize: '0.8rem',
                    whiteSpace: 'pre-wrap',
                    wordBreak: 'break-word',
                    background: '#f9fafb',
                    padding: '0.5rem',
                    borderRadius: 4,
                    maxHeight: 320,
                    overflow: 'auto',
                  }}
                >
                  {JSON.stringify(value, null, 2)}
                </pre>
              </details>
            );
          })}
        </div>
      </section>
    </main>
  );
}
