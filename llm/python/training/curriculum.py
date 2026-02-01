"""
Curriculum Learning System for Minecraft RL Agent.
Manages progressive learning stages with increasing complexity.
"""

import numpy as np
from typing import Dict, Any, List, Optional, Callable
from pathlib import Path

from agents.ppo_agent import PPOAgent
from utils.config import get_config
from utils.logger import get_logger

logger = get_logger(__name__)


class CurriculumStage:
    """
    A single curriculum stage

    Defines a learning stage with specific:
    - Available actions
    - Reward scaling
    - Environment conditions
    - Success criteria
    """

    def __init__(
        self,
        name: str,
        steps: int,
        actions: List[int],
        reward_scale: float = 1.0,
        success_threshold: float = 0.0,
        description: str = ""
    ):
        """
        Initialize curriculum stage

        Args:
            name: Stage name
            steps: Number of training steps for this stage
            actions: Available action IDs
            reward_scale: Reward scaling factor
            success_threshold: Success threshold for advancement
            description: Stage description
        """
        self.name = name
        self.steps = steps
        self.actions = actions
        self.reward_scale = reward_scale
        self.success_threshold = success_threshold
        self.description = description

        # Stage progress
        self.current_step = 0
        self.episodes_completed = 0
        self.episode_rewards = []
        self.best_reward = float('-inf')

    def add_episode_reward(self, reward: float):
        """Add episode reward to track progress"""
        self.episode_rewards.append(reward)
        self.episodes_completed += 1

        if reward > self.best_reward:
            self.best_reward = reward

    def is_complete(self) -> bool:
        """Check if stage is complete"""
        # Must have completed at least 10 episodes to evaluate
        if self.episodes_completed < 10:
            return False

        # Check if we've done enough steps
        if self.current_step >= self.steps:
            return True

        # Check if we've reached success threshold (based on recent 10 episodes)
        recent_avg = np.mean(self.episode_rewards[-10:])
        if recent_avg >= self.success_threshold:
            return True

        return False

    def get_progress(self) -> float:
        """Get stage progress (0-1)"""
        return min(self.current_step / self.steps, 1.0)

    def get_statistics(self) -> Dict[str, Any]:
        """Get stage statistics"""
        return {
            'name': self.name,
            'step': self.current_step,
            'total_steps': self.steps,
            'episodes': self.episodes_completed,
            'progress': self.get_progress(),
            'avg_reward': np.mean(self.episode_rewards) if self.episode_rewards else 0,
            'best_reward': self.best_reward,
        }


class Curriculum:
    """
    Curriculum learning manager

    Manages progressive learning through stages
    """

    def __init__(self, config: Dict[str, Any]):
        """
        Initialize curriculum

        Args:
            config: Configuration dictionary
        """
        self.config = config
        curriculum_config = config.get('training.curriculum', {})

        self.enabled = curriculum_config.get('enabled', True)
        self.stages_config = curriculum_config.get('stages', [])

        # Initialize stages
        self.stages: List[CurriculumStage] = []
        self.current_stage_idx = 0
        self._initialize_stages()

        logger.info(f"Curriculum initialized with {len(self.stages)} stages")

    def _initialize_stages(self):
        """Initialize curriculum stages from config"""
        stage_definitions = [
            {
                'name': 'basic_movement',
                'steps': 50000,  # 50K steps
                'actions': [0, 1, 2, 5, 8, 9, 10, 11, 12],  # NOOP, MOVE, JUMP, LOOK
                'reward_scale': 1.0,
                'success_threshold': 5000.0,  # Must avg 5K reward (reduced from 50K)
                'description': 'Learn basic movement and controls'
            },
            {
                'name': 'gathering',
                'steps': 250000,  # 250K steps
                'actions': [0, 1, 2, 5, 8, 9, 10, 11, 12, 17, 21, 22, 23],  # + ATTACK, DIG
                'reward_scale': 1.2,  # Reduced from 2.0
                'success_threshold': 10000.0,  # Must avg 10K reward (reduced from 150K)
                'description': 'Learn to gather resources by mining and attacking'
            },
            {
                'name': 'basic_crafting',
                'steps': 750000,  # 750K steps
                'actions': 'all',  # All actions available
                'reward_scale': 1.5,  # Reduced from 5.0
                'success_threshold': 20000.0,  # Must avg 20K reward (reduced from 400K)
                'description': 'Learn basic crafting recipes'
            },
            {
                'name': 'survival',
                'steps': 2000000,  # 2M steps
                'actions': 'all',
                'reward_scale': 2.0,  # Reduced from 10.0
                'success_threshold': 40000.0,  # Must avg 40K reward (reduced from 800K)
                'description': 'Learn to survive against mobs and at night'
            },
            {
                'name': 'building',
                'steps': 5000000,  # 5M steps
                'actions': 'all',
                'reward_scale': 2.5,  # Reduced from 15.0
                'success_threshold': 60000.0,  # Must avg 60K reward (reduced from 1.2M)
                'description': 'Learn to build structures and shelters'
            }
        ]

        for stage_def in stage_definitions:
            stage = CurriculumStage(
                name=stage_def['name'],
                steps=stage_def['steps'],
                actions=stage_def['actions'] if stage_def['actions'] != 'all' else 'all',
                reward_scale=stage_def['reward_scale'],
                success_threshold=stage_def['success_threshold'],
                description=stage_def['description']
            )
            self.stages.append(stage)

    def get_current_stage(self) -> Optional[CurriculumStage]:
        """Get current curriculum stage"""
        if self.current_stage_idx < len(self.stages):
            return self.stages[self.current_stage_idx]
        return None

    def advance_stage(self) -> bool:
        """
        Advance to next curriculum stage

        Returns:
            True if advanced, False if already at last stage
        """
        if self.current_stage_idx >= len(self.stages) - 1:
            return False

        old_stage = self.stages[self.current_stage_idx]
        self.current_stage_idx += 1
        new_stage = self.stages[self.current_stage_idx]

        logger.info(
            f"Curriculum advanced: {old_stage.name} → {new_stage.name}\n"
            f"  {new_stage.description}"
        )

        return True

    def should_advance(self) -> bool:
        """
        Check if we should advance to next stage

        Returns:
            True if ready to advance
        """
        current_stage = self.get_current_stage()

        if current_stage is None:
            return False

        return current_stage.is_complete()

    def update_progress(self, steps: int, episode_reward: float):
        """
        Update curriculum progress

        Args:
            steps: Number of steps taken this episode
            episode_reward: Reward earned this episode
        """
        current_stage = self.get_current_stage()

        if current_stage:
            current_stage.current_step += steps
            current_stage.add_episode_reward(episode_reward)

    def get_available_actions(self) -> List[int]:
        """
        Get available actions for current stage

        Returns:
            List of available action IDs
        """
        current_stage = self.get_current_stage()

        if current_stage and current_stage.actions != 'all':
            return current_stage.actions

        # All actions available (0-49)
        return list(range(50))

    def get_reward_scale(self) -> float:
        """
        Get reward scaling factor for current stage

        Returns:
            Reward scale
        """
        current_stage = self.get_current_stage()
        return current_stage.reward_scale if current_stage else 1.0

    def get_stage_statistics(self) -> List[Dict[str, Any]]:
        """
        Get statistics for all stages

        Returns:
            List of stage statistics
        """
        return [stage.get_statistics() for stage in self.stages]

    def get_progress_summary(self) -> Dict[str, Any]:
        """
        Get overall curriculum progress

        Returns:
            Dictionary with progress summary
        """
        completed_stages = self.current_stage_idx
        total_stages = len(self.stages)
        current_stage = self.get_current_stage()

        return {
            'current_stage': current_stage.name if current_stage else 'completed',
            'current_stage_idx': self.current_stage_idx,
            'completed_stages': completed_stages,
            'total_stages': total_stages,
            'progress_percentage': (completed_stages / total_stages) * 100 if total_stages > 0 else 100,
            'current_stage_progress': current_stage.get_progress() if current_stage else 1.0,
        }

    def reset(self):
        """Reset curriculum to first stage"""
        self.current_stage_idx = 0

        for stage in self.stages:
            stage.current_step = 0
            stage.episodes_completed = 0
            stage.episode_rewards = []
            stage.best_reward = float('-inf')

        logger.info("Curriculum reset to stage 0")

    def __repr__(self) -> str:
        summary = self.get_progress_summary()
        return f"Curriculum(stage={summary['current_stage']}, progress={summary['progress_percentage']:.1f}%)"


class RewardShaper:
    """
    Shapes rewards based on curriculum stage
    """

    def __init__(self, curriculum: Curriculum):
        """
        Initialize reward shaper

        Args:
            curriculum: Curriculum instance
        """
        self.curriculum = curriculum

    def shape_reward(self, reward: float) -> float:
        """
        Apply reward shaping based on current stage

        Args:
            reward: Raw reward

        Returns:
            Shaped reward
        """
        scale = self.curriculum.get_reward_scale()
        return reward * scale

    def get_bonus_rewards(self) -> Dict[str, float]:
        """
        Get stage-specific bonus rewards

        Returns:
            Dictionary with bonus multipliers
        """
        current_stage = self.curriculum.get_current_stage()

        if not current_stage:
            return {}

        bonuses = {
            'basic_movement': {
                'new_block': 10.0,
                'exploration': 2.0,
            },
            'gathering': {
                'block_mined': 1.0,
                'new_block_type': 15.0,
            },
            'basic_crafting': {
                'new_craft': 100.0,
                'craft_success': 10.0,
            },
            'survival': {
                'night_survived': 200.0,
                'mob_killed': 20.0,
            },
            'building': {
                'block_placed': 2.0,
                'structure_completed': 500.0,
            }
        }

        return bonuses.get(current_stage.name, {})


def create_curriculum(config: Dict[str, Any]) -> Curriculum:
    """
    Factory function to create curriculum

    Args:
        config: Configuration dictionary

    Returns:
        Curriculum instance
    """
    return Curriculum(config)
