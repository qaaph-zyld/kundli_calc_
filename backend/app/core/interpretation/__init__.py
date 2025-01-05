"""
Astrological Interpretation Module
PGF Protocol: INT_003
Gate: GATE_18
Version: 1.0.0
"""

from .framework import (
    InterpretationDomain,
    InterpretationTimeframe,
    InterpretationStrength,
    DomainInterpretation,
    ComprehensiveInterpretation,
    AstrologicalInterpreter
)
from .config import (
    DOMAIN_CONFIG,
    TIMEFRAME_CONFIG,
    STRENGTH_CONFIG,
    INTERPRETATION_PARAMS,
    TEMPLATE_CONFIG,
    get_interpretation_config
)

__all__ = [
    'InterpretationDomain',
    'InterpretationTimeframe',
    'InterpretationStrength',
    'DomainInterpretation',
    'ComprehensiveInterpretation',
    'AstrologicalInterpreter',
    'DOMAIN_CONFIG',
    'TIMEFRAME_CONFIG',
    'STRENGTH_CONFIG',
    'INTERPRETATION_PARAMS',
    'TEMPLATE_CONFIG',
    'get_interpretation_config'
]
