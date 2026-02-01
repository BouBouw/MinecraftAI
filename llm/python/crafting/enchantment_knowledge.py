"""
Complete Minecraft Enchantment Knowledge
All enchantments, their effects, levels, and compatibility
"""

ENCHANTMENT_DATABASE = {
    # ============================================================
    # SWORD ENCHANTMENTS
    # ============================================================

    'sharpness': {
        'category': 'combat',
        'applicable_to': ['sword', 'axe'],
        'max_level': 5,
        'weight': 10,
        'description': 'Increases melee damage',
        'effect_per_level': {
            1: '+0.5 hearts damage',
            2: '+1 heart damage',
            3: '+1.5 hearts damage',
            4: '+2 hearts damage',
            5: '+2.5 hearts damage'
        },
        'incompatible_with': ['smite', 'bane_of_arthropods'],
        'treasure': False,
        'curse': False
    },
    'smite': {
        'category': 'combat',
        'applicable_to': ['sword', 'axe'],
        'max_level': 5,
        'weight': 5,
        'description': 'Increases damage to undead mobs',
        'affects': ['zombie', 'zombie_villager', 'husk', 'drowned', 'skeleton', 'stray', 'wither_skeleton', 'phantom', 'with'],
        'effect_per_level': {
            1: '+2.5 hearts damage to undead',
            2: '+3 hearts damage to undead',
            3: '+3.5 hearts damage to undead',
            4: '+4 hearts damage to undead',
            5: '+4.5 hearts damage to undead'
        },
        'incompatible_with': ['sharpness', 'bane_of_arthropods'],
        'treasure': False,
        'curse': False
    },
    'bane_of_arthropods': {
        'category': 'combat',
        'applicable_to': ['sword', 'axe'],
        'max_level': 5,
        'weight': 5,
        'description': 'Increases damage and slows arthropods',
        'affects': ['spider', 'cave_spider', 'silverfish', 'bee', 'endermite'],
        'effect_per_level': {
            1: '+2.5 hearts damage + slowness I',
            2: '+3 hearts damage + slowness I',
            3: '+3.5 hearts damage + slowness II',
            4: '+4 hearts damage + slowness II',
            5: '+4.5 hearts damage + slowness III'
        },
        'incompatible_with': ['sharpness', 'smite'],
        'treasure': False,
        'curse': False
    },
    'fire_aspect': {
        'category': 'combat',
        'applicable_to': ['sword'],
        'max_level': 2,
        'weight': 2,
        'description': 'Sets target on fire',
        'effect_per_level': {
            1: 'Burn for 4 seconds',
            2: 'Burn for 8 seconds'
        },
        'incompatible_with': [],
        'treasure': False,
        'curse': False
    },
    'looting': {
        'category': 'combat',
        'applicable_to': ['sword'],
        'max_level': 3,
        'weight': 2,
        'description': 'Increases mob drops',
        'effect_per_level': {
            1: '+1 drop per level',
            2: '+2 drops per level',
            3: '+3 drops per level'
        },
        'special': 'Rare drops more common',
        'incompatible_with': [],
        'treasure': False,
        'curse': False
    },
    'sweeping_edge': {
        'category': 'combat',
        'applicable_to': ['sword'],
        'max_level': 3,
        'weight': 2,
        'description': 'Increases sweep attack damage',
        'effect_per_level': {
            1: '+50% sweep damage',
            2: '+67% sweep damage',
            3: '+75% sweep damage'
        },
        'incompatible_with': [],
        'treasure': False,
        'curse': False
    },
    'knockback': {
        'category': 'combat',
        'applicable_to': ['sword'],
        'max_level': 2,
        'weight': 5,
        'description': 'Increases knockback distance',
        'effect_per_level': {
            1: '+3 blocks knockback',
            2: '+6 blocks knockback'
        },
        'incompatible_with': [],
        'treasure': False,
        'curse': False
    },

    # ============================================================
    # TOOL ENCHANTMENTS
    # ============================================================

    'efficiency': {
        'category': 'tool',
        'applicable_to': ['pickaxe', 'axe', 'shovel', 'hoe'],
        'max_level': 5,
        'weight': 10,
        'description': 'Increases mining speed',
        'effect_per_level': {
            1: 'Mining speed ×2',
            2: 'Mining speed ×4',
            3: 'Mining speed ×6',
            4: 'Mining speed ×8',
            5: 'Mining speed ×10'
        },
        'incompatible_with': [],
        'treasure': False,
        'curse': False
    },
    'fortune': {
        'category': 'tool',
        'applicable_to': ['pickaxe', 'axe', 'shovel'],
        'max_level': 3,
        'weight': 2,
        'description': 'Increases block drops',
        'effect_per_level': {
            1: '33% chance for +1 drop',
            2: '25% chance for +1, 25% for +2',
            3: '20% chance for +1, 20% for +2, 20% for +3'
        },
        'incompatible_with': ['silk_touch'],
        'treasure': False,
        'curse': False,
        'affects': ['coal_ore', 'diamond_ore', 'emerald_ore', 'iron_ore', 'gold_ore', 'lapis_ore', 'redstone_ore', 'nether_quartz_ore']
    },
    'silk_touch': {
        'category': 'tool',
        'applicable_to': ['pickaxe', 'axe', 'shovel', 'hoe'],
        'max_level': 1,
        'weight': 1,
        'description': 'Mines blocks as themselves',
        'effect': 'Drops block itself instead of resources',
        'special_blocks': ['ice', 'glass', 'stone', 'coal_ore', 'diamond_ore', 'emerald_ore', 'redstone_ore', 'glowstone', 'grass_block', 'mycelium', 'podzol'],
        'incompatible_with': ['fortune'],
        'treasure': False,
        'curse': False
    },
    'unbreaking': {
        'category': 'durability',
        'applicable_to': ['sword', 'pickaxe', 'axe', 'shovel', 'hoe', 'helmet', 'chestplate', 'leggings', 'boots', 'bow', 'crossbow', 'fishing_rod', 'shears', 'flint_and_steel', 'elytra', 'trident', 'shield'],
        'max_level': 3,
        'weight': 5,
        'description': 'Decreases durability loss chance',
        'effect_per_level': {
            1: '50% chance to not lose durability',
            2: '67% chance to not lose durability',
            3: '75% chance to not lose durability'
        },
        'incompatible_with': [],
        'treasure': False,
        'curse': False
    },
    'mending': {
        'category': 'durability',
        'applicable_to': ['sword', 'pickaxe', 'axe', 'shovel', 'hoe', 'helmet', 'chestplate', 'leggings', 'boots', 'bow', 'crossbow', 'fishing_rod', 'shears', 'flint_and_steel', 'elytra', 'trident', 'shield'],
        'max_level': 1,
        'weight': 2,
        'description': 'Repairs item using XP',
        'effect': 'XP collected repairs durability (2 durability per 1 XP)',
        'incompatible_with': ['infinity'],
        'treasure': True,
        'curse': False
    },

    # ============================================================
    # ARMOR ENCHANTMENTS
    # ============================================================

    'protection': {
        'category': 'armor',
        'applicable_to': ['helmet', 'chestplate', 'leggings', 'boots'],
        'max_level': 4,
        'weight': 10,
        'description': 'Reduces damage taken',
        'effect_per_level': {
            1: '4% damage reduction',
            2: '8% damage reduction',
            3: '12% damage reduction',
            4: '16% damage reduction'
        },
        'works_on': ['all_damage_except'],
        'excepts': ['void', 'hunger', 'fall'],
        'incompatible_with': ['blast_protection', 'fire_protection', 'projectile_protection'],
        'treasure': False,
        'curse': False
    },
    'blast_protection': {
        'category': 'armor',
        'applicable_to': ['helmet', 'chestplate', 'leggings', 'boots'],
        'max_level': 4,
        'weight': 2,
        'description': 'Reduces explosion damage',
        'effect_per_level': {
            1: '8% explosion reduction + knockback reduction',
            2: '16% explosion reduction + knockback reduction',
            3: '24% explosion reduction + knockback reduction',
            4: '32% explosion reduction + knockback reduction'
        },
        'incompatible_with': ['protection', 'fire_protection', 'projectile_protection'],
        'treasure': False,
        'curse': False
    },
    'fire_protection': {
        'category': 'armor',
        'applicable_to': ['helmet', 'chestplate', 'leggings', 'boots'],
        'max_level': 4,
        'weight': 5,
        'description': 'Reduces fire damage and burn time',
        'effect_per_level': {
            1: '8% fire reduction + 15% less burn time',
            2: '16% fire reduction + 30% less burn time',
            3: '24% fire reduction + 45% less burn time',
            4: '32% fire reduction + 60% less burn time'
        },
        'incompatible_with': ['protection', 'blast_protection', 'projectile_protection'],
        'treasure': False,
        'curse': False
    },
    'projectile_protection': {
        'category': 'armor',
        'applicable_to': ['helmet', 'chestplate', 'leggings', 'boots'],
        'max_level': 4,
        'weight': 5,
        'description': 'Reduces projectile damage',
        'effect_per_level': {
            1: '8% projectile reduction + knockback reduction',
            2: '16% projectile reduction + knockback reduction',
            3: '24% projectile reduction + knockback reduction',
            4: '32% projectile reduction + knockback reduction'
        },
        'works_on': ['arrows', 'ghast_fireballs', 'blaze_fireballs', 'llama_spit'],
        'incompatible_with': ['protection', 'blast_protection', 'fire_protection'],
        'treasure': False,
        'curse': False
    },
    'feather_falling': {
        'category': 'armor',
        'applicable_to': ['boots'],
        'max_level': 4,
        'weight': 5,
        'description': 'Reduces fall damage',
        'effect_per_level': {
            1: '12% fall damage reduction',
            2: '24% fall damage reduction',
            3: '36% fall damage reduction',
            4: '48% fall damage reduction'
        },
        'incompatible_with': [],
        'treasure': False,
        'curse': False
    },
    'thorns': {
        'category': 'armor',
        'applicable_to': ['helmet', 'chestplate', 'leggings', 'boots'],
        'max_level': 3,
        'weight': 1,
        'description': 'Damages attacker',
        'effect_per_level': {
            1: '15% chance to deal 1-2 hearts damage',
            2: '30% chance to deal 1-3 hearts damage',
            3: '45% chance to deal 1-4 hearts damage'
        },
        'durability_cost': '2-3 durability per hit',
        'incompatible_with': [],
        'treasure': False,
        'curse': False
    },
    'respiration': {
        'category': 'armor',
        'applicable_to': ['helmet'],
        'max_level': 3,
        'weight': 2,
        'description': 'Extends underwater breathing time',
        'effect_per_level': {
            1: '+15 seconds underwater',
            2: '+30 seconds underwater',
            3: '+45 seconds underwater'
        },
        'special': 'Chance to not drown at all',
        'incompatible_with': [],
        'treasure': False,
        'curse': False
    },
    'depth_strider': {
        'category': 'armor',
        'applicable_to': ['boots'],
        'max_level': 3,
        'weight': 2,
        'description': 'Increases underwater movement speed',
        'effect_per_level': {
            1: 'Underwater speed ×1.7',
            2: 'Underwater speed ×2.6',
            3: 'Underwater speed ×3.4 (normal land speed)'
        },
        'incompatible_with': ['frost_walker'],
        'treasure': False,
        'curse': False
    },
    'frost_walker': {
        'category': 'armor',
        'applicable_to': ['boots'],
        'max_level': 2,
        'weight': 2,
        'description': 'Turns water to frosted ice',
        'effect_per_level': {
            1: 'Freezes water in 2-block radius',
            2: 'Freezes water in 3-block radius'
        },
        'special': 'Creates temporary ice path on water',
        'incompatible_with': ['depth_strider'],
        'treasure': True,
        'curse': False
    },
    'aqua_affinity': {
        'category': 'armor',
        'applicable_to': ['helmet'],
        'max_level': 1,
        'weight': 2,
        'description': 'Increases underwater mining speed',
        'effect': 'Mine underwater at normal speed',
        'incompatible_with': [],
        'treasure': False,
        'curse': False
    },
    'soul_speed': {
        'category': 'armor',
        'applicable_to': ['boots'],
        'max_level': 3,
        'weight': 1,
        'description': 'Increases movement on soul sand/soul soil',
        'effect_per_level': {
            1: '+42% speed on soul blocks',
            2: '+84% speed on soul blocks',
            3: '+126% speed on soul blocks'
        },
        'special': 'Damages boots (4 durability per block)',
        'incompatible_with': [],
        'treasure': True,
        'curse': False
    },
    'swift_sneak': {
        'category': 'armor',
        'applicable_to': ['leggings'],
        'max_level': 3,
        'weight': 1,
        'description': 'Increases sneak speed',
        'effect_per_level': {
            1: '+50% sneak speed',
            2: '+75% sneak speed',
            3: '+100% sneak speed (doubled)'
        },
        'treasure': True,
        'incompatible_with': [],
        'curse': False
    },

    # ============================================================
    # BOW ENCHANTMENTS
    # ============================================================

    'power': {
        'category': 'combat',
        'applicable_to': ['bow'],
        'max_level': 5,
        'weight': 10,
        'description': 'Increases arrow damage',
        'effect_per_level': {
            1: '+0.5 hearts damage per level',
            2: '+1 heart damage per level',
            3: '+1.5 hearts damage per level',
            4: '+2 hearts damage per level',
            5: '+2.5 hearts damage per level'
        },
        'incompatible_with': [],
        'treasure': False,
        'curse': False
    },
    'punch': {
        'category': 'combat',
        'applicable_to': ['bow'],
        'max_level': 2,
        'weight': 2,
        'description': 'Increases arrow knockback',
        'effect_per_level': {
            1: '+3 blocks knockback',
            2: '+6 blocks knockback'
        },
        'incompatible_with': [],
        'treasure': False,
        'curse': False
    },
    'flame': {
        'category': 'combat',
        'applicable_to': ['bow'],
        'max_level': 1,
        'weight': 2,
        'description': 'Arrows set targets on fire',
        'effect': 'Burns for 5 seconds',
        'special': 'Ignites TNT and campfires',
        'incompatible_with': [],
        'treasure': False,
        'curse': False
    },
    'infinity': {
        'category': 'combat',
        'applicable_to': ['bow'],
        'max_level': 1,
        'weight': 1,
        'description': 'Shooting consumes no arrows',
        'effect': 'Infinite arrows, needs at least 1 arrow in inventory',
        'incompatible_with': ['mending'],
        'treasure': False,
        'curse': False
    },

    # ============================================================
    # CROSSBOW ENCHANTMENTS
    # ============================================================

    'multishot': {
        'category': 'combat',
        'applicable_to': ['crossbow'],
        'max_level': 1,
        'weight': 2,
        'description': 'Shoots 3 arrows at once',
        'effect': 'Fires 3 arrows (only consumes 1)',
        'spread': '10 degrees',
        'incompatible_with': ['piercing'],
        'treasure': False,
        'curse': False
    },
    'piercing': {
        'category': 'combat',
        'applicable_to': ['crossbow'],
        'max_level': 4,
        'weight': 10,
        'description': 'Arrows pierce through entities',
        'effect_per_level': {
            1: 'Pierces 1 entity',
            2: 'Pierces 2 entities',
            3: 'Pierces 3 entities',
            4: 'Pierces 4 entities'
        },
        'incompatible_with': ['multishot'],
        'treasure': False,
        'curse': False
    },
    'quick_charge': {
        'category': 'combat',
        'applicable_to': ['crossbow'],
        'max_level': 3,
        'weight': 5,
        'description': 'Decreases crossbow reload time',
        'effect_per_level': {
            1: 'Reload in 1.25 seconds',
            2: 'Reload in 0.83 seconds',
            3: 'Reload in 0.42 seconds'
        },
        'incompatible_with': [],
        'treasure': False,
        'curse': False
    },

    # ============================================================
    # TRIDENT ENCHANTMENTS
    # ============================================================

    'channeling': {
        'category': 'combat',
        'applicable_to': ['trident'],
        'max_level': 1,
        'weight': 1,
        'description': 'Summons lightning during thunderstorms',
        'effect': 'Strikes target with lightning',
        'requires': 'thunderstorm',
        'incompatible_with': ['riptide'],
        'treasure': False,
        'curse': False
    },
    'riptide': {
        'category': 'combat',
        'applicable_to': ['trident'],
        'max_level': 3,
        'weight': 2,
        'description': 'Throws player with trident',
        'effect_per_level': {
            1: 'Launch velocity 2.5',
            2: 'Launch velocity 3.5',
            3: 'Launch velocity 4.5'
        },
        'requires': 'water or rain',
        'incompatible_with': ['channeling'],
        'treasure': False,
        'curse': False
    },
    'loyalty': {
        'category': 'combat',
        'applicable_to': ['trident'],
        'max_level': 3,
        'weight': 5,
        'description': 'Trident returns after throwing',
        'effect_per_level': {
            1: 'Returns in ~0.5 seconds',
            2: 'Returns in ~0.3 seconds',
            3: 'Returns instantly'
        },
        'special': 'Does not work in void or if it lands in a block',
        'incompatible_with': [],
        'treasure': False,
        'curse': False
    },
    'impaling': {
        'category': 'combat',
        'applicable_to': ['trident'],
        'max_level': 5,
        'weight': 2,
        'description': 'Increases damage to aquatic mobs',
        'effect_per_level': {
            1: '+2.5 hearts damage to aquatic',
            2: '+3 hearts damage to aquatic',
            3: '+3.5 hearts damage to aquatic',
            4: '+4 hearts damage to aquatic',
            5: '+4.5 hearts damage to aquatic'
        },
        'affects': ['drowned', 'guardian', 'elder_guardian', 'squid', 'glow_squid', 'turtle', 'fish', 'axolotl', 'tadpole'],
        'special': 'Also deals more damage in rain and water (Java only)',
        'incompatible_with': [],
        'treasure': False,
        'curse': False
    },

    # ============================================================
    # FISHING ROD ENCHANTMENTS
    # ============================================================

    'luck_of_the_sea': {
        'category': 'tool',
        'applicable_to': ['fishing_rod'],
        'max_level': 3,
        'weight': 2,
        'description': 'Increases treasure chances while fishing',
        'effect_per_level': {
            1: '+2% luck',
            2: '+4% luck',
            3: '+6% luck'
        },
        'special': 'Better loot, less junk',
        'incompatible_with': [],
        'treasure': False,
        'curse': False
    },
    'lure': {
        'category': 'tool',
        'applicable_to': ['fishing_rod'],
        'max_level': 3,
        'weight': 2,
        'description': 'Decreases fishing wait time',
        'effect_per_level': {
            1: '-7.5 seconds wait time',
            2: '-15 seconds wait time',
            3: '-22.5 seconds wait time'
        },
        'special': 'Maximum 30 seconds reduction',
        'incompatible_with': [],
        'treasure': False,
        'curse': False
    },

    # ============================================================
    # TRIDENT SPECIAL
    # ============================================================

    'channeling': {
        'category': 'trident',
        'applicable_to': ['trident'],
        'max_level': 1,
        'weight': 1,
        'description': 'Summons lightning bolt on hit during storm',
        'requires': 'thunderstorm',
        'effect': 'Instant lightning damage',
        'incompatible_with': ['riptide'],
        'treasure': False,
        'curse': False
    },

    # ============================================================
    # CURSES
    # ============================================================

    'vanishing_curse': {
        'category': 'curse',
        'applicable_to': ['all_enchantable'],
        'max_level': 1,
        'weight': 1,
        'description': 'Item vanishes on death',
        'effect': 'Item disappears instead of dropping',
        'incompatible_with': [],
        'treasure': True,
        'curse': True
    },
    'binding_curse': {
        'category': 'curse',
        'applicable_to': ['helmet', 'chestplate', 'leggings', 'boots'],
        'max_level': 1,
        'weight': 1,
        'description': 'Prevents removing armor',
        'effect': 'Armor cannot be taken off (breaks or dies to remove)',
        'incompatible_with': [],
        'treasure': True,
        'curse': True
    },

    # ============================================================
    # SHEARS
    # ============================================================

    'efficiency': {
        'category': 'tool',
        'applicable_to': ['shears'],
        'max_level': 5,
        'weight': 10,
        'description': 'Increases shearing speed',
        'incompatible_with': [],
        'treasure': False,
        'curse': False
    },
    'unbreaking': {
        'category': 'durability',
        'applicable_to': ['shears'],
        'max_level': 3,
        'weight': 5,
        'description': 'Decreases durability loss',
        'incompatible_with': [],
        'treasure': False,
        'curse': False
    },
    'mending': {
        'category': 'durability',
        'applicable_to': ['shears'],
        'max_level': 1,
        'weight': 2,
        'description': 'Repairs using XP',
        'incompatible_with': [],
        'treasure': True,
        'curse': False
    },

    # ============================================================
    # ELYTRA
    # ============================================================

    'unbreaking': {
        'category': 'durability',
        'applicable_to': ['elytra'],
        'max_level': 3,
        'weight': 5,
        'description': 'Decreases durability loss',
        'incompatible_with': [],
        'treasure': False,
        'curse': False
    },
    'mending': {
        'category': 'durability',
        'applicable_to': ['elytra'],
        'max_level': 1,
        'weight': 2,
        'description': 'Repairs using XP',
        'incompatible_with': [],
        'treasure': True,
        'curse': False
    },

    # ============================================================
    # FLINT AND STEEL
    # ============================================================

    'unbreaking': {
        'category': 'durability',
        'applicable_to': ['flint_and_steel'],
        'max_level': 3,
        'weight': 5,
        'description': 'Decreases durability loss',
        'incompatible_with': [],
        'treasure': False,
        'curse': False
    },
    'mending': {
        'category': 'durability',
        'applicable_to': ['flint_and_steel'],
        'max_level': 1,
        'weight': 2,
        'description': 'Repairs using XP',
        'incompatible_with': [],
        'treasure': True,
        'curse': False
    },

    # ============================================================
    # SHIELD
    # ============================================================

    'unbreaking': {
        'category': 'durability',
        'applicable_to': ['shield'],
        'max_level': 3,
        'weight': 5,
        'description': 'Decreases durability loss',
        'incompatible_with': [],
        'treasure': False,
        'curse': False
    },
    'mending': {
        'category': 'durability',
        'applicable_to': ['shield'],
        'max_level': 1,
        'weight': 2,
        'description': 'Repairs using XP',
        'incompatible_with': [],
        'treasure': True,
        'curse': False
    },

    # ============================================================
    # HOE
    # ============================================================

    'efficiency': {
        'category': 'tool',
        'applicable_to': ['hoe'],
        'max_level': 5,
        'weight': 10,
        'description': 'Increases farming speed',
        'incompatible_with': [],
        'treasure': False,
        'curse': False
    },
    'fortune': {
        'category': 'tool',
        'applicable_to': ['hoe'],
        'max_level': 3,
        'weight': 2,
        'description': 'Increases crop drops',
        'affects': ['potato', 'carrot', 'wheat', 'beetroot', 'pumpkin', 'melon'],
        'incompatible_with': ['silk_touch'],
        'treasure': False,
        'curse': False
    },
    'unbreaking': {
        'category': 'durability',
        'applicable_to': ['hoe'],
        'max_level': 3,
        'weight': 5,
        'description': 'Decreases durability loss',
        'incompatible_with': [],
        'treasure': False,
        'curse': False
    },
    'mending': {
        'category': 'durability',
        'applicable_to': ['hoe'],
        'max_level': 1,
        'weight': 2,
        'description': 'Repairs using XP',
        'incompatible_with': [],
        'treasure': True,
        'curse': False
    },

    # ============================================================
    # SPECIAL ENCHANTMENTS
    # ============================================================

    'silk_touch': {
        'category': 'tool',
        'applicable_to': ['hoe'],
        'max_level': 1,
        'weight': 1,
        'description': 'Harvests crops without replanting',
        'special': 'Hoes only - keeps plant when harvesting',
        'incompatible_with': ['fortune'],
        'treasure': False,
        'curse': False
    },
}

ENCHANTMENT_CATEGORIES = {
    'sword': ['sharpness', 'smite', 'bane_of_arthropods', 'fire_aspect', 'looting', 'knockback', 'sweeping_edge', 'unbreaking', 'mending'],
    'axe': ['sharpness', 'smite', 'bane_of_arthropods', 'efficiency', 'fortune', 'silk_touch', 'unbreaking', 'mending'],
    'pickaxe': ['efficiency', 'fortune', 'silk_touch', 'unbreaking', 'mending'],
    'shovel': ['efficiency', 'fortune', 'silk_touch', 'unbreaking', 'mending'],
    'hoe': ['efficiency', 'fortune', 'silk_touch', 'unbreaking', 'mending'],
    'bow': ['power', 'punch', 'flame', 'infinity', 'unbreaking', 'mending'],
    'crossbow': ['multishot', 'piercing', 'quick_charge', 'unbreaking', 'mending'],
    'trident': ['channeling', 'riptide', 'loyalty', 'impaling', 'unbreaking', 'mending'],
    'helmet': ['protection', 'blast_protection', 'fire_protection', 'projectile_protection', 'thorns', 'respiration', 'aqua_affinity', 'unbreaking', 'mending', 'vanishing_curse', 'binding_curse'],
    'chestplate': ['protection', 'blast_protection', 'fire_protection', 'projectile_protection', 'thorns', 'unbreaking', 'mending', 'vanishing_curse', 'binding_curse'],
    'leggings': ['protection', 'blast_protection', 'fire_protection', 'projectile_protection', 'thorns', 'swift_sneak', 'unbreaking', 'mending', 'vanishing_curse', 'binding_curse'],
    'boots': ['protection', 'blast_protection', 'fire_protection', 'projectile_protection', 'thorns', 'feather_falling', 'depth_strider', 'frost_walker', 'soul_speed', 'unbreaking', 'mending', 'vanishing_curse', 'binding_curse'],
    'fishing_rod': ['luck_of_the_sea', 'lure', 'unbreaking', 'mending', 'vanishing_curse'],
    'shears': ['efficiency', 'unbreaking', 'mending'],
    'elytra': ['unbreaking', 'mending', 'vanishing_curse'],
    'flint_and_steel': ['unbreaking', 'mending'],
    'shield': ['unbreaking', 'mending', 'vanishing_curse'],
}


def get_enchantment_info(enchantment_name: str) -> dict:
    """Get complete information about an enchantment"""
    return ENCHANTMENT_DATABASE.get(enchantment_name, {})


def get_enchantments_for_item(item_name: str) -> list:
    """Get all applicable enchantments for an item"""
    return ENCHANTMENT_CATEGORIES.get(item_name, [])


def get_enchantment_max_level(enchantment_name: str) -> int:
    """Get maximum level for an enchantment"""
    enchant = ENCHANTMENT_DATABASE.get(enchantment_name, {})
    return enchant.get('max_level', 1)


def is_enchantment_compatible(enchantment1: str, enchantment2: str) -> bool:
    """Check if two enchantments are compatible"""
    enchant1_info = ENCHANTMENT_DATABASE.get(enchantment1, {})
    incompatible = enchant1_info.get('incompatible_with', [])
    return enchantment2 not in incompatible


def get_enchantment_description(enchantment_name: str) -> str:
    """Get enchantment description"""
    enchant = ENCHANTMENT_DATABASE.get(enchantment_name, {})
    return enchant.get('description', 'No description available')


def get_enchantment_effect(enchantment_name: str, level: int = 1) -> str:
    """Get enchantment effect at specific level"""
    enchant = ENCHANTMENT_DATABASE.get(enchantment_name, {})
    effects = enchant.get('effect_per_level', {})
    return effects.get(level, enchant.get('effect', 'Unknown effect'))


def is_curse(enchantment_name: str) -> bool:
    """Check if an enchantment is a curse"""
    enchant = ENCHANTMENT_DATABASE.get(enchantment_name, {})
    return enchant.get('curse', False)


def is_treasure_enchantment(enchantment_name: str) -> bool:
    """Check if an enchantment is a treasure enchantment"""
    enchant = ENCHANTMENT_DATABASE.get(enchantment_name, {})
    return enchant.get('treasure', False)


def get_best_weapon_enchantment(target_mob_type: str = 'general') -> list:
    """Get recommended weapon enchantments for specific mob type"""
    if target_mob_type == 'undead':
        return ['smite', 'unbreaking', 'mending', 'sharpness', 'looting']
    elif target_mob_type == 'arthropod':
        return ['bane_of_arthropods', 'unbreaking', 'mending', 'sharpness', 'looting']
    elif target_mob_type == 'general':
        return ['sharpness', 'unbreaking', 'mending', 'looting', 'knockback']
    return []


def get_best_armor_enchantment(situation: str = 'general') -> list:
    """Get recommended armor enchantments for specific situation"""
    if situation == 'general':
        return ['protection', 'unbreaking', 'mending']
    elif situation == 'explosion':
        return ['blast_protection', 'unbreaking', 'mending']
    elif situation == 'fire':
        return ['fire_protection', 'unbreaking', 'mending']
    elif situation == 'projectile':
        return ['projectile_protection', 'unbreaking', 'mending']
    elif situation == 'underwater':
        return ['respiration', 'depth_strider', 'aqua_affinity', 'protection', 'unbreaking', 'mending']
    return []


def get_best_mining_enchantment(tool_type: str = 'pickaxe', priority: str = 'speed') -> list:
    """Get recommended mining enchantments"""
    if priority == 'speed':
        return ['efficiency', 'unbreaking', 'mending']
    elif priority == 'drops':
        return ['fortune', 'unbreaking', 'mending']
    elif priority == 'special':
        return ['silk_touch', 'unbreaking', 'mending']
    return []


def get_all_combat_enchantments() -> list:
    """Get all combat-related enchantments"""
    return [name for name, data in ENCHANTMENT_DATABASE.items() if data.get('category') in ['combat', 'trident']]


def get_all_armor_enchantments() -> list:
    """Get all armor-related enchantments"""
    return [name for name, data in ENCHANTMENT_DATABASE.items() if data.get('category') == 'armor']


def get_all_curses() -> list:
    """Get all curse enchantments"""
    return [name for name, data in ENCHANTMENT_DATABASE.items() if data.get('curse', False)]


def get_all_treasure_enchantments() -> list:
    """Get all treasure enchantments"""
    return [name for name, data in ENCHANTMENT_DATABASE.items() if data.get('treasure', False)]


if __name__ == '__main__':
    # Test enchantment knowledge
    print("=== ENCHANTMENT KNOWLEDGE ===")
    print(f"Total enchantments: {len(ENCHANTMENT_DATABASE)}")

    print("\n=== Sword Enchantments ===")
    for enc in get_enchantments_for_item('sword'):
        info = get_enchantment_info(enc)
        print(f"{enc}: Max level {info['max_level']} - {info['description']}")

    print("\n=== Best vs Undead ===")
    for enc in get_best_weapon_enchantment('undead'):
        print(f"- {enc}")

    print("\n=== Underwater Armor Setup ===")
    armor = {
        'helmet': ['respiration', 'aqua_affinity'],
        'chestplate': ['protection'],
        'leggings': ['protection'],
        'boots': ['depth_strider']
    }
    for slot, enchants in armor.items():
        print(f"{slot}: {', '.join(enchants)}")
