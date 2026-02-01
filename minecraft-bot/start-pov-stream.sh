#!/bin/bash
# Stream REAL Minecraft Bot POV to Twitch using screenshots

STREAM_DIR="$HOME/minecraft-stream"
ENV_FILE="$STREAM_DIR/.env"
SCREENSHOT_DIR="$STREAM_DIR/screenshots"

# Load configuration
if [ -f "$ENV_FILE" ]; then
    source "$ENV_FILE"
else
    echo "❌ Configuration not found: $ENV_FILE"
    exit 1
fi

RESOLUTION=${STREAM_RESOLUTION:-1280x720}
FPS=${STREAM_FPS:-30}
BITRATE=${STREAM_BITRATE:-3000k}

echo "🎬 Streaming Real Minecraft Bot POV to Twitch"
echo "============================================"
echo "📺 Resolution: ${RESOLUTION} @ ${FPS}fps"
echo "📸 Screenshot Dir: ${SCREENSHOT_DIR}"
echo "📤 Bitrate: ${BITRATE}"
echo ""

# Validate stream key
if [ -z "$TWITCH_STREAM_KEY" ] || [ "$TWITCH_STREAM_KEY" = "live_VOTRE_CLE_ICI" ]; then
    echo "❌ Twitch stream key not configured!"
    echo "📝 Edit $ENV_FILE and add your key"
    exit 1
fi

# Check if screenshots directory exists
if [ ! -d "$SCREENSHOT_DIR" ]; then
    echo "❌ Screenshot directory not found: $SCREENSHOT_DIR"
    echo "💡 Make sure the POV bot server is running"
    exit 1
fi

# Check for screenshots
SCREENSHOT_COUNT=$(ls -1 "$SCREENSHOT_DIR"/frame_*.jpg 2>/dev/null | wc -l)
if [ "$SCREENSHOT_COUNT" -eq 0 ]; then
    echo "⚠️  No screenshots found yet"
    echo "💡 The bot server needs to capture screenshots first"
    echo "💡 Start the POV server: node rl-bridge-pov-server.js"
    echo ""
    echo "⏳ Waiting for screenshots (will start streaming when available)..."
fi

# Stop any existing streams
echo "🧹 Stopping existing streams..."
pkill -f "ffmpeg.*rtmp" 2>/dev/null
sleep 2

echo "📺 Starting Twitch stream from screenshots..."
echo ""

# Stream screenshots to Twitch
# Uses ffmpeg to read sequential JPEG files and stream to Twitch
ffmpeg \
    -framerate ${FPS} \
    -i "$SCREENSHOT_DIR/frame_%06d.jpg" \
    -c:v libx264 \
    -preset veryfast \
    -b:v ${BITRATE} \
    -maxrate ${BITRATE} \
    -bufsize 6000k \
    -pix_fmt yuv420p \
    -g 50 \
    -f lavfi -i anullsrc=r=44100:cl=mono \
    -c:a aac \
    -b:a 128k \
    -ar 44100 \
    -f flv \
    "rtmp://live.twitch.tv/app/${TWITCH_STREAM_KEY}" \
    > "$STREAM_DIR/logs/pov-stream.log" 2>&1 &

FFMPEG_PID=$!

echo "✅ Twitch stream started!"
echo "   PID: ${FFMPEG_PID}"
echo ""

# Wait and check if stream is healthy
sleep 5

if ps -p ${FFMPEG_PID} > /dev/null 2>&1; then
    echo "✅ Stream is running!"
    echo ""
    echo "📊 Monitor with:"
    echo "   tail -f $STREAM_DIR/logs/pov-stream.log"
    echo ""
    echo "📸 Screenshot count:"
    echo "   ls -1 $SCREENSHOT_DIR/frame_*.jpg | wc -l"
    echo ""
    echo "🛑 Stop with:"
    echo "   kill ${FFMPEG_PID}"
    echo "   Or: pkill -f 'ffmpeg.*rtmp'"
else
    echo "❌ Stream failed to start!"
    echo ""
    echo "Check logs:"
    tail -30 "$STREAM_DIR/logs/pov-stream.log"
    exit 1
fi
