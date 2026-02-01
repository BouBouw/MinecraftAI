"""
Minecraft RL Environment - Gymnasium interface
Main environment class that integrates observations, actions, and rewards.
"""

import gymnasium as gym
from gymnasium import spaces
import numpy as np
from typing import Dict, Any, Tuple, Optional, List
import time

from .observations import ObservationSpace, create_observation_space
from .actions import ActionSpace, ActionType, create_action_space
from .rewards import RewardSystem, CurriculumRewardShaper, create_reward_system
from utils.logger import get_logger

logger = get_logger(__name__)


class MinecraftEnv(gym.Env):
    """
    Minecraft Reinforcement Learning Environment

    A Gymnasium-compatible environment for training RL agents in Minecraft.
    Connects to the Node.js bridge which interfaces with the Mineflayer bot.
    """

    # Metadata for Gymnasium compatibility
    metadata = {
        'render_modes': ['human', 'rgb_array'],
        'render_fps': 20,
    }

    def __init__(self, config: Dict[str, Any], curriculum=None, bridge_client=None):
        """
        Initialize Minecraft environment

        Args:
            config: Configuration dictionary
            curriculum: Curriculum object (optional)
            bridge_client: Client for communicating with Node.js bridge
        """
        super().__init__()

        self.config = config
        self.bridge = bridge_client
        self.curriculum = curriculum  # Store curriculum object

        # Initialize components
        self.observation_space_impl = create_observation_space(config)
        self.action_space_impl = create_action_space(config)
        self.reward_system = create_reward_system(config)
        self.reward_shaper = CurriculumRewardShaper(config)

        # Set Gymnasium spaces
        self.observation_space = self.observation_space_impl.space
        self.action_space = self.action_space_impl.space

        # Environment state
        self.current_state: Optional[Dict[str, Any]] = None
        self.episode_id = 0
        self.step_count = 0
        self.episode_rewards: List[float] = []
        self.done = False

        # Curriculum stage
        self.current_stage = 0
        self.curriculum_stages = config.get('training.curriculum.stages', [])
        self.available_actions = ActionType.get_basic_actions()

    def reset(
        self,
        seed: Optional[int] = None,
        options: Optional[Dict[str, Any]] = None
    ) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """
        Reset the environment

        Args:
            seed: Random seed
            options: Additional options

        Returns:
            Tuple of (observation, info)
        """
        super().reset(seed=seed)

        # Reset episode tracking
        self.episode_id += 1
        self.step_count = 0
        self.done = False
        self.reward_system.reset()

        # Request reset from bridge
        if self.bridge:
            try:
                # Connect bridge if not already connected
                if not self.bridge.connected:
                    import asyncio
                    try:
                        # Try to connect to the bridge
                        loop = asyncio.get_event_loop()
                        if loop.is_running():
                            # If loop is running, create task
                            asyncio.create_task(self.bridge.connect())
                        else:
                            # If loop is not running, run directly
                            loop.run_until_complete(self.bridge.connect())
                    except RuntimeError:
                        # No event loop, create new one
                        asyncio.run(self.bridge.connect())

                # Get initial state via async bridge
                import asyncio
                try:
                    loop = asyncio.get_event_loop()
                    if loop.is_running():
                        # Can't wait in running loop, use default state
                        logger.warning("Event loop is running, using default state")
                        self.current_state = self._create_default_state()
                    else:
                        self.current_state = loop.run_until_complete(self.bridge.reset_environment())
                except RuntimeError:
                    # No event loop, create new one
                    self.current_state = asyncio.run(self.bridge.reset_environment())

            except Exception as e:
                logger.error(f"Error resetting environment via bridge: {e}")
                # Create default state
                self.current_state = self._create_default_state()
        else:
            # No bridge - use mock state for testing
            logger.warning("No bridge provided - using mock state for testing")
            self.current_state = self._create_default_state()

        # Create observation
        observation = self.observation_space_impl.create_observation(self.current_state)

        # Info dictionary
        # Get stage name from curriculum object if available, otherwise fallback to config
        stage_name = 'unknown'
        if self.curriculum:
            stage_obj = self.curriculum.get_current_stage()
            if stage_obj:
                stage_name = stage_obj.name
        elif self.current_stage < len(self.curriculum_stages):
            stage_name = self.curriculum_stages[self.current_stage].get('name', 'unknown')

        info = {
            'episode_id': self.episode_id,
            'stage': stage_name,
        }

        return observation, info

    def step(
        self,
        action: Dict[str, Any]
    ) -> Tuple[Dict[str, Any], float, bool, bool, Dict[str, Any]]:
        """
        Execute one step in the environment

        Args:
            action: Action to execute

        Returns:
            Tuple of (observation, reward, terminated, truncated, info)
        """
        self.step_count += 1

        # Execute action via bridge
        if self.bridge:
            try:
                import asyncio
                try:
                    loop = asyncio.get_event_loop()
                    if loop.is_running():
                        # Can't wait in running loop, simulate instead
                        logger.warning("Event loop is running, simulating action")
                        next_state = self._simulate_action(action, self.current_state)
                        success = True
                    else:
                        next_state, success = loop.run_until_complete(self.bridge.execute_action(action, self.current_state))
                except RuntimeError:
                    # No event loop, create new one
                    result = asyncio.run(self.bridge.execute_action(action, self.current_state))
                    next_state, success = result
            except Exception as e:
                logger.error(f"Error executing action via bridge: {e}")
                next_state = self.current_state
                success = False
        else:
            # No bridge - simulate action
            logger.warning("No bridge provided - simulating action")
            next_state = self._simulate_action(action, self.current_state)
            success = True

        # Create observations
        next_observation = self.observation_space_impl.create_observation(next_state)

        # Calculate reward
        reward = self.reward_system.calculate_reward(
            self.current_state,
            action,
            next_state,
            False  # not done yet
        )

        # Apply curriculum reward shaping
        # Get stage name from curriculum object if available
        stage_name = ''
        if self.curriculum:
            stage_obj = self.curriculum.get_current_stage()
            if stage_obj:
                stage_name = stage_obj.name
        elif self.current_stage < len(self.curriculum_stages):
            stage_name = self.curriculum_stages[self.current_stage].get('name', '')

        if stage_name:
            reward = self.reward_shaper.shape_reward(reward, stage_name)

        # Check termination conditions
        terminated = self._check_termination(next_state)
        truncated = self._check_truncation()

        # Update state
        self.current_state = next_state
        self.episode_rewards.append(reward)

        # Info dictionary
        info = {
            'episode_id': self.episode_id,
            'step': self.step_count,
            'action_success': success,
            'reward_statistics': self.reward_system.get_statistics(),
        }

        # Reset if done
        if terminated or truncated:
            self.done = True
            # Add completion reward
            completion_reward = self.reward_system._episode_completion_reward(next_state)
            reward += completion_reward
            info['completion_reward'] = completion_reward

            # Check curriculum transition
            if self.reward_shaper.should_transition(self.episode_rewards):
                self._advance_curriculum()

        return next_observation, reward, terminated, truncated, info

    def _check_termination(self, state: Dict[str, Any]) -> bool:
        """Check if episode should terminate"""
        # Death
        if state.get('health', 20) <= 0:
            return True

        # Goal achieved (stage-specific)
        # This would be customized based on curriculum stage

        return False

    def _check_truncation(self) -> bool:
        """Check if episode should be truncated (timeout)"""
        # Max episode length
        max_steps = self.curriculum_stages[self.current_stage].get('max_steps', 10000) if self.current_stage < len(self.curriculum_stages) else 10000

        return self.step_count >= max_steps

    def _advance_curriculum(self):
        """Advance to next curriculum stage"""
        if self.current_stage < len(self.curriculum_stages) - 1:
            self.current_stage += 1
            stage_config = self.curriculum_stages[self.current_stage]
            stage_name = stage_config.get('name', 'unknown')

            print(f"\n{'='*60}")
            print(f"Advancing to curriculum stage {self.current_stage}: {stage_name}")
            print(f"{'='*60}\n")

            # Update available actions
            self.available_actions = self.action_space_impl.filter_actions_by_stage(stage_name)

            # Update reward shaper
            self.reward_shaper.set_stage(self.current_stage)

    def _create_default_state(self) -> Dict[str, Any]:
        """Create default state for testing without bridge"""
        return {
            'position': {'x': 0, 'y': 64, 'z': 0},
            'rotation': {'yaw': 0, 'pitch': 0},
            'velocity': {'dx': 0, 'dy': 0, 'dz': 0},
            'on_ground': True,
            'in_water': False,
            'health': 20,
            'food': 20,
            'saturation': 20,
            'inventory': [],
            'hotbar_selected': 0,
            'visible_blocks': [],
            'nearby_entities': [],
            'time_of_day': 0,
            'is_raining': False,
            'biome_id': 1,
            'held_item': 0,
            'armor': {'head': 0, 'chest': 0, 'legs': 0, 'feet': 0},
        }

    def _simulate_action(self, action: Dict[str, Any], state: Dict[str, Any]) -> Dict[str, Any]:
        """Simulate action for testing without bridge"""
        # Very simple simulation - just return the same state
        # In a real implementation, this would modify state based on action
        return state.copy()

    def render(self):
        """Render the environment (optional)"""
        # Rendering would be handled by the Minecraft client
        pass

    def close(self):
        """Clean up environment resources"""
        if self.bridge:
            try:
                self.bridge.close()
            except Exception as e:
                print(f"Error closing bridge: {e}")

    def get_episode_statistics(self) -> Dict[str, Any]:
        """Get statistics for the current episode"""
        return {
            'episode_id': self.episode_id,
            'step_count': self.step_count,
            'total_reward': sum(self.episode_rewards),
            'average_reward': np.mean(self.episode_rewards) if self.episode_rewards else 0,
            'reward_statistics': self.reward_system.get_statistics(),
            'curriculum_stage': self.current_stage,
        }

    def __repr__(self) -> str:
        return f"MinecraftEnv(episode={self.episode_id}, stage={self.current_stage})"


def create_minecraft_env(config: Dict[str, Any], curriculum=None, bridge_client=None) -> MinecraftEnv:
    """
    Factory function to create Minecraft environment

    Args:
        config: Configuration dictionary
        curriculum: Curriculum object (optional)
        bridge_client: Bridge client for communication

    Returns:
        MinecraftEnv instance
    """
    return MinecraftEnv(config, curriculum, bridge_client)
