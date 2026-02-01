#!/usr/bin/env python3
"""
Fix to extract observation from action_complete message
"""

file_path = 'llm/python/bridge/minecraft_bot_bridge.py'

# Read the file
with open(file_path, 'r') as f:
    content = f.read()

# Check if it needs fixing
if "'observation'" in content and "_handle_action_complete" in content:
    # Check if observation is already being extracted
    if "observation_data = data.get('observation')" in content:
        print("✅ Observation extraction already in place")
        exit(0)

# Update _handle_action_complete to also update current_state from observation
old_handler = """    async def _handle_action_complete(self, data: Dict[str, Any]):
        \"\"\"Handle action completion result\"\"\"
        success = data.get('success', False)
        action = data.get('action', {})

        # Store result and set event
        self._last_action_result = data
        self._action_complete_event.set()

        logger.debug(f"Action completed: success={success}")"""

# We need to check if the event fix was already applied
if "_action_complete_event" in content:
    # Event fix was applied, update this version
    new_handler = """    async def _handle_action_complete(self, data: Dict[str, Any]):
        \"\"\"Handle action completion result\"\"\"
        success = data.get('success', False)
        action = data.get('action', {})

        # Store result and set event
        self._last_action_result = data
        self._action_complete_event.set()

        # Update current_state from observation if included
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

    if old_handler in content:
        content = content.replace(old_handler, new_handler)
        print("✅ Updated _handle_action_complete to extract observation")
    else:
        # Try finding the version without event
        old_handler_no_event = """    async def _handle_action_complete(self, data: Dict[str, Any]):
        \"\"\"Handle action completion result\"\"\"
        success = data.get('success', False)
        action = data.get('action', {})

        logger.debug(f"Action completed: success={success}")"""

        new_handler_no_event = """    async def _handle_action_complete(self, data: Dict[str, Any]):
        \"\"\"Handle action completion result\"\"\"
        success = data.get('success', False)
        action = data.get('action', {})

        # Update current_state from observation if included
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

        if old_handler_no_event in content:
            content = content.replace(old_handler_no_event, new_handler_no_event)
            print("✅ Updated _handle_action_complete to extract observation")
        else:
            print("⚠️  Could not find _handle_action_complete")
            exit(1)
else:
    print("⚠️  Event fix not yet applied. Please run fix-action-wait.py first")
    exit(1)

# Write back
with open(file_path, 'w') as f:
    f.write(content)

print("✅ Observation extraction fix applied!")
