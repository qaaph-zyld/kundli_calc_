"""
House Analysis Validation Framework
PGF Protocol: VCI_002
Gate: GATE_3
Version: 1.0.0
"""

from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
import asyncio
import numpy as np
from datetime import datetime
from app.core.calculations.house_analysis import EnhancedHouseAnalysisEngine, HouseStrength

@dataclass
class ValidationMetrics:
    accuracy: float
    precision: float
    recall: float
    execution_time: float
    resource_usage: Dict[str, float]
    validation_status: str
    error_details: Optional[List[str]] = None

@dataclass
class ValidationThresholds:
    min_accuracy: float = 95.0
    min_precision: float = 90.0
    min_recall: float = 90.0
    max_execution_time: float = 100.0  # milliseconds
    max_memory_usage: float = 50.0  # MB

class HouseAnalysisValidator:
    def __init__(self):
        self.engine = EnhancedHouseAnalysisEngine()
        self.thresholds = ValidationThresholds()
        self.validation_history: List[ValidationMetrics] = []
        
    async def validate_house_analysis(
        self,
        test_cases: List[Dict[str, Any]]
    ) -> ValidationMetrics:
        """
        Validate house analysis engine against test cases
        
        Args:
            test_cases: List of test cases with expected results
            
        Returns:
            ValidationMetrics with detailed validation results
        """
        start_time = datetime.now()
        
        # Initialize metrics
        total_cases = len(test_cases)
        correct_predictions = 0
        true_positives = 0
        false_positives = 0
        false_negatives = 0
        error_details = []
        
        try:
            # Process test cases
            for case in test_cases:
                result = await self._validate_single_case(case)
                
                if result.is_valid:
                    correct_predictions += 1
                    if result.prediction_type == 'positive':
                        true_positives += 1
                else:
                    if result.prediction_type == 'positive':
                        false_positives += 1
                    else:
                        false_negatives += 1
                        
                if result.error:
                    error_details.append(result.error)
                    
            # Calculate metrics
            accuracy = (correct_predictions / total_cases) * 100
            precision = (true_positives / (true_positives + false_positives)) * 100
            recall = (true_positives / (true_positives + false_negatives)) * 100
            
            # Calculate execution time
            execution_time = (datetime.now() - start_time).total_seconds() * 1000
            
            # Get resource usage
            resource_usage = self._get_resource_usage()
            
            # Determine validation status
            validation_status = self._determine_validation_status(
                accuracy,
                precision,
                recall,
                execution_time,
                resource_usage
            )
            
            metrics = ValidationMetrics(
                accuracy=accuracy,
                precision=precision,
                recall=recall,
                execution_time=execution_time,
                resource_usage=resource_usage,
                validation_status=validation_status,
                error_details=error_details if error_details else None
            )
            
            # Store metrics in history
            self.validation_history.append(metrics)
            
            return metrics
            
        except Exception as e:
            error_details.append(f"Validation failed: {str(e)}")
            return ValidationMetrics(
                accuracy=0.0,
                precision=0.0,
                recall=0.0,
                execution_time=-1,
                resource_usage={},
                validation_status="FAILED",
                error_details=error_details
            )
    
    async def _validate_single_case(
        self,
        test_case: Dict[str, Any]
    ) -> Tuple[bool, str, Optional[str]]:
        """Validate a single test case"""
        try:
            # Extract test case data
            house = test_case['house']
            occupants = test_case['occupants']
            aspects = test_case['aspects']
            lord = test_case['lord']
            expected_strength = test_case['expected_strength']
            
            # Get actual result
            result = await self.engine.analyze_house(
                house=house,
                occupants=occupants,
                aspects=aspects,
                lord=lord,
                time_of_day=test_case.get('time_of_day', 'day'),
                all_house_lords=test_case.get('all_house_lords')
            )
            
            # Validate result
            is_valid = self._validate_strength_result(
                result.total_strength,
                expected_strength,
                tolerance=test_case.get('tolerance', 5.0)
            )
            
            prediction_type = 'positive' if result.total_strength >= 50 else 'negative'
            
            return (is_valid, prediction_type, None)
            
        except Exception as e:
            return (False, 'negative', str(e))
    
    def _validate_strength_result(
        self,
        actual: float,
        expected: float,
        tolerance: float
    ) -> bool:
        """Validate if actual strength is within acceptable range"""
        return abs(actual - expected) <= tolerance
    
    def _get_resource_usage(self) -> Dict[str, float]:
        """Get current resource usage metrics"""
        import psutil
        import os
        
        process = psutil.Process(os.getpid())
        
        return {
            'memory_mb': process.memory_info().rss / 1024 / 1024,
            'cpu_percent': process.cpu_percent(),
            'thread_count': process.num_threads(),
            'open_files': len(process.open_files())
        }
    
    def _determine_validation_status(
        self,
        accuracy: float,
        precision: float,
        recall: float,
        execution_time: float,
        resource_usage: Dict[str, float]
    ) -> str:
        """Determine overall validation status"""
        if (accuracy >= self.thresholds.min_accuracy and
            precision >= self.thresholds.min_precision and
            recall >= self.thresholds.min_recall and
            execution_time <= self.thresholds.max_execution_time and
            resource_usage['memory_mb'] <= self.thresholds.max_memory_usage):
            return "PASSED"
            
        if (accuracy >= self.thresholds.min_accuracy * 0.9 and
            precision >= self.thresholds.min_precision * 0.9 and
            recall >= self.thresholds.min_recall * 0.9):
            return "WARNING"
            
        return "FAILED"
    
    def get_validation_history(
        self,
        limit: Optional[int] = None
    ) -> List[ValidationMetrics]:
        """Get validation history with optional limit"""
        if limit:
            return self.validation_history[-limit:]
        return self.validation_history
    
    def get_trend_analysis(self) -> Dict[str, Any]:
        """Analyze validation trends"""
        if not self.validation_history:
            return {}
            
        metrics = np.array([
            [m.accuracy, m.precision, m.recall, m.execution_time]
            for m in self.validation_history
        ])
        
        return {
            'accuracy_trend': {
                'mean': float(np.mean(metrics[:, 0])),
                'std': float(np.std(metrics[:, 0])),
                'trend': 'improving' if metrics[-1, 0] > np.mean(metrics[:-1, 0])
                        else 'declining'
            },
            'precision_trend': {
                'mean': float(np.mean(metrics[:, 1])),
                'std': float(np.std(metrics[:, 1])),
                'trend': 'improving' if metrics[-1, 1] > np.mean(metrics[:-1, 1])
                        else 'declining'
            },
            'recall_trend': {
                'mean': float(np.mean(metrics[:, 2])),
                'std': float(np.std(metrics[:, 2])),
                'trend': 'improving' if metrics[-1, 2] > np.mean(metrics[:-1, 2])
                        else 'declining'
            },
            'performance_trend': {
                'mean': float(np.mean(metrics[:, 3])),
                'std': float(np.std(metrics[:, 3])),
                'trend': 'improving' if metrics[-1, 3] < np.mean(metrics[:-1, 3])
                        else 'declining'
            }
        }
