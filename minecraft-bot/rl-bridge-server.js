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
            await new Promise(resolve => setTimeout(resolve, 100));
            bot.setControlState('forward', false);
            break;
        case 2: // MOVE_BACKWARD
            bot.setControlState('back', true);
            await new Promise(resolve => setTimeout(resolve, 100));
            bot.setControlState('back', false);
            break;
        case 3: // MOVE_LEFT (strafe)
            bot.setControlState('left', true);
            await new Promise(resolve => setTimeout(resolve, 100));
            bot.setControlState('left', false);
            break;
        case 4: // MOVE_RIGHT (strafe)
            bot.setControlState('right', true);
            await new Promise(resolve => setTimeout(resolve, 100));
            bot.setControlState('right', false);
            break;
        case 5: // JUMP
            bot.setControlState('jump', true);
            await new Promise(resolve => setTimeout(resolve, 100));
            bot.setControlState('jump', false);
            break;
        case 6: // SNEAK
            bot.setControlState('sneak', true);
            await new Promise(resolve => setTimeout(resolve, 100));
            bot.setControlState('sneak', false);
            break;
        case 7: // SPRINT
            bot.setControlState('sprint', true);
            await new Promise(resolve => setTimeout(resolve, 100));
            bot.setControlState('sprint', false);
            break;
        case 8: // LOOK_LEFT
            bot.look(bot.entity.yaw + 0.2, bot.entity.pitch);
            await new Promise(resolve => setTimeout(resolve, 100));
            break;
        case 9: // LOOK_RIGHT
            bot.look(bot.entity.yaw - 0.2, bot.entity.pitch);
            await new Promise(resolve => setTimeout(resolve, 100));
            break;
        case 10: // LOOK_UP
            bot.look(bot.entity.yaw, bot.entity.pitch + 0.2);
            await new Promise(resolve => setTimeout(resolve, 100));
            break;
        case 11: // LOOK_DOWN
            bot.look(bot.entity.yaw, bot.entity.pitch - 0.2);
            await new Promise(resolve => setTimeout(resolve, 100));
            break;
        case 12: // ATTACK (mine blocks) - Legacy action ID
        case 17: // ATTACK (mine blocks) - New action ID from Python
            // Attack only swings arm, doesn't break blocks
            // For mining, we need to use bot.dig() on the block in front
            try {
                // Get block in front of bot
                const pos = bot.entity.position;
                const yaw = bot.entity.yaw;

                // Calculate block position in front of bot (1 block away)
                const dx = -Math.sin(yaw) * 1;
                const dz = Math.cos(yaw) * 1;
                const targetBlock = bot.blockAt(pos.offset(dx, 0, dz));

                if (targetBlock) {
                    await bot.dig(targetBlock);
                    console.log(`⛏️ Mined block at ${targetBlock.position}`);
                } else {
                    // No block, just attack (swing arm)
                    await bot.attack();
                }
            } catch (err) {
                // Fallback to attack if dig fails
                console.log(`Attack fallback: ${err.message}`);
                await bot.attack();
            }
            break;
        default:
            console.log(`Unknown action type: ${actionType}`);
    }

    // Wait for action to complete
    await new Promise(resolve => setTimeout(resolve, 100));
}

function startObservationLoop() {
    setInterval(() => {
        if (!botConnected || !bot.entity) return;

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
