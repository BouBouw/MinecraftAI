"""Craft discovery system for Minecraft RL agent"""

from .craft_discovery import CraftDiscoverySystem, CraftExperiment
from .recipe_learner import RecipeLearner
from .experiment_tracker import ExperimentTracker
from .recipe_db import RecipeDatabase
from .base_knowledge import BASE_RECIPES, BLOCK_KNOWLEDGE, MOB_KNOWLEDGE, ITEM_KNOWLEDGE, SURVIVAL_RULES, ACTION_SEQUENCES, RESOURCE_PRIORITIES, BIOME_KNOWLEDGE
from .block_knowledge import BLOCK_DATABASE, get_block_info, should_avoid_block, get_block_priority
from .mob_knowledge import MOB_DATABASE, get_mob_info, get_mob_danger_level, is_mob_hostile, get_mob_strategies, get_mob_drops, get_tameable_mobs, get_hostile_mobs, get_boss_mobs
from .vanilla_recipes import VANILLA_RECIPES
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
    # Knowledge loader
    'KnowledgeLoader',
    'get_knowledge_loader',
    'get_all_knowledge',
    'get_recipe',
    'is_dangerous_mob',
    'is_dangerous_block',
]
