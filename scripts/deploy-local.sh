#!/bin/bash
set -e

# One-command local production deployment
# Usage: ./deploy-local.sh

echo "🚀 Starting local production deployment..."
echo ""

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Error: Docker is not running"
    echo "Please start Docker Desktop and try again"
    exit 1
fi

# Generate secrets if not exists
if [ ! -f .env.local ]; then
    echo "📝 Generating secrets..."
    cat > .env.local << EOF
# Generated for local production testing
DB_PASSWORD=$(openssl rand -base64 32 | tr -d "=+/" | cut -c1-32)
SECRET_KEY=$(openssl rand -hex 32)
JWT_SECRET=$(openssl rand -hex 32)
GRAFANA_PASSWORD=admin123
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8000
EOF
    echo "✅ Secrets generated in .env.local"
else
    echo "📋 Using existing .env.local"
fi

# Load secrets
echo "🔐 Loading environment variables..."
export $(cat .env.local | grep -v '^#' | xargs)

# Create production env file if not exists
if [ ! -f backend/.env.production ]; then
    echo "📝 Creating backend/.env.production..."
    cat > backend/.env.production << EOF
ENVIRONMENT=production
DEBUG=False
LOG_LEVEL=INFO

API_V1_STR=/api/v1
PROJECT_NAME="Kundli Calculation Service"
VERSION=1.0.0

ALLOWED_ORIGINS=${ALLOWED_ORIGINS:-http://localhost:3000}
ALLOWED_HOSTS=localhost,127.0.0.1

DATABASE_URL=postgresql://kundli_user:${DB_PASSWORD}@postgres:5432/kundli_prod
ASYNC_DATABASE_URL=postgresql+asyncpg://kundli_user:${DB_PASSWORD}@postgres:5432/kundli_prod

REDIS_URL=redis://redis:6379/0

SECRET_KEY=${SECRET_KEY}
JWT_SECRET=${JWT_SECRET}
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

EPHEMERIS_PATH=/app/ephemeris

ENABLE_METRICS=True
PROMETHEUS_PORT=9090

RATE_LIMIT_PER_MINUTE=60
RATE_LIMIT_PER_HOUR=1000
EOF
    echo "✅ Backend environment created"
fi

# Build images
echo ""
echo "🔨 Building Docker images..."
docker-compose -f docker-compose.prod.yml build

# Stop any existing containers
echo ""
echo "🛑 Stopping existing containers..."
docker-compose -f docker-compose.prod.yml down

# Start services
echo ""
echo "🚀 Starting services..."
docker-compose -f docker-compose.prod.yml up -d

# Wait for database to be ready
echo ""
echo "⏳ Waiting for database to be ready..."
sleep 10

# Run migrations
echo ""
echo "🔄 Running database migrations..."
docker-compose -f docker-compose.prod.yml exec -T backend alembic upgrade head || echo "⚠️  Migration failed (database might not be ready yet)"

# Wait for all services
echo ""
echo "⏳ Waiting for services to be ready..."
sleep 20

# Health checks
echo ""
echo "🏥 Running health checks..."
echo ""

check_service() {
    local name=$1
    local url=$2
    echo -n "Checking $name... "
    if curl -sf "$url" > /dev/null 2>&1; then
        echo "✅ Healthy"
        return 0
    else
        echo "❌ Unhealthy"
        return 1
    fi
}

HEALTHY=true

check_service "Backend API" "http://localhost:8000/api/v1/system/health" || HEALTHY=false
check_service "API Docs" "http://localhost:8000/docs" || HEALTHY=false
check_service "Prometheus" "http://localhost:9090/-/healthy" || HEALTHY=false
check_service "Grafana" "http://localhost:3001/api/health" || HEALTHY=false

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if [ "$HEALTHY" = true ]; then
    echo "✅ Deployment complete! All services are healthy."
else
    echo "⚠️  Deployment complete with warnings. Some services are not responding."
    echo "   This is normal if services are still starting up."
    echo "   Wait a few more seconds and check again with: ./scripts/health-check.sh"
fi

echo ""
echo "📍 Services accessible at:"
echo "   Backend API: http://localhost:8000/docs"
echo "   Prometheus: http://localhost:9090"
echo "   Grafana: http://localhost:3001"
echo "      Username: admin"
echo "      Password: ${GRAFANA_PASSWORD}"
echo ""
echo "📋 Useful commands:"
echo "   View logs: docker-compose -f docker-compose.prod.yml logs -f"
echo "   Check health: ./scripts/health-check.sh"
echo "   Stop services: docker-compose -f docker-compose.prod.yml down"
echo ""
echo "🔐 Secrets stored in: .env.local"
echo "   Keep this file secure and DO NOT commit to git"
echo ""
