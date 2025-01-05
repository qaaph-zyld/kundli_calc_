"""
Service Scaling Processors
PGF Protocol: SCAL_002
Gate: GATE_33
Version: 1.0.0
"""

from typing import Dict, Any, Optional, List, Union, Set
from enum import Enum
from datetime import datetime
from dataclasses import dataclass
import asyncio
import json
import logging
from .strategies import (
    ScalingMode,
    ScalingTrigger,
    ScalingState,
    ScalingMetrics,
    HorizontalScaling,
    VerticalScaling,
    HybridScaling
)

class ProcessingState(str, Enum):
    """Processing states"""
    IDLE = "idle"
    ANALYZING = "analyzing"
    EXECUTING = "executing"
    VALIDATING = "validating"
    ERROR = "error"

@dataclass
class ProcessingMetrics:
    """Processing metrics"""
    
    total_operations: int
    successful_operations: int
    failed_operations: int
    average_processing_time: float
    last_operation_time: datetime
    current_state: ProcessingState

class ScalingProcessor:
    """Scaling processor"""
    
    def __init__(
        self,
        mode: ScalingMode = ScalingMode.HYBRID,
        analysis_interval: int = 60,
        execution_timeout: int = 300
    ):
        """Initialize processor"""
        self.mode = mode
        self.analysis_interval = analysis_interval
        self.execution_timeout = execution_timeout
        self.state = ProcessingState.IDLE
        
        # Initialize strategies
        self._init_strategies()
        
        # Initialize metrics
        self.metrics = ProcessingMetrics(
            total_operations=0,
            successful_operations=0,
            failed_operations=0,
            average_processing_time=0.0,
            last_operation_time=datetime.utcnow(),
            current_state=self.state
        )
        
        # Initialize logger
        self._init_logger()
    
    def _init_strategies(self):
        """Initialize scaling strategies"""
        # Initialize horizontal scaling
        self.horizontal = HorizontalScaling(
            min_replicas=1,
            max_replicas=10,
            cooldown_seconds=300
        )
        
        # Initialize vertical scaling
        self.vertical = VerticalScaling(
            min_resources={
                "cpu": 0.1,
                "memory": 128
            },
            max_resources={
                "cpu": 4.0,
                "memory": 8192
            },
            cooldown_seconds=300
        )
        
        # Initialize hybrid scaling
        self.hybrid = HybridScaling(
            horizontal=self.horizontal,
            vertical=self.vertical
        )
    
    def _init_logger(self):
        """Initialize logger"""
        self.logger = logging.getLogger("scaling_processor")
        self.logger.setLevel(logging.INFO)
        
        # Add handlers if not already added
        if not self.logger.handlers:
            # Console handler
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.INFO)
            
            # File handler
            file_handler = logging.FileHandler(
                "scaling_processor.log"
            )
            file_handler.setLevel(logging.DEBUG)
            
            # Create formatters
            console_formatter = logging.Formatter(
                "%(asctime)s - %(levelname)s - %(message)s"
            )
            file_formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )
            
            # Add formatters
            console_handler.setFormatter(console_formatter)
            file_handler.setFormatter(file_formatter)
            
            # Add handlers
            self.logger.addHandler(console_handler)
            self.logger.addHandler(file_handler)
    
    async def start_processing(self):
        """Start scaling processor"""
        self.logger.info("Starting scaling processor")
        
        try:
            while True:
                # Analyze metrics
                await self._analyze_metrics()
                
                # Wait for next interval
                await asyncio.sleep(self.analysis_interval)
        
        except Exception as e:
            self.logger.error(f"Processing error: {str(e)}")
            self.state = ProcessingState.ERROR
            raise e
    
    async def _analyze_metrics(self):
        """Analyze system metrics"""
        self.state = ProcessingState.ANALYZING
        
        try:
            # Get current metrics
            metrics = await self._get_system_metrics()
            
            # Check scaling triggers
            if self._check_triggers(metrics):
                # Execute scaling
                await self._execute_scaling(metrics)
            
            # Update state
            self.state = ProcessingState.IDLE
        
        except Exception as e:
            self.logger.error(f"Analysis error: {str(e)}")
            self.state = ProcessingState.ERROR
            raise e
    
    async def _get_system_metrics(self) -> Dict[str, Any]:
        """Get system metrics"""
        # Mock metrics collection
        return {
            "cpu_usage": 0.75,
            "memory_usage": 0.65,
            "request_count": 1000,
            "latency": 0.2
        }
    
    def _check_triggers(
        self,
        metrics: Dict[str, Any]
    ) -> bool:
        """Check scaling triggers"""
        # Check CPU trigger
        if metrics["cpu_usage"] > 0.8:
            return True
        
        # Check memory trigger
        if metrics["memory_usage"] > 0.8:
            return True
        
        # Check request count trigger
        if metrics["request_count"] > 1000:
            return True
        
        # Check latency trigger
        if metrics["latency"] > 0.5:
            return True
        
        return False
    
    async def _execute_scaling(
        self,
        metrics: Dict[str, Any]
    ):
        """Execute scaling operation"""
        self.state = ProcessingState.EXECUTING
        start_time = datetime.utcnow()
        
        try:
            # Select strategy
            strategy = self._select_strategy()
            
            # Execute scaling
            result = await asyncio.wait_for(
                strategy.scale(metrics),
                timeout=self.execution_timeout
            )
            
            # Update metrics
            self.metrics.total_operations += 1
            
            if result:
                self.metrics.successful_operations += 1
            else:
                self.metrics.failed_operations += 1
            
            # Calculate processing time
            end_time = datetime.utcnow()
            processing_time = (
                end_time - start_time
            ).total_seconds()
            
            # Update average processing time
            self.metrics.average_processing_time = (
                self.metrics.average_processing_time *
                (self.metrics.total_operations - 1) +
                processing_time
            ) / self.metrics.total_operations
            
            # Update last operation time
            self.metrics.last_operation_time = end_time
            
            # Validate scaling
            await self._validate_scaling()
        
        except Exception as e:
            self.logger.error(f"Execution error: {str(e)}")
            self.metrics.failed_operations += 1
            self.state = ProcessingState.ERROR
            raise e
    
    def _select_strategy(
        self
    ) -> Union[HorizontalScaling, VerticalScaling, HybridScaling]:
        """Select scaling strategy"""
        if self.mode == ScalingMode.HORIZONTAL:
            return self.horizontal
        elif self.mode == ScalingMode.VERTICAL:
            return self.vertical
        else:
            return self.hybrid
    
    async def _validate_scaling(self):
        """Validate scaling operation"""
        self.state = ProcessingState.VALIDATING
        
        try:
            # Get post-scaling metrics
            metrics = await self._get_system_metrics()
            
            # Validate metrics
            if self._check_triggers(metrics):
                self.logger.warning(
                    "Scaling validation failed: "
                    "triggers still active"
                )
            else:
                self.logger.info(
                    "Scaling validation successful"
                )
            
            # Update state
            self.state = ProcessingState.IDLE
        
        except Exception as e:
            self.logger.error(f"Validation error: {str(e)}")
            self.state = ProcessingState.ERROR
            raise e
    
    def get_metrics(self) -> ProcessingMetrics:
        """Get processing metrics"""
        return self.metrics
