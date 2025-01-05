"""
Test Automation Runner
PGF Protocol: TEST_002
Gate: GATE_4
Version: 1.0.0
"""

import os
import sys
import argparse
import pytest
import json
import logging
from datetime import datetime
from typing import List, Dict, Any
import asyncio
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class TestRunner:
    """Automated test runner for Kundli Calculation Service."""
    
    def __init__(self):
        self.test_dir = Path(__file__).parent.parent
        self.results_dir = self.test_dir / "results"
        self.results_dir.mkdir(exist_ok=True)
    
    def setup_test_environment(self):
        """Setup test environment variables and configurations."""
        os.environ["TESTING"] = "1"
        os.environ["MONGODB_URI"] = "mongodb://localhost:27017/test_kundli"
        os.environ["REDIS_URI"] = "redis://localhost:6379/1"
    
    def get_test_suites(self) -> List[str]:
        """Get all available test suites."""
        suites = []
        for path in (self.test_dir / "test_suites").glob("test_*.py"):
            suite_name = path.stem
            if suite_name.startswith("test_"):
                suites.append(suite_name)
        return suites
    
    def run_tests(
        self,
        suite: str = None,
        markers: List[str] = None,
        parallel: bool = False
    ) -> Dict[str, Any]:
        """Run specified tests and return results."""
        
        # Build pytest arguments
        pytest_args = [
            str(self.test_dir),
            "-v",
            "--tb=short",
            "--asyncio-mode=auto"
        ]
        
        # Add suite filter
        if suite:
            pytest_args.extend(["-k", suite])
        
        # Add markers
        if markers:
            for marker in markers:
                pytest_args.extend(["-m", marker])
        
        # Add parallel execution
        if parallel:
            pytest_args.extend(["-n", "auto"])
        
        # Add JUnit XML report
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_path = self.results_dir / f"report_{timestamp}.xml"
        pytest_args.extend(["--junitxml", str(report_path)])
        
        # Run tests
        try:
            result = pytest.main(pytest_args)
            return {
                "exit_code": result,
                "report_path": str(report_path),
                "timestamp": timestamp
            }
        except Exception as e:
            logger.error(f"Error running tests: {str(e)}")
            return {
                "exit_code": 1,
                "error": str(e),
                "timestamp": timestamp
            }
    
    def generate_report(self, results: Dict[str, Any]) -> str:
        """Generate detailed test report."""
        report = {
            "timestamp": results["timestamp"],
            "status": "success" if results["exit_code"] == 0 else "failure",
            "details": {}
        }
        
        if "report_path" in results:
            try:
                # Parse JUnit XML report
                import xml.etree.ElementTree as ET
                tree = ET.parse(results["report_path"])
                root = tree.getroot()
                
                # Extract test statistics
                report["details"] = {
                    "total": int(root.attrib.get("tests", 0)),
                    "passed": int(root.attrib.get("tests", 0)) - 
                             int(root.attrib.get("failures", 0)) - 
                             int(root.attrib.get("errors", 0)),
                    "failed": int(root.attrib.get("failures", 0)),
                    "errors": int(root.attrib.get("errors", 0)),
                    "skipped": int(root.attrib.get("skipped", 0)),
                    "duration": float(root.attrib.get("time", 0))
                }
            except Exception as e:
                logger.error(f"Error parsing test report: {str(e)}")
                report["details"] = {"error": str(e)}
        
        # Save report
        report_path = self.results_dir / f"summary_{results['timestamp']}.json"
        with open(report_path, "w") as f:
            json.dump(report, f, indent=2)
        
        return str(report_path)

def main():
    """Main entry point for test runner."""
    parser = argparse.ArgumentParser(description="Kundli Service Test Runner")
    parser.add_argument(
        "--suite",
        help="Specific test suite to run"
    )
    parser.add_argument(
        "--markers",
        nargs="+",
        help="Test markers to filter by"
    )
    parser.add_argument(
        "--parallel",
        action="store_true",
        help="Run tests in parallel"
    )
    args = parser.parse_args()
    
    # Initialize runner
    runner = TestRunner()
    
    # Setup environment
    runner.setup_test_environment()
    
    # Run tests
    logger.info("Starting test execution...")
    results = runner.run_tests(
        suite=args.suite,
        markers=args.markers,
        parallel=args.parallel
    )
    
    # Generate report
    report_path = runner.generate_report(results)
    logger.info(f"Test execution completed. Report saved to: {report_path}")
    
    # Exit with test result
    sys.exit(results["exit_code"])

if __name__ == "__main__":
    main()
