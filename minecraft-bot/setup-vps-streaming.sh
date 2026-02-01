#!/bin/bash
# Setup VPS for Streaming Minecraft Bot
# Run this on your VPS to install all dependencies

echo "🚀 Setting up VPS for Minecraft Bot Streaming"
echo "============================================="
echo ""

# Check if running as root
if [ "$EUID" -ne 0 ]; then
    echo "❌ Please run as root or with sudo"
    exit 1
fi

# Update packages
echo "📦 Updating packages..."
apt-get update -y

# Install dependencies
echo "📦 Installing dependencies..."
apt-get install -y \
    xvfb \
    x11vnc \
    ffmpeg \
    libavcodec-extra \
    pulseaudio \
    pulseaudio-utils \
    obs-studio \
    wmctrl \
    xdotool \
    git \
    curl \
    wget

# Install Node.js if not present
if ! command -v node &> /dev/null; then
    echo "📦 Installing Node.js..."
    curl -fsSL https://deb.nodesource.com/setup_20.x | bash -
    apt-get install -y nodejs
fi

echo ""
echo "✅ Installation complete!"
echo ""

# Create streaming directory
STREAM_DIR="/home/server/minecraft-stream"
mkdir -p "$STREAM_DIR/screenshots"
mkdir -p "$STREAM_DIR/logs"

# Create environment file
cat > "$STREAM_DIR/.env" << 'EOF'
# Stream Configuration
STREAM_RESOLUTION=1920x1080
STREAM_FPS=30
STREAM_BITRATE=4500k

# Twitch Configuration
TWITCH_ENABLED=true
TWITCH_STREAM_KEY=your_twitch_stream_key_here

# TikTok Configuration
TIKTOK_ENABLED=true
TIKTOK_STREAM_KEY=your_tiktok_stream_key_here

# Capture Settings
CAPTURE_SCREENSHOTS=false
SCREENSHOT_FPS=10
EOF

echo "📁 Created streaming directory: $STREAM_DIR"
echo ""
echo "📝 Edit $STREAM_DIR/.env with your stream keys"
echo ""

# Create systemd service for virtual display
cat > /etc/systemd/system/xvfb.service << 'EOF'
[Unit]
Description=Virtual Frame Buffer for Streaming
After=network.target

[Service]
Type=simple
User=server
Environment=DISPLAY=:99
ExecStart=/usr/bin/Xvfb :99 -screen 0 1920x1080x24
Restart=on-failure
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable xvfb
systemctl start xvfb

echo "✅ Virtual display started (DISPLAY=:99)"
echo ""

# Create systemd service for Minecraft bot stream
cat > /etc/systemd/system/minecraft-bot-stream.service << 'EOF'
[Unit]
Description=Minecraft Bot POV Streamer
After=xvfb.service
Requires=xvfb.service

[Service]
Type=simple
User=server
WorkingDirectory=/home/server/MinecraftAI/minecraft-bot
Environment=DISPLAY=:99
ExecStart=/usr/bin/node stream-bot-viewer.js
Restart=on-failure
RestartSec=10
StandardOutput=append:/home/server/minecraft-stream/logs/bot.log
StandardError=append:/home/server/minecraft-stream/logs/bot-error.log

[Install]
WantedBy=multi-user.target
EOF

echo "✅ Systemd services created"
echo ""

# Create stream control script
cat > "$STREAM_DIR/stream-control.sh" << 'EOF'
#!/bin/bash

STREAM_DIR="/home/server/minecraft-stream"
ENV_FILE="$STREAM_DIR/.env"

source "$ENV_FILE"

case "$1" in
    start)
        echo "🎬 Starting stream..."

        # Start OBS with scene configuration
        obs --startstreaming --minimize-to-tray &
        OBS_PID=$!
        echo "OBS PID: $OBS_PID"

        # Or use ffmpeg directly
        if [ "$TWITCH_ENABLED" = "true" ]; then
            ffmpeg -f x11grab -s $STREAM_RESOLUTION -r $STREAM_FPS -i :99 \
                -vcodec libx264 -preset veryfast -b:v $STREAM_BITRATE \
                -pix_fmt yuv420p -g 50 -c:a aac -b:a 128k -ar 44100 \
                -f flv "rtmp://live.twitch.tv/app/$TWITCH_STREAM_KEY" &
            echo "✅ Streaming to Twitch (PID: $!)"
        fi

        if [ "$TIKTOK_ENABLED" = "true" ]; then
            ffmpeg -f x11grab -s $STREAM_RESOLUTION -r $STREAM_FPS -i :99 \
                -vcodec libx264 -preset veryfast -b:v $STREAM_BITRATE \
                -pix_fmt yuv420p -g 50 -c:a aac -b:a 128k -ar 44100 \
                -f flv "rtmp://push.tiktok.com/live/$TIKTOK_STREAM_KEY" &
            echo "✅ Streaming to TikTok (PID: $!)"
        fi
        ;;

    stop)
        echo "🛑 Stopping stream..."
        pkill -f "ffmpeg.*rtmp"
        pkill -f obs
        echo "✅ Stream stopped"
        ;;

    status)
        if pgrep -f "ffmpeg.*rtmp" > /dev/null; then
            echo "✅ Stream is ACTIVE"
        else
            echo "❌ Stream is OFFLINE"
        fi

        echo ""
        echo "Services status:"
        systemctl status xvfb --no-pager
        systemctl status minecraft-bot-stream --no-pager
        ;;

    restart)
        $0 stop
        sleep 2
        $0 start
        ;;

    *)
        echo "Usage: $0 {start|stop|status|restart}"
        exit 1
        ;;
esac
EOF

chmod +x "$STREAM_DIR/stream-control.sh"

echo "✅ Stream control script created: $STREAM_DIR/stream-control.sh"
echo ""

cat << 'EOF'
╔════════════════════════════════════════════════════════════╗
║  🎉 VPS Streaming Setup Complete!                           ║
╚════════════════════════════════════════════════════════════╝

📝 Next Steps:

1. Edit stream configuration:
   nano /home/server/minecraft-stream/.env

2. Add your Twitch stream key from: https://dashboard.twitch.tv/u/username/stream/key
   TWITCH_STREAM_KEY=live_1234567890_ABCDEFGHIJ

3. Add your TikTok stream key (use TikTok Live Studio app to get it):
   TIKTOK_STREAM_KEY=your_key_here

4. Start streaming:
   /home/server/minecraft-stream/stream-control.sh start

5. Check status:
   /home/server/minecraft-stream/stream-control.sh status

6. View logs:
   tail -f /home/server/minecraft-stream/logs/bot.log

💡 Tips:
- Stream runs 24/7 on VPS (no PC needed!)
- Both Twitch & TikTok simultaneously
- Monitor with: watch -n 5 'nvidia-smi' (if GPU available)
- Adjust STREAM_BITRATE in .env based on your upload speed

EOF
