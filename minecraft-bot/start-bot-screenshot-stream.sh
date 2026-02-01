#!/bin/bash
# Stream REAL Minecraft Bot POV using screenshots
# This captures actual bot gameplay and streams to platforms

# Auto-detect home directory
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

echo "🎬 Streaming Real Minecraft Bot POV"
echo "===================================="
echo "📺 Resolution: ${RESOLUTION} @ ${FPS}fps"
echo ""

# Create screenshot directory
mkdir -p "$SCREENSHOT_DIR"

# Check if bot viewer is running and capturing screenshots
if ! pgrep -f "stream-bot-viewer" > /dev/null; then
    echo "❌ Bot viewer not running!"
    echo "Start it first:"
    echo "  cd ~/MinecraftAI/minecraft-bot"
    echo "  node stream-bot-viewer.js &"
    exit 1
fi

echo "✅ Bot viewer is running"
echo "⏳ Waiting for screenshots..."
sleep 5

# Check for screenshots
SCREENSHOT_COUNT=$(ls -1 "$SCREENSHOT_DIR"/frame_*.png 2>/dev/null | wc -l)
if [ "$SCREENSHOT_COUNT" -eq 0 ]; then
    echo "⚠️  No screenshots found yet, starting with test pattern..."
    USE_TEST_PATTERN=true
else
    echo "✅ Found $SCREENSHOT_COUNT screenshots"
    USE_TEST_PATTERN=false
fi

# Function to stream screenshots
stream_screenshots() {
    local PLATFORM=$1
    local RTMP_URL=$2

    echo "📺 Streaming to $PLATFORM..."

    # Use ffmpeg to stream screenshots as video
    # This creates a video stream from sequential PNG files
    ffmpeg \
        -framerate ${FPS} \
        -i "$SCREENSHOT_DIR/frame_%06d.png" \
        -vcodec libx264 \
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
        "${RTMP_URL}" \
        > /dev/null 2>&1 &

    local PID=$!
    echo "✅ $PLATFORM streaming (PID: ${PID})"

    # Monitor process
    sleep 5
    if ps -p ${PID} > /dev/null; then
        echo "✅ $PLATFORM stream is healthy"
    else
        echo "❌ $PLATFORM stream failed"
        return 1
    fi
}

# Function to stream test pattern (fallback)
stream_test_pattern() {
    local PLATFORM=$1
    local RTMP_URL=$2

    echo "📺 Streaming test pattern to $PLATFORM..."

    TEXT="${PLATFORM} - Minecraft Bot Training - Bot is learning - Real POV coming soon"

    ffmpeg \
        -f lavfi -i color=c=black:s=${RESOLUTION}:r=${FPS} \
        -f lavfi -i anullsrc=r=44100:cl=mono \
        -vf "drawtext=text=${TEXT}:x=(w-text_w)/2:y=(h-text_h)/2:fontsize=32:fontcolor=white:box=1:boxcolor=black@0.5" \
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
        "${RTMP_URL}" \
        > /dev/null 2>&1 &

    local PID=$!
    echo "✅ $PLATFORM streaming (PID: ${PID})"
}

# Kill existing streams
pkill -f "ffmpeg.*rtmp" 2>/dev/null
sleep 2

# Start streams
if [ "$USE_TEST_PATTERN" = true ]; then
    echo "⚠️  Using test pattern (no screenshots yet)"
    if [ "$TIKTOK_ENABLED" = "true" ] && [ -n "$TIKTOK_STREAM_KEY" ]; then
        stream_test_pattern "TikTok" "rtmp://push.tiktok.com/live/${TIKTOK_STREAM_KEY}"
    fi
    if [ "$TWITCH_ENABLED" = "true" ] && [ -n "$TWITCH_STREAM_KEY" ]; then
        stream_test_pattern "Twitch" "rtmp://live.twitch.tv/app/${TWITCH_STREAM_KEY}"
    fi
else
    echo "✅ Using real screenshots"
    if [ "$TIKTOK_ENABLED" = "true" ] && [ -n "$TIKTOK_STREAM_KEY" ]; then
        stream_screenshots "TikTok" "rtmp://push.tiktok.com/live/${TIKTOK_STREAM_KEY}"
    fi
    if [ "$TWITCH_ENABLED" = "true" ] && [ -n "$TWITCH_STREAM_KEY" ]; then
        stream_screenshots "Twitch" "rtmp://live.twitch.tv/app/${TWITCH_STREAM_KEY}"
    fi
fi

echo ""
echo "🎉 Stream started!"
echo ""
echo "📊 Monitor with:"
echo "   watch -n 2 'ps aux | grep ffmpeg'"
echo ""
echo "📁 Screenshots: $SCREENSHOT_DIR"
echo ""
echo "🛑 Stop with:"
echo "   pkill -f 'ffmpeg.*rtmp'"
echo ""
