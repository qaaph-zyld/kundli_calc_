"""
Kundli API Tests
PGF Protocol: TEST_002
Gate: GATE_7
Version: 1.0.0
"""

import pytest
from datetime import datetime
from app.core.testing.framework import (
    test_framework,
    TestCase,
    TestScope,
    TestPriority,
    unit_test,
    integration_test,
    e2e_test,
    performance_test,
    security_test
)

# Test data
VALID_KUNDLI_DATA = {
    "date": "2024-01-01",
    "time": "12:00:00",
    "latitude": 28.6139,
    "longitude": 77.2090,
    "timezone": "Asia/Kolkata"
}

INVALID_KUNDLI_DATA = {
    "date": "invalid",
    "time": "invalid",
    "latitude": 1000,
    "longitude": 1000,
    "timezone": "invalid"
}

@unit_test(
    name="test_calculate_kundli_valid",
    priority=TestPriority.CRITICAL,
    tags=["kundli", "calculation", "valid"]
)
async def test_calculate_kundli_valid():
    """Test Kundli calculation with valid data"""
    case = TestCase(
        name="Calculate Kundli - Valid Data",
        scope=TestScope.UNIT,
        priority=TestPriority.CRITICAL,
        inputs={
            "method": "POST",
            "endpoint": "/api/v1/kundli/calculate",
            "body": VALID_KUNDLI_DATA,
            "headers": {
                "Content-Type": "application/json",
                "Authorization": "Bearer test_token"
            }
        },
        expected={
            "status_code": 200,
            "body": {
                "success": True,
                "data": {
                    "planets": {"type": "object"},
                    "houses": {"type": "object"},
                    "aspects": {"type": "array"}
                }
            }
        }
    )
    return await test_framework.run_case(case)

@unit_test(
    name="test_calculate_kundli_invalid",
    priority=TestPriority.HIGH,
    tags=["kundli", "calculation", "invalid"]
)
async def test_calculate_kundli_invalid():
    """Test Kundli calculation with invalid data"""
    case = TestCase(
        name="Calculate Kundli - Invalid Data",
        scope=TestScope.UNIT,
        priority=TestPriority.HIGH,
        inputs={
            "method": "POST",
            "endpoint": "/api/v1/kundli/calculate",
            "body": INVALID_KUNDLI_DATA,
            "headers": {
                "Content-Type": "application/json",
                "Authorization": "Bearer test_token"
            }
        },
        expected={
            "status_code": 422,
            "body": {
                "success": False,
                "detail": {
                    "message": "Data validation failed"
                }
            }
        }
    )
    return await test_framework.run_case(case)

@integration_test(
    name="test_kundli_pattern_flow",
    priority=TestPriority.HIGH,
    tags=["kundli", "pattern", "integration"]
)
async def test_kundli_pattern_flow():
    """Test Kundli calculation and pattern analysis flow"""
    case = TestCase(
        name="Kundli Pattern Flow",
        scope=TestScope.INTEGRATION,
        priority=TestPriority.HIGH,
        inputs={
            "steps": [
                {
                    "name": "calculate_kundli",
                    "method": "POST",
                    "endpoint": "/api/v1/kundli/calculate",
                    "body": VALID_KUNDLI_DATA,
                    "headers": {
                        "Content-Type": "application/json",
                        "Authorization": "Bearer test_token"
                    }
                },
                {
                    "name": "analyze_patterns",
                    "method": "POST",
                    "endpoint": "/api/v1/kundli/patterns",
                    "body": {
                        "kundli_id": "{calculate_kundli.body.data.id}"
                    },
                    "headers": {
                        "Content-Type": "application/json",
                        "Authorization": "Bearer test_token"
                    }
                }
            ]
        },
        expected={
            "calculate_kundli": {
                "status_code": 200,
                "body": {"success": True}
            },
            "analyze_patterns": {
                "status_code": 200,
                "body": {"success": True}
            }
        }
    )
    return await test_framework.run_case(case)

@e2e_test(
    name="test_kundli_e2e_flow",
    priority=TestPriority.CRITICAL,
    tags=["kundli", "e2e"]
)
async def test_kundli_e2e_flow():
    """Test complete Kundli end-to-end flow"""
    case = TestCase(
        name="Kundli E2E Flow",
        scope=TestScope.E2E,
        priority=TestPriority.CRITICAL,
        inputs={
            "scenarios": [
                {
                    "name": "full_kundli_analysis",
                    "steps": [
                        {
                            "name": "calculate_kundli",
                            "method": "POST",
                            "endpoint": "/api/v1/kundli/calculate",
                            "body": VALID_KUNDLI_DATA
                        },
                        {
                            "name": "analyze_patterns",
                            "method": "POST",
                            "endpoint": "/api/v1/kundli/patterns",
                            "body": {
                                "kundli_id": "{calculate_kundli.body.data.id}"
                            }
                        },
                        {
                            "name": "get_kundli",
                            "method": "GET",
                            "endpoint": "/api/v1/kundli/{calculate_kundli.body.data.id}"
                        },
                        {
                            "name": "get_patterns",
                            "method": "GET",
                            "endpoint": "/api/v1/kundli/patterns/{calculate_kundli.body.data.id}"
                        }
                    ]
                }
            ]
        },
        expected={
            "full_kundli_analysis": {
                "calculate_kundli": {"status_code": 200},
                "analyze_patterns": {"status_code": 200},
                "get_kundli": {"status_code": 200},
                "get_patterns": {"status_code": 200}
            }
        }
    )
    return await test_framework.run_case(case)

@performance_test(
    name="test_kundli_performance",
    priority=TestPriority.HIGH,
    tags=["kundli", "performance"]
)
async def test_kundli_performance():
    """Test Kundli API performance"""
    case = TestCase(
        name="Kundli Performance Test",
        scope=TestScope.PERFORMANCE,
        priority=TestPriority.HIGH,
        inputs={
            "requests": [
                {
                    "method": "POST",
                    "endpoint": "/api/v1/kundli/calculate",
                    "body": VALID_KUNDLI_DATA,
                    "headers": {
                        "Content-Type": "application/json",
                        "Authorization": "Bearer test_token"
                    }
                }
            ] * 100  # Run 100 requests
        },
        expected={
            "summary": {
                "successful_requests": 100,
                "failed_requests": 0,
                "avg_response_time": {"max": 1.0}  # Max 1 second average
            }
        }
    )
    return await test_framework.run_case(case)

@security_test(
    name="test_kundli_security",
    priority=TestPriority.CRITICAL,
    tags=["kundli", "security"]
)
async def test_kundli_security():
    """Test Kundli API security"""
    case = TestCase(
        name="Kundli Security Test",
        scope=TestScope.SECURITY,
        priority=TestPriority.CRITICAL,
        inputs={
            "tests": [
                {
                    "name": "authentication",
                    "probes": [
                        {
                            "name": "no_token",
                            "method": "POST",
                            "endpoint": "/api/v1/kundli/calculate",
                            "body": VALID_KUNDLI_DATA
                        },
                        {
                            "name": "invalid_token",
                            "method": "POST",
                            "endpoint": "/api/v1/kundli/calculate",
                            "body": VALID_KUNDLI_DATA,
                            "headers": {
                                "Authorization": "Bearer invalid_token"
                            }
                        }
                    ]
                },
                {
                    "name": "injection",
                    "probes": [
                        {
                            "name": "sql_injection",
                            "method": "GET",
                            "endpoint": "/api/v1/kundli/1' OR '1'='1"
                        },
                        {
                            "name": "xss",
                            "method": "POST",
                            "endpoint": "/api/v1/kundli/calculate",
                            "body": {
                                **VALID_KUNDLI_DATA,
                                "name": "<script>alert('xss')</script>"
                            }
                        }
                    ]
                }
            ]
        },
        expected={
            "authentication": {
                "no_token": {"status_code": 401},
                "invalid_token": {"status_code": 401}
            },
            "injection": {
                "sql_injection": {"status_code": 404},
                "xss": {"status_code": 422}
            }
        }
    )
    return await test_framework.run_case(case)

# Test suite
test_suite = TestSuite(
    name="Kundli API Test Suite",
    description="Comprehensive tests for Kundli calculation API",
    cases=[
        test_calculate_kundli_valid(),
        test_calculate_kundli_invalid(),
        test_kundli_pattern_flow(),
        test_kundli_e2e_flow(),
        test_kundli_performance(),
        test_kundli_security()
    ],
    metadata={
        "version": "1.0.0",
        "owner": "QA Team",
        "priority": "Critical"
    }
)

# Run tests
if __name__ == "__main__":
    import asyncio
    results = asyncio.run(test_framework.run_suite(test_suite))
    
    # Print results
    for result in results:
        print(f"\nTest: {result.case.name}")
        print(f"Status: {result.status}")
        print(f"Duration: {result.duration:.3f}s")
        if result.error:
            print(f"Error: {result.error}")
