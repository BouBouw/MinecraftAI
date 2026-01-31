package com.mcaibuilder.mixin;

import com.mcaibuilder.mod.AIBuilderClient;
import com.mcaibuilder.renderer.SchematicDebugRenderer;
import net.minecraft.client.MinecraftClient;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfo;

/**
 * Mixin pour mettre à jour le rendu du schematic à chaque tick
 */
@Mixin(MinecraftClient.class)
public class SchematicDebugMixin {

    /**
     * Met à jour les boîtes de debug du schematic à chaque tick client
     */
    @Inject(method = "tick", at = @At("TAIL"))
    private void onTick(CallbackInfo ci) {
        try {
            SchematicDebugRenderer debugRenderer = AIBuilderClient.getSchematicDebugRenderer();
            if (debugRenderer != null) {
                debugRenderer.updateDebugBoxes();
            }
        } catch (Exception e) {
            // Ignorer les erreurs pendant le tick
        }
    }
}
