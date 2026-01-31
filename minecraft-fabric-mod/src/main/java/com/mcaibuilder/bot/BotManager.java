package com.mcaibuilder.bot;

import com.mcaibuilder.mod.AIBuilderMod;
import net.minecraft.client.MinecraftClient;
import net.minecraft.entity.player.PlayerEntity;
import net.minecraft.util.Formatting;

import java.util.HashMap;
import java.util.Map;
import java.util.UUID;

/**
 * Manages AI bots connected to the coordinator
 * Tracks bot status, owner, and provides control interface
 */
public class BotManager {

    private static BotManager instance;

    private final Map<UUID, BotInfo> bots = new HashMap<>();
    private final Map<String, BotInfo> botsByName = new HashMap<>();

    public static BotManager getInstance() {
        if (instance == null) {
            instance = new BotManager();
        }
        return instance;
    }

    /**
     * Register a bot when it connects
     */
    public void registerBot(String botName, UUID botUuid, String ownerName) {
        BotInfo botInfo = new BotInfo(botName, botUuid, ownerName);
        bots.put(botUuid, botInfo);
        botsByName.put(botName, botInfo);

        AIBuilderMod.LOGGER.info("🤖 Bot registered: {} ({}) owned by {}", botName, botUuid, ownerName);

        // Notify player
        MinecraftClient client = MinecraftClient.getInstance();
        if (client.player != null) {
            client.player.sendMessage(
                net.minecraft.text.Text.literal("")
                    .append(net.minecraft.text.Text.literal("🤖 ").formatted(Formatting.AQUA))
                    .append(net.minecraft.text.Text.literal("Bot connecté: ").formatted(Formatting.GREEN))
                    .append(net.minecraft.text.Text.literal(botName).formatted(Formatting.WHITE))
                    .append(net.minecraft.text.Text.literal(" (Clic droit pour gérer)").formatted(Formatting.GRAY))
            );
        }
    }

    /**
     * Unregister a bot when it disconnects
     */
    public void unregisterBot(UUID botUuid) {
        BotInfo removed = bots.remove(botUuid);
        if (removed != null) {
            botsByName.remove(removed.getName());
            AIBuilderMod.LOGGER.info("🤖 Bot unregistered: {}", removed.getName());

            MinecraftClient client = MinecraftClient.getInstance();
            if (client.player != null) {
                client.player.sendMessage(
                    net.minecraft.text.Text.literal("")
                        .append(net.minecraft.text.Text.literal("🤖 ").formatted(Formatting.RED))
                        .append(net.minecraft.text.Text.literal("Bot déconnecté: ").formatted(Formatting.RED))
                        .append(net.minecraft.text.Text.literal(removed.getName()).formatted(Formatting.WHITE))
                );
            }
        }
    }

    /**
     * Unregister a bot by name
     */
    public void unregisterBotByName(String botName) {
        BotInfo removed = botsByName.remove(botName);
        if (removed != null) {
            bots.remove(removed.getUuid());
            AIBuilderMod.LOGGER.info("🤖 Bot unregistered by name: {}", removed.getName());

            MinecraftClient client = MinecraftClient.getInstance();
            if (client.player != null) {
                client.player.sendMessage(
                    net.minecraft.text.Text.literal("")
                        .append(net.minecraft.text.Text.literal("🤖 ").formatted(Formatting.RED))
                        .append(net.minecraft.text.Text.literal("Bot déconnecté: ").formatted(Formatting.RED))
                        .append(net.minecraft.text.Text.literal(removed.getName()).formatted(Formatting.WHITE))
                );
            }
        }
    }

    /**
     * Get bot info by UUID
     */
    public BotInfo getBot(UUID uuid) {
        return bots.get(uuid);
    }

    /**
     * Get bot info by name
     */
    public BotInfo getBotByName(String name) {
        return botsByName.get(name);
    }

    /**
     * Get bot info by player entity (checks UUID first, then name)
     */
    public BotInfo getBot(PlayerEntity player) {
        // Try UUID first
        BotInfo bot = getBot(player.getUuid());
        if (bot != null) return bot;

        // Fallback to name lookup
        return getBotByName(player.getName().getString());
    }

    /**
     * Check if a player is a bot (checks UUID first, then name)
     */
    public boolean isBot(PlayerEntity player) {
        // Try UUID first
        if (bots.containsKey(player.getUuid())) return true;

        // Fallback to name lookup
        return botsByName.containsKey(player.getName().getString());
    }

    /**
     * Check if a player is a bot owned by the current player
     */
    public boolean isMyBot(PlayerEntity player) {
        BotInfo bot = getBot(player);
        if (bot == null) return false;

        MinecraftClient client = MinecraftClient.getInstance();
        return client.player != null && bot.getOwnerName().equals(client.player.getName().getString());
    }

    /**
     * Get all registered bots
     */
    public Map<UUID, BotInfo> getAllBots() {
        return new HashMap<>(bots);
    }

    /**
     * Update bot status
     */
    public void updateBotStatus(UUID botUuid, BotStatus status, int progress, int total) {
        BotInfo bot = bots.get(botUuid);
        if (bot != null) {
            bot.setStatus(status);
            bot.setProgress(progress);
            bot.setTotal(total);
        }
    }

    /**
     * Bot information class
     */
    public static class BotInfo {
        private final String name;
        private final UUID uuid;
        private final String ownerName;
        private BotStatus status = BotStatus.IDLE;
        private int progress;
        private int total;
        private float speed = 1.0f;

        public BotInfo(String name, UUID uuid, String ownerName) {
            this.name = name;
            this.uuid = uuid;
            this.ownerName = ownerName;
        }

        public String getName() { return name; }
        public UUID getUuid() { return uuid; }
        public String getOwnerName() { return ownerName; }
        public BotStatus getStatus() { return status; }
        public int getProgress() { return progress; }
        public int getTotal() { return total; }
        public float getSpeed() { return speed; }

        public void setStatus(BotStatus status) { this.status = status; }
        public void setProgress(int progress) { this.progress = progress; }
        public void setTotal(int total) { this.total = total; }
        public void setSpeed(float speed) { this.speed = speed; }

        public float getProgressPercentage() {
            return total > 0 ? (float) progress / total : 0;
        }
    }

    /**
     * Bot status enum
     */
    public enum BotStatus {
        IDLE("En attente"),
        BUILDING("Construction"),
        PAUSED("En pause"),
        MOVING("Déplacement"),
        STOPPED("Arrêté");

        private final String displayName;

        BotStatus(String displayName) {
            this.displayName = displayName;
        }

        public String getDisplayName() {
            return displayName;
        }
    }
}
