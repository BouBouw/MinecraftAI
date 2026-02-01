/**
 * Minecraft Bot POV Capture with Screenshot Streaming
 * Captures real bot gameplay and saves screenshots for streaming
 */

import 'dotenv/config';
import mineflayer from 'mineflayer';
import { WebSocketServer } from 'ws';
import express from 'express';
import cors from 'cors';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

const app = express();
app.use(cors());
app.use(express.json());

// Configuration
const MC_HOST = process.env.MC_HOST || 'localhost';
const MC_PORT = parseInt(process.env.MC_PORT) || 25565;
const MC_USERNAME = process.env.MC_USERNAME || 'STREAM_BOT';
const WS_PORT = 8765;
const SCREENSHOT_DIR = path.join(__dirname, '../screenshots');
const SCREENSHOT_INTERVAL = 100; // 10 FPS for screenshots

console.log('🎥 Minecraft Bot POV Capture');
console.log('='.repeat(60));
console.log(`📍 Minecraft: ${MC_HOST}:${MC_PORT}`);
console.log(`👤 Bot Username: ${MC_USERNAME}`);
console.log(`📸 Screenshot Dir: ${SCREENSHOT_DIR}`);
console.log(`📹 Screenshot Rate: ${1000/SCREENSHOT_INTERVAL} FPS\n`);

// Create screenshot directory
if (!fs.existsSync(SCREENSHOT_DIR)) {
    fs.mkdirSync(SCREENSHOT_DIR, { recursive: true });
    console.log('✅ Created screenshot directory\n');
}

// Create Mineflayer bot
const bot = mineflayer.createBot({
    host: MC_HOST,
    port: MC_PORT,
    username: MC_USERNAME,
    auth: 'offline',
    version: false
});

let botConnected = false;
let currentObservation = null;
let screenshotCount = 0;
let screenshotInterval = null;
let viewer = null;

bot.on('connect', () => {
    console.log('✅ Connected to Minecraft server');
    botConnected = true;
});

bot.on('spawn', () => {
    console.log(`✅ Bot spawned at ${bot.entity.position}`);
    startPOVCapture();
});

bot.on('error', (err) => {
    console.error('❌ Minecraft bot error:', err.message);
    botConnected = false;
});

bot.on('end', () => {
    console.log('🔌 Bot disconnected');
    botConnected = false;
    if (screenshotInterval) {
        clearInterval(screenshotInterval);
    }
});

// Start POV capture with screenshots
async function startPOVCapture() {
    console.log('🎬 Starting POV capture...\n');

    // Try to load prismarine-viewer
    try {
        const { Viewer } = await import('prismarine-viewer').mineflayer;

        // Initialize viewer in first-person mode
        viewer = Viewer(bot, {
            firstPerson: true,
            width: 1280,
            height: 720,
            outputType: 'jpeg',
            port: 3007
        });

        console.log('✅ Viewer initialized');
        console.log('📺 Web viewer available at: http://localhost:3007\n');

        // Start screenshot loop
        screenshotInterval = setInterval(() => {
            if (!botConnected || !bot.entity) return;

            try {
                // Capture screenshot from viewer
                const screenshot = viewer?.();

                if (screenshot) {
                    // Save screenshot
                    const filename = path.join(SCREENSHOT_DIR, `frame_${screenshotCount.toString().padStart(6, '0')}.jpg`);
                    fs.writeFileSync(filename, screenshot);
                    screenshotCount++;

                    // Keep only last 300 frames (30 seconds at 10 FPS)
                    if (screenshotCount % 100 === 0) {
                        cleanupOldScreenshots(300);
                    }
                }
            } catch (err) {
                // Silently fail - viewer might not be ready
            }
        }, SCREENSHOT_INTERVAL);

        console.log(`📸 Capturing screenshots every ${SCREENSHOT_INTERVAL}ms`);

    } catch (err) {
        console.error('⚠️  prismarine-viewer not available:', err.message);
        console.log('💡 Install with: npm install prismarine-viewer');
        console.log('💡 Falling back to observation data only...\n');

        // Fallback: observation streaming without screenshots
        startObservationLoop();
    }
}

function startObservationLoop() {
    console.log('📊 Starting observation data streaming...\n');

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
            saturation: bot.foodSaturation || 20,
            inventory: bot.inventory.slots.map(slot => [
                slot?.type || 0,
                slot?.count || 0
            ]).flat(),
            hotbar_selected: bot.quickBarSlot,
            visible_blocks: [],
            nearby_entities: [],
            time_of_day: bot.time.timeOfDay,
            is_raining: bot.isRaining ? 1 : 0,
            biome_id: bot.blockAt(bot.entity.position)?.biome?.id || 1,
            held_item: bot.heldItem?.type || 0,
            armor: [
                bot.inventory.slots[5]?.type || 0,
                bot.inventory.slots[6]?.type || 0,
                bot.inventory.slots[7]?.type || 0,
                bot.inventory.slots[8]?.type || 0
            ]
        };

        // Save observation as JSON for metadata
        const obsFile = path.join(SCREENSHOT_DIR, `obs_${screenshotCount.toString().padStart(6, '0')}.json`);
        fs.writeFileSync(obsFile, JSON.stringify(currentObservation));
        screenshotCount++;

    }, SCREENSHOT_INTERVAL);
}

function cleanupOldScreenshots(keep) {
    try {
        const files = fs.readdirSync(SCREENSHOT_DIR)
            .filter(f => f.endsWith('.jpg'))
            .sort();

        while (files.length > keep) {
            const oldFile = files.shift();
            fs.unlinkSync(path.join(SCREENSHOT_DIR, oldFile));

            // Also remove corresponding observation file
            const obsFile = oldFile.replace('.jpg', '.json');
            const obsPath = path.join(SCREENSHOT_DIR, obsFile);
            if (fs.existsSync(obsPath)) {
                fs.unlinkSync(obsPath);
            }
        }
    } catch (err) {
        console.error('Cleanup error:', err.message);
    }
}

// WebSocket server for control messages
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
        }
    });

    ws.on('close', () => {
        console.log('📡 Python client disconnected');
    });
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
        console.log('🔄 Resetting environment...');
        await new Promise(resolve => setTimeout(resolve, 2000));
        ws.send(JSON.stringify({ type: 'reset_complete', observation: currentObservation }));
    }
}

async function executeAction(action) {
    if (!botConnected || !bot.entity) {
        throw new Error('Bot not connected');
    }

    const actionType = action.action_type || action.action || action;

    switch(actionType) {
        case 0: break; // NOOP
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
        case 3: // MOVE_LEFT
            bot.setControlState('left', true);
            await new Promise(resolve => setTimeout(resolve, 100));
            bot.setControlState('left', false);
            break;
        case 4: // MOVE_RIGHT
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
        case 12: // ATTACK
            await bot.attack();
            break;
        default:
            console.log(`Unknown action: ${actionType}`);
    }

    await new Promise(resolve => setTimeout(resolve, 100));
}

// HTTP server for health checks
app.get('/health', (req, res) => {
    res.json({
        status: 'ok',
        bot_connected: botConnected,
        screenshots_captured: screenshotCount,
        minecraft: `${MC_HOST}:${MC_PORT}`
    });
});

app.get('/screenshot-count', (req, res) => {
    res.json({
        count: screenshotCount,
        directory: SCREENSHOT_DIR,
        viewer_active: viewer !== null
    });
});

app.listen(3000, () => {
    console.log(`🌐 HTTP server listening on port 3000`);
    console.log(`📊 Health check: http://localhost:3000/health`);
    console.log(`📸 Screenshot count: http://localhost:3000/screenshot-count\n`);
    console.log(`🎬 POV Capture Active!\n`);
});
