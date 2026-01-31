package com.mcaibuilder.mixin;

import com.mcaibuilder.mod.AIBuilderClient;
import com.mcaibuilder.renderer.SchematicRenderer;
import net.minecraft.client.render.Camera;
import net.minecraft.client.render.WorldRenderer;
import net.minecraft.client.util.math.MatrixStack;
import net.minecraft.util.math.Vec3d;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfo;

/**
 * Mixin pour le rendu du schematic 3D
 * Utilise renderBlockEntities qui a une signature stable
 */
@Mixin(WorldRenderer.class)
public class WorldRendererSchematicMixin {

    /**
     * Injecte après le rendu des block entities
     * C'est le bon moment pour rendre notre overlay 3D
     */
    @Inject(method = "renderBlockEntities", at = @At("RETURN"))
    private void onRenderSchematic(MatrixStack matrices, Camera camera, CallbackInfo ci) {
        try {
            SchematicRenderer schematicRenderer = AIBuilderClient.getSchematicRenderer();
            if (schematicRenderer != null && schematicRenderer.isOverlayEnabled()
                && AIBuilderClient.getSchematicManager().hasActiveSchematic()) {

                Vec3d cameraPos = camera.getPos();
                schematicRenderer.renderWorld(matrices, cameraPos);
            }
        } catch (Exception e) {
            com.mcaibuilder.mod.AIBuilderMod.LOGGER.error("Schematic render error: {}", e.getMessage(), e);
        }
    }
}
