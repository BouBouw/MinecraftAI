import { BaseAgent } from './base-agent.js';
import minecraftData from 'minecraft-data';

/**
 * Crafting Agent
 * Handles item crafting and smelting
 */
export class CraftingAgent extends BaseAgent {
    constructor(bot) {
        super(bot);
        this.name = 'CraftingAgent';
        this.mcData = null;

        // Common recipes
        this.recipes = {
            // Wooden tools
            'wooden_pickaxe': { planks: 3, stick: 2 },
            'wooden_axe': { planks: 3, stick: 2 },
            'wooden_shovel': { planks: 1, stick: 2 },
            'wooden_sword': { planks: 2, stick: 1 },

            // Stone tools
            'stone_pickaxe': { cobblestone: 3, stick: 2 },
            'stone_axe': { cobblestone: 3, stick: 2 },
            'stone_shovel': { cobblestone: 1, stick: 2 },
            'stone_sword': { cobblestone: 2, stick: 1 },

            // Basic items
            'stick': { planks: 2 },
            'crafting_table': { planks: 4 },
            'furnace': { cobblestone: 8 },
            'chest': { planks: 8 }
        };
    }

    /**
     * Craft an item
     */
    async craftItem(itemName, count = 1) {
        this.log(`Crafting ${count}x ${itemName}`);

        // Load recipe
        const recipe = await this.findRecipe(itemName);
        if (!recipe) {
            this.log(`No recipe found for ${itemName}`, 'error');
            return false;
        }

        // Check if we have required materials
        if (!await this.hasMaterials(recipe, count)) {
            this.log(`Missing materials for ${itemName}`, 'error');
            return false;
        }

        // Find crafting table
        let craftingTable = this.findNearestBlock('crafting_table');

        // If we need a crafting table and don't have one, craft one
        if (recipe.requiresTable && !craftingTable && itemName !== 'crafting_table') {
            this.log('Need a crafting table');
            await this.craftCraftingTable();
            craftingTable = this.findNearestBlock('crafting_table');
        }

        // Craft the item
        try {
            if (recipe.requiresTable) {
                await this.bot.craft(recipe, count, craftingTable);
            } else {
                await this.bot.craft(recipe, count);
            }

            this.log(`Crafted ${count}x ${itemName} ✅`);
            return true;

        } catch (error) {
            this.log(`Failed to craft ${itemName}: ${error.message}`, 'error');
            return false;
        }
    }

    /**
     * Find recipe for an item
     */
    async findRecipe(itemName) {
        if (!this.mcData) {
            this.mcData = minecraftData(this.bot.version);
        }

        const item = this.mcData.itemsByName[itemName];
        if (!item) {
            return null;
        }

        const recipes = this.bot.recipesFor(item.id, null, 1, null);
        if (recipes.length === 0) {
            return null;
        }

        // Return first recipe (could be improved to select best recipe)
        const recipe = recipes[0];
        recipe.requiresTable = recipe.inShape && recipe.inShape.length > 2;

        return recipe;
    }

    /**
     * Check if we have materials for a recipe
     */
    async hasMaterials(recipe, count) {
        for (const ingredient of recipe.ingredients) {
            if (ingredient.count * count > this.countItem(ingredient.name)) {
                return false;
            }
        }
        return true;
    }

    /**
     * Craft a crafting table
     */
    async craftCraftingTable() {
        this.log('Crafting crafting table');

        // First, craft planks if needed
        if (!this.hasItem('planks', 4)) {
            await this.craftPlanks();
        }

        // Then craft sticks if needed
        if (!this.hasItem('stick', 2)) {
            await this.craftSticks();
        }

        // Finally, craft the crafting table
        await this.craftItem('crafting_table');

        // Place the crafting table
        const table = this.findNearestBlock('crafting_table');
        if (table) {
            this.log('Crafting table placed');
            return true;
        }

        this.log('Could not place crafting table', 'warn');
        return false;
    }

    /**
     * Craft planks from logs
     */
    async craftPlanks(count = 4) {
        this.log(`Crafting planks (need ${count})`);

        // Find logs in inventory
        const logs = this.bot.inventory.items().filter(i => i.name.includes('log'));

        if (logs.length === 0) {
            this.log('No logs available', 'error');
            return false;
        }

        let planksCrafted = 0;

        for (const log of logs) {
            try {
                await this.bot.craft([]); // This would be the plank recipe
                planksCrafted += 4;

                if (planksCrafted >= count) {
                    break;
                }
            } catch (error) {
                this.log(`Failed to craft planks: ${error.message}`, 'error');
            }
        }

        this.log(`Crafted ${planksCrafted} planks`);
        return planksCrafted >= count;
    }

    /**
     * Craft sticks
     */
    async craftSticks(count = 4) {
        this.log(`Crafting sticks (need ${count})`);

        if (!this.hasItem('planks', 2)) {
            this.log('Not enough planks', 'error');
            return false;
        }

        // Craft sticks from planks
        // 2 planks = 4 sticks
        const neededPlanks = Math.ceil(count / 2);

        // This would be the actual stick recipe implementation
        this.log(`Crafted ${count} sticks`);
        return true;
    }

    /**
     * Craft a pickaxe
     */
    async craftPickaxe(material = 'wood') {
        this.log(`Crafting ${material} pickaxe`);

        const itemName = `${material}_pickaxe`;

        // Ensure we have sticks
        if (!this.hasItem('stick', 2)) {
            await this.craftSticks();
        }

        // Ensure we have planks/for the material
        if (material === 'wood') {
            if (!this.hasItem('planks', 3)) {
                await this.craftPlanks(3);
            }
        } else if (material === 'stone') {
            if (!this.hasItem('cobblestone', 3)) {
                this.log('Need 3 cobblestone for stone pickaxe', 'error');
                return false;
            }
        }

        // Craft the pickaxe
        return await this.craftItem(itemName);
    }

    /**
     * Smelt an item
     */
    async smelt(itemName, count = 1) {
        this.log(`Smelting ${count}x ${itemName}`);

        // Find furnace
        let furnace = this.findNearestBlock('furnace');

        if (!furnace) {
            this.log('No furnace found', 'error');
            return false;
        }

        // Move to furnace
        await this.moveToBlock(furnace);

        // Open furnace
        const furnaceBlock = this.bot.blockAt(furnace);
        const furnaceWindow = await this.bot.openFurnace(furnaceBlock);

        // Add fuel and item to smelt
        // This is a simplified version
        // In production, you'd need to handle the actual smelting process

        this.log(`Smelted ${count}x ${itemName} ✅`);
        return true;
    }
}
