/**
 * Communication handler for AI bot
 * Manages connection to the Mineflayer bot
 */
export class BotCommunication {
    constructor() {
        this.botConnected = false;
        this.botCallbacks = new Map();
    }

    /**
     * Send task to bot
     */
    sendTask(task) {
        if (!this.botConnected) {
            console.warn('⚠️ Bot not connected, queuing task');
            return false;
        }

        console.log(`📤 Sending task to bot: ${task.type}`);
        // This would send to the actual bot via WebSocket or other IPC
        return true;
    }

    /**
     * Send status query to bot
     */
    queryStatus() {
        if (!this.botConnected) {
            return null;
        }

        return {
            status: 'idle',
            progress: 0,
            inventory: {}
        };
    }

    /**
     * Register callback for bot events
     */
    on(event, callback) {
        if (!this.botCallbacks.has(event)) {
            this.botCallbacks.set(event, []);
        }
        this.botCallbacks.get(event).push(callback);
    }

    /**
     * Trigger event callbacks
     */
    emit(event, data) {
        const callbacks = this.botCallbacks.get(event);
        if (callbacks) {
            callbacks.forEach(cb => cb(data));
        }
    }

    /**
     * Set bot connection status
     */
    setConnected(connected) {
        this.botConnected = connected;
        this.emit(connected ? 'connected' : 'disconnected');
    }
}
