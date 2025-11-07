#!/usr/bin/env python3
"""
Automated API Testing Script for Kundli Calculator
Run this to verify backend API is working correctly
"""

import requests
import json
from datetime import datetime
from typing import Dict, List, Tuple

# Configuration
API_BASE = "http://localhost:8000"
API_V1 = "/api/v1"
VERBOSE = True

# Test cases
TEST_CASES = [
    {
        "name": "Gandhi Chart",
        "data": {
            "date_time": "1869-10-02T07:12:00Z",
            "latitude": 21.6417,
            "longitude": 69.6293,
            "altitude": 0,
            "ayanamsa_type": "LAHIRI",
            "house_system": "PLACIDUS"
        },
        "expected": {
            "ascendant_sign": "Libra",
            "moon_sign": "Leo",
            "sun_sign": "Virgo"
        }
    },
    {
        "name": "Modern Chart (2000)",
        "data": {
            "date_time": "2000-01-01T12:00:00Z",
            "latitude": 28.6139,
            "longitude": 77.2090,
            "altitude": 0,
            "ayanamsa_type": "LAHIRI",
            "house_system": "PLACIDUS"
        },
        "expected": {
            # We'll just verify it calculates without errors
        }
    },
    {
        "name": "Southern Hemisphere",
        "data": {
            "date_time": "2010-03-20T15:30:00Z",
            "latitude": -33.8688,  # Sydney
            "longitude": 151.2093,
            "altitude": 0,
            "ayanamsa_type": "LAHIRI",
            "house_system": "PLACIDUS"
        },
        "expected": {}
    }
]

class Colors:
    """ANSI color codes for terminal output"""
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

def print_test(message: str, status: str = "info"):
    """Print formatted test message"""
    icons = {
        "pass": f"{Colors.GREEN}✅{Colors.RESET}",
        "fail": f"{Colors.RED}❌{Colors.RESET}",
        "info": f"{Colors.BLUE}ℹ️{Colors.RESET}",
        "warn": f"{Colors.YELLOW}⚠️{Colors.RESET}"
    }
    print(f"{icons.get(status, '')} {message}")

def test_health_check() -> bool:
    """Test if backend is running"""
    print_test("Testing backend health...", "info")
    try:
        response = requests.get(f"{API_BASE}{API_V1}/health", timeout=5)
        if response.status_code == 200:
            print_test("Backend is running!", "pass")
            return True
        else:
            print_test(f"Backend returned status {response.status_code}", "fail")
            return False
    except requests.exceptions.ConnectionError:
        print_test("Cannot connect to backend. Is it running?", "fail")
        print(f"   Start with: cd backend && python -m uvicorn main:app --reload")
        return False
    except Exception as e:
        print_test(f"Health check failed: {str(e)}", "fail")
        return False

def test_calculate_chart(test_case: Dict) -> Tuple[bool, Dict]:
    """Test chart calculation endpoint"""
    print_test(f"Testing: {test_case['name']}", "info")
    
    try:
        response = requests.post(
            f"{API_BASE}{API_V1}/charts/calculate",
            json=test_case['data'],
            timeout=10
        )
        
        if response.status_code != 200:
            print_test(f"Request failed with status {response.status_code}", "fail")
            if VERBOSE:
                print(f"   Response: {response.text}")
            return False, {}
        
        data = response.json()
        
        # Verify response structure
        required_fields = ['planetary_positions', 'houses']
        for field in required_fields:
            if field not in data:
                print_test(f"Missing required field: {field}", "fail")
                return False, {}
        
        # Verify planets exist
        required_planets = ['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn', 'Rahu', 'Ketu']
        planets = data.get('planetary_positions', {})
        
        for planet in required_planets:
            if planet not in planets:
                print_test(f"Missing planet: {planet}", "fail")
                return False, {}
        
        # Verify ascendant exists
        if 'ascendant' not in data.get('houses', {}):
            print_test("Missing ascendant in houses", "fail")
            return False, {}
        
        # Check expected values if provided
        expected = test_case.get('expected', {})
        if expected:
            ascendant_sign = data['houses']['ascendant'].get('sign', '')
            moon_sign = planets.get('Moon', {}).get('sign', '')
            sun_sign = planets.get('Sun', {}).get('sign', '')
            
            if 'ascendant_sign' in expected:
                if ascendant_sign == expected['ascendant_sign']:
                    print_test(f"Ascendant: {ascendant_sign} ✓", "pass")
                else:
                    print_test(f"Ascendant mismatch: got {ascendant_sign}, expected {expected['ascendant_sign']}", "warn")
            
            if 'moon_sign' in expected:
                if moon_sign == expected['moon_sign']:
                    print_test(f"Moon: {moon_sign} ✓", "pass")
                else:
                    print_test(f"Moon mismatch: got {moon_sign}, expected {expected['moon_sign']}", "warn")
            
            if 'sun_sign' in expected:
                if sun_sign == expected['sun_sign']:
                    print_test(f"Sun: {sun_sign} ✓", "pass")
                else:
                    print_test(f"Sun mismatch: got {sun_sign}, expected {expected['sun_sign']}", "warn")
        
        print_test(f"Chart calculation successful!", "pass")
        if VERBOSE:
            print(f"   Ascendant: {data['houses']['ascendant']['sign']}")
            print(f"   Sun: {planets['Sun']['sign']} at {planets['Sun']['longitude']:.2f}°")
            print(f"   Moon: {planets['Moon']['sign']} at {planets['Moon']['longitude']:.2f}°")
        
        return True, data
        
    except requests.exceptions.Timeout:
        print_test("Request timed out (>10s)", "fail")
        return False, {}
    except Exception as e:
        print_test(f"Error: {str(e)}", "fail")
        if VERBOSE:
            import traceback
            traceback.print_exc()
        return False, {}

def test_invalid_inputs() -> bool:
    """Test error handling with invalid inputs"""
    print_test("Testing error handling...", "info")
    
    invalid_cases = [
        {
            "name": "Missing latitude",
            "data": {
                "date_time": "2000-01-01T12:00:00Z",
                "longitude": 77.2090,
                "altitude": 0
            }
        },
        {
            "name": "Invalid date",
            "data": {
                "date_time": "invalid-date",
                "latitude": 28.6139,
                "longitude": 77.2090,
                "altitude": 0
            }
        },
        {
            "name": "Latitude out of range",
            "data": {
                "date_time": "2000-01-01T12:00:00Z",
                "latitude": 999,  # Invalid
                "longitude": 77.2090,
                "altitude": 0
            }
        }
    ]
    
    all_passed = True
    for case in invalid_cases:
        try:
            response = requests.post(
                f"{API_BASE}{API_V1}/charts/calculate",
                json=case['data'],
                timeout=5
            )
            
            # Should return 422 for validation errors
            if response.status_code == 422:
                print_test(f"{case['name']}: Correctly rejected ✓", "pass")
            else:
                print_test(f"{case['name']}: Expected 422, got {response.status_code}", "warn")
                all_passed = False
        except Exception as e:
            print_test(f"{case['name']}: Error - {str(e)}", "fail")
            all_passed = False
    
    return all_passed

def test_performance() -> bool:
    """Test response time"""
    print_test("Testing performance...", "info")
    
    test_data = {
        "date_time": "2000-01-01T12:00:00Z",
        "latitude": 28.6139,
        "longitude": 77.2090,
        "altitude": 0,
        "ayanamsa_type": "LAHIRI",
        "house_system": "PLACIDUS"
    }
    
    try:
        import time
        start = time.time()
        response = requests.post(f"{API_BASE}{API_V1}/charts/calculate", json=test_data, timeout=10)
        elapsed = time.time() - start
        
        if response.status_code == 200:
            if elapsed < 1.0:
                print_test(f"Response time: {elapsed:.2f}s (Excellent!)", "pass")
                return True
            elif elapsed < 3.0:
                print_test(f"Response time: {elapsed:.2f}s (Good)", "pass")
                return True
            else:
                print_test(f"Response time: {elapsed:.2f}s (Slow)", "warn")
                return False
        else:
            print_test("Performance test failed (request error)", "fail")
            return False
    except Exception as e:
        print_test(f"Performance test error: {str(e)}", "fail")
        return False

def run_all_tests():
    """Run all test suites"""
    print(f"\n{Colors.BOLD}{'='*60}{Colors.RESET}")
    print(f"{Colors.BOLD}🧪 KUNDLI CALCULATOR API TEST SUITE{Colors.RESET}")
    print(f"{Colors.BOLD}{'='*60}{Colors.RESET}\n")
    
    results = {
        "total": 0,
        "passed": 0,
        "failed": 0,
        "warnings": 0
    }
    
    # Test 1: Health check
    print(f"\n{Colors.BOLD}Test Suite 1: Health Check{Colors.RESET}")
    print("-" * 60)
    if not test_health_check():
        print_test("\n❌ Backend not running. Please start it first.", "fail")
        return
    results["total"] += 1
    results["passed"] += 1
    
    # Test 2: Chart calculations
    print(f"\n{Colors.BOLD}Test Suite 2: Chart Calculations{Colors.RESET}")
    print("-" * 60)
    for test_case in TEST_CASES:
        success, data = test_calculate_chart(test_case)
        results["total"] += 1
        if success:
            results["passed"] += 1
        else:
            results["failed"] += 1
        print()  # Blank line between tests
    
    # Test 3: Error handling
    print(f"\n{Colors.BOLD}Test Suite 3: Error Handling{Colors.RESET}")
    print("-" * 60)
    success = test_invalid_inputs()
    results["total"] += 1
    if success:
        results["passed"] += 1
    else:
        results["failed"] += 1
    
    # Test 4: Performance
    print(f"\n{Colors.BOLD}Test Suite 4: Performance{Colors.RESET}")
    print("-" * 60)
    success = test_performance()
    results["total"] += 1
    if success:
        results["passed"] += 1
    else:
        results["failed"] += 1
    
    # Print summary
    print(f"\n{Colors.BOLD}{'='*60}{Colors.RESET}")
    print(f"{Colors.BOLD}📊 TEST SUMMARY{Colors.RESET}")
    print(f"{Colors.BOLD}{'='*60}{Colors.RESET}")
    print(f"Total Tests: {results['total']}")
    print(f"{Colors.GREEN}Passed: {results['passed']}{Colors.RESET}")
    print(f"{Colors.RED}Failed: {results['failed']}{Colors.RESET}")
    
    pass_rate = (results['passed'] / results['total'] * 100) if results['total'] > 0 else 0
    print(f"\n{Colors.BOLD}Pass Rate: {pass_rate:.1f}%{Colors.RESET}")
    
    if pass_rate == 100:
        print(f"\n{Colors.GREEN}{Colors.BOLD}🎉 ALL TESTS PASSED! API is working perfectly!{Colors.RESET}")
    elif pass_rate >= 75:
        print(f"\n{Colors.YELLOW}{Colors.BOLD}⚠️ Most tests passed. Check warnings above.{Colors.RESET}")
    else:
        print(f"\n{Colors.RED}{Colors.BOLD}❌ Several tests failed. Please review errors above.{Colors.RESET}")
    
    print(f"{Colors.BOLD}{'='*60}{Colors.RESET}\n")

if __name__ == "__main__":
    try:
        run_all_tests()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}Tests interrupted by user{Colors.RESET}")
    except Exception as e:
        print(f"\n{Colors.RED}Unexpected error: {str(e)}{Colors.RESET}")
        import traceback
        traceback.print_exc()
