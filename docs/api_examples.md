# Kundli Calculation Service - API Usage Examples

## Authentication

### 1. Obtain JWT Token
```bash
curl -X POST https://api.kundli-service.com/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "user@example.com",
    "password": "your_password"
  }'
```

Response:
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "token_type": "bearer",
  "expires_in": 3600
}
```

## Kundli Calculations

### 1. Calculate New Birth Chart
```bash
curl -X POST https://api.kundli-service.com/v1/kundli/calculate \
  -H "Authorization: Bearer your_jwt_token" \
  -H "Content-Type: application/json" \
  -d '{
    "date": "1990-01-01",
    "time": "12:00:00",
    "latitude": 28.6139,
    "longitude": 77.2090,
    "timezone": "Asia/Kolkata",
    "ayanamsa": "lahiri",
    "house_system": "placidus",
    "calculation_options": {
      "include_upagrahas": true,
      "include_special_points": true
    }
  }'
```

Response:
```json
{
  "request_id": "req_123abc",
  "timestamp": "2025-01-05T05:06:55Z",
  "input_data": {
    "date": "1990-01-01",
    "time": "12:00:00",
    "latitude": 28.6139,
    "longitude": 77.2090,
    "timezone": "Asia/Kolkata",
    "ayanamsa": "lahiri",
    "house_system": "placidus"
  },
  "planets": {
    "Sun": {
      "longitude": 280.5,
      "latitude": 0.0,
      "speed": 1.01,
      "house": 10
    },
    "Moon": {
      "longitude": 45.8,
      "latitude": -4.2,
      "speed": 12.5,
      "house": 3
    }
  },
  "houses": {
    "1": 75.5,
    "2": 105.3,
    "3": 135.1
  },
  "metadata": {
    "calculation_time": "0.123s",
    "ayanamsa_used": "Lahiri",
    "house_system": "Placidus"
  }
}
```

### 2. Validate Birth Details
```bash
curl -X POST https://api.kundli-service.com/v1/kundli/validate \
  -H "Authorization: Bearer your_jwt_token" \
  -H "Content-Type: application/json" \
  -d '{
    "date": "1990-01-01",
    "time": "12:00:00",
    "latitude": 28.6139,
    "longitude": 77.2090,
    "timezone": "Asia/Kolkata"
  }'
```

Response:
```json
{
  "is_valid": true,
  "warnings": [
    {
      "type": "business",
      "rule": "location_precision",
      "message": "Location coordinates should have more precision"
    }
  ],
  "metadata": {
    "timestamp": "2025-01-05T05:06:55Z",
    "data_metrics": {
      "total_validations": 5,
      "passed_validations": 5,
      "failed_validations": 0
    }
  }
}
```

### 3. Retrieve Birth Chart
```bash
curl -X GET https://api.kundli-service.com/v1/kundli/k_123abc \
  -H "Authorization: Bearer your_jwt_token"
```

### 4. Delete Birth Chart
```bash
curl -X DELETE https://api.kundli-service.com/v1/kundli/k_123abc \
  -H "Authorization: Bearer your_jwt_token"
```

## Error Handling Examples

### 1. Invalid Input
```bash
curl -X POST https://api.kundli-service.com/v1/kundli/calculate \
  -H "Authorization: Bearer your_jwt_token" \
  -H "Content-Type: application/json" \
  -d '{
    "date": "invalid_date",
    "time": "12:00:00",
    "latitude": 28.6139,
    "longitude": 77.2090,
    "timezone": "Asia/Kolkata"
  }'
```

Response:
```json
{
  "code": "VAL001",
  "message": "Invalid date format. Use YYYY-MM-DD",
  "category": "validation",
  "severity": "error",
  "timestamp": "2025-01-05T05:06:55Z",
  "details": {
    "field": "date",
    "value": "invalid_date"
  }
}
```

### 2. Unauthorized Access
```bash
curl -X POST https://api.kundli-service.com/v1/kundli/calculate \
  -H "Content-Type: application/json" \
  -d '{
    "date": "1990-01-01",
    "time": "12:00:00",
    "latitude": 28.6139,
    "longitude": 77.2090,
    "timezone": "Asia/Kolkata"
  }'
```

Response:
```json
{
  "code": "AUTH001",
  "message": "Missing or invalid authentication token",
  "category": "authentication",
  "severity": "error",
  "timestamp": "2025-01-05T05:06:55Z"
}
```

## Rate Limiting Example

When you exceed the rate limit (100 requests per minute), you'll receive:

```json
{
  "code": "SYS003",
  "message": "Rate limit exceeded",
  "category": "system",
  "severity": "error",
  "timestamp": "2025-01-05T05:06:55Z",
  "details": {
    "limit": 100,
    "remaining": 0,
    "reset": 45
  }
}
```

## Best Practices

1. **Authentication**
   - Always store JWT tokens securely
   - Refresh tokens before they expire
   - Never send tokens in URL parameters

2. **Error Handling**
   - Always check response status codes
   - Handle rate limiting gracefully
   - Implement exponential backoff for retries

3. **Data Validation**
   - Validate data before sending to API
   - Use proper timezone names
   - Provide precise coordinates

4. **Performance**
   - Cache frequently accessed data
   - Use compression for large requests
   - Implement request batching when possible
