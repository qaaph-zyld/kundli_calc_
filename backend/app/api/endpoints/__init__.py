"""
API Endpoints Package
All endpoint routers exported here
"""

from . import health
from . import ashtakavarga
from . import bhava
from . import prediction
from . import shadbala
from . import kp_system
from . import yogas
from . import transits
from . import additional_dashas
from . import dasha
from . import panchang
from . import charts
from . import horoscope
from . import divisional
from . import debug
from . import location
from . import famous_charts

__all__ = [
    "health",
    "ashtakavarga",
    "bhava",
    "prediction",
    "shadbala",
    "kp_system",
    "yogas",
    "transits",
    "additional_dashas",
    "dasha",
    "panchang",
    "charts",
    "horoscope",
    "divisional",
    "debug",
    "location",
    "famous_charts",
]
