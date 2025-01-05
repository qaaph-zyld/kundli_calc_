"""
Service Scaling Validation
PGF Protocol: SCAL_005
Gate: GATE_36
Version: 1.0.0
"""

from typing import Dict, Any, Optional, List, Union, Set, Tuple
from enum import Enum
from datetime import datetime
from dataclasses import dataclass
import asyncio
import json
import logging
from .config import ScalingConfig, ResourceConfig, ReplicaConfig
from .monitoring import ScalingMonitor

class ValidationLevel(str, Enum):
    """Validation levels"""
    BASIC = "basic"
    STANDARD = "standard"
    STRICT = "strict"

class ValidationScope(str, Enum):
    """Validation scopes"""
    CONFIGURATION = "configuration"
    RESOURCES = "resources"
    PERFORMANCE = "performance"
    COMPLIANCE = "compliance"

class ValidationStatus(str, Enum):
    """Validation status"""
    PENDING = "pending"
    PASSED = "passed"
    FAILED = "failed"
    WARNING = "warning"

@dataclass
class ValidationResult:
    """Validation result"""
    
    scope: ValidationScope
    status: ValidationStatus
    message: str
    timestamp: datetime
    details: Dict[str, Any]

class ValidationRule:
    """Validation rule base class"""
    
    def __init__(
        self,
        name: str,
        scope: ValidationScope,
        level: ValidationLevel = ValidationLevel.STANDARD
    ):
        """Initialize rule"""
        self.name = name
        self.scope = scope
        self.level = level
    
    async def validate(
        self,
        context: Dict[str, Any]
    ) -> ValidationResult:
        """Validate rule"""
        raise NotImplementedError

class ConfigurationRule(ValidationRule):
    """Configuration validation rule"""
    
    def __init__(self):
        """Initialize rule"""
        super().__init__(
            name="configuration_validation",
            scope=ValidationScope.CONFIGURATION,
            level=ValidationLevel.STRICT
        )
    
    async def validate(
        self,
        context: Dict[str, Any]
    ) -> ValidationResult:
        """Validate configuration"""
        try:
            config = context.get("config")
            
            if not config:
                return ValidationResult(
                    scope=self.scope,
                    status=ValidationStatus.FAILED,
                    message="Configuration not found",
                    timestamp=datetime.utcnow(),
                    details={}
                )
            
            # Validate resource config
            resource_valid = self._validate_resources(
                config.resources
            )
            
            if not resource_valid:
                return ValidationResult(
                    scope=self.scope,
                    status=ValidationStatus.FAILED,
                    message="Invalid resource configuration",
                    timestamp=datetime.utcnow(),
                    details={"component": "resources"}
                )
            
            # Validate replica config
            replica_valid = self._validate_replicas(
                config.replicas
            )
            
            if not replica_valid:
                return ValidationResult(
                    scope=self.scope,
                    status=ValidationStatus.FAILED,
                    message="Invalid replica configuration",
                    timestamp=datetime.utcnow(),
                    details={"component": "replicas"}
                )
            
            return ValidationResult(
                scope=self.scope,
                status=ValidationStatus.PASSED,
                message="Configuration validation passed",
                timestamp=datetime.utcnow(),
                details={}
            )
        
        except Exception as e:
            return ValidationResult(
                scope=self.scope,
                status=ValidationStatus.FAILED,
                message=str(e),
                timestamp=datetime.utcnow(),
                details={"error": str(e)}
            )
    
    def _validate_resources(
        self,
        resources: ResourceConfig
    ) -> bool:
        """Validate resource configuration"""
        # Validate CPU configuration
        if not (
            resources.min_cpu <= resources.cpu_request <=
            resources.cpu_limit <= resources.max_cpu
        ):
            return False
        
        # Validate memory configuration
        if not (
            resources.min_memory <= resources.memory_request <=
            resources.memory_limit <= resources.max_memory
        ):
            return False
        
        return True
    
    def _validate_replicas(
        self,
        replicas: ReplicaConfig
    ) -> bool:
        """Validate replica configuration"""
        # Validate replica counts
        if not (
            replicas.min_replicas <= replicas.target_replicas <=
            replicas.max_replicas
        ):
            return False
        
        # Validate thresholds
        if not (
            0.0 <= replicas.scale_down_threshold <
            replicas.scale_up_threshold <= 1.0
        ):
            return False
        
        return True

class ResourceRule(ValidationRule):
    """Resource validation rule"""
    
    def __init__(self):
        """Initialize rule"""
        super().__init__(
            name="resource_validation",
            scope=ValidationScope.RESOURCES,
            level=ValidationLevel.STANDARD
        )
    
    async def validate(
        self,
        context: Dict[str, Any]
    ) -> ValidationResult:
        """Validate resources"""
        try:
            metrics = context.get("metrics", {})
            config = context.get("config")
            
            if not metrics or not config:
                return ValidationResult(
                    scope=self.scope,
                    status=ValidationStatus.FAILED,
                    message="Missing metrics or configuration",
                    timestamp=datetime.utcnow(),
                    details={}
                )
            
            # Validate CPU usage
            cpu_valid = self._validate_cpu(
                metrics,
                config.resources
            )
            
            if not cpu_valid:
                return ValidationResult(
                    scope=self.scope,
                    status=ValidationStatus.WARNING,
                    message="CPU usage outside limits",
                    timestamp=datetime.utcnow(),
                    details={"component": "cpu"}
                )
            
            # Validate memory usage
            memory_valid = self._validate_memory(
                metrics,
                config.resources
            )
            
            if not memory_valid:
                return ValidationResult(
                    scope=self.scope,
                    status=ValidationStatus.WARNING,
                    message="Memory usage outside limits",
                    timestamp=datetime.utcnow(),
                    details={"component": "memory"}
                )
            
            return ValidationResult(
                scope=self.scope,
                status=ValidationStatus.PASSED,
                message="Resource validation passed",
                timestamp=datetime.utcnow(),
                details={}
            )
        
        except Exception as e:
            return ValidationResult(
                scope=self.scope,
                status=ValidationStatus.FAILED,
                message=str(e),
                timestamp=datetime.utcnow(),
                details={"error": str(e)}
            )
    
    def _validate_cpu(
        self,
        metrics: Dict[str, Any],
        resources: ResourceConfig
    ) -> bool:
        """Validate CPU usage"""
        cpu_usage = metrics.get("cpu_usage", 0.0)
        
        return (
            resources.min_cpu <= cpu_usage <= resources.max_cpu
        )
    
    def _validate_memory(
        self,
        metrics: Dict[str, Any],
        resources: ResourceConfig
    ) -> bool:
        """Validate memory usage"""
        memory_usage = metrics.get("memory_usage", 0.0)
        
        return (
            resources.min_memory <= memory_usage <= resources.max_memory
        )

class PerformanceRule(ValidationRule):
    """Performance validation rule"""
    
    def __init__(self):
        """Initialize rule"""
        super().__init__(
            name="performance_validation",
            scope=ValidationScope.PERFORMANCE,
            level=ValidationLevel.STANDARD
        )
    
    async def validate(
        self,
        context: Dict[str, Any]
    ) -> ValidationResult:
        """Validate performance"""
        try:
            metrics = context.get("metrics", {})
            thresholds = context.get("thresholds", {})
            
            if not metrics or not thresholds:
                return ValidationResult(
                    scope=self.scope,
                    status=ValidationStatus.FAILED,
                    message="Missing metrics or thresholds",
                    timestamp=datetime.utcnow(),
                    details={}
                )
            
            # Validate latency
            latency_valid = self._validate_latency(
                metrics,
                thresholds
            )
            
            if not latency_valid:
                return ValidationResult(
                    scope=self.scope,
                    status=ValidationStatus.WARNING,
                    message="Latency outside threshold",
                    timestamp=datetime.utcnow(),
                    details={"component": "latency"}
                )
            
            # Validate throughput
            throughput_valid = self._validate_throughput(
                metrics,
                thresholds
            )
            
            if not throughput_valid:
                return ValidationResult(
                    scope=self.scope,
                    status=ValidationStatus.WARNING,
                    message="Throughput outside threshold",
                    timestamp=datetime.utcnow(),
                    details={"component": "throughput"}
                )
            
            return ValidationResult(
                scope=self.scope,
                status=ValidationStatus.PASSED,
                message="Performance validation passed",
                timestamp=datetime.utcnow(),
                details={}
            )
        
        except Exception as e:
            return ValidationResult(
                scope=self.scope,
                status=ValidationStatus.FAILED,
                message=str(e),
                timestamp=datetime.utcnow(),
                details={"error": str(e)}
            )
    
    def _validate_latency(
        self,
        metrics: Dict[str, Any],
        thresholds: Dict[str, Any]
    ) -> bool:
        """Validate latency"""
        latency = metrics.get("latency", 0.0)
        threshold = thresholds.get("latency", 1.0)
        
        return latency <= threshold
    
    def _validate_throughput(
        self,
        metrics: Dict[str, Any],
        thresholds: Dict[str, Any]
    ) -> bool:
        """Validate throughput"""
        throughput = metrics.get("throughput", 0)
        threshold = thresholds.get("throughput", 1000)
        
        return throughput >= threshold

class ScalingValidator:
    """Scaling validator"""
    
    def __init__(
        self,
        config: ScalingConfig,
        monitor: ScalingMonitor,
        level: ValidationLevel = ValidationLevel.STANDARD
    ):
        """Initialize validator"""
        self.config = config
        self.monitor = monitor
        self.level = level
        
        # Initialize rules
        self._init_rules()
        
        # Initialize logger
        self._init_logger()
    
    def _init_rules(self):
        """Initialize validation rules"""
        self.rules = [
            ConfigurationRule(),
            ResourceRule(),
            PerformanceRule()
        ]
    
    def _init_logger(self):
        """Initialize logger"""
        self.logger = logging.getLogger("scaling_validator")
        self.logger.setLevel(logging.INFO)
        
        # Add handlers if not already added
        if not self.logger.handlers:
            # Console handler
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.INFO)
            
            # File handler
            file_handler = logging.FileHandler(
                "scaling_validator.log"
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
    
    async def validate(
        self
    ) -> List[ValidationResult]:
        """Run validation"""
        results = []
        
        try:
            # Get current context
            context = await self._get_context()
            
            # Run validation rules
            for rule in self.rules:
                # Skip rules above current level
                if (
                    self.level == ValidationLevel.BASIC and
                    rule.level != ValidationLevel.BASIC
                ):
                    continue
                
                if (
                    self.level == ValidationLevel.STANDARD and
                    rule.level == ValidationLevel.STRICT
                ):
                    continue
                
                # Run validation
                result = await rule.validate(context)
                results.append(result)
                
                # Log result
                self._log_result(result)
            
            return results
        
        except Exception as e:
            self.logger.error(f"Validation error: {str(e)}")
            raise e
    
    async def _get_context(self) -> Dict[str, Any]:
        """Get validation context"""
        return {
            "config": self.config,
            "metrics": self.monitor.get_metrics(),
            "thresholds": {
                "latency": 1.0,
                "throughput": 1000
            }
        }
    
    def _log_result(
        self,
        result: ValidationResult
    ):
        """Log validation result"""
        if result.status == ValidationStatus.FAILED:
            self.logger.error(
                f"Validation failed: {result.message}"
            )
        elif result.status == ValidationStatus.WARNING:
            self.logger.warning(
                f"Validation warning: {result.message}"
            )
        else:
            self.logger.info(
                f"Validation passed: {result.message}"
            )
