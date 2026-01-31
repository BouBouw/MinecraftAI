import fs from 'fs';
import nbt from 'prismarine-nbt';
import Vec3 from 'vec3';
import pkg from 'mineflayer-pathfinder';
import { SurvivalManager } from './survival-manager.js';
import { CraftSolver } from './craft-solver.js';
import { HumanBehavior } from './human-behavior.js';

// Get pathfinder components (same as server.js)
const { pathfinder, Movements, goals } = pkg;

/**
 * Schematic Builder - Constructs structures block by block
 * Uses right-click simulation like a real player
 */
export class SchematicBuilder {
    constructor(bot, schematicPath, origin) {
        this.bot = bot;
        this.schematicPath = schematicPath;
        this.origin = origin; // {x, y, z} - where to place the schematic

        console.log('=== SCHEMATIC BUILDER CONSTRUCTOR DEBUG ===');
        console.log('schematicPath:', schematicPath);
        console.log('origin received:', origin);
        console.log('origin type:', typeof origin);
        console.log('origin.x:', origin.x, 'type:', typeof origin.x);
        console.log('origin.y:', origin.y, 'type:', typeof origin.y);
        console.log('origin.z:', origin.z, 'type:', typeof origin.z);
        console.log('==========================================');

        this.blocks = [];
        this.currentIndex = 0;
        this.isBuilding = false;
        this.skippedBlocks = []; // Track blocks that couldn't be placed on first pass

        // Build control
        this.isPaused = false;
        this.isStopped = false;
        this.speedMultiplier = 1.0; // Speed multiplier for build and movement

        // Optional (decorative) blocks that can be skipped if too difficult
        this.optionalBlocks = new Set([
            'short_grass',
            'tall_grass',
            'seagrass',
            'tall_seagrass',
            'fern',
            'large_fern',
            'grass',
            'dead_bush',
            'flower',
            'sunflower',
            'lilac',
            'rose_bush',
            'peony',
            'white_carpet',
            'orange_carpet',
            'magenta_carpet',
            'light_blue_carpet',
            'yellow_carpet',
            'lime_carpet',
            'pink_carpet',
            'gray_carpet',
            'light_gray_carpet',
            'cyan_carpet',
            'purple_carpet',
            'blue_carpet',
            'brown_carpet',
            'green_carpet',
            'red_carpet',
            'black_carpet'
        ]);

        // Stats
        this.totalBlocks = 0;
        this.placedBlocks = 0;

        // Hotbar optimization
        this.hotbarCache = new Map(); // block name -> hotbar slot (0-8)
        this.currentHotbarSlots = new Array(9).fill(null); // Track what's in each slot

        // Scaffolding system
        this.scaffoldingBlocks = []; // Track temporary scaffolding blocks placed
        this.currentScaffoldingY = null; // Current scaffolding platform level

        // Survival mode manager
        this.survivalManager = null; // Will be initialized if in survival mode
        this.craftSolver = null; // Will be initialized if in survival mode
        this.humanBehavior = null; // Will be initialized for human-like behavior
    }

    /**
     * Load schematic and prepare for building
     */
    async loadSchematic() {
        try {
            console.log(`📂 Loading schematic: ${this.schematicPath}`);

            // Check if file exists
            if (!fs.existsSync(this.schematicPath)) {
                throw new Error(`Schematic file not found: ${this.schematicPath}`);
            }

            // Read the schematic file
            const data = fs.readFileSync(this.schematicPath);
            const fileContent = data.toString('utf8');

            // Check if file is JSON format (Sponge schematic)
            if (fileContent.trim().startsWith('{')) {
                console.log('📋 Detected Sponge JSON schematic format');
                return this.loadSpongeSchematic(JSON.parse(fileContent));
            }

            // Otherwise, try NBT format
            console.log('📦 Detected NBT schematic format');
            const parsed = await nbt.parse(data);

            const schematic = parsed.value.value.value;
            const width = schematic.Width.value;
            const height = schematic.Height.value;
            const length = schematic.Length.value;

            // Get block data
            const blockData = schematic.BlockData?.value || schematic.Blocks.value;
            const palette = schematic.Palette?.value || {};

            console.log(`   Dimensions: ${width}x${height}x${length}`);
            console.log(`   Palette size: ${Object.keys(palette).length} blocks`);

            // Parse blocks
            this.blocks = [];

            // Sponge schematic format
            if (schematic.BlockData !== undefined) {
                // Decode BlockData if it's a Buffer
                let decodedData;
                if (schematic.BlockData.Data) {
                    // Base64 encoded data - parse as varints
                    decodedData = Buffer.from(schematic.BlockData.Data, 'base64');

                    // Parse varint array
                    const blockIds = [];
                    let i = 0;
                    while (i < decodedData.length) {
                        let value = 0;
                        let shift = 0;
                        let b;
                        do {
                            b = decodedData[i++];
                            value |= (b & 0x7F) << shift;
                            shift += 7;
                        } while (b & 0x80);
                        blockIds.push(value);
                    }

                    console.log(`   Parsed ${blockIds.length} block IDs from varint format (NBT)`);

                    let index = 0;
                    for (let y = 0; y < height; y++) {
                        for (let z = 0; z < length; z++) {
                            for (let x = 0; x < width; x++) {
                                const blockId = blockIds[index];

                                // Skip air blocks
                                if (blockId !== 0) {
                                    const blockName = this.getBlockNameById(blockId, palette);

                                    // Calculate world position
                                    const worldPos = {
                                        x: this.origin.x + x,
                                        y: this.origin.y + y,
                                        z: this.origin.z + z
                                    };

                                    this.blocks.push({
                                        position: worldPos,
                                        name: blockName,
                                        local: { x, y, z }
                                    });
                                }

                                index++;
                            }
                        }
                    }
                } else {
                    decodedData = blockData;
                    // Legacy format without varints
                    let index = 0;
                    for (let y = 0; y < height; y++) {
                        for (let z = 0; z < length; z++) {
                            for (let x = 0; x < width; x++) {
                                const blockId = decodedData[index];

                                if (blockId !== 0) {
                                    const blockName = this.getBlockNameById(blockId, palette);

                                    const worldPos = {
                                        x: this.origin.x + x,
                                        y: this.origin.y + y,
                                        z: this.origin.z + z
                                    };

                                    this.blocks.push({
                                        position: worldPos,
                                        name: blockName,
                                        local: { x, y, z }
                                    });
                                }

                                index++;
                            }
                        }
                    }
                }
            }

            // Sort blocks by Y (build from bottom to top) for stability
            this.blocks.sort((a, b) => a.position.y - b.position.y);

            this.totalBlocks = this.blocks.length;
            this.currentIndex = 0;

            console.log(`✅ Schematic loaded: ${this.totalBlocks} blocks to place`);

            return {
                width,
                height,
                length,
                totalBlocks: this.totalBlocks,
                palette: Object.keys(palette)
            };

        } catch (error) {
            console.error('❌ Failed to load schematic:', error.message);
            throw error;
        }
    }

    /**
     * Load Sponge JSON schematic format
     */
    loadSpongeSchematic(json) {
        const width = json.Width;
        const height = json.Height;
        const length = json.Length;
        const palette = json.Palette;

        console.log(`   Dimensions: ${width}x${height}x${length}`);
        console.log(`   Palette size: ${Object.keys(palette).length} blocks`);

        // Debug: Show palette contents
        console.log(`   Palette contents:`);
        for (const [name, id] of Object.entries(palette)) {
            console.log(`     [${id}] = ${name}`);
        }

        console.log(`   DEBUG origin: (${this.origin.x}, ${this.origin.y}, ${this.origin.z})`);

        // Decode BlockData from base64
        const blockDataBuffer = Buffer.from(json.BlockData.Data, 'base64');

        // Parse varint array from BlockData
        const blockIds = [];
        let i = 0;
        while (i < blockDataBuffer.length) {
            let value = 0;
            let shift = 0;
            let b;
            do {
                b = blockDataBuffer[i++];
                value |= (b & 0x7F) << shift;
                shift += 7;
            } while (b & 0x80);
            blockIds.push(value);
        }

        console.log(`   Parsed ${blockIds.length} block IDs from varint format`);
        console.log(`   First 20 block IDs: ${blockIds.slice(0, 20).join(', ')}`);

        this.blocks = [];
        let index = 0;

        for (let y = 0; y < height; y++) {
            for (let z = 0; z < length; z++) {
                for (let x = 0; x < width; x++) {
                    const blockId = blockIds[index];

                    // Skip air blocks
                    if (blockId !== 0) {
                        // Find block name in palette
                        const blockName = this.getBlockNameById(blockId, palette);

                        const worldPos = {
                            x: this.origin.x + x,
                            y: this.origin.y + y,
                            z: this.origin.z + z
                        };

                        // Debug first block
                        if (this.blocks.length === 0) {
                            console.log(`   DEBUG first block calculation:`);
                            console.log(`     local=(${x},${y},${z})`);
                            console.log(`     origin=(${this.origin.x},${this.origin.y},${this.origin.z})`);
                            console.log(`     blockId from palette: ${blockId}`);
                            console.log(`     blockName: ${blockName}`);
                            console.log(`     worldPos calculation:`);
                            console.log(`       x: ${this.origin.x} + ${x} = ${worldPos.x}`);
                            console.log(`       y: ${this.origin.y} + ${y} = ${worldPos.y}`);
                            console.log(`       z: ${this.origin.z} + ${z} = ${worldPos.z}`);
                            console.log(`     result=(${worldPos.x}, ${worldPos.y}, ${worldPos.z})`);
                        }

                        this.blocks.push({
                            position: worldPos,
                            name: blockName,
                            local: { x, y, z }
                        });
                    }

                    index++;
                }
            }
        }

        // Sort blocks for layer-by-layer building:
        // 1. By Y (bottom to top)
        // 2. Within each layer: by Z (north to south)
        // 3. Within each row: by X (west to east)
        this.blocks.sort((a, b) => {
            if (a.position.y !== b.position.y) {
                return a.position.y - b.position.y; // Y ascending
            }
            if (a.position.z !== b.position.z) {
                return a.position.z - b.position.z; // Z ascending
            }
            return a.position.x - b.position.x; // X ascending
        });

        this.totalBlocks = this.blocks.length;
        this.currentIndex = 0;

        // Debug: Show unique block types
        const blockTypes = new Set(this.blocks.map(b => b.name));
        console.log(`   Block types to place: ${Array.from(blockTypes).join(', ')}`);

        console.log(`✅ Schematic loaded: ${this.totalBlocks} blocks to place`);

        return {
            width,
            height,
            length,
            totalBlocks: this.totalBlocks,
            palette: Object.keys(palette)
        };
    }

    /**
     * Get block name from palette by ID
     */
    getBlockNameById(blockId, palette) {
        for (const [name, id] of Object.entries(palette)) {
            if (id === blockId) {
                return name.replace('minecraft:', '');
            }
        }
        return 'stone'; // Default fallback
    }

    /**
     * Load schematic from direct block data (from Minecraft mod)
     * This bypasses file reading and uses exact data from the mod's preview
     */
    async loadFromDirectData(schematicData) {
        console.log('📦 Loading schematic from direct mod data');
        console.log(`   Dimensions: ${schematicData.dimensions.width}x${schematicData.dimensions.height}x${schematicData.dimensions.length}`);

        if (!schematicData.blocks_data || !schematicData.blocks_data.blocks) {
            throw new Error('No blocks data received from mod!');
        }

        const modBlocks = schematicData.blocks_data.blocks;
        const maxExpected = schematicData.dimensions.width * schematicData.dimensions.height * schematicData.dimensions.length;

        console.log(`   Received ${modBlocks.length} blocks from mod`);
        console.log(`   Dimensions: ${schematicData.dimensions.width}x${schematicData.dimensions.height}x${schematicData.dimensions.length}`);
        console.log(`   Expected max blocks: ${maxExpected}`);

        // Sanity check - if we received way too many blocks, there's a bug
        if (modBlocks.length > maxExpected * 2) {
            console.error(`   ❌ ERROR: Received ${modBlocks.length} blocks but expected max ${maxExpected}`);
            console.error(`   This indicates a bug in the mod's schematic loading!`);
            console.error(`   First 10 blocks:`, JSON.stringify(modBlocks.slice(0, 10), null, 2));
            throw new Error(`Invalid block data: received ${modBlocks.length} blocks for ${schematicData.dimensions.width}x${schematicData.dimensions.height}x${schematicData.dimensions.length} schematic (max ${maxExpected})`);
        }

        // Log first few blocks for debugging
        console.log(`   First 5 blocks from mod:`, JSON.stringify(modBlocks.slice(0, 5), null, 2));

        this.blocks = [];
        const blockTypes = new Set();

        // Process each block from mod
        for (const modBlock of modBlocks) {
            // Validate block data
            if (!modBlock.name) {
                console.error(`   ❌ Invalid block data: missing name`, JSON.stringify(modBlock));
                continue;
            }

            const worldPos = {
                x: this.origin.x + modBlock.x,
                y: this.origin.y + modBlock.y,
                z: this.origin.z + modBlock.z
            };

            // Convert mod block name to mineflayer format (with safety check)
            const blockName = modBlock.name.replace('minecraft:', '');

            this.blocks.push({
                position: worldPos,
                name: blockName,
                local: { x: modBlock.x, y: modBlock.y, z: modBlock.z }
            });

            blockTypes.add(blockName);
        }

        // Sort blocks for layer-by-layer building
        this.blocks.sort((a, b) => {
            if (a.position.y !== b.position.y) {
                return a.position.y - b.position.y;
            }
            if (a.position.z !== b.position.z) {
                return a.position.z - b.position.z;
            }
            return a.position.x - b.position.x;
        });

        this.totalBlocks = this.blocks.length;
        this.currentIndex = 0;

        console.log(`   Block types to place: ${Array.from(blockTypes).join(', ')}`);
        console.log(`✅ Schematic loaded from mod: ${this.totalBlocks} blocks to place`);

        return {
            width: schematicData.dimensions.width,
            height: schematicData.dimensions.height,
            length: schematicData.dimensions.length,
            totalBlocks: this.totalBlocks,
            palette: Array.from(blockTypes)
        };
    }

    /**
     * Start building the schematic - builds layer by layer (Y axis)
     */
    async startBuilding() {
        if (this.isBuilding) {
            console.warn('⚠️ Already building');
            return;
        }

        this.isBuilding = true;
        this.placedBlocks = 0;
        this.skippedBlocks = [];

        console.log(`🔨 Starting construction of ${this.totalBlocks} blocks...`);
        console.log(`   Origin: (${this.origin.x}, ${this.origin.y}, ${this.origin.z})`);
        console.log(`   Game mode: ${this.bot.game.gameMode}`);

        // SURVIVAL MODE: Initialize survival manager
        if (this.bot.game.gameMode !== 'creative') {
            console.log(`\n⚔️ SURVIVAL MODE DETECTED`);
            console.log(`   Initializing survival manager...`);

            this.survivalManager = new SurvivalManager(this.bot, this.origin);

            try {
                await this.survivalManager.establishBase();
            } catch (err) {
                console.error(`❌ Failed to establish base: ${err.message}`);
                console.error(`   Cannot proceed in survival mode without a base!`);
                this.isBuilding = false;
                throw err;
            }

            // Initialize craft solver and analyze requirements
            console.log(`\n🔧 Initializing craft solver...`);
            this.craftSolver = new CraftSolver(this.bot, this.survivalManager);
            this.craftSolver.analyzeRequirements(this.blocks);

            // Create and execute craft plan
            const craftPlan = await this.craftSolver.createCraftPlan();
            if (craftPlan.length > 0) {
                console.log(`\n📦 Need to craft/gather ${craftPlan.length} items before building...`);
                try {
                    await this.craftSolver.executeCraftPlan(craftPlan);
                } catch (err) {
                    console.error(`❌ Failed to execute craft plan: ${err.message}`);
                    console.error(`   Cannot proceed without required materials!`);
                    this.isBuilding = false;
                    throw err;
                }
            } else {
                console.log(`   ✅ All required materials available!`);
            }
        }

        // Initialize human-like behavior (works in both creative and survival)
        console.log(`\n🧠 Initializing human-like behavior...`);
        this.humanBehavior = new HumanBehavior(this.bot, this.survivalManager);
        console.log(`   ✅ Human behavior enabled (pauses, smooth rotation, mob defense)`);


        // =====================================================================
        // INTELLIGENT QUEUE-BASED CONSTRUCTION
        // =====================================================================
        // Instead of layer-by-layer, we use a dependency-based approach:
        // 1. Find blocks that have support (natural terrain or already placed)
        // 2. Place those blocks
        // 3. Repeat until all blocks are placed or no more progress can be made
        // =====================================================================

        console.log(`\n🏗️ Starting INTELLIGENT queue-based construction...`);
        console.log(`   This will build blocks based on support dependencies`);
        console.log(`   instead of fixed layer order`);

        // Track placed blocks positions (as "x,y,z" strings for fast lookup)
        const placedPositions = new Set();

        // Create a working copy of blocks to place
        let remainingBlocks = [...this.blocks];
        let iteration = 0;
        let stuckIterations = 0;

        // Wait for bot to be properly positioned after teleport
        // This ensures chunks are loaded around the schematic
        console.log(`\n⏳ Waiting for bot to settle after teleport...`);
        await this.sleep(2000);

        // DEBUG: Scan the world around origin to see what blocks exist
        console.log(`\n🔍 Scanning world around schematic origin to detect existing blocks...`);
        const bot = this.bot;
        const botPos = bot.entity.position;

        console.log(`   Bot position during scan: (${botPos.x.toFixed(1)}, ${botPos.y.toFixed(1)}, ${botPos.z.toFixed(1)})`);
        console.log(`   Schematic origin: (${this.origin.x}, ${this.origin.y}, ${this.origin.z})`);
        console.log(`   Distance from bot to origin: ${Math.sqrt(Math.pow(botPos.x - this.origin.x, 2) + Math.pow(botPos.y - this.origin.y, 2) + Math.pow(botPos.z - this.origin.z, 2)).toFixed(1)} blocks`);

        // Check a larger area: 11x11x11 area around origin (for better detection)
        let foundSolidBlocks = 0;
        const scanPositions = [];

        for (let dx = -5; dx <= 5; dx++) {
            for (let dy = -5; dy <= 5; dy++) {
                for (let dz = -5; dz <= 5; dz++) {
                    const checkPos = new Vec3(
                        this.origin.x + dx,
                        this.origin.y + dy,
                        this.origin.z + dz
                    );
                    const blockAtPos = bot.blockAt(checkPos);

                    if (blockAtPos && blockAtPos.name) {
                        scanPositions.push({
                            x: checkPos.x,
                            y: checkPos.y,
                            z: checkPos.z,
                            name: blockAtPos.name
                        });

                        if (blockAtPos.name !== 'air') {
                            foundSolidBlocks++;
                        }
                    }
                }
            }
        }

        console.log(`   Found ${foundSolidBlocks} solid blocks around origin (11x11x11 area)`);
        if (foundSolidBlocks > 0 && foundSolidBlocks <= 30) {
            console.log(`   Solid blocks near origin:`);
            for (const pos of scanPositions) {
                if (pos.name !== 'air') {
                    console.log(`     - (${pos.x}, ${pos.y}, ${pos.z}): ${pos.name}`);
                }
            }
        } else if (foundSolidBlocks === 0) {
            console.error(`   ❌ WARNING: No solid blocks found around origin!`);
            console.error(`   This means either:`);
            console.error(`   1. The schematic is truly floating (no terrain below)`);
            console.error(`   2. Chunks are not loaded around the schematic`);
            console.error(`   3. Bot is too far from the schematic to detect blocks`);
        }

        // Optimize hotbar once for all blocks (in creative mode)
        if (this.bot.game.gameMode === 'creative') {
            console.log(`\n🎒 Optimizing hotbar for all ${this.blocks.length} blocks...`);
            await this.optimizeHotbarForLayer(this.blocks);
        }

        while (remainingBlocks.length > 0) {
            // Wait while paused
            while (this.isPaused && !this.isStopped) {
                await this.sleep(500);
            }

            // Check if build was stopped
            if (this.isStopped) {
                console.log('⏹ Build stopped by user');
                break;
            }

            iteration++;
            console.log(`\n🔄 Iteration ${iteration}: ${remainingBlocks.length} blocks remaining`);

            // Find all blocks that currently have support
            const supportedBlocks = [];
            const unsupportedBlocks = [];

            for (const block of remainingBlocks) {
                if (this.hasBlockSupport(block, placedPositions)) {
                    supportedBlocks.push(block);
                } else {
                    unsupportedBlocks.push(block);
                }
            }

            console.log(`   ✅ Found ${supportedBlocks.length} blocks with support`);
            console.log(`   ⏳ ${unsupportedBlocks.length} blocks still lack support`);

            // If no blocks have support, try to place an anchor block
            if (supportedBlocks.length === 0) {
                console.warn(`   ⚠️ No blocks have support! Trying to place an anchor block...`);

                // Find the lowest block in the schematic (closest to potential ground)
                let lowestBlock = null;
                let lowestY = Infinity;

                for (const block of remainingBlocks) {
                    if (block.position.y < lowestY) {
                        lowestY = block.position.y;
                        lowestBlock = block;
                    }
                }

                if (lowestBlock) {
                    console.log(`   📍 Lowest block found at Y=${lowestY}, trying to place below it as anchor...`);

                    // Try to place a dirt block below the lowest schematic block
                    // This will serve as an anchor for the rest of the structure
                    try {
                        // Place a temporary dirt block at (lowestBlock.x, lowestBlock.y - 1, lowestBlock.z)
                        const anchorPos = {
                            x: lowestBlock.position.x,
                            y: lowestBlock.position.y - 1,
                            z: lowestBlock.position.z
                        };

                        console.log(`   📍 Placing anchor block at (${anchorPos.x}, ${anchorPos.y}, ${anchorPos.z})`);

                        // First, try to place a normal dirt block
                        const anchorPlaced = await this.placeAnchorBlock(anchorPos);

                        if (anchorPlaced) {
                            // Track the anchor position
                            const anchorKey = `${anchorPos.x},${anchorPos.y},${anchorPos.z}`;
                            placedPositions.add(anchorKey);
                            console.log(`   ✅ Anchor block placed! Retrying block placement...`);

                            // Don't break - continue to next iteration to place blocks with new anchor support
                            continue;
                        } else {
                            console.error(`   ❌ Failed to place anchor block. Cannot build floating schematic.`);
                            this.skippedBlocks = remainingBlocks;
                            break;
                        }
                    } catch (error) {
                        console.error(`   ❌ Failed to place anchor block: ${error.message}`);
                        this.skippedBlocks = remainingBlocks;
                        break;
                    }
                } else {
                    console.error(`   ❌ ERROR: No blocks have support! Cannot place any blocks.`);
                    console.error(`   This means the schematic is floating with no connection to terrain.`);
                    console.error(`   Remaining ${unsupportedBlocks.length} blocks cannot be placed.`);
                    this.skippedBlocks = unsupportedBlocks;
                    break;
                }
            }

            // Place all supported blocks
            console.log(`   🔨 Placing ${supportedBlocks.length} supported blocks...`);

            let placedThisIteration = 0;
            for (const block of supportedBlocks) {
                // Wait while paused
                while (this.isPaused && !this.isStopped) {
                    await this.sleep(500);
                }

                if (this.isStopped) {
                    break;
                }

                console.log(`🔨 [${placedThisIteration + 1}/${supportedBlocks.length}] Placing ${block.name}`);
                console.log(`   Position: (${block.position.x}, ${block.position.y}, ${block.position.z})`);

                try {
                    const placed = await this.placeBlock(block);

                    if (placed) {
                        // Track this position as placed
                        const posKey = `${block.position.x},${block.position.y},${block.position.z}`;
                        placedPositions.add(posKey);
                        placedThisIteration++;

                        // HUMAN BEHAVIOR: Maybe pause to "admire work"
                        if (this.humanBehavior) {
                            await this.humanBehavior.maybePause();
                        }

                        await this.sleep(50); // Small delay between blocks
                    } else {
                        // Keep in unsupported list for retry
                        unsupportedBlocks.push(block);
                    }
                } catch (error) {
                    console.error(`❌ Failed to place block: ${error.message}`);
                    unsupportedBlocks.push(block);
                }
            }

            console.log(`   ✅ Placed ${placedThisIteration} blocks in iteration ${iteration}`);
            console.log(`   Total progress: ${this.placedBlocks}/${this.totalBlocks} blocks (${((this.placedBlocks / this.totalBlocks) * 100).toFixed(1)}%)`);

            // Update remaining blocks (keep only unsupported)
            remainingBlocks = unsupportedBlocks;

            // Check for stuck condition (no progress made)
            if (placedThisIteration === 0) {
                stuckIterations++;
                if (stuckIterations >= 3) {
                    console.error(`   ❌ ERROR: No progress for 3 iterations! Stuck with ${remainingBlocks.length} blocks.`);
                    console.error(`   These blocks may be unreachable or lack support.`);
                    this.skippedBlocks = remainingBlocks;
                    break;
                }
            } else {
                stuckIterations = 0; // Reset if we made progress
            }
        }

        console.log(`\n✅ Construction completed! Total placed: ${this.placedBlocks} blocks`);
        if (this.skippedBlocks.length > 0) {
            console.warn(`⚠️ Warning: ${this.skippedBlocks.length} blocks could not be placed`);
            console.warn(`   These blocks may be unreachable or lack support from terrain/other blocks`);
        }
        this.isBuilding = false;
    }

    /**
     * Analyze block frequency in a layer and optimize hotbar
     * Pre-loads the 9 most frequent blocks into hotbar slots 0-8
     */
    async optimizeHotbarForLayer(layerBlocks) {
        if (this.bot.game.gameMode !== 'creative') {
            console.log(`   Hotbar optimization: Skipped (not in creative mode)`);
            return;
        }

        console.log(`\n🎒 Optimizing hotbar for layer (${layerBlocks.length} blocks)...`);

        // Count frequency of each block type in this layer
        const blockFrequency = new Map();
        for (const block of layerBlocks) {
            const name = block.name;
            blockFrequency.set(name, (blockFrequency.get(name) || 0) + 1);
        }

        // Sort by frequency (most frequent first)
        const sortedBlocks = Array.from(blockFrequency.entries())
            .sort((a, b) => b[1] - a[1]);

        console.log(`   Top 10 most frequent blocks in this layer:`);
        sortedBlocks.slice(0, 10).forEach(([name, count]) => {
            console.log(`     - ${name}: ${count} blocks`);
        });

        // Get top 9 blocks (or fewer if less than 9 types)
        const topBlocks = sortedBlocks.slice(0, 9).map(([name]) => name);

        console.log(`   Loading ${topBlocks.length} blocks into hotbar slots 0-8...`);

        // Clear current hotbar tracking
        this.currentHotbarSlots = new Array(9).fill(null);
        this.hotbarCache.clear();

        // Load each block into its hotbar slot (creative mode - using prismarine-item)
        try {
            // Import prismarine-item dynamically
            const { default: prismarineItem } = await import('prismarine-item');
            const Item = prismarineItem(this.bot.version);

            // Wait for inventory to be ready
            await this.sleep(500);

            for (let i = 0; i < topBlocks.length; i++) {
                const blockName = topBlocks[i];
                const item = this.bot.registry.itemsByName[blockName];

                if (!item) {
                    console.warn(`   ⚠️ Block ${blockName} not found in registry! Skipping.`);
                    console.warn(`      This is likely a modded block - will try to place anyway using fallback`);
                    continue;
                }

                // Create Item using prismarine-item (correct way for creative mode)
                const itemToSet = new Item(item.id, 64, 0);
                const slotIndex = 36 + i;

                console.log(`     Setting ${blockName} in slot ${i} (slotIndex ${slotIndex})...`);

                try {
                    await this.bot.creative.setInventorySlot(slotIndex, itemToSet);
                    await this.sleep(150);
                } catch (err) {
                    console.warn(`     ⚠️ Failed to set ${blockName} in slot ${i}: ${err.message}`);
                    continue; // Continue with next block instead of failing entire process
                }

                // Verify it was set
                const slotItem = this.bot.inventory.slots[slotIndex];
                if (slotItem && slotItem.name === blockName) {
                    console.log(`     ✅ Verified ${blockName} in slot ${i}`);
                } else {
                    console.warn(`     ⚠️ Failed to verify ${blockName} in slot ${i} (slot is ${slotItem ? slotItem.name : 'empty'})`);
                }

                // Update tracking
                this.currentHotbarSlots[i] = blockName;
                this.hotbarCache.set(blockName, i);
            }

            console.log(`   ✅ Hotbar optimized with ${this.currentHotbarSlots.filter(s => s !== null).length} blocks`);
        } catch (err) {
            console.error(`   ❌ Failed to optimize hotbar: ${err.message}`);
            console.error(`   Stack: ${err.stack}`);
        }
    }

    /**
     * Get the hotbar slot for a block, or load it if not in hotbar
     * Returns the hotbar slot number (0-8) or null if failed
     */
    async equipBlockForPlacement(blockName) {
        if (this.bot.game.gameMode !== 'creative') {
            // Survival mode: use normal equip
            const item = this.bot.inventory.items().find(i => i.name === blockName);
            if (!item) {
                console.warn(`   ⚠️ Block ${blockName} not found in inventory!`);
                return null;
            }
            await this.bot.equip(item, 'hand');
            await this.sleep(100);
            return this.bot.inventory.selectedSlot;
        }

        // Creative mode: use optimized hotbar
        const cachedSlot = this.hotbarCache.get(blockName);

        if (cachedSlot !== undefined) {
            // Block is already in hotbar
            if (this.bot.inventory.selectedSlot !== cachedSlot) {
                // Use bot.equip() to properly switch to the cached slot
                const slotIndex = 36 + cachedSlot;
                const item = this.bot.inventory.slots[slotIndex];

                if (item) {
                    try {
                        await this.bot.equip(item, 'hand');
                        await this.sleep(100);
                    } catch (err) {
                        // If equip fails, try direct slot change
                        console.warn(`   ⚠️ Equip failed, using direct slot change: ${err.message}`);
                        this.bot.inventory.selectedSlot = cachedSlot;
                        await this.sleep(100);
                    }
                } else {
                    this.bot.inventory.selectedSlot = cachedSlot;
                    await this.sleep(50);
                }
            }
            console.log(`   Hotbar: Using cached slot ${cachedSlot} for ${blockName}`);
            return cachedSlot;
        }

        // Block not in hotbar - find an available slot or reuse an existing one
        console.log(`   Hotbar: ${blockName} not cached, loading into available slot...`);

        try {
            const item = this.bot.registry.itemsByName[blockName];

            if (!item) {
                console.warn(`   ⚠️ Block ${blockName} not found in registry!`);
                console.warn(`      This is a MODDED block - trying to give using Minecraft ID directly...`);

                // Try to use any available slot and hope the server accepts it
                // For modded blocks, we'll try to give using /give command if OP
                try {
                    // Try using /give command
                    this.bot.chat(`/give ${this.bot.username} ${blockName}`);
                    await this.sleep(200);
                    this.bot.inventory.selectedSlot = 0;
                    console.log(`   ⚠️ Used /give command for modded block ${blockName}`);
                    return 0;
                } catch (err) {
                    console.warn(`   ⚠️ Could not give modded block ${blockName}: ${err.message}`);
                    return null;
                }
            }

            // Check if the block is already in any hotbar slot (even if not tracked)
            for (let slot = 0; slot < 9; slot++) {
                const slotIndex = 36 + slot;
                const slotItem = this.bot.inventory.slots[slotIndex];
                if (slotItem && slotItem.name === blockName) {
                    // Found it! Update tracking and select this slot
                    this.currentHotbarSlots[slot] = blockName;
                    this.hotbarCache.set(blockName, slot);
                    this.bot.inventory.selectedSlot = slot;
                    await this.sleep(50);
                    console.log(`   ✅ Found ${blockName} in existing hotbar slot ${slot}`);
                    return slot;
                }
            }

            // Find first available hotbar slot (preferably an empty one)
            let availableSlot = -1;
            for (let i = 0; i < 9; i++) {
                if (this.currentHotbarSlots[i] === null) {
                    availableSlot = i;
                    break;
                }
            }

            // If all slots are full, use slot 0 and replace its content
            if (availableSlot === -1) {
                availableSlot = 0;
                console.log(`     All hotbar slots full, replacing slot 0`);
            }

            // Use prismarine-item to create the item correctly
            const { default: prismarineItem } = await import('prismarine-item');
            const Item = prismarineItem(this.bot.version);

            const itemToSet = new Item(item.id, 64, 0);
            const slotIndex = 36 + availableSlot;

            console.log(`     Setting ${blockName} in slot ${availableSlot}...`);
            await this.bot.creative.setInventorySlot(slotIndex, itemToSet);
            await this.sleep(200);

            // Verify it was set
            const slotItem = this.bot.inventory.slots[slotIndex];
            if (!slotItem || slotItem.name !== blockName) {
                console.warn(`     ⚠️ Verification failed - slot is ${slotItem ? slotItem.name : 'empty'}`);
            }

            // Update tracking
            this.currentHotbarSlots[availableSlot] = blockName;
            this.hotbarCache.set(blockName, availableSlot);

            // Select the hotbar slot
            this.bot.inventory.selectedSlot = availableSlot;
            await this.sleep(50);

            console.log(`   ✅ Loaded ${blockName} into hotbar slot ${availableSlot}`);
            return availableSlot;
        } catch (err) {
            console.error(`   ❌ Failed to give block: ${err.message}`);
            return null;
        }
    }

    /**
     * Place a block at the specified position
     * Uses bot.placeBlock() for right-click simulation
     * In creative, bot should already have all blocks in inventory
     * Returns true if placed, false if skipped
     */
    async placeBlock(block) {
        const bot = this.bot;

        console.log(`   DEBUG: Starting placeBlock for ${block.name} at (${block.position.x}, ${block.position.y}, ${block.position.z})`);

        // Find reference block FIRST (before moving)
        const refBlock = this.findReferenceBlock(block.position);

        if (!refBlock) {
            // Check if this is an optional (decorative) block
            if (this.optionalBlocks.has(block.name)) {
                console.warn(`   ⊗ Skipping optional block '${block.name}' - no placement surface`);
                return true; // Return true so we don't retry optional blocks
            }
            console.warn(`   ⚠️ No adjacent block found to place against at (${block.position.x}, ${block.position.y}, ${block.position.z})`);
            return false; // Indicate block was not placed
        }

        console.log(`   DEBUG: refBlock found at (${refBlock.position.x}, ${refBlock.position.y}, ${refBlock.position.z})`);

        // CRITICAL: Enable creative flight BEFORE calculating position
        // In creative mode, bot should always be flying when building
        if (bot.game.gameMode === 'creative' && !bot.creative.flying) {
            console.log(`   Enabling creative flight mode`);
            bot.creative.startFlying();
        }

        // Calculate which face we're clicking on the reference block
        // face vector points FROM refBlock TO targetBlock
        const face = this.getFaceToClick(block.position, refBlock.position);

        // CRITICAL: Calculate the position where the bot should move to
        // In creative mode, we need special handling to avoid being AT the target block
        let targetPos;

        if (bot.game.gameMode === 'creative') {
            // In creative mode: position 1-2 blocks ABOVE the target block
            // This ensures the bot looks DOWN at the block instead of standing on it
            targetPos = new Vec3(
                block.position.x,  // Same X (will approach from side)
                block.position.y + 2,  // 2 blocks ABOVE target
                block.position.z   // Same Z (will approach from side)
            );
            console.log(`   Creative mode: positioning 2 blocks above target`);
        } else {
            // Normal mode: position based on face direction
            targetPos = new Vec3(
                block.position.x - face.x * 3,
                block.position.y - face.y * 3,
                block.position.z - face.z * 3
            );
        }

        console.log(`   Target block at: (${block.position.x}, ${block.position.y}, ${block.position.z})`);
        console.log(`   Face direction (ref→target): (${face.x}, ${face.y}, ${face.z})`);
        console.log(`   Bot should move to: (${targetPos.x}, ${targetPos.y}, ${targetPos.z})`);

        // Check current distance first
        const currentPos = bot.entity.position;
        const currentDist = Math.sqrt(
            Math.pow(currentPos.x - block.position.x, 2) +
            Math.pow(currentPos.y - block.position.y, 2) +
            Math.pow(currentPos.z - block.position.z, 2)
        );

        // No teleporting - bot will fly naturally to position in creative mode
        // Skip blocks that are too far away (will be retried later)
        if (bot.game.gameMode === 'creative' && currentDist > 30) {
            console.log(`   ⚠️ Block too far (${currentDist.toFixed(1)} blocks), will retry later`);
            return false;
        }

        // In CREATIVE MODE: Fly to the target position
        if (bot.game.gameMode === 'creative') {
            // Calculate distance to targetPos (where bot should be, not where block is)
            const distToTargetPos = Math.sqrt(
                Math.pow(currentPos.x - targetPos.x, 2) +
                Math.pow(currentPos.y - targetPos.y, 2) +
                Math.pow(currentPos.z - targetPos.z, 2)
            );

            // If bot is more than 4 blocks away from targetPos, fly closer
            if (distToTargetPos > 4) {
                console.log(`   Flying to position: ${distToTargetPos.toFixed(1)} blocks away...`);
                try {
                    // Reduced timeout for faster failure
                    await bot.creative.flyTo(targetPos, { timeout: 2000 });
                    await this.sleep(200); // Wait for flight to complete

                    // Verify we actually moved closer
                    const newPos = bot.entity.position;
                    const newDist = Math.sqrt(
                        Math.pow(newPos.x - targetPos.x, 2) +
                        Math.pow(newPos.y - targetPos.y, 2) +
                        Math.pow(newPos.z - targetPos.z, 2)
                    );

                    if (newDist >= distToTargetPos * 0.9) {
                        console.warn(`   ⚠️ Flight didn't move bot closer (was ${distToTargetPos.toFixed(1)}, now ${newDist.toFixed(1)})`);
                    }
                } catch (err) {
                    console.warn(`   ⚠️ Flight failed: ${err.message}`);
                    console.warn(`   ⏩ Will attempt placement from current position`);
                }
            }
        }

        // In survival mode, use pathfinder (rare case)
        if (bot.game.gameMode !== 'creative' && !bot.pathfinder) {
            bot.loadPlugin(pathfinder);
        }

        if (bot.game.gameMode !== 'creative') {
            const movements = new Movements(bot);
            bot.pathfinder.setMovements(movements);
            bot.pathfinder.setGoal(new goals.GoalNear(targetPos.x, targetPos.y, targetPos.z, 1));

            await new Promise(resolve => {
                const timeout = setTimeout(resolve, 4000);
                bot.once('goal_reached', () => {
                    clearTimeout(timeout);
                    resolve();
                });
            });
        }

        await this.sleep(200);

        // CRITICAL: Verify bot is at correct distance before proceeding
        const botPosAfterMove = bot.entity.position;
        const distToTarget = Math.sqrt(
            Math.pow(botPosAfterMove.x - block.position.x, 2) +
            Math.pow(botPosAfterMove.y - block.position.y, 2) +
            Math.pow(botPosAfterMove.z - block.position.z, 2)
        );

        console.log(`   DEBUG: Bot is ${distToTarget.toFixed(2)} blocks from target`);

        // In creative mode, bot can reach further when flying
        // Allow up to 30 blocks distance
        const maxDistance = bot.game.gameMode === 'creative' ? 30 : 6;

        if (distToTarget > maxDistance) {
            console.warn(`   ⚠️ Bot too far from target (${distToTarget.toFixed(2)} blocks), skipping for now`);
            return false;
        }

        console.log(`   DEBUG: Distance OK, equipping item`);

        // ANTI-COLLISION: Check if bot's bounding box intersects with target block
        // Bot occupies 1 block: at its block position, it occupies:
        // - Feet: (bx, by, bz)
        // - Head: (bx, by+1, bz)
        const botBlockPos = new Vec3(
            Math.floor(botPosAfterMove.x),
            Math.floor(botPosAfterMove.y),
            Math.floor(botPosAfterMove.z)
        );

        const targetBlockPos = new Vec3(block.position.x, block.position.y, block.position.z);

        // Check if bot is at the target position or one block above
        const isBotAtTarget =
            (botBlockPos.x === targetBlockPos.x && botBlockPos.z === targetBlockPos.z) &&
            (botBlockPos.y === targetBlockPos.y || botBlockPos.y === targetBlockPos.y - 1);

        if (isBotAtTarget) {
            console.log(`   ⚠️ Anti-collision: Bot is at target position, moving away...`);

            // Find a safe adjacent position to move to
            const escapeDirections = [
                { x: 1, y: 0, z: 0 },   // +X
                { x: -1, y: 0, z: 0 },  // -X
                { x: 0, y: 0, z: 1 },   // +Z
                { x: 0, y: 0, z: -1 },  // -Z
                { x: 0, y: 1, z: 0 },   // +Y (up in creative)
                { x: 0, y: -1, z: 0 }   // -Y (down)
            ];

            let foundSafePos = false;
            for (const dir of escapeDirections) {
                const checkPos = new Vec3(
                    botBlockPos.x + dir.x,
                    botBlockPos.y + dir.y,
                    botBlockPos.z + dir.z
                );

                // Check if this position is not the target and is air
                const blockAtCheck = bot.blockAt(checkPos);
                if (!blockAtCheck || blockAtCheck.name === 'air') {
                    // Move to this position naturally (no teleport)
                    if (bot.game.gameMode === 'creative') {
                        // In creative, fly to safety
                        bot.creative.flyTo(checkPos, { timeout: 2000 });
                        console.log(`   ✅ Flying to safe position: (${checkPos.x}, ${checkPos.y}, ${checkPos.z})`);
                        await this.sleep(300);
                        foundSafePos = true;
                        break;
                    }
                }
            }

            if (!foundSafePos) {
                console.warn(`   ⚠️ Could not find safe position, using scaffolding...`);

                // Place temporary dirt block to stand on
                const { default: prismarineItem } = await import('prismarine-item');
                const Item = prismarineItem(bot.version);
                const dirtItem = new Item(bot.registry.itemsByName.dirt.id, 1, 0);

                // Place dirt below to elevate
                bot.creative.setInventorySlot(36, dirtItem);
                await this.sleep(100);

                // Look down and place
                const belowPos = new Vec3(botBlockPos.x, botBlockPos.y - 1, botBlockPos.z);
                const blockBelow = bot.blockAt(belowPos);

                if (blockBelow) {
                    try {
                        await bot.placeBlock(blockBelow, new Vec3(0, 1, 0), { timeout: 3000 });
                        console.log(`   ✅ Placed temporary scaffolding below`);
                        await this.sleep(200);
                    } catch (err) {
                        console.warn(`   ⚠️ Failed to place scaffolding: ${err.message}`);
                    }
                }
            }

            // Re-check position after moving
            const newBotPos = bot.entity.position;
            const newBotBlockPos = new Vec3(
                Math.floor(newBotPos.x),
                Math.floor(newBotPos.y),
                Math.floor(newBotPos.z)
            );

            const stillAtTarget =
                (newBotBlockPos.x === targetBlockPos.x && newBotBlockPos.z === targetBlockPos.z) &&
                (newBotBlockPos.y === targetBlockPos.y || newBotBlockPos.y === targetBlockPos.y - 1);

            if (stillAtTarget) {
                console.error(`   ❌ Still at target position after move attempt! Skipping block.`);
                return false;
            }
        }

        // Use optimized hotbar system to equip the block
        const slot = await this.equipBlockForPlacement(block.name);
        if (slot === null) {
            console.warn(`   ⚠️ Failed to equip ${block.name}! Skipping.`);
            return false;
        }

        // CRITICAL: Verify the bot has the CORRECT block in hotbar slot (creative mode)
        await this.sleep(150); // Wait for inventory to update

        // Check hotbar slot instead of hand (more reliable in creative mode)
        const currentSlot = bot.inventory.selectedSlot;
        const slotIndex = 36 + currentSlot;
        const slotItem = bot.inventory.slots[slotIndex];
        const slotItemName = slotItem ? slotItem.name.replace('minecraft:', '') : 'empty';

        console.log(`   🔍 Block verification:`);
        console.log(`      Expected: ${block.name}`);
        console.log(`      Slot ${currentSlot}: ${slotItemName}`);

        // In creative mode, if slot is empty but should have block, trust the slot selection
        // and try to place anyway (inventory can be slow to update in creative)
        if (slotItemName !== block.name) {
            console.warn(`   ⚠️ Slot shows '${slotItemName}' but expected '${block.name}'`);
            console.warn(`   ⚠️ This is common in creative mode - trying to place anyway...`);
        } else {
            console.log(`   ✅ Correct block in slot ${currentSlot}`);
        }

        console.log(`   DEBUG: Face vector: (${face.x}, ${face.y}, ${face.z})`);

        // Look at the EXACT center of the reference block face
        // The face center is: refBlock position + 0.5 (center of block) + face * 0.5 (to surface of face)
        const lookAtPos = new Vec3(
            refBlock.position.x + 0.5 + face.x * 0.5,
            refBlock.position.y + 0.5 + face.y * 0.5,
            refBlock.position.z + 0.5 + face.z * 0.5
        );

        console.log(`   Looking at face center of ref block at (${refBlock.position.x}, ${refBlock.position.y}, ${refBlock.position.z})`);
        console.log(`   Face direction: (${face.x}, ${face.y}, ${face.z})`);
        console.log(`   Look position: (${lookAtPos.x}, ${lookAtPos.y}, ${lookAtPos.z})`);

        console.log(`   Looking at face center: (${lookAtPos.x}, ${lookAtPos.y}, ${lookAtPos.z})`);
        await bot.lookAt(lookAtPos);
        await this.sleep(200);

        console.log(`   DEBUG: Attempting bot.placeBlock()`);

        try {
            // Use bot.placeBlock() for right-click simulation
            // Pass the reference block and the face to click on
            // Use a longer timeout for creative mode (bot might be far)
            const timeout = bot.game.gameMode === 'creative' ? 10000 : 5000;
            await bot.placeBlock(refBlock, face, { timeout });
            console.log(`   ✅ bot.placeBlock() completed successfully`);

            // CRITICAL: Verify the block was actually placed correctly
            await this.sleep(100); // Wait for block to update

            const placedBlock = bot.blockAt(new Vec3(block.position.x, block.position.y, block.position.z));

            if (!placedBlock) {
                console.error(`   ❌ No block found at target position after placement!`);
                return false;
            }

            // Check if the correct block was placed
            const placedName = placedBlock.name.replace('minecraft:', '');

            // Try different name formats
            const expectedName = block.name;
            const isCorrect = placedName === expectedName ||
                             placedName === expectedName.replace('minecraft:', '') ||
                             expectedName === placedName.replace('minecraft:', '');

            console.log(`   Verification: expected="${expectedName}", placed="${placedName}", correct=${isCorrect}`);

            if (!isCorrect) {
                console.error(`   ❌ Wrong block placed! Expected ${block.name}, got ${placedName}`);
                return false;
            }

            console.log(`   ✅ Block placed and verified: ${block.name}`);
            this.placedBlocks++;
            return true; // Indicate success
        } catch (err) {
            console.error(`   ❌ Placement failed: ${err.message}`);
            // Don't throw - just return false to skip this block
            return false;
        }
    }

    /**
     * Get which face to click on the reference block
     * Returns a Vec3 representing the face direction
     */
    getFaceToClick(targetPos, refPos) {
        // Calculate which face of the reference block to click
        // The face should be FACING TOWARD the target position
        // If target is ABOVE reference (y > ref.y), click TOP face (0, 1, 0)
        // If target is BELOW reference (y < ref.y), click BOTTOM face (0, -1, 0)
        const dx = Math.sign(targetPos.x - refPos.x);
        const dy = Math.sign(targetPos.y - refPos.y);
        const dz = Math.sign(targetPos.z - refPos.z);

        // Return face direction (points FROM reference TOWARD target)
        // This is the face we click on the reference block
        return new Vec3(dx, dy, dz);
    }

    /**
     * Check if a block has solid support (adjacent solid blocks)
     * Checks both natural terrain and blocks already placed by the bot
     * @param {Object} block - Block to check
     * @param {Set} placedPositions - Set of positions that have been placed (as strings "x,y,z")
     * @returns {boolean} - True if block has solid adjacent support
     */
    hasBlockSupport(block, placedPositions) {
        const bot = this.bot;

        // Check all 6 adjacent positions for solid blocks
        const directions = [
            { x: 0, y: -1, z: 0 }, // down (gravity support - most important)
            { x: 0, y: 1, z: 0 },  // up
            { x: 1, y: 0, z: 0 },  // east
            { x: -1, y: 0, z: 0 }, // west
            { x: 0, y: 0, z: 1 },  // south
            { x: 0, y: 0, z: -1 }  // north
        ];

        for (const dir of directions) {
            const checkPos = {
                x: block.position.x + dir.x,
                y: block.position.y + dir.y,
                z: block.position.z + dir.z
            };

            // Check if there's a naturally occurring solid block or terrain
            const blockAtPos = bot.blockAt(new Vec3(checkPos.x, checkPos.y, checkPos.z));

            if (blockAtPos && blockAtPos.name && blockAtPos.name !== 'air') {
                // Found a solid block in the world
                return true;
            }

            // Check if this position was placed by us (in memory tracking)
            const posKey = `${checkPos.x},${checkPos.y},${checkPos.z}`;
            if (placedPositions.has(posKey)) {
                // We placed a block here earlier
                return true;
            }
        }

        // No solid support found in any direction
        return false;
    }

    /**
     * Place an anchor block to support floating structures
     * Uses dirt as a temporary foundation block
     */
    async placeAnchorBlock(position) {
        const bot = this.bot;

        try {
            // Check if there's actually a block at this position already (maybe terrain)
            const existingBlock = bot.blockAt(new Vec3(position.x, position.y, position.z));
            if (existingBlock && existingBlock.name && existingBlock.name !== 'air') {
                console.log(`   ✅ Found existing block at anchor position: ${existingBlock.name}`);
                return true;
            }

            // Try to equip dirt
            const slot = await this.equipBlockForPlacement('dirt');
            if (slot === null) {
                console.warn(`   ⚠️ Could not equip dirt for anchor block`);
                return false;
            }

            // Find a reference block (check all 6 directions)
            const refBlock = this.findReferenceBlock(position);
            if (!refBlock) {
                console.warn(`   ⚠️ No reference block found for anchor placement`);
                return false;
            }

            // Calculate face
            const face = this.getFaceToClick(position, refBlock.position);

            // Look at the reference block
            const lookAtPos = new Vec3(
                refBlock.position.x + 0.5 + face.x * 0.5,
                refBlock.position.y + 0.5 + face.y * 0.5,
                refBlock.position.z + 0.5 + face.z * 0.5
            );
            await bot.lookAt(lookAtPos);
            await this.sleep(200);

            // Place the dirt block
            await bot.placeBlock(refBlock, face, { timeout: 5000 });

            // Verify
            await this.sleep(100);
            const placedBlock = bot.blockAt(new Vec3(position.x, position.y, position.z));
            if (placedBlock && placedBlock.name && placedBlock.name !== 'air') {
                console.log(`   ✅ Anchor block placed and verified: ${placedBlock.name}`);
                return true;
            } else {
                console.warn(`   ⚠️ Anchor block placement verification failed`);
                return false;
            }
        } catch (error) {
            console.error(`   ❌ Failed to place anchor block: ${error.message}`);
            return false;
        }
    }

    /**
     * Find a reference block to place against
     * Checks already placed blocks and natural terrain
     * Also checks diagonal positions for floating blocks
     */
    findReferenceBlock(targetPos) {
        const bot = this.bot;

        // Check all 6 directions for a solid block
        const directions = [
            { x: 0, y: -1, z: 0 }, // down (check ground first - most reliable)
            { x: 0, y: 1, z: 0 },  // up
            { x: 1, y: 0, z: 0 },  // east
            { x: -1, y: 0, z: 0 }, // west
            { x: 0, y: 0, z: 1 },  // south
            { x: 0, y: 0, z: -1 }  // north
        ];

        // First pass: check adjacent blocks
        for (const dir of directions) {
            const checkPos = new Vec3(
                targetPos.x + dir.x,
                targetPos.y + dir.y,
                targetPos.z + dir.z
            );

            const blockAtPos = bot.blockAt(checkPos);

            // Found a solid block (including already placed blocks)
            if (blockAtPos && blockAtPos.name && blockAtPos.name !== 'air') {
                return blockAtPos;
            }
        }

        // Second pass: check diagonal positions (2 blocks away in horizontal directions)
        const diagonalDirections = [
            { x: 2, y: 0, z: 0 },   // east 2
            { x: -2, y: 0, z: 0 },  // west 2
            { x: 0, y: 0, z: 2 },   // south 2
            { x: 0, y: 0, z: -2 },  // north 2
            { x: 1, y: 0, z: 1 },   // southeast
            { x: -1, y: 0, z: 1 },  // southwest
            { x: 1, y: 0, z: -1 },  // northeast
            { x: -1, y: 0, z: -1 }, // northwest
        ];

        for (const dir of diagonalDirections) {
            const checkPos = new Vec3(
                targetPos.x + dir.x,
                targetPos.y + dir.y,
                targetPos.z + dir.z
            );

            const blockAtPos = bot.blockAt(checkPos);

            if (blockAtPos && blockAtPos.name && blockAtPos.name !== 'air') {
                console.log(`   Found diagonal reference block at (${checkPos.x}, ${checkPos.y}, ${checkPos.z})`);
                return blockAtPos;
            }
        }

        // Third pass: check extended range (3 blocks away) for edge cases
        const extendedDirections = [
            { x: 3, y: 0, z: 0 },
            { x: -3, y: 0, z: 0 },
            { x: 0, y: 0, z: 3 },
            { x: 0, y: 0, z: -3 },
        ];

        for (const dir of extendedDirections) {
            const checkPos = new Vec3(
                targetPos.x + dir.x,
                targetPos.y + dir.y,
                targetPos.z + dir.z
            );

            const blockAtPos = bot.blockAt(checkPos);

            if (blockAtPos && blockAtPos.name && blockAtPos.name !== 'air') {
                console.log(`   Found extended reference block at (${checkPos.x}, ${checkPos.y}, ${checkPos.z})`);
                return blockAtPos;
            }
        }

        return null;
    }

    /**
     * Walk to a position like a player (using controls)
     * Keeps 2-3 blocks distance on the exterior side of the structure
     */
    async walkToPosition(targetPos) {
        const bot = this.bot;

        // Calculate exterior position (2-3 blocks away from target)
        // Prefer -X direction (west) as default exterior
        const exteriorPos = new Vec3(
            targetPos.x - 3,
            targetPos.y,
            targetPos.z
        );

        console.log(`   Moving to exterior position: (${exteriorPos.x}, ${exteriorPos.y}, ${exteriorPos.z})`);
        console.log(`   Target block at: (${targetPos.x}, ${targetPos.y}, ${targetPos.z})`);

        // Only load plugin once
        if (!bot.pathfinder) {
            bot.loadPlugin(pathfinder);
            // Wait a bit for plugin to initialize
            await this.sleep(100);
        }

        const movements = new Movements(bot);
        bot.pathfinder.setMovements(movements);

        // Use Vec3 object for GoalNear
        const goal = new goals.GoalNear(exteriorPos.x, exteriorPos.y, exteriorPos.z, 2);

        bot.pathfinder.setGoal(goal);

        // Wait for arrival (max 5 seconds)
        await new Promise(resolve => {
            const timeout = setTimeout(() => resolve(), 5000);
            bot.once('goal_reached', () => {
                clearTimeout(timeout);
                resolve();
            });
            bot.once('path_update', (r) => {
                if (r.status === 'noPath') {
                    clearTimeout(timeout);
                    resolve(); // Continue anyway
                }
            });
        });

        await this.sleep(100); // Brief pause after movement
    }

    /**
     * Get item from creative inventory using prismarine-item
     */
    async getCreativeItem(blockName) {
        const bot = this.bot;

        const item = bot.registry.itemsByName[blockName];
        if (!item) {
            throw new Error(`Block ${blockName} not found in registry!`);
        }

        // Import prismarine-item
        const { default: prismarineItem } = await import('prismarine-item');
        const Item = prismarineItem(bot.version);

        // Set the item in the currently selected hotbar slot
        const currentSlot = bot.inventory.selectedSlot;
        const slotIndex = 36 + currentSlot; // Hotbar slots are 36-44

        // Create Item using prismarine-item (correct format)
        const itemToSet = new Item(item.id, 64, 0);
        await bot.creative.setInventorySlot(slotIndex, itemToSet);
        await this.sleep(100);

        console.log(`   ✅ Set ${blockName} in hotbar slot ${currentSlot}`);
    }

    /**
     * Sleep utility
     */
    sleep(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }

    /**
     * Check if a layer needs scaffolding (too high to reach from ground)
     * Returns true if scaffolding is needed
     */
    needsScaffolding(layerY) {
        const bot = this.bot;
        const botY = bot.entity.position.y;
        const reachDistance = 5; // Max reach in Minecraft (4.5 blocks + margin)

        // In creative mode, bot can fly, so check if layer is very high
        if (bot.game.gameMode === 'creative') {
            // If flying, we can reach any height
            if (bot.creative.flying) {
                return false;
            }
            // Not flying but in creative: check if layer is too high to jump to
            return layerY > botY + reachDistance + 1;
        }

        // Survival mode: check if we need to build up
        return layerY > botY + reachDistance + 1;
    }

    /**
     * Build a scaffolding platform at the specified Y level
     * Uses dirt blocks as temporary scaffolding
     * Returns true if scaffolding was built successfully
     */
    async buildScaffoldingPlatform(targetY, layerBlocks) {
        const bot = this.bot;

        console.log(`\n🏗️ Building scaffolding platform at Y=${targetY - 1}...`);

        // Calculate the area to cover with scaffolding
        let minX = Infinity, maxX = -Infinity, minZ = Infinity, maxZ = -Infinity;
        for (const block of layerBlocks) {
            minX = Math.min(minX, block.position.x);
            maxX = Math.max(maxX, block.position.x);
            minZ = Math.min(minZ, block.position.z);
            maxZ = Math.max(maxZ, block.position.z);
        }

        // Extend the platform by 1 block in all directions for walking space
        minX -= 1;
        maxX += 1;
        minZ -= 1;
        maxZ += 1;

        console.log(`   Platform area: X[${minX}, ${maxX}], Z[${minZ}, ${maxZ}] at Y=${targetY - 1}`);
        console.log(`   This requires ${(maxX - minX + 1) * (maxZ - minZ + 1)} dirt blocks`);

        // Equip dirt block
        if (bot.game.gameMode === 'creative') {
            try {
                const { default: prismarineItem } = await import('prismarine-item');
                const Item = prismarineItem(bot.version);
                const dirtItem = new Item(bot.registry.itemsByName.dirt.id, 64, 0);
                bot.creative.setInventorySlot(36, dirtItem);
                bot.inventory.selectedSlot = 0;
                await this.sleep(100);
            } catch (err) {
                console.error(`   ❌ Failed to equip dirt: ${err.message}`);
                return false;
            }
        }

        // Build the platform row by row (avoid where blocks already exist)
        const platformY = targetY - 1;
        let placedCount = 0;

        for (let z = minZ; z <= maxZ; z++) {
            for (let x = minX; x <= maxX; x++) {
                const pos = new Vec3(x, platformY, z);
                const existingBlock = bot.blockAt(pos);

                // Skip if there's already a solid block here
                if (existingBlock && existingBlock.name !== 'air') {
                    continue;
                }

                // Find a reference block to place against
                const refBlock = this.findReferenceBlock(pos);

                if (!refBlock) {
                    console.warn(`   ⚠️ No reference for scaffolding at (${x}, ${platformY}, ${z})`);
                    continue;
                }

                try {
                    // Move closer if needed
                    const dist = Math.sqrt(
                        Math.pow(bot.entity.position.x - x, 2) +
                        Math.pow(bot.entity.position.y - platformY, 2) +
                        Math.pow(bot.entity.position.z - z, 2)
                    );

                    if (dist > 6 && bot.game.gameMode === 'creative') {
                        // Fly closer for platform building
                        bot.creative.flyTo(new Vec3(x + 0.5, platformY + 2, z + 0.5), { timeout: 2000 });
                        await this.sleep(200);
                    }

                    // Calculate face
                    const face = this.getFaceToClick(pos, refBlock.position);

                    // Look at the reference block face
                    const lookAtPos = new Vec3(
                        refBlock.position.x + 0.5 + face.x * 0.5,
                        refBlock.position.y + 0.5 + face.y * 0.5,
                        refBlock.position.z + 0.5 + face.z * 0.5
                    );
                    await bot.lookAt(lookAtPos);
                    await this.sleep(100);

                    // Place the dirt block
                    await bot.placeBlock(refBlock, face, { timeout: 3000 });

                    // Track this scaffolding block
                    this.scaffoldingBlocks.push({ x, y: platformY, z });
                    placedCount++;

                    await this.sleep(50); // Small delay between placements
                } catch (err) {
                    console.warn(`   ⚠️ Failed to place scaffolding at (${x}, ${platformY}, ${z}): ${err.message}`);
                }
            }
        }

        console.log(`   ✅ Scaffolding platform complete: ${placedCount} blocks placed`);
        this.currentScaffoldingY = platformY;
        return true;
    }

    /**
     * Remove scaffolding blocks after layer completion
     */
    async removeScaffolding() {
        const bot = this.bot;

        if (this.scaffoldingBlocks.length === 0) {
            return;
        }

        console.log(`\n🧹 Removing ${this.scaffoldingBlocks.length} scaffolding blocks...`);

        // Equip a shovel (or just use hand/fist in creative)
        if (bot.game.gameMode === 'creative') {
            // In creative, we can break blocks instantly
            for (const pos of this.scaffoldingBlocks) {
                try {
                    const blockPos = new Vec3(pos.x, pos.y, pos.z);
                    const block = bot.blockAt(blockPos);

                    if (block && block.name === 'dirt') {
                        // Move closer if needed
                        const dist = Math.sqrt(
                            Math.pow(bot.entity.position.x - pos.x, 2) +
                            Math.pow(bot.entity.position.y - pos.y, 2) +
                            Math.pow(bot.entity.position.z - pos.z, 2)
                        );

                        if (dist > 6) {
                            bot.creative.flyTo(new Vec3(pos.x + 0.5, pos.y + 2, pos.z + 0.5), { timeout: 2000 });
                            await this.sleep(200);
                        }

                        await bot.lookAt(blockPos);
                        await this.sleep(100);

                        // Break the block
                        await bot.dig(block, { timeout: 1000 });
                        await this.sleep(50);
                    }
                } catch (err) {
                    console.warn(`   ⚠️ Failed to remove scaffolding at (${pos.x}, ${pos.y}, ${pos.z}): ${err.message}`);
                }
            }
        }

        console.log(`   ✅ Scaffolding removed`);
        this.scaffoldingBlocks = [];
        this.currentScaffoldingY = null;
    }

    /**
     * Pause the build
     */
    pause() {
        if (!this.isBuilding) {
            console.warn('⚠️ No build in progress to pause');
            return;
        }
        this.isPaused = true;
        console.log('⏸ Build paused');
    }

    /**
     * Resume the build
     */
    resume() {
        if (!this.isBuilding) {
            console.warn('⚠️ No build in progress to resume');
            return;
        }
        this.isPaused = false;
        console.log('▶️ Build resumed');
    }

    /**
     * Stop the build completely
     */
    stop() {
        if (!this.isBuilding) {
            console.warn('⚠️ No build in progress to stop');
            return;
        }
        this.isStopped = true;
        this.isPaused = false; // Unpause so we can exit gracefully
        console.log('⏹ Build stopped');
    }

    /**
     * Set build speed multiplier
     * @param {number} speed - Speed multiplier (0.5x to 3.0x)
     */
    setSpeed(speed) {
        if (speed < 0.5 || speed > 3.0) {
            console.warn(`⚠️ Invalid speed: ${speed}. Must be between 0.5x and 3.0x`);
            return;
        }
        this.speedMultiplier = speed;
        console.log(`⚡ Build speed set to ${speed}x`);
    }

    /**
     * Sleep with speed multiplier applied
     * Lower sleep duration for higher speeds
     */
    async sleep(ms) {
        const adjustedMs = ms / this.speedMultiplier;
        return new Promise(resolve => setTimeout(resolve, adjustedMs));
    }

    /**
     * Get build progress
     * @returns {Object} Progress information with placed and total blocks
     */
    getProgress() {
        return {
            placed: this.placedBlocks || 0,
            total: this.totalBlocks || 0,
            percentage: this.totalBlocks > 0 ? (this.placedBlocks / this.totalBlocks) : 0
        };
    }
}
