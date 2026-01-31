package com.mcaibuilder.mixin;

import com.mcaibuilder.bot.BotManager;
import com.mcaibuilder.gui.BotControlScreen;
import net.minecraft.client.MinecraftClient;
import net.minecraft.entity.Entity;
import net.minecraft.entity.player.PlayerEntity;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfo;

/**
 * Mixin to detect right-clicks on bot players
 */
@Mixin(MinecraftClient.class)
public class BotRightClickMixin {

    @Inject(method = "doItemUse", at = @At("HEAD"))
    private void onItemUse(CallbackInfo ci) {
        MinecraftClient client = (MinecraftClient) (Object) this;

        // Check if player is looking at an entity
        if (client.crosshairTarget == null) return;
        if (!client.crosshairTarget.getType().equals(net.minecraft.util.hit.HitResult.Type.ENTITY)) return;

        // Get the targeted entity
        Entity entity = ((net.minecraft.util.hit.EntityHitResult) client.crosshairTarget).getEntity();
        if (!(entity instanceof PlayerEntity player)) return;

        // Check if it's a bot
        BotManager botManager = BotManager.getInstance();
        if (!botManager.isBot(player)) return;

        // Check if it's owned by current player
        if (!botManager.isMyBot(player)) {
            if (client.player != null) {
                client.player.sendMessage(
                    net.minecraft.text.Text.literal("§cCe bot ne vous appartient pas !")
                );
            }
            return;
        }

        // Open bot control GUI
        BotControlScreen screen = new BotControlScreen(player, botManager.getBot(player));
        client.setScreen(screen);
    }
}
