"""
Service Scaling Configuration
PGF Protocol: SCAL_003
Gate: GATE_34
Version: 1.0.0
"""

from typing import Dict, Any, Optional, List, Union, Set
from enum import Enum
from datetime import datetime
from dataclasses import dataclass
from pydantic import BaseModel, Field
import json
import logging
from .strategies import ScalingMode, ScalingTrigger

class ResourceConfig(BaseModel):
    """Resource configuration"""
    
    min_cpu: float = Field(
        default=0.1,
        ge=0.1,
        le=4.0,
        description="Minimum CPU cores"
    )
    max_cpu: float = Field(
        default=4.0,
        ge=0.1,
        le=8.0,
        description="Maximum CPU cores"
    )
    min_memory: int = Field(
        default=128,
        ge=64,
        le=8192,
        description="Minimum memory in MB"
    )
    max_memory: int = Field(
        default=8192,
        ge=128,
        le=16384,
        description="Maximum memory in MB"
    )
    cpu_request: float = Field(
        default=0.5,
        ge=0.1,
        le=4.0,
        description="CPU request in cores"
    )
    memory_request: int = Field(
        default=512,
        ge=64,
        le=8192,
        description="Memory request in MB"
    )
    cpu_limit: float = Field(
        default=2.0,
        ge=0.1,
        le=8.0,
        description="CPU limit in cores"
    )
    memory_limit: int = Field(
        default=4096,
        ge=128,
        le=16384,
        description="Memory limit in MB"
    )

class ReplicaConfig(BaseModel):
    """Replica configuration"""
    
    min_replicas: int = Field(
        default=1,
        ge=1,
        le=100,
        description="Minimum replicas"
    )
    max_replicas: int = Field(
        default=10,
        ge=1,
        le=1000,
        description="Maximum replicas"
    )
    target_replicas: int = Field(
        default=2,
        ge=1,
        le=100,
        description="Target replicas"
    )
    scale_up_threshold: float = Field(
        default=0.8,
        ge=0.1,
        le=1.0,
        description="Scale up threshold"
    )
    scale_down_threshold: float = Field(
        default=0.2,
        ge=0.0,
        le=0.9,
        description="Scale down threshold"
    )

class TriggerConfig(BaseModel):
    """Trigger configuration"""
    
    cpu_threshold: float = Field(
        default=0.8,
        ge=0.1,
        le=1.0,
        description="CPU utilization threshold"
    )
    memory_threshold: float = Field(
        default=0.8,
        ge=0.1,
        le=1.0,
        description="Memory utilization threshold"
    )
    request_threshold: int = Field(
        default=1000,
        ge=100,
        le=10000,
        description="Request count threshold"
    )
    latency_threshold: float = Field(
        default=0.5,
        ge=0.1,
        le=5.0,
        description="Latency threshold in seconds"
    )
    evaluation_period: int = Field(
        default=60,
        ge=30,
        le=3600,
        description="Evaluation period in seconds"
    )
    cooldown_period: int = Field(
        default=300,
        ge=60,
        le=3600,
        description="Cooldown period in seconds"
    )

class PolicyConfig(BaseModel):
    """Policy configuration"""
    
    mode: ScalingMode = Field(
        default=ScalingMode.HYBRID,
        description="Scaling mode"
    )
    triggers: List[ScalingTrigger] = Field(
        default=[
            ScalingTrigger.CPU_USAGE,
            ScalingTrigger.MEMORY_USAGE
        ],
        description="Active triggers"
    )
    priority_triggers: List[ScalingTrigger] = Field(
        default=[ScalingTrigger.CPU_USAGE],
        description="Priority triggers"
    )
    scale_up_factor: float = Field(
        default=1.5,
        ge=1.1,
        le=5.0,
        description="Scale up factor"
    )
    scale_down_factor: float = Field(
        default=0.75,
        ge=0.1,
        le=0.9,
        description="Scale down factor"
    )

class ScalingConfig(BaseModel):
    """Scaling configuration"""
    
    resources: ResourceConfig = Field(
        default_factory=ResourceConfig,
        description="Resource configuration"
    )
    replicas: ReplicaConfig = Field(
        default_factory=ReplicaConfig,
        description="Replica configuration"
    )
    triggers: TriggerConfig = Field(
        default_factory=TriggerConfig,
        description="Trigger configuration"
    )
    policy: PolicyConfig = Field(
        default_factory=PolicyConfig,
        description="Policy configuration"
    )

class ConfigurationManager:
    """Configuration manager"""
    
    def __init__(
        self,
        config_path: Optional[str] = None
    ):
        """Initialize manager"""
        self.config_path = config_path
        self.config = ScalingConfig()
        
        # Initialize logger
        self._init_logger()
        
        # Load configuration
        if config_path:
            self.load_config()
    
    def _init_logger(self):
        """Initialize logger"""
        self.logger = logging.getLogger("scaling_config")
        self.logger.setLevel(logging.INFO)
        
        # Add handlers if not already added
        if not self.logger.handlers:
            # Console handler
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.INFO)
            
            # File handler
            file_handler = logging.FileHandler(
                "scaling_config.log"
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
    
    def load_config(self):
        """Load configuration from file"""
        try:
            with open(self.config_path, "r") as f:
                config_data = json.load(f)
                self.config = ScalingConfig(**config_data)
                self.logger.info("Configuration loaded successfully")
        
        except Exception as e:
            self.logger.error(f"Failed to load configuration: {str(e)}")
            raise e
    
    def save_config(self):
        """Save configuration to file"""
        try:
            config_data = self.config.dict()
            
            with open(self.config_path, "w") as f:
                json.dump(
                    config_data,
                    f,
                    indent=4
                )
            
            self.logger.info("Configuration saved successfully")
        
        except Exception as e:
            self.logger.error(f"Failed to save configuration: {str(e)}")
            raise e
    
    def update_config(
        self,
        config_data: Dict[str, Any]
    ):
        """Update configuration"""
        try:
            # Update configuration
            self.config = ScalingConfig(**config_data)
            
            # Save if path exists
            if self.config_path:
                self.save_config()
            
            self.logger.info("Configuration updated successfully")
        
        except Exception as e:
            self.logger.error(f"Failed to update configuration: {str(e)}")
            raise e
    
    def validate_config(
        self,
        config_data: Dict[str, Any]
    ) -> bool:
        """Validate configuration"""
        try:
            # Validate using pydantic
            ScalingConfig(**config_data)
            return True
        
        except Exception as e:
            self.logger.error(f"Configuration validation failed: {str(e)}")
            return False
    
    def get_resource_config(self) -> ResourceConfig:
        """Get resource configuration"""
        return self.config.resources
    
    def get_replica_config(self) -> ReplicaConfig:
        """Get replica configuration"""
        return self.config.replicas
    
    def get_trigger_config(self) -> TriggerConfig:
        """Get trigger configuration"""
        return self.config.triggers
    
    def get_policy_config(self) -> PolicyConfig:
        """Get policy configuration"""
        return self.config.policy
    
    def get_full_config(self) -> Dict[str, Any]:
        """Get full configuration"""
        return self.config.dict()
