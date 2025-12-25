"""
Structured Logging Configuration
================================
Centralized logging setup with proper formatting and levels.
"""

import logging
import sys
from datetime import datetime
from typing import Any, Dict
import json


class StructuredFormatter(logging.Formatter):
    """Custom formatter for structured JSON logs"""
    
    def format(self, record: logging.LogRecord) -> str:
        """Format log record as JSON"""
        log_data: Dict[str, Any] = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }
        
        # Add exception info if present
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)
        
        # Add extra fields if present
        if hasattr(record, "extra_data"):
            log_data["extra"] = record.extra_data
        
        # Add calculation context if present
        if hasattr(record, "calculation_type"):
            log_data["calculation"] = {
                "type": record.calculation_type,
                "duration_ms": getattr(record, "duration_ms", None),
                "success": getattr(record, "success", True)
            }
        
        return json.dumps(log_data)


class CalculationLogger:
    """Logger specifically for calculation operations"""
    
    def __init__(self, name: str):
        self.logger = logging.getLogger(f"calculations.{name}")
    
    def log_calculation_start(self, calc_type: str, params: Dict[str, Any]) -> None:
        """Log start of calculation"""
        self.logger.info(
            f"Starting {calc_type} calculation",
            extra={
                "extra_data": params,
                "calculation_type": calc_type
            }
        )
    
    def log_calculation_end(
        self, 
        calc_type: str, 
        duration_ms: float, 
        success: bool = True
    ) -> None:
        """Log end of calculation"""
        self.logger.info(
            f"Completed {calc_type} calculation",
            extra={
                "calculation_type": calc_type,
                "duration_ms": duration_ms,
                "success": success
            }
        )
    
    def log_calculation_error(
        self, 
        calc_type: str, 
        error: Exception, 
        params: Dict[str, Any]
    ) -> None:
        """Log calculation error"""
        self.logger.error(
            f"Error in {calc_type} calculation: {str(error)}",
            extra={
                "extra_data": params,
                "calculation_type": calc_type,
                "success": False
            },
            exc_info=True
        )


def setup_logging(
    level: str = "INFO",
    format_type: str = "json"
) -> None:
    """
    Setup application-wide logging configuration
    
    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        format_type: Format type ('json' or 'text')
    """
    # Get root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, level.upper()))
    
    # Remove existing handlers
    root_logger.handlers.clear()
    
    # Create console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(getattr(logging, level.upper()))
    
    # Set formatter
    if format_type == "json":
        formatter = StructuredFormatter()
    else:
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
    
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)
    
    # Set specific loggers
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("uvicorn.error").setLevel(logging.INFO)
    
    root_logger.info(f"Logging configured with level: {level}, format: {format_type}")


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance
    
    Args:
        name: Logger name
        
    Returns:
        Logger instance
    """
    return logging.getLogger(name)


def get_calculation_logger(name: str) -> CalculationLogger:
    """
    Get a calculation-specific logger
    
    Args:
        name: Calculation module name
        
    Returns:
        CalculationLogger instance
    """
    return CalculationLogger(name)
