#!/bin/bash
###############################################################################
# Start Minecraft RL AI System
# Launches the complete system: Bot + Bridge + RL Training
###############################################################################

set -e

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
RED='\033[0;31m'
NC='\033[0m'

log() {
    echo -e "${GREEN}[$(date +'%H:%M:%S')]${NC} $1"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1"
    exit 1
}

# Get project directory
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_DIR"

log "🚀 Starting Minecraft RL AI System..."
echo ""

# Check if .env exists
if [ ! -f "$PROJECT_DIR/.env" ]; then
    error ".env file not found. Please create it with MC_HOST, MC_PORT, MC_USERNAME"
fi

# Load environment variables
export $(grep -v '^#' "$PROJECT_DIR/.env" | xargs)

# Check required variables
: "${MC_HOST:?MC_HOST not set in .env}"
: "${MC_PORT:?MC_PORT not set in .env}"
: "${MC_USERNAME:?MC_USERNAME not set in .env}"

log "Configuration:"
echo "   MC Server: $MC_HOST:$MC_PORT"
echo "   Username: $MC_USERNAME"
echo ""

# Create data directories
mkdir -p llm/data/memories
mkdir -p llm/data/models
mkdir -p llm/data/logs
mkdir -p llm/data/logs/tensorboard

###############################################################################
# Start Bridge Server with Bot
###############################################################################

log "🌉 Starting Bridge Server with Minecraft Bot..."

# Check if bridge is already running
if [ -f "llm/bridge.pid" ]; then
    BRIDGE_PID=$(cat llm/bridge.pid)
    if ps -p $BRIDGE_PID > /dev/null 2>&1; then
        log "Bridge already running (PID: $BRIDGE_PID)"
    else
        rm llm/bridge.pid
    fi
fi

# Start bridge integration
cd llm/node
node main-bridge-integration.js > "$PROJECT_DIR/llm/data/logs/bridge.log" 2>&1 &
BRIDGE_PID=$!
echo $BRIDGE_PID > "$PROJECT_DIR/llm/bridge.pid"
cd "$PROJECT_DIR"

log "✅ Bridge started (PID: $BRIDGE_PID)"

# Wait for bridge to be ready
log "⏳ Waiting for bridge to initialize..."
sleep 5

# Check if bridge is running
if ! ps -p $BRIDGE_PID > /dev/null; then
    error "Bridge failed to start. Check llm/data/logs/bridge.log"
fi

log "✅ Bridge is ready!"
echo ""

###############################################################################
# Start TensorBoard (optional)
###############################################################################

log "📊 Starting TensorBoard..."

tensorboard --logdir="$PROJECT_DIR/llm/data/logs/tensorboard" \
    --port=6006 \
    --host=0.0.0.0 \
    > "$PROJECT_DIR/llm/data/logs/tensorboard.log" 2>&1 &

TB_PID=$!
echo $TB_PID > "$PROJECT_DIR/llm/tensorboard.pid"

log "✅ TensorBoard started (PID: $TB_PID)"
log "   URL: http://localhost:6006"
echo ""

###############################################################################
# Start RL Training
###############################################################################

log "🤖 Starting RL Training..."

# Activate virtual environment
if [ ! -d "$PROJECT_DIR/venv" ]; then
    log "Creating Python virtual environment..."
    python3 -m venv "$PROJECT_DIR/venv"
fi

source "$PROJECT_DIR/venv/bin/activate"

# Install dependencies if needed
if ! python -c "import gymnasium" 2>/dev/null; then
    log "Installing Python dependencies..."
    pip install -r "$PROJECT_DIR/llm/python/requirements.txt" \
        > "$PROJECT_DIR/llm/data/logs/install.log" 2>&1
fi

# Start training
cd "$PROJECT_DIR/llm/python"

# Parse arguments
STEPS=${1:-100000000}

python training/real_minecraft_trainer.py \
    --steps $STEPS \
    --bridge-host localhost \
    --bridge-port 8765 \
    > "$PROJECT_DIR/llm/data/logs/training.log" 2>&1 &

TRAIN_PID=$!
echo $TRAIN_PID > "$PROJECT_DIR/llm/training.pid"

cd "$PROJECT_DIR"

log "✅ RL Training started (PID: $TRAIN_PID)"
echo ""

###############################################################################
# Ready!
###############################################################################

echo -e "${CYAN}╔═══════════════════════════════════════════════════════════════╗${NC}"
echo -e "${CYAN}║                                                                   ║${NC}"
echo -e "${CYAN}║     🤖 MINECRAFT RL AI - NOW PLAYING & LEARNING!                 ║${NC}"
echo -e "${CYAN}║                                                                   ║${NC}"
echo -e "${CYAN}╚═══════════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${GREEN}✅ All systems running!${NC}"
echo ""
echo -e "${BLUE}📊 Monitoring:${NC}"
echo -e "  ${YELLOW}./llm/monitor.sh${NC}          (one-time status)"
echo -e "  ${YELLOW}./llm/monitor.sh --live${NC}     (live monitoring)"
echo ""
echo -e "${BLUE}📈 TensorBoard:${NC}"
echo -e "  ${CYAN}http://localhost:6006${NC}"
echo ""
echo -e "${BLUE}📋 Logs:${NC}"
echo -e "  ${YELLOW}tail -f llm/data/logs/training.log${NC}"
echo -e "  ${YELLOW}tail -f llm/data/logs/bridge.log${NC}"
echo ""
echo -e "${BLUE}🛑 Stop all:${NC}"
echo -e "  ${YELLOW}./llm/start-rl-minecraft.sh stop${NC}"
echo ""

# Wait a bit to check if training started successfully
sleep 3

if ! ps -p $TRAIN_PID > /dev/null; then
    error "Training failed to start. Check llm/data/logs/training.log"
fi

log "✅ System is running! The AI is now playing and learning!"
echo ""

# If command is "stop", stop everything
if [ "$1" == "stop" ]; then
    log "🛑 Stopping all services..."

    if [ -f "llm/training.pid" ]; then
        kill $(cat llm/training.pid) 2>/dev/null || true
        rm llm/training.pid
    fi

    if [ -f "llm/bridge.pid" ]; then
        kill $(cat llm/bridge.pid) 2>/dev/null || true
        rm llm/bridge.pid
    fi

    if [ -f "llm/tensorboard.pid" ]; then
        kill $(cat llm/tensorboard.pid) 2>/dev/null || true
        rm llm/tensorboard.pid
    fi

    log "✅ All services stopped"
    exit 0
fi

# Keep script running
log "Press Ctrl+C to stop all services..."
trap "./llm/start-rl-minecraft.sh stop; exit 0" INT TERM

while true; do
    sleep 10

    # Check if processes are still running
    if ! ps -p $BRIDGE_PID > /dev/null; then
        error "Bridge process died!"
    fi

    if ! ps -p $TRAIN_PID > /dev/null; then
        log "Training process finished"
        break
    fi
done

log "🎉 Training complete!"
