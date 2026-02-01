"""
Reward Normalization and Clipping for Stable Training

Based on:
- Common RL best practices for reward scaling

Key ideas:
1. Reward Clipping: Limit rewards to [-10, 10] to prevent extreme values
2. Reward Normalization: Normalize rewards using running statistics
3. Returns Normalization: Normalize episode returns for more stable updates

This prevents the network from being destabilized by extreme reward values
and leads to more stable, faster convergence.
"""

import numpy as np
from typing import Dict, Any, Optional
from collections import deque

from utils.logger import get_logger

logger = get_logger(__name__)


class RewardNormalizer:
    """
    Normalize rewards using running mean and std
    """

    def __init__(
        self,
        enabled: bool = True,
        clip_range: float = 10.0,  # Clip rewards to [-clip_range, clip_range]
        normalize: bool = True,  # Normalize rewards using running stats
        window_size: int = 1000  # Window for running statistics
    ):
        """
        Initialize reward normalizer

        Args:
            enabled: Whether to enable normalization
            clip_range: Maximum absolute reward value
            normalize: Whether to normalize using running statistics
            window_size: Size of rolling window for statistics
        """
        self.enabled = enabled
        self.clip_range = clip_range
        self.normalize = normalize
        self.window_size = window_size

        # Running statistics
        self.reward_history = deque(maxlen=window_size)
        self.running_mean = 0.0
        self.running_std = 1.0
        self.count = 0

        logger.info(f"Reward Normalizer initialized: enabled={enabled}, clip_range={clip_range}")

    def normalize_reward(self, reward: float) -> float:
        """
        Normalize and clip a reward

        Args:
            reward: Raw reward

        Returns:
            Normalized and clipped reward
        """
        if not self.enabled:
            return reward

        # Update running statistics
        self.reward_history.append(reward)
        self.count += 1

        if self.normalize and len(self.reward_history) > 10:
            # Update running statistics
            self.running_mean = np.mean(list(self.reward_history))
            self.running_std = np.std(list(self.reward_history)) + 1e-8  # Avoid division by zero

            # Normalize
            normalized = (reward - self.running_mean) / (self.running_std + 1e-8)
        else:
            normalized = reward

        # Clip to prevent extreme values
        clipped = np.clip(normalized, -self.clip_range, self.clip_range)

        return clipped

    def get_statistics(self) -> Dict[str, float]:
        """Get normalization statistics"""
        return {
            'running_mean': self.running_mean,
            'running_std': self.running_std,
            'count': self.count,
            'window_size': len(self.reward_history)
        }


class ReturnNormalizer:
    """
    Normalize episode returns (discounted sum of rewards)
    More effective than per-reward normalization for RL
    """

    def __init__(
        self,
        enabled: bool = True,
        gamma: float = 0.99,
        clip_range: float = 20.0,  # Higher clip for returns
        window_size: int = 100
    ):
        """
        Initialize return normalizer

        Args:
            enabled: Whether to enable normalization
            gamma: Discount factor
            clip_range: Maximum absolute return value
            window_size: Size of rolling window
        """
        self.enabled = enabled
        self.gamma = gamma
        self.clip_range = clip_range
        self.window_size = window_size

        # Running statistics for returns
        self.return_history = deque(maxlen=window_size)
        self.running_mean = 0.0
        self.running_std = 1.0

        # Current episode return
        self.current_episode_return = 0.0

        logger.info(f"Return Normalizer initialized: enabled={enabled}, gamma={gamma}")

    def add_reward(self, reward: float, done: bool) -> Optional[float]:
        """
        Add reward to current episode return and normalize if episode done

        Args:
            reward: Reward received
            done: Whether episode ended

        Returns:
            Normalized return if episode done, None otherwise
        """
        if not self.enabled:
            if done:
                self.current_episode_return = 0.0
            return None

        # Add to current return
        self.current_episode_return = self.gamma * self.current_episode_return + reward

        if done:
            # Episode ended, normalize the return
            normalized_return = self._normalize_return(self.current_episode_return)

            # Reset for next episode
            self.current_episode_return = 0.0

            return normalized_return

        return None

    def _normalize_return(self, return_value: float) -> float:
        """Normalize a return value"""
        # Update history
        self.return_history.append(return_value)

        # Compute running statistics
        if len(self.return_history) > 10:
            self.running_mean = np.mean(list(self.return_history))
            self.running_std = np.std(list(self.return_history)) + 1e-8

            # Normalize
            normalized = (return_value - self.running_mean) / (self.running_std + 1e-8)
        else:
            normalized = return_value

        # Clip
        clipped = np.clip(normalized, -self.clip_range, self.clip_range)

        return clipped

    def normalize_value(self, value: float) -> float:
        """
        Normalize a value estimate using the same statistics as returns

        Args:
            value: Value estimate

        Returns:
            Normalized value
        """
        if not self.enabled or len(self.return_history) < 10:
            return value

        # Normalize value using same statistics as returns
        normalized = (value - self.running_mean) / (self.running_std + 1e-8)
        clipped = np.clip(normalized, -self.clip_range, self.clip_range)

        return clipped

    def get_statistics(self) -> Dict[str, float]:
        """Get normalization statistics"""
        return {
            'running_mean': self.running_mean,
            'running_std': self.running_std,
            'window_size': len(self.return_history)
        }


class RewardNormalizationSystem:
    """
    Combined reward normalization system

    Integrates reward clipping, reward normalization, and return normalization
    for maximum training stability.
    """

    def __init__(self, config: Dict[str, Any]):
        """
        Initialize reward normalization system

        Args:
            config: Configuration dictionary
        """
        norm_config = config.get('training', {}).get('reward_normalization', {})

        self.enabled = norm_config.get('enabled', True)

        # Reward normalizer
        self.reward_normalizer = RewardNormalizer(
            enabled=self.enabled,
            clip_range=norm_config.get('reward_clip_range', 10.0),
            normalize=norm_config.get('normalize_rewards', True),
            window_size=norm_config.get('reward_window_size', 1000)
        )

        # Return normalizer
        self.return_normalizer = ReturnNormalizer(
            enabled=self.enabled,
            gamma=config.get('agent', {}).get('gamma', 0.99),
            clip_range=norm_config.get('return_clip_range', 20.0),
            window_size=norm_config.get('return_window_size', 100)
        )

        if self.enabled:
            logger.info("📊 Reward Normalization System: ENABLED")
            logger.info(f"   Reward clipping: ±{norm_config.get('reward_clip_range', 10.0)}")
            logger.info(f"   Return clipping: ±{norm_config.get('return_clip_range', 20.0)}")
        else:
            logger.info("📊 Reward Normalization System: DISABLED")

    def normalize_reward(self, reward: float) -> float:
        """
        Normalize and clip a reward

        Args:
            reward: Raw reward

        Returns:
            Normalized reward
        """
        return self.reward_normalizer.normalize_reward(reward)

    def process_step(self, reward: float, done: bool) -> Dict[str, Any]:
        """
        Process a step: normalize reward and track returns

        Args:
            reward: Raw reward
            done: Whether episode ended

        Returns:
            Dictionary with normalized reward and other info
        """
        # Normalize reward
        normalized_reward = self.normalize_reward(reward)

        # Update return normalizer
        normalized_return = self.return_normalizer.add_reward(normalized_reward, done)

        return {
            'normalized_reward': normalized_reward,
            'normalized_return': normalized_return,
            'episode_done': done
        }

    def normalize_value(self, value: float) -> float:
        """
        Normalize a value estimate

        Args:
            value: Value estimate

        Returns:
            Normalized value
        """
        return self.return_normalizer.normalize_value(value)

    def get_statistics(self) -> Dict[str, Any]:
        """Get system statistics"""
        return {
            'reward_normalizer': self.reward_normalizer.get_statistics(),
            'return_normalizer': self.return_normalizer.get_statistics()
        }


def create_reward_normalization(config: Dict[str, Any]) -> RewardNormalizationSystem:
    """
    Factory function to create reward normalization system

    Args:
        config: Configuration dictionary

    Returns:
        RewardNormalizationSystem instance
    """
    return RewardNormalizationSystem(config)
