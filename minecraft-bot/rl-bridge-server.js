/**
 * RL Bridge Server - WebSocket bridge between Python and Minecraft
 * This server connects to Mineflayer bot and exposes WebSocket API
 */

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
    // Attempt to reconnect after 10 seconds
    setTimeout(() => {
        console.log('🔄 Attempting to reconnect...');
        bot.connect();
    }, 10000);
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
            ws.send(JSON.stringify({ type: 'action_complete', success: true, action }));
        } catch (err) {
            ws.send(JSON.stringify({ type: 'action_complete', success: false, error: err.message }));
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
        case 5: // JUMP
            bot.setControlState('jump', true);
            await new Promise(resolve => setTimeout(resolve, 100));
            bot.setControlState('jump', false);
            break;
        // Add more action mappings as needed
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
            saturation: bot.saturation,
            inventory: bot.inventory.slots.map(slot => [
                slot?.type || 0,
                slot?.count || 0
            ]).flat(),
            hotbar_selected: bot.quickBarSlot,
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
