# Knowledge API Documentation

## Overview

The Knowledge API exposes **398 source-attributed interpretations** from 4 classical Vedic astrology texts with complete verse citations. This is the core differentiation of the Kundli service: **no AI-generated content**, only digitized classical knowledge with multi-source validation.

**Base URL:** `/api/v1/knowledge`

---

## Endpoints

### 1. Get Planet-in-House Interpretation

**GET** `/planet-in-house/{planet}/{house}`

Get multi-source interpretation for a planet in a specific house.

**Parameters:**
- `planet` (path): Planet name - Sun, Moon, Mars, Mercury, Jupiter, Venus, Saturn
- `house` (path): House number (1-12)
- `sources` (query, optional): Comma-separated source names to filter (BPHS,Saravali,Phaladeepika,Hora_Sara)

**Example Request:**
```bash
GET /api/v1/knowledge/planet-in-house/Sun/10
```

**Example Response:**
```json
{
  "planet": "Sun",
  "house": 10,
  "sources": {
    "BPHS": {
      "interpretation": {
        "verses": "24.11",
        "translation": "Sun in the 10th house makes one happy, will have abundant wealth...",
        "detailed_effects": [
          "Outstanding for career and public life",
          "Natural leader in professional sphere",
          "Fame and recognition in chosen field"
        ],
        "positive_effects": ["Exceptional career success", "Natural authority"],
        "challenging_effects": ["Work may consume personal life"],
        "remedies": ["Worship Sun deity for continued success"]
      },
      "metadata": {
        "full_name": "Brihat Parashara Hora Shastra",
        "author": "Maharishi Parashara",
        "translator": "R. Santhanam",
        "chapter_reference": "Chapter 24: Effects of Planets in Twelve Bhavas"
      }
    },
    "Saravali": { /* ... */ },
    "Phaladeepika": { /* ... */ },
    "Hora_Sara": { /* ... */ }
  },
  "source_count": 4,
  "agreement_level": "unanimous",
  "synthesis": {
    "common_positive_effects": [
      {"effect": "career success", "sources": ["BPHS", "Saravali", "Phaladeepika"]}
    ],
    "common_challenging_effects": [],
    "unique_insights": {
      "BPHS": ["May hold positions of power and influence"],
      "Saravali": ["Respected by superiors and subordinates"]
    },
    "remedies": ["Worship Sun deity", "Maintain humility"]
  },
  "contradictions": [],
  "metadata": {
    "total_sources_available": 4,
    "sources_with_data": 4,
    "coverage_percentage": 100,
    "missing_sources": []
  }
}
```

---

### 2. Get All Planets in House

**GET** `/house/{house}/all-planets`

Get interpretations for all 7 planets in a specific house.

**Parameters:**
- `house` (path): House number (1-12)

**Example Request:**
```bash
GET /api/v1/knowledge/house/10/all-planets
```

**Response:** Comparison for Sun, Moon, Mars, Mercury, Jupiter, Venus, Saturn in the specified house.

---

### 3. Get Knowledge Base Statistics

**GET** `/statistics`

Get comprehensive statistics about knowledge base coverage.

**Example Response:**
```json
{
  "total_interpretations": 398,
  "unique_combinations_covered": 84,
  "coverage_by_source": {
    "BPHS": {"count": 84, "percentage": 100},
    "Saravali": {"count": 84, "percentage": 100},
    "Phaladeepika": {"count": 84, "percentage": 100},
    "Hora_Sara": {"count": 64, "percentage": 76.2}
  },
  "multi_source_coverage": {
    "all_4_sources": 64,
    "3_sources": 20,
    "2_sources": 0,
    "1_source": 0,
    "0_sources": 0
  },
  "source_metadata": { /* Full source information */ }
}
```

---

### 4. Get Source Metadata

**GET** `/sources`

Get detailed metadata about all classical text sources.

**Example Response:**
```json
{
  "sources": {
    "BPHS": {
      "full_name": "Brihat Parashara Hora Shastra",
      "author": "Maharishi Parashara",
      "approximate_date": "1500-2000 BCE (traditional dating)",
      "translator": "R. Santhanam",
      "publisher": "Rajan Publications",
      "edition": "1984",
      "authority": "Primary classical text - most authoritative",
      "chapter_reference": "Chapter 24: Effects of Planets in Twelve Bhavas"
    }
    /* ... other sources */
  },
  "total_sources": 4,
  "note": "All interpretations are digitized from these classical texts with verse citations. No AI-generated content."
}
```

---

### 5. Search Interpretations

**GET** `/search`

Search across all interpretations by keyword with optional filters.

**Parameters:**
- `keyword` (query, required): Search keyword (minimum 3 characters)
- `planet` (query, optional): Filter by planet
- `house` (query, optional): Filter by house (1-12)
- `source` (query, optional): Filter by source

**Example Request:**
```bash
GET /api/v1/knowledge/search?keyword=wealth&planet=Jupiter
```

**Example Response:**
```json
{
  "keyword": "wealth",
  "filters": {
    "planet": "Jupiter",
    "house": null,
    "source": null
  },
  "total_results": 15,
  "results": [
    {
      "source": "BPHS",
      "planet": "Jupiter",
      "house": 11,
      "match_fields": ["positive_effects", "translation"],
      "interpretation": { /* Full interpretation data */ }
    }
    /* ... more results */
  ]
}
```

---

### 6. Compare Planet Across Houses

**GET** `/compare/{planet}`

Compare a single planet's effects across all 12 houses.

**Parameters:**
- `planet` (path): Planet name

**Example Request:**
```bash
GET /api/v1/knowledge/compare/Jupiter
```

**Response:** Jupiter's effects in all 12 houses with summary analysis.

---

## Agreement Levels

The API calculates agreement across sources:

- **`unanimous`**: All 4 sources agree (strongest validation)
- **`strong`**: 3 sources agree
- **`moderate`**: 2 sources agree
- **`single_source`**: Only 1 source available
- **`divergent`**: Sources contradict (flagged in response)

---

## Classical Sources

### 1. BPHS (Brihat Parashara Hora Shastra)
- **Author:** Maharishi Parashara
- **Date:** 1500-2000 BCE (traditional)
- **Translator:** R. Santhanam
- **Coverage:** 84/84 combinations (100%)
- **Authority:** Primary classical text - most authoritative

### 2. Saravali
- **Author:** Kalyana Varma
- **Date:** 800-900 CE
- **Translator:** R. Santhanam
- **Coverage:** 84/84 combinations (100%)
- **Authority:** Primary classical text - practical focus

### 3. Phaladeepika
- **Author:** Mantreswara
- **Date:** 15th-16th century CE
- **Translator:** V. Subrahmanya Sastri
- **Coverage:** 84/84 combinations (100%)
- **Authority:** Classical text - predictive techniques

### 4. Hora Sara
- **Author:** Prithuyasas
- **Date:** Unknown (ancient)
- **Translator:** R. Santhanam
- **Coverage:** 64/84 combinations (76%)
- **Authority:** Classical text - detailed predictive focus

---

## Data Integrity Guarantees

### Every Interpretation Includes:
✅ Chapter and verse references  
✅ Original text name and author  
✅ Translator name and publication  
✅ Literal translation from Sanskrit  
✅ Source-attributed effects  

### Never Includes:
❌ AI-generated interpretations  
❌ Modern additions without classical basis  
❌ Unattributed content  
❌ Personal opinions  

---

## Usage Examples

### Example 1: Get Career Indicators

```bash
# Check Sun in 10th (career house)
GET /api/v1/knowledge/planet-in-house/Sun/10

# Compare with Jupiter in 10th
GET /api/v1/knowledge/planet-in-house/Jupiter/10

# Search for all career-related interpretations
GET /api/v1/knowledge/search?keyword=career
```

### Example 2: Verify Multi-Source Agreement

```bash
# Get interpretation with all sources
GET /api/v1/knowledge/planet-in-house/Mars/1

# Check agreement_level in response
# If "unanimous", all 4 sources agree on effects
```

### Example 3: Study a Single Planet

```bash
# Get Jupiter's effects across all 12 houses
GET /api/v1/knowledge/compare/Jupiter

# Identify best and challenging houses
# Response includes "best_houses" and "challenging_houses"
```

### Example 4: Filter by Specific Source

```bash
# Get only BPHS interpretation
GET /api/v1/knowledge/planet-in-house/Venus/7?sources=BPHS

# Compare BPHS vs Saravali
GET /api/v1/knowledge/planet-in-house/Venus/7?sources=BPHS,Saravali
```

---

## Coverage Statistics

**Total:** 398 interpretations  
**Planets:** Sun, Moon, Mars, Mercury, Jupiter, Venus, Saturn (7 planets)  
**Houses:** 1-12 (all houses)  
**Multi-Source:** 100% of combinations have 2+ sources  

**Breakdown:**
- Planets in Houses: 316
- Yogas: 52  
- Dashas: 25
- Retrograde Effects: 5

---

## Error Handling

### Invalid Planet (400)
```json
{
  "detail": "Invalid planet. Must be one of: Sun, Moon, Mars, Mercury, Jupiter, Venus, Saturn"
}
```

### Invalid House (400)
```json
{
  "detail": "Invalid house. Must be between 1 and 12"
}
```

### No Data Found (404)
```json
{
  "detail": "No interpretations found for Mars in house 13"
}
```

---

## Integration with Chart Calculation

The Knowledge API is designed to work seamlessly with the main chart calculation API:

```python
# 1. Calculate chart
chart = POST /api/v1/charts/calculate

# 2. Get interpretations for each planetary placement
for planet, house in chart.planetary_positions:
    interpretation = GET /api/v1/knowledge/planet-in-house/{planet}/{house}
    
    # Access multi-source data
    print(f"{planet} in {house}:")
    print(f"  Sources: {interpretation.source_count}")
    print(f"  Agreement: {interpretation.agreement_level}")
    print(f"  Common effects: {interpretation.synthesis.common_positive_effects}")
```

---

## Future Expansions

Planned additions to the knowledge base:

1. **Rahu & Ketu** in all houses (+192 interpretations)
2. **Additional Yogas** from Saravali, Phaladeepika (+50 interpretations)
3. **Divisional Charts** (D9 Navamsa effects) (+84 interpretations)
4. **Planetary Aspects** (+100+ interpretations)
5. **Brihat Jataka** integration (new classical source)

Target: **1000+ source-attributed interpretations**

---

## Support

For questions or issues with the Knowledge API:
- Check verse citations in responses
- Verify source metadata
- Report discrepancies via GitHub issues
- All interpretations traceable to published classical texts
