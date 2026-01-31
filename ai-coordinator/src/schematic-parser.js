/**
 * Parser for Minecraft Schematic data
 * Extracts block information and creates optimized build plans
 */
export class SchematicParser {
    constructor() {
        this.blockPriority = this.initBlockPriority();
    }

    /**
     * Initialize block priority for building order
     * Lower priority = build first
     */
    initBlockPriority() {
        return {
            // Foundations first
            'stone': 1,
            'cobblestone': 1,
            'dirt': 2,
            'grass_block': 2,

            // Then main structure
            'oak_planks': 10,
            'spruce_planks': 10,
            'birch_planks': 10,
            'bricks': 10,
            'concrete': 10,

            // Details and decoration
            'glass': 50,
            'oak_fence': 60,
            'torch': 70,
            'redstone': 80,

            // Everything else
            'default': 20
        };
    }

    /**
     * Parse schematic data and extract block information
     */
    parse(schematic) {
        const blocks = [];
        const materials = {};

        // Process materials list
        for (const [blockId, count] of Object.entries(schematic.materials)) {
            materials[blockId] = count;
        }

        // Calculate layers (from bottom to top)
        const layers = schematic.dimensions.height;
        const blocksPerLayer = schematic.dimensions.width * schematic.dimensions.length;

        console.log(`📊 Parsing schematic: ${schematic.name}`);
        console.log(`   Total blocks: ${Object.values(materials).reduce((a, b) => a + b, 0)}`);
        console.log(`   Layers: ${layers}`);
        console.log(`   Different materials: ${Object.keys(materials).length}`);

        return {
            id: schematic.id,
            name: schematic.name,
            dimensions: schematic.dimensions,
            position: schematic.position,
            materials: materials,
            totalBlocks: Object.values(materials).reduce((a, b) => a + b, 0),
            layers: layers
        };
    }

    /**
     * Get build priority for a block type
     */
    getPriority(blockType) {
        // Try exact match first
        if (this.blockPriority[blockType] !== undefined) {
            return this.blockPriority[blockType];
        }

        // Try partial match
        for (const [key, priority] of Object.entries(this.blockPriority)) {
            if (blockType.includes(key)) {
                return priority;
            }
        }

        return this.blockPriority['default'];
    }

    /**
     * Calculate total resources needed
     */
    calculateResources(materials) {
        const resources = {};

        for (const [blockId, count] of Object.entries(materials)) {
            // Add base block requirement
            resources[blockId] = (resources[blockId] || 0) + count;

            // Calculate tool requirements
            if (blockId.includes('wood') || blockId.includes('log')) {
                resources['axe'] = 1;
            } else if (blockId.includes('stone') || blockId.includes('ore')) {
                resources['pickaxe'] = 1;
            }
        }

        return resources;
    }
}
