#!/bin/bash

# Configuration
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/backup"
RETENTION_DAYS=30
S3_BUCKET="s3://kundli-backups"

# MongoDB backup
echo "Starting MongoDB backup..."
mongodump --uri="$MONGODB_URL" --gzip --archive="$BACKUP_DIR/mongodb_$TIMESTAMP.gz"

# Redis backup
echo "Starting Redis backup..."
redis-cli save
cp /data/dump.rdb "$BACKUP_DIR/redis_$TIMESTAMP.rdb"

# Application files backup
echo "Backing up application files..."
tar -czf "$BACKUP_DIR/app_files_$TIMESTAMP.tar.gz" /app/data

# Upload to S3
echo "Uploading backups to S3..."
aws s3 sync "$BACKUP_DIR" "$S3_BUCKET/daily/$TIMESTAMP/"

# Cleanup old backups
echo "Cleaning up old backups..."
find "$BACKUP_DIR" -type f -mtime +$RETENTION_DAYS -delete

# Verify backups
echo "Verifying backups..."
aws s3 ls "$S3_BUCKET/daily/$TIMESTAMP/" --recursive

echo "Backup completed successfully!"
