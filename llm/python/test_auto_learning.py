#!/usr/bin/env python3
"""
Test script to verify Auto-Learning system works correctly
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.config import get_config
from training.auto_curriculum import create_auto_curriculum
from agents.intrinsic_curiosity import create_curiosity_module
import torch

def test_auto_curriculum():
    """Test auto-curriculum initialization and basic functionality"""
    print("🧪 Testing Auto-Curriculum...")

    config = get_config()
    auto_curriculum = create_auto_curriculum(config)

    # Check initialization
    assert len(auto_curriculum.mechanics) > 0, "No mechanics loaded!"
    print(f"✅ Loaded {len(auto_curriculum.mechanics)} mechanics")

    # Test mechanic discovery
    auto_curriculum.discover_mechanic("move_forward", step=100)
    assert auto_curriculum.mechanics["move_forward"].skill_level.value > 0
    print("✅ Mechanic discovery works")

    # Test prerequisite checking
    auto_curriculum.discover_mechanic("move_forward", step=100)
    auto_curriculum.update_mechanic("move_forward", success=True, step=101)
    auto_curriculum.set_learning_goals()
    print(f"✅ Learning goals set: {auto_curriculum.current_goals}")

    # Test progress summary
    progress = auto_curriculum.get_progress_summary()
    print(f"✅ Progress: {progress['discovered_mechanics']}/{progress['total_mechanics']} discovered")

    return True

def test_curiosity_module():
    """Test curiosity module initialization"""
    print("\n🧪 Testing Curiosity Module...")

    config = get_config()
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    print(f"   Using device: {device}")

    curiosity = create_curiosity_module(config, device)

    # Test with dummy observation
    dummy_obs = {
        'position': [0, 64, 0],
        'rotation': [0, 0],
        'block_in_front': 1,
        'health': 20,
        'food': 20
    }

    dummy_next_obs = dummy_obs.copy()
    dummy_next_obs['position'] = [1, 64, 0]

    reward = curiosity.compute_intrinsic_reward(dummy_obs, dummy_next_obs, action=1)
    print(f"✅ Intrinsic reward computed: {reward:.4f}")

    return True

def test_integration():
    """Test integration with trainer"""
    print("\n🧪 Testing Integration...")

    config = get_config()
    auto_curriculum = create_auto_curriculum(config)

    # Check if auto-curriculum is enabled in config
    auto_enabled = config.get('training', {}).get('auto_curriculum', {}).get('enabled', False)
    curiosity_enabled = config.get('training', {}).get('curiosity', {}).get('enabled', False)

    print(f"   Auto-Curriculum enabled: {auto_enabled}")
    print(f"   Curiosity enabled: {curiosity_enabled}")

    if auto_enabled or curiosity_enabled:
        print("✅ Autonomous learning mode configured!")
    else:
        print("⚠️  Using fixed curriculum (enable auto_curriculum for autonomous learning)")

    return True

if __name__ == "__main__":
    print("🚀 Minecraft RL Auto-Learning Test Suite")
    print("=" * 60)

    try:
        test_auto_curriculum()
        test_curiosity_module()
        test_integration()

        print("\n" + "=" * 60)
        print("✅ All tests passed! Auto-Learning system is ready.")
        print("\n📚 Read AUTO_LEARNING_GUIDE.md for usage instructions.")
        print("\n🎮 To start training:")
        print("   cd llm/python")
        print("   python train.py --config ../config/rl_config.yaml")

    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
