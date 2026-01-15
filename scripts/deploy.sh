#!/bin/bash
set -e

# Deployment script for Kundli Calculation Service
# Usage: ./deploy.sh [environment]

ENVIRONMENT=${1:-production}
COMPOSE_FILE="docker-compose.prod.yml"

echo "🚀 Starting deployment to $ENVIRONMENT..."

# Check if .env file exists
if [ ! -f ".env.${ENVIRONMENT}" ]; then
    echo "❌ Error: .env.${ENVIRONMENT} file not found"
    exit 1
fi

# Load environment variables
export $(cat .env.${ENVIRONMENT} | grep -v '^#' | xargs)

# Pull latest changes
echo "📥 Pulling latest changes from Git..."
git pull origin master

# Pull latest Docker images
echo "🐳 Pulling latest Docker images..."
docker-compose -f ${COMPOSE_FILE} pull

# Stop existing containers
echo "🛑 Stopping existing containers..."
docker-compose -f ${COMPOSE_FILE} down

# Start services
echo "🚀 Starting services..."
docker-compose -f ${COMPOSE_FILE} up -d

# Wait for services to be ready
echo "⏳ Waiting for services to be ready..."
sleep 10

# Run database migrations
echo "🔄 Running database migrations..."
docker-compose -f ${COMPOSE_FILE} exec -T backend alembic upgrade head

# Health check
echo "🏥 Performing health checks..."
BACKEND_HEALTH=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/api/v1/system/health || echo "000")

if [ "$BACKEND_HEALTH" = "200" ]; then
    echo "✅ Backend is healthy"
else
    echo "❌ Backend health check failed (HTTP $BACKEND_HEALTH)"
    docker-compose -f ${COMPOSE_FILE} logs backend --tail=50
    exit 1
fi

# Show running containers
echo "📊 Running containers:"
docker-compose -f ${COMPOSE_FILE} ps

echo "✅ Deployment complete!"
echo "📍 Backend API: http://localhost:8000/docs"
echo "📍 Prometheus: http://localhost:9090"
echo "📍 Grafana: http://localhost:3001"
