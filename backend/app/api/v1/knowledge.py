"""
Knowledge API Endpoints
========================
Expose classical text interpretations with multi-source comparison.

All interpretations are source-attributed with verse citations.
No AI-generated content - only digitized classical texts.
"""

from fastapi import APIRouter, HTTPException, Query
from typing import Optional

from app.core.knowledge.multi_source_comparison import (
    get_planet_in_house_multi_source,
    compare_all_planets_in_house,
    get_source_statistics,
    AgreementLevel
)

router = APIRouter()


@router.get("/planet-in-house/{planet}/{house}")
async def get_planet_in_house_interpretation(
    planet: str,
    house: int,
    sources: Optional[str] = Query(None, description="Comma-separated source names to include (BPHS,Saravali,Phaladeepika,Hora_Sara)")
):
    """
    Get multi-source interpretation for a planet in a house.
    
    Returns interpretations from all available classical sources with:
    - Original verse references
    - Source metadata (author, translator, publication)
    - Multi-source synthesis (common themes)
    - Contradiction detection
    - Agreement level
    
    Example: GET /api/v1/knowledge/planet-in-house/Sun/10
    """
    # Validate inputs
    valid_planets = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"]
    if planet not in valid_planets:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid planet. Must be one of: {', '.join(valid_planets)}"
        )
    
    if house < 1 or house > 12:
        raise HTTPException(
            status_code=400,
            detail="Invalid house. Must be between 1 and 12"
        )
    
    # Get multi-source data
    result = get_planet_in_house_multi_source(planet, house)
    
    # Filter sources if requested
    if sources:
        requested_sources = [s.strip() for s in sources.split(',')]
        result["sources"] = {
            k: v for k, v in result["sources"].items()
            if k in requested_sources
        }
        result["source_count"] = len(result["sources"])
    
    if result["source_count"] == 0:
        raise HTTPException(
            status_code=404,
            detail=f"No interpretations found for {planet} in house {house}"
        )
    
    return result


@router.get("/house/{house}/all-planets")
async def get_all_planets_in_house(house: int):
    """
    Get interpretations for all planets in a specific house.
    
    Useful for understanding the overall themes of a house across all planetary placements.
    
    Example: GET /api/v1/knowledge/house/10/all-planets
    """
    if house < 1 or house > 12:
        raise HTTPException(
            status_code=400,
            detail="Invalid house. Must be between 1 and 12"
        )
    
    result = compare_all_planets_in_house(house)
    return result


@router.get("/statistics")
async def get_knowledge_base_statistics():
    """
    Get statistics about knowledge base coverage.
    
    Returns:
    - Total interpretations count
    - Coverage by source
    - Multi-source coverage breakdown
    - Source metadata
    
    Example: GET /api/v1/knowledge/statistics
    """
    stats = get_source_statistics()
    
    # Add grand total count
    total_interpretations = sum(
        source_data["count"]
        for source_data in stats["coverage_by_source"].values()
    )
    
    stats["total_interpretations"] = total_interpretations
    stats["unique_combinations_covered"] = (
        stats["multi_source_coverage"]["all_4_sources"] +
        stats["multi_source_coverage"]["3_sources"] +
        stats["multi_source_coverage"]["2_sources"] +
        stats["multi_source_coverage"]["1_source"]
    )
    
    return stats


@router.get("/sources")
async def get_source_metadata():
    """
    Get metadata about all classical text sources.
    
    Returns information about:
    - Text name and author
    - Approximate dating
    - Translator and publisher
    - Authority level
    - Chapter references
    
    Example: GET /api/v1/knowledge/sources
    """
    from app.core.knowledge.multi_source_comparison import SourceMetadata
    
    return {
        "sources": SourceMetadata.SOURCES,
        "total_sources": len(SourceMetadata.SOURCES),
        "note": "All interpretations are digitized from these classical texts with verse citations. No AI-generated content."
    }


@router.get("/search")
async def search_interpretations(
    keyword: str = Query(..., min_length=3, description="Search keyword (minimum 3 characters)"),
    planet: Optional[str] = Query(None, description="Filter by planet"),
    house: Optional[int] = Query(None, ge=1, le=12, description="Filter by house"),
    source: Optional[str] = Query(None, description="Filter by source (BPHS, Saravali, Phaladeepika, Hora_Sara)")
):
    """
    Search interpretations by keyword with optional filters.
    
    Searches in:
    - Translations
    - Detailed effects
    - Positive/challenging effects
    
    Example: GET /api/v1/knowledge/search?keyword=wealth&planet=Jupiter
    """
    from app.core.knowledge.sources.bphs_planets_in_houses import BPHS_PLANETS_IN_HOUSES
    from app.core.knowledge.sources.saravali_planets_in_houses import SARAVALI_PLANETS_IN_HOUSES
    from app.core.knowledge.sources.phaladeepika_planets_in_houses import PHALADEEPIKA_PLANETS_IN_HOUSES
    from app.core.knowledge.sources.hora_sara_planets_in_houses import HORA_SARA_PLANETS_IN_HOUSES
    
    sources_data = {
        "BPHS": BPHS_PLANETS_IN_HOUSES,
        "Saravali": SARAVALI_PLANETS_IN_HOUSES,
        "Phaladeepika": PHALADEEPIKA_PLANETS_IN_HOUSES,
        "Hora_Sara": HORA_SARA_PLANETS_IN_HOUSES
    }
    
    # Apply source filter
    if source:
        if source not in sources_data:
            raise HTTPException(status_code=400, detail=f"Invalid source: {source}")
        sources_data = {source: sources_data[source]}
    
    keyword_lower = keyword.lower()
    results = []
    
    for source_name, source_data in sources_data.items():
        for planet_name, houses in source_data.items():
            # Apply planet filter
            if planet and planet_name != planet:
                continue
            
            for house_num, interpretation in houses.items():
                # Apply house filter
                if house and house_num != house:
                    continue
                
                # Search in various fields
                match_found = False
                match_fields = []
                
                # Search translation
                if "translation" in interpretation and keyword_lower in interpretation["translation"].lower():
                    match_found = True
                    match_fields.append("translation")
                
                # Search detailed effects
                if "detailed_effects" in interpretation:
                    for effect in interpretation["detailed_effects"]:
                        if keyword_lower in effect.lower():
                            match_found = True
                            match_fields.append("detailed_effects")
                            break
                
                # Search positive effects
                if "positive_effects" in interpretation:
                    for effect in interpretation["positive_effects"]:
                        if keyword_lower in effect.lower():
                            match_found = True
                            match_fields.append("positive_effects")
                            break
                
                # Search challenging effects
                if "challenging_effects" in interpretation:
                    for effect in interpretation["challenging_effects"]:
                        if keyword_lower in effect.lower():
                            match_found = True
                            match_fields.append("challenging_effects")
                            break
                
                if match_found:
                    results.append({
                        "source": source_name,
                        "planet": planet_name,
                        "house": house_num,
                        "match_fields": list(set(match_fields)),
                        "interpretation": interpretation
                    })
    
    return {
        "keyword": keyword,
        "filters": {
            "planet": planet,
            "house": house,
            "source": source
        },
        "total_results": len(results),
        "results": results[:50]  # Limit to 50 results
    }


@router.get("/compare/{planet}")
async def compare_planet_across_houses(planet: str):
    """
    Compare a single planet's effects across all 12 houses.
    
    Useful for understanding how a planet's energy manifests in different life areas.
    
    Example: GET /api/v1/knowledge/compare/Jupiter
    """
    valid_planets = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]
    if planet not in valid_planets:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid planet. Must be one of: {', '.join(valid_planets)}"
        )
    
    result = {
        "planet": planet,
        "houses": {},
        "summary": {
            "total_houses": 12,
            "houses_with_data": 0,
            "best_houses": [],
            "challenging_houses": []
        }
    }
    
    for house in range(1, 13):
        house_data = get_planet_in_house_multi_source(planet, house)
        result["houses"][house] = house_data
        
        if house_data["source_count"] > 0:
            result["summary"]["houses_with_data"] += 1
            
            # Simple heuristic: more positive effects = better house
            # This is source-based, not AI-generated
            total_positive = 0
            total_challenging = 0
            
            for source_info in house_data["sources"].values():
                interp = source_info["interpretation"]
                if "positive_effects" in interp:
                    total_positive += len(interp["positive_effects"])
                if "challenging_effects" in interp:
                    total_challenging += len(interp["challenging_effects"])
            
            if total_positive > total_challenging:
                result["summary"]["best_houses"].append(house)
            elif total_challenging > total_positive:
                result["summary"]["challenging_houses"].append(house)
    
    return result
