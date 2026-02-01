/**
 * Minecraft Bot POV Streamer
 * Captures the bot's point of view and renders to virtual display
 */

import 'dotenv/config';
import mineflayer from 'mineflayer';
import { createClient } from 'minecraft-protocol';
import { PrismaClient } from '@prisma/client';
import fs from 'fs';
import path from 'path';

const VIEWPORT_WIDTH = 1920;
const VIEWPORT_HEIGHT = 1080;

const prisma = new PrismaClient();

console.log('🎥 Minecraft Bot POV Streamer');
console.log('=' .repeat(60));

// Configuration
const MC_HOST = process.env.MC_HOST || 'localhost';
const MC_PORT = parseInt(process.env.MC_PORT) || 25565;
const MC_USERNAME = process.env.MC_USERNAME || 'STREAM_BOT';

console.log(`📍 Connecting to: ${MC_HOST}:${MC_PORT}`);
console.log(`👤 Bot Username: ${MC_USERNAME}`);
console.log(`🎬 Resolution: ${VIEWPORT_WIDTH}x${VIEWPORT_HEIGHT}\n`);

// Create Mineflayer bot with viewer
const bot = mineflayer.createBot({
    host: MC_HOST,
    port: MC_PORT,
    username: MC_USERNAME,
    auth: 'offline',
    version: false,
});

let viewer = null;
let recording = false;
let screenshotInterval = null;

bot.on('connect', () => {
    console.log('✅ Connected to Minecraft server');
});

bot.on('spawn', () => {
    console.log(`✅ Bot spawned at ${bot.entity.position}`);

    // Load mineflayer-viewer if available
    try {
        const { Viewer } = require('prismarine-viewer').mineflayer;

        // Create viewer that outputs to virtual display
        viewer = Viewer(bot, {
            firstPerson: true,
            width: VIEWPORT_WIDTH,
            height: VIEWPORT_HEIGHT,
            port: 3007, // Web viewer port
        });

        console.log('🎥 Viewer initialized');
        console.log('📺 Web viewer: http://localhost:3007\n');

        // Start capturing screenshots if enabled
        if (process.env.Capture_Screenshots === 'true') {
            startCapturing();
        }

    } catch (err) {
        console.error('⚠️  Viewer not available:', err.message);
        console.log('💡 Install with: npm install prismarine-viewer');
    }
});

bot.on('error', (err) => {
    console.error('❌ Bot error:', err.message);
});

function startCapturing() {
    if (recording) return;
    recording = true;

    const screenshotsDir = path.join(__dirname, 'screenshots');
    if (!fs.existsSync(screenshotsDir)) {
        fs.mkdirSync(screenshotsDir, { recursive: true });
    }

    let frameCount = 0;

    // Capture screenshot every 100ms (10 FPS for recording)
    screenshotInterval = setInterval(() => {
        if (!viewer) return;

        try {
            const screenshot = viewer.extract?.();
            if (screenshot) {
                const filename = path.join(screenshotsDir, `frame_${frameCount.toString().padStart(6, '0')}.png`);
                fs.writeFileSync(filename, screenshot);
                frameCount++;

                // Keep only last 1000 frames
                if (frameCount % 1000 === 0) {
                    cleanupOldFrames(screenshotsDir, 100);
                }
            }
        } catch (err) {
            console.error('Screenshot error:', err.message);
        }
    }, 100);

    console.log('📸 Screenshot capture started (10 FPS)');
}

function cleanupOldFrames(dir, keep) {
    const files = fs.readdirSync(dir)
        .filter(f => f.endsWith('.png'))
        .sort();

    while (files.length > keep) {
        const oldFile = files.shift();
        fs.unlinkSync(path.join(dir, oldFile));
    }
}

function stopCapturing() {
    if (screenshotInterval) {
        clearInterval(screenshotInterval);
        screenshotInterval = null;
    }
    recording = false;
    console.log('🛑 Screenshot capture stopped');
}

// Handle graceful shutdown
process.on('SIGINT', () => {
    console.log('\n\n🛑 Shutting down...');
    stopCapturing();
    bot.quit();
    process.exit(0);
});
