#!/usr/bin/env python3
"""
Quick fix for episodic memory curriculum_stage parameter
"""

file_path = 'llm/python/training/real_minecraft_trainer.py'

# Read the file
with open(file_path, 'r') as f:
    content = f.read()

# Check if it needs fixing
if 'episode_id = self.memory.episodic.start_episode(self.curriculum.current_stage_idx)' in content:
    print("✅ Already fixed")
    exit(0)

if 'episode_id = self.memory.episodic.start_episode(curriculum_stage)' in content:
    # Fix: Pass the index instead of the object
    content = content.replace(
        'episode_id = self.memory.episodic.start_episode(curriculum_stage)',
        'episode_id = self.memory.episodic.start_episode(self.curriculum.current_stage_idx)'
    )
    print("✅ Fixed start_episode() call")

# Comment out store_episode_summary call since method doesn't exist yet
old_store = '''            # Save memories
            self.memory.long_term.store_episode_summary(episode_id, {
                'total_reward': self.current_episode_reward,
                'length': episode_steps,
                'curriculum_stage': curriculum_stage
            })'''

new_store = '''            # Save memories
            # TODO: Implement store_episode_summary in long_term memory
            # self.memory.long_term.store_episode_summary(episode_id, {
            #     'total_reward': self.current_episode_reward,
            #     'length': episode_steps,
            #     'curriculum_stage': curriculum_stage.name if curriculum_stage else None
            # })'''

if old_store in content:
    content = content.replace(old_store, new_store)
    print("✅ Commented out store_episode_summary() call")

# Write back
with open(file_path, 'w') as f:
    f.write(content)

print("✅ All episodic memory fixes applied")
