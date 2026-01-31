import { BaseAgent } from './base-agent.js';

/**
 * Inventory Agent
 * Manages bot's inventory and storage
 */
export class InventoryAgent extends BaseAgent {
    constructor(bot) {
        super(bot);
        this.name = 'InventoryAgent';
    }

    /**
     * Organize inventory
     */
    async organizeInventory() {
        this.log('Organizing inventory...');

        const items = this.bot.inventory.items();
        const organized = {};

        // Group items by type
        for (const item of items) {
            const category = this.categorizeItem(item);
            if (!organized[category]) {
                organized[category] = [];
            }
            organized[category].push(item);
        }

        this.log('Inventory organized');
        return organized;
    }

    /**
     * Categorize an item
     */
    categorizeItem(item) {
        const name = item.name;

        if (name.includes('log') || name.includes('wood')) return 'wood';
        if (name.includes('stone') || name.includes('cobble')) return 'stone';
        if (name.includes('ore')) return 'ore';
        if (name.includes('pickaxe') || name.includes('axe') || name.includes('shovel')) return 'tools';
        if (name.includes('food') || name.includes('bread') || name.includes('meat')) return 'food';
        if (name.includes('plank')) return 'planks';

        return 'other';
    }

    /**
     * Store items in a chest
     */
    async storeItems(chestPosition, itemNames = null) {
        this.log('Storing items in chest...');

        // Move to chest
        await this.moveToBlock(chestPosition);

        // Open chest
        const chestBlock = this.bot.blockAt(chestPosition);
        const chest = await this.bot.openChest(chestBlock);

        const items = this.bot.inventory.items();
        let stored = 0;

        for (const item of items) {
            // Filter by item names if specified
            if (itemNames && !itemNames.includes(item.name)) {
                continue;
            }

            try {
                // Move item to chest
                await chest.deposit(item.type, null, item.count);
                stored += item.count;
                this.log(`Stored ${item.count}x ${item.name}`);
            } catch (error) {
                this.log(`Failed to store ${item.name}: ${error.message}`, 'warn');
            }
        }

        chest.close();
        this.log(`Stored ${stored} items total`);
        return stored;
    }

    /**
     * Retrieve items from a chest
     */
    async retrieveItems(chestPosition, itemNames) {
        this.log('Retrieving items from chest...');

        // Move to chest
        await this.moveToBlock(chestPosition);

        // Open chest
        const chestBlock = this.bot.blockAt(chestPosition);
        const chest = await this.bot.openChest(chestBlock);

        const chestItems = chest.items();
        let retrieved = 0;

        for (const itemName of itemNames) {
            const item = chestItems.find(i => i.name === itemName);

            if (item) {
                try {
                    await chest.withdraw(item.type, null, item.count);
                    retrieved += item.count;
                    this.log(`Retrieved ${item.count}x ${item.name}`);
                } catch (error) {
                    this.log(`Failed to retrieve ${item.name}: ${error.message}`, 'warn');
                }
            }
        }

        chest.close();
        this.log(`Retrieved ${retrieved} items total`);
        return retrieved;
    }

    /**
     * Count empty slots in inventory
     */
    getEmptySlots() {
        const items = this.bot.inventory.items();
        const emptySlots = 36 - items.length; // 36 is standard inventory size
        return emptySlots;
    }

    /**
     * Check if inventory is full
     */
    isInventoryFull() {
        return this.getEmptySlots() === 0;
    }

    /**
     * Find item in inventory
     */
    findItem(itemName) {
        const items = this.bot.inventory.items();
        return items.find(i => i.name === itemName);
    }

    /**
     * Toss unwanted items
     */
    async tossItems(itemNames) {
        this.log('Tossing unwanted items...');

        for (const itemName of itemNames) {
            const items = this.bot.inventory.items().filter(i => i.name === itemName);

            for (const item of items) {
                try {
                    await this.bot.toss(item.type, null, item.count);
                    this.log(`Tossed ${item.count}x ${item.name}`);
                } catch (error) {
                    this.log(`Failed to toss ${item.name}: ${error.message}`, 'warn');
                }
            }
        }
    }

    /**
     * Get inventory summary
     */
    getInventorySummary() {
        const items = this.bot.inventory.items();
        const summary = {};

        for (const item of items) {
            if (!summary[item.name]) {
                summary[item.name] = 0;
            }
            summary[item.name] += item.count;
        }

        return summary;
    }
}
