#!/usr/bin/env python3
file_path = 'llm/python/bridge/minecraft_bot_bridge.py'

with open(file_path, 'r') as f:
    content = f.read()

# Fix 1: reset_environment -> reset
content = content.replace(
    "'type': 'reset_environment'}",
    "'type': 'reset'"
)

# Fix 2: execute_action -> action
content = content.replace(
    "'type': 'execute_action'",
    "'type': 'action'"
)

# Fix 3: get_observation should not be sent
# Instead, we should wait for the bridge to send observations automatically
# For now, let's just comment it out or change it
old_get_obs = """        # Request observation
        await self.ws.send(json.dumps({'type': 'get_observation'}))"""

new_get_obs = """        # Don't request observation - bridge sends it automatically
        # await self.ws.send(json.dumps({'type': 'get_observation'}))"""

content = content.replace(old_get_obs, new_get_obs)

with open(file_path, 'w') as f:
    f.write(content)

print("✅ Fixed message types:")
print("   - reset_environment -> reset")
print("   - execute_action -> action")
print("   - get_observation request disabled")
