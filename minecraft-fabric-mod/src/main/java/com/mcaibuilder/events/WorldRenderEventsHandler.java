package com.mcaibuilder.events;

import com.mcaibuilder.mod.AIBuilderClient;
import com.mcaibuilder.mod.AIBuilderMod;
import com.mcaibuilder.renderer.SchematicRenderer;
import net.fabricmc.fabric.api.client.rendering.v1.WorldRenderContext;
import net.fabricmc.fabric.api.client.rendering.v1.WorldRenderEvents;
import net.minecraft.client.render.Camera;
import net.minecraft.client.render.VertexConsumerProvider;
import net.minecraft.client.util.math.MatrixStack;
import net.minecraft.util.math.Vec3d;

/**
 * Gestionnaire d'événements de rendu du monde utilisant Fabric API
 * S'inscrit pendant l'initialisation du client
 */
public class WorldRenderEventsHandler {

    /**
     * Enregistre les événements de rendu
     */
    public static void register() {
        AIBuilderMod.LOGGER.info("Registering WorldRenderEvents...");

        // S'inscrire à l'événement AFTER_TRANSLUCENT - après le rendu des blocs translucides
        WorldRenderEvents.AFTER_TRANSLUCENT.register(context -> {
            try {
                SchematicRenderer schematicRenderer = AIBuilderClient.getSchematicRenderer();
                if (schematicRenderer != null && schematicRenderer.isOverlayEnabled()) {
                    MatrixStack matrices = context.matrixStack();
                    Camera camera = context.camera();
                    Vec3d cameraPos = camera.getPos();

                    VertexConsumerProvider.Immediate immediate = (VertexConsumerProvider.Immediate) context.consumers();
                    schematicRenderer.renderWorld(matrices, cameraPos, immediate);
                }
            } catch (Exception e) {
                AIBuilderMod.LOGGER.error("WorldRenderEvent error: {}", e.getMessage(), e);
            }
        });

        AIBuilderMod.LOGGER.info("✅ WorldRenderEvents registered successfully!");
    }
}
