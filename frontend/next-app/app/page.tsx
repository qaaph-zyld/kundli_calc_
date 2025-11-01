import { getHealth } from '../src/lib/api';
import ChartDemo from '../src/components/ChartDemo';

export default async function Page() {
  let health: { status: string } | null = null;
  try {
    health = await getHealth();
  } catch (e) {
    health = null;
  }

  return (
    <main style={{ maxWidth: 900, margin: '0 auto', padding: 24 }}>
      <h1 style={{ marginBottom: 8 }}>Kundli Calc</h1>
      <p style={{ color: '#666', marginTop: 0 }}>
        Backend: {health ? `healthy (${health.status})` : 'unreachable'}
      </p>

      <section style={{ marginTop: 24 }}>
        <h2>Quick Chart Demo</h2>
        <p>Click to calculate a sample chart (Loznica, Serbia, 1990-10-09 07:10 UTC).</p>
        <ChartDemo />
      </section>
    </main>
  );
}
