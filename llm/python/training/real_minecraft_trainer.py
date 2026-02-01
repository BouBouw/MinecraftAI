#!/usr/bin/env python3
"""
Real Minecraft RL Trainer
Trains the RL agent on actual Minecraft gameplay

This is the script that actually makes the AI play and learn!
"""

import asyncio
import sys
import os
from pathlib import Path
import argparse
from typing import Optional, Dict, Any

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.config import get_config
from utils.logger import get_logger
from agents.ppo_agent import PPOAgent
from training.curriculum import Curriculum
from memory.memory_manager import MemoryManager
from bridge.minecraft_bot_bridge import MinecraftEnvironment

logger = get_logger(__name__)


class RealMinecraftTrainer:
    """
    Trainer that connects to actual Minecraft game
    """

    def __init__(
        self,
        config_path: Optional[str] = None,
        bridge_host: str = 'localhost',
        bridge_port: int = 8765
    ):
        self.config = get_config(config_path)
        self.bridge_host = bridge_host
        self.bridge_port = bridge_port

        # Initialize components
        self.memory = MemoryManager()
        self.curriculum = Curriculum(self.config)
        self.env = None  # Will be initialized in start()
        self.agent = None  # Will be initialized in start()

        # Training state
        self.total_steps = 0
        self.total_episodes = 0
        self.current_episode_reward = 0.0
        self.best_reward = float('-inf')

    async def start(self, total_timesteps: int = 100000000):
        """
        Start training on real Minecraft

        Args:
            total_timesteps: Total training steps (default: 100M)
        """
        logger.info("🚀 Starting Real Minecraft RL Training")
        logger.info(f"   Total timesteps: {total_timesteps:,}")
        logger.info(f"   Bridge: {self.bridge_host}:{self.bridge_port}")

        try:
            # Connect to real Minecraft environment
            logger.info("🔌 Connecting to Minecraft environment...")
            self.env = await MinecraftEnvironment.create(
                host=self.bridge_host,
                port=self.bridge_port
            )
            logger.info("✅ Connected to Minecraft!")

            # Initialize agent
            logger.info("🤖 Initializing PPO agent...")
            self.agent = PPOAgent(
                config=self.config,
                memory_manager=self.memory,
                device='cpu'  # Use CUDA if available
            )
            logger.info("✅ Agent ready!")

            # Start training loop
            await self.train(total_timesteps)

        except Exception as e:
            logger.error(f"❌ Training failed: {e}")
            raise

    async def train(self, total_timesteps: int):
        """
        Main training loop
        """
        logger.info("🎓 Starting training loop...")
        logger.info("")

        episode_num = 0
        steps = 0

        while steps < total_timesteps:
            episode_num += 1
            self.total_episodes = episode_num

            logger.info(f"🎮 Episode {episode_num}")

            # Reset environment
            observation, info = await self.env.reset()
            self.current_episode_reward = 0.0
            episode_steps = 0
            done = False

            # Start episode in memory
            curriculum_stage = self.curriculum.get_current_stage()
            episode_id = self.memory.episodic.start_episode(self.curriculum.current_stage_idx)

            # Episode loop
            while not done and steps < total_timesteps:
                # Get action from agent (returns tuple: action, log_prob, value)
                action_data = self.agent.select_action(observation)
                # Handle both tuple (action, log_prob, value) and int (action) returns
                if isinstance(action_data, tuple):
                    action_int = action_data[0]
                else:
                    action_int = action_data

                # Step expects a dict with 'action_type' key
                action = {'action_type': action_int}
                observation, reward, done, truncated, info = await self.env.step(action)

                # Store experience
                self.memory.short_term.remember(
                    state=observation,
                    action=action,
                    reward=reward,
                    done=done or truncated
                )

                # Update agent
                self.agent.update(
                    state=observation,
                    action=action,
                    reward=reward,
                    next_state=observation,
                    done=done or truncated
                )

                # Track metrics
                self.current_episode_reward += reward
                episode_steps += 1
                steps += 1
                self.total_steps = steps

                # Log progress
                if episode_steps % 100 == 0:
                    logger.info(
                        f"   Step {episode_steps} | "
                        f"Reward: {reward:.2f} | "
                        f"Total: {self.current_episode_reward:.2f}"
                    )

            # Episode complete
            logger.info(f"✅ Episode {episode_num} complete")
            logger.info(f"   Length: {episode_steps} steps")
            logger.info(f"   Total reward: {self.current_episode_reward:.2f}")
            logger.info("")

            # Update best reward
            if self.current_episode_reward > self.best_reward:
                self.best_reward = self.current_episode_reward
                logger.info(f"🏆 New best reward: {self.best_reward:.2f}")

                # Save checkpoint
                self.save_checkpoint(episode_num)

            # Update curriculum
            self.curriculum.update_progress(steps, self.current_episode_reward)

            # Save memories
            # TODO: Implement store_episode_summary in long_term memory
            # self.memory.long_term.store_episode_summary(episode_id, {
            #     'total_reward': self.current_episode_reward,
            #     'length': episode_steps,
            #     'curriculum_stage': curriculum_stage.name if curriculum_stage else None
            # })

            # Periodic logging
            if episode_num % 10 == 0:
                logger.info("📊 Progress:")
                logger.info(f"   Total steps: {steps:,} / {total_timesteps:,}")
                logger.info(f"   Total episodes: {episode_num}")
                logger.info(f"   Best reward: {self.best_reward:.2f}")
                logger.info(f"   Curriculum stage: {curriculum_stage}")
                logger.info("")

        # Training complete
        logger.info("🎉 Training complete!")
        logger.info(f"   Total steps: {steps:,}")
        logger.info(f"   Total episodes: {episode_num}")
        logger.info(f"   Best reward: {self.best_reward:.2f}")

    def save_checkpoint(self, episode_num: int):
        """Save model checkpoint"""
        checkpoint_path = (
            Path(__file__).parent.parent.parent
            / 'data' / 'models' / f'checkpoint_ep{episode_num}.pt'
        )

        self.agent.save(str(checkpoint_path))
        logger.info(f"💾 Checkpoint saved: {checkpoint_path.name}")


async def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='Train RL agent on real Minecraft'
    )
    parser.add_argument(
        '--steps',
        type=int,
        default=100000000,
        help='Total training steps (default: 100M)'
    )
    parser.add_argument(
        '--config',
        type=str,
        default=None,
        help='Path to config file'
    )
    parser.add_argument(
        '--bridge-host',
        type=str,
        default='localhost',
        help='Bridge server host'
    )
    parser.add_argument(
        '--bridge-port',
        type=int,
        default=8765,
        help='Bridge server port'
    )

    args = parser.parse_args()

    # Create trainer
    trainer = RealMinecraftTrainer(
        config_path=args.config,
        bridge_host=args.bridge_host,
        bridge_port=args.bridge_port
    )

    # Start training
    try:
        await trainer.start(total_timesteps=args.steps)
    except KeyboardInterrupt:
        logger.info("⏸ Training interrupted by user")
    except Exception as e:
        logger.error(f"❌ Training failed: {e}")
        sys.exit(1)


if __name__ == '__main__':
    asyncio.run(main())
