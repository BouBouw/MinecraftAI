package com.mcaibuilder.mixin;

import com.mcaibuilder.mod.AIBuilderClient;
import net.minecraft.client.MinecraftClient;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfo;

/**
 * Mixin pour intercepter les événements du client
 * Permet d'afficher des messages et gérer les touches
 */
@Mixin(MinecraftClient.class)
public class ClientMixin {

    /**
     * Injecte au début de chaque tick du client pour gérer les touches
     */
    @Inject(method = "tick", at = @At("HEAD"))
    private void onTick(CallbackInfo ci) {
        try {
            MinecraftClient client = (MinecraftClient) (Object) this;

            // Appeler notre méthode de gestion des touches
            AIBuilderClient.onClientTick(client);
        } catch (Exception e) {
            // Ignorer les erreurs pour éviter de crash le jeu
        }
    }
}
