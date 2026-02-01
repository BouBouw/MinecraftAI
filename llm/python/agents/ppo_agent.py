"""
PPO Agent - Proximal Policy Optimization implementation for Minecraft RL.
Main agent class for training and inference.
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torch.distributions import Categorical
import numpy as np
from typing import Dict, Any, List, Tuple, Optional
from collections import deque
from pathlib import Path

from .network import PPOModel, create_ppo_model
from memory.memory_manager import MemoryManager
from utils.config import get_config
from utils.logger import get_logger

logger = get_logger(__name__)


class RolloutBuffer:
    """
    Buffer for storing rollout data
    """

    def __init__(self, capacity: int = 2048):
        """
        Initialize rollout buffer

        Args:
            capacity: Buffer capacity
        """
        self.capacity = capacity
        self.observations = []
        self.actions = []
        self.log_probs = []
        self.rewards = []
        self.values = []
        self.dones = []

    def push(
        self,
        observation: Dict[str, Any],
        action: int,
        log_prob: float,
        reward: float,
        value: float,
        done: bool
    ):
        """
        Add transition to buffer

        Args:
            observation: State observation
            action: Action taken
            log_prob: Log probability of action
            reward: Reward received
            value: Estimated state value
            done: Whether episode is done
        """
        self.observations.append(observation)
        self.actions.append(action)
        self.log_probs.append(log_prob)
        self.rewards.append(reward)
        self.values.append(value)
        self.dones.append(done)

    def get_returns(self, gamma: float = 0.99, lam: float = 0.95) -> List[float]:
        """
        Calculate returns using GAE (Generalized Advantage Estimation)

        Args:
            gamma: Discount factor
            lam: GAE parameter

        Returns:
            List of returns
        """
        returns = []
        advantages = []

        last_value = 0
        last_advantage = 0

        for t in reversed(range(len(self.rewards))):
            if t == len(self.rewards) - 1:
                next_value = 0
                next_non_terminal = 1.0 - self.dones[t]
            else:
                next_value = self.values[t + 1]
                next_non_terminal = 1.0 - self.dones[t]

            delta = self.rewards[t] + gamma * next_value * next_non_terminal - self.values[t]
            advantages.insert(0, last_advantage = delta + gamma * lam * next_non_terminal * last_advantage)
            returns.insert(0, last_value = advantages[0] + self.values[t])

        return returns

    def sample(self, batch_size: int):
        """
        Sample a random batch from buffer

        Args:
            batch_size: Size of batch

        Returns:
            Sampled data
        """
        indices = np.random.permutation(len(self.observations))[:batch_size]

        return (
            [self.observations[i] for i in indices],
            [self.actions[i] for i in indices],
            [self.log_probs[i] for i in indices],
            [self.values[i] for i in indices],
            [self.dones[i] for i in indices],
            indices
        )

    def __len__(self):
        return len(self.observations)


class PPOAgent:
    """
    PPO Agent for Minecraft RL

    Implements Proximal Policy Optimization algorithm:
    - Actor-Critic architecture
    - Clipped surrogate objective
    - GAE advantage estimation
    - Multiple epochs per update
    """

    def __init__(
        self,
        config: Dict[str, Any],
        memory_manager: MemoryManager = None,
        device: str = 'cpu'
    ):
        """
        Initialize PPO agent

        Args:
            config: Configuration dictionary
            memory_manager: Memory manager instance
            device: Device to run on (cpu or cuda)
        """
        self.config = config
        self.memory = memory_manager
        self.device = torch.device(device)

        # PPO hyperparameters
        agent_config = config.get('agent', {})
        self.learning_rate = agent_config.get('learning_rate', 0.0003)
        self.gamma = agent_config.get('gamma', 0.99)
        self.gae_lambda = agent_config.get('gae_lambda', 0.95)
        self.clip_range = agent_config.get('clip_range', 0.2)
        self.entropy_coef = agent_config.get('entropy_coef', 0.01)
        self.vf_coef = agent_config.get('vf_coef', 0.5)
        self.max_grad_norm = agent_config.get('max_grad_norm', 0.5)

        # Training parameters
        training_config = config.get('training', {})
        self.batch_size = training_config.get('batch_size', 64)
        self.n_steps = training_config.get('n_steps', 2048)
        self.n_epochs = training_config.get('n_epochs', 10)

        # Create networks
        self.model = create_ppo_model(config).to(self.device)
        self.optimizer = optim.Adam(self.model.parameters(), lr=self.learning_rate)

        # Rollout buffer
        self.rollout_buffer = RolloutBuffer(self.n_steps)

        # Training stats
        self.episode_rewards = deque(maxlen=100)
        self.episode_lengths = deque(maxlen=100)

        # Current episode tracking
        self.current_episode_reward = 0
        self.current_episode_length = 0

        logger.info(f"PPO Agent initialized on {device}")

    def select_action(self, observation: Dict[str, Any]) -> Tuple[int, float, float]:
        """
        Select action using current policy

        Args:
            observation: Current observation

        Returns:
            Tuple of (action, log_prob, value)
        """
        # Convert observation to tensors
        obs_tensors = self._observation_to_tensors(observation)

        with torch.no_grad():
            logits = self.model.actor(obs_tensors)
            probs = F.softmax(logits, dim=-1)
            dist = Categorical(probs)
            action = dist.sample()
            log_prob = dist.log_prob(action)
            value = self.model.critic(obs_tensors)

        return action.item(), log_prob.item(), value.item()

    def _observation_to_tensors(self, observation: Dict[str, Any]) -> Dict[str, torch.Tensor]:
        """
        Convert observation dictionary to tensors

        Args:
            observation: Observation dictionary

        Returns:
            Dictionary of tensors with shape [1, features]
        """
        tensors = {}

        for key, value in observation.items():
            if isinstance(value, np.ndarray):
                tensors[key] = torch.FloatTensor(value).unsqueeze(0).to(self.device)
            elif isinstance(value, (int, float)):
                # Create 2D tensor [1, 1] for scalars
                tensors[key] = torch.FloatTensor([[value]]).to(self.device)
            else:
                # Create 2D tensor [1, features] for lists
                tensors[key] = torch.FloatTensor(value).unsqueeze(0).to(self.device)

        return tensors

    def update(self) -> Dict[str, float]:
        """
        Update policy using PPO algorithm

        Returns:
            Dictionary with training metrics
        """
        if len(self.rollout_buffer) < self.batch_size:
            return {}

        # Calculate returns
        returns = self.rollout_buffer.get_returns(
            gamma=self.gamma,
            lam=self.gae_lambda
        )

        # Convert to tensors
        observations = self.rollout_buffer.observations
        actions = torch.tensor(self.rollout_buffer.actions).to(self.device)
        old_log_probs = torch.tensor(self.rollout_buffer.log_probs).to(self.device)
        old_values = torch.tensor(self.rollout_buffer.values).to(self.device)
        returns_tensor = torch.tensor(returns).to(self.device)

        # Normalize advantages
        advantages = returns_tensor - old_values
        advantages = (advantages - advantages.mean()) / (advantages.std() + 1e-8)

        # Multiple epochs
        total_policy_loss = 0
        total_value_loss = 0
        total_entropy = 0
        updates = 0

        for epoch in range(self.n_epochs):
            # Create mini-batches
            batch_size = min(self.batch_size, len(observations))
            indices = np.random.permutation(len(observations))

            for start in range(0, len(observations), batch_size):
                end = start + batch_size
                batch_indices = indices[start:end]

                # Get batch data
                batch_obs = [observations[i] for i in batch_indices]
                batch_actions = actions[batch_indices]
                batch_old_log_probs = old_log_probs[batch_indices]
                batch_old_values = old_values[batch_indices]
                batch_returns = returns_tensor[batch_indices]
                batch_advantages = advantages[batch_indices]

                # Evaluate current policy
                obs_tensors_list = [self._observation_to_tensors(obs) for obs in batch_obs]

                # Stack tensors
                stacked_obs = {}
                for key in obs_tensors_list[0].keys():
                    stacked_obs[key] = torch.cat([obs[key] for obs in obs_tensors_list], dim=0)

                log_probs, values, entropy = self.model.evaluate_actions(stacked_obs, batch_actions)

                # Calculate ratio
                ratio = torch.exp(log_probs - batch_old_log_probs)

                # PPO clip loss
                surr1 = ratio * batch_advantages
                surr2 = torch.clamp(ratio, 1.0 - self.clip_range, 1.0 + self.clip_range) * batch_advantages
                policy_loss = -torch.min(surr1, surr2).mean()

                # Value loss
                value_loss = F.mse_loss(values, batch_returns)

                # Entropy bonus
                entropy_loss = -entropy.mean()

                # Total loss
                loss = policy_loss + self.vf_coef * value_loss + self.entropy_coef * entropy_loss

                # Optimize
                self.optimizer.zero_grad()
                loss.backward()
                nn.utils.clip_grad_norm_(self.model.parameters(), self.max_grad_norm)
                self.optimizer.step()

                total_policy_loss += policy_loss.item()
                total_value_loss += value_loss.item()
                total_entropy += entropy.item()
                updates += 1

        # Clear buffer
        self.rollout_buffer = RolloutBuffer(self.n_steps)

        # Return metrics
        return {
            'policy_loss': total_policy_loss / updates if updates > 0 else 0,
            'value_loss': total_value_loss / updates if updates > 0 else 0,
            'entropy': total_entropy / updates if updates > 0 else 0,
            'mean_reward': np.mean(self.episode_rewards) if self.episode_rewards else 0,
            'mean_length': np.mean(self.episode_lengths) if self.episode_lengths else 0,
        }

    def store_transition(
        self,
        observation: Dict[str, Any],
        action: int,
        log_prob: float,
        reward: float,
        value: float,
        done: bool
    ):
        """
        Store transition in rollout buffer

        Args:
            observation: State observation
            action: Action taken
            log_prob: Log probability of action
            reward: Reward received
            value: Estimated state value
            done: Whether episode is done
        """
        self.rollout_buffer.push(observation, action, log_prob, reward, value, done)

        # Track episode stats
        self.current_episode_reward += reward
        self.current_episode_length += 1

        if done:
            self.episode_rewards.append(self.current_episode_reward)
            self.episode_lengths.append(self.current_episode_length)
            self.current_episode_reward = 0
            self.current_episode_length = 0

    def save_model(self, filepath: str):
        """
        Save model weights

        Args:
            filepath: Path to save
        """
        self.model.save(filepath)
        logger.info(f"Model saved to {filepath}")

    def load_model(self, filepath: str):
        """
        Load model weights

        Args:
            filepath: Path to load from
        """
        self.model.load(filepath)
        logger.info(f"Model loaded from {filepath}")

    def get_statistics(self) -> Dict[str, Any]:
        """
        Get agent statistics

        Returns:
            Dictionary with statistics
        """
        return {
            'mean_reward': np.mean(self.episode_rewards) if self.episode_rewards else 0,
            'std_reward': np.std(self.episode_rewards) if len(self.episode_rewards) > 1 else 0,
            'mean_length': np.mean(self.episode_lengths) if self.episode_lengths else 0,
            'total_episodes': len(self.episode_rewards),
            'buffer_size': len(self.rollout_buffer),
        }

    def set_training_mode(self, training: bool):
        """
        Set training mode

        Args:
            training: Whether to train
        """
        self.model.train(training)

    def __repr__(self) -> str:
        stats = self.get_statistics()
        return f"PPOAgent(episodes={stats['total_episodes']}, mean_reward={stats['mean_reward']:.2f})"


def create_ppo_agent(
    config: Dict[str, Any],
    memory_manager: MemoryManager = None,
    device: str = 'cpu'
) -> PPOAgent:
    """
    Factory function to create PPO agent

    Args:
        config: Configuration dictionary
        memory_manager: Memory manager instance
        device: Device to run on

    Returns:
        PPOAgent instance
    """
    return PPOAgent(config, memory_manager, device)
