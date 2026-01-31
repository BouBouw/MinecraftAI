package com.mcaibuilder.mixin;

import com.mcaibuilder.bot.BotManager;
import com.mcaibuilder.gui.BotControlScreen;
import com.mcaibuilder.selection.SelectionManager;
import com.mcaibuilder.mod.AIBuilderMod;
import net.minecraft.block.Blocks;
import net.minecraft.client.MinecraftClient;
import net.minecraft.client.network.ClientPlayerEntity;
import net.minecraft.client.network.ClientPlayerInteractionManager;
import net.minecraft.entity.Entity;
import net.minecraft.entity.player.PlayerEntity;
import net.minecraft.item.Items;
import net.minecraft.text.Text;
import net.minecraft.util.ActionResult;
import net.minecraft.util.Formatting;
import net.minecraft.util.Hand;
import net.minecraft.util.hit.BlockHitResult;
import net.minecraft.util.hit.EntityHitResult;
import net.minecraft.util.hit.HitResult;
import net.minecraft.util.math.BlockPos;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfo;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfoReturnable;

/**
 * Mixin pour intercepter les clics droits avec du papier
 * Permet de créer des sélections de zone
 */
@Mixin(ClientPlayerInteractionManager.class)
public class ClientPlayerInteractionManagerMixin {

    /**
     * Intercepte les clics droits sur des blocs
     */
    @Inject(method = "interactBlock", at = @At("HEAD"), cancellable = true)
    private void onInteractBlock(ClientPlayerEntity player, Hand hand,
                                  BlockHitResult hitResult, CallbackInfoReturnable<ActionResult> cir) {
        try {
            MinecraftClient client = MinecraftClient.getInstance();

            // Vérifier si le joueur tient du papier
            if (player.getStackInHand(hand).getItem() != Items.PAPER) {
                return; // Laisser le comportement normal
            }

            // Vérifier que c'est un clic sur un bloc
            if (hitResult.getType() != HitResult.Type.BLOCK) {
                return;
            }

            // Gérer la sélection
            SelectionManager selectionManager = SelectionManager.getInstance();

            // Si pas de sélection en cours, démarrer
            if (selectionManager.getState() == SelectionManager.SelectionState.IDLE) {
                selectionManager.startSelection();
                player.sendMessage(Text.literal("§dSélection démarrée - Clic droit pour la première position"));
            }

            // Gérer le clic
            SelectionManager.SelectionState previousState = selectionManager.getState();
            boolean handled = selectionManager.handleRightClick(hitResult.getBlockPos());

            if (handled) {
                BlockPos pos = hitResult.getBlockPos();

                // Afficher un message selon l'action
                if (previousState == SelectionManager.SelectionState.WAITING_FIRST) {
                    player.sendMessage(Text.literal(String.format("§dPremière sélection : §e%d, %d, %d", pos.getX(), pos.getY(), pos.getZ())));
                    player.sendMessage(Text.literal("§eClic droit pour la deuxième position"));
                } else if (previousState == SelectionManager.SelectionState.WAITING_SECOND) {
                    player.sendMessage(Text.literal(String.format("§dSeconde sélection : §e%d, %d, %d", pos.getX(), pos.getY(), pos.getZ())));
                    player.sendMessage(Text.literal("§eUtilisez §d/save §epour sauvegarder le fichier"));
                }

                // Annuler le placement de bloc (ne pas placer le papier)
                cir.setReturnValue(ActionResult.SUCCESS);
                return;
            }

        } catch (Exception e) {
            AIBuilderMod.LOGGER.error("Error handling paper interaction: {}", e.getMessage());
        }
    }

    /**
     * Intercepte les clics droits sur les entités (joueurs/bots)
     * Détecte les clics droits sur les bots pour ouvrir le GUI de contrôle
     */
    @Inject(method = "interactEntity", at = @At("HEAD"), cancellable = true)
    private void onInteractEntity(PlayerEntity player, Entity entity, Hand hand, CallbackInfoReturnable<ActionResult> cir) {
        try {
            MinecraftClient client = MinecraftClient.getInstance();

            // Vérifier que c'est un joueur
            if (!(entity instanceof PlayerEntity targetPlayer)) {
                return; // Laisser le comportement normal
            }

            // Vérifier si c'est un bot
            BotManager botManager = BotManager.getInstance();
            if (!botManager.isBot(targetPlayer)) {
                return; // Laisser le comportement normal
            }

            // Vérifier si c'est notre bot
            if (!botManager.isMyBot(targetPlayer)) {
                if (client.player != null) {
                    client.player.sendMessage(
                        Text.literal("Ce bot ne vous appartient pas !").formatted(Formatting.RED)
                    );
                }
                cir.setReturnValue(ActionResult.FAIL);
                return;
            }

            // Ouvrir le GUI de contrôle du bot
            BotManager.BotInfo botInfo = botManager.getBot(targetPlayer);
            BotControlScreen screen = new BotControlScreen(targetPlayer, botInfo);
            client.setScreen(screen);

            // Annuler l'interaction par défaut
            cir.setReturnValue(ActionResult.SUCCESS);

        } catch (Exception e) {
            AIBuilderMod.LOGGER.error("Error handling bot interaction: {}", e.getMessage());
        }
    }
}
