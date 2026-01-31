package com.mcaibuilder.selection;

import net.minecraft.block.BlockState;
import net.minecraft.block.Blocks;
import net.minecraft.nbt.NbtCompound;
import net.minecraft.nbt.NbtHelper;
import net.minecraft.nbt.NbtIo;
import net.minecraft.nbt.NbtList;
import net.minecraft.nbt.NbtSizeTracker;
import net.minecraft.registry.Registries;
import net.minecraft.util.Identifier;
import net.minecraft.util.math.BlockPos;
import net.minecraft.util.math.Box;
import net.minecraft.util.math.Vec3d;

import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.nio.file.Path;
import java.util.HashMap;
import java.util.Map;
import java.util.zip.GZIPOutputStream;

/**
 * Gestionnaire de sélection de zone pour la capture de constructions
 * Utilise le papier pour définir deux positions (initiale et finale)
 */
public class SelectionManager {

    public enum SelectionState {
        IDLE,           // Pas de sélection en cours
        WAITING_FIRST,  // Attend le premier clic droit
        WAITING_SECOND  // Attend le deuxième clic droit
    }

    private SelectionState state = SelectionState.IDLE;
    private BlockPos firstPos = null;
    private BlockPos secondPos = null;
    private Map<BlockPos, BlockState> capturedBlocks = new HashMap<>();

    private static SelectionManager instance;

    private SelectionManager() {}

    public static SelectionManager getInstance() {
        if (instance == null) {
            instance = new SelectionManager();
        }
        return instance;
    }

    /**
     * Démarre une nouvelle sélection
     */
    public void startSelection() {
        state = SelectionState.WAITING_FIRST;
        firstPos = null;
        secondPos = null;
        capturedBlocks.clear();
        com.mcaibuilder.mod.AIBuilderMod.LOGGER.info("📝 Selection started - Right-click to set first position");
    }

    /**
     * Gère un clic droit sur un bloc
     * Retourne true si le clic a été utilisé par le système de sélection
     */
    public boolean handleRightClick(BlockPos pos) {
        if (state == SelectionState.IDLE) {
            return false;
        }

        if (state == SelectionState.WAITING_FIRST) {
            firstPos = pos;
            state = SelectionState.WAITING_SECOND;
            com.mcaibuilder.mod.AIBuilderMod.LOGGER.info("✅ First position set at ({}, {}, {})", pos.getX(), pos.getY(), pos.getZ());
            com.mcaibuilder.mod.AIBuilderMod.LOGGER.info("📝 Right-click again to set second position");
            return true;
        }

        if (state == SelectionState.WAITING_SECOND) {
            secondPos = pos;
            state = SelectionState.IDLE;
            com.mcaibuilder.mod.AIBuilderMod.LOGGER.info("✅ Second position set at ({}, {}, {})", pos.getX(), pos.getY(), pos.getZ());
            com.mcaibuilder.mod.AIBuilderMod.LOGGER.info("📦 Selection complete! Use commands to save.");
            return true;
        }

        return false;
    }

    /**
     * Annule la sélection en cours
     */
    public void cancelSelection() {
        state = SelectionState.IDLE;
        firstPos = null;
        secondPos = null;
        capturedBlocks.clear();
        com.mcaibuilder.mod.AIBuilderMod.LOGGER.info("❌ Selection cancelled");
    }

    /**
     * Capture les blocs entre les deux positions
     */
    public void captureBlocks(net.minecraft.world.World world) {
        if (firstPos == null || secondPos == null) {
            com.mcaibuilder.mod.AIBuilderMod.LOGGER.warn("⚠️  Cannot capture: positions not set");
            return;
        }

        capturedBlocks.clear();

        Box box = new Box(Vec3d.of(firstPos), Vec3d.of(secondPos));
        int minX = (int) Math.min(box.minX, box.maxX);
        int minY = (int) Math.min(box.minY, box.maxY);
        int minZ = (int) Math.min(box.minZ, box.maxZ);
        int maxX = (int) Math.max(box.minX, box.maxX);
        int maxY = (int) Math.max(box.minY, box.maxY);
        int maxZ = (int) Math.max(box.minZ, box.maxZ);

        int blockCount = 0;

        for (int x = minX; x <= maxX; x++) {
            for (int y = minY; y <= maxY; y++) {
                for (int z = minZ; z <= maxZ; z++) {
                    BlockPos pos = new BlockPos(x, y, z);
                    BlockState state = world.getBlockState(pos);

                    if (state != null && state != Blocks.AIR.getDefaultState()) {
                        capturedBlocks.put(pos, state);
                        blockCount++;
                    }
                }
            }
        }

        com.mcaibuilder.mod.AIBuilderMod.LOGGER.info("📦 Captured {} blocks", blockCount);
    }

    /**
     * Sauvegarde la sélection en fichier schematic
     */
    public boolean saveToSchematic(String filename) {
        if (capturedBlocks.isEmpty()) {
            com.mcaibuilder.mod.AIBuilderMod.LOGGER.warn("⚠️  No blocks to save");
            return false;
        }

        try {
            // Calculer les dimensions
            Box box = new Box(Vec3d.of(firstPos), Vec3d.of(secondPos));
            int minX = (int) Math.min(box.minX, box.maxX);
            int minY = (int) Math.min(box.minY, box.maxY);
            int minZ = (int) Math.min(box.minZ, box.maxZ);
            int maxX = (int) Math.max(box.minX, box.maxX);
            int maxY = (int) Math.max(box.minY, box.maxY);
            int maxZ = (int) Math.max(box.minZ, box.maxZ);

            int width = maxX - minX + 1;
            int height = maxY - minY + 1;
            int length = maxZ - minZ + 1;

            // Créer la structure NBT pour Sponge Schematic format
            NbtCompound schematic = new NbtCompound();
            schematic.putInt("Version", 2);
            schematic.putInt("DataVersion", 3700);
            schematic.putInt("Width", width);
            schematic.putInt("Height", height);
            schematic.putInt("Length", length);

            // Créer la palette (mapping des blocs)
            Map<String, Integer> palette = new HashMap<>();
            int nextPaletteId = 0;

            // Créer les données de blocs
            for (Map.Entry<BlockPos, BlockState> entry : capturedBlocks.entrySet()) {
                BlockState state = entry.getValue();
                String blockId = Registries.BLOCK.getId(state.getBlock()).toString();

                if (!palette.containsKey(blockId)) {
                    palette.put(blockId, nextPaletteId++);
                }
            }

            // Créer le NBT de la palette
            NbtCompound paletteData = new NbtCompound();
            for (Map.Entry<String, Integer> entry : palette.entrySet()) {
                paletteData.putInt(entry.getKey(), entry.getValue());
            }
            schematic.put("Palette", paletteData);

            // Préparer les données de blocs (varint encoding)
            java.io.ByteArrayOutputStream blockDataBytes = new java.io.ByteArrayOutputStream();
            for (int y = 0; y < height; y++) {
                for (int z = 0; z < length; z++) {
                    for (int x = 0; x < width; x++) {
                        BlockPos localPos = new BlockPos(x, y, z);
                        BlockPos worldPos = new BlockPos(minX + x, minY + y, minZ + z);

                        BlockState state = capturedBlocks.get(worldPos);
                        String blockId = (state != null) ? Registries.BLOCK.getId(state.getBlock()).toString() : "minecraft:air";

                        int paletteId = palette.getOrDefault(blockId, 0);

                        // Varint encoding
                        while ((paletteId & ~0x7F) != 0) {
                            blockDataBytes.write((paletteId & 0x7F) | 0x80);
                            paletteId >>>= 7;
                        }
                        blockDataBytes.write(paletteId);
                    }
                }
            }

            // Ajouter les données de blocs directement (Sponge Schematic v2 format)
            schematic.putByteArray("BlockData", blockDataBytes.toByteArray());

            // Sauvegarder le fichier
            File outputFile = new java.io.File(filename);
            try (FileOutputStream fos = new FileOutputStream(outputFile);
                 GZIPOutputStream gzos = new GZIPOutputStream(fos)) {

                NbtIo.writeCompressed(schematic, gzos);
                gzos.finish();
            }

            com.mcaibuilder.mod.AIBuilderMod.LOGGER.info("💾 Saved schematic to {} ({} blocks)", filename, capturedBlocks.size());
            return true;

        } catch (IOException e) {
            com.mcaibuilder.mod.AIBuilderMod.LOGGER.error("Failed to save schematic: {}", e.getMessage(), e);
            return false;
        }
    }

    // Getters
    public SelectionState getState() {
        return state;
    }

    public BlockPos getFirstPos() {
        return firstPos;
    }

    public BlockPos getSecondPos() {
        return secondPos;
    }

    public boolean hasSelection() {
        return firstPos != null && secondPos != null;
    }

    public Box getSelectionBox() {
        if (!hasSelection()) {
            return null;
        }
        return new Box(Vec3d.of(firstPos), Vec3d.of(secondPos));
    }

    public int getBlockCount() {
        return capturedBlocks.size();
    }
}
