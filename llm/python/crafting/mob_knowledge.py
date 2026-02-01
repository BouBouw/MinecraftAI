"""
Complete Minecraft Mob Knowledge
All mobs, their behaviors, drops, combat strategies, and interactions
"""

MOB_DATABASE = {
    # ============================================================
    # PASSIVE MOBS (Farm Animals)
    # ============================================================

    'cow': {
        'type': 'passive',
        'health': 10,
        'damage': 0,
        'behavior': 'wander',
        'drops': ['leather', 'raw_beef', 'steak'],
        'drop_chances': [0, 1, 1],
        'experience': [1, 1.0, 1.3],
        'categories': ['animal', 'farm'],
        'tamable': False,
        'breed_food': 'wheat',
        'size': 'large',
        'width': 1.4,
        'height': 1.4,
        'danger_level': 'none',
        'strategies': ['kill_for_food', 'breed_for_leather', 'milk_with_bucket'],
        'description': 'Source of leather, beef, and milk',
        'priority': 'high'
    },
    'mooshroom': {
        'type': 'passive',
        'health': 10,
        'damage': 0,
        'behavior': 'wander',
        'drops': ['leather', 'raw_beef', 'mushroom_stew'],
        'drop_chances': [0, 1, 0.2],
        'experience': [1, 1.0, 2],
        'categories': ['animal', 'farm', 'rare'],
        'tamable': False,
        'breed_food': 'wheat',
        'size': 'large',
        'width': 1.4,
        'height': 1.4,
        'danger_level': 'none',
        'strategies': ['kill_for_food', 'shear_for_mushrooms', 'milk_with_bucket'],
        'description': 'Cow variant that also provides mushrooms',
        'biome': 'mushroom_fields'
    },
    'pig': {
        'type': 'passive',
        'health': 10,
        'damage': 0,
        'behavior': 'wander',
        'drops': ['porkchop'],
        'drop_chances': [1],
        'experience': [1.3],
        'categories': ['animal', 'farm'],
        'tamable': False,
        'breed_food': ['carrot', 'potato', 'beetroot'],
        'size': 'medium',
        'width': 0.9,
        'height': 0.9,
        'danger_level': 'none',
        'strategies': ['kill_for_food', 'breed', 'saddle_ride'],
        'description': 'Source of pork, can be ridden',
        'priority': 'high'
    },
    'sheep': {
        'type': 'passive',
        'health': 8,
        'damage': 0,
        'behavior': 'wander',
        'drops': ['wool', 'mutton'],
        'drop_chances': [1, 1],
        'experience': [1.25, 1.25],
        'categories': ['animal', 'farm'],
        'tamable': False,
        'breed_food': 'wheat',
        'size': 'medium',
        'width': 0.9,
        'height': 1.3,
        'danger_level': 'none',
        'color_variants': ['white', 'orange', 'magenta', 'light_blue', 'lime', 'pink', 'gray', 'light_gray', 'cyan', 'purple', 'blue', 'brown', 'green', 'red', 'black'],
        'strategies': ['shear_for_wool', 'kill_for_mutton', 'breed'],
        'description': 'Source of wool and mutton',
        'priority': 'high'
    },
    'chicken': {
        'type': 'passive',
        'health': 4,
        'damage': 0,
        'behavior': 'wander',
        'drops': ['feather', 'chicken', 'egg'],
        'drop_chances': [0.8, 1, 1],
        'experience': [1.2, 1.2, 1.2],
        'categories': ['animal', 'farm'],
        'tamable': False,
        'breed_food': ['any_seeds'],
        'size': 'small',
        'width': 0.4,
        'height': 0.7,
        'danger_level': 'none',
        'abilities': ['lay_eggs', 'float_on_water'],
        'strategies': ['collect_eggs', 'kill_for_food', 'breed'],
        'description': 'Lays eggs periodically, floats on water',
        'priority': 'high'
    },
    'rabbit': {
        'type': 'passive',
        'health': 3,
        'damage': 0,
        'behavior': 'wander',
        'drops': ['rabbit', 'rabbit_foot', 'rabbit_hide'],
        'drop_chances': [1, 0.025, 0.2],
        'experience': [1.2, 1.2, 1.2],
        'categories': ['animal', 'farm'],
        'tamable': False,
        'breed_food': ['carrot', 'golden_carrot', 'dandelion'],
        'size': 'tiny',
        'width': 0.4,
        'height': 0.5,
        'danger_level': 'none',
        'abilities': ['fast_jump'],
        'strategies': ['kill_for_food', 'breed', 'chasing_movement'],
        'killer_bunny_variant': 'rare',
        'description': 'Fast movement, drops rabbit foot',
        'priority': 'medium'
    },

    # ============================================================
    # PASSIVE MOBS (Pets/Tameable)
    # ============================================================

    'wolf': {
        'type': 'neutral',
        'health': 8,
        'damage': 4,
        'behavior': 'wander',
        'drops': None,
        'categories': ['animal', 'wild', 'tamable'],
        'tamable': True,
        'breed_food': 'any_meat',
        'tame_food': 'bone',
        'size': 'medium',
        'width': 0.6,
        'height': 0.85,
        'danger_level': 'medium',
        'hostile_when': ['attacked', 'player_nearby'],
        'pack_hunter': True,
        'abilities': ['shake_fur', 'wolf_armor'],
        'strategies': ['tame', 'avoid', 'attack_if_tamed'],
        'description': 'Pack hunter, can be tamed',
        'priority': 'medium'
    },
    'cat': {
        'type': 'passive',
        'health': 10,
        'damage': 0,
        'behavior': 'wander',
        'drops': None,
        'categories': ['animal', 'tamable'],
        'tamable': True,
        'breed_food': ['cod', 'salmon', 'tropical_fish'],
        'tame_food': ['cod', 'salmon'],
        'size': 'small',
        'width': 0.6,
        'height': 0.7,
        'danger_level': 'none',
        'abilities': ['scare_creeper', 'gift_gifts'],
        'color_variants': ['tabby', 'tuxedo', 'siamese', 'red', 'british', 'calico', 'persian', 'ragdoll', 'white', 'jellie', 'all_black'],
        'strategies': ['tame', 'scare_creeper'],
        'description': 'Scares creepers, brings gifts',
        'village_spawn': True
    },
    'parrot': {
        'type': 'passive',
        'health': 6,
        'damage': 0,
        'behavior': 'fly',
        'drops': ['feather'],
        'drop_chances': [1.2],
        'experience': [1.2],
        'categories': ['animal', 'flying', 'tamable'],
        'tamable': True,
        'tame_food': ['any_seeds'],
        'size': 'tiny',
        'width': 0.5,
        'height': 0.9,
        'danger_level': 'none',
        'flying': True,
        'abilities': ['mimic_sounds', 'dance', 'shoulder_perch'],
        'color_variants': ['red', 'blue', 'green', 'cyan', 'gray'],
        'strategies': ['tame', 'dance_for_music_disc'],
        'description': 'Mimics sounds and dances to music',
        'rare': True,
        'biome': 'jungle'
    },
    'axolotl': {
        'type': 'passive',
        'health': 14,
        'damage': 0,
        'behavior': 'wander',
        'drops': None,
        'categories': ['animal', 'aquatic', 'tamable'],
        'tamable': True,
        'breed_food': 'bucket_of_tropical_fish',
        'tame_food': 'bucket_of_tropical_fish',
        'size': 'small',
        'width': 0.9,
        'height': 0.42,
        'danger_level': 'none',
        'aquatic': True,
        'abilities': ['regenerate', 'play_dead', 'attack_guardian'],
        'color_variants': ['leucistic', 'brown', 'gold', 'cyan', 'wild'],
        'strategies': ['bucket_collect', 'hunt_guardians'],
        'description': 'Regenerates, plays dead when hurt, attacks guardians',
        'biome': 'lush_caves'
    },

    # ============================================================
    # PASSIVE MOBS (Mounts)
    # ============================================================

    'horse': {
        'type': 'passive',
        'health': 15,
        'damage': 0,
        'behavior': 'wander',
        'drops': ['leather', 'beef'],
        'drop_chances': [0.25, 0.25],
        'experience': [1.3, 1.3],
        'categories': ['animal', 'rideable'],
        'tamable': True,
        'tame_food': ['wheat', 'sugar', 'hay_bale', 'apple', 'golden_carrot', 'golden_apple'],
        'breed_food': ['golden_apple', 'golden_carrot', 'hay_bale'],
        'size': 'large',
        'width': 1.4,
        'height': 1.6,
        'danger_level': 'none',
        'rideable': True,
        'abilities': ['jump', 'speed'],
        'color_variants': ['white', 'creamy', 'chestnut', 'brown', 'black', 'gray', 'dark_brown'],
        'marking_variants': ['none', 'white', 'white_field', 'white_dots', 'black_dots'],
        'strategies': ['tame', 'ride', 'breed'],
        'description': 'Fast mount, color variants',
        'priority': 'high'
    },
    'donkey': {
        'type': 'passive',
        'health': 15,
        'damage': 0,
        'behavior': 'wander',
        'drops': None,
        'categories': ['animal', 'rideable'],
        'tamable': True,
        'tame_food': ['wheat', 'hay_bale'],
        'breed_food': ['golden_apple', 'golden_carrot', 'hay_bale'],
        'size': 'medium',
        'width': 1.4,
        'height': 1.5,
        'danger_level': 'none',
        'rideable': True,
        'chest_carrier': True,
        'strategies': ['ride_with_chest', 'breed'],
        'description': 'Chest carrier, slower than horse'
    },
    'mule': {
        'type': 'passive',
        'health': 15,
        'damage': 0,
        'behavior': 'wander',
        'drops': None,
        'categories': ['animal', 'rideable', 'rare'],
        'tamable': False,
        'size': 'medium',
        'width': 1.4,
        'height': 1.6,
        'danger_level': 'none',
        'rideable': True,
        'chest_carrier': True,
        'offspring_of': ['horse', 'donkey'],
        'strategies': ['ride_with_chest'],
        'description': 'Best chest carrier, cannot breed'
    },
    'llama': {
        'type': 'neutral',
        'health': 15,
        'damage': 1,
        'behavior': 'wander',
        'drops': ['leather', 'wool', 'carpet'],
        'drop_chances': [0.25, 0.25, 0.33],
        'experience': [1.3, 1.3, 1.3],
        'categories': ['animal', 'rideable'],
        'tamable': True,
        'tame_food': 'hay_bale',
        'breed_food': 'hay_bale',
        'size': 'large',
        'width': 0.9,
        'height': 1.87,
        'danger_level': 'low',
        'rideable': False,
        'abilities': ['spit', 'carpet_decoration', 'chest_carrier'],
        'strategies': ['carpet_supplier', 'ride', 'breed'],
        'description': 'Spits at wolves, can be decorated',
        'caravan': True
    },
    'trader_llama': {
        'type': 'neutral',
        'health': 20,
        'damage': 1,
        'behavior': 'wander',
        'drops': ['leather', 'wool', 'carpet'],
        'drop_chances': [0.25, 0.25, 0.33],
        'categories': ['animal', 'rideable'],
        'tamable': False,
        'size': 'large',
        'width': 0.9,
        'height': 1.87,
        'danger_level': 'none',
        'rideable': False,
        'spit': True,
        'strategies': ['carpet_supplier'],
        'description': 'Belongs to wandering trader',
        'spawns_with': 'wandering_trader'
    },
    'camel': {
        'type': 'passive',
        'health': 32,
        'damage': 0,
        'behavior': 'wander',
        'drops': None,
        'categories': ['animal', 'rideable'],
        'tamable': True,
        'breed_food': 'cactus',
        'size': 'large',
        'width': 1.7,
        'height': 2.4,
        'danger_level': 'none',
        'rideable': True,
        'abilities': ['dash', 'two_riders'],
        'strategies': ['ride_with_two_players', 'dash'],
        'description': 'Can be ridden by two players, can dash',
        'biome': 'desert'
    },

    # ============================================================
    # PASSIVE MOBS (Wild/NPC)
    # ============================================================

    'fox': {
        'type': 'passive',
        'health': 10,
        'damage': 2,
        'behavior': 'wander',
        'drops': None,
        'categories': ['animal', 'wild'],
        'tamable': False,
        'breed_food': ['sweet_berries', 'glow_berries'],
        'size': 'small',
        'width': 0.6,
        'height': 0.7,
        'danger_level': 'low',
        'attacks': ['chicken', 'rabbit', 'baby_turtle', 'fish'],
        'abilities': ['carry_items', 'sleep', 'night_active'],
        'color_variants': ['red', 'snow'],
        'strategies': ['avoid', 'protect_farm', 'breed_with_berries'],
        'description': 'Hunts small animals, active at night',
        'biome': ['taiga', 'snowy_taiga']
    },
    'frog': {
        'type': 'passive',
        'health': 6,
        'damage': 0,
        'behavior': 'wander',
        'drops': None,
        'categories': ['animal', 'aquatic'],
        'tamable': False,
        'breed_food': 'slime_ball',
        'size': 'tiny',
        'width': 0.5,
        'height': 0.4,
        'danger_level': 'none',
        'aquatic': True,
        'abilities': ['eat_slime', 'eat_small_mobs', 'jump_high'],
        'color_variants': ['temperate', 'warm', 'cold'],
        'strategies': ['breed', 'collect_slime_balls'],
        'description': 'Eats slimes and small mobs, produces froglight',
        'biome': 'swamp'
    },
    'turtle': {
        'type': 'passive',
        'health': 30,
        'damage': 0,
        'behavior': 'wander',
        'drops': ['seagrass', 'turtle_egg', 'scute'],
        'drop_chances': [0.33, 1, 1],
        'experience': [1.2, 1.2, 1.2],
        'categories': ['animal', 'aquatic'],
        'tamable': False,
        'size': 'medium',
        'width': 1.2,
        'height': 0.4,
        'danger_level': 'none',
        'aquatic': True,
        'abilities': ['swim', 'lay_eggs', 'home_beach'],
        'strategies': ['collect_seagrass', 'breed', 'harvest_scutes'],
        'description': 'Swims in water, drops scutes for turtle helmet',
        'biome': 'beach'
    },
    'polar_bear': {
        'type': 'neutral',
        'health': 30,
        'damage': 6,
        'behavior': 'wander',
        'drops': None,
        'categories': ['animal', 'hostile', 'arctic'],
        'tamable': False,
        'size': 'large',
        'width': 1.4,
        'height': 1.4,
        'danger_level': 'medium',
        'hostile_when': ['attacked', 'player_nearby_cub'],
        'strategies': ['avoid', 'snow_biome'],
        'description': 'Aggressive if cub is nearby',
        'biome': ['snowy_plains', 'ice_spikes']
    },
    'panda': {
        'type': 'passive',
        'health': 20,
        'damage': 0,
        'behavior': 'wander',
        'drops': None,
        'categories': ['animal', 'rare'],
        'tamable': False,
        'breed_food': 'bamboo',
        'size': 'large',
        'width': 1.2,
        'height': 1.2,
        'danger_level': 'none',
        'abilities': ['roll_over', 'sit', 'eat_bamboo'],
        'personality_variants': ['normal', 'lazy', 'worried', 'playful', 'aggressive', 'brown', 'weak'],
        'strategies': ['feed_bamboo', 'breed'],
        'description': 'Loves bamboo, different personalities',
        'biome': 'bamboo_jungle'
    },
    'bee': {
        'type': 'passive',
        'health': 10,
        'damage': 0,
        'behavior': 'fly',
        'drops': None,
        'categories': ['animal', 'flying'],
        'tamable': False,
        'size': 'tiny',
        'width': 0.6,
        'height': 0.6,
        'danger_level': 'medium',
        'flying': True,
        'abilities': ['pollinate', 'honey', 'sting', 'hive_defense'],
        'hive_type': 'bee_nest',
        'strategies': ['collect_honeycomb', 'breed_flowers', 'avoid_attacking'],
        'description': 'Pollinates flowers, produces honey, sting kills bee',
        'attack': 'swarm'
    },
    'ocelot': {
        'type': 'passive',
        'health': 10,
        'damage': 0,
        'behavior': 'wander',
        'drops': None,
        'categories': ['animal', 'wild', 'shy'],
        'tamable': True,
        'breed_food': ['cod', 'salmon', 'tropical_fish'],
        'tame_food': ['cod', 'salmon', 'tropical_fish'],
        'size': 'small',
        'width': 0.6,
        'height': 0.7,
        'danger_level': 'none',
        'shy': True,
        'abilities': ['run_away', 'chicken_hunter'],
        'strategies': ['sneak_up_to_tame', 'chicken_hunter'],
        'description': 'Shy, runs from player, hunts chickens',
        'biome': 'jungle'
    },
    'dolphin': {
        'type': 'passive',
        'health': 10,
        'damage': 0,
        'behavior': 'swim',
        'drops': None,
        'categories': ['animal', 'aquatic', 'friendly'],
        'tamable': False,
        'size': 'large',
        'width': 0.9,
        'height': 0.6,
        'danger_level': 'none',
        'aquatic': True,
        'abilities': ['swim_fast', 'find_treasure', 'grant_speed'],
        'strategies': ['follow', 'feed_cod', 'treasure_hunter'],
        'description': 'Friendly, finds treasure, grants swimming speed',
        'gratitude': 'feed_cod'
    },
    'sniffer': {
        'type': 'passive',
        'health': 20,
        'damage': 0,
        'behavior': 'wander',
        'drops': None,
        'categories': ['animal', 'rare', 'ancient'],
        'tamable': False,
        'breed_food': 'torchflower_seeds',
        'size': 'large',
        'width': 1.9,
        'height': 1.7,
        'danger_level': 'none',
        'abilities': ['sniff_items', 'dig_up_seeds', 'old_mob'],
        'sniffable_items': ['torchflower_seeds', 'pitcher_pod'],
        'strategies': ['follow_for_digging', 'breed'],
        'description': 'Ancient mob, digs up rare seeds',
        'vote_winner': True
    },
    'armadillo': {
        'type': 'passive',
        'health': 12,
        'damage': 0,
        'behavior': 'wander',
        'drops': None,
        'categories': ['animal', 'wild'],
        'tamable': False,
        'breed_food': 'spider_eye',
        'size': 'medium',
        'width': 0.7,
        'height': 0.6,
        'danger_level': 'none',
        'abilities': ['roll_up', 'drop_scute'],
        'strategies': ['brush_for_scute', 'avoid_spiders'],
        'description': 'Rolls up when threatened, drops wolf armor scutes',
        'biome': 'savanna'
    },

    # ============================================================
    # AQUATIC MOBS (Fish)
    # ============================================================

    'cod': {
        'type': 'passive',
        'health': 6,
        'damage': 0,
        'behavior': 'swim',
        'drops': ['cod', 'bone_meal'],
        'drop_chances': [1, 0.05],
        'experience': [1.2, 1.2],
        'categories': ['animal', 'aquatic', 'food'],
        'tamable': False,
        'size': 'small',
        'width': 0.5,
        'height': 0.3,
        'danger_level': 'none',
        'aquatic': True,
        'schools': True,
        'strategies': ['kill_with_sword', 'fishing', 'bucket_collect'],
        'description': 'Common fish, drops bonemeal'
    },
    'salmon': {
        'type': 'passive',
        'health': 6,
        'damage': 0,
        'behavior': 'swim',
        'drops': ['salmon', 'bone_meal'],
        'drop_chances': [1, 0.05],
        'experience': [1.2, 1.2],
        'categories': ['animal', 'aquatic', 'food'],
        'tamable': False,
        'size': 'medium',
        'width': 0.7,
        'height': 0.4,
        'danger_level': 'none',
        'aquatic': True,
        'schools': True,
        'strategies': ['kill_with_sword', 'fishing', 'bucket_collect'],
        'description': 'Medium fish, drops bonemeal'
    },
    'tropical_fish': {
        'type': 'passive',
        'health': 6,
        'damage': 0,
        'behavior': 'swim',
        'drops': ['tropical_fish', 'bone_meal'],
        'drop_chances': [1, 0.05],
        'experience': [1.2, 1.2],
        'categories': ['animal', 'aquatic', 'food'],
        'tamable': False,
        'size': 'small',
        'width': 0.6,
        'height': 0.4,
        'danger_level': 'none',
        'aquatic': True,
        'schools': True,
        'color_variants': ['many', 'variants'],
        'strategies': ['catch_with_bucket', 'kill_with_sword', 'axolotl_food'],
        'description': 'Tropical fish, feeds axolotls'
    },
    'pufferfish': {
        'type': 'passive',
        'health': 6,
        'damage': 0,
        'behavior': 'swim',
        'drops': ['pufferfish', 'bone_meal'],
        'drop_chances': [1, 0.05],
        'experience': [1.2, 1.2],
        'categories': ['animal', 'aquatic', 'poisonous'],
        'tamable': False,
        'size': 'tiny',
        'width': 0.35,
        'height': 0.35,
        'danger_level': 'medium',
        'poison': 3,
        'aquatic': True,
        'abilities': ['puff_up', 'poisonous_touch'],
        'strategies': ['avoid_when_inflated', 'water_bucket_collect'],
        'description': 'Poisonous when attacked, puffs up'
    },
    'squid': {
        'type': 'passive',
        'health': 10,
        'damage': 0,
        'behavior': 'swim',
        'drops': ['ink_sac'],
        'drop_chances': [0.9],
        'experience': [1.3],
        'categories': ['animal', 'aquatic'],
        'tamable': False,
        'size': 'medium',
        'width': 0.8,
        'height': 0.8,
        'danger_level': 'none',
        'aquatic': True,
        'abilities': ['shoot_ink', 'swim_fast'],
        'strategies': ['collect_ink_sac', 'avoid_attacks'],
        'description': 'Shoots ink to escape'
    },
    'glow_squid': {
        'type': 'passive',
        'health': 10,
        'damage': 0,
        'behavior': 'swim',
        'drops': ['glow_ink_sac'],
        'drop_chances': [1],
        'experience': [1.3],
        'categories': ['animal', 'aquatic', 'light'],
        'tamable': False,
        'size': 'medium',
        'width': 0.8,
        'height': 0.8,
        'danger_level': 'none',
        'aquatic': True,
        'light_level': 9,
        'abilities': ['shoot_ink', 'glowing'],
        'strategies': ['collect_glow_ink_sac'],
        'description': 'Glows, produces glow ink sac',
        'vote_winner': True
    },
    'tadpole': {
        'type': 'passive',
        'health': 6,
        'damage': 0,
        'behavior': 'swim',
        'drops': None,
        'categories': ['animal', 'aquatic', 'baby'],
        'tamable': False,
        'size': 'tiny',
        'width': 0.4,
        'height': 0.3,
        'danger_level': 'none',
        'aquatic': True,
        'grows_into': 'frog',
        'strategies': ['catch_with_bucket', 'grow_to_frog'],
        'description': 'Baby frog, grows in water'
    },

    # ============================================================
    # NPC MOBS
    # ============================================================

    'villager': {
        'type': 'passive',
        'health': 20,
        'damage': 0,
        'behavior': 'wander',
        'drops': None,
        'categories': ['npc', 'trading'],
        'tamable': False,
        'size': 'adult',
        'professions': ['farmer', 'librarian', 'cleric', 'armorer', 'weapon_smith', 'tool_smith', 'butcher', 'leatherworker', 'fletcher', 'fisherman', 'cartographer', 'shepherd', 'mason', 'nitwit'],
        'trades': True,
        'currency': 'emerald',
        'abilities': ['work', 'sleep', 'gossip'],
        'strategies': ['trade_emeralds', 'cure_zombie_villager', 'employ_job_site'],
        'zombie_variant': 'zombie_villager',
        'description': 'Trading partner, professions available',
        'priority': 'high'
    },
    'wandering_trader': {
        'type': 'passive',
        'health': 20,
        'damage': 0,
        'behavior': 'wander',
        'drops': None,
        'categories': ['npc', 'trading', 'rare'],
        'tamable': False,
        'llama': True,
        'strategies': ['trade_rare_items', 'emerald_currency'],
        'description': 'Rare trader with special items',
        'spawns': 'periodically'
    },

    # ============================================================
    # GOLEMS
    # ============================================================

    'iron_golem': {
        'type': 'neutral',
        'health': 100,
        'damage': 7,
        'behavior': 'protect',
        'drops': ['iron_ingot', 'poppy'],
        'drop_chances': [0, 0.05],
        'experience': [0, 1.0],
        'categories': ['golem', 'neutral', 'construct', 'village'],
        'tamable': False,
        'size': 'large',
        'width': 1.4,
        'height': 2.7,
        'danger_level': 'none',
        'attacks': ['zombie', 'illager', 'pillager'],
        'village_protector': True,
        'created_by': ['villagers', 'player'],
        'summonable': True,
        'friendly': True,
        'strategies': ['create_for_village_protection', 'let_protect'],
        'description': 'Protects villagers, attacks zombies',
        'poppy_gift': True
    },
    'snow_golem': {
        'type': 'passive',
        'health': 4,
        'damage': 0,
        'behavior': 'wander',
        'drops': ['snowball'],
        'drop_chances': [0],
        'categories': ['golem', 'passive', 'construct'],
        'tamable': False,
        'size': 'medium',
        'width': 0.7,
        'height': 1.9,
        'danger_level': 'none',
        'attacks': ['blaze', 'creeper'],  # Only in nether
        'throws': ['snowball'],
        'created_by': ['player', 'villagers'],
        'summonable': True,
        'melts_in': ['desert', 'nether', 'jungle'],
        'strategies': ['create_for_snow_defense', 'snow_trail'],
        'description': 'Throws snowballs, creates snow trail'
    },

    # ============================================================
    # NEUTRAL MOBS
    # ============================================================

    'enderman': {
        'type': 'neutral',
        'health': 40,
        'damage': 7,
        'behavior': 'wander',
        'drops': ['ender_pearl'],
        'drop_chances': [1],
        'experience': [3.0],
        'categories': ['neutral', 'teleporting', 'end'],
        'tamable': False,
        'size': 'tall',
        'width': 0.6,
        'height': 2.9,
        'danger_level': 'very_high',
        'hostile_when': ['eye_contact', 'attacked'],
        'abilities': ['teleport', 'carry_blocks', 'water_damage'],
        'weakness': ['water', 'rain'],
        'strategies': ['avoid_eye_contact', 'use_water_bucket', 'build_3_high'],
        'description': 'Teleports, takes damage from water',
        'biome': 'all'
    },
    'polar_bear': {
        'type': 'neutral',
        'health': 30,
        'damage': 6,
        'behavior': 'wander',
        'drops': None,
        'categories': ['animal', 'hostile', 'arctic'],
        'tamable': False,
        'size': 'large',
        'width': 1.4,
        'height': 1.4,
        'danger_level': 'medium',
        'hostile_when': ['player_nearby_cub'],
        'strategies': ['avoid_cubs'],
        'description': 'Neutral unless cub is nearby',
        'biome': 'snowy_biomes'
    },
    'panda': {
        'type': 'neutral',
        'health': 20,
        'damage': 4,  # Aggressive personality
        'behavior': 'wander',
        'drops': None,
        'categories': ['animal', 'rare'],
        'tamable': False,
        'size': 'large',
        'width': 1.2,
        'height': 1.2,
        'danger_level': 'low',
        'hostile_when': ['attacked', 'aggressive_personality'],
        'personality_variants': ['normal', 'lazy', 'worried', 'playful', 'aggressive', 'brown', 'weak'],
        'strategies': ['feed_bamboo'],
        'description': 'Most personalities are peaceful',
        'biome': 'bamboo_jungle'
    },
    'llama': {
        'type': 'neutral',
        'health': 15,
        'damage': 1,
        'behavior': 'wander',
        'drops': ['leather', 'wool'],
        'drop_chances': [0.25, 0.25],
        'categories': ['animal', 'rideable'],
        'tamable': True,
        'size': 'large',
        'width': 0.9,
        'height': 1.87,
        'danger_level': 'low',
        'hostile_when': ['attacked', 'wolf_nearby'],
        'spit': True,
        'strategies': ['avoid_wolf'],
        'description': 'Spits at wolves when provoked'
    },
    'trader_llama': {
        'type': 'neutral',
        'health': 20,
        'damage': 1,
        'behavior': 'wander',
        'drops': None,
        'categories': ['animal', 'rideable'],
        'tamable': False,
        'size': 'large',
        'width': 0.9,
        'height': 1.87,
        'danger_level': 'none',
        'hostile_when': ['attacked', 'wolf_nearby'],
        'strategies': ['avoid_attacking'],
        'description': 'Protects wandering trader'
    },

    # ============================================================
    # NETHER NEUTRAL MOBS
    # ============================================================

    'piglin': {
        'type': 'neutral',
        'health': 16,
        'damage': 5,
        'behavior': 'wander',
        'drops': ['arrow', 'random_piglin_loot'],
        'drop_chances': [0.2, 0.1],
        'experience': [1.3, 1.3],
        'categories': ['neutral', 'nether', 'trading'],
        'tamable': False,
        'size': 'medium',
        'width': 0.6,
        'height': 1.95,
        'danger_level': 'medium',
        'hostile_when': ['attacked', 'opened_container', 'broken_gold_ore', 'no_gold_armor'],
        'trades': True,
        'currency': 'gold_ingot',
        'neutral_when': ['wearing_gold_armor', 'unprovoked'],
        'abilities': ['hunt_hoglin', 'barter', 'crossbow'],
        'zombification': 'zombified_piglin',
        'strategies': ['wear_gold_armor', 'barter', 'avoid_attacking'],
        'description': 'Nether traders, love gold',
        'biome': ['nether_wastes', 'crimson_forest']
    },
    'piglin_brute': {
        'type': 'hostile',
        'health': 50,
        'damage': 8,
        'behavior': 'attack',
        'drops': ['random_piglin_loot'],
        'drop_chances': [0.2],
        'experience': [1.3],
        'categories': ['nether', 'hostile', 'elite'],
        'tamable': False,
        'size': 'large',
        'width': 1.95,
        'height': 2.2,
        'danger_level': 'high',
        'hostile': True,
        'attacks': ['player', 'iron_golem'],
        'immune_to': ['knockback'],
        'strategies': ['avoid', 'crossbow_attack', 'wear_gold_armor_no_effect'],
        'description': 'Elite piglin, always hostile, immune to knockback',
        'spawns': 'bastion_remnant'
    },
    'hoglin': {
        'type': 'neutral',
        'health': 40,
        'damage': 6,
        'behavior': 'hunt',
        'drops': ['raw_porkchop', 'hoglin_tusk', 'leather'],
        'drop_chances': [1, 0.1, 0.25],
        'experience': [1.0, 1.0, 1.0],
        'categories': ['nether', 'neutral', 'breedable'],
        'tamable': False,
        'breed_food': 'crimson_fungus',
        'size': 'large',
        'width': 1.5,
        'height': 2.0,
        'danger_level': 'medium',
        'hostile_when': ['attacked', 'player_nearby', 'no_crimson_fungus'],
        'abilities': ['attack', 'breed', 'zombify'],
        'zombification': 'zoglin',
        'hunted_by': 'piglin',
        'strategies': ['attack_from_distance', 'counter_charge', 'breed_for_farming'],
        'description': 'Piglin hunting target, breedable for pork',
        'biome': 'crimson_forest'
    },

    # ============================================================
    # COMMON HOSTILE MOBS
    # ============================================================

    'zombie': {
        'type': 'hostile',
        'health': 20,
        'damage': 3,
        'behavior': 'attack',
        'drops': ['rotten_flesh', 'rare_drop'],
        'drop_chances': [1, 0.025],
        'experience': [1.0],
        'categories': ['undead', 'hostile', 'common', 'night'],
        'tamable': False,
        'size': 'medium',
        'width': 0.6,
        'height': 1.95,
        'danger_level': 'medium',
        'burns_in_sunlight': True,
        'doors': ['breaks_wood_doors', 'breaks_iron_doors_hard'],
        'infects_villagers': True,
        'summon': ['zombie_villager', 'chicken_jockey'],
        'reinforcements': True,
        'strategies': ['hit_and_run', 'weapon_diamond_or_better', 'use_shield', 'iron_golem_help'],
        'description': 'Classic undead mob, breaks doors',
        'spawns': ['night', 'caves']
    },
    'zombie_villager': {
        'type': 'hostile',
        'health': 20,
        'damage': 3,
        'behavior': 'attack',
        'drops': ['rotten_flesh'],
        'drop_chances': [1],
        'experience': [1.0],
        'categories': ['undead', 'hostile', 'curable'],
        'tamable': False,
        'size': 'medium',
        'width': 0.6,
        'height': 1.95,
        'danger_level': 'medium',
        'burns_in_sunlight': True,
        'profession': 'zombified_profession',
        'curable': True,
        'cure_method': ['weakness_potion', 'golden_apple'],
        'strategies': ['cure_with_weakness', 'kill'],
        'description': 'Zombified villager, can be cured',
        'spawns': 'zombie_kill_villager'
    },
    'husk': {
        'type': 'hostile',
        'health': 20,
        'damage': 3,
        'behavior': 'attack',
        'drops': ['rotten_flesh'],
        'drop_chances': [1],
        'experience': [1.0],
        'categories': ['undead', 'hostile', 'rare'],
        'tamable': False,
        'size': 'medium',
        'width': 0.6,
        'height': 1.95,
        'danger_level': 'medium',
        'no_burn_in_sunlight': True,
        'abilities': ['hunger_effect', 'no_burn_sunlight'],
        'strategies': ['avoid_hunger', 'kill_in_dark'],
        'description': 'Desert zombie, applies hunger',
        'biome': 'desert'
    },
    'drowned': {
        'type': 'hostile',
        'health': 20,
        'damage': 3,
        'behavior': 'attack',
        'drops': ['rotten_flesh', 'copper_ingot', 'gold_ingot', 'trident'],
        'drop_chances': [1, 0.03, 0.03, 0.006],
        'experience': [1.0, 0.6, 0.6, 2.0],
        'categories': ['undead', 'hostile', 'aquatic', 'rare'],
        'tamable': False,
        'size': 'medium',
        'width': 0.6,
        'height': 1.95,
        'danger_level': 'medium',
        'aquatic': True,
        'no_burn_in_water': True,
        'abilities': ['underwater_combat', 'trident_attack', 'suffocate_land'],
        'strategies': ['water_combat', 'kill_from_land', 'rare_trident_drop'],
        'description': 'Underwater zombie variant, may drop trident',
        'spawns': ['underwater', 'zombie_drown']
    },
    'skeleton': {
        'type': 'hostile',
        'health': 20,
        'damage': 2,
        'behavior': 'attack',
        'drops': ['arrow', 'bone', 'rare_drop'],
        'drop_chances': [0.5, 0.5, 0.025],
        'experience': [1.0],
        'categories': ['skeleton', 'hostile', 'ranged', 'night'],
        'tamable': False,
        'size': 'medium',
        'width': 0.6,
        'height': 1.99,
        'danger_level': 'medium',
        'weapon': 'bow',
        'damage_type': 'physical',
        'burns_in_sunlight': True,
        'strategies': ['get_up_close', 'strafe', 'use_shield'],
        'description': 'Ranged attacker, poor aim',
        'spawns': ['night', 'caves']
    },
    'stray': {
        'type': 'hostile',
        'health': 20,
        'damage': 2,
        'behavior': 'attack',
        'drops': ['arrow', 'bone', 'rare_drop'],
        'drop_chances': [0.5, 0.5, 0.025],
        'experience': [1.0],
        'categories': ['skeleton', 'hostile', 'ranged', 'rare'],
        'tamable': False,
        'size': 'medium',
        'width': 0.6,
        'height': 1.99,
        'danger_level': 'medium',
        'weapon': 'bow',
        'arrows': 'slowness',
        'burns_in_sunlight': True,
        'strategies': ['same_as_skeleton', 'watch_slowness'],
        'description': 'Ice variant skeleton, shoots slowness arrows',
        'biome': ['snowy_biomes', 'ice_spikes']
    },
    'spider': {
        'type': 'hostile',
        'health': 16,
        'damage': 2,
        'behavior': 'attack',
        'drops': ['string', 'spider_eye'],
        'drop_chances': [0.5, 0.5],
        'experience': [1.0],
        'categories': ['arthropod', 'hostile', 'common', 'night'],
        'tamable': False,
        'size': 'medium',
        'width': 1.4,
        'height': 0.9,
        'danger_level': 'medium',
        'abilities': ['climb_walls', 'jump_attack'],
        'neutral_daylight': True,
        'hostile_night': True,
        'strategies': ['attack_from_above', 'use_sword', 'knockback'],
        'weakness': 'bane_of_arthropods',
        'description': 'Climbs walls, neutral during day',
        'spawns': ['night', 'caves']
    },
    'cave_spider': {
        'type': 'hostile',
        'health': 12,
        'damage': 2,
        'behavior': 'attack',
        'drops': ['string', 'spider_eye'],
        'drop_chances': [0.5, 0.5],
        'experience': [1.0],
        'categories': ['arthropod', 'hostile', 'rare', 'underground'],
        'tamable': False,
        'size': 'small',
        'width': 0.7,
        'height': 0.5,
        'danger_level': 'medium',
        'abilities': ['poison', 'wall_climb'],
        'poison_duration': 7,
        'poison_damage': 2,
        'spawns_from': ['spawner', 'mineshaft'],
        'strategies': ['attack_from_distance', 'use_milk'],
        'description': 'Poisonous cave variant',
        'weakness': 'bane_of_arthropods'
    },
    'creeper': {
        'type': 'hostile',
        'health': 20,
        'damage': 65,  # Explosion
        'behavior': 'attack',
        'drops': ['gunpowder', 'music_disc', 'random_mob_head'],
        'drop_chances': [1, 0.01, 0.01],
        'experience': [5.0],
        'categories': ['hostile', 'explosive', 'common', 'night'],
        'tamable': False,
        'size': 'medium',
        'width': 0.6,
        'height': 1.7,
        'danger_level': 'extreme',
        'abilities': ['explode', 'charged_lightning', 'ignite_flint_and_steel'],
        'explosion_radius': 3,
        'charged_damage': 'double',
        'fears': ['cat', 'ocelot'],
        'strategies': ['run_away_immediately', 'use_shield', 'attack_from_distance', 'cat_defense'],
        'description': 'Silent approach, deadly explosion',
        'spawns': ['night', 'caves']
    },
    'silverfish': {
        'type': 'hostile',
        'health': 8,
        'damage': 1,
        'behavior': 'attack',
        'drops': None,
        'categories': ['arthropod', 'hostile', 'rare', 'underground'],
        'tamable': False,
        'size': 'tiny',
        'width': 0.4,
        'height': 0.3,
        'danger_level': 'low',
        'abilities': ['hide_in_stone', 'call_reinforcements'],
        'spawns_from': ['infested_block', 'stronghold', 'portal'],
        'strategies': ['avoid_breaking_infested', 'kill_quickly'],
        'description': 'Hides in stone, calls reinforcements',
        'weakness': 'bane_of_arthropods'
    },
    'witch': {
        'type': 'hostile',
        'health': 26,
        'damage': 2,  # Potions vary
        'behavior': 'attack',
        'drops': ['glass_bottle', 'glowstone_dust', 'gunpowder', 'redstone', 'spider_eye', 'sugar', 'stick', 'potion'],
        'drop_chances': [0.17, 0.17, 0.17, 0.17, 0.17, 0.17, 0.17, 0.17],
        'experience': [3.0],
        'categories': ['hostile', 'ranged', 'rare'],
        'tamable': False,
        'size': 'medium',
        'width': 0.6,
        'height': 1.95,
        'danger_level': 'high',
        'abilities': ['throw_potions', 'drink_potions', 'heal'],
        'potions': ['harm', 'poison', 'slowness', 'healing'],
        'strategies': ['attack_from_distance', 'use_shield', 'burn'],
        'description': 'Throws splash potions, drinks healing potions',
        'spawns': ['swamp_hut', 'raids']
    },

    # ============================================================
    # NETHER HOSTILE MOBS
    # ============================================================

    'blaze': {
        'type': 'hostile',
        'health': 20,
        'damage': 6,
        'behavior': 'attack',
        'drops': ['blaze_rod', 'experience_bottle'],
        'drop_chances': [0.5, 0.5],
        'experience': [2.0, 1.0],
        'categories': ['nether', 'hostile', 'flying', 'boss'],
        'tamable': False,
        'size': 'medium',
        'width': 0.6,
        'height': 1.8,
        'danger_level': 'high',
        'flying': True,
        'abilities': ['fireball', 'flight', 'hover'],
        'fireball_damage': 5,
        'fireballs': 3,
        'immunity': ['fire', 'lava'],
        'spawn_condition': 'nether_fortress',
        'strategies': ['snowball_attack', 'strafe', 'use_shield'],
        'description': 'Flying fire shooter, shoots 3 fireballs',
        'spawns': 'nether_fortress'
    },
    'wither_skeleton': {
        'type': 'hostile',
        'health': 20,
        'damage': 8,
        'behavior': 'attack',
        'drops': ['coal', 'bone', 'wither_rose_skull'],
        'drop_chances': [0.5, 0.5, 0.025],
        'experience': [1.0, 1.0, 3.0],
        'categories': ['nether', 'hostile', 'rare'],
        'tamable': False,
        'size': 'tall',
        'width': 0.7,
        'height': 2.4,
        'danger_level': 'very_high',
        'weapon': 'stone_sword',
        'wither_rose_chance': 0.5,
        'abilities': ['wither_effect', 'sword_attack'],
        'wither_duration': 10,
        'spawn_condition': 'nether_fortress',
        'strategies': ['use_shield', 'attack_from_distance', 'drink_milk'],
        'description': 'Applies wither effect, rare skull drop',
        'spawns': 'nether_fortress'
    },
    'ghast': {
        'type': 'hostile',
        'health': 30,
        'damage': 0,  # Fireball explosion
        'behavior': 'attack',
        'drops': ['ghast_tear', 'gunpowder'],
        'drop_chances': [0.4, 0.4],
        'experience': [1.0, 1.0],
        'categories': ['nether', 'hostile', 'flying', 'ranged'],
        'tamable': False,
        'size': 'large',
        'width': 4,
        'height': 3,
        'danger_level': 'high',
        'flying': True,
        'abilities': ['fireball', 'explosion'],
        'fireball_damage': 8,
        'explosion_radius': 1,
        'attack_range': 100,
        'immune_to': ['lava', 'fire', 'fall_damage'],
        'spawn_condition': 'nether_wastes',
        'strategies': ['shoot_in_mid_air', 'hide_terrain', 'reflect_fireballs'],
        'description': 'Flying, shoots explosive fireballs',
        'spawns': ['nether_wastes', 'soul_sand_valley']
    },
    'magma_cube': {
        'type': 'hostile',
        'health': 20,  # Large
        'damage': 6,
        'behavior': 'wander',
        'drops': ['magma_cream'],
        'drop_chances': [1],
        'experience': [1.0],
        'categories': ['nether', 'hostile', 'dangerous'],
        'tamable': False,
        'size': 'variable',
        'width': 0.98,
        'height': 0.98,
        'danger_level': 'high',
        'abilities': ['fire_resistant', 'lava_swim', 'drown_immune', 'split_on_death'],
        'immune_to': ['fire', 'lava', 'fall_damage'],
        'damage_type': 'fire',
        'split_into': ['medium_magma_cube', 'small_magma_cube'],
        'strategies': ['water_bucket', 'knockback', 'attack_final_small'],
        'description': 'Swims in lava, splits on death',
        'spawns': ['nether_wastes', 'basalt_deltas']
    },
    'zoglin': {
        'type': 'hostile',
        'health': 40,
        'damage': 6,
        'behavior': 'attack',
        'drops': ['rotten_flesh'],
        'drop_chances': [1],
        'experience': [1.0],
        'categories': ['nether', 'hostile', 'undead'],
        'tamable': False,
        'size': 'large',
        'width': 1.5,
        'height': 2.0,
        'danger_level': 'medium',
        'abilities': ['attack_everything', 'knockback_resistance'],
        'ignore': ['other_zoglin'],
        'strategies': ['avoid', 'attack_from_distance'],
        'description': 'Zombified hoglin, attacks everything',
        'spawns': ['hoglin_overworld', 'piglin_become']
    },

    # ============================================================
    # END HOSTILE MOBS
    # ============================================================

    'endermite': {
        'type': 'hostile',
        'health': 8,
        'damage': 0,
        'behavior': 'wander',
        'drops': None,
        'categories': ['end', 'hostile', 'rare'],
        'tamable': False,
        'size': 'tiny',
        'width': 0.4,
        'height': 0.3,
        'danger_level': 'low',
        'abilities': ['infest_endermen', 'spawn_endermen'],
        'hostile_when': ['player_attacks', 'endermen_nearby'],
        'spawn_from': 'ender_pearl_land',
        'strategies': ['avoid_angering_endermen', 'kill_quickly'],
        'description': 'Spawns from thrown ender pearls, angers endermen',
        'lifespan': '2_minutes'
    },
    'shulker': {
        'type': 'hostile',
        'health': 30,
        'damage': 4,
        'behavior': 'defend',
        'drops': ['shulker_shell'],
        'drop_chances': [0.5],
        'experience': [5.0],
        'categories': ['end', 'hostile', 'ranged'],
        'tamable': False,
        'size': 'medium',
        'width': 1,
        'height': 1,
        'danger_level': 'high',
        'abilities': ['shoot_bullet', 'levitation', 'hide_in_shell'],
        'immunity': ['levitation'],
        'bullet_effect': 'levitation',
        'strategies': ['attack_while_open', 'use_shield', 'avoid_bullets'],
        'description': 'Shoots levitation bullets, hides in shell',
        'spawns': 'end_city'
    },

    # ============================================================
    # RAID MOBS (Illagers)
    # ============================================================

    'vindicator': {
        'type': 'hostile',
        'health': 20,
        'damage': 8,  # Easy: 3, Normal: 5, Hard: 8
        'behavior': 'attack',
        'drops': ['emerald', 'iron_ingot'],
        'drop_chances': [0.16, 0.03],
        'experience': [3.0],
        'categories': ['illager', 'hostile', 'raid'],
        'tamable': False,
        'size': 'medium',
        'width': 0.6,
        'height': 1.95,
        'danger_level': 'high',
        'weapon': 'iron_axe',
        'abilities': ['charge_attack', 'johnny_attack'],
        'johnny_chance': 0.01,  # Attacks all mobs
        'spawns': ['raid', 'woodland_mansion', 'patrol'],
        'strategies': ['use_shield', 'attack_from_distance'],
        'description': 'Charges with axe, Johnny variant attacks all'
    },
    'evoker': {
        'type': 'hostile',
        'health': 24,
        'damage': 6,
        'behavior': 'attack',
        'drops': ['emerald', 'totem_of_undying', 'book'],
        'drop_chances': [0.16, 0.01, 0.03],
        'experience': [10.0],
        'categories': ['illager', 'hostile', 'raid', 'rare'],
        'tamable': False,
        'size': 'medium',
        'width': 0.6,
        'height': 1.95,
        'danger_level': 'very_high',
        'abilities': ['summon_vex', 'fang_attack', 'woolo_attack'],
        'attacks': ['vex_summon', 'fang_lines', 'woolo_teleport'],
        'strategies': ['kill_quickly', 'use_shield', 'avoid_fangs'],
        'description': 'Summons vexes, deadly fang attack',
        'spawns': ['raid', 'woodland_mansion']
    },
    'vex': {
        'type': 'hostile',
        'health': 14,
        'damage': 9,  # Hard: 13
        'behavior': 'attack',
        'drops': None,
        'categories': ['illager', 'hostile', 'summoned', 'flying'],
        'tamable': False,
        'size': 'small',
        'width': 0.4,
        'height': 0.8,
        'danger_level': 'very_high',
        'flying': True,
        'abilities': ['fly', 'phase_through_walls', 'evoker_summon'],
        'summoned_by': 'evoker',
        'lifespan': '30-120_seconds',
        'strategies': ['attack_with_sword', 'use_shield'],
        'description': 'Flying, phases through walls, summoned by evoker'
    },
    'pillager': {
        'type': 'hostile',
        'health': 20,
        'damage': 2,  # Crossbow
        'behavior': 'attack',
        'drops': ['arrow', 'emerald', 'crossbow', 'iron_ingot'],
        'drop_chances': [0.5, 0.16, 0.03, 0.03],
        'experience': [3.0],
        'categories': ['illager', 'hostile', 'ranged', 'raid'],
        'tamable': False,
        'size': 'medium',
        'width': 0.6,
        'height': 1.95,
        'danger_level': 'medium',
        'weapon': 'crossbow',
        'abilities': ['ranged_attack', 'patrol'],
        'spawns': ['raid', 'patrol', 'woodland_mansion'],
        'strategies': ['use_shield', 'get_up_close', 'dodge_arrows'],
        'description': 'Crossbow user, patrols with banner',
        'patrol_captain': 'ominous_banner'
    },
    'ravager': {
        'type': 'hostile',
        'health': 100,
        'damage': 7,  # Also has roar attack
        'behavior': 'attack',
        'drops': ['saddle'],
        'drop_chances': [0.5],
        'experience': [20.0],
        'categories': ['illager', 'hostile', 'raid', 'boss'],
        'tamable': False,
        'size': 'large',
        'width': 1.95,
        'height': 2.2,
        'danger_level': 'extreme',
        'abilities': ['charge', 'roar', 'destroy_leaves'],
        'immune_to': ['knockback'],
        'strategies': ['use_shield', 'attack_from_distance', 'avoid_roar'],
        'description': 'Powerful beast, destroys leaves, deadly roar',
        'spawns': 'raid_wave_5+'
    },
    'illusioner': {
        'type': 'hostile',
        'health': 32,
        'damage': 2,
        'behavior': 'attack',
        'drops': None,
        'categories': ['illager', 'hostile', 'unused'],
        'tamable': False,
        'size': 'medium',
        'width': 0.6,
        'height': 1.95,
        'danger_level': 'high',
        'abilities': ['blindness', 'clones', 'bow_attack'],
        'strategies': ['use_shield', 'find_real_one'],
        'description': 'Creates illusions, casts blindness',
        'note': 'Unused in vanilla, spawns via commands'
    },
    'witch': {
        'type': 'hostile',
        'health': 26,
        'damage': 2,
        'behavior': 'attack',
        'drops': ['glass_bottle', 'glowstone_dust', 'gunpowder', 'redstone', 'spider_eye', 'sugar', 'stick', 'potion'],
        'drop_chances': [0.17, 0.17, 0.17, 0.17, 0.17, 0.17, 0.17, 0.17],
        'experience': [3.0],
        'categories': ['hostile', 'raid', 'ranged'],
        'tamable': False,
        'size': 'medium',
        'width': 0.6,
        'height': 1.95,
        'danger_level': 'high',
        'abilities': ['throw_potions', 'drink_potions', 'heal'],
        'strategies': ['attack_from_distance', 'burn'],
        'description': 'Throws splash potions',
        'spawns': ['swamp_hut', 'raid']
    },

    # ============================================================
    # BOSS MOBS
    # ============================================================

    'ender_dragon': {
        'type': 'boss',
        'health': 200,
        'damage': 15,
        'behavior': 'attack',
        'drops': ['dragon_egg', 'elytra', 'dragon_breath', 'end_crystal'],
        'drop_chances': [1, 1, 1, 1],
        'experience': [12000],
        'categories': ['boss', 'end', 'legendary'],
        'size': 'boss',
        'width': 16,
        'height': 8,
        'danger_level': 'extreme',
        'abilities': ['dragon_breath', 'fly', 'charge', 'perch', 'destroy_crystal'],
        'immune_to': ['knockback', 'fall_damage', 'all_effects'],
        'phases': ['circle', 'perch', 'charge', 'death'],
        'summon_condition': 'end_portal_activated',
        'strategies': ['destroy_crystals', 'shoot_while_flying', 'bed_exploit'],
        'description': 'Final boss, requires strategy',
        'respawns': True
    },
    'wither': {
        'type': 'boss',
        'health': 300,
        'damage': 8,
        'behavior': 'attack',
        'drops': ['nether_star'],
        'drop_chances': [1],
        'experience': [100],
        'categories': ['boss', 'nether', 'legendary'],
        'size': 'boss',
        'width': 3,
        'height': 3.5,
        'danger_level': 'extreme',
        'abilities': ['wither_effect', 'wither_skull', 'dash', 'fly', 'immortal', 'spawn_witherskeletons'],
        'immune_to': ['wither', 'fire', 'lava'],
        'spawn_condition': 'wither_invocation',
        'phases': ['normal', 'half_health_invulnerable', 'armor_mode'],
        'strategies': ['shoot_skulls_back', 'drink_milk', 'hide', 'use_bow'],
        'description': 'Decaying boss, wither effect, three skulls',
        'summon': ['soul_sand', 'wither_skull_skulls']
    },
    'warden': {
        'type': 'boss',
        'health': 500,
        'damage': 15,  # Melee: 15, Sonic boom: 10
        'behavior': 'detect',
        'drops': ['sculk_catalyst'],
        'drop_chances': [1],
        'experience': [100],
        'categories': ['boss', 'underground', 'legendary'],
        'size': 'boss',
        'width': 2.7,
        'height': 2.7,
        'danger_level': 'extreme',
        'abilities': ['blindness', 'sonic_boom', 'soul_detect', 'dig', 'charge'],
        'sensing': 'vibration_and_smell',
        'blind': True,
        'immune_to': ['knockback', 'fire', 'lava'],
        'spawns_from': 'sculk_shrieker',
        'strategies': ['sneak', 'throw_projectiles', 'snowballs', 'avoid_sonic_boom'],
        'description': 'Blind but powerful, senses vibrations',
        'one_shot': True
    },
    'elder_guardian': {
        'type': 'boss',
        'health': 80,
        'damage': 8,
        'behavior': 'defend',
        'drops': ['wet_sponge', 'prismarine_shard', 'prismarine_crystals', 'raw_cod', 'raw_salmon'],
        'drop_chances': [1, 0.5, 0.5, 0.16, 0.16],
        'experience': [10],
        'categories': ['boss', 'aquatic', 'legendary'],
        'size': 'boss',
        'width': 2.7,
        'height': 2.7,
        'danger_level': 'high',
        'abilities': ['laser_beam', 'mining_fatigue', 'thorns', 'spike_damage'],
        'laser_damage': 8,
        'laser_charge_time': 2,
        'mining_fatigue_level': 3,
        'strategies': ['kill_underwater', 'use_sword', 'avoid_laser', 'milk_fatigue'],
        'description': 'Ocean monument boss, mining fatigue',
        'spawns': ['ocean_monument', 'raid_defense']
    },
    'red_dragon': {
        'type': 'boss',
        'health': 250,
        'damage': 18,
        'behavior': 'attack',
        'drops': None,
        'categories': ['boss', 'unused'],
        'tamable': False,
        'size': 'boss',
        'width': 16,
        'height': 8,
        'danger_level': 'extreme',
        'abilities': ['fly', 'fire_breath'],
        'note': 'Removed from game, unused',
        'description': 'Unused red dragon variant'
    },

    # ============================================================
    # SPECIAL MOBS
    # ============================================================

    'giant': {
        'type': 'hostile',
        'health': 100,
        'damage': 0,
        'behavior': 'attack',
        'drops': None,
        'categories': ['hostile', 'unused'],
        'tamable': False,
        'size': 'giant',
        'width': 3.6,
        'height': 12,
        'danger_level': 'high',
        'note': 'Unused, only spawns via commands',
        'description': 'Giant zombie, unused in vanilla'
    },
    'killer_bunny': {
        'type': 'hostile',
        'health': 3,
        'damage': 8,
        'behavior': 'attack',
        'drops': ['rabbit', 'rabbit_foot', 'rabbit_hide'],
        'categories': ['rare', 'hostile', 'easter_egg'],
        'tamable': False,
        'size': 'tiny',
        'width': 0.4,
        'height': 0.5,
        'danger_level': 'high',
        'name': 'The Killer Bunny',
        'strategies': ['attack_from_distance', 'run_away'],
        'description': 'Rare hostile rabbit variant, Easter egg',
        'spawn_chance': 'very_rare'
    },
    'zombie_horse': {
        'type': 'passive',
        'health': 15,
        'damage': 0,
        'behavior': 'wander',
        'drops': ['rotten_flesh'],
        'drop_chances': [1],
        'categories': ['undead', 'unused'],
        'tamable': False,
        'size': 'large',
        'width': 1.4,
        'height': 1.6,
        'danger_level': 'none',
        'note': 'Unused, cannot be tamed',
        'description': 'Unused zombie horse variant'
    },

    # ============================================================
    # UTILITY/FRIENDLY MOBS
    # ============================================================

    'allay': {
        'type': 'passive',
        'health': 20,
        'damage': 0,
        'behavior': 'collect',
        'drops': None,
        'categories': ['passive', 'helpful', 'rare'],
        'tamable': False,
        'size': 'tiny',
        'width': 0.35,
        'height': 0.6,
        'danger_level': 'none',
        'flying': True,
        'abilities': ['collect_items', 'deliver_items', 'dance'],
        'strategies': ['give_item', 'follow_note_block'],
        'description': 'Collects and delivers items, dances to music',
        'vote_winner': True,
        'spawns': ['pillager_outpost', 'woodland_mansion']
    },
    'villager': {
        'type': 'passive',
        'health': 20,
        'damage': 0,
        'behavior': 'work',
        'drops': None,
        'categories': ['passive', 'npc', 'trading'],
        'tamable': False,
        'size': 'adult',
        'danger_level': 'none',
        'abilities': ['trade', 'work', 'sleep', 'gossip', 'breed'],
        'strategies': ['trade', 'employ', 'breed', 'protect'],
        'description': 'Villager with trading and jobs',
        'priority': 'high'
    },
}

# Danger level ordering
DANGER_LEVELS = {
    'none': 0,
    'low': 1,
    'medium': 2,
    'high': 3,
    'very_high': 4,
    'extreme': 5
}

# Helper functions
def get_mob_info(mob_name: str) -> dict:
    """Get complete information about a mob"""
    return MOB_DATABASE.get(mob_name, {})

def get_mob_danger_level(mob_name: str) -> str:
    """Get danger level of a mob"""
    mob = MOB_DATABASE.get(mob_name, {})
    return mob.get('danger_level', 'unknown')

def is_mob_hostile(mob_name: str) -> bool:
    """Check if a mob is hostile"""
    mob = MOB_DATABASE.get(mob_name, {})
    mob_type = mob.get('type', 'passive')
    return mob_type in ['hostile', 'boss']

def is_mob_boss(mob_name: str) -> bool:
    """Check if a mob is a boss"""
    mob = MOB_DATABASE.get(mob_name, {})
    return mob.get('type') == 'boss'

def get_mob_drops(mob_name: str) -> list:
    """Get drops from a mob"""
    mob = MOB_DATABASE.get(mob_name, {})
    return mob.get('drops', [])

def get_mob_strategies(mob_name: str) -> list:
    """Get combat strategies against a mob"""
    mob = MOB_DATABASE.get(mob_name, {})
    return mob.get('strategies', [])

def get_mob_health(mob_name: str) -> int:
    """Get mob health"""
    mob = MOB_DATABASE.get(mob_name, {})
    return mob.get('health', 10)

def get_mob_damage(mob_name: str) -> int:
    """Get mob damage"""
    mob = MOB_DATABASE.get(mob_name, {})
    return mob.get('damage', 0)

def get_mob_weakness(mob_name: str) -> list:
    """Get mob weaknesses"""
    mob = MOB_DATABASE.get(mob_name, {})
    return mob.get('weakness', [])

def get_mob_abilities(mob_name: str) -> list:
    """Get mob abilities"""
    mob = MOB_DATABASE.get(mob_name, {})
    return mob.get('abilities', [])

def is_mob_tameable(mob_name: str) -> bool:
    """Check if a mob can be tamed"""
    mob = MOB_DATABASE.get(mob_name, {})
    return mob.get('tamable', False)

def get_mob_tame_food(mob_name: str) -> list:
    """Get food to tame a mob"""
    mob = MOB_DATABASE.get(mob_name, {})
    return mob.get('tame_food', [])

def get_mob_breed_food(mob_name: str) -> list:
    """Get food to breed a mob"""
    mob = MOB_DATABASE.get(mob_name, {})
    return mob.get('breed_food', [])

def can_mob_ride(mob_name: str) -> bool:
    """Check if a mob can be ridden"""
    mob = MOB_DATABASE.get(mob_name, {})
    return mob.get('rideable', False)

def get_mobs_by_category(category: str) -> list:
    """Get all mobs in a category"""
    result = []
    for mob_name, mob_data in MOB_DATABASE.items():
        if category in mob_data.get('categories', []):
            result.append(mob_name)
    return result

def get_hostile_mobs() -> list:
    """Get all hostile mobs"""
    return get_mobs_by_category('hostile')

def get_passive_mobs() -> list:
    """Get all passive mobs"""
    return get_mobs_by_category('passive')

def get_boss_mobs() -> list:
    """Get all boss mobs"""
    return get_mobs_by_category('boss')

def get_tameable_mobs() -> list:
    """Get all tameable mobs"""
    result = []
    for mob_name, mob_data in MOB_DATABASE.items():
        if mob_data.get('tamable', False):
            result.append(mob_name)
    return result

def get_mob_priority(mob_name: str) -> str:
    """Get priority level of a mob"""
    mob = MOB_DATABASE.get(mob_name, {})
    return mob.get('priority', 'medium')

def should_avoid_mob(mob_name: str) -> bool:
    """Check if a mob should be avoided"""
    danger = get_mob_danger_level(mob_name)
    return DANGER_LEVELS.get(danger, 0) >= DANGER_LEVELS['high']

def get_mob_description(mob_name: str) -> str:
    """Get mob description"""
    mob = MOB_DATABASE.get(mob_name, {})
    return mob.get('description', 'No description available')

def get_mob_biome(mob_name: str) -> list:
    """Get biome(s) where mob spawns"""
    mob = MOB_DATABASE.get(mob_name, {})
    biome = mob.get('biome', [])
    if isinstance(biome, str):
        return [biome]
    return biome

def compare_mob_danger(mob1: str, mob2: str) -> int:
    """Compare danger levels of two mobs
    Returns: 1 if mob1 is more dangerous, -1 if mob2 is more dangerous, 0 if equal
    """
    danger1 = get_mob_danger_level(mob1)
    danger2 = get_mob_danger_level(mob2)
    level1 = DANGER_LEVELS.get(danger1, 0)
    level2 = DANGER_LEVELS.get(danger2, 0)

    if level1 > level2:
        return 1
    elif level1 < level2:
        return -1
    else:
        return 0

def get_weapons_effective_against(mob_name: str) -> list:
    """Get recommended weapons against a mob"""
    mob = MOB_DATABASE.get(mob_name, {})
    strategies = mob.get('strategies', [])

    weapons = []
    for strategy in strategies:
        if 'sword' in strategy.lower():
            weapons.append('sword')
        if 'bow' in strategy.lower() or 'distance' in strategy.lower():
            weapons.append('bow')
        if 'shield' in strategy.lower():
            weapons.append('shield')
        if 'water' in strategy.lower():
            weapons.append('water_bucket')
        if 'snowball' in strategy.lower():
            weapons.append('snowball')

    return weapons if weapons else ['sword']

def get_mob_experience_reward(mob_name: str) -> int:
    """Get experience reward from killing a mob"""
    mob = MOB_DATABASE.get(mob_name, {})
    exp = mob.get('experience', [0])
    return max(exp) if exp else 0
