from fastapi.testclient import TestClient

def test_calculate_chart(client: TestClient):
    response = client.post(
        "/api/v1/charts/calculate",
        json={
            "date_time": "2024-01-01T12:00:00Z",
            "latitude": "13.0827",
            "longitude": "80.2707",
            "altitude": "0",
            "ayanamsa": "1",
            "house_system": "P"
        }
    )
    
    assert response.status_code == 200, f"Response: {response.json()}"
    data = response.json()
    assert "planetary_positions" in data
    assert "houses" in data
    assert "ayanamsa_value" in data

def test_invalid_coordinates(client: TestClient):
    response = client.post(
        "/api/v1/charts/calculate",
        json={
            "date_time": "2024-01-01T12:00:00Z",
            "latitude": "91",  # Invalid latitude
            "longitude": "80.2707",
            "altitude": "0",
            "ayanamsa": "1",
            "house_system": "P"
        }
    )
    
    assert response.status_code == 422  # Pydantic validation error
    error_detail = response.json()
    assert "detail" in error_detail
    assert any("latitude" in str(error).lower() for error in error_detail["detail"])
