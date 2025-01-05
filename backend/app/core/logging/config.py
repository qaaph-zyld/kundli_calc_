"""
Logging Configuration
PGF Protocol: LOG_002
Gate: GATE_11
Version: 1.0.0
"""

from typing import Dict, Any
from pathlib import Path
from .framework import (
    LogConfig,
    LogLevel,
    LogFormat,
    LogDestination
)

def get_logging_config(environment: str) -> LogConfig:
    """Get logging configuration for environment"""
    
    # Base configuration
    base_config = {
        "level": LogLevel.DEBUG if environment in ["local", "development"]
                else LogLevel.INFO,
        "format": LogFormat.CONSOLE if environment == "local"
                else LogFormat.JSON,
        "include_timestamp": True,
        "include_hostname": True,
        "include_pid": True,
        "max_size": 10 * 1024 * 1024,  # 10MB
        "backup_count": 5
    }
    
    # Environment-specific configuration
    if environment == "local":
        config = {
            **base_config,
            "destinations": [LogDestination.CONSOLE],
            "file_path": None
        }
    
    elif environment == "development":
        config = {
            **base_config,
            "destinations": [
                LogDestination.CONSOLE,
                LogDestination.FILE
            ],
            "file_path": "logs/dev-app.log"
        }
    
    elif environment == "staging":
        config = {
            **base_config,
            "destinations": [
                LogDestination.FILE,
                LogDestination.ELASTIC
            ],
            "file_path": "logs/staging-app.log",
            "elastic_host": "http://elasticsearch:9200",
            "elastic_index": "vedic-astrology-staging-logs"
        }
    
    else:  # production
        config = {
            **base_config,
            "destinations": [
                LogDestination.FILE,
                LogDestination.ELASTIC,
                LogDestination.SYSLOG
            ],
            "file_path": "logs/prod-app.log",
            "elastic_host": "http://elasticsearch:9200",
            "elastic_index": "vedic-astrology-prod-logs",
            "syslog_host": "localhost",
            "syslog_port": 514
        }
    
    return LogConfig(**config)

def setup_logging(environment: str) -> None:
    """Setup logging for application"""
    import logging.config
    
    # Create logs directory if it doesn't exist
    if environment != "local":
        Path("logs").mkdir(exist_ok=True)
    
    # Get logging configuration
    config = get_logging_config(environment)
    
    # Configure logging
    logging_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "json": {
                "()": "pythonjsonlogger.jsonlogger.JsonFormatter",
                "fmt": "%(asctime)s %(name)s %(levelname)s %(message)s"
            },
            "console": {
                "format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
            }
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "console" if environment == "local" else "json",
                "stream": "ext://sys.stdout"
            }
        },
        "root": {
            "level": config.level,
            "handlers": ["console"]
        },
        "loggers": {
            "uvicorn": {
                "handlers": ["console"],
                "level": "INFO",
                "propagate": False
            },
            "gunicorn": {
                "handlers": ["console"],
                "level": "INFO",
                "propagate": False
            }
        }
    }
    
    # Add file handler if configured
    if LogDestination.FILE in config.destinations:
        logging_config["handlers"]["file"] = {
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "json",
            "filename": config.file_path,
            "maxBytes": config.max_size,
            "backupCount": config.backup_count
        }
        logging_config["root"]["handlers"].append("file")
    
    # Configure logging
    logging.config.dictConfig(logging_config)
