"""
Trainer - Main training loop for Minecraft RL Agent.
Orchestrates the complete training process.
"""

import torch
import numpy as np
from typing import Dict, Any, Optional, Callable
from pathlib import Path
import time
from datetime import datetime

from agents.ppo_agent import PPOAgent, create_ppo_agent
from memory.memory_manager import MemoryManager, get_database_manager
from crafting.craft_discovery import CraftDiscoverySystem
from training.curriculum import Curriculum, RewardShaper, create_curriculum
from gym_env.minecraft_env import MinecraftEnv, create_minecraft_env
from bridge.minecraft_bot_bridge import MinecraftBotBridge
from utils.config import get_config
from utils.logger import get_logger, log_episode_start, log_episode_end

logger = get_logger(__name__)


class Trainer:
    """
    Main training orchestrator

    Coordinates:
    - PPO agent training
    - Curriculum learning
    - Memory management
    - Craft discovery
    - Logging and checkpointing
    """

    def __init__(
        self,
        config: Dict[str, Any] = None,
        env: MinecraftEnv = None,
        agent: PPOAgent = None,
        memory: MemoryManager = None,
        curriculum: Curriculum = None
    ):
        """
        Initialize trainer

        Args:
            config: Configuration dictionary
            env: Minecraft environment
            agent: PPO agent
            memory: Memory manager
            curriculum: Curriculum
        """
        self.config = config or get_config()
        self.training_config = self.config.get('training', {})

        # Initialize components
        self.env = env
        self.agent = agent
        self.memory = memory or get_database_manager()
        self.curriculum = curriculum or create_curriculum(self.config)

        # Craft discovery
        self.craft_discovery = CraftDiscoverySystem(self.memory)

        # Reward shaper
        self.reward_shaper = RewardShaper(self.curriculum)

        # Training state
        self.total_steps = 0
        self.total_episodes = 0
        self.best_mean_reward = float('-inf')
        self.current_episode_id = None

        # Checkpointing
        self.checkpoint_dir = Path(self.config.get('checkpointing.save_dir', './data/models'))
        self.checkpoint_dir.mkdir(parents=True, exist_ok=True)
        self.save_freq = self.config.get('checkpointing.save_frequency', 10000)

        # TensorBoard (if available)
        self.writer = None
        self._setup_tensorboard()

        logger.info("Trainer initialized")

    def _setup_tensorboard(self):
        """Setup TensorBoard writer"""
        try:
            from torch.utils.tensorboard import SummaryWriter

            log_dir = self.config.get('logging.tensorboard.log_dir', './data/logs/tensorboard')
            self.writer = SummaryWriter(log_dir)
            logger.info(f"TensorBoard logging to {log_dir}")
        except ImportError:
            logger.warning("TensorBoard not available")

    def train(
        self,
        total_timesteps: int = None,
        callback: Optional[Callable] = None
    ) -> Dict[str, Any]:
        """
        Main training loop

        Args:
            total_timesteps: Total training timesteps
            callback: Optional callback function

        Returns:
            Training statistics
        """
        if total_timesteps is None:
            total_timesteps = self.training_config.get('total_timesteps', 10000000)

        logger.info(f"Starting training for {total_timesteps} timesteps")

        start_time = time.time()
        episode_num = 0

        while self.total_steps < total_timesteps:
            episode_num += 1

            # Start episode
            episode_stats = self._train_episode(episode_num)

            # Log progress
            if episode_num % 10 == 0:
                self._log_progress(episode_num, episode_stats)

            # Check curriculum advancement
            if self.curriculum.should_advance():
                old_stage = self.curriculum.current_stage_idx
                self.curriculum.advance_stage()

                if old_stage != self.curriculum.current_stage_idx:
                    logger.info(f"✨ Advanced to curriculum stage {self.curriculum.current_stage_idx}")

            # Save checkpoint
            if self.total_steps % self.save_freq == 0 and self.total_steps > 0:
                self._save_checkpoint(episode_num)

            # Callback
            if callback:
                callback(self, episode_stats)

        # Training complete
        elapsed_time = time.time() - start_time

        logger.info(f"Training complete! Episodes: {episode_num}, Steps: {self.total_steps}, Time: {elapsed_time:.1f}s")

        # Final save
        self._save_checkpoint(episode_num, final=True)

        return {
            'total_episodes': episode_num,
            'total_steps': self.total_steps,
            'elapsed_time': elapsed_time,
            'final_stats': self.agent.get_statistics(),
            'curriculum_progress': self.curriculum.get_progress_summary(),
        }

    def _train_episode(self, episode_num: int) -> Dict[str, Any]:
        """
        Train for one episode

        Args:
            episode_num: Episode number

        Returns:
            Episode statistics
        """
        # Start episode
        obs, info = self.env.reset()
        episode_reward = 0
        episode_length = 0

        # Start tracking in memory
        if self.memory:
            self.current_episode_id = self.memory.create_episode(
                self.curriculum.current_stage_idx
            )
        else:
            self.current_episode_id = None

        log_episode_start(logger, self.current_episode_id or episode_num, info)

        done = False
        truncated = False

        while not (done or truncated):
            # Select action
            action, log_prob, value = self.agent.select_action(obs)

            # Step environment
            next_obs, reward, done, truncated, info = self.env.step(action)

            # Apply reward shaping
            shaped_reward = self.reward_shaper.shape_reward(reward)

            # Store transition
            self.agent.store_transition(
                observation=obs,
                action=action,
                log_prob=log_prob,
                reward=shaped_reward,
                value=value,
                done=done or truncated
            )

            # Store in memory (if memory manager supports it)
            if self.memory and hasattr(self.memory, 'remember_transition'):
                self.memory.remember_transition(obs, action, shaped_reward, done or truncated, next_obs)

            # Update curriculum progress
            self.curriculum.update_progress(1, shaped_reward)

            episode_reward += shaped_reward
            episode_length += 1
            self.total_steps += 1

            obs = next_obs

            # Update policy if buffer is full
            if len(self.agent.rollout_buffer) >= self.agent.n_steps:
                update_stats = self.agent.update()

                if update_stats and self.writer:
                    self._log_tensorboard(update_stats)

        # End episode
        if self.memory and hasattr(self.memory, 'current_episode_id'):
            death_cause = info.get('death_cause') if done else None
            # Convert inventory numpy array to list for JSON serialization
            final_inv = obs.get('inventory')
            final_inventory = final_inv.tolist() if hasattr(final_inv, 'tolist') else final_inv

            self.memory.update_episode(
                episode_id=self.current_episode_id,
                total_reward=episode_reward,
                death_cause=death_cause,
                final_inventory=final_inventory
            )

        stats = {
            'episode': episode_num,
            'reward': episode_reward,
            'length': episode_length,
            'curriculum_stage': self.curriculum.current_stage_idx,
        }

        log_episode_end(logger, self.current_episode_id or episode_num, stats)

        return stats

    def _log_progress(self, episode_num: int, episode_stats: Dict[str, Any]):
        """Log training progress"""
        agent_stats = self.agent.get_statistics()
        curriculum_progress = self.curriculum.get_progress_summary()

        logger.info(
            f"Episode {episode_num} | "
            f"Reward: {episode_stats['reward']:.2f} | "
            f"Length: {episode_stats['length']} | "
            f"Stage: {curriculum_progress['current_stage']} | "
            f"Progress: {curriculum_progress['progress_percentage']:.1f}%"
        )

    def _log_tensorboard(self, update_stats: Dict[str, float]):
        """Log to TensorBoard"""
        if not self.writer:
            return

        step = self.total_steps

        self.writer.add_scalar('Loss/policy_loss', update_stats['policy_loss'], step)
        self.writer.add_scalar('Loss/value_loss', update_stats['value_loss'], step)
        self.writer.add_scalar('Loss/entropy', update_stats['entropy'], step)
        self.writer.add_scalar('Reward/mean', update_stats['mean_reward'], step)
        self.writer.add_scalar('Episode/mean_length', update_stats['mean_length'], step)

    def _save_checkpoint(self, episode_num: int, final: bool = False):
        """Save model checkpoint"""
        checkpoint_path = self.checkpoint_dir / f'model_step_{self.total_steps}.pt'

        self.agent.save_model(str(checkpoint_path))

        logger.info(f"Checkpoint saved: {checkpoint_path}")

        # Keep only last N checkpoints
        if not final:
            self._cleanup_old_checkpoints()

    def _cleanup_old_checkpoints(self):
        """Remove old checkpoints, keeping only recent ones"""
        keep_last = self.config.get('checkpointing.keep_last_n', 5)

        checkpoints = sorted(self.checkpoint_dir.glob('model_step_*.pt'))

        if len(checkpoints) > keep_last:
            for old_checkpoint in checkpoints[:-keep_last]:
                old_checkpoint.unlink()

    def evaluate(
        self,
        num_episodes: int = 10
    ) -> Dict[str, Any]:
        """
        Evaluate current policy

        Args:
            num_episodes: Number of episodes to evaluate

        Returns:
            Evaluation statistics
        """
        logger.info(f"Evaluating policy for {num_episodes} episodes...")

        self.agent.set_training_mode(False)

        eval_rewards = []
        eval_lengths = []

        for episode in range(num_episodes):
            obs, _ = self.env.reset()
            episode_reward = 0
            episode_length = 0

            done = False
            while not done:
                action, _, _ = self.agent.select_action(obs)
                obs, reward, done, _, _ = self.env.step(action)
                episode_reward += reward
                episode_length += 1

            eval_rewards.append(episode_reward)
            eval_lengths.append(episode_length)

        self.agent.set_training_mode(True)

        return {
            'mean_reward': np.mean(eval_rewards),
            'std_reward': np.std(eval_rewards),
            'mean_length': np.mean(eval_lengths),
            'episodes': num_episodes,
        }

    def save_training_state(self, filepath: str):
        """
        Save complete training state

        Args:
            filepath: Path to save
        """
        state = {
            'total_steps': self.total_steps,
            'total_episodes': self.total_episodes,
            'best_mean_reward': self.best_mean_reward,
            'curriculum_stage': self.curriculum.current_stage_idx,
            'config': self.config,
        }

        torch.save(state, filepath)
        logger.info(f"Training state saved to {filepath}")

    def load_training_state(self, filepath: str):
        """
        Load training state

        Args:
            filepath: Path to load from
        """
        state = torch.load(filepath)

        self.total_steps = state['total_steps']
        self.total_episodes = state['total_episodes']
        self.best_mean_reward = state['best_mean_reward']
        self.curriculum.current_stage_idx = state['curriculum_stage']

        logger.info(f"Training state loaded from {filepath}")

    def close(self):
        """Clean up resources"""
        if self.writer:
            self.writer.close()

        if self.env:
            self.env.close()

        logger.info("Trainer closed")


def create_trainer(
    config: Dict[str, Any] = None
) -> Trainer:
    """
    Factory function to create trainer

    Args:
        config: Configuration dictionary (plain dict or Config object)

    Returns:
        Trainer instance
    """
    # If None, get the global config
    if config is None:
        config = get_config()

    # Create Minecraft bridge client
    bridge_config = config.get('bridge', {})
    bridge_host = bridge_config.get('host', 'localhost')
    bridge_port = bridge_config.get('port', 8765)

    logger.info(f"Creating Minecraft bridge client: {bridge_host}:{bridge_port}")
    bridge = MinecraftBotBridge(host=bridge_host, port=bridge_port)

    # Create curriculum first (needed by environment)
    curriculum = create_curriculum(config)

    # Create environment with bridge AND curriculum
    env = create_minecraft_env(config, curriculum=curriculum, bridge_client=bridge)

    # Create agent WITH curriculum for action masking
    agent = create_ppo_agent(config=config, curriculum=curriculum)

    # Create trainer with all components
    return Trainer(
        config=config,
        env=env,
        agent=agent,
        curriculum=curriculum  # Pass curriculum to trainer as well
    )


# Convenience function for quick training start
def train_minecraft_agent(
    total_timesteps: int = 100000,
    config_path: str = None,
    checkpoint_dir: str = './data/models'
):
    """
    Quick start training function

    Args:
        total_timesteps: Total training steps
        config_path: Path to config file
        checkpoint_dir: Checkpoint directory

    Returns:
        Training statistics
    """
    # Load config
    if config_path:
        from utils.config import Config
        config_obj = Config(config_path)
        config = config_obj.config
    else:
        config = get_config().config

    # Override checkpoint dir if specified
    if checkpoint_dir:
        config['checkpointing']['save_dir'] = checkpoint_dir

    # Create trainer
    trainer = create_trainer(config)

    # Train
    return trainer.train(total_timesteps=total_timesteps)
