# Accuracy Test Suite Guide

## Overview

This test suite validates calculation accuracy against Jagannatha Hora (JHora) and Swiss Ephemeris, ensuring our Vedic astrology calculations match professional-grade software.

## Test Files

### 1. `test_lahiri_accuracy.py` ✅
**Status**: Complete

**Tests**:
- Lahiri ayanamsa for years 1950, 2000, 2026
- Ayanamsa progression over time (precession rate)

**Tolerance**: ±0.1° (will tighten to ±0.001° after JHora validation)

**Run**: `pytest backend/tests/accuracy/test_lahiri_accuracy.py -v`

### 2. `test_whole_sign_houses.py` ✅
**Status**: Complete

**Tests**:
- House cusps at sign boundaries (multiples of 30°)
- Ascendant sign determines 1st house
- Sequential house progression (each house = 30°)
- Complete zodiac coverage (12 houses = 360°)
- Time-independence (Whole Sign ignores time within same ascendant sign)

**Run**: `pytest backend/tests/accuracy/test_whole_sign_houses.py -v`

### 3. `test_planet_positions.py` 📝
**Status**: Template ready (needs JHora reference data)

**Will Test**:
- Sidereal longitudes for all 9 planets
- Tropical to sidereal conversion
- Sign placements
- Retrograde detection
- Nakshatra calculations

**Tolerance**: ±0.01° (36 arcseconds)

### 4. `test_dasha_accuracy.py` 📝
**Status**: Template ready (needs JHora reference data)

**Will Test**:
- Vimshottari dasha start dates
- Mahadasha durations
- Antardasha periods
- Balance at birth calculation

**Tolerance**: ±1 day for dates

### 5. `test_divisional_charts.py` 📝
**Status**: Planned

**Will Test**:
- D9 (Navamsa) calculations
- D10 (Dashamsa) calculations
- Divisional ascendant accuracy

## Running Tests

### Run All Accuracy Tests
```bash
cd backend
pytest tests/accuracy/ -v
```

### Run Specific Test File
```bash
pytest tests/accuracy/test_lahiri_accuracy.py -v
```

### Run With Coverage
```bash
pytest tests/accuracy/ -v --cov=app.core.calculations
```

### Run Only Failing Tests
```bash
pytest tests/accuracy/ -v --lf
```

## Creating Reference Data

### Required: JHora Software
1. Download Jagannatha Hora (free Vedic astrology software)
2. Set preferences:
   - Ayanamsa: Lahiri (Chitrapaksha)
   - House System: Whole Sign
3. Generate test charts (see `reference_charts/README.md`)

### Reference Chart Workflow
1. Enter birth data in JHora
2. Export planet positions, houses, dashas
3. Create JSON file in `reference_charts/`
4. Update test file to use reference data
5. Run test and verify match

## Current Status

**Test Coverage**:
- ✅ Lahiri ayanamsa validation (4 tests)
- ✅ Whole Sign house validation (5 tests)
- ⏳ Planet position validation (needs JHora data)
- ⏳ Dasha calculation validation (needs JHora data)
- 📋 Divisional chart validation (planned)

**Reference Charts**:
- 0 JHora reference charts created
- Need: At least 3 diverse test charts

**Next Actions**:
1. Generate JHora reference charts
2. Implement planet position tests
3. Implement dasha tests
4. Tighten tolerance after validation
5. Add edge case tests

## Accuracy Goals

### Phase 1: Core Accuracy ✅
- [x] Lahiri ayanamsa matches Swiss Ephemeris
- [x] Whole Sign houses calculated correctly
- [ ] Planet positions match JHora (±0.01°)

### Phase 2: Advanced Accuracy
- [ ] Dasha periods match JHora (±1 day)
- [ ] Divisional charts match JHora
- [ ] Yoga detection matches classical texts

### Phase 3: Edge Cases
- [ ] Retrograde stations
- [ ] Sign boundary cusps
- [ ] Polar latitude calculations
- [ ] Historical dates (1900-2100)

## Best Practices

1. **Always validate against JHora** - It's the gold standard
2. **Document tolerance levels** - Be explicit about acceptable error
3. **Test edge cases** - Retrograde, boundaries, etc.
4. **Use real birth data** - Tests should reflect real-world usage
5. **Keep reference data** - Don't delete JHora exports

## Troubleshooting

### Test Fails Due to Tolerance
- Check if difference is systematic (offset) or random (calculation error)
- Verify JHora settings match (Lahiri, Whole Sign)
- Consider timezone conversions

### Planet Position Mismatch
- Verify Swiss Ephemeris data files are present
- Check ayanamsa value matches
- Confirm Julian Day calculation is correct

### Dasha Date Mismatch
- Verify birth time accuracy (±4 min can shift dates)
- Check balance at birth calculation
- Confirm mahadasha lord is correct

## Contact

For questions about accuracy validation:
- Check existing GitHub issues
- Review JHora documentation
- Consult classical Vedic astrology texts (BPHS, Saravali)

---

**Last Updated**: 2026-01-10
**Test Suite Version**: 1.0.0
**Status**: Phase 1 in progress
