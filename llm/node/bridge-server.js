/**
 * Bridge Server for Minecraft RL System
 * Communicates between Python RL Agent and Node.js Minecraft Bot
 *
 * Protocol:
 * - Python sends actions → Node executes via Mineflayer → Returns observations
 * - WebSocket or HTTP communication
 */

import * as WebSocket from 'ws';
import { EventEmitter } from 'events';
import Vec3 from 'vec3';

/**
 * Bridge Server Class
 * Handles communication between Python RL agent and Minecraft bot
 */
class MinecraftBridgeServer extends EventEmitter {
    constructor(port = 8765, botClient = null) {
        super();
        this.port = port;
        this.botClient = botClient; // Mineflayer bot instance
        this.wss = null;
        this.clients = new Set();
        this.currentEpisode = 0;
        this.currentStep = 0;

        // Message queues
        this.actionQueue = [];
        this.observationQueue = [];
    }

    /**
     * Start the WebSocket server
     */
    start() {
        this.wss = new WebSocket.WebSocketServer({ port: this.port });

        this.wss.on('listening', () => {
            console.log(`🌉 Minecraft Bridge Server listening on port ${this.port}`);
        });

        this.wss.on('connection', (ws, req) => {
            this.handleConnection(ws, req);
        });

        this.wss.on('error', (error) => {
            console.error('❌ Bridge server error:', error);
        });
    }

    /**
     * Handle new WebSocket connection
     */
    handleConnection(ws, req) {
        const clientId = `${req.socket.remoteAddress}:${req.socket.remotePort}`;
        console.log(`✅ Python client connected: ${clientId}`);

        this.clients.add(ws);

        ws.on('message', (message) => {
            this.handleMessage(ws, message);
        });

        ws.on('close', () => {
            console.log(`❌ Python client disconnected: ${clientId}`);
            this.clients.delete(ws);
        });

        ws.on('error', (error) => {
            console.error(`❌ Client error:`, error);
        });

        // Send welcome message
        this.send(ws, {
            type: 'connected',
            message: 'Bridge connection established',
            protocol_version: '1.0'
        });
    }

    /**
     * Handle incoming message from Python
     */
    handleMessage(ws, message) {
        try {
            const data = JSON.parse(message);
            console.log(`📨 Received from Python: ${data.type}`);

            switch (data.type) {
                case 'reset':
                    this.handleReset(ws, data);
                    break;

                case 'step':
                    this.handleStep(ws, data);
                    break;

                case 'action':
                    this.handleAction(ws, data);
                    break;

                case 'ping':
                    this.send(ws, { type: 'pong' });
                    break;

                default:
                    console.warn(`⚠️ Unknown message type: ${data.type}`);
            }
        } catch (error) {
            console.error('❌ Error handling message:', error);
            this.send(ws, {
                type: 'error',
                message: error.message
            });
        }
    }

    /**
     * Handle environment reset request
     */
    handleReset(ws, data) {
        console.log('🔄 Resetting environment...');

        this.currentEpisode++;
        this.currentStep = 0;

        // Reset bot if needed (respawn, clear inventory, etc.)
        if (this.botClient) {
            this.executeBotReset();
        }

        // Get initial state
        const state = this.getCurrentState();

        this.send(ws, {
            type: 'reset_complete',
            episode_id: this.currentEpisode,
            observation: state
        });
    }

    /**
     * Handle step request
     */
    handleStep(ws, data) {
        console.log(`📍 Step ${this.currentStep} for episode ${this.currentEpisode}`);

        this.currentStep++;

        // Get current state
        const state = this.getCurrentState();

        // Calculate reward (would be done by Python side)
        const reward = 0;

        // Check if done
        const done = this.checkTermination();

        this.send(ws, {
            type: 'step_complete',
            episode_id: this.currentEpisode,
            step: this.currentStep,
            observation: state,
            reward: reward,
            done: done
        });
    }

    /**
     * Handle action execution request
     */
    handleAction(ws, data) {
        const { action_type, target_pos, target_block, slot_index } = data.action;

        console.log(`🎮 Executing action ${action_type} (ep: ${this.currentEpisode}, step: ${this.currentStep})`);

        let success = false;
        let error = null;

        try {
            // Execute action via bot
            if (this.botClient) {
                success = this.executeBotAction(data.action);
            } else {
                // No bot - simulate success for testing
                success = true;
            }
        } catch (e) {
            error = e.message;
            console.error('❌ Action execution failed:', e);
        }

        // Get next state after action
        const next_state = this.getCurrentState();

        this.send(ws, {
            type: 'action_complete',
            episode_id: this.currentEpisode,
            step: this.currentStep,
            success: success,
            error: error,
            observation: next_state
        });
    }

    /**
     * Execute bot action using Mineflayer
     */
    executeBotAction(action) {
        if (!this.botClient || !this.botClient.mineflayerBot) {
            console.warn('⚠️ No bot client available');
            return false;
        }

        const bot = this.botClient.mineflayerBot;
        const { action_type, target_pos, target_block, slot_index } = action;

        try {
            switch (action_type) {
                case 0: // NOOP
                    return true;

                case 1: // MOVE_FORWARD
                    bot.setControlState('forward', true);
                    setTimeout(() => bot.setControlState('forward', false), 100);
                    return true;

                case 2: // MOVE_BACKWARD
                    bot.setControlState('back', true);
                    setTimeout(() => bot.setControlState('back', false), 100);
                    return true;

                case 3: // MOVE_LEFT
                    bot.setControlState('left', true);
                    setTimeout(() => bot.setControlState('left', false), 100);
                    return true;

                case 4: // MOVE_RIGHT
                    bot.setControlState('right', true);
                    setTimeout(() => bot.setControlState('right', false), 100);
                    return true;

                case 5: // JUMP
                    bot.setControlState('jump', true);
                    setTimeout(() => bot.setControlState('jump', false), 100);
                    return true;

                case 13: // SELECT_SLOT
                    if (slot_index !== undefined && slot_index >= 0 && slot_index < 9) {
                        bot.setQuickBarSlot(slot_index);
                        return true;
                    }
                    return false;

                case 19: // PLACE_BLOCK
                    // This would use the bot's block placing logic
                    // Implementation depends on Mineflayer API
                    return this.executePlaceBlock(bot, target_pos, target_block);

                case 21: // DIG_FORWARD
                    return this.executeDig(bot);

                // Add more actions as needed...

                default:
                    console.warn(`⚠️ Unimplemented action type: ${action_type}`);
                    return false;
            }
        } catch (error) {
            console.error(`❌ Error executing action ${action_type}:`, error);
            return false;
        }
    }

    /**
     * Execute place block action
     */
    async executePlaceBlock(bot, targetPos, blockType) {
        if (!targetPos) return false;

        try {
            const block = bot.blockAt(targetPos.x, targetPos.y, targetPos.z);
            if (!block) return false;

            await bot.placeBlock(block, new Vec3(targetPos.x, targetPos.y, targetPos.z));
            return true;
        } catch (error) {
            console.error('❌ Place block failed:', error);
            return false;
        }
    }

    /**
     * Execute dig action
     */
    async executeDig(bot) {
        try {
            const block = bot.blockAtCursor(5);
            if (!block || block.name === 'air') {
                return false;
            }

            await bot.dig(block);
            return true;
        } catch (error) {
            console.error('❌ Dig failed:', error);
            return false;
        }
    }

    /**
     * Reset bot state (respawn, etc.)
     */
    executeBotReset() {
        if (!this.botClient || !this.botClient.mineflayerBot) {
            return;
        }

        const bot = this.botClient.mineflayerBot;

        // Clear controls
        bot.clearControlStates();

        // Reset to spawn if needed
        // This would depend on the bot implementation

        console.log('🔄 Bot reset complete');
    }

    /**
     * Get current game state from bot
     */
    getCurrentState() {
        if (!this.botClient || !this.botClient.mineflayerBot || !this.botClient.isInGame) {
            // Return default state for testing
            return this.getDefaultState();
        }

        const bot = this.botClient.mineflayerBot;

        return {
            position: [bot.entity.position.x, bot.entity.position.y, bot.entity.position.z],
            rotation: [bot.entity.yaw, bot.entity.pitch],
            velocity: [bot.entity.velocity.x, bot.entity.velocity.y, bot.entity.velocity.z],
            on_ground: bot.entity.onGround ? 1 : 0,
            in_water: bot.entity.isInWater ? 1 : 0,
            health: bot.health || 20,
            food: bot.food || 20,
            saturation: bot.saturation || 20,
            inventory: this.getInventoryState(bot),
            hotbar_selected: bot.quickBarSlot || 0,
            visible_blocks: this.getVisibleBlocks(bot),
            nearby_entities: this.getNearbyEntities(bot),
            time_of_day: bot.time ? bot.time.timeOfDay || 0 : 0,
            is_raining: bot.isRaining ? 1 : 0,
            biome_id: this.getBiomeId(bot),
            held_item: this.getHeldItem(bot),
            armor: this.getArmorState(bot)
        };
    }

    /**
     * Get inventory state from bot
     */
    getInventoryState(bot) {
        // Return flat array: 36 slots × 2 values [item_id, count]
        const inventory = [];

        for (let i = 0; i < 36; i++) {
            const item = bot.inventory.slots[i];
            if (item) {
                inventory.push(item.type || 0);
                inventory.push(item.count || 0);
            } else {
                inventory.push(0);
                inventory.push(0);
            }
        }

        return inventory;
    }

    /**
     * Get visible blocks (simplified version)
     */
    getVisibleBlocks(bot) {
        // Return flat array: 100 blocks × 4 values [x, y, z, block_id]
        // For now, return zeros (will be filled by raycasting later)
        const blocks = [];
        for (let i = 0; i < 100; i++) {
            blocks.push(0, 0, 0, 0);  // x, y, z, block_id
        }
        return blocks;
    }

    /**
     * Get nearby entities
     */
    getNearbyEntities(bot) {
        // Return flat array: 10 entities × 4 values [type, x, y, z]
        const entities = new Array(40).fill(0);  // Default to zeros
        const nearbyEntities = Object.values(bot.entities);
        let idx = 0;

        for (const entity of nearbyEntities) {
            if (idx >= 10) break;  // Max 10 entities
            if (entity.position.distanceTo(bot.entity.position) < 10) {
                entities[idx * 4] = entity.name || entity.type || 0;
                entities[idx * 4 + 1] = entity.position.x;
                entities[idx * 4 + 2] = entity.position.y;
                entities[idx * 4 + 3] = entity.position.z;
                idx++;
            }
        }

        return entities;
    }

    /**
     * Get biome ID (simplified)
     */
    getBiomeId(bot) {
        // This would get the actual biome
        return 1; // Default to plains
    }

    /**
     * Get held item ID
     */
    getHeldItem(bot) {
        const slot = bot.inventory.slots[bot.quickBarSlot];
        return slot ? slot.type : 0;
    }

    /**
     * Get armor state
     */
    getArmorState(bot) {
        return [
            bot.inventory.slots[5]?.type || 0,  // head
            bot.inventory.slots[6]?.type || 0,  // chest
            bot.inventory.slots[7]?.type || 0,  // legs
            bot.inventory.slots[8]?.type || 0   // feet
        ];
    }

    /**
     * Get default state for testing
     */
    getDefaultState() {
        return {
            position: [0, 64, 0],
            rotation: [0, 0],
            velocity: [0, 0, 0],
            on_ground: 1,
            in_water: 0,
            health: 20,
            food: 20,
            saturation: 20,
            inventory: new Array(72).fill(0),  // 36 slots × 2
            hotbar_selected: 0,
            visible_blocks: new Array(400).fill(0),  // 100 blocks × 4
            nearby_entities: new Array(40).fill(0),  // 10 entities × 4
            time_of_day: 0,
            is_raining: 0,
            biome_id: 1,
            held_item: 0,
            armor: [0, 0, 0, 0]  // [head, chest, legs, feet]
        };
    }

    /**
     * Check termination condition
     */
    checkTermination() {
        if (!this.botClient || !this.botClient.mineflayerBot) {
            return false;
        }

        // Death
        if (this.botClient.mineflayerBot.health <= 0) {
            return true;
        }

        return false;
    }

    /**
     * Send message to client
     */
    send(ws, data) {
        if (ws.readyState === WebSocket.OPEN) {
            ws.send(JSON.stringify(data));
        }
    }

    /**
     * Broadcast message to all clients
     */
    broadcast(data) {
        for (const ws of this.clients) {
            this.send(ws, data);
        }
    }

    /**
     * Stop the server
     */
    stop() {
        console.log('🛑 Stopping bridge server...');
        for (const ws of this.clients) {
            ws.close();
        }
        if (this.wss) {
            this.wss.close();
        }
        console.log('✅ Bridge server stopped');
    }

    /**
     * Set bot client
     */
    setBotClient(botClient) {
        this.botClient = botClient;
        console.log('✅ Bot client set');
    }
}

export default MinecraftBridgeServer;
