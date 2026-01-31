"""
Action space definition for Minecraft RL environment.
Defines what actions the agent can take in the game.
"""

import numpy as np
import gymnasium as gym
from gymnasium import spaces
from typing import Dict, Any, List
from enum import IntEnum


class ActionType(IntEnum):
    """
    Enumeration of all possible action types

    Movement (0-7):
        0: NOOP              - No operation
        1: MOVE_FORWARD      - Move forward
        2: MOVE_BACKWARD     - Move backward
        3: MOVE_LEFT         - Strafe left
        4: MOVE_RIGHT        - Strafe right
        5: JUMP              - Jump
        6: SNEAK             - Sneak (walk slowly, no fall damage)
        7: SPRINT            - Sprint (move faster)

    Camera (8-12):
        8: LOOK_AT           - Look at specific position
        9: TURN_LEFT         - Turn left
        10: TURN_RIGHT       - Turn right
        11: LOOK_UP          - Look up
        12: LOOK_DOWN        - Look down

    Inventory (13-16):
        13: SELECT_SLOT      - Select hotbar slot (0-8)
        14: SCROLL_HOTBAR    - Scroll hotbar
        15: SWAP_HANDS       - Swap main hand and off-hand
        16: DROP_ITEM        - Drop held item

    Blocks (17-24):
        17: ATTACK           - Attack entity / break block
        18: USE_ITEM         - Use held item
        19: PLACE_BLOCK      - Place block
        20: BREAK_BLOCK      - Break block (alternative)
        21: DIG_FORWARD      - Dig block in front
        22: DIG_DOWN         - Dig block below
        23: DIG_UP           - Dig block above
        24: BLOCK_INTERACT   - Interact with block (chest, door, etc.)

    Crafting (25-30):
        25: OPEN_INVENTORY   - Open inventory screen
        26: CLOSE_INVENTORY  - Close inventory screen
        27: CRAFT_ITEM       - Craft known recipe
        28: CRAFT_UNKNOWN    - Attempt unknown recipe
        29: SMELT_ITEM       - Smelt item in furnace
        30: EXPERIMENT_CRAFT - Try random craft combination

    Items (31-35):
        31: EAT              - Eat food item
        32: DRINK            - Drink potion
        33: FILL_BUCKET      - Fill bucket with water/lava
        34: EMPTY_BUCKET     - Empty bucket
        35: PICKUP_ITEM      - Pick up nearby item

    Equipment (36-38):
        36: EQUIP_ARMOR      - Equip armor piece
        37: UNEQUIP_ARMOR    - Unequip armor piece
        38: SORT_INVENTORY   - Sort inventory items

    Entity (39-40):
        39: ENTITY_INTERACT  - Interact with entity (villager, animal)
        40: THROW_ITEM       - Throw item at entity

    Environment (41-45):
        41: SLEEP            - Sleep in bed
        42: WAKE_UP          - Wake up from bed
        43: RESPAWN          - Respawn after death
        44: OBSERVE          - Observe surroundings (no action)
        45: WAIT             - Wait/tick

    Advanced (46-49):
        46: COMBINE_ITEMS    - Combine items (e.g., tools + armor)
        47: TALK             - Chat with villagers/players
        48: RECALL_MEMORY    - Recall specific memory
        49: BUILD            - Build from schematic/plans
    """

    # Movement
    NOOP = 0
    MOVE_FORWARD = 1
    MOVE_BACKWARD = 2
    MOVE_LEFT = 3
    MOVE_RIGHT = 4
    JUMP = 5
    SNEAK = 6
    SPRINT = 7

    # Camera
    LOOK_AT = 8
    TURN_LEFT = 9
    TURN_RIGHT = 10
    LOOK_UP = 11
    LOOK_DOWN = 12

    # Inventory
    SELECT_SLOT = 13
    SCROLL_HOTBAR = 14
    SWAP_HANDS = 15
    DROP_ITEM = 16

    # Blocks
    ATTACK = 17
    USE_ITEM = 18
    PLACE_BLOCK = 19
    BREAK_BLOCK = 20
    DIG_FORWARD = 21
    DIG_DOWN = 22
    DIG_UP = 23
    BLOCK_INTERACT = 24

    # Crafting
    OPEN_INVENTORY = 25
    CLOSE_INVENTORY = 26
    CRAFT_ITEM = 27
    CRAFT_UNKNOWN = 28
    SMELT_ITEM = 29
    EXPERIMENT_CRAFT = 30

    # Items
    EAT = 31
    DRINK = 32
    FILL_BUCKET = 33
    EMPTY_BUCKET = 34
    PICKUP_ITEM = 35

    # Equipment
    EQUIP_ARMOR = 36
    UNEQUIP_ARMOR = 37
    SORT_INVENTORY = 38

    # Entity
    ENTITY_INTERACT = 39
    THROW_ITEM = 40

    # Environment
    SLEEP = 41
    WAKE_UP = 42
    RESPAWN = 43
    OBSERVE = 44
    WAIT = 45

    # Advanced
    COMBINE_ITEMS = 46
    TALK = 47
    RECALL_MEMORY = 48
    BUILD = 49

    @classmethod
    def get_movement_actions(cls) -> List[int]:
        """Get list of movement action IDs"""
        return [cls.MOVE_FORWARD, cls.MOVE_BACKWARD, cls.MOVE_LEFT,
                cls.MOVE_RIGHT, cls.JUMP, cls.SNEAK, cls.SPRINT]

    @classmethod
    def get_crafting_actions(cls) -> List[int]:
        """Get list of crafting action IDs"""
        return [cls.OPEN_INVENTORY, cls.CLOSE_INVENTORY, cls.CRAFT_ITEM,
                cls.CRAFT_UNKNOWN, cls.SMELT_ITEM, cls.EXPERIMENT_CRAFT]

    @classmethod
    def get_block_actions(cls) -> List[int]:
        """Get list of block interaction action IDs"""
        return [cls.ATTACK, cls.USE_ITEM, cls.PLACE_BLOCK, cls.BREAK_BLOCK,
                cls.DIG_FORWARD, cls.DIG_DOWN, cls.DIG_UP, cls.BLOCK_INTERACT]

    @classmethod
    def get_basic_actions(cls) -> List[int]:
        """Get list of basic actions for early training"""
        return [cls.NOOP, cls.MOVE_FORWARD, cls.MOVE_BACKWARD, cls.JUMP,
                cls.LOOK_AT, cls.TURN_LEFT, cls.TURN_RIGHT]

    @classmethod
    def get_all_actions(cls) -> List[int]:
        """Get all action IDs"""
        return list(range(50))


class ActionSpace:
    """
    Action space for Minecraft RL agent

    Actions are represented as a dictionary with:
    - action_type: Discrete action type (0-49)
    - target_pos: Target position (x, y, z) for some actions
    - target_block: Block ID for placement/breaking
    - slot_index: Inventory slot index
    - continuous: Continuous action parameters
    """

    def __init__(self, config: Dict[str, Any]):
        """
        Initialize action space

        Args:
            config: Configuration dictionary
        """
        self.config = config
        self.action_config = config.get('action_space', {})

        # Build action space
        self.space = self._build_action_space()

    def _build_action_space(self) -> spaces.Dict:
        """
        Build the Gymnasium action space

        Returns:
            Dictionary action space
        """
        space_dict = {
            # Discrete action type
            'action_type': spaces.Discrete(50),

            # Target position (x, y, z)
            'target_pos': spaces.Box(
                low=-100000, high=100000, shape=(3,), dtype=np.float32
            ),

            # Target block ID
            'target_block': spaces.Discrete(1000),

            # Inventory slot index
            'slot_index': spaces.Discrete(36),
        }

        # Add continuous actions if enabled
        if self.action_config.get('continuous_actions', True):
            space_dict.update({
                'move_forward': spaces.Box(low=0, high=1, shape=(1,), dtype=np.float32),
                'move_backward': spaces.Box(low=0, high=1, shape=(1,), dtype=np.float32),
                'move_left': spaces.Box(low=0, high=1, shape=(1,), dtype=np.float32),
                'move_right': spaces.Box(low=0, high=1, shape=(1,), dtype=np.float32),
                'jump': spaces.Box(low=0, high=1, shape=(1,), dtype=np.float32),
                'sprint': spaces.Box(low=0, high=1, shape=(1,), dtype=np.float32),
                'sneak': spaces.Box(low=0, high=1, shape=(1,), dtype=np.float32),
            })

        return spaces.Dict(space_dict)

    def create_action(self, action_type: int, **kwargs) -> Dict[str, Any]:
        """
        Create action dictionary from action type and parameters

        Args:
            action_type: Type of action to perform
            **kwargs: Additional action parameters

        Returns:
            Action dictionary matching action space
        """
        action = {
            'action_type': action_type,
            'target_pos': kwargs.get('target_pos', [0, 0, 0]),
            'target_block': kwargs.get('target_block', 0),
            'slot_index': kwargs.get('slot_index', 0),
        }

        # Add continuous actions if enabled
        if self.action_config.get('continuous_actions', True):
            action.update({
                'move_forward': np.array([kwargs.get('move_forward', 0)], dtype=np.float32),
                'move_backward': np.array([kwargs.get('move_backward', 0)], dtype=np.float32),
                'move_left': np.array([kwargs.get('move_left', 0)], dtype=np.float32),
                'move_right': np.array([kwargs.get('move_right', 0)], dtype=np.float32),
                'jump': np.array([kwargs.get('jump', 0)], dtype=np.float32),
                'sprint': np.array([kwargs.get('sprint', 0)], dtype=np.float32),
                'sneak': np.array([kwargs.get('sneak', 0)], dtype=np.float32),
            })

        return action

    def sample(self) -> Dict[str, Any]:
        """
        Sample a random action from the action space

        Returns:
            Random action dictionary
        """
        return self.space.sample()

    def contains(self, action: Dict[str, Any]) -> bool:
        """
        Check if action is within the action space

        Args:
            action: Action to check

        Returns:
            True if action is valid
        """
        return self.space.contains(action)

    def filter_actions_by_stage(self, stage: str) -> List[int]:
        """
        Get available actions for a specific curriculum stage

        Args:
            stage: Curriculum stage name

        Returns:
            List of available action type IDs
        """
        stage_actions = {
            'basic_movement': ActionType.get_basic_actions(),
            'gathering': ActionType.get_basic_actions() +
                         ActionType.get_block_actions()[:4],  # Add basic block actions
            'basic_crafting': ActionType.get_all_actions(),  # All actions for crafting
            'survival': ActionType.get_all_actions(),
            'building': ActionType.get_all_actions(),
        }

        return stage_actions.get(stage, ActionType.get_basic_actions())

    @property
    def n(self) -> int:
        """Get number of discrete action types"""
        return 50

    def __repr__(self) -> str:
        return f"ActionSpace(n={self.n}, continuous={self.action_config.get('continuous_actions', True)})"


def create_action_space(config: Dict[str, Any]) -> ActionSpace:
    """
    Factory function to create action space

    Args:
        config: Configuration dictionary

    Returns:
        ActionSpace instance
    """
    return ActionSpace(config)
