export const API_BASE =
  process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000';

export async function getHealth(): Promise<{ status: string }> {
  const res = await fetch(`${API_BASE}/api/v1/health`);
  if (!res.ok) throw new Error(`Health failed: ${res.status}`);
  return res.json();
}

export interface ChartRequest {
  date_time: string;
  latitude: number;
  longitude: number;
  altitude?: number;
  ayanamsa_type?: string;
  ayanamsa?: number;
  house_system?: string;
}

export async function calculateChart(body: ChartRequest) {
  const res = await fetch(`${API_BASE}/api/v1/charts/calculate`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  });
  if (!res.ok) {
    const t = await res.text();
    throw new Error(`Chart failed: ${res.status} ${t}`);
  }
  return res.json();
}

export async function resolvePlace(query: string): Promise<{ latitude: number; longitude: number; display_name: string; raw: any; }>{
  const res = await fetch(`${API_BASE}/api/v1/geo/resolve`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ query })
  });
  if (!res.ok) {
    const t = await res.text();
    throw new Error(`Geo resolve failed: ${res.status} ${t}`);
  }
  return res.json();
}

export async function timezoneFromCoords(latitude: number, longitude: number): Promise<{ timezone: string }>{
  const res = await fetch(`${API_BASE}/api/v1/geo/timezone`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ latitude, longitude })
  });
  if (!res.ok) {
    const t = await res.text();
    throw new Error(`Timezone lookup failed: ${res.status} ${t}`);
  }
  return res.json();
}

// ============= KP SYSTEM API =============
export interface KPRequest {
  datetime: string;
  latitude: number;
  longitude: number;
  timezone?: string;
  planets: Record<string, number>;
  house_cusps: number[];
}

export async function calculateKPData(body: KPRequest) {
  const res = await fetch(`${API_BASE}/api/v1/kp/calculate`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  });
  if (!res.ok) {
    const t = await res.text();
    throw new Error(`KP calculation failed: ${res.status} ${t}`);
  }
  return res.json();
}

export async function getKPPosition(longitude: number) {
  const res = await fetch(`${API_BASE}/api/v1/kp/position/${longitude}`);
  if (!res.ok) throw new Error(`KP position failed: ${res.status}`);
  return res.json();
}

export async function getRulingPlanets(datetime: string, moonLon: number, ascLon: number) {
  const res = await fetch(`${API_BASE}/api/v1/kp/ruling-planets`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      datetime,
      moon_longitude: moonLon,
      ascendant_longitude: ascLon
    }),
  });
  if (!res.ok) throw new Error(`Ruling planets failed: ${res.status}`);
  return res.json();
}

// ============= YOGAS API =============
export interface YogaRequest {
  planets: Record<string, { longitude: number; sign?: number; house?: number }>;
  houses: Record<number, string[]>;
  ascendant_sign: number;
}

export async function calculateYogas(body: YogaRequest) {
  const res = await fetch(`${API_BASE}/api/v1/yogas/calculate`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  });
  if (!res.ok) {
    const t = await res.text();
    throw new Error(`Yoga calculation failed: ${res.status} ${t}`);
  }
  return res.json();
}

export async function getYogaCategories() {
  const res = await fetch(`${API_BASE}/api/v1/yogas/categories`);
  if (!res.ok) throw new Error(`Yoga categories failed: ${res.status}`);
  return res.json();
}

// ============= TRANSIT API =============
export interface TransitRequest {
  natal_moon_sign: number;
  natal_planets: Record<string, number>;
  current_positions: Record<string, number>;
  datetime?: string;
}

export async function analyzeTransits(body: TransitRequest) {
  const res = await fetch(`${API_BASE}/api/v1/transits/analyze`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  });
  if (!res.ok) {
    const t = await res.text();
    throw new Error(`Transit analysis failed: ${res.status} ${t}`);
  }
  return res.json();
}

export async function checkSadeSati(moonSign: number, saturnLon: number) {
  const res = await fetch(`${API_BASE}/api/v1/transits/sade-sati`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      natal_moon_sign: moonSign,
      current_saturn_longitude: saturnLon
    }),
  });
  if (!res.ok) throw new Error(`Sade Sati check failed: ${res.status}`);
  return res.json();
}

// ============= DASHA API =============
export interface DashaRequest {
  birth_datetime: string;
  moon_longitude: number;
  ascendant_longitude?: number;
  planet_longitudes?: Record<string, number>;
}

export async function calculateAllDashas(body: DashaRequest) {
  const res = await fetch(`${API_BASE}/api/v1/dashas/all-systems`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  });
  if (!res.ok) {
    const t = await res.text();
    throw new Error(`Dasha calculation failed: ${res.status} ${t}`);
  }
  return res.json();
}

export async function getCurrentDashas(body: DashaRequest & { current_datetime?: string }) {
  const res = await fetch(`${API_BASE}/api/v1/dashas/current`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  });
  if (!res.ok) throw new Error(`Current dasha failed: ${res.status}`);
  return res.json();
}

export async function getDashaComparison() {
  const res = await fetch(`${API_BASE}/api/v1/dashas/comparison`);
  if (!res.ok) throw new Error(`Dasha comparison failed: ${res.status}`);
  return res.json();
}

// ============= DIVISIONAL CHARTS API =============
export interface DivisionalRequest {
  date_time: string;
  latitude: number;
  longitude: number;
  altitude?: number;
  division: number;  // D1=1, D2=2, D9=9, etc.
}

export async function calculateDivisionalChart(body: DivisionalRequest) {
  const res = await fetch(`${API_BASE}/api/v1/divisional/calculate`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  });
  if (!res.ok) {
    const t = await res.text();
    throw new Error(`Divisional chart failed: ${res.status} ${t}`);
  }
  return res.json();
}

// Common divisional charts
export const DIVISIONAL_CHARTS = {
  D1: { division: 1, name: 'Rasi', description: 'Main birth chart' },
  D2: { division: 2, name: 'Hora', description: 'Wealth and prosperity' },
  D3: { division: 3, name: 'Drekkana', description: 'Siblings and courage' },
  D4: { division: 4, name: 'Chaturthamsa', description: 'Fortune and property' },
  D7: { division: 7, name: 'Saptamsa', description: 'Children and progeny' },
  D9: { division: 9, name: 'Navamsa', description: 'Marriage and dharma' },
  D10: { division: 10, name: 'Dasamsa', description: 'Career and profession' },
  D12: { division: 12, name: 'Dwadasamsa', description: 'Parents and ancestry' },
  D16: { division: 16, name: 'Shodasamsa', description: 'Vehicles and happiness' },
  D20: { division: 20, name: 'Vimshamsa', description: 'Spiritual progress' },
  D24: { division: 24, name: 'Chaturvimshamsa', description: 'Education and learning' },
  D27: { division: 27, name: 'Nakshatramsa', description: 'Strengths and weaknesses' },
  D30: { division: 30, name: 'Trimsamsa', description: 'Misfortunes and evils' },
  D60: { division: 60, name: 'Shashtyamsa', description: 'Past life karma' },
} as const;

// ============= SHADBALA API =============
export interface ShadbalaRequest {
  planetary_positions: Record<string, { longitude: number; sign: string; house: number }>;
  ascendant_longitude: number;
  birth_datetime: string;
}

export async function calculateShadbala(body: ShadbalaRequest) {
  const res = await fetch(`${API_BASE}/api/v1/shadbala/calculate`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  });
  if (!res.ok) {
    const t = await res.text();
    throw new Error(`Shadbala calculation failed: ${res.status} ${t}`);
  }
  return res.json();
}

// ============= ASHTAKAVARGA API =============
export interface AshtakavargaRequest {
  planet_positions: Record<string, number>;  // Planet name to house number (1-12)
}

export async function calculateAshtakavarga(body: AshtakavargaRequest) {
  const res = await fetch(`${API_BASE}/api/v1/ashtakavarga/calculate`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  });
  if (!res.ok) {
    const t = await res.text();
    throw new Error(`Ashtakavarga calculation failed: ${res.status} ${t}`);
  }
  return res.json();
}
