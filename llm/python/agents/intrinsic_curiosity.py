"""
Intrinsic Curiosity Module for Autonomous Minecraft Learning

Based on:
- Pathak et al. "Curiosity-driven Exploration by Self-supervised Prediction"
- Burda et al. "Exploration by Random Network Distillation"
- Tang et al. #Exploration by Random Network Distillation

The agent is intrinsically motivated to explore novel states and discover mechanics.
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
from typing import Dict, Any, Tuple
from collections import deque

from utils.logger import get_logger

logger = get_logger(__name__)


class InverseDynamicsModel(nn.Module):
    """
    Predicts the action taken to go from state s to state s'
    Learns features that are relevant to action (controllable)
    """

    def __init__(self, config: Dict[str, Any]):
        super().__init__()

        network_config = config.get('agent.network', {})
        hidden_size = network_config.get('hidden_size', 512)

        # Encode state and next state
        self.state_encoder = nn.Sequential(
            nn.Linear(1000, 256),  # Observation flattened
            nn.ReLU(),
            nn.Linear(256, 128)
        )

        # Predict action from encoded states
        self.fc = nn.Sequential(
            nn.Linear(128 * 2, 256),
            nn.ReLU(),
            nn.Linear(256, 50)  # 50 possible actions
        )

    def forward(self, state: torch.Tensor, next_state: torch.Tensor) -> torch.Tensor:
        """
        Predict action that transitioned from state to next_state

        Args:
            state: Current state [batch, obs_dim]
            next_state: Next state [batch, obs_dim]

        Returns:
            Action logits [batch, 50]
        """
        # Encode states
        feat_s = self.state_encoder(state)
        feat_sp = self.state_encoder(next_state)

        # Concatenate and predict action
        combined = torch.cat([feat_s, feat_sp], dim=-1)
        action_logits = self.fc(combined)

        return action_logits


class ForwardDynamicsModel(nn.Module):
    """
    Predicts next state feature given current state feature and action
    Used to measure prediction error (curiosity signal)
    """

    def __init__(self, config: Dict[str, Any]):
        super().__init__()

        network_config = config.get('agent.network', {})
        hidden_size = network_config.get('hidden_size', 512)

        # Encode state
        self.state_encoder = nn.Sequential(
            nn.Linear(1000, 256),
            nn.ReLU(),
            nn.Linear(256, 128)
        )

        # Predict next state feature from state + action
        self.fc = nn.Sequential(
            nn.Linear(128 + 50, 256),  # state feature + action
            nn.ReLU(),
            nn.Linear(256, 128)  # Predict next state feature
        )

    def forward(self, state: torch.Tensor, action: torch.Tensor) -> torch.Tensor:
        """
        Predict next state feature

        Args:
            state: Current state [batch, obs_dim]
            action: Action taken [batch, 50] (one-hot)

        Returns:
            Predicted next state feature [batch, 128]
        """
        feat_s = self.state_encoder(state)

        # Concatenate state feature with action
        combined = torch.cat([feat_s, action], dim=-1)

        # Predict next state feature
        pred_feat_sp = self.fc(combined)

        return pred_feat_sp


class RandomNetworkDistillation(nn.Module):
    """
    Random Network Distillation (RND) for novelty-based exploration
    Uses prediction error on randomly initialized network as novelty signal

    States rarely seen -> high prediction error -> high novelty bonus
    States often seen -> low prediction error -> low novelty bonus
    """

    def __init__(self, config: Dict[str, Any]):
        super().__init__()

        network_config = config.get('agent.network', {})
        hidden_size = network_config.get('hidden_size', 512)

        # Random target network (frozen, randomly initialized)
        self.random_target = nn.Sequential(
            nn.Linear(1000, 256),
            nn.ReLU(),
            nn.Linear(256, 128)
        )

        # Predictor network (trained to match random target)
        self.predictor = nn.Sequential(
            nn.Linear(1000, 256),
            nn.ReLU(),
            nn.Linear(256, 128)
        )

        # Freeze random target
        for param in self.random_target.parameters():
            param.requires_grad = False

    def forward(self, state: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor]:
        """
        Compute RND novelty bonus

        Args:
            state: Current state [batch, obs_dim]

        Returns:
            Tuple of (prediction_error, random_output)
        """
        # Random target output (fixed)
        random_output = self.random_target(state)

        # Predictor output (trained)
        predicted_output = self.predictor(state)

        # Prediction error = novelty signal
        prediction_error = F.mse_loss(predicted_output, random_output, reduction='none')

        return prediction_error, random_output


class CountBasedBonus:
    """
    Count-based exploration bonus
    States visited less often get higher bonus

    Uses pseudo-counts with hash table
    """

    def __init__(self, config: Dict[str, Any]):
        self.config = config

        # Hash table for state visitation counts
        self.state_counts = {}

        # Parameters
        self.beta = 0.01  # Scaling factor
        self.power = 0.5  # Power for count bonus

    def get_bonus(self, state_hash: str) -> float:
        """
        Get count-based exploration bonus

        Args:
            state_hash: Hashable representation of state

        Returns:
            Exploration bonus
        """
        # Get count (default to 0 if new state)
        count = self.state_counts.get(state_hash, 0)

        # Update count
        self.state_counts[state_hash] = count + 1

        # Compute bonus: N(s)^-power
        # New states (count=0) get bonus = 1.0
        # Often visited states get bonus -> 0
        bonus = self.beta / ((count + 1) ** self.power)

        return bonus

    def hash_state(self, observation: Dict[str, Any]) -> str:
        """
        Create hashable representation of observation

        Args:
            observation: State observation

        Returns:
            String hash
        """
        # Discretize continuous values for hashing
        position = observation.get('position', [0, 64, 0])
        if isinstance(position, list):
            # Round to nearest block
            pos_str = f"{int(position[0])}_{int(position[1])}_{int(position[2])}"
        else:
            pos_str = f"{int(position.get('x', 0))}_{int(position.get('y', 64))}_{int(position.get('z', 0))}"

        # Block in front
        block = observation.get('block_in_front', 0)
        block_str = f"block_{block}"

        # Health range
        health = observation.get('health', 20)
        if isinstance(health, list):
            health = health[0] if len(health) > 0 else 20
        health_str = f"hp_{int(health // 5)}"  # 5 HP buckets

        # Nearby entities (simplified)
        entities = observation.get('nearby_entities', [])
        entities_str = f"ent_{len(entities)}" if isinstance(entities, list) else "ent_0"

        # Time of day
        time = observation.get('time_of_day', 0)
        time_str = f"time_{int(time // 3000)}"  # 8 time periods

        return f"{pos_str}_{block_str}_{health_str}_{entities_str}_{time_str}"


class IntrinsicCuriosityModule:
    """
    Combines multiple intrinsic motivation signals:
    1. Curiosity (ICM) - prediction error of forward dynamics
    2. Novelty (RND) - prediction error on random network
    3. Count-based - bonus for rare states
    4. Information gain - bonus for reducing uncertainty
    """

    def __init__(self, config: Dict[str, Any], device: str = 'cpu'):
        self.config = config
        self.device = torch.device(device)

        # Curiosity coefficients
        curiosity_config = config.get('curiosity', {})
        self.icm_coef = curiosity_config.get('icm_scale', 0.1)
        self.rnd_coef = curiosity_config.get('rnd_scale', 0.1)
        self.count_coef = curiosity_config.get('count_scale', 0.01)

        # Create models
        self.inverse_model = InverseDynamicsModel(config).to(self.device)
        self.forward_model = ForwardDynamicsModel(config).to(self.device)
        self.rnd = RandomNetworkDistillation(config).to(self.device)

        # Optimizers
        icm_lr = curiosity_config.get('icm_lr', 0.001)
        self.icm_optimizer = torch.optim.Adam(
            list(self.inverse_model.parameters()) + list(self.forward_model.parameters()),
            lr=icm_lr
        )

        rnd_lr = curiosity_config.get('rnd_lr', 0.0001)
        self.rnd_optimizer = torch.optim.Adam(self.rnd.predictor.parameters(), lr=rnd_lr)

        # Count-based bonus
        self.count_bonus = CountBasedBonus(config)

        # Normalization statistics for RND
        self.rnd_mean = deque(maxlen=1000)
        self.rnd_std = deque(maxlen=1000)

        logger.info("Intrinsic Curiosity Module initialized")

    def compute_intrinsic_reward(
        self,
        observation: Dict[str, Any],
        next_observation: Dict[str, Any],
        action: int
    ) -> float:
        """
        Compute intrinsic reward for transition

        Args:
            observation: Current observation
            next_observation: Next observation
            action: Action taken

        Returns:
            Intrinsic reward
        """
        with torch.no_grad():
            # Convert to tensors (add batch dimension with unsqueeze)
            obs_tensor = self._obs_to_tensor(observation).unsqueeze(0).float()
            next_obs_tensor = self._obs_to_tensor(next_observation).unsqueeze(0).float()
            action_tensor = F.one_hot(torch.tensor(action), 50).float().to(self.device).unsqueeze(0)

            # 1. Curiosity bonus (ICM) - forward model prediction error
            pred_next_feat = self.forward_model(obs_tensor, action_tensor)
            actual_next_feat = self.forward_model.state_encoder(next_obs_tensor)
            curiosity_bonus = F.mse_loss(pred_next_feat, actual_next_feat)

            # 2. Novelty bonus (RND)
            rnd_error, _ = self.rnd(next_obs_tensor)

            # Normalize RND error (running statistics)
            rnd_error_mean = rnd_error.mean().item()
            self.rnd_mean.append(rnd_error_mean)

            # Compute std
            if len(self.rnd_mean) > 1:
                std = np.std(list(self.rnd_mean))
                self.rnd_std.append(std)
            else:
                std = 1.0

            # Normalized novelty bonus
            if len(self.rnd_std) > 0:
                normalized_novelty = rnd_error_mean / (self.rnd_std[-1] + 1e-8)
            else:
                normalized_novelty = rnd_error_mean

            novelty_bonus = normalized_novelty

            # 3. Count-based exploration bonus
            state_hash = self.count_bonus.hash_state(next_observation)
            count_bonus = self.count_bonus.get_bonus(state_hash)

            # Combine bonuses
            total_intrinsic = (
                self.icm_coef * curiosity_bonus.item() +
                self.rnd_coef * novelty_bonus +
                self.count_coef * count_bonus
            )

            return total_intrinsic

    def update_icm(
        self,
        observations: list,
        next_observations: list,
        actions: list
    ) -> Dict[str, float]:
        """
        Update Intrinsic Curiosity Module

        Args:
            observations: Batch of observations
            next_observations: Batch of next observations
            actions: Batch of actions

        Returns:
            Loss metrics
        """
        # Convert to tensors
        obs_tensors = torch.stack([self._obs_to_tensor(obs) for obs in observations]).to(self.device).float()
        next_obs_tensors = torch.stack([self._obs_to_tensor(obs) for obs in next_observations]).to(self.device).float()
        action_tensors = F.one_hot(torch.tensor(actions), 50).float().to(self.device)

        # Convert actions to long tensor for cross_entropy (class indices)
        action_targets = torch.tensor(actions, dtype=torch.long).to(self.device)

        # Train ICM
        self.icm_optimizer.zero_grad()

        # Inverse model loss
        pred_actions = self.inverse_model(obs_tensors, next_obs_tensors)
        inverse_loss = F.cross_entropy(pred_actions, action_targets)

        # Forward model loss
        pred_next_features = self.forward_model(obs_tensors, action_tensors)
        actual_next_features = self.forward_model.state_encoder(next_obs_tensors)
        forward_loss = F.mse_loss(pred_next_features, actual_next_features)

        # Total ICM loss
        icm_loss = inverse_loss + 0.2 * forward_loss  # Weight forward loss less

        icm_loss.backward()
        self.icm_optimizer.step()

        # Train RND
        self.rnd_optimizer.zero_grad()

        _, random_outputs = self.rnd(obs_tensors)
        predicted_outputs = self.rnd.predictor(obs_tensors)
        rnd_loss = F.mse_loss(predicted_outputs, random_outputs)

        rnd_loss.backward()
        self.rnd_optimizer.step()

        return {
            'icm_loss': icm_loss.item(),
            'inverse_loss': inverse_loss.item(),
            'forward_loss': forward_loss.item(),
            'rnd_loss': rnd_loss.item()
        }

    def _obs_to_tensor(self, observation: Dict[str, Any]) -> torch.Tensor:
        """
        Convert observation to flattened tensor

        Args:
            observation: Observation dictionary

        Returns:
            Flattened tensor [1000] (no batch dimension - will be added by stack)
        """
        # Flatten all observation values
        flat_obs = []

        for key, value in observation.items():
            if isinstance(value, np.ndarray):
                # Convert to float32 to avoid dtype issues
                flat_obs.extend(value.flatten().astype(np.float32))
            elif isinstance(value, list):
                flat_obs.extend([float(v) for v in value])
            elif isinstance(value, (int, float)):
                flat_obs.append(float(value))
            else:
                # Skip complex objects
                pass

        # Pad or truncate to 1000
        if len(flat_obs) < 1000:
            flat_obs.extend([0.0] * (1000 - len(flat_obs)))
        else:
            flat_obs = flat_obs[:1000]

        return torch.FloatTensor(flat_obs).to(self.device)

    def save(self, filepath: str):
        """Save ICM models"""
        torch.save({
            'inverse_model': self.inverse_model.state_dict(),
            'forward_model': self.forward_model.state_dict(),
            'rnd_predictor': self.rnd.predictor.state_dict(),
            'rnd_target': self.rnd.random_target.state_dict(),
            'state_counts': self.count_bonus.state_counts,
        }, filepath)
        logger.info(f"ICM saved to {filepath}")

    def load(self, filepath: str):
        """Load ICM models"""
        checkpoint = torch.load(filepath)

        self.inverse_model.load_state_dict(checkpoint['inverse_model'])
        self.forward_model.load_state_dict(checkpoint['forward_model'])
        self.rnd.predictor.load_state_dict(checkpoint['rnd_predictor'])
        self.rnd.random_target.load_state_dict(checkpoint['rnd_target'])
        self.count_bonus.state_counts = checkpoint['state_counts']

        logger.info(f"ICM loaded from {filepath}")


def create_curiosity_module(config: Dict[str, Any], device: str = 'cpu') -> IntrinsicCuriosityModule:
    """
    Factory function to create curiosity module

    Args:
        config: Configuration dictionary
        device: Device to run on

    Returns:
        IntrinsicCuriosityModule instance
    """
    return IntrinsicCuriosityModule(config, device)
