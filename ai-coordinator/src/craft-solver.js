/**
 * Recursive Craft Solver
 * Analyzes required materials and creates a dependency tree for crafting
 * Handles resource gathering and crafting operations
 */
export class CraftSolver {
    constructor(bot, survivalManager) {
        this.bot = bot;
        this.survivalManager = survivalManager;

        // Crafting recipes database (simplified Minecraft recipes)
        this.recipes = this.initializeRecipes();

        // Required materials tracker
        this.requiredMaterials = new Map(); // block name -> count needed
        this.craftingQueue = []; // Items to craft
    }

    /**
     * Initialize crafting recipes database
     */
    initializeRecipes() {
        return {
            // Wooden items
            'planks': { input: [['log', 1]], outputCount: 4, table: false },
            'stick': { input: [['planks', 2]], outputCount: 4, table: false },
            'crafting_table': { input: [['planks', 4]], outputCount: 1, table: false },

            // Stone tools
            'stone_pickaxe': {
                input: [['cobblestone', 3], ['stick', 2]],
                outputCount: 1,
                table: true
            },
            'stone_axe': {
                input: [['cobblestone', 3], ['stick', 2]],
                outputCount: 1,
                table: true
            },
            'stone_shovel': {
                input: [['cobblestone', 1], ['stick', 2]],
                outputCount: 1,
                table: true
            },
            'stone_sword': {
                input: [['cobblestone', 2], ['stick', 1]],
                outputCount: 1,
                table: true
            },

            // Iron tools
            'iron_pickaxe': {
                input: [['iron_ingot', 3], ['stick', 2]],
                outputCount: 1,
                table: true
            },
            'iron_axe': {
                input: [['iron_ingot', 3], ['stick', 2]],
                outputCount: 1,
                table: true
            },

            // Smelting recipes
            'iron_ingot': {
                input: [['iron_ore', 1]],
                outputCount: 1,
                smelt: true,
                cookTime: 10000 // 10 seconds
            },
            'gold_ingot': {
                input: [['gold_ore', 1]],
                outputCount: 1,
                smelt: true,
                cookTime: 10000
            },

            // Stone/Cobble variants
            'cobblestone': {
                input: [['stone', 1]],
                outputCount: 1,
                action: 'mine' // Special action needed
            },
            'stone': {
                input: [['cobblestone', 1]],
                outputCount: 1,
                smelt: true,
                cookTime: 10000
            },

            // Glass
            'glass': {
                input: [['sand', 1]],
                outputCount: 1,
                smelt: true,
                cookTime: 10000
            },

            // Stairs and slabs (examples)
            'stone_stairs': {
                input: [['stone', 6]],
                outputCount: 4,
                table: true
            },
            'oak_stairs': {
                input: [['planks', 6]],
                outputCount: 4,
                table: true
            },
            'stone_slab': {
                input: [['stone', 3]],
                outputCount: 6,
                table: true
            },

            // Storage
            'chest': {
                input: [['planks', 8]],
                outputCount: 1,
                table: true
            },
            'furnace': {
                input: [['cobblestone', 8]],
                outputCount: 1,
                table: true
            }
        };
    }

    /**
     * Analyze schematic blocks and create material requirements
     */
    analyzeRequirements(blocks) {
        console.log(`\n📊 ANALYZING MATERIAL REQUIREMENTS...`);

        // Count required blocks
        const requirements = new Map();
        for (const block of blocks) {
            const name = block.name;
            requirements.set(name, (requirements.get(name) || 0) + 1);
        }

        console.log(`   Required materials:`);
        for (const [name, count] of requirements) {
            console.log(`     - ${name}: ${count}`);
        }

        this.requiredMaterials = requirements;
        return requirements;
    }

    /**
     * Calculate what we need to craft/gather
     * Returns a craft plan with recursive dependencies
     */
    async createCraftPlan() {
        console.log(`\n📝 CREATING CRAFT PLAN...`);

        const plan = [];
        const inventory = this.bot.inventory.items();

        // Count what we already have
        const available = new Map();
        for (const item of inventory) {
            available.set(item.name, (available.get(item.name) || 0) + item.count);
        }

        // Include chest contents
        // TODO: Add chest checking once chest access is implemented

        console.log(`   Available materials in inventory:`);
        for (const [name, count] of available) {
            console.log(`     - ${name}: ${count}`);
        }

        // Calculate what's missing
        const missing = new Map();
        for (const [name, count] of this.requiredMaterials) {
            const have = available.get(name) || 0;
            if (have < count) {
                missing.set(name, count - have);
            }
        }

        if (missing.size === 0) {
            console.log(`   ✅ All materials available!`);
            return [];
        }

        console.log(`   Missing materials:`);
        for (const [name, count] of missing) {
            console.log(`     - ${name}: ${count}`);
        }

        // Recursively solve what we need to craft
        for (const [name, count] of missing) {
            const craftSteps = await this.solveCrafting(name, count, available);
            plan.push(...craftSteps);
        }

        console.log(`\n   Craft plan created with ${plan.length} steps`);
        return plan;
    }

    /**
     * Recursively solve how to craft an item
     * Returns array of craft steps
     */
    async solveCrafting(itemName, count, available) {
        const steps = [];

        // Check if we can craft this item
        const recipe = this.recipes[itemName];
        if (!recipe) {
            // No recipe - need to gather/mined this
            console.log(`   🔸 No recipe for ${itemName} - need to gather ${count}`);
            steps.push({
                action: 'gather',
                item: itemName,
                count: count,
                priority: 1
            });
            return steps;
        }

        // Special case: mining action
        if (recipe.action === 'mine') {
            steps.push({
                action: 'mine',
                item: itemName,
                count: count,
                tool: this.getBestToolForBlock(itemName)
            });
            return steps;
        }

        // Calculate how many crafting operations needed
        const craftOps = Math.ceil(count / recipe.outputCount);
        console.log(`   🔸 Crafting ${itemName}: need ${count}, recipe produces ${recipe.outputCount}, need ${craftOps} operations`);

        // Check if we need a crafting table
        if (recipe.table) {
            const hasTable = available.get('crafting_table') > 0 || this.survivalManager?.baseCraftingTable;
            if (!hasTable) {
                console.log(`   ⚠️ Need crafting table first!`);
                const tableSteps = await this.solveCrafting('crafting_table', 1, available);
                steps.push(...tableSteps);
            }
        }

        // Calculate required inputs
        for (const [inputName, inputCount] of recipe.input) {
            const totalNeeded = inputCount * craftOps;
            const have = available.get(inputName) || 0;

            if (have < totalNeeded) {
                // Need to craft/gather the input first
                const needed = totalNeeded - have;
                console.log(`     Missing ${inputName}: need ${totalNeeded}, have ${have}`);

                const inputSteps = await this.solveCrafting(inputName, needed, available);
                steps.push(...inputSteps);
            }

            // Update available (we'll have these after crafting)
            available.set(inputName, (available.get(inputName) || 0) + totalNeeded);
        }

        // Add the actual crafting step
        steps.push({
            action: recipe.smelt ? 'smelt' : 'craft',
            item: itemName,
            count: count,
            recipe: recipe,
            operations: craftOps,
            table: recipe.table,
            cookTime: recipe.cookTime || 0
        });

        // Update available with output
        available.set(itemName, (available.get(itemName) || 0) + count * recipe.outputCount);

        return steps;
    }

    /**
     * Get the best tool for mining a block
     */
    getBestToolForBlock(blockName) {
        const inventory = this.bot.inventory.items();

        // Priority: diamond > iron > stone > wooden
        const toolPriority = ['diamond_pickaxe', 'iron_pickaxe', 'stone_pickaxe', 'wooden_pickaxe'];

        for (const toolName of toolPriority) {
            const hasTool = inventory.some(i => i.name === toolName);
            if (hasTool) {
                return toolName;
            }
        }

        return null; // No tool available
    }

    /**
     * Execute a craft plan step by step
     */
    async executeCraftPlan(plan) {
        console.log(`\n🔨 EXECUTING CRAFT PLAN (${plan.length} steps)...`);

        for (let i = 0; i < plan.length; i++) {
            const step = plan[i];
            console.log(`\n   [${i + 1}/${plan.length}] ${step.action.toUpperCase()}: ${step.item} x${step.count}`);

            try {
                switch (step.action) {
                    case 'craft':
                        await this.craftItem(step);
                        break;
                    case 'smelt':
                        await this.smeltItem(step);
                        break;
                    case 'mine':
                        await this.mineBlock(step);
                        break;
                    case 'gather':
                        await this.gatherResource(step);
                        break;
                }

                console.log(`   ✅ Step completed`);
            } catch (err) {
                console.error(`   ❌ Step failed: ${err.message}`);
                throw err;
            }
        }

        console.log(`\n✅ CRAFT PLAN COMPLETED!`);
    }

    /**
     * Craft an item at crafting table
     */
    async craftItem(step) {
        const bot = this.bot;

        // Find crafting table
        const tablePos = this.survivalManager?.baseCraftingTable;
        if (!tablePos && step.table) {
            throw new Error('No crafting table available!');
        }

        // Move to crafting table
        if (tablePos) {
            await bot.pathfinder.goto(new (require('mineflayer-pathfinder').goals.GoalNear)(tablePos.x, tablePos.y, tablePos.z, 2));
        }

        // Get recipe from bot's recipe book
        const recipe = bot.recipesFor(step.item, null, null, tablePos?.block)[0];
        if (!recipe) {
            throw new Error(`No recipe found for ${step.item}`);
        }

        // Craft the item
        await bot.craft(recipe, step.operations, tablePos?.block);
        console.log(`     Crafted ${step.item} x${step.count}`);
    }

    /**
     * Smelt an item in furnace
     */
    async smeltItem(step) {
        const bot = this.bot;

        // Find furnace
        const furnacePos = this.survivalManager?.baseFurnaces?.[0];
        if (!furnacePos) {
            throw new Error('No furnace available!');
        }

        // Move to furnace
        await bot.pathfinder.goto(new (require('mineflayer-pathfinder').goals.GoalNear)(furnacePos.x, furnacePos.y, furnacePos.z, 2));

        const furnaceBlock = bot.blockAt(new (require('vec3'))(furnacePos.x, furnacePos.y, furnacePos.z));
        const furnace = await bot.openFurnace(furnaceBlock);

        // Put input item
        const inputItem = bot.inventory.items().find(i => i.name === step.recipe.input[0][0]);
        if (!inputItem) {
            throw new Error(`Missing input: ${step.recipe.input[0][0]}`);
        }

        await furnace.putInput(inputItem.type, null, step.operations);

        // Wait for smelting
        console.log(`     Smelting ${step.item} x${step.count} (${step.cookTime}ms)...`);
        await this.sleep(step.cookTime);

        // Take output
        await furnace.takeOutput();

        console.log(`     Smelted ${step.item} x${step.count}`);
        furnace.close();
    }

    /**
     * Mine blocks
     */
    async mineBlock(step) {
        // TODO: Implement mining logic
        console.log(`     ⚠️ Mining not yet implemented for ${step.item} x${step.count}`);
    }

    /**
     * Gather resources (find in world)
     */
    async gatherResource(step) {
        // TODO: Implement gathering logic
        console.log(`     ⚠️ Gathering not yet implemented for ${step.item} x${step.count}`);
    }

    /**
     * Sleep utility
     */
    sleep(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }
}
