"""
Quick test script for multi-source API endpoints
"""

import sys
import asyncio
from backend.app.api.endpoints.interpretations import (
    compare_sources,
    get_comprehensive_interpretation,
    list_available_combinations,
    demo_sun_first_comparison
)

async def test_endpoints():
    """Test the new multi-source endpoints"""
    
    print("=" * 80)
    print("TESTING MULTI-SOURCE API ENDPOINTS")
    print("=" * 80)
    
    # Test 1: Compare sources
    print("\n1. Testing compare_sources endpoint...")
    try:
        result = await compare_sources(planet="Sun", house=1)
        print(f"   ✓ Success: {result['planet']} in house {result['house']}")
        print(f"   Sources: {result['sources_available']}")
        print(f"   Agreement: {result['agreement_level']}")
        print(f"   Confidence: {result['confidence_score']}")
    except Exception as e:
        print(f"   ✗ Error: {e}")
    
    # Test 2: Comprehensive interpretation
    print("\n2. Testing comprehensive interpretation...")
    try:
        result = await get_comprehensive_interpretation(planet="Jupiter", house=1, include_comparison=True)
        print(f"   ✓ Success: {result['planet']} in house {result['house']}")
        print(f"   Sources available: {len(result['sources_available'])}")
        has_comp = 'comparison' in result
        print(f"   Has comparison: {has_comp}")
    except Exception as e:
        print(f"   ✗ Error: {e}")
    
    # Test 3: List combinations
    print("\n3. Testing list_available_combinations...")
    try:
        result = await list_available_combinations()
        print(f"   ✓ Success: {result['statistics']['total_combinations']} combinations")
        print(f"   Multi-source: {result['statistics']['multi_source']}")
        print(f"   Coverage: {result['coverage_rate']['percentage']}%")
    except Exception as e:
        print(f"   ✗ Error: {e}")
    
    # Test 4: Demo endpoint
    print("\n4. Testing demo endpoint...")
    try:
        result = await demo_sun_first_comparison()
        print(f"   ✓ Success: {result['demo']}")
        print(f"   Agreement: {result['agreement_level']}")
        print(f"   Confidence: {result['confidence_score']}")
    except Exception as e:
        print(f"   ✗ Error: {e}")
    
    print("\n" + "=" * 80)
    print("ALL ENDPOINT TESTS COMPLETED")
    print("=" * 80)

if __name__ == "__main__":
    asyncio.run(test_endpoints())
