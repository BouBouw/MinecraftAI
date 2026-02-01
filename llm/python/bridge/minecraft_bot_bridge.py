"""
Python Bridge for Minecraft RL Agent
Connects Python RL agent to Mineflayer bot via WebSocket
Enables real-time gameplay and learning
"""

import asyncio
import websockets
import json
import numpy as np
from typing import Dict, Any, Optional, List, Tuple
from dataclasses import dataclass
from collections import deque
import time

from utils.config import get_config
from utils.logger import get_logger
from gym_env.observations import create_observation_space
from gym_env.actions import create_action_space

logger = get_logger(__name__)


@dataclass
class BotState:
    """Current state of the Minecraft bot"""
    position: List[float]  # [x, y, z]
    rotation: List[float]  # [yaw, pitch]
    health: float
    food: float
    saturation: float
    on_ground: int  # 0 or 1
    in_water: int  # 0 or 1
    inventory: List[List[int]]  # [[item_id, count], ...]
    held_item: int
    armor: List[int]  # [head, chest, legs, feet]
    nearby_entities: List[Dict[str, Any]]
    time_of_day: int
    is_raining: int  # 0 or 1
    biome_id: int


class MinecraftBotBridge:
    """
    Bridge between Python RL Agent and Minecraft Bot (via WebSocket)

    This is what actually connects the AI to the game!
    """

    def __init__(self, host: str = 'localhost', port: int = 8765):
        """
        Initialize bridge to Minecraft bot

        Args:
            host: WebSocket server host (Node.js bridge)
            port: WebSocket server port
        """
        self.host = host
        self.port = port
        self.ws = None
        self.connected = False

        # Bot state cache
        self.current_state: Optional[BotState] = None
        self.last_action_time = 0

        # Action completion tracking
        self._action_complete_event = asyncio.Event()
        self._last_action_result = None

        # Action callbacks
        self.action_callbacks = {
            'move_forward': None,
            'move_backward': None,
            'jump': None,
            'attack': None,
            'craft': None,
            'place_block': None,
            'break_block': None,
            'use_item': None,
            'look_at': None,
            'select_slot': None,
        }

    async def connect(self):
        """Connect to the WebSocket server"""
        try:
            logger.info(f"🔌 Connecting to WebSocket server at {self.host}:{self.port}...")

            # Connect as client to the Node.js WebSocket server
            self.ws = await websockets.connect(
                f"ws://{self.host}:{self.port}",
                ping_interval=30,
                ping_timeout=20,
                close_timeout=10
            )

            logger.info("✅ Connected to Minecraft bot via WebSocket")
            self.connected = True

            # Start listening for messages in background
            # This won't block - it creates a background task
            asyncio.create_task(self._listen_loop())

        except Exception as e:
            logger.error(f"❌ Failed to connect: {e}")
            raise

    async def _listen_loop(self):
        """Listen for messages from the bot"""
        try:
            async for message in self.ws:
                try:
                    data = json.loads(message)
                    await self.handle_message(data)
                except json.JSONDecodeError as e:
                    logger.error(f"Failed to parse message: {e}")

        except websockets.exceptions.ConnectionClosed:
            logger.warning("WebSocket connection closed")
            self.connected = False

    async def handle_message(self, data: Dict[str, Any]):
        """Handle incoming message from bot"""
        msg_type = data.get('type')

        if msg_type == 'observation':
            await self._handle_observation(data)
        elif msg_type == 'action_complete':
            await self._handle_action_complete(data)
        elif msg_type == 'bot_state_update':
            await self._handle_bot_state(data)
        elif msg_type == 'death':
            await self._handle_death(data)
        elif msg_type == 'chat':
            logger.info(f"📝 Bot chat: {data.get('message')}")
        else:
            logger.debug(f"Unknown message type: {msg_type}")

    async def _handle_observation(self, data: Dict[str, Any]):
        """Handle observation from bot"""
        obs_data = data['observation']

        # Parse observation
        self.current_state = BotState(
            position=obs_data['position'],
            rotation=obs_data['rotation'],
            health=obs_data['health'],
            food=obs_data['food'],
            saturation=obs_data['saturation'],
            on_ground=obs_data.get('on_ground', 1),
            in_water=obs_data.get('in_water', 0),
            inventory=obs_data['inventory'],
            held_item=obs_data.get('hotbar_selected', 0),
            armor=obs_data.get('armor', [0, 0, 0, 0]),
            nearby_entities=obs_data.get('nearby_entities', []),
            time_of_day=obs_data.get('time_of_day', 0),
            is_raining=obs_data.get('is_raining', 0),
            biome_id=obs_data.get('biome_id', 0)
        )

    async def _handle_action_complete(self, data: Dict[str, Any]):
        """Handle action completion result"""
        success = data.get('success', False)
        action = data.get('action', {})

        # Store result and set event
        self._last_action_result = data
        self._action_complete_event.set()

        # Update current_state from observation if included
        observation_data = data.get('observation')
        if observation_data:
            logger.debug(f"Received observation: {list(observation_data.keys())}")
            self.current_state = BotState(
                position=observation_data.get('position', [0, 64, 0]),
                rotation=observation_data.get('rotation', [0, 0]),
                health=observation_data.get('health', 20),
                food=observation_data.get('food', 20),
                saturation=observation_data.get('saturation', 20),
                on_ground=observation_data.get('on_ground', 1),
                in_water=observation_data.get('in_water', 0),
                inventory=observation_data.get('inventory', []),
                held_item=observation_data.get('hotbar_selected', 0),
                armor=observation_data.get('armor', {}),
                nearby_entities=observation_data.get('nearby_entities', []),
                time_of_day=observation_data.get('time_of_day', 0),
                is_raining=observation_data.get('is_raining', 0),
                biome_id=observation_data.get('biome_id', 0)
            )
            logger.info(f"✅ Updated state: health={self.current_state.health}, food={self.current_state.food}")
        else:
            logger.warning("⚠️  No observation in action_complete message")

        logger.debug(f"Action completed: success={success}")

    async def _handle_bot_state(self, data: Dict[str, Any]):
        """Handle bot state update"""
        # Update current state
        pass

    async def _handle_death(self, data: Dict[str, Any]):
        """Handle bot death"""
        cause = data.get('cause', 'unknown')
        logger.warning(f"💀 Bot died from {cause}")

        # Trigger death reward penalty
        # This will be handled by the RL agent

    async def send_action(self, action_type: int, **params) -> Dict[str, Any]:
        """
        Send action to bot

        Args:
            action_type: Type of action (0-49)
            **params: Additional action parameters

        Returns:
            Result from action execution
        """
        if not self.connected or not self.ws:
            logger.error("Not connected to bot")
            return {'success': False}

        message = {
            'type': 'action',
            'action': {
                'action_type': action_type,
                **params
            }
        }

        await self.ws.send(json.dumps(message))

        # Wait for result (with timeout)
        result = await self._wait_for_action_result()

        return result

    async def _wait_for_action_result(self, timeout: float = 30.0) -> Dict[str, Any]:
        """
        Wait for action completion result

        Args:
            timeout: Timeout in seconds

        Returns:
            Action result
        """
        start_time = time.time()

        while time.time() - start_time < timeout:
            # Will receive action_complete message
            await asyncio.sleep(0.1)
        else:
            logger.warning(f"Action timeout after {timeout}s")
            return {'success': False, 'timeout': True}

    async def get_observation(self) -> Dict[str, Any]:
        """
        Get current observation from bot

        Returns:
            Current bot state as observation
        """
        if not self.connected or not self.ws:
            logger.error("Not connected to bot")
            return self._get_default_observation()

        # Return cached state
        if self.current_state:
            obs = {
                'position': self.current_state.position,
                'rotation': self.current_state.rotation,
                'health': self.current_state.health,
                'food': self.current_state.food,
                'saturation': self.current_state.saturation,
                'on_ground': self.current_state.on_ground,
                'in_water': self.current_state.in_water,
                'inventory': self.current_state.inventory,
                'held_item': self.current_state.held_item,
                'armor': self.current_state.armor,
                'nearby_entities': self.current_state.nearby_entities,
                'time_of_day': self.current_state.time_of_day,
                'is_raining': self.current_state.is_raining,
                'biome_id': self.current_state.biome_id,
            }
            logger.debug(f"get_observation: health={obs['health']}, food={obs['food']}")
            return obs
        else:
            logger.warning("current_state is None, returning defaults")
            return self._get_default_observation()

    def _get_default_observation(self) -> Dict[str, Any]:
        """Return default observation when state is not available"""
        return {
            'position': [0, 64, 0],
            'rotation': [0, 0],
            'health': 20,
            'food': 20,
            'saturation': 20,
            'on_ground': 1,
            'in_water': 0,
            'inventory': [],
            'held_item': 0,
            'armor': [0, 0, 0, 0],
            'nearby_entities': [],
            'time_of_day': 0,
            'is_raining': 0,
            'biome_id': 1
        }

    async def reset_environment(self) -> Dict[str, Any]:
        """
        Reset the environment (respawn)

        Returns:
            Initial observation after reset
        """
        if not self.connected or not self.ws:
            logger.error("Not connected to bot")
            return {}

        # Send reset command
        await self.ws.send(json.dumps({'type': 'reset'}))

        # Wait for reset to complete
        await asyncio.sleep(2)

        # Return new observation
        return await self.get_observation()

    async def disconnect(self):
        """Disconnect from bot"""
        if self.ws:
            await self.ws.close()

        self.connected = False
        logger.info("Disconnected from bot")


class MinecraftEnvironment:
    """
    Real Minecraft Environment for RL Training

    This is the actual interface that lets the AI play Minecraft!
    """

    def __init__(self, bridge_host: str = 'localhost', bridge_port: int = 8765):
        """
        Initialize Minecraft environment

        Args:
            bridge_host: Bridge server host
            bridge_port: Bridge port
        """
        self.bridge = MinecraftBotBridge(bridge_host, bridge_port)

        # Get config for spaces
        config = get_config()

        # Create observation and action spaces
        self.observation_space = create_observation_space(config)
        self.action_space = create_action_space(config)

        # Action mapping
        self.action_names = {
            0: 'NOOP',
            1: 'MOVE_FORWARD',
            2: 'MOVE_BACKWARD',
            3: 'MOVE_LEFT',
            4: 'MOVE_RIGHT',
            5: 'JUMP',
            6: 'SNEAK',
            7: 'SPRINT',
            8: 'LOOK_AT',
            9: 'TURN_LEFT',
            10: 'TURN_RIGHT',
            11: 'LOOK_UP',
            12: 'LOOK_DOWN',
            13: 'SELECT_SLOT',
            14: 'DIG_DOWN',
            15: 'DIG_UP',
            16: 'DIG_FORWARD',
            17: 'ATTACK',
            18: 'USE_ITEM',
            19: 'PLACE_BLOCK',
            20: 'BREAK_BLOCK',
            21: 'CRAFT_ITEM',
            22: 'SMELT_ITEM',
            23: 'EAT',
            24: 'DRINK',
            25: 'CRAFT_UNKNOWN',
            26: 'FILL_BUCKET',
            27: 'EMPTY_BUCKET',
            28: 'PICKUP_ITEM',
            29: 'EQUIP_ARMOR',
            30: 'UNEQUIP_ARMOR',
            31: 'SORT_INVENTORY',
            32: 'THROW_ITEM',
            33: 'ENTITY_INTERACT',
            34: 'SLEEP',
            35: 'WAKE_UP',
            36: 'RESPAWN',
            37: 'OBSERVE',
            38: 'WAIT',
            39: 'RECALL_MEMORY',
            40: 'BUILD',
            41: 'DROP_ITEM',
            42: 'SWAP_HANDS',
            43: 'COMBINE_ITEMS',
            44: 'TALK',
            45: 'SCROLL_HOTBAR',
            46: 'BLOCK_INTERACT',
            47: 'CLOSE_INVENTORY',
            48: 'OPEN_INVENTORY',
            49: 'MOVE_FORWARD_2',
            50: 'MOVE_BACKWARD_2',
        }

    @classmethod
    async def create(cls, host: str = 'localhost', port: int = 8765):
        """
        Create and connect a Minecraft environment asynchronously

        Args:
            host: Bridge server host
            port: Bridge port

        Returns:
            Connected MinecraftEnvironment instance
        """
        logger.info(f"🌉 Creating Minecraft environment connected to {host}:{port}...")

        # Create instance
        env = cls(bridge_host=host, bridge_port=port)

        # Connect to the bridge
        await env.bridge.connect()

        logger.info("✅ Minecraft environment connected and ready!")

        return env

    async def reset(self) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """
        Reset environment and return initial observation

        Returns:
            Tuple of (observation, info)
        """
        logger.info("🔄 Resetting environment...")

        # Reset bot state
        result = await self.bridge.reset_environment()

        observation = result
        info = {
            'episode_length': 0,
            'episode_start_time': time.time()
        }

        return observation, info

    async def step(
        self,
        action: Dict[str, Any]
    ) -> Tuple[Dict[str, Any], float, bool, bool, Dict[str, Any]]:
        """
        Execute one step in the environment

        Args:
            action: Action to execute

        Returns:
            Tuple of (observation, reward, done, truncated, info)
        """
        action_type = action['action_type']

        # Execute action via bridge
        result = await self.bridge.send_action(
            action_type=action_type,
            **{k: v for k, v in action.items() if k != 'action_type'}
        )

        # Get new observation
        observation = await self.bridge.get_observation()

        # Calculate reward
        reward = self._calculate_reward(result, observation)

        # Check if episode is done
        done = observation['health'] <= 0
        truncated = False  # Can be used for timeouts

        info = {
            'action_success': result.get('success', False),
            'action_type': action_type
        }

        return observation, reward, done, truncated, info

    def _calculate_reward(self, action_result: Dict[str, Any], observation: Dict[str, Any]) -> float:
        """Calculate reward for this step"""
        reward = 0.0

        # Survival rewards
        reward += observation['health'] * 0.1
        reward += observation['food'] * 0.05

        # Action-specific rewards
        if action_result.get('success'):
            action_type = action_result.get('action_type', 0)

            # Mining
            if action_type in [17, 20, 21, 22, 23]:  # ATTACK, BREAK_BLOCK, DIG_*
                reward += 1.0

            # Crafting
            elif action_type in [21, 25]:  # CRAFT_ITEM
                reward += 5.0

            # Building
            elif action_type == 19:  # PLACE_BLOCK
                reward += 2.0

        # Death penalty
        if observation['health'] <= 0:
            reward -= 500

        # Small time penalty to encourage efficiency
        reward -= 0.01

        return reward

    async def close(self):
        """Close the environment"""
        await self.bridge.disconnect()


# Factory function
async def create_minecraft_environment(
    host: str = 'localhost',
    port: int = 8765
) -> MinecraftEnvironment:
    """
    Factory function to create Minecraft environment

    Args:
        host: Bridge server host
        port: Bridge port

    Returns:
        MinecraftEnvironment instance
    """
    env = MinecraftEnvironment(host, port)
    await env.bridge.connect()
    return env
