#!/usr/bin/env python3
"""
Fix PPO network to output only 9 actions (0-5, 13, 19, 21)
"""

file_path = 'llm/python/agents/network.py'

with open(file_path, 'r') as f:
    content = f.read()

# Fix: Remplacer 50 par 9 dans l'actor
content = content.replace(
    'self.actor_output = nn.Linear(512, 50)',
    'self.actor_output = nn.Linear(512, 9)'
)

# Fix: Remplacer 50 par 9 dans les commentaires si nécessaire
content = content.replace(
    '# action space (0-49)',
    '# action space (0-8: mapped to 0-5,13,19,21)'
)

with open(file_path, 'w') as f:
    f.write(content)

print("✅ PPO network output limited to 9 actions")
print("   Actions: 0-5 (move), 13 (slot), 19 (place), 21 (dig)")
