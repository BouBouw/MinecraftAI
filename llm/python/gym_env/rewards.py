"""
Reward system for Minecraft RL environment.
Calculates rewards based on actions and state changes.

SUPPORTS TWO MODES:
1. Extrinsic rewards (hand-crafted) - Traditional RL with human-designed rewards
2. Intrinsic rewards (autonomous) - Self-motivated exploration via curiosity
"""

import numpy as np
from typing import Dict, Any, List, Set, Optional
from collections import defaultdict

from utils.logger import get_logger

logger = get_logger(__name__)


class RewardSystem:
    """
    Reward calculation system for Minecraft RL agent

    Rewards are based on:
    - Survival (health, food)
    - Progression (mining, crafting, building)
    - Exploration (new areas, biomes)
    - Efficiency (time penalty)
    - Achievements (first-time discoveries)
    """

    def __init__(
        self,
        config: Dict[str, Any],
        curiosity_module: Optional['IntrinsicCuriosityModule'] = None,
        auto_curriculum: Optional['AutoCurriculum'] = None
    ):
        """
        Initialize reward system

        Args:
            config: Configuration dictionary
            curiosity_module: Optional intrinsic curiosity module for autonomous learning
            auto_curriculum: Optional auto-curriculum for tracking discoveries
        """
        self.config = config
        self.reward_config = config.get('rewards', {})

        # Check if using intrinsic rewards (autonomous mode)
        training_config = config.get('training', {})
        self.use_intrinsic = training_config.get('auto_curriculum', {}).get('enabled', False)
        self.use_extrinsic = training_config.get('use_extrinsic_rewards', True)

        self.curiosity_module = curiosity_module
        self.auto_curriculum = auto_curriculum

        # Tracking for first-time bonuses
        self.discovered_blocks: Set[int] = set()
        self.discovered_biomes: Set[int] = set()
        self.discovered_crafts: Set[int] = set()
        self.visited_chunks: Set[tuple] = set()

        # Episode tracking
        self.episode_mined_blocks = defaultdict(int)
        self.episode_crafted_items = defaultdict(int)
        self.episode_placed_blocks = 0

        # Movement tracking - encourage exploration
        self.last_position = None
        self.total_distance = 0.0

        # Track last observation for intrinsic reward
        self.last_observation: Optional[Dict[str, Any]] = None
        self.last_action: Optional[int] = None

        if self.use_intrinsic:
            logger.info("🤖 Reward System: INTRINSIC MODE (autonomous learning)")
        else:
            logger.info("🎯 Reward System: EXTRINSIC MODE (hand-crafted rewards)")

    def reset(self):
        """Reset episode-specific tracking"""
        self.episode_mined_blocks.clear()
        self.episode_crafted_items.clear()
        self.episode_placed_blocks = 0
        self.last_position = None
        self.total_distance = 0.0

    def calculate_reward(
        self,
        state: Dict[str, Any],
        action: Any,
        next_state: Dict[str, Any],
        done: bool
    ) -> float:
        """
        Calculate reward for a single step

        INTRINSIC MODE: Uses curiosity, novelty, count-based exploration
        EXTRINSIC MODE: Uses hand-crafted rewards for specific actions

        Args:
            state: Current state
            action: Action taken (int or dict)
            next_state: Next state
            done: Whether episode is done

        Returns:
            Reward value (positive or negative)
        """
        reward = 0.0

        # Get action_type if action is a dict
        if isinstance(action, dict):
            action_type = action.get('action_type', 0)
            action_id = action_type
        else:
            action_type = action
            action_id = action

        # === INTRINSIC REWARDS (Autonomous Learning) ===
        if self.use_intrinsic and self.curiosity_module:
            # Curiosity-driven reward based on prediction error
            intrinsic_reward = self.curiosity_module.compute_intrinsic_reward(
                state, next_state, action_id
            )
            reward += intrinsic_reward

        # === EXTRINSIC REWARDS (Hand-crafted) ===
        if self.use_extrinsic:
            # 1. Survival rewards (minimal penalties only)
            reward += self._survival_reward(state, next_state)

            # 2. Progression rewards (action-based)
            reward += self._progression_reward(state, action, next_state)

            # 3. Exploration rewards (movement)
            reward += self._exploration_reward(state, next_state)

            # 4. Achievement rewards (first-time bonuses)
            reward += self._achievement_reward(state, action, next_state)

            # 5. Time penalty (small efficiency penalty)
            reward += self.reward_config.get('time_penalty', -0.01)  # Reduced from -0.1

        # === AUTO-CURRICULUM TRACKING ===
        if self.auto_curriculum:
            # Update mechanic tracking based on action
            self._update_auto_curriculum(action, next_state, done)

        # === EPISODE COMPLETION ===
        if done:
            reward += self._episode_completion_reward(next_state)

        # Store for next intrinsic reward calculation
        self.last_observation = next_state
        self.last_action = action_id

        return reward

    def _update_auto_curriculum(self, action: Any, next_state: Dict[str, Any], done: bool):
        """Update auto-curriculum tracking based on action results"""
        if not self.auto_curriculum:
            return

        # Get action type
        if isinstance(action, dict):
            action_type = action.get('action_type', 0)
        else:
            action_type = action

        # Track block discoveries
        if 'block_in_front' in next_state:
            block_id = next_state['block_in_front']
            if block_id not in self.discovered_blocks and block_id != 0:
                self.discovered_blocks.add(block_id)
                # Auto-curriculum will track this

        # Track movement
        pos = next_state.get('position', [0, 64, 0])
        if isinstance(pos, list):
            x, y, z = pos[0], pos[1], pos[2]
        else:
            x, y, z = pos.get('x', 0), pos.get('y', 64), pos.get('z', 0)

        if self.last_position is not None:
            last_x, last_y, last_z = self.last_position
            distance = ((x - last_x)**2 + (z - last_z)**2)**0.5
            self.total_distance += distance

        self.last_position = (x, y, z)

        # Update curriculum
        self.auto_curriculum.update(step=getattr(self, 'step', 0))

    def _survival_reward(self, state: Dict[str, Any], next_state: Dict[str, Any]) -> float:
        """
        Calculate survival-based rewards
        REMOVED passive health/food bonuses - no free rewards for just existing
        Only penalties for damage/death
        """
        reward = 0.0

        # Death penalty (only penalty, no passive bonuses)
        health_check = next_state.get('health', [20])
        if isinstance(health_check, list):
            health_check = health_check[0] if len(health_check) > 0 else 20
        if health_check <= 0:
            death_penalty = self.reward_config.get('death_penalty', -100)
            reward += death_penalty

        # Damage penalty (handle both list [health] and scalar health)
        state_health = state.get('health', [20])
        next_health = next_state.get('health', [20])
        if isinstance(state_health, list):
            state_health = state_health[0] if len(state_health) > 0 else 20
        if isinstance(next_health, list):
            next_health = next_health[0] if len(next_health) > 0 else 20
        health_lost = state_health - next_health
        if health_lost > 0:
            reward -= health_lost * 5.0  # Increased penalty for taking damage

        return reward

    def _progression_reward(
        self,
        state: Dict[str, Any],
        action: Any,
        next_state: Dict[str, Any]
    ) -> float:
        """
        Calculate progression-based rewards
        Rewards are based on actions taken, not passive survival
        """
        reward = 0.0

        # Handle both int actions (from agent) and dict actions (from bridge)
        if isinstance(action, int):
            action_type = action
            target_block = 0  # Unknown when action is just an int
        else:
            action_type = action.get('action_type', 0)
            target_block = action.get('target_block', 0)

        # Mining rewards - ONLY give reward if actually mined something (not air!)
        if action_type in [17, 20, 21, 22, 23]:  # ATTACK, BREAK_BLOCK, DIG_*
            # SMALL exploration bonus for TRYING (reduced from 3.0 to 1.0)
            # This encourages trying to mine, but not spamming
            reward += 1.0

            # BIG bonus only if we actually discovered a new block type
            # (meaning we actually mined something, not air)
            if isinstance(action, dict):
                mined_block = target_block
                if mined_block not in self.discovered_blocks and mined_block != 0:  # 0 = air
                    self.discovered_blocks.add(mined_block)
                    reward += 50.0  # HUGE discovery bonus for NEW block type
                    logger.info(f"🎉 Discovered new block type: {mined_block}")
                elif mined_block != 0:  # Known block type, but still mined something
                    reward += 5.0  # Standard mining reward
                    self.episode_mined_blocks[mined_block] += 1
                else:  # mined_block == 0 (air) - wasted action!
                    reward -= 2.0  # PENALTY for mining air (discourage spam)
                    logger.debug("⚠️ Tried to mine air - penalty applied")

        # Crafting rewards - higher value (more complex)
        elif action_type in [27, 28]:  # CRAFT_ITEM, CRAFT_UNKNOWN
            reward += 5.0  # Higher reward for crafting (more valuable)

            if isinstance(action, dict):
                crafted_item = target_block
                self.episode_crafted_items[crafted_item] += 1

        # Building rewards - medium value
        elif action_type == 19:  # PLACE_BLOCK
            reward += 1.5  # Medium reward for building
            self.episode_placed_blocks += 1

        # Eating rewards - encourage survival behavior
        elif action_type == 31:  # EAT
            reward += 2.0  # Eating is good

        # Look actions - SMALL penalty to discourage spamming
        elif action_type in [8, 9, 10, 11]:  # LOOK_LEFT, RIGHT, UP, DOWN
            reward -= 0.5  # Small penalty for excessive looking

        return reward

    def _exploration_reward(
        self,
        state: Dict[str, Any],
        next_state: Dict[str, Any]
    ) -> float:
        """Calculate exploration-based rewards"""
        reward = 0.0

        # Distance reward - encourage movement!
        pos = next_state.get('position', [0, 64, 0])
        # Handle both list format [x, y, z] and dict format {x:, y:, z:}
        if isinstance(pos, list):
            x, y, z = pos[0], pos[1], pos[2]
        else:
            x, y, z = pos.get('x', 0), pos.get('y', 64), pos.get('z', 0)

        # Calculate distance from last position
        if self.last_position is not None:
            last_x, last_y, last_z = self.last_position
            distance = ((x - last_x)**2 + (z - last_z)**2)**0.5  # Only X-Z distance

            # Reward for movement - INCREASED to make movement VERY attractive
            reward += distance * 2.0  # 2.0 per block (instead of 0.1) - 20× more!

            self.total_distance += distance

        self.last_position = (x, y, z)

        # New chunk exploration
        chunk_x = int(x // 16)
        chunk_z = int(z // 16)
        chunk_key = (chunk_x, chunk_z)

        if chunk_key not in self.visited_chunks:
            self.visited_chunks.add(chunk_key)
            new_chunk_bonus = self.reward_config.get('new_chunk', 1)
            reward += new_chunk_bonus

        # New biome discovery
        biome_id = next_state.get('biome_id', 0)
        if biome_id not in self.discovered_biomes:
            self.discovered_biomes.add(biome_id)
            new_biome_bonus = self.reward_config.get('new_biome', 10)
            reward += new_biome_bonus

        # New structure discovery (would require external detection)
        # This is a placeholder - actual implementation would detect structures
        # reward += self._check_structure_discovery(next_state)

        return reward

    def _achievement_reward(
        self,
        state: Dict[str, Any],
        action: Any,
        next_state: Dict[str, Any]
    ) -> float:
        """
        Calculate first-time achievement bonuses
        Large bonuses for discovering new things
        """
        reward = 0.0

        # Handle both int actions (from agent) and dict actions (from bridge)
        if isinstance(action, int):
            action_type = action
            crafted_item = 0
        else:
            action_type = action.get('action_type', 0)
            crafted_item = action.get('target_block', 0)

        # First craft discovery - BIG bonus (crafting is complex)
        if action_type in [27, 28]:  # CRAFT_ITEM, CRAFT_UNKNOWN
            if crafted_item not in self.discovered_crafts and crafted_item != 0:
                self.discovered_crafts.add(crafted_item)
                reward += 50.0  # Significant bonus for new craft discovery

        # First tool use (could add tracking later)
        # First armor equipped (could add tracking later)
        # First night survived (could add tracking later)
        # First shelter built (could add tracking later)

        return reward

    def _episode_completion_reward(self, final_state: Dict[str, Any]) -> float:
        """
        Calculate episode completion reward
        Bonus rewards based on actual accomplishments during episode
        """
        reward = 0.0

        # Survival bonus (handle both list [health] and scalar health)
        # Only give survival bonus if still alive
        health = final_state.get('health', [20])
        if isinstance(health, list):
            health = health[0] if len(health) > 0 else 20
        if health > 10:
            survival_bonus = self.reward_config.get('survival_bonus', 100)
            reward += survival_bonus

        # Building bonus - tiered based on amount
        if self.episode_placed_blocks > 50:
            reward += 100  # Big bonus for significant building
        elif self.episode_placed_blocks > 20:
            reward += 50  # Medium bonus

        # Mining bonus - tiered based on amount
        total_mined = sum(self.episode_mined_blocks.values())
        if total_mined > 100:
            reward += 50  # Bonus for significant mining
        elif total_mined > 50:
            reward += 25  # Medium bonus

        # Crafting bonus - tiered based on items crafted
        total_crafted = sum(self.episode_crafted_items.values())
        if total_crafted > 20:
            reward += 100  # Big bonus for lots of crafting
        elif total_crafted > 10:
            reward += 50  # Medium bonus
        elif total_crafted > 0:
            reward += 10  # Small bonus for crafting anything

        # Discovery bonus - new things discovered
        discoveries = len(self.discovered_blocks) + len(self.discovered_crafts)
        if discoveries > 10:
            reward += 50  # Bonus for exploration

        return reward

    def get_statistics(self) -> Dict[str, Any]:
        """
        Get reward statistics for the episode

        Returns:
            Dictionary with statistics
        """
        return {
            'discovered_blocks': len(self.discovered_blocks),
            'discovered_biomes': len(self.discovered_biomes),
            'discovered_crafts': len(self.discovered_crafts),
            'visited_chunks': len(self.visited_chunks),
            'blocks_mined': dict(self.episode_mined_blocks),
            'items_crafted': dict(self.episode_crafted_items),
            'blocks_placed': self.episode_placed_blocks,
            'distance_traveled': self.total_distance,
        }


class CurriculumRewardShaper:
    """
    Reward shaping for curriculum learning

    Adjusts rewards based on curriculum stage to encourage
    specific behaviors at each stage.
    """

    def __init__(self, config: Dict[str, Any]):
        """Initialize curriculum reward shaper"""
        self.config = config
        self.curriculum_config = config.get('training.curriculum', {})
        self.current_stage = 0
        self.stages = self.curriculum_config.get('stages', [])

    def set_stage(self, stage_index: int):
        """Set current curriculum stage"""
        self.current_stage = max(0, min(stage_index, len(self.stages) - 1))

    def shape_reward(self, reward: float, stage: str) -> float:
        """
        Scale reward based on curriculum stage

        Args:
            reward: Raw reward
            stage: Current stage name

        Returns:
            Scaled reward
        """
        if self.current_stage < len(self.stages):
            stage_config = self.stages[self.current_stage]
            reward_scale = stage_config.get('reward_scale', 1.0)
            return reward * reward_scale

        return reward

    def should_transition(self, episode_rewards: List[float]) -> bool:
        """
        Check if curriculum should progress to next stage

        Args:
            episode_rewards: Recent episode rewards

        Returns:
            True if should transition
        """
        if self.current_stage >= len(self.stages) - 1:
            return False  # Already at last stage

        # Simple heuristic: transition if average reward is positive
        if len(episode_rewards) >= 10:
            avg_reward = np.mean(episode_rewards[-10:])
            return avg_reward > 0

        return False


def create_reward_system(config: Dict[str, Any]) -> RewardSystem:
    """
    Factory function to create reward system

    Args:
        config: Configuration dictionary

    Returns:
        RewardSystem instance
    """
    return RewardSystem(config)
