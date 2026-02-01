"""
Complete Minecraft Potion Knowledge
All potions, brewing recipes, status effects
"""

POTION_DATABASE = {
    # ============================================================
    # POSITIVE EFFECTS
    # ============================================================

    'regeneration': {
        'type': 'positive',
        'potion_name': 'Potion of Regeneration',
        'duration': {
            'base': 900,  # 45 seconds
            'extended': 1800,  # 90 seconds
            'splash': 900,  # 45 seconds
            'lingering': 450  # 22.5 seconds cloud
        },
        'amplifier': {
            'I': 'heal 0.5 hearts every 2.5 seconds',
            'II': 'heal 1 heart every 1.25 seconds'
        },
        'description': 'Restores health over time',
        'brewing_recipe': {
            'base': 'ghast_tear + awkward_potion',
            'extended': 'redstone',
            'upgraded': 'glowstone_dust'
        },
        'item_variant': 'golden_apple',
        'mob_uses': ['zombie_villager_cure'],
        'color': 'pink',
        'particles': 'pink'
    },
    'speed': {
        'type': 'positive',
        'potion_name': 'Potion of Swiftness',
        'duration': {
            'base': 1800,  # 3 minutes
            'extended': 4800,  # 8 minutes
            'splash': 1800,
            'lingering': 900
        },
        'amplifier': {
            'I': '+20% movement speed',
            'II': '+40% movement speed'
        },
        'description': 'Increases movement and mining speed',
        'brewing_recipe': {
            'base': 'sugar + awkward_potion',
            'extended': 'redstone',
            'upgraded': 'glowstone_dust'
        },
        'beacon_effect': True,
        'color': 'blue',
        'particles': 'blue'
    },
    'fire_resistance': {
        'type': 'positive',
        'potion_name': 'Potion of Fire Resistance',
        'duration': {
            'base': 1800,  # 3 minutes
            'extended': 4800,  # 8 minutes
            'splash': 1800,
            'lingering': 900
        },
        'amplifier': {
            'I': 'immune to fire, lava, and blaze fireballs'
        },
        'description': 'Grants immunity to fire and lava damage',
        'brewing_recipe': {
            'base': 'magma_cream + awkward_potion',
            'extended': 'redstone',
            'upgraded': None  # Cannot be upgraded
        },
        'beacon_effect': True,
        'color': 'orange',
        'particles': 'orange',
        'mob_immune': ['nether_mob', 'blaze']
    },
    'poison': {
        'type': 'negative',
        'potion_name': 'Potion of Poison',
        'duration': {
            'base': 900,  # 45 seconds
            'extended': 1800,  # 90 seconds
            'splash': 900,
            'lingering': 450
        },
        'amplifier': {
            'I': '0.5 hearts damage every 1.25 seconds, total 36 hearts',
            'II': '1 heart damage every 1.25 seconds, total 72 hearts'
        },
        'description': 'Inflicts poison damage over time (cannot kill)',
        'brewing_recipe': {
            'base': 'spider_eye + awkward_potion',
            'extended': 'redstone',
            'upgraded': 'glowstone_dust'
        },
        'color': 'green',
        'particles': 'green',
        'sources': ['cave_spider', 'pufferfish', 'witch']
    },
    'healing': {
        'type': 'positive',
        'potion_name': 'Potion of Healing',
        'duration': {
            'base': 'instant',
            'splash': 'instant',
            'lingering': 'instant_cloud'
        },
        'amplifier': {
            'I': 'heal 4 hearts',
            'II': 'heal 8 hearts'
        },
        'description': 'Instantly restores health',
        'brewing_recipe': {
            'base': 'glistering_melon_slice + awkward_potion',
            'extended': None,  # Cannot be extended
            'upgraded': 'glowstone_dust'
        },
        'beacon_effect': 'regeneration',
        'hurts_undead': True,
        'color': 'red',
        'particles': 'red'
    },
    'night_vision': {
        'type': 'positive',
        'potion_name': 'Potion of Night Vision',
        'duration': {
            'base': 3600,  # 3 minutes
            'extended': 9600,  # 8 minutes
            'splash': 3600,
            'lingering': 1800
        },
        'amplifier': {
            'I': 'see in darkness as if it were day'
        },
        'description': 'Grants ability to see in the dark',
        'brewing_recipe': {
            'base': 'golden_carrot + awkward_potion',
            'extended': 'redstone',
            'upgraded': None  # Cannot be upgraded
        },
        'beacon_effect': False,
        'color': 'blue',
        'particles': 'blue',
        'special': 'can see underwater clearly'
    },
    'strength': {
        'type': 'positive',
        'potion_name': 'Potion of Strength',
        'duration': {
            'base': 1800,  # 3 minutes
            'extended': 4800,  # 8 minutes
            'splash': 1800,
            'lingering': 900
        },
        'amplifier': {
            'I': '+130% melee damage (3 hearts × 1.3 = 4 hearts)',
            'II': '+260% melee damage (3 hearts × 2.6 = 8 hearts)'
        },
        'description': 'Increases melee damage dealt',
        'brewing_recipe': {
            'base': 'blaze_powder + awkward_potion',
            'extended': 'redstone',
            'upgraded': 'glowstone_dust'
        },
        'beacon_effect': True,
        'color': 'red',
        'particles': 'red'
    },
    'leaping': {
        'type': 'positive',
        'potion_name': 'Potion of Leaping',
        'duration': {
            'base': 1800,  # 3 minutes
            'extended': 4800,  # 8 minutes
            'splash': 1800,
            'lingering': 900
        },
        'amplifier': {
            'I': '+0.5 block jump height',
            'II': '+1 block jump height, reduced fall damage'
        },
        'description': 'Increases jump height and reduces fall damage',
        'brewing_recipe': {
            'base': 'rabbit_foot + awkward_potion',
            'extended': 'redstone',
            'upgraded': 'glowstone_dust'
        },
        'color': 'green',
        'particles': 'green'
    },
    'water_breathing': {
        'type': 'positive',
        'potion_name': 'Potion of Water Breathing',
        'duration': {
            'base': 3600,  # 3 minutes
            'extended': 9600,  # 8 minutes
            'splash': 3600,
            'lingering': 1800
        },
        'amplifier': {
            'I': 'cannot drown'
        },
        'description': 'Grants ability to breathe underwater',
        'brewing_recipe': {
            'base': 'pufferfish + awkward_potion',
            'extended': 'redstone',
            'upgraded': None  # Cannot be upgraded
        },
        'beacon_effect': False,
        'color': 'aquamarine',
        'particles': 'aquamarine',
        'conduit_effect': True
    },
    'invisibility': {
        'type': 'positive',
        'potion_name': 'Potion of Invisibility',
        'duration': {
            'base': 1800,  # 3 minutes
            'extended': 4800,  # 8 minutes
            'splash': 1800,
            'lingering': 900
        },
        'amplifier': {
            'I': 'invisible to mobs and players'
        },
        'description': 'Makes player invisible (except armor held items)',
        'brewing_recipe': {
            'base': 'fermented_spider_eye + potion_of_night_vision',
            'extended': 'redstone',
            'upgraded': None
        },
        'beacon_effect': False,
        'color': 'light_gray',
        'particles': 'none',
        'limitations': ['armor_visible', 'held_items_visible', 'particles_seen', 'mob_detection_range']
    },
    'slow_falling': {
        'type': 'positive',
        'potion_name': 'Potion of Slow Falling',
        'duration': {
            'base': 1800,  # 3 minutes
            'extended': 4800,  # 8 minutes
            'splash': 1800,
            'lingering': 900
        },
        'amplifier': {
            'I': 'no fall damage, slow descent'
        },
        'description': 'Eliminates fall damage and slows falling',
        'brewing_recipe': {
            'base': 'phantom_membrane + awkward_potion',
            'extended': 'redstone',
            'upgraded': None
        },
        'beacon_effect': False,
        'color': 'white',
        'particles': 'white',
        'special': 'useful for elytra flying, building tall structures'
    },
    'luck': {
        'type': 'positive',
        'potion_name': 'Potion of Luck',
        'duration': {
            'base': 3600,  # 5 minutes
            'extended': None,
            'splash': 3600,
            'lingering': 1800
        },
        'amplifier': {
            'I': 'better loot from fishing and chests'
        },
        'description': 'Increases luck with fishing and loot',
        'brewing_recipe': {
            'base': 'no_recipe',  # Only available via commands
            'note': 'Cannot be brewed in survival'
        },
        'beacon_effect': False,
        'color': 'aquamarine',
        'particles': 'aquamarine'
    },

    # ============================================================
    # NEGATIVE EFFECTS
    # ============================================================

    'slowness': {
        'type': 'negative',
        'potion_name': 'Potion of Slowness',
        'duration': {
            'base': 900,  # 45 seconds
            'extended': 2400,  # 2 minutes
            'splash': 900,
            'lingering': 450
        },
        'amplifier': {
            'I': '-15% movement speed',
            'II': '-30% movement speed',
            'III': '-60% movement speed',
            'IV': '-75% movement speed'
        },
        'description': 'Decreases movement and mining speed',
        'brewing_recipe': {
            'base': 'fermented_spider_eye + potion_of_fire_resistance or potion_of_swiftness',
            'extended': 'redstone',
            'upgraded': 'glowstone_dust'
        },
        'beacon_effect': False,
        'color': 'cyan',
        'particles': 'cyan',
        'sources': ['stray_arrow', 'witch']
    },
    'weakness': {
        'type': 'negative',
        'potion_name': 'Potion of Weakness',
        'duration': {
            'base': 900,  # 45 seconds
            'extended': 2400,  # 2 minutes
            'splash': 900,
            'lingering': 450
        },
        'amplifier': {
            'I': '-0.5 hearts damage (reduces attack to 0.5 hearts)'
        },
        'description': 'Reduces melee damage dealt',
        'brewing_recipe': {
            'base': 'fermented_spider_eye + water_bottle or thick_potion',
            'extended': 'redstone',
            'upgraded': None
        },
        'beacon_effect': False,
        'color': 'dark_gray',
        'particles': 'gray',
        'uses': ['cure_zombie_villager'],
        'sources': ['wither', 'wither_skeleton']
    },
    'wither': {
        'type': 'negative',
        'potion_name': 'Wither effect',
        'duration': {
            'base': 800,  # 40 seconds
            'splash': None,
            'lingering': None
        },
        'amplifier': {
            'I': '1 heart damage every 2 seconds, total 10 hearts',
            'II': '2 hearts damage every 2 seconds, total 20 hearts'
        },
        'description': 'Withers away health (can kill)',
        'brewing_recipe': {
            'base': 'no_recipe',  # Only from wither skulls and wither
            'note': 'Cannot be brewed'
        },
        'beacon_effect': False,
        'color': 'dark_brown',
        'particles': 'dark_brown',
        'sources': ['wither', 'wither_skeleton_skull', 'wither_rose'],
        'special': 'turns hearts black, can kill unlike poison'
    },
    'harming': {
        'type': 'negative',
        'potion_name': 'Potion of Harming',
        'duration': {
            'base': 'instant',
            'splash': 'instant',
            'lingering': 'instant_cloud'
        },
        'amplifier': {
            'I': '6 hearts damage',
            'II': '12 hearts damage'
        },
        'description': 'Instantly inflicts damage',
        'brewing_recipe': {
            'base': 'fermented_spider_eye + potion_of_healing',
            'extended': None,
            'upgraded': 'glowstone_dust'
        },
        'heals_undead': True,
        'color': 'red',
        'particles': 'red'
    },
    'nausea': {
        'type': 'negative',
        'potion_name': 'Nausea effect',
        'duration': {
            'base': 900,  # 45 seconds
            'extended': None,
            'splash': None,
            'lingering': None
        },
        'amplifier': {
            'I': 'warping screen effect'
        },
        'description': 'Warps and distorts the screen',
        'brewing_recipe': {
            'base': 'no_recipe',  # Only from pufferfish
            'note': 'Cannot be brewed'
        },
        'beacon_effect': False,
        'particles': 'purple',
        'sources': ['pufferfish', 'nether_portal']
    },
    'blindness': {
        'type': 'negative',
        'potion_name': 'Blindness effect',
        'duration': {
            'base': 900,  # 45 seconds
            'extended': None,
            'splash': None,
            'lingering': None
        },
        'amplifier': {
            'I': 'darkens screen, prevents sprinting and critical hits'
        },
        'description': 'Impairs vision and prevents critical hits',
        'brewing_recipe': {
            'base': 'no_recipe',
            'note': 'Cannot be brewed'
        },
        'beacon_effect': False,
        'particles': 'thick_black',
        'sources': ['guardian_elder', 'illusioner']
    },
    'hunger': {
        'type': 'negative',
        'potion_name': 'Hunger effect',
        'duration': {
            'base': 900,  # 45 seconds
            'extended': None,
            'splash': None,
            'lingering': None
        },
        'amplifier': {
            'I': 'drains hunger faster',
            'II': 'drains hunger very fast'
        },
        'description': 'Increases hunger depletion rate',
        'brewing_recipe': {
            'base': 'no_recipe',
            'note': 'Cannot be brewed'
        },
        'beacon_effect': False,
        'particles': 'orange',
        'sources': ['raw_chicken', 'rotten_flesh', 'husk', 'pufferfish']
    },
    'bad_omen': {
        'type': 'negative',
        'potion_name': 'Bad Omen',
        'duration': {
            'base': 600000,  # Until raid completes
            'extended': None,
            'splash': None,
            'lingering': None
        },
        'amplifier': {
            'I': 'triggers normal raid',
            'II': 'triggers large raid (+1 wave)',
            'III': 'triggers larger raid (+2 waves)',
            'IV': 'triggers massive raid (+3 waves)',
            'V': 'triggers huge raid (+4 waves)'
        },
        'description': 'Triggers raid when entering village',
        'brewing_recipe': {
            'base': 'no_recipe',
            'note': 'Only from killing patrol captain'
        },
        'beacon_effect': False,
        'particles': 'gray',
        'sources': ['pillager_captain_ominous_banner']
    },
    'hero_of_the_village': {
        'type': 'positive',
        'potion_name': 'Hero of the Village',
        'duration': {
            'base': 48000,  # 40 minutes
        },
        'amplifier': {
            'I': 'villager discounts + gifts'
        },
        'description': 'Grants discounts and gifts from villagers',
        'brewing_recipe': {
            'base': 'no_recipe',
            'note': 'Only from defeating raid'
        },
        'beacon_effect': False,
        'particles': 'green',
        'benefits': ['trading_discounts', 'villager_gifts', 'farming_bonus']
    },
    'glowing': {
        'type': 'neutral',
        'potion_name': 'Glowing effect',
        'duration': {
            'base': 800,  # 40 seconds
            'extended': None,
            'splash': None,
            'lingering': None
        },
        'amplifier': {
            'I': 'outline visible through blocks'
        },
        'description': 'Creates outline visible through blocks',
        'brewing_recipe': {
            'base': 'no_recipe',
            'note': 'Only from spectral arrows'
        },
        'beacon_effect': False,
        'particles': 'none',
        'sources': ['spectral_arrow']
    },
    'levitation': {
        'type': 'mixed',
        'potion_name': 'Levitation effect',
        'duration': {
            'base': 800,  # 40 seconds
            'extended': None,
            'splash': None,
            'lingering': None
        },
        'amplifier': {
            'I': 'float upward 0.9 blocks/sec',
            'I': 'float upward 1.8 blocks/sec',
            'XXX': 'float upward extremely fast (shulker bullet)'
        },
        'description': 'Causes player to float upward',
        'brewing_recipe': {
            'base': 'no_recipe',
            'note': 'Only from shulker bullets'
        },
        'beacon_effect': False,
        'particles': 'white',
        'sources': ['shulker'],
        'special': 'can be used to reach end cities'
    },
    'dolphins_grace': {
        'type': 'positive',
        'potion_name': "Dolphin's Grace",
        'duration': {
            'base': 'while_near_dolphin'
        },
        'amplifier': {
            'I': 'increased swimming speed, faster underwater mining'
        },
        'description': 'Grants faster underwater movement and mining',
        'brewing_recipe': {
            'base': 'no_recipe',
            'note': 'Only from dolphins'
        },
        'beacon_effect': False,
        'particles': 'none',
        'sources': ['dolphin', 'dolphin_gratitude']
    },
    'conduit_power': {
        'type': 'positive',
        'potion_name': 'Conduit Power',
        'duration': {
            'base': 'while_in_range'
        },
        'amplifier': {
            'I': 'underwater speed + night vision',
            'II': 'underwater speed + night vision + strength'
        },
        'description': 'Grants underwater powers when near conduit',
        'brewing_recipe': {
            'base': 'no_recipe',
            'note': 'Only from fully powered conduit'
        },
        'beacon_effect': False,
        'particles': 'blue',
        'special': 'requires 16 nautilus shells, range 32 blocks'
    },
}

# Brewing recipes
BREWING_RECIPES = {
    # Base potions
    'water_bottle': {'input': 'glass_bottle', 'output': 'water_bottle', 'type': 'fill'},
    'awkward_potion': {'input': 'nether_wart', 'base': 'water_bottle', 'output': 'awkward_potion'},
    'thick_potion': {'input': 'glowstone_dust', 'base': 'water_bottle', 'output': 'thick_potion'},
    'mundane_potion': {'input': 'redstone', 'base': 'water_bottle', 'output': 'mundane_potion'},

    # Effect potions
    'regeneration': {'input': 'ghast_tear', 'base': 'awkward_potion', 'output': 'potion_of_regeneration'},
    'swiftness': {'input': 'sugar', 'base': 'awkward_potion', 'output': 'potion_of_swiftness'},
    'fire_resistance': {'input': 'magma_cream', 'base': 'awkward_potion', 'output': 'potion_of_fire_resistance'},
    'poison': {'input': 'spider_eye', 'base': 'awkward_potion', 'output': 'potion_of_poison'},
    'healing': {'input': 'glistering_melon_slice', 'base': 'awkward_potion', 'output': 'potion_of_healing'},
    'night_vision': {'input': 'golden_carrot', 'base': 'awkward_potion', 'output': 'potion_of_night_vision'},
    'strength': {'input': 'blaze_powder', 'base': 'awkward_potion', 'output': 'potion_of_strength'},
    'slowness': {'input': 'fermented_spider_eye', 'base': 'potion_of_fire_resistance', 'output': 'potion_of_slowness'},
    'leaping': {'input': 'rabbit_foot', 'base': 'awkward_potion', 'output': 'potion_of_leaping'},
    'water_breathing': {'input': 'pufferfish', 'base': 'awkward_potion', 'output': 'potion_of_water_breathing'},
    'invisibility': {'input': 'fermented_spider_eye', 'base': 'potion_of_night_vision', 'output': 'potion_of_invisibility'},
    'slow_falling': {'input': 'phantom_membrane', 'base': 'awkward_potion', 'output': 'potion_of_slow_falling'},
    'weakness': {'input': 'fermented_spider_eye', 'base': 'water_bottle', 'output': 'potion_of_weakness'},
    'harming': {'input': 'fermented_spider_eye', 'base': 'potion_of_healing', 'output': 'potion_of_harming'},

    # Modifiers
    'splash_potion': {'input': 'gunpowder', 'applies_to': 'any_potion', 'output': 'splash_potion'},
    'lingering_potion': {'input': 'dragon_breath', 'applies_to': 'splash_potion', 'output': 'lingering_potion'},
    'extended_duration': {'input': 'redstone', 'applies_to': 'most_potions', 'effect': 'extends_duration'},
    'upgraded_tier': {'input': 'glowstone_dust', 'applies_to': 'most_potions', 'effect': 'upgrades_tier'},
}

# Brewing ingredients
BREWING_INGREDIENTS = {
    'nether_wart': {'purpose': 'awkward_potion_base', 'found_in': 'nether_fortress'},
    'ghast_tear': {'purpose': 'regeneration', 'found_in': 'ghast_drop', 'rarity': 'uncommon'},
    'sugar': {'purpose': 'swiftness', 'found_in': 'sugar_cane', 'rarity': 'common'},
    'magma_cream': {'purpose': 'fire_resistance', 'found_in': 'magma_cube_drop', 'rarity': 'common'},
    'spider_eye': {'purpose': 'poison', 'found_in': 'spider_drop', 'rarity': 'common'},
    'glistering_melon_slice': {'purpose': 'healing', 'found_in': 'crafting', 'rarity': 'medium'},
    'golden_carrot': {'purpose': 'night_vision', 'found_in': 'crafting', 'rarity': 'medium'},
    'blaze_powder': {'purpose': 'strength', 'found_in': 'blaze_drop', 'rarity': 'common'},
    'fermented_spider_eye': {'purpose': 'weakness/potion_inversion', 'found_in': 'crafting', 'rarity': 'medium'},
    'rabbit_foot': {'purpose': 'leaping', 'found_in': 'rabbit_drop', 'rarity': 'rare'},
    'pufferfish': {'purpose': 'water_breathing', 'found_in': 'fishing', 'rarity': 'uncommon'},
    'phantom_membrane': {'purpose': 'slow_falling', 'found_in': 'phantom_drop', 'rarity': 'uncommon'},
    'turtle_helmet': {'purpose': 'master_potion_base', 'found_in': 'turtle_drop', 'rarity': 'rare'},
    'redstone': {'purpose': 'extend_duration', 'found_in': 'mining', 'rarity': 'common'},
    'glowstone_dust': {'purpose': 'upgrade_tier', 'found_in': 'mining', 'rarity': 'common'},
    'gunpowder': {'purpose': 'splash_potion', 'found_in': 'creeper_drop', 'rarity': 'common'},
    'dragon_breath': {'purpose': 'lingering_potion', 'found_in': 'ender_dragon', 'rarity': 'once_per_game'},
}


def get_potion_info(effect_name: str) -> dict:
    """Get complete information about a potion effect"""
    return POTION_DATABASE.get(effect_name, {})


def get_all_positive_effects() -> list:
    """Get all positive potion effects"""
    return [name for name, data in POTION_DATABASE.items() if data.get('type') == 'positive']


def get_all_negative_effects() -> list:
    """Get all negative potion effects"""
    return [name for name, data in POTION_DATABASE.items() if data.get('type') == 'negative']


def get_potion_duration(effect_name: str, variant: str = 'base') -> int:
    """Get potion duration in ticks"""
    effect = POTION_DATABASE.get(effect_name, {})
    durations = effect.get('duration', {})
    return durations.get(variant, 0)


def get_potion_brewing_recipe(effect_name: str) -> dict:
    """Get brewing recipe for a potion"""
    effect = POTION_DATABASE.get(effect_name, {})
    return effect.get('brewing_recipe', {})


def get_potion_description(effect_name: str) -> str:
    """Get potion description"""
    effect = POTION_DATABASE.get(effect_name, {})
    return effect.get('description', 'No description available')


def is_potion_brewable(effect_name: str) -> bool:
    """Check if a potion can be brewed in survival"""
    recipe = get_potion_brewing_recipe(effect_name)
    if not recipe:
        return False
    return recipe.get('base') != 'no_recipe'


def get_potion_effect_level(effect_name: str, level: int = 1) -> str:
    """Get effect description at specific level"""
    effect = POTION_DATABASE.get(effect_name, {})
    amplifiers = effect.get('amplifier', {})
    level_key = f'I' * level if level <= 3 else 'I'  # I, II, III or just I
    return amplifiers.get(level_key, amplifiers.get('I', 'Unknown'))


def get_best_combat_potions() -> list:
    """Get recommended potions for combat"""
    return [
        ('strength', 'II', 'splash'),
        ('healing', 'II', 'splash'),
        ('speed', 'II', 'normal'),
        ('fire_resistance', 'I', 'extended')
    ]


def get_best_exploration_potions() -> list:
    """Get recommended potions for exploration"""
    return [
        ('night_vision', 'I', 'extended'),
        ('speed', 'I', 'extended'),
        ('fire_resistance', 'I', 'extended'),
        ('water_breathing', 'I', 'extended')
    ]


def get_best_boss_fight_potions() -> list:
    """Get recommended potions for boss fights"""
    return [
        ('strength', 'II', 'normal'),
        ('healing', 'II', 'splash'),
        ('speed', 'II', 'splash'),
        ('regeneration', 'II', 'normal'),
        ('slow_falling', 'I', 'extended'),
        ('fire_resistance', 'I', 'extended')
    ]


def get_potion_ingredients(effect_name: str) -> list:
    """Get ingredients needed to brew a potion"""
    recipe = get_potion_brewing_recipe(effect_name)
    ingredients = []

    # Base ingredient
    base = recipe.get('base')
    if base == 'awkward_potion':
        ingredients.append('nether_wart')
    elif base == 'water_bottle':
        ingredients.append('water_bottle')

    # Effect ingredient
    effect_ingredient = recipe.get('base')
    if effect_ingredient and effect_ingredient != 'water_bottle':
        for name, data in BREWING_INGREDIENTS.items():
            if data.get('purpose') == effect_ingredient:
                ingredients.append(name)
                break

    # Modifiers
    if recipe.get('extended'):
        ingredients.append('redstone')
    if recipe.get('upgraded'):
        ingredients.append('glowstone_dust')

    return ingredients


def get_potion_color(effect_name: str) -> str:
    """Get potion color for rendering"""
    effect = POTION_DATABASE.get(effect_name, {})
    return effect.get('color', 'unknown')


if __name__ == '__main__':
    # Test potion knowledge
    print("=== POTION KNOWLEDGE ===")
    print(f"Total effects: {len(POTION_DATABASE)}")

    print("\n=== Positive Effects ===")
    for effect in get_all_positive_effects():
        info = get_potion_info(effect)
        print(f"{effect}: {info.get('description', 'No description')}")

    print("\n=== Combat Potions ===")
    for potion, level, variant in get_best_combat_potions():
        print(f"{potion} {level} ({variant})")

    print("\n=== Brewing Ingredients ===")
    for ingredient, data in BREWING_INGREDIENTS.items():
        print(f"{ingredient}: {data['purpose']} - {data['rarity']}")
