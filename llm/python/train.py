#!/usr/bin/env python3
"""
Main Training Script for Minecraft RL Agent
Quick start script for training the autonomous Minecraft AI
"""

import argparse
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from training.trainer import create_trainer, train_minecraft_agent
from utils.config import get_config
from utils.logger import Logger, get_logger


def main():
    """Main training function"""
    parser = argparse.ArgumentParser(
        description='Train Minecraft RL Agent',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  # Train with default settings (1M steps)
  python train.py

  # Train for custom number of steps
  python train.py --steps 5000000

  # Train with custom config
  python train.py --config path/to/config.yaml

  # Train and save to custom checkpoint directory
  python train.py --checkpoint-dir ./my_checkpoints

  # Resume from checkpoint
  python train.py --resume ./checkpoints/model_step_100000.pt
        '''
    )

    parser.add_argument(
        '--steps',
        type=int,
        default=10000000,
        help='Total training timesteps (default: 10M)'
    )

    parser.add_argument(
        '--config',
        type=str,
        default=None,
        help='Path to config YAML file'
    )

    parser.add_argument(
        '--checkpoint-dir',
        type=str,
        default=None,
        help='Directory to save checkpoints'
    )

    parser.add_argument(
        '--resume',
        type=str,
        default=None,
        help='Path to checkpoint file to resume from'
    )

    parser.add_argument(
        '--eval-only',
        action='store_true',
        help='Only run evaluation, no training'
    )

    parser.add_argument(
        '--eval-episodes',
        type=int,
        default=10,
        help='Number of episodes for evaluation (default: 10)'
    )

    parser.add_argument(
        '--device',
        type=str,
        default='cpu',
        choices=['cpu', 'cuda'],
        help='Device to train on (default: cpu)'
    )

    parser.add_argument(
        '--debug',
        action='store_true',
        help='Enable debug logging'
    )

    args = parser.parse_args()

    # Initialize logger
    Logger.initialize()

    if args.debug:
        import logging
        logging.getLogger().setLevel(logging.DEBUG)

    logger = get_logger(__name__)
    logger.info("🚀 Starting Minecraft RL Training")
    logger.info(f"📊 Total steps: {args.steps:,}")
    logger.info(f"💾 Device: {args.device}")

    # Load config
    if args.config:
        from utils.config import Config
        config_obj = Config(args.config)
        config = config_obj.config
    else:
        config = get_config().config

    # Override checkpoint dir if specified
    if args.checkpoint_dir:
        config['checkpointing']['save_dir'] = args.checkpoint_dir
        logger.info(f"📁 Checkpoint directory: {args.checkpoint_dir}")

    try:
        # Create trainer
        logger.info("🎓 Initializing trainer...")
        trainer = create_trainer(config)

        # Resume from checkpoint if specified
        if args.resume:
            logger.info(f"📂 Resuming from checkpoint: {args.resume}")
            trainer.load_training_state(args.resume)

        # Eval only mode
        if args.eval_only:
            logger.info(f"🧪 Running evaluation ({args.eval_episodes} episodes)...")
            eval_stats = trainer.evaluate(num_episodes=args.eval_episodes)

            logger.info("📊 Evaluation Results:")
            logger.info(f"   Mean Reward: {eval_stats['mean_reward']:.2f}")
            logger.info(f"   Std Reward:  {eval_stats['std_reward']:.2f}")
            logger.info(f"   Mean Length: {eval_stats['mean_length']:.1f}")

            return 0

        # Training mode
        logger.info("🏋️ Starting training...")

        # Progress callback
        def progress_callback(trainer, stats):
            """Called every episode/step"""
            # Handle both single env (episode stats) and parallel env (step stats)
            if 'episode' in stats:
                # Single environment mode
                if stats['episode'] % 100 == 0:
                    logger.info(
                        f"Episode {stats['episode']}: "
                        f"reward={stats.get('reward', 0):.2f}, "
                        f"length={stats.get('length', 0)}, "
                        f"stage={stats.get('curriculum_stage', 'N/A')}"
                    )
            elif 'total_reward' in stats:
                # Parallel environment mode
                logger.info(
                    f"Steps {trainer.total_steps}: "
                    f"avg_reward={stats['total_reward']/(stats.get('num_steps', 1) or 1):.2f}, "
                    f"steps={stats.get('num_steps', 0)}"
                )

        # Train
        final_stats = trainer.train(
            total_timesteps=args.steps,
            callback=progress_callback
        )

        # Print final results
        logger.info("\n" + "="*60)
        logger.info("🎉 Training Complete!")
        logger.info("="*60)
        logger.info(f"Total Episodes: {final_stats['total_episodes']:,}")
        logger.info(f"Total Steps: {final_stats['total_steps']:,}")
        logger.info(f"Elapsed Time: {final_stats['elapsed_time']:.1f}s")
        logger.info(f"Final Stage: {final_stats['curriculum_progress']['current_stage']}")
        logger.info(f"Curriculum Progress: {final_stats['curriculum_progress']['progress_percentage']:.1f}%")

        if final_stats['final_stats']:
            agent_stats = final_stats['final_stats']
            logger.info(f"\nFinal Agent Stats:")
            logger.info(f"   Mean Reward: {agent_stats['mean_reward']:.2f}")
            logger.info(f"   Total Episodes: {agent_stats['total_episodes']}")

        return 0

    except KeyboardInterrupt:
        logger.info("\n⚠️ Training interrupted by user")
        return 130

    except Exception as e:
        logger.error(f"❌ Training failed: {e}", exc_info=True)
        return 1

    finally:
        logger.info("✅ Cleanup complete")


if __name__ == '__main__':
    sys.exit(main())
