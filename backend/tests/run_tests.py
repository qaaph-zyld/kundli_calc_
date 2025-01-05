#!/usr/bin/env python3
"""
Test Runner for Vedic Astrology System
Executes test suites and generates performance reports
"""

import pytest
import psutil
import time
import json
import platform
import asyncio
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List

from app.core.testing.framework import (
    TestFramework,
    TestConfig,
    TestCase,
    TestScope,
    TestPriority,
    TestStatus,
    TestSuite
)
from app.main import app

class TestRunner:
    """Test execution and performance monitoring framework"""
    
    def __init__(self):
        self.results = {
            'timestamp': datetime.now().isoformat(),
            'system_info': self._get_system_info(),
            'test_results': {},
            'performance_metrics': {}
        }
        
        self.test_framework = TestFramework(
            TestConfig(
                app=app,
                base_url="http://test",
                test_data_dir="./test_data",
                artifacts_dir="./test_artifacts",
                timeout=30,
                retries=3,
                parallel=True,
                options={
                    "mock_external_services": True,
                    "use_test_database": True
                }
            )
        )
    
    def _get_system_info(self) -> Dict[str, Any]:
        """Gather system information"""
        return {
            'cpu_count': psutil.cpu_count(),
            'memory_total': psutil.virtual_memory().total / (1024 * 1024 * 1024),  # GB
            'python_version': platform.python_version(),
            'platform': platform.platform()
        }
    
    async def run_framework_tests(self) -> Dict[str, Any]:
        """Run tests using testing framework"""
        framework_results = []
        
        # Import test suites
        from tests.api.test_kundli import test_suite as kundli_suite
        
        # Run test suites
        suites = [kundli_suite]
        for suite in suites:
            suite_results = await self.test_framework.run_suite(suite)
            framework_results.extend(suite_results)
        
        # Process results
        test_stats = {
            'total': len(framework_results),
            'passed': len([r for r in framework_results if r.status == TestStatus.PASSED]),
            'failed': len([r for r in framework_results if r.status == TestStatus.FAILED]),
            'skipped': len([r for r in framework_results if r.status == TestStatus.SKIPPED]),
            'error': len([r for r in framework_results if r.status == TestStatus.ERROR])
        }
        
        # Calculate success rate
        success_rate = (test_stats['passed'] / test_stats['total']) * 100 if test_stats['total'] > 0 else 0
        
        return {
            'framework_stats': test_stats,
            'success_rate': success_rate,
            'results': [
                {
                    'name': result.case.name,
                    'scope': result.case.scope,
                    'priority': result.case.priority,
                    'status': result.status,
                    'duration': result.duration,
                    'error': result.error if result.error else None
                }
                for result in framework_results
            ]
        }
    
    def run_tests(self) -> Dict[str, Any]:
        """Execute test suite with performance monitoring"""
        test_start = time.time()
        initial_memory = psutil.Process().memory_info().rss
        
        # Run pytest with detailed output
        pytest_args = [
            '-v',
            '--durations=10',
            '--maxfail=5',
            'tests'
        ]
        
        test_result = pytest.main(pytest_args)
        
        # Run framework tests
        framework_results = asyncio.run(self.run_framework_tests())
        
        # Calculate metrics
        test_duration = time.time() - test_start
        final_memory = psutil.Process().memory_info().rss
        memory_used = (final_memory - initial_memory) / (1024 * 1024)  # MB
        
        self.results['performance_metrics'] = {
            'test_duration_seconds': round(test_duration, 2),
            'memory_usage_mb': round(memory_used, 2),
            'peak_memory_mb': round(psutil.Process().memory_info().peak_wset / (1024 * 1024), 2)
        }
        
        self.results['test_results'] = {
            'pytest': {
                'exit_code': test_result,
                'status': 'Success' if test_result == 0 else 'Failed'
            },
            'framework': framework_results
        }
        
        return self.results
    
    def generate_report(self) -> Path:
        """Generate detailed test report"""
        report_path = Path('test_reports')
        report_path.mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        report_file = report_path / f'test_report_{timestamp}.json'
        
        with open(report_file, 'w') as f:
            json.dump(self.results, f, indent=4)
        
        return report_file

if __name__ == '__main__':
    runner = TestRunner()
    results = runner.run_tests()
    report_file = runner.generate_report()
    
    print("\nTest Execution Summary:")
    print("\nPytest Results:")
    print(f"Status: {results['test_results']['pytest']['status']}")
    
    print("\nFramework Results:")
    framework_stats = results['test_results']['framework']['framework_stats']
    print(f"Total Tests: {framework_stats['total']}")
    print(f"Passed: {framework_stats['passed']}")
    print(f"Failed: {framework_stats['failed']}")
    print(f"Skipped: {framework_stats['skipped']}")
    print(f"Errors: {framework_stats['error']}")
    print(f"Success Rate: {results['test_results']['framework']['success_rate']:.2f}%")
    
    print("\nPerformance Metrics:")
    print(f"Duration: {results['performance_metrics']['test_duration_seconds']}s")
    print(f"Memory Usage: {results['performance_metrics']['memory_usage_mb']}MB")
    print(f"Report saved to: {report_file}")
