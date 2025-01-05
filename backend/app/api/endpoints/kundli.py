"""
Kundli Calculation Endpoints
PGF Protocol: KUNDLI_001
Gate: GATE_4
Version: 1.0.0
"""

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field, validator
from datetime import datetime
from typing import Dict, List, Any, Optional
from app.core.calculations.astronomical import AstronomicalCalculator
from app.models.location import Location
from app.core.validation.validation_framework import ValidationFramework
from app.core.schemas.base import BaseResponse
from app.core.schemas.error import ErrorResponse
from app.core.data.pipeline import data_pipeline, PipelineConfig, ValidationLevel, ValidationScope
from app.core.services.registry import service_registry, ServiceType, ServiceStatus
from app.core.services.integration import integration_manager, IntegrationProtocol, IntegrationPolicy
from app.core.services.config import config_manager
from app.core.storage.repository import kundli_repository, pattern_repository, KundliData, PatternData
from app.core.security.engine import security_engine, SecurityScope
from app.core.security.authorization import authorization_manager, Role, ResourceType, Permission
from app.core.caching.strategy import cache_manager, DataType
from app.core.monitoring import monitor

router = APIRouter()

# Initialize services
calculation_service = config_manager.create_service_definition("kundli_calculation")
analysis_service = config_manager.create_service_definition("kundli_analysis")

# Register services
service_registry.register_service(calculation_service)
service_registry.register_service(analysis_service)

# Register integrations
calculation_integration = integration_manager.register_integration(
    calculation_service,
    IntegrationPolicy(
        protocol=IntegrationProtocol.REST,
        timeout=60,
        retry_count=3,
        cache_ttl=300
    )
)

analysis_integration = integration_manager.register_integration(
    analysis_service,
    IntegrationPolicy(
        protocol=IntegrationProtocol.REST,
        timeout=30,
        retry_count=2,
        cache_ttl=600
    )
)

class KundliRequest(BaseModel):
    """Request model for kundli calculation with enhanced validation"""
    
    date: str = Field(..., description="Date in YYYY-MM-DD format")
    time: str = Field(..., description="Time in HH:MM:SS format")
    latitude: float = Field(..., description="Latitude in decimal degrees", ge=-90, le=90)
    longitude: float = Field(..., description="Longitude in decimal degrees", ge=-180, le=180)
    timezone: str = Field(..., description="Timezone name (e.g., 'Asia/Kolkata')")
    
    @validator('date')
    def validate_date(cls, v):
        try:
            datetime.strptime(v, "%Y-%m-%d")
            return v
        except ValueError:
            raise ValueError("Invalid date format. Use YYYY-MM-DD")
    
    @validator('time')
    def validate_time(cls, v):
        try:
            datetime.strptime(v, "%H:%M:%S")
            return v
        except ValueError:
            raise ValueError("Invalid time format. Use HH:MM:SS")

class KundliResponse(BaseResponse):
    """Standardized response model for kundli calculations"""
    
    data: Dict[str, Any] = Field(..., description="Kundli calculation results")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional calculation metadata")
    
    class Config:
        schema_extra = {
            "example": {
                "status": "success",
                "data": {
                    "planets": {},
                    "houses": {},
                    "aspects": {}
                },
                "metadata": {
                    "calculation_time": "0.123s",
                    "ayanamsa_used": "Lahiri",
                    "house_system": "Placidus"
                },
                "timestamp": "2024-12-29T21:59:58+01:00"
            }
        }

class ValidationRequest(BaseModel):
    """Request model for kundli data validation"""
    
    data: KundliRequest = Field(..., description="Kundli data to validate")
    validation_level: str = Field("STANDARD", description="Validation level (STRICT, STANDARD, RELAXED)")
    validation_scope: str = Field("ALL", description="Validation scope (ALL, INPUT, CALCULATION, OUTPUT, SYSTEM)")

class CorrelationRequest(BaseModel):
    """Request model for kundli correlation analysis"""
    
    kundli1: KundliRequest = Field(..., description="First kundli data")
    kundli2: KundliRequest = Field(..., description="Second kundli data")
    analysis_type: str = Field("FULL", description="Type of analysis (FULL, BASIC, CUSTOM)")

class PatternsResponse(BaseResponse):
    """Standardized response model for planetary patterns"""
    
    data: Dict[str, Any] = Field(..., description="Planetary patterns")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional pattern metadata")
    
    class Config:
        schema_extra = {
            "example": {
                "status": "success",
                "data": {
                    "yogas": [],
                    "raja_yogas": [],
                    "dhana_yogas": [],
                    "malefic_patterns": [],
                    "benefic_patterns": []
                },
                "metadata": {
                    "pattern_detection_time": "0.123s",
                    "pattern_analysis_time": "0.456s"
                },
                "timestamp": "2024-12-29T21:59:58+01:00"
            }
        }

class CorrelationResponse(BaseResponse):
    """Standardized response model for kundli correlation analysis"""
    
    data: Dict[str, Any] = Field(..., description="Correlation analysis results")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional correlation metadata")
    
    class Config:
        schema_extra = {
            "example": {
                "status": "success",
                "data": {
                    "overall_score": 0.8,
                    "aspects": [],
                    "factors": {
                        "temperament": 0.7,
                        "mental": 0.6,
                        "emotional": 0.8,
                        "spiritual": 0.9,
                        "physical": 0.5
                    }
                },
                "metadata": {
                    "correlation_time": "0.123s",
                    "analysis_time": "0.456s"
                },
                "timestamp": "2024-12-29T21:59:58+01:00"
            }
        }

class ValidationResponse(BaseResponse):
    """Standardized response model for kundli data validation"""
    
    data: Dict[str, Any] = Field(..., description="Validation results")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional validation metadata")
    
    class Config:
        schema_extra = {
            "example": {
                "status": "success",
                "data": {
                    "is_valid": True,
                    "errors": []
                },
                "metadata": {
                    "validation_time": "0.123s"
                },
                "timestamp": "2024-12-29T21:59:58+01:00"
            }
        }

@router.post("/calculate", response_model=KundliResponse)
async def calculate_kundli(
    request: KundliRequest,
    current_user: TokenData = Depends(security_engine.get_current_user)
):
    """Calculate Kundli based on input parameters"""
    # Check authorization
    if not authorization_manager.has_permission(
        role=current_user.metadata.get("role", Role.GUEST),
        resource_type=ResourceType.KUNDLI,
        permission=Permission.CREATE
    ):
        raise HTTPException(
            status_code=403,
            detail="Insufficient permissions to calculate Kundli"
        )
    
    pipeline_config = PipelineConfig(
        validation_level=ValidationLevel.STRICT,
        validation_scope=ValidationScope.INPUT,
        transformation_rules=["datetime_iso8601", "coordinates_normalize"],
        enrichment_enabled=True
    )
    
    pipeline_result = await data_pipeline.process(request.dict(), pipeline_config)
    if not pipeline_result.success:
        raise HTTPException(
            status_code=422,
            detail={
                "message": "Data validation failed",
                "errors": pipeline_result.validation_result["errors"] if pipeline_result.validation_result else None
            }
        )
    
    try:
        # Start monitoring
        with monitor.track_request("calculate_kundli"):
            calculation_result = await calculation_integration.execute(
                "calculate",
                data=pipeline_result.data
            )
            
            kundli_data = KundliData(
                date=pipeline_result.data["date"],
                time=pipeline_result.data["time"],
                latitude=pipeline_result.data["latitude"],
                longitude=pipeline_result.data["longitude"],
                timezone=pipeline_result.data["timezone"],
                planets=calculation_result["planets"],
                houses=calculation_result["houses"],
                aspects=calculation_result["aspects"],
                user_id=current_user.sub
            )
            
            kundli_id = await kundli_repository.create(kundli_data)
            
            # Cache the result
            await cache_manager.cache.set(
                cache_manager.build_key(DataType.KUNDLI, kundli_id),
                kundli_data.dict()
            )
            
            return KundliResponse(
                status="success",
                data={**calculation_result, "id": kundli_id},
                metadata={
                    "processing_time": pipeline_result.metadata["duration"],
                    "calculation_time": calculation_result.get("calculation_time"),
                    "service_version": calculation_service.version
                }
            )
        
    except Exception as e:
        service_registry.update_service_status(calculation_service.id, ServiceStatus.DEGRADED)
        raise HTTPException(
            status_code=500,
            detail=f"Calculation service error: {str(e)}"
        )

@router.post("/patterns", response_model=PatternsResponse)
async def analyze_patterns(
    request: Dict[str, Any],
    current_user: TokenData = Depends(security_engine.get_current_user)
):
    """Analyze astrological patterns"""
    # Check authorization
    if not authorization_manager.has_permission(
        role=current_user.metadata.get("role", Role.GUEST),
        resource_type=ResourceType.PATTERN,
        permission=Permission.CREATE
    ):
        raise HTTPException(
            status_code=403,
            detail="Insufficient permissions to analyze patterns"
        )
    
    pipeline_config = PipelineConfig(
        validation_level=ValidationLevel.STANDARD,
        validation_scope=ValidationScope.INPUT,
        transformation_rules=["datetime_iso8601"],
        enrichment_enabled=True
    )
    
    pipeline_result = await data_pipeline.process(request, pipeline_config)
    if not pipeline_result.success:
        raise HTTPException(
            status_code=422,
            detail={
                "message": "Data validation failed",
                "errors": pipeline_result.validation_result["errors"] if pipeline_result.validation_result else None
            }
        )
    
    try:
        # Start monitoring
        with monitor.track_request("analyze_patterns"):
            # Verify Kundli ownership
            kundli = await kundli_repository.find_by_id(pipeline_result.data["kundli_id"])
            if not kundli or kundli.user_id != current_user.sub:
                raise HTTPException(
                    status_code=404,
                    detail="Kundli not found or access denied"
                )
            
            analysis_result = await analysis_integration.execute(
                "analyze_patterns",
                data=pipeline_result.data
            )
            
            pattern_data = PatternData(
                kundli_id=pipeline_result.data["kundli_id"],
                yogas=analysis_result["yogas"],
                raja_yogas=analysis_result["raja_yogas"],
                dhana_yogas=analysis_result["dhana_yogas"],
                malefic_patterns=analysis_result["malefic_patterns"],
                benefic_patterns=analysis_result["benefic_patterns"],
                analysis=analysis_result["analysis"],
                user_id=current_user.sub
            )
            
            pattern_id = await pattern_repository.create(pattern_data)
            
            # Cache the result
            await cache_manager.cache.set(
                cache_manager.build_key(DataType.PATTERN, pattern_id),
                pattern_data.dict()
            )
            
            return PatternsResponse(
                status="success",
                data={**analysis_result, "id": pattern_id},
                metadata={
                    "processing_time": pipeline_result.metadata["duration"],
                    "analysis_time": analysis_result.get("analysis_time"),
                    "service_version": analysis_service.version,
                    "pattern_count": len(analysis_result.get("patterns", []))
                }
            )
        
    except Exception as e:
        service_registry.update_service_status(analysis_service.id, ServiceStatus.DEGRADED)
        raise HTTPException(
            status_code=500,
            detail=f"Analysis service error: {str(e)}"
        )

@router.get("/kundli/{kundli_id}", response_model=KundliResponse)
@cache_manager.cached_kundli()
async def get_kundli(
    kundli_id: str,
    current_user: TokenData = Depends(security_engine.get_current_user)
):
    """Get Kundli by ID"""
    # Check authorization
    if not authorization_manager.has_permission(
        role=current_user.metadata.get("role", Role.GUEST),
        resource_type=ResourceType.KUNDLI,
        permission=Permission.READ
    ):
        raise HTTPException(
            status_code=403,
            detail="Insufficient permissions to read Kundli"
        )
    
    try:
        # Start monitoring
        with monitor.track_request("get_kundli"):
            kundli_data = await kundli_repository.find_by_id(kundli_id)
            if not kundli_data:
                raise HTTPException(
                    status_code=404,
                    detail=f"Kundli with ID {kundli_id} not found"
                )
            
            # Verify ownership unless admin
            if (current_user.metadata.get("role") != Role.ADMIN and
                kundli_data.user_id != current_user.sub):
                raise HTTPException(
                    status_code=403,
                    detail="Access denied"
                )
            
            return KundliResponse(
                status="success",
                data=kundli_data.dict(),
                metadata={
                    "retrieved_at": datetime.utcnow().isoformat()
                }
            )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving Kundli: {str(e)}"
        )

@router.get("/patterns/{kundli_id}", response_model=PatternsResponse)
@cache_manager.cached_pattern()
async def get_patterns(
    kundli_id: str,
    current_user: TokenData = Depends(security_engine.get_current_user)
):
    """Get patterns by Kundli ID"""
    # Check authorization
    if not authorization_manager.has_permission(
        role=current_user.metadata.get("role", Role.GUEST),
        resource_type=ResourceType.PATTERN,
        permission=Permission.READ
    ):
        raise HTTPException(
            status_code=403,
            detail="Insufficient permissions to read patterns"
        )
    
    try:
        # Start monitoring
        with monitor.track_request("get_patterns"):
            pattern_data = await pattern_repository.find_one(
                filters={"kundli_id": {QueryOperator.EQ: kundli_id}}
            )
            
            if not pattern_data:
                raise HTTPException(
                    status_code=404,
                    detail=f"Patterns for Kundli ID {kundli_id} not found"
                )
            
            # Verify ownership unless admin
            if (current_user.metadata.get("role") != Role.ADMIN and
                pattern_data.user_id != current_user.sub):
                raise HTTPException(
                    status_code=403,
                    detail="Access denied"
                )
            
            return PatternsResponse(
                status="success",
                data=pattern_data.dict(),
                metadata={
                    "retrieved_at": datetime.utcnow().isoformat()
                }
            )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving patterns: {str(e)}"
        )

@router.post("/correlate", response_model=CorrelationResponse)
async def analyze_correlation(request: CorrelationRequest):
    """Analyze correlation between two kundlis"""
    pipeline_config = PipelineConfig(
        validation_level=ValidationLevel.STRICT,
        validation_scope=ValidationScope.INPUT,
        transformation_rules=["datetime_iso8601", "coordinates_normalize"],
        enrichment_enabled=True
    )
    
    pipeline_result = await data_pipeline.process(request.dict(), pipeline_config)
    if not pipeline_result.success:
        raise HTTPException(
            status_code=422,
            detail={
                "message": "Data validation failed",
                "errors": pipeline_result.validation_result["errors"] if pipeline_result.validation_result else None
            }
        )
    
    try:
        # Start monitoring
        with monitor.track_request("analyze_correlation"):
            correlation_result = await analysis_integration.execute(
                "correlate_charts",
                data=pipeline_result.data
            )
            
            return CorrelationResponse(
                status="success",
                data=correlation_result,
                metadata={
                    "processing_time": pipeline_result.metadata["duration"],
                    "correlation_time": correlation_result.get("correlation_time"),
                    "service_version": analysis_service.version,
                    "charts_correlated": 2
                }
            )
        
    except Exception as e:
        service_registry.update_service_status(analysis_service.id, ServiceStatus.DEGRADED)
        raise HTTPException(
            status_code=500,
            detail=f"Correlation service error: {str(e)}"
        )

@router.post("/validate", response_model=ValidationResponse)
async def validate_kundli(request: ValidationRequest):
    """Validate kundli data"""
    level = ValidationLevel[request.validation_level]
    scope = ValidationScope[request.validation_scope]
    
    pipeline_config = PipelineConfig(
        validation_level=level,
        validation_scope=scope,
        transformation_rules=["datetime_iso8601", "coordinates_normalize"],
        enrichment_enabled=True
    )
    
    pipeline_result = await data_pipeline.process(request.data.dict(), pipeline_config)
    if not pipeline_result.success:
        raise HTTPException(
            status_code=422,
            detail={
                "message": "Data validation failed",
                "errors": pipeline_result.validation_result["errors"] if pipeline_result.validation_result else None
            }
        )
    
    validator = ValidationFramework(default_level=level)
    
    data = pipeline_result.data
    
    results = await validator.validate(data, scope=scope, level=level)
    
    is_valid = all(result.is_valid for result in results)
    errors = [
        {
            "rule": result.rule_name,
            "scope": result.scope.value,
            "level": result.level.value,
            "message": result.error_message
        }
        for result in results if not result.is_valid
    ]
    
    return ValidationResponse(
        status="success",
        data={
            "is_valid": is_valid,
            "errors": errors
        },
        metadata={
            "validation_time": "0.123s",
            "processing_time": pipeline_result.metadata["duration"],
            "validation_level": pipeline_config.validation_level,
            "transformations_applied": pipeline_result.transformation_result["changes"] if pipeline_result.transformation_result else None
        }
    )

class EnhancedKundliRequest(BaseModel):
    """Enhanced Kundli calculation request model"""
    date: str = Field(..., description="Date in YYYY-MM-DD format")
    time: str = Field(..., description="Time in HH:MM:SS format")
    latitude: float = Field(..., description="Latitude in decimal degrees", ge=-90, le=90)
    longitude: float = Field(..., description="Longitude in decimal degrees", ge=-180, le=180)
    timezone: str = Field(..., description="Timezone name (e.g., 'Asia/Kolkata')")
    ayanamsa: Optional[str] = Field("lahiri", description="Ayanamsa system to use")
    house_system: Optional[str] = Field("placidus", description="House system to use")
    calculation_options: Dict[str, Any] = Field(
        default_factory=dict,
        description="Additional calculation options"
    )
    
    @validator("date")
    def validate_date(cls, v):
        try:
            datetime.strptime(v, "%Y-%m-%d")
            return v
        except ValueError:
            raise ValueError("Invalid date format. Use YYYY-MM-DD")
            
    @validator("time")
    def validate_time(cls, v):
        try:
            datetime.strptime(v, "%H:%M:%S")
            return v
        except ValueError:
            raise ValueError("Invalid time format. Use HH:MM:SS")
            
    @validator("timezone")
    def validate_timezone(cls, v):
        from zoneinfo import ZoneInfo
        try:
            ZoneInfo(v)
            return v
        except Exception:
            raise ValueError("Invalid timezone")

class EnhancedKundliResponse(BaseModel):
    """Enhanced Kundli calculation response model"""
    request_id: str = Field(..., description="Unique request identifier")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    input_data: Dict[str, Any] = Field(..., description="Input parameters")
    planets: Dict[str, Any] = Field(..., description="Planetary positions")
    houses: Dict[str, Any] = Field(..., description="House positions")
    aspects: List[Dict[str, Any]] = Field(..., description="Planetary aspects")
    yogas: List[Dict[str, Any]] = Field(default_factory=list, description="Yoga combinations")
    dashas: Dict[str, Any] = Field(default_factory=dict, description="Dasha periods")
    ashtakavarga: Dict[str, Any] = Field(default_factory=dict, description="Ashtakavarga points")
    charts: Dict[str, Any] = Field(default_factory=dict, description="Various chart types")
    predictions: Dict[str, Any] = Field(default_factory=dict, description="Basic predictions")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Calculation metadata")

@router.post("/enhanced_calculate", response_model=EnhancedKundliResponse, responses={400: {"model": ErrorResponse}})
async def enhanced_calculate_kundli(
    request: EnhancedKundliRequest,
    detailed: bool = Query(False, description="Include detailed calculations"),
    current_user: TokenData = Depends(security_engine.get_current_user)
) -> EnhancedKundliResponse:
    """
    Calculate comprehensive Kundli based on input parameters
    """
    start_time = datetime.utcnow()
    
    try:
        # Start monitoring
        with monitor.track_request("enhanced_calculate_kundli"):
            # Validate input data
            validation_result = await validation_framework.validate(
                request.dict(),
                level=ValidationLevel.STRICT,
                scope=ValidationScope.INPUT
            )
            
            if not validation_result.is_valid:
                raise HTTPException(
                    status_code=400,
                    detail={
                        "message": "Validation failed",
                        "errors": [error.dict() for error in validation_result.errors]
                    }
                )
                
            # Check cache
            cache_key = f"kundli:{hash(str(request.dict()))}"
            cached_result = await cache_manager.get(cache_key)
            if cached_result:
                return EnhancedKundliResponse(**cached_result)
                
            # Initialize components
            astro_calc = AstronomicalCalculator()
            pattern_detector = PatternDetector()
            correlation_analyzer = CorrelationAnalyzer()
            yoga_engine = YogaEngine()
            prediction_engine = PredictionEngine()

            # Calculate planetary positions
            planets = await astro_calc.calculate_planets(
                date=request.date,
                time=request.time,
                latitude=request.latitude,
                longitude=request.longitude,
                timezone=request.timezone,
                ayanamsa=request.ayanamsa
            )
            
            # Calculate houses
            houses = await astro_calc.calculate_houses(
                date=request.date,
                time=request.time,
                latitude=request.latitude,
                longitude=request.longitude,
                timezone=request.timezone,
                system=request.house_system
            )
            
            # Calculate aspects
            aspects = await astro_calc.calculate_aspects(planets)
            
            # Detect patterns and yogas
            yogas = await yoga_engine.analyze_yogas(planets, houses)
            
            # Calculate basic predictions
            predictions = {}
            if detailed:
                predictions = await prediction_engine.generate_predictions(
                    planets=planets,
                    houses=houses,
                    aspects=aspects,
                    yogas=yogas
                )
                
            # Calculate dashas
            dashas = await astro_calc.calculate_dashas(
                date=request.date,
                time=request.time,
                planets=planets
            )
            
            # Calculate ashtakavarga
            ashtakavarga = await astro_calc.calculate_ashtakavarga(planets)
            
            # Generate charts
            charts = await astro_calc.generate_charts(
                planets=planets,
                houses=houses
            )
            
            # Create response
            response = EnhancedKundliResponse(
                request_id=f"KUN_{datetime.utcnow().timestamp()}",
                input_data=request.dict(),
                planets=planets,
                houses=houses,
                aspects=aspects,
                yogas=yogas,
                dashas=dashas,
                ashtakavarga=ashtakavarga,
                charts=charts,
                predictions=predictions,
                metadata={
                    "calculation_time": (datetime.utcnow() - start_time).total_seconds(),
                    "ayanamsa_used": request.ayanamsa,
                    "house_system": request.house_system
                }
            )
            
            # Cache result
            await cache_manager.set(cache_key, response.dict(), expire=3600)
            
            # Track metrics
            await monitor.track_metric(
                "kundli_calculation_time",
                (datetime.utcnow() - start_time).total_seconds(),
                labels={
                    "user_id": current_user.username,
                    "detailed": str(detailed)
                }
            )
            
            return response
        
    except Exception as e:
        # Track error
        await monitor.track_metric(
            "kundli_calculation_errors",
            1,
            labels={
                "error_type": type(e).__name__,
                "user_id": current_user.username
            }
        )
        
        raise HTTPException(
            status_code=400,
            detail={
                "message": "Calculation failed",
                "error": str(e)
            }
        )

@router.get("/enhanced_kundli/{kundli_id}", response_model=EnhancedKundliResponse, responses={404: {"model": ErrorResponse}})
async def get_enhanced_kundli(
    kundli_id: str = Path(..., description="Kundli calculation ID"),
    current_user: TokenData = Depends(security_engine.get_current_user)
) -> EnhancedKundliResponse:
    """
    Retrieve previously calculated Kundli by ID
    """
    cache_key = f"kundli:{kundli_id}"
    cached_result = await cache_manager.get(cache_key)
    
    if not cached_result:
        raise HTTPException(
            status_code=404,
            detail={
                "message": "Kundli not found",
                "kundli_id": kundli_id
            }
        )
        
    return EnhancedKundliResponse(**cached_result)

@router.delete("/enhanced_kundli/{kundli_id}", status_code=204)
async def delete_enhanced_kundli(
    kundli_id: str = Path(..., description="Kundli calculation ID"),
    current_user: TokenData = Depends(security_engine.get_current_user)
):
    """
    Delete previously calculated Kundli by ID
    """
    cache_key = f"kundli:{kundli_id}"
    if not await cache_manager.exists(cache_key):
        raise HTTPException(
            status_code=404,
            detail={
                "message": "Kundli not found",
                "kundli_id": kundli_id
            }
        )
        
    await cache_manager.delete(cache_key)
