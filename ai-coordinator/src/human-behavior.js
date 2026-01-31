/**
 * Human-Like Behavior Manager
 * Adds realistic pauses, smooth rotations, and mob defense to the bot
 */
export class HumanBehavior {
    constructor(bot, survivalManager) {
        this.bot = bot;
        this.survivalManager = survivalManager;

        // Behavior settings
        this.pauseChance = 0.1; // 10% chance to pause after placing a block
        this.pauseDuration = 1000; // 1 second
        this.rotationSpeed = 0.1; // Radians per tick for smooth rotation

        // Mob defense
        this.hostileMobs = [
            'zombie', 'skeleton', 'spider', 'creeper', 'enderman',
            'witch', 'slime', 'phantom', 'drowned', 'husk', 'stray'
        ];
        this.isDefending = false;
        this.buildingPaused = false;

        // Initialize mob defense
        this.initializeMobDefense();
    }

    /**
     * Initialize mob defense listeners
     */
    initializeMobDefense() {
        // Listen for entity spawns
        this.bot.on('entitySpawn', (entity) => {
            if (this.isHostileMob(entity)) {
                console.log(`⚠️ Hostile mob detected: ${entity.name || entity.displayName}`);
                this.handleHostileMob(entity);
            }
        });

        // Listen for player being hurt
        this.bot.on('entityHurt', (entity) => {
            if (entity === this.bot.entity) {
                console.log(`🛡️ Bot is under attack!`);
                this.handleAttack();
            }
        });

        // Listen for health changes
        this.bot.on('health', () => {
            if (this.bot.health < 10) {
                console.log(`❤️ Low health: ${this.bot.health}/20`);
                this.handleLowHealth();
            }
        });
    }

    /**
     * Check if an entity is a hostile mob
     */
    isHostileMob(entity) {
        if (!entity || !entity.name) return false;

        const mobName = entity.name.toLowerCase();
        return this.hostileMobs.some(mob => mobName.includes(mob));
    }

    /**
     * Handle detected hostile mob
     */
    async handleHostileMob(mob) {
        if (this.isDefending) return;

        const dist = this.bot.entity.position.distanceTo(mob.position);

        if (dist < 16) {
            console.log(`🛡️ Hostile mob within ${dist.toFixed(1)} blocks, engaging defense...`);
            await this.engageDefense(mob);
        }
    }

    /**
     * Handle being attacked
     */
    async handleAttack() {
        if (this.isDefending) return;

        this.buildingPaused = true;
        console.log(`⏸️ Construction paused due to attack`);

        // Find nearest hostile mob
        const nearestMob = this.findNearestHostileMob();

        if (nearestMob) {
            await this.engageDefense(nearestMob);
        } else {
            // Flee to base if no mob found but we're being hurt
            await this.fleeToBase();
        }

        this.buildingPaused = false;
        console.log(`▶️ Construction resumed`);
    }

    /**
     * Handle low health situation
     */
    async handleLowHealth() {
        console.log(`🏃 Fleeing to base due to low health...`);
        await this.fleeToBase();
        console.log(`   Safe at base. Waiting to heal...`);

        // Wait for health to regenerate
        while (this.bot.health < 15) {
            await this.sleep(1000);
        }

        console.log(`   ✅ Health restored: ${this.bot.health}/20`);
    }

    /**
     * Find nearest hostile mob
     */
    findNearestHostileMob() {
        let nearest = null;
        let nearestDist = Infinity;

        for (const entity of Object.values(this.bot.entities)) {
            if (this.isHostileMob(entity)) {
                const dist = this.bot.entity.position.distanceTo(entity.position);
                if (dist < nearestDist) {
                    nearestDist = dist;
                    nearest = entity;
                }
            }
        }

        return nearest;
    }

    /**
     * Engage in combat/defense against a mob
     */
    async engageDefense(mob) {
        this.isDefending = true;

        const dist = this.bot.entity.position.distanceTo(mob.position);

        // Decide whether to fight or flee based on health
        if (this.bot.health < 6 || dist < 3) {
            // Low health or mob too close - flee
            console.log(`   Fleeing from ${mob.name || 'mob'}...`);
            await this.fleeToBase();
        } else {
            // Fight back
            console.log(`   Fighting ${mob.name || 'mob'}...`);
            await this.fightMob(mob);
        }

        this.isDefending = false;
    }

    /**
     * Fight a hostile mob
     */
    async fightMob(mob) {
        const weapon = this.getBestWeapon();

        if (weapon) {
            await this.bot.equip(weapon, 'hand');
        }

        // Move within attack range
        const attackRange = 3;

        try {
            // Attack the mob repeatedly
            let attempts = 0;
            const maxAttempts = 10;

            while (attempts < maxAttempts && mob.isValid) {
                const dist = this.bot.entity.position.distanceTo(mob.position);

                if (dist > attackRange) {
                    // Move closer
                    await this.bot.pathfinder.goto(
                        new (require('mineflayer-pathfinder').goals.GoalNear)(
                            mob.position.x,
                            mob.position.y,
                            mob.position.z,
                            1
                        )
                    );
                }

                // Attack
                await this.bot.attack(mob);
                console.log(`   ⚔️ Attacked ${mob.name || 'mob'}!`);
                await this.sleep(500);

                attempts++;

                // Check if mob is dead
                if (!mob.isValid || mob.health <= 0) {
                    console.log(`   ✅ Defeated ${mob.name || 'mob'}!`);
                    break;
                }
            }
        } catch (err) {
            console.warn(`   ⚠️ Combat error: ${err.message}`);
        }
    }

    /**
     * Get best weapon from inventory
     */
    getBestWeapon() {
        const items = this.bot.inventory.items();
        const weapons = items.filter(i =>
            i.name.includes('sword') ||
            i.name.includes('axe')
        );

        // Priority: diamond > iron > stone > wooden
        const priority = ['diamond', 'iron', 'stone', 'wooden'];

        for (const material of priority) {
            const weapon = weapons.find(w => w.name.includes(material));
            if (weapon) return weapon;
        }

        // Fallback to first weapon
        return weapons[0] || null;
    }

    /**
     * Flee to base
     */
    async fleeToBase() {
        const base = this.survivalManager?.baseLocation;

        if (!base) {
            console.warn(`   ⚠️ No base to flee to!`);
            return;
        }

        console.log(`   🏃 Fleeing to base at (${base.x}, ${base.y}, ${base.z})...`);

        try {
            await this.bot.pathfinder.goto(
                new (require('mineflayer-pathfinder').goals.GoalNear)(base.x, base.y, base.z, 2)
            );

            // Look away from danger
            await this.bot.look(
                this.bot.entity.yaw + Math.PI,
                0
            );

            console.log(`   ✅ Reached base safely`);
        } catch (err) {
            console.warn(`   ⚠️ Failed to reach base: ${err.message}`);
        }
    }

    /**
     * Maybe pause after an action (simulates human reflection)
     */
    async maybePause() {
        if (Math.random() < this.pauseChance) {
            console.log(`   🤔 Taking a moment to admire the work...`);
            await this.sleep(this.pauseDuration);

            // Look around randomly
            const randomYaw = (Math.random() - 0.5) * Math.PI * 2;
            const randomPitch = (Math.random() - 0.5) * Math.PI / 2;

            await this.bot.look(randomYaw, randomPitch);
            await this.sleep(this.pauseDuration);
        }
    }

    /**
     * Smooth look rotation (instead of instant)
     */
    async smoothLook(yaw, pitch) {
        const currentYaw = this.bot.entity.yaw;
        const currentPitch = this.bot.entity.pitch;

        const yawDiff = this.normalizeAngle(yaw - currentYaw);
        const pitchDiff = pitch - currentPitch;

        const steps = 10;
        const yawStep = yawDiff / steps;
        const pitchStep = pitchDiff / steps;

        for (let i = 0; i < steps; i++) {
            this.bot.entity.yaw += yawStep;
            this.bot.entity.pitch += pitchStep;
            await this.sleep(20); // 1 tick
        }

        // Final adjustment
        await this.bot.look(yaw, pitch);
    }

    /**
     * Normalize angle to -PI to PI range
     */
    normalizeAngle(angle) {
        while (angle > Math.PI) angle -= Math.PI * 2;
        while (angle < -Math.PI) angle += Math.PI * 2;
        return angle;
    }

    /**
     * Sleep utility
     */
    sleep(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }
}
