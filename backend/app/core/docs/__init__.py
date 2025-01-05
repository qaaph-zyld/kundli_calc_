"""
Documentation Module
PGF Protocol: DOC_003
Gate: GATE_8
Version: 1.0.0
"""

from .framework import (
    DocType,
    DocFormat,
    DocSection,
    Documentation,
    DocGenerator
)
from .generator import (
    DocumentationGenerator,
    generate_docs
)

__all__ = [
    'DocType',
    'DocFormat',
    'DocSection',
    'Documentation',
    'DocGenerator',
    'DocumentationGenerator',
    'generate_docs'
]
