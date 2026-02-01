#!/bin/bash
# Script to launch 8 parallel WebSocket bridge servers
# Each server connects to Minecraft with a different bot username

echo "🚀 Launching 8 Parallel RL Bridge Servers..."
echo "=========================================="

# Configuration
MC_HOST="${MC_HOST:-151.241.161.51}"
MC_PORT="${MC_PORT:-25566}"
BASE_PORT="${BASE_PORT:-8765}"
NUM_SERVERS="${NUM_SERVERS:-8}"

echo "📍 Minecraft Server: ${MC_HOST}:${MC_PORT}"
echo "🔌 WebSocket Ports: ${BASE_PORT} - $((BASE_PORT + NUM_SERVERS - 1))"
echo ""

# Function to launch a single bridge server
launch_server() {
    local PORT=$1
    local BOT_NUM=$2

    # Create unique username for each bot
    local BOT_USERNAME="RLAgent_${BOT_NUM}"

    echo "🔌 Starting bridge server ${BOT_NUM} on port ${PORT}..."

    # Set environment variables and launch
    MC_HOST="${MC_HOST}" \
    MC_PORT="${MC_PORT}" \
    MC_USERNAME="${BOT_USERNAME}" \
    WS_PORT="${PORT}" \
    node minecraft-bot/rl-bridge-server.js \
        > logs/bridge-${PORT}.log 2>&1 &

    # Store PID
    echo $! > pids/bridge-${PORT}.pid

    echo "✅ Bridge ${BOT_NUM} started (PID: $(cat pids/bridge-${PORT}.pid))"
}

# Create necessary directories
mkdir -p logs pids

# Kill any existing servers on these ports
echo "🧹 Cleaning up any existing servers..."
for port in $(seq $BASE_PORT $((BASE_PORT + NUM_SERVERS - 1))); do
    if [ -f "pids/bridge-${port}.pid" ]; then
        pid=$(cat pids/bridge-${port}.pid)
        if ps -p $pid > /dev/null 2>&1; then
            echo "  Killing existing server on port ${port} (PID: ${pid})"
            kill $pid
        fi
        rm pids/bridge-${port}.pid
    fi
done

echo ""

# Launch all servers
for i in $(seq 1 $NUM_SERVERS); do
    PORT=$((BASE_PORT + i - 1))
    launch_server $PORT $i
    sleep 1  # Small delay between launches
done

echo ""
echo "=========================================="
echo "✅ All ${NUM_SERVERS} bridge servers launched!"
echo ""
echo "📊 View logs:"
echo "   tail -f logs/bridge-8765.log"
echo ""
echo "🛑 Stop all servers:"
echo "   ./minecraft-bot/stop-parallel-bridges.sh"
echo ""
echo "🔍 Check status:"
echo "   ./minecraft-bot/check-bridges.sh"
echo ""
