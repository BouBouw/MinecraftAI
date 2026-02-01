"""
Prioritized Experience Replay (PER) for Minecraft RL

Based on:
- Schaul et al. "Prioritized Experience Replay" (ICLR 2016)

Key idea:
Not all transitions are equally important. Transitions with high TD-error
(prediction error) are more surprising and provide more learning signal.

By prioritizing these transitions, the agent learns more efficiently from
its mistakes, leading to 2-3x faster learning.

Example:
- Boring transition: Walking in safe area → Low TD-error → Sampled rarely
- Important transition: Almost died fighting zombie → High TD-error → Sampled often!
"""

import numpy as np
import torch
from typing import Dict, Any, List, Tuple, Optional
from collections import namedtuple
import heapq
import random

from utils.logger import get_logger

logger = get_logger(__name__)

# Transition namedtuple for easy storage
Transition = namedtuple('Transition', [
    'observation', 'action', 'reward', 'next_observation', 'done',
    'td_error', 'priority'
])


class PrioritizedReplayBuffer:
    """
    Prioritized Experience Replay Buffer

    Uses proportional prioritization with importance sampling correction.
    """

    def __init__(
        self,
        capacity: int = 100000,
        alpha: float = 0.6,  # Priority exponent (0 = uniform, 1 = full prioritization)
        beta: float = 0.4,   # Importance sampling exponent (annealed to 1)
        beta_increment: float = 0.001,
        epsilon: float = 1e-6  # Small constant to ensure non-zero priority
    ):
        """
        Initialize prioritized replay buffer

        Args:
            capacity: Maximum number of transitions
            alpha: How much prioritization to use (0 = uniform, 1 = full)
            beta: Importance sampling correction (annealed during training)
            beta_increment: How much to increase beta each step
            epsilon: Small constant to avoid zero priority
        """
        self.capacity = capacity
        self.alpha = alpha
        self.beta = beta
        self.beta_increment = beta_increment
        self.epsilon = epsilon

        # Storage
        self.buffer: List[Transition] = []
        self.priorities = np.zeros((capacity,), dtype=np.float32)
        self.pos = 0
        self.size = 0

        # Max priority for new transitions (optimistic initialization)
        self.max_priority = 1.0

        logger.info(f"Prioritized Replay Buffer initialized: capacity={capacity}")

    def store_transition(
        self,
        observation: Dict[str, Any],
        action: int,
        reward: float,
        next_observation: Dict[str, Any],
        done: bool,
        td_error: Optional[float] = None
    ):
        """
        Store a transition with priority

        Args:
            observation: Current observation
            action: Action taken
            reward: Reward received
            next_observation: Next observation
            done: Whether episode ended
            td_error: TD-error for this transition (if None, use max priority)
        """
        # Create transition
        transition = Transition(
            observation=observation,
            action=action,
            reward=reward,
            next_observation=next_observation,
            done=done,
            td_error=td_error,
            priority=0.0  # Will be set below
        )

        # Add to buffer
        if self.size < self.capacity:
            self.buffer.append(transition)
            self.size += 1
        else:
            self.buffer[self.pos] = transition

        # Set priority (use max priority if TD-error not provided)
        if td_error is None:
            priority = self.max_priority
        else:
            priority = (abs(td_error) + self.epsilon) ** self.alpha

        self.priorities[self.pos] = priority
        self.max_priority = max(self.max_priority, priority)

        # Update position
        self.pos = (self.pos + 1) % self.capacity

    def sample(self, batch_size: int) -> Tuple[List[Transition], np.ndarray, np.ndarray]:
        """
        Sample a batch of transitions with proportional prioritization

        Args:
            batch_size: Number of transitions to sample

        Returns:
            Tuple of (transitions, indices, weights)
            - transitions: List of sampled transitions
            - indices: Indices in buffer (for updating priorities)
            - weights: Importance sampling weights
        """
        if self.size == 0:
            return [], np.array([]), np.array([])

        # Calculate sampling probabilities
        probs = self.priorities[:self.size] / self.priorities[:self.size].sum()

        # Sample indices
        indices = np.random.choice(self.size, batch_size, p=probs)

        # Get transitions
        transitions = [self.buffer[idx] for idx in indices]

        # Calculate importance sampling weights
        weights = (self.size * probs[indices]) ** (-self.beta)
        weights = weights / weights.max()  # Normalize

        # Anneal beta
        self.beta = min(1.0, self.beta + self.beta_increment)

        return transitions, indices, weights

    def update_priorities(self, indices: np.ndarray, td_errors: np.ndarray):
        """
        Update priorities for sampled transitions

        Args:
            indices: Indices of transitions to update
            td_errors: New TD-errors for these transitions
        """
        for idx, td_error in zip(indices, td_errors):
            priority = (abs(td_error) + self.epsilon) ** self.alpha
            self.priorities[idx] = priority
            self.max_priority = max(self.max_priority, priority)

    def __len__(self) -> int:
        """Return buffer size"""
        return self.size


class PrioritizedExperienceReplay:
    """
    Prioritized Experience Replay for Minecraft

    Integrates with PPO to provide more efficient learning from
    important experiences (high TD-error transitions).
    """

    def __init__(self, config: Dict[str, Any]):
        """
        Initialize PER

        Args:
            config: Configuration dictionary
        """
        self.config = config
        per_config = config.get('training', {}).get('priority_replay', {})

        self.enabled = per_config.get('enabled', False)
        self.buffer_size = per_config.get('buffer_size', 100000)
        self.alpha = per_config.get('alpha', 0.6)
        self.beta = per_config.get('beta', 0.4)
        self.beta_increment = per_config.get('beta_increment', 0.001)

        if self.enabled:
            self.buffer = PrioritizedReplayBuffer(
                capacity=self.buffer_size,
                alpha=self.alpha,
                beta=self.beta,
                beta_increment=self.beta_increment
            )
            logger.info("🎯 Prioritized Experience Replay: ENABLED")
            logger.info(f"   Buffer size: {self.buffer_size}")
            logger.info(f"   Alpha: {self.alpha}, Beta: {self.beta}")
        else:
            self.buffer = None
            logger.info("🎯 Prioritized Experience Replay: DISABLED")

    def store_transition(
        self,
        observation: Dict[str, Any],
        action: int,
        reward: float,
        next_observation: Dict[str, Any],
        done: bool,
        td_error: Optional[float] = None
    ):
        """
        Store a transition in prioritized buffer

        Args:
            observation: Current observation
            action: Action taken
            reward: Reward received
            next_observation: Next observation
            done: Whether episode ended
            td_error: TD-error for prioritization (optional)
        """
        if self.enabled and self.buffer:
            self.buffer.store_transition(
                observation, action, reward, next_observation, done, td_error
            )

    def sample_prioritized_batch(self, batch_size: int) -> Optional[Tuple]:
        """
        Sample a batch with prioritization

        Args:
            batch_size: Batch size

        Returns:
            Tuple of (transitions, indices, weights) or None
        """
        if self.enabled and self.buffer and len(self.buffer) > 0:
            return self.buffer.sample(batch_size)
        return None

    def update_priorities(self, indices: np.ndarray, td_errors: np.ndarray):
        """
        Update priorities after learning

        Args:
            indices: Indices of sampled transitions
            td_errors: New TD-errors
        """
        if self.enabled and self.buffer:
            self.buffer.update_priorities(indices, td_errors)

    def get_statistics(self) -> Dict[str, Any]:
        """
        Get PER statistics

        Returns:
            Dictionary of statistics
        """
        stats = {
            'enabled': self.enabled,
            'buffer_size': len(self.buffer) if self.buffer else 0,
            'beta': self.buffer.beta if self.buffer else 0.0,
            'max_priority': self.buffer.max_priority if self.buffer else 0.0
        }
        return stats


def create_priority_replay(config: Dict[str, Any]) -> PrioritizedExperienceReplay:
    """
    Factory function to create PER module

    Args:
        config: Configuration dictionary

    Returns:
        PrioritizedExperienceReplay instance
    """
    return PrioritizedExperienceReplay(config)
