"""
Neural Network Architecture for Minecraft RL Agent.
PyTorch implementation of PPO Actor-Critic networks.
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
from typing import Dict, Any, Tuple, List
import numpy as np

from utils.config import get_config
from utils.logger import get_logger

logger = get_logger(__name__)


class MinecraftCNN(nn.Module):
    """
    CNN for processing visual data (blocks, entities)
    """

    def __init__(self, input_channels: int = 4, output_dim: int = 256):
        """
        Initialize CNN

        Args:
            input_channels: Number of input channels
            output_dim: Output feature dimension
        """
        super().__init__()

        self.features = nn.Sequential(
            # Conv block 1
            nn.Conv2d(input_channels, 32, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2),

            # Conv block 2
            nn.Conv2d(32, 64, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2),

            # Conv block 3
            nn.Conv2d(64, 128, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.AdaptiveAvgPool2d((1, 1))
        )

        self.fc = nn.Linear(128, output_dim)

    def forward(self, x):
        """
        Forward pass

        Args:
            x: Input tensor (batch, channels, height, width)

        Returns:
            Feature tensor
        """
        x = self.features(x)
        x = x.view(x.size(0), -1)
        x = self.fc(x)
        return x


class ResidualBlock(nn.Module):
    """
    Residual block with optional LayerNorm
    """
    def __init__(self, hidden_size: int, activation_fn, use_layer_norm: bool = False):
        super().__init__()

        layers = []
        if use_layer_norm:
            layers.append(nn.LayerNorm(hidden_size))
        layers.extend([
            nn.Linear(hidden_size, hidden_size),
            activation_fn
        ])

        self.layers = nn.Sequential(*layers)

    def forward(self, x):
        return x + self.layers(x)


class MinecraftEncoder(nn.Module):
    """
    Encodes different parts of the observation into a unified feature vector
    """

    def __init__(self, config: Dict[str, Any]):
        """
        Initialize encoder

        Args:
            config: Configuration dictionary
        """
        super().__init__()

        self.config = config
        network_config = config.get('agent.network', {})

        hidden_size = network_config.get('hidden_size', 512)
        num_layers = network_config.get('num_layers', 3)
        use_layer_norm = network_config.get('use_layer_norm', False)
        use_residual = network_config.get('use_residual', False)
        activation = network_config.get('activation', 'relu')

        # Store for forward method
        self.use_residual = use_residual

        # Choose activation function
        if activation == 'leaky_relu':
            activation_fn = nn.LeakyReLU(0.01)
        elif activation == 'tanh':
            activation_fn = nn.Tanh()
        else:  # relu
            activation_fn = nn.ReLU()

        # Get observation config to determine input sizes
        obs_config = config.get('observation_space', {})
        visible_blocks_count = obs_config.get('visible_blocks_count', 100)
        nearby_entities_count = obs_config.get('nearby_entities_count', 10)

        # Position encoder
        position_layers = [
            nn.Linear(3, 64),
            activation_fn,
        ]
        if use_layer_norm:
            position_layers.append(nn.LayerNorm(64))
        position_layers.extend([
            nn.Linear(64, 64),
            activation_fn
        ])
        self.position_encoder = nn.Sequential(*position_layers)

        # Inventory encoder
        inventory_layers = [
            nn.Linear(36 * 2, 256),
            activation_fn,
        ]
        if use_layer_norm:
            inventory_layers.append(nn.LayerNorm(256))
        inventory_layers.extend([
            nn.Linear(256, 256),
            activation_fn
        ])
        self.inventory_encoder = nn.Sequential(*inventory_layers)

        # Visual encoder (for blocks and entities)
        visual_input_size = visible_blocks_count * 4 + nearby_entities_count * 4
        visual_layers = [
            nn.Linear(visual_input_size, 512),
            activation_fn,
        ]
        if use_layer_norm:
            visual_layers.append(nn.LayerNorm(512))
        visual_layers.extend([
            nn.Linear(512, 256),
            activation_fn
        ])
        self.visual_encoder = nn.Sequential(*visual_layers)

        # Environment encoder
        env_layers = [
            nn.Linear(9, 64),
            activation_fn,
        ]
        if use_layer_norm:
            env_layers.append(nn.LayerNorm(64))
        env_layers.extend([
            nn.Linear(64, 64),
            activation_fn
        ])
        self.env_encoder = nn.Sequential(*env_layers)

        # Feature fusion
        total_features = 64 + 256 + 256 + 64  # position + inventory + visual + env
        fusion_layers = [
            nn.Linear(total_features, hidden_size),
            activation_fn
        ]
        if use_layer_norm:
            fusion_layers.append(nn.LayerNorm(hidden_size))
        self.fusion = nn.Sequential(*fusion_layers)

        # Additional layers with optional residual connections
        if use_residual:
            self.additional_layers = self._build_residual_layers(hidden_size, num_layers, activation_fn, use_layer_norm)
        else:
            layers = []
            for _ in range(num_layers - 1):
                layer_list = [
                    nn.Linear(hidden_size, hidden_size),
                    activation_fn
                ]
                if use_layer_norm:
                    layer_list.append(nn.LayerNorm(hidden_size))
                layers.extend(layer_list)
            self.additional_layers = nn.Sequential(*layers)

    def _build_residual_layers(self, hidden_size: int, num_layers: int, activation_fn, use_layer_norm: bool):
        """Build layers with residual connections"""
        layers = []
        for _ in range(num_layers - 1):
            layers.append(ResidualBlock(hidden_size, activation_fn, use_layer_norm))
        return nn.Sequential(*layers)

    def forward(self, observations: Dict[str, torch.Tensor]) -> torch.Tensor:
        """
        Encode observations into feature vector

        Args:
            observations: Dictionary of observation tensors

        Returns:
            Feature tensor
        """
        # Encode position
        pos = observations.get('position', torch.zeros(1, 3))
        pos_features = self.position_encoder(pos)

        # Encode inventory
        inv = observations.get('inventory', torch.zeros(1, 72))
        inv_features = self.inventory_encoder(inv)

        # Encode visual (blocks + entities)
        blocks = observations.get('visible_blocks', torch.zeros(1, 400))
        entities = observations.get('nearby_entities', torch.zeros(1, 40))
        visual = torch.cat([blocks.flatten(1), entities.flatten(1)], dim=1)
        visual_features = self.visual_encoder(visual)

        # Encode environment
        env_features = torch.cat([
            observations.get('health', torch.zeros(1, 1)),
            observations.get('food', torch.zeros(1, 1)),
            observations.get('saturation', torch.zeros(1, 1)),
            observations.get('time_of_day', torch.zeros(1, 1)).float() / 24000,
            observations.get('is_raining', torch.zeros(1, 1)).float(),
            observations.get('on_ground', torch.zeros(1, 1)).float(),
            observations.get('in_water', torch.zeros(1, 1)).float(),
            observations.get('hotbar_selected', torch.zeros(1, 1)).float() / 9,
            observations.get('block_in_front', torch.zeros(1, 1)).float() / 1000,  # Block type in front
        ], dim=1)
        env_features = self.env_encoder(env_features)

        # Fuse all features
        combined = torch.cat([
            pos_features,
            inv_features,
            visual_features,
            env_features
        ], dim=-1)

        features = self.fusion(combined)
        features = self.additional_layers(features)

        return features


class ActorNetwork(nn.Module):
    """
    Actor network (policy) for PPO
    Outputs action probabilities
    """

    def __init__(self, config: Dict[str, Any]):
        """
        Initialize actor network

        Args:
            config: Configuration dictionary
        """
        super().__init__()

        self.config = config
        network_config = config.get('agent.network', {})
        hidden_size = network_config.get('hidden_size', 512)

        # Encoder
        self.encoder = MinecraftEncoder(config)

        # Actor head - output 50 actions for all possible action types
        self.actor = nn.Sequential(
            nn.Linear(hidden_size, hidden_size),
            nn.ReLU(),
            nn.Linear(hidden_size, 50)  # 50 action types (0-49)
        )

        # Initialize weights
        self._initialize_weights()

    def _initialize_weights(self):
        """Initialize network weights"""
        for module in self.modules():
            if isinstance(module, nn.Linear):
                nn.init.orthogonal_(module.weight, gain=0.01)
                nn.init.constant_(module.bias, 0)

    def forward(self, observations: Dict[str, torch.Tensor]) -> torch.Tensor:
        """
        Forward pass

        Args:
            observations: Dictionary of observation tensors

        Returns:
            Action logits
        """
        features = self.encoder(observations)
        logits = self.actor(features)
        return logits

    def get_action_probs(self, observations: Dict[str, torch.Tensor]) -> torch.Tensor:
        """
        Get action probabilities

        Args:
            observations: Dictionary of observation tensors

        Returns:
            Action probabilities
        """
        logits = self.forward(observations)
        probs = F.softmax(logits, dim=-1)
        return probs

    def get_action_log_probs(self, observations: Dict[str, torch.Tensor]) -> torch.Tensor:
        """
        Get action log probabilities

        Args:
            observations: Dictionary of observation tensors

        Returns:
            Action log probabilities
        """
        logits = self.forward(observations)
        log_probs = F.log_softmax(logits, dim=-1)
        return log_probs


class CriticNetwork(nn.Module):
    """
    Critic network (value function) for PPO
    Estimates state value
    """

    def __init__(self, config: Dict[str, Any]):
        """
        Initialize critic network

        Args:
            config: Configuration dictionary
        """
        super().__init__()

        self.config = config
        network_config = config.get('agent.network', {})
        hidden_size = network_config.get('hidden_size', 512)

        # Encoder (share architecture with actor)
        self.encoder = MinecraftEncoder(config)

        # Critic head
        self.critic = nn.Sequential(
            nn.Linear(hidden_size, hidden_size),
            nn.ReLU(),
            nn.Linear(hidden_size, 1)
        )

        # Initialize weights
        self._initialize_weights()

    def _initialize_weights(self):
        """Initialize network weights"""
        for module in self.modules():
            if isinstance(module, nn.Linear):
                nn.init.orthogonal_(module.weight, gain=1.0)
                nn.init.constant_(module.bias, 0)

    def forward(self, observations: Dict[str, torch.Tensor]) -> torch.Tensor:
        """
        Forward pass

        Args:
            observations: Dictionary of observation tensors

        Returns:
            State value
        """
        features = self.encoder(observations)
        value = self.critic(features)
        return value


class PPOModel(nn.Module):
    """
    Combined PPO Actor-Critic Model
    """

    def __init__(self, config: Dict[str, Any]):
        """
        Initialize PPO model

        Args:
            config: Configuration dictionary
        """
        super().__init__()

        self.config = config

        # Actor and Critic
        self.actor = ActorNetwork(config)
        self.critic = CriticNetwork(config)

        logger.info("PPO Model initialized")

    def forward(
        self,
        observations: Dict[str, torch.Tensor]
    ) -> Tuple[torch.Tensor, torch.Tensor]:
        """
        Forward pass through both actor and critic

        Args:
            observations: Dictionary of observation tensors

        Returns:
            Tuple of (action logits, state value)
        """
        logits = self.actor(observations)
        value = self.critic(observations)
        return logits, value

    def get_action(self, observations: Dict[str, torch.Tensor]) -> int:
        """
        Sample an action from the policy

        Args:
            observations: Dictionary of observation tensors

        Returns:
            Action ID
        """
        with torch.no_grad():
            logits = self.actor(observations)
            probs = F.softmax(logits, dim=-1)
            action = torch.multinomial(probs, 1).item()

        return action

    def evaluate_actions(
        self,
        observations: Dict[str, torch.Tensor],
        actions: torch.Tensor,
        available_actions: List[int] = None
    ) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
        """
        Evaluate actions for PPO update

        Args:
            observations: Dictionary of observation tensors
            actions: Actions taken
            available_actions: List of available action IDs (for masking)

        Returns:
            Tuple of (log_probs, values, entropy)
        """
        logits = self.actor(observations)
        values = self.critic(observations)

        # Apply softmax to get probabilities
        probs = F.softmax(logits, dim=-1)
        log_probs = F.log_softmax(logits, dim=-1)

        # Mask unavailable actions if provided
        if available_actions is not None and len(available_actions) < 50:
            # Create mask (0 for unavailable, 1 for available)
            mask = torch.zeros_like(probs)
            for action_id in available_actions:
                mask[:, action_id] = 1.0

            # Apply mask to probabilities
            probs = probs * mask

            # Re-normalize
            prob_sum = probs.sum(dim=-1, keepdim=True)
            probs = probs / (prob_sum + 1e-8)

            # Recalculate log_probs from masked probabilities
            log_probs = torch.log(probs + 1e-8)

        # Get log probs for taken actions
        action_log_probs = log_probs.gather(1, actions.unsqueeze(1)).squeeze(1)

        # Calculate entropy (only over available actions)
        entropy = -(probs * log_probs).sum(dim=-1)

        return action_log_probs, values.squeeze(-1), entropy

    def save(self, filepath: str):
        """
        Save model weights

        Args:
            filepath: Path to save file
        """
        torch.save({
            'actor_state_dict': self.actor.state_dict(),
            'critic_state_dict': self.critic.state_dict(),
            'config': self.config
        }, filepath)

        logger.info(f"Model saved to {filepath}")

    def load(self, filepath: str):
        """
        Load model weights

        Args:
            filepath: Path to load file
        """
        checkpoint = torch.load(filepath)

        self.actor.load_state_dict(checkpoint['actor_state_dict'])
        self.critic.load_state_dict(checkpoint['critic_state_dict'])

        logger.info(f"Model loaded from {filepath}")

    def to(self, device):
        """Move model to device"""
        self.actor = self.actor.to(device)
        self.critic = self.critic.to(device)
        return self


def create_ppo_model(config: Dict[str, Any]) -> PPOModel:
    """
    Factory function to create PPO model

    Args:
        config: Configuration dictionary

    Returns:
        PPOModel instance
    """
    return PPOModel(config)
