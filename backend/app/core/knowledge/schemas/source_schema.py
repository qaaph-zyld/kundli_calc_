"""
Source Attribution Schema
==========================
Pydantic models for knowledge source tracking and citation.
"""
from typing import Optional, List, Dict, Any
from enum import Enum
from pydantic import BaseModel, Field


class SourceType(str, Enum):
    """Type of knowledge source"""
    CLASSICAL_TEXT = "classical_text"
    COMMENTARY = "commentary"
    MODERN_REFERENCE = "modern_reference"
    COMPUTATIONAL = "computational"


class ConfidenceLevel(str, Enum):
    """Confidence level for interpretation"""
    DIRECT_QUOTE = "direct_quote"          # Exact verse/passage from text
    DIRECT_INTERPRETATION = "direct_interpretation"  # Clear traditional interpretation
    SYNTHESIZED = "synthesized"            # Combined from multiple sources
    INFERRED = "inferred"                  # Logical inference from principles
    COMPUTATIONAL = "computational"        # Derived from calculations


class ClassicalText(str, Enum):
    """Canonical classical texts"""
    BPHS = "Brihat Parashara Hora Shastra"
    SARAVALI = "Saravali"
    PHALADEEPIKA = "Phaladeepika"
    JATAKA_PARIJATA = "Jataka Parijata"
    HORA_SARA = "Hora Sara"
    JAIMINI_SUTRAS = "Jaimini Sutras"
    UTTARA_KALAMRITA = "Uttara Kalamrita"
    BRIHAT_JATAKA = "Brihat Jataka"
    SARVARTHA_CHINTAMANI = "Sarvartha Chintamani"


class SourceCitation(BaseModel):
    """Citation for a knowledge source"""
    text: ClassicalText = Field(..., description="Source text name")
    chapter: Optional[int] = Field(None, description="Chapter number")
    verses: Optional[str] = Field(None, description="Verse range (e.g., '3-4' or '10')")
    section: Optional[str] = Field(None, description="Section name if applicable")
    translator: Optional[str] = Field(None, description="Translation source (e.g., 'Santhanam', 'Raman')")
    edition: Optional[str] = Field(None, description="Edition/publication details")
    page: Optional[int] = Field(None, description="Page number in edition")
    
    def format_citation(self) -> str:
        """Format as human-readable citation"""
        parts = [self.text.value]
        if self.chapter:
            parts.append(f"Ch. {self.chapter}")
        if self.verses:
            parts.append(f"v. {self.verses}")
        if self.translator:
            parts.append(f"(trans. {self.translator})")
        return ", ".join(parts)


class SourcedContent(BaseModel):
    """Content with source attribution"""
    content: str = Field(..., description="The actual interpretation/content")
    citation: SourceCitation = Field(..., description="Source citation")
    confidence: ConfidenceLevel = Field(..., description="Confidence level")
    original_language: Optional[str] = Field(None, description="Original Sanskrit if available")
    notes: Optional[str] = Field(None, description="Additional notes or context")


class InterpretationSource(BaseModel):
    """Complete source information for an interpretation"""
    primary_sources: List[SourcedContent] = Field(
        default_factory=list,
        description="Primary classical text sources"
    )
    supporting_sources: List[SourcedContent] = Field(
        default_factory=list,
        description="Supporting references"
    )
    synthesis_note: Optional[str] = Field(
        None,
        description="Note on how multiple sources were synthesized"
    )
    
    def get_all_citations(self) -> List[str]:
        """Get all formatted citations"""
        citations = []
        for source in self.primary_sources:
            citations.append(source.citation.format_citation())
        for source in self.supporting_sources:
            citations.append(source.citation.format_citation())
        return citations


class InterpretationMetadata(BaseModel):
    """Metadata for an interpretation"""
    interpretation_type: str = Field(..., description="Type (planet_in_house, yoga, dasha, etc.)")
    confidence_score: float = Field(..., ge=0.0, le=1.0, description="Overall confidence (0-1)")
    last_updated: str = Field(..., description="ISO datetime of last update")
    validator: Optional[str] = Field(None, description="Who validated this interpretation")
    tags: List[str] = Field(default_factory=list, description="Classification tags")
