"""
Data Excellence Framework - Transformation
PGF Protocol: DATA_002
Gate: GATE_4
Version: 1.0.0
"""

from typing import Any, Dict, List, Optional, Union, Type
from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum
import json
import pytz
from decimal import Decimal

class TransformationType(str, Enum):
    """Data transformation types"""
    FORMAT = "format"          # Data format conversion
    NORMALIZE = "normalize"    # Data normalization
    ENRICH = "enrich"         # Data enrichment
    AGGREGATE = "aggregate"    # Data aggregation
    FILTER = "filter"         # Data filtering

class TransformationRule(BaseModel):
    """Data transformation rule"""
    
    name: str
    description: str
    transformation_type: TransformationType
    source_format: Optional[str] = None
    target_format: Optional[str] = None
    parameters: Dict[str, Any] = Field(default_factory=dict)
    priority: int = Field(default=1, ge=1, le=10)
    
    class Config:
        schema_extra = {
            "example": {
                "name": "datetime_format",
                "description": "Convert datetime format",
                "transformation_type": TransformationType.FORMAT,
                "source_format": "%Y-%m-%d %H:%M:%S",
                "target_format": "ISO8601",
                "parameters": {
                    "timezone": "UTC"
                },
                "priority": 1
            }
        }

class TransformationResult(BaseModel):
    """Transformation result"""
    
    success: bool
    data: Any
    changes: List[Dict[str, Any]] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class DataTransformer:
    """Enterprise data transformation engine"""
    
    def __init__(self):
        self._rules: Dict[str, TransformationRule] = {}
        self._custom_transformers: Dict[str, callable] = {}
        self._initialize_default_rules()
    
    def _initialize_default_rules(self) -> None:
        """Initialize default transformation rules"""
        self.add_rule(TransformationRule(
            name="datetime_iso8601",
            description="Convert datetime to ISO8601",
            transformation_type=TransformationType.FORMAT,
            source_format="%Y-%m-%d %H:%M:%S",
            target_format="ISO8601",
            parameters={"timezone": "UTC"}
        ))
        
        self.add_rule(TransformationRule(
            name="coordinates_normalize",
            description="Normalize geographic coordinates",
            transformation_type=TransformationType.NORMALIZE,
            parameters={
                "precision": 6,
                "format": "decimal"
            }
        ))
        
        self.add_rule(TransformationRule(
            name="timezone_convert",
            description="Convert between timezones",
            transformation_type=TransformationType.FORMAT,
            parameters={
                "source_timezone": "UTC",
                "target_timezone": "local"
            }
        ))
    
    def add_rule(self, rule: TransformationRule) -> None:
        """Add transformation rule"""
        self._rules[rule.name] = rule
    
    def add_custom_transformer(self, name: str, transformer: callable) -> None:
        """Add custom transformer function"""
        self._custom_transformers[name] = transformer
    
    async def transform(
        self,
        data: Union[Dict[str, Any], BaseModel],
        rules: Optional[List[str]] = None
    ) -> TransformationResult:
        """Transform data using specified rules"""
        changes = []
        metadata = {
            "rules_applied": [],
            "start_time": datetime.utcnow()
        }
        
        # Convert BaseModel to dict if necessary
        if isinstance(data, BaseModel):
            data = data.dict()
        
        # Make a copy of the original data
        transformed_data = data.copy()
        
        try:
            # Get rules to apply
            rules_to_apply = (
                [self._rules[name] for name in rules]
                if rules
                else sorted(self._rules.values(), key=lambda x: x.priority)
            )
            
            # Apply transformations
            for rule in rules_to_apply:
                if rule.transformation_type == TransformationType.FORMAT:
                    transformed_data = await self._format_transform(transformed_data, rule)
                elif rule.transformation_type == TransformationType.NORMALIZE:
                    transformed_data = await self._normalize_transform(transformed_data, rule)
                elif rule.transformation_type == TransformationType.ENRICH:
                    transformed_data = await self._enrich_transform(transformed_data, rule)
                elif rule.transformation_type == TransformationType.AGGREGATE:
                    transformed_data = await self._aggregate_transform(transformed_data, rule)
                elif rule.transformation_type == TransformationType.FILTER:
                    transformed_data = await self._filter_transform(transformed_data, rule)
                
                metadata["rules_applied"].append(rule.name)
                
                # Record changes
                changes.append({
                    "rule": rule.name,
                    "type": rule.transformation_type,
                    "timestamp": datetime.utcnow().isoformat()
                })
            
            metadata["end_time"] = datetime.utcnow()
            metadata["duration"] = (metadata["end_time"] - metadata["start_time"]).total_seconds()
            
            return TransformationResult(
                success=True,
                data=transformed_data,
                changes=changes,
                metadata=metadata
            )
            
        except Exception as e:
            return TransformationResult(
                success=False,
                data=data,
                changes=changes,
                metadata={
                    **metadata,
                    "error": str(e),
                    "end_time": datetime.utcnow()
                }
            )
    
    async def _format_transform(self, data: Dict[str, Any], rule: TransformationRule) -> Dict[str, Any]:
        """Format transformation implementation"""
        if rule.name == "datetime_iso8601":
            return await self._transform_datetime_to_iso8601(data, rule.parameters)
        elif rule.name == "timezone_convert":
            return await self._transform_timezone(data, rule.parameters)
        return data
    
    async def _normalize_transform(self, data: Dict[str, Any], rule: TransformationRule) -> Dict[str, Any]:
        """Normalization transformation implementation"""
        if rule.name == "coordinates_normalize":
            return await self._normalize_coordinates(data, rule.parameters)
        return data
    
    async def _transform_datetime_to_iso8601(
        self,
        data: Dict[str, Any],
        parameters: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Convert datetime to ISO8601 format"""
        result = data.copy()
        timezone = pytz.timezone(parameters.get("timezone", "UTC"))
        
        for key, value in data.items():
            if isinstance(value, str) and "date" in key.lower():
                try:
                    dt = datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
                    dt = timezone.localize(dt)
                    result[key] = dt.isoformat()
                except (ValueError, TypeError):
                    pass
        
        return result
    
    async def _normalize_coordinates(
        self,
        data: Dict[str, Any],
        parameters: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Normalize geographic coordinates"""
        result = data.copy()
        precision = parameters.get("precision", 6)
        
        for key, value in data.items():
            if key in ["latitude", "longitude"] and isinstance(value, (int, float)):
                result[key] = round(Decimal(str(value)), precision)
        
        return result
    
    async def _transform_timezone(
        self,
        data: Dict[str, Any],
        parameters: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Convert between timezones"""
        result = data.copy()
        source_tz = pytz.timezone(parameters.get("source_timezone", "UTC"))
        target_tz = pytz.timezone(parameters.get("target_timezone", "UTC"))
        
        for key, value in data.items():
            if isinstance(value, str) and "time" in key.lower():
                try:
                    dt = datetime.fromisoformat(value)
                    if dt.tzinfo is None:
                        dt = source_tz.localize(dt)
                    result[key] = dt.astimezone(target_tz).isoformat()
                except (ValueError, TypeError):
                    pass
        
        return result

# Global transformer instance
data_transformer = DataTransformer()
