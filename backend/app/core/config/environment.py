"""Environment configuration module."""
from functools import lru_cache
from typing import Dict, Any
import os
from pathlib import Path
from dotenv import load_dotenv

class Environment:
    """Environment configuration manager."""

    def __init__(self):
        self.env = os.getenv("APP_ENV", "development")
        self._load_env_file()
        self._validate_required_vars()

    def _load_env_file(self):
        """Load environment file based on APP_ENV."""
        env_file = Path(__file__).parent / "environments" / f"{self.env}.env"
        if not env_file.exists():
            raise ValueError(f"Environment file not found: {env_file}")
        load_dotenv(env_file)

    def _validate_required_vars(self):
        """Validate that all required environment variables are set."""
        required_vars = [
            "MONGODB_URL",
            "MONGODB_DB_NAME",
            "REDIS_URL",
            "SECRET_KEY",
        ]
        
        missing_vars = [var for var in required_vars if not os.getenv(var)]
        if missing_vars:
            raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")

    @property
    def is_development(self) -> bool:
        """Check if environment is development."""
        return self.env == "development"

    @property
    def is_staging(self) -> bool:
        """Check if environment is staging."""
        return self.env == "staging"

    @property
    def is_production(self) -> bool:
        """Check if environment is production."""
        return self.env == "production"

    def get_settings(self) -> Dict[str, Any]:
        """Get all environment settings."""
        return {
            "DEBUG": os.getenv("DEBUG", "False").lower() == "true",
            "HOST": os.getenv("HOST", "0.0.0.0"),
            "PORT": int(os.getenv("PORT", "8000")),
            "MONGODB_URL": os.getenv("MONGODB_URL"),
            "MONGODB_DB_NAME": os.getenv("MONGODB_DB_NAME"),
            "REDIS_URL": os.getenv("REDIS_URL"),
            "SECRET_KEY": os.getenv("SECRET_KEY"),
            "ACCESS_TOKEN_EXPIRE_MINUTES": int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30")),
            "REFRESH_TOKEN_EXPIRE_DAYS": int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "7")),
            "BACKEND_CORS_ORIGINS": eval(os.getenv("BACKEND_CORS_ORIGINS", "[]")),
            "LOG_LEVEL": os.getenv("LOG_LEVEL", "INFO"),
            "LOG_FORMAT": os.getenv("LOG_FORMAT", "json"),
            "EPHE_PATH": os.getenv("EPHE_PATH", "/app/ephe"),
            "ENABLE_PREMIUM_FEATURES": os.getenv("ENABLE_PREMIUM_FEATURES", "True").lower() == "true",
            "ENABLE_DETAILED_LOGGING": os.getenv("ENABLE_DETAILED_LOGGING", "False").lower() == "true",
            "ENABLE_PERFORMANCE_METRICS": os.getenv("ENABLE_PERFORMANCE_METRICS", "True").lower() == "true",
            "PROMETHEUS_METRICS": os.getenv("PROMETHEUS_METRICS", "False").lower() == "true",
            "GRAFANA_ENABLED": os.getenv("GRAFANA_ENABLED", "False").lower() == "true",
            "RATE_LIMIT_PER_MINUTE": int(os.getenv("RATE_LIMIT_PER_MINUTE", "60")),
            "SSL_CERT_PATH": os.getenv("SSL_CERT_PATH"),
            "SSL_KEY_PATH": os.getenv("SSL_KEY_PATH"),
            "ENABLE_SSL": os.getenv("ENABLE_SSL", "False").lower() == "true",
            "BACKUP_ENABLED": os.getenv("BACKUP_ENABLED", "False").lower() == "true",
            "BACKUP_RETENTION_DAYS": int(os.getenv("BACKUP_RETENTION_DAYS", "30")),
            "BACKUP_S3_BUCKET": os.getenv("BACKUP_S3_BUCKET"),
        }

@lru_cache()
def get_environment() -> Environment:
    """Get cached environment instance."""
    return Environment()

# Create global instance
env = get_environment()
