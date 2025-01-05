"""
Data Excellence Framework - Pipeline
PGF Protocol: DATA_003
Gate: GATE_4
Version: 1.0.0
"""

from typing import Any, Dict, List, Optional, Union, Type
from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum
from .validation import data_validator, ValidationLevel, ValidationScope
from .transformer import data_transformer, TransformationType

class PipelineStage(str, Enum):
    """Data pipeline stages"""
    VALIDATION = "validation"
    TRANSFORMATION = "transformation"
    ENRICHMENT = "enrichment"
    PERSISTENCE = "persistence"

class PipelineConfig(BaseModel):
    """Data pipeline configuration"""
    
    validation_level: ValidationLevel = ValidationLevel.STANDARD
    validation_scope: ValidationScope = ValidationScope.INPUT
    transformation_rules: List[str] = Field(default_factory=list)
    enrichment_enabled: bool = True
    persistence_enabled: bool = True
    
    class Config:
        schema_extra = {
            "example": {
                "validation_level": ValidationLevel.STRICT,
                "validation_scope": ValidationScope.INPUT,
                "transformation_rules": ["datetime_iso8601", "coordinates_normalize"],
                "enrichment_enabled": True,
                "persistence_enabled": True
            }
        }

class PipelineResult(BaseModel):
    """Data pipeline execution result"""
    
    success: bool
    stage: PipelineStage
    data: Any
    validation_result: Optional[Dict[str, Any]] = None
    transformation_result: Optional[Dict[str, Any]] = None
    enrichment_result: Optional[Dict[str, Any]] = None
    persistence_result: Optional[Dict[str, Any]] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class DataPipeline:
    """Enterprise data pipeline orchestrator"""
    
    def __init__(self, config: Optional[PipelineConfig] = None):
        self.config = config or PipelineConfig()
        self._enrichers: Dict[str, callable] = {}
        self._persisters: Dict[str, callable] = {}
    
    def add_enricher(self, name: str, enricher: callable) -> None:
        """Add data enrichment function"""
        self._enrichers[name] = enricher
    
    def add_persister(self, name: str, persister: callable) -> None:
        """Add data persistence function"""
        self._persisters[name] = persister
    
    async def process(
        self,
        data: Union[Dict[str, Any], BaseModel],
        config: Optional[PipelineConfig] = None
    ) -> PipelineResult:
        """Process data through pipeline"""
        pipeline_config = config or self.config
        start_time = datetime.utcnow()
        
        try:
            # Stage 1: Validation
            validation_result = await self._execute_validation(data, pipeline_config)
            if not validation_result["valid"]:
                return PipelineResult(
                    success=False,
                    stage=PipelineStage.VALIDATION,
                    data=data,
                    validation_result=validation_result,
                    metadata={"duration": (datetime.utcnow() - start_time).total_seconds()}
                )
            
            # Stage 2: Transformation
            transformation_result = await self._execute_transformation(
                data,
                pipeline_config.transformation_rules
            )
            if not transformation_result["success"]:
                return PipelineResult(
                    success=False,
                    stage=PipelineStage.TRANSFORMATION,
                    data=data,
                    validation_result=validation_result,
                    transformation_result=transformation_result,
                    metadata={"duration": (datetime.utcnow() - start_time).total_seconds()}
                )
            
            transformed_data = transformation_result["data"]
            
            # Stage 3: Enrichment
            enrichment_result = None
            if pipeline_config.enrichment_enabled:
                enrichment_result = await self._execute_enrichment(transformed_data)
                if enrichment_result["success"]:
                    transformed_data = enrichment_result["data"]
            
            # Stage 4: Persistence
            persistence_result = None
            if pipeline_config.persistence_enabled:
                persistence_result = await self._execute_persistence(transformed_data)
            
            return PipelineResult(
                success=True,
                stage=PipelineStage.PERSISTENCE,
                data=transformed_data,
                validation_result=validation_result,
                transformation_result=transformation_result,
                enrichment_result=enrichment_result,
                persistence_result=persistence_result,
                metadata={
                    "duration": (datetime.utcnow() - start_time).total_seconds(),
                    "pipeline_config": pipeline_config.dict()
                }
            )
            
        except Exception as e:
            return PipelineResult(
                success=False,
                stage=PipelineStage.VALIDATION,
                data=data,
                metadata={
                    "error": str(e),
                    "duration": (datetime.utcnow() - start_time).total_seconds()
                }
            )
    
    async def _execute_validation(
        self,
        data: Union[Dict[str, Any], BaseModel],
        config: PipelineConfig
    ) -> Dict[str, Any]:
        """Execute validation stage"""
        validation_result = await data_validator.validate(
            data,
            level=config.validation_level,
            scope=config.validation_scope
        )
        return validation_result.dict()
    
    async def _execute_transformation(
        self,
        data: Union[Dict[str, Any], BaseModel],
        rules: List[str]
    ) -> Dict[str, Any]:
        """Execute transformation stage"""
        transformation_result = await data_transformer.transform(data, rules)
        return transformation_result.dict()
    
    async def _execute_enrichment(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute enrichment stage"""
        enriched_data = data.copy()
        changes = []
        
        for name, enricher in self._enrichers.items():
            try:
                result = await enricher(enriched_data)
                if result["success"]:
                    enriched_data.update(result["data"])
                    changes.append({
                        "enricher": name,
                        "timestamp": datetime.utcnow().isoformat()
                    })
            except Exception as e:
                return {
                    "success": False,
                    "error": str(e),
                    "data": data
                }
        
        return {
            "success": True,
            "data": enriched_data,
            "changes": changes
        }
    
    async def _execute_persistence(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute persistence stage"""
        results = []
        
        for name, persister in self._persisters.items():
            try:
                result = await persister(data)
                results.append({
                    "persister": name,
                    "success": result["success"],
                    "timestamp": datetime.utcnow().isoformat()
                })
            except Exception as e:
                results.append({
                    "persister": name,
                    "success": False,
                    "error": str(e),
                    "timestamp": datetime.utcnow().isoformat()
                })
        
        return {
            "success": all(r["success"] for r in results),
            "results": results
        }

# Global pipeline instance
data_pipeline = DataPipeline()
