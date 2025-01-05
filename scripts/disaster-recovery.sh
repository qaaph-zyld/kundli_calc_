#!/bin/bash

# Configuration
BACKUP_DIR="/backup"
S3_BUCKET="s3://kundli-backups"

# Function to restore MongoDB
restore_mongodb() {
    local backup_file=$1
    echo "Restoring MongoDB from $backup_file..."
    mongorestore --uri="$MONGODB_URL" --gzip --archive="$backup_file"
}

# Function to restore Redis
restore_redis() {
    local backup_file=$1
    echo "Restoring Redis from $backup_file..."
    systemctl stop redis
    cp "$backup_file" /data/dump.rdb
    systemctl start redis
}

# Function to restore application files
restore_app_files() {
    local backup_file=$1
    echo "Restoring application files from $backup_file..."
    tar -xzf "$backup_file" -C /
}

# Main recovery procedure
main() {
    local recovery_timestamp=$1
    
    if [ -z "$recovery_timestamp" ]; then
        echo "Please provide a backup timestamp for recovery"
        exit 1
    }
    
    # Download backups from S3
    echo "Downloading backups from S3..."
    aws s3 sync "$S3_BUCKET/daily/$recovery_timestamp/" "$BACKUP_DIR/"
    
    # Stop services
    echo "Stopping services..."
    docker-compose down
    
    # Restore backups
    restore_mongodb "$BACKUP_DIR/mongodb_$recovery_timestamp.gz"
    restore_redis "$BACKUP_DIR/redis_$recovery_timestamp.rdb"
    restore_app_files "$BACKUP_DIR/app_files_$recovery_timestamp.tar.gz"
    
    # Start services
    echo "Starting services..."
    docker-compose up -d
    
    # Verify recovery
    echo "Verifying recovery..."
    curl -f http://localhost:8000/health
    
    echo "Recovery completed successfully!"
}

# Execute main function with provided timestamp
main "$1"
