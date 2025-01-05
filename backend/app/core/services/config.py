"""
Service Configuration Manager
PGF Protocol: SERVICE_003
Gate: GATE_4
Version: 1.0.0
"""

from typing import Dict, List, Optional, Any, Union
from pydantic import BaseModel, Field
from datetime import datetime
import json
import os
from pathlib import Path
from .registry import ServiceType, ServiceDefinition, ServiceEndpoint

class ServiceConfig(BaseModel):
    """Service configuration"""
    
    name: str
    version: str
    type: ServiceType
    description: str
    base_url: str
    endpoints: Dict[str, Dict[str, Any]]
    dependencies: List[str] = Field(default_factory=list)
    settings: Dict[str, Any] = Field(default_factory=dict)
    environment: Dict[str, str] = Field(default_factory=dict)
    metadata: Dict[str, Any] = Field(default_factory=dict)

class ConfigurationSource(BaseModel):
    """Configuration source definition"""
    
    name: str
    type: str
    location: str
    priority: int = 1
    refresh_interval: Optional[int] = None
    last_refresh: Optional[datetime] = None

class ConfigManager:
    """Service configuration manager"""
    
    def __init__(self, config_dir: Optional[str] = None):
        self._config_dir = config_dir or "config"
        self._configs: Dict[str, ServiceConfig] = {}
        self._sources: Dict[str, ConfigurationSource] = {}
        self._initialize_sources()
    
    def _initialize_sources(self) -> None:
        """Initialize configuration sources"""
        self.add_source(ConfigurationSource(
            name="local",
            type="file",
            location=os.path.join(self._config_dir, "local"),
            priority=1
        ))
        
        self.add_source(ConfigurationSource(
            name="environment",
            type="env",
            location="",
            priority=2
        ))
        
        self.add_source(ConfigurationSource(
            name="remote",
            type="http",
            location=os.getenv("REMOTE_CONFIG_URL", ""),
            priority=3,
            refresh_interval=300
        ))
    
    def add_source(self, source: ConfigurationSource) -> None:
        """Add configuration source"""
        self._sources[source.name] = source
    
    def load_config(self, service_name: str) -> ServiceConfig:
        """Load service configuration"""
        config_data = {}
        
        # Load from each source in priority order
        for source in sorted(self._sources.values(), key=lambda x: x.priority):
            try:
                source_data = self._load_from_source(source, service_name)
                if source_data:
                    config_data.update(source_data)
            except Exception as e:
                print(f"Error loading config from {source.name}: {e}")
        
        if not config_data:
            raise ValueError(f"No configuration found for service {service_name}")
        
        config = ServiceConfig(**config_data)
        self._configs[service_name] = config
        
        return config
    
    def _load_from_source(
        self,
        source: ConfigurationSource,
        service_name: str
    ) -> Optional[Dict[str, Any]]:
        """Load configuration from source"""
        if source.type == "file":
            return self._load_from_file(source, service_name)
        elif source.type == "env":
            return self._load_from_env(service_name)
        elif source.type == "http":
            return self._load_from_remote(source, service_name)
        return None
    
    def _load_from_file(
        self,
        source: ConfigurationSource,
        service_name: str
    ) -> Optional[Dict[str, Any]]:
        """Load configuration from file"""
        config_file = os.path.join(source.location, f"{service_name}.json")
        if not os.path.exists(config_file):
            return None
            
        with open(config_file, "r") as f:
            return json.load(f)
    
    def _load_from_env(self, service_name: str) -> Dict[str, Any]:
        """Load configuration from environment variables"""
        prefix = f"{service_name.upper()}_"
        config = {}
        
        for key, value in os.environ.items():
            if key.startswith(prefix):
                config_key = key[len(prefix):].lower()
                try:
                    # Try to parse as JSON for complex values
                    config[config_key] = json.loads(value)
                except json.JSONDecodeError:
                    config[config_key] = value
        
        return config
    
    def _load_from_remote(
        self,
        source: ConfigurationSource,
        service_name: str
    ) -> Optional[Dict[str, Any]]:
        """Load configuration from remote source"""
        # Implement remote configuration loading
        # For now, return None
        return None
    
    def get_config(self, service_name: str) -> ServiceConfig:
        """Get service configuration"""
        if service_name not in self._configs:
            return self.load_config(service_name)
        return self._configs[service_name]
    
    def update_config(
        self,
        service_name: str,
        updates: Dict[str, Any]
    ) -> ServiceConfig:
        """Update service configuration"""
        config = self.get_config(service_name)
        
        # Update configuration
        config_dict = config.dict()
        self._deep_update(config_dict, updates)
        
        # Validate and store updated config
        updated_config = ServiceConfig(**config_dict)
        self._configs[service_name] = updated_config
        
        return updated_config
    
    def _deep_update(
        self,
        base_dict: Dict[str, Any],
        update_dict: Dict[str, Any]
    ) -> None:
        """Deep update dictionary"""
        for key, value in update_dict.items():
            if (
                key in base_dict
                and isinstance(base_dict[key], dict)
                and isinstance(value, dict)
            ):
                self._deep_update(base_dict[key], value)
            else:
                base_dict[key] = value
    
    def create_service_definition(
        self,
        service_name: str
    ) -> ServiceDefinition:
        """Create service definition from configuration"""
        config = self.get_config(service_name)
        
        # Convert config endpoints to ServiceEndpoint objects
        endpoints = {
            name: ServiceEndpoint(**endpoint_config)
            for name, endpoint_config in config.endpoints.items()
        }
        
        return ServiceDefinition(
            name=config.name,
            version=config.version,
            type=config.type,
            description=config.description,
            endpoints=endpoints,
            dependencies=config.dependencies,
            metadata={
                **config.metadata,
                "base_url": config.base_url,
                "settings": config.settings,
                "environment": config.environment
            }
        )

# Global configuration manager instance
config_manager = ConfigManager()
