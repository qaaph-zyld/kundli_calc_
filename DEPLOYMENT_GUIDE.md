# Production Deployment Guide

## Prerequisites

### 1. VPS Requirements
- **OS:** Ubuntu 22.04 LTS or similar
- **RAM:** 4GB minimum (8GB recommended)
- **Storage:** 50GB minimum
- **Software:** Docker & Docker Compose installed

### 2. Domain & SSL
- Domain name configured and pointing to your VPS
- SSL certificate (Let's Encrypt recommended)

### 3. Required Secrets
Generate these before deployment:
```bash
# Database password (strong random password)
openssl rand -base64 32

# Secret key for application
openssl rand -hex 32

# JWT secret for authentication
openssl rand -hex 32

# Grafana admin password
openssl rand -base64 16
```

---

## Quick Start Deployment

### Step 1: Clone Repository
```bash
git clone https://github.com/qaaph-zyld/kundli_calc_.git
cd kundli_calc_
```

### Step 2: Configure Environment
```bash
# Copy example environment file
cp backend/.env.production.example backend/.env.production

# Edit with your actual values
nano backend/.env.production
```

**Required changes in `.env.production`:**
- `DATABASE_URL`: Replace `CHANGE_ME` with your database password
- `SECRET_KEY`: Use generated secret from prerequisites
- `JWT_SECRET`: Use generated JWT secret
- `ALLOWED_ORIGINS`: Update with your actual domain

### Step 3: Set Environment Variables
```bash
# Create .env file for docker-compose
cat > .env << EOF
DB_PASSWORD=your_database_password_here
SECRET_KEY=your_secret_key_here
JWT_SECRET=your_jwt_secret_here
GRAFANA_PASSWORD=your_grafana_password_here
ALLOWED_ORIGINS=https://yourdomain.com
EOF
```

### Step 4: SSL Certificate Setup
```bash
# Using Let's Encrypt (recommended)
sudo apt-get install certbot
sudo certbot certonly --standalone -d yourdomain.com -d www.yourdomain.com

# Copy certificates to nginx directory
sudo cp /etc/letsencrypt/live/yourdomain.com/fullchain.pem nginx/ssl/kundli-app.crt
sudo cp /etc/letsencrypt/live/yourdomain.com/privkey.pem nginx/ssl/kundli-app.key
```

### Step 5: Deploy Services
```bash
# Build and start all services
docker-compose -f docker-compose.prod.yml up -d --build

# Check service status
docker-compose -f docker-compose.prod.yml ps
```

### Step 6: Initialize Database
```bash
# Run database migrations
docker-compose -f docker-compose.prod.yml exec backend alembic upgrade head

# Verify database
docker-compose -f docker-compose.prod.yml exec postgres psql -U kundli_user -d kundli_prod -c "\dt"
```

### Step 7: Verify Deployment
```bash
# Check backend health
curl http://localhost:8000/api/v1/system/health

# Expected response:
# {"status":"healthy","timestamp":"...","version":"1.0.0"}

# Check all services
docker-compose -f docker-compose.prod.yml logs -f
```

---

## Access Points

After successful deployment:

- **API Documentation:** https://yourdomain.com/api/v1/docs
- **API ReDoc:** https://yourdomain.com/api/v1/redoc
- **Grafana Dashboard:** http://yourdomain.com:3001
- **Prometheus Metrics:** http://yourdomain.com:9090

---

## Monitoring & Maintenance

### View Logs
```bash
# All services
docker-compose -f docker-compose.prod.yml logs -f

# Specific service
docker-compose -f docker-compose.prod.yml logs -f backend

# Last 100 lines
docker-compose -f docker-compose.prod.yml logs --tail=100 backend
```

### Database Backup
```bash
# Create backup
docker-compose -f docker-compose.prod.yml exec postgres pg_dump -U kundli_user kundli_prod > backup_$(date +%Y%m%d).sql

# Restore backup
docker-compose -f docker-compose.prod.yml exec -T postgres psql -U kundli_user kundli_prod < backup_20260114.sql
```

### Automated Backups
Create cron job for daily backups:
```bash
# Edit crontab
crontab -e

# Add daily backup at 2 AM
0 2 * * * cd /opt/kundli-app && docker-compose -f docker-compose.prod.yml exec -T postgres pg_dump -U kundli_user kundli_prod > /opt/backups/kundli_$(date +\%Y\%m\%d).sql
```

### Update Deployment
```bash
# Pull latest changes
git pull origin master

# Rebuild and restart services
docker-compose -f docker-compose.prod.yml up -d --build

# Run migrations if needed
docker-compose -f docker-compose.prod.yml exec backend alembic upgrade head
```

---

## Rollback Procedure

If deployment fails or issues occur:

```bash
# Stop services
docker-compose -f docker-compose.prod.yml down

# Checkout previous version
git log --oneline  # Find previous commit hash
git checkout <previous-commit-hash>

# Rebuild and restart
docker-compose -f docker-compose.prod.yml up -d --build

# Rollback database if needed
docker-compose -f docker-compose.prod.yml exec backend alembic downgrade -1
```

---

## Performance Tuning

### Backend Workers
Adjust workers based on CPU cores:
```yaml
# In docker-compose.prod.yml
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
# Rule: workers = (2 x CPU cores) + 1
```

### Database Connection Pool
```python
# In backend/app/core/database.py
engine = create_engine(
    DATABASE_URL,
    pool_size=20,  # Adjust based on load
    max_overflow=40,
    pool_pre_ping=True
)
```

### Redis Memory
```yaml
# In docker-compose.prod.yml
redis:
  command: redis-server --maxmemory 256mb --maxmemory-policy allkeys-lru
```

---

## Security Checklist

- [ ] All secrets generated and stored securely
- [ ] SSL certificates installed and auto-renewal configured
- [ ] Firewall configured (allow only 80, 443, 22)
- [ ] Database not exposed to public internet
- [ ] Redis not exposed to public internet
- [ ] Grafana admin password changed from default
- [ ] Rate limiting enabled in Nginx
- [ ] CORS origins restricted to your domain
- [ ] Regular security updates scheduled

---

## Troubleshooting

### Backend won't start
```bash
# Check logs
docker-compose -f docker-compose.prod.yml logs backend

# Common issues:
# - Database not ready: Wait for postgres health check
# - Missing environment variables: Check .env file
# - Port already in use: Change port in docker-compose
```

### Database connection errors
```bash
# Verify postgres is running
docker-compose -f docker-compose.prod.yml ps postgres

# Test connection
docker-compose -f docker-compose.prod.yml exec postgres psql -U kundli_user -d kundli_prod -c "SELECT 1"

# Reset database (WARNING: destroys data)
docker-compose -f docker-compose.prod.yml down -v
docker-compose -f docker-compose.prod.yml up -d
```

### High memory usage
```bash
# Check resource usage
docker stats

# Restart specific service
docker-compose -f docker-compose.prod.yml restart backend

# Clear Redis cache
docker-compose -f docker-compose.prod.yml exec redis redis-cli FLUSHALL
```

---

## CI/CD with GitHub Actions

### Setup GitHub Secrets
In your GitHub repository settings, add:

- `VPS_HOST`: Your VPS IP address
- `VPS_USERNAME`: SSH username (e.g., root or ubuntu)
- `VPS_SSH_KEY`: Private SSH key for authentication
- `DB_PASSWORD`: Database password
- `SECRET_KEY`: Application secret key
- `JWT_SECRET`: JWT secret key
- `GRAFANA_PASSWORD`: Grafana admin password

### Automatic Deployment
Push to master branch triggers automatic deployment:
```bash
git add .
git commit -m "feat: Add new feature"
git push origin master

# GitHub Actions will:
# 1. Run all tests
# 2. Build Docker images
# 3. Push to registry
# 4. Deploy to VPS
# 5. Run migrations
```

---

## Support & Documentation

- **API Documentation:** `/api/v1/docs`
- **GitHub Repository:** https://github.com/qaaph-zyld/kundli_calc_
- **Issue Tracker:** https://github.com/qaaph-zyld/kundli_calc_/issues

---

## Production Checklist

Before going live:

- [ ] All tests passing (23/23)
- [ ] Environment variables configured
- [ ] SSL certificates installed
- [ ] Database initialized and migrated
- [ ] Backups configured
- [ ] Monitoring dashboards accessible
- [ ] Rate limiting tested
- [ ] Load testing completed
- [ ] Documentation reviewed
- [ ] Rollback procedure tested

**System is production-ready when all items checked!**
