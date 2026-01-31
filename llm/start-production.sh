#!/bin/bash
###############################################################################
# Minecraft RL AI - Production Launcher for OVH Server
# Optimized for 24/7 autonomous learning
###############################################################################

set -e

# Configuration
PROJECT_DIR="/root/MinecraftAI"
PYTHON_DIR="$PROJECT_DIR/llm/python"
NODE_DIR="$PROJECT_DIR/ai-coordinator"
LOG_DIR="$PROJECT_DIR/llm/data/logs"
VENV_DIR="$PROJECT_DIR/venv"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

log() {
    echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')]${NC} $1"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

###############################################################################
# System Preparation
###############################################################################

prepare_system() {
    log "🖥️  Preparing system for 24/7 AI training..."

    # Set CPU governor to performance mode
    if [ -w /sys/devices/system/cpu/cpu0/cpufreq/scaling_governor ]; then
        echo performance | tee /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor > /dev/null
        log "✅ CPU governor set to performance mode"
    fi

    # Increase file limits
    ulimit -n 65536
    log "✅ File descriptors limit increased"

    # Disable swap (better for RL training)
    if command -v swapoff &> /dev/null; then
        sudo swapoff -a || warn "Could not disable swap"
    fi

    # Configure sysctl for optimal performance
    sudo sysctl -w net.core.rmem_max=134217728 > /dev/null
    sudo sysctl -w net.core.wmem_max=134217728 > /dev/null
    log "✅ Network buffers optimized"
}

###############################################################################
# Environment Setup
###############################################################################

setup_environment() {
    log "📦 Setting up Python environment..."

    if [ ! -d "$VENV_DIR" ]; then
        python3 -m venv "$VENV_DIR"
        log "✅ Virtual environment created"
    fi

    source "$VENV_DIR/bin/activate"

    # Upgrade pip
    pip install --upgrade pip setuptools wheel > /dev/null 2>&1

    # Install dependencies
    log "📚 Installing Python packages..."
    pip install -r "$PYTHON_DIR/requirements.txt" > "$LOG_DIR/install.log" 2>&1

    log "✅ Python packages installed"
}

###############################################################################
# Start Services
###############################################################################

start_bridge_server() {
    log "🌉 Starting Bridge Server..."

    cd "$NODE_DIR"

    # Start bridge server in background with logging
    nohup node node/llm/node/bridge-server.js \
        > "$LOG_DIR/bridge.log" 2>&1 &

    BRIDGE_PID=$!
    echo $BRIDGE_PID > "$PROJECT_DIR/llm/bridge.pid"

    # Wait for bridge to start
    sleep 5

    if ps -p $BRIDGE_PID > /dev/null; then
        log "✅ Bridge Server started (PID: $BRIDGE_PID)"
    else
        error "Failed to start Bridge Server"
        return 1
    fi
}

start_ai_coordinator() {
    log "🤖 Starting AI Coordinator..."

    cd "$NODE_DIR"

    # Check if already running
    if pgrep -f "node.*server.js" > /dev/null; then
        warn "AI Coordinator already running"
        return 0
    fi

    # Start AI coordinator in background
    nohup npm start \
        > "$LOG_DIR/coordinator.log" 2>&1 &

    COORDINATOR_PID=$!
    echo $COORDINATOR_PID > "$PROJECT_DIR/ai-coordinator.pid"

    # Wait for coordinator to start
    sleep 5

    if ps -p $COORDINATOR_PID > /dev/null; then
        log "✅ AI Coordinator started (PID: $COORDINATOR_PID)"
    else
        error "Failed to start AI Coordinator"
        return 1
    fi
}

start_rl_training() {
    log "🧠 Starting RL Training..."

    cd "$PYTHON_DIR"

    # Activate virtual environment
    source "$VENV_DIR/bin/activate"

    # Configure for multi-core training
    export OMP_NUM_THREADS=16
    export MKL_NUM_THREADS=16
    export OPENBLAS_NUM_THREADS=16

    # Training parameters
    TOTAL_STEPS=${TOTAL_STEPS:=100000000}  # 100M steps (~10 days)
    BATCH_SIZE=${BATCH_SIZE:=256}
    CHECKPOINT_DIR="$PROJECT_DIR/llm/data/models"

    mkdir -p "$CHECKPOINT_DIR"
    mkdir -p "$LOG_DIR"

    log "🎯 Training parameters:"
    log "   Total steps: $TOTAL_STEPS"
    log "   Batch size: $BATCH_SIZE"
    log "   CPU cores: 16"
    log "   Checkpoint dir: $CHECKPOINT_DIR"

    # Start training in background with auto-restart
    nohup python train.py \
        --steps $TOTAL_STEPS \
        --checkpoint-dir "$CHECKPOINT_DIR" \
        > "$LOG_DIR/training.log" 2>&1 &

    TRAIN_PID=$!
    echo $TRAIN_PID > "$PROJECT_DIR/llm/training.pid"

    # Wait a bit to check if training started successfully
    sleep 10

    if ps -p $TRAIN_PID > /dev/null; then
        log "✅ RL Training started (PID: $TRAIN_PID)"
    else
        error "Failed to start RL Training - check $LOG_DIR/training.log"
        return 1
    fi
}

###############################################################################
# Monitoring
###############################################################################

start_tensorboard() {
    log "📊 Starting TensorBoard..."

    cd "$PROJECT_DIR"

    source "$VENV_DIR/bin/activate"

    # Start TensorBoard in background
    nohup tensorboard --logdir="$PROJECT_DIR/llm/data/logs/tensorboard" \
        --port 6006 \
        --host 0.0.0.0 \
        > "$LOG_DIR/tensorboard.log" 2>&1 &

    TB_PID=$!
    echo $TB_PID > "$PROJECT_DIR/llm/tensorboard.pid"

    sleep 3

    if ps -p $TB_PID > /dev/null; then
        log "✅ TensorBoard started on http://0.0.0.0:6006 (PID: $TB_PID)"
    else
        warn "TensorBoard failed to start"
    fi
}

show_status() {
    log "📈 System Status:"
    echo ""

    # Check processes
    if [ -f "$PROJECT_DIR/llm/bridge.pid" ]; then
        BRIDGE_PID=$(cat "$PROJECT_DIR/llm/bridge.pid")
        if ps -p $BRIDGE_PID > /dev/null; then
            echo -e "  ✅ Bridge Server: ${GREEN}RUNNING${NC} (PID: $BRIDGE_PID)"
        else
            echo -e "  ❌ Bridge Server: ${RED}STOPPED${NC}"
        fi
    fi

    if [ -f "$PROJECT_DIR/ai-coordinator.pid" ]; then
        COORD_PID=$(cat "$PROJECT_DIR/ai-coordinator.pid")
        if ps -p $COORD_PID > /dev/null; then
            echo -e "  ✅ AI Coordinator: ${GREEN}RUNNING${NC} (PID: $COORD_PID)"
        else
            echo -e "  ❌ AI Coordinator: ${RED}STOPPED${NC}"
        fi
    fi

    if [ -f "$PROJECT_DIR/llm/training.pid" ]; then
        TRAIN_PID=$(cat "$PROJECT_DIR/llm/training.pid")
        if ps -p $TRAIN_PID > /dev/null; then
            echo -e "  ✅ RL Training: ${GREEN}RUNNING${NC} (PID: $TRAIN_PID)"

            # Show training progress from logs
            if [ -f "$LOG_DIR/training.log" ]; then
                LAST_REWARD=$(tail -20 "$LOG_DIR/training.log" | grep "reward=" | tail -1 | grep -oP 'reward=\K[0-9.-]+')
                if [ ! -z "$LAST_REWARD" ]; then
                    echo -e "     Last reward: ${BLUE}$LAST_REWARD${NC}"
                fi
            fi
        else
            echo -e "  ❌ RL Training: ${RED}STOPPED${NC}"
        fi
    fi

    if [ -f "$PROJECT_DIR/llm/tensorboard.pid" ]; then
        TB_PID=$(cat "$PROJECT_DIR/llm/tensorboard.pid")
        if ps -p $TB_PID > /dev/null; then
            echo -e "  ✅ TensorBoard: ${GREEN}RUNNING${NC} (PID: $TB_PID)"
        else
            echo -e "  ❌ TensorBoard: ${RED}STOPPED${NC}"
        fi
    fi

    echo ""
    log "💾 Disk Usage:"
    df -h "$PROJECT_DIR" | tail -1

    log "🧠 Memory Usage:"
    free -h | grep Mem:
}

###############################################################################
# Stop Services
###############################################################################

stop_all() {
    log "🛑 Stopping all services..."

    # Stop TensorBoard
    if [ -f "$PROJECT_DIR/llm/tensorboard.pid" ]; then
        TB_PID=$(cat "$PROJECT_DIR/llm/tensorboard.pid")
        if ps -p $TB_PID > /dev/null; then
            kill $TB_PID
            log "✅ TensorBoard stopped"
        fi
        rm -f "$PROJECT_DIR/llm/tensorboard.pid"
    fi

    # Stop training
    if [ -f "$PROJECT_DIR/llm/training.pid" ]; then
        TRAIN_PID=$(cat "$PROJECT_DIR/llm/training.pid")
        if ps -p $TRAIN_PID > /dev/null; then
            kill -INT $TRAIN_PID
            sleep 5
            if ps -p $TRAIN_PID > /dev/null; then
                kill -9 $TRAIN_PID
            fi
            log "✅ RL Training stopped"
        fi
        rm -f "$PROJECT_DIR/llm/training.pid"
    fi

    # Stop AI coordinator
    if [ -f "$PROJECT_DIR/ai-coordinator.pid" ]; then
        COORD_PID=$(cat "$PROJECT_DIR/ai-coordinator.pid")
        if ps -p $COORD_PID > /dev/null; then
            kill $COORD_PID
            log "✅ AI Coordinator stopped"
        fi
        rm -f "$PROJECT_DIR/ai-coordinator.pid"
    fi

    # Stop bridge server
    if [ -f "$PROJECT_DIR/llm/bridge.pid" ]; then
        BRIDGE_PID=$(cat "$PROJECT_DIR/llm/bridge.pid")
        if ps -p $BRIDGE_PID > /dev/null; then
            kill $BRIDGE_PID
            log "✅ Bridge Server stopped"
        fi
        rm -f "$PROJECT_DIR/llm/bridge.pid"
    fi

    log "✅ All services stopped"
}

###############################################################################
# Auto-restart on crash
###############################################################################

auto_restart_training() {
    log "🔄 Starting training with auto-restart..."

    cd "$PYTHON_DIR"
    source "$VENV_DIR/bin/activate"

    MAX_RESTARTS=10
    RESTART_DELAY=30
    restart_count=0

    while [ $restart_count -lt $MAX_RESTARTS ]; do
        # Start training
        python train.py \
            --steps ${TOTAL_STEPS:=100000000} \
            --checkpoint-dir "$PROJECT_DIR/llm/data/models" \
            >> "$LOG_DIR/training.log" 2>&1

        EXIT_CODE=$?

        if [ $EXIT_CODE -eq 0 ]; then
            log "✅ Training completed successfully!"
            break
        elif [ $EXIT_CODE -eq 130 ]; then
            log "⚠️ Training interrupted by user"
            break
        else
            restart_count=$((restart_count + 1))
            warn "Training crashed (exit code: $EXIT_CODE), restarting in ${RESTART_DELAY}s... (attempt $restart_count/$MAX_RESTARTS)"

            # Save crash info
            echo "[$(date)] Crash detected, exit code: $EXIT_CODE, restart: $restart_count" >> "$LOG_DIR/crashes.log"

            sleep $RESTART_DELAY
        fi
    done

    if [ $restart_count -ge $MAX_RESTARTS ]; then
        error "Too many crashes, giving up"
        return 1
    fi
}

###############################################################################
# Main Menu
###############################################################################

show_usage() {
    cat << EOF
${BLUE}╔═══════════════════════════════════════════════════════════════╗
║         Minecraft RL AI - Production Launcher                  ║
║         Optimized for OVH 24/7 Autonomous Learning           ║
╚═══════════════════════════════════════════════════════════════╝${NC}

Usage: $0 <command> [options]

Commands:
    start         Start all services for 24/7 training
    stop          Stop all services
    restart       Restart all services
    status        Show status of all services
    train         Start RL training only
    monitor       Start TensorBoard monitoring
    logs          Show recent logs
    prepare       Prepare system for production
    auto-start    Start training with auto-restart on crash

Options:
    --steps N     Total training steps (default: 100M)
    --batch N     Batch size (default: 256)
    --no-tb       Don't start TensorBoard

Examples:
    $0 start               Start everything
    $0 start --steps 50M   Start with 50M steps
    $0 status              Check status
    $0 logs                View logs
    $0 stop                Stop all services
    $0 auto-start          Start with auto-restart on crashes

For monitoring:
    - TensorBoard: http://localhost:6006
    - Logs: tail -f llm/data/logs/training.log
EOF
}

# Parse command
case "${1:-}" in
    prepare)
        prepare_system
        setup_environment
        ;;

    start)
        prepare_system
        setup_environment
        start_bridge_server
        start_ai_coordinator
        start_rl_training
        if [ "${2:-}" != "--no-tb" ]; then
            start_tensorboard
        fi
        echo ""
        log "🚀 All services started!"
        log "📊 Monitor with: $0 status"
        log "📊 TensorBoard: http://localhost:6006"
        ;;

    stop)
        stop_all
        ;;

    restart)
        stop_all
        sleep 3
        exec $0 start
        ;;

    status)
        show_status
        ;;

    train)
        prepare_system
        setup_environment
        start_rl_training
        ;;

    monitor)
        start_tensorboard
        ;;

    logs)
        log "📋 Recent logs (last 50 lines):"
        if [ -f "$LOG_DIR/training.log" ]; then
            tail -50 "$LOG_DIR/training.log"
        else
            warn "No training log found"
        fi
        ;;

    auto-start)
        prepare_system
        setup_environment
        start_bridge_server
        start_ai_coordinator
        if [ "${2:-}" != "--no-tb" ]; then
            start_tensorboard
        fi
        auto_restart_training
        ;;

    *)
        show_usage
        exit 1
        ;;
esac

exit 0
