#!/usr/bin/env python3
"""
Add debug logging and better error handling for observations
"""

file_path = 'llm/python/bridge/minecraft_bot_bridge.py'

# Read the file
with open(file_path, 'r') as f:
    content = f.read()

# 1. Add debug logging to _handle_action_complete
old_handler = """        # Update current_state from observation if included
        observation_data = data.get('observation')
        if observation_data:
            self.current_state = BotState(
                position=observation_data.get('position', {}),
                rotation=observation_data.get('rotation', {}),
                health=observation_data.get('health', 20),
                food=observation_data.get('food', 20),
                saturation=observation_data.get('saturation', 20),
                on_ground=observation_data.get('on_ground', False),
                in_water=observation_data.get('in_water', False),
                inventory=observation_data.get('inventory', []),
                held_item=observation_data.get('hotbar_selected', 0),
                armor=observation_data.get('armor', {}),
                nearby_entities=observation_data.get('nearby_entities', []),
                time_of_day=observation_data.get('time_of_day', 0),
                is_raining=observation_data.get('is_raining', False),
                biome_id=observation_data.get('biome_id', 0)
            )

        logger.debug(f"Action completed: success={success}")"""

new_handler = """        # Update current_state from observation if included
        observation_data = data.get('observation')
        if observation_data:
            logger.debug(f"Received observation: {list(observation_data.keys())}")
            self.current_state = BotState(
                position=observation_data.get('position', {}),
                rotation=observation_data.get('rotation', {}),
                health=observation_data.get('health', 20),
                food=observation_data.get('food', 20),
                saturation=observation_data.get('saturation', 20),
                on_ground=observation_data.get('on_ground', False),
                in_water=observation_data.get('in_water', False),
                inventory=observation_data.get('inventory', []),
                held_item=observation_data.get('hotbar_selected', 0),
                armor=observation_data.get('armor', {}),
                nearby_entities=observation_data.get('nearby_entities', []),
                time_of_day=observation_data.get('time_of_day', 0),
                is_raining=observation_data.get('is_raining', False),
                biome_id=observation_data.get('biome_id', 0)
            )
            logger.info(f"✅ Updated state: health={self.current_state.health}, food={self.current_state.food}")
        else:
            logger.warning("⚠️  No observation in action_complete message")

        logger.debug(f"Action completed: success={success}")"""

if old_handler in content:
    content = content.replace(old_handler, new_handler)
    print("✅ Added debug logging to _handle_action_complete")
else:
    print("⚠️  Could not find exact pattern for _handle_action_complete")
    print("Looking for observation_data assignment...")

# 2. Update get_observation to handle missing current_state with defaults
old_get_obs = """    async def get_observation(self) -> Dict[str, Any]:
        \"\"\"
        Get current observation from bot

        Returns:
            Current bot state as observation
        \"\"\"
        if not self.connected or not self.ws:
            logger.error("Not connected to bot")
            return {}

        # Don't request observation - bridge sends it automatically
        # await self.ws.send(json.dumps({'type': 'get_observation'}))

        # Wait for observation (with timeout)
        # Will be handled by _handle_observation

        # Return cached state
        if self.current_state:
            return {
                'position': self.current_state.position,
                'rotation': self.current_state.rotation,
                'health': self.current_state.health,
                'food': self.current_state.food,
                'saturation': self.current_state.saturation,
                'on_ground': self.current_state.on_ground,
                'in_water': self.current_state.in_water,
                'inventory': self.current_state.inventory,
                'held_item': self.current_state.held_item,
                'armor': self.current_state.armor,
                'nearby_entities': self.current_state.nearby_entities,
                'time_of_day': self.current_state.time_of_day,
                'is_raining': self.current_state.is_raining,
                'biome_id': self.current_state.biome_id,
            }
        else:
            return {}"""

new_get_obs = """    async def get_observation(self) -> Dict[str, Any]:
        \"\"\"
        Get current observation from bot

        Returns:
            Current bot state as observation
        \"\"\"
        if not self.connected or not self.ws:
            logger.error("Not connected to bot")
            return self._get_default_observation()

        # Return cached state
        if self.current_state:
            obs = {
                'position': self.current_state.position,
                'rotation': self.current_state.rotation,
                'health': self.current_state.health,
                'food': self.current_state.food,
                'saturation': self.current_state.saturation,
                'on_ground': self.current_state.on_ground,
                'in_water': self.current_state.in_water,
                'inventory': self.current_state.inventory,
                'held_item': self.current_state.held_item,
                'armor': self.current_state.armor,
                'nearby_entities': self.current_state.nearby_entities,
                'time_of_day': self.current_state.time_of_day,
                'is_raining': self.current_state.is_raining,
                'biome_id': self.current_state.biome_id,
            }
            logger.debug(f"get_observation: health={obs['health']}, food={obs['food']}")
            return obs
        else:
            logger.warning("current_state is None, returning defaults")
            return self._get_default_observation()

    def _get_default_observation(self) -> Dict[str, Any]:
        \"\"\"Return default observation when state is not available\"\"\"
        return {
            'position': {'x': 0, 'y': 64, 'z': 0},
            'rotation': {'yaw': 0, 'pitch': 0},
            'health': 20,
            'food': 20,
            'saturation': 20,
            'on_ground': True,
            'in_water': False,
            'inventory': [],
            'held_item': 0,
            'armor': {},
            'nearby_entities': [],
            'time_of_day': 0,
            'is_raining': False,
            'biome_id': 1
        }"""

if old_get_obs in content:
    content = content.replace(old_get_obs, new_get_obs)
    print("✅ Updated get_observation with default fallback")
else:
    print("⚠️  Could not find get_observation pattern")

# Write back
with open(file_path, 'w') as f:
    f.write(content)

print("✅ Observation logging fix applied!")
