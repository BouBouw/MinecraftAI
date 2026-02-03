/**
 * PERCEPTEUR - Transforme les données Minecraft en texte pour le LLM
 *
 * Ce module observe l'état du bot et génère un rapport textuel
 * que le LLM peut comprendre.
 */

class MinecraftPercepteur {
    constructor(bot) {
        this.bot = bot;
    }

    /**
     * Génère un rapport complet de l'état actuel
     * @returns {string} Rapport textuel pour le LLM
     */
    genererRapport() {
        const sections = [];

        // 1. Position et orientation
        sections.push(this._formatPosition());

        // 2. Santé et survie
        sections.push(this._formatSante());

        // 3. Inventaire
        sections.push(this._formatInventaire());

        // 4. Environnement proche
        sections.push(this._formatEnvironnement());

        // 5. Entités nearby
        sections.push(this._formatEntites());

        return sections.join('\n');
    }

    /**
     * Formate la position du bot
     */
    _formatPosition() {
        const pos = this.bot.entity.position;
        return `📍 POSITION: [${Math.floor(pos.x)}, ${Math.floor(pos.y)}, ${Math.floor(pos.z)}]
   Orientation: ${this._getCardinalDirection()}`;
    }

    /**
     * Formate la santé et faim
     */
    _formatSante() {
        const health = this.bot.health;
        const food = this.bot.food;
        const saturation = this.bot.saturation;

        let status = '❤️ SANTÉ: ';
        if (health > 15) status += 'Bonne';
        else if (health > 8) status += 'Moyenne';
        else status += 'CRITIQUE';

        status += ` (${health}/20)

🍗 FAIM: ${food}/20`;
        if (food < 6) status += ' [URGENT - MANGER]';
        else if (food < 10) status += ' [BAS]';

        return status;
    }

    /**
     * Formate l'inventaire
     */
    _formatInventaire() {
        const items = this.bot.inventory.items();
        const counts = {};

        // Compter les items par type
        items.forEach(item => {
            const name = item.name.replace('minecraft:', '');
            counts[name] = (counts[name] || 0) + item.count;
        });

        if (Object.keys(counts).length === 0) {
            return '🎒 INVENTAIRE: Vide';
        }

        let inv = '🎒 INVENTAIRE:\n';
        for (const [item, count] of Object.entries(counts)) {
            inv += `   - ${item}: x${count}\n`;
        }

        return inv.trim();
    }

    /**
     * Formate l'environnement visible (blocs proches)
     */
    _formatEnvironnement() {
        const pos = this.bot.entity.position;
        const radius = 5;

        const blocks = {};
        const blockTypes = ['oak_log', 'stone', 'coal_ore', 'iron_ore', 'diamond_ore',
                           'crafting_table', 'furnace', 'chest', 'cobblestone', 'dirt'];

        // Scanner les blocs proches
        for (let x = -radius; x <= radius; x++) {
            for (let y = -2; y <= 2; y++) {
                for (let z = -radius; z <= radius; z++) {
                    const block = this.bot.blockAt(pos.offset(x, y, z));
                    if (block && block.name !== 'air' && block.name !== 'cave_air') {
                        const name = block.name.replace('minecraft:', '');
                        if (blockTypes.includes(name)) {
                            blocks[name] = (blocks[name] || 0) + 1;
                        }
                    }
                }
            }
        }

        if (Object.keys(blocks).length === 0) {
            return '👁️ ENVIRONNEMENT: Zone dégagée';
        }

        let env = '👁️ BLOCS VISIBLES (rayon 5):\n';
        for (const [block, count] of Object.entries(blocks)) {
            env += `   - ${block}: x${count}\n`;
        }

        return env.trim();
    }

    /**
     * Formate les entités proches (mobs, animaux)
     */
    _formatEntites() {
        const entities = Object.values(this.bot.entities)
            .filter(e => e.position.distanceTo(this.bot.entity.position) < 16);

        if (entities.length === 0) {
            return '🐾 ENTITÉS: Aucune';
        }

        const byType = {};
        entities.forEach(ent => {
            const name = ent.name || ent.displayName || 'unknown';
            byType[name] = (byType[name] || 0) + 1;
        });

        let ents = '🐾 ENTITÉS PROCHES (16 blocs):\n';
        for (const [name, count] of Object.entries(byType)) {
            const hostile = this._isHostile(name);
            const emoji = hostile ? '⚔️' : '🐄';
            ents += `   ${emoji} ${name}: x${count}\n`;
        }

        return ents.trim();
    }

    /**
     * Obtient la direction cardinale
     */
    _getCardinalDirection() {
        const yaw = this.bot.entity.yaw;
        const deg = ((yaw * 180) / Math.PI) % 360;

        if (deg >= 315 || deg < 45) return 'Sud';
        if (deg >= 45 && deg < 135) return 'Ouest';
        if (deg >= 135 && deg < 225) return 'Nord';
        return 'Est';
    }

    /**
     * Vérifie si une entité est hostile
     */
    _isHostile(name) {
        const hostile = ['zombie', 'skeleton', 'spider', 'creeper', 'witch'];
        return hostile.some(h => name.toLowerCase().includes(h));
    }
}

module.exports = MinecraftPercepteur;
