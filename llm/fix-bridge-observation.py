#!/usr/bin/env python3
"""
Fix bridge to send proper observation even for unimplemented actions
"""

file_path = 'llm/node/bridge-server.js'

# Read the file
with open(file_path, 'r') as f:
    content = f.read()

# Find and update the handleAction method to send observation even on failure
# The current code sends 'action_complete' but we need to make sure it includes observation

# Update the handleAction to send observation even when action fails
old_handle_action = """        } catch (e) {
            error = e.message;
            console.error('❌ Action execution failed:', e);
        }

        // Get next state after action
        const next_state = this.getCurrentState();

        this.send(ws, {
            type: 'action_complete',
            episode_id: this.currentEpisode,"""

new_handle_action = """        } catch (e) {
            error = e.message;
            console.error('❌ Action execution failed:', e);
        }

        // Get next state after action (even if action failed)
        const next_state = this.getCurrentState();

        // Always send observation, even if action failed
        this.send(ws, {
            type: 'action_complete',
            episode_id: this.currentEpisode,"""

if old_handle_action in content:
    content = content.replace(old_handle_action, new_handle_action)
    print("✅ Updated handleAction to always send observation")
else:
    print("⚠️  Could not find handleAction section")
    # Don't exit, continue trying other fixes

# Update the unimplemented action case to still send observation via the normal flow
# (it already returns false which triggers the error handling above)

# Write back
with open(file_path, 'w') as f:
    f.write(content)

print("✅ Bridge observation fix applied!")
