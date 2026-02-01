#!/usr/bin/env node
/**
 * Stream Manager - Automated Multi-Platform Streaming for Minecraft Bot
 * Streams to Twitch & TikTok simultaneously from VPS
 */

import { spawn } from 'child_process';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import readline from 'readline';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

class StreamManager {
    constructor(config) {
        this.config = config;
        this.twitchProcess = null;
        this.tiktokProcess = null;
        this.botProcess = null;
        this.isStreaming = false;
    }

    async start() {
        console.log('🎬 Starting Minecraft Bot Stream');
        console.log('='.repeat(60));
        console.log(`📺 Resolution: ${this.config.resolution}`);
        console.log(`🎞️  FPS: ${this.config.fps}`);
        console.log(`📤 Bitrate: ${this.config.bitrate}`);
        console.log('');

        // Check if virtual display is running
        const displayAvailable = await this.checkVirtualDisplay();
        if (!displayAvailable) {
            console.error('❌ Virtual display not available!');
            console.log('💡 Start Xvfb first: Xvfb :99 -screen 0 1920x1080x24 &');
            return false;
        }

        // Start Minecraft bot viewer
        await this.startBotViewer();

        // Start streaming to platforms
        if (this.config.twitch.enabled && this.config.twitch.streamKey) {
            await this.startTwitchStream();
        }

        if (this.config.tiktok.enabled && this.config.tiktok.streamKey) {
            await this.startTikTokStream();
        }

        this.isStreaming = true;
        console.log('\n✅ Stream started successfully!');
        console.log('Press Ctrl+C to stop\n');

        return true;
    }

    async checkVirtualDisplay() {
        try {
            const result = spawn('xdpyinfo', ['-display', ':99']);
            return new Promise((resolve) => {
                result.on('close', (code) => resolve(code === 0));
                result.on('error', () => resolve(false));
            });
        } catch {
            return false;
        }
    }

    async startBotViewer() {
        console.log('🤖 Starting Minecraft Bot Viewer...');

        const botScript = path.join(__dirname, 'stream-bot-viewer.js');
        this.botProcess = spawn('node', [botScript], {
            stdio: 'inherit',
            env: {
                ...process.env,
                DISPLAY: ':99',
                CAPTURE_SCREENSHOTS: 'true'
            }
        });

        this.botProcess.on('error', (err) => {
            console.error('❌ Bot viewer error:', err.message);
        });

        // Wait for bot to spawn
        await this.sleep(5000);
        console.log('✅ Bot viewer started');
    }

    async startTwitchStream() {
        console.log(`📺 Starting Twitch stream...`);

        const rtmpUrl = `rtmp://live.twitch.tv/app/${this.config.twitch.streamKey}`;

        const args = [
            '-f', 'x11grab',
            '-s', this.config.resolution,
            '-r', this.config.fps.toString(),
            '-i', ':99',
            '-f', 'pulse',
            '-i', 'default',
            '-vcodec', 'libx264',
            '-preset', 'veryfast',
            '-b:v', this.config.bitrate,
            '-maxrate', this.config.bitrate,
            '-bufsize', '9000k',
            '-pix_fmt', 'yuv420p',
            '-g', '50',
            '-c:a', 'aac',
            '-b:a', '128k',
            '-ar', '44100',
            '-f', 'flv',
            rtmpUrl
        ];

        this.twitchProcess = spawn('ffmpeg', args, {
            stdio: ['ignore', 'pipe', 'pipe']
        });

        this.twitchProcess.stderr.on('data', (data) => {
            const log = data.toString();
            if (log.includes('error') || log.includes('Warning')) {
                console.error('Twitch:', log.trim());
            }
        });

        await this.sleep(2000);
        console.log('✅ Twitch stream started');
    }

    async startTikTokStream() {
        console.log(`📱 Starting TikTok stream...`);

        const rtmpUrl = `rtmp://push.tiktok.com/live/${this.config.tiktok.streamKey}`;

        const args = [
            '-f', 'x11grab',
            '-s', this.config.resolution,
            '-r', this.config.fps.toString(),
            '-i', ':99',
            '-f', 'pulse',
            '-i', 'default',
            '-vcodec', 'libx264',
            '-preset', 'veryfast',
            '-b:v', this.config.bitrate,
            '-maxrate', this.config.bitrate,
            '-bufsize', '9000k',
            '-pix_fmt', 'yuv420p',
            '-g', '50',
            '-c:a', 'aac',
            '-b:a', '128k',
            '-ar', '44100',
            '-f', 'flv',
            rtmpUrl
        ];

        this.tiktokProcess = spawn('ffmpeg', args, {
            stdio: ['ignore', 'pipe', 'pipe']
        });

        this.tiktokProcess.stderr.on('data', (data) => {
            const log = data.toString();
            if (log.includes('error') || log.includes('Warning')) {
                console.error('TikTok:', log.trim());
            }
        });

        await this.sleep(2000);
        console.log('✅ TikTok stream started');
    }

    async stop() {
        console.log('\n🛑 Stopping stream...');

        if (this.twitchProcess) {
            this.twitchProcess.kill('SIGTERM');
            console.log('✅ Twitch stream stopped');
        }

        if (this.tiktokProcess) {
            this.tiktokProcess.kill('SIGTERM');
            console.log('✅ TikTok stream stopped');
        }

        if (this.botProcess) {
            this.botProcess.kill('SIGTERM');
            console.log('✅ Bot viewer stopped');
        }

        this.isStreaming = false;
        console.log('\n👋 Stream ended');
    }

    async getStats() {
        const stats = {
            twitch: this.twitchProcess?.pid || null,
            tiktok: this.tiktokProcess?.pid || null,
            bot: this.botProcess?.pid || null,
            active: this.isStreaming
        };
        return stats;
    }

    sleep(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }
}

// Load configuration
function loadConfig() {
    const envPath = path.join(__dirname, '.env.stream');

    let twitchKey = process.env.TWITCH_STREAM_KEY || '';
    let tiktokKey = process.env.TIKTOK_STREAM_KEY || '';

    if (fs.existsSync(envPath)) {
        const env = fs.readFileSync(envPath, 'utf-8');
        const matchTwitch = env.match(/TWITCH_STREAM_KEY=(.+)/);
        const matchTiktok = env.match(/TIKTOK_STREAM_KEY=(.+)/);
        if (matchTwitch) twitchKey = matchTwitch[1].trim();
        if (matchTiktok) tiktokKey = matchTiktok[1].trim();
    }

    return {
        resolution: process.env.STREAM_RESOLUTION || '1920x1080',
        fps: parseInt(process.env.STREAM_FPS) || 30,
        bitrate: process.env.STREAM_BITRATE || '4500k',
        twitch: {
            enabled: process.env.TWITCH_ENABLED === 'true',
            streamKey: twitchKey
        },
        tiktok: {
            enabled: process.env.TIKTOK_ENABLED === 'true',
            streamKey: tiktokKey
        }
    };
}

// Main execution
async function main() {
    const args = process.argv.slice(2);
    const command = args[0] || 'start';

    const config = loadConfig();
    const manager = new StreamManager(config);

    switch (command) {
        case 'start':
            const success = await manager.start();
            if (success) {
                // Handle graceful shutdown
                process.on('SIGINT', async () => {
                    await manager.stop();
                    process.exit(0);
                });

                // Keep process alive
                await new Promise(() => {});
            }
            break;

        case 'stop':
            await manager.stop();
            break;

        case 'status':
            const stats = await manager.getStats();
            console.log('📊 Stream Status:');
            console.log('='.repeat(40));
            console.log(`Active: ${stats.active ? '✅' : '❌'}`);
            console.log(`Twitch PID: ${stats.twitch || 'Not running'}`);
            console.log(`TikTok PID: ${stats.tiktok || 'Not running'}`);
            console.log(`Bot PID: ${stats.bot || 'Not running'}`);
            break;

        default:
            console.log('Usage: node stream-manager.js [start|stop|status]');
            process.exit(1);
    }
}

main().catch(console.error);
