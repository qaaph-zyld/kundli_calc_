"""
Famous Charts Database
Reference charts from notable personalities for study and comparison.

Source: VedAstro Famous People Dataset (HuggingFace)
https://huggingface.co/datasets/vedastro-org/15000-Famous-People-Birth-Date-Location
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, List, Optional


@dataclass
class FamousChart:
    """A famous person's birth data"""

    name: str
    birth_date: datetime
    birth_place: str
    latitude: float
    longitude: float
    timezone: float
    category: str
    description: str
    verified: bool = True


# Curated selection of famous charts with verified data
FAMOUS_CHARTS: Dict[str, FamousChart] = {
    # World Leaders
    "narendra_modi": FamousChart(
        name="Narendra Modi",
        birth_date=datetime(1950, 9, 17, 11, 0),
        birth_place="Vadnagar, Gujarat, India",
        latitude=23.7833,
        longitude=72.6333,
        timezone=5.5,
        category="Politics",
        description="Prime Minister of India",
    ),
    "mahatma_gandhi": FamousChart(
        name="Mahatma Gandhi",
        birth_date=datetime(1869, 10, 2, 7, 12),
        birth_place="Porbandar, Gujarat, India",
        latitude=21.6417,
        longitude=69.6083,
        timezone=5.5,
        category="Politics",
        description="Father of the Indian Nation",
    ),
    "jawaharlal_nehru": FamousChart(
        name="Jawaharlal Nehru",
        birth_date=datetime(1889, 11, 14, 23, 0),
        birth_place="Allahabad, India",
        latitude=25.4358,
        longitude=81.8463,
        timezone=5.5,
        category="Politics",
        description="First Prime Minister of India",
    ),
    "indira_gandhi": FamousChart(
        name="Indira Gandhi",
        birth_date=datetime(1917, 11, 19, 23, 11),
        birth_place="Allahabad, India",
        latitude=25.4358,
        longitude=81.8463,
        timezone=5.5,
        category="Politics",
        description="Prime Minister of India",
    ),
    # Scientists & Thinkers
    "albert_einstein": FamousChart(
        name="Albert Einstein",
        birth_date=datetime(1879, 3, 14, 11, 30),
        birth_place="Ulm, Germany",
        latitude=48.4011,
        longitude=9.9876,
        timezone=1.0,
        category="Science",
        description="Theoretical Physicist, Nobel Laureate",
    ),
    "cv_raman": FamousChart(
        name="C.V. Raman",
        birth_date=datetime(1888, 11, 7, 5, 30),
        birth_place="Tiruchirappalli, India",
        latitude=10.7905,
        longitude=78.7047,
        timezone=5.5,
        category="Science",
        description="Nobel Prize in Physics (Raman Effect)",
    ),
    "abdul_kalam": FamousChart(
        name="A.P.J. Abdul Kalam",
        birth_date=datetime(1931, 10, 15, 1, 15),
        birth_place="Rameswaram, India",
        latitude=9.2876,
        longitude=79.3129,
        timezone=5.5,
        category="Science",
        description="Missile Man of India, President",
    ),
    # Spiritual Leaders
    "swami_vivekananda": FamousChart(
        name="Swami Vivekananda",
        birth_date=datetime(1863, 1, 12, 6, 33),
        birth_place="Kolkata, India",
        latitude=22.5726,
        longitude=88.3639,
        timezone=5.5,
        category="Spiritual",
        description="Hindu monk, key figure in Vedanta",
    ),
    "ramana_maharshi": FamousChart(
        name="Ramana Maharshi",
        birth_date=datetime(1879, 12, 30, 1, 0),
        birth_place="Tiruchuzhi, India",
        latitude=9.7439,
        longitude=78.3012,
        timezone=5.5,
        category="Spiritual",
        description="Advaita Vedanta sage",
    ),
    "paramahansa_yogananda": FamousChart(
        name="Paramahansa Yogananda",
        birth_date=datetime(1893, 1, 5, 20, 38),
        birth_place="Gorakhpur, India",
        latitude=26.7606,
        longitude=83.3732,
        timezone=5.5,
        category="Spiritual",
        description="Author of Autobiography of a Yogi",
    ),
    # Entertainment
    "amitabh_bachchan": FamousChart(
        name="Amitabh Bachchan",
        birth_date=datetime(1942, 10, 11, 16, 0),
        birth_place="Allahabad, India",
        latitude=25.4358,
        longitude=81.8463,
        timezone=5.5,
        category="Entertainment",
        description="Bollywood Actor",
    ),
    "shah_rukh_khan": FamousChart(
        name="Shah Rukh Khan",
        birth_date=datetime(1965, 11, 2, 2, 30),
        birth_place="New Delhi, India",
        latitude=28.6139,
        longitude=77.2090,
        timezone=5.5,
        category="Entertainment",
        description="Bollywood Actor",
    ),
    "lata_mangeshkar": FamousChart(
        name="Lata Mangeshkar",
        birth_date=datetime(1929, 9, 28, 10, 0),
        birth_place="Indore, India",
        latitude=22.7196,
        longitude=75.8577,
        timezone=5.5,
        category="Entertainment",
        description="Legendary Playback Singer",
    ),
    "ar_rahman": FamousChart(
        name="A.R. Rahman",
        birth_date=datetime(1967, 1, 6, 0, 0),
        birth_place="Chennai, India",
        latitude=13.0827,
        longitude=80.2707,
        timezone=5.5,
        category="Entertainment",
        description="Music Composer, Oscar Winner",
    ),
    # Sports
    "sachin_tendulkar": FamousChart(
        name="Sachin Tendulkar",
        birth_date=datetime(1973, 4, 24, 16, 15),
        birth_place="Mumbai, India",
        latitude=19.0760,
        longitude=72.8777,
        timezone=5.5,
        category="Sports",
        description="Cricket Legend, Master Blaster",
    ),
    "virat_kohli": FamousChart(
        name="Virat Kohli",
        birth_date=datetime(1988, 11, 5, 0, 0),
        birth_place="New Delhi, India",
        latitude=28.6139,
        longitude=77.2090,
        timezone=5.5,
        category="Sports",
        description="Indian Cricket Captain",
    ),
    "ms_dhoni": FamousChart(
        name="M.S. Dhoni",
        birth_date=datetime(1981, 7, 7, 23, 10),
        birth_place="Ranchi, India",
        latitude=23.3441,
        longitude=85.3096,
        timezone=5.5,
        category="Sports",
        description="Former Indian Cricket Captain",
    ),
    # Business
    "mukesh_ambani": FamousChart(
        name="Mukesh Ambani",
        birth_date=datetime(1957, 4, 19, 0, 0),
        birth_place="Aden, Yemen",
        latitude=12.8000,
        longitude=45.0333,
        timezone=3.0,
        category="Business",
        description="Chairman of Reliance Industries",
    ),
    "ratan_tata": FamousChart(
        name="Ratan Tata",
        birth_date=datetime(1937, 12, 28, 0, 0),
        birth_place="Mumbai, India",
        latitude=19.0760,
        longitude=72.8777,
        timezone=5.5,
        category="Business",
        description="Chairman Emeritus of Tata Sons",
    ),
    # International
    "steve_jobs": FamousChart(
        name="Steve Jobs",
        birth_date=datetime(1955, 2, 24, 19, 15),
        birth_place="San Francisco, USA",
        latitude=37.7749,
        longitude=-122.4194,
        timezone=-8.0,
        category="Business",
        description="Co-founder of Apple",
    ),
    "elon_musk": FamousChart(
        name="Elon Musk",
        birth_date=datetime(1971, 6, 28, 7, 0),
        birth_place="Pretoria, South Africa",
        latitude=-25.7479,
        longitude=28.2293,
        timezone=2.0,
        category="Business",
        description="CEO of Tesla and SpaceX",
    ),
    "bill_gates": FamousChart(
        name="Bill Gates",
        birth_date=datetime(1955, 10, 28, 22, 0),
        birth_place="Seattle, USA",
        latitude=47.6062,
        longitude=-122.3321,
        timezone=-8.0,
        category="Business",
        description="Co-founder of Microsoft",
    ),
}


def get_famous_chart(key: str) -> Optional[FamousChart]:
    """Get a famous chart by key"""
    return FAMOUS_CHARTS.get(key.lower().replace(" ", "_"))


def list_famous_charts(category: Optional[str] = None) -> List[Dict[str, Any]]:
    """List all famous charts, optionally filtered by category"""
    charts = []

    for key, chart in FAMOUS_CHARTS.items():
        if category and chart.category.lower() != category.lower():
            continue

        charts.append(
            {
                "key": key,
                "name": chart.name,
                "birth_date": chart.birth_date.isoformat(),
                "birth_place": chart.birth_place,
                "category": chart.category,
                "description": chart.description,
            }
        )

    return sorted(charts, key=lambda x: x["name"])


def get_categories() -> List[str]:
    """Get list of available categories"""
    categories = set(chart.category for chart in FAMOUS_CHARTS.values())
    return sorted(categories)


def search_famous_charts(query: str) -> List[Dict[str, Any]]:
    """Search famous charts by name"""
    query_lower = query.lower()
    results = []

    for key, chart in FAMOUS_CHARTS.items():
        if query_lower in chart.name.lower() or query_lower in chart.description.lower():
            results.append(
                {
                    "key": key,
                    "name": chart.name,
                    "birth_date": chart.birth_date.isoformat(),
                    "birth_place": chart.birth_place,
                    "category": chart.category,
                    "description": chart.description,
                }
            )

    return results
