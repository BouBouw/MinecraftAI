#!/bin/bash
# Setup Headless Streaming for Minecraft Bot VPS
# This installs everything needed for streaming WITHOUT a display

echo "🚀 Setting up Headless Minecraft Bot Streaming"
echo "==============================================="
echo ""

# Check if running as root
if [ "$EUID" -ne 0 ]; then
    echo "❌ Please run as root or with sudo"
    exit 1
fi

# Update packages
echo "📦 Updating packages..."
apt-get update -y

# Install headless dependencies (no X11/OBS needed)
echo "📦 Installing headless streaming dependencies..."
apt-get install -y \
    ffmpeg \
    libavcodec-extra \
    git \
    curl \
    wget \
    python3 \
    python3-pip \
    nodejs \
    npm

echo ""
echo "✅ Installation complete!"
echo ""

# Create streaming directory
STREAM_DIR="/home/server/minecraft-stream"
mkdir -p "$STREAM_DIR/screenshots"
mkdir -p "$STREAM_DIR/logs"
chown -R server:server "$STREAM_DIR"

# Create environment file
cat > "$STREAM_DIR/.env" << 'EOF'
# Stream Configuration
STREAM_RESOLUTION=1280x720
STREAM_FPS=30
STREAM_BITRATE=3000k

# Twitch Configuration
TWITCH_ENABLED=false
TWITCH_STREAM_KEY=your_twitch_stream_key_here

# TikTok Configuration
TIKTOK_ENABLED=true
TIKTOK_STREAM_KEY=your_tiktok_stream_key_here

# Capture Settings
CAPTURE_METHOD=screenshot  # Options: screenshot, testpattern
SCREENSHOT_DIR=/home/server/minecraft-stream/screenshots
EOF

chown server:server "$STREAM_DIR/.env"

echo "📁 Created streaming directory: $STREAM_DIR"
echo ""

cat << 'EOF'
╔════════════════════════════════════════════════════════════╗
║  🎉 Headless VPS Streaming Setup Complete!                 ║
╚════════════════════════════════════════════════════════════╝

📝 Next Steps:

1. Edit stream configuration:
   nano /home/server/minecraft-stream/.env

2. Add your TikTok stream key (get from TikTok Live Studio app)
   TIKTOK_STREAM_KEY=your_key_here

3. Add Twitch key if needed:
   TWITCH_ENABLED=true
   TWITCH_STREAM_KEY=live_1234567890_ABCDEFGHIJ

4. Start streaming:
   bash ~/MinecraftAI/minecraft-bot/start-vps-stream.sh

5. Check status:
   ps aux | grep ffmpeg

💡 IMPORTANT - How it works:

Since your VPS is headless (no display), we use:
- Test pattern with text overlay (current method)
- Or screenshots from bot (need to implement)

For REAL Minecraft bot POV streaming, you have two options:

OPTION 1: Screenshot-based (Recommended for VPS)
----------------------------------------------
The bot captures screenshots → ffmpeg encodes them → stream

Pros: True POV, works on headless VPS
Cons: Higher CPU usage, slight delay

To implement:
1. Install prismarine-viewer in minecraft-bot/
   npm install prismarine-viewer

2. Modify rl-bridge-server.js to capture screenshots

3. Update start-vps-stream.sh to use screenshots instead of test pattern

OPTION 2: Dedicated GPU Server (Best Quality)
----------------------------------------------
Rent a GPU server (e.g., Hetzner, Lambda Labs)
Install full desktop environment + OBS
Capture true OpenGL rendering

🔧 Troubleshooting:

Stream won't start?
→ Check stream key in .env

Poor quality?
→ Reduce STREAM_BITRATE to 2000k
→ Reduce STREAM_FPS to 24

High CPU usage?
→ Reduce STREAM_FPS to 24
→ Reduce STREAM_RESOLUTION to 854x480

EOF
