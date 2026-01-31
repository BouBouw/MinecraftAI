package com.mcaibuilder.mod;

import net.fabricmc.api.ClientModInitializer;
import net.minecraft.client.MinecraftClient;
import net.minecraft.util.math.BlockPos;

import com.mcaibuilder.events.WorldRenderEventsHandler;
import com.mcaibuilder.gui.InGameMessenger;
import com.mcaibuilder.renderer.SchematicRenderer;
import com.mcaibuilder.renderer.SchematicDebugRenderer;
import com.mcaibuilder.schematic.SchematicManager;
import com.mcaibuilder.network.ModWebSocketClient;
import com.mcaibuilder.config.ModConfig;
import com.mcaibuilder.config.ModKeyBindings;
import com.mcaibuilder.selection.SelectionManager;

/**
 * Client-side initialization for AI Builder Mod
 * Handles rendering, input, and communication
 */
public class AIBuilderClient implements ClientModInitializer {

    private static SchematicManager schematicManager;
    private static SchematicRenderer schematicRenderer;
    private static SchematicDebugRenderer schematicDebugRenderer;
    private static ModWebSocketClient webSocketClient;

    @Override
    public void onInitializeClient() {
        AIBuilderMod.LOGGER.info("AI Builder Client initializing...");

        // Register keybindings
        ModKeyBindings.register();

        // Initialize managers (WebSocket will be initialized later when needed)
        schematicManager = new SchematicManager();
        schematicRenderer = new SchematicRenderer(schematicManager);
        schematicDebugRenderer = new SchematicDebugRenderer(schematicManager);
        // Don't initialize WebSocket yet to avoid blocking game startup
        webSocketClient = null;

        // Enregistrer les événements de rendu de Fabric API
        WorldRenderEventsHandler.register();

        // Auto-load test schematic if it exists
        loadTestSchematic();

        AIBuilderMod.LOGGER.info("✅ AI Builder Client initialized successfully!");
        AIBuilderMod.LOGGER.info("🎮 Keybinds registered in Controls menu!");
    }

    /**
     * Charge automatiquement le schematic de test
     * Le positionnement se fera plus tard quand le joueur sera dans le monde
     * Cherche build.schem, build.nbt, ou build.litematic (par ordre de priorité)
     */
    private void loadTestSchematic() {
        try {
            String[] testFiles = {"build.schem", "build.nbt", "build.litematic"};
            String foundFile = null;

            // Chercher le premier fichier qui existe
            for (String fileName : testFiles) {
                java.io.File file = new java.io.File(fileName);
                if (file.exists()) {
                    foundFile = fileName;
                    break;
                }
            }

            if (foundFile != null) {
                AIBuilderMod.LOGGER.info("Loading test schematic from {}...", foundFile);
                boolean loaded = schematicManager.loadSchematic(foundFile);

                if (loaded) {
                    AIBuilderMod.LOGGER.info("✅ Test schematic loaded successfully!");
                    AIBuilderMod.LOGGER.info("   Dimensions: {}x{}x{}",
                        schematicManager.getActiveSchematic().getWidth(),
                        schematicManager.getActiveSchematic().getHeight(),
                        schematicManager.getActiveSchematic().getLength()
                    );
                    AIBuilderMod.LOGGER.info("   ⏳ Waiting for player to position schematic...");
                } else {
                    AIBuilderMod.LOGGER.warn("⚠️  Failed to load test schematic");
                }
            } else {
                AIBuilderMod.LOGGER.info("No test schematic found (looking for build.schem, build.nbt, build.litematic)");
                AIBuilderMod.LOGGER.info("Place one of these files at the root to test the mod");
            }
        } catch (Exception e) {
            AIBuilderMod.LOGGER.error("Error loading test schematic: {}", e.getMessage());
        }
    }

    /**
     * Called from mixins to handle key presses using KeyBindings
     */
    public static void onClientTick(MinecraftClient client) {
        if (client.player == null) return;

        // Check R key - toggle overlay
        while (ModKeyBindings.TOGGLE_OVERLAY.wasPressed()) {
            // Utiliser le debugRenderer pour le rendu fiable
            schematicDebugRenderer.toggleOverlay();
            boolean enabled = schematicDebugRenderer.isOverlayEnabled();
            AIBuilderMod.LOGGER.info("🔄 Overlay toggled: {}", enabled);

            // Message dans le chat (uniquement pour le joueur)
            if (client.player != null) {
                String message = enabled ? "§a✓ Overlay Activé" : "§c✗ Overlay Désactivé";
                client.player.sendMessage(net.minecraft.text.Text.literal(message));
                AIBuilderMod.LOGGER.info("Message envoyé au joueur: {}", message);
            }

            // Repositionner le schematic près du joueur quand on active l'overlay
            if (enabled && schematicManager.hasActiveSchematic()) {
                repositionSchematicNearPlayer(client);
            }

            // Toggle aussi le renderer old school pour compatibilité
            schematicRenderer.toggleOverlay();
        }

        // Check LEFT SHIFT - move schematic up
        while (ModKeyBindings.MOVE_UP.wasPressed()) {
            if (schematicDebugRenderer.isOverlayEnabled()) {
                schematicManager.moveSchematic(1);
                AIBuilderMod.LOGGER.info("⬆️  Schematic moved up");
                if (client.player != null) {
                    client.player.sendMessage(net.minecraft.text.Text.literal("§e⬆️ Schematic déplacé vers le haut"));
                }
            }
        }

        // Check LEFT CONTROL - move schematic down
        while (ModKeyBindings.MOVE_DOWN.wasPressed()) {
            if (schematicDebugRenderer.isOverlayEnabled()) {
                schematicManager.moveSchematic(-1);
                AIBuilderMod.LOGGER.info("⬇️  Schematic moved down");
                if (client.player != null) {
                    client.player.sendMessage(net.minecraft.text.Text.literal("§e⬇️ Schematic déplacé vers le bas"));
                }
            }
        }

        // Check ENTER - validate and send to bot
        while (ModKeyBindings.VALIDATE_SCHEMATIC.wasPressed()) {
            if (schematicDebugRenderer.isOverlayEnabled()) {
                if (schematicManager.hasActiveSchematic()) {
                    AIBuilderMod.LOGGER.info("✅ Validating schematic and sending to bot...");
                    InGameMessenger.showSuccess(client, "Schematic validated! Sending to bot...");

                    // Initialize WebSocket if not already done
                    if (webSocketClient == null) {
                        try {
                            webSocketClient = new ModWebSocketClient(java.net.URI.create(ModConfig.WEBSOCKET_SERVER_URL));
                        } catch (Exception e) {
                            AIBuilderMod.LOGGER.error("❌ Failed to create WebSocket client: {}", e.getMessage());
                            InGameMessenger.showError(client, "Failed to connect to bot");
                            return;
                        }
                    }

                    webSocketClient.sendSchematicValidation(
                        schematicManager.getActiveSchematic(),
                        client.player.getBlockPos()
                    );
                } else {
                    AIBuilderMod.LOGGER.warn("⚠️  No active schematic to validate");
                    InGameMessenger.showError(client, "No active schematic to validate");
                }
            }
        }

        // Check if overlay is enabled for keybinds
        boolean overlayEnabled = schematicDebugRenderer.isOverlayEnabled();

        // Check V key - save selection OR lock schematic and send bot
        while (ModKeyBindings.SAVE_SELECTION.wasPressed()) {
            if (overlayEnabled && schematicManager.hasActiveSchematic()) {
                // Mode overlay: Lock schematic et envoyer le bot
                handleLockAndSendBot(client);
            } else {
                // Mode normal: Sauvegarder la sélection
                handleSaveCommand(client);
            }
        }

        // Arrow keys - move schematic (only when overlay is enabled)

        // LEFT arrow - move schematic west (negative X)
        while (ModKeyBindings.MOVE_LEFT.wasPressed()) {
            if (overlayEnabled) {
                schematicManager.moveSchematicHorizontal(-1, 0);
                AIBuilderMod.LOGGER.info("⬅️  Schematic moved left (west)");
                if (client.player != null) {
                    client.player.sendMessage(net.minecraft.text.Text.literal("§e⬅️ Schematic déplacé vers la gauche (ouest)"));
                }
            }
        }

        // RIGHT arrow - move schematic east (positive X)
        while (ModKeyBindings.MOVE_RIGHT.wasPressed()) {
            if (overlayEnabled) {
                schematicManager.moveSchematicHorizontal(1, 0);
                AIBuilderMod.LOGGER.info("➡️  Schematic moved right (east)");
                if (client.player != null) {
                    client.player.sendMessage(net.minecraft.text.Text.literal("§e➡️ Schematic déplacé vers la droite (est)"));
                }
            }
        }

        // UP arrow - move schematic north (negative Z)
        while (ModKeyBindings.MOVE_FORWARD.wasPressed()) {
            if (overlayEnabled) {
                schematicManager.moveSchematicHorizontal(0, -1);
                AIBuilderMod.LOGGER.info("⬆️  Schematic moved forward (north)");
                if (client.player != null) {
                    client.player.sendMessage(net.minecraft.text.Text.literal("§e⬆️ Schematic déplacé vers l'avant (nord)"));
                }
            }
        }

        // DOWN arrow - move schematic south (positive Z)
        while (ModKeyBindings.MOVE_BACKWARD.wasPressed()) {
            if (overlayEnabled) {
                schematicManager.moveSchematicHorizontal(0, 1);
                AIBuilderMod.LOGGER.info("⬇️  Schematic moved backward (south)");
                if (client.player != null) {
                    client.player.sendMessage(net.minecraft.text.Text.literal("§e⬇️ Schematic déplacé vers l'arrière (sud)"));
                }
            }
        }
    }

    /**
     * Repositionne le schematic près du joueur de manière intelligente
     * NE REPOSITIONNE PAS si le schematic est locké
     */
    private static void repositionSchematicNearPlayer(MinecraftClient client) {
        // Ne pas repositionner si le schematic est locké
        if (schematicManager.isLocked()) {
            AIBuilderMod.LOGGER.info("🔒 Schematic is locked, not repositioning");
            BlockPos lockedPos = schematicManager.getPosition();
            AIBuilderMod.LOGGER.info("   Locked position: ({}, {}, {})", lockedPos.getX(), lockedPos.getY(), lockedPos.getZ());
            return;
        }

        BlockPos playerPos = client.player.getBlockPos();

        // Calculer la position idéale:
        // - X, Z: Devant le joueur (dans la direction du regard)
        // - Y: Au niveau des pieds du joueur
        float yaw = client.player.getYaw();
        float distance = 3; // 3 blocs devant le joueur

        // Calculer la position devant le joueur
        double offsetX = -Math.sin(Math.toRadians(yaw)) * distance;
        double offsetZ = Math.cos(Math.toRadians(yaw)) * distance;

        int schematicX = (int)(playerPos.getX() + offsetX);
        int schematicY = playerPos.getY(); // Au niveau des pieds du joueur
        int schematicZ = (int)(playerPos.getZ() + offsetZ);

        // Centrer le schematic sur cette position
        int width = schematicManager.getActiveSchematic().getWidth();
        int length = schematicManager.getActiveSchematic().getLength();
        schematicX -= width / 2;
        schematicZ -= length / 2;

        schematicManager.moveSchematicTo(schematicX, schematicY, schematicZ);

        AIBuilderMod.LOGGER.info("📍 Schematic repositioned at ({}, {}, {})", schematicX, schematicY, schematicZ);
        AIBuilderMod.LOGGER.info("   Player is at ({}, {}, {})", playerPos.getX(), playerPos.getY(), playerPos.getZ());
    }

    // Getters for access from other classes
    public static SchematicManager getSchematicManager() {
        return schematicManager;
    }

    public static SchematicRenderer getSchematicRenderer() {
        return schematicRenderer;
    }

    public static ModWebSocketClient getWebSocketClient() {
        return webSocketClient;
    }

    public static SchematicDebugRenderer getSchematicDebugRenderer() {
        return schematicDebugRenderer;
    }

    /**
     * Show a notification message to the player (called from WebSocket client)
     */
    public static void showNotification(String message) {
        MinecraftClient client = MinecraftClient.getInstance();
        if (client != null && client.player != null) {
            client.player.sendMessage(net.minecraft.text.Text.literal(message));
        }
    }

    /**
     * Gère la sauvegarde de la sélection (touche V)
     */
    private static void handleSaveCommand(MinecraftClient client) {
        SelectionManager selectionManager = SelectionManager.getInstance();

        try {
            if (!selectionManager.hasSelection()) {
                client.player.sendMessage(net.minecraft.text.Text.literal("§cErreur : Aucune sélection active"));
                client.player.sendMessage(net.minecraft.text.Text.literal("§eUtilisez du papier et faites 2 clics droits pour définir une zone"));
                AIBuilderMod.LOGGER.warn("Attempted to save without selection");
                return;
            }

            // Capturer les blocs
            if (client.world == null) {
                client.player.sendMessage(net.minecraft.text.Text.literal("§cErreur : Monde non chargé"));
                return;
            }

            selectionManager.captureBlocks(client.world);

            int blockCount = selectionManager.getBlockCount();
            if (blockCount == 0) {
                client.player.sendMessage(net.minecraft.text.Text.literal("§cErreur : Aucun bloc dans la sélection"));
                AIBuilderMod.LOGGER.warn("Selection contains no blocks");
                return;
            }

            // Générer le nom du fichier avec timestamp
            String timestamp = new java.text.SimpleDateFormat("yyyyMMdd_HHmmss").format(new java.util.Date());
            String filename = "build_" + timestamp + ".schem";

            // Sauvegarder
            boolean saved = selectionManager.saveToSchematic(filename);

            if (saved) {
                client.player.sendMessage(net.minecraft.text.Text.literal("§aSauvegarde réussie !"));
                client.player.sendMessage(net.minecraft.text.Text.literal(String.format("§eFichier : §d%s", filename)));
                client.player.sendMessage(net.minecraft.text.Text.literal(String.format("§eBlocs capturés : §d%d", blockCount)));
                AIBuilderMod.LOGGER.info("Selection saved to {}", filename);
            } else {
                client.player.sendMessage(net.minecraft.text.Text.literal("§cErreur lors de la sauvegarde"));
                AIBuilderMod.LOGGER.error("Failed to save schematic");
            }

        } catch (Exception e) {
            client.player.sendMessage(net.minecraft.text.Text.literal("§cErreur : " + e.getMessage()));
            AIBuilderMod.LOGGER.error("Error saving schematic", e);
        }
    }

    /**
     * Gère le lock du schematic et l'envoi du bot (touche V en mode overlay)
     */
    private static void handleLockAndSendBot(MinecraftClient client) {
        if (!schematicManager.hasActiveSchematic()) {
            client.player.sendMessage(net.minecraft.text.Text.literal("§cErreur : Aucun schematic actif"));
            AIBuilderMod.LOGGER.warn("Attempted to lock without active schematic");
            return;
        }

        try {
            // 1. Locker le schematic à sa position actuelle
            schematicManager.lock();
            client.player.sendMessage(net.minecraft.text.Text.literal("§a✓ Schematic verrouillé à sa position actuelle"));

            BlockPos schematicPos = schematicManager.getPosition();
            AIBuilderMod.LOGGER.info("🔒 Schematic locked at ({}, {}, {})", schematicPos.getX(), schematicPos.getY(), schematicPos.getZ());

            // 2. Initialize WebSocket si pas déjà fait
            if (webSocketClient == null) {
                try {
                    webSocketClient = new ModWebSocketClient(java.net.URI.create(ModConfig.WEBSOCKET_SERVER_URL));
                    client.player.sendMessage(net.minecraft.text.Text.literal("§eConnexion au serveur bot..."));
                } catch (Exception e) {
                    AIBuilderMod.LOGGER.error("❌ Failed to create WebSocket client: {}", e.getMessage());
                    client.player.sendMessage(net.minecraft.text.Text.literal("§cErreur: Impossible de connecter au bot"));
                    return;
                }
            }

            // 3. Envoyer la commande au bot pour qu'il rejoigne la position
            webSocketClient.sendBotMoveToSchematic(
                schematicManager.getActiveSchematic(),
                schematicPos
            );

            client.player.sendMessage(net.minecraft.text.Text.literal("§b🤖 Bot en route vers la position du schematic..."));
            client.player.sendMessage(net.minecraft.text.Text.literal(String.format("§ePosition cible: §dX=%d, Y=%d, Z=%d",
                schematicPos.getX(), schematicPos.getY(), schematicPos.getZ())));

            AIBuilderMod.LOGGER.info("🤖 Bot command sent to move to schematic position ({}, {}, {})",
                schematicPos.getX(), schematicPos.getY(), schematicPos.getZ());

        } catch (Exception e) {
            client.player.sendMessage(net.minecraft.text.Text.literal("§cErreur : " + e.getMessage()));
            AIBuilderMod.LOGGER.error("Error locking schematic and sending bot", e);
        }
    }
}
