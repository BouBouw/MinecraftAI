#!/usr/bin/env python3
"""
Fix bridge to send proper observation even for unimplemented actions
"""

file_path = 'llm/node/bridge-server.js'

# Read the file
with open(file_path, 'r') as f:
    content = f.read()

# Check if it needs fixing
if 'action_failed' in content and 'observation' in content:
    # Already has some error handling, check if it's correct
    pass

# Find the unimplemented action case and make it send a proper observation
old_unimplemented = '''                default:
                    console.warn(`⚠️ Unimplemented action type: ${action_type}`)
                    return false''';

new_unimplemented = '''                default:
                    console.warn(`⚠️ Unimplemented action type: ${action_type}`)
                    // Send current observation even if action failed
                    ws.send(JSON.stringify({
                        type: 'observation',
                        observation: this.getCurrentObservation(),
                        reward: 0,
                        done: false
                    }))
                    return false''';

if old_unimplemented in content:
    content = content.replace(old_unimplemented, new_unimplemented)
    print("✅ Updated unimplemented action to send observation")

# Also need to add getCurrentObservation method if it doesn't exist
if 'getCurrentObservation()' not in content:
    # Find a good place to add it (after the executeAction method)
    # Find the closing brace of executeAction
    execute_action_end = '''                    ws.send(JSON.stringify({
                        type: 'observation',
                        observation: observation,
                        reward: reward,
                        done: done
                    }))
                }
            }
        } catch (error) {
            logger.error(`Error executing action: ${error.message}`)
        }
    }'''

    new_method = execute_action_end + '''

    getCurrentObservation() {
        if (!this.bot || !this.bot.entity) {
            return {
                position: [0, 70, 0],
                rotation: [0, 0],
                health: 20,
                food: 20,
                inventory: []
            }
        }

        const bot = this.bot
        const entity = bot.entity

        // Get inventory
        const inventory = []
        if (bot.inventory && bot.inventory.items) {
            for (let i = 0; i < 36; i++) {
                const item = bot.inventory.items().find(item => item.slot === i)
                inventory.push([
                    item ? item.type : 0,
                    item ? item.count : 0
                ])
            }
        }

        return {
            position: [
                entity.position.x,
                entity.position.y,
                entity.position.z
            ],
            rotation: [
                entity.yaw || 0,
                entity.pitch || 0
            ],
            health: bot.health || 20,
            food: bot.food || 20,
            saturation: bot.saturation || 20,
            inventory: inventory,
            hotbar_selected: bot.quickBarSlot || 0,
            on_ground: bot.entity.onGround ? 1 : 0,
            in_water: bot.entity.isInWater ? 1 : 0,
            time_of_day: bot.time ? bot.time.timeOfDay || 0 : 0,
            is_raining: bot.isRaining ? 1 : 0
        }
    }'''

    # Only replace if we found the exact pattern
    if execute_action_end in content:
        content = content.replace(execute_action_end, new_method)
        print("✅ Added getCurrentObservation() method")
    else:
        print("⚠️  Could not find place to insert getCurrentObservation()")

# Write back
with open(file_path, 'w') as f:
    f.write(content)

print("✅ Bridge error response fix applied!")
