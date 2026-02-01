#!/bin/bash
###############################################################################
# Fix Python imports and start RL training
###############################################################################

set -e

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

log() { echo -e "${GREEN}[$(date +'%H:%M:%S')]${NC} $1"; }
warn() { echo -e "${YELLOW}[WARNING]${NC} $1"; }
error() { echo -e "${RED}[ERROR]${NC} $1"; }

cd ~/MinecraftAI

log "🔧 Step 1: Clearing Python cache..."
find llm/python -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
find llm/python -type f -name "*.pyc" -delete 2>/dev/null || true
log "  ✅ Cache cleared"

log ""
log "🔧 Step 2: Verifying __init__.py files..."

# Fix utils/__init__.py
log "  Checking llm/python/utils/__init__.py..."
cat > llm/python/utils/__init__.py << 'EOF'
"""Utility modules for Minecraft RL system"""

from .config import Config, get_config, reload_config
from .logger import Logger, get_logger, log_episode_start, log_episode_end, log_step

__all__ = [
    'Config',
    'get_config',
    'reload_config',
    'Logger',
    'get_logger',
    'log_episode_start',
    'log_episode_end',
    'log_step',
]
EOF

# Fix gym_env/__init__.py
log "  Checking llm/python/gym_env/__init__.py..."
cat > llm/python/gym_env/__init__.py << 'EOF'
"""Minecraft RL Environment - Gymnasium interface"""

from .minecraft_env import MinecraftEnv, create_minecraft_env
from .observations import ObservationSpace, create_observation_space
from .actions import ActionSpace, ActionType, create_action_space
from .rewards import RewardSystem, CurriculumRewardShaper, create_reward_system

__all__ = [
    'MinecraftEnv',
    'create_minecraft_env',
    'ObservationSpace',
    'create_observation_space',
    'ActionSpace',
    'ActionType',
    'create_action_space',
    'RewardSystem',
    'CurriculumRewardShaper',
    'create_reward_system',
]

__version__ = '0.1.0'
EOF

# Fix agents/__init__.py
log "  Checking llm/python/agents/__init__.py..."
cat > llm/python/agents/__init__.py << 'EOF'
"""RL Agents for Minecraft"""

from .network import PPOModel, MinecraftCNN, MinecraftEncoder, ActorNetwork, CriticNetwork, create_ppo_model
from .ppo_agent import PPOAgent, RolloutBuffer, create_ppo_agent

__all__ = [
    'PPOModel',
    'MinecraftCNN',
    'MinecraftEncoder',
    'ActorNetwork',
    'CriticNetwork',
    'create_ppo_model',
    'PPOAgent',
    'RolloutBuffer',
    'create_ppo_agent',
]
EOF

# Fix memory/__init__.py
log "  Checking llm/python/memory/__init__.py..."
cat > llm/python/memory/__init__.py << 'EOF'
"""Memory systems for Minecraft RL agent"""

from .database import DatabaseManager, get_database_manager
from .short_term import ShortTermMemory, MemoryTransition
from .long_term import LongTermMemory
from .episodic import EpisodicMemory
from .semantic import SemanticMemory
from .memory_manager import MemoryManager

__all__ = [
    'DatabaseManager',
    'get_database_manager',
    'ShortTermMemory',
    'MemoryTransition',
    'LongTermMemory',
    'EpisodicMemory',
    'SemanticMemory',
    'MemoryManager',
]
EOF

# Fix training/__init__.py
log "  Checking llm/python/training/__init__.py..."
cat > llm/python/training/__init__.py << 'EOF'
"""Training system for Minecraft RL"""

from .curriculum import Curriculum, CurriculumStage, RewardShaper, create_curriculum
from .trainer import Trainer, create_trainer, train_minecraft_agent

__all__ = [
    'Curriculum',
    'CurriculumStage',
    'RewardShaper',
    'create_curriculum',
    'Trainer',
    'create_trainer',
    'train_minecraft_agent',
]
EOF

# Create bridge/__init__.py if missing
log "  Creating llm/python/bridge/__init__.py..."
mkdir -p llm/python/bridge
cat > llm/python/bridge/__init__.py << 'EOF'
"""Bridge system for Minecraft RL"""

from .minecraft_bot_bridge import MinecraftBotBridge, MinecraftEnvironment, BotState

__all__ = [
    'MinecraftBotBridge',
    'MinecraftEnvironment',
    'BotState',
]
EOF

# Fix minecraft_bot_bridge.py imports
log "  Fixing bridge/minecraft_bot_bridge.py imports..."
sed -i 's/from \.\.utils\./from utils./g' llm/python/bridge/minecraft_bot_bridge.py
sed -i 's/from \.\.gym_env\./from gym_env./g' llm/python/bridge/minecraft_bot_bridge.py
sed -i 's/from \.\.agents\./from agents./g' llm/python/bridge/minecraft_bot_bridge.py
sed -i 's/from \.\.memory\./from memory./g' llm/python/bridge/minecraft_bot_bridge.py

# Fix other double-dot imports in all Python files
log "  Fixing all double-dot imports..."
find llm/python -name "*.py" -type f -exec sed -i '
s/from \.\.utils\./from utils./g
s/from \.\.gym_env\./from gym_env./g
s/from \.\.agents\./from agents./g
s/from \.\.memory\./from memory./g
s/from \.\.training\./from training./g
s/from \.\.crafting\./from crafting./g
s/from \.\.bridge\./from bridge./g
s/from \.utils\./from utils./g
s/from \.gym_env\./from gym_env./g
s/from \.agents\./from agents./g
s/from \.memory\./from memory./g
s/from \.training\./from training./g
s/from \.crafting\./from crafting./g
s/from \.bridge\./from bridge./g
' {} +

log "  ✅ All imports fixed"

log ""
log "🔧 Step 3: Testing basic imports..."
cd llm/python
python3 << 'PYTEST'
import sys
sys.path.insert(0, '.')

try:
    from utils.config import get_config
    print("  ✅ utils.config imports correctly")
except Exception as e:
    print(f"  ❌ utils.config failed: {e}")
    sys.exit(1)

try:
    from utils.logger import get_logger
    print("  ✅ utils.logger imports correctly")
except Exception as e:
    print(f"  ❌ utils.logger failed: {e}")
    sys.exit(1)

print("\n  ✅ Basic imports successful!")
PYTEST

if [ $? -ne 0 ]; then
    error "Import test failed"
    exit 1
fi

cd ~/MinecraftAI

log ""
log "🚀 Step 4: Starting RL training..."
cd llm
bash start-rl-minecraft.sh
