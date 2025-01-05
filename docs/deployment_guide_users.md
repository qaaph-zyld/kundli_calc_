# Kundli Calculation Service - Deployment Guide for Users

## Overview
This guide helps you deploy and integrate the Kundli Calculation Service into your application. Whether you're using our service via API calls or deploying a local instance, this guide provides step-by-step instructions.

## Table of Contents
1. [Cloud API Integration](#cloud-api-integration)
2. [Local Deployment](#local-deployment)
3. [Docker Deployment](#docker-deployment)
4. [Kubernetes Deployment](#kubernetes-deployment)
5. [Configuration](#configuration)
6. [Monitoring](#monitoring)
7. [Troubleshooting](#troubleshooting)

## Cloud API Integration

### 1. API Key Setup
1. Register at https://kundli-service.com/register
2. Navigate to API Keys section
3. Generate a new API key
4. Store the API key securely

### 2. Authentication Setup
```javascript
// Example using fetch API
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
```

### 3. Making API Calls
```javascript
// Example API call
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
    longitude: 77.2090
  })
});
```

## Local Deployment

### 1. Prerequisites
- Python 3.9+
- MongoDB 4.4+
- Redis 6.0+
- Swiss Ephemeris files

### 2. Installation Steps
```bash
# Clone repository
git clone https://github.com/your-org/kundli-service.git
cd kundli-service

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Setup environment variables
cp .env.example .env
# Edit .env with your settings

# Initialize database
python scripts/init_db.py

# Start service
python main.py
```

## Docker Deployment

### 1. Using Docker Compose
```yaml
# docker-compose.yml
version: '3.8'
services:
  kundli-service:
    image: kundli-service:latest
    ports:
      - "8000:8000"
    environment:
      - MONGODB_URI=mongodb://mongodb:27017/kundli
      - REDIS_URI=redis://redis:6379/0
    depends_on:
      - mongodb
      - redis

  mongodb:
    image: mongo:4.4
    volumes:
      - mongodb_data:/data/db

  redis:
    image: redis:6.0
    volumes:
      - redis_data:/data

volumes:
  mongodb_data:
  redis_data:
```

### 2. Deployment Commands
```bash
# Build and start services
docker-compose up -d

# Check logs
docker-compose logs -f

# Stop services
docker-compose down
```

## Kubernetes Deployment

### 1. Prerequisites
- Kubernetes cluster
- kubectl configured
- Helm (optional)

### 2. Deployment Steps
```bash
# Apply configurations
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/secrets.yaml

# Deploy services
kubectl apply -f k8s/mongodb/
kubectl apply -f k8s/redis/
kubectl apply -f k8s/kundli-service/

# Verify deployment
kubectl get pods -n kundli-service
kubectl get services -n kundli-service
```

## Configuration

### 1. Environment Variables
```bash
# API Configuration
API_VERSION=v1
API_PREFIX=/api/v1
DEBUG_MODE=false

# Security
JWT_SECRET=your-secret-key
JWT_ALGORITHM=HS256
JWT_EXPIRY=3600

# Database
MONGODB_URI=mongodb://localhost:27017/kundli
REDIS_URI=redis://localhost:6379/0

# Calculation Settings
AYANAMSA=Lahiri
HOUSE_SYSTEM=Placidus
```

### 2. Application Settings
```yaml
# config.yaml
calculation:
  precision: high
  cache_ttl: 3600
  max_concurrent: 100

security:
  rate_limit: 100
  allowed_origins:
    - https://your-domain.com
```

## Monitoring

### 1. Health Checks
```bash
# Check service health
curl http://localhost:8000/health

# Check dependencies
curl http://localhost:8000/health/dependencies
```

### 2. Metrics
```bash
# Prometheus metrics
curl http://localhost:8000/metrics

# Custom metrics
curl http://localhost:8000/metrics/custom
```

### 3. Logging
```bash
# View logs
tail -f logs/kundli-service.log

# Docker logs
docker-compose logs -f kundli-service
```

## Troubleshooting

### 1. Common Issues

#### Connection Issues
```bash
# Check MongoDB connection
mongosh mongodb://localhost:27017/kundli

# Check Redis connection
redis-cli ping
```

#### Performance Issues
1. Check system resources
2. Monitor API response times
3. Review cache hit rates
4. Analyze database queries

### 2. Debug Mode
```bash
# Enable debug mode
export DEBUG_MODE=true
python main.py

# Check debug logs
tail -f logs/debug.log
```

### 3. Support
- Email: support@kundli-service.com
- Documentation: https://docs.kundli-service.com
- Community Forum: https://community.kundli-service.com
