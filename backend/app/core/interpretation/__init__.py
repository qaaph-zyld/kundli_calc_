"""
Astrological Interpretation Module
PGF Protocol: INT_003
Gate: GATE_18
Version: 1.0.0
"""

from .config import (
    DOMAIN_CONFIG,
    INTERPRETATION_PARAMS,
    STRENGTH_CONFIG,
    TEMPLATE_CONFIG,
    TIMEFRAME_CONFIG,
    get_interpretation_config,
)
from .framework import (
    AstrologicalInterpreter,
    ComprehensiveInterpretation,
    DomainInterpretation,
    InterpretationDomain,
    InterpretationStrength,
    InterpretationTimeframe,
)

__all__ = [
    "InterpretationDomain",
    "InterpretationTimeframe",
    "InterpretationStrength",
    "DomainInterpretation",
    "ComprehensiveInterpretation",
    "AstrologicalInterpreter",
    "DOMAIN_CONFIG",
    "TIMEFRAME_CONFIG",
    "STRENGTH_CONFIG",
    "INTERPRETATION_PARAMS",
    "TEMPLATE_CONFIG",
    "get_interpretation_config",
]
