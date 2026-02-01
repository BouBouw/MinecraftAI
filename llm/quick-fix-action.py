#!/usr/bin/env python3
"""
Quick fix for select_action() return value
"""

file_path = 'llm/python/training/real_minecraft_trainer.py'

# Read the file
with open(file_path, 'r') as f:
    content = f.read()

# Check if it needs fixing
if 'action_data[0] if isinstance(action_data, tuple)' in content:
    print("✅ Already fixed")
    exit(0)

# Fix the action extraction
old_action = '''                # Get action from agent
                action = self.agent.select_action(observation)

                # Execute action in real Minecraft
                observation, reward, done, truncated, info = await self.env.step(action)'''

new_action = '''                # Get action from agent (returns tuple: action, log_prob, value)
                action_data = self.agent.select_action(observation)
                action = action_data[0] if isinstance(action_data, tuple) else action_data

                # Execute action in real Minecraft
                observation, reward, done, truncated, info = await self.env.step(action)'''

if old_action in content:
    content = content.replace(old_action, new_action)

    # Write back
    with open(file_path, 'w') as f:
        f.write(content)

    print("✅ Fixed select_action() to extract action from tuple")
else:
    print("⚠️  Could not find the pattern to fix")
