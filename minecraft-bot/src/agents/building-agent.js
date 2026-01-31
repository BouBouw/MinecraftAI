import { BaseAgent } from './base-agent.js';

/**
 * Building Agent
 * Handles construction of schematics and structures
 */
export class BuildingAgent extends BaseAgent {
    constructor(bot) {
        super(bot);
        this.name = 'BuildingAgent';
        this.currentSchematic = null;
    }

    /**
     * Build a layer of the schematic
     */
    async buildLayer(layerNumber) {
        this.log(`Building layer ${layerNumber}`);

        if (!this.currentSchematic) {
            this.log('No schematic loaded', 'error');
            return false;
        }

        const { dimensions, position } = this.currentSchematic;
        const blocks = this.currentSchematic.blocks;

        // Get blocks for this layer
        const layerBlocks = this.getLayerBlocks(layerNumber);

        this.log(`Layer ${layerNumber} has ${layerBlocks.length} blocks`);

        // Build each block in the layer
        let built = 0;
        for (const block of layerBlocks) {
            try {
                await this.placeBlock(block.position, block.type);
                built++;

                if (built % 10 === 0) {
                    this.log(`Built ${built}/${layerBlocks.length} blocks`);
                }
            } catch (error) {
                this.log(`Failed to place block at ${block.position}: ${error.message}`, 'error');
            }
        }

        this.log(`Layer ${layerNumber} complete! ✅`);
        return true;
    }

    /**
     * Get blocks for a specific layer
     */
    getLayerBlocks(layerNumber) {
        // This would parse the schematic and return blocks for this layer
        // For now, return empty array
        return [];
    }

    /**
     * Place a block at a specific position
     */
    async placeBlock(position, blockType) {
        // Move to position
        const pos = {
            x: position.x,
            y: position.y,
            z: position.z
        };

        // Check if bot has the required block
        if (!this.hasItem(blockType)) {
            this.log(`Missing ${blockType}, cannot place`, 'error');
            throw new Error(`Missing block: ${blockType}`);
        }

        // Equip the block
        await this.equipItem(blockType);

        // Find a reference block (adjacent block to place against)
        const refBlock = this.findReferenceBlock(pos);

        if (!refBlock) {
            this.log('No reference block found', 'error');
            throw new Error('Cannot place block - no reference');
        }

        // Place the block
        try {
            await this.bot.placeBlock(refBlock, this.getPlaceFace(pos, refBlock.position));
            this.log(`Placed ${blockType} at ${pos.x}, ${pos.y}, ${pos.z}`);
            return true;
        } catch (error) {
            this.log(`Failed to place block: ${error.message}`, 'error');
            throw error;
        }
    }

    /**
     * Find a reference block adjacent to the target position
     */
    findReferenceBlock(targetPos) {
        const directions = [
            { x: 0, y: 1, z: 0 },  // above
            { x: 0, y: -1, z: 0 }, // below
            { x: 1, y: 0, z: 0 },  // north
            { x: -1, y: 0, z: 0 }, // south
            { x: 0, y: 0, z: 1 },  // east
            { x: 0, y: 0, z: -1 }  // west
        ];

        for (const dir of directions) {
            const checkPos = {
                x: targetPos.x + dir.x,
                y: targetPos.y + dir.y,
                z: targetPos.z + dir.z
            };

            const block = this.bot.blockAt(checkPos);
            if (block && block.name !== 'air') {
                return block;
            }
        }

        return null;
    }

    /**
     * Get the face to place against
     */
    getPlaceFace(targetPos, refBlockPos) {
        const dx = targetPos.x - refBlockPos.x;
        const dy = targetPos.y - refBlockPos.y;
        const dz = targetPos.z - refBlockPos.z;

        if (dy === 1) return new this.vec3(0, 1, 0);  // top
        if (dy === -1) return new this.vec3(0, -1, 0); // bottom
        if (dx === 1) return new this.vec3(1, 0, 0);  // north
        if (dx === -1) return new this.vec3(-1, 0, 0); // south
        if (dz === 1) return new this.vec3(0, 0, 1);  // east
        if (dz === -1) return new this.vec3(0, 0, -1); // west

        return new this.vec3(0, 1, 0); // default to top
    }

    /**
     * Set the current schematic to build
     */
    setSchematic(schematic) {
        this.currentSchematic = schematic;
        this.log(`Loaded schematic: ${schematic.name}`);
    }

    /**
     * Build the entire schematic
     */
    async buildSchematic(schematic) {
        this.log(`Starting build: ${schematic.name}`);

        this.setSchematic(schematic);

        // Build layer by layer
        for (let layer = 0; layer < schematic.dimensions.height; layer++) {
            await this.buildLayer(layer);
        }

        this.log(`Build complete: ${schematic.name} ✅`);
        return true;
    }

    /**
     * Build a wall
     */
    async buildWall(start, end, blockType, height = 3) {
        this.log(`Building wall from (${start.x}, ${start.y}, ${start.z}) to (${end.x}, ${end.y}, ${end.z})`);

        for (let y = 0; y < height; y++) {
            for (let x = start.x; x <= end.x; x++) {
                for (let z = start.z; z <= end.z; z++) {
                    const position = { x, y: start.y + y, z };
                    await this.placeBlock(position, blockType);
                }
            }
        }

        this.log('Wall complete! ✅');
    }

    /**
     * Build a floor
     */
    async buildFloor(start, end, blockType) {
        this.log(`Building floor from (${start.x}, ${start.y}, ${start.z}) to (${end.x}, ${end.y}, ${end.z})`);

        for (let x = start.x; x <= end.x; x++) {
            for (let z = start.z; z <= end.z; z++) {
                const position = { x, y: start.y, z };
                await this.placeBlock(position, blockType);
            }
        }

        this.log('Floor complete! ✅');
    }

    /**
     * Create scaffolding to reach high places
     */
    async createScaffolding(targetHeight) {
        this.log(`Creating scaffolding to Y=${targetHeight}`);

        const botY = Math.floor(this.bot.entity.position.y);

        if (botY >= targetHeight) {
            this.log('Already at target height');
            return;
        }

        const heightDifference = targetHeight - botY;

        // Place blocks underneath to climb up
        for (let i = 0; i < heightDifference; i++) {
            const pos = {
                x: Math.floor(this.bot.entity.position.x),
                y: botY + i,
                z: Math.floor(this.bot.entity.position.z)
            };

            // Jump and place block
            this.bot.setControlState('jump', true);
            await this.sleep(100);
            await this.placeBlock(pos, 'dirt');
            this.bot.setControlState('jump', false);
            await this.sleep(500);
        }

        this.log('Scaffolding complete');
    }

    /**
     * Sleep helper
     */
    sleep(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }

    /**
     * Vector3 helper
     */
    vec3(x, y, z) {
        return { x, y, z };
    }
}
