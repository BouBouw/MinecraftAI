package com.mcaibuilder.network;

import com.mcaibuilder.mod.AIBuilderMod;
import com.mcaibuilder.schematic.SchematicData;
import net.minecraft.block.BlockState;
import net.minecraft.block.Blocks;
import net.minecraft.util.math.BlockPos;
import org.java_websocket.client.WebSocketClient;
import org.java_websocket.handshake.ServerHandshake;

import java.net.URI;
import java.util.HashMap;
import java.util.Map;

/**
 * WebSocket client for communication with AI coordinator server
 */
public class ModWebSocketClient extends WebSocketClient {

    private boolean connected = false;

    public ModWebSocketClient(URI serverUri) {
        super(serverUri);
        connect();
    }

    @Override
    public void onOpen(ServerHandshake handshakedata) {
        AIBuilderMod.LOGGER.info("WebSocket connection opened");
        this.connected = true;
    }

    @Override
    public void onMessage(String message) {
        AIBuilderMod.LOGGER.info("WebSocket message received: {}", message);
        // Handle incoming messages from server
        handleMessage(message);
    }

    @Override
    public void onClose(int code, String reason, boolean remote) {
        AIBuilderMod.LOGGER.info("WebSocket connection closed: {} - {}", code, reason);
        this.connected = false;
    }

    @Override
    public void onError(Exception ex) {
        AIBuilderMod.LOGGER.error("WebSocket error", ex);
    }

    /**
     * Send schematic validation to server
     */
    public void sendSchematicValidation(SchematicData schematic, BlockPos position) {
        // Auto-reconnect if disconnected
        if (!connected) {
            AIBuilderMod.LOGGER.warn("Validation: Not connected, reconnecting...");
            ensureConnected();
            // Wait a bit for connection
            try {
                Thread.sleep(500);
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        }

        if (!connected) {
            AIBuilderMod.LOGGER.warn("Cannot send validation: still not connected to server after retry");
            return;
        }

        try {
            Map<String, Object> data = new HashMap<>();
            data.put("type", "schematic_validation");
            data.put("name", schematic.getName());
            data.put("position", Map.of(
                "x", position.getX(),
                "y", position.getY(),
                "z", position.getZ()
            ));
            data.put("dimensions", Map.of(
                "width", schematic.getWidth(),
                "height", schematic.getHeight(),
                "length", schematic.getLength()
            ));

            // Add block data
            Map<String, Integer> materials = new HashMap<>();
            for (BlockState block : schematic.getBlocks()) {
                if (block != null && block != Blocks.AIR.getDefaultState()) {
                    String blockId = block.getBlock().getTranslationKey();
                    materials.put(blockId, materials.getOrDefault(blockId, 0) + 1);
                }
            }
            data.put("materials", materials);

            // Convert to JSON and send
            String json = toJson(data);
            send(json);

            AIBuilderMod.LOGGER.info("Schematic validation sent to server");
        } catch (Exception e) {
            AIBuilderMod.LOGGER.error("Failed to send schematic validation", e);
        }
    }

    /**
     * Ensure connection is active, reconnect if necessary
     */
    public void ensureConnected() {
        if (!connected && !isConnecting()) {
            AIBuilderMod.LOGGER.info("Reconnecting to AI Coordinator...");
            this.reconnect();
        }
    }

    private boolean isConnecting() {
        return !this.isClosed() && !connected;
    }

    /**
     * Send command to bot to move to schematic position
     */
    public void sendBotMoveToSchematic(SchematicData schematic, BlockPos position) {
        // Auto-reconnect if disconnected
        if (!connected) {
            AIBuilderMod.LOGGER.warn("Bot command: Not connected, reconnecting...");
            ensureConnected();
            // Wait a bit for connection
            try {
                Thread.sleep(500);
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        }

        if (!connected) {
            AIBuilderMod.LOGGER.warn("Cannot send bot command: still not connected to server after retry");
            return;
        }

        try {
            // Collect all non-air blocks with their data
            java.util.Map<String, Object> blocksData = new java.util.HashMap<>();
            java.util.List<java.util.Map<String, Object>> blocksList = new java.util.ArrayList<>();

            int totalBlocks = schematic.getWidth() * schematic.getHeight() * schematic.getLength();
            AIBuilderMod.LOGGER.info("Preparing to send schematic data: {}x{}x{} = {} total blocks",
                schematic.getWidth(), schematic.getHeight(), schematic.getLength(), totalBlocks);
            AIBuilderMod.LOGGER.info("Block array has {} elements", schematic.getBlocks().length);

            for (int y = 0; y < schematic.getHeight(); y++) {
                for (int z = 0; z < schematic.getLength(); z++) {
                    for (int x = 0; x < schematic.getWidth(); x++) {
                        var block = schematic.getBlockAt(x, y, z);
                        if (block != null && !block.isAir()) {
                            java.util.Map<String, Object> blockInfo = new java.util.HashMap<>();
                            blockInfo.put("x", x);
                            blockInfo.put("y", y);
                            blockInfo.put("z", z);

                            // Get block registry name
                            String blockId = net.minecraft.registry.Registries.BLOCK.getId(block.getBlock())
                                .toString();
                            blockInfo.put("name", blockId);

                            blocksList.add(blockInfo);
                        }
                    }
                }
            }

            AIBuilderMod.LOGGER.info("Collected {} non-air blocks to send", blocksList.size());

            blocksData.put("blocks", blocksList);

            Map<String, Object> data = new HashMap<>();
            data.put("type", "bot_move_to_schematic");
            data.put("schematic_name", schematic.getName());
            data.put("target_position", Map.of(
                "x", position.getX(),
                "y", position.getY(),
                "z", position.getZ()
            ));
            data.put("dimensions", Map.of(
                "width", schematic.getWidth(),
                "height", schematic.getHeight(),
                "length", schematic.getLength()
            ));
            data.put("blocks_data", blocksData);

            // Add player name as owner
            net.minecraft.client.MinecraftClient client = net.minecraft.client.MinecraftClient.getInstance();
            if (client.player != null) {
                data.put("owner_name", client.player.getName().getString());
            }

            String json = toJson(data);
            send(json);

            AIBuilderMod.LOGGER.info("Bot move command sent to server - Target: ({}, {}, {}) with {} blocks",
                position.getX(), position.getY(), position.getZ(), blocksList.size());
        } catch (Exception e) {
            AIBuilderMod.LOGGER.error("Failed to send bot move command", e);
        }
    }

    /**
     * Handle incoming message from server
     */
    private void handleMessage(String message) {
        try {
            // Simple JSON parsing to extract type
            if (message.contains("\"type\"")) {
                String type = extractJsonValue(message, "type");

                switch (type) {
                    case "welcome":
                        AIBuilderMod.LOGGER.info("Connected to AI Coordinator");
                        break;
                    case "bot_move_ack":
                        String status = extractJsonValue(message, "status");
                        String msg = extractJsonValue(message, "message");
                        AIBuilderMod.LOGGER.info("Bot status: {} - {}", status, msg);
                        // Afficher dans le chat si possible
                        notifyClient("§bBot: " + msg);
                        break;
                    case "bot_spawn":
                        String botName = extractJsonValue(message, "bot_name");
                        String botUuidStr = extractJsonValue(message, "bot_uuid");
                        String ownerName = extractJsonValue(message, "owner_name");
                        AIBuilderMod.LOGGER.info("Bot spawned: {} ({}) owned by {}", botName, botUuidStr, ownerName);

                        // Register bot in BotManager
                        try {
                            java.util.UUID botUuid;
                            // Handle fallback UUID format or empty UUID
                            if (botUuidStr == null || botUuidStr.isEmpty() || botUuidStr.endsWith("-fallback")) {
                                // Generate a consistent UUID from the username
                                botUuid = java.util.UUID.nameUUIDFromBytes(botName.getBytes());
                                AIBuilderMod.LOGGER.info("Using name-based UUID for bot: {}", botUuid);
                            } else {
                                botUuid = java.util.UUID.fromString(botUuidStr);
                            }
                            com.mcaibuilder.bot.BotManager.getInstance().registerBot(botName, botUuid, ownerName);
                            notifyClient("§a✓ Bot connecté: " + botName + " (Clic droit pour gérer)");
                        } catch (Exception e) {
                            AIBuilderMod.LOGGER.error("Failed to register bot", e);
                            // Try to register with name-based UUID as last resort
                            try {
                                java.util.UUID fallbackUuid = java.util.UUID.nameUUIDFromBytes(botName.getBytes());
                                com.mcaibuilder.bot.BotManager.getInstance().registerBot(botName, fallbackUuid, ownerName);
                                notifyClient("§a✓ Bot connecté: " + botName + " (Clic droit pour gérer)");
                            } catch (Exception e2) {
                                AIBuilderMod.LOGGER.error("Failed to register bot with fallback UUID", e2);
                            }
                        }
                        break;
                    case "bot_status":
                        String botStatus = extractJsonValue(message, "status");
                        String statusMsg = extractJsonValue(message, "message");
                        AIBuilderMod.LOGGER.info("Bot status update: {} - {}", botStatus, statusMsg);
                        notifyClient("§aBot " + botStatus + ": " + statusMsg);
                        break;
                    case "bot_error":
                        String errorMsg = extractJsonValue(message, "message");
                        AIBuilderMod.LOGGER.error("Bot error: {}", errorMsg);
                        notifyClient("§cBot Error: " + errorMsg);
                        break;
                    default:
                        AIBuilderMod.LOGGER.info("Received message from server: {}", message);
                }
            }
        } catch (Exception e) {
            AIBuilderMod.LOGGER.error("Failed to handle message", e);
        }
    }

    /**
     * Simple JSON value extractor
     */
    private String extractJsonValue(String json, String key) {
        String pattern = "\"" + key + "\"\\s*:\\s*\"([^\"]+)\"";
        java.util.regex.Pattern p = java.util.regex.Pattern.compile(pattern);
        java.util.regex.Matcher m = p.matcher(json);
        if (m.find()) {
            return m.group(1);
        }
        return "";
    }

    /**
     * Notify the client (player) with a message
     */
    private void notifyClient(String message) {
        // This will be called from the client side
        // The actual display will be handled by AIBuilderClient
        com.mcaibuilder.mod.AIBuilderClient.showNotification(message);
    }

    /**
     * Simple JSON converter (production would use a proper JSON library)
     */
    private String toJson(Map<String, Object> data) {
        StringBuilder sb = new StringBuilder("{");
        boolean first = true;

        for (Map.Entry<String, Object> entry : data.entrySet()) {
            if (!first) sb.append(",");
            first = false;

            sb.append("\"").append(entry.getKey()).append("\":");

            Object value = entry.getValue();
            if (value instanceof String) {
                sb.append("\"").append(value).append("\"");
            } else if (value instanceof Number) {
                sb.append(value);
            } else if (value instanceof Map) {
                sb.append(mapToJson((Map<?, ?>) value));
            } else if (value instanceof java.util.List) {
                sb.append(listToJson((java.util.List<?>) value));
            } else {
                sb.append("\"").append(value).append("\"");
            }
        }

        sb.append("}");
        return sb.toString();
    }

    private String mapToJson(Map<?, ?> map) {
        StringBuilder sb = new StringBuilder("{");
        boolean first = true;

        for (Map.Entry<?, ?> entry : map.entrySet()) {
            if (!first) sb.append(",");
            first = false;

            sb.append("\"").append(entry.getKey()).append("\":");

            Object value = entry.getValue();
            if (value instanceof String) {
                sb.append("\"").append(value).append("\"");
            } else if (value instanceof Number) {
                sb.append(value);
            } else if (value instanceof Map) {
                sb.append(mapToJson((Map<?, ?>) value));
            } else if (value instanceof java.util.List) {
                sb.append(listToJson((java.util.List<?>) value));
            } else {
                sb.append("\"").append(value).append("\"");
            }
        }

        sb.append("}");
        return sb.toString();
    }

    private String listToJson(java.util.List<?> list) {
        StringBuilder sb = new StringBuilder("[");
        boolean first = true;

        for (Object item : list) {
            if (!first) sb.append(",");
            first = false;

            if (item instanceof String) {
                sb.append("\"").append(item).append("\"");
            } else if (item instanceof Number) {
                sb.append(item);
            } else if (item instanceof Map) {
                sb.append(mapToJson((Map<?, ?>) item));
            } else if (item instanceof java.util.List) {
                sb.append(listToJson((java.util.List<?>) item));
            } else {
                sb.append("\"").append(item).append("\"");
            }
        }

        sb.append("]");
        return sb.toString();
    }

    public boolean isConnected() {
        return connected;
    }

    /**
     * Send a control command to a bot (pause, resume, stop)
     */
    public void sendBotCommand(java.util.UUID botUuid, String command) {
        if (!connected) {
            AIBuilderMod.LOGGER.warn("Cannot send bot command: not connected");
            return;
        }

        try {
            Map<String, Object> data = new HashMap<>();
            data.put("type", "bot_control");
            data.put("bot_uuid", botUuid.toString());
            data.put("command", command);

            String json = toJson(data);
            send(json);

            AIBuilderMod.LOGGER.info("Bot control command sent: {} -> {}", command, botUuid);
        } catch (Exception e) {
            AIBuilderMod.LOGGER.error("Failed to send bot control command", e);
        }
    }

    /**
     * Send speed multiplier to a bot
     */
    public void sendBotSpeed(java.util.UUID botUuid, float speed) {
        if (!connected) {
            AIBuilderMod.LOGGER.warn("Cannot send bot speed: not connected");
            return;
        }

        try {
            Map<String, Object> data = new HashMap<>();
            data.put("type", "bot_speed");
            data.put("bot_uuid", botUuid.toString());
            data.put("speed", speed);

            String json = toJson(data);
            send(json);

            AIBuilderMod.LOGGER.info("Bot speed sent: {}x -> {}", speed, botUuid);
        } catch (Exception e) {
            AIBuilderMod.LOGGER.error("Failed to send bot speed", e);
        }
    }
}
