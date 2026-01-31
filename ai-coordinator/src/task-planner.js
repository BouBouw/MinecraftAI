/**
 * Task planner for AI building operations
 * Breaks down schematic construction into manageable tasks
 */
export class TaskPlanner {
    constructor() {
        this.taskTypes = {
            GATHER_RESOURCES: 'gather_resources',
            CRAFT_ITEMS: 'craft_items',
            MOVE_TO_SITE: 'move_to_site',
            BUILD_LAYER: 'build_layer',
            PLACE_BLOCK: 'place_block'
        };
    }

    /**
     * Plan the building tasks for a schematic
     */
    planBuild(schematic) {
        const tasks = [];

        console.log('📋 Planning build tasks...');

        // Task 1: Gather resources
        tasks.push({
            id: 1,
            type: this.taskTypes.GATHER_RESOURCES,
            priority: 1,
            description: 'Gather required materials',
            materials: schematic.materials,
            estimatedTime: this.estimateGatherTime(schematic.materials)
        });

        // Task 2: Craft necessary items
        const craftTasks = this.planCrafting(schematic.materials);
        tasks.push(...craftTasks);

        // Task 3: Move to build site
        tasks.push({
            id: tasks.length + 1,
            type: this.taskTypes.MOVE_TO_SITE,
            priority: 2,
            description: 'Move to build location',
            position: schematic.position,
            estimatedTime: 30 // seconds
        });

        // Task 4-n: Build layer by layer
        const buildTasks = this.planLayers(schematic);
        tasks.push(...buildTasks);

        // Final task: Cleanup
        tasks.push({
            id: tasks.length + 1,
            type: 'cleanup',
            priority: 100,
            description: 'Clean up and finalize',
            estimatedTime: 60
        });

        console.log(`✅ Generated ${tasks.length} tasks`);
        return tasks;
    }

    /**
     * Plan crafting tasks based on materials
     */
    planCrafting(materials) {
        const tasks = [];

        // Check if we need to craft tools
        const needsTools = this.checkToolRequirements(materials);

        if (needsTools.pickaxe) {
            tasks.push({
                type: this.taskTypes.CRAFT_ITEMS,
                priority: 1,
                item: 'wooden_pickaxe',
                description: 'Craft wooden pickaxe',
                materials: ['planks:3', 'stick:2']
            });
        }

        if (needsTools.axe) {
            tasks.push({
                type: this.taskTypes.CRAFT_ITEMS,
                priority: 1,
                item: 'wooden_axe',
                description: 'Craft wooden axe',
                materials: ['planks:3', 'stick:2']
            });
        }

        return tasks;
    }

    /**
     * Plan layer-by-layer construction
     */
    planLayers(schematic) {
        const tasks = [];
        const layers = schematic.dimensions.height;

        for (let layer = 0; layer < layers; layer++) {
            tasks.push({
                id: tasks.length + 1,
                type: this.taskTypes.BUILD_LAYER,
                priority: 10 + layer,
                layer: layer,
                description: `Build layer ${layer + 1}/${layers}`,
                estimatedBlocks: Math.floor(schematic.dimensions.width * schematic.dimensions.length),
                estimatedTime: this.estimateLayerTime(
                    schematic.dimensions.width,
                    schematic.dimensions.length
                )
            });
        }

        return tasks;
    }

    /**
     * Check if tools are needed
     */
    checkToolRequirements(materials) {
        const needs = {
            pickaxe: false,
            axe: false
        };

        for (const blockId of Object.keys(materials)) {
            if (blockId.includes('stone') || blockId.includes('ore') || blockId.includes('coal')) {
                needs.pickaxe = true;
            }
            if (blockId.includes('wood') || blockId.includes('log') || blockId.includes('plank')) {
                needs.axe = true;
            }
        }

        return needs;
    }

    /**
     * Estimate time to gather resources
     */
    estimateGatherTime(materials) {
        // Very rough estimate in seconds
        const totalBlocks = Object.values(materials).reduce((a, b) => a + b, 0);
        return Math.ceil(totalBlocks * 2); // 2 seconds per block average
    }

    /**
     * Estimate time to build a layer
     */
    estimateLayerTime(width, length) {
        const blocks = width * length;
        return Math.ceil(blocks * 1.5); // 1.5 seconds per block
    }
}
