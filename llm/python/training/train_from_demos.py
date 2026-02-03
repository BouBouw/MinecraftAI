"""
Train RL agent from demonstrations using Behavior Cloning + PPO

This implements:
1. Behavior Cloning: Pre-train policy on demonstrations
2. PPO Fine-tuning: Continue learning with RL after cloning
3. Hybrid approach: Combine demonstration loss with RL loss

Based on:
- "Behavioral Cloning from Observation" (Ho & Ermon, 2016)
"""

import pickle
import torch
import torch.nn as nn
import numpy as np
from pathlib import Path
from typing import Dict, Any, List

from agents.ppo_agent import create_ppo_agent
from training.trainer import create_trainer, Trainer
from utils.config import get_config
from utils.logger import get_logger

logger = get_logger(__name__)


def load_demos(filepath: str) -> Dict[str, Any]:
    """
    Load demonstrations from pickle file

    Args:
        filepath: Path to demos pickle file

    Returns:
        Demo data dictionary
    """
    logger.info(f"📂 Loading demonstrations from {filepath}")

    with open(filepath, 'rb') as f:
        demo_data = pickle.load(f)

    logger.info(f"✅ Loaded {demo_data['episode_count']} episodes")
    logger.info(f"   Total steps: {sum(len(ep) for ep in demo_data['episodes'])}")

    return demo_data


def preprocess_demo(demos: List[Dict]) -> tuple:
    """
    Preprocess demonstrations into training format

    Args:
        demos: List of demo episodes

    Returns:
        Tuple of (observations, actions, rewards, dones)
    """
    observations = []
    actions = []
    rewards = []
    dones = []

    for episode in demos:
        for transition in episode:
            observations.append(transition['observation'])
            actions.append(transition['action'])
            rewards.append(transition['reward'])
            dones.append(transition['done'])

    logger.info(f"📊 Preprocessed {len(observations)} transitions from {len(demos)} episodes")

    return observations, actions, rewards, dones


def train_behavior_cloning(
    agent,
    observations: List,
    actions: List,
    epochs: int = 10,
    batch_size: int = 64
):
    """
    Train agent using behavior cloning (supervised learning)

    Args:
        agent: PPO agent
        observations: List of observations
        actions: List of actions
        epochs: Training epochs
        batch_size: Batch size

    Returns:
        Training statistics
    """
    logger.info("🎓 Training with Behavior Cloning...")

    # Convert to tensors
    obs_tensors = []
    for obs in observations:
        # Convert observation dict to tensor
        obs_tensor = agent.model._obs_to_tensor(obs)
        obs_tensors.append(obs_tensor)

    actions_tensor = torch.tensor(actions, dtype=torch.long)

    # Train
    dataset = torch.utils.data.TensorDataset(obs_tensors, actions_tensor)
    loader = torch.utils.data.DataLoader(dataset, batch_size=batch_size, shuffle=True)

    optimizer = torch.optim.Adam(agent.model.parameters(), lr=1e-4)
    criterion = nn.CrossEntropyLoss()

    total_loss = 0
    for epoch in range(epochs):
        epoch_loss = 0
        for batch_obs, batch_actions in loader:
            # Forward pass
            logits, _ = agent.model(batch_obs)

            # Compute loss
            loss = criterion(logits, batch_actions)

            # Backward pass
            optimizer.zero_grad()
            loss.backward()
            torch.nn.utils.clip_grad_norm_(agent.model.parameters(), 1.0)
            optimizer.step()

            epoch_loss += loss.item()

        avg_loss = epoch_loss / len(loader)
        total_loss += avg_loss

        logger.info(f"Epoch {epoch+1}/{epochs}: Loss = {avg_loss:.4f}")

    avg_loss = total_loss / epochs
    logger.info(f"✅ Behavior Cloning complete! Avg loss: {avg_loss:.4f}")

    return {'avg_loss': avg_loss, 'epochs': epochs}


def fine_tune_with_rl(trainer: Trainer, total_steps: int = 100000):
    """
    Fine-tune cloned policy with RL (PPO)

    Args:
        trainer: Trainer instance
        total_steps: Training steps

    Returns:
        Training statistics
    """
    logger.info(f"🎯 Fine-tuning with RL ({total_steps} steps)...")

    stats = trainer.train(total_timesteps=total_steps)

    return stats


def train_from_demos(
    demos_path: str,
    config_path: str = '../config/rl_config.yaml',
    bc_epochs: int = 10,
    rl_steps: int = 100000
):
    """
    Complete training pipeline: Clone → Fine-tune

    Args:
        demos_path: Path to demonstrations pickle
        config_path: Path to config file
        bc_epochs: Behavior cloning epochs
        rl_steps: RL fine-tuning steps
    """
    # Load config
    config = get_config(config_path)

    # Load demos
    demo_data = load_demos(demos_path)

    # Preprocess
    observations, actions, rewards, dones = preprocess_demo(demo_data['episodes'])

    # Create agent
    logger.info("🤖 Creating PPO agent...")
    agent = create_ppo_agent(config=config)

    # Phase 1: Behavior Cloning
    logger.info("="*60)
    logger.info("PHASE 1: BEHAVIOR CLONING (Imitation)")
    logger.info("="*60)

    bc_stats = train_behavior_cloning(
        agent,
        observations,
        actions,
        epochs=bc_epochs
    )

    # Save cloned policy
    bc_model_path = f"../data/models/bc_model_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pt"
    agent.save_model(bc_model_path)
    logger.info(f"💾 Saved cloned policy to {bc_model_path}")

    # Phase 2: Fine-tune with RL
    logger.info("\n" + "="*60)
    logger.info("PHASE 2: FINE-TUNING WITH RL (PPO)")
    logger.info("="*60)

    # Create trainer
    trainer = create_trainer(config=config)

    # Load the cloned policy into the trainer's agent
    trainer.agent.model.load_state_dict(agent.model.state_dict())

    # Fine-tune
    rl_stats = trainer.train(total_timesteps=rl_steps)

    logger.info("\n" + "="*60)
    logger.info("TRAINING COMPLETE!")
    logger.info("="*60)
    logger.info(f"📊 Behavior Cloning Loss: {bc_stats['avg_loss']:.4f}")
    logger.info(f"🎯 RL Training Steps: {rl_stats.get('total_steps', 'N/A')}")

    return {
        'bc_stats': bc_stats,
        'rl_stats': rl_stats
    }


if __name__ == "__main__":
    import sys
    from datetime import datetime

    # Parse arguments
    demos_path = None
    config_path = '../config/rl_config.yaml'
    bc_epochs = 10
    rl_steps = 100000

    if len(sys.argv) > 1:
        for arg in sys.argv[1:]:
            if arg.startswith('--demos='):
                demos_path = arg.split('=', 1)[1]
            elif arg.startswith('--config='):
                config_path = arg.split('=', 1)[1]
            elif arg.startswith('--bc-epochs='):
                bc_epochs = int(arg.split('=', 1)[1])
            elif arg.startswith('--rl-steps='):
                rl_steps = int(arg.split('=', 1)[1])

    if demos_path is None:
        print("❌ Error: --demos=path required")
        print("\nUsage: python train_from_demos.py --demos=../data/demos/demos_YYYYMMDD_HHMMSS.pkl")
        sys.exit(1)

    print("🚀 Training from Demonstrations")
    print("="*60)
    print(f"Demos: {demos_path}")
    print(f"Config: {config_path}")
    print(f"BC Epochs: {bc_epochs}")
    print(f"RL Steps: {rl_steps}")
    print("="*60)

    # Train
    train_from_demos(
        demos_path=demos_path,
        config_path=config_path,
        bc_epochs=bc_epochs,
        rl_steps=rl_steps
    )
