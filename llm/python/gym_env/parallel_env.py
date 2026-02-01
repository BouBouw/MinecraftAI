"""
Parallel Minecraft Environments
Run multiple Minecraft instances in parallel for faster training.

This allows 8+ bots to explore simultaneously, providing:
- 8x more experience per unit time
- More diverse training data
- Better generalization
- More stable learning
"""

import numpy as np
from typing import Dict, Any, Tuple, List, Optional
import concurrent.futures
import threading

from .minecraft_env import MinecraftEnv, create_minecraft_env
from bridge.minecraft_bot_bridge import MinecraftBotBridge
from utils.logger import get_logger

logger = get_logger(__name__)


class ParallelMinecraftEnv:
    """
    Vectorized environment for running multiple Minecraft instances in parallel.

    Each environment has its own:
    - WebSocket connection (different port)
    - Minecraft bot instance
    - World/episode state

    Example:
        # Create 8 parallel environments
        env = ParallelMinecraftEnv(config, num_envs=8)

        # Reset all environments
        observations, infos = env.reset()

        # Step all environments with different actions
        actions = [agent.select_action(obs) for obs in observations]
        next_obs, rewards, dones, truncateds, infos = env.step(actions)
    """

    def __init__(
        self,
        config: Dict[str, Any],
        num_envs: int = 8,
        base_port: int = 8765
    ):
        """
        Initialize parallel environments

        Args:
            config: Configuration dictionary
            num_envs: Number of parallel environments
            base_port: Starting port number (will use base_port, base_port+1, ...)
        """
        self.config = config
        self.num_envs = num_envs
        self.base_port = base_port

        logger.info(f"Initializing {num_envs} parallel Minecraft environments")
        logger.info(f"Port range: {base_port} - {base_port + num_envs - 1}")

        # Create individual environments
        self.envs = []
        for i in range(num_envs):
            port = base_port + i

            # Create bridge client for this environment
            bridge = MinecraftBotBridge(host='localhost', port=port)

            # Create environment
            env = create_minecraft_env(config, bridge_client=bridge)

            self.envs.append(env)
            logger.info(f"Environment {i}: Created on port {port}")

        # Environment state
        self._is_reset = False

        logger.info(f"All {num_envs} parallel environments initialized")

    def reset(
        self,
        seed: Optional[int] = None,
        options: Optional[Dict[str, Any]] = None
    ) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
        """
        Reset all environments

        Args:
            seed: Random seed (will be offset for each env)
            options: Reset options

        Returns:
            Tuple of (observations, infos) where each is a list of length num_envs
        """
        logger.info(f"Resetting {self.num_envs} parallel environments...")

        # Reset all environments (potentially in parallel)
        observations = []
        infos = []

        # Use thread pool for parallel reset
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.num_envs) as executor:
            # Submit all reset tasks
            futures = []
            for i, env in enumerate(self.envs):
                env_seed = seed + i if seed is not None else None
                future = executor.submit(env.reset, seed=env_seed, options=options)
                futures.append(future)

            # Collect results
            for i, future in enumerate(futures):
                obs, info = future.result(timeout=30)  # 30s timeout per env
                observations.append(obs)
                infos.append(info)
                logger.debug(f"Environment {i}: Reset complete")

        self._is_reset = True

        logger.info(f"All {self.num_envs} environments reset")

        return observations, infos

    def step(
        self,
        actions: List[int]
    ) -> Tuple[List[Dict[str, Any]], List[float], List[bool], List[bool], List[Dict[str, Any]]]:
        """
        Step all environments with corresponding actions

        Args:
            actions: List of actions, one per environment

        Returns:
            Tuple of (next_observations, rewards, dones, truncateds, infos)
            Each is a list of length num_envs
        """
        if not self._is_reset:
            raise RuntimeError("Must call reset() before step()")

        if len(actions) != self.num_envs:
            raise ValueError(f"Expected {self.num_envs} actions, got {len(actions)}")

        # Step all environments in parallel
        next_observations = [None] * self.num_envs
        rewards = [0.0] * self.num_envs
        dones = [False] * self.num_envs
        truncateds = [False] * self.num_envs
        infos = [None] * self.num_envs

        # Use thread pool for parallel step
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.num_envs) as executor:
            # Submit all step tasks
            futures = {}
            for i, (env, action) in enumerate(zip(self.envs, actions)):
                future = executor.submit(env.step, action)
                futures[future] = i

            # Collect results as they complete
            for future in concurrent.futures.as_completed(futures):
                i = futures[future]
                try:
                    next_obs, reward, done, truncated, info = future.result(timeout=10)
                    next_observations[i] = next_obs
                    rewards[i] = reward
                    dones[i] = done
                    truncateds[i] = truncated
                    infos[i] = info
                except Exception as e:
                    logger.error(f"Environment {i} step failed: {e}")
                    # Mark as done if error
                    dones[i] = True
                    next_observations[i] = self.envs[i].current_state or {}

        return next_observations, rewards, dones, truncateds, infos

    def reset_terminated(
        self,
        indices: List[int],
        seed: Optional[int] = None,
        options: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        Reset only the environments that have terminated

        Args:
            indices: Indices of environments to reset
            seed: Random seed
            options: Reset options
        """
        for i in indices:
            if i < self.num_envs:
                env_seed = seed + i if seed is not None else None
                self.envs[i].reset(seed=env_seed, options=options)
                logger.debug(f"Environment {i}: Reset (auto-reset after done)")

    def close(self):
        """Close all environments"""
        logger.info("Closing all parallel environments...")

        for i, env in enumerate(self.envs):
            try:
                if hasattr(env, 'close'):
                    env.close()
                logger.debug(f"Environment {i}: Closed")
            except Exception as e:
                logger.error(f"Error closing environment {i}: {e}")

        logger.info("All environments closed")

    def __len__(self) -> int:
        """Return number of environments"""
        return self.num_envs

    @property
    def observation_space(self):
        """Return observation space (same for all envs)"""
        return self.envs[0].observation_space if self.envs else None

    @property
    def action_space(self):
        """Return action space (same for all envs)"""
        return self.envs[0].action_space if self.envs else None


def create_parallel_env(config: Dict[str, Any], **kwargs) -> ParallelMinecraftEnv:
    """
    Factory function to create parallel environments

    Args:
        config: Configuration dictionary
        **kwargs: Additional arguments for ParallelMinecraftEnv

    Returns:
        ParallelMinecraftEnv instance
    """
    return ParallelMinecraftEnv(config, **kwargs)
