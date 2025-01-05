# Technical Documentation

## System Architecture

### Overview
The Kundli Calculation Service is built on a microservices architecture, utilizing FastAPI for the backend, Redis for caching, and MongoDB for persistent storage.

```mermaid
graph TD
    Client[Client] --> LB[Load Balancer]
    LB --> API[API Gateway]
    API --> Auth[Auth Service]
    API --> Calc[Calculation Service]
    API --> Data[Data Service]
    Auth --> Cache[(Redis Cache)]
    Auth --> DB[(MongoDB)]
    Calc --> Cache
    Calc --> DB
    Data --> Cache
    Data --> DB
```

### Components

1. **API Gateway**
   - FastAPI application
   - JWT authentication
   - Rate limiting
   - Request validation
   - Response caching

2. **Authentication Service**
   - User management
   - Token generation
   - Permission control
   - Role management

3. **Calculation Service**
   - Swiss Ephemeris integration
   - Planetary calculations
   - Chart generation
   - Pattern analysis

4. **Data Service**
   - Data persistence
   - Query optimization
   - Data validation
   - Cache management

## Deployment Guide

### Prerequisites
1. Docker and Docker Compose
2. Kubernetes cluster
3. MongoDB (4.4+)
4. Redis (6.0+)
5. Python (3.9+)

### Environment Setup

1. **Clone Repository**
```bash
git clone https://github.com/org/kundli-service.git
cd kundli-service
```

2. **Configure Environment Variables**
```bash
cp .env.example .env
# Edit .env with your settings
```

3. **Build Docker Images**
```bash
docker-compose build
```

4. **Deploy Services**
```bash
docker-compose up -d
```

### Kubernetes Deployment

1. **Apply Configurations**
```bash
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/secrets.yaml
```

2. **Deploy Services**
```bash
kubectl apply -f k8s/services/
```

3. **Verify Deployment**
```bash
kubectl get pods -n kundli-service
kubectl get services -n kundli-service
```

## Maintenance Procedures

### Database Maintenance

1. **Backup Procedure**
```bash
#!/bin/bash
DATE=$(date +%Y%m%d)
mongodump --uri="mongodb://user:pass@host:port" --out="/backup/$DATE"
aws s3 cp /backup/$DATE s3://bucket/backups/$DATE --recursive
```

2. **Restore Procedure**
```bash
#!/bin/bash
BACKUP_DATE=$1
aws s3 cp s3://bucket/backups/$BACKUP_DATE /restore/$BACKUP_DATE --recursive
mongorestore --uri="mongodb://user:pass@host:port" /restore/$BACKUP_DATE
```

### Cache Management

1. **Clear Cache**
```python
async def clear_cache():
    redis = await get_redis()
    await redis.flushdb()
```

2. **Refresh Cache**
```python
async def refresh_cache(pattern: str):
    redis = await get_redis()
    keys = await redis.keys(pattern)
    for key in keys:
        await refresh_key(key)
```

## Monitoring and Alerts

### Metrics Collection

1. **System Metrics**
```yaml
metrics:
  - name: api_request_duration_seconds
    type: Histogram
    labels: [endpoint, method, status]
  
  - name: calculation_duration_seconds
    type: Histogram
    labels: [calculation_type]
  
  - name: cache_hit_ratio
    type: Gauge
    labels: [cache_type]
```

2. **Business Metrics**
```yaml
metrics:
  - name: calculations_total
    type: Counter
    labels: [type, user_tier]
  
  - name: active_users
    type: Gauge
    labels: [tier]
```

### Alert Configuration

1. **High Error Rate**
```yaml
alerts:
  - name: HighErrorRate
    condition: error_rate > 0.01
    duration: 5m
    severity: critical
    channels: [slack, email]
```

2. **Service Degradation**
```yaml
alerts:
  - name: ServiceDegradation
    condition: latency_p95 > 2000ms
    duration: 10m
    severity: warning
    channels: [slack]
```

## Backup and Recovery

### Backup Strategy

1. **Database Backups**
   - Full backup: Daily
   - Incremental backup: Hourly
   - Retention: 30 days

2. **Configuration Backups**
   - Git repository
   - Environment variables
   - Kubernetes configs

### Recovery Procedures

1. **Service Recovery**
```bash
# Roll back deployment
kubectl rollout undo deployment/kundli-service -n kundli-service

# Verify status
kubectl rollout status deployment/kundli-service -n kundli-service
```

2. **Data Recovery**
```bash
# Restore from backup
./scripts/restore.sh --date 2025-01-05 --env production

# Verify data integrity
./scripts/verify_data.sh
```

## Incident Response

### Response Procedures

1. **Service Outage**
```yaml
steps:
  - Check monitoring dashboards
  - Identify affected components
  - Execute relevant playbook
  - Notify stakeholders
  - Post-mortem analysis
```

2. **Security Incident**
```yaml
steps:
  - Isolate affected systems
  - Collect forensic data
  - Execute containment procedures
  - Investigate root cause
  - Implement fixes
```

### Playbooks

1. **High Latency**
```yaml
actions:
  - Check system resources
  - Analyze slow queries
  - Scale affected services
  - Clear unnecessary caches
  - Optimize database queries
```

2. **Data Corruption**
```yaml
actions:
  - Stop write operations
  - Identify corruption scope
  - Restore from backup
  - Verify data integrity
  - Resume operations
```

## Performance Optimization

### Database Optimization

1. **Indexes**
```javascript
// MongoDB indexes
db.kundlis.createIndex({ "user_id": 1 });
db.kundlis.createIndex({ "created_at": -1 });
db.calculations.createIndex({ "date": 1, "time": 1 });
```

2. **Query Optimization**
```python
# Use projection
db.kundlis.find(
    {"user_id": user_id},
    {"planets": 1, "houses": 1}
)

# Use aggregation pipeline
db.calculations.aggregate([
    {"$match": {"user_id": user_id}},
    {"$sort": {"created_at": -1}},
    {"$limit": 10}
])
```

### Cache Optimization

1. **Cache Policies**
```python
CACHE_POLICIES = {
    "kundli": {
        "ttl": 3600,  # 1 hour
        "max_size": 1000
    },
    "calculations": {
        "ttl": 1800,  # 30 minutes
        "max_size": 500
    }
}
```

2. **Cache Implementation**
```python
async def get_cached_kundli(kundli_id: str):
    cache_key = f"kundli:{kundli_id}"
    
    # Try cache first
    cached = await redis.get(cache_key)
    if cached:
        return json.loads(cached)
    
    # Calculate and cache
    kundli = await calculate_kundli(kundli_id)
    await redis.setex(
        cache_key,
        CACHE_POLICIES["kundli"]["ttl"],
        json.dumps(kundli)
    )
    
    return kundli
```

## Security Measures

### Authentication

1. **JWT Configuration**
```python
JWT_SETTINGS = {
    "algorithm": "HS256",
    "access_token_expire_minutes": 60,
    "refresh_token_expire_days": 7
}
```

2. **Rate Limiting**
```python
RATE_LIMITS = {
    "basic": 100,    # requests per minute
    "premium": 1000, # requests per minute
    "enterprise": 5000 # requests per minute
}
```

### API Security

1. **Security Headers**
```python
SECURITY_HEADERS = {
    "X-Frame-Options": "DENY",
    "X-Content-Type-Options": "nosniff",
    "X-XSS-Protection": "1; mode=block",
    "Content-Security-Policy": "default-src 'self'"
}
```

2. **Input Validation**
```python
from pydantic import BaseModel, validator

class KundliInput(BaseModel):
    date: str
    time: str
    latitude: float
    longitude: float
    timezone: str
    
    @validator("latitude")
    def validate_latitude(cls, v):
        if not -90 <= v <= 90:
            raise ValueError("Invalid latitude")
        return v
```
