package com.mcaibuilder.mixin;

import com.mcaibuilder.mod.AIBuilderMod;
import com.mcaibuilder.selection.SelectionManager;
import net.minecraft.client.MinecraftClient;
import net.minecraft.client.network.ClientPlayerEntity;
import net.minecraft.text.Text;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfo;

/**
 * Mixin pour intercepter les messages du chat
 * Permet d'implémenter des commandes personnalisées comme /save
 */
@Mixin(ClientPlayerEntity.class)
public class ClientPlayerChatMixin {

    /**
     * Intercepte l'envoi de commandes dans le chat
     */
    @Inject(method = "sendCommand", at = @At("HEAD"), cancellable = true)
    private void onSendCommand(String command, CallbackInfo ci) {
        if (command == null || command.isEmpty()) {
            return;
        }

        // Vérifier si c'est la commande /save
        if (command.trim().equalsIgnoreCase("/save")) {
            // Annuler l'envoi de la commande normale
            ci.cancel();

            // Gérer la sauvegarde
            handleSaveCommand();
            return;
        }
    }

    /**
     * Gère la commande /save pour sauvegarder la sélection
     */
    private void handleSaveCommand() {
        ClientPlayerEntity player = (ClientPlayerEntity) (Object) this;
        SelectionManager selectionManager = SelectionManager.getInstance();

        try {
            if (!selectionManager.hasSelection()) {
                player.sendMessage(Text.literal("§cErreur : Aucune sélection active"));
                player.sendMessage(Text.literal("§eUtilisez du papier et faites 2 clics droits pour définir une zone"));
                AIBuilderMod.LOGGER.warn("Attempted to save without selection");
                return;
            }

            // Capturer les blocs
            MinecraftClient client = MinecraftClient.getInstance();
            if (client.world == null) {
                player.sendMessage(Text.literal("§cErreur : Monde non chargé"));
                return;
            }

            selectionManager.captureBlocks(client.world);

            int blockCount = selectionManager.getBlockCount();
            if (blockCount == 0) {
                player.sendMessage(Text.literal("§cErreur : Aucun bloc dans la sélection"));
                AIBuilderMod.LOGGER.warn("Selection contains no blocks");
                return;
            }

            // Générer le nom du fichier avec timestamp
            String timestamp = new java.text.SimpleDateFormat("yyyyMMdd_HHmmss").format(new java.util.Date());
            String filename = "build_" + timestamp + ".schem";

            // Sauvegarder
            boolean saved = selectionManager.saveToSchematic(filename);

            if (saved) {
                player.sendMessage(Text.literal("§aSauvegarde réussie !"));
                player.sendMessage(Text.literal(String.format("§eFichier : §d%s", filename)));
                player.sendMessage(Text.literal(String.format("§eBlocs capturés : §d%d", blockCount)));
                AIBuilderMod.LOGGER.info("Selection saved to {}", filename);
            } else {
                player.sendMessage(Text.literal("§cErreur lors de la sauvegarde"));
                AIBuilderMod.LOGGER.error("Failed to save schematic");
            }

        } catch (Exception e) {
            player.sendMessage(Text.literal("§cErreur : " + e.getMessage()));
            AIBuilderMod.LOGGER.error("Error saving schematic", e);
        }
    }
}
