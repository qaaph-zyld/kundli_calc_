#!/bin/bash
set -e

# Database restore script
# Usage: ./restore.sh <backup-file>

if [ -z "$1" ]; then
    echo "❌ Error: Backup file not specified"
    echo "Usage: ./restore.sh <backup-file>"
    echo ""
    echo "Available backups:"
    ls -lh backups/*.sql 2>/dev/null || echo "No backups found in backups/ directory"
    exit 1
fi

BACKUP_FILE="$1"

if [ ! -f "$BACKUP_FILE" ]; then
    echo "❌ Error: Backup file not found: $BACKUP_FILE"
    exit 1
fi

echo "⚠️  WARNING: This will restore the database from backup"
echo "   Backup file: $BACKUP_FILE"
echo "   All current data will be replaced!"
echo ""
read -p "Are you sure you want to continue? (type 'yes' to confirm): " CONFIRM

if [ "$CONFIRM" != "yes" ]; then
    echo "❌ Restore cancelled"
    exit 0
fi

echo "🔄 Starting database restore..."

# Check if database container is running
if ! docker-compose ps postgres | grep -q "Up"; then
    echo "❌ Error: PostgreSQL container is not running"
    echo "Start it with: docker-compose -f docker-compose.prod.yml up -d postgres"
    exit 1
fi

# Get database credentials from environment
if [ -f ".env.production" ]; then
    export $(cat .env.production | grep -v '^#' | grep -E 'DB_PASSWORD' | xargs)
fi

DB_USER="${DB_USER:-kundli_user}"
DB_NAME="${DB_NAME:-kundli_prod}"
DB_PASSWORD="${DB_PASSWORD}"

if [ -z "$DB_PASSWORD" ]; then
    echo "❌ Error: DB_PASSWORD not found in .env.production"
    exit 1
fi

# Stop backend to prevent writes during restore
echo "🛑 Stopping backend service..."
docker-compose -f docker-compose.prod.yml stop backend

# Create a backup of current state before restore
CURRENT_BACKUP="backups/pre-restore-$(date +%Y%m%d-%H%M%S).sql"
echo "📦 Creating backup of current state: $CURRENT_BACKUP"
mkdir -p backups
docker-compose exec -T postgres pg_dump -U "$DB_USER" -d "$DB_NAME" -F c > "$CURRENT_BACKUP"

# Drop and recreate database
echo "🗑️  Dropping existing database..."
docker-compose exec -T postgres psql -U "$DB_USER" -d postgres -c "DROP DATABASE IF EXISTS ${DB_NAME};"
docker-compose exec -T postgres psql -U "$DB_USER" -d postgres -c "CREATE DATABASE ${DB_NAME};"

# Restore from backup
echo "📥 Restoring from backup..."
if [[ "$BACKUP_FILE" == *.sql ]]; then
    # Plain SQL file
    cat "$BACKUP_FILE" | docker-compose exec -T postgres psql -U "$DB_USER" -d "$DB_NAME"
else
    # Custom format
    cat "$BACKUP_FILE" | docker-compose exec -T postgres pg_restore -U "$DB_USER" -d "$DB_NAME" -v
fi

# Run migrations to ensure schema is up to date
echo "🔄 Running database migrations..."
docker-compose -f docker-compose.prod.yml start backend
sleep 5
docker-compose exec -T backend alembic upgrade head

echo "✅ Database restore complete!"
echo ""
echo "📋 Next steps:"
echo "   1. Verify data integrity"
echo "   2. Test application functionality"
echo "   3. Check logs: docker-compose logs backend"
echo ""
echo "💾 Pre-restore backup saved: $CURRENT_BACKUP"
echo "   (Keep for rollback if needed)"
