#!/bin/bash
set -e

# Health check script for all services
# Usage: ./health-check.sh

COMPOSE_FILE="${COMPOSE_FILE:-docker-compose.prod.yml}"
FAILED=0

echo "🏥 Running health checks for all services..."
echo ""

# Function to check HTTP endpoint
check_http() {
    local name=$1
    local url=$2
    local expected=${3:-200}
    
    echo -n "Checking $name... "
    
    HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" "$url" 2>/dev/null || echo "000")
    
    if [ "$HTTP_CODE" = "$expected" ]; then
        echo "✅ OK (HTTP $HTTP_CODE)"
        return 0
    else
        echo "❌ FAILED (HTTP $HTTP_CODE, expected $expected)"
        FAILED=$((FAILED + 1))
        return 1
    fi
}

# Function to check container status
check_container() {
    local name=$1
    
    echo -n "Checking container $name... "
    
    if docker-compose -f "$COMPOSE_FILE" ps "$name" | grep -q "Up"; then
        echo "✅ Running"
        return 0
    else
        echo "❌ Not running"
        FAILED=$((FAILED + 1))
        return 1
    fi
}

# Function to check database
check_database() {
    echo -n "Checking PostgreSQL... "
    
    if docker-compose -f "$COMPOSE_FILE" exec -T postgres pg_isready -U kundli_user -d kundli_prod > /dev/null 2>&1; then
        echo "✅ Accepting connections"
        
        # Check connection count
        CONN_COUNT=$(docker-compose -f "$COMPOSE_FILE" exec -T postgres psql -U kundli_user -d kundli_prod -t -c "SELECT count(*) FROM pg_stat_activity;" 2>/dev/null | tr -d ' ')
        echo "   Active connections: $CONN_COUNT"
        return 0
    else
        echo "❌ Not accepting connections"
        FAILED=$((FAILED + 1))
        return 1
    fi
}

# Function to check Redis
check_redis() {
    echo -n "Checking Redis... "
    
    if docker-compose -f "$COMPOSE_FILE" exec -T redis redis-cli PING > /dev/null 2>&1; then
        echo "✅ Responding"
        
        # Check memory usage
        MEMORY=$(docker-compose -f "$COMPOSE_FILE" exec -T redis redis-cli INFO memory | grep "used_memory_human" | cut -d: -f2 | tr -d '\r')
        echo "   Memory usage: $MEMORY"
        return 0
    else
        echo "❌ Not responding"
        FAILED=$((FAILED + 1))
        return 1
    fi
}

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Container Status"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
check_container "backend"
check_container "postgres"
check_container "redis"
check_container "prometheus"
check_container "grafana"
if docker-compose -f "$COMPOSE_FILE" ps nginx > /dev/null 2>&1; then
    check_container "nginx"
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Service Health"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
check_database
check_redis

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "HTTP Endpoints"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
check_http "Backend Health" "http://localhost:8000/api/v1/system/health" "200"
check_http "Backend API Docs" "http://localhost:8000/docs" "200"
check_http "Prometheus" "http://localhost:9090/-/healthy" "200"
check_http "Grafana" "http://localhost:3001/api/health" "200"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Resource Usage"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Docker stats (one-time snapshot)
docker stats --no-stream --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}\t{{.NetIO}}" $(docker-compose -f "$COMPOSE_FILE" ps -q)

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Disk Usage"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Docker volumes
docker system df -v | grep -A 100 "VOLUME NAME" | grep kundli || echo "No volumes found"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Summary"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if [ $FAILED -eq 0 ]; then
    echo "✅ All checks passed!"
    echo ""
    echo "📍 Services accessible at:"
    echo "   Backend API: http://localhost:8000/docs"
    echo "   Prometheus: http://localhost:9090"
    echo "   Grafana: http://localhost:3001"
    exit 0
else
    echo "❌ $FAILED check(s) failed"
    echo ""
    echo "🔍 Troubleshooting:"
    echo "   View logs: docker-compose -f $COMPOSE_FILE logs"
    echo "   Restart services: docker-compose -f $COMPOSE_FILE restart"
    echo "   Check documentation: docs/TROUBLESHOOTING.md"
    exit 1
fi
