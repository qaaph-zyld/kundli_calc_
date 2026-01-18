"""Planetary positions model module."""

from app.models.base import BaseModel
from sqlalchemy import Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship


class PlanetaryPosition(BaseModel):
    """Planetary position model."""

    __tablename__ = "planetary_positions"
    __table_args__ = {"extend_existing": True}

    birth_chart_id = Column(String(36), ForeignKey("birth_charts.id"))
    planet_name = Column(String(50), nullable=False)
    longitude = Column(Float, nullable=False)
    latitude = Column(Float)
    speed = Column(Float)
    house = Column(Integer)
    zodiac_sign = Column(String(50))
    nakshatra = Column(String(50))
    nakshatra_pada = Column(Integer)

    # Relationships
    birth_chart = relationship("BirthChart", back_populates="planetary_positions")
