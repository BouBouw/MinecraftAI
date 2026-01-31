package com.mcaibuilder.gui;

import com.mcaibuilder.bot.BotManager;
import com.mcaibuilder.network.ModWebSocketClient;
import com.mcaibuilder.mod.AIBuilderClient;
import net.minecraft.client.MinecraftClient;
import net.minecraft.client.gui.DrawContext;
import net.minecraft.client.gui.screen.Screen;
import net.minecraft.client.gui.widget.ButtonWidget;
import net.minecraft.entity.player.PlayerEntity;
import net.minecraft.text.Text;
import net.minecraft.util.Formatting;

import java.util.Map;

/**
 * GUI for controlling AI bots
 * Shows bot status, progress, and provides control buttons
 */
public class BotControlScreen extends Screen {

    private final PlayerEntity botPlayer;
    private final BotManager.BotInfo botInfo;
    private final MinecraftClient client;

    // Buttons
    private static final int BUTTON_WIDTH = 200;
    private static final int BUTTON_HEIGHT = 20;
    private static final int BUTTON_SPACING = 5;

    // Speed values
    private static final float[] SPEED_VALUES = {0.5f, 1.0f, 1.5f, 2.0f, 3.0f};

    public BotControlScreen(PlayerEntity botPlayer, BotManager.BotInfo botInfo) {
        super(Text.literal("Bot Control"));
        this.botPlayer = botPlayer;
        this.botInfo = botInfo;
        this.client = MinecraftClient.getInstance();
    }

    @Override
    protected void init() {
        super.init();

        int centerX = this.width / 2;
        int startY = 80;

        // Find current speed index
        int currentSpeedIndex = 0;
        for (int i = 0; i < SPEED_VALUES.length; i++) {
            if (SPEED_VALUES[i] == botInfo.getSpeed()) {
                currentSpeedIndex = i;
                break;
            }
        }

        // Pause/Resume button
        addDrawableChild(ButtonWidget.builder(Text.literal(botInfo.getStatus() == BotManager.BotStatus.PAUSED ? "▶ Reprendre" : "⏸ Pauser"), button -> {
            togglePause();
        }).dimensions(centerX - BUTTON_WIDTH / 2, startY, BUTTON_WIDTH, BUTTON_HEIGHT).build());

        // Stop button
        addDrawableChild(ButtonWidget.builder(Text.literal("⏹ Arrêter").formatted(Formatting.RED), button -> {
            stopBuild();
        }).dimensions(centerX - BUTTON_WIDTH / 2, startY + (BUTTON_HEIGHT + BUTTON_SPACING) * 1, BUTTON_WIDTH, BUTTON_HEIGHT).build());

        // Speed increase button
        final int speedIndex = currentSpeedIndex;
        addDrawableChild(ButtonWidget.builder(Text.literal("⚡ Vitesse: " + SPEED_VALUES[speedIndex] + "x"), button -> {
            cycleSpeed(speedIndex);
        }).dimensions(centerX - BUTTON_WIDTH / 2, startY + (BUTTON_HEIGHT + BUTTON_SPACING) * 2, BUTTON_WIDTH, BUTTON_HEIGHT).build());

        // Close button
        addDrawableChild(ButtonWidget.builder(Text.literal("Fermer"), button -> {
            close();
        }).dimensions(centerX - BUTTON_WIDTH / 2, startY + (BUTTON_HEIGHT + BUTTON_SPACING) * 4, BUTTON_WIDTH, BUTTON_HEIGHT).build());
    }

    private void togglePause() {
        ModWebSocketClient wsClient = AIBuilderClient.getWebSocketClient();
        if (wsClient != null) {
            // Update bot status locally first
            if (botInfo.getStatus() == BotManager.BotStatus.PAUSED) {
                botInfo.setStatus(BotManager.BotStatus.BUILDING);
                wsClient.sendBotCommand(botInfo.getUuid(), "resume");
            } else {
                botInfo.setStatus(BotManager.BotStatus.PAUSED);
                wsClient.sendBotCommand(botInfo.getUuid(), "pause");
            }
        }

        // Rebuild screen to update button text
        client.setScreen(new BotControlScreen(botPlayer, botInfo));
    }

    private void stopBuild() {
        ModWebSocketClient wsClient = AIBuilderClient.getWebSocketClient();
        if (wsClient != null) {
            wsClient.sendBotCommand(botInfo.getUuid(), "stop");
        }
        close();
    }

    private void cycleSpeed(int currentIndex) {
        int nextIndex = (currentIndex + 1) % SPEED_VALUES.length;
        float newSpeed = SPEED_VALUES[nextIndex];

        // Update bot info with new speed
        botInfo.setSpeed(newSpeed);

        ModWebSocketClient wsClient = AIBuilderClient.getWebSocketClient();
        if (wsClient != null) {
            wsClient.sendBotSpeed(botInfo.getUuid(), newSpeed);
        }

        // Rebuild screen to update button text
        client.setScreen(new BotControlScreen(botPlayer, botInfo));
    }

    @Override
    public void render(DrawContext context, int mouseX, int mouseY, float delta) {
        // Dark background
        context.fillGradient(0, 0, this.width, this.height, 0xC0101010, 0xD0101010);

        // Title
        int centerX = this.width / 2;
        context.drawCenteredTextWithShadow(
            this.textRenderer,
            Text.literal("🤖 Contrôle du Bot").formatted(Formatting.AQUA, Formatting.BOLD),
            centerX,
            30,
            0xFFFFFF
        );

        // Bot info
        String botName = botInfo.getName();
        String statusText = botInfo.getStatus().getDisplayName();
        Formatting statusColor = getStatusColor(botInfo.getStatus());

        context.drawCenteredTextWithShadow(
            this.textRenderer,
            Text.literal("Bot: ").formatted(Formatting.GRAY)
                .append(Text.literal(botName).formatted(Formatting.WHITE)),
            centerX,
            55,
            0xFFFFFF
        );

        context.drawCenteredTextWithShadow(
            this.textRenderer,
            Text.literal("Statut: ").formatted(Formatting.GRAY)
                .append(Text.literal(statusText).formatted(statusColor)),
            centerX,
            65,
            0xFFFFFF
        );

        // Progress bar
        if (botInfo.getTotal() > 0) {
            int barWidth = 200;
            int barHeight = 10;
            int barX = centerX - barWidth / 2;
            int barY = 200;

            // Background
            context.fill(barX, barY, barX + barWidth, barY + barHeight, 0xFF333333);

            // Progress
            int progressWidth = (int) (barWidth * botInfo.getProgressPercentage());
            context.fill(barX, barY, barX + progressWidth, barY + barHeight, 0xFF55FF55);

            // Text
            String progressText = String.format("%d / %d blocs (%.1f%%)",
                botInfo.getProgress(),
                botInfo.getTotal(),
                botInfo.getProgressPercentage() * 100
            );

            context.drawCenteredTextWithShadow(
                this.textRenderer,
                Text.literal(progressText).formatted(Formatting.WHITE),
                centerX,
                barY + 15,
                0xFFFFFF
            );
        }

        super.render(context, mouseX, mouseY, delta);
    }

    private Formatting getStatusColor(BotManager.BotStatus status) {
        return switch (status) {
            case IDLE -> Formatting.GRAY;
            case BUILDING -> Formatting.GREEN;
            case PAUSED -> Formatting.YELLOW;
            case MOVING -> Formatting.AQUA;
            case STOPPED -> Formatting.RED;
        };
    }

    @Override
    public boolean shouldPause() {
        return false;
    }

    @Override
    public boolean shouldCloseOnEsc() {
        return true;
    }
}
