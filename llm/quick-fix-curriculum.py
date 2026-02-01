#!/usr/bin/env python3
"""
Quick fix for curriculum method calls
"""

file_path = 'llm/python/training/real_minecraft_trainer.py'

# Read the file
with open(file_path, 'r') as f:
    content = f.read()

# Check if it needs fixing
if 'curriculum_stage = self.curriculum.get_current_stage(steps)' in content:
    # Fix 1: Remove steps argument from get_current_stage()
    content = content.replace(
        'curriculum_stage = self.curriculum.get_current_stage(steps)',
        'curriculum_stage = self.curriculum.get_current_stage()'
    )
    print("✅ Fixed get_current_stage() call")

if 'self.curriculum.update_progress(steps)' in content:
    # Fix 2: Add episode_reward argument to update_progress()
    content = content.replace(
        'self.curriculum.update_progress(steps)',
        'self.curriculum.update_progress(steps, self.current_episode_reward)'
    )
    print("✅ Fixed update_progress() call")

if 'curriculum_stage = self.curriculum.get_current_stage()' not in content:
    print("⚠️  File doesn't seem to need fixing")
    exit(0)

# Write back
with open(file_path, 'w') as f:
    f.write(content)

print("✅ All curriculum fixes applied")
