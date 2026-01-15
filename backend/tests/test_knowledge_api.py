"""
Tests for Knowledge API - Multi-Source Classical Text Comparison
=================================================================
Tests the knowledge API endpoints that expose 398 interpretations
from 4 classical sources with verse citations.
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


class TestKnowledgeAPI:
    """Test suite for knowledge API endpoints"""
    
    def test_get_planet_in_house_basic(self):
        """Test basic planet-in-house interpretation retrieval"""
        response = client.get("/api/v1/knowledge/planet-in-house/Sun/10")
        assert response.status_code == 200
        
        data = response.json()
        assert data["planet"] == "Sun"
        assert data["house"] == 10
        assert data["source_count"] > 0
        assert "sources" in data
        assert "synthesis" in data
        assert "metadata" in data
    
    def test_get_planet_in_house_multiple_sources(self):
        """Test that Sun in 10th house has multiple sources (should be all 4)"""
        response = client.get("/api/v1/knowledge/planet-in-house/Sun/10")
        data = response.json()
        
        # Sun in 10th should be covered by all 4 sources
        assert data["source_count"] == 4
        assert "BPHS" in data["sources"]
        assert "Saravali" in data["sources"]
        assert "Phaladeepika" in data["sources"]
        assert "Hora_Sara" in data["sources"]
        
        # Check agreement level
        assert data["agreement_level"] == "unanimous"
    
    def test_source_metadata_included(self):
        """Test that source metadata is properly included"""
        response = client.get("/api/v1/knowledge/planet-in-house/Jupiter/9")
        data = response.json()
        
        for source_name, source_data in data["sources"].items():
            assert "interpretation" in source_data
            assert "metadata" in source_data
            
            metadata = source_data["metadata"]
            assert "full_name" in metadata
            assert "author" in metadata
            assert "translator" in metadata
            assert "chapter_reference" in metadata
    
    def test_verse_citations_present(self):
        """Test that interpretations include verse citations"""
        response = client.get("/api/v1/knowledge/planet-in-house/Mars/3")
        data = response.json()
        
        # Check BPHS has verse citation
        if "BPHS" in data["sources"]:
            interp = data["sources"]["BPHS"]["interpretation"]
            assert "verses" in interp
            assert "translation" in interp
    
    def test_synthesis_generated(self):
        """Test that multi-source synthesis is generated"""
        response = client.get("/api/v1/knowledge/planet-in-house/Venus/7")
        data = response.json()
        
        if data["source_count"] >= 2:
            synthesis = data["synthesis"]
            assert "common_positive_effects" in synthesis
            assert "common_challenging_effects" in synthesis
            assert "unique_insights" in synthesis
    
    def test_invalid_planet(self):
        """Test error handling for invalid planet"""
        response = client.get("/api/v1/knowledge/planet-in-house/Pluto/1")
        assert response.status_code == 400
    
    def test_invalid_house(self):
        """Test error handling for invalid house"""
        response = client.get("/api/v1/knowledge/planet-in-house/Sun/13")
        assert response.status_code == 400
    
    def test_get_all_planets_in_house(self):
        """Test retrieving all planets for a single house"""
        response = client.get("/api/v1/knowledge/house/1/all-planets")
        assert response.status_code == 200
        
        data = response.json()
        assert data["house"] == 1
        assert "planets" in data
        assert "house_summary" in data
        
        # Check that 7 planets are covered (Sun-Saturn)
        assert len(data["planets"]) == 7
        assert "Sun" in data["planets"]
        assert "Saturn" in data["planets"]
    
    def test_knowledge_statistics(self):
        """Test knowledge base statistics endpoint"""
        response = client.get("/api/v1/knowledge/statistics")
        assert response.status_code == 200
        
        data = response.json()
        assert "total_interpretations" in data
        assert "coverage_by_source" in data
        assert "multi_source_coverage" in data
        assert "source_metadata" in data
        
        # Verify we have ~398 interpretations
        assert data["total_interpretations"] >= 398
        
        # Check source coverage
        assert "BPHS" in data["coverage_by_source"]
        assert data["coverage_by_source"]["BPHS"]["count"] == 84
    
    def test_source_metadata_endpoint(self):
        """Test source metadata retrieval"""
        response = client.get("/api/v1/knowledge/sources")
        assert response.status_code == 200
        
        data = response.json()
        assert "sources" in data
        assert "total_sources" == 4
        
        # Check BPHS metadata
        assert "BPHS" in data["sources"]
        bphs = data["sources"]["BPHS"]
        assert bphs["full_name"] == "Brihat Parashara Hora Shastra"
        assert bphs["author"] == "Maharishi Parashara"
        assert "translator" in bphs
    
    def test_search_by_keyword(self):
        """Test keyword search across interpretations"""
        response = client.get("/api/v1/knowledge/search?keyword=wealth")
        assert response.status_code == 200
        
        data = response.json()
        assert data["keyword"] == "wealth"
        assert "results" in data
        assert "total_results" in data
        assert data["total_results"] > 0
    
    def test_search_with_filters(self):
        """Test search with planet and house filters"""
        response = client.get("/api/v1/knowledge/search?keyword=career&planet=Sun&house=10")
        assert response.status_code == 200
        
        data = response.json()
        assert len(data["results"]) > 0
        
        # Verify filters applied
        for result in data["results"]:
            assert result["planet"] == "Sun"
            assert result["house"] == 10
    
    def test_compare_planet_across_houses(self):
        """Test comparing a planet across all 12 houses"""
        response = client.get("/api/v1/knowledge/compare/Jupiter")
        assert response.status_code == 200
        
        data = response.json()
        assert data["planet"] == "Jupiter"
        assert "houses" in data
        assert len(data["houses"]) == 12
        
        summary = data["summary"]
        assert "best_houses" in summary
        assert "challenging_houses" in summary
        assert summary["houses_with_data"] == 12  # Jupiter should be in all sources
    
    def test_source_filtering(self):
        """Test filtering by specific sources"""
        response = client.get("/api/v1/knowledge/planet-in-house/Moon/4?sources=BPHS,Saravali")
        assert response.status_code == 200
        
        data = response.json()
        # Should only have 2 sources
        assert data["source_count"] == 2
        assert "BPHS" in data["sources"]
        assert "Saravali" in data["sources"]
        assert "Phaladeepika" not in data["sources"]
    
    def test_no_ai_generated_content(self):
        """Verify that all content is source-attributed"""
        response = client.get("/api/v1/knowledge/planet-in-house/Saturn/12")
        data = response.json()
        
        # Every source must have metadata
        for source_name, source_data in data["sources"].items():
            assert "metadata" in source_data
            metadata = source_data["metadata"]
            assert "author" in metadata
            assert "translator" in metadata
            
            # Interpretation must have verse reference
            interp = source_data["interpretation"]
            assert "verses" in interp or "chapter" in interp


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
