"""API Integration tests for Kundli Calculation Service."""
import pytest
from httpx import AsyncClient
from fastapi import status
import json
import os
from datetime import datetime, timedelta

from app.main import app
from app.core.security import create_access_token
from app.models.user import UserRole

# Load test data
with open(os.path.join(os.path.dirname(__file__), '../../tests/data/test_data/birth_data.json')) as f:
    TEST_BIRTH_DATA = json.load(f)

@pytest.fixture
async def client():
    """Create test client."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client

@pytest.fixture
def auth_headers():
    """Create authentication headers."""
    access_token = create_access_token(
        data={"sub": "test@example.com", "role": UserRole.USER.value}
    )
    return {"Authorization": f"Bearer {access_token}"}

@pytest.mark.integration
class TestAuthAPI:
    """Test authentication endpoints."""

    async def test_login(self, client):
        """Test login endpoint."""
        response = await client.post("/auth/login", json={
            "email": "test@example.com",
            "password": "testpassword"
        })
        assert response.status_code == status.HTTP_200_OK
        assert "access_token" in response.json()
        assert "token_type" in response.json()

    async def test_refresh_token(self, client, auth_headers):
        """Test token refresh endpoint."""
        response = await client.post("/auth/refresh", headers=auth_headers)
        assert response.status_code == status.HTTP_200_OK
        assert "access_token" in response.json()

@pytest.mark.integration
class TestKundliAPI:
    """Test Kundli calculation endpoints."""

    async def test_create_kundli(self, client, auth_headers):
        """Test Kundli creation endpoint."""
        test_data = TEST_BIRTH_DATA[0]
        response = await client.post(
            "/kundli/create",
            headers=auth_headers,
            json=test_data
        )
        assert response.status_code == status.HTTP_201_CREATED
        assert "kundli_id" in response.json()

    async def test_get_kundli(self, client, auth_headers):
        """Test get Kundli endpoint."""
        # First create a Kundli
        test_data = TEST_BIRTH_DATA[0]
        create_response = await client.post(
            "/kundli/create",
            headers=auth_headers,
            json=test_data
        )
        kundli_id = create_response.json()["kundli_id"]

        # Then retrieve it
        response = await client.get(f"/kundli/{kundli_id}", headers=auth_headers)
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["birth_data"] == test_data

@pytest.mark.integration
class TestCalculationAPI:
    """Test calculation endpoints."""

    async def test_planetary_positions(self, client, auth_headers):
        """Test planetary positions calculation."""
        test_data = TEST_BIRTH_DATA[0]
        response = await client.post(
            "/calculate/planets",
            headers=auth_headers,
            json=test_data
        )
        assert response.status_code == status.HTTP_200_OK
        assert "planets" in response.json()
        assert len(response.json()["planets"]) > 0

    async def test_house_calculation(self, client, auth_headers):
        """Test house system calculation."""
        test_data = TEST_BIRTH_DATA[0]
        response = await client.post(
            "/calculate/houses",
            headers=auth_headers,
            json=test_data
        )
        assert response.status_code == status.HTTP_200_OK
        assert "houses" in response.json()
        assert len(response.json()["houses"]) == 12

@pytest.mark.integration
class TestUserAPI:
    """Test user management endpoints."""

    async def test_create_user(self, client, auth_headers):
        """Test user creation."""
        response = await client.post(
            "/users/",
            headers=auth_headers,
            json={
                "email": "newuser@example.com",
                "password": "newpassword",
                "full_name": "New User"
            }
        )
        assert response.status_code == status.HTTP_201_CREATED
        assert "id" in response.json()
        assert response.json()["email"] == "newuser@example.com"

    async def test_get_user_profile(self, client, auth_headers):
        """Test get user profile."""
        response = await client.get("/users/me", headers=auth_headers)
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["email"] == "test@example.com"

@pytest.mark.integration
class TestErrorHandling:
    """Test error handling scenarios."""

    async def test_invalid_birth_data(self, client, auth_headers):
        """Test error handling for invalid birth data."""
        response = await client.post(
            "/kundli/create",
            headers=auth_headers,
            json={"invalid": "data"}
        )
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    async def test_unauthorized_access(self, client):
        """Test unauthorized access handling."""
        response = await client.get("/users/me")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    async def test_not_found(self, client, auth_headers):
        """Test not found error handling."""
        response = await client.get("/kundli/nonexistent", headers=auth_headers)
        assert response.status_code == status.HTTP_404_NOT_FOUND
