package com.mcaibuilder.renderer;

import com.mcaibuilder.mod.AIBuilderMod;
import net.minecraft.client.MinecraftClient;
import net.minecraft.util.math.Vec3d;

/**
 * Renderer simple et direct pour les schematics
 */
public class SchematicOverlayRenderer {

    private static boolean shouldRender = false;
    private static int blockCount = 0;

    /**
     * Marque que le rendu est nécessaire
     */
    public static void markForRendering(int blockCount) {
        shouldRender = true;
        SchematicOverlayRenderer.blockCount = blockCount;
    }

    /**
     * Marque que le rendu n'est pas nécessaire
     */
    public static void clearRendering() {
        shouldRender = false;
        blockCount = 0;
    }

    /**
     * Vérifie si le rendu est nécessaire
     */
    public static boolean shouldRender() {
        return shouldRender;
    }

    /**
     * Affiche un message de debug en jeu
     */
    public static void renderDebugText(MinecraftClient client) {
        if (!shouldRender || client.player == null) {
            return;
        }

        try {
            Vec3d cameraPos = client.gameRenderer.getCamera().getPos();

            // Afficher un message simple dans les logs pour confirmer que le rendu est appelé
            AIBuilderMod.LOGGER.debug("Rendering {} blocks at camera position ({}, {}, {})",
                blockCount, cameraPos.x, cameraPos.y, cameraPos);
        } catch (Exception e) {
            // Ignorer les erreurs
        }
    }
}
