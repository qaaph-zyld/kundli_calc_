import http from 'k6/http';
import { check, sleep } from 'k6';
import { Rate } from 'k6/metrics';

// Custom metrics
const errorRate = new Rate('errors');

// Test configuration
export const options = {
  stages: [
    { duration: '1m', target: 50 },  // Ramp up to 50 users
    { duration: '3m', target: 50 },  // Stay at 50 users
    { duration: '1m', target: 100 }, // Ramp up to 100 users
    { duration: '3m', target: 100 }, // Stay at 100 users
    { duration: '1m', target: 0 },   // Ramp down to 0 users
  ],
  thresholds: {
    http_req_duration: ['p(95)<500'], // 95% of requests should be below 500ms
    'http_req_duration{type:kundliCalculation}': ['p(95)<2000'], // 95% of kundli calculations should be below 2s
    errors: ['rate<0.1'],  // Error rate should be below 10%
  },
};

// Simulated user behavior
export default function () {
  // Get auth token
  const loginRes = http.post('http://localhost:8000/auth/login', {
    email: 'testuser@example.com',
    password: 'testpassword',
  });

  check(loginRes, {
    'login successful': (r) => r.status === 200,
  }) || errorRate.add(1);

  const authToken = loginRes.json('access_token');

  // Headers for authenticated requests
  const params = {
    headers: {
      'Authorization': `Bearer ${authToken}`,
      'Content-Type': 'application/json',
    },
  };

  // Test kundli calculation
  const kundliData = {
    birth_date: '2000-01-01',
    birth_time: '12:00:00',
    latitude: 28.6139,
    longitude: 77.2090,
    timezone: 'Asia/Kolkata',
  };

  const kundliRes = http.post('http://localhost:8000/kundli/create', 
    JSON.stringify(kundliData), 
    { 
      ...params,
      tags: { type: 'kundliCalculation' },
    }
  );

  check(kundliRes, {
    'kundli calculation successful': (r) => r.status === 201,
  }) || errorRate.add(1);

  const kundliId = kundliRes.json('kundli_id');

  // Test getting kundli details
  const getKundliRes = http.get(
    `http://localhost:8000/kundli/${kundliId}`,
    params
  );

  check(getKundliRes, {
    'get kundli successful': (r) => r.status === 200,
  }) || errorRate.add(1);

  // Test planetary positions calculation
  const planetsRes = http.post(
    'http://localhost:8000/calculate/planets',
    JSON.stringify(kundliData),
    params
  );

  check(planetsRes, {
    'planetary calculation successful': (r) => r.status === 200,
  }) || errorRate.add(1);

  // Test house system calculation
  const housesRes = http.post(
    'http://localhost:8000/calculate/houses',
    JSON.stringify(kundliData),
    params
  );

  check(housesRes, {
    'house calculation successful': (r) => r.status === 200,
  }) || errorRate.add(1);

  // Random sleep between requests to simulate real user behavior
  sleep(Math.random() * 3);
}
