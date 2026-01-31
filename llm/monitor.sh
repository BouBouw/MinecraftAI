#!/bin/bash
###############################################################################
# Minecraft RL AI - Monitoring Script
# Real-time monitoring for 24/7 training on OVH server
###############################################################################

set -e

# Configuration
PROJECT_DIR="/root/MinecraftAI"
LOG_DIR="$PROJECT_DIR/llm/data/logs"
MODEL_DIR="$PROJECT_DIR/llm/data/models"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

# Get current timestamp
timestamp() {
    date '+%Y-%m-%d %H:%M:%S'
}

print_header() {
    clear
    echo -e "${CYAN}╔═══════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${CYAN}║         Minecraft RL AI - Real-time Monitor                     ║${NC}"
    echo -e "${CYAN}║         $(timestamp)                                   ║${NC}"
    echo -e "${CYAN}╚═══════════════════════════════════════════════════════════════╝${NC}"
    echo ""
}

check_process() {
    local name=$1
    local pidfile=$2

    if [ -f "$pidfile" ]; then
        local pid=$(cat "$pidfile")
        if ps -p $pid > /dev/null; then
            echo -e "  ${GREEN}✓${NC} $name: ${GREEN}RUNNING${NC} (PID: $pid)"
            return 0
        else
            echo -e "  ${RED}✗${NC} $name: ${RED}STOPPED${NC}"
            return 1
        fi
    else
        echo -e "  ${YELLOW}○${NC} $name: ${YELLOW}NOT STARTED${NC}"
        return 2
    fi
}

show_system_stats() {
    echo -e "${BLUE}🖥️  System Resources${NC}"
    echo ""

    # CPU Usage
    local cpu_usage=$(top -bn1 | grep "Cpu(s)" | sed "s/.*, *\([0-9.]*\)%* id.*/\1/")
    echo -e "  CPU: $cpu_usage (16 cores)"

    # Memory Usage
    local mem_info=$(free -h | grep Mem)
    echo $mem_info

    # Disk Usage
    echo ""
    df -h "$PROJECT_DIR" | grep -v Filesystem | grep -v Mounted

    # Load Average
    local load=$(uptime | awk -F'load average:' '{print $1}')
    echo -e "  Load Average:$load"

    echo ""
}

show_training_stats() {
    echo -e "${BLUE}🧠 Training Progress${NC}"
    echo ""

    # Check if training is running
    if [ -f "$PROJECT_DIR/llm/training.pid" ]; then
        local train_pid=$(cat "$PROJECT_DIR/llm/training.pid")
        if ps -p $train_pid > /dev/null; then
            # Get recent rewards from log
            if [ -f "$LOG_DIR/training.log" ]; then
                local recent_rewards=$(tail -100 "$LOG_DIR/training.log" | grep "reward=" | tail -20 | grep -oP 'reward=\K[0-9.-]+')

                if [ ! -z "$recent_rewards" ]; then
                    echo -e "  Recent rewards:"
                    echo "$recent_rewards" | while read reward; do
                        # Colorize rewards
                        if [ $(echo "$reward > 0" | bc -l) -eq 1 ]; then
                            echo -e "    ${GREEN}$reward${NC}"
                        else
                            echo -e "    ${RED}$reward${NC}"
                        fi
                    done
                    echo ""
                fi

                # Show recent episode info
                local recent_episode=$(tail -100 "$LOG_DIR/training.log" | grep "Episode " | tail -1)
                if [ ! -z "$recent_episode" ]; then
                    echo "  $recent_episode"
                fi
            fi

            # Show training duration
            local start_time=$(ps -o etimes= -p $train_pid | awk '{sum += $1} END {print sum}')
            local duration=$((start_time / 60))
            echo -e "  Training duration: ${CYAN}$duration minutes${NC}"
        fi
    else
        echo -e "  ${YELLOW}No training process found${NC}"
    fi

    echo ""
}

show_curriculum_progress() {
    echo -e "${BLUE}📚 Curriculum Progress${NC}"
    echo ""

    # Parse curriculum progress from logs
    if [ -f "$LOG_DIR/training.log" ]; then
        local current_stage=$(tail -500 "$LOG_DIR/training.log" | grep "current_stage=" | tail -1 | grep -oP 'current_stage=\K[0-9]+')
        local progress=$(tail -500 "$LOG_DIR/training.log" | grep "progress_percentage=" | tail -1 | grep -oP 'progress_percentage=\K[0-9.]+')

        if [ ! -z "$current_stage" ]; then
            local stages=("Basic Movement" "Gathering" "Crafting" "Survival" "Building")
            local stage_idx=$((current_stage))
            echo -e "  Current Stage: ${CYAN}${stages[$stage_idx]}${NC}"

            if [ ! -z "$progress" ]; then
                echo -e "  Progress: ${GREEN}${progress}%${NC}"
            fi
        fi
    fi

    echo ""
}

show_model_checkpoints() {
    echo -e "${BLUE}💾 Model Checkpoints${NC}"
    echo ""

    if [ -d "$MODEL_DIR" ]; then
        local checkpoints=$(ls -lt "$MODEL_DIR"/model_step_*.pt 2>/dev/null | head -5)
        local checkpoint_count=$(ls "$MODEL_DIR"/model_step_*.pt 2>/dev/null | wc -l)

        if [ $checkpoint_count -gt 0 ]; then
            echo -e "  Total checkpoints: ${GREEN}$checkpoint_count${NC}"
            echo ""
            echo "  Recent checkpoints:"
            echo "$checkpoints" | while read -r line; do
                local filename=$(echo "$line" | awk '{print $NF}')
                local size=$(echo "$line" | awk '{print $5}')
                local date=$(echo "$line" | awk '{print $6, $7}')
                echo "    📄 $filename ($size, $date)"
            done
        else
            echo -e "  ${YELLOW}No checkpoints yet${NC}"
        fi
    fi

    echo ""
}

show_memory_stats() {
    echo -e "${BLUE}🧠 Memory Database${NC}"
    echo ""

    if [ -f "$PROJECT_DIR/llm/data/memories/minecraft_rl.db" ]; then
        # Get stats from SQLite
        local total_memories=$(sqlite3 "$PROJECT_DIR/llm/data/memories/minecraft_rl.db" "SELECT COUNT(*) FROM long_term_memory;" 2>/dev/null)
        local total_episodes=$(sqlite3 "$PROJECT_DIR/llm/data/memories/minecraft_rl.db" "SELECT COUNT(*) FROM episodes;" 2>/dev/null)
        local discovered_recipes=$(sqlite3 "$PROJECT_DIR/llm/data/memories/minecraft_rl.db" "SELECT COUNT(*) FROM discovered_recipes;" 2>/dev/null)

        echo -e "  Long-term memories: ${GREEN}${total_memories:-0}${NC}"
        echo -e "  Episodes completed: ${GREEN}${total_episodes:-0}${NC}"
        echo -e "  Recipes discovered: ${GREEN}${discovered_recipes:-0}${NC}"
    else
        echo -e "  ${YELLOW}No database yet${NC}"
    fi

    echo ""
}

show_recent_errors() {
    echo -e "${BLUE}⚠️  Recent Errors${NC}"
    echo ""

    if [ -f "$LOG_DIR/training.log" ]; then
        local errors=$(tail -500 "$LOG_DIR/training.log" | grep -i "error\|failed\|crash" | tail -10)
        if [ ! -z "$errors" ]; then
            echo "$errors"
            echo ""
        else
            echo -e "  ${GREEN}No recent errors${NC}"
            echo ""
        fi
    fi
}

show_tensorboard_link() {
    echo -e "${BLUE}📊 Monitoring Links${NC}"
    echo ""

    # Check if TensorBoard is running
    if [ -f "$PROJECT_DIR/llm/tensorboard.pid" ]; then
        local tb_pid=$(cat "$PROJECT_DIR/llm/tensorboard.pid")
        if ps -p $tb_pid > /dev/null; then
            echo -e "  TensorBoard: ${GREEN}RUNNING${NC}"
            echo -e "  URL: ${CYAN}http://localhost:6006${NC}"
            echo ""
            echo -e "  Access remotely: ${YELLOW}ssh -L localhost:6006:localhost:6006 user@ovh-server${NC}"
        fi
    else
        echo -e "  ${YELLOW}TensorBoard not running${NC}"
        echo -e "  Start with: $0 monitor"
    fi

    echo ""
}

show_live_monitor() {
    # Continuously update every 5 seconds
    while true; do
        print_header
        show_system_stats
        show_training_stats
        show_curriculum_progress
        show_model_checkpoints
        show_memory_stats
        show_recent_errors
        show_tensorboard_link

        echo -e "${CYAN}Press Ctrl+C to exit${NC}"
        echo ""
        sleep 5
    done
}

show_help() {
    cat << EOF
${BLUE}Minecraft RL AI - Monitoring Script${NC}

Usage: $0 [options]

Options:
    (no args)       Show one-time status snapshot
    --live, -l      Live monitoring mode (updates every 5 seconds)
    --stats         Show detailed statistics only
    --logs          Show recent log entries
    --errors        Show recent errors only
    --checkpoints   Show model checkpoints only

Examples:
    $0              Show current status
    $0 --live       Live monitoring mode
    $0 --stats      Show detailed stats
    $0 --logs       Show recent logs

Monitoring:
    - TensorBoard: http://localhost:6006
    - Training logs: tail -f llm/data/logs/training.log
EOF
}

# Main
case "${1:-}" in
    --live|-l)
        show_live_monitor
        ;;

    --stats)
        print_header
        show_system_stats
        show_training_stats
        show_curriculum_progress
        show_model_checkpoints
        show_memory_stats
        ;;

    --logs)
        echo -e "${BLUE}📋 Recent Logs${NC}"
        echo ""
        if [ -f "$LOG_DIR/training.log" ]; then
            tail -50 "$LOG_DIR/training.log"
        else
            echo "No logs found"
        fi
        ;;

    --errors)
        show_recent_errors
        ;;

    --checkpoints)
        print_header
        show_model_checkpoints
        ;;

    --help|-h)
        show_help
        ;;

    *)
        print_header
        check_process "Bridge Server" "$PROJECT_DIR/llm/bridge.pid"
        check_process "AI Coordinator" "$PROJECT_DIR/ai-coordinator.pid"
        check_process "RL Training" "$PROJECT_DIR/llm/training.pid"
        check_process "TensorBoard" "$PROJECT_DIR/llm/tensorboard.pid"
        echo ""

        show_system_stats
        show_training_stats
        show_curriculum_progress
        show_model_checkpoints
        show_memory_stats
        show_tensorboard_link
        ;;
esac

exit 0
