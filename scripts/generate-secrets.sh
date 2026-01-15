#!/bin/bash
set -e

# Generate secure secrets for production deployment
# Usage: ./generate-secrets.sh [output-file]

OUTPUT_FILE="${1:-.env.secrets}"

echo "🔐 Generating secure secrets..."

# Generate random secrets
DB_PASSWORD=$(openssl rand -base64 32 | tr -d "=+/" | cut -c1-32)
SECRET_KEY=$(openssl rand -hex 32)
JWT_SECRET=$(openssl rand -hex 32)
GRAFANA_PASSWORD=$(openssl rand -base64 16 | tr -d "=+/" | cut -c1-16)

# Create secrets file
cat > "$OUTPUT_FILE" << EOF
# Generated secrets - $(date)
# KEEP THIS FILE SECURE - DO NOT COMMIT TO VERSION CONTROL

# Database
DB_PASSWORD=${DB_PASSWORD}

# Application Security
SECRET_KEY=${SECRET_KEY}
JWT_SECRET=${JWT_SECRET}

# Monitoring
GRAFANA_PASSWORD=${GRAFANA_PASSWORD}

# Usage:
# 1. Review these secrets
# 2. Copy to .env.production
# 3. Update docker-compose.prod.yml environment variables
# 4. Store securely (password manager, secrets vault)
# 5. Delete this file after copying: rm $OUTPUT_FILE
EOF

chmod 600 "$OUTPUT_FILE"

echo "✅ Secrets generated and saved to: $OUTPUT_FILE"
echo ""
echo "⚠️  IMPORTANT:"
echo "   1. Review the generated secrets"
echo "   2. Copy values to your .env.production file"
echo "   3. Store these secrets securely"
echo "   4. Delete this file: rm $OUTPUT_FILE"
echo ""
echo "📋 Generated secrets preview:"
echo "   - DB_PASSWORD: ${DB_PASSWORD:0:8}... (32 chars)"
echo "   - SECRET_KEY: ${SECRET_KEY:0:16}... (64 chars)"
echo "   - JWT_SECRET: ${JWT_SECRET:0:16}... (64 chars)"
echo "   - GRAFANA_PASSWORD: ${GRAFANA_PASSWORD:0:4}... (16 chars)"
