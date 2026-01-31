package com.mcaibuilder.schematic;

import net.minecraft.block.BlockState;
import net.minecraft.block.Blocks;
import net.minecraft.util.math.BlockPos;

import com.mcaibuilder.mod.AIBuilderMod;

import java.io.File;
import java.util.HashMap;
import java.util.Map;

/**
 * Manager for active schematic operations
 */
public class SchematicManager {

    private SchematicData activeSchematic;
    private SchematicLoader loader;
    private BlockPos position;
    private int rotation; // 0, 90, 180, 270
    private boolean enabled = false;
    private boolean locked = false; // Indique si la position est verrouillée

    public SchematicManager() {
        this.loader = new SchematicLoader();
        this.position = new BlockPos(0, 0, 0);
        this.rotation = 0;
    }

    /**
     * Load a schematic from file
     */
    public boolean loadSchematic(String filepath) {
        File file = new File(filepath);
        if (!file.exists()) {
            AIBuilderMod.LOGGER.error("Schematic file not found: {}", filepath);
            return false;
        }

        SchematicData schematic = loader.loadSchematic(file);
        if (schematic != null) {
            this.activeSchematic = schematic;
            this.enabled = true;
            AIBuilderMod.LOGGER.info("Schematic loaded successfully: {}", schematic.getName());
            return true;
        }

        return false;
    }

    /**
     * Set the position for the schematic
     */
    public void setPosition(BlockPos pos) {
        this.position = pos;
        if (activeSchematic != null) {
            activeSchematic = new SchematicData(
                activeSchematic.getName(),
                activeSchematic.getWidth(),
                activeSchematic.getHeight(),
                activeSchematic.getLength(),
                activeSchematic.getBlocks(),
                pos
            );
        }
    }

    /**
     * Move schematic to absolute position
     */
    public void moveSchematicTo(int x, int y, int z) {
        setPosition(new BlockPos(x, y, z));
        AIBuilderMod.LOGGER.info("Schematic moved to ({}, {}, {})", x, y, z);
    }

    /**
     * Move the schematic up or down
     */
    public void moveSchematic(int deltaY) {
        if (activeSchematic != null && !locked) {
            BlockPos newPos = position.up(deltaY);
            setPosition(newPos);
            AIBuilderMod.LOGGER.info("Schematic moved {} to Y={}", deltaY > 0 ? "up" : "down", newPos.getY());
        } else if (locked) {
            AIBuilderMod.LOGGER.info("Schematic is locked, cannot move");
        }
    }

    /**
     * Move the schematic horizontally (X and Z axes)
     * @param deltaX Offset for X axis (positive = east, negative = west)
     * @param deltaZ Offset for Z axis (positive = south, negative = north)
     */
    public void moveSchematicHorizontal(int deltaX, int deltaZ) {
        if (activeSchematic != null && !locked) {
            BlockPos newPos = position.add(deltaX, 0, deltaZ);
            setPosition(newPos);
            AIBuilderMod.LOGGER.info("Schematic moved horizontally by ({}, {}) to ({}, {}, {})",
                deltaX, deltaZ, newPos.getX(), newPos.getY(), newPos.getZ());
        } else if (locked) {
            AIBuilderMod.LOGGER.info("Schematic is locked, cannot move");
        }
    }

    /**
     * Check if there's an active schematic
     */
    public boolean hasActiveSchematic() {
        return activeSchematic != null && enabled;
    }

    /**
     * Get the active schematic
     */
    public SchematicData getActiveSchematic() {
        return activeSchematic;
    }

    /**
     * Get list of required materials with counts
     */
    public Map<String, Integer> getRequiredMaterials() {
        Map<String, Integer> materials = new HashMap<>();

        if (activeSchematic == null) {
            return materials;
        }

        for (BlockState block : activeSchematic.getBlocks()) {
            if (block != null && block != Blocks.AIR.getDefaultState()) {
                String blockId = block.getBlock().getTranslationKey();
                materials.put(blockId, materials.getOrDefault(blockId, 0) + 1);
            }
        }

        return materials;
    }

    /**
     * Clear the active schematic
     */
    public void clearSchematic() {
        this.activeSchematic = null;
        this.enabled = false;
        AIBuilderMod.LOGGER.info("Schematic cleared");
    }

    /**
     * Toggle schematic visibility
     */
    public void toggleEnabled() {
        this.enabled = !this.enabled;
    }

    public boolean isEnabled() {
        return enabled;
    }

    public BlockPos getPosition() {
        return position;
    }

    /**
     * Verrouille la position du schematic
     */
    public void lock() {
        this.locked = true;
        AIBuilderMod.LOGGER.info("Schematic locked at position ({}, {}, {})", position.getX(), position.getY(), position.getZ());
    }

    /**
     * Déverrouille la position du schematic
     */
    public void unlock() {
        this.locked = false;
        AIBuilderMod.LOGGER.info("Schematic unlocked");
    }

    /**
     * Toggle le lock du schematic
     */
    public void toggleLock() {
        this.locked = !this.locked;
        AIBuilderMod.LOGGER.info("Schematic lock toggled: {}", locked ? "LOCKED" : "UNLOCKED");
    }

    /**
     * Vérifie si le schematic est verrouillé
     */
    public boolean isLocked() {
        return locked;
    }
}
