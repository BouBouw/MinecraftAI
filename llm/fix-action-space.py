#!/usr/bin/env python3
"""
Fix action space to only use implemented actions
Implemented: 0-5, 13, 19, 21 (9 actions total)
"""

file_path = 'llm/config/rl_config.yaml'

with open(file_path, 'r') as f:
    content = f.read()

# Remplacer le nombre d'actions de 50 à 9
content = content.replace('n_actions: 50', 'n_actions: 9')

with open(file_path, 'w') as f:
    f.write(content)

print("✅ Action space limited to 9 implemented actions (0-5, 13, 19, 21)")
