"""Craft discovery system for Minecraft RL agent"""

from .craft_discovery import CraftDiscoverySystem, CraftExperiment
from .recipe_learner import RecipeLearner
from .experiment_tracker import ExperimentTracker
from .recipe_db import RecipeDatabase
from .base_knowledge import BASE_RECIPES, BLOCK_KNOWLEDGE, MOB_KNOWLEDGE, ITEM_KNOWLEDGE, SURVIVAL_RULES, ACTION_SEQUENCES, RESOURCE_PRIORITIES, BIOME_KNOWLEDGE
from .block_knowledge import BLOCK_DATABASE, get_block_info, should_avoid_block, get_block_priority
from .mob_knowledge import MOB_DATABASE, get_mob_info, get_mob_danger_level, is_mob_hostile, get_mob_strategies, get_mob_drops, get_tameable_mobs, get_hostile_mobs, get_boss_mobs
from .vanilla_recipes import VANILLA_RECIPES
from .enchantment_knowledge import ENCHANTMENT_DATABASE, get_enchantment_info, get_enchantments_for_item, get_best_weapon_enchantment, get_best_armor_enchantment, get_all_combat_enchantments, get_all_armor_enchantments
from .potion_knowledge import POTION_DATABASE, get_potion_info, get_all_positive_effects, get_all_negative_effects, get_potion_brewing_recipe, get_potion_duration, get_best_combat_potions, get_best_exploration_potions
from .biome_knowledge import BIOME_DATABASE, STRUCTURE_DATABASE, DIMENSION_DATABASE, get_biome_info, get_structure_info, get_dimension_info, get_safe_biomes, get_best_biomes_for_resource
from .redstone_knowledge import REDSTONE_BASICS, COMMON_CIRCUITS, AUTOMATION_SYSTEMS, get_component_info, get_circuit_info, get_automation_info, get_logic_gates, get_farm_types
from .knowledge_loader import KnowledgeLoader, get_knowledge_loader, get_all_knowledge, get_recipe, is_dangerous_mob, is_dangerous_block

__all__ = [
    # Craft discovery
    'CraftDiscoverySystem',
    'CraftExperiment',
    'RecipeLearner',
    'ExperimentTracker',
    'RecipeDatabase',
    # Knowledge modules
    'BASE_RECIPES',
    'BLOCK_KNOWLEDGE',
    'MOB_KNOWLEDGE',
    'ITEM_KNOWLEDGE',
    'SURVIVAL_RULES',
    'ACTION_SEQUENCES',
    'RESOURCE_PRIORITIES',
    'BIOME_KNOWLEDGE',
    'BLOCK_DATABASE',
    'MOB_DATABASE',
    'VANILLA_RECIPES',
    'ENCHANTMENT_DATABASE',
    'POTION_DATABASE',
    'BIOME_DATABASE',
    'STRUCTURE_DATABASE',
    'DIMENSION_DATABASE',
    'REDSTONE_BASICS',
    'COMMON_CIRCUITS',
    'AUTOMATION_SYSTEMS',
    # Block knowledge helpers
    'get_block_info',
    'should_avoid_block',
    'get_block_priority',
    # Mob knowledge helpers
    'get_mob_info',
    'get_mob_danger_level',
    'is_mob_hostile',
    'get_mob_strategies',
    'get_mob_drops',
    'get_tameable_mobs',
    'get_hostile_mobs',
    'get_boss_mobs',
    # Enchantment knowledge helpers
    'get_enchantment_info',
    'get_enchantments_for_item',
    'get_best_weapon_enchantment',
    'get_best_armor_enchantment',
    'get_all_combat_enchantments',
    'get_all_armor_enchantments',
    # Potion knowledge helpers
    'get_potion_info',
    'get_all_positive_effects',
    'get_all_negative_effects',
    'get_potion_brewing_recipe',
    'get_potion_duration',
    'get_best_combat_potions',
    'get_best_exploration_potions',
    # Biome/structure/dimension knowledge helpers
    'get_biome_info',
    'get_structure_info',
    'get_dimension_info',
    'get_safe_biomes',
    'get_best_biomes_for_resource',
    # Redstone knowledge helpers
    'get_component_info',
    'get_circuit_info',
    'get_automation_info',
    'get_logic_gates',
    'get_farm_types',
    # Knowledge loader
    'KnowledgeLoader',
    'get_knowledge_loader',
    'get_all_knowledge',
    'get_recipe',
    'is_dangerous_mob',
    'is_dangerous_block',
]
