/**
 * RL Coordinator - Integrates RL Agent with existing AI Coordinator
 * Bridges the RL system with the Minecraft bot system
 */

import WebSocket from 'ws';
import { spawn } from 'child_process';
import { EventEmitter } from 'events';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

/**
 * RL Coordinator Class
 * Manages communication between AI Coordinator and RL Agent
 */
class RLCoordinator extends EventEmitter {
    constructor(aiCoordinatorWs, config = {}) {
        super();

        this.aiCoordinatorWs = aiCoordinatorWs; // WebSocket to AI Coordinator
        this.config = config;

        // Python RL Agent process
        this.rlProcess = null;
        this.rlWs = null; // WebSocket to RL Agent

        // Communication state
        this.isRLAgentRunning = false;
        this.currentEpisode = 0;
        this.pendingActions = new Map();

        // Bind methods
        this.handleAIMessage = this.handleAIMessage.bind(this);
        this.handleRLMessage = this.handleRLMessage.bind(this);

        // Setup AI coordinator listener
        if (this.aiCoordinatorWs) {
            this.aiCoordinatorWs.on('message', this.handleAIMessage);
        }

        // RL Bridge server port
        this.rlBridgePort = config.rlBridgePort || 8765;
    }

    /**
     * Start the RL Agent
     */
    async startRLAgent() {
        console.log('🤖 Starting RL Agent...');

        // Spawn Python RL agent process
        const pythonPath = config.pythonPath || 'python';
        const trainScript = path.join(__dirname, '../../python/training/trainer.py');
        const configFile = path.join(__dirname, '../../config/rl_config.yaml');

        this.rlProcess = spawn(pythonPath, [
            trainScript,
            '--config', configFile
        ], {
            cwd: path.join(__dirname, '../../python'),
            stdio: 'pipe'
        });

        this.rlProcess.stdout.on('data', (data) => {
            console.log(`[RL Agent] ${data.toString()}`);
        });

        this.rlProcess.stderr.on('data', (data) => {
            console.error(`[RL Agent Error] ${data.toString()}`);
        });

        this.rlProcess.on('close', (code) => {
            console.log(`RL Agent process exited with code ${code}`);
            this.isRLAgentRunning = false;
            this.emit('rl_agent_stopped');
        });

        // Wait a bit for agent to start
        await this.sleep(2000);

        // Connect to RL Agent via WebSocket
        this.rlWs = new WebSocket(`ws://localhost:${this.rlBridgePort}`);

        this.rlWs.on('open', () => {
            console.log('✅ Connected to RL Agent');
            this.isRLAgentRunning = true;
            this.emit('rl_agent_started');
        });

        this.rlWs.on('message', this.handleRLMessage);

        this.rlWs.on('error', (error) => {
            console.error('RL Agent WebSocket error:', error);
        });

        this.rlWs.on('close', () => {
            console.log('RL Agent WebSocket disconnected');
            this.isRLAgentRunning = false;
            this.emit('rl_agent_stopped');
        });
    }

    /**
     * Handle messages from AI Coordinator
     */
    handleAIMessage(data) {
        try {
            const message = JSON.parse(data.toString());

            switch (message.type) {
                case 'bot_move_to_schematic':
                    this.handleMoveToSchematic(message);
                    break;

                case 'bot_status':
                    this.handleBotStatus(message);
                    break;

                case 'start_rl_training':
                    this.handleStartTraining(message);
                    break;

                case 'stop_rl_training':
                    this.handleStopTraining();
                    break;

                case 'get_rl_status':
                    this.sendRLStatus();
                    break;

                default:
                    console.log(`Unhandled AI message type: ${message.type}`);
            }
        } catch (error) {
            console.error('Error handling AI message:', error);
        }
    }

    /**
     * Handle messages from RL Agent
     */
    handleRLMessage(data) {
        try {
            const message = JSON.parse(data.toString());

            switch (message.type) {
                case 'action_request':
                    this.handleActionRequest(message);
                    break;

                case 'observation_request':
                    this.handleObservationRequest(message);
                    break;

                case 'episode_complete':
                    this.handleEpisodeComplete(message);
                    break;

                case 'training_progress':
                    this.emit('training_progress', message);
                    break;

                default:
                    console.log(`Unhandled RL message type: ${message.type}`);
            }
        } catch (error) {
            console.error('Error handling RL message:', error);
        }
    }

    /**
     * Handle move to schematic command
     */
    handleMoveToSchematic(message) {
        console.log('📍 Received move to schematic command (RL mode)');

        if (!this.isRLAgentRunning) {
            console.log('Starting RL Agent...');
            this.startRLAgent();
        }

        // Forward to RL agent
        this.sendToRL({
            type: 'navigate_to_target',
            target: message.target,
            schematic: message.schematic
        });
    }

    /**
     * Handle bot status updates
     */
    handleBotStatus(message) {
        // Forward bot status to RL agent
        if (this.isRLAgentRunning && this.rlWs && this.rlWs.readyState === WebSocket.OPEN) {
            this.sendToRL({
                type: 'bot_state_update',
                status: message.status,
                position: message.position,
                health: message.health,
                food: message.food
            });
        }
    }

    /**
     * Handle start training command
     */
    handleStartTraining(message) {
        console.log('🎓 Starting RL training...');

        if (!this.isRLAgentRunning) {
            this.startRLAgent();
        }

        // Send training parameters
        this.sendToRL({
            type: 'start_training',
            params: message.params || {}
        });
    }

    /**
     * Handle stop training command
     */
    handleStopTraining() {
        console.log('🛑 Stopping RL training');

        if (this.rlProcess) {
            this.rlProcess.kill('SIGTERM');
        }

        if (this.rlWs) {
            this.rlWs.close();
        }
    }

    /**
     * Handle action request from RL agent
     */
    async handleActionRequest(message) {
        const { episode_id, step, action } = message;

        console.log(`Executing RL action ${action} (ep: ${episode_id}, step: ${step})`);

        // Send action to AI coordinator to execute via bot
        this.sendToAI({
            type: 'execute_bot_action',
            action: action,
            rl_episode: episode_id,
            rl_step: step
        });
    }

    /**
     * Handle observation request from RL agent
     */
    handleObservationRequest(message) {
        const { episode_id, step } = message;

        // Request observation from bot
        this.sendToAI({
            type: 'get_observation',
            rl_episode: episode_id,
            rl_step: step
        });
    }

    /**
     * Handle episode complete from RL agent
     */
    handleEpisodeComplete(message) {
        const { episode_id, total_reward, length } = message;

        console.log(`Episode ${episode_id} complete: reward=${total_reward:.2f}, length=${length}`);

        this.currentEpisode = episode_id;

        // Forward to AI coordinator
        this.sendToAI({
            type: 'rl_episode_complete',
            episode_id: episode_id,
            total_reward: total_reward,
            length: length
        });
    }

    /**
     * Send RL status
     */
    sendRLStatus() {
        const status = {
            type: 'rl_status',
            is_running: this.isRLAgentRunning,
            current_episode: this.currentEpisode,
            config: this.config
        };

        this.sendToAI(status);
    }

    /**
     * Send message to RL Agent
     */
    sendToRL(data) {
        if (this.rlWs && this.rlWs.readyState === WebSocket.OPEN) {
            this.rlWs.send(JSON.stringify(data));
        } else {
            console.warn('RL Agent not connected, cannot send message');
        }
    }

    /**
     * Send message to AI Coordinator
     */
    sendToAI(data) {
        if (this.aiCoordinatorWs && this.aiCoordinatorWs.readyState === WebSocket.OPEN) {
            this.aiCoordinatorWs.send(JSON.stringify(data));
        } else {
            console.warn('AI Coordinator not connected, cannot send message');
        }
    }

    /**
     * Utility: Sleep function
     */
    sleep(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }

    /**
     * Stop the coordinator
     */
    stop() {
        console.log('🛑 Stopping RL Coordinator...');

        if (this.rlProcess) {
            this.rlProcess.kill('SIGTERM');
        }

        if (this.rlWs) {
            this.rlWs.close();
        }

        if (this.aiCoordinatorWs) {
            this.aiCoordinatorWs.removeEventListener('message', this.handleAIMessage);
        }

        console.log('✅ RL Coordinator stopped');
    }
}

export default RLCoordinator;
