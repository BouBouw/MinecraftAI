"""
Expert Bot for generating automatic Minecraft demonstrations

This bot plays Minecraft automatically and generates demonstrations
for imitation learning. It demonstrates:
- Movement
- Mining various blocks
- Basic crafting
- Survival behaviors

Usage:
    python generate_auto_demos.py --num_episodes 100 --output ../data/demos/auto_demos.pkl
"""

import asyncio
import pickle
import numpy as np
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List

from gym_env.minecraft_env import create_minecraft_env
from utils.config import get_config
from utils.logger import get_logger

logger = get_logger(__name__)


class ExpertMinecraftBot:
    """
    Expert Minecraft bot that generates demonstrations

    This bot demonstrates basic Minecraft skills automatically.
    """

    def __init__(self, config: Dict[str, Any], env):
        """
        Initialize expert bot

        Args:
            config: Configuration dictionary
            env: Minecraft environment
        """
        self.config = config
        self.env = env
        self.episode_count = 0

    async def generate_demonstration(self, max_steps: int = 200) -> List[Dict]:
        """
        Generate one demonstration episode

        Args:
            max_steps: Maximum steps per episode

        Returns:
            List of (obs, action, reward, next_obs, done) transitions
        """
        episode = []

        # Reset environment
        obs, info = await self.env.reset()
        if isinstance(obs, tuple):
            obs = obs[0]  # Handle if obs returns tuple

        # Get current position
        pos = obs.get('position', [0, 64, 0])

        # Sequence of actions to demonstrate
        action_sequence = self._generate_action_sequence(pos, max_steps)

        logger.info(f"📹 Generating demo episode {self.episode_count + 1} ({len(action_sequence)} steps)")

        for i, action in enumerate(action_sequence):
            # Execute action using environment's step method
            try:
                # Convert action to dict format if needed
                action_dict = {'action': action} if isinstance(action, int) else action

                # Step the environment - returns (obs, reward, terminated, truncated, info)
                result = await self.env.step(action_dict)

                # Unpack the 5-tuple
                if len(result) == 5:
                    next_obs, reward, terminated, truncated, info = result
                    done = terminated or truncated
                else:
                    # Fallback for older interface
                    next_obs, reward, done, info = result

                # Record transition
                episode.append({
                    'observation': obs,
                    'action': action,
                    'reward': reward,
                    'next_observation': next_obs,
                    'done': done,
                    'timestamp': datetime.now().isoformat()
                })

                obs = next_obs

                # Small delay between actions
                await asyncio.sleep(0.1)

                if done:
                    break

            except Exception as e:
                logger.warning(f"⚠️  Action {action} failed: {e}")
                import traceback
                logger.debug(traceback.format_exc())
                break

        self.episode_count += 1
        logger.info(f"✅ Episode {self.episode_count} generated ({len(episode)} steps)")

        return episode

    def _generate_action_sequence(self, start_pos: List[float], max_steps: int) -> List[int]:
        """
        Generate a sequence of actions for demonstration

        Args:
            start_pos: Starting position
            max_steps: Maximum steps

        Returns:
            List of action IDs
        """
        actions = []

        # Simple demonstration sequences
        sequence_type = np.random.choice([
            'mining',      # Mine blocks
            'movement',    # Move around
            'crafting',    # Basic crafting
            'survival'     # Eat when hungry
        ])

        if sequence_type == 'mining':
            # Mining sequence
            actions.extend([1, 1, 1])  # Move forward 3x
            actions.extend([27])  # Look around
            actions.extend([5])    # Jump
            actions.extend([22])  # Look down
            actions.extend([8, 8, 8, 8, 8])  # Mine 5x

        elif sequence_type == 'movement':
            # Movement sequence
            actions.extend([1, 1, 1, 1])  # Walk forward
            actions.extend([24])  # Look left
            actions.extend([1, 1])  # Walk left
            actions.extend([25])  # Look right
            actions.extend([5])  # Jump
            actions.extend([1, 1, 1])  # Walk back

        elif sequence_type == 'crafting':
            # Crafting sequence
            actions.extend([43])  # Open inventory
            actions.extend([9])   # Select slot 1 (logs)
            actions.extend([44])  # Close inventory (was 43 before)
            actions.extend([20])  # Craft planks

        elif sequence_type == 'survival':
            # Survival sequence
            actions.extend([50])  # Eat

        # Fill remaining steps with random exploration
        remaining = max_steps - len(actions)
        for _ in range(remaining):
            # Random action from basic set
            actions.append(np.random.choice([1, 5, 22, 23, 24, 25]))

        return actions[:max_steps]

    async def generate_multiple_demos(self, num_episodes: int = 100, max_steps: int = 200) -> List[Dict]:
        """
        Generate multiple demonstration episodes

        Args:
            num_episodes: Number of episodes to generate
            max_steps: Maximum steps per episode

        Returns:
            List of episodes
        """
        all_demos = []

        logger.info(f"🎬 Generating {num_episodes} demonstration episodes...")

        for i in range(num_episodes):
            try:
                episode = await self.generate_demonstration(max_steps)
                all_demos.append(episode)

                # Progress update
                if (i + 1) % 10 == 0:
                    logger.info(f"📊 Progress: {i + 1}/{num_episodes} episodes generated")

            except Exception as e:
                logger.error(f"❌ Error generating episode {i}: {e}")
                import traceback
                logger.debug(traceback.format_exc())
                continue

        logger.info(f"✅ Generated {len(all_demos)} demonstration episodes")
        return all_demos


async def generate_auto_demos_main():
    """Main function to generate automatic demonstrations"""
    import sys

    # Parse arguments
    num_episodes = 100
    config_path = '../config/rl_config.yaml'
    output_path = None

    if len(sys.argv) > 1:
        for arg in sys.argv[1:]:
            if arg.startswith('--num-episodes='):
                num_episodes = int(arg.split('=', 1)[1])
            elif arg.startswith('--config='):
                config_path = arg.split('=', 1)[1]
            elif arg.startswith('--output='):
                output_path = arg.split('=', 1)[1]

    # Generate output path if not specified
    if output_path is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = f"../data/demos/auto_demos_{timestamp}.pkl"

    # Load config
    config = get_config(config_path)

    logger.info(f"🤖 Creating Expert Bot (auto-demos)")
    logger.info(f"Episodes to generate: {num_episodes}")
    logger.info(f"Output: {output_path}")

    # Create environment
    env = await create_minecraft_env(config=config)

    # Generate demonstrations
    expert_bot = ExpertMinecraftBot(config, env)
    demos = await expert_bot.generate_multiple_demos(
        num_episodes=num_episodes,
        max_steps=200
    )

    # Save demos
    demo_data = {
        'episodes': demos,
        'episode_count': len(demos),
        'generation_method': 'automatic_expert_bot',
        'generated_at': datetime.now().isoformat(),
        'config': config
    }

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, 'wb') as f:
        pickle.dump(demo_data, f)

    logger.info(f"💾 Saved {len(demos)} episodes to {output_path}")
    logger.info(f"   Total steps: {sum(len(ep) for ep in demos)}")
    logger.info("✅ Auto-demo generation complete!")


if __name__ == "__main__":
    asyncio.run(generate_auto_demos_main())
