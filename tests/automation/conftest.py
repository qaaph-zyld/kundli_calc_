"""
Test Automation Configuration
PGF Protocol: TEST_001
Gate: GATE_4
Version: 1.0.0
"""

import pytest
import asyncio
from typing import Generator, AsyncGenerator
from fastapi.testclient import TestClient
from httpx import AsyncClient
from motor.motor_asyncio import AsyncIOMotorClient
from redis.asyncio import Redis

from app.main import app
from app.core.config import settings
from app.core.database import get_database
from app.core.cache import get_redis

# Test database settings
TEST_MONGODB_URI = "mongodb://localhost:27017/test_kundli"
TEST_REDIS_URI = "redis://localhost:6379/1"

@pytest.fixture(scope="session")
def event_loop() -> Generator:
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="session")
async def test_client() -> AsyncGenerator[AsyncClient, None]:
    """Create a test client instance."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client

@pytest.fixture(scope="session")
async def mongodb_client() -> AsyncGenerator[AsyncIOMotorClient, None]:
    """Create a MongoDB test client."""
    client = AsyncIOMotorClient(TEST_MONGODB_URI)
    yield client
    await client.drop_database("test_kundli")
    client.close()

@pytest.fixture(scope="session")
async def redis_client() -> AsyncGenerator[Redis, None]:
    """Create a Redis test client."""
    client = Redis.from_url(TEST_REDIS_URI)
    yield client
    await client.flushdb()
    await client.close()

@pytest.fixture(autouse=True)
async def setup_test_db(mongodb_client: AsyncIOMotorClient):
    """Setup test database before each test."""
    db = mongodb_client.test_kundli
    
    # Create test data
    await db.users.insert_many([
        {
            "email": "test@example.com",
            "hashed_password": "test_hash",
            "is_active": True
        }
    ])
    
    yield
    
    # Cleanup after test
    await db.users.delete_many({})
    await db.kundlis.delete_many({})
    await db.calculations.delete_many({})

@pytest.fixture
def test_user():
    """Test user fixture."""
    return {
        "email": "test@example.com",
        "password": "test_password"
    }

@pytest.fixture
def test_kundli_data():
    """Test kundli calculation data."""
    return {
        "date": "2025-01-05",
        "time": "06:22:27",
        "latitude": 28.6139,
        "longitude": 77.2090,
        "timezone": "Asia/Kolkata"
    }

@pytest.fixture
def auth_headers(test_user):
    """Generate authentication headers."""
    return {
        "Authorization": f"Bearer test_token"
    }

# Custom markers
def pytest_configure(config):
    """Configure custom pytest markers."""
    markers = [
        "integration: mark test as an integration test",
        "e2e: mark test as an end-to-end test",
        "performance: mark test as a performance test",
        "security: mark test as a security test",
    ]
    for marker in markers:
        config.addinivalue_line("markers", marker)

# Test reporting
def pytest_terminal_summary(terminalreporter, exitstatus, config):
    """Add custom reporting to test summary."""
    print("\nTest Summary:")
    print(f"Total tests: {terminalreporter.stats.get('total', 0)}")
    print(f"Passed: {len(terminalreporter.stats.get('passed', []))}")
    print(f"Failed: {len(terminalreporter.stats.get('failed', []))}")
    print(f"Skipped: {len(terminalreporter.stats.get('skipped', []))}")
    print(f"Error: {len(terminalreporter.stats.get('error', []))}")

# Async test utilities
async def async_test(coroutine):
    """Run async test coroutine."""
    loop = asyncio.get_event_loop()
    return await loop.create_task(coroutine)

# Test data generators
def generate_test_data(data_type: str, **kwargs):
    """Generate test data based on type."""
    if data_type == "kundli":
        return {
            "date": kwargs.get("date", "2025-01-05"),
            "time": kwargs.get("time", "06:22:27"),
            "latitude": kwargs.get("latitude", 28.6139),
            "longitude": kwargs.get("longitude", 77.2090),
            "timezone": kwargs.get("timezone", "Asia/Kolkata")
        }
    elif data_type == "user":
        return {
            "email": kwargs.get("email", "test@example.com"),
            "password": kwargs.get("password", "test_password")
        }
    return {}

# Mock responses
class MockResponse:
    """Mock HTTP response."""
    def __init__(self, data, status_code=200):
        self.data = data
        self.status_code = status_code
    
    async def json(self):
        return self.data
    
    async def __aenter__(self):
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        pass
