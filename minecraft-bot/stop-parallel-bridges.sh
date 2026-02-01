#!/bin/bash
# Script to stop all parallel bridge servers

echo "🛑 Stopping all Parallel RL Bridge Servers..."
echo "=========================================="

BASE_PORT="${BASE_PORT:-8765}"
NUM_SERVERS="${NUM_SERVERS:-8}"

if [ ! -d "pids" ]; then
    echo "⚠️  No PID directory found"
    echo "   Servers may not be running"
    exit 0
fi

stopped=0
for port in $(seq $BASE_PORT $((BASE_PORT + NUM_SERVERS - 1))); do
    if [ -f "pids/bridge-${port}.pid" ]; then
        pid=$(cat pids/bridge-${port}.pid)

        if ps -p $pid > /dev/null 2>&1; then
            echo "  🛑 Stopping bridge on port ${port} (PID: ${pid})"
            kill $pid
            stopped=$((stopped + 1))
        else
            echo "  ⚠️  Bridge on port ${port} already stopped (PID: ${pid})"
        fi

        rm pids/bridge-${port}.pid
    fi
done

echo ""
echo "=========================================="
if [ $stopped -eq 0 ]; then
    echo "ℹ️  No servers were running"
else
    echo "✅ Stopped ${stopped} server(s)"
fi
echo ""
