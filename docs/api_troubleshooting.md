# API Troubleshooting Guide

## Common Issues and Solutions

### Authentication Issues

#### 1. Invalid Token
**Problem**: Receiving `AUTH001: Invalid authentication token`
**Solutions**:
1. Check token expiration
2. Verify token format
3. Ensure token is being sent in Authorization header
4. Try refreshing the token

**Example Debug Process**:
```python
# Check token expiration
import jwt
try:
    decoded = jwt.decode(token, verify=False)
    exp_timestamp = decoded['exp']
    # Check if expired
except jwt.InvalidTokenError:
    # Token is malformed
```

#### 2. Token Expired
**Problem**: Receiving `AUTH002: Token expired`
**Solutions**:
1. Use refresh token to get new access token
2. Re-authenticate if refresh token also expired
3. Check system clock synchronization

### Validation Issues

#### 1. Invalid Date Format
**Problem**: Receiving `VAL001: Invalid date format`
**Solutions**:
1. Use YYYY-MM-DD format
2. Check for leading/trailing spaces
3. Ensure date is valid

**Example Fix**:
```python
from datetime import datetime

# Wrong
date = "01-01-2025"  # Wrong format

# Correct
date = "2025-01-01"  # Correct format

# Validation
try:
    datetime.strptime(date, "%Y-%m-%d")
except ValueError:
    print("Invalid date format")
```

#### 2. Invalid Coordinates
**Problem**: Receiving `VAL002: Invalid coordinates`
**Solutions**:
1. Ensure latitude is between -90 and 90
2. Ensure longitude is between -180 and 180
3. Use decimal degrees format

### Calculation Issues

#### 1. Calculation Failed
**Problem**: Receiving `CALC001: Calculation failed`
**Solutions**:
1. Verify input data accuracy
2. Check timezone validity
3. Ensure date is within supported range (1800-2099)

#### 2. Ephemeris Error
**Problem**: Receiving `CALC002: Ephemeris error`
**Solutions**:
1. Verify Swiss Ephemeris files are present
2. Check file permissions
3. Ensure date is within ephemeris range

### Performance Issues

#### 1. Rate Limiting
**Problem**: Receiving `SYS003: Rate limit exceeded`
**Solutions**:
1. Check current rate limits for your tier
2. Implement request throttling
3. Consider upgrading account tier

**Example Implementation**:
```python
import time
import asyncio

class RateLimiter:
    def __init__(self, calls_per_minute):
        self.calls_per_minute = calls_per_minute
        self.calls = []

    async def acquire(self):
        now = time.time()
        # Remove old calls
        self.calls = [call for call in self.calls if call > now - 60]
        
        if len(self.calls) >= self.calls_per_minute:
            sleep_time = self.calls[0] - (now - 60)
            await asyncio.sleep(sleep_time)
            
        self.calls.append(now)
```

#### 2. Slow Response Times
**Problem**: API requests taking too long
**Solutions**:
1. Use caching where appropriate
2. Optimize query parameters
3. Check network latency

### Integration Issues

#### 1. CORS Errors
**Problem**: Receiving CORS policy errors
**Solutions**:
1. Add your domain to allowed origins
2. Check request headers
3. Verify HTTPS usage

**Example Configuration**:
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://your-domain.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

#### 2. Content Type Issues
**Problem**: Receiving `415 Unsupported Media Type`
**Solutions**:
1. Set Content-Type header to application/json
2. Properly stringify JSON data
3. Check request body format

## Debugging Tools

### 1. Request Inspection
Use the following curl command to inspect requests:

```bash
curl -v -X POST https://api.kundli-service.com/v1/kundli/calculate \
  -H "Authorization: Bearer your_token" \
  -H "Content-Type: application/json" \
  -d '{
    "date": "2025-01-05",
    "time": "12:00:00",
    "latitude": 28.6139,
    "longitude": 77.2090,
    "timezone": "Asia/Kolkata"
  }'
```

### 2. Response Headers Analysis
Important headers to check:
```http
X-Request-ID: For tracking requests
X-Response-Time: For performance monitoring
X-RateLimit-*: For rate limit information
```

### 3. Logging
Enable debug logging:
```python
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

## Error Code Reference

### Authentication Errors (AUTH*)
- AUTH001: Invalid token
- AUTH002: Token expired
- AUTH003: Insufficient permissions

### Validation Errors (VAL*)
- VAL001: Invalid input format
- VAL002: Invalid coordinates
- VAL003: Invalid timezone

### Calculation Errors (CALC*)
- CALC001: Calculation failed
- CALC002: Ephemeris error
- CALC003: Invalid calculation parameters

### System Errors (SYS*)
- SYS001: Internal server error
- SYS002: Service unavailable
- SYS003: Rate limit exceeded

## Support Resources

1. **API Status Page**: https://status.kundli-service.com
2. **Developer Forum**: https://community.kundli-service.com
3. **Email Support**: api-support@kundli-service.com

## Best Practices

1. **Error Handling**
   - Always check response status codes
   - Implement retry logic with exponential backoff
   - Log detailed error information

2. **Performance**
   - Cache frequently used data
   - Batch requests when possible
   - Monitor rate limits

3. **Security**
   - Rotate tokens regularly
   - Use HTTPS for all requests
   - Never log sensitive data

4. **Integration**
   - Use SDK when available
   - Implement proper error handling
   - Follow rate limiting guidelines
