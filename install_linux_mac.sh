#!/bin/bash

echo "🚀 PMI Bot Setup Script - Linux/Mac"
echo "=================================="
echo ""

# Check Python
echo "✓ Checking Python..."
python3 --version || { echo "❌ Python 3 not found"; exit 1; }

# Install dependencies
echo "✓ Installing dependencies..."
pip3 install -r requirements.txt || { echo "❌ Failed to install dependencies"; exit 1; }

# Install Chromium
echo "✓ Installing Chromium..."
python3 -m playwright install chromium || { echo "❌ Failed to install Chromium"; exit 1; }

echo ""
echo "✅ SETUP COMPLETE!"
echo ""
echo "🎯 Next steps:"
echo ""
echo "Option 1: Run bot directly"
echo "  python3 bot_pmi.py"
echo ""
echo "Option 2: Setup systemd service (auto-start)"
echo "  sudo cp bot-pmi.service /etc/systemd/system/"
echo "  sudo systemctl daemon-reload"
echo "  sudo systemctl enable bot-pmi.service"
echo "  sudo systemctl start bot-pmi.service"
echo ""
echo "Option 3: Use Docker Compose"
echo "  docker-compose up -d"
echo ""
echo "Then open Telegram and use the bot! 🤖"
