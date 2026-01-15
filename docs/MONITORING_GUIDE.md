# Monitoring Guide

Complete guide for monitoring the Kundli Calculation Service in production using Prometheus and Grafana.

## Overview

The monitoring stack consists of:
- **Prometheus**: Metrics collection and alerting
- **Grafana**: Visualization and dashboards  
- **Loki**: Log aggregation
- **Promtail**: Log shipping

## Quick Access

```bash
# Prometheus
http://localhost:9090

# Grafana
http://localhost:3001
Username: admin
Password: (set in .env.production)

# Alertmanager (if configured)
http://localhost:9093
```

## Key Metrics

### Application Metrics

#### HTTP Request Metrics
```promql
# Total requests per second
rate(http_requests_total[5m])

# Requests by endpoint
sum(rate(http_requests_total[5m])) by (endpoint)

# Error rate percentage
sum(rate(http_requests_total{status=~"5.."}[5m])) / sum(rate(http_requests_total[5m])) * 100

# Average response time
rate(http_request_duration_seconds_sum[5m]) / rate(http_request_duration_seconds_count[5m])

# 95th percentile response time
histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket[5m])) by (le))

# 99th percentile response time
histogram_quantile(0.99, sum(rate(http_request_duration_seconds_bucket[5m])) by (le))
```

#### Kundli Calculation Metrics
```promql
# Calculations per minute
rate(kundli_calculations_total[1m]) * 60

# Average calculation time
rate(calculation_duration_seconds_sum[5m]) / rate(calculation_duration_seconds_count[5m])

# Failed calculations
rate(calculation_errors_total[5m])

# Calculations by chart type
sum(rate(kundli_calculations_total[5m])) by (chart_type)
```

#### Cache Metrics
```promql
# Cache hit rate
rate(cache_hits_total[5m]) / (rate(cache_hits_total[5m]) + rate(cache_misses_total[5m])) * 100

# Cache size
redis_memory_used_bytes

# Cache evictions
rate(redis_evicted_keys_total[5m])
```

### System Metrics

#### CPU Usage
```promql
# Overall CPU usage
100 - (avg by(instance) (rate(node_cpu_seconds_total{mode="idle"}[5m])) * 100)

# Per-container CPU
rate(container_cpu_usage_seconds_total[5m]) * 100
```

#### Memory Usage
```promql
# Memory usage percentage
(node_memory_MemTotal_bytes - node_memory_MemAvailable_bytes) / node_memory_MemTotal_bytes * 100

# Container memory usage
container_memory_usage_bytes

# Container memory limit
container_spec_memory_limit_bytes
```

#### Disk Usage
```promql
# Disk space used
(node_filesystem_size_bytes - node_filesystem_avail_bytes) / node_filesystem_size_bytes * 100

# Disk I/O
rate(node_disk_read_bytes_total[5m])
rate(node_disk_written_bytes_total[5m])
```

#### Network
```promql
# Network traffic in
rate(node_network_receive_bytes_total[5m])

# Network traffic out
rate(node_network_transmit_bytes_total[5m])

# Network errors
rate(node_network_receive_errs_total[5m])
```

### Database Metrics

#### PostgreSQL
```promql
# Active connections
pg_stat_database_numbackends

# Connection utilization
pg_stat_database_numbackends / pg_settings_max_connections * 100

# Query duration (slow queries)
rate(pg_stat_statements_mean_time_seconds{query=~".*"}[5m]) > 1

# Transactions per second
rate(pg_stat_database_xact_commit[5m]) + rate(pg_stat_database_xact_rollback[5m])

# Database size
pg_database_size_bytes
```

#### Redis
```promql
# Connected clients
redis_connected_clients

# Memory usage
redis_memory_used_bytes

# Commands per second
rate(redis_commands_processed_total[5m])

# Cache hit rate
rate(redis_keyspace_hits_total[5m]) / (rate(redis_keyspace_hits_total[5m]) + rate(redis_keyspace_misses_total[5m])) * 100
```

## Grafana Dashboards

### Main Dashboard: Kundli Service Overview

**Panels:**
1. **System Health** (top row)
   - Service uptime
   - Active services count
   - Current error rate
   - Response time (p95)

2. **Request Metrics** (second row)
   - Requests per second (graph)
   - Requests by endpoint (bar chart)
   - Status codes distribution (pie chart)
   - Response time heatmap

3. **Application Performance**
   - Average calculation time
   - Calculations per minute
   - Failed calculations rate
   - Cache hit rate

4. **System Resources**
   - CPU usage (graph)
   - Memory usage (graph)
   - Disk usage (gauge)
   - Network I/O (graph)

5. **Database Performance**
   - PostgreSQL connections
   - Query duration
   - Transactions per second
   - Database size

### Creating Custom Dashboard

1. **Access Grafana:**
```bash
http://localhost:3001
```

2. **Create New Dashboard:**
   - Click "+" → "Dashboard"
   - Add Panel
   - Select visualization type

3. **Add Prometheus Query:**
```promql
# Example: Request rate by endpoint
sum(rate(http_requests_total[5m])) by (endpoint)
```

4. **Configure Panel:**
   - Title: "Requests by Endpoint"
   - Type: Time series or Bar chart
   - Legend: Show with values
   - Unit: requests/sec

5. **Save Dashboard:**
   - Click save icon
   - Give descriptive name
   - Add tags for organization

### Dashboard JSON Export

To share or backup dashboards:

```bash
# Export dashboard
curl -H "Content-Type: application/json" \
  http://admin:password@localhost:3001/api/dashboards/uid/<dashboard-uid> \
  > dashboard-backup.json

# Import dashboard
curl -X POST -H "Content-Type: application/json" \
  -d @dashboard-backup.json \
  http://admin:password@localhost:3001/api/dashboards/db
```

## Alerting

### Prometheus Alert Rules

Located in `monitoring/prometheus/alert.rules`

#### Critical Alerts

**Service Down**
```yaml
- alert: ServiceDown
  expr: up == 0
  for: 5m
  labels:
    severity: critical
  annotations:
    summary: "Service {{ $labels.job }} is down"
    description: "{{ $labels.instance }} has been down for 5 minutes"
```

**High Error Rate**
```yaml
- alert: HighErrorRate
  expr: sum(rate(http_requests_total{status=~"5.."}[5m])) / sum(rate(http_requests_total[5m])) * 100 > 5
  for: 5m
  labels:
    severity: critical
  annotations:
    summary: "High error rate detected"
    description: "Error rate is {{ $value }}% (threshold: 5%)"
```

**Database Down**
```yaml
- alert: DatabaseDown
  expr: pg_up == 0
  for: 2m
  labels:
    severity: critical
  annotations:
    summary: "PostgreSQL database is down"
    description: "Database {{ $labels.instance }} is not responding"
```

#### Warning Alerts

**High Response Time**
```yaml
- alert: HighResponseTime
  expr: histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m])) > 2
  for: 10m
  labels:
    severity: warning
  annotations:
    summary: "High response time detected"
    description: "95th percentile response time is {{ $value }}s (threshold: 2s)"
```

**High CPU Usage**
```yaml
- alert: HighCPUUsage
  expr: 100 - (avg by(instance) (rate(node_cpu_seconds_total{mode="idle"}[5m])) * 100) > 80
  for: 10m
  labels:
    severity: warning
  annotations:
    summary: "High CPU usage on {{ $labels.instance }}"
    description: "CPU usage is {{ $value }}% (threshold: 80%)"
```

**High Memory Usage**
```yaml
- alert: HighMemoryUsage
  expr: (node_memory_MemTotal_bytes - node_memory_MemAvailable_bytes) / node_memory_MemTotal_bytes * 100 > 85
  for: 10m
  labels:
    severity: warning
  annotations:
    summary: "High memory usage on {{ $labels.instance }}"
    description: "Memory usage is {{ $value }}% (threshold: 85%)"
```

### Configuring Alert Notifications

#### Grafana Alert Channels

1. **Email Notifications:**
```bash
# Grafana configuration
docker-compose exec grafana grafana-cli admin reset-admin-password newpassword
```

Go to Configuration → Notification channels → Add channel

**Email Setup:**
- Name: Production Alerts
- Type: Email
- Addresses: ops@example.com, team@example.com
- Send test: ✓

2. **Slack Notifications:**

Create Slack webhook: https://api.slack.com/messaging/webhooks

Add channel:
- Name: Slack Alerts
- Type: Slack
- Webhook URL: https://hooks.slack.com/services/YOUR/WEBHOOK/URL
- Channel: #alerts
- Mention: @channel for critical

3. **PagerDuty:**
- Name: PagerDuty Critical
- Type: PagerDuty
- Integration Key: (from PagerDuty)
- Severity mapping: critical → trigger

### Alert Testing

```bash
# Trigger test alert
curl -X POST http://localhost:9090/api/v1/alerts

# View active alerts
curl http://localhost:9090/api/v1/alerts

# Silence alert (for maintenance)
# Use Alertmanager UI or API
```

## Log Analysis

### Accessing Logs

```bash
# View all logs
docker-compose logs -f

# Backend logs only
docker-compose logs -f backend

# Error logs only
docker-compose logs backend | grep ERROR

# Last 100 lines
docker-compose logs --tail=100 backend
```

### Grafana Log Exploration

1. Access Grafana Explore: http://localhost:3001/explore
2. Select Loki datasource
3. Enter LogQL query:

```logql
# All backend logs
{container="kundli-backend"}

# Error logs only
{container="kundli-backend"} |= "ERROR"

# Specific endpoint logs
{container="kundli-backend"} |= "/api/v1/charts/calculate"

# Filter by log level
{container="kundli-backend"} | json | level="error"

# Rate of errors
rate({container="kundli-backend"} |= "ERROR"[5m])
```

### Common Log Patterns

```logql
# Authentication failures
{container="kundli-backend"} |= "Authentication failed"

# Slow queries (>1s)
{container="kundli-backend"} | json | duration > 1000

# 5xx errors
{container="kundli-backend"} | json | status >= 500

# Database connection errors
{container="kundli-backend"} |= "database" |= "connection"
```

## Performance Monitoring

### Request Tracing

Track slow endpoints:

```promql
# Top 10 slowest endpoints
topk(10, sum(rate(http_request_duration_seconds_sum[5m])) by (endpoint) / sum(rate(http_request_duration_seconds_count[5m])) by (endpoint))

# Requests taking >3 seconds
sum(rate(http_request_duration_seconds_bucket{le="3"}[5m])) - sum(rate(http_request_duration_seconds_bucket{le="+Inf"}[5m]))
```

### Database Query Monitoring

```sql
-- Connect to PostgreSQL
docker-compose exec postgres psql -U kundli_user -d kundli_prod

-- Enable pg_stat_statements
CREATE EXTENSION IF NOT EXISTS pg_stat_statements;

-- Top 10 slowest queries
SELECT 
  query,
  calls,
  mean_exec_time,
  max_exec_time
FROM pg_stat_statements
ORDER BY mean_exec_time DESC
LIMIT 10;
```

### Resource Trends

```promql
# CPU trend (increase/decrease)
delta(node_cpu_seconds_total[1h])

# Memory growth rate
rate(container_memory_usage_bytes[1h])

# Disk usage prediction (when will disk be full)
predict_linear(node_filesystem_avail_bytes[1h], 24*3600)
```

## Best Practices

### Dashboard Organization

1. **Create dashboard folders:**
   - System Overview
   - Application Metrics
   - Database Performance
   - Business Metrics

2. **Use variables for filtering:**
   - Instance selection
   - Time range presets
   - Environment (prod/staging)

3. **Standard time ranges:**
   - Last 15 minutes (troubleshooting)
   - Last 24 hours (daily review)
   - Last 7 days (weekly reports)

### Alert Tuning

1. **Avoid alert fatigue:**
   - Set appropriate thresholds
   - Use `for` clause to avoid flapping
   - Group related alerts

2. **Alert hierarchy:**
   - Critical: Immediate action required
   - Warning: Monitor, action may be needed
   - Info: Awareness only

3. **Test alerts regularly:**
   - Run failure scenarios
   - Verify notification delivery
   - Document response procedures

### Monitoring Hygiene

```bash
# Regular cleanup
# Remove old metrics (automatic with retention policy)
# Default: 15 days in prometheus.yml

# Backup Grafana dashboards
for dash in $(curl -s http://admin:password@localhost:3001/api/search | jq -r '.[].uid'); do
  curl -s http://admin:password@localhost:3001/api/dashboards/uid/$dash > backup_$dash.json
done

# Optimize Prometheus storage
docker-compose exec prometheus promtool tsdb analyze /prometheus
```

## Troubleshooting Monitoring

### Prometheus Not Scraping

```bash
# Check targets
curl http://localhost:9090/api/v1/targets | jq '.data.activeTargets[] | {job: .labels.job, health: .health}'

# Verify metrics endpoint
curl http://localhost:8000/api/v1/metrics
```

### Grafana No Data

```bash
# Test datasource connection
curl http://localhost:3001/api/datasources/proxy/1/api/v1/query?query=up

# Check Grafana logs
docker-compose logs grafana | grep -i error
```

### High Cardinality Issues

```promql
# Find high cardinality metrics
topk(10, count by (__name__)({__name__=~".+"}))

# Use recording rules for frequently queried metrics
groups:
  - name: kundli_recording_rules
    interval: 30s
    rules:
      - record: job:http_requests:rate5m
        expr: sum(rate(http_requests_total[5m])) by (job)
```

## Additional Resources

- [Prometheus Documentation](https://prometheus.io/docs/)
- [Grafana Documentation](https://grafana.com/docs/)
- [PromQL Tutorial](https://prometheus.io/docs/prometheus/latest/querying/basics/)
- [LogQL Documentation](https://grafana.com/docs/loki/latest/logql/)
