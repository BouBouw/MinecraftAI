package com.mcaibuilder.mod;

import net.fabricmc.api.ModInitializer;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/**
 * Main mod class for AI Builder
 * This mod allows visualization and validation of Minecraft schematics for AI building
 */
public class AIBuilderMod implements ModInitializer {
    public static final String MOD_ID = "ai-builder-mod";
    public static final Logger LOGGER = LoggerFactory.getLogger(MOD_ID);

	@Override
	public void onInitialize() {
		LOGGER.info("AI Builder Mod initialized - Ready to build!");
	}
}
