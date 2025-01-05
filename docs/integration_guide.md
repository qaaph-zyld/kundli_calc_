# Kundli Calculation Service - Integration Guide

## Overview
This guide provides detailed instructions for integrating the Kundli Calculation Service into your applications. It covers various integration patterns, authentication methods, and best practices.

## Table of Contents
1. [REST API Integration](#rest-api-integration)
2. [SDK Integration](#sdk-integration)
3. [Webhook Integration](#webhook-integration)
4. [Authentication](#authentication)
5. [Error Handling](#error-handling)
6. [Rate Limiting](#rate-limiting)
7. [Best Practices](#best-practices)

## REST API Integration

### 1. Basic API Usage

#### Authentication
```javascript
// Get JWT token
const getToken = async () => {
  const response = await fetch('https://api.kundli-service.com/v1/auth/token', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      api_key: 'your_api_key'
    })
  });
  
  const { token } = await response.json();
  return token;
};
```

#### Calculate Kundli
```javascript
// Calculate basic kundli
const calculateKundli = async (token, data) => {
  const response = await fetch('https://api.kundli-service.com/v1/kundli/calculate', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      date: '2025-01-05',
      time: '06:18:33',
      latitude: 28.6139,
      longitude: 77.2090,
      timezone: 'Asia/Kolkata'
    })
  });
  
  return await response.json();
};
```

### 2. Advanced API Usage

#### Batch Processing
```javascript
// Calculate multiple kundlis
const batchCalculate = async (token, dataList) => {
  const response = await fetch('https://api.kundli-service.com/v1/kundli/batch', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      calculations: dataList
    })
  });
  
  return await response.json();
};
```

#### Streaming Results
```javascript
// Stream calculation results
const streamCalculations = async (token, query) => {
  const response = await fetch('https://api.kundli-service.com/v1/kundli/stream', {
    method: 'GET',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Accept': 'text/event-stream',
    }
  });
  
  const reader = response.body.getReader();
  
  while (true) {
    const { done, value } = await reader.read();
    if (done) break;
    console.log(new TextDecoder().decode(value));
  }
};
```

## SDK Integration

### 1. Python SDK

#### Installation
```bash
pip install kundli-service-sdk
```

#### Usage
```python
from kundli_service import KundliClient

# Initialize client
client = KundliClient(api_key='your_api_key')

# Calculate kundli
result = client.calculate_kundli(
    date='2025-01-05',
    time='06:18:33',
    latitude=28.6139,
    longitude=77.2090,
    timezone='Asia/Kolkata'
)

# Get planetary positions
planets = result.get_planetary_positions()

# Get house cusps
houses = result.get_house_cusps()

# Get yogas
yogas = result.get_yogas()
```

### 2. JavaScript SDK

#### Installation
```bash
npm install kundli-service-sdk
```

#### Usage
```javascript
import { KundliClient } from 'kundli-service-sdk';

// Initialize client
const client = new KundliClient({
  apiKey: 'your_api_key'
});

// Calculate kundli
const calculateKundli = async () => {
  const result = await client.calculateKundli({
    date: '2025-01-05',
    time: '06:18:33',
    latitude: 28.6139,
    longitude: 77.2090,
    timezone: 'Asia/Kolkata'
  });
  
  // Get calculations
  const planets = result.getPlanetaryPositions();
  const houses = result.getHouseCusps();
  const yogas = result.getYogas();
};
```

## Webhook Integration

### 1. Configure Webhooks
```javascript
// Register webhook endpoint
const registerWebhook = async (token, endpoint) => {
  const response = await fetch('https://api.kundli-service.com/v1/webhooks', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      url: endpoint,
      events: ['calculation.complete', 'calculation.error']
    })
  });
  
  return await response.json();
};
```

### 2. Handle Webhook Events
```javascript
// Express.js webhook handler
app.post('/webhooks/kundli', async (req, res) => {
  const { event, data } = req.body;
  
  switch (event) {
    case 'calculation.complete':
      await handleCalculationComplete(data);
      break;
    
    case 'calculation.error':
      await handleCalculationError(data);
      break;
  }
  
  res.sendStatus(200);
});
```

## Authentication

### 1. API Key Authentication
```javascript
// Using API key in header
const headers = {
  'X-API-Key': 'your_api_key',
  'Content-Type': 'application/json'
};
```

### 2. JWT Authentication
```javascript
// Refresh token
const refreshToken = async (refresh_token) => {
  const response = await fetch('https://api.kundli-service.com/v1/auth/refresh', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      refresh_token
    })
  });
  
  return await response.json();
};
```

## Error Handling

### 1. Error Types
```javascript
// Handle specific error types
try {
  await client.calculateKundli(data);
} catch (error) {
  switch (error.code) {
    case 'VALIDATION_ERROR':
      handleValidationError(error);
      break;
    
    case 'CALCULATION_ERROR':
      handleCalculationError(error);
      break;
    
    case 'AUTH_ERROR':
      handleAuthError(error);
      break;
    
    default:
      handleGenericError(error);
  }
}
```

### 2. Retry Logic
```javascript
// Implement retry with exponential backoff
const retryWithBackoff = async (fn, maxRetries = 3) => {
  for (let i = 0; i < maxRetries; i++) {
    try {
      return await fn();
    } catch (error) {
      if (i === maxRetries - 1) throw error;
      await new Promise(resolve => 
        setTimeout(resolve, Math.pow(2, i) * 1000)
      );
    }
  }
};
```

## Rate Limiting

### 1. Client-Side Rate Limiting
```javascript
// Implement token bucket rate limiting
class RateLimiter {
  constructor(tokensPerSecond) {
    this.tokens = tokensPerSecond;
    this.tokensPerSecond = tokensPerSecond;
    this.lastRefill = Date.now();
  }
  
  async acquire() {
    const now = Date.now();
    const timePassed = (now - this.lastRefill) / 1000;
    this.tokens = Math.min(
      this.tokensPerSecond,
      this.tokens + timePassed * this.tokensPerSecond
    );
    
    if (this.tokens < 1) {
      const waitTime = (1 - this.tokens) / this.tokensPerSecond * 1000;
      await new Promise(resolve => setTimeout(resolve, waitTime));
    }
    
    this.tokens -= 1;
    this.lastRefill = now;
  }
}
```

### 2. Handle Rate Limit Errors
```javascript
// Check rate limits and handle errors
const makeRequest = async () => {
  try {
    await rateLimiter.acquire();
    return await client.calculateKundli(data);
  } catch (error) {
    if (error.code === 'RATE_LIMIT_EXCEEDED') {
      const retryAfter = error.headers.get('Retry-After');
      await new Promise(resolve => 
        setTimeout(resolve, retryAfter * 1000)
      );
      return makeRequest();
    }
    throw error;
  }
};
```

## Best Practices

### 1. Connection Management
```javascript
// Implement connection pooling
class ConnectionPool {
  constructor(maxConnections = 10) {
    this.pool = [];
    this.maxConnections = maxConnections;
  }
  
  async getConnection() {
    if (this.pool.length < this.maxConnections) {
      const connection = await createConnection();
      this.pool.push(connection);
      return connection;
    }
    
    return this.pool[Math.floor(Math.random() * this.pool.length)];
  }
}
```

### 2. Caching
```javascript
// Implement result caching
class ResultCache {
  constructor(ttl = 3600) {
    this.cache = new Map();
    this.ttl = ttl;
  }
  
  async get(key) {
    const item = this.cache.get(key);
    if (!item) return null;
    
    if (Date.now() > item.expiry) {
      this.cache.delete(key);
      return null;
    }
    
    return item.value;
  }
  
  set(key, value) {
    this.cache.set(key, {
      value,
      expiry: Date.now() + this.ttl * 1000
    });
  }
}
```

### 3. Monitoring
```javascript
// Implement basic monitoring
class ServiceMonitor {
  constructor() {
    this.metrics = {
      requests: 0,
      errors: 0,
      latency: []
    };
  }
  
  async trackRequest(fn) {
    const start = Date.now();
    try {
      this.metrics.requests++;
      return await fn();
    } catch (error) {
      this.metrics.errors++;
      throw error;
    } finally {
      this.metrics.latency.push(Date.now() - start);
    }
  }
  
  getMetrics() {
    return {
      ...this.metrics,
      averageLatency: this.metrics.latency.reduce((a, b) => a + b, 0) / 
        this.metrics.latency.length
    };
  }
}
```
