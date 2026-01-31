package com.mcaibuilder.gui;

import com.mcaibuilder.mod.AIBuilderClient;
import com.mcaibuilder.renderer.SchematicRenderer;
import com.mcaibuilder.schematic.SchematicData;
import com.mcaibuilder.schematic.SchematicManager;
import net.minecraft.client.MinecraftClient;
import net.minecraft.client.font.TextRenderer;
import net.minecraft.client.gui.DrawContext;
import net.minecraft.text.Text;
import net.minecraft.util.Formatting;

/**
 * Système de messages visuels en jeu (overlay)
 * Affiche des notifications temporaires et les infos du schematic
 */
public class InGameMessenger {

    private static Message currentMessage = null;

    public static void show(MinecraftClient client, String message, int durationTicks) {
        show(client, Text.literal(message), durationTicks);
    }

    public static void show(MinecraftClient client, Text message, int durationTicks) {
        currentMessage = new Message(message, durationTicks);
    }

    public static void render(DrawContext context) {
        // Afficher le message temporaire s'il y en a un
        if (currentMessage != null) {
            currentMessage.render(context);

            if (currentMessage.isExpired()) {
                currentMessage = null;
            }
        }

        // Afficher les infos du schematic si l'overlay est activé
        renderSchematicInfo(context);
    }

    /**
     * Affiche les informations du schematic en haut à gauche de l'écran
     */
    private static void renderSchematicInfo(DrawContext context) {
        try {
            SchematicRenderer schematicRenderer = AIBuilderClient.getSchematicRenderer();
            SchematicManager schematicManager = AIBuilderClient.getSchematicManager();

            if (schematicRenderer == null || !schematicRenderer.isOverlayEnabled()) {
                return;
            }

            if (schematicManager == null || !schematicManager.hasActiveSchematic()) {
                return;
            }

            SchematicData schematic = schematicManager.getActiveSchematic();
            MinecraftClient client = MinecraftClient.getInstance();
            TextRenderer textRenderer = client.textRenderer;

            int x = 10;
            int y = 10;
            int lineHeight = 12;

            // Fond semi-transparent pour la lisibilité
            int boxWidth = 200;
            int boxHeight = 60;
            context.fill(x - 4, y - 4, x + boxWidth, y + boxHeight, 0x80000000);

            // Titre
            context.drawText(textRenderer,
                Text.literal("Schematic: ").formatted(Formatting.AQUA)
                    .append(Text.literal(schematic.getName()).formatted(Formatting.WHITE)),
                x, y, 0xFFFFFF, true);
            y += lineHeight + 4;

            // Dimensions
            context.drawText(textRenderer,
                Text.literal(String.format("Size: %dx%dx%d",
                    schematic.getWidth(), schematic.getHeight(), schematic.getLength()))
                    .formatted(Formatting.GRAY),
                x, y, 0xFFFFFF, true);
            y += lineHeight + 4;

            // Position
            context.drawText(textRenderer,
                Text.literal(String.format("Pos: %d, %d, %d",
                    schematic.getOrigin().getX(),
                    schematic.getOrigin().getY(),
                    schematic.getOrigin().getZ()))
                    .formatted(Formatting.YELLOW),
                x, y, 0xFFFFFF, true);
            y += lineHeight + 4;

            // Nombre de blocs
            context.drawText(textRenderer,
                Text.literal(String.format("Blocks: %d", schematic.getTotalBlocks()))
                    .formatted(Formatting.GREEN),
                x, y, 0xFFFFFF, true);

        } catch (Exception e) {
            // Ignorer les erreurs de rendu
        }
    }

    public static void showSuccess(MinecraftClient client, String message) {
        show(client, Text.literal(message).formatted(Formatting.GREEN), 100);
    }

    public static void showError(MinecraftClient client, String message) {
        show(client, Text.literal(message).formatted(Formatting.RED), 150);
    }

    public static void showInfo(MinecraftClient client, String message) {
        show(client, Text.literal(message).formatted(Formatting.YELLOW), 100);
    }

    public static void showToggle(MinecraftClient client, boolean enabled) {
        if (enabled) {
            show(client, Text.literal("✓ Overlay Activé").formatted(Formatting.GREEN), 60);
        } else {
            show(client, Text.literal("✗ Overlay Désactivé").formatted(Formatting.RED), 60);
        }
    }

    private static class Message {
        private final Text text;
        private final int durationTicks;
        private int timer;

        Message(Text text, int durationTicks) {
            this.text = text;
            this.durationTicks = durationTicks;
            this.timer = 0;
        }

        void render(DrawContext context) {
            timer++;

            // Effet de fade in/out
            float opacity = 1.0f;
            if (timer < 10) {
                opacity = timer / 10.0f;
            } else if (timer > durationTicks - 10) {
                opacity = (durationTicks - timer) / 10.0f;
            }

            if (opacity <= 0) {
                return;
            }

            MinecraftClient client = MinecraftClient.getInstance();
            TextRenderer textRenderer = client.textRenderer;
            int screenWidth = client.getWindow().getScaledWidth();
            int screenHeight = client.getWindow().getScaledHeight();

            int messageWidth = textRenderer.getWidth(text);
            int x = (screenWidth - messageWidth) / 2;
            int y = screenHeight / 4;

            // Fond semi-transparent
            int padding = 6;
            int boxWidth = messageWidth + padding * 2;
            int boxHeight = 20;

            context.fill(x - padding, y - padding, x - padding + boxWidth, y - padding + boxHeight,
                0x80000000 | ((int)(opacity * 255) << 24));

            // Texte
            context.drawText(textRenderer, text, x, y, 0xFFFFFF, true);
        }

        boolean isExpired() {
            return timer >= durationTicks;
        }
    }
}
