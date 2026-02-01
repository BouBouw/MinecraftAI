"""
Observation space definition for Minecraft RL environment.
Defines what the agent can observe from the game state.
"""

import numpy as np
import gymnasium as gym
from gymnasium import spaces
from typing import Dict, Any, Tuple


class ObservationSpace:
    """
    Observation space for Minecraft RL agent

    Observations include:
    - Position and movement (x, y, z, velocity, rotation)
    - Player state (health, food, saturation)
    - Inventory (36 slots)
    - Visible blocks (via raycast)
    - Nearby entities
    - Environment (time, weather, biome)
    - Equipment (held item, armor)
    """

    def __init__(self, config: Dict[str, Any]):
        """
        Initialize observation space

        Args:
            config: Configuration dictionary
        """
        self.config = config
        self.obs_config = config.get('observation_space', {})

        # Build observation space
        self.space = self._build_observation_space()

    def _build_observation_space(self) -> spaces.Dict:
        """
        Build the Gymnasium observation space

        Returns:
            Dictionary observation space
        """
        space_dict = {}

        # Position and movement
        if self.obs_config.get('position', True):
            space_dict['position'] = spaces.Box(
                low=-100000, high=100000, shape=(3,), dtype=np.float32
            )

        if self.obs_config.get('rotation', True):
            space_dict['rotation'] = spaces.Box(
                low=-180, high=180, shape=(2,), dtype=np.float32  # yaw, pitch
            )

        if self.obs_config.get('velocity', True):
            space_dict['velocity'] = spaces.Box(
                low=-10, high=10, shape=(3,), dtype=np.float32
            )

        if self.obs_config.get('on_ground', True):
            space_dict['on_ground'] = spaces.Discrete(2)

        if self.obs_config.get('in_water', True):
            space_dict['in_water'] = spaces.Discrete(2)

        # Player state
        if self.obs_config.get('health', True):
            space_dict['health'] = spaces.Box(low=0, high=20, shape=(1,), dtype=np.float32)

        if self.obs_config.get('food', True):
            space_dict['food'] = spaces.Box(low=0, high=20, shape=(1,), dtype=np.float32)

        if self.obs_config.get('saturation', True):
            space_dict['saturation'] = spaces.Box(low=0, high=20, shape=(1,), dtype=np.float32)

        # Inventory
        if self.obs_config.get('inventory', True):
            # [item_id, count] for each of 36 slots
            space_dict['inventory'] = spaces.Box(
                low=0, high=1000, shape=(36, 2), dtype=np.int32
            )

        if self.obs_config.get('hotbar_selected', True):
            space_dict['hotbar_selected'] = spaces.Discrete(9)

        # Vision - visible blocks
        if self.obs_config.get('visible_blocks', True):
            count = self.obs_config.get('visible_blocks_count', 100)
            # [x, y, z, block_id] for each visible block
            space_dict['visible_blocks'] = spaces.Box(
                low=-100000, high=100000, shape=(count, 4), dtype=np.int32
            )

        # Nearby entities
        if self.obs_config.get('nearby_entities', True):
            count = self.obs_config.get('nearby_entities_count', 10)
            # [entity_type, x, y, z] for each entity
            space_dict['nearby_entities'] = spaces.Box(
                low=-100000, high=100000, shape=(count, 4), dtype=np.int32
            )

        # Environment
        if self.obs_config.get('time_of_day', True):
            space_dict['time_of_day'] = spaces.Box(low=0, high=24000, shape=(1,), dtype=np.int32)

        if self.obs_config.get('is_raining', True):
            space_dict['is_raining'] = spaces.Discrete(2)

        if self.obs_config.get('biome_id', True):
            space_dict['biome_id'] = spaces.Discrete(200)

        # Equipment
        if self.obs_config.get('held_item', True):
            space_dict['held_item'] = spaces.Discrete(1000)  # item_id

        if self.obs_config.get('armor', True):
            space_dict['armor'] = spaces.Box(
                low=0, high=1000, shape=(4,), dtype=np.int32  # head, chest, legs, feet
            )

        return spaces.Dict(space_dict)

    def create_observation(self, raw_state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create observation from raw game state

        Args:
            raw_state: Raw state from Minecraft bot

        Returns:
            Formatted observation matching the observation space
        """
        obs = {}

        # Position and movement
        if 'position' in self.space:
            pos = raw_state.get('position', {})
            obs['position'] = np.array([
                pos.get('x', 0),
                pos.get('y', 0),
                pos.get('z', 0)
            ], dtype=np.float32)

        if 'rotation' in self.space:
            rot = raw_state.get('rotation', {})
            obs['rotation'] = np.array([
                rot.get('yaw', 0),
                rot.get('pitch', 0)
            ], dtype=np.float32)

        if 'velocity' in self.space:
            vel = raw_state.get('velocity', {})
            obs['velocity'] = np.array([
                vel.get('dx', 0),
                vel.get('dy', 0),
                vel.get('dz', 0)
            ], dtype=np.float32)

        if 'on_ground' in self.space:
            obs['on_ground'] = int(raw_state.get('on_ground', False))

        if 'in_water' in self.space:
            obs['in_water'] = int(raw_state.get('in_water', False))

        # Player state
        if 'health' in self.space:
            obs['health'] = np.array([raw_state.get('health', 20)], dtype=np.float32)

        if 'food' in self.space:
            obs['food'] = np.array([raw_state.get('food', 20)], dtype=np.float32)

        if 'saturation' in self.space:
            obs['saturation'] = np.array([raw_state.get('saturation', 20)], dtype=np.float32)

        # Inventory
        if 'inventory' in self.space:
            inventory = raw_state.get('inventory', [])
            inv_array = np.zeros((36, 2), dtype=np.int32)

            for i, slot in enumerate(inventory[:36]):
                if slot:
                    inv_array[i] = [slot.get('item_id', 0), slot.get('count', 0)]

            obs['inventory'] = inv_array

        if 'hotbar_selected' in self.space:
            obs['hotbar_selected'] = raw_state.get('hotbar_selected', 0)

        # Vision
        if 'visible_blocks' in self.space:
            blocks = raw_state.get('visible_blocks', [])
            blocks_array = np.zeros((100, 4), dtype=np.int32)

            for i, block in enumerate(blocks[:100]):
                blocks_array[i] = [
                    block.get('x', 0),
                    block.get('y', 0),
                    block.get('z', 0),
                    block.get('block_id', 0)
                ]

            obs['visible_blocks'] = blocks_array

        # Entities
        if 'nearby_entities' in self.space:
            entities = raw_state.get('nearby_entities', [])
            entities_array = np.zeros((10, 4), dtype=np.int32)

            for i, entity in enumerate(entities[:10]):
                entities_array[i] = [
                    entity.get('type', 0),
                    entity.get('x', 0),
                    entity.get('y', 0),
                    entity.get('z', 0)
                ]

            obs['nearby_entities'] = entities_array

        # Environment
        if 'time_of_day' in self.space:
            obs['time_of_day'] = np.array([raw_state.get('time_of_day', 0)], dtype=np.int32)

        if 'is_raining' in self.space:
            obs['is_raining'] = int(raw_state.get('is_raining', False))

        if 'biome_id' in self.space:
            obs['biome_id'] = raw_state.get('biome_id', 0)

        # Equipment
        if 'held_item' in self.space:
            obs['held_item'] = raw_state.get('held_item', 0)

        if 'armor' in self.space:
            armor = raw_state.get('armor', {})
            obs['armor'] = np.array([
                armor.get('head', 0),
                armor.get('chest', 0),
                armor.get('legs', 0),
                armor.get('feet', 0)
            ], dtype=np.int32)

        # Debug logging
        from utils.logger import get_logger
        logger = get_logger(__name__)
        logger.info(f"Created observation with {len(obs)} fields: {list(obs.keys())}")

        return obs

    def flatten_observation(self, obs: Dict[str, Any]) -> np.ndarray:
        """
        Flatten observation dict to 1D array for neural network input

        Args:
            obs: Observation dictionary

        Returns:
            Flattened 1D numpy array
        """
        flat_list = []

        for key in sorted(self.space.spaces.keys()):
            value = obs[key]
            flat_list.append(value.flatten())

        return np.concatenate(flat_list)

    @property
    def shape(self) -> Tuple[int, ...]:
        """Get flattened observation shape"""
        # Calculate total size
        total_size = 0
        for space in self.space.spaces.values():
            if isinstance(space, spaces.Box):
                total_size += np.prod(space.shape)
            elif isinstance(space, spaces.Discrete):
                total_size += 1
            elif isinstance(space, spaces.Dict):
                # Recursively calculate
                pass  # Handle nested dicts if needed

        return (total_size,)

    def __repr__(self) -> str:
        return f"ObservationSpace({self.space})"


def create_observation_space(config: Dict[str, Any]) -> ObservationSpace:
    """
    Factory function to create observation space

    Args:
        config: Configuration dictionary

    Returns:
        ObservationSpace instance
    """
    return ObservationSpace(config)
