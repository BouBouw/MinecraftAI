#!/bin/bash
# Script to check status of parallel bridge servers

echo "🔍 Checking Parallel RL Bridge Servers Status..."
echo "=============================================="

BASE_PORT="${BASE_PORT:-8765}"
NUM_SERVERS="${NUM_SERVERS:-8}"

if [ ! -d "pids" ]; then
    echo "⚠️  No PID directory found"
    echo "   Servers have not been started"
    exit 0
fi

running=0
stopped=0

for port in $(seq $BASE_PORT $((BASE_PORT + NUM_SERVERS - 1))); do
    if [ -f "pids/bridge-${port}.pid" ]; then
        pid=$(cat pids/bridge-${port}.pid)

        if ps -p $pid > /dev/null 2>&1; then
            echo "  ✅ Port ${port}: RUNNING (PID: ${pid})"
            running=$((running + 1))
        else
            echo "  ❌ Port ${port}: STOPPED (stale PID: ${pid})"
            stopped=$((stopped + 1))
        fi
    else
        echo "  ⚪ Port ${port}: NOT STARTED"
        stopped=$((stopped + 1))
    fi
done

echo ""
echo "=============================================="
echo "📊 Summary:"
echo "   Running: ${running}/${NUM_SERVERS}"
echo "   Stopped: ${stopped}/${NUM_SERVERS}"
echo ""

if [ $running -eq $NUM_SERVERS ]; then
    echo "✅ All servers are running!"
    echo ""
    echo "📊 View logs:"
    for port in $(seq $BASE_PORT $((BASE_PORT + NUM_SERVERS - 1))); do
        if [ -f "logs/bridge-${port}.log" ]; then
            echo "   tail -f logs/bridge-${port}.log  # Port ${port}"
        fi
    done | head -3
    echo "   ..."
else
    echo "⚠️  Some servers are not running"
    echo "   Start them with: ./minecraft-bot/launch-parallel-bridges.sh"
fi
echo ""
