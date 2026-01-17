# Load Testing Guide
**Date:** 2026-01-16  
**Tool:** Locust  
**Target:** Backend API (FastAPI)  
**Status:** Framework ready, execution pending

---

## Overview

**Purpose:** Validate system performance under realistic concurrent load to identify bottlenecks and establish capacity limits.

**Tool Choice: Locust**
- Python-based (matches backend stack)
- Realistic user behavior simulation
- Web UI for monitoring
- Distributed testing capable
- Easy scenario definition

**Existing Setup:**
- `tests/load/locustfile.py` - Already present
- Basic load test scenarios implemented

---

## Load Testing Framework

### Installation

```bash
cd backend
pip install locust
```

**Dependencies:**
- locust >= 2.14.0
- Python 3.9+

### Configuration

**Environment Variables:**
```bash
export API_BASE_URL=http://localhost:8000
export TEST_USERS=100
export SPAWN_RATE=10
export RUN_TIME=5m
```

---

## Test Scenarios

### Scenario 1: Chart Calculation (Primary Flow)

**User Journey:**
1. Calculate birth chart
2. Retrieve planetary positions
3. Get Vimshottari dasha
4. Fetch yoga analysis

**Load Pattern:**
- Concurrent users: 10, 50, 100, 200
- Duration: 5 minutes per test
- Spawn rate: 10 users/second

**Expected Performance:**
- Chart calculation: P95 < 500ms
- API response: P95 < 500ms
- Error rate: < 1%

### Scenario 2: Mixed Operations

**User Mix:**
- 50% chart calculations
- 20% divisional chart requests
- 15% yoga analysis
- 10% dasha calculations
- 5% transit analysis

**Load Pattern:**
- Concurrent users: 50-100
- Duration: 10 minutes
- Realistic think time: 2-5 seconds

### Scenario 3: Spike Test

**Pattern:**
- Baseline: 20 users
- Spike to: 200 users
- Duration: 30 seconds spike
- Return to baseline

**Purpose:** Test system recovery and autoscaling

### Scenario 4: Soak Test

**Pattern:**
- Constant load: 50 users
- Duration: 30 minutes
- Purpose: Memory leaks, resource exhaustion

---

## Enhanced Locust Configuration

### Updated locustfile.py Structure

```python
from locust import HttpUser, task, between, constant
from datetime import datetime, timedelta
import random

class KundliUser(HttpUser):
    """Simulates typical Kundli calculation user"""
    
    wait_time = between(2, 5)  # Realistic think time
    
    def on_start(self):
        """Initialize user session"""
        self.birth_data = self._generate_birth_data()
    
    @task(5)  # Weight: 50%
    def calculate_chart(self):
        """Primary user flow: Calculate birth chart"""
        payload = {
            "date_time": self.birth_data["datetime"],
            "latitude": self.birth_data["latitude"],
            "longitude": self.birth_data["longitude"],
            "ayanamsa": 1,  # Lahiri
            "house_system": "W"  # Whole Sign
        }
        
        with self.client.post(
            "/api/v1/charts/calculate",
            json=payload,
            catch_response=True,
            name="/charts/calculate"
        ) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Status {response.status_code}")
    
    @task(2)  # Weight: 20%
    def get_divisional_chart(self):
        """Request D9 (Navamsa) chart"""
        # Reuse birth data
        self.client.get(
            f"/api/v1/divisional/D9",
            params=self.birth_data,
            name="/divisional/D9"
        )
    
    @task(1.5)  # Weight: 15%
    def analyze_yogas(self):
        """Yoga analysis request"""
        self.client.post(
            "/api/v1/yogas/calculate",
            json=self.birth_data,
            name="/yogas/calculate"
        )
    
    @task(1)  # Weight: 10%
    def calculate_dasha(self):
        """Vimshottari dasha calculation"""
        self.client.post(
            "/api/v1/dasha/vimshottari",
            json=self.birth_data,
            name="/dasha/vimshottari"
        )
    
    @task(0.5)  # Weight: 5%
    def get_transits(self):
        """Current transit analysis"""
        self.client.get(
            "/api/v1/transits/current",
            name="/transits/current"
        )
    
    def _generate_birth_data(self):
        """Generate realistic birth data"""
        # Random date between 1950-2020
        year = random.randint(1950, 2020)
        month = random.randint(1, 12)
        day = random.randint(1, 28)
        hour = random.randint(0, 23)
        minute = random.randint(0, 59)
        
        # Random Indian city coordinates
        cities = [
            {"name": "Delhi", "lat": 28.6139, "lon": 77.209},
            {"name": "Mumbai", "lat": 19.076, "lon": 72.8777},
            {"name": "Bangalore", "lat": 12.9716, "lon": 77.5946},
            {"name": "Kolkata", "lat": 22.5726, "lon": 88.3639},
            {"name": "Chennai", "lat": 13.0827, "lon": 80.2707},
        ]
        city = random.choice(cities)
        
        return {
            "datetime": f"{year:04d}-{month:02d}-{day:02d}T{hour:02d}:{minute:02d}:00Z",
            "latitude": city["lat"],
            "longitude": city["lon"],
            "timezone": "Asia/Kolkata",
            "city": city["name"]
        }


class PowerUser(HttpUser):
    """Simulates advanced user with heavier usage"""
    
    wait_time = between(1, 3)  # Faster think time
    
    @task
    def advanced_analysis(self):
        """Complex multi-step analysis"""
        # Generate birth data
        birth_data = self._generate_birth_data()
        
        # Step 1: Chart
        self.client.post("/api/v1/charts/calculate", json=birth_data)
        
        # Step 2: Multiple divisional charts
        for d_chart in ["D1", "D9", "D10", "D12"]:
            self.client.get(f"/api/v1/divisional/{d_chart}", params=birth_data)
        
        # Step 3: Comprehensive analysis
        self.client.post("/api/v1/yogas/calculate", json=birth_data)
        self.client.post("/api/v1/dasha/vimshottari", json=birth_data)
        self.client.get("/api/v1/transits/current")
    
    def _generate_birth_data(self):
        # Same as KundliUser
        pass


class SpikeUser(HttpUser):
    """User for spike testing"""
    
    wait_time = constant(0)  # No wait time for spike
    
    @task
    def quick_calculation(self):
        """Fast successive calculations"""
        payload = {
            "date_time": "1990-10-09T08:10:00Z",
            "latitude": 44.5333,
            "longitude": 19.2333,
            "ayanamsa": 1,
            "house_system": "W"
        }
        self.client.post("/api/v1/charts/calculate", json=payload)
```

---

## Running Load Tests

### Basic Test (10 users, 1 minute)

```bash
locust -f tests/load/locustfile.py --host=http://localhost:8000 --users 10 --spawn-rate 2 --run-time 1m --headless
```

### Realistic Load (100 users, 5 minutes)

```bash
locust -f tests/load/locustfile.py --host=http://localhost:8000 --users 100 --spawn-rate 10 --run-time 5m --headless --html=load_test_report.html
```

### Spike Test

```bash
locust -f tests/load/locustfile.py --host=http://localhost:8000 --users 200 --spawn-rate 50 --run-time 2m --headless
```

### Web UI Mode (Interactive)

```bash
locust -f tests/load/locustfile.py --host=http://localhost:8000
# Open browser: http://localhost:8089
```

---

## Performance Targets

### Response Time Targets

| Endpoint | P50 | P95 | P99 | Max |
|----------|-----|-----|-----|-----|
| /charts/calculate | < 200ms | < 500ms | < 1s | < 2s |
| /yogas/calculate | < 300ms | < 600ms | < 1.2s | < 2s |
| /dasha/vimshottari | < 150ms | < 400ms | < 800ms | < 1.5s |
| /divisional/* | < 200ms | < 500ms | < 1s | < 2s |
| /transits/current | < 100ms | < 300ms | < 600ms | < 1s |

### Throughput Targets

- **Requests per second:** 100+ RPS
- **Concurrent users:** 100+ sustained
- **Peak capacity:** 200+ users
- **Error rate:** < 1%

### Resource Limits

- **CPU:** < 80% average
- **Memory:** < 2GB per worker
- **Database connections:** < 50% pool
- **Redis connections:** < 100 active

---

## Monitoring During Tests

### Metrics to Track

**Application Metrics:**
- Request latency (P50, P95, P99)
- Throughput (RPS)
- Error rate
- Active connections

**System Metrics:**
- CPU utilization
- Memory usage
- Disk I/O
- Network I/O

**Database Metrics:**
- Query time
- Connection pool usage
- Cache hit rate (Redis)
- Slow query log

### Tools

1. **Locust Dashboard:** http://localhost:8089 (real-time)
2. **Prometheus:** http://localhost:9090 (metrics)
3. **Grafana:** http://localhost:3000 (visualization)
4. **FastAPI metrics:** /api/v1/metrics

---

## Test Execution Plan

### Week 2: Initial Load Tests

**Day 1: Baseline**
- 10 users, 5 minutes
- Establish baseline metrics
- Identify obvious bottlenecks

**Day 2: Moderate Load**
- 50 users, 10 minutes
- Monitor resource usage
- Check cache effectiveness

**Day 3: Target Load**
- 100 users, 15 minutes
- Validate targets are met
- Document any issues

**Day 4: Peak Load**
- 200 users, 5 minutes
- Find breaking point
- Test recovery

**Day 5: Soak Test**
- 50 users, 30 minutes
- Check for memory leaks
- Verify stability

### Week 3: Optimization & Re-test

**After identifying bottlenecks:**
- Implement optimizations
- Re-run failed scenarios
- Compare before/after metrics
- Document improvements

---

## Common Bottlenecks & Solutions

### Bottleneck 1: Database Queries

**Symptoms:**
- Slow response times under load
- Database CPU high
- Query queue building up

**Solutions:**
- Add database indexes
- Optimize N+1 queries
- Implement query caching
- Connection pool tuning

### Bottleneck 2: Swiss Ephemeris Calculations

**Symptoms:**
- High CPU during chart calculations
- Calculation endpoints slow

**Solutions:**
- Cache planetary positions (date/location key)
- Pre-calculate common charts
- Consider calculation worker pool
- Async processing for heavy calculations

### Bottleneck 3: Redis Cache

**Symptoms:**
- Cache misses under load
- Memory exhaustion
- Eviction rate high

**Solutions:**
- Increase cache memory
- Optimize TTL values
- Implement cache warming
- Use compression for large values

### Bottleneck 4: API Rate Limiting

**Symptoms:**
- 429 Too Many Requests errors
- Legitimate users blocked

**Solutions:**
- Adjust rate limit thresholds
- Implement tiered limits
- Add burst allowance
- Better user identification

---

## Load Test Report Template

### Test Configuration
- Date: [Date]
- Duration: [Duration]
- Users: [Concurrent users]
- Spawn rate: [Users/second]
- Test type: [Baseline/Stress/Spike/Soak]

### Results Summary
- Total requests: [Number]
- RPS: [Average]
- Error rate: [Percentage]
- P50 latency: [ms]
- P95 latency: [ms]
- P99 latency: [ms]

### Endpoint Performance
| Endpoint | Requests | Failures | P50 | P95 | RPS |
|----------|----------|----------|-----|-----|-----|
| /charts/calculate | X | Y | Zms | Zms | Z |

### Resource Usage
- CPU: [Average/Peak]
- Memory: [Average/Peak]
- Database: [Connections/Query time]
- Cache: [Hit rate]

### Bottlenecks Identified
1. [Description]
2. [Description]

### Recommendations
1. [Action]
2. [Action]

---

## Integration with CI/CD

### Automated Load Testing

**GitHub Actions Workflow:**

```yaml
name: Load Testing

on:
  schedule:
    - cron: '0 2 * * 0'  # Weekly, Sunday 2 AM
  workflow_dispatch:

jobs:
  load-test:
    runs-on: ubuntu-latest
    services:
      backend:
        image: kundli-backend:latest
        ports:
          - 8000:8000
    
    steps:
      - uses: actions/checkout@v2
      
      - name: Setup Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      
      - name: Install Locust
        run: pip install locust
      
      - name: Run Load Test
        run: |
          locust -f tests/load/locustfile.py \
            --host=http://localhost:8000 \
            --users 50 \
            --spawn-rate 5 \
            --run-time 5m \
            --headless \
            --html=load_test_report.html \
            --exit-code-on-error 1
      
      - name: Upload Report
        uses: actions/upload-artifact@v2
        with:
          name: load-test-report
          path: load_test_report.html
      
      - name: Check Performance Targets
        run: |
          python tests/load/check_performance.py load_test_report.html
```

---

## Performance Regression Detection

### Baseline Comparison Script

```python
# tests/load/check_performance.py

import json
import sys

def check_performance(report_file, baseline_file):
    """Compare load test results against baseline"""
    
    with open(report_file) as f:
        current = json.load(f)
    
    with open(baseline_file) as f:
        baseline = json.load(f)
    
    # Check P95 latency
    current_p95 = current["stats"]["p95"]
    baseline_p95 = baseline["stats"]["p95"]
    
    if current_p95 > baseline_p95 * 1.2:  # 20% threshold
        print(f"⚠️  Performance regression detected:")
        print(f"   Current P95: {current_p95}ms")
        print(f"   Baseline P95: {baseline_p95}ms")
        print(f"   Degradation: {((current_p95/baseline_p95 - 1) * 100):.1f}%")
        sys.exit(1)
    
    print("✅ Performance targets met")
    sys.exit(0)
```

---

## Next Steps

### Immediate (This Session)
1. ✅ Review existing locustfile.py
2. ✅ Document load testing framework
3. ✅ Create execution guide
4. ⏭️ Summary of Week 1 deliverables

### Week 2 (Requires Running Backend)
1. Start backend API server
2. Run baseline load test (10 users)
3. Analyze results
4. Identify bottlenecks
5. Run full load test suite

### Week 3 (Optimization)
1. Implement optimizations
2. Re-run load tests
3. Compare performance improvements
4. Document final capacity limits

---

## Success Criteria

### Performance Validated ✅
- [ ] 100+ concurrent users sustained
- [ ] P95 latency < 500ms for chart calculations
- [ ] Error rate < 1%
- [ ] No memory leaks in soak test
- [ ] System recovers from spike load

### Documentation Complete ✅
- [x] Load testing guide created
- [x] Execution instructions documented
- [x] Performance targets defined
- [x] Bottleneck solutions documented
- [x] CI/CD integration planned

### Capacity Known
- [ ] Maximum concurrent users determined
- [ ] Bottlenecks identified
- [ ] Scaling recommendations made
- [ ] Cost projections calculated

---

**Guide Status:** Complete, ready for execution  
**Next Action:** Run baseline load test (requires backend running)  
**Maintainer:** Autonomous AI System
