#!/bin/bash
# Stream Minecraft Bot to Twitch from VPS (Headless)
# Simple version - Twitch only, no OBS needed

# Auto-detect home directory
STREAM_DIR="$HOME/minecraft-stream"
ENV_FILE="$STREAM_DIR/.env"

# Load configuration
if [ -f "$ENV_FILE" ]; then
    source "$ENV_FILE"
else
    echo "❌ Configuration not found!"
    echo "Creating default configuration..."
    mkdir -p "$STREAM_DIR"
    cat > "$ENV_FILE" << 'EOF'
# Stream Configuration
STREAM_RESOLUTION=1280x720
STREAM_FPS=30
STREAM_BITRATE=3000k

# Twitch Configuration
TWITCH_STREAM_KEY=live_YOUR_KEY_HERE
EOF
    echo "✅ Created $ENV_FILE"
    echo "📝 Edit it and add your Twitch stream key from: https://dashboard.twitch.tv/u/username/stream/key"
    exit 1
fi

RESOLUTION=${STREAM_RESOLUTION:-1280x720}
FPS=${STREAM_FPS:-30}
BITRATE=${STREAM_BITRATE:-3000k}

# Validate stream key
if [ -z "$TWITCH_STREAM_KEY" ] || [ "$TWITCH_STREAM_KEY" = "live_YOUR_KEY_HERE" ]; then
    echo "❌ Twitch stream key not configured!"
    echo "📝 Edit $ENV_FILE and add your key:"
    echo "   nano $ENV_FILE"
    echo ""
    echo "Get your key from: https://dashboard.twitch.tv/u/username/stream/key"
    exit 1
fi

echo "🎬 Starting Twitch Stream (VPS Mode)"
echo "===================================="
echo "📺 Resolution: ${RESOLUTION} @ ${FPS}fps"
echo "📤 Bitrate: ${BITRATE}"
echo ""

# Stop any existing streams
echo "🧹 Stopping existing streams..."
pkill -f "ffmpeg.*rtmp" 2>/dev/null
sleep 2

echo "📺 Starting Twitch stream..."
echo ""

# Start streaming with test pattern + text overlay
# TODO: Replace with real bot screenshots once implemented
ffmpeg \
    -f lavfi -i color=c=black:s=${RESOLUTION}:r=${FPS} \
    -f lavfi -i anullsrc=r=44100:cl=mono \
    -vf "drawtext=text='🤖 Minecraft AI Bot Training\n\n🎓 Training RL agent to play Minecraft\n📊 Episode: N/A | Reward: N/A\n📈 Stage: gathering (basic)\n\n⏳ Training 24/7 on VPS\n\nPowered by: PPO + Curriculum Learning':x=(w-text_w)/2:y=(h-text_h)/2:fontsize=24:fontcolor=white:box=1:boxcolor=black@0.5:line_spacing=20" \
    -vcodec libx264 \
    -preset veryfast \
    -b:v ${BITRATE} \
    -maxrate ${BITRATE} \
    -bufsize 6000k \
    -pix_fmt yuv420p \
    -g 50 \
    -c:a aac \
    -b:a 128k \
    -ar 44100 \
    -f flv \
    "rtmp://live.twitch.tv/app/${TWITCH_STREAM_KEY}" \
    > "$STREAM_DIR/logs/ffmpeg.log" 2>&1 &

FFMPEG_PID=$!

echo "✅ Twitch stream started!"
echo "   PID: ${FFMPEG_PID}"
echo ""

# Check if ffmpeg is still running after 5 seconds
sleep 5
if ps -p ${FFMPEG_PID} > /dev/null; then
    echo "✅ Stream is healthy and running!"
    echo ""
    echo "📊 Monitor with:"
    echo "   tail -f $STREAM_DIR/logs/ffmpeg.log"
    echo ""
    echo "🛑 Stop with:"
    echo "   kill ${FFMPEG_PID}"
    echo "   Or: pkill -f 'ffmpeg.*rtmp'"
else
    echo "❌ Stream failed to start!"
    echo "Check logs:"
    tail -20 "$STREAM_DIR/logs/ffmpeg.log"
    exit 1
fi
