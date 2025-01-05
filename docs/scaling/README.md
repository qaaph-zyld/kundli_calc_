# Service Scaling Framework Documentation

## Overview
The Service Scaling Framework provides a comprehensive solution for managing service scaling operations in the Kundli Calculation Web Service. It supports horizontal, vertical, and hybrid scaling strategies with built-in monitoring, validation, and integration capabilities.

## Architecture
The framework consists of several key components:

### 1. Scaling Strategies
- **Horizontal Scaling**: Manages replica-based scaling
- **Vertical Scaling**: Handles resource-based scaling
- **Hybrid Scaling**: Combines both approaches for optimal scaling

### 2. Scaling Processing
- **State Management**: Tracks scaling states
- **Operation Execution**: Handles scaling operations
- **Error Handling**: Manages failures and recovery

### 3. Scaling Configuration
- **Resource Configuration**: CPU and memory settings
- **Replica Configuration**: Instance count settings
- **Policy Configuration**: Scaling rules and thresholds

### 4. Scaling Monitoring
- **Resource Metrics**: CPU, memory usage
- **Performance Metrics**: Latency, throughput
- **Business Metrics**: Cost, savings

### 5. Scaling Validation
- **Configuration Validation**: Verifies settings
- **Resource Validation**: Checks resource usage
- **Performance Validation**: Validates metrics

### 6. Scaling Integration
- **Platform Integration**: Kubernetes, Cloud, Standalone
- **API Integration**: RESTful endpoints
- **Metrics Integration**: Prometheus support

## Installation

```bash
# Install required packages
pip install -r requirements.txt

# Set up configuration
cp config/scaling.example.json config/scaling.json
```

## Configuration

### Basic Configuration
```json
{
    "mode": "hybrid",
    "resources": {
        "min_cpu": 0.1,
        "max_cpu": 4.0,
        "min_memory": 128,
        "max_memory": 8192
    },
    "replicas": {
        "min_replicas": 1,
        "max_replicas": 10,
        "target_replicas": 2
    }
}
```

### Advanced Configuration
```json
{
    "mode": "hybrid",
    "resources": {
        "min_cpu": 0.1,
        "max_cpu": 4.0,
        "min_memory": 128,
        "max_memory": 8192,
        "cpu_request": 0.5,
        "memory_request": 512,
        "cpu_limit": 2.0,
        "memory_limit": 4096
    },
    "replicas": {
        "min_replicas": 1,
        "max_replicas": 10,
        "target_replicas": 2,
        "scale_up_threshold": 0.8,
        "scale_down_threshold": 0.2
    },
    "triggers": {
        "cpu_threshold": 0.8,
        "memory_threshold": 0.8,
        "request_threshold": 1000,
        "latency_threshold": 0.5,
        "evaluation_period": 60,
        "cooldown_period": 300
    },
    "policy": {
        "mode": "hybrid",
        "triggers": ["cpu_usage", "memory_usage"],
        "priority_triggers": ["cpu_usage"],
        "scale_up_factor": 1.5,
        "scale_down_factor": 0.75
    }
}
```

## Usage

### Starting the Service
```python
from app.core.scaling.integration import ScalingIntegration

# Initialize integration
integration = ScalingIntegration(
    mode="standalone",
    config_path="config/scaling.json"
)

# Start integration
await integration.start()
```

### API Endpoints

#### Health Check
```bash
curl http://localhost:8001/health
```

#### Get Metrics
```bash
curl http://localhost:8001/metrics
```

#### Trigger Scaling
```bash
curl -X POST http://localhost:8001/scale \
    -H "Content-Type: application/json" \
    -d '{"mode": "horizontal", "replicas": 3}'
```

#### Get Configuration
```bash
curl http://localhost:8001/config
```

#### Update Configuration
```bash
curl -X POST http://localhost:8001/config \
    -H "Content-Type: application/json" \
    -d @config/scaling.json
```

#### Get Validation
```bash
curl http://localhost:8001/validation
```

## Monitoring

### Prometheus Metrics
The following metrics are available at `http://localhost:8000/metrics`:

- `scaling_cpu_usage`: CPU usage percentage
- `scaling_memory_usage`: Memory usage percentage
- `scaling_request_latency`: Request latency in seconds
- `scaling_request_count`: Total request count
- `scaling_operations_total`: Total scaling operations
- `scaling_operation_duration`: Scaling operation duration
- `scaling_cost`: Scaling cost in dollars
- `scaling_savings`: Cost savings in dollars

### Grafana Dashboard
A sample Grafana dashboard is available in `dashboards/scaling.json`.

## Development

### Running Tests
```bash
# Run unit tests
pytest tests/scaling/unit

# Run integration tests
pytest tests/scaling/integration

# Run all tests with coverage
pytest tests/scaling --cov=app/core/scaling
```

### Code Style
```bash
# Check code style
flake8 app/core/scaling

# Format code
black app/core/scaling
```

### Documentation
```bash
# Generate API documentation
pdoc --html app/core/scaling

# Generate coverage report
coverage html
```

## Best Practices

### 1. Configuration
- Use environment-specific configurations
- Validate all configuration changes
- Keep sensitive data in secrets

### 2. Monitoring
- Monitor both system and business metrics
- Set up appropriate alerts
- Maintain metric retention policies

### 3. Scaling
- Start with conservative thresholds
- Use appropriate cooldown periods
- Monitor scaling costs

### 4. Security
- Secure API endpoints
- Encrypt sensitive data
- Implement access controls

## Troubleshooting

### Common Issues

1. **Scaling Not Triggered**
   - Check trigger thresholds
   - Verify metric collection
   - Review cooldown periods

2. **High Resource Usage**
   - Adjust scaling thresholds
   - Review resource limits
   - Check for resource leaks

3. **Integration Errors**
   - Verify platform credentials
   - Check network connectivity
   - Review API permissions

### Logging

Logs are available in the following locations:
- `logs/scaling_integration.log`
- `logs/scaling_monitor.log`
- `logs/scaling_validator.log`

## Support

For support and bug reports:
- GitHub Issues: [Project Issues](https://github.com/your-repo/issues)
- Documentation: [Project Wiki](https://github.com/your-repo/wiki)
- Email: support@your-domain.com

## License
This project is licensed under the MIT License - see the LICENSE file for details.
