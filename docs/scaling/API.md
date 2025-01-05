# Service Scaling Framework API Documentation

## API Overview
The Service Scaling Framework provides a RESTful API for managing scaling operations, configurations, and monitoring.

## Base URL
All endpoints are relative to: `http://localhost:8001`

## Authentication
Authentication is required for all endpoints. Use Bearer token authentication:
```bash
Authorization: Bearer <your_token>
```

## Endpoints

### Health Check

#### GET /health
Check the health status of the scaling service.

**Response**
```json
{
    "status": "ready",
    "timestamp": "2024-12-30T05:42:48+01:00"
}
```

### Metrics

#### GET /metrics
Get current scaling metrics.

**Response**
```json
{
    "integration": {
        "total_operations": 100,
        "successful_operations": 95,
        "failed_operations": 5,
        "average_latency": 0.5,
        "last_operation_time": "2024-12-30T05:42:48+01:00",
        "current_status": "ready"
    },
    "monitoring": {
        "cpu_usage": 0.6,
        "memory_usage": 0.4,
        "request_count": 1000,
        "average_latency": 0.2
    }
}
```

### Scaling

#### POST /scale
Trigger a scaling operation.

**Request**
```json
{
    "mode": "horizontal",
    "replicas": 3,
    "resources": {
        "cpu": 1.0,
        "memory": 1024
    }
}
```

**Response**
```json
{
    "status": "success",
    "platform": "kubernetes",
    "timestamp": "2024-12-30T05:42:48+01:00"
}
```

### Configuration

#### GET /config
Get current scaling configuration.

**Response**
```json
{
    "mode": "hybrid",
    "resources": {
        "min_cpu": 0.1,
        "max_cpu": 4.0,
        "min_memory": 128,
        "max_memory": 8192,
        "cpu_request": 0.5,
        "memory_request": 512,
        "cpu_limit": 2.0,
        "memory_limit": 4096
    },
    "replicas": {
        "min_replicas": 1,
        "max_replicas": 10,
        "target_replicas": 2,
        "scale_up_threshold": 0.8,
        "scale_down_threshold": 0.2
    }
}
```

#### POST /config
Update scaling configuration.

**Request**
```json
{
    "mode": "hybrid",
    "resources": {
        "min_cpu": 0.1,
        "max_cpu": 4.0
    },
    "replicas": {
        "min_replicas": 1,
        "max_replicas": 10
    }
}
```

**Response**
```json
{
    "status": "success"
}
```

### Validation

#### GET /validation
Get validation results.

**Response**
```json
[
    {
        "scope": "configuration",
        "status": "passed",
        "message": "Configuration validation passed",
        "timestamp": "2024-12-30T05:42:48+01:00",
        "details": {}
    },
    {
        "scope": "resources",
        "status": "warning",
        "message": "CPU usage outside limits",
        "timestamp": "2024-12-30T05:42:48+01:00",
        "details": {
            "component": "cpu"
        }
    }
]
```

## Error Responses

### 400 Bad Request
```json
{
    "detail": "Invalid request parameters"
}
```

### 401 Unauthorized
```json
{
    "detail": "Invalid authentication credentials"
}
```

### 403 Forbidden
```json
{
    "detail": "Not authorized to perform operation"
}
```

### 404 Not Found
```json
{
    "detail": "Resource not found"
}
```

### 500 Internal Server Error
```json
{
    "detail": "Internal server error occurred"
}
```

## Rate Limiting
API endpoints are rate limited to:
- 100 requests per minute for GET endpoints
- 10 requests per minute for POST endpoints

## Versioning
API versioning is handled through the `Accept` header:
```bash
Accept: application/vnd.scaling.v1+json
```

## SDK Examples

### Python
```python
from app.core.scaling.integration import ScalingIntegration

# Initialize integration
integration = ScalingIntegration()

# Trigger scaling
result = await integration.scale({
    "mode": "horizontal",
    "replicas": 3
})

print(result)
```

### JavaScript
```javascript
const response = await fetch('http://localhost:8001/scale', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer <your_token>'
    },
    body: JSON.stringify({
        mode: 'horizontal',
        replicas: 3
    })
});

const result = await response.json();
console.log(result);
```

### Curl
```bash
# Trigger scaling
curl -X POST http://localhost:8001/scale \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer <your_token>" \
    -d '{
        "mode": "horizontal",
        "replicas": 3
    }'
```

## Webhook Integration

### Webhook Format
```json
{
    "event": "scaling_completed",
    "timestamp": "2024-12-30T05:42:48+01:00",
    "data": {
        "mode": "horizontal",
        "replicas": 3,
        "status": "success"
    }
}
```

### Webhook Configuration
```json
{
    "webhooks": {
        "enabled": true,
        "url": "https://your-domain.com/webhook",
        "secret": "your_webhook_secret",
        "events": ["scaling_completed", "scaling_failed"]
    }
}
```

## Best Practices

1. **Authentication**
   - Use secure tokens
   - Rotate tokens regularly
   - Implement token expiration

2. **Rate Limiting**
   - Implement client-side throttling
   - Handle rate limit responses
   - Use exponential backoff

3. **Error Handling**
   - Handle all error responses
   - Implement retry logic
   - Log error details

4. **Monitoring**
   - Monitor API usage
   - Track error rates
   - Set up alerts

## Support
For API support and issues:
- Email: api-support@your-domain.com
- Documentation: [API Documentation](https://your-domain.com/docs/api)
- Status: [API Status](https://status.your-domain.com)
