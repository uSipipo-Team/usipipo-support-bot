#!/bin/bash
# uSipipo Support Bot - Environment Setup Script
# This script helps set up the environment for the support bot

set -e

echo "🔧 Setting up uSipipo Support Bot environment..."

# Check if .env exists
if [ -f ".env" ]; then
    echo "⚠️  .env file already exists!"
    read -p "Do you want to overwrite it? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "❌ Aborted"
        exit 1
    fi
fi

# Copy example.env to .env
echo "📋 Creating .env file from example.env..."
cp example.env .env

echo ""
echo "✅ Environment file created!"
echo ""
echo "📝 Next steps:"
echo "1. Edit .env file with your configuration:"
echo "   nano .env"
echo ""
echo "2. Set required variables:"
echo "   - BOT_TOKEN (from @BotFather)"
echo "   - BACKEND_URL (e.g., https://api.usipipo.com)"
echo "   - REDIS_URL (e.g., redis://localhost:6379/1)"
echo ""
echo "3. Install dependencies:"
echo "   uv sync --dev"
echo ""
echo "4. Run the bot:"
echo "   uv run python -m src"
echo ""
