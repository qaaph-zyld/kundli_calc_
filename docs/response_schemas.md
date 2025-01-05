# Response Schemas Documentation

## Overview
This document details all response schemas used in the Kundli Calculation Service API. Each schema includes a description, required fields, and example responses.

## Common Response Structure
All API responses follow this base structure:

```typescript
interface BaseResponse {
    status: "success" | "error";
    timestamp: string;  // ISO 8601 format
    request_id: string; // UUID v4
}
```

## Kundli Calculation Responses

### 1. Basic Kundli Response
```typescript
interface KundliResponse extends BaseResponse {
    data: {
        planets: {
            [key: string]: {
                longitude: number;
                latitude: number;
                speed: number;
                house: number;
                nakshatra: {
                    name: string;
                    pada: number;
                    lord: string;
                };
            };
        };
        houses: {
            [key: number]: number;  // house number -> longitude
        };
        aspects: Array<{
            planet1: string;
            planet2: string;
            aspect_type: string;
            orb: number;
            strength: number;
        }>;
        metadata: {
            calculation_time: string;
            ayanamsa_used: string;
            house_system: string;
        };
    };
}
```

### 2. Advanced Kundli Response
```typescript
interface AdvancedKundliResponse extends KundliResponse {
    data: {
        // Includes all fields from KundliResponse.data, plus:
        yogas: Array<{
            name: string;
            description: string;
            strength: number;
            planets_involved: string[];
        }>;
        dashas: {
            current: {
                planet: string;
                start_date: string;
                end_date: string;
                sub_dasha: {
                    planet: string;
                    start_date: string;
                    end_date: string;
                };
            };
            all_periods: Array<{
                planet: string;
                start_date: string;
                end_date: string;
            }>;
        };
        ashtakavarga: {
            [planet: string]: {
                points: number;
                details: {
                    [house: number]: number;
                };
            };
        };
        special_points: {
            arudha_lagna: number;
            hora_lagna: number;
            ghati_lagna: number;
        };
    };
}
```

### 3. Validation Response
```typescript
interface ValidationResponse extends BaseResponse {
    is_valid: boolean;
    errors: Array<{
        type: "data" | "business" | "security";
        rule: string;
        message: string;
        field?: string;
        value?: any;
    }>;
    warnings: Array<{
        type: "data" | "business" | "security";
        rule: string;
        message: string;
        field?: string;
        value?: any;
    }>;
    metadata: {
        validation_time: string;
        rules_checked: number;
    };
}
```

### 4. Pattern Analysis Response
```typescript
interface PatternResponse extends BaseResponse {
    data: {
        raja_yogas: Array<{
            name: string;
            description: string;
            strength: number;
            planets: string[];
            houses: number[];
        }>;
        dhana_yogas: Array<{
            name: string;
            description: string;
            strength: number;
            planets: string[];
            houses: number[];
        }>;
        doshas: Array<{
            name: string;
            description: string;
            severity: number;
            planets: string[];
            remedies: string[];
        }>;
    };
    metadata: {
        analysis_time: string;
        patterns_checked: number;
    };
}
```

### 5. Compatibility Analysis Response
```typescript
interface CompatibilityResponse extends BaseResponse {
    data: {
        overall_score: number;
        aspects: Array<{
            type: string;
            score: number;
            description: string;
        }>;
        factors: {
            mental: number;
            emotional: number;
            spiritual: number;
            physical: number;
            financial: number;
            domestic: number;
        };
        recommendations: Array<string>;
    };
    metadata: {
        analysis_time: string;
        comparison_method: string;
    };
}
```

## Error Responses

### 1. Validation Error
```typescript
interface ValidationError {
    code: string;      // e.g., "VAL001"
    message: string;
    category: "validation";
    severity: "error";
    details: {
        field: string;
        value: any;
        constraint: string;
    };
    timestamp: string;
    request_id: string;
}
```

### 2. Authentication Error
```typescript
interface AuthError {
    code: string;      // e.g., "AUTH001"
    message: string;
    category: "authentication";
    severity: "error";
    details?: {
        reason: string;
        required_roles?: string[];
    };
    timestamp: string;
    request_id: string;
}
```

### 3. System Error
```typescript
interface SystemError {
    code: string;      // e.g., "SYS001"
    message: string;
    category: "system";
    severity: "error" | "critical";
    details?: {
        component: string;
        error_type: string;
    };
    timestamp: string;
    request_id: string;
}
```

## Response Headers

### 1. Standard Headers
```http
Content-Type: application/json
X-Request-ID: uuid-v4-string
X-Response-Time: time-in-ms
```

### 2. Rate Limiting Headers
```http
X-RateLimit-Limit: requests-per-minute
X-RateLimit-Remaining: remaining-requests
X-RateLimit-Reset: seconds-until-reset
```

### 3. Caching Headers
```http
Cache-Control: max-age=3600
ETag: "33a64df551425fcc55e4d42a148795d9f25f89d4"
Last-Modified: Wed, 21 Oct 2015 07:28:00 GMT
```

## Response Examples

### 1. Successful Kundli Calculation
```json
{
    "status": "success",
    "timestamp": "2025-01-05T05:11:41Z",
    "request_id": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
    "data": {
        "planets": {
            "Sun": {
                "longitude": 280.5,
                "latitude": 0.0,
                "speed": 1.01,
                "house": 10,
                "nakshatra": {
                    "name": "Uttara Ashadha",
                    "pada": 2,
                    "lord": "Sun"
                }
            }
        },
        "houses": {
            "1": 75.5,
            "2": 105.3
        },
        "aspects": [
            {
                "planet1": "Sun",
                "planet2": "Moon",
                "aspect_type": "conjunction",
                "orb": 2.5,
                "strength": 0.95
            }
        ],
        "metadata": {
            "calculation_time": "0.123s",
            "ayanamsa_used": "Lahiri",
            "house_system": "Placidus"
        }
    }
}
```

### 2. Validation Error Response
```json
{
    "code": "VAL001",
    "message": "Invalid input data",
    "category": "validation",
    "severity": "error",
    "details": {
        "field": "date",
        "value": "2025-13-45",
        "constraint": "date format must be YYYY-MM-DD"
    },
    "timestamp": "2025-01-05T05:11:41Z",
    "request_id": "f47ac10b-58cc-4372-a567-0e02b2c3d479"
}
```

## Best Practices

1. **Response Structure**
   - Always include status, timestamp, and request_id
   - Use consistent field naming conventions
   - Include metadata for debugging

2. **Error Handling**
   - Use appropriate HTTP status codes
   - Include detailed error messages
   - Add error codes for easy reference

3. **Performance**
   - Use compression for large responses
   - Implement pagination for large datasets
   - Cache responses when appropriate

4. **Security**
   - Never expose sensitive data in responses
   - Validate all response data
   - Use appropriate security headers
