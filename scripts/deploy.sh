#!/bin/bash
# uSipipo Support Bot - Deployment Script
# This script deploys the support bot to production

set -e

echo "🚀 Deploying uSipipo Support Bot..."

# Configuration
SERVICE_NAME="usipipo-support-bot"
INSTALL_DIR="/opt/usipipo-support-bot"
LOG_DIR="/var/log/usipipo"

# Check if running as root
if [ "$EUID" -ne 0 ]; then
  echo "❌ Please run as root (sudo)"
  exit 1
fi

# Create log directory
echo "📁 Creating log directory..."
mkdir -p "$LOG_DIR"
chown -R usipipo:usipipo "$LOG_DIR" || true

# Install directory
echo "📁 Creating install directory..."
mkdir -p "$INSTALL_DIR"
chown -R usipipo:usipipo "$INSTALL_DIR" || true

# Copy service file
echo "📋 Installing systemd service..."
cp "$INSTALL_DIR/usipipo-support-bot.service" "/etc/systemd/system/$SERVICE_NAME.service"

# Reload systemd
echo "🔄 Reloading systemd..."
systemctl daemon-reload

# Enable service
echo "✅ Enabling service..."
systemctl enable "$SERVICE_NAME"

# Restart service
echo "🔄 Restarting service..."
systemctl restart "$SERVICE_NAME"

# Check status
echo "📊 Service status:"
systemctl status "$SERVICE_NAME" --no-pager

echo ""
echo "✅ Deployment complete!"
echo ""
echo "View logs: sudo journalctl -u $SERVICE_NAME -f"
echo "Stop bot: sudo systemctl stop $SERVICE_NAME"
echo "Start bot: sudo systemctl start $SERVICE_NAME"
