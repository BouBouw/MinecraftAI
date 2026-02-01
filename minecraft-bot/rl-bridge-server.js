/**
 * RL Bridge Server - WebSocket bridge between Python and Minecraft
 * This server connects to Mineflayer bot and exposes WebSocket API
 */

import 'dotenv/config';
import mineflayer from 'mineflayer';
import { WebSocketServer } from 'ws';
import express from 'express';
import cors from 'cors';

const app = express();
app.use(cors());
app.use(express.json());

// Configuration
const MC_HOST = process.env.MC_HOST || 'localhost';
const MC_PORT = parseInt(process.env.MC_PORT) || 25565;
const MC_USERNAME = process.env.MC_USERNAME || 'RLBOT_24_7';
const WS_PORT = 8765;

console.log('🚀 Starting RL Bridge Server...');
console.log(`📍 Minecraft: ${MC_HOST}:${MC_PORT}`);
console.log(`👤 Bot Username: ${MC_USERNAME}`);
console.log(`🔌 WebSocket Port: ${WS_PORT}\n`);

// Create Mineflayer bot
const bot = mineflayer.createBot({
    host: MC_HOST,
    port: MC_PORT,
    username: MC_USERNAME,
    auth: 'offline',
    version: false
});

// Track connection state
let botConnected = false;
let currentObservation = null;

bot.on('connect', () => {
    console.log('✅ Connected to Minecraft server');
    botConnected = true;
});

bot.on('spawn', () => {
    console.log(`✅ Bot spawned in world at position ${bot.entity.position}`);
    startObservationLoop();
});

bot.on('error', (err) => {
    console.error('❌ Minecraft bot error:', err.message);
    botConnected = false;
});

bot.on('end', () => {
    console.log('🔌 Bot disconnected from Minecraft');
    botConnected = false;
    // Note: Mineflayer doesn't support reconnection, need to restart the server
    console.log('⚠️  Please restart the bridge server to reconnect');
});

// Create WebSocket server
const wss = new WebSocketServer({ port: WS_PORT });

console.log(`🔌 WebSocket server listening on port ${WS_PORT}\n`);

wss.on('connection', (ws) => {
    console.log('📡 Python client connected');

    ws.on('message', async (data) => {
        try {
            const message = JSON.parse(data.toString());
            await handleMessage(ws, message);
        } catch (err) {
            console.error('Error handling message:', err);
            ws.send(JSON.stringify({ type: 'error', message: err.message }));
        }
    });

    ws.on('close', () => {
        console.log('📡 Python client disconnected');
    });

    // Send initial observation
    if (currentObservation) {
        ws.send(JSON.stringify({ type: 'observation', observation: currentObservation }));
    }
});

async function handleMessage(ws, message) {
    const { type, action } = message;

    if (type === 'action') {
        try {
            await executeAction(action);
            ws.send(JSON.stringify({ type: 'action_complete', success: true, action, observation: currentObservation }));
        } catch (err) {
            ws.send(JSON.stringify({ type: 'action_complete', success: false, error: err.message, observation: currentObservation }));
        }
    } else if (type === 'reset') {
        // Respawn bot
        console.log('🔄 Resetting environment...');
        // TODO: Implement proper reset logic
        await new Promise(resolve => setTimeout(resolve, 2000));
        ws.send(JSON.stringify({ type: 'reset_complete', observation: currentObservation }));
    }
}

async function executeAction(action) {
    if (!botConnected || !bot.entity) {
        throw new Error('Bot not connected');
    }

    const actionType = action.action_type;

    // Map action types to bot behaviors
    switch(actionType) {
        case 0: // NOOP
            break;
        case 1: // MOVE_FORWARD
            bot.setControlState('forward', true);
            await new Promise(resolve => setTimeout(resolve, 50));  // 100ms → 50ms (plus rapide)
            bot.setControlState('forward', false);
            break;
        case 2: // MOVE_BACKWARD
            bot.setControlState('back', true);
            await new Promise(resolve => setTimeout(resolve, 50));
            bot.setControlState('back', false);
            break;
        case 3: // MOVE_LEFT (strafe)
            bot.setControlState('left', true);
            await new Promise(resolve => setTimeout(resolve, 50));
            bot.setControlState('left', false);
            break;
        case 4: // MOVE_RIGHT (strafe)
            bot.setControlState('right', true);
            await new Promise(resolve => setTimeout(resolve, 50));
            bot.setControlState('right', false);
            break;
        case 5: // JUMP
            bot.setControlState('jump', true);
            await new Promise(resolve => setTimeout(resolve, 50));
            bot.setControlState('jump', false);
            break;
        case 6: // SNEAK
            bot.setControlState('sneak', true);
            await new Promise(resolve => setTimeout(resolve, 50));
            bot.setControlState('sneak', false);
            break;
        case 7: // SPRINT
            bot.setControlState('sprint', true);
            await new Promise(resolve => setTimeout(resolve, 50));
            bot.setControlState('sprint', false);
            break;
        case 8: // LOOK_LEFT
            bot.look(bot.entity.yaw + 0.2, bot.entity.pitch);
            await new Promise(resolve => setTimeout(resolve, 50));  // 100ms → 50ms (plus fluide)
            break;
        case 9: // LOOK_RIGHT
            bot.look(bot.entity.yaw - 0.2, bot.entity.pitch);
            await new Promise(resolve => setTimeout(resolve, 50));
            break;
        case 10: // LOOK_UP
            bot.look(bot.entity.yaw, bot.entity.pitch + 0.2);
            await new Promise(resolve => setTimeout(resolve, 50));
            break;
        case 11: // LOOK_DOWN
            bot.look(bot.entity.yaw, bot.entity.pitch - 0.2);
            await new Promise(resolve => setTimeout(resolve, 50));
            break;
        case 12: // ATTACK (mine blocks) - Legacy action ID
        case 17: // ATTACK (mine blocks) - New action ID from Python
            try {
                // Get block in front of bot
                const pos = bot.entity.position;
                const yaw = bot.entity.yaw;

                // Calculate block position in front of bot (1 block away, at eye level)
                const dx = -Math.sin(yaw) * 1;
                const dz = Math.cos(yaw) * 1;
                const targetBlock = bot.blockAt(pos.offset(dx, 0, dz));

                if (targetBlock) {
                    // CRITICAL FIX: Check if block is AIR (already broken)
                    // Type 0 = air, Type name 'air' = also air
                    if (targetBlock.type === 0 || targetBlock.name === 'air') {
                        console.log(`🌬️ Block is air - nothing to mine (position: ${targetBlock.position})`);
                        // Don't try to mine air - just skip
                        break;
                    }

                    // Log what we're mining for debugging
                    const blockName = targetBlock.name || 'unknown';

                    console.log(`⛏️ Mining ${blockName} at ${targetBlock.position}`);

                    // Smart tool selection: use best tool available
                    const bestTool = bot.inventory.items().find(item =>
                        item.name.includes('pickaxe') ||
                        item.name.includes('axe') ||
                        item.name.includes('shovel')
                    );

                    if (bestTool) {
                        console.log(`🔧 Equipping tool: ${bestTool.name}`);
                        await bot.equip(bestTool, 'hand');
                    }

                    // Calculate exact mining time based on block and tool
                    // Source: https://minecraft.wiki/w/Breaking
                    const blockHardness = targetBlock.hardness || 1;  // Default to 1 if unknown
                    const canHarvest = targetBlock.canHarvest || false;

                    // Tool speed multiplier
                    let toolSpeed = 1;  // By hand (default)
                    if (bestTool) {
                        // Tool material speed multipliers
                        if (bestTool.name.includes('wooden')) toolSpeed = 2;
                        else if (bestTool.name.includes('stone')) toolSpeed = 4;
                        else if (bestTool.name.includes('iron')) toolSpeed = 6;
                        else if (bestTool.name.includes('diamond')) toolSpeed = 8;
                        else if (bestTool.name.includes('golden')) toolSpeed = 12;
                    }

                    // Check for Efficiency enchantment (mineflayer uses .enchants property)
                    let efficiencyBonus = 0;
                    if (bestTool && bestTool.enchants) {
                        const efficiencyEnchant = bestTool.enchants.find(e => e.name === 'efficiency');
                        if (efficiencyEnchant) {
                            efficiencyBonus = efficiencyEnchant.lvl * 3;  // mineflayer uses .lvl
                        }
                    }

                    // Mining speed formula (simplified from Minecraft)
                    // time = hardness / (toolSpeed * (1 + efficiencyBonus * 0.03)) * (correctTool ? 1 : 3) * (canHarvest ? 1 : 10)
                    const isCorrectTool = bot.canHarvestBlock(targetBlock);
                    const toolMultiplier = isCorrectTool ? 1 : 3;
                    const harvestMultiplier = canHarvest ? 1 : 10;

                    let miningTime = (blockHardness * toolMultiplier * harvestMultiplier) / (toolSpeed * (1 + efficiencyBonus * 0.03));

                    // Add base delay (about 0.25s for arm swing animation)
                    miningTime += 0.25;

                    // Clamp to reasonable limits (min 0.5s, max 30s for obsidian with wrong tool)
                    miningTime = Math.max(0.5, Math.min(30, miningTime));

                    // Add 50% margin for network lag and variability
                    const digTimeout = Math.ceil(miningTime * 1000 * 1.5);  // Convert to ms, add 50% margin

                    console.log(`⏱️  Mining ${blockName}: hardness=${blockHardness}, tool=${bestTool?.name || 'hand'}, speed=${toolSpeed}, efficiency=${efficiencyBonus}, time=${miningTime.toFixed(2)}s, timeout=${digTimeout}ms`);

                    const digPromise = bot.dig(targetBlock);
                    const timeoutPromise = new Promise((_, reject) =>
                        setTimeout(() => reject(new Error('Dig timeout - block too hard or unbreakable')), digTimeout)
                    );

                    await Promise.race([digPromise, timeoutPromise]).catch(err => {
                        console.log(`⚠️  Dig failed: ${err.message}`);
                        // Check if block is still there after timeout
                        const blockAfter = bot.blockAt(targetBlock.position);
                        if (blockAfter && blockAfter.type !== 0) {
                            console.log(`🛑 Block too hard or wrong tool - giving up on ${blockAfter.name}`);
                        }
                    });

                    console.log(`✅ Finished mining ${blockName} at ${targetBlock.position}`);
                } else {
                    // No block, just attack (swing arm) for mobs
                    console.log(`⚔️ No block to mine - attacking (mob check)`);
                    await bot.attack();
                }
            } catch (err) {
                // Fallback to attack if dig fails
                console.log(`⚠️ Attack fallback: ${err.message}`);
                await bot.attack();
            }
            break;
        default:
            console.log(`Unknown action type: ${actionType}`);
    }

    // NOTE: No additional delay here - each action already has its own delay (50ms)
    // This makes actions more fluid/tac-au-tac
}

function startObservationLoop() {
    setInterval(() => {
        if (!botConnected || !bot.entity) return;

        // Calculate block in front of bot (for intelligent mining decisions)
        const pos = bot.entity.position;
        const yaw = bot.entity.yaw;
        const dx = -Math.sin(yaw) * 1;
        const dz = Math.cos(yaw) * 1;
        const blockInFront = bot.blockAt(pos.offset(dx, 0, dz));

        currentObservation = {
            position: [bot.entity.position.x, bot.entity.position.y, bot.entity.position.z],
            rotation: [bot.entity.yaw, bot.entity.pitch],
            velocity: [bot.entity.velocity.x, bot.entity.velocity.y, bot.entity.velocity.z],
            on_ground: bot.entity.onGround ? 1 : 0,
            in_water: bot.entity.isInWater ? 1 : 0,
            health: bot.health,
            food: bot.food,
            saturation: bot.foodSaturation || 20,  // Added saturation with fallback
            inventory: bot.inventory.slots.map(slot => [
                slot?.type || 0,
                slot?.count || 0
            ]).flat(),
            hotbar_selected: bot.quickBarSlot,
            block_in_front: blockInFront?.type || 0,  // Type of block directly in front (0 = air)
            visible_blocks: [], // TODO: Implement raycasting for visible blocks
            nearby_entities: [], // TODO: Implement entity tracking
            time_of_day: bot.time.timeOfDay,
            is_raining: bot.isRaining ? 1 : 0,
            biome_id: bot.blockAt(bot.entity.position)?.biome?.id || 1,
            held_item: bot.heldItem?.type || 0,
            armor: [
                bot.inventory.slots[5]?.type || 0, // Head
                bot.inventory.slots[6]?.type || 0, // Chest
                bot.inventory.slots[7]?.type || 0, // Legs
                bot.inventory.slots[8]?.type || 0  // Feet
            ]
        };

        // Broadcast to all connected clients
        wss.clients.forEach(client => {
            if (client.readyState === 1) { // OPEN
                client.send(JSON.stringify({ type: 'observation', observation: currentObservation }));
            }
        });
    }, 100); // 10 Hz observation rate
}

// Start Express server (for health checks)
app.get('/health', (req, res) => {
    res.json({
        status: 'ok',
        bot_connected: botConnected,
        minecraft: `${MC_HOST}:${MC_PORT}`
    });
});

app.listen(3000, () => {
    console.log(`🌐 HTTP server listening on port 3000`);
    console.log(`📊 Health check: http://localhost:3000/health\n`);
});
