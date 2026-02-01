#!/bin/bash
# Stream Minecraft Bot POV to Twitch + TikTok from VPS (Headless)
# This version works WITHOUT OBS/X11 - uses pure ffmpeg

# Configuration
STREAM_DIR="/home/server/minecraft-stream"
ENV_FILE="$STREAM_DIR/.env"

# Load configuration
if [ -f "$ENV_FILE" ]; then
    source "$ENV_FILE"
else
    echo "❌ Configuration file not found: $ENV_FILE"
    echo "Creating default configuration..."
    mkdir -p "$STREAM_DIR"
    cat > "$ENV_FILE" << 'EOF'
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
EOF
    echo "✅ Created $ENV_FILE - Edit it with your stream keys!"
    exit 1
fi

RESOLUTION=${STREAM_RESOLUTION:-1280x720}
FPS=${STREAM_FPS:-30}
BITRATE=${STREAM_BITRATE:-3000k}
AUDIO_BITRATE="128k"

echo "🎬 Starting Minecraft Bot Stream (VPS Mode)"
echo "============================================"
echo "📺 Resolution: ${RESOLUTION} @ ${FPS}fps"
echo "📤 Bitrate: ${BITRATE}"
echo ""

# Kill any existing streams
echo "🧹 Stopping existing streams..."
pkill -f "ffmpeg.*rtmp" 2>/dev/null
sleep 2

# Function to stream to platform
stream_to_platform() {
    local PLATFORM_NAME=$1
    local PLATFORM_KEY=$2
    local ENABLED=$3

    if [ "$ENABLED" != "true" ]; then
        echo "⏭️  Skipping $PLATFORM_NAME (disabled in config)"
        return
    fi

    if [ -z "$PLATFORM_KEY" ] || [ "$PLATFORM_KEY" = "your_${PLATFORM_NAME,,}_stream_key_here" ]; then
        echo "⚠️  $PLATFORM_NAME stream key not configured - skipping"
        return
    fi

    echo "📺 Starting $PLATFORM_NAME stream..."

    # For now, we'll use a test pattern or color since we can't capture X11
    # TODO: Integrate with actual Minecraft bot viewer
    ffmpeg \
        -f lavfi -i color=c=black:s=${RESOLUTION}:r=${FPS} \
        -f lavfi -i anullsrc=r=44100:cl=mono \
        -vf "drawtext=text='${PLATFORM_NAME} - Minecraft Bot Training':x=(w-text_w)/2:y=(h-text_h)/2:fontsize=32:fontcolor=white:box=1:boxcolor=black@0.5" \
        -vcodec libx264 \
        -preset veryfast \
        -b:v ${BITRATE} \
        -maxrate ${BITRATE} \
        -bufsize 6000k \
        -pix_fmt yuv420p \
        -g 50 \
        -c:a aac \
        -b:a ${AUDIO_BITRATE} \
        -ar 44100 \
        -f flv \
        "${PLATFORM_KEY}" \
        > /dev/null 2>&1 &

    local PID=$!
    echo "✅ $PLATFORM_NAME streaming (PID: ${PID})"

    # Wait a bit to check if ffmpeg started successfully
    sleep 3
    if ps -p ${PID} > /dev/null; then
        echo "✅ $PLATFORM_NAME stream is active"
    else
        echo "❌ $PLATFORM_NAME stream failed to start"
    fi
}

# Start streams
if [ "$TWITCH_ENABLED" = "true" ]; then
    stream_to_platform "Twitch" "rtmp://live.twitch.tv/app/${TWITCH_STREAM_KEY}" "true"
fi

if [ "$TIKTOK_ENABLED" = "true" ]; then
    stream_to_platform "TikTok" "rtmp://push.tiktok.com/live/${TIKTOK_STREAM_KEY}" "true"
fi

echo ""
echo "🎉 Stream started!"
echo ""
echo "📊 Check status:"
echo "   ps aux | grep ffmpeg"
echo ""
echo "🛑 To stop:"
echo "   pkill -f 'ffmpeg.*rtmp'"
echo ""
