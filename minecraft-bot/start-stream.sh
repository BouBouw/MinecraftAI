#!/bin/bash
# Stream Minecraft Bot POV to Twitch + TikTok simultaneously

# Configuration
TWITCH_RTMP="rtmp://live.twitch.tv/app/YOUR_TWITCH_STREAM_KEY"
TIKTOK_RTMP="rtmp://push.tiktok.com/live/YOUR_TIKTOK_STREAM_KEY"
RESOLUTION="1920x1080"
FPS="30"
BITRATE="4500k"  # 4.5 Mbps pour qualité 1080p
AUDIO_BITRATE="128k"

# Display virtuel pour Xvfb
export DISPLAY=:99

echo "🎬 Starting Minecraft Bot Stream..."
echo "📺 Resolution: ${RESOLUTION} @ ${FPS}fps"
echo "🔴 Streaming to: Twitch + TikTok"
echo ""

# Vérifier que Xvfb tourne
if ! pgrep -x "Xvfb" > /dev/null; then
    echo "❌ Xvfb not running. Start it first:"
    echo "   Xvfb :99 -screen 0 ${RESOLUTION}x24 &"
    exit 1
fi

# Fonction pour streamer vers Twitch
stream_twitch() {
    ffmpeg \
        -f x11grab \
        -s ${RESOLUTION} \
        -r ${FPS} \
        -i ${DISPLAY} \
        -f pulse -i default \
        -vcodec libx264 \
        -preset veryfast \
        -b:v ${BITRATE} \
        -maxrate ${BITRATE} \
        -bufsize 9000k \
        -pix_fmt yuv420p \
        -g 50 \
        -c:a aac \
        -b:a ${AUDIO_BITRATE} \
        -ar 44100 \
        -f flv \
        "${TWITCH_RTMP}" \
        > /dev/null 2>&1 &
    TWITCH_PID=$!
    echo "✅ Twitch streaming (PID: ${TWITCH_PID})"
}

# Fonction pour streamer vers TikTok
stream_tiktok() {
    ffmpeg \
        -f x11grab \
        -s ${RESOLUTION} \
        -r ${FPS} \
        -i ${DISPLAY} \
        -f pulse -i default \
        -vcodec libx264 \
        -preset veryfast \
        -b:v ${BITRATE} \
        -maxrate ${BITRATE} \
        -bufsize 9000k \
        -pix_fmt yuv420p \
        -g 50 \
        -c:a aac \
        -b:a ${AUDIO_BITRATE} \
        -ar 44100 \
        -f flv \
        "${TIKTOK_RTMP}" \
        > /dev/null 2>&1 &
    TIKTOK_PID=$!
    echo "✅ TikTok streaming (PID: ${TIKTOK_PID})"
}

# Démarrer les deux streams
stream_twitch
sleep 2
stream_tiktok

echo ""
echo "🎉 Stream actif !"
echo "Twitch PID: ${TWITCH_PID}"
echo "TikTok PID: ${TIKTOK_PID}"
echo ""
echo "Pour arrêter: kill ${TWITCH_PID} ${TIKTOK_PID}"
echo "Ou: pkill -f ffmpeg"
