"""
Complete Minecraft Redstone Knowledge
Redstone mechanics, circuits, and contraptions
"""

REDSTONE_BASICS = {
    'redstone_wire': {
        'description': 'Transmits power up to 15 blocks',
        'power_levels': '0-15',
        'placement': 'on opaque blocks',
        'signal_type': 'wire',
        'visual': 'dust that glows brighter with more power'
    },
    'redstone_torch': {
        'description': 'Constant power source or inverter',
        'power_output': '15 when powered, 0 when unpowered',
        'functions': ['power_source', 'inverter', 'signal_blocker'],
        'placement': 'on side or top of blocks'
    },
    'redstone_block': {
        'description': 'Strong always-on power source',
        'power_output': '15 (always)',
        'functions': ['compact_power_source', 'movable_power', 'pushable_by_piston'],
        'special': 'powers adjacent blocks in all directions'
    },
    'repeater': {
        'description': 'Extends signal and introduces delay',
        'power_output': '15 (strong signal)',
        'delay': '1-4 ticks (configurable)',
        'functions': ['signal_extension', 'delay', 'diode', 'signal_repeater'],
        'special': 'only accepts signal from back, outputs to front'
    },
    'comparator': {
        'description': 'Compares signals and reads containers',
        'power_output': 'matches input side or subtracts',
        'modes': ['compare', 'subtract'],
        'functions': ['container_reading', 'signal_comparison', 'signal_subtraction', 'signal_diode'],
        'special': 'can detect item levels in containers'
    },
    'piston': {
        'description': 'Pushes blocks and entities',
        'push_distance': '1 block',
        'activation': 'redstone signal',
        'sticky_variant': 'piston_that_also_pulls',
        'functions': ['push_blocks', 'create_doors', 'moving_parts'],
        'limitations': ['cannot_push_bedrock', 'barrier', 'obsidian', 'end_portal']
    },
    'sticky_piston': {
        'description': 'Pushes and pulls blocks',
        'push_distance': '1 block',
        'pull_distance': '1 block',
        'functions': ['push_blocks', 'pull_blocks', 'compact_doors', 'elevators'],
        'special': 'can pull blocks back when retracted'
    },
    'observer': {
        'description': 'Detects block updates and emits pulse',
        'pulse_length': '2 ticks',
        'face': 'detects_block_changes',
        'back': 'outputs_signal',
        'functions': ['crop_farming', 'block_update_detection', 'clock_circuits'],
        'special': 'can detect growth, fluids, entities'
    },
    'hopper': {
        'description': 'Transfers items between containers',
        'transfer_speed': '8 items per 2.5 seconds (2.5 ticks)',
        'functions': ['item_sorting', 'automatic_smelting', 'item_collection'],
        'special': 'can pick up entities, minecart interaction'
    },
    'dispenser': {
        'description': 'Shoots items or uses them',
        'activation': 'redstone signal',
        'functions': ['shooting_arrows', 'placing_water/lava', 'farming', 'mob_transport'],
        'special': 'different actions for different items'
    },
    'dropper': {
        'description': 'Drops items into containers',
        'activation': 'redstone signal',
        'functions': ['item_transfer', 'random_dispensing', 'sorting'],
        'special': 'can deposit into containers'
    },
    'note_block': {
        'description': 'Plays musical notes',
        'note_range': '0-24 (F#3 to F#5)',
        'instrument': 'depends on block below',
        'functions': ['music', 'notification_systems', 'combination_locks'],
        'instruments': {
            'wood': 'bass',
            'sand': 'snare',
            'glass': 'clicks/sticks',
            'stone': 'bass_drum',
            'gold': 'bell',
            'clay': 'flute',
            'packed_ice': 'chime',
            'wool': 'guitar',
            'bone_block': 'xylophone',
            'iron_block': 'bass_guitar',
            'soul_sand': 'cow_bell',
            'pumpkin': 'didgeridoo'
        }
    },
    'target': {
        'description': 'Outputs signal when hit by projectile',
        'signal_strength': 'depends on projectile accuracy',
        'functions': ['target_practice', 'minigames', 'detection'],
        'special': 'emits redstone signal when hit by arrow'
    },
    'lever': {
        'description': 'Toggle switch',
        'signal_output': '15 (on) or 0 (off)',
        'functions': ['power_control', 'switches', 'manual_activation'],
        'toggle': True,
        'sticky': False
    },
    'stone_button': {
        'description': 'Momentary switch',
        'signal_duration': '10 ticks (0.5 seconds)',
        'signal_output': '15',
        'functions': ['impulse_activation', 'doors', 'pistons']
    },
    'wooden_button': {
        'description': 'Longer momentary switch',
        'signal_duration': '15 ticks (0.75 seconds)',
        'signal_output': '15',
        'functions': ['longer_pulses', 'doors', 'pistons']
    },
    'stone_pressure_plate': {
        'description': 'Triggered by all entities and players',
        'signal_output': '15',
        'trigger': 'players_and_mobs',
        'functions': ['traps', 'doors', 'detection']
    },
    'wooden_pressure_plate': {
        'description': 'Triggered only by players/mobs (items dropped)',
        'signal_output': '15',
        'trigger': 'players_and_mobs',
        'functions': ['detection', 'doors']
    },
    'heavy_weighted_pressure_plate': {
        'description': 'Triggered by entities, outputs vary by weight',
        'signal_output': '1-15 based on entity count/weight',
        'trigger': 'mobs_and_items',
        'functions': ['entity_counting', 'item_detection']
    },
    'light_weighted_pressure_plate': {
        'description': 'Triggered by items, outputs vary by count',
        'signal_output': '1-15 based on item count',
        'trigger': 'items_only',
        'functions': ['item_counting', 'sorting']
    },
    'tripwire': {
        'description': 'String that detects entities',
        'signal_output': '15 for 5 ticks when entity passes',
        'placement': 'between tripwire_hooks',
        'functions': ['detection', 'traps', 'security']
    },
    'tripwire_hook': {
        'description': 'Anchor for tripwire',
        'signal_output': '15 when activated',
        'functions': ['tripwire_system', 'detection']
    },
    'daylight_detector': {
        'description': 'Detects time of day',
        'signal_output': 'variable based on sun position',
        'day_max': '15 at noon',
        'night_max': '0 at midnight',
        'functions': ['clocks', 'automatic_day_night_switches', 'solar_panels']
    },
    'sculk_sensor': {
        'description': 'Detects vibrations and emits signal',
        'signal_strength': 'based on vibration distance',
        'range': '8 blocks radius',
        'functions': ['vibration_detection', 'wireless_redstone', 'mob_detection'],
        'special': 'detects walking, placing, breaking, projectiles'
    },
    'calibrated_sculk_sensor': {
        'description': 'Sculk sensor with adjustable sensitivity',
        'signal_strength': 'based on vibration and sensitivity setting',
        'functions': ['fine_tuned_detection', 'wireless_redstone'],
        'special': 'can detect different vibration levels'
    }
}

REDSTONE_COMPONENTS = {
    'power_sources': ['redstone_torch', 'redstone_block', 'lever', 'stone_button', 'wooden_button', 'daylight_detector', 'target', 'sculk_sensor'],
    'transmission': ['redstone_wire', 'repeater', 'comparator'],
    'components': ['piston', 'sticky_piston', 'observer', 'hopper', 'dispenser', 'dropper', 'note_block'],
    'triggers': ['stone_pressure_plate', 'wooden_pressure_plate', 'heavy_weighted_pressure_plate', 'light_weighted_pressure_plate', 'tripwire', 'tripwire_hook', 'target', 'sculk_sensor']
}

COMMON_CIRCUITS = {
    'not_gate': {
        'description': 'Inverts input signal',
        'components': ['redstone_torch'],
        'input': 'any redstone signal',
        'output': 'inverted signal',
        'uses': ['inverter', 'lock_systems', 'memory']
    },
    'repeater_clock': {
        'description': 'Oscillating signal using repeaters',
        'components': ['2 repeaters', 'redstone_wire'],
        'period': '2-8 ticks (adjustable)',
        'uses': ['clocks', 'timers', 'pulsing']
    },
    'hopper_clock': {
        'description': 'Very slow clock using hoppers',
        'components': ['2 hoppers', '2 comparators', '1 item'],
        'period': 'very slow (many seconds)',
        'uses': ['long_timers', 'slow_clocks']
    },
    't_flip_flop': {
        'description': 'Memory cell with toggle',
        'components': ['2 repeaters', '2 redstone_torches', 'redstone_wire'],
        'uses': ['memory', 'toggle_switches', 'latches']
    },
    'rs_nor_latch': {
        'description': 'Set-reset latch',
        'components': ['2 redstone_torches', '2 repeaters'],
        'set_input': 'sets_output_on',
        'reset_input': 'sets_output_off',
        'uses': ['memory', 'control_systems']
    },
    'monostable_circuit': {
        'description': 'Pulse generator',
        'components': ['piston', 'redstone_wire', 'repeater'],
        'output': 'single_pulse_on_trigger',
        'uses': ['pulse_extenders', 'edge_detectors']
    },
    'pulse_extender': {
        'description': 'Lengthens redstone pulses',
        'components': ['repeater', 'redstone_torch', 'piston'],
        'input': 'short_pulse',
        'output': 'longer_pulse',
        'uses': ['extending_signals', 'timing_circuits']
    },
    'pulse_shortener': {
        'description': 'Shortens redstone pulses',
        'components': ['repeater', 'redstone_torch'],
        'input': 'long_pulse',
        'output': 'short_pulse',
        'uses': ['edge_detection', 'timing_circuits']
    },
    'observer_clock': {
        'description': 'Fast clock using observers',
        'components': ['2 observers', 'redstone_wire', 'dirt', 'redstone_block'],
        'period': '1-2 ticks (very fast)',
        'uses': ['fast_clocks', 'rapid_pulses']
    },
    'clock_generator': {
        'description': 'Multi-clock circuit',
        'components': ['multiple_observers', 'pistons', 'repeaters'],
        'outputs': ['multiple_different_periods'],
        'uses': ['complex_timing', 'multiple_timers']
    },
    'randomizer': {
        'description': 'Random output generator',
        'components': ['command_blocks', 'comparators'],
        'uses': ['random_outputs', 'games', 'variations']
    },
    'cellular_automaton': {
        'description': 'Game of Life in redstone',
        'components': ['many_pistons', 'redstone_wire'],
        'uses': ['demonstration', 'simulation']
    },
    'addition': {
        'description': 'Adds two signals',
        'components': ['3 comparators', 'redstone_wire'],
        'input': 'signal_A', 'signal_B',
        'output': 'A + B (capped at 15)',
        'uses': ['signal_combination', 'counting']
    },
    'subtraction': {
        'description': 'Subtracts signals',
        'components': ['1 comparator (subtract mode)'],
        'input': 'signal_from_side', 'signal_from_back',
        'output': 'back - side (min 0)',
        'uses': ['signal_subtraction', 'comparators']
    },
    'multiplexer': {
        'description': 'Selects one of two inputs',
        'components': ['multiple_repeaters', 'redstone_wire'],
        'select': 'choose_input_A_or_B',
        'uses': ['data_selection', 'routing']
    },
    'demultiplexer': {
        'description': 'Routes input to one of two outputs',
        'components': ['multiple_repeaters', 'redstone_wire'],
        'select': 'route_to_A_or_B',
        'uses': ['data_routing', 'distribution']
    },
    'logic_gate_and': {
        'description': 'AND gate',
        'components': ['3 repeaters (torch lock)'],
        'truth_table': 'A AND B',
        'uses': ['logic', 'combination_locks']
    },
    'logic_gate_or': {
        'description': 'OR gate',
        'components': ['direct_wire_connection'],
        'truth_table': 'A OR B',
        'uses': ['logic', 'any_input']
    },
    'logic_gate_xor': {
        'description': 'XOR gate',
        'components': ['2 torch locks', 'inverter'],
        'truth_table': 'A XOR B',
        'uses': ['adders', 'toggle_with_2_inputs']
    },
    'logic_gate_nand': {
        'description': 'NAND gate',
        'components': ['repeater', 'redstone_torches'],
        'truth_table': 'NOT (A AND B)',
        'uses': ['universal_logic']
    },
    'logic_gate_nor': {
        'description': 'NOR gate',
        'components': ['redstone_torch'],
        'truth_table': 'NOT (A OR B)',
        'uses': ['universal_logic']
    },
    'bit_counter': {
        'description': 'Counts pulses or items',
        'components': ['hoppers', 'comparators', 'chest'],
        'output': 'binary_representation',
        'uses': ['item_counting', 'scoreboards', 'statistics']
    },
    'binary_display': {
        'description': 'Shows binary output with lamps',
        'components': ['lamps', 'repeaters'],
        'input': 'binary_signal',
        'uses': ['visual_output', 'displays']
    },
    'shift_register': {
        'description': 'Stores and shifts data',
        'components': ['many_t_flip_flops'],
        'uses': ['data_storage', 'serial_data']
    },
    'decoder': {
        'description': 'Converts binary to one-hot',
        'components': ['AND_gates', 'inverters'],
        'input': 'binary_number',
        'output': 'one_active_line',
        'uses': ['selection', 'routing']
    },
    'encoder': {
        'description': 'Converts one-hot to binary',
        'components': ['OR_gates'],
        'input': 'one_active_input',
        'output': 'binary_number',
        'uses': ['compression', 'priority_encoding']
    }
}

AUTOMATION_SYSTEMS = {
    'automatic_farm': {
        'description': 'Harvests crops automatically',
        'components': ['observer', 'dispenser', 'water', 'hopper'],
        'crops': ['wheat', 'carrot', 'potato', 'beetroot', 'pumpkin', 'melon'],
        'mechanism': 'observer_detects_growth -> triggers_dispenser/harvest',
        'collection': 'hoppers_to_chest'
    },
    'automatic_smelter': {
        'description': 'Auto-smelts items',
        'components': ['hoppers', 'furnace', 'chests'],
        'input': 'hopper_to_furnace',
        'fuel': 'auto_feed_fuel',
        'output': 'hopper_from_furnace_to_chest',
        'expansion': 'multiple_furnaces_parallel'
    },
    'item_sorter': {
        'description': 'Sorts items into different chests',
        'components': ['hoppers', 'comparators', 'chests'],
        'mechanism': 'comparator_detects_item_type -> hopper_routes_to_correct_chest',
        'expansion': 'multiple_sorting_columns'
    },
    'mob_farm': {
        'description': 'Farms mobs automatically',
        'components': ['spawning_platform', 'water_flush', 'hopper_collection', 'kill_mechanism'],
        'types': ['creeper_farm', 'enderman_farm', 'general_mob_farm'],
        'collection': 'hopper_to_chest'
    },
    'iron_farm': {
        'description': 'Farms iron golems',
        'components': ['villager_housing', 'zombie', 'spawn_point', 'lava_kill', 'hopper_collection'],
        'mechanism': 'villagers_summon_golem -> lava_kills_golem -> iron_collected',
        'rate': 'variable_iron_per_hour'
    },
    'gold_farm': {
        'description': 'Farms piglins in nether',
        'components': ['portals', 'zombified_piglin', 'trap', 'loot_collection'],
        'mechanism': 'piglin_portal_spawning -> kill -> drops_collected',
        'location': 'nether'
    },
    'sugar_cane_farm': {
        'description': 'Auto-harvests sugar cane',
        'components': ['pistons', 'observer', 'collection_system'],
        'mechanism': 'observer_detects_growth -> piston_breaks -> item_collected',
        'types': ['flying_machine', 'dual_row', 'bonemeal_speed']
    },
    'bamboo_farm': {
        'description': 'Auto-harvests bamboo',
        'components': ['pistons', 'observer', 'collection'],
        'mechanism': 'observer_detects_height -> piston_breaks_top',
        'special': 'bamboo_grows_tall'
    },
    'cactus_farm': {
        'description': 'Auto-farms cactus',
        'components': ['pistons', 'cactus_layout', 'collection'],
        'mechanism': 'piston_breaks_cactus -> item_collected',
        'special': 'cactus_destroys_items'
    },
    'kelp_farm': {
        'description': 'Auto-harvests kelp',
        'components': ['flying_machine', 'bonemeal'],
        'mechanism': 'breaks_bottom_kelp -> kelp_grows_back',
        'uses': ['dried_kelp_fuel', 'smelting']
    },
    'wool_farm': {
        'description': 'Shears sheep automatically',
        'components': ['sheep', 'dispenser_with_shears', 'grass', 'hopper'],
        'mechanism': 'sheep_eats_grass -> wool_grows -> dispenser_shears -> wool_collected',
        'special': 'sheep_regrows_wool'
    },
    'chicken_egg_farm': {
        'description': 'Collects eggs from chickens',
        'components': ['chickens', 'hopper', 'chest'],
        'mechanism': 'chicken_lays_egg -> hopper_collects',
        'expansion': 'auto_hatching_to_maintain_population'
    },
    'cow_milk_farm': {
        'description': 'Auto-milks cows',
        'components': ['cows', 'dispenser_with_buckets', 'hopper_system'],
        'mechanism': 'detects_cow -> dispenses_empty_bucket -> fills -> collects_milk',
        'special': 'complex_bucket_management'
    },
    'honey_farm': {
        'description': 'Auto-harvests honey',
        'components': ['bees', 'flowers', 'dispenser_with_shears', 'campfire'],
        'mechanism': 'bees_fill_honeycomb -> shears_collect -> campfire_calms_bees',
        'special': 'campfire_prevents_anger'
    },
    'mob_switch': {
        'description': 'Controls mob types',
        'components': ['minecart_with_hopper', 'detector Rails', 'sorting_system'],
        'mechanism': 'detects_mob_type -> routes_to_different_path',
        'uses': ['hostile_passive_separation', 'sorting']
    },
    'xp_farm': {
        'description': 'Farms experience orbs',
        'components': ['spawning_platform', 'kill_method', 'xp_collection'],
        'types': ['end_gateway', 'guardian', 'witch_farm'],
        'collection': 'player_collects_or_hopper_with_mending_repair'
    },
    'storage_system': {
        'description': 'Organized storage with item IO',
        'components': ['chests', 'hoppers', 'item_sorter', 'redstone_control'],
        'features': ['auto_sort', 'input_output', 'overflow_handling'],
        'expansion': 'modular_storage_units'
    },
    'traffic_light': {
        'description': 'Controls flow of entities/items',
        'components': ['pistons', 'redstone_lamps', 'timing_circuit'],
        'uses': ['entity_control', 'minecart_routing', 'visual_indicators']
    },
    'secret_door': {
        'description': 'Hidden door mechanism',
        'components': ['pistons', 'blocks_matching_terrain'],
        'trigger': 'hidden_lever_or_pressure_plate',
        'uses': ['hidden_bases', 'secret_entrances']
    },
    'elevator': {
        'description': 'Vertical transport',
        'types': ['piston_elevator', 'water_elevator', 'bubble_elevator', 'soul_sand_magma_elevator'],
        'components': ['pistons', 'water', 'soul_sand', 'magma_block'],
        'mechanism': 'pistons_push_player_up_or_water_lifts',
        'special': 'vertical_transport'
    },
    'drawbridge': {
        'description': 'Lowerable/raiseable bridge',
        'components': ['pistons', 'sticky_pistons', 'bridge_blocks'],
        'control': 'lever_or_button',
        'uses': ['moat_crossing', 'gate', 'castle_defense']
    },
    'castle_gate': {
        'description': 'Opening portcullis',
        'components': ['sticky_pistons', 'fence_gates_or_fence', 'redstone'],
        'mechanism': 'pistons_raise_and_lower_fence',
        'uses': ['castle_entrance', 'secure_exit']
    },
    'trap_door': {
        'description': 'Hidden trapdoor in floor',
        'components': ['pistons', 'trapdoors', 'pressure_plates'],
        'trigger': 'pressure_plate_or_tripwire',
        'uses': ['mob_traps', 'hidden_entrance', 'security']
    },
    'alarm_system': {
        'description': 'Visual/audio alarm',
        'components': ['not_gate', 'clock', 'redstone_lamp', 'note_block', 'bell'],
        'trigger': 'any_redstone_signal',
        'uses': ['intrusion_detection', 'notification']
    },
    'combination_lock': {
        'description': 'Requires specific input sequence',
        'components': ['multiple_levers', 'logic_gates', 't_flip_flops', 'output'],
        'sequence': 'specific_lever_combination',
        'uses': ['security', 'vault', 'secret_rooms']
    },
    'vending_machine': {
        'description': 'Dispenses items for payment',
        'components': ['dispenser', 'comparators', 'hoppers', 'payment_chest'],
        'mechanism': 'detect_payment -> dispenses_product',
        'uses': ['trading', 'servers', 'economy']
    }
}

TIPS_AND_TRICKS = {
    'signal_strength': {
        'description': 'Signal loses strength over distance',
        'wire': '1 power per block',
        'max_distance': '15 blocks without repeater',
        'solution': 'Use repeaters every 15 blocks'
    },
    'diode_behavior': {
        'description': 'Repeaters and comparators only accept from back',
        'implication': 'Prevents signal backflow',
        'use': 'Create one-way circuits'
    },
    'instant_wire': {
        'description': 'Redstone updates instantly through components',
        'components': ['repeater', 'comparator', 'piston', 'redstone_block'],
        'implication': 'Zero tick delay for these components'
    },
    'torches_as_wires': {
        'description': 'Redstone torch can transmit signal vertically',
        'use': 'Compact vertical transmission'
    },
    'powering_rails': {
        'description': 'Powered rails move minecarts',
        'power_source': 'redstone',
        'speed': 'powered_minecart_moves_fast'
    },
    'detector_rail': {
        'description': 'Emits signal when minecart passes',
        'signal_strength': 'varies_by_cart_contents',
        'uses': ['cart_detection', 'automation']
    },
    'activator_rail': {
        'description': 'Activates minecart contents',
        'uses': ['dispense_minecart', 'hopper_minecart', 'tnt_minecart']
    },
    'observer_updates': {
        'description': 'Observers detect specific changes',
        'detections': ['crop_growth', 'fluid_change', 'block_break', 'block_place', 'container_open'],
        'uses': ['farming', 'automated_detection']
    },
    'piston_update_order': {
        'description': 'Pistons update in specific order',
        'implication': '1-tick_piston_mechanisms_possible',
        'uses': ['instant_transmission', 'super_compact_circuits']
    },
    'comparator_subtraction': {
        'description': 'Subtract mode subtracts side from back',
        'formula': 'output = max(back - side, 0)',
        'uses': ['signal_arithmetic', 'container_level_detection']
    },
    'daylight_sensor_inversion': {
        'description': 'Invert to detect night',
        'method': 'right_click_daylight_detector',
        'uses': 'night_only_activation'
    },
    'sculk_sensor_range': {
        'description': 'Detects vibrations within radius',
        'range': '8 blocks spherical',
        'falloff': 'signal_fades_with_distance',
        'calibration': 'adjust_sensitivity_with_amplifier'
    },
    'rail_powering': {
        'description': 'Efficient rail powering',
        'method': 'powered_rail_every_37_blocks',
        'alternative': 'detector_rail_toggle'
    },
    'compact_logic': {
        'description': 'Smallest logic gates',
        'not_gate': '1_torch',
        'or_gate': 'direct_wire',
        'and_gate': 'torch_lock',
        'uses': 'minimize_space_requirements'
    },
    'zero_tick_farming': {
        'description': 'Pistons can break and replace in 1 tick',
        'requirement': 'specific_piston_update_order',
        'uses': 'ultra_fast_crop_growth',
        'note': 'Some_patches_fixed_this'
    },
    'flying_machine': {
        'description': 'Slime block flying machines',
        'components': ['slime_block', 'honey_block', 'piston', 'sticky_piston'],
        'mechanism': 'alternating_slime_honey_propulsion',
        'uses': 'horizontal_transport', 'farms'
    }
}

def get_component_info(component_name: str) -> dict:
    """Get information about a redstone component"""
    return REDSTONE_BASICS.get(component_name, {})

def get_circuit_info(circuit_name: str) -> dict:
    """Get information about a circuit"""
    return COMMON_CIRCUITS.get(circuit_name, {})

def get_automation_info(automation_type: str) -> dict:
    """Get information about an automation system"""
    return AUTOMATION_SYSTEMS.get(automation_type, {})

def get_power_sources() -> list:
    """Get all power source components"""
    return REDSTONE_COMPONENTS['power_sources']

def get_transmission_components() -> list:
    """Get all signal transmission components"""
    return REDSTONE_COMPONENTS['transmission']

def get_logic_gates() -> list:
    """Get all logic gate circuits"""
    return [name for name in COMMON_CIRCUITS.keys() if 'logic_gate' in name]

def get_clock_circuits() -> list:
    """Get all clock circuits"""
    return [name for name in COMMON_CIRCUITS.keys() if 'clock' in name]

def get_farm_types() -> list:
    """Get all farm types"""
    return [name for name in AUTOMATION_SYSTEMS.keys() if 'farm' in name]

if __name__ == '__main__':
    # Test redstone knowledge
    print("=== REDSTONE KNOWLEDGE ===")
    print(f"Components: {len(REDSTONE_BASICS)}")
    print(f"Circuits: {len(COMMON_CIRCUITS)}")
    print(f"Automation: {len(AUTOMATION_SYSTEMS)}")

    print("\n=== Power Sources ===")
    for source in get_power_sources():
        print(f"- {source}")

    print("\n=== Logic Gates ===")
    for gate in get_logic_gates():
        info = get_circuit_info(gate)
        print(f"{gate}: {info.get('description', 'No description')}")

    print("\n=== Farm Types ===")
    for farm in get_farm_types():
        info = get_automation_info(farm)
        print(f"{farm}: {info.get('description', 'No description')}")
