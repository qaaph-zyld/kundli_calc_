# Kundli Calculation Service - Configuration Guide

## Overview
This guide details all configuration options available in the Kundli Calculation Service, including environment variables, configuration files, and runtime settings.

## Table of Contents
1. [Environment Variables](#environment-variables)
2. [Configuration Files](#configuration-files)
3. [Security Settings](#security-settings)
4. [Performance Tuning](#performance-tuning)
5. [Integration Settings](#integration-settings)
6. [Logging Configuration](#logging-configuration)
7. [Monitoring Setup](#monitoring-setup)

## Environment Variables

### Core Settings
```bash
# API Configuration
API_VERSION=v1
API_PREFIX=/api/v1
DEBUG_MODE=false
ENVIRONMENT=production  # production, staging, development

# Server Settings
HOST=0.0.0.0
PORT=8000
WORKERS=4
```

### Security Settings
```bash
# JWT Configuration
JWT_SECRET=your-secret-key
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=60
JWT_REFRESH_TOKEN_EXPIRE_DAYS=7

# CORS Settings
CORS_ORIGINS=["https://app1.com", "https://app2.com"]
CORS_METHODS=["GET", "POST", "PUT", "DELETE"]
CORS_HEADERS=["*"]

# Rate Limiting
RATE_LIMIT_PER_MINUTE=100
RATE_LIMIT_BURST=200
```

### Database Settings
```bash
# MongoDB Configuration
MONGODB_URI=mongodb://localhost:27017/kundli
MONGODB_MAX_POOL_SIZE=100
MONGODB_MIN_POOL_SIZE=10
MONGODB_MAX_IDLE_TIME_MS=10000

# Redis Configuration
REDIS_URI=redis://localhost:6379/0
REDIS_MAX_CONNECTIONS=100
REDIS_TIMEOUT=5
```

### Calculation Settings
```bash
# Astrological Settings
DEFAULT_AYANAMSA=Lahiri
DEFAULT_HOUSE_SYSTEM=Placidus
CALCULATION_PRECISION=2  # decimal places

# Optimization
CACHE_TTL=3600  # seconds
MAX_CONCURRENT_CALCULATIONS=100
CALCULATION_TIMEOUT=30  # seconds
```

## Configuration Files

### 1. Main Configuration (config.yaml)
```yaml
api:
  version: v1
  prefix: /api/v1
  debug: false
  environment: production

server:
  host: 0.0.0.0
  port: 8000
  workers: 4
  keepalive: 65

security:
  jwt:
    secret: your-secret-key
    algorithm: HS256
    access_token_expire_minutes: 60
    refresh_token_expire_days: 7
  
  cors:
    origins:
      - https://app1.com
      - https://app2.com
    methods:
      - GET
      - POST
      - PUT
      - DELETE
    headers:
      - "*"
  
  rate_limit:
    per_minute: 100
    burst: 200

database:
  mongodb:
    uri: mongodb://localhost:27017/kundli
    max_pool_size: 100
    min_pool_size: 10
    max_idle_time_ms: 10000
  
  redis:
    uri: redis://localhost:6379/0
    max_connections: 100
    timeout: 5

calculation:
  ayanamsa: Lahiri
  house_system: Placidus
  precision: 2
  cache_ttl: 3600
  max_concurrent: 100
  timeout: 30
```

### 2. Logging Configuration (logging.yaml)
```yaml
version: 1
disable_existing_loggers: false

formatters:
  standard:
    format: "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
  json:
    class: pythonjsonlogger.jsonlogger.JsonFormatter
    format: "%(asctime)s %(name)s %(levelname)s %(message)s"

handlers:
  console:
    class: logging.StreamHandler
    formatter: standard
    stream: ext://sys.stdout
  
  file:
    class: logging.handlers.RotatingFileHandler
    formatter: json
    filename: logs/kundli-service.log
    maxBytes: 10485760  # 10MB
    backupCount: 5

loggers:
  kundli_service:
    level: INFO
    handlers: [console, file]
    propagate: false

root:
  level: INFO
  handlers: [console]
```

### 3. Metrics Configuration (metrics.yaml)
```yaml
metrics:
  enabled: true
  host: 0.0.0.0
  port: 9090
  path: /metrics
  
  collectors:
    - type: counter
      name: api_requests_total
      description: Total API requests
      labels:
        - endpoint
        - method
        - status
    
    - type: histogram
      name: api_request_duration_seconds
      description: API request duration
      labels:
        - endpoint
      buckets: [0.1, 0.5, 1.0, 2.0, 5.0]
    
    - type: gauge
      name: active_calculations
      description: Number of active calculations
```

## Security Settings

### 1. Authentication Configuration
```yaml
authentication:
  providers:
    - type: jwt
      enabled: true
      settings:
        secret: your-secret-key
        algorithm: HS256
    
    - type: api_key
      enabled: true
      settings:
        header_name: X-API-Key
        prefix: Bearer
    
  session:
    enabled: false
```

### 2. Authorization Configuration
```yaml
authorization:
  roles:
    - name: admin
      permissions:
        - all
    
    - name: user
      permissions:
        - calculate.basic
        - calculate.advanced
        - view.own
    
    - name: guest
      permissions:
        - calculate.basic
```

## Performance Tuning

### 1. Cache Settings
```yaml
cache:
  backend: redis
  default_ttl: 3600
  
  patterns:
    kundli:
      ttl: 86400  # 24 hours
      max_size: 50000  # bytes
    
    transit:
      ttl: 1800  # 30 minutes
      max_size: 10000  # bytes
```

### 2. Database Optimization
```yaml
database:
  mongodb:
    read_preference: primaryPreferred
    write_concern:
      w: 1
      j: true
    
    indexes:
      - collection: kundlis
        fields:
          - name: user_id
            type: 1
          - name: created_at
            type: -1
    
    query_cache:
      enabled: true
      ttl: 300  # seconds
```

## Integration Settings

### 1. API Integration
```yaml
integrations:
  ephemeris:
    type: swiss_ephemeris
    path: /path/to/ephe
    settings:
      precision: high
  
  timezone:
    type: timezonefinder
    settings:
      in_memory: true
```

### 2. Notification Settings
```yaml
notifications:
  email:
    enabled: true
    provider: smtp
    settings:
      host: smtp.example.com
      port: 587
      username: user
      password: pass
  
  webhooks:
    enabled: true
    endpoints:
      - url: https://webhook1.example.com
        events: [calculation.complete]
      - url: https://webhook2.example.com
        events: [calculation.error]
```

## Logging Configuration

### 1. Log Levels
```yaml
logging:
  root_level: INFO
  
  loggers:
    api:
      level: INFO
      handlers: [console, file]
    
    calculation:
      level: DEBUG
      handlers: [file]
    
    security:
      level: WARNING
      handlers: [file, security_file]
```

### 2. Log Rotation
```yaml
log_rotation:
  max_size: 10485760  # 10MB
  backup_count: 5
  compression: true
  compression_method: gz
```

## Monitoring Setup

### 1. Health Checks
```yaml
health_checks:
  enabled: true
  path: /health
  
  checks:
    - name: database
      timeout: 5
    - name: redis
      timeout: 2
    - name: calculation_service
      timeout: 10
```

### 2. Alerting
```yaml
alerting:
  providers:
    - type: email
      enabled: true
      recipients: [admin@example.com]
    
    - type: slack
      enabled: true
      webhook_url: https://hooks.slack.com/services/xxx
  
  rules:
    - name: high_error_rate
      condition: "error_rate > 0.01"
      duration: 5m
      severity: critical
```
