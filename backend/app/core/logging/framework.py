"""
Logging Framework
PGF Protocol: LOG_001
Gate: GATE_11
Version: 1.0.0
"""

import logging
import json
import sys
import threading
import queue
import asyncio
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional, List, Union
from enum import Enum
from pydantic import BaseModel, Field
import structlog
from structlog.processors import (
    TimeStamper,
    JSONRenderer,
    StackInfoRenderer,
    format_exc_info
)
from structlog.stdlib import (
    add_log_level,
    add_logger_name,
    filter_by_level
)

class LogLevel(str, Enum):
    """Log levels"""
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"

class LogFormat(str, Enum):
    """Log formats"""
    JSON = "json"
    CONSOLE = "console"
    SYSLOG = "syslog"

class LogDestination(str, Enum):
    """Log destinations"""
    CONSOLE = "console"
    FILE = "file"
    SYSLOG = "syslog"
    ELASTIC = "elastic"

class LogContext(BaseModel):
    """Log context"""
    
    request_id: Optional[str] = None
    user_id: Optional[str] = None
    ip_address: Optional[str] = None
    endpoint: Optional[str] = None
    method: Optional[str] = None
    status_code: Optional[int] = None
    duration_ms: Optional[float] = None
    error: Optional[str] = None
    service: Optional[str] = None
    environment: Optional[str] = None
    version: Optional[str] = None

class LogConfig(BaseModel):
    """Log configuration"""
    
    level: LogLevel = LogLevel.INFO
    format: LogFormat = LogFormat.JSON
    destinations: List[LogDestination] = [LogDestination.CONSOLE]
    file_path: Optional[str] = "logs/app.log"
    max_size: int = 10 * 1024 * 1024  # 10MB
    backup_count: int = 5
    include_timestamp: bool = True
    include_hostname: bool = True
    include_pid: bool = True
    elastic_host: Optional[str] = None
    elastic_index: Optional[str] = None
    syslog_host: Optional[str] = None
    syslog_port: Optional[int] = None

class AsyncQueueHandler(logging.Handler):
    """Async queue handler for logging"""
    
    def __init__(self, queue: asyncio.Queue):
        super().__init__()
        self.queue = queue
    
    def emit(self, record: logging.LogRecord) -> None:
        """Emit log record"""
        try:
            self.queue.put_nowait(record)
        except asyncio.QueueFull:
            self.handleError(record)

class LogProcessor:
    """Log processor for formatting and enriching logs"""
    
    def __init__(self, config: LogConfig):
        self.config = config
        self._setup_processors()
    
    def _setup_processors(self) -> None:
        """Setup log processors"""
        self.processors = [
            structlog.stdlib.add_log_level,
            structlog.stdlib.add_logger_name,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            self._add_extra_fields,
        ]
        
        if self.config.format == LogFormat.JSON:
            self.processors.append(structlog.processors.JSONRenderer())
        else:
            self.processors.append(
                structlog.dev.ConsoleRenderer(
                    colors=True,
                    level_styles={
                        "debug": "cyan",
                        "info": "green",
                        "warning": "yellow",
                        "error": "red",
                        "critical": "red,bold"
                    }
                )
            )
    
    def _add_extra_fields(
        self,
        logger: str,
        method_name: str,
        event_dict: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Add extra fields to log record"""
        if self.config.include_timestamp:
            event_dict["timestamp"] = datetime.utcnow().isoformat()
        
        if self.config.include_hostname:
            import socket
            event_dict["hostname"] = socket.gethostname()
        
        if self.config.include_pid:
            import os
            event_dict["pid"] = os.getpid()
        
        return event_dict
    
    def process_record(
        self,
        record: logging.LogRecord,
        context: Optional[LogContext] = None
    ) -> str:
        """Process log record"""
        # Convert record to event dict
        event_dict = {
            "logger": record.name,
            "level": record.levelname,
            "message": record.msg,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        # Add context if provided
        if context:
            event_dict.update(context.dict(exclude_none=True))
        
        # Add exception info if present
        if record.exc_info:
            event_dict["exc_info"] = format_exc_info(record.exc_info)
        
        # Process through processors
        for processor in self.processors:
            event_dict = processor(record.name, record.levelname, event_dict)
        
        return event_dict

class LogWriter:
    """Log writer for different destinations"""
    
    def __init__(self, config: LogConfig):
        self.config = config
        self._setup_writers()
    
    def _setup_writers(self) -> None:
        """Setup log writers"""
        self.writers = []
        
        # Console writer
        if LogDestination.CONSOLE in self.config.destinations:
            self.writers.append(self._write_console)
        
        # File writer
        if LogDestination.FILE in self.config.destinations:
            Path(self.config.file_path).parent.mkdir(parents=True, exist_ok=True)
            self.writers.append(self._write_file)
        
        # Elastic writer
        if LogDestination.ELASTIC in self.config.destinations:
            from elasticsearch import AsyncElasticsearch
            self.elastic = AsyncElasticsearch([self.config.elastic_host])
            self.writers.append(self._write_elastic)
        
        # Syslog writer
        if LogDestination.SYSLOG in self.config.destinations:
            import syslog
            syslog.openlog("vedic-astrology")
            self.writers.append(self._write_syslog)
    
    def _write_console(self, log_entry: Dict[str, Any]) -> None:
        """Write log to console"""
        if self.config.format == LogFormat.JSON:
            print(json.dumps(log_entry))
        else:
            print(self._format_console(log_entry))
    
    def _write_file(self, log_entry: Dict[str, Any]) -> None:
        """Write log to file"""
        with open(self.config.file_path, "a") as f:
            f.write(json.dumps(log_entry) + "\n")
    
    async def _write_elastic(self, log_entry: Dict[str, Any]) -> None:
        """Write log to Elasticsearch"""
        await self.elastic.index(
            index=self.config.elastic_index,
            document=log_entry
        )
    
    def _write_syslog(self, log_entry: Dict[str, Any]) -> None:
        """Write log to syslog"""
        import syslog
        priority = self._get_syslog_priority(log_entry["level"])
        message = json.dumps(log_entry)
        syslog.syslog(priority, message)
    
    def _format_console(self, log_entry: Dict[str, Any]) -> str:
        """Format log entry for console"""
        level_colors = {
            "DEBUG": "\033[36m",  # cyan
            "INFO": "\033[32m",   # green
            "WARNING": "\033[33m", # yellow
            "ERROR": "\033[31m",  # red
            "CRITICAL": "\033[31;1m"  # bold red
        }
        reset = "\033[0m"
        
        level = log_entry["level"]
        timestamp = log_entry.get("timestamp", "")
        message = log_entry["message"]
        context = {k: v for k, v in log_entry.items()
                  if k not in ["level", "timestamp", "message"]}
        
        return (
            f"{timestamp} "
            f"{level_colors.get(level, '')}{level:8}{reset} "
            f"{message} "
            f"{json.dumps(context) if context else ''}"
        )
    
    def _get_syslog_priority(self, level: str) -> int:
        """Get syslog priority from log level"""
        import syslog
        priorities = {
            "DEBUG": syslog.LOG_DEBUG,
            "INFO": syslog.LOG_INFO,
            "WARNING": syslog.LOG_WARNING,
            "ERROR": syslog.LOG_ERR,
            "CRITICAL": syslog.LOG_CRIT
        }
        return priorities.get(level, syslog.LOG_INFO)
    
    async def write(self, log_entry: Dict[str, Any]) -> None:
        """Write log entry to all configured destinations"""
        for writer in self.writers:
            if asyncio.iscoroutinefunction(writer):
                await writer(log_entry)
            else:
                writer(log_entry)

class LogManager:
    """Log manager for handling logs"""
    
    def __init__(self, config: LogConfig):
        self.config = config
        self.processor = LogProcessor(config)
        self.writer = LogWriter(config)
        self.queue = asyncio.Queue(maxsize=10000)
        self._setup_logger()
    
    def _setup_logger(self) -> None:
        """Setup logger"""
        # Set root logger level
        logging.root.setLevel(self.config.level)
        
        # Remove existing handlers
        logging.root.handlers = []
        
        # Add async queue handler
        handler = AsyncQueueHandler(self.queue)
        logging.root.addHandler(handler)
        
        # Configure structlog
        structlog.configure(
            processors=self.processor.processors,
            logger_factory=structlog.stdlib.LoggerFactory(),
            wrapper_class=structlog.stdlib.BoundLogger,
            cache_logger_on_first_use=True
        )
    
    async def process_logs(self) -> None:
        """Process logs from queue"""
        while True:
            try:
                # Get log record from queue
                record = await self.queue.get()
                
                # Process record
                log_entry = self.processor.process_record(record)
                
                # Write to destinations
                await self.writer.write(log_entry)
                
                # Mark task as done
                self.queue.task_done()
                
            except Exception as e:
                print(f"Error processing log: {str(e)}", file=sys.stderr)
    
    def get_logger(self, name: str) -> structlog.BoundLogger:
        """Get logger instance"""
        return structlog.get_logger(name)
    
    async def start(self) -> None:
        """Start log processing"""
        await self.process_logs()
    
    def log(
        self,
        level: LogLevel,
        message: str,
        context: Optional[LogContext] = None,
        **kwargs: Any
    ) -> None:
        """Log message with context"""
        logger = self.get_logger(__name__)
        
        # Merge context with kwargs
        log_args = kwargs
        if context:
            log_args.update(context.dict(exclude_none=True))
        
        # Log message
        getattr(logger, level.lower())(message, **log_args)
