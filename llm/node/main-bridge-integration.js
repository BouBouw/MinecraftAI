#!/usr/bin/env node
/**
 * Main RL Bridge Integration
 * Connects Python RL Agent to actual Minecraft gameplay via Mineflayer
 *
 * This is the missing piece that makes the AI actually play Minecraft!
 */

import MinecraftBridgeServer from './bridge-server.js';
import mineflayer from 'mineflayer';
import pathfinder from 'mineflayer-pathfinder';
import Vec3 from 'vec3';
import dotenv from 'dotenv';

dotenv.config();

// Configuration
const BRIDGE_PORT = 8765;
const MC_HOST = process.env.MC_HOST || 'localhost';
const MC_PORT = parseInt(process.env.MC_PORT) || 25565;
const MC_USERNAME = process.env.MC_USERNAME || 'RLAgent';

/**
 * RL Bot Client
 * Wraps a Mineflayer bot for RL training
 */
class RLBotClient {
    constructor(host, port, username) {
        this.host = host;
        this.port = port;
        this.username = username;
        this.mineflayerBot = null;
        this.isConnected = false;
        this.isInGame = false;
    }

    /**
     * Connect bot to Minecraft server
     */
    async connect() {
        console.log(`🎮 Connecting to Minecraft server ${this.host}:${this.port}...`);

        return new Promise((resolve, reject) => {
            // Create bot
            this.mineflayerBot = mineflayer.createBot({
                host: this.host,
                port: this.port,
                username: this.username,
                auth: 'offline',
                version: false, // Auto-detect
                hideErrors: true
            });

            // Load pathfinder
            this.mineflayerBot.loadPlugin(pathfinder);

            // Connect event
            this.mineflayerBot.on('connect', () => {
                console.log('✅ Bot connected to server!');
                this.isConnected = true;
            });

            // Spawn event
            this.mineflayerBot.on('spawn', () => {
                console.log('✅ Bot spawned in world!');
                this.isInGame = true;
                console.log(`   Position: ${this.mineflayerBot.entity.position}`);
                console.log(`   Health: ${this.mineflayerBot.health}/20`);
                console.log(`   Food: ${this.mineflayerBot.food}/20`);
                resolve(this);
            });

            // Error handling
            this.mineflayerBot.on('error', (err) => {
                if (err.message.includes('array size is abnormally large')) {
                    // Ignore NBT errors
                    return;
                }
                console.error('❌ Bot error:', err.message);
                this.isConnected = false;
                this.isInGame = false;
                reject(err);
            });

            // Kicked
            this.mineflayerBot.on('kicked', (reason) => {
                console.warn('⚠️ Bot kicked:', reason);
                this.isConnected = false;
                this.isInGame = false;
            });

            // End/disconnect
            this.mineflayerBot.on('end', () => {
                console.log('🔌 Bot disconnected');
                this.isConnected = false;
                this.isInGame = false;
            });

            // Death
            this.mineflayerBot.on('death', () => {
                console.log('💀 Bot died!');
                // Will auto-respawn
            });

            // Respawn
            this.mineflayerBot.on('respawn', () => {
                console.log('✅ Bot respawned');
            });

            // Timeout
            setTimeout(() => {
                if (!this.isInGame) {
                    reject(new Error('Connection timeout'));
                }
            }, 30000);
        });
    }

    /**
     * Disconnect bot
     */
    disconnect() {
        if (this.mineflayerBot) {
            this.mineflayerBot.quit();
        }
        this.isConnected = false;
        this.isInGame = false;
    }
}

/**
 * Main Integration Class
 */
class MainRLIntegration {
    constructor() {
        this.botClient = null;
        this.bridgeServer = null;
        this.isRunning = false;
    }

    /**
     * Start the complete RL system
     */
    async start() {
        console.log('🚀 Starting Minecraft RL System...');
        console.log('=' .repeat(60));
        console.log(`   Bridge Port: ${BRIDGE_PORT}`);
        console.log(`   MC Server: ${MC_HOST}:${MC_PORT}`);
        console.log(`   Username: ${MC_USERNAME}`);
        console.log('=' .repeat(60));
        console.log('');

        try {
            // Step 1: Connect bot to Minecraft
            this.botClient = new RLBotClient(MC_HOST, MC_PORT, MC_USERNAME);
            await this.botClient.connect();
            console.log('');

            // Step 2: Start bridge server with bot attached
            console.log('🌉 Starting bridge server...');
            this.bridgeServer = new MinecraftBridgeServer(BRIDGE_PORT, this.botClient);
            this.bridgeServer.start();
            console.log('');

            console.log('✅ RL System is ready!');
            console.log('');
            console.log('📋 The AI can now play Minecraft!');
            console.log('');
            console.log('🔗 Next steps:');
            console.log('   1. Start Python training: cd llm/python && python training/trainer.py');
            console.log('   2. Or use: cd .. && ./llm/start-production.sh start');
            console.log('   3. Monitor with: ./llm/monitor.sh --live');
            console.log('');
            console.log('📊 TensorBoard: http://localhost:6006');
            console.log('   (Use SSH tunnel: ssh -L 6006:localhost:6006 user@server)');
            console.log('');

            this.isRunning = true;

            // Handle graceful shutdown
            process.on('SIGINT', () => this.shutdown());
            process.on('SIGTERM', () => this.shutdown());

            // Keep running
            await this.keepRunning();

        } catch (error) {
            console.error('❌ Failed to start RL system:', error.message);
            console.error('');
            console.error('🔧 Troubleshooting:');
            console.error('   1. Make sure Minecraft server is running');
            console.error(`   2. Check server: ${MC_HOST}:${MC_PORT}`);
            console.error('   3. Check .env file configuration');
            process.exit(1);
        }
    }

    /**
     * Keep the process running
     */
    async keepRunning() {
        while (this.isRunning) {
            // Periodically check bot connection
            if (!this.botClient.isConnected || !this.botClient.isInGame) {
                console.warn('⚠️ Bot disconnected, attempting to reconnect...');
                try {
                    await this.botClient.connect();
                    console.log('✅ Reconnected!');
                } catch (error) {
                    console.error('❌ Reconnect failed:', error.message);
                    await this.sleep(5000);
                }
            }

            await this.sleep(5000);
        }
    }

    /**
     * Graceful shutdown
     */
    shutdown() {
        console.log('');
        console.log('🛑 Shutting down RL system...');

        this.isRunning = false;

        if (this.bridgeServer) {
            this.bridgeServer.stop();
        }

        if (this.botClient) {
            this.botClient.disconnect();
        }

        console.log('✅ Shutdown complete');
        process.exit(0);
    }

    /**
     * Sleep utility
     */
    sleep(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }
}

// Start the integration
const integration = new MainRLIntegration();
integration.start().catch(error => {
    console.error('Fatal error:', error);
    process.exit(1);
});

export { MainRLIntegration, RLBotClient };
