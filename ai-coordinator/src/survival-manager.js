import Vec3 from 'vec3';

/**
 * Survival Mode Manager
 * Handles base establishment, resource management, crafting, and furnace operations
 */
export class SurvivalManager {
    constructor(bot, schematicOrigin) {
        this.bot = bot;
        this.schematicOrigin = schematicOrigin;

        // Base location
        this.baseLocation = null; // {x, y, z} - Home position
        this.baseChest = null; // Position of chest
        this.baseCraftingTable = null; // Position of crafting table
        this.baseFurnaces = []; // Array of furnace positions

        // Resource tracking
        this.requiredMaterials = new Map(); // block name -> count needed
        this.availableMaterials = new Map(); // block name -> count in inventory/chest
    }

    /**
     * Phase 1: Establish Base (2x4 perimeter)
     * - Find suitable location near schematic
     * - Clear area
     * - Place chest, crafting table, furnaces
     */
    async establishBase() {
        console.log(`\n🏠 PHASE 1: ESTABLISHING BASE...`);
        console.log(`   Schematic origin: (${this.schematicOrigin.x}, ${this.schematicOrigin.y}, ${this.schematicOrigin.z})`);

        // Step 1: Find a suitable base location
        const basePos = await this.findBaseLocation();
        if (!basePos) {
            throw new Error('Could not find suitable base location!');
        }

        this.baseLocation = basePos;
        console.log(`   ✅ Base location found: (${basePos.x}, ${basePos.y}, ${basePos.z})`);

        // Step 2: Clear the area
        console.log(`   🧹 Clearing base area (2x4)...`);
        await this.clearBaseArea(basePos);
        console.log(`   ✅ Base area cleared`);

        // Step 3: Place chest
        console.log(`   📦 Placing chest...`);
        this.baseChest = await this.placeBlock(basePos.x, basePos.y, basePos.z, 'chest');
        console.log(`   ✅ Chest placed at (${this.baseChest.x}, ${this.baseChest.y}, ${this.baseChest.z})`);

        // Step 4: Place crafting table
        console.log(`   🔨 Placing crafting table...`);
        this.baseCraftingTable = await this.placeBlock(basePos.x + 1, basePos.y, basePos.z, 'crafting_table');
        console.log(`   ✅ Crafting table placed at (${this.baseCraftingTable.x}, ${this.baseCraftingTable.y}, ${this.baseCraftingTable.z})`);

        // Step 5: Place furnace(s)
        console.log(`   🔥 Placing furnace...`);
        const furnace = await this.placeBlock(basePos.x + 2, basePos.y, basePos.z, 'furnace');
        this.baseFurnaces.push(furnace);
        console.log(`   ✅ Furnace placed at (${furnace.x}, ${furnace.y}, ${furnace.z})`);

        console.log(`\n✅ BASE ESTABLISHED SUCCESSFULLY!`);
        console.log(`   Home: (${basePos.x}, ${basePos.y}, ${basePos.z})`);
        return this.baseLocation;
    }

    /**
     * Find a suitable base location near the schematic
     * Looks for flat 2x4 area within 3-4 blocks of schematic border
     */
    async findBaseLocation() {
        const bot = this.bot;
        const schematicX = this.schematicOrigin.x;
        const schematicZ = this.schematicOrigin.z;

        console.log(`   🔍 Searching for base location near schematic...`);

        // Search in a spiral pattern around the schematic
        const searchRadius = 10;
        const directions = [
            { x: -1, z: 0 },  // West
            { x: 1, z: 0 },   // East
            { x: 0, z: -1 },  // North
            { x: 0, z: 1 }    // South
        ];

        for (const dir of directions) {
            for (let dist = 4; dist <= searchRadius; dist++) {
                const testX = schematicX + dir.x * dist;
                const testZ = schematicZ + dir.z * dist;

                // Find ground level at this position
                const groundY = await this.findGroundLevel(testX, testZ);

                if (groundY === null) {
                    continue; // No valid ground here
                }

                // Check if 2x4 area is flat
                let isFlat = true;
                for (let dx = 0; dx < 2; dx++) {
                    for (let dz = 0; dz < 4; dz++) {
                        const checkY = await this.findGroundLevel(testX + dx, testZ + dz);
                        if (checkY !== groundY) {
                            isFlat = false;
                            break;
                        }
                    }
                    if (!isFlat) break;
                }

                if (isFlat) {
                    console.log(`   Found flat area at (${testX}, ${groundY}, ${testZ})`);
                    return { x: testX, y: groundY, z: testZ };
                }
            }
        }

        return null; // No suitable location found
    }

    /**
     * Find ground level at a given X, Z position
     * Returns Y level or null if no solid ground found
     */
    async findGroundLevel(x, z) {
        const bot = this.bot;

        // Search from Y=256 down to Y=0
        for (let y = 256; y >= 0; y--) {
            const pos = new Vec3(x, y, z);
            const block = bot.blockAt(pos);

            if (block && block.name !== 'air') {
                // Found solid block
                return y;
            }
        }

        return null; // No solid ground found
    }

    /**
     * Clear the base area (remove grass, flowers, etc.)
     */
    async clearBaseArea(basePos) {
        const bot = this.bot;

        for (let dx = 0; dx < 2; dx++) {
            for (let dz = 0; dz < 4; dz++) {
                const x = basePos.x + dx;
                const z = basePos.z + dz;
                const pos = new Vec3(x, basePos.y, z);
                const block = bot.blockAt(pos);

                // Remove any non-air block except bedrock
                if (block && block.name !== 'air' && block.name !== 'bedrock') {
                    try {
                        // Move closer
                        const dist = Math.sqrt(
                            Math.pow(bot.entity.position.x - x, 2) +
                            Math.pow(bot.entity.position.y - basePos.y, 2) +
                            Math.pow(bot.entity.position.z - z, 2)
                        );

                        if (dist > 5) {
                            // Use pathfinder to get closer
                            bot.pathfinder.setGoal(new (require('mineflayer-pathfinder').goals.GoalNear)(x, basePos.y, z, 2));
                            await new Promise(resolve => {
                                const timeout = setTimeout(resolve, 5000);
                                bot.once('goal_reached', () => {
                                    clearTimeout(timeout);
                                    resolve();
                                });
                            });
                        }

                        await bot.lookAt(pos);
                        await bot.dig(block, { timeout: 5000 });
                        console.log(`     Cleared ${block.name} at (${x}, ${basePos.y}, ${z})`);
                        await this.sleep(100);
                    } catch (err) {
                        console.warn(`     Warning: Could not clear block at (${x}, ${basePos.y}, ${z}): ${err.message}`);
                    }
                }
            }
        }
    }

    /**
     * Place a block at the specified position
     */
    async placeBlock(x, y, z, blockName) {
        const bot = this.bot;

        // Find the block in inventory
        const item = bot.inventory.items().find(i => i.name === blockName);
        if (!item) {
            throw new Error(`Block ${blockName} not found in inventory!`);
        }

        await bot.equip(item, 'hand');
        await this.sleep(100);

        // Find reference block
        const targetPos = new Vec3(x, y, z);
        const refBlock = this.findReferenceBlock(targetPos);

        if (!refBlock) {
            throw new Error(`No reference block found for (${x}, ${y}, ${z})`);
        }

        // Calculate face
        const face = this.getFaceToClick(targetPos, refBlock.position);

        // Move into position
        const botPos = new Vec3(
            targetPos.x - face.x * 3,
            targetPos.y - face.y * 3,
            targetPos.z - face.z * 3
        );

        bot.pathfinder.setGoal(new (require('mineflayer-pathfinder').goals.GoalNear)(botPos.x, botPos.y, botPos.z, 1));
        await new Promise(resolve => {
            const timeout = setTimeout(resolve, 4000);
            bot.once('goal_reached', () => {
                clearTimeout(timeout);
                resolve();
            });
        });

        await this.sleep(200);

        // Look at and place block
        const lookAtPos = new Vec3(
            refBlock.position.x + 0.5 + face.x * 0.5,
            refBlock.position.y + 0.5 + face.y * 0.5,
            refBlock.position.z + 0.5 + face.z * 0.5
        );

        await bot.lookAt(lookAtPos);
        await this.sleep(200);

        await bot.placeBlock(refBlock, face, { timeout: 5000 });
        await this.sleep(100);

        return { x, y, z };
    }

    /**
     * Find a reference block to place against
     */
    findReferenceBlock(targetPos) {
        const bot = this.bot;

        const directions = [
            { x: 0, y: -1, z: 0 }, // down
            { x: 0, y: 1, z: 0 },  // up
            { x: 1, y: 0, z: 0 },  // east
            { x: -1, y: 0, z: 0 }, // west
            { x: 0, y: 0, z: 1 },  // south
            { x: 0, y: 0, z: -1 }  // north
        ];

        for (const dir of directions) {
            const checkPos = new Vec3(
                targetPos.x + dir.x,
                targetPos.y + dir.y,
                targetPos.z + dir.z
            );

            const block = bot.blockAt(checkPos);
            if (block && block.name !== 'air') {
                return block;
            }
        }

        return null;
    }

    /**
     * Get which face to click on the reference block
     */
    getFaceToClick(targetPos, refPos) {
        const dx = Math.sign(targetPos.x - refPos.x);
        const dy = Math.sign(targetPos.y - refPos.y);
        const dz = Math.sign(targetPos.z - refPos.z);

        return new Vec3(dx, dy, dz);
    }

    /**
     * Sleep utility
     */
    sleep(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }
}
