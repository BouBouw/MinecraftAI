package com.mcaibuilder.schematic;

import net.minecraft.block.BlockState;
import net.minecraft.util.math.BlockPos;

/**
 * Data class representing a loaded schematic
 */
public class SchematicData {

    private final String name;
    private final int width;
    private final int height;
    private final int length;
    private final BlockState[] blocks;
    private final BlockPos origin;

    public SchematicData(String name, int width, int height, int length, BlockState[] blocks, BlockPos origin) {
        this.name = name;
        this.width = width;
        this.height = height;
        this.length = length;
        this.blocks = blocks;
        this.origin = origin;
    }

    public String getName() {
        return name;
    }

    public int getWidth() {
        return width;
    }

    public int getHeight() {
        return height;
    }

    public int getLength() {
        return length;
    }

    public BlockState[] getBlocks() {
        return blocks;
    }

    public BlockPos getOrigin() {
        return origin;
    }

    public int getTotalBlocks() {
        // Return the expected size based on dimensions, not array length
        // (array might be larger due to reuse from previous schematic)
        return width * height * length;
    }

    /**
     * Get block at relative position
     */
    public BlockState getBlockAt(int x, int y, int z) {
        if (x < 0 || x >= width || y < 0 || y >= height || z < 0 || z >= length) {
            return null;
        }
        int index = y * width * length + z * width + x;
        // Safety check: don't read past array bounds
        if (index < 0 || index >= blocks.length) {
            return null;
        }
        return blocks[index];
    }

    /**
     * Get world position from relative position
     */
    public BlockPos getWorldPosition(int x, int y, int z) {
        return new BlockPos(origin.getX() + x, origin.getY() + y, origin.getZ() + z);
    }
}
