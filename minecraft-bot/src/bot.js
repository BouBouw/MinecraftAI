import mineflayer from 'mineflayer';
import pathfinderPlugin from 'mineflayer-pathfinder';
import { config } from '../config.js';
import { WebSocket } from 'ws';

import { MiningAgent } from './agents/mining-agent.js';
import { CraftingAgent } from './agents/crafting-agent.js';
import { InventoryAgent } from './agents/inventory-agent.js';
import { BuildingAgent } from './agents/building-agent.js';

const { pathfinder, Movements, goals } = pathfinderPlugin;

/**
 * Main Minecraft Bot class
 * Connects to a Minecraft server and performs automated tasks
 */
class MinecraftBot {
    constructor(options = {}) {
        this.config = { ...config, ...options };
        this.bot = null;
        this.wsClient = null;
        this.currentTask = null;
        this.status = 'idle';

        // Agents
        this.agents = {};
    }

    /**
     * Start the bot
     */
    async start() {
        console.log('🤖 Starting Minecraft AI Bot...');

        try {
            // Create bot instance
            this.bot = mineflayer.createBot({
                host: this.config.server.host,
                port: this.config.server.port,
                username: this.config.server.username,
                password: this.config.server.password,
                auth: this.config.server.auth,
                version: false // Auto-detect version
            });

            // Load plugins
            this.bot.loadPlugin(pathfinder);

            // Setup event handlers
            this.setupEventHandlers();

            // Initialize agents
            this.initializeAgents();

            // Connect to coordinator
            this.connectToCoordinator();

        } catch (error) {
            console.error('❌ Failed to start bot:', error);
            throw error;
        }
    }

    /**
     * Setup bot event handlers
     */
    setupEventHandlers() {
        this.bot.on('spawn', () => {
            console.log(`✅ Bot spawned in ${this.bot.game.gameMode} mode`);
            console.log(`   Position: ${this.bot.entity.position}`);
            console.log(`   Health: ${this.bot.health}/20`);

            // Setup pathfinding movements
            const mcData = require('minecraft-data')(this.bot.version);
            const defaultMove = new Movements(this.bot, mcData);
            this.bot.pathfinder.setMovements(defaultMove);

            // Start from scratch if needed
            if (this.config.startFromScratch) {
                this.startFromScratch();
            }
        });

        this.bot.on('chat', (username, message) => {
            if (username === this.bot.username) return;
            console.log(`💬 ${username}: ${message}`);
        });

        this.bot.on('error', (err) => {
            console.error('❌ Bot error:', err);
        });

        this.bot.on('kicked', (reason) => {
            console.log('👢 Bot kicked:', reason);
        });

        this.bot.on('end', () => {
            console.log('🔌 Bot disconnected');
            this.status = 'disconnected';
        });

        this.bot.on('whisper', (username, message) => {
            console.log(`🤫 ${username} whispers: ${message}`);
            // Handle commands from players
            this.handlePlayerCommand(username, message);
        });
    }

    /**
     * Initialize all agents
     */
    initializeAgents() {
        this.agents.mining = new MiningAgent(this.bot);
        this.agents.crafting = new CraftingAgent(this.bot);
        this.agents.inventory = new InventoryAgent(this.bot);
        this.agents.building = new BuildingAgent(this.bot);

        console.log('✅ All agents initialized');
    }

    /**
     * Connect to the AI coordinator server
     */
    connectToCoordinator() {
        try {
            this.wsClient = new WebSocket(this.config.coordinatorUrl);

            this.wsClient.on('open', () => {
                console.log('✅ Connected to coordinator server');
                this.sendStatus('ready');
            });

            this.wsClient.on('message', (data) => {
                this.handleCoordinatorMessage(JSON.parse(data.toString()));
            });

            this.wsClient.on('error', (error) => {
                console.error('❌ WebSocket error:', error.message);
            });

            this.wsClient.on('close', () => {
                console.log('🔌 Disconnected from coordinator');
                // Attempt reconnect after 5 seconds
                setTimeout(() => this.connectToCoordinator(), 5000);
            });

        } catch (error) {
            console.error('❌ Failed to connect to coordinator:', error);
        }
    }

    /**
     * Handle messages from coordinator
     */
    async handleCoordinatorMessage(data) {
        console.log('📨 Received from coordinator:', data.type);

        switch (data.type) {
            case 'build_task':
                this.currentTask = data;
                await this.executeBuildTask(data);
                break;

            case 'ping':
                this.wsClient.send(JSON.stringify({ type: 'pong' }));
                break;

            default:
                console.warn('⚠️ Unknown message type:', data.type);
        }
    }

    /**
     * Execute a build task
     */
    async executeBuildTask(taskData) {
        console.log('🏗️  Starting build task...');
        this.status = 'building';
        this.sendStatus('building');

        try {
            const { schematic, tasks } = taskData;

            // Execute each task in order
            for (const task of tasks) {
                console.log(`📋 Task: ${task.description}`);
                await this.executeSubTask(task);

                // Update progress
                const progress = Math.round((task.id / tasks.length) * 100);
                this.sendStatus('building', progress, task.description);
            }

            // Build complete
            this.status = 'idle';
            this.wsClient.send(JSON.stringify({
                type: 'build_complete',
                schematicId: schematic.id
            }));
            console.log('✅ Build completed!');

        } catch (error) {
            console.error('❌ Build failed:', error);
            this.wsClient.send(JSON.stringify({
                type: 'error',
                message: error.message
            }));
        }
    }

    /**
     * Execute a single sub-task
     */
    async executeSubTask(task) {
        switch (task.type) {
            case 'gather_resources':
                await this.agents.mining.gatherResources(task.materials);
                break;

            case 'craft_items':
                await this.agents.crafting.craftItem(task.item);
                break;

            case 'move_to_site':
                await this.moveTo(task.position);
                break;

            case 'build_layer':
                await this.agents.building.buildLayer(task.layer);
                break;

            default:
                console.warn('⚠️ Unknown task type:', task.type);
        }
    }

    /**
     * Start from scratch (gather basic resources)
     */
    async startFromScratch() {
        console.log('🌱 Starting from scratch...');

        try {
            // Find and chop a tree
            console.log('🌲 Looking for a tree...');
            const tree = await this.agents.mining.findNearestTree();
            if (tree) {
                await this.agents.mining.mineBlock(tree);
                console.log('✅ Got wood!');
            }

            // Craft crafting table
            await this.agents.crafting.craftCraftingTable();
            console.log('✅ Crafting table ready!');

            // Craft wooden pickaxe
            await this.agents.crafting.craftPickaxe('wood');
            console.log('⛏️  Wooden pickaxe ready!');

            // Now we can start gathering more resources
            console.log('✅ Ready to gather resources!');

        } catch (error) {
            console.error('❌ Failed to start from scratch:', error);
        }
    }

    /**
     * Move to a specific position
     */
    async moveTo(position) {
        const pos = { x: position.x, y: position.y, z: position.z };
        const goal = new goals.GoalBlock(pos.x, pos.y, pos.z);

        return new Promise((resolve, reject) => {
            this.bot.pathfinder.setGoal(goal);

            this.bot.once('goal_reached', () => {
                console.log(`📍 Reached position: ${pos.x}, ${pos.y}, ${pos.z}`);
                resolve();
            });

            this.bot.once('path_stop', () => {
                reject(new Error('Pathfinding stopped'));
            });

            setTimeout(() => reject(new Error('Movement timeout')), 30000);
        });
    }

    /**
     * Send status update to coordinator
     */
    sendStatus(status, progress = null, message = '') {
        if (!this.wsClient || this.wsClient.readyState !== 1) { // 1 = OPEN state
            return;
        }

        this.wsClient.send(JSON.stringify({
            type: 'status_update',
            status: status,
            progress: progress,
            message: message
        }));
    }

    /**
     * Handle player commands
     */
    handlePlayerCommand(username, message) {
        const args = message.split(' ');
        const command = args[0].toLowerCase();

        switch (command) {
            case '!status':
                this.bot.whisper(username, `Status: ${this.status}`);
                break;

            case '!follow':
                // Follow the player
                this.bot.whisper(username, 'Following you!');
                break;

            case '!stop':
                this.status = 'idle';
                this.bot.pathfinder.setGoal(null);
                this.bot.whisper(username, 'Stopped!');
                break;

            default:
                this.bot.whisper(username, 'Unknown command. Try: !status, !follow, !stop');
        }
    }

    /**
     * Stop the bot
     */
    stop() {
        if (this.bot) {
            this.bot.quit();
        }
        if (this.wsClient) {
            this.wsClient.close();
        }
        console.log('🛑 Bot stopped');
    }
}

// Start bot if this file is run directly
if (import.meta.url === `file://${process.argv[1]}`) {
    const bot = new MinecraftBot();
    bot.start().catch(console.error);

    // Handle graceful shutdown
    process.on('SIGINT', () => {
        console.log('\\n🛑 Shutting down bot...');
        bot.stop();
        process.exit(0);
    });
}

export { MinecraftBot };
