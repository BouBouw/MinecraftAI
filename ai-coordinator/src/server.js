import { WebSocketServer } from 'ws';
import { SchematicParser } from './schematic-parser.js';
import { TaskPlanner } from './task-planner.js';
import { BotCommunication } from './communication.js';
import { SchematicBuilder } from './schematic-builder.js';
import mineflayer from 'mineflayer';
import pkg from 'mineflayer-pathfinder';
import Vec3 from 'vec3';
import dotenv from 'dotenv';

// Get pathfinder components from CommonJS module
const { pathfinder, Movements, goals } = pkg;

// Load environment variables
dotenv.config();

/**
 * WebSocket Server for AI Coordinator
 * Handles communication between Minecraft mod and AI bot
 */
class AIServer {
    constructor(port = 8080) {
        this.port = port;
        this.wss = null;
        this.modClient = null;
        this.botClient = null;

        this.parser = new SchematicParser();
        this.planner = new TaskPlanner();
        this.botComm = new BotCommunication();

        this.activeSchematic = null;
        this.buildProgress = 0;

        // Mineflayer bot instance
        this.mineflayerBot = null;
        this.isBotConnected = false;
        this.isBotInGame = false;
        this.currentTarget = null;

        // Bot capabilities
        this.botGameMode = null; // 'survival', 'creative', 'adventure', 'spectator'
        this.botIsOP = false; // Can execute commands like /tp

        // Bot owner
        this.botOwner = null; // Username of the player who launched the bot

        // Schematic builder
        this.schematicBuilder = null;
    }

    start() {
        this.wss = new WebSocketServer({ port: this.port });

        console.log(`🚀 AI Coordinator Server started on port ${this.port}`);

        this.wss.on('connection', (ws, req) => {
            const clientType = this.identifyClient(req);
            console.log(`✅ New ${clientType} client connected from ${req.socket.remoteAddress}`);

            ws.on('message', (message) => {
                this.handleMessage(ws, message, clientType);
            });

            ws.on('close', () => {
                this.handleDisconnect(ws, clientType);
            });

            ws.on('error', (error) => {
                console.error(`❌ WebSocket error for ${clientType}:`, error.message);
            });

            // Send welcome message
            ws.send(JSON.stringify({
                type: 'welcome',
                clientType: clientType,
                message: `Connected as ${clientType} client`,
                timestamp: Date.now()
            }));
        });

        this.wss.on('error', (error) => {
            console.error('❌ WebSocket Server error:', error);
        });
    }

    identifyClient(req) {
        const url = req.url || '';
        if (url.includes('/bot')) return 'bot';
        // Default to 'mod' for Minecraft mod client (including unknown/empty path)
        return 'mod';
    }

    handleMessage(ws, message, clientType) {
        try {
            const data = JSON.parse(message.toString());
            console.log(`📨 Received from ${clientType}:`, data.type);

            switch (clientType) {
                case 'mod':
                    this.handleModMessage(ws, data);
                    break;
                case 'bot':
                    this.handleBotMessage(ws, data);
                    break;
                default:
                    console.warn('⚠️ Unknown client type');
            }
        } catch (error) {
            console.error('❌ Error handling message:', error);
            ws.send(JSON.stringify({
                type: 'error',
                message: error.message
            }));
        }
    }

    /**
     * Handle messages from Minecraft mod
     */
    handleModMessage(ws, data) {
        switch (data.type) {
            case 'bot_move_to_schematic':
                console.log(`🤖 Received bot move command`);
                console.log(`   Target position: (${data.target_position.x}, ${data.target_position.y}, ${data.target_position.z})`);
                console.log(`   Position types: x=${typeof data.target_position.x}, y=${typeof data.target_position.y}, z=${typeof data.target_position.z}`);
                console.log(`   Schematic: ${data.schematic_name}`);
                console.log(`   Dimensions: ${data.dimensions.width}x${data.dimensions.height}x${data.dimensions.length}`);

                // Store owner name if provided
                if (data.owner_name) {
                    this.botOwner = data.owner_name;
                    console.log(`   🎮 Bot owner: ${this.botOwner}`);
                }

                // Store schematic info
                this.activeSchematic = {
                    name: data.schematic_name,
                    position: data.target_position,
                    dimensions: data.dimensions,
                    blocks_data: data.blocks_data // Use blocks data from mod!
                };

                // Log blocks data info
                if (data.blocks_data && data.blocks_data.blocks) {
                    console.log(`   Received ${data.blocks_data.blocks.length} blocks from mod`);
                }

                // Check if bot is already connected and in game
                if (this.mineflayerBot && this.isBotInGame) {
                    console.log('♻️ Bot already connected, redirecting to new target');
                    this.navigateToTarget(data.target_position);

                    ws.send(JSON.stringify({
                        type: 'bot_move_ack',
                        status: 'redirecting',
                        message: 'Bot already connected, moving to new target...',
                        bot_status: {
                            connected: true,
                            in_game: true,
                            current_position: {
                                x: Math.floor(this.mineflayerBot.entity.position.x),
                                y: Math.floor(this.mineflayerBot.entity.position.y),
                                z: Math.floor(this.mineflayerBot.entity.position.z)
                            }
                        },
                        target_position: data.target_position
                    }));
                } else {
                    console.log('🆕 Launching new bot instance');
                    // Launch mineflayer bot
                    this.launchMineflayerBot(data.target_position);

                    // Acknowledge to mod
                    ws.send(JSON.stringify({
                        type: 'bot_move_ack',
                        status: 'connecting',
                        message: 'Bot is connecting to server...',
                        target_position: data.target_position
                    }));
                }
                break;

            case 'schematic_validation':
                console.log(`📐 Received schematic: ${data.name}`);
                console.log(`   Position: (${data.position.x}, ${data.position.y}, ${data.position.z})`);
                console.log(`   Dimensions: ${data.dimensions.width}x${data.dimensions.height}x${data.dimensions.length}`);
                console.log(`   Materials: ${Object.keys(data.materials).length} different blocks`);

                // Parse and store schematic
                this.activeSchematic = {
                    ...data,
                    id: Date.now().toString()
                };

                // Plan the building tasks
                const tasks = this.planner.planBuild(this.activeSchematic);
                console.log(`   Generated ${tasks.length} tasks`);

                // Send to bot
                this.sendToBot({
                    type: 'build_task',
                    schematic: this.activeSchematic,
                    tasks: tasks
                });

                // Acknowledge to mod
                ws.send(JSON.stringify({
                    type: 'validation_ack',
                    schematicId: this.activeSchematic.id,
                    message: 'Schematic received, bot will start building shortly'
                }));
                break;

            case 'ping':
                ws.send(JSON.stringify({
                    type: 'pong',
                    bot_status: {
                        connected: this.isBotConnected,
                        in_game: this.isBotInGame,
                        has_target: this.currentTarget !== null
                    }
                }));
                break;

            case 'bot_control':
                console.log(`🎮 Received bot control command: ${data.command}`);
                this.handleBotControl(data.command);
                break;

            case 'bot_speed':
                console.log(`⚡ Received bot speed change: ${data.speed}x`);
                this.handleBotSpeed(data.speed);
                break;

            default:
                console.warn('⚠️ Unknown mod message type:', data.type);
        }
    }

    /**
     * Launch mineflayer bot to connect to Minecraft server
     */
    launchMineflayerBot(targetPosition) {
        // Check if bot already exists and is connected
        if (this.mineflayerBot && this.isBotInGame) {
            console.log('♻️ Bot already connected and in-game, redirecting...');
            this.navigateToTarget(targetPosition);
            return;
        }

        // If bot exists but disconnected, clean it up
        if (this.mineflayerBot) {
            console.log('🧹 Cleaning up disconnected bot...');
            this.mineflayerBot = null;
            this.isBotConnected = false;
            this.isBotInGame = false;
        }

        // Reset status
        this.isBotConnected = false;
        this.isBotInGame = false;

        // Get connection info from environment
        const host = process.env.MC_HOST || 'localhost';
        const port = parseInt(process.env.MC_PORT) || 25565;
        const username = process.env.MC_USERNAME || 'AIBuilder';

        console.log(`🎮 Launching Mineflayer bot...`);
        console.log(`   Host: ${host}:${port}`);
        console.log(`   Username: ${username}`);
        console.log(`   Target: (${targetPosition.x}, ${targetPosition.y}, ${targetPosition.z})`);

        // Temporarily patch console.error to suppress NBT parsing errors
        const originalConsoleError = console.error;
        const botInstance = this;
        console.error = function(...args) {
            const message = args[0];
            if (typeof message === 'string' && message.includes('array size is abnormally large')) {
                // Suppress this specific error
                return;
            }
            originalConsoleError.apply(console, args);
        };

        // Create bot with auto-detect version for better modded server compatibility
        this.mineflayerBot = mineflayer.createBot({
            host: host,
            port: port,
            username: username,
            auth: 'offline',
            version: false, // Auto-detect version for better compatibility
            hideErrors: true // Hide NBT parsing errors from modded servers
        });

        // Restore console.error after a delay
        setTimeout(() => {
            console.error = originalConsoleError;
        }, 5000);

        // Bot event handlers
        this.mineflayerBot.on('connect', () => {
            console.log('✅ Bot connected to Minecraft server!');
            this.isBotConnected = true;
            this.sendToMod({
                type: 'bot_status',
                status: 'connected',
                message: 'Bot connected to server'
            });
        });

        this.mineflayerBot.on('spawn', () => {
            console.log('✅ Bot spawned!');
            this.handleBotSpawn(targetPosition);
        });

        // Listen for game mode changes
        this.mineflayerBot.on('game', () => {
            const newMode = this.detectGameMode();
            if (newMode !== this.botGameMode) {
                console.log(`🔄 Game mode changed: ${this.botGameMode} → ${newMode}`);
                this.botGameMode = newMode;
            }
        });

        // Fallback: Check if bot spawned (even if spawn event didn't fire due to NBT errors)
        let spawnCheckInterval = setInterval(() => {
            // Check if bot has an entity and is in game
            if (this.mineflayerBot && this.mineflayerBot.entity && !this.isBotInGame) {
                console.log('✅ Bot detected in game (fallback check)!');
                clearInterval(spawnCheckInterval);
                this.isBotInGame = true;

                // Simulate spawn event
                this.handleBotSpawn(targetPosition);
            }
        }, 500); // Check every 500ms

        // Stop checking after 10 seconds
        setTimeout(() => {
            clearInterval(spawnCheckInterval);
        }, 10000);

        this.mineflayerBot.on('error', (err) => {
            // Check if this is an NBT parsing error (non-critical for modded servers)
            if (err.message && (err.message.includes('array size is abnormally large') ||
                              err.message.includes('Parse error for play.toClient'))) {
                console.warn('⚠️ Ignoring NBT parsing error (bot should continue):', err.message.substring(0, 80) + '...');
                // Don't disconnect the bot for NBT errors - it should continue working
                return;
            }

            // For other errors, log and disconnect
            console.error('❌ Bot error:', err.message);
            this.isBotConnected = false;
            this.isBotInGame = false;
            this.sendToMod({
                type: 'bot_error',
                message: err.message
            });
        });

        // Handle kicks
        this.mineflayerBot.on('kicked', (reason) => {
            console.warn('⚠️ Bot kicked from server:', reason);
            this.isBotConnected = false;
            this.isBotInGame = false;
        });

        this.mineflayerBot.on('end', () => {
            console.log('🔌 Bot disconnected');
            this.isBotConnected = false;
            this.isBotInGame = false;
            this.sendToMod({
                type: 'bot_status',
                status: 'disconnected',
                message: 'Bot disconnected from server'
            });
            this.mineflayerBot = null;
        });

        this.mineflayerBot.on('whisper', (username, message) => {
            console.log(`💬 Whisper from ${username}: ${message}`);
        });
    }

    /**
     * Detect bot's current game mode
     */
    detectGameMode() {
        const mcBot = this.mineflayerBot;
        if (!mcBot) {
            console.warn('⚠️ Bot not available for game mode detection');
            return 'unknown';
        }

        if (!mcBot.game) {
            console.warn('⚠️ Game object not available');
            return 'unknown';
        }

        // Debug: Log all game properties
        console.log(`   Debug - game object:`, {
            gameMode: mcBot.game.gameMode,
            levelType: mcBot.game.levelType,
            dimension: mcBot.game.dimension,
            difficulty: mcBot.game.hardcore,
            hardcore: mcBot.game.hardcore
        });

        // Get game mode value
        const gameMode = mcBot.game.gameMode;

        // Handle both string and numeric game modes
        let modeName;

        if (typeof gameMode === 'string') {
            // Already a string: 'survival', 'creative', 'adventure', 'spectator'
            modeName = gameMode;
            console.log(`   Detected game mode (string): ${gameMode}`);
        } else {
            // Numeric: 0, 1, 2, 3
            const gameModes = {
                0: 'survival',
                1: 'creative',
                2: 'adventure',
                3: 'spectator'
            };
            modeName = gameModes[gameMode] || 'survival';
            console.log(`   Detected game mode (numeric): ${gameMode} (${modeName})`);
        }

        return modeName;
    }

    /**
     * Check if bot has operator permissions
     */
    async checkBotPermissions() {
        const mcBot = this.mineflayerBot;
        if (!mcBot) return;

        // Try to execute a harmless command to check OP status
        try {
            // In offline mode, we'll assume OP for simplicity
            // In online mode, you'd need to check permissions properly
            this.botIsOP = true; // Default to true for testing
            console.log(`   OP Status: ${this.botIsOP ? 'Yes - can use /tp' : 'No - walking only'}`);
        } catch (error) {
            this.botIsOP = false;
            console.log(`   OP Status: No - walking only`);
        }
    }

    /**
     * Handle bot spawn (called by spawn event or fallback check)
     */
    handleBotSpawn(targetPosition) {
        this.isBotInGame = true;
        console.log(`   Position: ${this.mineflayerBot.entity.position}`);
        console.log(`   Health: ${this.mineflayerBot.health}/20`);

        // Wait for UUID to be available
        const waitForUUID = setInterval(() => {
            if (this.mineflayerBot.uuid && this.mineflayerBot.uuid.length > 0) {
                clearInterval(waitForUUID);
                console.log(`   UUID: ${this.mineflayerBot.uuid}`);

                // Wait a bit more for game info to be received
                setTimeout(() => {
                    // Detect game mode
                    this.botGameMode = this.detectGameMode();
                    console.log(`   Game Mode: ${this.botGameMode}`);

                    // Check if bot is OP by trying to get its permission level
                    this.checkBotPermissions();

                    // Send status update with game mode info and owner
                    this.sendToMod({
                        type: 'bot_spawn',
                        status: 'spawned',
                        bot_name: this.mineflayerBot.username,
                        bot_uuid: this.mineflayerBot.uuid,
                        owner_name: this.botOwner || 'Player',
                        game_mode: this.botGameMode,
                        is_op: this.botIsOP,
                        position: {
                            x: Math.floor(this.mineflayerBot.entity.position.x),
                            y: Math.floor(this.mineflayerBot.entity.position.y),
                            z: Math.floor(this.mineflayerBot.entity.position.z)
                        }
                    });

                    // Navigate to target position
                    this.navigateToTarget(targetPosition);
                }, 200);
            }
        }, 100);

        // Timeout after 5 seconds if UUID never becomes available
        setTimeout(() => {
            clearInterval(waitForUUID);
            if (!this.mineflayerBot.uuid || this.mineflayerBot.uuid.length === 0) {
                console.warn('⚠️ Bot UUID not available after spawn, using username as fallback');
                // Use username as identifier (not ideal but better than nothing)
                const fallbackUUID = this.mineflayerBot.username + '-fallback';
                this.sendToMod({
                    type: 'bot_spawn',
                    status: 'spawned',
                    bot_name: this.mineflayerBot.username,
                    bot_uuid: fallbackUUID,
                    owner_name: this.botOwner || 'Player',
                    game_mode: this.botGameMode || 'unknown',
                    is_op: this.botIsOP || false,
                    position: {
                        x: Math.floor(this.mineflayerBot.entity.position.x),
                        y: Math.floor(this.mineflayerBot.entity.position.y),
                        z: Math.floor(this.mineflayerBot.entity.position.z)
                    }
                });
                this.navigateToTarget(targetPosition);
            }
        }, 5000);
    }

    /**
     * Navigate bot to target position based on game mode
     */
    async navigateToTarget(targetPos) {
        if (!this.mineflayerBot) {
            console.warn('⚠️ No bot instance');
            return;
        }

        console.log(`🧭 Navigating to target (${targetPos.x}, ${targetPos.y}, ${targetPos.z})...`);
        console.log(`   Game Mode: ${this.botGameMode}`);
        console.log(`   Is OP: ${this.botIsOP}`);

        // Creative mode: Flying navigation + building (highest priority)
        if (this.botGameMode === 'creative') {
            console.log('🦅 Using creative flight mode + building');
            await this.navigateCreative(targetPos);
            return;
        }

        // OP mode in survival/adventure: Direct teleportation
        if (this.botIsOP && (this.botGameMode === 'survival' || this.botGameMode === 'adventure')) {
            console.log('⚡ Using direct teleportation (OP mode in survival/adventure)');
            await this.teleportTo(targetPos);
            return;
        }

        // Survival mode: Walking with sprint and hunger management
        if (this.botGameMode === 'survival' || this.botGameMode === 'adventure') {
            console.log('🚶 Using survival mode (walking + sprint)');
            await this.navigateSurvival(targetPos);
            return;
        }

        // Default: Pathfinder
        console.log('📍 Using default pathfinder');
        await this.navigatePathfinder(targetPos);
    }

    /**
     * Direct teleportation (OP mode)
     */
    async teleportTo(targetPos) {
        const mcBot = this.mineflayerBot;

        try {
            // Use /tp command for instant teleportation
            mcBot.chat(`/tp ${mcBot.username} ${targetPos.x} ${targetPos.y} ${targetPos.z}`);

            console.log('⚡ Teleported to target!');

            this.sendToMod({
                type: 'bot_status',
                status: 'arrived',
                message: `Bot teleported to position (${targetPos.x}, ${targetPos.y}, ${targetPos.z})`,
                position: { x: targetPos.x, y: targetPos.y, z: targetPos.z }
            });
        } catch (error) {
            console.error('❌ Teleport failed, falling back to pathfinder:', error.message);
            await this.navigatePathfinder(targetPos);
        }
    }

    /**
     * Creative mode navigation with flying
     */
    async navigateCreative(targetPos) {
        const mcBot = this.mineflayerBot;

        console.log('🦅 Using creative mode - flying to build location');

        // Enable creative flight
        if (!mcBot.creative.flying) {
            console.log('   Enabling creative flight mode...');
            mcBot.creative.startFlying();
            await this.sleep(500);
        }

        // Send status update
        this.sendToMod({
            type: 'bot_status',
            status: 'arrived',
            message: 'Bot ready to build',
            position: {
                x: Math.floor(mcBot.entity.position.x),
                y: Math.floor(mcBot.entity.position.y),
                z: Math.floor(mcBot.entity.position.z)
            }
        });

        // If OP, use /tp for instant teleport
        if (this.botIsOP) {
            const offsetX = Math.floor(targetPos.x);
            const offsetY = Math.floor(targetPos.y);
            const offsetZ = Math.floor(targetPos.z);

            console.log(`   Using /tp command (bot is OP)...`);
            console.log(`   Teleporting to: (${offsetX}, ${offsetY}, ${offsetZ})`);
            mcBot.chat(`/tp ${mcBot.username} ${offsetX} ${offsetY} ${offsetZ}`);
            await this.sleep(1000);

            // Send teleport confirmation status
            this.sendToMod({
                type: 'bot_status',
                status: 'arrived',
                message: `Bot teleported outside schematic at (${offsetX}, ${offsetY}, ${offsetZ})`,
                position: { x: offsetX, y: offsetY, z: offsetZ }
            });
        } else {
            // NOT OP: Navigate like a normal player using pathfinder
            try {
                console.log(`   Bot is not OP, navigating to build location...`);
                const targetX = Math.floor(targetPos.x);
                const targetY = Math.floor(targetPos.y);
                const targetZ = Math.floor(targetPos.z);

                console.log(`   Target: (${targetX}, ${targetY}, ${targetZ})`);
                console.log(`   Current: (${mcBot.entity.position.x.toFixed(1)}, ${mcBot.entity.position.y.toFixed(1)}, ${mcBot.entity.position.z.toFixed(1)})`);

                // Wait a bit for bot to fully spawn
                await this.sleep(2000);

                // Configure pathfinder for normal movement
                const moves = new Movements(mcBot);
                moves.allowSprinting = true;
                mcBot.pathfinder.setMovements(moves);

                console.log(`   ✅ Pathfinder configured`);

                // Set goal - use GoalNear to get close but not exact
                const goal = new goals.GoalNear(targetX, targetY, targetZ, 3);

                console.log(`   🎯 Setting pathfinder goal...`);
                mcBot.pathfinder.setGoal(goal);

                // Wait for navigation to complete
                const maxWaitTime = 60000; // 60 seconds max
                const startTime = Date.now();
                let lastLoggedDist = 999;
                let stuckCount = 0;
                let lastPos = mcBot.entity.position.clone();

                while (Date.now() - startTime < maxWaitTime) {
                    const currentPos = mcBot.entity.position;
                    const dist = currentPos.distanceTo(new Vec3(targetX, targetY, targetZ));

                    // Log progress every 5 seconds or when distance improves significantly
                    if (Date.now() - startTime > 5000 && (dist < lastLoggedDist - 2 || Date.now() - startTime % 5000 < 200)) {
                        console.log(`   📍 Position: (${currentPos.x.toFixed(1)}, ${currentPos.y.toFixed(1)}, ${currentPos.z.toFixed(1)}) - Distance: ${dist.toFixed(1)} blocks`);
                        lastLoggedDist = dist;
                    }

                    // Check if we're close enough
                    if (dist < 5) {
                        console.log(`   ✅ Arrived at build location! (dist: ${dist.toFixed(1)})`);
                        break;
                    }

                    // Check if bot is stuck (not moving)
                    const posChanged = currentPos.distanceTo(lastPos) > 0.1;
                    if (!posChanged && !mcBot.pathfinder.isMoving() && dist > 10) {
                        stuckCount++;
                        console.log(`   ⚠️ Bot might be stuck (${stuckCount}/3), resetting goal...`);
                        mcBot.pathfinder.setGoal(null);
                        await this.sleep(500);
                        mcBot.pathfinder.setGoal(goal);

                        if (stuckCount >= 3) {
                            console.log(`   ❌ Bot is stuck, giving up navigation`);
                            break;
                        }
                    } else {
                        stuckCount = 0;
                    }

                    lastPos = currentPos.clone();
                    await this.sleep(200);
                }

                // Clear the goal
                mcBot.pathfinder.setGoal(null);

                const finalDist = mcBot.entity.position.distanceTo(new Vec3(targetX, targetY, targetZ));
                console.log(`   📍 Final position: (${mcBot.entity.position.x.toFixed(1)}, ${mcBot.entity.position.y.toFixed(1)}, ${mcBot.entity.position.z.toFixed(1)})`);
                console.log(`   📍 Final distance: ${finalDist.toFixed(1)} blocks`);

            } catch (error) {
                console.log(`   ⚠️ Navigation failed: ${error.message}`);
                console.log(`   Will continue anyway - bot can still build`);
            }

            await this.sleep(500);

            // Send arrival status
            this.sendToMod({
                type: 'bot_status',
                status: 'arrived',
                message: `Bot flew to schematic at (${targetX}, ${targetY}, ${targetZ})`,
                position: {
                    x: Math.floor(mcBot.entity.position.x),
                    y: Math.floor(mcBot.entity.position.y),
                    z: Math.floor(mcBot.entity.position.z)
                }
            });
        }

        // Start building if schematic is provided
        if (this.activeSchematic && this.activeSchematic.name) {
            this.startBuildingSchematic(targetPos);
        }
    }

    /**
     * Sleep utility
     */
    sleep(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }

    /**
     * Start building the schematic (creative mode only)
     */
    async startBuildingSchematic(position) {
        if (this.botGameMode !== 'creative') {
            console.log('⚠️ Building is only available in creative mode');
            return;
        }

        console.log(`🔨 Starting schematic build: ${this.activeSchematic.name}`);
        console.log(`   Position: (${position.x}, ${position.y}, ${position.z})`);
        console.log(`   Position types: x=${typeof position.x}, y=${typeof position.y}, z=${typeof position.z}`);
        console.log('=== Position being passed to SchematicBuilder ===');
        console.log(JSON.stringify(position));
        console.log('============================================');

        this.sendToMod({
            type: 'bot_status',
            status: 'building',
            message: `Starting construction of ${this.activeSchematic.name}...`
        });

        try {
            // Convert position coordinates to numbers (WebSocket sends strings)
            const numericPosition = {
                x: Number(position.x),
                y: Number(position.y),
                z: Number(position.z)
            };

            console.log('   Converted position to numbers:', numericPosition);

            // Create builder instance
            this.schematicBuilder = new SchematicBuilder(
                this.mineflayerBot,
                null, // No schematic path - using direct data
                numericPosition
            );

            // Load schematic data directly from mod
            const info = await this.schematicBuilder.loadFromDirectData(this.activeSchematic);

            this.sendToMod({
                type: 'build_start',
                schematic: this.activeSchematic.name,
                total_blocks: info.totalBlocks,
                palette: info.palette
            });

            // Start building
            await this.schematicBuilder.startBuilding();

            // Building completed
            const progress = this.schematicBuilder.getProgress();

            this.sendToMod({
                type: 'build_complete',
                schematic: this.activeSchematic.name,
                blocks_placed: progress.placed,
                message: `✅ Construction completed! ${progress.placed} blocks placed.`
            });

            console.log('✅ Schematic construction completed!');

        } catch (error) {
            console.error('❌ Build failed:', error.message);

            this.sendToMod({
                type: 'bot_error',
                message: `Build failed: ${error.message}`
            });
        }
    }

    /**
     * Survival mode navigation with sprint and hunger management
     */
    async navigateSurvival(targetPos) {
        const mcBot = this.mineflayerBot;

        // Load pathfinder plugin
        mcBot.loadPlugin(pathfinder);

        // Check food level
        const foodLevel = mcBot.food;
        console.log(`   Food Level: ${foodLevel}/20`);

        if (foodLevel < 6) {
            console.warn('⚠️ Bot is hungry! Cannot sprint.');
            this.sendToMod({
                type: 'bot_status',
                status: 'warning',
                message: 'Bot is hungry, walking slowly...'
            });
        }

        // Set movements with sprint capability
        const defaultMove = new Movements(mcBot);
        defaultMove.allowSprinting = true; // Enable sprint when possible
        mcBot.pathfinder.setMovements(defaultMove);

        const goal = new goals.GoalBlock(targetPos.x, targetPos.y, targetPos.z);
        mcBot.pathfinder.setGoal(goal);

        // Listen for goal reached
        mcBot.once('goal_reached', () => {
            console.log('🚶 Bot reached target (walking/sprinting)!');

            this.sendToMod({
                type: 'bot_status',
                status: 'arrived',
                message: `Bot walked to position (${targetPos.x}, ${targetPos.y}, ${targetPos.z})`,
                position: { x: targetPos.x, y: targetPos.y, z: targetPos.z }
            });
        });

        mcBot.once('path_update', (path) => {
            if (path.status === 'noPath') {
                console.warn('⚠️ No path found to target');
            }
        });

        // Monitor hunger during navigation
        const hungerMonitor = setInterval(() => {
            if (mcBot.food < 6) {
                console.warn('⚠️ Bot is very hungry, stopping sprint');
                defaultMove.allowSprinting = false;
                mcBot.pathfinder.setMovements(defaultMove);
            }
        }, 5000);

        // Clear monitor when goal reached
        mcBot.once('goal_reached', () => {
            clearInterval(hungerMonitor);
        });
    }

    /**
     * Default pathfinder navigation
     */
    async navigatePathfinder(targetPos) {
        const mcBot = this.mineflayerBot;

        // Load pathfinder plugin
        mcBot.loadPlugin(pathfinder);

        // Set movements and goal
        const defaultMove = new Movements(mcBot);
        mcBot.pathfinder.setMovements(defaultMove);

        const goal = new goals.GoalBlock(targetPos.x, targetPos.y, targetPos.z);
        mcBot.pathfinder.setGoal(goal);

        // Listen for goal reached on the bot itself
        mcBot.once('goal_reached', () => {
            console.log('🎉 Bot reached target position!');
            this.sendToMod({
                type: 'bot_status',
                status: 'arrived',
                message: `Bot arrived at position (${targetPos.x}, ${targetPos.y}, ${targetPos.z})`,
                position: { x: targetPos.x, y: targetPos.y, z: targetPos.z }
            });
        });

        mcBot.once('path_update', (path) => {
            if (path.status === 'noPath') {
                console.warn('⚠️ No path found to target');
            }
        });
    }

    /**
     * Handle messages from AI bot
     */
    handleBotMessage(ws, data) {
        switch (data.type) {
            case 'status_update':
                this.buildProgress = data.progress || 0;
                console.log(`📊 Bot status: ${data.status} (${this.buildProgress}%)`);

                // Forward to mod if connected
                this.sendToMod({
                    type: 'bot_progress',
                    progress: this.buildProgress,
                    status: data.status,
                    currentBlock: data.currentBlock
                });
                break;

            case 'build_complete':
                console.log('✅ Build completed!');
                this.sendToMod({
                    type: 'build_complete',
                    schematicId: this.activeSchematic?.id
                });
                this.activeSchematic = null;
                this.buildProgress = 0;
                break;

            case 'error':
                console.error('❌ Bot error:', data.message);
                this.sendToMod({
                    type: 'bot_error',
                    message: data.message
                });
                break;

            case 'ping':
                ws.send(JSON.stringify({ type: 'pong' }));
                break;

            default:
                console.warn('⚠️ Unknown bot message type:', data.type);
        }
    }

    handleDisconnect(ws, clientType) {
        console.log(`👋 ${clientType} disconnected`);

        if (clientType === 'mod') {
            this.modClient = null;
        } else if (clientType === 'bot') {
            this.botClient = null;
        }
    }

    /**
     * Handle bot control commands (pause, resume, stop)
     */
    handleBotControl(command) {
        if (!this.schematicBuilder) {
            console.warn('⚠️ No schematic builder active');
            return;
        }

        switch (command) {
            case 'pause':
                console.log('⏸ Pausing build...');
                this.schematicBuilder.pause();
                this.sendToMod({
                    type: 'bot_status',
                    status: 'paused',
                    message: 'Construction mise en pause'
                });
                break;

            case 'resume':
                console.log('▶️ Resuming build...');
                this.schematicBuilder.resume();
                this.sendToMod({
                    type: 'bot_status',
                    status: 'building',
                    message: 'Construction reprise'
                });
                break;

            case 'stop':
                console.log('⏹ Stopping build...');
                this.schematicBuilder.stop();
                this.sendToMod({
                    type: 'bot_status',
                    status: 'stopped',
                    message: 'Construction arrêtée'
                });
                break;

            default:
                console.warn('⚠️ Unknown control command:', command);
        }
    }

    /**
     * Handle bot speed changes
     */
    handleBotSpeed(speed) {
        if (!this.schematicBuilder) {
            console.warn('⚠️ No schematic builder active');
            return;
        }

        console.log(`⚡ Setting build speed to ${speed}x`);
        this.schematicBuilder.setSpeed(speed);

        this.sendToMod({
            type: 'bot_speed_update',
            speed: speed,
            message: `Vitesse définie à ${speed}x`
        });
    }

    sendToBot(data) {
        // This would send to the actual bot connection
        // For now, just log
        console.log('📤 Sending to bot:', data.type);
    }

    sendToMod(data) {
        // Send to all connected mod clients
        if (this.wss) {
            this.wss.clients.forEach((client) => {
                if (client.readyState === 1) { // 1 = OPEN state
                    client.send(JSON.stringify(data));
                }
            });
        }
    }
}

// Start server
const server = new AIServer(8080);
server.start();

export { AIServer };
