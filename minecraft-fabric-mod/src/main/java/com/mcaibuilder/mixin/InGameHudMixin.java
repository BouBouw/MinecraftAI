package com.mcaibuilder.mixin;

import com.mcaibuilder.gui.SchematicHud;
import com.mcaibuilder.mod.AIBuilderClient;
import com.mcaibuilder.renderer.SchematicRenderer;
import com.mcaibuilder.schematic.SchematicManager;
import net.minecraft.client.gui.DrawContext;
import net.minecraft.client.gui.hud.InGameHud;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfo;

/**
 * Mixin pour le rendu HUD dans le jeu
 * Permet d'afficher les informations du schematic et l'overlay 3D
 */
@Mixin(InGameHud.class)
public class InGameHudMixin {

    /**
     * Injecte après le rendu normal du HUD pour ajouter nos éléments
     */
    @Inject(method = "render", at = @At("RETURN"))
    private void afterRender(DrawContext context, float tickDelta, CallbackInfo ci) {
        try {
            SchematicRenderer renderer = AIBuilderClient.getSchematicRenderer();
            SchematicManager manager = AIBuilderClient.getSchematicManager();

            // Rendre le HUD textuel
            if (manager != null && manager.hasActiveSchematic()) {
                SchematicHud.setEnabled(renderer != null && renderer.isOverlayEnabled());
                SchematicHud.render(context, net.minecraft.client.MinecraftClient.getInstance());
            }
        } catch (Exception e) {
            // Ignorer les erreurs pour éviter de crash
        }
    }
}
