"""
Trainer - Main training loop for Minecraft RL Agent.
Orchestrates the complete training process.
"""

import torch
import numpy as np
from typing import Dict, Any, Optional, Callable, List, Tuple
from pathlib import Path
import time
from datetime import datetime

from agents.ppo_agent import PPOAgent, create_ppo_agent
from agents.intrinsic_curiosity import IntrinsicCuriosityModule, create_curiosity_module
from memory.memory_manager import MemoryManager, get_database_manager
from crafting.craft_discovery import CraftDiscoverySystem
from training.curriculum import Curriculum, RewardShaper, create_curriculum
from training.auto_curriculum import AutoCurriculum, create_auto_curriculum
from training.hindsight_experience_replay import HindsightExperienceReplay, create_her
from training.priority_experience_replay import PrioritizedExperienceReplay, create_priority_replay
from training.reward_normalization import RewardNormalizationSystem, create_reward_normalization
from gym_env.minecraft_env import MinecraftEnv, create_minecraft_env
from gym_env.parallel_env import ParallelMinecraftEnv, create_parallel_env
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
        curriculum: Curriculum = None,
        curiosity_module: IntrinsicCuriosityModule = None,
        auto_curriculum: AutoCurriculum = None,
        her_module: HindsightExperienceReplay = None,
        per_module: PrioritizedExperienceReplay = None,
        reward_normalization_system: RewardNormalizationSystem = None
    ):
        """
        Initialize trainer

        Args:
            config: Configuration dictionary
            env: Minecraft environment
            agent: PPO agent
            memory: Memory manager
            curriculum: Curriculum (fixed or auto)
            curiosity_module: Intrinsic curiosity module for autonomous learning
            auto_curriculum: Auto-curriculum for self-directed learning
            her_module: Hindsight Experience Replay module
            per_module: Prioritized Experience Replay module
            reward_normalization_system: Reward normalization and clipping system
        """
        self.config = config or get_config()
        self.training_config = self.config.get('training', {})

        # Check if using auto-curriculum mode
        self.auto_curriculum_enabled = self.training_config.get('auto_curriculum', {}).get('enabled', False)
        self.curiosity_enabled = self.training_config.get('curiosity', {}).get('enabled', False)
        self.use_parallel_envs = self.training_config.get('parallel_envs', {}).get('enabled', False)

        logger.info(f"🎓 Auto-Curriculum: {'ENABLED' if self.auto_curriculum_enabled else 'DISABLED'}")
        logger.info(f"🤖 Intrinsic Curiosity: {'ENABLED' if self.curiosity_enabled else 'DISABLED'}")
        if self.use_parallel_envs:
            num_envs = self.training_config.get('parallel_envs', {}).get('num_envs', 8)
            logger.info(f"⚡ Parallel Environments: ENABLED ({num_envs}x speedup)")
        else:
            logger.info("⚡ Parallel Environments: DISABLED")

        # Initialize components
        self.env = env
        self.agent = agent
        self.memory = memory or get_database_manager()

        # Curriculum (fixed or auto)
        self.curriculum = curriculum
        self.auto_curriculum = auto_curriculum

        # If auto-curriculum enabled, use it instead of fixed curriculum
        if self.auto_curriculum_enabled and self.auto_curriculum:
            logger.info("🚀 Using AUTO-CURRICULUM - agent sets its own learning goals")
        elif self.curriculum:
            logger.info("📋 Using FIXED CURRICULUM - human-defined stages")
            # Reward shaper only for fixed curriculum
            self.reward_shaper = RewardShaper(self.curriculum)

        # Curiosity module for intrinsic rewards
        self.curiosity_module = curiosity_module

        # Hindsight Experience Replay for learning from failures
        self.her_module = her_module

        # Prioritized Experience Replay for learning from important mistakes
        self.per_module = per_module

        # Reward normalization system for stable training
        self.reward_normalization_system = reward_normalization_system

        # Craft discovery
        self.craft_discovery = CraftDiscoverySystem(self.memory)

        # Training state
        self.total_steps = 0
        self.total_episodes = 0
        self.best_mean_reward = float('-inf')
        self.current_episode_id = None

        # Checkpointing
        self.checkpoint_dir = Path(self.config.get('checkpointing.save_dir', './data/models'))
        self.checkpoint_dir.mkdir(parents=True, exist_ok=True)
        self.save_freq = self.config.get('checkpointing.save_frequency', 10000)
        self.log_freq = self.training_config.get('log_freq', 5000)

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
        logger.info(f"Mode: {'AUTO-CURRICULUM' if self.auto_curriculum_enabled else 'FIXED CURRICULUM'}")
        if self.use_parallel_envs:
            num_envs = self.training_config.get('parallel_envs', {}).get('num_envs', 8)
            logger.info(f"⚡ Using {num_envs} PARALLEL ENVIRONMENTS")

        start_time = time.time()
        episode_num = 0

        # Initialize parallel environments
        if self.use_parallel_envs:
            logger.info("Resetting all parallel environments...")
            current_observations, _ = self.env.reset()
            logger.info(f"All {len(self.env)} environments ready!")

        while self.total_steps < total_timesteps:
            if self.use_parallel_envs:
                # Parallel environments: run steps across all envs
                parallel_stats = self._train_parallel_step(current_observations)

                # Update observations for next step
                current_observations = parallel_stats['next_observations']

                # Log progress less frequently for parallel (more steps per iteration)
                if self.total_steps % self.log_freq == 0:
                    logger.info(
                        f"⚡ Steps: {self.total_steps}/{total_timesteps} | "
                        f"Avg Reward: {parallel_stats['total_reward']/(parallel_stats['num_steps'] or 1):.2f} | "
                        f"Speed: {len(self.env)}x"
                    )

                    # Log mechanic mastery if using auto-curriculum
                    if self.auto_curriculum_enabled and self.auto_curriculum and self.total_steps % 10000 == 0:
                        logger.info(self.auto_curriculum.get_mechanic_report())

                # Save checkpoint
                if self.total_steps % self.save_freq == 0 and self.total_steps > 0:
                    self._save_checkpoint(episode_num)

                # Callback
                if callback:
                    callback(self, parallel_stats)

            else:
                # Single environment: run full episodes
                episode_num += 1

                # Start episode
                episode_stats = self._train_episode(episode_num)

                # Log progress
                if episode_num % 10 == 0:
                    self._log_progress(episode_num, episode_stats)

                    # Log mechanic mastery if using auto-curriculum
                    if self.auto_curriculum_enabled and self.auto_curriculum and episode_num % 100 == 0:
                        logger.info(self.auto_curriculum.get_mechanic_report())

                # Curriculum advancement (only for fixed curriculum)
                if not self.auto_curriculum_enabled and self.curriculum:
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

        # Get curriculum progress
        if self.auto_curriculum_enabled and self.auto_curriculum:
            curriculum_progress = self.auto_curriculum.get_progress_summary()
            logger.info("\n" + self.auto_curriculum.get_mechanic_report())
        elif self.curriculum:
            curriculum_progress = self.curriculum.get_progress_summary()
        else:
            curriculum_progress = {}

        return {
            'total_episodes': episode_num,
            'total_steps': self.total_steps,
            'elapsed_time': elapsed_time,
            'final_stats': self.agent.get_statistics(),
            'curriculum_progress': curriculum_progress,
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
            stage_idx = 0
            if self.auto_curriculum_enabled and self.auto_curriculum:
                stage_idx = 0  # Auto-curriculum doesn't have fixed stages
            elif self.curriculum:
                stage_idx = self.curriculum.current_stage_idx

            self.current_episode_id = self.memory.create_episode(stage_idx)
        else:
            self.current_episode_id = None

        log_episode_start(logger, self.current_episode_id or episode_num, info)

        done = False
        truncated = False

        # Collect transitions for ICM update
        icm_observations = []
        icm_next_observations = []
        icm_actions = []

        while not (done or truncated):
            # Select action
            action, log_prob, value = self.agent.select_action(obs)

            # Step environment
            next_obs, reward, done, truncated, info = self.env.step(action)

            # Apply reward shaping (only for fixed curriculum)
            if self.auto_curriculum_enabled:
                # In intrinsic mode, reward is already computed by curiosity module
                shaped_reward = reward
            elif hasattr(self, 'reward_shaper'):
                shaped_reward = self.reward_shaper.shape_reward(reward)
            else:
                shaped_reward = reward

            # Apply reward normalization and clipping to prevent explosion
            if self.reward_normalization_system:
                norm_result = self.reward_normalization_system.process_step(shaped_reward, done or truncated)
                shaped_reward = norm_result['normalized_reward']

            # Log reward régulièrement pour voir s'il y a du progrès
            if self.total_steps % 100 == 0:
                logger.info(f"Step {self.total_steps}: reward={shaped_reward:.6f}")

            # Store transition for PPO
            self.agent.store_transition(
                observation=obs,
                action=action,
                log_prob=log_prob,
                reward=shaped_reward,
                value=value,
                done=done or truncated
            )

            # Store in HER buffer for learning from failures
            if self.her_module:
                self.her_module.store_transition(
                    observation=obs,
                    action=action,
                    reward=shaped_reward,
                    next_observation=next_obs,
                    done=done or truncated
                )

            # Store in PER buffer for prioritized learning
            if self.per_module:
                # We'll compute TD-error later during update
                # For now, store without priority (will use max)
                self.per_module.store_transition(
                    observation=obs,
                    action=action,
                    reward=shaped_reward,
                    next_observation=next_obs,
                    done=done or truncated,
                    td_error=None  # Will be computed during update
                )

            # Store in memory (if memory manager supports it)
            if self.memory and hasattr(self.memory, 'remember_transition'):
                self.memory.remember_transition(obs, action, shaped_reward, done or truncated, next_obs)

            # Update curriculum progress
            if self.auto_curriculum_enabled and self.auto_curriculum:
                self.auto_curriculum.update(self.total_steps)
            elif self.curriculum:
                self.curriculum.update_progress(1, shaped_reward)

            # Collect for ICM update
            if self.curiosity_enabled:
                icm_observations.append(obs)
                icm_next_observations.append(next_obs)
                icm_actions.append(action)

            episode_reward += shaped_reward
            episode_length += 1
            self.total_steps += 1

            obs = next_obs

            # Update policy if buffer is full
            if len(self.agent.rollout_buffer) >= self.agent.n_steps:
                update_stats = self.agent.update()

                # Update curiosity module
                if self.curiosity_enabled and self.curiosity_module and len(icm_observations) > 0:
                    icm_stats = self.curiosity_module.update_icm(
                        icm_observations,
                        icm_next_observations,
                        icm_actions
                    )
                    if update_stats:
                        update_stats.update(icm_stats)

                    # Clear ICM buffer
                    icm_observations = []
                    icm_next_observations = []
                    icm_actions = []

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

        # Get reward statistics to see what the bot actually accomplished
        reward_stats = self.env.reward_system.get_statistics()

        # Get curriculum stage
        if self.auto_curriculum_enabled and self.auto_curriculum:
            curriculum_stage = 0  # Auto-curriculum doesn't have fixed stages
            # Add mechanic mastery info
            stats = {
                'episode': episode_num,
                'reward': episode_reward,
                'length': episode_length,
                'curriculum_stage': curriculum_stage,
                'auto_curriculum': True,
                # Mechanic mastery
                'mechanic_mastery': {
                    name: mech.mastery
                    for name, mech in self.auto_curriculum.mechanics.items()
                    if mech.skill_level.value > 0  # Only include discovered mechanics
                },
                # Actual accomplishments
                'blocks_mined': reward_stats.get('blocks_mined', {}),
                'items_crafted': reward_stats.get('items_crafted', {}),
                'blocks_placed': reward_stats.get('blocks_placed', 0),
                'distance_traveled': reward_stats.get('distance_traveled', 0.0),
                'discovered_blocks': reward_stats.get('discovered_blocks', 0),
                'discovered_biomes': reward_stats.get('discovered_biomes', 0),
                'visited_chunks': reward_stats.get('visited_chunks', 0),
            }
        elif self.curriculum:
            curriculum_stage = self.curriculum.current_stage_idx
            stats = {
                'episode': episode_num,
                'reward': episode_reward,
                'length': episode_length,
                'curriculum_stage': curriculum_stage,
                'auto_curriculum': False,
                # Actual accomplishments
                'blocks_mined': reward_stats.get('blocks_mined', {}),
                'items_crafted': reward_stats.get('items_crafted', {}),
                'blocks_placed': reward_stats.get('blocks_placed', 0),
                'distance_traveled': reward_stats.get('distance_traveled', 0.0),
                'discovered_blocks': reward_stats.get('discovered_blocks', 0),
                'discovered_biomes': reward_stats.get('discovered_biomes', 0),
                'visited_chunks': reward_stats.get('visited_chunks', 0),
            }
        else:
            # Fallback
            stats = {
                'episode': episode_num,
                'reward': episode_reward,
                'length': episode_length,
                'curriculum_stage': 0,
                'blocks_mined': {},
                'items_crafted': {},
                'blocks_placed': 0,
                'distance_traveled': 0.0,
            }

        # Enhanced logging with accomplishments
        log_episode_end(logger, self.current_episode_id or episode_num, stats)

        # Additional detailed log every episode
        logger.info(f"📊 Episode {episode_num} Accomplishments:")
        logger.info(f"   ⛏️  Blocks mined: {sum(reward_stats.get('blocks_mined', {}).values())} total")
        if reward_stats.get('blocks_mined'):
            for block_type, count in reward_stats['blocks_mined'].items():
                if count > 0:
                    logger.info(f"      - Block type {block_type}: {count}")
        logger.info(f"   🔨 Items crafted: {sum(reward_stats.get('items_crafted', {}).values())} total")
        logger.info(f"   🧱 Blocks placed: {reward_stats.get('blocks_placed', 0)}")
        logger.info(f"   🚶 Distance: {reward_stats.get('distance_traveled', 0.0):.1f} blocks")
        logger.info(f"   🔬 Discoveries: {reward_stats.get('discovered_blocks', 0)} block types, {reward_stats.get('visited_chunks', 0)} chunks")

        return stats

    def _train_parallel_step(self, observations: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Run one step across all parallel environments

        Args:
            observations: List of current observations from each environment

        Returns:
            Combined statistics from all environments
        """
        num_envs = len(self.env)

        # Select actions for all environments
        actions = []
        log_probs = []
        values = []

        for obs in observations:
            action, log_prob, value = self.agent.select_action(obs)
            actions.append(action)
            log_probs.append(log_prob)
            values.append(value)

        # Step all environments
        next_observations, rewards, dones, truncateds, infos = self.env.step(actions)

        # Process transitions from all environments
        total_reward = 0
        total_steps = num_envs

        # Store transitions and collect ICM data
        icm_observations = []
        icm_next_observations = []
        icm_actions = []

        for i in range(num_envs):
            obs = observations[i]
            action = actions[i]
            log_prob = log_probs[i]
            value = values[i]
            reward = rewards[i]
            done = dones[i] or truncateds[i]
            next_obs = next_observations[i]

            # Apply reward shaping
            if self.auto_curriculum_enabled:
                shaped_reward = reward
            elif hasattr(self, 'reward_shaper'):
                shaped_reward = self.reward_shaper.shape_reward(reward)
            else:
                shaped_reward = reward

            # Store transition
            self.agent.store_transition(
                observation=obs,
                action=action,
                log_prob=log_prob,
                reward=shaped_reward,
                value=value,
                done=done
            )

            # Store in HER buffer for learning from failures
            if self.her_module:
                self.her_module.store_transition(
                    observation=obs,
                    action=action,
                    reward=shaped_reward,
                    next_observation=next_obs,
                    done=done
                )

            # Store in PER buffer for prioritized learning
            if self.per_module:
                self.per_module.store_transition(
                    observation=obs,
                    action=action,
                    reward=shaped_reward,
                    next_observation=next_obs,
                    done=done,
                    td_error=None
                )

            # Collect for ICM update
            if self.curiosity_enabled:
                icm_observations.append(obs)
                icm_next_observations.append(next_obs)
                icm_actions.append(action)

            total_reward += shaped_reward

            # Update curriculum progress
            if self.auto_curriculum_enabled and self.auto_curriculum:
                self.auto_curriculum.update(self.total_steps + i)
            elif self.curriculum:
                self.curriculum.update_progress(1, shaped_reward)

        self.total_steps += total_steps

        # Update policy if buffer is full
        update_stats = None
        if len(self.agent.rollout_buffer) >= self.agent.n_steps:
            update_stats = self.agent.update()

            # Update curiosity module
            if self.curiosity_enabled and self.curiosity_module and len(icm_observations) > 0:
                icm_stats = self.curiosity_module.update_icm(
                    icm_observations,
                    icm_next_observations,
                    icm_actions
                )
                if update_stats:
                    update_stats.update(icm_stats)

        # Auto-reset terminated environments
        terminated_indices = [i for i, done in enumerate(dones) if done]
        if terminated_indices:
            # For terminated environments, we'll reset them and use a placeholder obs
            # The actual reset will happen in the next iteration
            self.env.reset_terminated(terminated_indices)
            # Mark terminated observations for reset (will be handled in next iteration)
            for i in terminated_indices:
                # Keep the observation but it will be replaced after reset
                pass

        return {
            'next_observations': next_observations,
            'total_reward': total_reward,
            'num_steps': total_steps,
            'update_stats': update_stats
        }

    def _log_progress(self, episode_num: int, episode_stats: Dict[str, Any]):
        """Log training progress"""
        agent_stats = self.agent.get_statistics()

        if self.auto_curriculum_enabled and self.auto_curriculum:
            curriculum_progress = self.auto_curriculum.get_progress_summary()
            stage_name = f"Auto ({curriculum_progress['discovered_mechanics']}/{curriculum_progress['total_mechanics']} mechanics)"
            progress_pct = curriculum_progress['mastery_percentage']
        elif self.curriculum:
            curriculum_progress = self.curriculum.get_progress_summary()
            current_stage = self.curriculum.get_current_stage()
            stage_name = current_stage.name if current_stage else 'unknown'
            progress_pct = curriculum_progress['progress_percentage']
        else:
            stage_name = 'N/A'
            progress_pct = 0

        logger.info(
            f"📈 Episode {episode_num} | "
            f"Reward: {episode_stats['reward']:.1f} | "
            f"Length: {episode_stats['length']} | "
            f"Stage: {stage_name} | "
            f"Progress: {progress_pct:.1f}%"
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

    # Check training mode
    training_config = config.get('training', {})
    auto_curriculum_enabled = training_config.get('auto_curriculum', {}).get('enabled', False)
    curiosity_enabled = training_config.get('curiosity', {}).get('enabled', False)

    # Check if using parallel environments
    parallel_env_config = training_config.get('parallel_envs', {})
    use_parallel_envs = parallel_env_config.get('enabled', False)

    # Create curriculum (fixed or auto)
    if auto_curriculum_enabled:
        logger.info("🚀 Creating AUTO-CURRICULUM for autonomous learning")
        curriculum = None  # Not using fixed curriculum
        auto_curriculum = create_auto_curriculum(config)
    else:
        logger.info("📋 Creating FIXED CURRICULUM")
        curriculum = create_curriculum(config)
        auto_curriculum = None

    # Create environment(s)
    if use_parallel_envs:
        # PARALLEL ENVIRONMENTS - 8x speedup!
        num_envs = parallel_env_config.get('num_envs', 8)
        base_port = parallel_env_config.get('base_port', 8765)

        logger.info(f"⚡ Creating {num_envs} PARALLEL ENVIRONMENTS")
        logger.info(f"   Port range: {base_port} - {base_port + num_envs - 1}")
        logger.info(f"   Expected speedup: ~{num_envs}x")

        env = create_parallel_env(
            config,
            num_envs=num_envs,
            base_port=base_port
        )
    else:
        # Single environment
        # Create Minecraft bridge client
        bridge_config = config.get('bridge', {})
        bridge_host = bridge_config.get('host', 'localhost')
        bridge_port = bridge_config.get('port', 8765)

        logger.info(f"Creating Minecraft bridge client: {bridge_host}:{bridge_port}")
        bridge = MinecraftBotBridge(host=bridge_host, port=bridge_port)

        # Create environment with bridge and curriculum
        env = create_minecraft_env(config, curriculum=curriculum, bridge_client=bridge)

    # Create curiosity module if enabled
    curiosity_module = None
    if curiosity_enabled:
        logger.info("🤖 Creating INTRINSIC CURIOSITY MODULE")
        device = 'cuda' if torch.cuda.is_available() else 'cpu'
        curiosity_module = create_curiosity_module(config, device)

    # Create Hindsight Experience Replay module if enabled
    her_module = None
    her_config = training_config.get('her', {})
    her_enabled = her_config.get('enabled', False)
    if her_enabled:
        logger.info("🔄 Creating HINDSIGHT EXPERIENCE REPLAY module")
        her_module = create_her(config)

    # Create Prioritized Experience Replay module if enabled
    per_module = None
    per_config = training_config.get('priority_replay', {})
    per_enabled = per_config.get('enabled', False)
    if per_enabled:
        logger.info("🎯 Creating PRIORITIZED EXPERIENCE REPLAY module")
        per_module = create_priority_replay(config)

    # Create Reward Normalization System
    reward_normalization_system = create_reward_normalization(config)

    # Create agent WITH curriculum (fixed or auto) for action masking
    effective_curriculum = auto_curriculum if auto_curriculum_enabled else curriculum
    agent = create_ppo_agent(config=config, curriculum=effective_curriculum)

    # Update environment's reward system with curiosity and auto-curriculum
    if hasattr(env, 'reward_system'):
        env.reward_system.curiosity_module = curiosity_module
        env.reward_system.auto_curriculum = auto_curriculum

    # Create trainer with all components
    return Trainer(
        config=config,
        env=env,
        agent=agent,
        curriculum=curriculum,
        curiosity_module=curiosity_module,
        auto_curriculum=auto_curriculum,
        her_module=her_module,
        per_module=per_module,
        reward_normalization_system=reward_normalization_system
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
