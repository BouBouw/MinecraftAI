#!/usr/bin/env python3
file_path = 'llm/python/training/real_minecraft_trainer.py'

with open(file_path, 'r') as f:
    content = f.read()

# Ancien code
old = '''action_data = self.agent.select_action(observation)
                # Handle both tuple (action, log_prob, value) and int (action) returns
                if isinstance(action_data, tuple):
                    action = action_data[0]
                else:
                    action = action_data

                # Execute action in real Minecraft
                observation, reward, done, truncated, info = await self.env.step(action)'''

# Nouveau code
new = '''action_data = self.agent.select_action(observation)
                # Handle both tuple (action, log_prob, value) and int (action) returns
                if isinstance(action_data, tuple):
                    action_int = action_data[0]
                else:
                    action_int = action_data

                # Step expects a dict with 'action_type' key
                action = {'action_type': action_int}
                observation, reward, done, truncated, info = await self.env.step(action)'''

if old in content:
    content = content.replace(old, new)
    with open(file_path, 'w') as f:
        f.write(content)
    print("✅ Fixed - action is now passed as dict")
else:
    print("⚠️  Pattern not found - checking file...")
    if "'action_type': action_int" in content:
        print("✅ Already fixed!")
    else:
        print("❌ Fix not applied")
