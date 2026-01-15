# Troubleshooting Guide

Common issues and solutions for Kundli Calculation Service production deployment.

## Table of Contents
- [Service Issues](#service-issues)
- [Database Issues](#database-issues)
- [API Issues](#api-issues)
- [Performance Issues](#performance-issues)
- [SSL/Certificate Issues](#sslcertificate-issues)
- [Monitoring Issues](#monitoring-issues)
- [Docker Issues](#docker-issues)

---

## Service Issues

### Backend Service Not Starting

**Symptoms:**
- Container exits immediately
- Health checks fail
- API not accessible

**Diagnosis:**
```bash
# Check container status
docker-compose -f docker-compose.prod.yml ps

# View logs
docker-compose -f docker-compose.prod.yml logs backend

# Check container details
docker inspect kundli-backend
```

**Solutions:**

1. **Missing environment variables:**
```bash
# Verify .env.production exists and is complete
cat backend/.env.production

# Check for required variables
grep -E "DATABASE_URL|SECRET_KEY|JWT_SECRET" backend/.env.production
```

2. **Database connection failure:**
```bash
# Test database connection
docker-compose exec postgres pg_isready -U kundli_user -d kundli_prod

# Check database logs
docker-compose logs postgres
```

3. **Port already in use:**
```bash
# Check what's using port 8000
sudo lsof -i :8000

# Stop conflicting service or change port
```

### Frontend Not Accessible

**Symptoms:**
- Frontend shows 502/503 error
- Next.js not responding

**Solutions:**

1. **Backend not ready:**
```bash
# Verify backend is running
curl http://localhost:8000/api/v1/system/health

# Wait for backend, then restart frontend
docker-compose restart frontend
```

2. **Build failure:**
```bash
# Rebuild frontend
docker-compose -f docker-compose.prod.yml build frontend

# Check build logs
docker-compose logs frontend
```

### Nginx Reverse Proxy Issues

**Symptoms:**
- 502 Bad Gateway
- 504 Gateway Timeout

**Solutions:**

1. **Backend not responding:**
```bash
# Test backend directly
curl http://localhost:8000/api/v1/system/health

# Check nginx error logs
docker-compose logs nginx
```

2. **Configuration error:**
```bash
# Test nginx config
docker-compose exec nginx nginx -t

# Reload nginx
docker-compose exec nginx nginx -s reload
```

---

## Database Issues

### PostgreSQL Connection Refused

**Symptoms:**
- `psycopg2.OperationalError: could not connect`
- Backend can't connect to database

**Diagnosis:**
```bash
# Check PostgreSQL status
docker-compose ps postgres

# Test connection
docker-compose exec postgres psql -U kundli_user -d kundli_prod -c "SELECT 1;"
```

**Solutions:**

1. **Database not ready:**
```bash
# Wait for health check
docker-compose exec postgres pg_isready -U kundli_user

# Check startup logs
docker-compose logs postgres --tail=50
```

2. **Wrong credentials:**
```bash
# Verify DATABASE_URL in .env.production
grep DATABASE_URL backend/.env.production

# Match with docker-compose.prod.yml POSTGRES_PASSWORD
```

### Database Migration Failures

**Symptoms:**
- Alembic migration errors
- Schema inconsistencies

**Solutions:**

1. **Check migration status:**
```bash
# View current version
docker-compose exec backend alembic current

# View migration history
docker-compose exec backend alembic history
```

2. **Manual migration:**
```bash
# Apply migrations step by step
docker-compose exec backend alembic upgrade +1

# Or force to specific revision
docker-compose exec backend alembic upgrade <revision>
```

3. **Migration conflict:**
```bash
# Stamp database with current version
docker-compose exec backend alembic stamp head

# Create new migration
docker-compose exec backend alembic revision -m "fix conflicts"
```

### Slow Database Queries

**Symptoms:**
- High response times
- Database CPU at 100%

**Diagnosis:**
```bash
# Check active queries
docker-compose exec postgres psql -U kundli_user -d kundli_prod -c "SELECT pid, query, state, query_start FROM pg_stat_activity WHERE state = 'active';"

# Find slow queries
docker-compose exec postgres psql -U kundli_user -d kundli_prod -c "SELECT query, mean_exec_time FROM pg_stat_statements ORDER BY mean_exec_time DESC LIMIT 10;"
```

**Solutions:**

1. **Add indexes:**
```sql
-- Connect to database
docker-compose exec postgres psql -U kundli_user -d kundli_prod

-- Create index on frequently queried column
CREATE INDEX CONCURRENTLY idx_column_name ON table_name(column_name);
```

2. **Vacuum database:**
```bash
# Vacuum all tables
docker-compose exec postgres vacuumdb -U kundli_user -d kundli_prod -z -v
```

---

## API Issues

### 500 Internal Server Error

**Diagnosis:**
```bash
# Check backend logs
docker-compose logs backend --tail=100 | grep ERROR

# Test specific endpoint
curl -v http://localhost:8000/api/v1/charts/calculate
```

**Solutions:**

1. **Check application logs:**
```bash
# Follow logs in real-time
docker-compose logs -f backend

# Search for stack traces
docker-compose logs backend | grep -A 20 "Traceback"
```

2. **Verify Swiss Ephemeris files:**
```bash
# Check ephemeris directory
ls -la backend/ephemeris/

# Should contain .se1 files
# If missing, download from https://www.astro.com/ftp/swisseph/
```

### Rate Limiting Triggering

**Symptoms:**
- 429 Too Many Requests
- Users blocked unexpectedly

**Solutions:**

1. **Adjust rate limits:**
```bash
# Edit backend/.env.production
RATE_LIMIT_PER_MINUTE=100
RATE_LIMIT_PER_HOUR=2000

# Restart backend
docker-compose restart backend
```

2. **Check Redis:**
```bash
# Verify Redis is working
docker-compose exec redis redis-cli PING

# Clear rate limit data (use with caution)
docker-compose exec redis redis-cli FLUSHDB
```

### JWT Authentication Failures

**Symptoms:**
- `401 Unauthorized`
- `Invalid token` errors

**Solutions:**

1. **Token expired:**
```bash
# Increase token expiry
# Edit backend/.env.production
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

2. **Secret key mismatch:**
```bash
# Verify JWT_SECRET hasn't changed
grep JWT_SECRET backend/.env.production

# If changed, users must re-authenticate
```

---

## Performance Issues

### High Response Times

**Diagnosis:**
```bash
# Check Prometheus metrics
curl http://localhost:9090/api/v1/query?query=http_request_duration_seconds

# View slow endpoints in logs
docker-compose logs backend | grep "duration="
```

**Solutions:**

1. **Enable caching:**
```bash
# Verify Redis is working
docker-compose exec redis redis-cli INFO stats

# Check cache hit rate
docker-compose exec redis redis-cli INFO stats | grep keyspace_hits
```

2. **Optimize calculations:**
```python
# Add caching decorator to expensive functions
from functools import lru_cache

@lru_cache(maxsize=1000)
def expensive_calculation(params):
    # ...
```

### Memory Leaks

**Symptoms:**
- Container memory grows continuously
- OOM (Out of Memory) kills

**Diagnosis:**
```bash
# Monitor memory usage
docker stats

# Check container limits
docker inspect kundli-backend | grep -A 5 Memory
```

**Solutions:**

1. **Set memory limits:**
```yaml
# docker-compose.prod.yml
backend:
  mem_limit: 2g
  mem_reservation: 1g
```

2. **Profile application:**
```bash
# Install memory profiler
pip install memory_profiler

# Add profiling to suspect functions
@profile
def suspect_function():
    # ...
```

### High CPU Usage

**Diagnosis:**
```bash
# Check CPU usage
docker stats --no-stream

# Find CPU-intensive processes
docker-compose exec backend top -b -n 1
```

**Solutions:**

1. **Optimize calculations:**
- Use vectorized operations (numpy)
- Cache repeated calculations
- Offload to background workers

2. **Scale horizontally:**
```yaml
# docker-compose.prod.yml
backend:
  deploy:
    replicas: 3
```

---

## SSL/Certificate Issues

### Certificate Expired

**Symptoms:**
- `SSL certificate problem: certificate has expired`
- Browser shows security warning

**Solutions:**

1. **Renew certificate:**
```bash
# Manual renewal
sudo certbot renew

# Force renewal
sudo certbot renew --force-renewal
```

2. **Verify auto-renewal:**
```bash
# Test renewal
sudo certbot renew --dry-run

# Check renewal timer
sudo systemctl status certbot.timer
```

### Mixed Content Warnings

**Symptoms:**
- Browser console shows mixed content errors
- Some resources load over HTTP

**Solutions:**

1. **Force HTTPS:**
```nginx
# nginx/nginx.prod.conf
add_header Content-Security-Policy "upgrade-insecure-requests";
```

2. **Update API URLs:**
```bash
# Verify all URLs use HTTPS
grep -r "http://" frontend/

# Update to https://
```

---

## Monitoring Issues

### Prometheus Not Collecting Metrics

**Diagnosis:**
```bash
# Check Prometheus targets
curl http://localhost:9090/api/v1/targets | jq '.data.activeTargets[] | {job, health}'

# View Prometheus logs
docker-compose logs prometheus
```

**Solutions:**

1. **Backend metrics endpoint not accessible:**
```bash
# Test metrics endpoint
curl http://localhost:8000/api/v1/metrics

# If 404, verify metrics are enabled
grep ENABLE_METRICS backend/.env.production
```

2. **Scrape config incorrect:**
```yaml
# monitoring/prometheus/prometheus.yml
scrape_configs:
  - job_name: 'backend'
    metrics_path: '/api/v1/metrics'
    static_configs:
      - targets: ['backend:8000']  # Use container name
```

### Grafana Dashboard Not Loading

**Solutions:**

1. **Datasource connection failed:**
```bash
# Test Prometheus from Grafana container
docker-compose exec grafana wget -O- http://prometheus:9090/api/v1/query?query=up
```

2. **Re-provision datasources:**
```bash
# Restart Grafana
docker-compose restart grafana

# Check provisioning logs
docker-compose logs grafana | grep provisioning
```

---

## Docker Issues

### Disk Space Full

**Symptoms:**
- `no space left on device`
- Containers failing to start

**Solutions:**

1. **Clean Docker resources:**
```bash
# Remove unused images
docker image prune -a

# Remove unused volumes
docker volume prune

# Clean everything (use with caution)
docker system prune -a --volumes
```

2. **Check disk usage:**
```bash
# Docker disk usage
docker system df

# System disk usage
df -h
```

### Port Conflicts

**Symptoms:**
- `port is already allocated`
- Container fails to start

**Solutions:**

1. **Find conflicting process:**
```bash
# Check what's using the port
sudo lsof -i :8000

# Kill process
sudo kill -9 <PID>
```

2. **Change port mapping:**
```yaml
# docker-compose.prod.yml
backend:
  ports:
    - "8001:8000"  # Change external port
```

### Container Restart Loops

**Diagnosis:**
```bash
# Check restart count
docker-compose ps

# View exit code
docker inspect kundli-backend | grep -A 3 State
```

**Solutions:**

1. **Health check too aggressive:**
```yaml
# docker-compose.prod.yml
healthcheck:
  interval: 60s  # Increase interval
  start_period: 30s  # Give more startup time
```

2. **Fix application error:**
```bash
# Check why container exits
docker-compose logs backend --tail=50

# Run container interactively for debugging
docker-compose run --rm backend bash
```

---

## Getting Help

### Collect Diagnostic Information

```bash
# Create diagnostics bundle
cat > collect-diagnostics.sh << 'EOF'
#!/bin/bash
mkdir -p diagnostics
docker-compose -f docker-compose.prod.yml ps > diagnostics/containers.txt
docker-compose -f docker-compose.prod.yml logs --tail=500 > diagnostics/logs.txt
docker system df > diagnostics/docker-df.txt
df -h > diagnostics/disk.txt
free -h > diagnostics/memory.txt
curl -s http://localhost:8000/api/v1/system/health > diagnostics/health.json
tar -czf diagnostics-$(date +%Y%m%d-%H%M%S).tar.gz diagnostics/
rm -rf diagnostics/
EOF

chmod +x collect-diagnostics.sh
./collect-diagnostics.sh
```

### Support Channels

- GitHub Issues: Report bugs and feature requests
- Documentation: Check latest docs for updates
- Community Forum: Ask questions and share solutions

### Emergency Rollback

```bash
# Quick rollback procedure
./scripts/emergency-rollback.sh

# Or manually:
docker-compose -f docker-compose.prod.yml down
git checkout <previous-stable-tag>
docker-compose -f docker-compose.prod.yml up -d
```
