# Kundli Calculation Service API Documentation

## Overview
The Kundli Calculation Service provides a robust API for calculating and analyzing astrological birth charts (Kundli). The service follows REST principles and uses JSON for request and response payloads.

## Base URL
```
https://api.kundli-service.com/v1
```

## Authentication
All API endpoints require authentication using JWT (JSON Web Token). Include the token in the Authorization header:
```
Authorization: Bearer <your_jwt_token>
```

## Endpoints

### 1. Calculate Kundli
Calculate a new birth chart based on birth details.

**Endpoint:** `/kundli/calculate`  
**Method:** `POST`  
**Content-Type:** `application/json`

#### Request Body
```json
{
    "date": "1990-01-01",           // Birth date (YYYY-MM-DD)
    "time": "12:00:00",             // Birth time (HH:MM:SS)
    "latitude": 28.6139,            // Birth place latitude
    "longitude": 77.2090,           // Birth place longitude
    "timezone": "Asia/Kolkata",     // Timezone name
    "ayanamsa": "lahiri",           // Optional: Ayanamsa system
    "house_system": "placidus",     // Optional: House system
    "calculation_options": {         // Optional: Additional options
        "include_upagrahas": true,
        "include_special_points": true
    }
}
```

#### Response
```json
{
    "request_id": "req_123abc",
    "timestamp": "2024-01-01T12:00:00Z",
    "input_data": {
        // Input parameters as provided
    },
    "planets": {
        "Sun": {
            "longitude": 280.5,
            "latitude": 0.0,
            "speed": 1.01,
            "house": 10
        },
        // Other planets...
    },
    "houses": {
        "1": 75.5,
        // Other houses...
    },
    "aspects": [
        {
            "planet1": "Sun",
            "planet2": "Moon",
            "aspect_type": "conjunction",
            "orb": 2.5
        }
        // Other aspects...
    ],
    "yogas": [
        {
            "name": "Raj Yoga",
            "description": "...",
            "strength": 0.85
        }
        // Other yogas...
    ],
    "dashas": {
        "current": {
            "planet": "Venus",
            "start": "2020-01-01",
            "end": "2025-01-01"
        },
        // Other dasha periods...
    },
    "ashtakavarga": {
        "Sun": {
            "points": 25,
            "details": {}
        }
        // Other planets...
    },
    "charts": {
        "rashi": {},
        "navamsa": {},
        "d60": {}
    },
    "predictions": {
        "general": "...",
        "career": "...",
        "relationships": "..."
    },
    "metadata": {
        "calculation_time": "0.123s",
        "ayanamsa_used": "Lahiri",
        "house_system": "Placidus"
    }
}
```

### 2. Validate Kundli Data
Validate birth details before calculation.

**Endpoint:** `/kundli/validate`  
**Method:** `POST`  
**Content-Type:** `application/json`

#### Request Body
```json
{
    "date": "1990-01-01",
    "time": "12:00:00",
    "latitude": 28.6139,
    "longitude": 77.2090,
    "timezone": "Asia/Kolkata",
    "validation_types": ["data", "business"]  // Optional
}
```

#### Response
```json
{
    "is_valid": true,
    "errors": [
        {
            "type": "data",
            "rule": "date_format",
            "message": "Invalid date format"
        }
    ],
    "warnings": [
        {
            "type": "business",
            "rule": "location_precision",
            "message": "Location coordinates should have more precision"
        }
    ],
    "metadata": {
        "timestamp": "2024-01-01T12:00:00Z",
        "data_metrics": {
            "total_validations": 5,
            "passed_validations": 4,
            "failed_validations": 1
        },
        "business_metrics": {
            "total_validations": 3,
            "passed_validations": 2,
            "failed_validations": 1
        }
    }
}
```

### 3. Retrieve Kundli
Retrieve a previously calculated birth chart.

**Endpoint:** `/kundli/{kundli_id}`  
**Method:** `GET`

#### Response
Same as Calculate Kundli response

### 4. Delete Kundli
Delete a previously calculated birth chart.

**Endpoint:** `/kundli/{kundli_id}`  
**Method:** `DELETE`

#### Response
```json
{
    "status": "success",
    "message": "Kundli deleted successfully",
    "kundli_id": "k_123abc"
}
```

### 5. Analyze Patterns
Analyze planetary patterns and combinations.

**Endpoint:** `/kundli/{kundli_id}/patterns`  
**Method:** `GET`

#### Response
```json
{
    "status": "success",
    "data": {
        "yogas": [
            {
                "name": "Raj Yoga",
                "description": "...",
                "strength": 0.85
            }
        ],
        "raja_yogas": [],
        "dhana_yogas": [],
        "malefic_patterns": [],
        "benefic_patterns": []
    },
    "metadata": {
        "pattern_detection_time": "0.123s",
        "pattern_analysis_time": "0.456s"
    },
    "timestamp": "2024-01-01T12:00:00Z"
}
```

### 6. Analyze Correlation
Analyze correlation between two birth charts.

**Endpoint:** `/kundli/correlation`  
**Method:** `POST`  
**Content-Type:** `application/json`

#### Request Body
```json
{
    "kundli1": {
        "date": "1990-01-01",
        "time": "12:00:00",
        "latitude": 28.6139,
        "longitude": 77.2090,
        "timezone": "Asia/Kolkata"
    },
    "kundli2": {
        "date": "1992-01-01",
        "time": "15:00:00",
        "latitude": 19.0760,
        "longitude": 72.8777,
        "timezone": "Asia/Kolkata"
    },
    "analysis_type": "FULL"
}
```

#### Response
```json
{
    "status": "success",
    "data": {
        "overall_score": 0.8,
        "aspects": [],
        "factors": {
            "temperament": 0.7,
            "mental": 0.6,
            "emotional": 0.8,
            "spiritual": 0.9,
            "physical": 0.5
        }
    },
    "metadata": {
        "correlation_time": "0.123s",
        "analysis_time": "0.456s"
    },
    "timestamp": "2024-01-01T12:00:00Z"
}
```

## Error Handling

### Error Response Format
```json
{
    "code": "ERR001",
    "message": "Error description",
    "category": "validation",
    "severity": "error",
    "timestamp": "2024-01-01T12:00:00Z",
    "details": {
        "field": "date",
        "value": "invalid_date"
    },
    "request_id": "req_123abc"
}
```

### Common Error Codes
- `AUTH001`: Invalid credentials
- `AUTH002`: Token expired
- `AUTH003`: Insufficient permissions
- `VAL001`: Invalid input
- `VAL002`: Missing required field
- `VAL003`: Invalid format
- `CALC001`: Calculation failed
- `CALC002`: Invalid coordinates
- `CALC003`: Ephemeris error
- `DB001`: Database connection error
- `DB002`: Database query error
- `DB003`: Database write error
- `CACHE001`: Cache connection error
- `CACHE002`: Cache read error
- `CACHE003`: Cache write error
- `SYS001`: Internal server error
- `SYS002`: Service unavailable
- `SYS003`: Rate limit exceeded

## Rate Limiting
- Rate limit: 100 requests per minute per API key
- Rate limit headers included in response:
  - `X-RateLimit-Limit`
  - `X-RateLimit-Remaining`
  - `X-RateLimit-Reset`

## Best Practices
1. Always validate input data before calculation
2. Use appropriate timezone names from the IANA Time Zone Database
3. Provide coordinates with at least 4 decimal places for accuracy
4. Cache frequently accessed calculations
5. Handle rate limits appropriately
6. Implement proper error handling
7. Use HTTPS for all API calls
8. Keep your API keys secure

## Support
For API support, contact:
- Email: api-support@kundli-service.com
- Documentation: https://docs.kundli-service.com
- Status Page: https://status.kundli-service.com
