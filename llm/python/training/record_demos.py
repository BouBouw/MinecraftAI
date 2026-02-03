"""
Demonstration Recorder for Minecraft RL Agent

Records human gameplay demonstrations for imitation learning.

Usage:
    # Start recording
    python record_demos.py --config ../config/rl_config.yaml

    # Play Minecraft! The recorder will capture:
    # - Observations (what you see)
    # - Actions (what you do)
    # - Rewards (optional, for manual labeling)
"""

import asyncio
import json
import pickle
import numpy as np
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List, Tuple

from bridge.minecraft_bot_bridge import MinecraftBotBridge
from gym_env.observations import ObservationSpace
from gym_env.actions import ActionSpace
from utils.config import get_config
from utils.logger import get_logger

logger = get_logger(__name__)


class DemoRecorder:
    """
    Records gameplay demonstrations for imitation learning

    Captures observation-action pairs during human gameplay.
    """

    def __init__(self, config: Dict[str, Any], bridge: MinecraftBotBridge):
        """
        Initialize demo recorder

        Args:
            config: Configuration dictionary
            bridge: Minecraft bot bridge
        """
        self.config = config
        self.bridge = bridge
        self.observation_space = ObservationSpace(config)
        self.action_space = ActionSpace(config)

        # Storage
        self.demos = []  # List of (observation, action, reward) tuples
        self.current_episode = []
        self.episode_count = 0

        # Recording metadata
        self.recording_start = None

        logger.info("📹 Demo Recorder initialized")

    async def start_recording(self):
        """Start recording demonstrations"""
        logger.info("📹 Starting demonstration recording...")
        logger.info("🎮 Play Minecraft now! Your actions will be recorded.")
        logger.info("🛑 Type 'stop' when done recording")

        self.recording_start = datetime.now()
        self.current_episode = []

        # Connect to bot
        if not self.bridge.connected:
            await self.bridge.connect()

        # Start observation loop
        await self._recording_loop()

    async def _recording_loop(self):
        """Main recording loop - continuously captures observations"""
        try:
            while True:
                # Get current observation
                obs = await self.bridge.get_observation()

                # Wait for human action (via console input)
                action = await self._get_human_action(obs)

                if action == "stop":
                    # Save episode and stop recording
                    if len(self.current_episode) > 0:
                        self.demos.append(list(self.current_episode))
                        self.episode_count += 1
                        logger.info(f"✅ Episode {self.episode_count} saved ({len(self.current_episode)} steps)")
                    break

                # Execute action
                next_obs, reward, done, info = await self.bridge.execute_action(action)

                # Record transition
                self.current_episode.append({
                    'observation': obs,
                    'action': action,
                    'reward': reward,
                    'next_observation': next_obs,
                    'done': done,
                    'timestamp': datetime.now().isoformat()
                })

                # Episode ended?
                if done:
                    if len(self.current_episode) > 0:
                        self.demos.append(list(self.current_episode))
                        self.episode_count += 1
                        logger.info(f"✅ Episode {self.episode_count} saved ({len(self.current_episode)} steps)")
                    self.current_episode = []

                # Small delay to avoid overwhelming the system
                await asyncio.sleep(0.05)

        except KeyboardInterrupt:
            logger.info("⏸️ Recording interrupted by user")
            if len(self.current_episode) > 0:
                self.demos.append(list(self.current_episode))
                self.episode_count += 1
                logger.info(f"✅ Episode {self.episode_count} saved ({len(self.current_episode)} steps)")

    async def _get_human_action(self, observation: Dict[str, Any]) -> int:
        """
        Get action from human player via console

        Args:
            observation: Current observation

        Returns:
            Action ID
        """
        # Show observation summary to guide player
        if observation:
            pos = observation.get('position', [0, 0, 0])
            health = observation.get('health', 0)
            inv = observation.get('inventory', [])
            logger.info(f"📍 Position: [{pos[0]:.1f}, {pos[1]:.1f}, {pos[2]:.1f}] | Health: {health:.0f} | Inventory: {len(inv)} items")

        # Simple console input for actions
        print("\n" + "="*60)
        print("Available actions:")
        print("  0-49: Action ID (see actions.txt for full list)")
        print("  h: Show this help")
        print("  s: Show observation details")
        print("  stop: Stop recording")
        print("="*60)

        while True:
            try:
                cmd = input("\nAction (or command): ").strip().lower()

                if cmd == 'stop':
                    return "stop"
                elif cmd == 'h':
                    self._show_action_help()
                elif cmd == 's':
                    self._show_observation_details(observation)
                elif cmd.isdigit():
                    action_id = int(cmd)
                    if 0 <= action_id < 50:
                        return action_id
                    else:
                        print("❌ Invalid action ID (0-49)")
                else:
                    print("❌ Invalid command")

            except (EOFError, KeyboardInterrupt):
                return "stop"

    def _show_action_help(self):
        """Show action help"""
        print("\n📖 Common Actions:")
        print("  Movement:")
        print("    0: No-op / Idle")
        print("    1: Move Forward")
        print("    2: Move Backward")
        print("    3: Move Left")
        print("    4: Move Right")
        print("    5: Jump")
        print("  Mining/Combat:")
        print("    6: Attack (click left)")
        print("    7: Use Item (click right)")
        print("    8: Mine Block (click & hold)")
        print("  Inventory:")
        print("    9-18: Select hotbar slot 1-9")
        print("  Vision:")
        print("    19-27: Look actions")
        print("    28: Look At (specific coordinate)")
        print("\n💡 Tip: Start with basic actions (1=forward, 5=jump, 8=mine)")

    def _show_observation_details(self, observation: Dict[str, Any]):
        """Show detailed observation"""
        print("\n📊 Observation Details:")
        for key, value in observation.items():
            if isinstance(value, np.ndarray):
                print(f"  {key}: shape={value.shape}, dtype={value.dtype}")
                if len(value) < 20:
                    print(f"    values: {value}")
            elif isinstance(value, list):
                print(f"  {key}: length={len(value)}")
                if len(value) < 10:
                    print(f"    values: {value}")
            else:
                print(f"  {key}: {value}")

    def save_demos(self, filepath: str):
        """
        Save recorded demonstrations to file

        Args:
            filepath: Path to save demos
        """
        demo_data = {
            'episodes': self.demos,
            'episode_count': self.episode_count,
            'recording_start': self.recording_start.isoformat() if self.recording_start else None,
            'recording_end': datetime.now().isoformat(),
            'config': self.config
        }

        output_path = Path(filepath)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, 'wb') as f:
            pickle.dump(demo_data, f)

        logger.info(f"💾 Saved {self.episode_count} demonstrations to {output_path}")
        logger.info(f"   Total steps: {sum(len(ep) for ep in self.demos)}")

    def get_statistics(self) -> Dict[str, Any]:
        """Get recording statistics"""
        if not self.demos:
            return {}

        episode_lengths = [len(ep) for ep in self.demos]

        return {
            'episode_count': self.episode_count,
            'total_steps': sum(episode_lengths),
            'avg_episode_length': np.mean(episode_lengths),
            'min_episode_length': min(episode_lengths),
            'max_episode_length': max(episode_lengths)
        }


async def record_interactive():
    """Interactive recording session"""
    import sys

    # Parse arguments
    config_path = '../config/rl_config.yaml'
    output_path = None

    if len(sys.argv) > 1:
        for arg in sys.argv[1:]:
            if arg.startswith('--config='):
                config_path = arg.split('=', 1)[1]
            elif arg.startswith('--output='):
                output_path = arg.split('=', 1)[1]

    # Load config
    config = get_config(config_path)

    # Create bridge
    bridge_config = config.get('bridge', {})
    bridge_host = bridge_config.get('host', 'localhost')
    bridge_port = bridge_config.get('port', 8765)

    logger.info(f"Connecting to bridge: {bridge_host}:{bridge_port}")
    bridge = MinecraftBotBridge(host=bridge_host, port=bridge_port)

    # Create recorder
    recorder = DemoRecorder(config, bridge)

    # Start recording
    await recorder.start_recording()

    # Save demos
    if output_path is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = f"../data/demos/demos_{timestamp}.pkl"

    recorder.save_demos(output_path)

    # Show statistics
    stats = recorder.get_statistics()
    if stats:
        logger.info("📊 Recording Statistics:")
        logger.info(f"   Episodes: {stats['episode_count']}")
        logger.info(f"   Total steps: {stats['total_steps']}")
        logger.info(f"   Avg length: {stats['avg_episode_length']:.1f}")


if __name__ == "__main__":
    asyncio.run(record_interactive())
