#!/bin/bash
###############################################################################
# One-Click Deployment for Minecraft RL AI on OVH Server
# Automates entire setup process
###############################################################################

set -e

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

log() {
    echo -e "${GREEN}[$(date +'%H:%M:%S')]${NC} $1"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1"
    exit 1
}

print_banner() {
    clear
    echo -e "${CYAN}╔═══════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${CYAN}║                                                                   ║${NC}"
    echo -e "${CYAN}║     🤖 MINECRAFT RL AI - ONE-CLICK DEPLOYMENT (OVH)              ║${NC}"
    echo -e "${CYAN}║                                                                   ║${NC}"
    echo -e "${CYAN}║     Optimized for: 60GB RAM, 16 Cores, 400GB SSD              ║${NC}"
    echo -e "${CYAN}║     24/7 Autonomous Learning - Ready to Train!               ║${NC}"
    echo -e "${CYAN}║                                                                   ║${NC}"
    echo -e "${CYAN}╚═══════════════════════════════════════════════════════════════╝${NC}"
    echo ""
}

###############################################################################
# Step 1: System Preparation
###############################################################################

step1_prepare_system() {
    log "📦 Step 1/7: Preparing system..."

    # Update system
    log "  Updating system packages..."
    apt update > /dev/null 2>&1
    apt upgrade -y > /dev/null 2>&1

    # Install essential packages
    log "  Installing essential packages..."
    apt install -y \
        python3 \
        python3-venv \
        python3-pip \
        nodejs \
        npm \
        sqlite3 \
        git \
        curl \
        wget \
        htop \
        build-essential \
        ca-certificates \
        > /dev/null 2>&1

    # Configure system limits
    log "  Configuring system limits..."
    echo "* soft nofile 65536" >> /etc/security/limits.conf
    echo "* hard nofile 65536" >> /etc/security/limits.conf

    # Set CPU performance mode
    if [ -w /sys/devices/system/cpu/cpu0/cpufreq/scaling_governor ]; then
        echo performance | tee /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor > /dev/null 2>&1
        log "  ✅ CPU set to performance mode"
    fi

    log "✅ System prepared"
}

###############################################################################
# Step 2: Setup Project
###############################################################################

step2_setup_project() {
    log "📁 Step 2/7: Setting up project..."

    # Auto-detect project directory
    SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

    if [ -d "$SCRIPT/../llm" ]; then
        # Script is in llm/ subdirectory, go to parent
        PROJECT_DIR="$(cd "$SCRIPT/.." && pwd)"
    elif [ -d "$SCRIPT/llm" ]; then
        # Script is run from project root
        PROJECT_DIR="$SCRIPT"
    elif [ -d "/opt/MinecraftAI" ]; then
        # Project is in /opt (standard location)
        PROJECT_DIR="/opt/MinecraftAI"
    else
        log "  ⚠️  Project directory not found in standard location"
        log "  Using script parent directory: $SCRIPT"
        PROJECT_DIR="$SCRIPT"
    fi

    log "  Project directory: $PROJECT_DIR"

    cd "$PROJECT_DIR"

    # Make scripts executable
    chmod +x llm/*.sh 2>/dev/null || true
    chmod +x llm/monitor.sh 2>/dev/null || true

    log "✅ Project setup complete"
}

###############################################################################
# Step 3: Python Environment
###############################################################################

step3_setup_python() {
    log "🐍 Step 3/7: Setting up Python environment..."

    cd "$PROJECT_DIR"

    # Create virtual environment
    if [ ! -d "venv" ]; then
        log "  Creating Python virtual environment..."
        python3 -m venv venv
    fi

    # Activate venv
    source venv/bin/activate

    # Upgrade pip
    log "  Installing Python packages..."
    pip install --upgrade pip setuptools wheel > /dev/null 2>&1

    # Install requirements
    if [ -f "llm/python/requirements.txt" ]; then
        pip install -r llm/python/requirements.txt > llm/data/logs/install.log 2>&1
        log "  ✅ Python packages installed"
    else
        warn "  ⚠️  requirements.txt not found, installing core packages..."
        pip install \
            gymnasium \
            stable-baselines3 \
            torch \
            numpy \
            pyyaml \
            websockets \
            tensorboard \
            sentence-transformers \
            > /dev/null 2>&1
    fi

    log "✅ Python environment ready"
}

###############################################################################
# Step 4: Node.js Environment
###############################################################################

step4_setup_nodejs() {
    log "📦 Step 4/7: Setting up Node.js environment..."

    # Install RL bridge dependencies
    if [ -d "$PROJECT_DIR/llm/node" ]; then
        cd "$PROJECT_DIR/llm/node"

        if [ -f "package.json" ]; then
            log "  Installing RL bridge packages..."
            npm install > /dev/null 2>&1
            log "  ✅ RL bridge packages installed"
        fi

        cd "$PROJECT_DIR"
    fi

    # Install AI Coordinator dependencies (if exists)
    if [ -d "$PROJECT_DIR/ai-coordinator" ]; then
        cd "$PROJECT_DIR/ai-coordinator"

        if [ -f "package.json" ]; then
            log "  Installing AI coordinator packages..."
            npm install > /dev/null 2>&1
            log "  ✅ AI coordinator packages installed"
        fi

        cd "$PROJECT_DIR"
    fi

    log "✅ Node.js environment ready"
}

###############################################################################
# Step 5: Create Directories
###############################################################################

step5_create_directories() {
    log "📂 Step 5/7: Creating data directories..."

    mkdir -p llm/data/memories
    mkdir -p llm/data/experiences
    mkdir -p llm/data/models
    mkdir -p llm/data/logs
    mkdir -p llm/data/logs/tensorboard

    log "✅ Directories created"
}

###############################################################################
# Step 6: Copy Configuration
###############################################################################

step6_setup_config() {
    log "⚙️  Step 6/7: Setting up configuration..."

    cd "$PROJECT_DIR"

    # Use OVH-optimized config if available
    if [ -f "llm/config/rl_config_ovh.yaml" ]; then
        cp llm/config/rl_config_ovh.yaml llm/config/rl_config.yaml
        log "  ✅ Using OVH-optimized configuration"
    elif [ -f "llm/config/rl_config.yaml" ]; then
        log "  ✅ Using default configuration"
    else
        warn "  ⚠️  No configuration found, using defaults"
    fi

    log "✅ Configuration ready"
}

###############################################################################
# Step 7: Start Services
###############################################################################

step7_start_services() {
    log "🚀 Step 7/7: Starting AI services..."

    cd "$PROJECT_DIR"

    # Check if .env exists
    if [ ! -f ".env" ]; then
        log "  ⚠️  .env file not found, creating default..."
        cat > .env << EOF
# Minecraft Server Configuration
MC_HOST=localhost
MC_PORT=25565
MC_USERNAME=RLAgent
EOF
        log "  ✅ Created .env file (please update with your MC server details)"
    fi

    # Use the RL Minecraft launcher
    if [ -f "llm/start-rl-minecraft.sh" ]; then
        bash llm/start-rl-minecraft.sh
    else
        log "  ⚠️  start-rl-minecraft.sh not found, using production launcher..."
        bash llm/start-production.sh start
    fi

    log ""
    log "🎉 DEPLOYMENT COMPLETE!"
    echo ""
    echo -e "${GREEN}═══════════════════════════════════════════════════════════════${NC}"
    echo ""
    echo -e "${CYAN}Your Minecraft RL AI is now running!${NC}"
    echo ""
    echo -e "${BLUE}📊 Monitor with:${NC}"
    echo -e "  ${YELLOW}./llm/monitor.sh${NC}          (one-time status)"
    echo -e "  ${YELLOW}./llm/monitor.sh --live${NC}     (live monitoring)"
    echo ""
    echo -e "${BLUE}📈 TensorBoard:${NC}"
    echo -e "  ${CYAN}http://localhost:6006${NC}"
    echo -e "  ${YELLOW}(SSH tunnel: ssh -L 6006:localhost:6006 user@your-server)${NC}"
    echo ""
    echo -e "${BLUE}📋 Logs:${NC}"
    echo -e "  ${YELLOW}tail -f llm/data/logs/training.log${NC}"
    echo -e "  ${YELLOW}tail -f llm/data/logs/bridge.log${NC}"
    echo ""
    echo -e "${BLUE}🛑 Stop services:${NC}"
    echo -e "  ${YELLOW}./llm/start-rl-minecraft.sh stop${NC}"
    echo ""
}

###############################################################################
# Main Deployment Flow
###############################################################################

main() {
    print_banner

    echo -e "${YELLOW}This will:${NC}"
    echo "  • Update system packages"
    echo "  • Install Python & Node.js"
    echo "  • Setup project structure"
    echo "  • Install all dependencies"
    echo "  • Start RL AI training"
    echo ""
    read -p "$(echo -e ${YELLOW}Continue? [y/N]: ${NC}) " -n 1 -r

    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Aborted."
        exit 1
    fi

    echo ""

    # Run all steps
    step1_prepare_system
    step2_setup_project
    step3_setup_python
    step4_setup_nodejs
    step5_create_directories
    step6_setup_config
    step7_start_services

    echo ""
    log "🎊 All done! Your AI is now learning 24/7!"
}

# Run main
main
