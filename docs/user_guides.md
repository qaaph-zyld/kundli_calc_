# Kundli Calculation Service - User Guides

## Getting Started

### 1. Account Setup
1. Register for an account at https://kundli-service.com/register
2. Choose your subscription tier:
   - Basic: 100 calculations/month
   - Premium: 1000 calculations/month
   - Enterprise: Custom limits
3. Generate your API keys from the dashboard

### 2. Authentication
1. Use your API key to obtain a JWT token:
```bash
curl -X POST https://api.kundli-service.com/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "api_key": "your_api_key"
  }'
```

2. Include the token in all API requests:
```bash
Authorization: Bearer your_jwt_token
```

## Feature Guides

### 1. Basic Kundli Calculation
Calculate a basic birth chart with planetary positions and house cusps.

#### Required Information:
- Birth date (YYYY-MM-DD)
- Birth time (HH:MM:SS)
- Birth place coordinates (latitude, longitude)
- Timezone name

#### Example Request:
```bash
curl -X POST https://api.kundli-service.com/v1/kundli/calculate \
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

### 2. Advanced Kundli Features
Premium features for detailed astrological analysis.

#### Available Features:
1. **Dasha Calculations**
   - Vimshottari Dasha
   - Yogini Dasha
   - Char Dasha

2. **Yoga Analysis**
   - Raja Yoga
   - Dhana Yoga
   - Special combinations

3. **Ashtakavarga System**
   - Sarvashtakavarga
   - Individual planet's Ashtakavarga
   - Kaksha Bala

### 3. Compatibility Analysis
Compare two birth charts for compatibility.

#### Steps:
1. Calculate both birth charts
2. Send compatibility analysis request
3. Receive detailed comparison report

#### Example:
```bash
curl -X POST https://api.kundli-service.com/v1/kundli/compatibility \
  -H "Authorization: Bearer your_jwt_token" \
  -H "Content-Type: application/json" \
  -d '{
    "kundli1_id": "k_123abc",
    "kundli2_id": "k_456def"
  }'
```

## Best Practices

### 1. Data Accuracy
- Use precise birth time (seconds if available)
- Verify timezone information
- Double-check coordinates
- Validate data before sending

### 2. Performance Optimization
- Cache frequently used calculations
- Implement request batching
- Monitor rate limits
- Use appropriate error handling

### 3. Security
- Secure API key storage
- Regular token rotation
- HTTPS for all requests
- Input validation

## Troubleshooting

### Common Issues

1. **Invalid Time Format**
   ```javascript
   // Wrong
   "time": "12:00"
   
   // Correct
   "time": "12:00:00"
   ```

2. **Timezone Errors**
   ```javascript
   // Wrong
   "timezone": "IST"
   
   // Correct
   "timezone": "Asia/Kolkata"
   ```

3. **Coordinate Format**
   ```javascript
   // Wrong
   "latitude": "28°36'50\"N"
   
   // Correct
   "latitude": 28.6139
   ```

### Error Resolution

1. **Authentication Errors**
   - Check token expiration
   - Verify API key status
   - Confirm subscription status

2. **Validation Errors**
   - Review input format
   - Check data ranges
   - Verify timezone names

3. **Calculation Errors**
   - Confirm date range validity
   - Check coordinate accuracy
   - Verify calculation parameters

## FAQ

### General Questions

1. **What is the supported date range?**
   - From year 1800 to 2099

2. **Which ayanamsa systems are supported?**
   - Lahiri (Default)
   - Raman
   - Krishnamurti

3. **What are the rate limits?**
   - Basic: 100 requests/minute
   - Premium: 1000 requests/minute
   - Enterprise: Custom limits

### Technical Questions

1. **How accurate are the calculations?**
   - Planetary positions: Up to 1 arc second
   - House cusps: Up to 1 arc minute

2. **Which house systems are supported?**
   - Placidus (Default)
   - Koch
   - Equal House
   - Whole Sign

3. **How long are calculations cached?**
   - Basic calculations: 24 hours
   - Advanced calculations: 12 hours
   - Custom caching available for enterprise

## Support

### Getting Help
1. **Documentation**: https://docs.kundli-service.com
2. **API Status**: https://status.kundli-service.com
3. **Email Support**: support@kundli-service.com
4. **Community Forum**: https://community.kundli-service.com

### Feature Requests
Submit feature requests through:
1. GitHub Issues
2. Support Portal
3. Email to features@kundli-service.com

## Updates and Maintenance

### Service Updates
- Scheduled maintenance: First Sunday of each month
- Emergency updates: Notified 24 hours in advance
- Version updates: Announced 2 weeks in advance

### API Versions
- Current stable: v1
- Beta features: v2-beta
- Legacy support: v0 (deprecated)
