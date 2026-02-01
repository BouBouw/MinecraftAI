"""
Minecraft Base Knowledge
Essential recipes and rules for Minecraft RL agent
"""

# Essential crafting recipes
BASE_RECIPES = {
    # Wood to Planks
    'log_to_planks': {
        'input': [[None, None, None],
                  [None, 'log', None],
                  [None, None, None]],
        'output': ('planks', 4),
        'description': '1 log → 4 planks'
    },

    # Planks to Sticks
    'planks_to_sticks': {
        'input': [[None, None, None],
                  [None, 'planks', None],
                  [None, 'planks', None]],
        'output': ('sticks', 4),
        'description': '2 planks → 4 sticks'
    },

    # Wooden Pickaxe
    'wooden_pickaxe': {
        'input': [['planks', 'planks', 'planks'],
                  [None, 'sticks', None],
                  [None, 'sticks', None]],
        'output': ('wooden_pickaxe', 1),
        'description': 'Basic mining tool'
    },

    # Crafting Table
    'crafting_table': {
        'input': [['planks', 'planks', None],
                  ['planks', 'planks', None],
                  [None, None, None]],
        'output': ('crafting_table', 1),
        'description': 'Essential for crafting'
    },

    # Furnace
    'furnace': {
        'input': [['cobblestone', 'cobblestone', 'cobblestone'],
                  ['cobblestone', None, 'cobblestone'],
                  ['cobblestone', 'cobblestone', 'cobblestone']],
        'output': ('furnace', 1),
        'description': 'For smelting'
    },

    # Stone Pickaxe
    'stone_pickaxe': {
        'input': [['cobblestone', 'cobblestone', 'cobblestone'],
                  [None, 'sticks', None],
                  [None, 'sticks', None]],
        'output': ('stone_pickaxe', 1),
        'description': 'Better mining tool'
    },

    # Wooden Sword
    'wooden_sword': {
        'input': [[None, 'planks', None],
                  [None, 'planks', None],
                  [None, 'sticks', None]],
        'output': ('wooden_sword', 1),
        'description': 'Basic weapon'
    },

    # Torch
    'torch': {
        'input': [['coal', None, None],
                  [None, 'stick', None],
                  [None, None, None]],
        'output': ('torch', 4),
        'description': 'Light source'
    },

    # Chest
    'chest': {
        'input': [['planks', 'planks', 'planks'],
                  ['planks', None, 'planks'],
                  ['planks', 'planks', 'planks']],
        'output': ('chest', 1),
        'description': 'Storage'
    },
}

# Block properties and drops
BLOCK_KNOWLEDGE = {
    'log': {
        'hardness': 2,
        'tool': 'axe',
        'drops': 'log',
        'description': 'Essential resource from trees',
        'priority': 'high'
    },
    'planks': {
        'hardness': 2,
        'tool': 'axe',
        'drops': 'planks',
        'description': 'Basic building material',
        'priority': 'high'
    },
    'cobblestone': {
        'hardness': 2,
        'tool': 'pickaxe',
        'drops': 'cobblestone',
        'description': 'Mining stone gives cobblestone',
        'priority': 'high'
    },
    'stone': {
        'hardness': 3,
        'tool': 'pickaxe',
        'drops': 'cobblestone',
        'description': 'Must be mined with pickaxe',
        'priority': 'medium'
    },
    'coal_ore': {
        'hardness': 3,
        'tool': 'pickaxe',
        'drops': 'coal',
        'description': 'Fuel for smelting and torches',
        'priority': 'high'
    },
    'iron_ore': {
        'hardness': 3,
        'tool': 'pickaxe',
        'drops': 'raw_iron',
        'description': 'Must be smelted in furnace',
        'priority': 'medium'
    },
    'dirt': {
        'hardness': 0.5,
        'tool': 'shovel',
        'drops': 'dirt',
        'description': 'Can be mined with anything',
        'priority': 'low'
    },
    'grass_block': {
        'hardness': 0.6,
        'tool': 'shovel',
        'drops': 'dirt',
        'description': 'Drops dirt when mined',
        'priority': 'low'
    },
    'sand': {
        'hardness': 0.5,
        'tool': 'shovel',
        'drops': 'sand',
        'description': 'Used for glass',
        'priority': 'low'
    },
    'water': {
        'hardness': 100,
        'tool': None,
        'drops': None,
        'description': 'Cannot be mined, must be avoided',
        'priority': 'avoid'
    },
    'lava': {
        'hardness': 100,
        'tool': None,
        'drops': None,
        'description': 'Dangerous! Causes damage',
        'priority': 'avoid'
    },
}

# Important items and their uses
ITEM_KNOWLEDGE = {
    'wooden_pickaxe': {
        'purpose': 'mine stone and ores',
        'durability': 59,
        'mining_speed': 2.0,
        'priority': 'essential'
    },
    'stone_pickaxe': {
        'purpose': 'mine iron and harder materials',
        'durability': 131,
        'mining_speed': 4.0,
        'priority': 'important'
    },
    'wooden_sword': {
        'purpose': 'defend against mobs',
        'damage': 4,
        'durability': 59,
        'priority': 'important'
    },
    'torch': {
        'purpose': 'light up dark areas',
        'priority': 'important'
    },
    'crafting_table': {
        'purpose': 'craft complex items',
        'priority': 'essential'
    },
    'furnace': {
        'purpose': 'smelt ores and cook food',
        'priority': 'important'
    },
    'chest': {
        'purpose': 'store items',
        'priority': 'useful'
    },
}

# Priority action sequences
ACTION_SEQUENCES = {
    'early_game': [
        {
            'name': 'get_wood',
            'description': 'Find and mine a tree log',
            'actions': ['find_tree', 'mine_log'],
            'reward': 100,
            'blocks_needed': ['log']
        },
        {
            'name': 'craft_planks',
            'description': 'Craft planks from log',
            'actions': ['open_crafting', 'craft_log_to_planks'],
            'reward': 50,
            'items_needed': ['log']
        },
        {
            'name': 'craft_table',
            'description': 'Craft a crafting table',
            'actions': ['open_crafting', 'craft_crafting_table'],
            'reward': 100,
            'items_needed': ['planks']
        },
        {
            'name': 'craft_pickaxe',
            'description': 'Craft a wooden pickaxe',
            'actions': ['open_crafting', 'craft_wooden_pickaxe'],
            'reward': 150,
            'items_needed': ['planks', 'sticks']
        },
        {
            'name': 'mine_stone',
            'description': 'Mine stone with pickaxe',
            'actions': ['find_stone', 'mine_stone'],
            'reward': 50,
            'items_needed': ['wooden_pickaxe']
        },
    ],
    'mid_game': [
        {
            'name': 'get_coal',
            'description': 'Find and mine coal',
            'actions': ['explore_cave', 'mine_coal_ore'],
            'reward': 100,
            'items_needed': ['pickaxe']
        },
        {
            'name': 'craft_torches',
            'description': 'Craft torches for light',
            'actions': ['open_crafting', 'craft_torch'],
            'reward': 80,
            'items_needed': ['coal', 'stick']
        },
        {
            'name': 'get_iron',
            'description': 'Find and mine iron ore',
            'actions': ['explore_cave', 'mine_iron_ore'],
            'reward': 150,
            'items_needed': ['stone_pickaxe']
        },
    ]
}

# Survival rules
SURVIVAL_RULES = {
    'health_low': {
        'threshold': 5,
        'action': 'eat_food',
        'priority': 'critical',
        'message': 'Health critically low! Eat food immediately!'
    },
    'night_coming': {
        'time_threshold': 13000,  # Day ends at 13000
        'actions': ['craft_bed', 'find_shelter', 'place_torches'],
        'priority': 'high',
        'message': 'Night approaching! Find shelter!'
    },
    'hostile_mob': {
        'distance_threshold': 5,
        'actions': ['retreat', 'equip_weapon', 'attack'],
        'priority': 'high',
        'message': 'Hostile mob nearby!'
    },
    'hunger_low': {
        'threshold': 5,
        'action': 'eat_food',
        'priority': 'high',
        'message': 'Hunger low! Eat food!'
    },
    'inventory_full': {
        'threshold': 0.9,  # 90% full
        'action': 'use_chest',
        'priority': 'medium',
        'message': 'Inventory nearly full! Store items.'
    },
}

# Resource gathering priorities
RESOURCE_PRIORITIES = {
    'log': 10,          # Highest priority - essential for tools
    'cobblestone': 8,   # Essential for tools and furnace
    'coal': 9,          # Essential for torches and smelting
    'iron_ore': 7,      # Important for better tools
    'food': 10,         # Critical for survival
    'wool': 3,          # Lower priority - for bed
    'sand': 2,          # Lower priority - for glass
    'dirt': 1,          # Lowest priority - abundant
}

# Mob knowledge
MOB_KNOWLEDGE = {
    'zombie': {
        'hostile': True,
        'damage': 3,
        'health': 20,
        'drops': ['rotten_flesh'],
        'danger_level': 'high',
        'strategy': 'attack_with_weapon or retreat'
    },
    'skeleton': {
        'hostile': True,
        'damage': 2,
        'health': 20,
        'drops': ['arrows', 'bones'],
        'danger_level': 'high',
        'strategy': 'attack_with_shield or retreat'
    },
    'spider': {
        'hostile': True,
        'damage': 2,
        'health': 16,
        'drops': ['string', 'spider_eye'],
        'danger_level': 'medium',
        'strategy': 'attack_with_weapon'
    },
    'creeper': {
        'hostile': True,
        'damage': 65,  # Explosion damage!
        'health': 20,
        'drops': ['gunpowder'],
        'danger_level': 'extreme',
        'strategy': 'run_away_immediately'
    },
    'cow': {
        'hostile': False,
        'damage': 0,
        'health': 10,
        'drops': ['beef', 'leather'],
        'danger_level': 'none',
        'strategy': 'kill_for_food'
    },
    'pig': {
        'hostile': False,
        'damage': 0,
        'health': 10,
        'drops': ['porkchop'],
        'danger_level': 'none',
        'strategy': 'kill_for_food'
    },
    'sheep': {
        'hostile': False,
        'damage': 0,
        'health': 8,
        'drops': ['wool'],
        'danger_level': 'none',
        'strategy': 'shear_for_wool'
    },
    'chicken': {
        'hostile': False,
        'damage': 0,
        'health': 4,
        'drops': ['chicken', 'feather'],
        'danger_level': 'none',
        'strategy': 'kill_for_food'
    },
}

# Biome knowledge
BIOME_KNOWLEDGE = {
    'plains': {
        'resources': ['log', 'dirt', 'grass', 'animals'],
        'danger_level': 'low',
        'description': 'Good starting area with trees and animals'
    },
    'forest': {
        'resources': ['log', 'saplings', 'wolft'],
        'danger_level': 'medium',
        'description': 'Lots of wood, wolves present'
    },
    'desert': {
        'resources': ['sand', 'cactus', 'sandstone'],
        'danger_level': 'medium',
        'description': 'No wood, very hot'
    },
    'mountains': {
        'resources': ['stone', 'coal_ore', 'iron_ore', 'emerald_ore'],
        'danger_level': 'high',
        'description': 'Rich in ores but dangerous falls'
    },
    'cave': {
        'resources': ['coal_ore', 'iron_ore', 'gold_ore', 'diamond_ore'],
        'danger_level': 'very_high',
        'description': 'Best ores but very dangerous'
    },
}

# Helper functions
def get_recipe_for_item(item_name):
    """Get crafting recipe for an item"""
    for recipe_name, recipe in BASE_RECIPES.items():
        if recipe['output'][0] == item_name:
            return recipe
    return None

def get_block_drop(block_name, tool=None):
    """Get what a block drops when mined"""
    if block_name not in BLOCK_KNOWLEDGE:
        return block_name

    block = BLOCK_KNOWLEDGE[block_name]
    if block['tool'] and tool != block['tool']:
        return None  # Wrong tool, can't mine
    return block['drops']

def is_mob_hostile(mob_name):
    """Check if a mob is hostile"""
    return MOB_KNOWLEDGE.get(mob_name, {}).get('hostile', False)

def get_mob_danger(mob_name):
    """Get danger level of a mob"""
    return MOB_KNOWLEDGE.get(mob_name, {}).get('danger_level', 'unknown')

def should_avoid_block(block_name):
    """Check if a block should be avoided"""
    return BLOCK_KNOWLEDGE.get(block_name, {}).get('priority') == 'avoid'

def get_next_goal(current_inventory, completed_goals):
    """Suggest next goal based on current progress"""
    for sequence_name, sequence in ACTION_SEQUENCES.items():
        if sequence_name == 'early_game':
            for goal in sequence:
                if goal not in completed_goals:
                    # Check if we have prerequisites
                    if 'items_needed' in goal:
                        has_prereqs = all(item in current_inventory for item in goal['items_needed'])
                        if has_prereqs or not goal['items_needed']:
                            return goal
    return None
