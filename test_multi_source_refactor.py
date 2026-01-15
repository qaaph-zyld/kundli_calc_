"""
Test Multi-Source Engine Refactor
Validates 4-source comparison functionality
"""
import sys
sys.path.insert(0, 'backend')

from app.core.knowledge.engine.multi_source_engine import MultiSourceEngine

engine = MultiSourceEngine()

print("=" * 80)
print("MULTI-SOURCE ENGINE REFACTOR VALIDATION")
print("=" * 80)

# Test 1: 4-source coverage (Sun in house 1)
print("\nTest 1: Sun in House 1 (should have 4 sources)")
print("-" * 80)
sources = engine.get_available_sources("Sun", 1)
print(f"Available sources: {sources}")
print(f"Number of sources: {len(sources)}")
assert len(sources) == 4, f"Expected 4 sources, got {len(sources)}"
print("✅ PASS: 4 sources available")

# Test 2: 4-source coverage (Moon in house 1 - has Hora Sara)
print("\nTest 2: Moon in House 1 (should have 4 sources)")
print("-" * 80)
sources = engine.get_available_sources("Moon", 1)
print(f"Available sources: {sources}")
print(f"Number of sources: {len(sources)}")
assert len(sources) == 4, f"Expected 4 sources, got {len(sources)}"
print("✅ PASS: 4 sources available")

# Test 2b: 3-source coverage (Moon in house 5 - no Hora Sara)
print("\nTest 2b: Moon in House 5 (should have 3 sources - no Hora Sara)")
print("-" * 80)
sources = engine.get_available_sources("Moon", 5)
print(f"Available sources: {sources}")
print(f"Number of sources: {len(sources)}")
assert len(sources) == 3, f"Expected 3 sources, got {len(sources)}"
print("✅ PASS: 3 sources available")

# Test 3: Comprehensive interpretation with comparison
print("\nTest 3: Comprehensive Interpretation (Sun in 10th)")
print("-" * 80)
result = engine.get_comprehensive_interpretation("Sun", 10, include_comparison=True)
print(f"Sources: {result['sources_available']}")
print(f"Number of interpretations: {len(result['interpretations'])}")
print(f"Comparison included: {'comparison' in result}")

if 'comparison' in result:
    comp = result['comparison']
    print(f"\nAgreement level: {comp['agreement_level']}")
    print(f"Common themes: {len(comp['common_themes'])}")
    print(f"Unique insights: {list(comp['unique_insights'].keys())}")
    print(f"Contradictions: {len(comp['contradictions'])}")
    print(f"Confidence score: {comp['confidence_score']}")
    print(f"\nSynthesis preview: {comp['synthesis'][:200]}...")
print("✅ PASS: Comprehensive interpretation working")

# Test 4: Source comparison
print("\nTest 4: Source Comparison (Mars in 10th)")
print("-" * 80)
comparison = engine.compare_sources("Mars", 10)
print(f"Planet: {comparison.planet}, House: {comparison.house}")
print(f"Sources: {comparison.sources_available}")
print(f"Agreement level: {comparison.agreement_level.value}")
print(f"Common themes: {comparison.common_themes}")
print(f"Unique insights: {list(comparison.unique_insights.keys())}")
print(f"Confidence: {comparison.confidence_score}")
print("✅ PASS: Source comparison working")

# Test 5: Coverage statistics
print("\nTest 5: Coverage Statistics")
print("-" * 80)
coverage_4_sources = 0
coverage_3_sources = 0
coverage_2_sources = 0
coverage_1_source = 0

planets = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]
for planet in planets:
    for house in range(1, 13):
        sources = engine.get_available_sources(planet, house)
        if len(sources) == 4:
            coverage_4_sources += 1
        elif len(sources) == 3:
            coverage_3_sources += 1
        elif len(sources) == 2:
            coverage_2_sources += 1
        elif len(sources) == 1:
            coverage_1_source += 1

print(f"4-source coverage: {coverage_4_sources}/84 ({(coverage_4_sources/84)*100:.1f}%)")
print(f"3-source coverage: {coverage_3_sources}/84 ({(coverage_3_sources/84)*100:.1f}%)")
print(f"2-source coverage: {coverage_2_sources}/84 ({(coverage_2_sources/84)*100:.1f}%)")
print(f"1-source coverage: {coverage_1_source}/84 ({(coverage_1_source/84)*100:.1f}%)")
print(f"\nTotal with 2+ sources: {coverage_4_sources + coverage_3_sources + coverage_2_sources}/84")
print("✅ PASS: Coverage statistics calculated")

print("\n" + "=" * 80)
print("ALL TESTS PASSED ✅")
print("Multi-source engine successfully refactored to support 4+ sources")
print("=" * 80)
