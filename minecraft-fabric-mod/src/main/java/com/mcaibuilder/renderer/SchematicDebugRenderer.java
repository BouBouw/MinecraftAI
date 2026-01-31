package com.mcaibuilder.renderer;

import com.mcaibuilder.mod.AIBuilderMod;
import com.mcaibuilder.schematic.SchematicData;
import com.mcaibuilder.schematic.SchematicManager;
import net.minecraft.block.BlockState;
import net.minecraft.block.Blocks;
import net.minecraft.client.MinecraftClient;
import net.minecraft.util.math.BlockPos;

/**
 * Renderer pour schematic utilisant le DebugRenderer de Minecraft
 * Dessine des boîtes colorées pour chaque bloc du schematic
 * Approche 100% fiable car utilise le système officiel de Minecraft
 */
public class SchematicDebugRenderer {

    private final SchematicManager schematicManager;
    private boolean overlayEnabled = false;

    public SchematicDebugRenderer(SchematicManager schematicManager) {
        this.schematicManager = schematicManager;
    }

    /**
     * Active/désactive l'overlay
     */
    public void toggleOverlay() {
        this.overlayEnabled = !this.overlayEnabled;

        if (overlayEnabled) {
            AIBuilderMod.LOGGER.info("✅ Debug rendering enabled");
        } else {
            AIBuilderMod.LOGGER.info("❌ Debug rendering disabled");
        }
    }

    public boolean isOverlayEnabled() {
        return overlayEnabled;
    }

    /**
     * Retourne les positions des blocs à dessiner
     * Appelé par le système de rendu
     */
    public java.util.List<BlockPos> getBlockPositions() {
        java.util.List<BlockPos> positions = new java.util.ArrayList<>();

        if (!overlayEnabled || !schematicManager.hasActiveSchematic()) {
            return positions;
        }

        try {
            SchematicData schematic = schematicManager.getActiveSchematic();
            if (schematic == null) {
                return positions;
            }

            BlockPos origin = schematic.getOrigin();

            // Ajouter chaque position de bloc
            for (int y = 0; y < schematic.getHeight(); y++) {
                for (int z = 0; z < schematic.getLength(); z++) {
                    for (int x = 0; x < schematic.getWidth(); x++) {
                        BlockState blockState = schematic.getBlockAt(x, y, z);

                        if (blockState == null || blockState == Blocks.AIR.getDefaultState()) {
                            continue;
                        }

                        BlockPos worldPos = new BlockPos(
                            origin.getX() + x,
                            origin.getY() + y,
                            origin.getZ() + z
                        );

                        positions.add(worldPos);
                    }
                }
            }

        } catch (Exception e) {
            AIBuilderMod.LOGGER.error("Debug render error: {}", e.getMessage(), e);
        }

        return positions;
    }
}
