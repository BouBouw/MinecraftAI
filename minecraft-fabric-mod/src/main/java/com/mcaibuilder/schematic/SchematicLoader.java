package com.mcaibuilder.schematic;

import net.minecraft.block.BlockState;
import net.minecraft.block.Blocks;
import net.minecraft.nbt.NbtCompound;
import net.minecraft.nbt.NbtElement;
import net.minecraft.nbt.NbtHelper;
import net.minecraft.nbt.NbtList;
import net.minecraft.nbt.NbtIo;
import net.minecraft.nbt.NbtSizeTracker;

import com.mcaibuilder.mod.AIBuilderMod;

import java.io.File;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.HashMap;
import java.util.Map;

/**
 * Loader for multiple schematic formats:
 * - .schem (Sponge Schematic format)
 * - .litematic (LiteLoader Schematic format)
 * - .nbt (Raw NBT format)
 */
public class SchematicLoader {

    /**
     * Load a schematic from file (auto-detect format by extension)
     */
    public SchematicData loadSchematic(File file) {
        String fileName = file.getName().toLowerCase();
        AIBuilderMod.LOGGER.info("Loading schematic file: {}", fileName);

        try {
            if (fileName.endsWith(".schem")) {
                return loadSpongeSchematic(file);
            } else if (fileName.endsWith(".litematic")) {
                return loadLitematicSchematic(file);
            } else if (fileName.endsWith(".nbt")) {
                return loadNBTSchematic(file);
            } else {
                AIBuilderMod.LOGGER.error("Unknown schematic format: {}", fileName);
                return null;
            }
        } catch (Exception e) {
            AIBuilderMod.LOGGER.error("Failed to load schematic: {}", file.getName(), e);
            return null;
        }
    }

    /**
     * Load Sponge Schematic format (.schem)
     */
    private SchematicData loadSpongeSchematic(File file) throws IOException {
        Path path = file.toPath();
        NbtCompound nbt = NbtIo.readCompressed(path, NbtSizeTracker.ofUnlimitedBytes());

        // Check version
        int version = nbt.getInt("Version");
        if (version != 2 && version != 3) {
            AIBuilderMod.LOGGER.error("Unsupported schematic version: {}", version);
            return null;
        }

        // Read dimensions
        int width = nbt.getInt("Width");
        int height = nbt.getInt("Height");
        int length = nbt.getInt("Length");

        AIBuilderMod.LOGGER.info("Loading Sponge schematic: {}x{}x{}", width, height, length);

        // Read palette (block mappings)
        Map<Integer, String> palette = new HashMap<>();
        NbtCompound paletteData = nbt.getCompound("Palette");
        for (String key : paletteData.getKeys()) {
            int id = paletteData.getInt(key);
            palette.put(id, key);
        }

        // Read block data (direct byte array in Sponge Schematic v2)
        byte[] data = nbt.getByteArray("BlockData");

        // Parse blocks
        int expectedSize = width * height * length;
        BlockState[] blocks = parseBlocks(data, palette, expectedSize);

        AIBuilderMod.LOGGER.info("Loaded Sponge schematic {}x{}x{} with {} blocks", width, height, length, blocks.length);

        return new SchematicData(
            file.getName(),
            width,
            height,
            length,
            blocks,
            new net.minecraft.util.math.BlockPos(0, 0, 0)
        );
    }

    /**
     * Load Litematic format (.litematic)
     */
    private SchematicData loadLitematicSchematic(File file) throws IOException {
        Path path = file.toPath();
        NbtCompound nbt = NbtIo.readCompressed(path, NbtSizeTracker.ofUnlimitedBytes());

        // Litematic format structure
        NbtCompound nbtData = nbt.getCompound("EmbeddedModule"); // In litematic, data is in "EmbeddedModule" or directly in root
        if (nbtData == null || nbtData.isEmpty()) {
            nbtData = nbt;
        }

        // Read regions
        NbtCompound regions = nbtData.getCompound("Regions");
        if (regions == null || regions.isEmpty()) {
            AIBuilderMod.LOGGER.error("No regions found in litematic file");
            return null;
        }

        // For simplicity, we'll only load the first region
        String firstRegion = regions.getKeys().iterator().next();
        NbtCompound region = regions.getCompound(firstRegion);

        // Read dimensions
        NbtCompound size = region.getCompound("Size");
        int width = size.getInt("x");
        int height = size.getInt("y");
        int length = size.getInt("z");

        AIBuilderMod.LOGGER.info("Loading Litematic schematic region '{}': {}x{}x{}", firstRegion, width, height, length);

        // Read position
        net.minecraft.util.math.BlockPos position = net.minecraft.util.math.BlockPos.ORIGIN;
        if (region.contains("Position")) {
            NbtCompound pos = region.getCompound("Position");
            position = new net.minecraft.util.math.BlockPos(pos.getInt("x"), pos.getInt("y"), pos.getInt("z"));
        }

        // Get block state palette
        NbtList paletteList = region.getList("BlockStatePalette", NbtElement.COMPOUND_TYPE);
        Map<Integer, String> palette = new HashMap<>();
        for (int i = 0; i < paletteList.size(); i++) {
            NbtCompound blockState = paletteList.getCompound(i);
            String blockName = blockState.getString("Name");
            palette.put(i, blockName);
        }

        // Read block data
        NbtCompound blockStates = region.getCompound("BlockStates");
        long[] longArray = blockStates.getLongArray("Data"); // Data is stored in "Data" tag
        int bitsPerBlock = region.getInt("BitsPerBlock");

        BlockState[] blocks = parseLitematicBlocks(longArray, palette, width, height, length, bitsPerBlock);

        AIBuilderMod.LOGGER.info("Loaded Litematic schematic {}x{}x{} with {} blocks", width, height, length, blocks.length);

        return new SchematicData(
            file.getName(),
            width,
            height,
            length,
            blocks,
            position
        );
    }

    /**
     * Load NBT format (.nbt)
     * Raw NBT files containing schematic data
     */
    private SchematicData loadNBTSchematic(File file) throws IOException {
        AIBuilderMod.LOGGER.info("Loading .nbt schematic (raw NBT format)");

        Path path = file.toPath();
        NbtCompound nbt = NbtIo.readCompressed(path, NbtSizeTracker.ofUnlimitedBytes());

        // Debug: Log NBT structure
        AIBuilderMod.LOGGER.info("NBT root keys: {}", nbt.getKeys());
        for (String key : nbt.getKeys()) {
            // Log the type of each tag
            if (nbt.contains(key, NbtElement.COMPOUND_TYPE)) {
                AIBuilderMod.LOGGER.info("  - {}: COMPOUND", key);
            } else if (nbt.contains(key, NbtElement.INT_TYPE)) {
                AIBuilderMod.LOGGER.info("  - {}: INT = {}", key, nbt.getInt(key));
            } else if (nbt.contains(key, NbtElement.LIST_TYPE)) {
                AIBuilderMod.LOGGER.info("  - {}: LIST", key);
            } else {
                AIBuilderMod.LOGGER.info("  - {}: {}", key, nbt.get(key).getClass().getSimpleName());
            }
        }

        // NBT files can have different structures, try to detect format
        // Check if it matches Sponge Schematic format
        if (nbt.contains("Version") && nbt.contains("Width") && nbt.contains("Height") && nbt.contains("Length")) {
            AIBuilderMod.LOGGER.info("NBT file matches Sponge Schematic format");
            return loadSpongeSchematic(file);
        }

        // Check if it matches Litematic format
        if (nbt.contains("EmbeddedModule") || nbt.contains("Regions")) {
            AIBuilderMod.LOGGER.info("NBT file matches Litematic format");
            return loadLitematicSchematic(file);
        }

        // Try generic NBT structure
        if (nbt.contains("Blocks") || nbt.contains("Data") || nbt.contains("Entities") || nbt.contains("size")) {
            return loadGenericNBTSchematic(nbt, file.getName());
        }

        AIBuilderMod.LOGGER.error("Unknown NBT schematic structure in file: {}", file.getName());
        AIBuilderMod.LOGGER.error("Available keys: {}", nbt.getKeys());
        return null;
    }

    /**
     * Load generic NBT schematic
     * Attempts to read common NBT schematic structures
     */
    private SchematicData loadGenericNBTSchematic(NbtCompound nbt, String fileName) {
        AIBuilderMod.LOGGER.info("Loading generic NBT schematic");

        // Try to extract dimensions and blocks from common formats
        int width = 0, height = 0, length = 0;

        // Try different dimension naming conventions
        if (nbt.contains("Width") && nbt.contains("Height") && nbt.contains("Length")) {
            width = nbt.getInt("Width");
            height = nbt.getInt("Height");
            length = nbt.getInt("Length");
        } else if (nbt.contains("size", NbtElement.LIST_TYPE)) {
            // Cobblemon format: size is a LIST of 3 integers [x, y, z]
            AIBuilderMod.LOGGER.info("Found 'size' as LIST type (Cobblemon format)");
            NbtList sizeList = nbt.getList("size", NbtElement.INT_TYPE);
            AIBuilderMod.LOGGER.info("Size list has {} elements", sizeList.size());
            if (sizeList.size() >= 3) {
                width = sizeList.getInt(0);
                height = sizeList.getInt(1);
                length = sizeList.getInt(2);
                AIBuilderMod.LOGGER.info("Found dimensions in 'size' list: {}x{}x{}", width, height, length);
            }
        } else if (nbt.contains("size")) {
            // Try lowercase 'size' tag (NBTCompound)
            NbtCompound sizeTag = nbt.getCompound("size");
            AIBuilderMod.LOGGER.info("Size tag keys: {}", sizeTag.getKeys());
            AIBuilderMod.LOGGER.info("Size tag isEmpty: {}", sizeTag.isEmpty());
            for (String key : sizeTag.getKeys()) {
                AIBuilderMod.LOGGER.info("  - {}: {}", key, sizeTag.get(key).getClass().getSimpleName());
            }
            if (!sizeTag.isEmpty()) {
                width = sizeTag.getInt("x");
                height = sizeTag.getInt("y");
                length = sizeTag.getInt("z");
                AIBuilderMod.LOGGER.info("Found dimensions in 'size' tag: {}x{}x{}", width, height, length);
            }
        } else if (nbt.contains("x") && nbt.contains("y") && nbt.contains("z")) {
            NbtCompound size = nbt.getCompound("size");
            if (!size.isEmpty()) {
                width = size.getInt("x");
                height = size.getInt("y");
                length = size.getInt("z");
            } else {
                width = nbt.getInt("x");
                height = nbt.getInt("y");
                length = nbt.getInt("z");
            }
        } else if (nbt.contains("X") && nbt.contains("Y") && nbt.contains("Z")) {
            width = nbt.getInt("X");
            height = nbt.getInt("Y");
            length = nbt.getInt("Z");
        }

        if (width <= 0 || height <= 0 || length <= 0) {
            AIBuilderMod.LOGGER.error("Invalid dimensions in NBT file: {}x{}x{}", width, height, length);
            return null;
        }

        AIBuilderMod.LOGGER.info("NBT schematic dimensions: {}x{}x{}", width, height, length);

        // Try to read block data
        BlockState[] blocks;

        // Try Sponge-style BlockData (with capitalized or lowercase names)
        if ((nbt.contains("BlockData") || nbt.contains("blockdata")) && (nbt.contains("Palette") || nbt.contains("palette"))) {
            AIBuilderMod.LOGGER.info("Found Sponge-style BlockData and Palette");
            Map<Integer, String> palette = new HashMap<>();

            // Try capitalized Palette first
            NbtCompound paletteData = nbt.getCompound("Palette");
            if (paletteData.isEmpty()) {
                paletteData = nbt.getCompound("palette");
            }

            for (String key : paletteData.getKeys()) {
                int id = paletteData.getInt(key);
                palette.put(id, key);
            }

            byte[] data = nbt.contains("BlockData") ? nbt.getByteArray("BlockData") : nbt.getByteArray("blockdata");
            blocks = parseBlocks(data, palette, width * height * length);
        }
        // Try direct blocks list format (Cobblemon/other formats)
        else if (nbt.contains("blocks") && nbt.contains("palette")) {
            AIBuilderMod.LOGGER.info("Found 'blocks' and 'palette' tags");
            blocks = parseCobblemonFormat(nbt, width, height, length);
        }
        // Try alternative formats
        else if (nbt.contains("Blocks")) {
            AIBuilderMod.LOGGER.info("Found 'Blocks' tag, trying to parse");
            blocks = parseBlocksTag(nbt.getCompound("Blocks"), width, height, length);
        }
        // Try Schematic-style format
        else if (nbt.contains("TileEntities")) {
            AIBuilderMod.LOGGER.info("Found TileEntities, might be old schematic format");
            blocks = parseTileEntitiesFormat(nbt, width, height, length);
        }
        else {
            // Create empty schematic if no block data found
            AIBuilderMod.LOGGER.warn("No block data found in NBT file, creating empty schematic");
            blocks = new BlockState[width * height * length];
            for (int i = 0; i < blocks.length; i++) {
                blocks[i] = Blocks.AIR.getDefaultState();
            }
        }

        return new SchematicData(
            fileName,
            width,
            height,
            length,
            blocks,
            new net.minecraft.util.math.BlockPos(0, 0, 0)
        );
    }

    /**
     * Parse Cobblemon-style NBT format
     * Has 'blocks', 'palette', 'size', 'entities' tags as LIST types
     */
    private BlockState[] parseCobblemonFormat(NbtCompound nbt, int width, int height, int length) {
        AIBuilderMod.LOGGER.info("Parsing Cobblemon-style NBT format (LIST-based)");

        int totalBlocks = width * height * length;
        BlockState[] blocks = new BlockState[totalBlocks];

        // Read palette from LIST
        Map<Integer, String> palette = new HashMap<>();
        if (nbt.contains("palette", NbtElement.LIST_TYPE)) {
            NbtList paletteList = nbt.getList("palette", NbtElement.COMPOUND_TYPE);
            AIBuilderMod.LOGGER.info("Palette is a LIST with {} entries", paletteList.size());

            // In Cobblemon format, palette is a list of compounds
            for (int i = 0; i < paletteList.size(); i++) {
                NbtCompound entry = paletteList.getCompound(i);
                // Each entry might have a "Name" or "id" field
                String blockId = entry.contains("Name") ? entry.getString("Name") :
                                 entry.contains("id") ? entry.getString("id") :
                                 entry.contains("block_id") ? entry.getString("block_id") : null;
                if (blockId != null) {
                    palette.put(i, blockId);
                }
            }
        } else if (nbt.contains("palette")) {
            // Try as COMPOUND
            NbtCompound paletteTag = nbt.getCompound("palette");
            if (!paletteTag.isEmpty()) {
                for (String key : paletteTag.getKeys()) {
                    int id = paletteTag.getInt(key);
                    palette.put(id, key);
                }
            }
        }

        AIBuilderMod.LOGGER.info("Palette has {} entries", palette.size());

        // Read blocks from LIST
        if (nbt.contains("blocks", NbtElement.LIST_TYPE)) {
            NbtList blocksList = nbt.getList("blocks", NbtElement.COMPOUND_TYPE);
            AIBuilderMod.LOGGER.info("Blocks is a LIST with {} entries", blocksList.size());

            // Log first few block entries to understand structure
            int sampleCount = Math.min(3, blocksList.size());
            for (int i = 0; i < sampleCount; i++) {
                NbtCompound blockEntry = blocksList.getCompound(i);
                AIBuilderMod.LOGGER.info("Block[{}] keys: {}", i, blockEntry.getKeys());
                for (String key : blockEntry.getKeys()) {
                    if (blockEntry.contains(key, NbtElement.INT_TYPE)) {
                        AIBuilderMod.LOGGER.info("  - {}: INT = {}", key, blockEntry.getInt(key));
                    } else if (blockEntry.contains(key, NbtElement.INT_ARRAY_TYPE)) {
                        int[] arr = blockEntry.getIntArray(key);
                        AIBuilderMod.LOGGER.info("  - {}: INT_ARRAY length = {}", key, arr.length);
                    } else if (blockEntry.contains(key, NbtElement.STRING_TYPE)) {
                        AIBuilderMod.LOGGER.info("  - {}: STRING = {}", key, blockEntry.getString(key));
                    } else {
                        AIBuilderMod.LOGGER.info("  - {}: {}", key, blockEntry.get(key).getClass().getSimpleName());
                    }
                }
            }

            // Each block entry should have position and state data
            for (int i = 0; i < blocksList.size(); i++) {
                NbtCompound blockEntry = blocksList.getCompound(i);

                // Read position (might be "pos", "Pos", or separate x,y,z)
                int x, y, z;
                if (blockEntry.contains("pos") && blockEntry.getIntArray("pos").length > 0) {
                    int[] pos = blockEntry.getIntArray("pos");
                    x = pos[0];
                    y = pos[1];
                    z = pos[2];
                } else {
                    x = blockEntry.getInt("x");
                    y = blockEntry.getInt("y");
                    z = blockEntry.getInt("z");
                }

                // Read state (palette index or block ID)
                int paletteId;
                if (blockEntry.contains("state")) {
                    paletteId = blockEntry.getInt("state");
                } else if (blockEntry.contains("id")) {
                    paletteId = blockEntry.getInt("id");
                } else {
                    continue;
                }

                // Convert to linear index
                if (x >= 0 && x < width && y >= 0 && y < height && z >= 0 && z < length) {
                    int index = y * width * length + z * width + x;
                    if (index < blocks.length) {
                        String blockId = palette.get(paletteId);
                        if (blockId != null) {
                            blocks[index] = parseBlockState(blockId);
                        } else {
                            blocks[index] = Blocks.AIR.getDefaultState();
                        }
                    }
                }
            }
        }

        // Fill null entries with air
        for (int i = 0; i < blocks.length; i++) {
            if (blocks[i] == null) {
                blocks[i] = Blocks.AIR.getDefaultState();
            }
        }

        AIBuilderMod.LOGGER.info("Parsed {} blocks from Cobblemon format", blocks.length);
        return blocks;
    }

    /**
     * Parse Cobblemon blocks list format
     */
    private BlockState[] parseCobblemonBlocksList(NbtCompound blocksTag, Map<Integer, String> palette, int width, int height, int length) {
        BlockState[] blocks = new BlockState[width * height * length];

        AIBuilderMod.LOGGER.info("Parsing Cobblemon blocks list");

        // Try to find block data in various formats
        if (blocksTag.contains("States")) {
            // List of block states
            // Parse according to format
            AIBuilderMod.LOGGER.info("Found 'States' in blocks tag");
        }

        // Fallback to air
        for (int i = 0; i < blocks.length; i++) {
            blocks[i] = Blocks.AIR.getDefaultState();
        }

        return blocks;
    }

    /**
     * Parse blocks from 'Blocks' NBT tag (older format)
     */
    private BlockState[] parseBlocksTag(NbtCompound blocksTag, int width, int height, int length) {
        BlockState[] blocks = new BlockState[width * height * length];

        AIBuilderMod.LOGGER.info("Parsing Blocks tag: {}", blocksTag.getKeys());

        // Try to find data within Blocks tag
        if (blocksTag.contains("Data")) {
            byte[] data = blocksTag.getByteArray("Data");
            if (blocksTag.contains("Palette")) {
                Map<Integer, String> palette = new HashMap<>();
                NbtCompound paletteData = blocksTag.getCompound("Palette");
                for (String key : paletteData.getKeys()) {
                    int id = paletteData.getInt(key);
                    palette.put(id, key);
                }
                return parseBlocks(data, palette, width * height * length);
            }
        }

        // If parsing failed, return air
        for (int i = 0; i < blocks.length; i++) {
            blocks[i] = Blocks.AIR.getDefaultState();
        }
        return blocks;
    }

    /**
     * Parse TileEntities format (very old schematic format)
     */
    private BlockState[] parseTileEntitiesFormat(NbtCompound nbt, int width, int height, int length) {
        BlockState[] blocks = new BlockState[width * height * length];

        AIBuilderMod.LOGGER.warn("TileEntities format not fully supported, creating empty schematic");

        for (int i = 0; i < blocks.length; i++) {
            blocks[i] = Blocks.AIR.getDefaultState();
        }
        return blocks;
    }

    /**
     * Parse Litematic block data from packed long array
     */
    private BlockState[] parseLitematicBlocks(long[] data, Map<Integer, String> palette, int width, int height, int length, int bitsPerBlock) {
        int totalBlocks = width * height * length;
        BlockState[] blocks = new BlockState[totalBlocks];

        long mask = (1L << bitsPerBlock) - 1L;
        int blocksPerLong = 64 / bitsPerBlock;
        int index = 0;

        for (int i = 0; i < data.length && index < totalBlocks; i++) {
            long value = data[i];
            for (int j = 0; j < blocksPerLong && index < totalBlocks; j++) {
                int paletteId = (int) (value & mask);
                value >>>= bitsPerBlock;

                String blockId = palette.get(paletteId);
                if (blockId != null) {
                    blocks[index] = parseBlockState(blockId);
                } else {
                    blocks[index] = Blocks.AIR.getDefaultState();
                }
                index++;
            }
        }

        return blocks;
    }

    /**
     * Parse block data from schematic format
     */
    private BlockState[] parseBlocks(byte[] data, Map<Integer, String> palette, int totalBlocks) {
        BlockState[] blocks = new BlockState[totalBlocks];

        AIBuilderMod.LOGGER.info("Parsing {} blocks from {} bytes of data", totalBlocks, data.length);
        AIBuilderMod.LOGGER.info("Palette has {} entries", palette.size());

        // Simple varint decoding
        int index = 0;
        int nonAirCount = 0;
        for (int i = 0; i < totalBlocks && index < data.length; i++) {
            int paletteId = 0;
            int shift = 0;
            byte b;

            do {
                b = data[index++];
                paletteId |= (b & 0x7F) << shift;
                shift += 7;
            } while ((b & 0x80) != 0 && index < data.length);

            String blockId = palette.get(paletteId);
            if (blockId != null) {
                blocks[i] = parseBlockState(blockId);
                if (blocks[i] != null && blocks[i] != Blocks.AIR.getDefaultState()) {
                    nonAirCount++;
                }
            } else {
                blocks[i] = Blocks.AIR.getDefaultState();
            }

            if (i < 10) {
                AIBuilderMod.LOGGER.info("Block[{}]: paletteId={}, blockId={}, state={}",
                    i, paletteId, blockId, blocks[i]);
            }
        }

        AIBuilderMod.LOGGER.info("Parsed {} blocks ({} non-AIR)", totalBlocks, nonAirCount);

        return blocks;
    }

    /**
     * Parse block state from Minecraft block ID string
     */
    private BlockState parseBlockState(String blockId) {
        try {
            // Remove namespace if present
            String id = blockId.contains(":") ? blockId.split(":")[1] : blockId;

            // Remove properties
            id = id.split("\\[")[0];

            // Try to get block from registry
            // Note: This is a simplified version. In production, you'd use the Block registry
            return net.minecraft.registry.Registries.BLOCK.get(
                net.minecraft.util.Identifier.tryParse(blockId)
            ).getDefaultState();
        } catch (Exception e) {
            AIBuilderMod.LOGGER.warn("Failed to parse block: {}", blockId);
            return Blocks.AIR.getDefaultState();
        }
    }
}
