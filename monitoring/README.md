# Monitoring Stack

Complete monitoring solution for the Kundli Calculation Service using Prometheus, Grafana, Loki, and Promtail.

## Components

### Prometheus
- **Purpose:** Metrics collection and alerting
- **Port:** 9090
- **Config:** `prometheus/prometheus.yml`
- **Alerts:** `prometheus/alert.rules`

### Grafana
- **Purpose:** Metrics visualization and dashboards
- **Port:** 3001
- **Default credentials:** admin / admin (change on first login)
- **Dashboards:** Auto-provisioned from `grafana/dashboards/`
- **Datasources:** Auto-configured from `grafana/datasources/`

### Loki
- **Purpose:** Log aggregation
- **Port:** 3100
- **Config:** `loki/loki-config.yml`

### Promtail
- **Purpose:** Log collection and forwarding to Loki
- **Config:** `promtail/promtail-config.yml`

## Quick Start

### Access Monitoring

```bash
# Prometheus
http://localhost:9090

# Grafana
http://localhost:3001
# Default: admin / admin
```

### View Metrics

1. Open Grafana at http://localhost:3001
2. Navigate to Dashboards → Kundli Dashboard
3. Select time range and refresh interval

### Configure Alerts

Edit `prometheus/alert.rules` to add custom alerts:

```yaml
- alert: CustomAlert
  expr: your_metric > threshold
  for: 5m
  labels:
    severity: warning
  annotations:
    summary: Custom alert description
```

## Available Metrics

### Application Metrics
- `http_requests_total` - Total HTTP requests by endpoint
- `http_request_duration_seconds` - Request duration histogram
- `active_users` - Current active users
- `calculation_duration_seconds` - Kundli calculation time
- `cache_hits_total` - Redis cache hits
- `cache_misses_total` - Redis cache misses

### System Metrics
- `cpu_usage_percent` - CPU utilization
- `memory_usage_bytes` - Memory usage
- `disk_usage_bytes` - Disk usage
- `network_bytes_sent` - Network traffic sent
- `network_bytes_received` - Network traffic received

### Database Metrics
- `postgres_connections` - PostgreSQL active connections
- `postgres_slow_queries` - Slow query count
- `redis_connected_clients` - Redis active connections
- `redis_memory_usage_bytes` - Redis memory usage

## Alert Rules

### Critical Alerts
- **ServiceDown:** Service not responding for 5 minutes
- **HighErrorRate:** Error rate > 5% for 5 minutes
- **DatabaseDown:** PostgreSQL/Redis down for 5 minutes

### Warning Alerts
- **HighResponseTime:** 95th percentile > 2 seconds
- **HighCPUUsage:** CPU > 80% for 5 minutes
- **HighMemoryUsage:** Memory > 85% for 5 minutes
- **HighRateLimiting:** Rate limit violations increasing

## Dashboard Features

### Kundli Dashboard
- **Overview:** System health, request rates, error rates
- **Performance:** Response times, throughput, cache hit ratio
- **Resources:** CPU, memory, disk, network usage
- **Database:** Connection pools, query performance
- **Business Metrics:** Calculations per minute, active users

## Troubleshooting

### Prometheus Not Scraping Metrics

```bash
# Check Prometheus targets
curl http://localhost:9090/api/v1/targets

# Verify backend metrics endpoint
curl http://localhost:8000/api/v1/metrics
```

### Grafana Dashboard Not Loading

```bash
# Check Grafana logs
docker-compose logs grafana

# Verify datasource configuration
docker-compose exec grafana grafana-cli admin reset-admin-password newpassword
```

### Missing Metrics

```bash
# Restart Prometheus to reload config
docker-compose restart prometheus

# Check Prometheus logs
docker-compose logs prometheus
```

## Production Configuration

### Enable External Access

Update `docker-compose.prod.yml` to expose ports:

```yaml
nginx:
  ports:
    - "80:80"
    - "443:443"
```

Add reverse proxy rules in `nginx/nginx.prod.conf`:

```nginx
location /grafana/ {
    proxy_pass http://grafana:3000/;
}

location /prometheus/ {
    proxy_pass http://prometheus:9090/;
}
```

### Configure Alerting

1. Set up Alertmanager (optional)
2. Configure notification channels in Grafana
3. Add webhook receivers for Slack/Email

### Secure Access

1. Enable authentication on Prometheus
2. Use strong Grafana admin password
3. Configure SSL/TLS for all services
4. Restrict network access with firewall rules

## Maintenance

### Backup Grafana Data

```bash
docker-compose exec grafana grafana-cli admin export-dashboard > backup.json
```

### Clear Old Metrics

Prometheus automatically manages retention (default: 15 days).

Configure in `prometheus.yml`:

```yaml
global:
  storage.tsdb.retention.time: 30d
```

### Update Dashboards

1. Edit JSON files in `grafana/dashboards/`
2. Restart Grafana: `docker-compose restart grafana`
3. Dashboards auto-reload on container restart

## Performance Tuning

### Reduce Scrape Frequency

```yaml
# prometheus.yml
global:
  scrape_interval: 30s  # Increase from 15s
```

### Optimize Query Performance

- Use recording rules for frequently queried metrics
- Limit dashboard time ranges
- Use appropriate step intervals

### Scale Prometheus

For high-cardinality metrics:
- Use remote storage (Thanos, Cortex)
- Implement metric federation
- Shard scrape targets

## Support

For issues or questions:
- Check Prometheus docs: https://prometheus.io/docs/
- Check Grafana docs: https://grafana.com/docs/
- Review application logs: `docker-compose logs -f`
