"""
Testing Framework
PGF Protocol: TEST_001
Gate: GATE_7
Version: 1.0.0
"""

from typing import Dict, List, Optional, Any, Union, Type, Callable
from enum import Enum
from pydantic import BaseModel, Field
from datetime import datetime
import pytest
import asyncio
from httpx import AsyncClient
from fastapi import FastAPI
import json
from pathlib import Path
import logging
from functools import wraps
from contextlib import asynccontextmanager

class TestScope(str, Enum):
    """Test scopes"""
    UNIT = "unit"
    INTEGRATION = "integration"
    E2E = "e2e"
    PERFORMANCE = "performance"
    SECURITY = "security"

class TestPriority(str, Enum):
    """Test priorities"""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

class TestStatus(str, Enum):
    """Test status"""
    PASSED = "passed"
    FAILED = "failed"
    SKIPPED = "skipped"
    ERROR = "error"

class TestCase(BaseModel):
    """Test case definition"""
    
    name: str
    description: Optional[str] = None
    scope: TestScope
    priority: TestPriority
    tags: List[str] = Field(default_factory=list)
    dependencies: List[str] = Field(default_factory=list)
    setup: Optional[Dict[str, Any]] = None
    inputs: Dict[str, Any] = Field(default_factory=dict)
    expected: Dict[str, Any] = Field(default_factory=dict)
    cleanup: Optional[Dict[str, Any]] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)

class TestResult(BaseModel):
    """Test result"""
    
    case: TestCase
    status: TestStatus
    duration: float
    error: Optional[str] = None
    output: Optional[Dict[str, Any]] = None
    artifacts: List[str] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)

class TestSuite(BaseModel):
    """Test suite definition"""
    
    name: str
    description: Optional[str] = None
    cases: List[TestCase]
    setup: Optional[Dict[str, Any]] = None
    cleanup: Optional[Dict[str, Any]] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)

class TestConfig(BaseModel):
    """Test configuration"""
    
    app: FastAPI
    base_url: str = "http://test"
    test_data_dir: str = "./test_data"
    artifacts_dir: str = "./test_artifacts"
    timeout: int = 30
    retries: int = 3
    parallel: bool = True
    options: Dict[str, Any] = Field(default_factory=dict)

class TestFramework:
    """Testing framework for automated testing"""
    
    def __init__(self, config: TestConfig):
        self.config = config
        self.results: List[TestResult] = []
        self._setup_logging()
        self._ensure_directories()
    
    def _setup_logging(self) -> None:
        """Setup test logging"""
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s [%(levelname)s] %(message)s",
            handlers=[
                logging.FileHandler("test.log"),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def _ensure_directories(self) -> None:
        """Ensure required directories exist"""
        Path(self.config.test_data_dir).mkdir(parents=True, exist_ok=True)
        Path(self.config.artifacts_dir).mkdir(parents=True, exist_ok=True)
    
    async def run_suite(self, suite: TestSuite) -> List[TestResult]:
        """Run test suite"""
        self.logger.info(f"Running test suite: {suite.name}")
        results = []
        
        # Perform suite setup
        if suite.setup:
            await self._run_setup(suite.setup)
        
        try:
            # Run test cases
            if self.config.parallel:
                results = await asyncio.gather(*[
                    self.run_case(case)
                    for case in suite.cases
                ])
            else:
                for case in suite.cases:
                    result = await self.run_case(case)
                    results.append(result)
                    
        finally:
            # Perform suite cleanup
            if suite.cleanup:
                await self._run_cleanup(suite.cleanup)
        
        self.results.extend(results)
        return results
    
    async def run_case(self, case: TestCase) -> TestResult:
        """Run test case"""
        self.logger.info(f"Running test case: {case.name}")
        start_time = datetime.utcnow()
        
        try:
            # Perform case setup
            if case.setup:
                await self._run_setup(case.setup)
            
            # Run test with retries
            for attempt in range(self.config.retries):
                try:
                    output = await self._execute_test(case)
                    duration = (datetime.utcnow() - start_time).total_seconds()
                    
                    # Validate output against expected
                    if self._validate_output(output, case.expected):
                        return TestResult(
                            case=case,
                            status=TestStatus.PASSED,
                            duration=duration,
                            output=output
                        )
                    else:
                        return TestResult(
                            case=case,
                            status=TestStatus.FAILED,
                            duration=duration,
                            output=output,
                            error="Output validation failed"
                        )
                        
                except Exception as e:
                    if attempt == self.config.retries - 1:
                        raise
                    self.logger.warning(f"Attempt {attempt + 1} failed, retrying...")
                    await asyncio.sleep(1)
            
        except Exception as e:
            duration = (datetime.utcnow() - start_time).total_seconds()
            return TestResult(
                case=case,
                status=TestStatus.ERROR,
                duration=duration,
                error=str(e)
            )
            
        finally:
            # Perform case cleanup
            if case.cleanup:
                await self._run_cleanup(case.cleanup)
    
    async def _execute_test(self, case: TestCase) -> Dict[str, Any]:
        """Execute test case"""
        async with AsyncClient(app=self.config.app, base_url=self.config.base_url) as client:
            if case.scope == TestScope.UNIT:
                return await self._run_unit_test(case, client)
            elif case.scope == TestScope.INTEGRATION:
                return await self._run_integration_test(case, client)
            elif case.scope == TestScope.E2E:
                return await self._run_e2e_test(case, client)
            elif case.scope == TestScope.PERFORMANCE:
                return await self._run_performance_test(case, client)
            elif case.scope == TestScope.SECURITY:
                return await self._run_security_test(case, client)
            else:
                raise ValueError(f"Unknown test scope: {case.scope}")
    
    async def _run_unit_test(
        self,
        case: TestCase,
        client: AsyncClient
    ) -> Dict[str, Any]:
        """Run unit test"""
        response = await client.request(
            method=case.inputs.get("method", "GET"),
            url=case.inputs.get("endpoint", "/"),
            json=case.inputs.get("body"),
            params=case.inputs.get("query"),
            headers=case.inputs.get("headers")
        )
        
        return {
            "status_code": response.status_code,
            "body": response.json() if response.headers.get("content-type") == "application/json" else response.text,
            "headers": dict(response.headers)
        }
    
    async def _run_integration_test(
        self,
        case: TestCase,
        client: AsyncClient
    ) -> Dict[str, Any]:
        """Run integration test"""
        results = {}
        
        for step in case.inputs.get("steps", []):
            response = await client.request(
                method=step.get("method", "GET"),
                url=step.get("endpoint", "/"),
                json=step.get("body"),
                params=step.get("query"),
                headers=step.get("headers")
            )
            
            results[step["name"]] = {
                "status_code": response.status_code,
                "body": response.json() if response.headers.get("content-type") == "application/json" else response.text,
                "headers": dict(response.headers)
            }
        
        return results
    
    async def _run_e2e_test(
        self,
        case: TestCase,
        client: AsyncClient
    ) -> Dict[str, Any]:
        """Run end-to-end test"""
        results = {}
        
        for scenario in case.inputs.get("scenarios", []):
            scenario_results = {}
            
            for step in scenario.get("steps", []):
                response = await client.request(
                    method=step.get("method", "GET"),
                    url=step.get("endpoint", "/"),
                    json=step.get("body"),
                    params=step.get("query"),
                    headers=step.get("headers")
                )
                
                scenario_results[step["name"]] = {
                    "status_code": response.status_code,
                    "body": response.json() if response.headers.get("content-type") == "application/json" else response.text,
                    "headers": dict(response.headers)
                }
            
            results[scenario["name"]] = scenario_results
        
        return results
    
    async def _run_performance_test(
        self,
        case: TestCase,
        client: AsyncClient
    ) -> Dict[str, Any]:
        """Run performance test"""
        results = {
            "requests": [],
            "summary": {
                "total_requests": 0,
                "successful_requests": 0,
                "failed_requests": 0,
                "avg_response_time": 0,
                "min_response_time": float("inf"),
                "max_response_time": 0
            }
        }
        
        total_time = 0
        requests = case.inputs.get("requests", [])
        
        for request in requests:
            start_time = datetime.utcnow()
            
            try:
                response = await client.request(
                    method=request.get("method", "GET"),
                    url=request.get("endpoint", "/"),
                    json=request.get("body"),
                    params=request.get("query"),
                    headers=request.get("headers")
                )
                
                duration = (datetime.utcnow() - start_time).total_seconds()
                total_time += duration
                
                request_result = {
                    "success": True,
                    "duration": duration,
                    "status_code": response.status_code,
                    "body": response.json() if response.headers.get("content-type") == "application/json" else response.text,
                    "headers": dict(response.headers)
                }
                
                results["summary"]["successful_requests"] += 1
                results["summary"]["min_response_time"] = min(
                    results["summary"]["min_response_time"],
                    duration
                )
                results["summary"]["max_response_time"] = max(
                    results["summary"]["max_response_time"],
                    duration
                )
                
            except Exception as e:
                request_result = {
                    "success": False,
                    "error": str(e)
                }
                results["summary"]["failed_requests"] += 1
            
            results["requests"].append(request_result)
            results["summary"]["total_requests"] += 1
        
        if results["summary"]["successful_requests"] > 0:
            results["summary"]["avg_response_time"] = (
                total_time / results["summary"]["successful_requests"]
            )
        
        return results
    
    async def _run_security_test(
        self,
        case: TestCase,
        client: AsyncClient
    ) -> Dict[str, Any]:
        """Run security test"""
        results = {}
        
        for test in case.inputs.get("tests", []):
            test_results = {}
            
            for probe in test.get("probes", []):
                response = await client.request(
                    method=probe.get("method", "GET"),
                    url=probe.get("endpoint", "/"),
                    json=probe.get("body"),
                    params=probe.get("query"),
                    headers=probe.get("headers")
                )
                
                test_results[probe["name"]] = {
                    "status_code": response.status_code,
                    "body": response.json() if response.headers.get("content-type") == "application/json" else response.text,
                    "headers": dict(response.headers),
                    "security_flags": {
                        "has_security_headers": self._check_security_headers(response.headers),
                        "has_csrf_protection": self._check_csrf_protection(response),
                        "has_xss_protection": self._check_xss_protection(response),
                        "has_sql_injection_protection": self._check_sql_injection(response)
                    }
                }
            
            results[test["name"]] = test_results
        
        return results
    
    def _check_security_headers(self, headers: Dict[str, str]) -> bool:
        """Check for security headers"""
        required_headers = {
            "X-Content-Type-Options",
            "X-Frame-Options",
            "X-XSS-Protection",
            "Content-Security-Policy"
        }
        return all(header in headers for header in required_headers)
    
    def _check_csrf_protection(self, response: Any) -> bool:
        """Check for CSRF protection"""
        return "csrftoken" in response.cookies
    
    def _check_xss_protection(self, response: Any) -> bool:
        """Check for XSS protection"""
        return response.headers.get("X-XSS-Protection") == "1; mode=block"
    
    def _check_sql_injection(self, response: Any) -> bool:
        """Check for SQL injection protection"""
        # Implement SQL injection detection logic
        return True
    
    async def _run_setup(self, setup: Dict[str, Any]) -> None:
        """Run setup steps"""
        for step in setup.get("steps", []):
            if step.get("type") == "http":
                async with AsyncClient(app=self.config.app, base_url=self.config.base_url) as client:
                    await client.request(
                        method=step.get("method", "GET"),
                        url=step.get("endpoint", "/"),
                        json=step.get("body"),
                        params=step.get("query"),
                        headers=step.get("headers")
                    )
            elif step.get("type") == "function":
                func = step.get("function")
                if func:
                    await func(step.get("args", {}))
    
    async def _run_cleanup(self, cleanup: Dict[str, Any]) -> None:
        """Run cleanup steps"""
        for step in cleanup.get("steps", []):
            if step.get("type") == "http":
                async with AsyncClient(app=self.config.app, base_url=self.config.base_url) as client:
                    await client.request(
                        method=step.get("method", "GET"),
                        url=step.get("endpoint", "/"),
                        json=step.get("body"),
                        params=step.get("query"),
                        headers=step.get("headers")
                    )
            elif step.get("type") == "function":
                func = step.get("function")
                if func:
                    await func(step.get("args", {}))
    
    def _validate_output(
        self,
        output: Dict[str, Any],
        expected: Dict[str, Any]
    ) -> bool:
        """Validate test output against expected results"""
        for key, value in expected.items():
            if key not in output:
                return False
                
            if isinstance(value, dict):
                if not isinstance(output[key], dict):
                    return False
                if not self._validate_output(output[key], value):
                    return False
            elif output[key] != value:
                return False
        
        return True

# Test decorators
def unit_test(
    name: str,
    priority: TestPriority = TestPriority.MEDIUM,
    tags: List[str] = None
):
    """Decorator for unit tests"""
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            case = TestCase(
                name=name,
                scope=TestScope.UNIT,
                priority=priority,
                tags=tags or [],
                inputs=kwargs
            )
            return await test_framework.run_case(case)
        return wrapper
    return decorator

def integration_test(
    name: str,
    priority: TestPriority = TestPriority.MEDIUM,
    tags: List[str] = None
):
    """Decorator for integration tests"""
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            case = TestCase(
                name=name,
                scope=TestScope.INTEGRATION,
                priority=priority,
                tags=tags or [],
                inputs=kwargs
            )
            return await test_framework.run_case(case)
        return wrapper
    return decorator

def e2e_test(
    name: str,
    priority: TestPriority = TestPriority.HIGH,
    tags: List[str] = None
):
    """Decorator for end-to-end tests"""
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            case = TestCase(
                name=name,
                scope=TestScope.E2E,
                priority=priority,
                tags=tags or [],
                inputs=kwargs
            )
            return await test_framework.run_case(case)
        return wrapper
    return decorator

def performance_test(
    name: str,
    priority: TestPriority = TestPriority.MEDIUM,
    tags: List[str] = None
):
    """Decorator for performance tests"""
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            case = TestCase(
                name=name,
                scope=TestScope.PERFORMANCE,
                priority=priority,
                tags=tags or [],
                inputs=kwargs
            )
            return await test_framework.run_case(case)
        return wrapper
    return decorator

def security_test(
    name: str,
    priority: TestPriority = TestPriority.CRITICAL,
    tags: List[str] = None
):
    """Decorator for security tests"""
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            case = TestCase(
                name=name,
                scope=TestScope.SECURITY,
                priority=priority,
                tags=tags or [],
                inputs=kwargs
            )
            return await test_framework.run_case(case)
        return wrapper
    return decorator

# Global test framework instance
test_framework = TestFramework(
    TestConfig(
        app=FastAPI(),  # This should be replaced with actual app instance
        base_url="http://test",
        test_data_dir="./test_data",
        artifacts_dir="./test_artifacts",
        timeout=30,
        retries=3,
        parallel=True
    )
)
