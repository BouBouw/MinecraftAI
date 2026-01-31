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

    PROJECT_DIR="/opt/MinecraftAI"

    # Clone project if not exists
    if [ ! -d "$PROJECT_DIR" ]; then
        log "  Cloning project to /opt/MinecraftAI..."
        cd /opt

        # If using git (replace with your repository)
        # git clone https://github.com/your-repo/MinecraftAI.git

        log "  ⚠️  Please ensure MinecraftAI project is in /opt/MinecraftAI"
        log "  (Upload via scp/rsync if needed)"
    fi

    cd "$PROJECT_DIR"

    # Make scripts executable
    chmod +x llm/*.sh
    chmod +x llm/monitor.sh

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

    cd "$PROJECT_DIR/ai-coordinator"

    # Install dependencies
    if [ -f "package.json" ]; then
        log "  Installing Node.js packages..."
        npm install > /dev/null 2>&1
        log "  ✅ Node.js packages installed"
    else
        warn "  ⚠️  No package.json found in ai-coordinator"
    fi

    cd "$PROJECT_DIR"
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

    # Use the production launcher
    bash llm/start-production.sh start

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
    echo -e "  ${YELLOW}(SSH tunnel: ssh -L 6006:localhost:6006 root@your-server)${NC}"
    echo ""
    echo -e "${BLUE}📋 Logs:${NC}"
    echo -e "  ${YELLOW}tail -f llm/data/logs/training.log${NC}"
    echo ""
    echo -e "${BLUE}🛑 Stop services:${NC}"
    echo -e "  ${YELLOW}./llm/start-production.sh stop${NC}"
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
