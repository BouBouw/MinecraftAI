#!/bin/bash
# Stop Real Minecraft Bot POV Streaming

echo "🛑 Stopping Minecraft Bot POV Streaming"
echo "========================================"
echo ""

# Stop stream
echo "📺 Stopping Twitch stream..."
pkill -f "ffmpeg.*rtmp" 2>/dev/null
if [ $? -eq 0 ]; then
    echo "✅ Stream stopped"
else
    echo "ℹ️  No stream was running"
fi

# Stop POV server
echo ""
echo "🤖 Stopping POV bridge server..."
pkill -f "rl-bridge-pov-server" 2>/dev/null
if [ $? -eq 0 ]; then
    echo "✅ POV server stopped"
else
    echo "ℹ️  No POV server was running"
fi

# Restart normal bridge server (optional)
echo ""
read -p "🔄 Restart normal rl-bridge-server? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "🚀 Starting normal bridge server..."
    cd ~/MinecraftAI/minecraft-bot
    node rl-bridge-server.js &
    echo "✅ Normal bridge server restarted"
fi

echo ""
echo "✅ Cleanup complete!"
echo ""
