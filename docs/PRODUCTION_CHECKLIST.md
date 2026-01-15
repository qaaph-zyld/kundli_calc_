# Production Deployment Checklist

Complete checklist for deploying Kundli Calculation Service to production.

## Pre-Deployment

### Infrastructure Setup
- [ ] VPS provisioned (Ubuntu 22.04 LTS, 4GB RAM, 50GB storage)
- [ ] Domain name registered and DNS configured
- [ ] Firewall configured (ports 80, 443, 22)
- [ ] SSH key-based authentication enabled
- [ ] Non-root sudo user created
- [ ] Fail2ban installed and configured

### Software Installation
- [ ] Docker installed (latest stable)
- [ ] Docker Compose installed (v2.x)
- [ ] Git installed
- [ ] Nginx installed (if not using Docker nginx)
- [ ] Certbot installed for SSL certificates

### Security Configuration
- [ ] Strong passwords generated for all services
- [ ] SSH password authentication disabled
- [ ] UFW/iptables firewall configured
- [ ] Automated security updates enabled
- [ ] Log rotation configured
- [ ] Backup strategy defined

## Environment Configuration

### Backend Environment
- [ ] `backend/.env.production` created
- [ ] Database password generated (strong, 32+ characters)
- [ ] SECRET_KEY generated: `openssl rand -hex 32`
- [ ] JWT_SECRET generated: `openssl rand -hex 32`
- [ ] ALLOWED_ORIGINS updated with production domain
- [ ] ALLOWED_HOSTS updated with production domain
- [ ] Database URL configured correctly
- [ ] Redis URL configured correctly

### Frontend Environment
- [ ] `frontend/next-app/.env.production` created
- [ ] NEXT_PUBLIC_API_URL set to production backend URL
- [ ] NEXT_PUBLIC_APP_URL set to production frontend URL
- [ ] Analytics/monitoring keys configured (if applicable)

### Root Environment
- [ ] `.env.production` created in project root
- [ ] DB_PASSWORD set
- [ ] SECRET_KEY set
- [ ] JWT_SECRET set
- [ ] GRAFANA_PASSWORD set

## SSL/TLS Setup

### Let's Encrypt Certificate
- [ ] Domain DNS A record pointing to VPS IP
- [ ] Certbot run to obtain certificate
- [ ] Certificate auto-renewal configured
- [ ] Certificate files copied to `nginx/ssl/` if needed
- [ ] Nginx configured for HTTPS
- [ ] HTTP to HTTPS redirect enabled

### Certificate Verification
```bash
# Test SSL configuration
openssl s_client -connect yourdomain.com:443 -servername yourdomain.com

# Check certificate expiry
echo | openssl s_client -servername yourdomain.com -connect yourdomain.com:443 2>/dev/null | openssl x509 -noout -dates
```

## GitHub Configuration

### Repository Secrets
- [ ] `VPS_HOST` - Production server IP/hostname
- [ ] `VPS_USERNAME` - SSH username
- [ ] `VPS_SSH_KEY` - Private SSH key for deployment
- [ ] `DB_PASSWORD` - Production database password
- [ ] `SECRET_KEY` - Application secret key
- [ ] `JWT_SECRET` - JWT signing secret
- [ ] `GRAFANA_PASSWORD` - Grafana admin password

### Repository Settings
- [ ] Branch protection enabled for `master`
- [ ] Required status checks configured
- [ ] Required reviews configured
- [ ] Actions enabled
- [ ] Workflow permissions set correctly

## Application Deployment

### Initial Deployment
- [ ] Repository cloned to VPS: `/opt/kundli-app`
- [ ] Environment files created
- [ ] Ephemeris files present in `backend/ephemeris/`
- [ ] Docker images built successfully
- [ ] Database initialized: `docker-compose exec backend alembic upgrade head`
- [ ] Services started: `docker-compose -f docker-compose.prod.yml up -d`
- [ ] Health checks passing

### Service Verification
```bash
# Check all services running
docker-compose -f docker-compose.prod.yml ps

# Verify backend health
curl https://api.yourdomain.com/api/v1/system/health

# Verify frontend accessible
curl https://yourdomain.com

# Check Prometheus metrics
curl http://localhost:9090/-/healthy

# Check Grafana
curl http://localhost:3001/api/health
```

## Database Configuration

### PostgreSQL Setup
- [ ] Database initialized
- [ ] Migrations applied
- [ ] Database backup configured
- [ ] Connection pooling verified
- [ ] Slow query logging enabled

### Redis Setup
- [ ] Redis persistence enabled (AOF)
- [ ] Redis password configured (if needed)
- [ ] Memory limits set appropriately
- [ ] Eviction policy configured

## Monitoring Setup

### Prometheus
- [ ] Prometheus accessible
- [ ] All scrape targets UP
- [ ] Alert rules loaded
- [ ] Alertmanager configured (optional)

### Grafana
- [ ] Grafana accessible
- [ ] Admin password changed from default
- [ ] Datasources configured
- [ ] Dashboards imported
- [ ] Alert notifications configured

### Log Aggregation
- [ ] Loki receiving logs
- [ ] Promtail configured
- [ ] Log retention policy set

## Performance Testing

### Load Testing
- [ ] Load test with 10 concurrent users
- [ ] Load test with 50 concurrent users
- [ ] Load test with 100 concurrent users
- [ ] Response times acceptable (< 2s)
- [ ] Error rate < 1%

### Stress Testing
- [ ] Database connection pool handling verified
- [ ] Redis caching working correctly
- [ ] Rate limiting functioning
- [ ] Memory usage stable under load

## Backup & Recovery

### Automated Backups
- [ ] Database backup script configured
- [ ] Backup schedule set (daily recommended)
- [ ] Backup retention policy defined
- [ ] Backup storage location configured
- [ ] Backup restoration tested

### Disaster Recovery Plan
- [ ] Recovery procedure documented
- [ ] Recovery time objective (RTO) defined
- [ ] Recovery point objective (RPO) defined
- [ ] Restoration tested successfully

## Documentation

### User Documentation
- [ ] API documentation accessible at `/docs`
- [ ] User guide available
- [ ] Authentication flow documented
- [ ] Rate limiting explained

### Operations Documentation
- [ ] Deployment guide complete
- [ ] Monitoring guide available
- [ ] Troubleshooting guide created
- [ ] Runbook for common issues

## Post-Deployment

### Immediate Verification (First 24 Hours)
- [ ] All services running
- [ ] No critical errors in logs
- [ ] SSL certificate valid
- [ ] Monitoring dashboards accessible
- [ ] Alerts configured and working
- [ ] Backup successful

### Week 1 Checks
- [ ] Performance metrics reviewed
- [ ] Error rates within acceptable range
- [ ] Resource usage (CPU, memory, disk) acceptable
- [ ] Database performance acceptable
- [ ] No security incidents
- [ ] User feedback collected

### Ongoing Maintenance
- [ ] Daily health check automated
- [ ] Weekly security updates
- [ ] Monthly performance review
- [ ] Quarterly disaster recovery drill
- [ ] Regular dependency updates

## Rollback Plan

### Rollback Procedure
- [ ] Previous Docker images tagged
- [ ] Database backup before deployment
- [ ] Rollback script tested
- [ ] Rollback trigger conditions defined

### Rollback Commands
```bash
# Stop current deployment
docker-compose -f docker-compose.prod.yml down

# Checkout previous version
git checkout <previous-tag>

# Restore database (if needed)
./scripts/restore.sh <backup-file>

# Restart services
docker-compose -f docker-compose.prod.yml up -d
```

## Compliance & Legal

### Data Protection
- [ ] GDPR compliance verified (if applicable)
- [ ] Privacy policy published
- [ ] Terms of service published
- [ ] Data retention policy defined
- [ ] User data deletion process defined

### Security
- [ ] Penetration testing completed
- [ ] Security audit performed
- [ ] Vulnerability scanning automated
- [ ] Incident response plan documented

## Sign-Off

### Deployment Team
- [ ] Development lead approval
- [ ] DevOps engineer approval
- [ ] Security team approval
- [ ] Product owner approval

### Production Readiness Score
Calculate score by counting completed items:
- 90-100%: Ready for production ✅
- 80-89%: Minor issues, deploy with caution ⚠️
- Below 80%: Not ready, address critical items ❌

---

**Date:** _________________

**Deployed by:** _________________

**Version:** _________________

**Notes:** _________________
