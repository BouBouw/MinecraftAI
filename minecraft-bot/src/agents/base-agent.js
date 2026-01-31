import pathfinderPlugin from 'mineflayer-pathfinder';
const { goals } = pathfinderPlugin;

/**
 * Base Agent class
 * All other agents extend this class
 */
export class BaseAgent {
    constructor(bot) {
        this.bot = bot;
        this.name = 'BaseAgent';
    }

    /**
     * Log message with agent name
     */
    log(message, level = 'info') {
        const prefix = `[${this.name}]`;
        const timestamp = new Date().toLocaleTimeString();

        switch (level) {
            case 'error':
                console.error(`${timestamp} ${prefix} ${message}`);
                break;
            case 'warn':
                console.warn(`${timestamp} ${prefix} ${message}`);
                break;
            default:
                console.log(`${timestamp} ${prefix} ${message}`);
        }
    }

    /**
     * Find nearest block of type
     */
    findNearestBlock(blockType, maxDistance = 64) {
        const blocks = this.bot.findBlocks({
            matching: blockType,
            maxDistance: maxDistance,
            count: 1
        });

        if (blocks.length === 0) {
            return null;
        }

        return blocks[0];
    }

    /**
     * Move to a block position
     */
    async moveToBlock(block) {
        return new Promise((resolve, reject) => {
            const goal = new goals.GoalBlock(block.x, block.y, block.z);

            this.bot.pathfinder.setGoal(goal);

            this.bot.once('goal_reached', () => {
                resolve();
            });

            this.bot.once('path_stop', () => {
                reject(new Error('Could not reach block'));
            });

            setTimeout(() => reject(new Error('Movement timeout')), 30000);
        });
    }

    /**
     * Equip item from inventory
     */
    async equipItem(itemType) {
        const item = this.bot.inventory.items().find(i =>
            i.name.includes(itemType)
        );

        if (item) {
            await this.bot.equip(item, 'hand');
            return true;
        }

        return false;
    }

    /**
     * Check if bot has item in inventory
     */
    hasItem(itemName, count = 1) {
        const items = this.bot.inventory.items();
        const matchingItems = items.filter(i =>
            i.name.includes(itemName)
        );

        const totalCount = matchingItems.reduce((sum, item) => sum + item.count, 0);
        return totalCount >= count;
    }

    /**
     * Count items in inventory
     */
    countItem(itemName) {
        const items = this.bot.inventory.items();
        const matchingItems = items.filter(i =>
            i.name.includes(itemName)
        );

        return matchingItems.reduce((sum, item) => sum + item.count, 0);
    }
}
