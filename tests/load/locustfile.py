"""
Load Testing Scenarios
PGF Protocol: TEST_004
Gate: GATE_5
Version: 1.0.0
"""

import json
import random
from datetime import datetime, timedelta
from typing import Dict, Any
from locust import HttpUser, task, between, events
from locust.runners import MasterRunner, WorkerRunner

class KundliUser(HttpUser):
    """Simulated user for load testing."""
    
    wait_time = between(1, 5)  # Wait 1-5 seconds between tasks
    
    def on_start(self):
        """Setup before starting tasks."""
        # Login
        self.token = self.login()
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }
    
    def login(self) -> str:
        """Login and get authentication token."""
        credentials = {
            "email": f"test_user_{random.randint(1, 1000)}@example.com",
            "password": "test_password"
        }
        
        with self.client.post(
            "/auth/login",
            json=credentials,
            catch_response=True
        ) as response:
            if response.status_code == 200:
                return response.json()["access_token"]
            response.failure("Login failed")
            return ""
    
    def generate_birth_details(self) -> Dict[str, Any]:
        """Generate random birth details."""
        # Random date in last 50 years
        date = datetime.now() - timedelta(
            days=random.randint(1, 18250)  # 50 years in days
        )
        
        return {
            "date": date.strftime("%Y-%m-%d"),
            "time": date.strftime("%H:%M:%S"),
            "latitude": random.uniform(-90, 90),
            "longitude": random.uniform(-180, 180),
            "timezone": "UTC"
        }
    
    @task(3)
    def calculate_kundli(self):
        """Test Kundli calculation endpoint."""
        birth_details = self.generate_birth_details()
        
        with self.client.post(
            "/kundli/calculate",
            json=birth_details,
            headers=self.headers,
            catch_response=True
        ) as response:
            if response.status_code == 201:
                kundli_id = response.json()["id"]
                # Store ID for later use
                self.kundli_ids = getattr(self, "kundli_ids", [])
                self.kundli_ids.append(kundli_id)
            else:
                response.failure(f"Failed to calculate Kundli: {response.text}")
    
    @task(2)
    def get_kundli(self):
        """Test retrieving Kundli details."""
        if hasattr(self, "kundli_ids") and self.kundli_ids:
            kundli_id = random.choice(self.kundli_ids)
            
            with self.client.get(
                f"/kundli/{kundli_id}",
                headers=self.headers,
                catch_response=True
            ) as response:
                if response.status_code != 200:
                    response.failure(f"Failed to get Kundli: {response.text}")
    
    @task(1)
    def batch_calculate(self):
        """Test batch calculation endpoint."""
        calculations = [
            self.generate_birth_details()
            for _ in range(random.randint(2, 5))
        ]
        
        with self.client.post(
            "/kundli/batch",
            json={"calculations": calculations},
            headers=self.headers,
            catch_response=True
        ) as response:
            if response.status_code != 201:
                response.failure(f"Batch calculation failed: {response.text}")
    
    @task(1)
    def validate_birth_details(self):
        """Test birth details validation endpoint."""
        birth_details = self.generate_birth_details()
        
        with self.client.post(
            "/kundli/validate",
            json=birth_details,
            headers=self.headers,
            catch_response=True
        ) as response:
            if response.status_code != 200:
                response.failure(f"Validation failed: {response.text}")

class ApiUser(HttpUser):
    """Simulated API user for load testing."""
    
    wait_time = between(0.1, 1)  # Faster requests for API users
    
    def on_start(self):
        """Setup before starting tasks."""
        self.api_key = "test_api_key"
        self.headers = {
            "X-API-Key": self.api_key,
            "Content-Type": "application/json"
        }
    
    @task
    def api_calculate(self):
        """Test API calculation endpoint."""
        birth_details = {
            "date": "2025-01-05",
            "time": "06:34:08",
            "latitude": 28.6139,
            "longitude": 77.2090,
            "timezone": "Asia/Kolkata"
        }
        
        with self.client.post(
            "/api/v1/calculate",
            json=birth_details,
            headers=self.headers,
            catch_response=True
        ) as response:
            if response.status_code != 200:
                response.failure(f"API calculation failed: {response.text}")

# Custom event handlers
@events.test_start.add_listener
def on_test_start(environment, **kwargs):
    """Handler for test start event."""
    if isinstance(environment.runner, MasterRunner):
        print("Starting load test...")
        environment.runner.send_message("test_starting", "")

@events.test_stop.add_listener
def on_test_stop(environment, **kwargs):
    """Handler for test stop event."""
    if isinstance(environment.runner, MasterRunner):
        print("Load test completed")
        environment.runner.send_message("test_stopping", "")

# Message handlers for distributed testing
@events.init.add_listener
def on_locust_init(environment, **kwargs):
    """Initialize message handlers for distributed testing."""
    if isinstance(environment.runner, WorkerRunner):
        @environment.runner.register_message("test_starting")
        def on_test_starting(msg, **kwargs):
            print(f"Worker {environment.runner.worker_index} starting")
        
        @environment.runner.register_message("test_stopping")
        def on_test_stopping(msg, **kwargs):
            print(f"Worker {environment.runner.worker_index} stopping")
