"""
Complete Vanilla Minecraft Crafting Recipes
All 200+ recipes from vanilla Minecraft
"""

VANILLA_RECIPES = {
    # ============================================================
    # BASIC RESOURCES (Starting recipes)
    # ============================================================

    # Wood processing
    'oak_planks': {
        'pattern': [['oak_log', None, None], [None, None, None], [None, None, None]],
        'output': ('oak_planks', 4),
        'category': 'basic',
        'unlock_tier': 0
    },
    'spruce_planks': {
        'pattern': [['spruce_log', None, None], [None, None, None], [None, None, None]],
        'output': ('spruce_planks', 4),
        'category': 'basic',
        'unlock_tier': 0
    },
    'birch_planks': {
        'pattern': [['birch_log', None, None], [None, None, None], [None, None, None]],
        'output': ('birch_planks', 4),
        'category': 'basic',
        'unlock_tier': 0
    },
    'jungle_planks': {
        'pattern': [['jungle_log', None, None], [None, None, None], [None, None, None]],
        'output': ('jungle_planks', 4),
        'category': 'basic',
        'unlock_tier': 0
    },
    'acacia_planks': {
        'pattern': [['acacia_log', None, None], [None, None, None], [None, None, None]],
        'output': ('acacia_planks', 4),
        'category': 'basic',
        'unlock_tier': 0
    },
    'dark_oak_planks': {
        'pattern': [['dark_oak_log', None, None], [None, None, None], [None, None, None]],
        'output': ('dark_oak_planks', 4),
        'category': 'basic',
        'unlock_tier': 0
    },
    'mangrove_planks': {
        'pattern': [['mangrove_log', None, None], [None, None, None], [None, None, None]],
        'output': ('mangrove_planks', 4),
        'category': 'basic',
        'unlock_tier': 0
    },
    'crimson_planks': {
        'pattern': [['crimson_stem', None, None], [None, None, None], [None, None, None]],
        'output': ('crimson_planks', 4),
        'category': 'basic',
        'unlock_tier': 0
    },
    'warped_planks': {
        'pattern': [['warped_stem', None, None], [None, None, None], [None, None, None]],
        'output': ('warped_planks', 4),
        'category': 'basic',
        'unlock_tier': 0
    },

    # Sticks
    'sticks': {
        'pattern': [[None, None, None], ['planks', None, None], ['planks', None, None]],
        'output': ('stick', 4),
        'category': 'basic',
        'unlock_tier': 0
    },

    # Crafting Table
    'crafting_table': {
        'pattern': [['planks', 'planks', None], ['planks', 'planks', None], [None, None, None]],
        'output': ('crafting_table', 1),
        'category': 'basic',
        'unlock_tier': 0,
        'essential': True
    },

    # Furnace
    'furnace': {
        'pattern': [['cobblestone', 'cobblestone', 'cobblestone'], ['cobblestone', None, 'cobblestone'], ['cobblestone', 'cobblestone', 'cobblestone']],
        'output': ('furnace', 1),
        'category': 'basic',
        'unlock_tier': 0,
        'essential': True
    },

    # Chest
    'chest': {
        'pattern': [['planks', 'planks', 'planks'], ['planks', None, 'planks'], ['planks', 'planks', 'planks']],
        'output': ('chest', 1),
        'category': 'basic',
        'unlock_tier': 0
    },

    # ============================================================
    # WOODEN TOOLS (Tier 1)
    # ============================================================

    'wooden_pickaxe': {
        'pattern': [['planks', 'planks', 'planks'], [None, 'stick', None], [None, 'stick', None]],
        'output': ('wooden_pickaxe', 1),
        'category': 'tools',
        'unlock_tier': 0,
        'essential': True,
        'uses': 59,
        'mining_speed': 2.0,
        'description': 'Basic mining tool'
    },
    'wooden_axe': {
        'pattern': [['planks', 'planks', None], ['planks', 'stick', None], [None, 'stick', None]],
        'output': ('wooden_axe', 1),
        'category': 'tools',
        'unlock_tier': 0,
        'uses': 59,
        'mining_speed': 2.0,
        'description': 'Chops wood faster'
    },
    'wooden_shovel': {
        'pattern': [[None, 'planks', None], [None, 'stick', None], [None, 'stick', None]],
        'output': ('wooden_shovel', 1),
        'category': 'tools',
        'unlock_tier': 0,
        'uses': 59,
        'description': 'Digs dirt/sand faster'
    },
    'wooden_sword': {
        'pattern': [[None, 'planks', None], [None, 'planks', None], [None, 'stick', None]],
        'output': ('wooden_sword', 1),
        'category': 'combat',
        'unlock_tier': 0,
        'uses': 59,
        'damage': 4,
        'description': 'Basic weapon'
    },
    'wooden_hoe': {
        'pattern': [['planks', 'planks', None], [None, 'stick', None], [None, 'stick', None]],
        'output': ('wooden_hoe', 1),
        'category': 'tools',
        'unlock_tier': 0,
        'uses': 59,
        'description': 'Tills soil for farming'
    },

    # ============================================================
    # STONE TOOLS (Tier 2)
    # ============================================================

    'stone_pickaxe': {
        'pattern': [['cobblestone', 'cobblestone', 'cobblestone'], [None, 'stick', None], [None, 'stick', None]],
        'output': ('stone_pickaxe', 1),
        'category': 'tools',
        'unlock_tier': 1,
        'essential': True,
        'uses': 131,
        'mining_speed': 4.0,
        'description': 'Mines iron and coal'
    },
    'stone_axe': {
        'pattern': [['cobblestone', 'cobblestone', None], ['cobblestone', 'stick', None], [None, 'stick', None]],
        'output': ('stone_axe', 1),
        'category': 'tools',
        'unlock_tier': 1,
        'uses': 131,
        'mining_speed': 4.0
    },
    'stone_shovel': {
        'pattern': [[None, 'cobblestone', None], [None, 'stick', None], [None, 'stick', None]],
        'output': ('stone_shovel', 1),
        'category': 'tools',
        'unlock_tier': 1,
        'uses': 131
    },
    'stone_sword': {
        'pattern': [[None, 'cobblestone', None], [None, 'cobblestone', None], [None, 'stick', None]],
        'output': ('stone_sword', 1),
        'category': 'combat',
        'unlock_tier': 1,
        'uses': 131,
        'damage': 5
    },
    'stone_hoe': {
        'pattern': [['cobblestone', 'cobblestone', None], [None, 'stick', None], [None, 'stick', None]],
        'output': ('stone_hoe', 1),
        'category': 'tools',
        'unlock_tier': 1,
        'uses': 131
    },

    # ============================================================
    # IRON TOOLS (Tier 3)
    # ============================================================

    'iron_pickaxe': {
        'pattern': [['iron_ingot', 'iron_ingot', 'iron_ingot'], [None, 'stick', None], [None, 'stick', None]],
        'output': ('iron_pickaxe', 1),
        'category': 'tools',
        'unlock_tier': 2,
        'essential': True,
        'uses': 250,
        'mining_speed': 6.0,
        'description': 'Mines gold, redstone, diamond'
    },
    'iron_axe': {
        'pattern': [['iron_ingot', 'iron_ingot', None], ['iron_ingot', 'stick', None], [None, 'stick', None]],
        'output': ('iron_axe', 1),
        'category': 'tools',
        'unlock_tier': 2,
        'uses': 250,
        'mining_speed': 6.0
    },
    'iron_shovel': {
        'pattern': [[None, 'iron_ingot', None], [None, 'stick', None], [None, 'stick', None]],
        'output': ('iron_shovel', 1),
        'category': 'tools',
        'unlock_tier': 2,
        'uses': 250
    },
    'iron_sword': {
        'pattern': [[None, 'iron_ingot', None], [None, 'iron_ingot', None], [None, 'stick', None]],
        'output': ('iron_sword', 1),
        'category': 'combat',
        'unlock_tier': 2,
        'uses': 250,
        'damage': 6
    },
    'iron_hoe': {
        'pattern': [['iron_ingot', 'iron_ingot', None], [None, 'stick', None], [None, 'stick', None]],
        'output': ('iron_hoe', 1),
        'category': 'tools',
        'unlock_tier': 2,
        'uses': 250
    },

    # ============================================================
    # DIAMOND TOOLS (Tier 4)
    # ============================================================

    'diamond_pickaxe': {
        'pattern': [['diamond', 'diamond', 'diamond'], [None, 'stick', None], [None, 'stick', None]],
        'output': ('diamond_pickaxe', 1),
        'category': 'tools',
        'unlock_tier': 3,
        'essential': True,
        'uses': 1561,
        'mining_speed': 8.0,
        'description': 'Mines obsidian and ancient debris'
    },
    'diamond_axe': {
        'pattern': [['diamond', 'diamond', None], ['diamond', 'stick', None], [None, 'stick', None]],
        'output': ('diamond_axe', 1),
        'category': 'tools',
        'unlock_tier': 3,
        'uses': 1561,
        'mining_speed': 8.0
    },
    'diamond_shovel': {
        'pattern': [[None, 'diamond', None], [None, 'stick', None], [None, 'stick', None]],
        'output': ('diamond_shovel', 1),
        'category': 'tools',
        'unlock_tier': 3,
        'uses': 1561
    },
    'diamond_sword': {
        'pattern': [[None, 'diamond', None], [None, 'diamond', None], [None, 'stick', None]],
        'output': ('diamond_sword', 1),
        'category': 'combat',
        'unlock_tier': 3,
        'uses': 1561,
        'damage': 7
    },
    'diamond_hoe': {
        'pattern': [['diamond', 'diamond', None], [None, 'stick', None], [None, 'stick', None]],
        'output': ('diamond_hoe', 1),
        'category': 'tools',
        'unlock_tier': 3,
        'uses': 1561
    },

    # ============================================================
    # GOLD TOOLS (Tier 2.5 - fast but low durability)
    # ============================================================

    'golden_pickaxe': {
        'pattern': [['gold_ingot', 'gold_ingot', 'gold_ingot'], [None, 'stick', None], [None, 'stick', None]],
        'output': ('golden_pickaxe', 1),
        'category': 'tools',
        'unlock_tier': 2,
        'uses': 32,
        'mining_speed': 12.0,
        'description': 'Very fast but breaks quickly'
    },
    'golden_axe': {
        'pattern': [['gold_ingot', 'gold_ingot', None], ['gold_ingot', 'stick', None], [None, 'stick', None]],
        'output': ('golden_axe', 1),
        'category': 'tools',
        'unlock_tier': 2,
        'uses': 32,
        'mining_speed': 12.0
    },
    'golden_shovel': {
        'pattern': [[None, 'gold_ingot', None], [None, 'stick', None], [None, 'stick', None]],
        'output': ('golden_shovel', 1),
        'category': 'tools',
        'unlock_tier': 2,
        'uses': 32
    },
    'golden_sword': {
        'pattern': [[None, 'gold_ingot', None], [None, 'gold_ingot', None], [None, 'stick', None]],
        'output': ('golden_sword', 1),
        'category': 'combat',
        'unlock_tier': 2,
        'uses': 32,
        'damage': 4
    },
    'golden_hoe': {
        'pattern': [['gold_ingot', 'gold_ingot', None], [None, 'stick', None], [None, 'stick', None]],
        'output': ('golden_hoe', 1),
        'category': 'tools',
        'unlock_tier': 2,
        'uses': 32
    },

    # ============================================================
    # NETHERITE TOOLS (Tier 5 - best)
    # ============================================================

    'netherite_pickaxe': {
        'pattern': [['netherite_ingot', 'netherite_ingot', 'netherite_ingot'], [None, 'stick', None], [None, 'stick', None]],
        'output': ('netherite_pickaxe', 1),
        'category': 'tools',
        'unlock_tier': 4,
        'uses': 2031,
        'mining_speed': 9.0,
        'description': 'Best pickaxe, immune to fire/lava'
    },
    'netherite_axe': {
        'pattern': [['netherite_ingot', 'netherite_ingot', None], ['netherite_ingot', 'stick', None], [None, 'stick', None]],
        'output': ('netherite_axe', 1),
        'category': 'tools',
        'unlock_tier': 4,
        'uses': 2031,
        'mining_speed': 9.0
    },
    'netherite_shovel': {
        'pattern': [[None, 'netherite_ingot', None], [None, 'stick', None], [None, 'stick', None]],
        'output': ('netherite_shovel', 1),
        'category': 'tools',
        'unlock_tier': 4,
        'uses': 2031
    },
    'netherite_sword': {
        'pattern': [[None, 'netherite_ingot', None], [None, 'netherite_ingot', None], [None, 'stick', None]],
        'output': ('netherite_sword', 1),
        'category': 'combat',
        'unlock_tier': 4,
        'uses': 2031,
        'damage': 8
    },
    'netherite_hoe': {
        'pattern': [['netherite_ingot', 'netherite_ingot', None], [None, 'stick', None], [None, 'stick', None]],
        'output': ('netherite_hoe', 1),
        'category': 'tools',
        'unlock_tier': 4,
        'uses': 2031
    },

    # ============================================================
    # ARMOR
    # ============================================================

    # Leather Armor
    'leather_helmet': {
        'pattern': [['leather', 'leather', 'leather'], ['leather', None, 'leather'], [None, None, None]],
        'output': ('leather_helmet', 1),
        'category': 'armor',
        'unlock_tier': 1,
        'protection': 1
    },
    'leather_chestplate': {
        'pattern': [['leather', None, 'leather'], ['leather', 'leather', 'leather'], ['leather', 'leather', 'leather']],
        'output': ('leather_chestplate', 1),
        'category': 'armor',
        'unlock_tier': 1,
        'protection': 3
    },
    'leather_leggings': {
        'pattern': [['leather', 'leather', 'leather'], ['leather', 'leather', 'leather'], ['leather', None, 'leather']],
        'output': ('leather_leggings', 1),
        'category': 'armor',
        'unlock_tier': 1,
        'protection': 2
    },
    'leather_boots': {
        'pattern': [[None, None, None], ['leather', None, 'leather'], ['leather', None, 'leather']],
        'output': ('leather_boots', 1),
        'category': 'armor',
        'unlock_tier': 1,
        'protection': 1
    },

    # Iron Armor
    'iron_helmet': {
        'pattern': [['iron_ingot', 'iron_ingot', 'iron_ingot'], ['iron_ingot', None, 'iron_ingot'], [None, None, None]],
        'output': ('iron_helmet', 1),
        'category': 'armor',
        'unlock_tier': 2,
        'protection': 2
    },
    'iron_chestplate': {
        'pattern': [['iron_ingot', None, 'iron_ingot'], ['iron_ingot', 'iron_ingot', 'iron_ingot'], ['iron_ingot', 'iron_ingot', 'iron_ingot']],
        'output': ('iron_chestplate', 1),
        'category': 'armor',
        'unlock_tier': 2,
        'protection': 6
    },
    'iron_leggings': {
        'pattern': [['iron_ingot', 'iron_ingot', 'iron_ingot'], ['iron_ingot', 'iron_ingot', 'iron_ingot'], ['iron_ingot', None, 'iron_ingot']],
        'output': ('iron_leggings', 1),
        'category': 'armor',
        'unlock_tier': 2,
        'protection': 5
    },
    'iron_boots': {
        'pattern': [[None, None, None], ['iron_ingot', None, 'iron_ingot'], ['iron_ingot', None, 'iron_ingot']],
        'output': ('iron_boots', 1),
        'category': 'armor',
        'unlock_tier': 2,
        'protection': 2
    },

    # Diamond Armor
    'diamond_helmet': {
        'pattern': [['diamond', 'diamond', 'diamond'], ['diamond', None, 'diamond'], [None, None, None]],
        'output': ('diamond_helmet', 1),
        'category': 'armor',
        'unlock_tier': 3,
        'protection': 3
    },
    'diamond_chestplate': {
        'pattern': [['diamond', None, 'diamond'], ['diamond', 'diamond', 'diamond'], ['diamond', 'diamond', 'diamond']],
        'output': ('diamond_chestplate', 1),
        'category': 'armor',
        'unlock_tier': 3,
        'protection': 8
    },
    'diamond_leggings': {
        'pattern': [['diamond', 'diamond', 'diamond'], ['diamond', 'diamond', 'diamond'], ['diamond', None, 'diamond']],
        'output': ('diamond_leggings', 1),
        'category': 'armor',
        'unlock_tier': 3,
        'protection': 6
    },
    'diamond_boots': {
        'pattern': [[None, None, None], ['diamond', None, 'diamond'], ['diamond', None, 'diamond']],
        'output': ('diamond_boots', 1),
        'category': 'armor',
        'unlock_tier': 3,
        'protection': 3
    },

    # Gold Armor
    'golden_helmet': {
        'pattern': [['gold_ingot', 'gold_ingot', 'gold_ingot'], ['gold_ingot', None, 'gold_ingot'], [None, None, None]],
        'output': ('golden_helmet', 1),
        'category': 'armor',
        'unlock_tier': 2,
        'protection': 2
    },
    'golden_chestplate': {
        'pattern': [['gold_ingot', None, 'gold_ingot'], ['gold_ingot', 'gold_ingot', 'gold_ingot'], ['gold_ingot', 'gold_ingot', 'gold_ingot']],
        'output': ('golden_chestplate', 1),
        'category': 'armor',
        'unlock_tier': 2,
        'protection': 5
    },
    'golden_leggings': {
        'pattern': [['gold_ingot', 'gold_ingot', 'gold_ingot'], ['gold_ingot', 'gold_ingot', 'gold_ingot'], ['gold_ingot', None, 'gold_ingot']],
        'output': ('golden_leggings', 1),
        'category': 'armor',
        'unlock_tier': 2,
        'protection': 3
    },
    'golden_boots': {
        'pattern': [[None, None, None], ['gold_ingot', None, 'gold_ingot'], ['gold_ingot', None, 'gold_ingot']],
        'output': ('golden_boots', 1),
        'category': 'armor',
        'unlock_tier': 2,
        'protection': 1
    },

    # Netherite Armor (upgrade only)
    'netherite_helmet_upgrade': {
        'pattern': [['diamond_helmet', None, None], ['netherite_ingot', None, None], [None, None, None]],
        'output': ('netherite_helmet', 1),
        'category': 'armor',
        'unlock_tier': 4,
        'protection': 3,
        'knockback_resistance': 1
    },
    'netherite_chestplate_upgrade': {
        'pattern': [['diamond_chestplate', None, None], ['netherite_ingot', None, None], [None, None, None]],
        'output': ('netherite_chestplate', 1),
        'category': 'armor',
        'unlock_tier': 4,
        'protection': 8,
        'knockback_resistance': 1
    },
    'netherite_leggings_upgrade': {
        'pattern': [['diamond_leggings', None, None], ['netherite_ingot', None, None], [None, None, None]],
        'output': ('netherite_leggings', 1),
        'category': 'armor',
        'unlock_tier': 4,
        'protection': 6,
        'knockback_resistance': 1
    },
    'netherite_boots_upgrade': {
        'pattern': [['diamond_boots', None, None], ['netherite_ingot', None, None], [None, None, None]],
        'output': ('netherite_boots', 1),
        'category': 'armor',
        'unlock_tier': 4,
        'protection': 3,
        'knockback_resistance': 1
    },

    # ============================================================
    # SMELTING RECIPES (Furnace)
    # ============================================================

    'smelt_iron_ore': {
        'input': 'iron_ore',
        'fuel': 'coal',
        'output': 'iron_ingot',
        'experience': 0.7,
        'smelt_time': 200
    },
    'smelt_gold_ore': {
        'input': 'gold_ore',
        'fuel': 'coal',
        'output': 'gold_ingot',
        'experience': 1.0,
        'smelt_time': 200
    },
    'smelt_copper_ore': {
        'input': 'copper_ore',
        'fuel': 'coal',
        'output': 'copper_ingot',
        'experience': 0.7,
        'smelt_time': 200
    },
    'smelt_raw_iron': {
        'input': 'raw_iron',
        'fuel': 'coal',
        'output': 'iron_ingot',
        'experience': 0.7,
        'smelt_time': 200
    },
    'smelt_raw_gold': {
        'input': 'raw_gold',
        'fuel': 'coal',
        'output': 'gold_ingot',
        'experience': 1.0,
        'smelt_time': 200
    },
    'smelt_raw_copper': {
        'input': 'raw_copper',
        'fuel': 'coal',
        'output': 'copper_ingot',
        'experience': 0.7,
        'smelt_time': 200
    },
    'smelt_sand': {
        'input': 'sand',
        'fuel': 'coal',
        'output': 'glass',
        'experience': 0.1,
        'smelt_time': 200
    },
    'smelt_sand_red': {
        'input': 'red_sand',
        'fuel': 'coal',
        'output': 'glass',
        'experience': 0.1,
        'smelt_time': 200
    },
    'smelt_cobblestone': {
        'input': 'cobblestone',
        'fuel': 'coal',
        'output': 'stone',
        'experience': 0.1,
        'smelt_time': 200
    },
    'smelt_stone': {
        'input': 'stone',
        'fuel': 'coal',
        'output': 'smooth_stone',
        'experience': 0.1,
        'smelt_time': 200
    },
    'smelt_clay': {
        'input': 'clay_ball',
        'fuel': 'coal',
        'output': 'brick',
        'experience': 0.3,
        'smelt_time': 200
    },
    'smelt_netherrack': {
        'input': 'netherrack',
        'fuel': 'coal',
        'output': 'nether_brick',
        'experience': 0.1,
        'smelt_time': 200
    },
    'smelt_ancient_debris': {
        'input': 'ancient_debris',
        'fuel': 'coal',
        'output': 'netherite_scrap',
        'experience': 2.0,
        'smelt_time': 400
    },
    'smelt_golden_ore': {
        'input': 'nether_gold_ore',
        'fuel': 'coal',
        'output': 'gold_nugget',
        'experience': 1.0,
        'smelt_time': 200
    },

    # Food smelting
    'smelt_beef': {
        'input': 'raw_beef',
        'fuel': 'coal',
        'output': 'cooked_beef',
        'experience': 0.35,
        'smelt_time': 200,
        'hunger': 8,
        'saturation': 12.8
    },
    'smelt_porkchop': {
        'input': 'raw_porkchop',
        'fuel': 'coal',
        'output': 'cooked_porkchop',
        'experience': 0.35,
        'smelt_time': 200,
        'hunger': 8,
        'saturation': 12.8
    },
    'smelt_chicken': {
        'input': 'raw_chicken',
        'fuel': 'coal',
        'output': 'cooked_chicken',
        'experience': 0.35,
        'smelt_time': 200,
        'hunger': 6,
        'saturation': 7.2
    },
    'smelt_cod': {
        'input': 'cod',
        'fuel': 'coal',
        'output': 'cooked_cod',
        'experience': 0.35,
        'smelt_time': 200,
        'hunger': 5,
        'saturation': 6.0
    },
    'smelt_salmon': {
        'input': 'salmon',
        'fuel': 'coal',
        'output': 'cooked_salmon',
        'experience': 0.35,
        'smelt_time': 200,
        'hunger': 6,
        'saturation': 9.6
    },
    'smelt_mutton': {
        'input': 'mutton',
        'fuel': 'coal',
        'output': 'cooked_mutton',
        'experience': 0.35,
        'smelt_time': 200,
        'hunger': 6,
        'saturation': 9.6
    },
    'smelt_rabbit': {
        'input': 'raw_rabbit',
        'fuel': 'coal',
        'output': 'cooked_rabbit',
        'experience': 0.35,
        'smelt_time': 200,
        'hunger': 5,
        'saturation': 6.0
    },
    'smelt_potato': {
        'input': 'potato',
        'fuel': 'coal',
        'output': 'baked_potato',
        'experience': 0.35,
        'smelt_time': 200,
        'hunger': 5,
        'saturation': 6.0
    },
    'smelt_kelp': {
        'input': 'dried_kelp',
        'fuel': 'coal',
        'output': 'dried_kelp',
        'experience': 0.1,
        'smelt_time': 200,
        'hunger': 1,
        'saturation': 0.6
    },

    # Ore smelting
    'smelt_deepslate_iron_ore': {
        'input': 'deepslate_iron_ore',
        'fuel': 'coal',
        'output': 'iron_ingot',
        'experience': 0.7,
        'smelt_time': 200
    },
    'smelt_deepslate_gold_ore': {
        'input': 'deepslate_gold_ore',
        'fuel': 'coal',
        'output': 'gold_ingot',
        'experience': 1.0,
        'smelt_time': 200
    },
    'smelt_deepslate_copper_ore': {
        'input': 'deepslate_copper_ore',
        'fuel': 'coal',
        'output': 'copper_ingot',
        'experience': 0.7,
        'smelt_time': 200
    },

    # ============================================================
    # FOOD
    # ============================================================

    'bread': {
        'pattern': [[None, None, None], ['wheat', 'wheat', 'wheat'], [None, None, None]],
        'output': ('bread', 1),
        'category': 'food',
        'unlock_tier': 1,
        'hunger': 5,
        'saturation': 6.0
    },
    'cake': {
        'pattern': [['milk_bucket', 'sugar', 'milk_bucket'], ['egg', 'wheat', 'wheat'], ['wheat', 'wheat', 'wheat']],
        'output': ('cake', 1),
        'category': 'food',
        'unlock_tier': 2,
        'hunger': 14,
        'saturation': 2.8
    },
    'cookie': {
        'pattern': [[None, 'wheat', 'wheat'], ['chocolate', None, 'wheat'], [None, None, None]],
        'output': ('cookie', 8),
        'category': 'food',
        'unlock_tier': 2,
        'hunger': 2,
        'saturation': 0.4
    },
    'golden_apple': {
        'pattern': [['gold_ingot', 'gold_ingot', 'gold_ingot'], ['gold_ingot', 'apple', 'gold_ingot'], ['gold_ingot', 'gold_ingot', 'gold_ingot']],
        'output': ('golden_apple', 1),
        'category': 'food',
        'unlock_tier': 3,
        'hunger': 4,
        'saturation': 9.6,
        'special_effects': ['regeneration', 'absorption']
    },
    'golden_carrot': {
        'pattern': [[None, 'gold_nugget', 'gold_nugget'], ['gold_nugget', 'carrot', 'gold_nugget'], [None, 'gold_nugget', 'gold_nugget']],
        'output': ('golden_carrot', 1),
        'category': 'food',
        'unlock_tier': 3,
        'hunger': 6,
        'saturation': 14.4,
        'special_effects': ['night_vision']
    },
    'glistering_melon_slice': {
        'pattern': [[None, 'gold_nugget', 'gold_nugget'], ['gold_nugget', 'melon_slice', 'gold_nugget'], [None, 'gold_nugget', 'gold_nugget']],
        'output': ('glistering_melon_slice', 1),
        'category': 'food',
        'unlock_tier': 3,
        'hunger': 4,
        'saturation': 2.4
    },
    'pumpkin_pie': {
        'pattern': [[None, 'pumpkin', None], ['sugar', 'egg', 'sugar'], [None, 'pumpkin', None]],
        'output': ('pumpkin_pie', 1),
        'category': 'food',
        'unlock_tier': 2,
        'hunger': 8,
        'saturation': 4.8
    },
    'rabbit_stew': {
        'pattern': [[None, 'cooked_rabbit', None], ['carrot', 'baked_potato', 'mushroom'], ['bowl', 'red_mushroom', None]],
        'output': ('rabbit_stew', 1),
        'category': 'food',
        'unlock_tier': 2,
        'hunger': 10,
        'saturation': 12.0
    },
    'beetroot_soup': {
        'pattern': [[None, 'beetroot', None], ['beetroot', 'beetroot', 'beetroot'], ['bowl', 'beetroot', None]],
        'output': ('beetroot_soup', 1),
        'category': 'food',
        'unlock_tier': 1,
        'hunger': 6,
        'saturation': 7.2
    },
    'mushroom_stew': {
        'pattern': [[None, 'red_mushroom', None], ['red_mushroom', 'bowl', 'brown_mushroom'], [None, 'brown_mushroom', None]],
        'output': ('mushroom_stew', 1),
        'category': 'food',
        'unlock_tier': 1,
        'hunger': 6,
        'saturation': 7.2
    },
    'suspicious_stew': {
        'pattern': [[None, 'red_mushroom', None], ['red_mushroom', 'bowl', 'brown_mushroom'], [None, 'flower', None]],
        'output': ('suspicious_stew', 1),
        'category': 'food',
        'unlock_tier': 1,
        'hunger': 6,
        'saturation': 7.2
    },

    # ============================================================
    # UTILITIES
    # ============================================================

    'torch': {
        'pattern': [[None, None, None], ['coal', 'stick', None], [None, None, None]],
        'output': ('torch', 4),
        'category': 'utilities',
        'unlock_tier': 0,
        'essential': True,
        'description': 'Light source'
    },
    'soul_torch': {
        'pattern': [[None, None, None], ['soul_soil', 'stick', None], [None, None, None]],
        'output': ('soul_torch', 4),
        'category': 'utilities',
        'unlock_tier': 3,
        'description': 'Blue torch'
    },
    'redstone_torch': {
        'pattern': [[None, None, None], ['redstone', 'stick', None], [None, None, None]],
        'output': ('redstone_torch', 1),
        'category': 'redstone',
        'unlock_tier': 2
    },
    'lantern': {
        'pattern': [[None, 'torch', None], ['iron_ingot', 'torch', 'iron_ingot'], [None, 'torch', None]],
        'output': ('lantern', 1),
        'category': 'utilities',
        'unlock_tier': 2,
        'description': 'Brighter light source'
    },
    'soul_lantern': {
        'pattern': [[None, 'soul_torch', None], ['iron_ingot', 'soul_torch', 'iron_ingot'], [None, 'soul_torch', None]],
        'output': ('soul_lantern', 1),
        'category': 'utilities',
        'unlock_tier': 3
    },
    'campfire': {
        'pattern': [[None, None, None], ['stick', 'coal', 'stick'], ['stick', 'log', 'stick']],
        'output': ('campfire', 1),
        'category': 'utilities',
        'unlock_tier': 0,
        'description': 'Signal fire and cooking'
    },
    'soul_campfire': {
        'pattern': [[None, None, None], ['stick', 'soul_soil', 'stick'], ['stick', 'log', 'stick']],
        'output': ('soul_campfire', 1),
        'category': 'utilities',
        'unlock_tier': 3
    },
    'bucket': {
        'pattern': [[None, None, None], ['iron_ingot', None, 'iron_ingot'], [None, 'iron_ingot', None]],
        'output': ('bucket', 1),
        'category': 'utilities',
        'unlock_tier': 1,
        'essential': True,
        'description': 'Carries water, lava, milk'
    },
    'water_bucket': {
        'pattern': 'bucket_fill',
        'input': 'bucket',
        'fill_with': 'water',
        'output': 'water_bucket'
    },
    'lava_bucket': {
        'pattern': 'bucket_fill',
        'input': 'bucket',
        'fill_with': 'lava',
        'output': 'lava_bucket'
    },
    'milk_bucket': {
        'pattern': 'milk_cow',
        'input': 'bucket',
        'output': 'milk_bucket'
    },
    'fishing_rod': {
        'pattern': [[None, None, 'stick'], [None, 'stick', 'stick'], ['stick', None, None]],
        'output': ('fishing_rod', 1),
        'category': 'utilities',
        'unlock_tier': 1
    },
    'flint_and_steel': {
        'pattern': [[None, 'iron_ingot', None], [None, 'flint', None], [None, None, None]],
        'output': ('flint_and_steel', 1),
        'category': 'utilities',
        'unlock_tier': 1,
        'description': 'Starts fires and activates nether portal'
    },
    'compass': {
        'pattern': [[None, 'redstone', None], ['iron_ingot', 'redstone', 'iron_ingot'], [None, 'iron_ingot', None]],
        'output': ('compass', 1),
        'category': 'utilities',
        'unlock_tier': 2,
        'description': 'Points to spawn'
    },
    'clock': {
        'pattern': [[None, 'redstone', None], ['gold_ingot', 'redstone', 'gold_ingot'], [None, 'gold_ingot', None]],
        'output': ('clock', 1),
        'category': 'utilities',
        'unlock_tier': 2,
        'description': 'Shows time'
    },
    'shears': {
        'pattern': [[None, None, None], ['iron_ingot', None, None], [None, 'iron_ingot', None]],
        'output': ('shears', 1),
        'category': 'tools',
        'unlock_tier': 1,
        'uses': 238,
        'description': 'Harvest wool, leaves, tall grass'
    },

    # ============================================================
    # BUILDING BLOCKS
    # ============================================================

    # Bricks and stone
    'bricks': {
        'pattern': [[None, 'brick', None], ['brick', None, 'brick'], [None, 'brick', None]],
        'output': ('bricks', 1),
        'category': 'building',
        'unlock_tier': 2
    },
    'stone_bricks': {
        'pattern': [[None, None, None], ['stone', 'stone', None], ['stone', 'stone', None]],
        'output': ('stone_bricks', 4),
        'category': 'building',
        'unlock_tier': 1
    },
    'stone_brick_slab': {
        'pattern': [[None, None, None], ['stone_bricks', 'stone_bricks', 'stone_bricks'], [None, None, None]],
        'output': ('stone_brick_slab', 6),
        'category': 'building',
        'unlock_tier': 1
    },
    'stone_brick_stairs': {
        'pattern': [[None, None, None], ['stone_bricks', None, None], ['stone_bricks', 'stone_bricks', None]],
        'output': ('stone_brick_stairs', 4),
        'category': 'building',
        'unlock_tier': 1
    },
    'chiseled_stone_bricks': {
        'pattern': [[None, 'stone_brick_slab', None], [None, 'stone_brick_slab', None], [None, 'stone_brick_slab', None]],
        'output': ('chiseled_stone_bricks', 1),
        'category': 'building',
        'unlock_tier': 1
    },
    'cracked_stone_bricks': {
        'pattern': 'smelt',
        'input': 'stone_bricks',
        'output': 'cracked_stone_bricks'
    },

    # Sandstone
    'sandstone': {
        'pattern': [[None, None, None], ['sand', 'sand', None], ['sand', 'sand', None]],
        'output': ('sandstone', 1),
        'category': 'building',
        'unlock_tier': 1
    },
    'chiseled_sandstone': {
        'pattern': [[None, 'sandstone_slab', None], [None, 'sandstone_slab', None], [None, 'sandstone_slab', None]],
        'output': ('chiseled_sandstone', 1),
        'category': 'building',
        'unlock_tier': 1
    },
    'cut_sandstone': {
        'pattern': [[None, None, None], ['sandstone', 'sandstone', None], ['sandstone', 'sandstone', None]],
        'output': ('cut_sandstone', 1),
        'category': 'building',
        'unlock_tier': 1
    },
    'sandstone_slab': {
        'pattern': [[None, None, None], ['sandstone', 'sandstone', 'sandstone'], [None, None, None]],
        'output': ('sandstone_slab', 6),
        'category': 'building',
        'unlock_tier': 1
    },
    'sandstone_stairs': {
        'pattern': [[None, None, None], ['sandstone', None, None], ['sandstone', 'sandstone', None]],
        'output': ('sandstone_stairs', 4),
        'category': 'building',
        'unlock_tier': 1
    },

    # Red Sandstone
    'red_sandstone': {
        'pattern': [[None, None, None], ['red_sand', 'red_sand', None], ['red_sand', 'red_sand', None]],
        'output': ('red_sandstone', 1),
        'category': 'building',
        'unlock_tier': 1
    },
    'chiseled_red_sandstone': {
        'pattern': [[None, 'red_sandstone_slab', None], [None, 'red_sandstone_slab', None], [None, 'red_sandstone_slab', None]],
        'output': ('chiseled_red_sandstone', 1),
        'category': 'building',
        'unlock_tier': 1
    },
    'cut_red_sandstone': {
        'pattern': [[None, None, None], ['red_sandstone', 'red_sandstone', None], ['red_sandstone', 'red_sandstone', None]],
        'output': ('cut_red_sandstone', 1),
        'category': 'building',
        'unlock_tier': 1
    },

    # Quartz
    'quartz_block': {
        'pattern': [[None, None, None], ['quartz', 'quartz', None], ['quartz', 'quartz', None]],
        'output': ('quartz_block', 1),
        'category': 'building',
        'unlock_tier': 3
    },
    'quartz_bricks': {
        'pattern': [[None, 'quartz_block', None], ['quartz_block', None, 'quartz_block'], [None, 'quartz_block', None]],
        'output': ('quartz_bricks', 1),
        'category': 'building',
        'unlock_tier': 3
    },
    'quartz_pillar': {
        'pattern': [[None, 'quartz_block', None], ['quartz_block', None, 'quartz_block'], [None, 'quartz_block', None]],
        'output': ('quartz_pillar', 2),
        'category': 'building',
        'unlock_tier': 3
    },
    'chiseled_quartz_block': {
        'pattern': [[None, 'quartz_slab', None], [None, 'quartz_slab', None], [None, 'quartz_slab', None]],
        'output': ('chiseled_quartz_block', 1),
        'category': 'building',
        'unlock_tier': 3
    },

    # Purpur
    'purpur_block': {
        'pattern': [[None, None, None], ['purpur_pillar', 'purpur_pillar', None], ['purpur_pillar', 'purpur_pillar', None]],
        'output': ('purpur_block', 1),
        'category': 'building',
        'unlock_tier': 3
    },
    'purpur_pillar': {
        'pattern': [[None, 'purpur_block', None], ['purpur_block', None, 'purpur_block'], [None, 'purpur_block', None]],
        'output': ('purpur_pillar', 1),
        'category': 'building',
        'unlock_tier': 3
    },
    'purpur_stairs': {
        'pattern': [[None, None, None], ['purpur_block', None, None], ['purpur_block', 'purpur_block', None]],
        'output': ('purpur_stairs', 4),
        'category': 'building',
        'unlock_tier': 3
    },

    # Concrete Powder
    'white_concrete_powder': {
        'pattern': [[None, None, None], ['sand', 'sand', 'gravel'], ['sand', 'sand', 'gravel']],
        'output': ('white_concrete_powder', 8),
        'category': 'building',
        'unlock_tier': 2
    },
    # Add all other colors...

    # ============================================================
    # DECORATIONS
    # ============================================================

    'bed': {
        'pattern': [['wool', 'wool', 'wool'], ['planks', 'planks', 'planks'], [None, None, None]],
        'output': ('red_bed', 1),
        'category': 'utilities',
        'unlock_tier': 1,
        'description': 'Sleep through night'
    },
    'bookshelf': {
        'pattern': [['planks', 'planks', 'planks'], ['book', 'book', 'book'], ['planks', 'planks', 'planks']],
        'output': ('bookshelf', 1),
        'category': 'building',
        'unlock_tier': 1,
        'description': 'Enchanting boost'
    },
    'painting': {
        'pattern': [['stick', 'stick', 'stick'], ['stick', 'wool', 'stick'], ['stick', 'stick', 'stick']],
        'output': ('painting', 1),
        'category': 'decoration',
        'unlock_tier': 1
    },
    'item_frame': {
        'pattern': [[None, 'leather', None], ['stick', None, 'leather'], [None, 'leather', None]],
        'output': ('item_frame', 1),
        'category': 'decoration',
        'unlock_tier': 1
    },
    'flower_pot': {
        'pattern': [[None, None, None], ['brick', None, 'brick'], [None, 'brick', None]],
        'output': ('flower_pot', 1),
        'category': 'decoration',
        'unlock_tier': 1
    },
    'armor_stand': {
        'pattern': [[None, 'stick', None], ['stick', 'smooth_stone_slab', 'stick'], [None, 'stick', None]],
        'output': ('armor_stand', 1),
        'category': 'decoration',
        'unlock_tier': 2
    },

    # ============================================================
    # REDSTONE
    # ============================================================

    'repeater': {
        'pattern': [[None, 'redstone_torch', None], ['redstone', 'redstone', 'redstone'], ['None', 'stone', None]],
        'output': ('repeater', 1),
        'category': 'redstone',
        'unlock_tier': 2,
        'description': 'Extends redstone signal'
    },
    'comparator': {
        'pattern': [[None, 'redstone_torch', None], ['redstone', 'redstone', 'redstone'], [None, 'stone', None]],
        'output': ('comparator', 1),
        'category': 'redstone',
        'unlock_tier': 3,
        'description': 'Compares signal strengths'
    },
    'piston': {
        'pattern': [['planks', 'planks', 'planks'], ['cobblestone', 'iron_ingot', 'cobblestone'], ['cobblestone', 'redstone', 'cobblestone']],
        'output': ('piston', 1),
        'category': 'redstone',
        'unlock_tier': 2,
        'description': 'Pushes blocks'
    },
    'sticky_piston': {
        'pattern': [[None, 'slime_ball', None], ['piston', None, None], [None, None, None]],
        'output': ('sticky_piston', 1),
        'category': 'redstone',
        'unlock_tier': 3,
        'description': 'Pushes and pulls blocks'
    },
    'observer': {
        'pattern': [[None, 'cobblestone', None], ['cobblestone', 'redstone', 'cobblestone'], [None, 'cobblestone', None]],
        'output': ('observer', 1),
        'category': 'redstone',
        'unlock_tier': 3,
        'description': 'Detects block updates'
    },
    'hopper': {
        'pattern': [[None, None, None], ['iron_ingot', 'chest', 'iron_ingot'], [None, 'iron_ingot', None]],
        'output': ('hopper', 1),
        'category': 'redstone',
        'unlock_tier': 2,
        'description': 'Transfers items'
    },
    'dispenser': {
        'pattern': [['cobblestone', 'cobblestone', 'cobblestone'], ['cobblestone', 'bow', 'cobblestone'], ['cobblestone', 'redstone', 'cobblestone']],
        'output': ('dispenser', 1),
        'category': 'redstone',
        'unlock_tier': 2
    },
    'dropper': {
        'pattern': [['cobblestone', 'cobblestone', 'cobblestone'], ['cobblestone', 'redstone', 'cobblestone'], ['cobblestone', 'redstone', 'cobblestone']],
        'output': ('dropper', 1),
        'category': 'redstone',
        'unlock_tier': 2
    },
    'note_block': {
        'pattern': [[None, None, None], ['planks', 'redstone', 'planks'], [None, 'planks', None]],
        'output': ('note_block', 1),
        'category': 'redstone',
        'unlock_tier': 1
    },
    'target': {
        'pattern': [[None, 'redstone', None], ['hay_block', 'hay_block', 'hay_block'], [None, 'redstone', None]],
        'output': ('target', 1),
        'category': 'redstone',
        'unlock_tier': 1
    },

    # ============================================================
    # TRANSPORTATION
    # ============================================================

    'rail': {
        'pattern': [[None, 'iron_ingot', None], ['stick', None, 'stick'], [None, 'iron_ingot', None]],
        'output': ('rail', 16),
        'category': 'transportation',
        'unlock_tier': 2
    },
    'powered_rail': {
        'pattern': [[None, 'gold_ingot', None], ['stick', None, 'stick'], [None, 'redstone', None]],
        'output': ('powered_rail', 6),
        'category': 'transportation',
        'unlock_tier': 3
    },
    'detector_rail': {
        'pattern': [[None, 'iron_ingot', None], ['stick', None, 'stick'], [None, 'redstone', None]],
        'output': ('detector_rail', 6),
        'category': 'transportation',
        'unlock_tier': 3
    },
    'activator_rail': {
        'pattern': [[None, 'iron_ingot', None], ['stick', None, 'stick'], [None, 'redstone', None]],
        'output': ('activator_rail', 6),
        'category': 'transportation',
        'unlock_tier': 3
    },
    'minecart': {
        'pattern': [[None, None, None], ['iron_ingot', None, 'iron_ingot'], [None, None, None]],
        'output': ('minecart', 1),
        'category': 'transportation',
        'unlock_tier': 2
    },
    'chest_minecart': {
        'pattern': [[None, None, None], ['chest', None, None], [None, None, None]],
        'output': ('chest_minecart', 1),
        'category': 'transportation',
        'unlock_tier': 2
    },
    'furnace_minecart': {
        'pattern': [[None, None, None], ['furnace', None, None], [None, None, None]],
        'output': ('furnace_minecart', 1),
        'category': 'transportation',
        'unlock_tier': 2
    },
    'hopper_minecart': {
        'pattern': [[None, None, None], ['hopper', None, None], [None, None, None]],
        'output': ('hopper_minecart', 1),
        'category': 'transportation',
        'unlock_tier': 3
    },
    'tnt_minecart': {
        'pattern': [[None, None, None], ['tnt', None, None], [None, None, None]],
        'output': ('tnt_minecart', 1),
        'category': 'transportation',
        'unlock_tier': 2
    },
    'boat': {
        'pattern': [[None, None, None], [None, 'planks', None], [None, 'planks', None]],
        'output': ('oak_boat', 1),
        'category': 'transportation',
        'unlock_tier': 0,
        'description': 'Travels on water'
    },
    'saddle': {
        'pattern': 'treasure',
        'source': 'village_chest',
        'description': 'Cannot be crafted, must find'
    },

    # ============================================================
    # LATE GAME
    # ============================================================

    'enchanting_table': {
        'pattern': [['book', None, None], ['obsidian', 'obsidian', 'obsidian'], ['diamond', 'obsidian', 'diamond']],
        'output': ('enchanting_table', 1),
        'category': 'magic',
        'unlock_tier': 3,
        'essential': True,
        'description': 'Enchant tools and armor'
    },
    'anvil': {
        'pattern': [[None, None, None], ['iron_block', 'iron_block', None], ['iron_ingot', 'iron_ingot', None]],
        'output': ('anvil', 1),
        'category': 'utility',
        'unlock_tier': 2,
        'essential': True,
        'description': 'Repair and combine items'
    },
    'brewing_stand': {
        'pattern': [[None, 'blaze_rod', None], ['cobblestone', 'blaze_rod', 'cobblestone'], [None, 'cobblestone', None]],
        'output': ('brewing_stand', 1),
        'category': 'magic',
        'unlock_tier': 3,
        'description': 'Brew potions'
    },
    'cauldron': {
        'pattern': [[None, None, None], ['iron_ingot', 'water', 'iron_ingot'], ['iron_ingot', None, 'iron_ingot']],
        'output': ('cauldron', 1),
        'category': 'utility',
        'unlock_tier': 2,
        'description': 'Hold water'
    },
    'loom': {
        'pattern': [[None, None, None], ['string', 'string', None], ['planks', 'planks', None]],
        'output': ('loom', 1),
        'category': 'utility',
        'unlock_tier': 1,
        'description': 'Apply banners to items'
    },
    'cartography_table': {
        'pattern': [[None, 'paper', None], ['planks', 'planks', None], [None, 'planks', None]],
        'output': ('cartography_table', 1),
        'category': 'utility',
        'unlock_tier': 1
    },
    'fletching_table': {
        'pattern': [[None, 'flint', None], ['planks', 'planks', None], [None, 'planks', None]],
        'output': ('fletching_table', 1),
        'category': 'utility',
        'unlock_tier': 1
    },
    'smithing_table': {
        'pattern': [[None, 'iron_ingot', None], ['planks', 'planks', None], [None, 'planks', None]],
        'output': ('smithing_table', 1),
        'category': 'utility',
        'unlock_tier': 1,
        'essential': True,
        'description': 'Upgrade diamond gear to netherite'
    },
    'grindstone': {
        'pattern': [[None, None, None], ['stone', 'stone', None], [None, 'planks', None]],
        'output': ('grindstone', 1),
        'category': 'utility',
        'unlock_tier': 1,
        'description': 'Disenchant and repair'
    },
    'stonecutter': {
        'pattern': [[None, 'iron_ingot', None], ['stone', None, None], [None, None, None]],
        'output': ('stonecutter', 1),
        'category': 'utility',
        'unlock_tier': 1,
        'essential': True,
        'description': 'Cut stone into stairs, slabs, etc.'
    },

    # ============================================================
    # EXPLOSIVES
    # ============================================================

    'tnt': {
        'pattern': [['gunpowder', None, 'gunpowder'], ['sand', 'gunpowder', 'sand'], ['sand', 'gunpowder', 'sand']],
        'output': ('tnt', 1),
        'category': 'explosives',
        'unlock_tier': 1,
        'description': 'Explosive'
    },
    'firework_rocket': {
        'pattern': [[None, 'paper', None], ['gunpowder', None, 'gunpowder'], [None, 'firework_star', None]],
        'output': ('firework_rocket', 3),
        'category': 'explosives',
        'unlock_tier': 3
    },
    'firework_star': {
        'pattern': [['gunpowder', None, 'gunpowder'], [None, 'dye', None], [None, 'gunpowder', None]],
        'output': ('firework_star', 1),
        'category': 'explosives',
        'unlock_tier': 3
    },

    # ============================================================
    # NETHER
    # ============================================================

    'nether_portal': {
        'pattern': 'obsidian_frame',
        'min_size': (4, 5),
        'ignite_with': 'flint_and_steel',
        'description': 'Portal to Nether dimension'
    },
    'crimson_fungus': {
        'pattern': [[None, 'crimson_fungus', None], ['crimson_fungus', 'crimson_fungus', 'crimson_fungus'], [None, 'crimson_fungus', None]],
        'output': ('crimson_fungus', 1),
        'category': 'nether'
    },
    'warped_fungus': {
        'pattern': [[None, 'warped_fungus', None], ['warped_fungus', 'warped_fungus', 'warped_fungus'], [None, 'warped_fungus', None]],
        'output': ('warped_fungus', 1),
        'category': 'nether'
    },
    'crimson_nylium': {
        'pattern': [[None, 'crimson_fungus', None], ['crimson_fungus', None, 'crimson_fungus'], [None, 'crimson_fungus', None]],
        'output': ('crimson_nylium', 1),
        'category': 'nether'
    },
    'warped_nylium': {
        'pattern': [[None, 'warped_fungus', None], ['warped_fungus', None, 'warped_fungus'], [None, 'warped_fungus', None]],
        'output': ('warped_nylium', 1),
        'category': 'nether'
    },
    'nether_bricks': {
        'pattern': [[None, 'nether_brick', None], ['nether_brick', 'nether_brick', 'nether_brick'], [None, 'nether_brick', None]],
        'output': ('nether_bricks', 1),
        'category': 'nether'
    },
    'nether_brick_fence': {
        'pattern': [[None, 'nether_brick', None], ['nether_brick', 'stick', 'nether_brick'], [None, 'nether_brick', None]],
        'output': ('nether_brick_fence', 6),
        'category': 'nether'
    },
    'nether_brick_stairs': {
        'pattern': [[None, None, None], ['nether_bricks', None, None], ['nether_bricks', 'nether_bricks', None]],
        'output': ('nether_brick_stairs', 4),
        'category': 'nether'
    },
    'nether_wart_block': {
        'pattern': [[None, 'nether_wart', None], ['nether_wart', 'nether_wart', 'nether_wart'], [None, 'nether_wart', None]],
        'output': ('nether_wart_block', 1),
        'category': 'nether'
    },
    'shroomlight': {
        'pattern': [[None, 'shroomlight', None], ['shroomlight', None, 'shroomlight'], [None, 'shroomlight', None]],
        'output': ('shroomlight', 1),
        'category': 'nether'
    },

    # ============================================================
    # THE END
    # ============================================================

    'ender_chest': {
        'pattern': [[None, 'obsidian', None], ['obsidian', 'ender_pearl', 'obsidian'], [None, 'obsidian', None]],
        'output': ('ender_chest', 1),
        'category': 'end',
        'unlock_tier': 4,
        'description': 'Portable inventory across dimensions'
    },
    'eye_of_ender': {
        'pattern': [[None, 'ender_pearl', None], ['ender_pearl', 'blaze_powder', 'ender_pearl'], [None, 'ender_pearl', None]],
        'output': ('eye_of_ender', 1),
        'category': 'end',
        'unlock_tier': 3,
        'description': 'Locate strongholds and activate portal'
    },

    # ============================================================
    # MISCELLANEOUS
    # ============================================================

    'ladder': {
        'pattern': [[None, 'stick', None], ['stick', 'stick', None], [None, 'stick', None]],
        'output': ('ladder', 3),
        'category': 'building',
        'unlock_tier': 0
    },
    'trapdoor': {
        'pattern': [[None, None, None], ['planks', 'planks', 'planks'], [None, None, None]],
        'output': ('trapdoor', 2),
        'category': 'building',
        'unlock_tier': 1
    },
    'door': {
        'pattern': [[None, None, None], ['planks', 'planks', None], ['planks', 'planks', None]],
        'output': ('oak_door', 3),
        'category': 'building',
        'unlock_tier': 0
    },
    'fence': {
        'pattern': [[None, 'planks', None], ['stick', 'stick', 'planks'], [None, 'stick', 'stick']],
        'output': ('oak_fence', 3),
        'category': 'building',
        'unlock_tier': 0
    },
    'fence_gate': {
        'pattern': [[None, 'stick', None], ['planks', 'planks', 'stick'], [None, 'stick', None]],
        'output': ('fence_gate', 1),
        'category': 'building',
        'unlock_tier': 0
    },
    'sign': {
        'pattern': [[None, None, None], ['planks', 'planks', 'planks'], [None, 'planks', None]],
        'output': ('oak_sign', 3),
        'category': 'utility',
        'unlock_tier': 0,
        'description': 'Write text'
    },
    'glass_pane': {
        'pattern': [[None, None, None], ['glass', 'glass', 'glass'], [None, None, None]],
        'output': ('glass_pane', 16),
        'category': 'building',
        'unlock_tier': 1
    },
    'iron_bars': {
        'pattern': [[None, None, None], ['iron_ingot', 'iron_ingot', 'iron_ingot'], [None, None, None]],
        'output': ('iron_bars', 16),
        'category': 'building',
        'unlock_tier': 2
    },
    'crafting_table': {
        'pattern': [['planks', 'planks', None], ['planks', 'planks', None], [None, None, None]],
        'output': ('crafting_table', 1),
        'category': 'basic',
        'unlock_tier': 0,
        'essential': True
    },
}

# Recipe aliases for different wood types
WOOD_TYPES = ['oak', 'spruce', 'birch', 'jungle', 'acacia', 'dark_oak', 'mangrove', 'crimson', 'warped']

for wood in WOOD_TYPES:
    if wood == 'crimson' or wood == 'warped':
        log_name = f'{wood}_stem'
    else:
        log_name = f'{wood}_log'

    planks_name = f'{wood}_planks'

    # Add planks recipe
    VANILLA_RECIPES[f'{wood}_planks_from_log'] = {
        'pattern': [[log_name, None, None], [None, None, None], [None, None, None]],
        'output': (planks_name, 4),
        'category': 'basic',
        'unlock_tier': 0
    }

    # Add boat recipe
    VANILLA_RECIPES[f'{wood}_boat'] = {
        'pattern': [[None, None, None], [None, planks_name, None], [None, planks_name, None]],
        'output': (f'{wood}_boat', 1),
        'category': 'transportation',
        'unlock_tier': 0
    }

    # Add door recipe
    VANILLA_RECIPES[f'{wood}_door'] = {
        'pattern': [[None, None, None], [planks_name, planks_name, None], [planks_name, planks_name, None]],
        'output': (f'{wood}_door', 3),
        'category': 'building',
        'unlock_tier': 0
    }

    # Add fence recipe
    VANILLA_RECIPES[f'{wood}_fence'] = {
        'pattern': [[None, planks_name, None], ['stick', 'stick', planks_name], [None, 'stick', 'stick']],
        'output': (f'{wood}_fence', 3),
        'category': 'building',
        'unlock_tier': 0
    }

    # Add trapdoor recipe
    VANILLA_RECIPES[f'{wood}_trapdoor'] = {
        'pattern': [[None, None, None], [planks_name, planks_name, planks_name], [None, None, None]],
        'output': (f'{wood}_trapdoor', 2),
        'category': 'building',
        'unlock_tier': 1
    }

    # Add sign recipe
    VANILLA_RECIPES[f'{wood}_sign'] = {
        'pattern': [[None, None, None], [planks_name, planks_name, planks_name], [None, planks_name, None]],
        'output': (f'{wood}_sign', 3),
        'category': 'utility',
        'unlock_tier': 0
    }

    # Add pressure plate recipe
    VANILLA_RECIPES[f'{wood}_pressure_plate'] = {
        'pattern': [[None, None, None], [planks_name, None, None], [None, None, None]],
        'output': (f'{wood}_pressure_plate', 1),
        'category': 'redstone',
        'unlock_tier': 1
    }

    # Add button recipe
    VANILLA_RECIPES[f'{wood}_button'] = {
        'pattern': [[None, None, None], [planks_name, None, None], [None, None, None]],
        'output': (f'{wood}_button', 1),
        'category': 'redstone',
        'unlock_tier': 1
    }

    # Add stairs recipe
    VANILLA_RECIPES[f'{wood}_stairs'] = {
        'pattern': [[None, None, None], [planks_name, None, None], [planks_name, planks_name, None]],
        'output': (f'{wood}_stairs', 4),
        'category': 'building',
        'unlock_tier': 1
    }

    # Add slab recipe
    VANILLA_RECIPES[f'{wood}_slab'] = {
        'pattern': [[None, None, None], [planks_name, planks_name, planks_name], [None, None, None]],
        'output': (f'{wood}_slab', 6),
        'category': 'building',
        'unlock_tier': 1
    }

# Wool colors for beds
WOOL_COLORS = ['white', 'orange', 'magenta', 'light_blue', 'yellow', 'lime', 'pink', 'gray', 'light_gray', 'cyan', 'purple', 'blue', 'brown', 'green', 'red', 'black']

for color in WOOL_COLORS:
    VANILLA_RECIPES[f'{color}_bed'] = {
        'pattern': [[f'{color}_wool', f'{color}_wool', f'{color}_wool'], ['planks', 'planks', 'planks'], [None, None, None]],
        'output': (f'{color}_bed', 1),
        'category': 'utilities',
        'unlock_tier': 1
    }

    VANILLA_RECIPES[f'{color}_carpet'] = {
        'pattern': [[None, None, None], [f'{color}_wool', f'{color}_wool', f'{color}_wool'], [None, None, None]],
        'output': (f'{color}_carpet', 3),
        'category': 'decoration',
        'unlock_tier': 1
    }

# Stained glass colors
DYE_COLORS = ['white', 'orange', 'magenta', 'light_blue', 'yellow', 'lime', 'pink', 'gray', 'light_gray', 'cyan', 'purple', 'blue', 'brown', 'green', 'red', 'black']

for color in DYE_COLORS:
    VANILLA_RECIPES[f'{color}_stained_glass'] = {
        'pattern': [[None, 'glass', None], ['glass', f'{color}_dye', 'glass'], [None, 'glass', None]],
        'output': (f'{color}_stained_glass', 8),
        'category': 'decoration',
        'unlock_tier': 2
    }

    VANILLA_RECIPES[f'{color}_stained_glass_pane'] = {
        'pattern': [[None, None, None], [f'{color}_stained_glass', f'{color}_stained_glass', f'{color}_stained_glass'], [None, None, None]],
        'output': (f'{color}_stained_glass_pane', 16),
        'category': 'decoration',
        'unlock_tier': 2
    }
