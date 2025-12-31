"""Calculation Metadata and Transparency Module
===============================================
Provides metadata about calculations including formulas, sources, and methods.

This module supports the goal of calculation transparency by documenting:
- Formulas used for each calculation
- Academic/classical sources (BPHS, Swiss Ephemeris, etc.)
- Calculation methods and algorithms
- Accuracy standards and tolerances

Author: Kundli Calculation Engine
Date: 2024-12-31
"""

from typing import Dict, List, Optional, Any
from enum import Enum


class CalculationType(str, Enum):
    """Types of calculations performed."""
    PLANETARY_POSITION = "planetary_position"
    HOUSE_CALCULATION = "house_calculation"
    DIVISIONAL_CHART = "divisional_chart"
    DASHA_SYSTEM = "dasha_system"
    SHADBALA = "shadbala"
    ASHTAKAVARGA = "ashtakavarga"
    YOGA_DETECTION = "yoga_detection"
    AYANAMSA = "ayanamsa"
    PANCHANG = "panchang"
    KP_SYSTEM = "kp_system"
    NAKSHATRA = "nakshatra"
    COMPATIBILITY = "compatibility"
    TRANSIT = "transit"


class CalculationMetadata:
    """Provides metadata for various astrological calculations."""
    
    @staticmethod
    def get_planetary_position_metadata() -> Dict[str, Any]:
        """Metadata for planetary position calculations."""
        return {
            "type": CalculationType.PLANETARY_POSITION,
            "method": "Swiss Ephemeris DE431",
            "accuracy": "±0.01 arc seconds",
            "source": "Swiss Ephemeris library by Astrodienst",
            "reference": "https://www.astro.com/swisseph/",
            "formula": "Tropical longitude - Ayanamsa = Sidereal longitude",
            "notes": [
                "Uses JPL DE431 ephemeris data",
                "Sub-arc-second precision for modern dates",
                "Accounts for nutation and aberration"
            ]
        }
    
    @staticmethod
    def get_ayanamsa_metadata(system: str = "Lahiri") -> Dict[str, Any]:
        """Metadata for ayanamsa calculations."""
        metadata = {
            "type": CalculationType.AYANAMSA,
            "system": system,
            "method": "Swiss Ephemeris calculation",
            "accuracy": "±0.001 degrees",
            "annual_precession": "~50.27 arc seconds/year"
        }
        
        system_specific = {
            "Lahiri": {
                "full_name": "Lahiri Chitrapaksha",
                "reference_year": 1900,
                "reference_value": "22.46 degrees",
                "source": "Indian Government standard (1956)",
                "formula": "Ayanamsa = 22.46° + (Year - 1900) × 50.27″/year",
                "zero_year": "285 CE (approx)",
                "notes": [
                    "Official ayanamsa for Indian ephemeris",
                    "Based on Spica (Chitra) at 180°",
                    "Matches BPHS traditional calculations"
                ]
            },
            "KP": {
                "full_name": "Krishnamurti Paddhati",
                "reference_year": 1900,
                "reference_value": "22.362222 degrees",
                "source": "K.S. Krishnamurti",
                "formula": "Ayanamsa = 22.3622° + (Year - 1900) × 50.27″/year",
                "notes": [
                    "~6 arc minutes less than Lahiri",
                    "Used in KP system exclusively"
                ]
            },
            "Raman": {
                "full_name": "B.V. Raman's Ayanamsa",
                "reference_year": 1900,
                "reference_value": "22.38 degrees",
                "source": "B.V. Raman",
                "notes": [
                    "Slight variation from Lahiri",
                    "Popular in South Indian astrology"
                ]
            }
        }
        
        if system in system_specific:
            metadata.update(system_specific[system])
        
        return metadata
    
    @staticmethod
    def get_house_system_metadata(system: str = "Whole Sign") -> Dict[str, Any]:
        """Metadata for house system calculations."""
        metadata = {
            "type": CalculationType.HOUSE_CALCULATION,
            "system": system,
            "method": "Mathematical division of ecliptic"
        }
        
        system_specific = {
            "Whole Sign": {
                "formula": "Each sign (30°) = One house",
                "house_1_cusp": "Start of Ascendant sign",
                "source": "Classical Vedic astrology (BPHS)",
                "reference": "Brihat Parashara Hora Shastra, Ch. 14",
                "advantages": [
                    "Simplest and most ancient system",
                    "No house size variation",
                    "Clear sign-house correlation"
                ],
                "calculation": "House N = (Ascendant_Sign + N - 1) mod 12",
                "notes": [
                    "Default system in Vedic astrology",
                    "Each house exactly 30 degrees",
                    "Ascendant degree determines all house cusps"
                ]
            },
            "Placidus": {
                "formula": "Trisection of semi-arcs",
                "source": "Placidus de Titis (1688)",
                "calculation": "Based on time divisions of Earth's rotation",
                "notes": [
                    "Most popular in Western astrology",
                    "Variable house sizes",
                    "Difficult at high latitudes"
                ]
            },
            "Equal": {
                "formula": "30° divisions from Ascendant degree",
                "calculation": "House N = Ascendant_Long + (N - 1) × 30°",
                "notes": [
                    "Equal 30° houses",
                    "Different from Whole Sign (uses degree, not sign)"
                ]
            }
        }
        
        if system in system_specific:
            metadata.update(system_specific[system])
        
        return metadata
    
    @staticmethod
    def get_shadbala_metadata() -> Dict[str, Any]:
        """Metadata for Shadbala calculations."""
        return {
            "type": CalculationType.SHADBALA,
            "method": "Six-fold planetary strength per BPHS",
            "source": "Brihat Parashara Hora Shastra, Chapter 27",
            "units": "Shashtiamsas (1 Rupa = 60 Shashtiamsas)",
            "components": {
                "Sthana Bala": {
                    "description": "Positional strength",
                    "sub_components": [
                        "Uccha Bala (Exaltation strength)",
                        "Saptavargaja Bala (7 divisional charts)",
                        "Ojhayugma Bala (Odd/even sign)",
                        "Kendra Bala (Angular house)",
                        "Drekkana Bala (Decanate)"
                    ],
                    "formula": "Sum of 5 sub-components"
                },
                "Dig Bala": {
                    "description": "Directional strength",
                    "max_value": "60 Shashtiamsas",
                    "best_houses": {
                        "Sun": 10, "Moon": 4, "Mars": 10,
                        "Mercury": 1, "Jupiter": 1, "Venus": 4, "Saturn": 7
                    },
                    "formula": "60 × (1 - angular_distance/180°)"
                },
                "Kala Bala": {
                    "description": "Temporal strength",
                    "sub_components": [
                        "Nathonnatha (Day/night)",
                        "Paksha (Lunar fortnight)",
                        "Vara (Weekday)"
                    ],
                    "notes": ["Time-dependent strength"]
                },
                "Chesta Bala": {
                    "description": "Motional strength",
                    "max_value": "60 Shashtiamsas",
                    "notes": [
                        "Not applicable to Sun and Moon",
                        "Maximum for retrograde planets",
                        "Based on daily speed variation"
                    ]
                },
                "Naisargika Bala": {
                    "description": "Natural/inherent strength",
                    "values": {
                        "Sun": 60.0, "Moon": 51.43, "Mars": 17.14,
                        "Mercury": 25.71, "Jupiter": 34.29,
                        "Venus": 42.86, "Saturn": 8.57
                    },
                    "notes": ["Fixed values per BPHS"]
                },
                "Drik Bala": {
                    "description": "Aspectual strength",
                    "notes": [
                        "Based on aspects received",
                        "Benefic aspects add strength",
                        "Malefic aspects reduce strength"
                    ]
                }
            },
            "minimum_required": {
                "description": "Minimum Shadbala in Rupas for planet to be strong",
                "values": {
                    "Sun": 6.5, "Moon": 6.0, "Mars": 5.0,
                    "Mercury": 7.0, "Jupiter": 6.5,
                    "Venus": 5.5, "Saturn": 5.0
                }
            },
            "interpretation": {
                ">=150%": "Excellent strength",
                "120-150%": "Very good strength",
                "100-120%": "Good strength (meets minimum)",
                "80-100%": "Fair strength (slightly weak)",
                "60-80%": "Weak",
                "<60%": "Very weak"
            }
        }
    
    @staticmethod
    def get_ashtakavarga_metadata() -> Dict[str, Any]:
        """Metadata for Ashtakavarga calculations."""
        return {
            "type": CalculationType.ASHTAKAVARGA,
            "method": "Eight-fold benefic point system",
            "source": "Brihat Parashara Hora Shastra, Chapters 51-52",
            "reference": "Also: Phaladeepika Ch. 9, Saravali Ch. 38",
            "description": "Measures benefic points (bindus) contributed to each house",
            "reference_points": [
                "Lagna", "Sun", "Moon", "Mars",
                "Mercury", "Jupiter", "Venus", "Saturn"
            ],
            "calculation": {
                "method": "Count benefic contributions from 8 reference points",
                "formula": "For each house: Sum bindus from all reference points",
                "tables": "Per BPHS predefined benefic position tables"
            },
            "sarvashtakavarga": {
                "description": "Combined ashtakavarga of all planets",
                "minimum_per_house": 28,
                "maximum_per_house": 49,
                "interpretation": {
                    ">=35": "Very strong house",
                    "30-34": "Strong house",
                    "25-29": "Moderate house",
                    "<25": "Weak house"
                }
            },
            "usage": {
                "transit_analysis": "Planet transits give results in high-bindu houses",
                "dasha_results": "Modulates Vimshottari dasha predictions",
                "timing": "Events likely when transits hit high-bindu houses"
            },
            "notes": [
                "Traditional system for measuring house strength",
                "Each planet has individual ashtakavarga",
                "Combines all for Sarvashtakavarga",
                "Critical for transit predictions"
            ]
        }
    
    @staticmethod
    def get_divisional_chart_metadata(division: int) -> Dict[str, Any]:
        """Metadata for divisional chart calculations."""
        chart_names = {
            1: ("Rashi", "Birth chart", "Overall life"),
            2: ("Hora", "Wealth", "Financial matters"),
            3: ("Drekkana", "Siblings", "Co-borns, courage"),
            4: ("Chaturthamsa", "Property", "Fixed assets, fortune"),
            7: ("Saptamsa", "Children", "Progeny"),
            9: ("Navamsa", "Spouse", "Marriage, dharma, strength"),
            10: ("Dasamsa", "Career", "Profession, status"),
            12: ("Dwadasamsa", "Parents", "Parents, ancestry"),
            16: ("Shodasamsa", "Vehicles", "Conveyances, happiness"),
            20: ("Vimsamsa", "Spirituality", "Religious pursuits"),
            24: ("Chaturvimsamsa", "Learning", "Education, knowledge"),
            27: ("Nakshatramsa", "Strengths/Weaknesses", "Hidden talents"),
            30: ("Trimsamsa", "Evils", "Misfortunes, obstacles"),
            40: ("Khavedamsa", "Auspicious/Inauspicious", "Maternal legacy"),
            45: ("Akshavedamsa", "Character", "Conduct, behavior"),
            60: ("Shashtyamsa", "Karma", "Past life, general well-being")
        }
        
        name, signification, area = chart_names.get(division, (f"D{division}", "Various", "See texts"))
        
        return {
            "type": CalculationType.DIVISIONAL_CHART,
            "division": division,
            "name": name,
            "signification": signification,
            "area_of_life": area,
            "formula": f"Planet_Varga = (Planet_Long × {division}) mod 360 ÷ 30",
            "source": "Brihat Parashara Hora Shastra, Chapters 6-7",
            "method": "Fractional degree division per Parashara",
            "calculation_steps": [
                f"1. Multiply sidereal longitude by {division}",
                "2. Take modulo 360",
                "3. Divide by 30 to get sign number",
                "4. Degree within varga sign = (step2 mod 30)"
            ],
            "notes": [
                f"D{division} divides each sign into {division} parts",
                "Each planet's position recalculated",
                f"Shows {area.lower()} matters specifically"
            ]
        }
    
    @staticmethod
    def get_dasha_metadata(system: str = "Vimshottari") -> Dict[str, Any]:
        """Metadata for dasha system calculations."""
        metadata = {
            "type": CalculationType.DASHA_SYSTEM,
            "system": system,
            "source": "Brihat Parashara Hora Shastra, Chapters 45-46"
        }
        
        system_specific = {
            "Vimshottari": {
                "description": "120-year cycle dasha system",
                "basis": "Moon's nakshatra at birth",
                "cycle_years": 120,
                "planet_periods": {
                    "Sun": 6, "Moon": 10, "Mars": 7,
                    "Rahu": 18, "Jupiter": 16, "Saturn": 19,
                    "Mercury": 17, "Ketu": 7, "Venus": 20
                },
                "formula": "Balance of dasha = Remaining portion of nakshatra",
                "calculation": [
                    "1. Determine Moon's nakshatra",
                    "2. Find nakshatra lord",
                    "3. Calculate elapsed portion (Moon_Long mod 13.333...)",
                    "4. Balance = Total_years × (1 - elapsed%)"
                ],
                "subdivisions": {
                    "Mahadasha": "Main period",
                    "Antardasha": "Sub-period (1/9 of mahadasha)",
                    "Pratyantardasha": "Sub-sub-period",
                    "Sookshma": "Sub-sub-sub-period",
                    "Prana": "Sub-sub-sub-sub-period"
                },
                "notes": [
                    "Most popular dasha system",
                    "Used for timing predictions",
                    "Sequence: Sun→Moon→Mars→Rahu→Jupiter→Saturn→Mercury→Ketu→Venus"
                ]
            }
        }
        
        if system in system_specific:
            metadata.update(system_specific[system])
        
        return metadata
    
    @staticmethod
    def get_calculation_metadata(calc_type: CalculationType, **kwargs) -> Dict[str, Any]:
        """Get metadata for any calculation type."""
        metadata_functions = {
            CalculationType.PLANETARY_POSITION: CalculationMetadata.get_planetary_position_metadata,
            CalculationType.AYANAMSA: lambda: CalculationMetadata.get_ayanamsa_metadata(kwargs.get('system', 'Lahiri')),
            CalculationType.HOUSE_CALCULATION: lambda: CalculationMetadata.get_house_system_metadata(kwargs.get('system', 'Whole Sign')),
            CalculationType.SHADBALA: CalculationMetadata.get_shadbala_metadata,
            CalculationType.ASHTAKAVARGA: CalculationMetadata.get_ashtakavarga_metadata,
            CalculationType.DIVISIONAL_CHART: lambda: CalculationMetadata.get_divisional_chart_metadata(kwargs.get('division', 9)),
            CalculationType.DASHA_SYSTEM: lambda: CalculationMetadata.get_dasha_metadata(kwargs.get('system', 'Vimshottari'))
        }
        
        if calc_type in metadata_functions:
            return metadata_functions[calc_type]()
        
        return {
            "type": calc_type,
            "message": "Metadata not yet documented for this calculation type"
        }
    
    @staticmethod
    def get_all_sources() -> List[Dict[str, str]]:
        """Get list of all sources and references used."""
        return [
            {
                "name": "Swiss Ephemeris",
                "type": "Computational",
                "url": "https://www.astro.com/swisseph/",
                "description": "High-precision planetary ephemeris",
                "license": "AGPL/Dual"
            },
            {
                "name": "Brihat Parashara Hora Shastra (BPHS)",
                "type": "Classical Text",
                "author": "Sage Parashara",
                "description": "Foundation text of Vedic astrology",
                "topics": "Houses, dashas, yogas, strength calculations"
            },
            {
                "name": "Jagannatha Hora",
                "type": "Reference Software",
                "author": "P.V.R. Narasimha Rao",
                "url": "https://www.vedicastrologer.org/jh/",
                "description": "Desktop software for accuracy verification",
                "usage": "Calculation verification standard"
            },
            {
                "name": "Phaladeepika",
                "type": "Classical Text",
                "author": "Mantreswara",
                "description": "Classical text on predictive astrology"
            },
            {
                "name": "Saravali",
                "type": "Classical Text",
                "author": "Kalyana Varma",
                "description": "Comprehensive classical text"
            },
            {
                "name": "Jataka Parijata",
                "type": "Classical Text",
                "author": "Vaidyanatha Dikshita",
                "description": "Classical text on horoscopy"
            }
        ]
