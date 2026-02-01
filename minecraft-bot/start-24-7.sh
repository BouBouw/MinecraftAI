#!/bin/bash
# Setup Minecraft Bot Bridge as systemd service for 24/7 operation

echo "🚀 Setting up Minecraft Bot Bridge 24/7"
echo "======================================"
echo ""

# Must run as root
if [ "$EUID" -ne 0 ]; then
    echo "❌ Run with sudo"
    exit 1
fi

REAL_USER=${SUDO_USER:-$USER}
USER_HOME=$(eval echo ~$REAL_USER)

echo "👤 User: $REAL_USER"
echo ""

# Stop existing processes
echo "🧹 Cleaning up..."
pkill -f "rl-bridge-server" 2>/dev/null
sleep 1

# Create systemd service
cat > /etc/systemd/system/minecraft-bridge.service << EOF
[Unit]
Description=Minecraft Bot Bridge Server
After=network.target

[Service]
Type=simple
User=$REAL_USER
WorkingDirectory=$USER_HOME/MinecraftAI/minecraft-bot
Environment="NODE_ENV=production"
ExecStart=/usr/bin/node rl-bridge-server.js
Restart=always
RestartSec=10
StandardOutput=append:$USER_HOME/minecraft-stream/logs/bridge.log
StandardError=append:$USER_HOME/minecraft-stream/logs/bridge-error.log
MemoryMax=2G

[Install]
WantedBy=multi-user.target
EOF

# Create logs dir
mkdir -p "$USER_HOME/minecraft-stream/logs"

# Reload and enable
systemctl daemon-reload
systemctl enable minecraft-bridge.service
systemctl start minecraft-bridge.service

echo "✅ Setup complete!"
echo ""
echo "📊 Status:"
systemctl status minecraft-bridge.service --no-pager
echo ""
echo "🎮 Control with: ~/MinecraftAI/minecraft-bot/bridge-control.sh"
