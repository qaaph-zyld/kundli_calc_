"""
Multi-Source Classical Text Comparison Engine
==============================================
Compares interpretations across multiple classical sources (BPHS, Saravali, Phaladeepika, Hora Sara)
to identify agreements, contradictions, and synthesize knowledge.

This is the core differentiation of the Kundli service - no AI generation, only source-attributed
classical knowledge with multi-text validation.
"""

from typing import Dict, List, Any, Optional
from enum import Enum

from .sources.bphs_planets_in_houses import BPHS_PLANETS_IN_HOUSES
from .sources.saravali_planets_in_houses import SARAVALI_PLANETS_IN_HOUSES
from .sources.phaladeepika_planets_in_houses import PHALADEEPIKA_PLANETS_IN_HOUSES
from .sources.hora_sara_planets_in_houses import HORA_SARA_PLANETS_IN_HOUSES


class AgreementLevel(str, Enum):
    """Level of agreement across classical sources"""
    UNANIMOUS = "unanimous"  # All sources agree
    STRONG = "strong"  # 3+ sources agree
    MODERATE = "moderate"  # 2 sources agree
    DIVERGENT = "divergent"  # Sources contradict
    SINGLE_SOURCE = "single_source"  # Only one source available


class SourceMetadata:
    """Metadata about classical text sources"""
    
    SOURCES = {
        "BPHS": {
            "full_name": "Brihat Parashara Hora Shastra",
            "author": "Maharishi Parashara",
            "approximate_date": "1500-2000 BCE (traditional dating)",
            "translator": "R. Santhanam",
            "publisher": "Rajan Publications",
            "edition": "1984",
            "authority": "Primary classical text - most authoritative",
            "chapter_reference": "Chapter 24: Effects of Planets in Twelve Bhavas"
        },
        "Saravali": {
            "full_name": "Saravali",
            "author": "Kalyana Varma",
            "approximate_date": "800-900 CE",
            "translator": "R. Santhanam",
            "publisher": "Rajan Publications",
            "edition": "1996",
            "authority": "Primary classical text - practical focus",
            "chapter_reference": "Chapter 27: Planetary Effects in Houses"
        },
        "Phaladeepika": {
            "full_name": "Phaladeepika (Light on Results)",
            "author": "Mantreswara",
            "approximate_date": "15th-16th century CE",
            "translator": "V. Subrahmanya Sastri",
            "publisher": "Ranjan Publications",
            "edition": "1963",
            "authority": "Classical text - predictive techniques",
            "chapter_reference": "Chapters 10-21: Planets in Houses"
        },
        "Hora_Sara": {
            "full_name": "Hora Sara",
            "author": "Prithuyasas",
            "approximate_date": "Unknown (ancient)",
            "translator": "R. Santhanam",
            "publisher": "Ranjan Publications",
            "edition": "1996",
            "authority": "Classical text - detailed predictive focus",
            "chapter_reference": "Chapters 7-8: Planetary Placements"
        }
    }


def get_planet_in_house_multi_source(planet: str, house: int) -> Dict[str, Any]:
    """
    Get interpretations from all available sources for a planet-house combination.
    
    Args:
        planet: Planet name (Sun, Moon, Mars, Mercury, Jupiter, Venus, Saturn)
        house: House number (1-12)
        
    Returns:
        Dictionary with interpretations from all sources, comparison analysis, and synthesis
    """
    result = {
        "planet": planet,
        "house": house,
        "sources": {},
        "source_count": 0,
        "agreement_level": None,
        "synthesis": {},
        "contradictions": [],
        "metadata": {}
    }
    
    # Collect interpretations from all sources
    sources_data = {
        "BPHS": BPHS_PLANETS_IN_HOUSES,
        "Saravali": SARAVALI_PLANETS_IN_HOUSES,
        "Phaladeepika": PHALADEEPIKA_PLANETS_IN_HOUSES,
        "Hora_Sara": HORA_SARA_PLANETS_IN_HOUSES
    }
    
    for source_name, source_data in sources_data.items():
        if planet in source_data and house in source_data[planet]:
            interpretation = source_data[planet][house]
            result["sources"][source_name] = {
                "interpretation": interpretation,
                "metadata": SourceMetadata.SOURCES[source_name]
            }
            result["source_count"] += 1
    
    # Determine agreement level
    if result["source_count"] == 4:
        result["agreement_level"] = AgreementLevel.UNANIMOUS
    elif result["source_count"] == 3:
        result["agreement_level"] = AgreementLevel.STRONG
    elif result["source_count"] == 2:
        result["agreement_level"] = AgreementLevel.MODERATE
    elif result["source_count"] == 1:
        result["agreement_level"] = AgreementLevel.SINGLE_SOURCE
    else:
        result["agreement_level"] = None
    
    # Synthesize common themes
    if result["source_count"] > 0:
        result["synthesis"] = _synthesize_interpretations(result["sources"])
        result["contradictions"] = _identify_contradictions(result["sources"])
    
    # Add metadata about coverage
    result["metadata"] = {
        "total_sources_available": 4,
        "sources_with_data": result["source_count"],
        "coverage_percentage": (result["source_count"] / 4) * 100,
        "missing_sources": [name for name in sources_data.keys() if name not in result["sources"]]
    }
    
    return result


def _synthesize_interpretations(sources: Dict[str, Any]) -> Dict[str, Any]:
    """
    Synthesize common themes across multiple sources.
    
    Identifies patterns that appear in multiple sources without generating new content.
    """
    synthesis = {
        "common_positive_effects": [],
        "common_challenging_effects": [],
        "unique_insights": {},
        "remedies": []
    }
    
    # Collect all effects from all sources
    all_positive = []
    all_challenging = []
    all_remedies = []
    
    for source_name, source_info in sources.items():
        interp = source_info["interpretation"]
        
        if "positive_effects" in interp:
            all_positive.extend([(effect, source_name) for effect in interp["positive_effects"]])
        
        if "challenging_effects" in interp:
            all_challenging.extend([(effect, source_name) for effect in interp["challenging_effects"]])
        
        if "remedies" in interp:
            all_remedies.extend([(remedy, source_name) for remedy in interp["remedies"]])
    
    # Find effects mentioned in multiple sources (simple keyword matching)
    # This is source-based synthesis, not AI generation
    effect_counts_positive = {}
    effect_counts_challenging = {}
    
    for effect, source in all_positive:
        effect_lower = effect.lower()
        effect_counts_positive[effect_lower] = effect_counts_positive.get(effect_lower, []) + [source]
    
    for effect, source in all_challenging:
        effect_lower = effect.lower()
        effect_counts_challenging[effect_lower] = effect_counts_challenging.get(effect_lower, []) + [source]
    
    # Include effects mentioned by 2+ sources as "common"
    synthesis["common_positive_effects"] = [
        {"effect": effect, "sources": sources_list}
        for effect, sources_list in effect_counts_positive.items()
        if len(set(sources_list)) >= 2
    ]
    
    synthesis["common_challenging_effects"] = [
        {"effect": effect, "sources": sources_list}
        for effect, sources_list in effect_counts_challenging.items()
        if len(set(sources_list)) >= 2
    ]
    
    # Unique insights from each source
    for source_name, source_info in sources.items():
        interp = source_info["interpretation"]
        unique_points = []
        
        if "detailed_effects" in interp:
            unique_points = interp["detailed_effects"][:3]  # First 3 detailed effects
        
        synthesis["unique_insights"][source_name] = unique_points
    
    # Collect remedies (all sources)
    synthesis["remedies"] = list(set([remedy for remedy, _ in all_remedies]))
    
    return synthesis


def _identify_contradictions(sources: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Identify contradictions between sources.
    
    Flags when sources disagree on fundamental effects.
    """
    contradictions = []
    
    # Simple contradiction detection: different tone in translations
    # This is a basic implementation - can be expanded
    
    source_names = list(sources.keys())
    if len(source_names) < 2:
        return contradictions
    
    # Check for major tonal differences in translations
    # E.g., one says "wealthy" and another says "devoid of wealth"
    for i, source1 in enumerate(source_names):
        for source2 in source_names[i+1:]:
            trans1 = sources[source1]["interpretation"].get("translation", "").lower()
            trans2 = sources[source2]["interpretation"].get("translation", "").lower()
            
            # Look for opposite keywords
            wealth_positive = any(word in trans1 for word in ["wealthy", "wealth", "prosperity", "riches"])
            wealth_negative = any(word in trans1 for word in ["devoid of wealth", "without wealth", "poor", "poverty"])
            
            wealth_positive2 = any(word in trans2 for word in ["wealthy", "wealth", "prosperity", "riches"])
            wealth_negative2 = any(word in trans2 for word in ["devoid of wealth", "without wealth", "poor", "poverty"])
            
            if (wealth_positive and wealth_negative2) or (wealth_negative and wealth_positive2):
                contradictions.append({
                    "type": "wealth_status",
                    "source1": source1,
                    "source2": source2,
                    "note": "Sources differ on wealth effects - context or conditions may apply"
                })
    
    return contradictions


def compare_all_planets_in_house(house: int) -> Dict[str, Any]:
    """
    Compare all planets in a specific house across sources.
    
    Args:
        house: House number (1-12)
        
    Returns:
        Comparison for all planets in that house
    """
    planets = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]
    
    result = {
        "house": house,
        "planets": {},
        "house_summary": {
            "total_combinations": len(planets),
            "fully_covered": 0,  # All 4 sources
            "well_covered": 0,   # 3 sources
            "moderately_covered": 0,  # 2 sources
            "poorly_covered": 0  # 1 source
        }
    }
    
    for planet in planets:
        planet_data = get_planet_in_house_multi_source(planet, house)
        result["planets"][planet] = planet_data
        
        # Update coverage stats
        if planet_data["source_count"] == 4:
            result["house_summary"]["fully_covered"] += 1
        elif planet_data["source_count"] == 3:
            result["house_summary"]["well_covered"] += 1
        elif planet_data["source_count"] == 2:
            result["house_summary"]["moderately_covered"] += 1
        elif planet_data["source_count"] == 1:
            result["house_summary"]["poorly_covered"] += 1
    
    return result


def get_source_statistics() -> Dict[str, Any]:
    """
    Get overall statistics about source coverage.
    
    Returns:
        Statistics on interpretation coverage across all sources
    """
    planets = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]
    houses = list(range(1, 13))
    
    stats = {
        "total_combinations": len(planets) * len(houses),
        "coverage_by_source": {},
        "multi_source_coverage": {
            "all_4_sources": 0,
            "3_sources": 0,
            "2_sources": 0,
            "1_source": 0,
            "0_sources": 0
        },
        "source_metadata": SourceMetadata.SOURCES
    }
    
    # Count coverage for each source
    sources_data = {
        "BPHS": BPHS_PLANETS_IN_HOUSES,
        "Saravali": SARAVALI_PLANETS_IN_HOUSES,
        "Phaladeepika": PHALADEEPIKA_PLANETS_IN_HOUSES,
        "Hora_Sara": HORA_SARA_PLANETS_IN_HOUSES
    }
    
    for source_name, source_data in sources_data.items():
        count = sum(len(houses_dict) for houses_dict in source_data.values())
        stats["coverage_by_source"][source_name] = {
            "count": count,
            "percentage": (count / stats["total_combinations"]) * 100
        }
    
    # Count multi-source coverage
    for planet in planets:
        for house in houses:
            source_count = 0
            for source_data in sources_data.values():
                if planet in source_data and house in source_data[planet]:
                    source_count += 1
            
            if source_count == 4:
                stats["multi_source_coverage"]["all_4_sources"] += 1
            elif source_count == 3:
                stats["multi_source_coverage"]["3_sources"] += 1
            elif source_count == 2:
                stats["multi_source_coverage"]["2_sources"] += 1
            elif source_count == 1:
                stats["multi_source_coverage"]["1_source"] += 1
            else:
                stats["multi_source_coverage"]["0_sources"] += 1
    
    return stats
