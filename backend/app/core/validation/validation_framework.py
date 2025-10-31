"""
Validation Framework
PGF Protocol: VAL_001
Gate: GATE_3
Version: 1.0.0
"""

from typing import Dict, Any, List, Optional
from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field, validator
import json
from app.core.cache import redis_cache

class ValidationLevel(str, Enum):
    """Validation levels"""
    STRICT = "STRICT"
    STANDARD = "STANDARD"
    RELAXED = "RELAXED"

class ValidationScope(str, Enum):
    """Validation scopes"""
    ALL = "ALL"
    INPUT = "INPUT"
    CALCULATION = "CALCULATION"
    OUTPUT = "OUTPUT"
    SYSTEM = "SYSTEM"

class ValidationError(BaseModel):
    """Validation error model"""
    code: str
    message: str
    field: Optional[str] = None
    details: Optional[Dict[str, Any]] = None
    severity: str = "ERROR"
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class ValidationResult(BaseModel):
    """Validation result model"""
    is_valid: bool
    errors: List[ValidationError] = []
    warnings: List[ValidationError] = []
    metadata: Dict[str, Any] = Field(default_factory=dict)

class ValidationRule(BaseModel):
    """Validation rule model"""
    code: str
    name: str
    description: str
    level: ValidationLevel
    scope: ValidationScope
    severity: str = "ERROR"
    enabled: bool = True
    parameters: Dict[str, Any] = Field(default_factory=dict)

class ValidationFramework:
    """Enhanced validation framework for Kundli calculations"""
    
    def __init__(self):
        self.rules: Dict[str, ValidationRule] = {}
        self._load_rules()
        
    def _load_rules(self):
        """Load validation rules"""
        # Basic input validation rules
        self.add_rule(ValidationRule(
            code="DATE_VALID",
            name="Date Validation",
            description="Validates date format and range",
            level=ValidationLevel.STRICT,
            scope=ValidationScope.INPUT,
            parameters={
                "min_year": 1900,
                "max_year": 2100
            }
        ))
        
        self.add_rule(ValidationRule(
            code="COORDINATES_VALID",
            name="Coordinates Validation",
            description="Validates latitude and longitude",
            level=ValidationLevel.STRICT,
            scope=ValidationScope.INPUT,
            parameters={
                "lat_range": (-90, 90),
                "lon_range": (-180, 180)
            }
        ))
        
        # Calculation validation rules
        self.add_rule(ValidationRule(
            code="PLANET_POSITIONS",
            name="Planet Positions Validation",
            description="Validates calculated planetary positions",
            level=ValidationLevel.STANDARD,
            scope=ValidationScope.CALCULATION,
            parameters={
                "position_range": (0, 360),
                "speed_range": (-5, 5)
            }
        ))
        
        self.add_rule(ValidationRule(
            code="HOUSE_SYSTEM",
            name="House System Validation",
            description="Validates house system calculations",
            level=ValidationLevel.STANDARD,
            scope=ValidationScope.CALCULATION,
            parameters={
                "valid_systems": ["Placidus", "Koch", "Equal", "Whole Sign"]
            }
        ))
        
        # Output validation rules
        self.add_rule(ValidationRule(
            code="ASPECT_VALID",
            name="Aspect Validation",
            description="Validates calculated aspects",
            level=ValidationLevel.STANDARD,
            scope=ValidationScope.OUTPUT,
            parameters={
                "max_orb": 10,
                "valid_aspects": [0, 60, 90, 120, 180]
            }
        ))
        
    def add_rule(self, rule: ValidationRule):
        """Add validation rule"""
        self.rules[rule.code] = rule
        
    def get_rule(self, code: str) -> Optional[ValidationRule]:
        """Get validation rule by code"""
        return self.rules.get(code)
        
    async def validate(
        self,
        data: Dict[str, Any],
        level: ValidationLevel = ValidationLevel.STANDARD,
        scope: ValidationScope = ValidationScope.ALL
    ) -> ValidationResult:
        """Validate data against rules"""
        result = ValidationResult(is_valid=True)
        start_time = datetime.utcnow()
        
        # Get cached validation result if available
        cache_key = f"validation:{hash(str(data))}"
        cached_result_str = redis_cache.get(cache_key)
        if cached_result_str:
            try:
                cached_obj = json.loads(cached_result_str)
                return ValidationResult(**cached_obj)
            except Exception:
                pass
            
        for rule in self.rules.values():
            if not rule.enabled:
                continue
                
            if rule.level.value > level.value:
                continue
                
            if scope != ValidationScope.ALL and rule.scope != scope:
                continue
                
            # Apply rule-specific validation
            error = await self._apply_rule(rule, data)
            if error:
                result.errors.append(error)
                if error.severity == "ERROR":
                    result.is_valid = False
                else:
                    result.warnings.append(error)
                    
        # Add metadata
        result.metadata.update({
            "validation_time": (datetime.utcnow() - start_time).total_seconds(),
            "rules_applied": len(self.rules),
            "level": level.value,
            "scope": scope.value
        })
        
        # Cache validation result
        try:
            redis_cache.set(cache_key, json.dumps(result.model_dump()), expire=300)
        except Exception:
            pass
        
        return result
        
    async def _apply_rule(self, rule: ValidationRule, data: Dict[str, Any]) -> Optional[ValidationError]:
        """Apply validation rule to data"""
        try:
            if rule.code == "DATE_VALID":
                return self._validate_date(data, rule)
            elif rule.code == "COORDINATES_VALID":
                return self._validate_coordinates(data, rule)
            elif rule.code == "PLANET_POSITIONS":
                return self._validate_planet_positions(data, rule)
            elif rule.code == "HOUSE_SYSTEM":
                return self._validate_house_system(data, rule)
            elif rule.code == "ASPECT_VALID":
                return self._validate_aspects(data, rule)
        except Exception as e:
            return ValidationError(
                code=rule.code,
                message=f"Validation error: {str(e)}",
                severity=rule.severity
            )
        return None
        
    def _validate_date(self, data: Dict[str, Any], rule: ValidationRule) -> Optional[ValidationError]:
        """Validate date"""
        try:
            date_str = data.get("date")
            if not date_str:
                return ValidationError(
                    code=rule.code,
                    message="Date is required",
                    field="date"
                )
                
            date = datetime.strptime(date_str, "%Y-%m-%d")
            min_year = rule.parameters["min_year"]
            max_year = rule.parameters["max_year"]
            
            if not min_year <= date.year <= max_year:
                return ValidationError(
                    code=rule.code,
                    message=f"Year must be between {min_year} and {max_year}",
                    field="date"
                )
        except ValueError:
            return ValidationError(
                code=rule.code,
                message="Invalid date format. Use YYYY-MM-DD",
                field="date"
            )
        return None
        
    def _validate_coordinates(self, data: Dict[str, Any], rule: ValidationRule) -> Optional[ValidationError]:
        """Validate coordinates"""
        lat = data.get("latitude")
        lon = data.get("longitude")
        
        if lat is None or lon is None:
            return ValidationError(
                code=rule.code,
                message="Latitude and longitude are required",
                field="coordinates"
            )
            
        lat_min, lat_max = rule.parameters["lat_range"]
        lon_min, lon_max = rule.parameters["lon_range"]
        
        if not lat_min <= lat <= lat_max:
            return ValidationError(
                code=rule.code,
                message=f"Latitude must be between {lat_min} and {lat_max}",
                field="latitude"
            )
            
        if not lon_min <= lon <= lon_max:
            return ValidationError(
                code=rule.code,
                message=f"Longitude must be between {lon_min} and {lon_max}",
                field="longitude"
            )
            
        return None
        
    def _validate_planet_positions(self, data: Dict[str, Any], rule: ValidationRule) -> Optional[ValidationError]:
        """Validate planet positions"""
        planets = data.get("planets", {})
        if not planets:
            return ValidationError(
                code=rule.code,
                message="No planetary positions found",
                field="planets"
            )
            
        pos_min, pos_max = rule.parameters["position_range"]
        speed_min, speed_max = rule.parameters["speed_range"]
        
        for planet, details in planets.items():
            position = details.get("longitude")
            speed = details.get("speed")
            
            if position is None or not pos_min <= position <= pos_max:
                return ValidationError(
                    code=rule.code,
                    message=f"Invalid position for {planet}",
                    field=f"planets.{planet}.longitude"
                )
                
            if speed is not None and not speed_min <= speed <= speed_max:
                return ValidationError(
                    code=rule.code,
                    message=f"Invalid speed for {planet}",
                    field=f"planets.{planet}.speed"
                )
                
        return None
        
    def _validate_house_system(self, data: Dict[str, Any], rule: ValidationRule) -> Optional[ValidationError]:
        """Validate house system"""
        house_system = data.get("house_system")
        if not house_system:
            return ValidationError(
                code=rule.code,
                message="House system is required",
                field="house_system"
            )
            
        valid_systems = rule.parameters["valid_systems"]
        if house_system not in valid_systems:
            return ValidationError(
                code=rule.code,
                message=f"Invalid house system. Must be one of: {', '.join(valid_systems)}",
                field="house_system"
            )
            
        return None
        
    def _validate_aspects(self, data: Dict[str, Any], rule: ValidationRule) -> Optional[ValidationError]:
        """Validate aspects"""
        aspects = data.get("aspects", [])
        if not aspects:
            return None
            
        max_orb = rule.parameters["max_orb"]
        valid_aspects = rule.parameters["valid_aspects"]
        
        for aspect in aspects:
            angle = aspect.get("angle")
            orb = aspect.get("orb")
            
            if angle is None or angle not in valid_aspects:
                return ValidationError(
                    code=rule.code,
                    message=f"Invalid aspect angle. Must be one of: {', '.join(map(str, valid_aspects))}",
                    field="aspects.angle"
                )
                
            if orb is None or orb > max_orb:
                return ValidationError(
                    code=rule.code,
                    message=f"Invalid orb. Must be less than {max_orb} degrees",
                    field="aspects.orb"
                )
                
        return None


# Global validation framework instance
validation_framework = ValidationFramework()
