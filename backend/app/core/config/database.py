"""Database configuration module."""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .settings import settings

# Database configuration: prefer Settings.DATABASE_URL with SQLite fallback
DATABASE_URL = settings.DATABASE_URL or "sqlite:///./kundli.db"

# Create SQLAlchemy engine
if str(DATABASE_URL).startswith("sqlite"):
    engine = create_engine(
        str(DATABASE_URL),
        connect_args={"check_same_thread": False}
    )
else:
    engine = create_engine(str(DATABASE_URL))

# Create SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency to get DB session
def get_db():
    """Get database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
