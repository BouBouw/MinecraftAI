package com.mcaibuilder.config;

/**
 * Configuration constants for AI Builder Mod
 */
public class ModConfig {

    // WebSocket server configuration
    public static final String WEBSOCKET_SERVER_URL = "ws://localhost:8080";

    // Default schematic path
    public static final String DEFAULT_SCHEMATIC_PATH = "./schematics";

    // Rendering configuration
    public static final int RENDER_DISTANCE = 64; // blocks
    public static final float OVERLAY_OPACITY = 0.3f;

    // Movement configuration
    public static final int MOVE_STEP = 1; // blocks
    public static final int ROTATION_STEP = 90; // degrees

    // Colors for rendering
    public static final int OVERLAY_COLOR = 0x80FFFFFF; // ARGB format
    public static final int ERROR_COLOR = 0x80FF0000;   // Red for errors
    public static final int SUCCESS_COLOR = 0x8000FF00; // Green for success
}
