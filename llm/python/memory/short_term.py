"""
Short-term memory for Minecraft RL agent.
Stores recent actions, observations, and rewards in RAM.
"""

import numpy as np
from collections import deque
from typing import Dict, Any, List, Tuple, Optional
from dataclasses import dataclass

from utils.config import get_config
from utils.logger import get_logger

logger = get_logger(__name__)


@dataclass
class MemoryTransition:
    """A single transition (state, action, reward, next_state)"""
    state: Dict[str, Any]
    action: Dict[str, Any]
    reward: float
    next_state: Dict[str, Any]
    done: bool
    timestamp: float


class ShortTermMemory:
    """
    Short-term memory (STM) - stores recent experience in RAM

    Features:
    - Fast access to recent transitions
    - Sliding window of N most recent experiences
    - Context window for agent decision making
    - Efficient sampling for training batches
    """

    def __init__(self, capacity: int = 1000, context_window: int = 50):
        """
        Initialize short-term memory

        Args:
            capacity: Maximum number of transitions to store
            context_window: Size of context window for retrieval
        """
        config = get_config()
        self.capacity = config.get('memory.short_term.capacity', capacity)
        self.context_window = config.get('memory.short_term.context_window', context_window)

        # Deques for efficient append/pop from both ends
        self.states = deque(maxlen=self.capacity)
        self.actions = deque(maxlen=self.capacity)
        self.rewards = deque(maxlen=self.capacity)
        self.dones = deque(maxlen=self.capacity)

        # Episode tracking
        self.episode_starts = []  # Indices where episodes start

        logger.debug(f"Short-term memory initialized (capacity={self.capacity})")

    def remember(
        self,
        state: Dict[str, Any],
        action: Dict[str, Any],
        reward: float,
        done: bool
    ):
        """
        Store a transition in short-term memory

        Args:
            state: Current state observation
            action: Action taken
            reward: Reward received
            done: Whether episode is done
        """
        # Store in deques
        self.states.append(state)
        self.actions.append(action)
        self.rewards.append(reward)
        self.dones.append(done)

        # Track episode boundaries
        if done and len(self.episode_starts) > 0:
            # Mark next index as new episode start
            self.episode_starts.append(len(self.states))

        logger.debug(
            f"STM: Stored transition (reward={reward:.2f}, done={done}), "
            f"size={len(self.states)}/{self.capacity}"
        )

    def get_recent_context(self, n: int = None) -> Tuple[List, List, List, List]:
        """
        Get recent context (last n transitions)

        Args:
            n: Number of recent transitions to retrieve. If None, uses context_window

        Returns:
            Tuple of (states, actions, rewards, dones)
        """
        if n is None:
            n = self.context_window

        n = min(n, len(self.states))

        states = list(self.states)[-n:]
        actions = list(self.actions)[-n:]
        rewards = list(self.rewards)[-n:]
        dones = list(self.dones)[-n:]

        return states, actions, rewards, dones

    def get_recent_states(self, n: int = None) -> List[Dict[str, Any]]:
        """
        Get recent states only

        Args:
            n: Number of recent states

        Returns:
            List of recent states
        """
        if n is None:
            n = self.context_window

        n = min(n, len(self.states))
        return list(self.states)[-n:]

    def get_recent_actions(self, n: int = None) -> List[Dict[str, Any]]:
        """
        Get recent actions only

        Args:
            n: Number of recent actions

        Returns:
            List of recent actions
        """
        if n is None:
            n = self.context_window

        n = min(n, len(self.actions))
        return list(self.actions)[-n:]

    def sample_batch(self, batch_size: int) -> List[MemoryTransition]:
        """
        Sample a random batch of transitions

        Args:
            batch_size: Size of batch to sample

        Returns:
            List of MemoryTransition objects
        """
        if len(self.states) < batch_size:
            batch_size = len(self.states)

        # Sample random indices
        indices = np.random.choice(len(self.states), batch_size, replace=False)

        batch = []
        for idx in indices:
            # Get next state (handle end of episode)
            if idx + 1 < len(self.states):
                next_state = self.states[idx + 1]
            else:
                next_state = self.states[idx]  # Use current state as next state

            transition = MemoryTransition(
                state=self.states[idx],
                action=self.actions[idx],
                reward=self.rewards[idx],
                next_state=next_state,
                done=self.dones[idx],
                timestamp=0  # Could add timestamp tracking
            )
            batch.append(transition)

        return batch

    def get_sequence(self, length: int) -> Optional[List[MemoryTransition]]:
        """
        Get a continuous sequence of transitions

        Useful for RNN/LSTM training

        Args:
            length: Length of sequence

        Returns:
            List of transitions or None if not enough data
        """
        if len(self.states) < length:
            return None

        # Get most recent sequence that doesn't cross episode boundary
        end_idx = len(self.states) - 1

        # Find start of current episode
        start_idx = 0
        for episode_start in reversed(self.episode_starts):
            if episode_start <= end_idx - length + 1:
                start_idx = episode_start
                break

        # Ensure we don't cross episode boundary
        if end_idx - start_idx + 1 < length:
            # Not enough data in current episode
            return None

        # Build sequence
        sequence = []
        for idx in range(start_idx, start_idx + length):
            if idx + 1 < len(self.states):
                next_state = self.states[idx + 1]
            else:
                next_state = self.states[idx]

            transition = MemoryTransition(
                state=self.states[idx],
                action=self.actions[idx],
                reward=self.rewards[idx],
                next_state=next_state,
                done=self.dones[idx],
                timestamp=0
            )
            sequence.append(transition)

        return sequence

    def mark_episode_start(self):
        """Mark the current position as the start of a new episode"""
        self.episode_starts.append(len(self.states))
        logger.debug("Episode start marked")

    def get_episode_transitions(self, episode_idx: int = -1) -> List[MemoryTransition]:
        """
        Get all transitions from a specific episode

        Args:
            episode_idx: Episode index (-1 for current episode)

        Returns:
            List of transitions
        """
        if len(self.episode_starts) == 0:
            # All data is from one episode
            start_idx = 0
            end_idx = len(self.states) - 1
        elif episode_idx == -1:
            # Current episode
            start_idx = self.episode_starts[-1] if self.episode_starts else 0
            end_idx = len(self.states) - 1
        else:
            # Specific episode
            start_idx = self.episode_starts[episode_idx]
            end_idx = (self.episode_starts[episode_idx + 1] - 1
                      if episode_idx + 1 < len(self.episode_starts)
                      else len(self.states) - 1)

        transitions = []
        for idx in range(start_idx, end_idx + 1):
            if idx + 1 <= end_idx:
                next_state = self.states[idx + 1]
            else:
                next_state = self.states[idx]

            transition = MemoryTransition(
                state=self.states[idx],
                action=self.actions[idx],
                reward=self.rewards[idx],
                next_state=next_state,
                done=self.dones[idx] or idx == end_idx,
                timestamp=0
            )
            transitions.append(transition)

        return transitions

    def clear(self):
        """Clear all short-term memory"""
        self.states.clear()
        self.actions.clear()
        self.rewards.clear()
        self.dones.clear()
        self.episode_starts.clear()
        logger.debug("Short-term memory cleared")

    def size(self) -> int:
        """Get current size of memory"""
        return len(self.states)

    def is_full(self) -> bool:
        """Check if memory is at capacity"""
        return len(self.states) >= self.capacity

    def get_statistics(self) -> Dict[str, Any]:
        """
        Get statistics about short-term memory

        Returns:
            Dictionary with statistics
        """
        if len(self.rewards) == 0:
            return {
                'size': 0,
                'capacity': self.capacity,
                'utilization': 0.0
            }

        rewards_list = list(self.rewards)

        return {
            'size': len(self.states),
            'capacity': self.capacity,
            'utilization': len(self.states) / self.capacity,
            'total_reward': sum(rewards_list),
            'average_reward': np.mean(rewards_list),
            'min_reward': min(rewards_list),
            'max_reward': max(rewards_list),
            'std_reward': np.std(rewards_list),
            'num_episodes': len(self.episode_starts) + (1 if len(self.states) > 0 else 0),
            'episode_starts': self.episode_starts.copy()
        }

    def __len__(self) -> int:
        """Get current size of memory"""
        return len(self.states)

    def __repr__(self) -> str:
        return f"ShortTermMemory(size={len(self.states)}/{self.capacity}, episodes={len(self.episode_starts)})"
