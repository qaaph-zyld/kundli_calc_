# API Versioning Guide

## Overview
This document outlines the versioning strategy for the Kundli Calculation Service API, including version lifecycle, migration guides, and deprecation policies.

## Table of Contents
1. [Versioning Strategy](#versioning-strategy)
2. [Current Versions](#current-versions)
3. [Version Lifecycle](#version-lifecycle)
4. [Breaking Changes](#breaking-changes)
5. [Migration Guides](#migration-guides)
6. [Deprecation Policy](#deprecation-policy)

## Versioning Strategy

### 1. Version Format
We use semantic versioning (MAJOR.MINOR.PATCH) with the following rules:
- MAJOR version for incompatible API changes
- MINOR version for backwards-compatible feature additions
- PATCH version for backwards-compatible bug fixes

### 2. API URL Structure
```
https://api.kundli-service.com/v{major_version}/{resource}
```

Example:
```
https://api.kundli-service.com/v1/kundli/calculate
https://api.kundli-service.com/v2/kundli/calculate
```

### 3. Version Headers
```http
Accept: application/json; version=1.2
X-API-Version: 1.2
```

## Current Versions

### 1. Stable Versions
| Version | Status | Released | End of Life |
|---------|---------|-----------|-------------|
| v1      | Active  | 2024-01-01| 2026-01-01 |
| v2      | Beta    | 2025-01-01| -          |

### 2. Version Features
#### v1 (Current Stable)
- Basic Kundli calculations
- Planetary positions
- House cusps
- Basic Yogas

#### v2 (Beta)
- Advanced Kundli calculations
- Detailed Yoga analysis
- Transit predictions
- Compatibility analysis

## Version Lifecycle

### 1. Beta Phase
- New features are added
- Breaking changes may occur
- Not recommended for production use
- Feedback actively solicited

### 2. Stable Phase
- API is production-ready
- No breaking changes
- Regular bug fixes and improvements
- Full documentation available

### 3. Maintenance Phase
- Only critical bug fixes
- No new features
- Deprecation notices issued
- Migration guides available

### 4. End of Life
- No further updates
- Limited support
- Users encouraged to migrate
- Documentation archived

## Breaking Changes

### 1. What Constitutes a Breaking Change
- URL structure changes
- Request/response format changes
- Removed endpoints or parameters
- Changed parameter types
- Modified authentication methods

### 2. Change Management
```json
{
  "breaking_changes": {
    "v1_to_v2": [
      {
        "type": "parameter_change",
        "endpoint": "/kundli/calculate",
        "old": {
          "time": "string (HH:MM)"
        },
        "new": {
          "time": "string (HH:MM:SS)"
        }
      },
      {
        "type": "response_format",
        "endpoint": "/kundli/planets",
        "description": "Added additional fields for planetary states"
      }
    ]
  }
}
```

## Migration Guides

### 1. v1 to v2 Migration

#### Authentication Changes
```javascript
// v1 Authentication
const v1Auth = async () => {
  const response = await fetch('/v1/auth/token', {
    method: 'POST',
    body: JSON.stringify({
      api_key: 'key'
    })
  });
};

// v2 Authentication
const v2Auth = async () => {
  const response = await fetch('/v2/auth/token', {
    method: 'POST',
    body: JSON.stringify({
      api_key: 'key',
      scope: ['basic', 'advanced']  // New in v2
    })
  });
};
```

#### Request Format Changes
```javascript
// v1 Request
const v1Request = {
  date: "2025-01-05",
  time: "06:18",
  latitude: 28.6139,
  longitude: 77.2090
};

// v2 Request
const v2Request = {
  datetime: "2025-01-05T06:18:33Z",  // ISO 8601
  location: {
    latitude: 28.6139,
    longitude: 77.2090,
    altitude: 0  // New in v2
  }
};
```

#### Response Format Changes
```javascript
// v1 Response
const v1Response = {
  planets: {
    Sun: {
      longitude: 280.5
    }
  }
};

// v2 Response
const v2Response = {
  planets: {
    Sun: {
      longitude: 280.5,
      state: {  // New in v2
        exalted: false,
        debilitated: false,
        retrograde: false
      }
    }
  }
};
```

### 2. Migration Checklist
```markdown
1. Update Authentication
   - [ ] Implement new token format
   - [ ] Add scope parameters
   - [ ] Update refresh logic

2. Update Requests
   - [ ] Convert timestamps to ISO 8601
   - [ ] Restructure location data
   - [ ] Add new required fields

3. Update Response Handling
   - [ ] Handle new response formats
   - [ ] Implement error handling
   - [ ] Update caching logic
```

## Deprecation Policy

### 1. Timeline
```yaml
deprecation:
  notice_period: 12 months
  grace_period: 3 months
  stages:
    - name: Announcement
      duration: 1 month
      actions:
        - Email notification
        - Documentation update
        - Deprecation header added
    
    - name: Warning
      duration: 9 months
      actions:
        - Regular reminders
        - Warning headers
        - Usage statistics provided
    
    - name: Grace Period
      duration: 3 months
      actions:
        - Final notifications
        - Migration support
        - Limited functionality
```

### 2. Deprecation Headers
```http
# Warning Header (During deprecation period)
Warning: 299 - "The endpoint /v1/kundli/basic will be deprecated on 2026-01-01"

# Sunset Header (90 days before EOL)
Sunset: Sat, 1 Jan 2026 00:00:00 GMT
```

### 3. Monitoring Deprecated Usage
```python
class DeprecationMonitor:
    def track_usage(self, version: str, endpoint: str):
        metrics.increment(
            "api.deprecated.usage",
            tags={
                "version": version,
                "endpoint": endpoint
            }
        )
    
    def notify_users(self, version: str):
        users = self.get_users_using_version(version)
        for user in users:
            self.send_deprecation_notice(user, version)
```

### 4. Communication Plan
```yaml
communication:
  channels:
    - email:
        frequency: monthly
        template: deprecation_notice.html
    
    - api_response:
        headers: true
        body: include_migration_link
    
    - documentation:
        banner: true
        migration_guide: true
    
    - dashboard:
        alerts: true
        usage_stats: true
```
