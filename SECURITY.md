# Security Guidelines

## Environment Variables and Secrets

### Critical: Never Commit Secrets

The following files contain sensitive information and must **NEVER** be committed to version control:
- `.env`
- `.env.production`
- `.env.staging`
- Any `.env.*.local` files

### Production Deployment Checklist

Before deploying to production:

1. **Generate Strong Secrets**
   ```bash
   # Generate a secure SECRET_KEY (min 32 characters)
   python -c "import secrets; print(secrets.token_urlsafe(32))"
   
   # Generate secure database password
   openssl rand -base64 32
   ```

2. **Create `.env` file from template**
   ```bash
   cp .env.production.example .env
   # Then edit .env with your actual secrets
   ```

3. **Required Environment Variables**
   - `SECRET_KEY` - Application secret key (min 32 chars)
   - `POSTGRES_PASSWORD` - Database password
   - `GRAFANA_ADMIN_PASSWORD` - Monitoring dashboard password

4. **Optional but Recommended**
   - `SENTRY_DSN` - Error tracking
   - `ALLOWED_ORIGINS` - CORS whitelist for your domain

### Docker Compose Security

The `docker-compose.yml` file is configured to read secrets from environment variables:

```yaml
environment:
  - SECRET_KEY=${SECRET_KEY}          # Required
  - POSTGRES_PASSWORD=${POSTGRES_PASSWORD}  # Required
  - GRAFANA_ADMIN_PASSWORD=${GRAFANA_ADMIN_PASSWORD:-admin}  # Change default
```

### Default Credentials to Change

**Immediately change these default passwords in production:**

| Service | Default User | Default Password | Environment Variable |
|---------|-------------|------------------|---------------------|
| PostgreSQL | postgres | (from env) | `POSTGRES_PASSWORD` |
| Grafana | admin | admin | `GRAFANA_ADMIN_PASSWORD` |

### Rate Limiting

Enable rate limiting in production:
```env
RATE_LIMIT_ENABLED=true
RATE_LIMIT_PER_MINUTE=60
```

### Reporting Security Issues

If you discover a security vulnerability, please email: [your-email]

Do **NOT** open a public GitHub issue for security vulnerabilities.

### Security Best Practices

1. **Keep Dependencies Updated**
   ```bash
   # Backend
   pip list --outdated
   pip install -U package_name
   
   # Frontend
   npm outdated
   npm update
   ```

2. **Run Security Scans**
   ```bash
   # Python security scan
   pip install safety
   safety check
   
   # Dependency vulnerabilities
   pip install bandit
   bandit -r backend/app
   ```

3. **Use HTTPS in Production**
   - Configure SSL/TLS certificates
   - Use Let's Encrypt for free certificates
   - Redirect HTTP to HTTPS

4. **Database Security**
   - Never use default passwords
   - Use strong passwords (32+ characters)
   - Restrict database access to localhost or VPC
   - Enable database encryption at rest

5. **API Security**
   - Rate limiting enabled
   - JWT tokens with expiration
   - CORS properly configured
   - Input validation on all endpoints

### Incident Response

If credentials are compromised:

1. **Immediately rotate all secrets**
   - Generate new SECRET_KEY
   - Change all database passwords
   - Regenerate JWT tokens (forces re-login)

2. **Review access logs**
   ```bash
   docker-compose logs backend | grep -i "error\|unauthorized"
   ```

3. **Update and redeploy**
   ```bash
   # Update .env with new secrets
   docker-compose down
   docker-compose up -d --build
   ```

### Compliance Notes

- All passwords are environment-based (12-factor app pattern)
- Secrets never stored in source control
- Logging configured to exclude sensitive data
- Database connections use password authentication
- API requires authentication for all non-public endpoints

For more information on securing FastAPI applications:
https://fastapi.tiangolo.com/tutorial/security/
