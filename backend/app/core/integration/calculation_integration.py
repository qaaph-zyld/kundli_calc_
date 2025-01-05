"""
Calculation Integration Layer
PGF Protocol: INT_001
Gate: GATE_3
Version: 1.0.0
"""

from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
import asyncio
import logging
from datetime import datetime
from app.core.calculations.house_analysis import EnhancedHouseAnalysisEngine
from app.core.recovery.error_recovery import RecoveryManager, with_error_recovery
from app.core.validation.house_analysis_validator import HouseAnalysisValidator

@dataclass
class IntegrationMetrics:
    """Metrics for integration layer performance"""
    request_count: int
    success_count: int
    error_count: int
    avg_response_time: float
    peak_memory_usage: float
    active_calculations: int

class CalculationIntegrationLayer:
    """Integration layer for astrological calculations"""
    
    def __init__(self):
        self.analysis_engine = EnhancedHouseAnalysisEngine()
        self.recovery_manager = RecoveryManager()
        self.validator = HouseAnalysisValidator()
        self.logger = logging.getLogger(__name__)
        self.metrics = IntegrationMetrics(0, 0, 0, 0.0, 0.0, 0)
        
    async def process_calculation_request(
        self,
        calculation_id: str,
        input_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Process a calculation request with full integration support"""
        start_time = datetime.now()
        self.metrics.request_count += 1
        self.metrics.active_calculations += 1
        
        try:
            # Start calculation with recovery support
            await self.recovery_manager.start_calculation(
                calculation_id,
                input_data
            )
            
            # Validate input data
            validation_result = await self.validator.validate_house_analysis(
                [input_data]
            )
            if validation_result.validation_status != "PASSED":
                raise ValueError(
                    f"Input validation failed: {validation_result.error_details}"
                )
            
            # Process calculation with error recovery
            result = await self._process_calculation(
                calculation_id,
                input_data
            )
            
            # Update metrics
            self.metrics.success_count += 1
            self._update_performance_metrics(start_time)
            
            return result
            
        except Exception as e:
            self.metrics.error_count += 1
            self.logger.error(f"Calculation failed: {str(e)}")
            raise
            
        finally:
            self.metrics.active_calculations -= 1
    
    @with_error_recovery(RecoveryManager())
    async def _process_calculation(
        self,
        calculation_id: str,
        input_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Process calculation with error recovery support"""
        try:
            # Extract calculation parameters
            house = input_data['house']
            occupants = input_data.get('occupants', [])
            aspects = input_data.get('aspects', [])
            lord = input_data.get('lord', {})
            time_of_day = input_data.get('time_of_day', 'day')
            
            # Update calculation state
            await self.recovery_manager.update_calculation_state(
                calculation_id,
                "processing",
                {"parameters_extracted": True},
                "parameter_extraction"
            )
            
            # Perform house analysis
            result = await self.analysis_engine.analyze_house(
                house=house,
                occupants=occupants,
                aspects=aspects,
                lord=lord,
                time_of_day=time_of_day
            )
            
            # Update calculation state
            await self.recovery_manager.update_calculation_state(
                calculation_id,
                "analyzing",
                {"analysis_complete": True},
                "house_analysis"
            )
            
            # Validate results
            validation_result = await self.validator.validate_house_analysis(
                [{**input_data, "expected_strength": result.total_strength}]
            )
            if validation_result.validation_status != "PASSED":
                raise ValueError(
                    f"Result validation failed: {validation_result.error_details}"
                )
            
            # Complete calculation
            await self.recovery_manager.complete_calculation(
                calculation_id,
                {"result": result.__dict__}
            )
            
            return {
                "calculation_id": calculation_id,
                "status": "completed",
                "result": result.__dict__,
                "validation": validation_result.__dict__
            }
            
        except Exception as e:
            # Handle error with recovery
            await self.recovery_manager.handle_error(calculation_id, e)
            raise
    
    def _update_performance_metrics(self, start_time: datetime) -> None:
        """Update performance metrics"""
        execution_time = (datetime.now() - start_time).total_seconds()
        
        # Update average response time
        total_time = (self.metrics.avg_response_time * 
                     (self.metrics.success_count - 1))
        self.metrics.avg_response_time = (
            (total_time + execution_time) / self.metrics.success_count
        )
        
        # Update peak memory usage
        import psutil
        current_memory = psutil.Process().memory_info().rss / 1024 / 1024
        self.metrics.peak_memory_usage = max(
            self.metrics.peak_memory_usage,
            current_memory
        )
    
    async def get_metrics(self) -> Dict[str, Any]:
        """Get current integration metrics"""
        return {
            "request_count": self.metrics.request_count,
            "success_rate": (
                self.metrics.success_count / self.metrics.request_count
                if self.metrics.request_count > 0 else 0
            ),
            "error_rate": (
                self.metrics.error_count / self.metrics.request_count
                if self.metrics.request_count > 0 else 0
            ),
            "avg_response_time": self.metrics.avg_response_time,
            "peak_memory_usage": self.metrics.peak_memory_usage,
            "active_calculations": self.metrics.active_calculations
        }
    
    async def reset_metrics(self) -> None:
        """Reset integration metrics"""
        self.metrics = IntegrationMetrics(0, 0, 0, 0.0, 0.0, 0)
