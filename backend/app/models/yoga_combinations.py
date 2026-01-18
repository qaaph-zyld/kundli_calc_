"""Yoga combinations model module."""

from app.models.base import BaseModel
from sqlalchemy import Column, Float, ForeignKey, String
from sqlalchemy.orm import relationship


class YogaCombination(BaseModel):
    """Yoga combination model."""

    __tablename__ = "yoga_combinations"
    __table_args__ = {"extend_existing": True}

    birth_chart_id = Column(String(36), ForeignKey("birth_charts.id"))
    yoga_name = Column(String(100), nullable=False)
    description = Column(String(1000))
    strength = Column(Float)  # 0-1 scale
    planets_involved = Column(String(255))  # Comma-separated list
    houses_involved = Column(String(255))  # Comma-separated list

    # Relationships
    birth_chart = relationship("BirthChart", back_populates="yoga_combinations")
