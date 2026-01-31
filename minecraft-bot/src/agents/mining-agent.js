import { BaseAgent } from './base-agent.js';

/**
 * Mining Agent
 * Handles resource gathering and block mining
 */
export class MiningAgent extends BaseAgent {
    constructor(bot) {
        super(bot);
        this.name = 'MiningAgent';
    }

    /**
     * Gather resources based on material requirements
     */
    async gatherResources(materials) {
        this.log('Starting resource gathering...');

        for (const [blockId, count] of Object.entries(materials)) {
            this.log(`Need ${count}x ${blockId}`);

            // Check if we already have enough
            const currentCount = this.countItem(blockId);
            if (currentCount >= count) {
                this.log(`Already have ${currentCount}x ${blockId}`);
                continue;
            }

            const needed = count - currentCount;
            await this.gatherBlock(blockId, needed);
        }

        this.log('Resource gathering complete!');
    }

    /**
     * Gather a specific number of blocks
     */
    async gatherBlock(blockType, count) {
        this.log(`Gathering ${count}x ${blockType}`);

        let gathered = 0;

        while (gathered < count) {
            const block = this.findNearestBlock(blockType, 128);

            if (!block) {
                this.log(`No more ${blockType} found nearby`, 'warn');
                break;
            }

            try {
                await this.mineBlock(block);
                gathered++;
                this.log(`Gathered ${gathered}/${count} ${blockType}`);
            } catch (error) {
                this.log(`Failed to mine block: ${error.message}`, 'error');
                break;
            }

            // Small delay to avoid overwhelming
            await this.sleep(500);
        }
    }

    /**
     * Mine a specific block
     */
    async mineBlock(block) {
        // Move to block
        await this.moveToBlock(block);

        // Equip appropriate tool
        await this.equipToolForBlock(block);

        // Mine the block
        try {
            await this.bot.dig(block);
            this.log(`Mined block at ${block.x}, ${block.y}, ${block.z}`);
        } catch (error) {
            this.log(`Failed to dig: ${error.message}`, 'error');
            throw error;
        }
    }

    /**
     * Find nearest tree
     */
    async findNearestTree(maxDistance = 64) {
        const logTypes = ['oak_log', 'birch_log', 'spruce_log', 'jungle_log'];

        for (const logType of logTypes) {
            const block = this.findNearestBlock(logType, maxDistance);
            if (block) {
                return block;
            }
        }

        return null;
    }

    /**
     * Find nearest ore
     */
    async findNearestOre(oreType, maxDistance = 128) {
        const block = this.findNearestBlock(oreType, maxDistance);
        return block;
    }

    /**
     * Create mineshaft
     */
    async createMineshaft(depth = 60) {
        this.log(`Creating mineshaft to Y=${depth}`);

        const currentY = Math.floor(this.bot.entity.position.y);

        if (currentY > depth) {
            this.log(`Digging down to Y=${depth}`);

            while (Math.floor(this.bot.entity.position.y) > depth) {
                const below = this.bot.blockAt(this.bot.entity.position.offset(0, -1, 0));

                if (below.name === 'bedrock') {
                    this.log('Reached bedrock', 'warn');
                    break;
                }

                try {
                    await this.bot.dig(below);
                } catch (error) {
                    this.log(`Cannot dig here: ${error.message}`, 'warn');
                    break;
                }

                await this.sleep(500);
            }
        }

        this.log('Mineshaft created');
    }

    /**
     * Equip appropriate tool for block type
     */
    async equipToolForBlock(block) {
        const blockName = block.name;

        // Determine best tool
        let toolType = null;
        if (blockName.includes('log') || blockName.includes('wood')) {
            toolType = 'axe';
        } else if (blockName.includes('stone') || blockName.includes('ore') || blockName.includes('coal')) {
            toolType = 'pickaxe';
        } else if (blockName.includes('dirt') || blockName.includes('grass') || blockName.includes('sand')) {
            toolType = 'shovel';
        }

        if (toolType) {
            // Try to equip best available tool
            const tools = ['diamond', 'iron', 'stone', 'wood'];

            for (const material of tools) {
                if (await this.equipItem(`${material}_${toolType}`)) {
                    this.log(`Equipped ${material} ${toolType}`);
                    return;
                }
            }

            this.log(`No ${toolType} available`, 'warn');
        }
    }

    /**
     * Sleep helper
     */
    sleep(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }
}
