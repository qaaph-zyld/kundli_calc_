import http from 'k6/http';
import { check, sleep, group } from 'k6';
import { Counter, Rate, Trend } from 'k6/metrics';
import { randomIntBetween } from 'https://jslib.k6.io/k6-utils/1.2.0/index.js';

// Custom metrics
const successfulCalculations = new Counter('successful_calculations');
const calculationDuration = new Trend('calculation_duration');
const errorRate = new Rate('error_rate');
const cachingEfficiency = new Rate('caching_efficiency');

// Test configuration for different scenarios
export const options = {
  scenarios: {
    // Smoke test
    smoke: {
      executor: 'constant-vus',
      vus: 1,
      duration: '1m',
      tags: { test_type: 'smoke' },
    },
    
    // Load test
    load: {
      executor: 'ramping-vus',
      startVUs: 0,
      stages: [
        { duration: '2m', target: 100 },  // Ramp up
        { duration: '5m', target: 100 },  // Stay at load
        { duration: '2m', target: 0 },    // Ramp down
      ],
      tags: { test_type: 'load' },
    },
    
    // Stress test
    stress: {
      executor: 'ramping-vus',
      startVUs: 0,
      stages: [
        { duration: '2m', target: 100 },   // Ramp up to load
        { duration: '5m', target: 100 },   // Stay at load
        { duration: '2m', target: 200 },   // Ramp up to stress
        { duration: '5m', target: 200 },   // Stay at stress
        { duration: '2m', target: 300 },   // Ramp up to breaking point
        { duration: '5m', target: 300 },   // Stay at breaking point
        { duration: '2m', target: 0 },     // Ramp down
      ],
      tags: { test_type: 'stress' },
    },
    
    // Soak test
    soak: {
      executor: 'constant-vus',
      vus: 50,
      duration: '2h',
      tags: { test_type: 'soak' },
    },
    
    // Spike test
    spike: {
      executor: 'ramping-vus',
      startVUs: 0,
      stages: [
        { duration: '1m', target: 0 },     // Baseline
        { duration: '10s', target: 500 },  // Spike up
        { duration: '1m', target: 500 },   // Stay at spike
        { duration: '10s', target: 0 },    // Spike down
        { duration: '3m', target: 0 },     // Recovery
      ],
      tags: { test_type: 'spike' },
    },
  },
  thresholds: {
    http_req_duration: ['p(95)<2000'], // 95% of requests should be below 2s
    error_rate: ['rate<0.1'],          // Error rate should be below 10%
    'calculation_duration{type:kundli}': ['p(95)<5000'], // 95% of kundli calculations should be below 5s
    'caching_efficiency': ['rate>0.8'], // Cache hit rate should be above 80%
  },
};

// Test setup
const BASE_URL = 'http://localhost:8000';

// Helper function to get auth token
function getAuthToken() {
  const loginRes = http.post(`${BASE_URL}/auth/login`, {
    email: 'testuser@example.com',
    password: 'testpassword',
  });
  
  if (loginRes.status !== 200) {
    errorRate.add(1);
    return null;
  }
  
  return loginRes.json('access_token');
}

// Main test function
export default function () {
  const authToken = getAuthToken();
  if (!authToken) return;
  
  const params = {
    headers: {
      'Authorization': `Bearer ${authToken}`,
      'Content-Type': 'application/json',
    },
  };
  
  group('Kundli Calculation Tests', function () {
    // Generate random birth data
    const birthData = {
      birth_date: '2000-01-01',
      birth_time: `${randomIntBetween(0, 23)}:${randomIntBetween(0, 59)}:00`,
      latitude: 28.6139 + (Math.random() * 2 - 1),  // Random variation around Delhi
      longitude: 77.2090 + (Math.random() * 2 - 1),
      timezone: 'Asia/Kolkata',
    };
    
    // Test kundli calculation
    const startTime = new Date();
    const kundliRes = http.post(
      `${BASE_URL}/kundli/create`,
      JSON.stringify(birthData),
      params
    );
    calculationDuration.add(new Date() - startTime, { type: 'kundli' });
    
    if (check(kundliRes, {
      'kundli calculation successful': (r) => r.status === 201,
    })) {
      successfulCalculations.add(1);
    } else {
      errorRate.add(1);
    }
    
    if (kundliRes.status === 201) {
      const kundliId = kundliRes.json('kundli_id');
      
      // Test cached response
      const cachedRes = http.get(
        `${BASE_URL}/kundli/${kundliId}`,
        params
      );
      
      if (cachedRes.headers['X-Cache'] === 'HIT') {
        cachingEfficiency.add(1);
      } else {
        cachingEfficiency.add(0);
      }
    }
  });
  
  group('Planetary Calculations Tests', function () {
    // Test planetary positions
    const planetsRes = http.post(
      `${BASE_URL}/calculate/planets`,
      JSON.stringify({
        date: '2000-01-01',
        time: '12:00:00',
        latitude: 28.6139,
        longitude: 77.2090,
      }),
      params
    );
    
    check(planetsRes, {
      'planetary calculation successful': (r) => r.status === 200,
    }) || errorRate.add(1);
  });
  
  // Random sleep between requests
  sleep(randomIntBetween(1, 5));
}
