#!/usr/bin/env python3
"""
Reset Curriculum to Stage 0
Resets the training curriculum back to the first stage.
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from training.curriculum import create_curriculum
from utils.config import get_config
from utils.logger import Logger, get_logger

def main():
    """Reset curriculum to stage 0"""
    # Initialize logger
    Logger.initialize()
    logger = get_logger(__name__)

    logger.info("🔄 Resetting curriculum to Stage 0...")

    # Load config and create curriculum
    config = get_config()
    curriculum = create_curriculum(config.config)

    # Reset to stage 0
    curriculum.reset()

    logger.info("✅ Curriculum reset to Stage 0")
    logger.info(f"Current stage: {curriculum.current_stage_idx}")
    logger.info(f"Stage name: {curriculum.get_current_stage().name}")
    logger.info("")
    logger.info("⚠️  Note: This only resets the curriculum object in memory.")
    logger.info("   If you have saved checkpoints, you need to:")
    logger.info("   1. Delete or rename checkpoint files, OR")
    logger.info("   2. Start training without --resume flag")

    # Show checkpoint directory
    checkpoint_dir = config.config.get('checkpointing', {}).get('save_dir', './data/models')
    logger.info(f"\n📁 Checkpoint directory: {checkpoint_dir}")

    return 0

if __name__ == '__main__':
    sys.exit(main())
