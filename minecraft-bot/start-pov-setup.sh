#!/bin/bash
# Start Real Minecraft Bot POV Streaming - Automated Setup

echo "🎬 Starting Real Minecraft Bot POV Streaming"
echo "=============================================="
echo ""

# Check if running on VPS
if [ ! -d "$HOME/minecraft-stream" ]; then
    echo "📁 Creating directories..."
    mkdir -p ~/minecraft-stream/screenshots
    mkdir -p ~/minecraft-stream/logs
    echo "✅ Directories created\n"
fi

# Check config
if [ ! -f "$HOME/minecraft-stream/.env" ]; then
    echo "❌ Configuration not found!"
    echo "📝 Creating default config..."
    cat > "$HOME/minecraft-stream/.env" << 'EOF'
STREAM_RESOLUTION=1280x720
STREAM_FPS=30
STREAM_BITRATE=3000k
TWITCH_STREAM_KEY=live_VOTRE_CLE_ICI
EOF
    echo "✅ Config created"
    echo "⚠️  Edit ~/minecraft-stream/.env and add your Twitch stream key!\n"
fi

# Navigate to bot directory
cd ~/MinecraftAI/minecraft-bot

# Check if prismarine-viewer is installed
if ! npm list prismarine-viewer > /dev/null 2>&1; then
    echo "📦 Installing prismarine-viewer..."
    npm install prismarine-viewer
    echo "✅ Installation complete\n"
else
    echo "✅ prismarine-viewer already installed\n"
fi

# Stop old bridge server
echo "🧹 Stopping old bridge server..."
pkill -f "rl-bridge-server" 2>/dev/null
sleep 2

# Stop old streams
echo "🧹 Stopping old streams..."
pkill -f "ffmpeg.*rtmp" 2>/dev/null
sleep 2

# Start POV server
echo "🚀 Starting POV bridge server..."
node rl-bridge-pov-server.js &
POV_PID=$!
echo "✅ POV server started (PID: ${POV_PID})"

# Wait for screenshots to generate
echo ""
echo "⏳ Waiting for screenshots to generate (10 seconds)..."
sleep 10

# Check if screenshots were generated
SCREENSHOT_COUNT=$(ls -1 ~/minecraft-stream/screenshots/frame_*.jpg 2>/dev/null | wc -l)
echo "📸 Screenshots captured: $SCREENSHOT_COUNT"

if [ "$SCREENSHOT_COUNT" -eq 0 ]; then
    echo ""
    echo "⚠️  WARNING: No screenshots captured yet!"
    echo "💡 This is normal if:"
    echo "   - prismarine-viewer is still initializing"
    echo "   - The bot hasn't spawned yet"
    echo ""
    echo "💡 The stream will start automatically when screenshots are available"
    echo ""
fi

# Start stream
echo ""
echo "📺 Starting Twitch stream..."
bash ~/MinecraftAI/minecraft-bot/start-pov-stream.sh

echo ""
echo "✅ Setup complete!"
echo ""
echo "📊 Monitor:"
echo "   Screenshots: watch -n 2 'ls -1 ~/minecraft-stream/screenshots/frame_*.jpg | wc -l'"
echo "   Stream logs: tail -f ~/minecraft-stream/logs/pov-stream.log"
echo "   POV server:  http://localhost:3000/health"
echo ""
echo "🛑 Stop everything:"
echo "   pkill -f 'rl-bridge-pov-server'"
echo "   pkill -f 'ffmpeg.*rtmp'"
echo ""
