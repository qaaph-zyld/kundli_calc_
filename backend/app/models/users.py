"""User model module."""
from sqlalchemy import Boolean, Column, String, DateTime
from sqlalchemy.orm import relationship

from app.models.base import BaseModel


class User(BaseModel):
    """User model."""

    metadata = MetaData()
    __table__ = Table(
        'users',
        metadata,
        extend_existing=True,
        Column('email', String(255), unique=True, nullable=False, index=True),
        Column('hashed_password', String(255), nullable=False),
        Column('full_name', String(255)),
        Column('last_login', DateTime(timezone=True)),
        Column('is_active', Boolean, default=True),
        Column('is_superuser', Boolean, default=False)
    )
    is_superuser = Column(Boolean, default=False)

    # Relationships
    birth_charts = relationship("BirthChart", back_populates="user")
