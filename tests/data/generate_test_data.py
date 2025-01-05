"""Test data generation script for Kundli Calculation Service."""
import random
from datetime import datetime, timedelta
import json
import os
from typing import List, Dict, Any

class TestDataGenerator:
    """Generate test data for various test scenarios."""

    def __init__(self):
        """Initialize test data generator."""
        self.locations = [
            {"city": "Mumbai", "lat": 19.0760, "lon": 72.8777},
            {"city": "Delhi", "lat": 28.6139, "lon": 77.2090},
            {"city": "Bangalore", "lat": 12.9716, "lon": 77.5946},
            {"city": "Chennai", "lat": 13.0827, "lon": 80.2707},
            {"city": "Kolkata", "lat": 22.5726, "lon": 88.3639}
        ]

    def generate_birth_data(self, count: int = 100) -> List[Dict[str, Any]]:
        """Generate sample birth data for testing."""
        data = []
        start_date = datetime(1950, 1, 1)
        end_date = datetime(2020, 12, 31)
        
        for _ in range(count):
            birth_time = start_date + timedelta(
                seconds=random.randint(0, int((end_date - start_date).total_seconds()))
            )
            
            location = random.choice(self.locations)
            
            data.append({
                "name": f"Test Person {_}",
                "birth_date": birth_time.strftime("%Y-%m-%d"),
                "birth_time": birth_time.strftime("%H:%M:%S"),
                "latitude": location["lat"],
                "longitude": location["lon"],
                "city": location["city"],
                "timezone": "Asia/Kolkata"
            })
        
        return data

    def generate_user_data(self, count: int = 50) -> List[Dict[str, Any]]:
        """Generate sample user data for testing."""
        data = []
        roles = ["user", "premium", "admin"]
        
        for i in range(count):
            data.append({
                "username": f"test_user_{i}",
                "email": f"test{i}@example.com",
                "role": random.choice(roles),
                "is_active": random.choice([True, False]) if i > 10 else True,
                "created_at": (datetime.now() - timedelta(days=random.randint(1, 365))).isoformat()
            })
        
        return data

    def generate_calculation_data(self, count: int = 200) -> List[Dict[str, Any]]:
        """Generate sample calculation data for testing."""
        data = []
        calculation_types = ["basic", "detailed", "prediction"]
        
        birth_data = self.generate_birth_data(count // 2)
        
        for i in range(count):
            birth_info = random.choice(birth_data)
            data.append({
                "calculation_id": f"calc_{i}",
                "type": random.choice(calculation_types),
                "birth_info": birth_info,
                "timestamp": (datetime.now() - timedelta(days=random.randint(1, 30))).isoformat(),
                "status": random.choice(["completed", "failed", "in_progress"]),
                "duration_ms": random.randint(100, 5000)
            })
        
        return data

    def save_test_data(self, output_dir: str = "test_data"):
        """Save generated test data to files."""
        os.makedirs(output_dir, exist_ok=True)
        
        # Generate and save birth data
        birth_data = self.generate_birth_data()
        with open(os.path.join(output_dir, "birth_data.json"), "w") as f:
            json.dump(birth_data, f, indent=2)
        
        # Generate and save user data
        user_data = self.generate_user_data()
        with open(os.path.join(output_dir, "user_data.json"), "w") as f:
            json.dump(user_data, f, indent=2)
        
        # Generate and save calculation data
        calc_data = self.generate_calculation_data()
        with open(os.path.join(output_dir, "calculation_data.json"), "w") as f:
            json.dump(calc_data, f, indent=2)

def main():
    """Main function to generate test data."""
    generator = TestDataGenerator()
    generator.save_test_data()

if __name__ == "__main__":
    main()
