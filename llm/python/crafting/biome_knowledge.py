"""
Complete Minecraft Biome Knowledge
All biomes, their features, resources, and characteristics
"""

BIOME_DATABASE = {
    # ============================================================
    # OVERWORLD BIOMES - Temperate
    # ============================================================

    'plains': {
        'category': 'overworld',
        'temperature': 'medium',
        'humidity': 'medium',
        'rarity': 'common',
        'color': 'green',
        'description': 'Grassy flatlands with scattered trees',
        'resources': ['grass', 'dirt', 'oak_log', 'water', 'sand', 'clay'],
        'mobs': ['pig', 'cow', 'sheep', 'chicken', 'horse', 'donkey', 'villager'],
        'structures': ['village', 'pillager_outpost', 'mineshaft', 'ruined_portal', 'trail_ruins'],
        'special_features': ['sunflower_plains_variant', 'starting_biome'],
        'danger_level': 'low',
        'priority': 'high',
        'recommended_for': 'base_building'
    },
    'sunflower_plains': {
        'category': 'overworld',
        'temperature': 'medium',
        'humidity': 'medium',
        'rarity': 'rare',
        'variant_of': 'plains',
        'description': 'Plains with sunflowers',
        'resources': ['sunflower', 'grass', 'dirt', 'oak_log'],
        'mobs': ['rabbit', 'pig', 'cow', 'sheep', 'chicken'],
        'structures': ['village'],
        'special_features': ['abundant_sunflowers'],
        'danger_level': 'low',
        'priority': 'medium'
    },
    'forest': {
        'category': 'overworld',
        'temperature': 'medium',
        'humidity': 'medium',
        'rarity': 'common',
        'color': 'green',
        'description': 'Dense oak and birch tree forests',
        'resources': ['oak_log', 'birch_log', 'grass', 'flowers', 'mushroom', 'bee_nest'],
        'mobs': ['wolf', 'pig', 'cow', 'sheep', 'chicken', 'rabbit', 'bee'],
        'structures': ['woodland_mansion', 'trail_ruins'],
        'special_features': ['dense_trees', 'flower_forest_variant'],
        'danger_level': 'low',
        'priority': 'high',
        'recommended_for': 'wood_gathering'
    },
    'flower_forest': {
        'category': 'overworld',
        'temperature': 'medium',
        'humidity': 'medium',
        'rarity': 'rare',
        'variant_of': 'forest',
        'description': 'Forest with many flower types',
        'resources': ['flowers', 'oak_log', 'birch_log', 'bee_nest'],
        'mobs': ['rabbit', 'bee'],
        'structures': [],
        'special_features': ['rare_flowers', 'tulips', 'cornflowers', 'lilies'],
        'danger_level': 'low',
        'priority': 'medium',
        'recommended_for': 'bee_farming'
    },
    'dark_forest': {
        'category': 'overworld',
        'temperature': 'medium',
        'humidity': 'medium',
        'rarity': 'uncommon',
        'color': 'dark_green',
        'description': 'Dense forest with dark oak trees and huge mushrooms',
        'resources': ['dark_oak_log', 'brown_mushroom', 'red_mushroom', 'grass', 'flowers'],
        'mobs': ['spider', 'skeleton', 'zombie', 'witch', 'wolf', 'panda'],
        'structures': ['woodland_mansion', 'trail_ruins'],
        'special_features': ['huge_mushrooms', 'dark_oak', 'shade'],
        'danger_level': 'high',
        'priority': 'medium',
        'recommended_for': 'woodland_mansion_loot'
    },
    'birch_forest': {
        'category': 'overworld',
        'temperature': 'medium',
        'humidity': 'medium',
        'rarity': 'common',
        'variant_of': 'forest',
        'description': 'Forest of mostly birch trees',
        'resources': ['birch_log', 'grass', 'mushroom'],
        'mobs': ['pig', 'cow', 'sheep', 'chicken', 'wolf'],
        'structures': ['trail_ruins'],
        'special_features': ['tall_birch_variant', 'old_growth_birch'],
        'danger_level': 'low',
        'priority': 'medium'
    },
    'river': {
        'category': 'overworld',
        'temperature': 'varies',
        'humidity': 'high',
        'rarity': 'common',
        'color': 'blue',
        'description': 'Flowing water cutting through terrain',
        'resources': ['water', 'clay', 'sand', 'dirt', 'grass', 'seagrass', 'kelp', 'salmon', 'cod'],
        'mobs': ['dolphin', 'salmon', 'cod', 'squid', 'turtle', 'frog'],
        'structures': ['shipwreck', 'ocean_ruins', 'trail_ruins'],
        'special_features': ['water_source', 'fishing'],
        'danger_level': 'none',
        'priority': 'medium',
        'recommended_for': 'water_source'
    },

    # ============================================================
    # OVERWORLD BIOMES - Cold
    # ============================================================

    'taiga': {
        'category': 'overworld',
        'temperature': 'cold',
        'humidity': 'medium',
        'rarity': 'common',
        'color': 'dark_green',
        'description': 'Cold forest with spruce trees',
        'resources': ['spruce_log', 'grass', 'fern', 'sweet_berry_bush', 'dirt'],
        'mobs': ['wolf', 'fox', 'rabbit', 'pig', 'cow', 'sheep', 'chicken'],
        'structures': ['village', 'pillager_outpost', 'trail_ruins'],
        'special_features': ['snowy_variant', 'sweet_berry_bushes'],
        'danger_level': 'low',
        'priority': 'medium',
        'recommended_for': 'sweet_berry_farming'
    },
    'snowy_taiga': {
        'category': 'overworld',
        'temperature': 'cold',
        'humidity': 'medium',
        'rarity': 'uncommon',
        'variant_of': 'taiga',
        'description': 'Taiga covered in snow',
        'resources': ['spruce_log', 'snow', 'snow_block', 'sweet_berry_bush'],
        'mobs': ['wolf', 'fox', 'rabbit', 'polar_bear', 'pig', 'cow', 'sheep'],
        'structures': ['village', 'igloo', 'trail_ruins'],
        'special_features': ['snow_covered', 'ice'],
        'danger_level': 'medium',
        'priority': 'medium'
    },
    'old_growth_spruce_taiga': {
        'category': 'overworld',
        'temperature': 'cold',
        'humidity': 'medium',
        'rarity': 'rare',
        'variant_of': 'taiga',
        'description': 'Large spruce trees with podzol',
        'resources': ['spruce_log', 'podzol', 'moss_block', 'dirt', 'grass', 'fern'],
        'mobs': ['wolf', 'fox', 'rabbit', 'pig', 'cow', 'sheep', 'chicken'],
        'structures': ['trail_ruins'],
        'special_features': ['huge_spruce', 'podzol', 'moss_carpet'],
        'danger_level': 'low',
        'priority': 'medium',
        'recommended_for': 'moss_blocks'
    },
    'snowy_plains': {
        'category': 'overworld',
        'temperature': 'cold',
        'humidity': 'low',
        'rarity': 'common',
        'color': 'white',
        'description': 'Flat snowy wasteland',
        'resources': ['snow', 'snow_block', 'ice', 'dirt'],
        'mobs': ['polar_bear', 'rabbit', 'stray', 'pig', 'cow', 'sheep', 'chicken'],
        'structures': ['village', 'igloo', 'pillager_outpost', 'trail_ruins'],
        'special_features': ['exposed_dripstone_caves', 'frozen_rivers'],
        'danger_level': 'medium',
        'priority': 'low'
    },
    'ice_spikes': {
        'category': 'overworld',
        'temperature': 'cold',
        'humidity': 'low',
        'rarity': 'rare',
        'variant_of': 'snowy_plains',
        'description': 'Snowy plains with ice spikes',
        'resources': ['snow', 'snow_block', 'packed_ice', 'blue_ice'],
        'mobs': ['polar_bear', 'rabbit', 'stray'],
        'structures': [],
        'special_features': ['ice_spike_structures', 'blue_ice_rare'],
        'danger_level': 'medium',
        'priority': 'medium',
        'recommended_for': 'packed_ice'
    },
    'frozen_river': {
        'category': 'overworld',
        'temperature': 'cold',
        'humidity': 'high',
        'rarity': 'uncommon',
        'variant_of': 'river',
        'description': 'River frozen over with ice',
        'resources': ['ice', 'water', 'dirt', 'sand', 'clay'],
        'mobs': ['salmon', 'cod', 'dolphin'],
        'structures': ['shipwreck', 'ocean_ruins'],
        'special_features': ['ice_surface', 'water_underneath'],
        'danger_level': 'low',
        'priority': 'medium'
    },
    'grove': {
        'category': 'overworld',
        'temperature': 'cold',
        'humidity': 'medium',
        'rarity': 'uncommon',
        'color': 'white_green',
        'description': 'Snowy taiga with mountains',
        'resources': ['spruce_log', 'snow', 'powder_snow', 'dirt'],
        'mobs': ['rabbit', 'fox', 'pig', 'cow', 'sheep', 'chicken'],
        'structures': ['igloo', 'trail_ruins'],
        'special_features': ['powder_snow', 'snowy_mountains'],
        'danger_level': 'medium',
        'priority': 'medium'
    },
    'snowy_slopes': {
        'category': 'overworld',
        'temperature': 'cold',
        'humidity': 'low',
        'rarity': 'uncommon',
        'color': 'white',
        'description': 'Mountain slopes with snow',
        'resources': ['snow', 'snow_block', 'powder_snow', 'stone', 'dirt'],
        'mobs': ['goat', 'rabbit', 'polar_bear'],
        'structures': ['pillager_outpost', 'trail_ruins'],
        'special_features': ['goats', 'powder_snow'],
        'danger_level': 'medium',
        'priority': 'medium'
    },

    # ============================================================
    # OVERWORLD BIOMES - Dry/Hot
    # ============================================================

    'desert': {
        'category': 'overworld',
        'temperature': 'hot',
        'humidity': 'low',
        'rarity': 'common',
        'color': 'yellow',
        'description': 'Sandy wasteland with cacti',
        'resources': ['sand', 'sandstone', 'cactus', 'dirt', 'dead_bush', 'sugar_cane'],
        'mobs': ['rabbit', 'husk'],
        'structures': ['village', 'desert_pyramid', 'fossil', 'pillager_outpost', 'trail_ruins'],
        'special_features': ['no_rain', 'sandstorms'],
        'danger_level': 'medium',
        'priority': 'medium',
        'recommended_for': 'sand_farming'
    },
    'savanna': {
        'category': 'overworld',
        'temperature': 'hot',
        'humidity': 'low',
        'rarity': 'uncommon',
        'color': 'yellow_green',
        'description': 'Flat grassland with acacia trees',
        'resources': ['acacia_log', 'grass', 'dirt', 'tall_grass', 'coarse_dirt', 'flower'],
        'mobs': ['pig', 'cow', 'sheep', 'chicken', 'horse', 'donkey', 'llama', 'villager'],
        'structures': ['village', 'pillager_outpost', 'trail_ruins'],
        'special_features': ['flat_terrain', 'acacia_trees', 'windswept_variant'],
        'danger_level': 'low',
        'priority': 'medium',
        'recommended_for': 'horse_taming'
    },
    'windswept_savanna': {
        'category': 'overworld',
        'temperature': 'hot',
        'humidity': 'low',
        'rarity': 'rare',
        'variant_of': 'savanna',
        'description': 'Mountainous savanna',
        'resources': ['acacia_log', 'stone', 'grass', 'dirt'],
        'mobs': ['pig', 'cow', 'sheep', 'chicken', 'llama'],
        'structures': ['trail_ruins'],
        'special_features': ['mountains', 'acacia_trees'],
        'danger_level': 'medium',
        'priority': 'low'
    },
    'badlands': {
        'category': 'overworld',
        'temperature': 'hot',
        'humidity': 'low',
        'rarity': 'rare',
        'color': 'orange_red',
        'description': 'Red clay and terracotta formations',
        'resources': ['red_sand', 'terracotta', 'red_terracotta', 'gold_ore', 'dead_bush', 'cactus'],
        'mobs': ['armadillo', 'minecart_with_chest'],
        'structures': ['mineshaft', 'badlands_biomewoods'],
        'special_features': ['no_rain', 'unique_terrain', 'abundant_gold'],
        'danger_level': 'low',
        'priority': 'medium',
        'recommended_for': 'gold_mining', 'terracotta'
    },
    'eroded_badlands': {
        'category': 'overworld',
        'temperature': 'hot',
        'humidity': 'low',
        'rarity': 'rare',
        'variant_of': 'badlands',
        'description': 'Badlands with unique tall formations',
        'resources': ['red_sand', 'terracotta', 'red_terracotta', 'gold_ore'],
        'mobs': ['armadillo', 'minecart_with_chest'],
        'structures': ['mineshaft'],
        'special_features': ['tall_terracotta_formation'],
        'danger_level': 'low',
        'priority': 'medium',
        'recommended_for': 'sightseeing'
    },

    # ============================================================
    # OVERWORLD BIOMES - Unique
    # ============================================================

    'jungle': {
        'category': 'overworld',
        'temperature': 'hot',
        'humidity': 'high',
        'rarity': 'uncommon',
        'color': 'bright_green',
        'description': 'Dense tropical forest',
        'resources': ['jungle_log', 'cocoa_bean', 'melon', 'vines', 'bamboo', 'moss_carpet', 'fern'],
        'mobs': ['parrot', 'ocelot', 'panda', 'chicken', 'pig', 'cow', 'sheep', 'zombie', 'skeleton', 'spider', 'creeper'],
        'structures': ['jungle_pyramid', 'trail_ruins'],
        'special_features': ['cocoa_pods', 'melons', 'bamboo', 'vines', 'dense_canopy'],
        'danger_level': 'medium',
        'priority': 'medium',
        'recommended_for': 'cocoa_melon_bamboo'
    },
    'bamboo_jungle': {
        'category': 'overworld',
        'temperature': 'hot',
        'humidity': 'high',
        'rarity': 'rare',
        'variant_of': 'jungle',
        'description': 'Jungle variant with abundant bamboo',
        'resources': ['bamboo', 'jungle_log', 'cocoa_bean', 'melon', 'grass', 'dirt'],
        'mobs': ['parrot', 'panda', 'ocelot', 'chicken', 'pig', 'cow', 'sheep'],
        'structures': ['jungle_pyramid'],
        'special_features': ['abundant_bamboo', 'podzol_patches'],
        'danger_level': 'medium',
        'priority': 'medium',
        'recommended_for': 'bamboo_farming'
    },
    'swamp': {
        'category': 'overworld',
        'temperature': 'medium',
        'humidity': 'high',
        'rarity': 'uncommon',
        'color': 'dark_green',
        'description': 'Wetland with trees and water',
        'resources': ['clay', 'sand', 'grass', 'water_lily', 'blue_orchid', 'mushroom', 'oak_log'],
        'mobs': ['slime', 'frog', 'chicken', 'pig', 'cow', 'sheep', 'zombie', 'skeleton', 'creeper'],
        'structures': ['swamp_hut', 'fossil', 'shipwreck', 'ocean_ruins', 'trail_ruins'],
        'special_features': ['slime_spawn', 'blue_orchid', 'water_lily', 'fog'],
        'danger_level': 'medium',
        'priority': 'medium',
        'recommended_for': 'slime_farming'
    },
    'mangrove_swamp': {
        'category': 'overworld',
        'temperature': 'hot',
        'humidity': 'high',
        'rarity': 'uncommon',
        'variant_of': 'swamp',
        'description': 'Swamp with mangrove trees',
        'resources': ['mangrove_log', 'mangrove_roots', 'muddy_mangrove_roots', 'clay', 'water_lily', 'moss_carpet'],
        'mobs': ['frog', 'slime', 'chicken', 'pig', 'cow', 'sheep', 'bee'],
        'structures': ['trail_ruins'],
        'special_features': ['mangrove_trees', 'mud', 'warm_frogs'],
        'danger_level': 'medium',
        'priority': 'medium',
        'recommended_for': 'mud_mangrove_logs'
    },
    'mushroom_fields': {
        'category': 'overworld',
        'temperature': 'medium',
        'humidity': 'medium',
        'rarity': 'rare',
        'color': 'purple',
        'description': 'Island covered in mycelium and mushrooms',
        'resources': ['mycelium', 'mushroom', 'brown_mushroom', 'red_mushroom', 'dirt'],
        'mobs': ['mooshroom'],
        'structures': [],
        'special_features': ['no_hostile_mobs', 'mycelium', 'huge_mushroom_growth'],
        'danger_level': 'none',
        'priority': 'high',
        'recommended_for': 'mushroom_farming', 'mooshroom_farm'
    },
    'beach': {
        'category': 'overworld',
        'temperature': 'varies',
        'humidity': 'medium',
        'rarity': 'common',
        'color': 'yellow',
        'description': 'Sandy shore between land and ocean',
        'resources': ['sand', 'dirt', 'clay', 'water', 'turtle_egg', 'seagrass', 'sugar_cane'],
        'mobs': ['turtle', 'crab', 'dolphin', 'cod', 'salmon'],
        'structures': ['shipwreck', 'buried_treasure', 'trail_ruins'],
        'special_features': ['turtle_nesting', 'sand', 'ocean_access'],
        'danger_level': 'low',
        'priority': 'medium'
    },
    'stony_shore': {
        'category': 'overworld',
        'temperature': 'varies',
        'humidity': 'medium',
        'rarity': 'uncommon',
        'variant_of': 'beach',
        'description': 'Stone shore with gravel',
        'resources': ['stone', 'gravel', 'dirt', 'coal_ore', 'iron_ore', 'sand'],
        'mobs': ['cod', 'dolphin'],
        'structures': ['buried_treasure', 'shipwreck', 'trail_ruins'],
        'special_features': ['steep_cliffs', 'stone_terrain'],
        'danger_level': 'medium',
        'priority': 'low'
    },
    'stony_peaks': {
        'category': 'overworld',
        'temperature': 'cold',
        'humidity': 'low',
        'rarity': 'uncommon',
        'color': 'gray',
        'description': 'High mountain peaks with stone',
        'resources': ['stone', 'gravel', 'calcite', 'coal_ore', 'iron_ore', 'copper_ore', 'emerald_ore'],
        'mobs': ['goat'],
        'structures': ['pillager_outpost'],
        'special_features': ['high_altitude', 'snowy_peaks_above', 'goats'],
        'danger_level': 'medium',
        'priority': 'medium',
        'recommended_for': 'emerald_mining'
    },
    'meadow': {
        'category': 'overworld',
        'temperature': 'medium',
        'humidity': 'medium',
        'rarity': 'uncommon',
        'color': 'light_green',
        'description': 'Grassy flatland with flowers and tall grass',
        'resources': ['grass', 'tall_grass', 'dirt', 'flowers', 'dandelion', 'azure_bluet', 'oxeye_daisy'],
        'mobs': ['horse', 'donkey', 'buried_treasure', 'pig', 'cow', 'sheep', 'chicken'],
        'structures': ['trail_ruins'],
        'special_features': ['abundant_flowers', 'tall_grass', 'horse_spawn'],
        'danger_level': 'low',
        'priority': 'medium',
        'recommended_for': 'horse_taming', 'flower_farming'
    },
    'cherry_grove': {
        'category': 'overworld',
        'temperature': 'medium',
        'humidity': 'medium',
        'rarity': 'uncommon',
        'color': 'pink',
        'description': 'Mountain with cherry blossom trees',
        'resources': ['cherry_log', 'cherry_sapling', 'pink_petals', 'grass', 'dirt'],
        'mobs': ['pig', 'cow', 'sheep', 'chicken', 'bee'],
        'structures': ['trail_ruins'],
        'special_features': ['cherry_blossoms', 'pink_petals', 'mountainous'],
        'danger_level': 'low',
        'priority': 'medium',
        'recommended_for': 'scenic_building'
    },

    # ============================================================
    # OVERWORLD BIOMES - Mountainous
    # ============================================================

    'windswept_hills': {
        'category': 'overworld',
        'temperature': 'cold',
        'humidity': 'medium',
        'rarity': 'uncommon',
        'color': 'gray_green',
        'description': 'Mountainous terrain with snow',
        'resources': ['stone', 'gravel', 'coal_ore', 'iron_ore', 'emerald_ore', 'dirt', 'grass'],
        'mobs': ['llama', 'pig', 'cow', 'sheep', 'chicken'],
        'structures': ['pillager_outpost', 'trail_ruins'],
        'special_features': ['mountains', 'emeralds', 'llamas'],
        'danger_level': 'medium',
        'priority': 'medium',
        'recommended_for': 'emerald_mining'
    },
    'jagged_peaks': {
        'category': 'overworld',
        'temperature': 'cold',
        'humidity': 'low',
        'rarity': 'uncommon',
        'color': 'white_gray',
        'description': 'High snowy peaks',
        'resources': ['snow', 'snow_block', 'ice', 'packed_ice', 'stone', 'coal_ore', 'emerald_ore'],
        'mobs': ['goat', 'pig', 'cow', 'sheep', 'chicken'],
        'structures': ['pillager_outpost', 'trail_ruins'],
        'special_features': ['snowy_peaks', 'goats', 'emeralds', 'ice'],
        'danger_level': 'medium',
        'priority': 'medium',
        'recommended_for': 'emerald_mining', 'snow'
    },
    'frozen_peaks': {
        'category': 'overworld',
        'temperature': 'cold',
        'humidity': 'low',
        'rarity': 'uncommon',
        'variant_of': 'jagged_peaks',
        'description': 'Ice covered mountain peaks',
        'resources': ['packed_ice', 'snow', 'snow_block', 'stone', 'coal_ore', 'emerald_ore'],
        'mobs': ['goat', 'rabbit'],
        'structures': [],
        'special_features': ['ice_peaks', 'goats'],
        'danger_level': 'medium',
        'priority': 'medium',
        'recommended_for': 'packed_ice'
    },

    # ============================================================
    # OVERWORLD BIOMES - Underground/Caves
    # ============================================================

    'dripstone_caves': {
        'category': 'underground',
        'temperature': 'varies',
        'humidity': 'varies',
        'rarity': 'common',
        'color': 'brown',
        'description': 'Caves with dripstone and pointed dripstone',
        'resources': ['pointed_dripstone', 'dripstone_block', 'water', 'lava', 'copper_ore', 'iron_ore', 'coal_ore'],
        'mobs': ['drowned', 'zombie', 'skeleton', 'spider', 'cave_spider'],
        'structures': ['monster_room', 'mineshaft', 'stronghold'],
        'special_features': ['dripstone', 'stalactites', 'stalagmites'],
        'danger_level': 'high',
        'priority': 'medium',
        'recommended_for': 'dripstone_farming'
    },
    'lush_caves': {
        'category': 'underground',
        'temperature': 'medium',
        'humidity': 'high',
        'rarity': 'uncommon',
        'color': 'bright_green',
        'description': 'Caves with abundant vegetation',
        'resources': ['moss_block', 'moss_carpet', 'azalea', 'flowering_azalea', 'cave_vines', 'glow_berries', 'grass', 'dirt', 'water'],
        'mobs': ['axolotl', 'drowned', 'zombie', 'skeleton', 'spider'],
        'structures': ['monster_room', 'mineshaft', 'stronghold'],
        'special_features': ['glowing_berries', 'azalea_trees', 'spore_blossom', 'water_lakes'],
        'danger_level': 'medium',
        'priority': 'high',
        'recommended_for': 'moss_blocks', 'glow_berries', 'axolotl'
    },
    'deep_dark': {
        'category': 'underground',
        'temperature': 'medium',
        'humidity': 'medium',
        'rarity': 'uncommon',
        'color': 'dark_blue',
        'description': 'Deep underground with sculk',
        'resources': ['sculk', 'sculk_sensor', 'sculk_catalyst', 'sculk_shrieker', 'sculk_vein', 'ancient_city_loot'],
        'mobs': ['warden', 'skeleton', 'spider', 'zombie'],
        'structures': ['ancient_city', 'stronghold'],
        'special_features': ['warden_spawn', 'darkness', 'ancient_city', 'sculk_spreading'],
        'danger_level': 'extreme',
        'priority': 'medium',
        'recommended_for': 'ancient_city_loot', 'sculk'
    },
    'deepslate': {
        'category': 'underground',
        'temperature': 'medium',
        'humidity': 'medium',
        'rarity': 'common',
        'color': 'dark_gray',
        'description': 'Deep underground with deepslate',
        'resources': ['deepslate', 'cobbled_deepslate', 'diamond_ore', 'iron_ore', 'gold_ore', 'redstone_ore', 'lapis_ore', 'copper_ore', 'coal_ore', 'emerald_ore'],
        'mobs': ['zombie', 'skeleton', 'spider', 'cave_spider', 'silverfish', 'enderman'],
        'structures': ['monster_room', 'mineshaft', 'stronghold', 'mineshaft'],
        'special_features': ['deepslate_variants', 'diamonds_below_0', 'infested_deepslate'],
        'danger_level': 'high',
        'priority': 'high',
        'recommended_for': 'diamond_mining'
    },

    # ============================================================
    # OCEAN BIOMES
    # ============================================================

    'ocean': {
        'category': 'ocean',
        'temperature': 'varies',
        'humidity': 'high',
        'rarity': 'common',
        'color': 'blue',
        'description': 'Deep water with floor',
        'resources': ['water', 'seagrass', 'kelp', 'sand', 'dirt', 'clay', 'gravel', 'coal_ore', 'iron_ore', 'gold_ore'],
        'mobs': ['dolphin', 'squid', 'cod', 'salmon', 'tropical_fish', 'pufferfish', 'drowned'],
        'structures': ['shipwreck', 'ocean_ruins', 'ocean_monument', 'buried_treasure', 'trail_ruins'],
        'special_features': ['fishing', 'seagrass', 'ruins'],
        'danger_level': 'medium',
        'priority': 'medium',
        'recommended_for': 'fishing', 'ocean_monument'
    },
    'deep_ocean': {
        'category': 'ocean',
        'temperature': 'varies',
        'humidity': 'high',
        'rarity': 'uncommon',
        'variant_of': 'ocean',
        'description': 'Very deep ocean',
        'resources': ['water', 'seagrass', 'kelp', 'sand', 'dirt', 'gravel', 'coal_ore', 'iron_ore', 'gold_ore', 'diamond_ore'],
        'mobs': ['dolphin', 'squid', 'cod', 'salmon', 'guardian', 'elder_guardian', 'drowned'],
        'structures': ['ocean_monument', 'shipwreck', 'ocean_ruins', 'buried_treasure'],
        'special_features': ['ocean_monument', 'guardians', 'deep_water'],
        'danger_level': 'high',
        'priority': 'medium',
        'recommended_for': 'ocean_monument', 'sponges'
    },
    'frozen_ocean': {
        'category': 'ocean',
        'temperature': 'cold',
        'humidity': 'high',
        'rarity': 'uncommon',
        'variant_of': 'ocean',
        'description': 'Ocean with ice surface',
        'resources': ['water', 'ice', 'packed_ice', 'seagrass', 'snow', 'sand', 'dirt', 'gravel'],
        'mobs': ['dolphin', 'squid', 'cod', 'salmon', 'polar_bear', 'stray', 'drowned'],
        'structures': ['shipwreck', 'ocean_ruins', 'buried_treasure', 'trail_ruins'],
        'special_features': ['ice_surface', 'blue_ice', 'polar_bears'],
        'danger_level': 'medium',
        'priority': 'medium',
        'recommended_for': 'blue_ice'
    },
    'cold_ocean': {
        'category': 'ocean',
        'temperature': 'cold',
        'humidity': 'high',
        'rarity': 'uncommon',
        'variant_of': 'ocean',
        'description': 'Cold ocean water',
        'resources': ['water', 'seagrass', 'kelp', 'sand', 'dirt', 'gravel', 'coal_ore', 'iron_ore'],
        'mobs': ['dolphin', 'squid', 'cod', 'salmon', 'drowned'],
        'structures': ['shipwreck', 'ocean_ruins', 'buried_treasure', 'trail_ruins'],
        'special_features': ['salmon_cod', 'kelp_forests'],
        'danger_level': 'medium',
        'priority': 'medium'
    },
    'lukewarm_ocean': {
        'category': 'ocean',
        'temperature': 'medium',
        'humidity': 'high',
        'rarity': 'uncommon',
        'variant_of': 'ocean',
        'description': 'Warm ocean with coral',
        'resources': ['water', 'seagrass', 'sand', 'dirt', 'clay', 'coral', 'sea_pickle'],
        'mobs': ['dolphin', 'squid', 'cod', 'pufferfish', 'tropical_fish', 'drowned'],
        'structures': ['shipwreck', 'ocean_ruins', 'trail_ruins'],
        'special_features': ['coral', 'sea_pickles'],
        'danger_level': 'medium',
        'priority': 'medium',
        'recommended_for': 'coral', 'sea_pickles'
    },
    'warm_ocean': {
        'category': 'ocean',
        'temperature': 'hot',
        'humidity': 'high',
        'rarity': 'rare',
        'variant_of': 'ocean',
        'description': 'Warm ocean with abundant coral',
        'resources': ['water', 'coral', 'coral_block', 'sea_pickle', 'sand', 'dirt'],
        'mobs': ['dolphin', 'squid', 'pufferfish', 'tropical_fish', 'drowned'],
        'structures': ['shipwreck', 'ocean_ruins'],
        'special_features': ['coral_reefs', 'sea_pickles', 'no_salmon'],
        'danger_level': 'medium',
        'priority': 'medium',
        'recommended_for': 'coral_blocks', 'tropical_fish'
    },

    # ============================================================
    # NETHER BIOMES
    # ============================================================

    'nether_wastes': {
        'category': 'nether',
        'temperature': 'hot',
        'humidity': 'dry',
        'rarity': 'common',
        'color': 'red',
        'description': 'Open nether with netherrack',
        'resources': ['netherrack', 'nether_quartz_ore', 'glowstone', 'gravel', 'soul_sand', 'lava'],
        'mobs': ['zombified_piglin', 'piglin', 'ghast', 'strider'],
        'structures': ['nether_fortress', 'bastion_remnant', 'ruined_portal'],
        'special_features': ['nether_fortress_spawn', 'piglin_neutral'],
        'danger_level': 'high',
        'priority': 'medium',
        'recommended_for': 'nether_quartz', 'glowstone'
    },
    'crimson_forest': {
        'category': 'nether',
        'temperature': 'hot',
        'humidity': 'dry',
        'rarity': 'uncommon',
        'color': 'crimson_red',
        'description': 'Red forest with crimson fungus',
        'resources': ['crimson_nylium', 'crimson_stem', 'crimson_fungus', 'shroomlight', 'weeping_vines', 'nether_wart'],
        'mobs': ['hoglin', 'piglin', 'zombified_piglin', 'strider'],
        'structures': ['bastion_remnant', 'ruined_portal'],
        'special_features': ['hoglin_spawn', 'crimson_trees'],
        'danger_level': 'high',
        'priority': 'high',
        'recommended_for': 'hoglin_farming', 'crimson_stem'
    },
    'warped_forest': {
        'category': 'nether',
        'temperature': 'hot',
        'humidity': 'dry',
        'rarity': 'uncommon',
        'color': 'blue_green',
        'description': 'Blue forest with warped fungus',
        'resources': ['warped_nylium', 'warped_stem', 'warped_fungus', 'shroomlight', 'twisting_vines', 'nether_sprouts'],
        'mobs': ['enderman', 'strider'],
        'structures': ['bastion_remnant', 'ruined_portal'],
        'special_features': ['enderman_spawn', 'safe_from_piglins'],
        'danger_level': 'low',
        'priority': 'high',
        'recommended_for': 'safe_base', 'warped_stem'
    },
    'soul_sand_valley': {
        'category': 'nether',
        'temperature': 'hot',
        'humidity': 'dry',
        'rarity': 'uncommon',
        'color': 'brown',
        'description': 'Blue sand with soul fire',
        'resources': ['soul_sand', 'soul_soil', 'soul_fire', 'basalt', 'glowstone', 'gravel', 'bone_block'],
        'mobs': ['skeleton', 'skeleton_horse', 'ghast', 'strider'],
        'structures': ['bastion_remnant', 'nether_fortress', 'ruined_portal'],
        'special_features': ['soul_fire', 'basalt_deltas', 'skeleton_horses'],
        'danger_level': 'high',
        'priority': 'medium',
        'recommended_for': 'soul_sand', 'soul_soil'
    },
    'basalt_deltas': {
        'category': 'nether',
        'temperature': 'hot',
        'humidity': 'dry',
        'rarity': 'uncommon',
        'color': 'gray',
        'description': 'Volcanic terrain with basalt columns',
        'resources': ['basalt', 'blackstone', 'magma_block', 'glowstone', 'gravel', 'lava'],
        'mobs': ['magma_cube', 'ghast'],
        'structures': ['bastion_remnant', 'ruined_portal'],
        'special_features': ['basalt_columns', 'magma_cube_spawn', 'no_piglin'],
        'danger_level': 'high',
        'priority': 'medium',
        'recommended_for': 'basalt', 'blackstone', 'magma_cream'
    },

    # ============================================================
    # THE END BIOMES
    # ============================================================

    'the_end': {
        'category': 'end',
        'temperature': 'medium',
        'humidity': 'dry',
        'rarity': 'unique',
        'color': 'purple',
        'description': 'Main end dimension',
        'resources': ['end_stone', 'obsidian', 'ender_pearl', 'ender_dragon_loot'],
        'mobs': ['enderman', 'ender_dragon'],
        'structures': ['end_city', 'end_ship'],
        'special_features': ['ender_dragon_fight', 'end_gateway', 'outer_islands'],
        'danger_level': 'extreme',
        'priority': 'high',
        'recommended_for': 'ender_dragon', 'elytra'
    },
    'end_midlands': {
        'category': 'end',
        'temperature': 'medium',
        'humidity': 'dry',
        'rarity': 'common',
        'variant_of': 'the_end',
        'description': 'Flat end islands',
        'resources': ['end_stone', 'obsidian', 'chorus_plant', 'purpur_block'],
        'mobs': ['enderman', 'shulker'],
        'structures': ['end_city'],
        'special_features': ['end_city_spawn', 'purpur_blocks', 'shulkers'],
        'danger_level': 'high',
        'priority': 'high',
        'recommended_for': 'end_city', 'elytra', 'purpur'
    },
    'end_highlands': {
        'category': 'end',
        'temperature': 'medium',
        'humidity': 'dry',
        'rarity': 'uncommon',
        'variant_of': 'the_end',
        'description': 'Floating end islands',
        'resources': ['end_stone', 'obsidian', 'chorus_plant', 'purpur_block'],
        'mobs': ['enderman', 'shulker'],
        'structures': ['end_city', 'end_ship'],
        'special_features': ['floating_islands', 'chorus_trees'],
        'danger_level': 'high',
        'priority': 'medium',
        'recommended_for': 'chorus_farming'
    },
    'small_end_islands': {
        'category': 'end',
        'temperature': 'medium',
        'humidity': 'dry',
        'rarity': 'common',
        'variant_of': 'the_end',
        'description': 'Small outer end islands',
        'resources': ['end_stone', 'chorus_plant'],
        'mobs': ['enderman'],
        'structures': [],
        'special_features': ['chorus_trees', 'gateway_portals'],
        'danger_level': 'medium',
        'priority': 'medium',
        'recommended_for': 'chorus_farming'
    },

    # ============================================================
    # STRUCTURE LOCATIONS
    # ============================================================

    # Overworld structures
    'village_biomes': ['plains', 'sunflower_plains', 'taiga', 'snowy_taiga', 'desert', 'savanna', 'meadow'],
    'pillager_outpost_biomes': ['plains', 'sunflower_plains', 'taiga', 'snowy_taiga', 'desert', 'savanna', 'meadow', 'grove', 'snowy_slopes', 'windswept_hills'],
    'woodland_mansion_biomes': ['dark_forest', 'forest', 'birch_forest', 'taiga'],
    'mineshaft_biomes': ['all_overworld_biomes'],
    'ocean_monument_biomes': ['ocean', 'deep_ocean', 'cold_ocean', 'frozen_ocean'],
    'shipwreck_biomes': ['ocean', 'beach', 'frozen_ocean'],
    'buried_treasure_biomes': ['ocean', 'beach'],
    'ocean_ruins_biomes': ['ocean', 'deep_ocean', 'cold_ocean', 'frozen_ocean'],
    'swamp_hut_biomes': ['swamp', 'mangrove_swamp'],
    'jungle_pyramid_biomes': ['jungle', 'bamboo_jungle'],
    'desert_pyramid_biomes': ['desert'],
    'igloo_biomes': ['snowy_plains', 'snowy_taiga', 'frozen_river'],
    'ruined_portal_biomes': ['all_overworld', 'nether'],
    'trail_ruins_biomes': ['river', 'swamp', 'beach', 'ocean', 'taiga', 'snowy_plains', 'jungle', 'mangrove_swamp', 'meadow', 'grove', 'snowy_slopes', 'stony_shore'],
    'stronghold_biomes': ['underground', 'deepslate'],
    'ancient_city_biomes': ['deep_dark'],

    # Nether structures
    'nether_fortress_biomes': ['nether_wastes', 'soul_sand_valley'],
    'bastion_remnant_biomes': ['nether_wastes', 'crimson_forest', 'warped_forest', 'soul_sand_valley', 'basalt_deltas'],
    'ruined_portal_biomes': ['all_nether_biomes'],

    # End structures
    'end_city_biomes': ['end_midlands', 'end_highlands'],
    'end_ship_biomes': ['end_midlands', 'end_highlands'],
}

STRUCTURE_DATABASE = {
    # Overworld structures
    'village': {
        'category': 'overworld',
        'rarity': 'uncommon',
        'biomes': BIOME_DATABASE['village_biomes'],
        'description': 'Group of houses with villagers',
        'loot': ['emerald', 'iron_ingot', 'food', 'rare_items'],
        'special': ['trading', 'iron_golem_spawns', 'workstations']
    },
    'pillager_outpost': {
        'category': 'overworld',
        'rarity': 'uncommon',
        'biomes': BIOME_DATABASE['pillager_outpost_biomes'],
        'description': 'Watchtower with pillagers',
        'loot': ['crossbow', 'iron_ingot', 'omniscient_banner'],
        'special': ['bad_omen', 'captain', 'patrols']
    },
    'woodland_mansion': {
        'category': 'overworld',
        'rarity': 'rare',
        'biomes': BIOME_DATABASE['woodland_mansion_biomes'],
        'description': 'Large house with illagers',
        'loot': ['diamond', 'enchanted_book', 'music_disc', 'totem_of_undying'],
        'special': ['evoker', 'vindicator', 'vex', 'secret_rooms']
    },
    'mineshaft': {
        'category': 'underground',
        'rarity': 'common',
        'biomes': ['all_overworld'],
        'description': 'Abandoned mine tunnels',
        'loot': ['rails', 'minecart_with_chest', 'iron_ingot', 'gold_ingot', 'diamond'],
        'special': ['cave_spider_spawner', 'rails', 'wood_supports']
    },
    'ocean_monument': {
        'category': 'ocean',
        'rarity': 'rare',
        'biomes': BIOME_DATABASE['ocean_monument_biomes'],
        'description': 'Underwater prismarine temple',
        'loot': ['sponge', 'prismarine', 'sea_lantern', 'gold_ingot', 'wet_sponge'],
        'special': ['elder_guardian', 'guardians', 'mining_fatigue']
    },
    'shipwreck': {
        'category': 'ocean',
        'rarity': 'common',
        'biomes': BIOME_DATABASE['shipwreck_biomes'],
        'description': 'Sunken ship',
        'loot': ['treasure_map', 'iron_ingot', 'gold_ingot', 'enchanted_book', 'bottle_o_enchanting'],
        'special': ['buried_treasure_map', 'supply_chests']
    },
    'buried_treasure': {
        'category': 'overworld',
        'rarity': 'rare',
        'biomes': BIOME_DATABASE['buried_treasure_biomes'],
        'description': 'Hidden chest underground',
        'loot': ['heart_of_the_sea', 'iron_ingot', 'gold_ingot', 'treasure_map', 'bottle_o_enchanting'],
        'special': ['heart_of_the_sea', 'locator_map']
    },
    'ocean_ruins': {
        'category': 'ocean',
        'rarity': 'common',
        'biomes': BIOME_DATABASE['ocean_ruins_biomes'],
        'description': 'Underwater ruins',
        'loot': ['coal', 'iron_ingot', 'gold_ingot', 'wheat', 'emerald'],
        'special': ['cut_sandstone', 'wet_sponge', ' buried_chests']
    },
    'swamp_hut': {
        'category': 'overworld',
        'rarity': 'rare',
        'biomes': BIOME_DATABASE['swamp_hut_biomes'],
        'description': 'Small house',
        'loot': ['redstone', 'fermented_spider_eye', 'bottle_o_enchanting', 'stick'],
        'special': ['witch_spawn', 'cat']
    },
    'jungle_pyramid': {
        'category': 'overworld',
        'rarity': 'rare',
        'biomes': BIOME_DATABASE['jungle_pyramid_biomes'],
        'description': 'Overgrown jungle temple',
        'loot': ['diamond', 'gold_ingot', 'enchanted_book', 'bottle_o_enchanting'],
        'special': ['puzzles', 'traps', 'hidden_chests']
    },
    'desert_pyramid': {
        'category': 'overworld',
        'rarity': 'rare',
        'biomes': BIOME_DATABASE['desert_pyramid_biomes'],
        'description': 'Sand pyramid',
        'loot': ['diamond', 'gold_ingot', 'enchanted_book', 'bottle_o_enchanting', 'tnt'],
        'special': ['traps', 'hidden_chamber', 'tnt_trap']
    },
    'igloo': {
        'category': 'overworld',
        'rarity': 'rare',
        'biomes': BIOME_DATABASE['igloo_biomes'],
        'description': 'Snow house',
        'loot': ['gold_apple', 'coal', 'emerald', 'bottle_o_enchanting'],
        'special': ['basement_laboratory', 'villager_zombie', 'brewing_stand']
    },
    'ruined_portal': {
        'category': 'overworld',
        'rarity': 'common',
        'biomes': ['all_overworld_biomes'],
        'description': 'Broken nether portal',
        'loot': ['gold_ingot', 'iron_ingot', 'flint_and_steel', 'obsidian', 'fire_charge'],
        'special': ['nether_portal_repair', 'gold_equipment']
    },
    'trail_ruins': {
        'category': 'overworld',
        'rarity': 'common',
        'biomes': BIOME_DATABASE['trail_ruins_biomes'],
        'description': 'Gravel ruins',
        'loot': ['emerald', 'coal', 'wheat', 'wood', 'gravel'],
        'special': ['gravel_path', 'buried_ruins']
    },
    'stronghold': {
        'category': 'underground',
        'rarity': 'rare',
        'biomes': ['underground'],
        'description': 'Underground stone brick fortress',
        'loot': ['ender_pearl', 'iron_ingot', 'gold_ingot', 'redstone', 'diamond'],
        'special': ['end_portal', 'library', 'prison', 'portal_room']
    },
    'ancient_city': {
        'category': 'underground',
        'rarity': 'extremely_rare',
        'biomes': ['deep_dark'],
        'description': 'Massive city deep underground',
        'loot': ['enchanted_book', 'disc_fragment', 'diamond', 'echo_shard', 'soul_speed_enchantment'],
        'special': ['warden', 'sculk', 'soul_speed_boots', 'city_center']
    },
    'fossil': {
        'category': 'overworld',
        'rarity': 'rare',
        'biomes': ['desert', 'swamp'],
        'description': 'Bone structure underground',
        'loot': ['bone_block', 'coal_ore', 'diamond_ore'],
        'special': ['coal_ore_in_bones', 'diamond_rare']
    },
    'monster_room': {
        'category': 'underground',
        'rarity': 'common',
        'biomes': ['caves', 'dripstone_caves', 'lush_caves', 'deepslate'],
        'description': 'Small dungeon',
        'loot': ['string', 'bone', 'redstone', 'coal', 'iron_ingot', 'music_disc_rare'],
        'special': ['spawner', 'chests', 'cobwebs']
    },
    'conduit': {
        'category': 'ocean',
        'rarity': 'player_created',
        'biomes': ['ocean', 'deep_ocean'],
        'description': 'Player created structure',
        'loot': ['heart_of_the_sea'],
        'special': ['conduit_power', 'underwater_vision', 'attacks_hostile']
    },

    # Nether structures
    'nether_fortress': {
        'category': 'nether',
        'rarity': 'uncommon',
        'biomes': BIOME_DATABASE['nether_fortress_biomes'],
        'description': 'Nether brick fortress',
        'loot': ['nether_wart', 'blaze_rod', 'iron_ingot', 'gold_ingot', 'diamond', 'witherskeleton_skull'],
        'special': ['blaze_spawner', 'wither_skeleton', 'nether_wart', 'fortress_bridges']
    },
    'bastion_remnant': {
        'category': 'nether',
        'rarity': 'uncommon',
        'biomes': BIOME_DATABASE['bastion_remnant_biomes'],
        'description': 'Large blackstone structure',
        'loot': ['netherite_ingot', 'ancient_debris', 'snout_banner_pattern', 'gold_ingot', 'soul_speed_enchantment'],
        'special': ['piglin_brute', 'piglin', 'magma_cube_spawner', 'gold_blocks', 'treasure']
    },

    # End structures
    'end_city': {
        'category': 'end',
        'rarity': 'rare',
        'biomes': BIOME_DATABASE['end_city_biomes'],
        'description': 'Purpur city',
        'loot': ['elytra', 'enchanted_book', 'diamond', 'iron_ingot', 'gold_ingot', 'beacon'],
        'special': ['elytra', 'shulker', 'end_ship', 'purpur_blocks', 'treasure_room']
    },
    'end_ship': {
        'category': 'end',
        'rarity': 'rare',
        'biomes': BIOME_DATABASE['end_ship_biomes'],
        'description': 'Floating ship',
        'loot': ['elytra', 'dragon_head', 'enchanted_book'],
        'special': ['elytra', 'dragon_head']
    },
}

# Dimension info
DIMENSION_DATABASE = {
    'overworld': {
        'biomes': ['plains', 'forest', 'desert', 'taiga', 'jungle', 'savanna', 'mountains', 'ocean', 'caves'],
        'unique_features': ['day_night_cycle', 'weather', 'villages', 'strongholds', 'woodland_mansions'],
        'ores': ['coal_ore', 'iron_ore', 'gold_ore', 'copper_ore', 'lapis_ore', 'redstone_ore', 'diamond_ore', 'emerald_ore', 'ancient_debris'],
        'dimensions': 'main'
    },
    'nether': {
        'biomes': ['nether_wastes', 'crimson_forest', 'warped_forest', 'soul_sand_valley', 'basalt_deltas'],
        'unique_features': ['lava_oceans', 'nether_portal', 'fortress', 'bastion', 'blaze', 'ghast'],
        'ores': ['nether_quartz_ore', 'ancient_debris', 'nether_gold_ore'],
        'mobs': ['piglin', 'hoglin', 'zombified_piglin', 'blaze', 'ghast', 'magma_cube', 'strider', 'enderman'],
        'portals': 'nether_portal'
    },
    'end': {
        'biomes': ['the_end', 'end_midlands', 'end_highlands', 'small_end_islands'],
        'unique_features': ['ender_dragon', 'end_city', 'elytra', 'chorus_trees', 'void'],
        'ores': ['end_stone'],
        'mobs': ['enderman', 'ender_dragon', 'shulker'],
        'portals': 'end_portal'
    },
}

def get_biome_info(biome_name: str) -> dict:
    """Get complete information about a biome"""
    return BIOME_DATABASE.get(biome_name, {})

def get_structure_info(structure_name: str) -> dict:
    """Get complete information about a structure"""
    return STRUCTURE_DATABASE.get(structure_name, {})

def get_dimension_info(dimension: str) -> dict:
    """Get dimension information"""
    return DIMENSION_DATABASE.get(dimension, {})

def get_biomes_by_category(category: str) -> list:
    """Get all biomes in a category"""
    return [name for name, data in BIOME_DATABASE.items() if data.get('category') == category]

def get_safe_biomes() -> list:
    """Get biomes with no hostile mob spawns naturally"""
    return [name for name, data in BIOME_DATABASE.items() if data.get('danger_level') in ['none', 'low']]

def get_dangerous_biomes(min_danger: str = 'high') -> list:
    """Get biomes above a danger level"""
    danger_levels = {'none': 0, 'low': 1, 'medium': 2, 'high': 3, 'extreme': 4, 'very_high': 5}
    threshold = danger_levels.get(min_danger, 2)
    return [name for name, data in BIOME_DATABASE.items() if danger_levels.get(data.get('danger_level', 'low'), 0) >= threshold]

def get_structure_locations(structure_name: str) -> list:
    """Get biomes where a structure spawns"""
    structure = STRUCTURE_DATABASE.get(structure_name, {})
    return structure.get('biomes', [])

def get_best_biomes_for_resource(resource: str) -> list:
    """Get best biomes to find a specific resource"""
    biomes = []
    for biome_name, biome_data in BIOME_DATABASE.items():
        if resource in biome_data.get('resources', []):
            biomes.append(biome_name)
    return biomes

if __name__ == '__main__':
    # Test biome knowledge
    print("=== BIOME KNOWLEDGE ===")
    print(f"Total biomes: {len(BIOME_DATABASE)}")
    print(f"Total structures: {len(STRUCTURE_DATABASE)}")

    print("\n=== Safe Biomes ===")
    for biome in get_safe_biomes():
        print(f"- {biome}")

    print("\n=== Desert Pyramid Location ===")
    print(get_structure_locations('desert_pyramid'))

    print("\n=== Best for Emerald Mining ===")
    print(get_best_biomes_for_resource('emerald_ore'))
