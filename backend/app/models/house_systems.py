"""House systems model module."""

from app.models.base import BaseModel
from sqlalchemy import Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship


class HouseSystem(BaseModel):
    """House system model."""

    __tablename__ = "house_systems"
    __table_args__ = {"extend_existing": True}

    birth_chart_id = Column(String(36), ForeignKey("birth_charts.id"))
    system_name = Column(String(50), nullable=False)
    house_number = Column(Integer, nullable=False)
    cusp_longitude = Column(Float, nullable=False)
    sign = Column(String(50))
    degree = Column(Float)

    # Relationships
    birth_chart = relationship("BirthChart", back_populates="house_systems")
