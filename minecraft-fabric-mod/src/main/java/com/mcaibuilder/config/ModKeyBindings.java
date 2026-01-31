package com.mcaibuilder.config;

import net.fabricmc.fabric.api.client.keybinding.v1.KeyBindingHelper;
import net.minecraft.client.option.KeyBinding;
import org.lwjgl.glfw.GLFW;

/**
 * Gestionnaire des keybinds du mod
 * Enregistre les raccourcis clavier et les rend configurables dans le menu des contrôles
 */
public class ModKeyBindings {

    // KeyBindings principaux
    public static KeyBinding TOGGLE_OVERLAY;
    public static KeyBinding MOVE_UP;
    public static KeyBinding MOVE_DOWN;
    public static KeyBinding MOVE_LEFT;
    public static KeyBinding MOVE_RIGHT;
    public static KeyBinding MOVE_FORWARD;
    public static KeyBinding MOVE_BACKWARD;
    public static KeyBinding VALIDATE_SCHEMATIC;
    public static KeyBinding SAVE_SELECTION;

    /**
     * Enregistre tous les keybinds
     */
    public static void register() {
        // Toggle l'overlay (R par défaut)
        TOGGLE_OVERLAY = KeyBindingHelper.registerKeyBinding(new KeyBinding(
            "key.ai-builder.toggle_overlay",
            GLFW.GLFW_KEY_R,
            "key.categories.ai-builder"
        ));

        // Déplacer vers le haut (Left Shift par défaut)
        MOVE_UP = KeyBindingHelper.registerKeyBinding(new KeyBinding(
            "key.ai-builder.move_up",
            GLFW.GLFW_KEY_LEFT_SHIFT,
            "key.categories.ai-builder"
        ));

        // Déplacer vers le bas (Left Control par défaut)
        MOVE_DOWN = KeyBindingHelper.registerKeyBinding(new KeyBinding(
            "key.ai-builder.move_down",
            GLFW.GLFW_KEY_LEFT_CONTROL,
            "key.categories.ai-builder"
        ));

        // Déplacer à gauche (Left Arrow par défaut)
        MOVE_LEFT = KeyBindingHelper.registerKeyBinding(new KeyBinding(
            "key.ai-builder.move_left",
            GLFW.GLFW_KEY_LEFT,
            "key.categories.ai-builder"
        ));

        // Déplacer à droite (Right Arrow par défaut)
        MOVE_RIGHT = KeyBindingHelper.registerKeyBinding(new KeyBinding(
            "key.ai-builder.move_right",
            GLFW.GLFW_KEY_RIGHT,
            "key.categories.ai-builder"
        ));

        // Déplacer en avant (Up Arrow par défaut)
        MOVE_FORWARD = KeyBindingHelper.registerKeyBinding(new KeyBinding(
            "key.ai-builder.move_forward",
            GLFW.GLFW_KEY_UP,
            "key.categories.ai-builder"
        ));

        // Déplacer en arrière (Down Arrow par défaut)
        MOVE_BACKWARD = KeyBindingHelper.registerKeyBinding(new KeyBinding(
            "key.ai-builder.move_backward",
            GLFW.GLFW_KEY_DOWN,
            "key.categories.ai-builder"
        ));

        // Valider le schematic (Enter par défaut)
        VALIDATE_SCHEMATIC = KeyBindingHelper.registerKeyBinding(new KeyBinding(
            "key.ai-builder.validate_schematic",
            GLFW.GLFW_KEY_ENTER,
            "key.categories.ai-builder"
        ));

        // Sauvegarder la sélection (V par défaut)
        SAVE_SELECTION = KeyBindingHelper.registerKeyBinding(new KeyBinding(
            "key.ai-builder.save_selection",
            GLFW.GLFW_KEY_V,
            "key.categories.ai-builder"
        ));
    }
}
