"""
Complete Minecraft Block Knowledge
All block types, properties, drops, and interactions
"""

BLOCK_DATABASE = {
    # ============================================================
    # OVERWORLD BLOCKS - Natural
    # ============================================================

    # Woods
    'oak_log': {
        'hardness': 2,
        'best_tool': 'axe',
        'drops': 'oak_log',
        'can_burn': True,
        'flammability': 5,
        'categories': ['wood', 'natural', 'resource'],
        'uses': ['planks', 'sticks', 'furnace_fuel', 'building'],
        'priority': 'essential',
        'description': 'Basic wood from oak trees'
    },
    'spruce_log': {
        'hardness': 2,
        'best_tool': 'axe',
        'drops': 'spruce_log',
        'can_burn': True,
        'flammability': 5,
        'categories': ['wood', 'natural', 'resource'],
        'uses': ['planks', 'sticks', 'furnace_fuel', 'building'],
        'priority': 'essential',
        'description': 'Dark wood from spruce trees'
    },
    'birch_log': {
        'hardness': 2,
        'best_tool': 'axe',
        'drops': 'birch_log',
        'can_burn': True,
        'flammability': 5,
        'categories': ['wood', 'natural', 'resource'],
        'uses': ['planks', 'sticks', 'furnace_fuel', 'building'],
        'priority': 'essential',
        'description': 'Light wood from birch trees'
    },
    'jungle_log': {
        'hardness': 2,
        'best_tool': 'axe',
        'drops': 'jungle_log',
        'can_burn': True,
        'flammability': 5,
        'categories': ['wood', 'natural', 'resource'],
        'uses': ['planks', 'sticks', 'furnace_fuel', 'building'],
        'priority': 'essential',
        'description': 'Tropical wood from jungle trees'
    },
    'acacia_log': {
        'hardness': 2,
        'best_tool': 'axe',
        'drops': 'acacia_log',
        'can_burn': True,
        'flammability': 5,
        'categories': ['wood', 'natural', 'resource'],
        'uses': ['planks', 'sticks', 'furnace_fuel', 'building'],
        'priority': 'essential',
        'description': 'Savanna wood from acacia trees'
    },
    'dark_oak_log': {
        'hardness': 2,
        'best_tool': 'axe',
        'drops': 'dark_oak_log',
        'can_burn': True,
        'flammability': 5,
        'categories': ['wood', 'natural', 'resource'],
        'uses': ['planks', 'sticks', 'furnace_fuel', 'building'],
        'priority': 'essential',
        'description': 'Dark wood from dark oak trees'
    },
    'mangrove_log': {
        'hardness': 2,
        'best_tool': 'axe',
        'drops': 'mangrove_log',
        'can_burn': True,
        'flammability': 5,
        'categories': ['wood', 'natural', 'resource'],
        'uses': ['planks', 'sticks', 'furnace_fuel', 'building'],
        'priority': 'essential',
        'description': 'Swamp wood from mangrove trees'
    },
    'crimson_stem': {
        'hardness': 2,
        'best_tool': 'axe',
        'drops': 'crimson_stem',
        'can_burn': False,
        'categories': ['wood', 'nether', 'resource'],
        'uses': ['planks', 'sticks', 'building'],
        'priority': 'essential',
        'description': 'Nether wood from crimson fungi'
    },
    'warped_stem': {
        'hardness': 2,
        'best_tool': 'axe',
        'drops': 'warped_stem',
        'can_burn': False,
        'categories': ['wood', 'nether', 'resource'],
        'uses': ['planks', 'sticks', 'building'],
        'priority': 'essential',
        'description': 'Nether wood from warped fungi'
    },

    # Leaves
    'oak_leaves': {
        'hardness': 0.2,
        'best_tool': 'shears',
        'drops': ['oak_sapling', 'apple', 'stick'],
        'drop_chances': [0.05, 0.005, 0.02],
        'can_burn': True,
        'flammability': 30,
        'categories': ['natural', 'decoration'],
        'uses': ['compost', 'decoration'],
        'gravity': False,
        'transparent': True
    },
    'spruce_leaves': {
        'hardness': 0.2,
        'best_tool': 'shears',
        'drops': 'spruce_sapling',
        'drop_chances': [0.05],
        'can_burn': True,
        'flammability': 30,
        'categories': ['natural', 'decoration'],
        'uses': ['compost', 'decoration'],
        'gravity': False,
        'transparent': True
    },
    'birch_leaves': {
        'hardness': 0.2,
        'best_tool': 'shears',
        'drops': 'birch_sapling',
        'drop_chances': [0.05],
        'can_burn': True,
        'flammability': 30,
        'categories': ['natural', 'decoration'],
        'uses': ['compost', 'decoration'],
        'gravity': False,
        'transparent': True
    },
    'jungle_leaves': {
        'hardness': 0.2,
        'best_tool': 'shears',
        'drops': ['jungle_sapling', 'stick'],
        'drop_chances': [0.025, 0.02],
        'can_burn': True,
        'flammability': 30,
        'categories': ['natural', 'decoration'],
        'uses': ['compost', 'decoration'],
        'gravity': False,
        'transparent': True
    },
    'acacia_leaves': {
        'hardness': 0.2,
        'best_tool': 'shears',
        'drops': ['acacia_sapling', 'stick'],
        'drop_chances': [0.05, 0.02],
        'can_burn': True,
        'flammability': 30,
        'categories': ['natural', 'decoration'],
        'uses': ['compost', 'decoration'],
        'gravity': False,
        'transparent': True
    },
    'dark_oak_leaves': {
        'hardness': 0.2,
        'best_tool': 'shears',
        'drops': ['dark_oak_sapling', 'apple', 'stick'],
        'drop_chances': [0.05, 0.005, 0.02],
        'can_burn': True,
        'flammability': 30,
        'categories': ['natural', 'decoration'],
        'uses': ['compost', 'decoration'],
        'gravity': False,
        'transparent': True
    },
    'azalea_leaves': {
        'hardness': 0.2,
        'best_tool': 'shears',
        'drops': ['azalea_sapling', 'azalea'],
        'drop_chances': [0.05, 0.005],
        'can_burn': True,
        'flammability': 30,
        'categories': ['natural', 'decoration'],
        'uses': ['compost', 'decoration'],
        'gravity': False,
        'transparent': True
    },
    'flowering_azalea_leaves': {
        'hardness': 0.2,
        'best_tool': 'shears',
        'drops': 'azalea',
        'can_burn': True,
        'flammability': 30,
        'categories': ['natural', 'decoration'],
        'uses': ['compost', 'decoration'],
        'gravity': False,
        'transparent': True
    },
    'mangrove_leaves': {
        'hardness': 0.2,
        'best_tool': 'shears',
        'drops': ['mangrove_propagule', 'stick'],
        'drop_chances': [0.05, 0.02],
        'can_burn': True,
        'flammability': 30,
        'categories': ['natural', 'decoration'],
        'uses': ['compost', 'decoration'],
        'gravity': False,
        'transparent': True
    },
    'crimson_leaves': {
        'hardness': 0.2,
        'best_tool': 'shears',
        'drops': [],
        'can_burn': False,
        'categories': ['natural', 'nether', 'decoration'],
        'uses': ['compost'],
        'gravity': False,
        'transparent': True
    },
    'warped_leaves': {
        'hardness': 0.2,
        'best_tool': 'shears',
        'drops': [],
        'can_burn': False,
        'categories': ['natural', 'nether', 'decoration'],
        'uses': ['compost'],
        'gravity': False,
        'transparent': True
    },

    # Saplings
    'oak_sapling': {
        'hardness': 0,
        'best_tool': None,
        'drops': 'oak_sapling',
        'can_burn': True,
        'categories': ['natural', 'resource'],
        'uses': ['tree_farming', 'decoration'],
        'gravity': True,
        'plantable': ['dirt', 'grass_block', 'farmland'],
        'growth_time': 'medium'
    },
    'spruce_sapling': {
        'hardness': 0,
        'best_tool': None,
        'drops': 'spruce_sapling',
        'can_burn': True,
        'categories': ['natural', 'resource'],
        'uses': ['tree_farming', 'decoration'],
        'gravity': True,
        'plantable': ['dirt', 'grass_block', 'farmland'],
        'growth_time': 'medium'
    },
    'birch_sapling': {
        'hardness': 0,
        'best_tool': None,
        'drops': 'birch_sapling',
        'can_burn': True,
        'categories': ['natural', 'resource'],
        'uses': ['tree_farming', 'decoration'],
        'gravity': True,
        'plantable': ['dirt', 'grass_block', 'farmland'],
        'growth_time': 'fast'
    },
    'jungle_sapling': {
        'hardness': 0,
        'best_tool': None,
        'drops': 'jungle_sapling',
        'can_burn': True,
        'categories': ['natural', 'resource'],
        'uses': ['tree_farming', 'decoration'],
        'gravity': True,
        'plantable': ['dirt', 'grass_block', 'farmland'],
        'growth_time': 'slow'
    },
    'acacia_sapling': {
        'hardness': 0,
        'best_tool': None,
        'drops': 'acacia_sapling',
        'can_burn': True,
        'categories': ['natural', 'resource'],
        'uses': ['tree_farming', 'decoration'],
        'gravity': True,
        'plantable': ['dirt', 'grass_block', 'farmland'],
        'growth_time': 'slow'
    },
    'dark_oak_sapling': {
        'hardness': 0,
        'best_tool': None,
        'drops': 'dark_oak_sapling',
        'can_burn': True,
        'categories': ['natural', 'resource'],
        'uses': ['tree_farming', 'decoration'],
        'gravity': True,
        'plantable': ['dirt', 'grass_block', 'farmland'],
        'growth_time': 'slow',
        'special': 'requires_4x4_space'
    },
    'mangrove_propagule': {
        'hardness': 0,
        'best_tool': None,
        'drops': 'mangrove_propagule',
        'can_burn': True,
        'categories': ['natural', 'resource'],
        'uses': ['tree_farming', 'decoration'],
        'gravity': True,
        'plantable': ['dirt', 'grass_block', 'farmland', 'mud'],
        'growth_time': 'slow',
        'special': 'water_rooted'
    },

    # Stone variants
    'stone': {
        'hardness': 1.5,
        'best_tool': 'pickaxe',
        'drops': 'cobblestone',
        'can_burn': False,
        'categories': ['natural', 'building', 'resource'],
        'uses': ['smelt_to_smooth_stone', 'stonecutter', 'building'],
        'priority': 'high',
        'description': 'Common building material'
    },
    'granite': {
        'hardness': 1.5,
        'best_tool': 'pickaxe',
        'drops': 'granite',
        'can_burn': False,
        'categories': ['natural', 'building', 'decoration'],
        'uses': ['building', 'polishing'],
        'priority': 'medium'
    },
    'diorite': {
        'hardness': 1.5,
        'best_tool': 'pickaxe',
        'drops': 'diorite',
        'can_burn': False,
        'categories': ['natural', 'building', 'decoration'],
        'uses': ['building', 'polishing'],
        'priority': 'medium'
    },
    'andesite': {
        'hardness': 1.5,
        'best_tool': 'pickaxe',
        'drops': 'andesite',
        'can_burn': False,
        'categories': ['natural', 'building', 'decoration'],
        'uses': ['building', 'polishing'],
        'priority': 'medium'
    },
    'cobblestone': {
        'hardness': 2,
        'best_tool': 'pickaxe',
        'drops': 'cobblestone',
        'can_burn': False,
        'categories': ['natural', 'building', 'resource'],
        'uses': ['tools', 'crafting_table', 'furnace', 'smelt_to_stone'],
        'priority': 'essential',
        'description': 'First mining material'
    },
    'deepslate': {
        'hardness': 3,
        'best_tool': 'pickaxe',
        'drops': 'deepslate',
        'drops_cobbled': 'cobbled_deepslate',
        'can_burn': False,
        'categories': ['natural', 'building'],
        'uses': ['building'],
        'priority': 'low',
        'description': 'Underground stone variant'
    },
    'tuff': {
        'hardness': 3,
        'best_tool': 'pickaxe',
        'drops': 'tuff',
        'can_burn': False,
        'categories': ['natural', 'decoration'],
        'uses': ['decoration', 'crafting'],
        'priority': 'low'
    },
    'calcite': {
        'hardness': 3,
        'best_tool': 'pickaxe',
        'drops': 'calcite',
        'can_burn': False,
        'categories': ['natural', 'decoration'],
        'uses': ['decoration'],
        'priority': 'low'
    },
    'amethyst_block': {
        'hardness': 1.5,
        'best_tool': 'pickaxe',
        'drops': 'amethyst_block',
        'can_burn': False,
        'categories': ['natural', 'decoration', 'resource'],
        'uses': ['decoration'],
        'priority': 'medium'
    },

    # Ores
    'coal_ore': {
        'hardness': 3,
        'best_tool': 'pickaxe',
        'drops': 'coal',
        'experience': 0.2,
        'can_burn': False,
        'categories': ['natural', 'ore', 'resource'],
        'uses': ['fuel', 'torch', 'crafting'],
        'priority': 'essential',
        'rarity': 'common',
        'y_levels': [0, 132],
        'description': 'Essential fuel source'
    },
    'deepslate_coal_ore': {
        'hardness': 3,
        'best_tool': 'pickaxe',
        'drops': 'coal',
        'experience': 0.2,
        'can_burn': False,
        'categories': ['natural', 'ore', 'resource'],
        'uses': ['fuel', 'torch', 'crafting'],
        'priority': 'essential',
        'rarity': 'common',
        'y_levels': [0, 132],
        'description': 'Coal in deepslate'
    },
    'iron_ore': {
        'hardness': 3,
        'best_tool': 'pickaxe',
        'drops': 'raw_iron',
        'experience': 0.3,
        'can_burn': False,
        'categories': ['natural', 'ore', 'resource'],
        'uses': ['smelt_to_iron_ingot', 'iron_tools', 'iron_armor'],
        'priority': 'essential',
        'rarity': 'common',
        'y_levels': [-64, 72, 80, 256],
        'description': 'Essential for tools and armor'
    },
    'deepslate_iron_ore': {
        'hardness': 3,
        'best_tool': 'pickaxe',
        'drops': 'raw_iron',
        'experience': 0.3,
        'can_burn': False,
        'categories': ['natural', 'ore', 'resource'],
        'uses': ['smelt_to_iron_ingot', 'iron_tools', 'iron_armor'],
        'priority': 'essential',
        'rarity': 'common',
        'description': 'Iron in deepslate'
    },
    'copper_ore': {
        'hardness': 3,
        'best_tool': 'pickaxe',
        'drops': 'raw_copper',
        'experience': 0.3,
        'can_burn': False,
        'categories': ['natural', 'ore', 'resource'],
        'uses': ['smelt_to_copper_ingot', 'copper_blocks', 'lightning_rod', 'spyglass'],
        'priority': 'high',
        'rarity': 'common',
        'y_levels': [-16, 112],
        'description': 'Copper for redstone and decoration'
    },
    'deepslate_copper_ore': {
        'hardness': 3,
        'best_tool': 'pickaxe',
        'drops': 'raw_copper',
        'experience': 0.3,
        'can_burn': False,
        'categories': ['natural', 'ore', 'resource'],
        'uses': ['smelt_to_copper_ingot'],
        'priority': 'high',
        'rarity': 'common'
    },
    'gold_ore': {
        'hardness': 3,
        'best_tool': 'pickaxe',
        'drops': 'raw_gold',
        'experience': 1.0,
        'can_burn': False,
        'categories': ['natural', 'ore', 'resource'],
        'uses': ['smelt_to_gold_ingot', 'golden_apple', 'golden_tools', 'powered_rail'],
        'priority': 'high',
        'rarity': 'uncommon',
        'y_levels': [-64, 32],
        'description': 'Gold for fast tools and rail'
    },
    'deepslate_gold_ore': {
        'hardness': 3,
        'best_tool': 'pickaxe',
        'drops': 'raw_gold',
        'experience': 1.0,
        'can_burn': False,
        'categories': ['natural', 'ore', 'resource'],
        'uses': ['smelt_to_gold_ingot'],
        'priority': 'high',
        'rarity': 'uncommon'
    },
    'lapis_ore': {
        'hardness': 3,
        'best_tool': 'pickaxe',
        'drops': 'lapis_lazuli',
        'drop_range': (4, 9),
        'experience': 0.2,
        'can_burn': False,
        'categories': ['natural', 'ore', 'resource'],
        'uses': ['enchanting', 'decoration', 'blue_dye'],
        'priority': 'high',
        'rarity': 'uncommon',
        'y_levels': [-64, 64],
        'description': 'Enchanting material'
    },
    'deepslate_lapis_ore': {
        'hardness': 3,
        'best_tool': 'pickaxe',
        'drops': 'lapis_lazuli',
        'drop_range': (4, 9),
        'experience': 0.2,
        'can_burn': False,
        'categories': ['natural', 'ore', 'resource'],
        'uses': ['enchanting'],
        'priority': 'high',
        'rarity': 'uncommon'
    },
    'redstone_ore': {
        'hardness': 3,
        'best_tool': 'iron_pickaxe',
        'drops': 'redstone',
        'drop_range': (1, 5),
        'experience': 0.6,
        'can_burn': False,
        'categories': ['natural', 'ore', 'resource'],
        'uses': ['redstone_circuits', 'piston', 'crafting'],
        'priority': 'high',
        'rarity': 'uncommon',
        'y_levels': [-64, 16],
        'description': 'Redstone for circuits and automation'
    },
    'deepslate_redstone_ore': {
        'hardness': 3,
        'best_tool': 'iron_pickaxe',
        'drops': 'redstone',
        'drop_range': (1, 5),
        'experience': 0.6,
        'can_burn': False,
        'categories': ['natural', 'ore', 'resource'],
        'uses': ['redstone'],
        'priority': 'high',
        'rarity': 'uncommon'
    },
    'emerald_ore': {
        'hardness': 3,
        'best_tool': 'iron_pickaxe',
        'drops': 'emerald',
        'experience': 3.0,
        'can_burn': False,
        'categories': ['natural', 'ore', 'resource'],
        'uses': ['trading', 'beacon', 'decoration'],
        'priority': 'medium',
        'rarity': 'rare',
        'y_levels': ['mountains', -16, 256],
        'description': 'Trading currency with villagers'
    },
    'diamond_ore': {
        'hardness': 3,
        'best_tool': 'iron_pickaxe',
        'drops': 'diamond',
        'experience': 3.5,
        'can_burn': False,
        'categories': ['natural', 'ore', 'resource'],
        'uses': ['diamond_tools', 'diamond_armor', 'enchanting_table', 'jukebox'],
        'priority': 'essential',
        'rarity': 'rare',
        'y_levels': [-64, 16],
        'description': 'Best tools and armor'
    },
    'deepslate_diamond_ore': {
        'hardness': 3,
        'best_tool': 'iron_pickaxe',
        'drops': 'diamond',
        'experience': 3.5,
        'can_burn': False,
        'categories': ['natural', 'ore', 'resource'],
        'uses': ['diamond_tools', 'diamond_armor'],
        'priority': 'essential',
        'rarity': 'rare'
    },

    # Dirt and soil
    'dirt': {
        'hardness': 0.5,
        'best_tool': 'shovel',
        'drops': 'dirt',
        'can_burn': False,
        'categories': ['natural', 'building'],
        'uses': ['farming', 'grass_spreading', 'decoration'],
        'gravity': True,
        'priority': 'low'
    },
    'grass_block': {
        'hardness': 0.6,
        'best_tool': 'shovel',
        'drops': 'dirt',
        'can_burn': False,
        'categories': ['natural', 'building'],
        'uses': ['farming', 'decoration'],
        'gravity': True,
        'priority': 'low',
        'description': 'Dirt with grass on top'
    },
    'grass_path': {
        'hardness': 0.6,
        'best_tool': 'shovel',
        'drops': 'dirt',
        'can_burn': False,
        'categories': ['building', 'decoration'],
        'uses': ['pathway'],
        'gravity': True,
        'priority': 'low',
        'description': 'Fast walking path'
    },
    'coarse_dirt': {
        'hardness': 0.5,
        'best_tool': 'shovel',
        'drops': 'dirt',
        'can_burn': False,
        'categories': ['natural', 'building'],
        'uses': ['decoration', 'convert_to_dirt'],
        'gravity': True,
        'priority': 'low'
    },
    'podzol': {
        'hardness': 0.5,
        'best_tool': 'shovel',
        'drops': 'dirt',
        'can_burn': False,
        'categories': ['natural', 'building'],
        'uses': ['growing_trees', 'decoration'],
        'gravity': True,
        'priority': 'low',
        'description': 'Forest floor, grows trees'
    },
    'mycelium': {
        'hardness': 0.5,
        'best_tool': 'shovel',
        'drops': 'dirt',
        'can_burn': False,
        'categories': ['natural', 'building'],
        'uses': ['mushroom_farming', 'decoration'],
        'gravity': True,
        'priority': 'low',
        'description': 'Mushroom biome floor'
    },
    'farmland': {
        'hardness': 0.6,
        'best_tool': 'shovel',
        'drops': 'dirt',
        'can_burn': False,
        'categories': ['building', 'farming'],
        'uses': ['crop_farming'],
        'gravity': True,
        'priority': 'high',
        'description': 'Essential for farming'
    },
    'rooted_dirt': {
        'hardness': 0.5,
        'best_tool': 'shovel',
        'drops': 'dirt',
        'can_burn': False,
        'categories': ['natural', 'building'],
        'uses': ['tree_farming'],
        'gravity': True,
        'priority': 'low'
    },
    'mud': {
        'hardness': 0.5,
        'best_tool': 'shovel',
        'drops': 'dirt',
        'can_burn': False,
        'categories': ['natural', 'building'],
        'uses': ['mangrove_farming', 'decoration'],
        'gravity': True,
        'priority': 'low'
    },

    # Sand
    'sand': {
        'hardness': 0.5,
        'best_tool': 'shovel',
        'drops': 'sand',
        'can_burn': False,
        'categories': ['natural', 'building', 'resource'],
        'uses': ['glass', ' TNT', 'sandstone', 'concrete'],
        'gravity': True,
        'priority': 'high',
        'description': 'Desert material, essential for glass'
    },
    'red_sand': {
        'hardness': 0.5,
        'best_tool': 'shovel',
        'drops': 'red_sand',
        'can_burn': False,
        'categories': ['natural', 'building', 'resource'],
        'uses': ['red_sandstone', ' TNT', 'concrete'],
        'gravity': True,
        'priority': 'high',
        'description': 'Badlands sand'
    },
    'gravel': {
        'hardness': 0.6,
        'best_tool': 'shovel',
        'drops': ['gravel', 'flint'],
        'drop_chances': [0.9, 0.1],
        'can_burn': False,
        'categories': ['natural', 'building', 'resource'],
        'uses': ['concrete', 'arrow', 'flint_and_steel'],
        'gravity': True,
        'priority': 'medium',
        'description': 'Source of flint'
    },
    'soul_sand': {
        'hardness': 0.5,
        'best_tool': 'shovel',
        'drops': 'soul_sand',
        'can_burn': False,
        'categories': ['natural', 'nether', 'building'],
        'uses': ['soul_torch', 'bubble_column', 'growing_nether_wart'],
        'gravity': True,
        'priority': 'high',
        'description': 'Slows entities and bubbles'
    },
    'soul_soil': {
        'hardness': 0.5,
        'best_tool': 'shovel',
        'drops': 'soul_soil',
        'can_burn': False,
        'categories': ['natural', 'nether', 'building'],
        'uses': ['soul_torch', 'growing_nether_wart'],
        'gravity': True,
        'priority': 'high'
    },

    # Clay
    'clay': {
        'hardness': 0.6,
        'best_tool': 'shovel',
        'drops': 'clay_ball',
        'drop_range': (1, 4),
        'can_burn': False,
        'categories': ['natural', 'resource'],
        'uses': ['bricks', 'terracotta'],
        'gravity': True,
        'priority': 'medium'
    },

    # Snow and ice
    'snow': {
        'hardness': 0.2,
        'best_tool': 'shovel',
        'drops': 'snowball',
        'drop_range': (1, 7),
        'can_burn': False,
        'categories': ['natural', 'decoration'],
        'uses': ['snow_block', 'snowball_weapon'],
        'gravity': False,
        'transparent': False
    },
    'snow_block': {
        'hardness': 0.2,
        'best_tool': 'shovel',
        'drops': 'snow',
        'can_burn': False,
        'categories': ['building', 'decoration'],
        'uses': ['decoration'],
        'gravity': True
    },
    'ice': {
        'hardness': 0.5,
        'best_tool': 'pickaxe',
        'drops': None,
        'can_burn': False,
        'categories': ['natural', 'decoration'],
        'uses': ['decoration', 'water_bucket'],
        'gravity': False,
        'transparent': True,
        'friction': 0.98,
        'description': 'Slippery, melts near light'
    },
    'packed_ice': {
        'hardness': 0.5,
        'best_tool': 'pickaxe',
        'drops': None,
        'can_burn': False,
        'categories': ['building', 'decoration'],
        'uses': ['blue_ice', 'decoration'],
        'gravity': True,
        'friction': 0.98,
        'description': 'Does not melt'
    },
    'blue_ice': {
        'hardness': 2.8,
        'best_tool': 'pickaxe',
        'drops': None,
        'can_burn': False,
        'categories': ['building', 'decoration'],
        'uses': ['decoration'],
        'gravity': True,
        'friction': 0.98,
        'description': 'Slipperiest block, fastest boat'
    },
    'powder_snow': {
        'hardness': 0.25,
        'best_tool': 'shovel',
        'drops': 'powder_snow',
        'can_burn': False,
        'categories': ['natural', 'decoration'],
        'uses': ['snow_block', 'decoration'],
        'gravity': True,
        'description': 'Minecraft powder snow'
    },

    # Water
    'water': {
        'hardness': 100,
        'best_tool': None,
        'drops': None,
        'can_burn': False,
        'categories': ['natural', 'liquid'],
        'uses': ['fishing', 'farming', 'bucket'],
        'gravity': False,
        'transparent': True,
        'description': 'Essential for farming and fishing'
    },

    # Lava
    'lava': {
        'hardness': 100,
        'best_tool': None,
        'drops': None,
        'can_burn': True,
        'categories': ['natural', 'liquid', 'dangerous'],
        'uses': ['fuel', 'obsidian', 'cobblestone_generator'],
        'gravity': False,
        'transparent': True,
        'damage': 4,
        'light': 15,
        'description': 'Dangerous liquid, excellent fuel'
    },

    # ============================================================
    # NETHER BLOCKS
    # ============================================================

    'netherrack': {
        'hardness': 0.4,
        'best_tool': 'pickaxe',
        'drops': 'netherrack',
        'can_burn': False,
        'categories': ['nether', 'building', 'natural'],
        'uses': ['smelt_to_nether_brick', 'decoration'],
        'priority': 'medium',
        'flammability': 0,
        'gravity': True,
        'description': 'Main nether building block'
    },
    'crimson_nylium': {
        'hardness': 0.4,
        'best_tool': 'pickaxe',
        'drops': 'crimson_nylium',
        'can_burn': False,
        'categories': ['nether', 'natural', 'building'],
        'uses': ['grow_crimson_fungus', 'decoration'],
        'gravity': True,
        'priority': 'medium'
    },
    'warped_nylium': {
        'hardness': 0.4,
        'best_tool': 'pickaxe',
        'drops': 'warped_nylium',
        'can_burn': False,
        'categories': ['nether', 'natural', 'building'],
        'uses': ['grow_warped_fungus', 'decoration'],
        'gravity': True,
        'priority': 'medium'
    },
    'soul_soil': {
        'hardness': 0.5,
        'best_tool': 'shovel',
        'drops': 'soul_soil',
        'can_burn': False,
        'categories': ['nether', 'building', 'natural'],
        'uses': ['soul_fire', 'grow_nether_wart'],
        'gravity': True,
        'priority': 'high'
    },
    'basalt': {
        'hardness': 1.25,
        'best_tool': 'pickaxe',
        'drops': 'basalt',
        'can_burn': False,
        'categories': ['nether', 'building', 'natural'],
        'uses': ['polishing', 'decoration'],
        'gravity': True,
        'priority': 'low'
    },
    'blackstone': {
        'hardness': 1.5,
        'best_tool': 'pickaxe',
        'drops': 'blackstone',
        'can_burn': False,
        'categories': ['nether', 'building', 'natural'],
        'uses': ['polishing', 'tools', 'decoration'],
        'gravity': True,
        'priority': 'high',
        'description': 'Nether equivalent of stone'
    },
    'magma_block': {
        'hardness': 0.5,
        'best_tool': 'pickaxe',
        'drops': 'magma_block',
        'can_burn': False,
        'categories': ['nether', 'building', 'natural', 'dangerous'],
        'uses': ['decoration', 'fuel_bucket'],
        'gravity': True,
        'damage': 1,
        'light': 3,
        'description': 'Magma source'
    },
    'glowstone': {
        'hardness': 0.3,
        'best_tool': None,
        'drops': ['glowstone_dust', 'glowstone'],
        'drop_chances': [0.33, 0.67],
        'can_burn': False,
        'categories': ['nether', 'natural', 'light'],
        'uses': ['redstone_lamp', 'decorative_lighting'],
        'gravity': True,
        'light': 15,
        'priority': 'high',
        'description': 'Bright nether light source'
    },
    'ghast_tear': {
        'hardness': 100,
        'best_tool': None,
        'drops': None,
        'can_burn': False,
        'categories': ['nether', 'resource', 'dropped'],
        'uses': ['end_crystal', 'magma_cream'],
        'priority': 'medium',
        'description': 'Drop from ghasts'
    },
    'nether_quartz_ore': {
        'hardness': 3,
        'best_tool': 'pickaxe',
        'drops': 'nether_quartz',
        'drop_range': (1, 5),
        'experience': 0.2,
        'can_burn': False,
        'categories': ['nether', 'ore', 'resource'],
        'uses': ['quartz_blocks', 'comparator', 'daylight_sensor'],
        'priority': 'high',
        'rarity': 'uncommon',
        'description': 'Nether quartz'
    },
    'ancient_debris': {
        'hardness': 3,
        'best_tool': 'diamond_pickaxe',
        'drops': 'ancient_debris',
        'can_burn': False,
        'categories': ['nether', 'ore', 'resource'],
        'uses': ['smelt_to_netherite_scrap', 'netherite_ingot'],
        'priority': 'essential',
        'rarity': 'very_rare',
        'y_levels': [15, 30, 45],
        'blast_resistance': True,
        'description': 'Netherite source'
    },

    # ============================================================
    # THE END BLOCKS
    # ============================================================

    'end_stone': {
        'hardness': 3,
        'best_tool': 'pickaxe',
        'drops': 'end_stone',
        'can_burn': False,
        'categories': ['end', 'building', 'natural'],
        'uses': ['end_bricks', 'decoration'],
        'gravity': True,
        'priority': 'medium'
    },
    'obsidian': {
        'hardness': 50,
        'best_tool': 'diamond_pickaxe',
        'drops': 'obsidian',
        'can_burn': False,
        'categories': ['natural', 'building', 'resource'],
        'uses': ['enchanting_table', 'ender_chest', 'nether_portal'],
        'priority': 'essential',
        'description': 'Created when water meets lava'
    },
    'crying_obsidian': {
        'hardness': 50,
        'best_tool': 'diamond_pickaxe',
        'drops': 'crying_obsidian',
        'can_burn': False,
        'categories': ['end', 'natural', 'building', 'resource'],
        'uses': ['respawn_anchor', 'lodestone'],
        'priority': 'medium'
    },
    'ender_chest': {
        'hardness': 22.5,
        'best_tool': 'diamond_pickaxe',
        'drops': 'ender_chest',
        'can_burn': False,
        'categories': ['end', 'utility'],
        'uses': ['storage'],
        'priority': 'medium',
        'description': 'Inventory sync across dimensions'
    },
    'chorus_plant': {
        'hardness': 0.4,
        'best_tool': 'axe',
        'drops': ['chorus_fruit', 'chorus_flower'],
        'can_burn': False,
        'categories': ['end', 'natural', 'farming'],
        'uses': ['chorus_fruit', 'purpur'],
        'gravity': False,
        'priority': 'high'
    },
    'chorus_flower': {
        'hardness': 0.4,
        'best_tool': 'axe',
        'drops': 'chorus_flower',
        'can_burn': False,
        'categories': ['end', 'natural', 'resource'],
        'uses': ['purpur_block'],
        'priority': 'high',
        'description': 'Grows chorus plant'
    },
    'chorus_fruit': {
        'hardness': 1,
        'best_tool': 'axe',
        'drops': 'chorus_fruit',
        'can_burn': False,
        'categories': ['end', 'food', 'natural'],
        'hunger': 4,
        'saturation': 2.4,
        'priority': 'medium'
    },
    'shulker_box': {
        'hardness': 2,
        'best_tool': 'pickaxe',
        'drops': 'shulker_box',
        'can_burn': False,
        'categories': ['end', 'utility'],
        'uses': ['storage', 'decoration'],
        'priority': 'medium',
        'description': 'Storage, drops shulker shells'
    },
    'purpur_block': {
        'hardness': 1.5,
        'best_tool': 'pickaxe',
        'drops': 'purpur_block',
        'can_burn': False,
        'categories': ['end', 'building'],
        'uses': ['purpur_pillar', 'purpur_stairs'],
        'gravity': True,
        'priority': 'medium'
    },
    'purpur_pillar': {
        'hardness': 1.5,
        'best_tool': 'pickaxe',
        'drops': 'purpur_pillar',
        'can_burn': False,
        'categories': ['end', 'building'],
        'uses': ['decoration'],
        'gravity': True
    },

    # ============================================================
    # FLUID BLOCKS
    # ============================================================

    'water Cauldron': {
        'hardness': 2,
        'best_tool': None,
        'drops': 'cauldron',
        'can_burn': False,
        'categories': ['utility', 'storage'],
        'uses': ['water_storage', 'dyeing_armor'],
        'priority': 'medium',
        'description': 'Holds water'
    },
    'lava_cauldron': {
        'hardness': 2,
        'best_tool': None,
        'drops': 'cauldron',
        'can_burn': True,
        'categories': ['utility', 'dangerous'],
        'uses': ['lava_storage', 'armor_trimming'],
        'priority': 'low'
    },
    'powder_snow_cauldron': {
        'hardness': 2,
        'best_tool': None,
        'drops': 'cauldron',
        'can_burn': False,
        'categories': ['utility'],
        'uses': ['armor_trimming'],
        'priority': 'low'
    },

    # ============================================================
    # PLANT BLOCKS
    # ============================================================

    'wheat': {
        'hardness': 0,
        'best_tool': None,
        'drops': ['wheat', 'seeds'],
        'can_burn': False,
        'categories': ['natural', 'food', 'farming'],
        'uses': ['bread', 'cake', 'compost'],
        'gravity': False,
        'plantable': 'farmland',
        'growth_stages': 8,
        'priority': 'essential',
        'description': 'Essential food source'
    },
    'carrots': {
        'hardness': 0,
        'best_tool': None,
        'drops': ['carrot', 'carrot'],
        'can_burn': False,
        'categories': ['natural', 'food', 'farming'],
        'uses': ['food', 'golden_carrot', 'rabbit_breeding'],
        'gravity': False,
        'plantable': 'farmland',
        'growth_stages': 8,
        'priority': 'high',
        'description': 'Food and breeding'
    },
    'potatoes': {
        'hardness': 0,
        'best_tool': None,
        'drops': ['potato', 'potato'],
        'can_burn': False,
        'categories': ['natural', 'food', 'farming'],
        'uses': ['food', 'baked_potato', 'poisonous_potato'],
        'gravity': False,
        'plantable': 'farmland',
        'growth_stages': 8,
        'priority': 'high',
        'description': 'Versatile food crop'
    },
    'beetroots': {
        'hardness': 0,
        'best_tool': None,
        'drops': ['beetroot', 'beetroot_seeds'],
        'can_burn': False,
        'categories': ['natural', 'food', 'farming'],
        'uses': ['food', 'beetroot_soup', 'red_dye'],
        'gravity': False,
        'plantable': 'farmland',
        'growth_stages': 4,
        'priority': 'medium',
        'description': 'Food and red dye'
    },
    'pumpkin': {
        'hardness': 1,
        'best_tool': 'axe',
        'drops': 'pumpkin',
        'can_burn': True,
        'categories': ['natural', 'farming', 'decoration'],
        'uses': ['pumpkin_pie', 'pumpkin_seeds', 'iron_golem', 'snow_golem'],
        'gravity': True,
        'plantable': 'farmland',
        'growth_stages': 8,
        'priority': 'medium',
        'description': 'Food and snow golem'
    },
    'melon': {
        'hardness': 1,
        'best_tool': 'axe',
        'drops': ['melon_slice', 'melon_seeds'],
        'drop_chances': [0.9, 0.1],
        'can_burn': True,
        'categories': ['natural', 'farming', 'food'],
        'uses': ['food', 'glistering_melon_slice'],
        'gravity': True,
        'plantable': 'farmland',
        'growth_stages': 8,
        'priority': 'medium',
        'description': 'Growing stem blocks'
    },
    'sugar_cane': {
        'hardness': 0.6,
        'best_tool': None,
        'drops': 'sugar_cane',
        'can_burn': True,
        'categories': ['natural', 'farming', 'resource'],
        'uses': ['sugar', 'paper'],
        'gravity': False,
        'plantable': ['sand', 'grass_block', 'dirt'],
        'growth_stages': 3,
        'priority': 'high',
        'description': 'Essential for cake and potions'
    },
    'cactus': {
        'hardness': 0.4,
        'best_tool': None,
        'drops': 'cactus',
        'can_burn': False,
        'categories': ['natural', 'farming', 'decoration'],
        'uses': ['green_dye', 'defense'],
        'gravity': True,
        'plantable': ['sand', 'red_sand'],
        'damage': 1,
        'priority': 'medium',
        'description': 'Desert plant, damages entities'
    },
    'bamboo': {
        'hardness': 1,
        'best_tool': 'axe',
        'drops': 'bamboo',
        'can_burn': True,
        'categories': ['natural', 'farming', 'resource'],
        'uses': ['scaffolding', 'sticks', 'bamboo_planks'],
        'gravity': True,
        'plantable': ['dirt', 'grass_block', 'sand', 'gravel'],
        'priority': 'high',
        'description': 'Fast growing wood'
    },
    'sugar_cane': {
        'hardness': 0.6,
        'best_tool': None,
        'drops': 'sugar_cane',
        'can_burn': True,
        'categories': ['natural', 'farming', 'resource'],
        'uses': ['sugar', 'paper'],
        'gravity': False,
        'plantable': ['sand', 'grass_block', 'dirt'],
        'growth_stages': 3,
        'priority': 'high'
    },
    'vine': {
        'hardness': 0.2,
        'best_tool': 'axe',
        'drops': 'vine',
        'can_burn': True,
        'categories': ['natural', 'decoration'],
        'uses': ['decoration', 'shears'],
        'gravity': False,
        'transparent': True
    },
    'lily_pad': {
        'hardness': 0,
        'best_tool': None,
        'drops': 'lily_pad',
        'can_burn': False,
        'categories': ['natural', 'decoration'],
        'uses': ['water_transportation'],
        'gravity': False,
        'transparent': False,
        'plantable': 'water',
        'description': 'Walk on water'
    },
    'seagrass': {
        'hardness': 0,
        'best_tool': None,
        'drops': None,
        'can_burn': False,
        'categories': ['natural', 'decoration'],
        'uses': ['compost', 'dried_kelp'],
        'gravity': False,
        'transparent': True
    },
    'kelp': {
        'hardness': 0,
        'best_tool': None,
        'drops': None,
        'can_burn': False,
        'categories': ['natural', 'farming', 'food'],
        'uses': ['dried_kelp', 'smelting_fuel'],
        'gravity': False,
        'transparent': True,
        'priority': 'medium',
        'description': 'Underwater plant'
    },
    'sea_pickle': {
        'hardness': 0,
        'best_tool': None,
        'drops': None,
        'can_burn': False,
        'categories': ['natural', 'decoration'],
        'uses': ['compost', 'light'],
        'gravity': False,
        'transparent': True,
        'light': 14,
        'description': 'Underwater light'
    },

    # Flowers
    'dandelion': {
        'hardness': 0,
        'best_tool': None,
        'drops': 'dandelion',
        'can_burn': False,
        'categories': ['natural', 'decoration', 'resource'],
        'uses': ['yellow_dye', 'rabbit_breeding'],
        'gravity': False,
        'priority': 'low'
    },
    'poppy': {
        'hardness': 0,
        'best_tool': None,
        'drops': 'poppy',
        'can_burn': False,
        'categories': ['natural', 'decoration', 'resource'],
        'uses': ['red_dye', 'rabbit_breeding'],
        'gravity': False,
        'priority': 'low'
    },
    'cornflower': {
        'hardness': 0,
        'best_tool': None,
        'drops': 'cornflower',
        'can_burn': False,
        'categories': ['natural', 'decoration', 'resource'],
        'uses': ['blue_dye'],
        'gravity': False,
        'priority': 'low'
    },
    'lily_of_the_valley': {
        'hardness': 0,
        'best_tool': None,
        'drops': 'lily_of_the_valley',
        'can_burn': False,
        'categories': ['natural', 'decoration', 'dangerous'],
        'uses': ['white_dye'],
        'gravity': False,
        'poisonous': True,
        'priority': 'low'
    },
    'wither_rose': {
        'hardness': 0,
        'best_tool': None,
        'drops': 'wither_rose',
        'can_burn': False,
        'categories': ['natural', 'decoration', 'dangerous'],
        'uses': ['black_dye', 'wither_skeleton_spawn'],
        'gravity': False,
        'priority': 'low'
    },
    'sunflower': {
        'hardness': 0,
        'best_tool': None,
        'drops': 'sunflower',
        'can_burn': False,
        'categories': ['natural', 'decoration'],
        'uses': ['yellow_dye', 'guidance'],
        'gravity': False,
        'priority': 'low',
        'description': 'Always faces east'
    },
    'peony': {
        'hardness': 0,
        'best_tool': None,
        'drops': 'peony',
        'can_burn': False,
        'categories': ['natural', 'decoration'],
        'uses': ['pink_dye'],
        'gravity': False,
        'priority': 'low'
    },
    'lilac': {
        'hardness': 0,
        'best_tool': None,
        'drops': 'lilac',
        'can_burn': False,
        'categories': ['natural', 'decoration'],
        'uses': ['magenta_dye'],
        'gravity': False,
        'priority': 'low'
    },
    'rose_bush': {
        'hardness': 0,
        'best_tool': None,
        'drops': 'rose',
        'can_burn': False,
        'categories': ['natural', 'decoration'],
        'uses': ['red_dye'],
        'gravity': False,
        'priority': 'low'
    },
    'peony': {
        'hardness': 0,
        'best_tool': None,
        'drops': 'peony',
        'can_burn': False,
        'categories': ['natural', 'decoration'],
        'uses': ['pink_dye'],
        'gravity': False,
        'priority': 'low'
    },
    'azure_bluet': {
        'hardness': 0,
        'best_tool': None,
        'drops': 'azure_bluet',
        'can_burn': False,
        'categories': ['natural', 'decoration'],
        'uses': ['light_gray_dye'],
        'gravity': False,
        'priority': 'low'
    },
    'red_tulip': {
        'hardness': 0,
        'best_tool': None,
        'drops': 'red_tulip',
        'can_burn': False,
        'categories': ['natural', 'decoration'],
        'uses': ['red_dye'],
        'gravity': False,
        'priority': 'low'
    },
    'orange_tulip': {
        'hardness': 0,
        'best_tool': None,
        'drops': 'orange_tulip',
        'can_burn': False,
        'categories': ['natural', 'decoration'],
        'uses': ['orange_dye'],
        'gravity': False,
        'priority': 'low'
    },
    'white_tulip': {
        'hardness': 0,
        'best_tool': None,
        'drops': 'white_tulip',
        'can_burn': False,
        'categories': ['natural', 'decoration'],
        'uses': ['light_gray_dye'],
        'gravity': False,
        'priority': 'low'
    },
    'pink_tulip': {
        'hardness': 0,
        'best_tool': None,
        'drops': 'pink_tulip',
        'can_burn': False,
        'categories': ['natural', 'decoration'],
        'uses': ['pink_dye'],
        'gravity': False,
        'priority': 'low'
    },
    'allium': {
        'hardness': 0,
        'best_tool': None,
        'drops': 'allium',
        'can_burn': False,
        'categories': ['natural', 'decoration'],
        'uses': ['magenta_dye'],
        'gravity': False,
        'priority': 'low'
    },
    'blue_orchid': {
        'hardness': 0,
        'best_tool': None,
        'drops': 'blue_orchid',
        'can_burn': False,
        'categories': ['natural', 'decoration'],
        'uses': ['light_blue_dye'],
        'gravity': False,
        'priority': 'low'
    },
    'oxeye_daisy': {
        'hardness': 0,
        'best_tool': None,
        'drops': 'oxeye_daisy',
        'can_burn': False,
        'categories': ['natural', 'decoration'],
        'uses': ['light_gray_dye'],
        'gravity': False,
        'priority': 'low'
    },
    'cornflower': {
        'hardness': 0,
        'best_tool': None,
        'drops': 'cornflower',
        'can_burn': False,
        'categories': ['natural', 'decoration'],
        'uses': ['blue_dye'],
        'gravity': False,
        'priority': 'low'
    },
    'lily_of_the_valley': {
        'hardness': 0,
        'best_tool': None,
        'drops': 'lily_of_the_valley',
        'can_burn': False,
        'categories': ['natural', 'decoration', 'dangerous'],
        'uses': ['white_dye'],
        'gravity': False,
        'poisonous': True,
        'priority': 'low'
    },
    'wither_rose': {
        'hardness': 0,
        'best_tool': None,
        'drops': 'wither_rose',
        'can_burn': False,
        'categories': ['natural', 'decoration', 'dangerous'],
        'uses': ['black_dye'],
        'gravity': False,
        'priority': 'low'
    },
    'spore_blossom': {
        'hardness': 0,
        'best_tool': None,
        'drops': 'spore_blossom',
        'can_burn': False,
        'categories': ['nether', 'decoration'],
        'uses': ['mushroom_stew', 'suspicious_stew'],
        'gravity': False,
        'priority': 'low'
    },
    'crimson_fungus': {
        'hardness': 0,
        'best_tool': None,
        'drops': 'crimson_fungus',
        'can_burn': False,
        'categories': ['nether', 'natural', 'farming'],
        'uses': ['crimson_planks', 'crimson_nylium'],
        'gravity': False,
        'plantable': ['crimson_nylium'],
        'priority': 'high'
    },
    'warped_fungus': {
        'hardness': 0,
        'best_tool': None,
        'drops': 'warped_fungus',
        'can_burn': False,
        'categories': ['nether', 'natural', 'farming'],
        'uses': ['warped_planks', 'warped_nylium', 'warped_wart_block'],
        'gravity': False,
        'plantable': ['warped_nylium'],
        'priority': 'high'
    },
    'nether_wart': {
        'hardness': 0,
        'best_tool': None,
        'drops': 'nether_wart',
        'can_burn': False,
        'categories': ['nether', 'farming', 'resource'],
        'uses': ['nether_wart_block', 'redstone', 'potion'],
        'gravity': False,
        'plantable': ['soul_sand'],
        'growth_stages': 4,
        'priority': 'essential',
        'description': 'Essential for potions'
    },
    'sweet_berries': {
        'hardness': 0,
        'best_tool': None,
        'drops': 'sweet_berries',
        'can_burn': False,
        'categories': ['natural', 'food', 'farming'],
        'hunger': 2,
        'saturation': 1.6,
        'uses': ['sweet_berry_bush'],
        'gravity': False,
        'plantable': ['grass_block', 'dirt'],
        'growth_stages': 3,
        'priority': 'medium',
        'description': 'Food and defense'
    },
    'cocoa_beans': {
        'hardness': 0.2,
        'best_tool': None,
        'drops': 'cocoa_beans',
        'can_burn': False,
        'categories': ['natural', 'farming', 'resource'],
        'uses': ['cookies', 'brown_dye'],
        'gravity': False,
        'plantable': ['jungle_log'],
        'growth_stages': 3,
        'priority': 'high',
        'description': 'Grows on jungle trees'
    },

    # ============================================================
    # MUSHROOMS
    # ============================================================

    'brown_mushroom': {
        'hardness': 0,
        'best_tool': None,
        'drops': 'brown_mushroom',
        'can_burn': False,
        'categories': ['natural', 'food', 'resource'],
        'uses': ['mushroom_stew', 'rabbit', 'suspicious_stew', 'mushroom_block'],
        'gravity': False,
        'light': 1,
        'priority': 'medium',
        'spread_to': ['dirt', 'grass_block', 'podzol', 'mycelium'],
        'description': 'Light source in darkness'
    },
    'red_mushroom': {
        'hardness': 0,
        'best_tool': None,
        'drops': 'red_mushroom',
        'can_burn': False,
        'categories': ['natural', 'food', 'resource'],
        'uses': ['mushroom_stew', 'suspicious_stew', 'rabbit', 'flower_pot', 'mushroom_block'],
        'gravity': False,
        'priority': 'medium',
        'spread_to': ['mycelium', 'podzol'],
        'description': 'Red mushrooms'
    },
    'mushroom_stem': {
        'hardness': 0,
        'best_tool': None,
        'drops': 'mushroom_stem',
        'can_burn': False,
        'categories': ['natural', 'building'],
        'uses': ['mushroom_block', 'decoration'],
        'gravity': False,
        'transparent': True
    },
    'mushroom_block': {
        'hardness': 0.2,
        'best_tool': None,
        'drops': None,
        'can_burn': False,
        'categories': ['building', 'decoration'],
        'uses': ['decoration'],
        'gravity': True
    },

    # ============================================================
    # DANGEROUS BLOCKS
    # ============================================================

    'bedrock': {
        'hardness': -1,
        'best_tool': None,
        'drops': None,
        'can_burn': False,
        'categories': ['natural', 'unbreakable'],
        'description': 'Indestructible bottom layer'
    },
    'barrier': {
        'hardness': -1,
        'best_tool': None,
        'drops': None,
        'can_burn': False,
        'categories': ['creative', 'unbreakable'],
        'description': 'Indestructible creative block'
    },
    'command_block': {
        'hardness': -1,
        'best_tool': None,
        'drops': None,
        'can_burn': False,
        'categories': ['technical', 'unbreakable'],
        'description': 'Command execution block'
    },
    'structure_block': {
        'hardness': -1,
        'best_tool': None,
        'drops': None,
        'can_burn': False,
        'categories': ['technical', 'unbreakable'],
        'description': 'Technical block'
    },
    'jigsaw_block': {
        'hardness': -1,
        'best_tool': None,
        'drops': None,
        'can_burn': False,
        'categories': ['technical', 'unbreakable'],
        'description': 'Technical block'
    },

    # ============================================================
    # UTILITIES
    # ============================================================

    'crafting_table': {
        'hardness': 2.5,
        'best_tool': 'axe',
        'drops': 'crafting_table',
        'can_burn': True,
        'categories': ['utility', 'essential'],
        'uses': ['crafting'],
        'priority': 'essential',
        'description': 'Essential for crafting'
    },
    'furnace': {
        'hardness': 3.5,
        'best_tool': 'pickaxe',
        'drops': 'furnace',
        'can_burn': False,
        'categories': ['utility', 'essential'],
        'uses': ['smelting', 'cooking', 'ore_processing'],
        'priority': 'essential',
        'description': 'Smelt ores and cook food'
    },
    'blast_furnace': {
        'hardness': 3.5,
        'best_tool': 'pickaxe',
        'drops': 'blast_furnace',
        'can_burn': False,
        'categories': ['utility', 'essential'],
        'uses': ['fast_smelting', 'ore_doubling', 'netherite_smelting'],
        'priority': 'high',
        'description': 'Fast smelting with fuel efficiency'
    },
    'smoker': {
        'hardness': 3.5,
        'best_tool': 'pickaxe',
        'drops': 'smoker',
        'can_burn': False,
        'categories': ['utility'],
        'uses': ['fast_cooking'],
        'priority': 'medium',
        'description': 'Fast food cooking'
    },
    'anvil': {
        'hardness': 5,
        'best_tool': 'pickaxe',
        'drops': 'anvil',
        'can_burn': False,
        'categories': ['utility', 'essential'],
        'uses': ['repairing', 'combining', 'renaming'],
        'priority': 'essential',
        'description': 'Repair and upgrade tools'
    },
    'enchanting_table': {
        'hardness': 1,
        'best_tool': 'axe',
        'drops': 'enchanting_table',
        'can_burn': True,
        'categories': ['utility', 'magic', 'essential'],
        'uses': ['enchanting'],
        'priority': 'essential',
        'description': 'Enchant tools and armor'
    },
    'brewing_stand': {
        'hardness': 0.5,
        'best_tool': 'pickaxe',
        'drops': 'brewing_stand',
        'can_burn': False,
        'categories': ['utility', 'magic'],
        'uses': ['potions', 'splash_potions', 'lingering_potions'],
        'priority': 'high',
        'description': 'Brew potions'
    },
    'cauldron': {
        'hardness': 2,
        'best_tool': 'pickaxe',
        'drops': 'cauldron',
        'can_burn': False,
        'categories': ['utility'],
        'uses': ['water_storage', 'dyeing', 'potion_storage'],
        'priority': 'medium',
        'description': 'Hold and heat liquids'
    },
    'cartography_table': {
        'hardness': 1.25,
        'best_tool': 'axe',
        'drops': 'cartography_table',
        'can_burn': True,
        'categories': ['utility'],
        'uses': ['map_making', 'cloning_maps', 'zoom_maps'],
        'priority': 'low'
    },
    'fletching_table': {
        'hardness': 1.25,
        'best_tool': 'axe',
        'drops': 'fletching_table',
        'can_burn': True,
        'categories': ['utility'],
        'uses': ['arrow_repairing', 'tipped_arrows'],
        'priority': 'medium'
    },
    'smithing_table': {
        'hardness': 1.25,
        'best_tool': 'axe',
        'drops': 'smithing_table',
        'can_burn': True,
        'categories': ['utility', 'essential'],
        'uses': ['netherite_upgrades', 'diamond_gear'],
        'priority': 'essential',
        'description': 'Upgrade to netherite'
    },
    'grindstone': {
        'hardness': 2,
        'best_tool': 'pickaxe',
        'drops': 'grindstone',
        'can_burn': False,
        'categories': ['utility'],
        'uses': ['disenchanting', 'repairing'],
        'priority': 'medium',
        'description': 'Disenchant and repair'
    },
    'stonecutter': {
        'hardness': 2,
        'best_tool': 'pickaxe',
        'drops': 'stonecutter',
        'can_burn': False,
        'categories': ['utility', 'essential'],
        'uses': ['stone_processing', 'stairs_slabs'],
        'priority': 'essential',
        'description': 'Efficient stone processing'
    },
    'loom': {
        'hardness': 1.25,
        'best_tool': 'axe',
        'drops': 'loom',
        'can_burn': True,
        'categories': ['utility'],
        'uses': ['banner_patterns', 'banner_cloning'],
        'priority': 'low'
    },
    'barrel': {
        'hardness': 2.5,
        'best_tool': 'axe',
        'drops': ['barrel', 'item'],
        'can_burn': True,
        'categories': ['utility', 'storage'],
        'uses': ['item_storage', 'water_cauldron', 'food_preservation'],
        'priority': 'medium'
    },
    'smoker': {
        'hardness': 3.5,
        'best_tool': 'pickaxe',
        'drops': 'smoker',
        'can_burn': False,
        'categories': ['utility'],
        'uses': ['fast_cooking'],
        'priority': 'medium'
    },
    'blast_furnace': {
        'hardness': 3.5,
        'best_tool': 'pickaxe',
        'drops': 'blast_furnace',
        'can_burn': False,
        'categories': ['utility'],
        'uses': ['fast_smelting', 'ore_doubling'],
        'priority': 'high'
    },
    'lectern': {
        'hardness': 2.5,
        'best_tool': 'axe',
        'drops': 'lectern',
        'can_burn': True,
        'categories': ['utility', 'redstone'],
        'uses': ['book_storage', 'redstone_power'],
        'priority': 'medium'
    },
    'composter': {
        'hardness': 0.5,
        'best_tool': 'axe',
        'drops': 'composter',
        'can_burn': True,
        'categories': ['utility', 'farming'],
        'uses': ['bone_meal', 'compost'],
        'priority': 'medium',
        'description': 'Converts food and plants to bone meal'
    },
    'grindstone': {
        'hardness': 2,
        'best_tool': 'pickaxe',
        'drops': 'grindstone',
        'can_burn': False,
        'categories': ['utility'],
        'uses': ['disenchanting', 'repairing', 'recycling'],
        'priority': 'medium'
    },
    'smithing_table': {
        'hardness': 1.25,
        'best_tool': 'axe',
        'drops': 'smithing_table',
        'can_burn': True,
        'categories': ['utility', 'essential'],
        'uses': ['netherite_upgrading', 'tool_repairing', 'gear_making'],
        'priority': 'essential',
        'description': 'Netherite upgrades and repairs'
    },
    'fletching_table': {
        'hardness': 1.25,
        'best_tool': 'axe',
        'drops': 'fletching_table',
        'can_burn': True,
        'categories': ['utility'],
        'uses': ['arrow_making', 'tipped_arrows', 'arrow_repairing'],
        'priority': 'medium'
    },
    'cartography_table': {
        'hardness': 1.25,
        'best_tool': 'axe',
        'drops': 'cartography_table',
        'can_burn': True,
        'categories': ['utility'],
        'uses': ['map_making', 'map_cloning', 'map_zooming'],
        'priority': 'low'
    },
}

# Helper functions
def get_block_info(block_name: str) -> dict:
    """Get complete information about a block"""
    return BLOCK_DATABASE.get(block_name, {})

def can_harvest(block_name: str, tool: str) -> bool:
    """Check if a block can be harvested with given tool"""
    block = BLOCK_DATABASE.get(block_name, {})
    best_tool = block.get('best_tool', None)
    return best_tool is None or tool == best_tool

def get_block_drop(block_name: str, tool: str = None) -> str:
    """Get what a block drops when mined"""
    block = BLOCK_DATABASE.get(block_name, {})
    if tool and tool != block.get('best_tool'):
        return None  # Wrong tool, can't mine
    return block.get('drops', block_name)

def is_block_safe(block_name: str) -> bool:
    """Check if a block is safe to walk on"""
    block = BLOCK_DATABASE.get(block_name, {})
    return block.get('damage', 0) == 0

def get_block_priority(block_name: str) -> str:
    """Get priority level of a block"""
    block = BLOCK_DATABASE.get(block_name, {})
    return block.get('priority', 'low')

def should_avoid(block_name: str) -> bool:
    """Check if a block should be avoided"""
    block = BLOCK_DATABASE.get(block_name, {})
    return (
        block.get('damage', 0) > 0 or
        block.get('priority') == 'avoid' or
        block.get('categories', []) == ['liquid', 'dangerous']
    )

def get_block_value(block_name: str) -> float:
    """Get the value/importance of a block (0-1 scale)"""
    priority_scores = {
        'essential': 1.0,
        'high': 0.8,
        'medium': 0.5,
        'low': 0.2,
        'avoid': -0.1
    }
    block = BLOCK_DATABASE.get(block_name, {})
    return priority_scores.get(block.get('priority', 'low'), 0.2)
