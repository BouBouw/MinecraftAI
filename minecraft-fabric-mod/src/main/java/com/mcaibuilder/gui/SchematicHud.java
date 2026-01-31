package com.mcaibuilder.gui;

import com.mcaibuilder.mod.AIBuilderMod;
import com.mcaibuilder.schematic.SchematicData;
import com.mcaibuilder.schematic.SchematicManager;
import net.minecraft.client.MinecraftClient;
import net.minecraft.client.font.TextRenderer;
import net.minecraft.client.gui.DrawContext;
import net.minecraft.text.Text;
import net.minecraft.util.Formatting;

/**
 * HUD overlay pour afficher les informations du schematic
 */
public class SchematicHud {

    private static boolean enabled = true;

    public static void setEnabled(boolean enabled) {
        SchematicHud.enabled = enabled;
    }

    public static boolean isEnabled() {
        return enabled;
    }

    /**
     * Rend le HUD avec les informations du schematic
     */
    public static void render(DrawContext context, MinecraftClient client) {
        if (!enabled || client.player == null) {
            return;
        }

        SchematicManager manager = com.mcaibuilder.mod.AIBuilderClient.getSchematicManager();
        if (manager == null || !manager.hasActiveSchematic()) {
            return;
        }

        SchematicData schematic = manager.getActiveSchematic();
        TextRenderer textRenderer = client.textRenderer;

        int x = 10;
        int y = 10;
        int lineHeight = 12;

        // Fond semi-transparent
        int boxWidth = 200;
        int boxHeight = 80;
        context.fill(x, y, x + boxWidth, y + boxHeight, 0x80000000);

        // Titre
        context.drawText(textRenderer, Text.literal("AI Builder Schematic")
            .formatted(Formatting.BOLD, Formatting.GOLD), x + 5, y + 5, 0xFFFFFF, true);

        // Position
        String posText = String.format("Pos: %d, %d, %d",
            schematic.getOrigin().getX(),
            schematic.getOrigin().getY(),
            schematic.getOrigin().getZ());
        context.drawText(textRenderer, Text.literal(posText), x + 5, y + 20, 0xAAAAAA, true);

        // Dimensions
        String dimText = String.format("Size: %dx%dx%d (%d blocks)",
            schematic.getWidth(),
            schematic.getHeight(),
            schematic.getLength(),
            schematic.getWidth() * schematic.getHeight() * schematic.getLength());
        context.drawText(textRenderer, Text.literal(dimText), x + 5, y + 35, 0xAAAAAA, true);

        // Instructions
        context.drawText(textRenderer, Text.literal("R: Toggle | SHIFT/CTRL: Move")
            .formatted(Formatting.GRAY), x + 5, y + 55, 0x888888, true);
        context.drawText(textRenderer, Text.literal("ENTER: Validate to bot")
            .formatted(Formatting.GRAY), x + 5, y + 67, 0x888888, true);
    }
}
