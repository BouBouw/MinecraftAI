"""
Auto-Curriculum: Agent sets its own learning goals

Unlike fixed curriculum, the agent:
1. Discovers mechanics autonomously
2. Sets sub-goals based on what it doesn't know
3. Gradually increases complexity as it masters skills
4. Learns ALL mechanics without human specification
"""

import numpy as np
from typing import Dict, Any, List, Tuple, Set
from collections import defaultdict, deque
from dataclasses import dataclass
from enum import Enum

from utils.logger import get_logger

logger = get_logger(__name__)


class SkillLevel(Enum):
    """Mastery level for a mechanic"""
    UNKNOWN = 0      # Never encountered
    NOVICE = 1       # Tried once, don't understand
    APPRENTICE = 2   # Can do it with difficulty
    COMPETENT = 3    # Can do it reliably
    EXPERT = 4       # Mastered, can optimize
    INNOVATOR = 5    # Discovers new uses


@dataclass
class Mechanic:
    """
    Represents a game mechanic the bot can learn
    """
    name: str
    description: str
    required_skills: List[str]  # Prerequisites
    skill_level: SkillLevel = SkillLevel.UNKNOWN
    attempts: int = 0
    successes: int = 0
    failures: int = 0
    last_attempt: int = -1
    discovery_step: int = -1

    @property
    def success_rate(self) -> float:
        """Success rate for this mechanic"""
        if self.attempts == 0:
            return 0.0
        return self.successes / self.attempts

    @property
    def mastery(self) -> float:
        """Mastery score (0-1)"""
        return self.skill_level.value / 5.0

    def update(self, success: bool, step: int):
        """Update mechanic statistics"""
        self.attempts += 1
        self.last_attempt = step

        if success:
            self.successes += 1
            # Level up if enough successes
            if self.skill_level == SkillLevel.UNKNOWN and self.successes >= 1:
                self.skill_level = SkillLevel.NOVICE
                logger.info(f"🎓 Learned new skill: {self.name} (NOVICE)")
            elif self.skill_level == SkillLevel.NOVICE and self.successes >= 5:
                self.skill_level = SkillLevel.APPRENTICE
                logger.info(f"🎓 Improved skill: {self.name} (APPRENTICE)")
            elif self.skill_level == SkillLevel.APPRENTICE and self.successes >= 20:
                self.skill_level = SkillLevel.COMPETENT
                logger.info(f"🎓 Improved skill: {self.name} (COMPETENT)")
            elif self.skill_level == SkillLevel.COMPETENT and self.successes >= 50:
                self.skill_level = SkillLevel.EXPERT
                logger.info(f"🎓 Mastered skill: {self.name} (EXPERT)")
            elif self.skill_level == SkillLevel.EXPERT and self.successes >= 100:
                self.skill_level = SkillLevel.INNOVATOR
                logger.info(f"🎓 Innovated with skill: {self.name} (INNOVATOR)")
        else:
            self.failures += 1


class AutoCurriculum:
    """
    Auto-generating curriculum based on agent's discovery and mastery

    The agent:
    1. Discovers mechanics through exploration
    2. Tracks mastery level for each mechanic
    3. Sets learning goals based on prerequisites
    4. Adjusts action availability based on current goals
    """

    # All discoverable mechanics in Minecraft
    MECHANICS_DEFINITIONS = [
        # Basic Movement
        {"name": "move_forward", "description": "Move forward", "required_skills": []},
        {"name": "move_backward", "description": "Move backward", "required_skills": []},
        {"name": "move_left", "description": "Strafe left", "required_skills": []},
        {"name": "move_right", "description": "Strafe right", "required_skills": []},
        {"name": "jump", "description": "Jump", "required_skills": []},
        {"name": "sneak", "description": "Sneak (slow)", "required_skills": []},
        {"name": "sprint", "description": "Sprint (fast)", "required_skills": []},

        # Looking
        {"name": "look_around", "description": "Look around", "required_skills": []},

        # Basic Interaction
        {"name": "attack", "description": "Attack entities", "required_skills": ["look_around"]},
        {"name": "mine_block", "description": "Mine blocks", "required_skills": ["look_around", "attack"]},

        # Block Types Discovery
        {"name": "mine_dirt", "description": "Mine dirt", "required_skills": ["mine_block"]},
        {"name": "mine_stone", "description": "Mine stone", "required_skills": ["mine_block"]},
        {"name": "mine_wood", "description": "Mine wood", "required_skills": ["mine_block"]},
        {"name": "mine_sand", "description": "Mine sand", "required_skills": ["mine_block"]},
        {"name": "mine_gravel", "description": "Mine gravel", "required_skills": ["mine_block"]},
        {"name": "mine_coal_ore", "description": "Mine coal", "required_skills": ["mine_stone"]},
        {"name": "mine_iron_ore", "description": "Mine iron", "required_skills": ["mine_stone"]},
        {"name": "mine_gold_ore", "description": "Mine gold", "required_skills": ["mine_stone", "use_stone_pickaxe"]},
        {"name": "mine_diamond_ore", "description": "Mine diamond", "required_skills": ["mine_stone", "use_iron_pickaxe"]},
        {"name": "mine_obsidian", "description": "Mine obsidian", "required_skills": ["mine_diamond_ore"]},

        # Tools
        {"name": "use_wood_pickaxe", "description": "Use wooden pickaxe", "required_skills": []},
        {"name": "use_stone_pickaxe", "description": "Use stone pickaxe", "required_skills": []},
        {"name": "use_iron_pickaxe", "description": "Use iron pickaxe", "required_skills": []},
        {"name": "use_diamond_pickaxe", "description": "Use diamond pickaxe", "required_skills": []},

        # Crafting
        {"name": "craft_planks", "description": "Craft wooden planks", "required_skills": []},
        {"name": "craft_sticks", "description": "Craft sticks", "required_skills": ["craft_planks"]},
        {"name": "craft_workbench", "description": "Craft crafting table", "required_skills": ["craft_planks"]},
        {"name": "craft_wood_pickaxe", "description": "Craft wooden pickaxe", "required_skills": ["craft_sticks", "craft_planks"]},
        {"name": "craft_stone_pickaxe", "description": "Craft stone pickaxe", "required_skills": ["craft_wood_pickaxe", "mine_stone"]},
        {"name": "craft_iron_pickaxe", "description": "Craft iron pickaxe", "required_skills": ["craft_stone_pickaxe", "mine_iron_ore"]},
        {"name": "craft_furnace", "description": "Craft furnace", "required_skills": ["mine_stone", "craft_workbench"]},
        {"name": "smelt_ore", "description": "Smelt ores in furnace", "required_skills": ["craft_furnace"]},

        # Building
        {"name": "place_block", "description": "Place blocks", "required_skills": ["mine_block"]},
        {"name": "build_shelter", "description": "Build simple shelter", "required_skills": ["place_block"]},
        {"name": "build_farm", "description": "Build farm", "required_skills": ["place_block", "mine_water"]},

        # Survival
        {"name": "eat_food", "description": "Eat food", "required_skills": []},
        {"name": "avoid_hunger", "description": "Manage hunger", "required_skills": ["eat_food"]},
        {"name": "avoid_damage", "description": "Avoid taking damage", "required_skills": []},
        {"name": "survive_night", "description": "Survive first night", "required_skills": ["build_shelter"]},

        # Combat
        {"name": "kill_zombie", "description": "Kill zombie", "required_skills": ["attack"]},
        {"name": "kill_skeleton", "description": "Kill skeleton", "required_skills": ["attack"]},
        {"name": "kill_spider", "description": "Kill spider", "required_skills": ["attack"]},
        {"name": "kill_creeper", "description": "Kill creeper", "required_skills": ["attack", "avoid_damage"]},

        # Advanced
        {"name": "use_torch", "description": "Place torches for light", "required_skills": ["craft_sticks", "mine_coal_ore"]},
        {"name": "mine_lava", "description": "Mine lava source (with bucket)", "required_skills": ["mine_iron_ore"]},
        {"name": "use_water_bucket", "description": "Use water bucket", "required_skills": ["mine_iron_ore"]},
        {"name": "enchant_item", "description": "Enchant items", "required_skills": ["mine_diamond_ore", "mine_obsidian"]},
        {"name": "brew_potion", "description": "Brew potions", "required_skills": ["mine_nether"]},
        {"name": "mine_nether", "description": "Enter Nether", "required_skills": ["build_shelter", "mine_obsidian"]},
    ]

    # Action mappings for mechanics
    MECHANIC_ACTIONS = {
        "move_forward": [1],
        "move_backward": [2],
        "move_left": [3],
        "move_right": [4],
        "jump": [5],
        "sneak": [6],
        "sprint": [7],
        "look_around": [8, 9, 10, 11],
        "attack": [12, 17],
        "mine_block": [12, 17],
        "place_block": [19],
        "eat_food": [31],
        "craft": [27, 28],
    }

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.step = 0

        # Initialize all mechanics
        self.mechanics: Dict[str, Mechanic] = {}
        for mech_def in self.MECHANICS_DEFINITIONS:
            self.mechanics[mech_def["name"]] = Mechanic(
                name=mech_def["name"],
                description=mech_def["description"],
                required_skills=mech_def["required_skills"]
            )

        # Discovery tracking
        self.discovered_blocks: Set[int] = set()
        self.discovered_items: Set[int] = set()
        self.discovered_biomes: Set[int] = set()
        self.discovered_entities: Set[str] = set()
        self.discovered_structures: Set[str] = set()

        # Episode history
        self.episode_rewards = deque(maxlen=100)
        self.episode_stats = deque(maxlen=100)

        # Current learning goals (mechanics to focus on)
        self.current_goals: List[str] = []

        # Prerequisites cache
        self._prereq_cache = {}

        logger.info(f"Auto-Curriculum initialized with {len(self.mechanics)} mechanics")

    def discover_mechanic(self, mechanic_name: str, step: int):
        """Mark a mechanic as discovered"""
        if mechanic_name in self.mechanics:
            mech = self.mechanics[mechanic_name]
            if mech.skill_level == SkillLevel.UNKNOWN:
                mech.skill_level = SkillLevel.NOVICE
                mech.discovery_step = step
                logger.info(f"🔍 Discovered new mechanic: {mechanic_name} at step {step}")

    def update_mechanic(self, mechanic_name: str, success: bool, step: int):
        """Update mechanic statistics"""
        if mechanic_name in self.mechanics:
            self.mechanics[mechanic_name].update(success, step)

    def get_available_actions(self) -> List[int]:
        """
        Get available actions based on current learning goals

        Returns:
            List of available action IDs
        """
        # Start with basic actions always available
        available = {0, 1, 2, 3, 4, 5, 8, 9, 10, 11}  # NOOP, movement, look

        # Add actions for current goals
        for goal in self.current_goals:
            if goal in self.MECHANIC_ACTIONS:
                available.update(self.MECHANIC_ACTIONS[goal])

        # Add actions for mastered mechanics (can still use them)
        for mech_name, mech in self.mechanics.items():
            if mech.skill_level.value >= SkillLevel.COMPETENT.value:
                if mech_name in self.MECHANIC_ACTIONS:
                    available.update(self.MECHANIC_ACTIONS[mech_name])

        # If very early, enable mining for discovery
        if self.step < 1000:
            available.update([12, 17])  # ATTACK/MINE

        return sorted(list(available))

    def set_learning_goals(self):
        """
        Automatically set learning goals based on:
        1. What's not yet discovered
        2. What prerequisites are met
        3. What would be most valuable to learn next
        """
        self.current_goals = []

        # 1. Prioritize undiscovered mechanics with met prerequisites
        candidates = []

        for mech_name, mech in self.mechanics.items():
            if mech.skill_level == SkillLevel.UNKNOWN:
                # Check if prerequisites are met
                if self._prerequisites_met(mech_name):
                    # Score this mechanic
                    score = self._score_mechanic(mech_name)
                    candidates.append((score, mech_name))

        # Sort by score and pick top 5 as goals
        candidates.sort(reverse=True, key=lambda x: x[0])
        self.current_goals = [name for _, name in candidates[:5]]

        if self.step % 1000 == 0 and self.current_goals:
            logger.info(f"🎯 Current learning goals: {self.current_goals}")

    def _prerequisites_met(self, mechanic_name: str) -> bool:
        """Check if prerequisites for a mechanic are met"""
        if mechanic_name in self._prereq_cache:
            return self._prereq_cache[mechanic_name]

        mech = self.mechanics.get(mechanic_name)
        if not mech:
            return False

        # Check if all required skills are at least COMPETENT
        met = all(
            self.mechanics.get(req, Mechanic(req, "", [])).skill_level.value >= SkillLevel.COMPETENT.value
            for req in mech.required_skills
        )

        self._prereq_cache[mechanic_name] = met
        return met

    def _score_mechanic(self, mechanic_name: str) -> float:
        """
        Score a mechanic based on:
        1. How many other mechanics unlock it
        2. How important it is for survival
        3. Discovery potential
        """
        score = 0.0

        # 1. Count how many mechanics require this one
        unlocks_count = sum(
            1 for mech in self.mechanics.values()
            if mechanic_name in mech.required_skills
        )
        score += unlocks_count * 10  # High value for unlocking others

        # 2. Survival importance
        survival_keywords = ["eat", "avoid", "survive", "shelter", "kill"]
        if any(kw in mechanic_name for kw in survival_keywords):
            score += 5

        # 3. Resource gathering importance
        resource_keywords = ["mine", "craft", "smelt", "build"]
        if any(kw in mechanic_name for kw in resource_keywords):
            score += 3

        return score

    def discover_block(self, block_id: int, block_name: str = "unknown"):
        """Record discovery of new block type"""
        if block_id not in self.discovered_blocks:
            self.discovered_blocks.add(block_id)
            logger.info(f"🧱 Discovered new block: {block_name} (ID: {block_id})")

            # Update relevant mechanics
            if "dirt" in block_name:
                self.discover_mechanic("mine_dirt", self.step)
            elif "stone" in block_name:
                self.discover_mechanic("mine_stone", self.step)
            elif "wood" in block_name or "log" in block_name:
                self.discover_mechanic("mine_wood", self.step)
            elif "coal_ore" in block_name:
                self.discover_mechanic("mine_coal_ore", self.step)
            elif "iron_ore" in block_name:
                self.discover_mechanic("mine_iron_ore", self.step)
            elif "gold_ore" in block_name:
                self.discover_mechanic("mine_gold_ore", self.step)
            elif "diamond_ore" in block_name:
                self.discover_mechanic("mine_diamond_ore", self.step)
            elif "obsidian" in block_name:
                self.discover_mechanic("mine_obsidian", self.step)

    def discover_entity(self, entity_name: str):
        """Record discovery of new entity type"""
        if entity_name not in self.discovered_entities:
            self.discovered_entities.add(entity_name)
            logger.info(f"👾 Discovered new entity: {entity_name}")

            # Update combat mechanics
            if entity_name == "zombie":
                self.discover_mechanic("kill_zombie", self.step)
            elif entity_name == "skeleton":
                self.discover_mechanic("kill_skeleton", self.step)
            elif entity_name == "spider":
                self.discover_mechanic("kill_spider", self.step)
            elif entity_name == "creeper":
                self.discover_mechanic("kill_creeper", self.step)

    def update(self, step: int):
        """Update curriculum state"""
        self.step = step

        # Periodically set new learning goals
        if step % 500 == 0:
            self.set_learning_goals()

    def get_progress_summary(self) -> Dict[str, Any]:
        """Get curriculum progress summary"""
        discovered = sum(1 for m in self.mechanics.values() if m.skill_level != SkillLevel.UNKNOWN)
        mastered = sum(1 for m in self.mechanics.values() if m.skill_level.value >= SkillLevel.EXPERT.value)

        return {
            'total_mechanics': len(self.mechanics),
            'discovered_mechanics': discovered,
            'mastered_mechanics': mastered,
            'discovery_percentage': (discovered / len(self.mechanics)) * 100,
            'mastery_percentage': (mastered / len(self.mechanics)) * 100,
            'current_goals': self.current_goals,
            'discovered_blocks': len(self.discovered_blocks),
            'discovered_entities': len(self.discovered_entities),
            'discovered_biomes': len(self.discovered_biomes),
        }

    def get_mechanic_report(self) -> str:
        """Generate detailed report of all mechanics"""
        lines = ["\n📊 MECHANIC MASTERY REPORT", "=" * 60]

        for category in ["Movement", "Mining", "Crafting", "Building", "Survival", "Combat"]:
            lines.append(f"\n{category}:")
            for mech_name, mech in self.mechanics.items():
                if any(cat.lower() in mech_name for cat in [category.lower()]):
                    status = "❓UNKNOWN"
                    if mech.skill_level == SkillLevel.NOVICE:
                        status = "🌱NOVICE"
                    elif mech.skill_level == SkillLevel.APPRENTICE:
                        status = "📚APPRENTICE"
                    elif mech.skill_level == SkillLevel.COMPETENT:
                        status = "✅COMPETENT"
                    elif mech.skill_level == SkillLevel.EXPERT:
                        status = "⭐EXPERT"
                    elif mech.skill_level == SkillLevel.INNOVATOR:
                        status = "🚀INNOVATOR"

                    lines.append(f"  {mech.name:25} {status:15} ({mech.successes}/{mech.attempts} attempts)")

        return "\n".join(lines)


def create_auto_curriculum(config: Dict[str, Any]) -> AutoCurriculum:
    """
    Factory function to create auto-curriculum

    Args:
        config: Configuration dictionary

    Returns:
        AutoCurriculum instance
    """
    return AutoCurriculum(config)
