#!/usr/bin/env python3
"""
Fix action mapping - map network outputs (0-8) to implemented action IDs
"""

file_path = 'llm/python/training/real_minecraft_trainer.py'

# Read the file
with open(file_path, 'r') as f:
    content = f.read()

# Check if it needs fixing
if 'ACTION_MAPPING' in content:
    print("✅ Action mapping already added")
    exit(0)

# Add action mapping after the logger import (around line 26)
old_logger = "logger = get_logger(__name__)\n\n\nclass RealMinecraftTrainer:"

new_logger = """logger = get_logger(__name__)

# Map network outputs (0-8) to actual implemented action IDs
# Network outputs 9 actions, but we need to map to the specific IDs the bridge implements
ACTION_MAPPING = {
    0: 0,   # NOOP
    1: 1,   # MOVE_FORWARD
    2: 2,   # MOVE_BACKWARD
    3: 3,   # MOVE_LEFT
    4: 4,   # MOVE_RIGHT
    5: 5,   # JUMP
    6: 13,  # SELECT_SLOT
    7: 19,  # PLACE_BLOCK
    8: 21,  # DIG_FORWARD
}


class RealMinecraftTrainer:"""

if old_logger in content:
    content = content.replace(old_logger, new_logger)
    print("✅ Added ACTION_MAPPING")
else:
    print("⚠️  Could not find logger section")
    print("Looking for:", repr(old_logger[:50]))
    exit(1)

# Now update the action extraction to use the mapping (lines 120-129)
old_action = """                # Get action from agent (returns tuple: action, log_prob, value)
                action_data = self.agent.select_action(observation)
                # Handle both tuple (action, log_prob, value) and int (action) returns
                if isinstance(action_data, tuple):
                    action_int = action_data[0]
                else:
                    action_int = action_data

                # Step expects a dict with 'action_type' key
                action = {'action_type': action_int}"""

new_action = """                # Get action from agent (returns tuple: action, log_prob, value)
                action_data = self.agent.select_action(observation)
                # Handle both tuple (action, log_prob, value) and int (action) returns
                if isinstance(action_data, tuple):
                    network_action = action_data[0]
                else:
                    network_action = action_data

                # Map network output (0-8) to actual implemented action ID
                actual_action_id = ACTION_MAPPING[network_action]
                action = {'action_type': actual_action_id}"""

if old_action in content:
    content = content.replace(old_action, new_action)
    print("✅ Updated action extraction to use mapping")
else:
    print("⚠️  Could not find action extraction code")
    exit(1)

# Write back
with open(file_path, 'w') as f:
    f.write(content)

print("✅ Action mapping fix applied!")
print("   Network outputs 0-8 will be mapped to:", [0, 1, 2, 3, 4, 5, 13, 19, 21])
