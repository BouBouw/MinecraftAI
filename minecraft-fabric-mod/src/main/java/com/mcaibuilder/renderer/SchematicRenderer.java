package com.mcaibuilder.renderer;

import com.mcaibuilder.config.ModConfig;
import com.mcaibuilder.schematic.SchematicData;
import com.mcaibuilder.schematic.SchematicManager;
import net.minecraft.block.BlockState;
import net.minecraft.block.Blocks;
import net.minecraft.client.MinecraftClient;
import net.minecraft.client.render.*;
import net.minecraft.client.render.block.BlockRenderManager;
import net.minecraft.client.util.math.MatrixStack;
import net.minecraft.util.math.BlockPos;
import net.minecraft.util.math.Vec3d;
import net.minecraft.world.BlockRenderView;
import org.joml.Matrix4f;

/**
 * Renderer pour schematic overlay - Style Schematica
 * Affiche des blocs semi-transparents avec bordures colorées
 * Non-collidable (on peut passer à travers)
 */
public class SchematicRenderer {

    private final SchematicManager schematicManager;
    private boolean overlayEnabled = false;

    // Couleurs pour le rendu
    private static final float OPACITY = 0.5f; // 50% de transparence (plus visible)

    public SchematicRenderer(SchematicManager schematicManager) {
        this.schematicManager = schematicManager;
    }

    /**
     * Point d'entrée principal pour le rendu depuis WorldRenderer
     * Compatible Minecraft 1.21 avec matrices JOML directes
     */
    public void renderWithMatrices(Matrix4f projectionMatrix, Matrix4f projectionMatrix2, Vec3d cameraPos) {
        if (!schematicManager.hasActiveSchematic()) {
            return;
        }

        // Si l'overlay est désactivé mais une construction est en cours, afficher seulement le contour du sol
        boolean isOverlayDisabled = !overlayEnabled;
        boolean isBuildingInProgress = isBuildingInProgress();

        if (isOverlayDisabled && isBuildingInProgress) {
            // Mode minimal : afficher seulement le contour du sol
            renderFloorOutlineOnly(cameraPos);
            return;
        }

        if (!overlayEnabled) {
            return;
        }

        try {
            SchematicData schematic = schematicManager.getActiveSchematic();
            BlockPos origin = schematic.getOrigin();
            MinecraftClient client = MinecraftClient.getInstance();

            // Créer un MatrixStack temporaire pour le rendu
            MatrixStack matrices = new MatrixStack();

            // Rendre chaque bloc
            for (int y = 0; y < schematic.getHeight(); y++) {
                for (int z = 0; z < schematic.getLength(); z++) {
                    for (int x = 0; x < schematic.getWidth(); x++) {
                        BlockState blockState = schematic.getBlockAt(x, y, z);

                        if (blockState == null || blockState == Blocks.AIR.getDefaultState()) {
                            continue;
                        }

                        BlockPos worldPos = new BlockPos(
                            origin.getX() + x,
                            origin.getY() + y,
                            origin.getZ() + z
                        );

                        // Vérifier la distance de rendu
                        if (!isWithinRenderDistance(worldPos, BlockPos.ofFloored(cameraPos))) {
                            continue;
                        }

                        // Rendre le bloc
                        renderBlock(matrices, worldPos, blockState, cameraPos,
                            client.getBufferBuilders().getEntityVertexConsumers(), client);
                    }
                }
            }

            // Dessiner
            VertexConsumerProvider.Immediate immediate = client.getBufferBuilders().getEntityVertexConsumers();
            immediate.draw(RenderLayer.getTranslucent());
            immediate.draw(RenderLayer.getLines());

        } catch (Exception e) {
            com.mcaibuilder.mod.AIBuilderMod.LOGGER.error("Render error: {}", e.getMessage(), e);
        }
    }

    /**
     * Point d'entrée principal pour le rendu depuis WorldRenderer
     * Version legacy pour compatibilité
     */
    public void renderWorld(MatrixStack matrices, Vec3d cameraPos) {
        // Version legacy : utilise getEntityVertexConsumers() du client
        MinecraftClient client = MinecraftClient.getInstance();
        var immediate = client.getBufferBuilders().getEntityVertexConsumers();
        renderWorld(matrices, cameraPos, immediate);
    }

    /**
     * Version pour Fabric API WorldRenderEvents
     * Utilise le VertexConsumerProvider fourni par le contexte de Fabric
     */
    public void renderWorld(MatrixStack matrices, Vec3d cameraPos,
                          VertexConsumerProvider.Immediate immediate) {
        com.mcaibuilder.mod.AIBuilderMod.LOGGER.info("🎨 renderWorld with VCP - overlayEnabled={}, hasSchematic={}",
            overlayEnabled, schematicManager.hasActiveSchematic());

        if (!schematicManager.hasActiveSchematic()) {
            com.mcaibuilder.mod.AIBuilderMod.LOGGER.warn("❌ renderWorld skipped - no schematic");
            return;
        }

        // Si l'overlay est désactivé mais une construction est en cours, afficher seulement le contour du sol
        boolean isOverlayDisabled = !overlayEnabled;
        boolean isBuildingInProgress = isBuildingInProgress();

        if (isOverlayDisabled && isBuildingInProgress) {
            // Mode minimal : afficher seulement le contour du sol
            renderFloorOutlineOnly(cameraPos);
            return;
        }

        if (!overlayEnabled) {
            com.mcaibuilder.mod.AIBuilderMod.LOGGER.warn("❌ renderWorld skipped - overlay disabled, no build in progress");
            return;
        }

        try {
            SchematicData schematic = schematicManager.getActiveSchematic();
            BlockPos origin = schematic.getOrigin();
            MinecraftClient client = MinecraftClient.getInstance();

            com.mcaibuilder.mod.AIBuilderMod.LOGGER.info("📍 Rendering {} blocks at origin ({}, {}, {})",
                schematic.getWidth() * schematic.getHeight() * schematic.getLength(),
                origin.getX(), origin.getY(), origin.getZ());

            int blockCount = 0;
            int visibleBlockCount = 0;

            // Rendre chaque bloc
            for (int y = 0; y < schematic.getHeight(); y++) {
                for (int z = 0; z < schematic.getLength(); z++) {
                    for (int x = 0; x < schematic.getWidth(); x++) {
                        BlockState blockState = schematic.getBlockAt(x, y, z);

                        if (blockState == null || blockState == Blocks.AIR.getDefaultState()) {
                            continue;
                        }

                        BlockPos worldPos = new BlockPos(
                            origin.getX() + x,
                            origin.getY() + y,
                            origin.getZ() + z
                        );

                        // Vérifier la distance de rendu
                        if (!isWithinRenderDistance(worldPos, BlockPos.ofFloored(cameraPos))) {
                            continue;
                        }

                        // Rendre le bloc
                        renderBlock(matrices, worldPos, blockState, cameraPos, immediate, client);
                        blockCount++;
                        visibleBlockCount++;
                    }
                }
            }

            com.mcaibuilder.mod.AIBuilderMod.LOGGER.info("Drew {} blocks", visibleBlockCount);

            // Dessiner la bordure aqua autour du schéma entier avec marge de 1 bloc
            renderSchematicBorder(matrices, cameraPos, immediate, schematic, origin);

            // IMPORTANT: Dessiner les buffers immédiatement
            // Utiliser draw() sans paramètre pour dessiner tous les layers
            immediate.draw();

        } catch (Exception e) {
            com.mcaibuilder.mod.AIBuilderMod.LOGGER.error("Render error: {}", e.getMessage(), e);
        }
    }

    /**
     * Dessine une bordure aqua autour du schéma entier avec une marge de 1 bloc
     * Pas de marge pour le sol (Y minimum)
     */
    private void renderSchematicBorder(MatrixStack matrices, Vec3d cameraPos,
                                      VertexConsumerProvider.Immediate immediate,
                                      SchematicData schematic, BlockPos origin) {
        // Marge de 1 bloc sur chaque côté SAUF le sol (Y min)
        int margin = 1;
        int bottomMargin = 0; // Pas de marge pour le sol

        double minX = origin.getX() - margin - cameraPos.x;
        double minY = origin.getY() - bottomMargin - cameraPos.y; // Pas de marge en bas
        double minZ = origin.getZ() - margin - cameraPos.z;
        double maxX = origin.getX() + schematic.getWidth() + margin - cameraPos.x;
        double maxY = origin.getY() + schematic.getHeight() + margin - cameraPos.y;
        double maxZ = origin.getZ() + schematic.getLength() + margin - cameraPos.z;

        matrices.push();
        // Pas de translate nécessaire car on utilise les positions relatives à la caméra

        // Couleur aqua pour la bordure générale
        float r = 0.0f;  // Rouge
        float g = 1.0f;  // Vert (100%)
        float b = 1.0f;  // Bleu (100%) = Aqua
        float a = 0.9f;  // Opacité élevée pour bien voir la bordure

        VertexConsumer consumer = immediate.getBuffer(RenderLayer.getLines());

        // Dessiner les 12 arêtes de la boîte englobante
        // Arêtes du bas (Y = minY)
        drawEdge(consumer, matrices, (float)minX, (float)minY, (float)minZ, (float)maxX, (float)minY, (float)minZ, r, g, b, a);
        drawEdge(consumer, matrices, (float)maxX, (float)minY, (float)minZ, (float)maxX, (float)minY, (float)maxZ, r, g, b, a);
        drawEdge(consumer, matrices, (float)maxX, (float)minY, (float)maxZ, (float)minX, (float)minY, (float)maxZ, r, g, b, a);
        drawEdge(consumer, matrices, (float)minX, (float)minY, (float)maxZ, (float)minX, (float)minY, (float)minZ, r, g, b, a);

        // Arêtes du haut (Y = maxY)
        drawEdge(consumer, matrices, (float)minX, (float)maxY, (float)minZ, (float)maxX, (float)maxY, (float)minZ, r, g, b, a);
        drawEdge(consumer, matrices, (float)maxX, (float)maxY, (float)minZ, (float)maxX, (float)maxY, (float)maxZ, r, g, b, a);
        drawEdge(consumer, matrices, (float)maxX, (float)maxY, (float)maxZ, (float)minX, (float)maxY, (float)maxZ, r, g, b, a);
        drawEdge(consumer, matrices, (float)minX, (float)maxY, (float)maxZ, (float)minX, (float)maxY, (float)minZ, r, g, b, a);

        // Arêtes verticales
        drawEdge(consumer, matrices, (float)minX, (float)minY, (float)minZ, (float)minX, (float)maxY, (float)minZ, r, g, b, a);
        drawEdge(consumer, matrices, (float)maxX, (float)minY, (float)minZ, (float)maxX, (float)maxY, (float)minZ, r, g, b, a);
        drawEdge(consumer, matrices, (float)maxX, (float)minY, (float)maxZ, (float)maxX, (float)maxY, (float)maxZ, r, g, b, a);
        drawEdge(consumer, matrices, (float)minX, (float)minY, (float)maxZ, (float)minX, (float)maxY, (float)maxZ, r, g, b, a);

        matrices.pop();
    }

    /**
     * Rend un bloc individuel avec texture semi-transparente et bordure
     * Style Schematica - bloc texturé avec transparence + bordure colorée
     * Bordure verte si pas de bloc, rouge si bloc déjà placé
     */
    private void renderBlock(MatrixStack matrices, BlockPos pos, BlockState blockState,
                           Vec3d cameraPos, VertexConsumerProvider.Immediate immediate,
                           MinecraftClient client) {

        // Position relative à la caméra
        double x = pos.getX() - cameraPos.x;
        double y = pos.getY() - cameraPos.y;
        double z = pos.getZ() - cameraPos.z;

        // DEBUG: Log la position
        com.mcaibuilder.mod.AIBuilderMod.LOGGER.debug("  Rendering block at rel pos ({}, {}, {})", x, y, z);

        matrices.push();

        // Positionner à l'emplacement du bloc
        matrices.translate(x, y, z);

        // 1. Rendre le bloc avec sa vraie texture semi-transparente
        renderTexturedBlock(matrices, pos, blockState, immediate, client);

        // 2. Vérifier si un bloc est déjà placé à cette position
        BlockState worldBlock = null;
        boolean hasBlock = false;
        boolean isCorrectBlock = false;

        if (client.world != null) {
            worldBlock = client.world.getBlockState(pos);
            hasBlock = worldBlock != null && worldBlock != Blocks.AIR.getDefaultState();

            // Vérifier si le bloc est correct
            if (hasBlock) {
                // Comparer les blocs par leur ID de registre
                var expectedBlockId = net.minecraft.registry.Registries.BLOCK.getId(blockState.getBlock());
                var worldBlockId = net.minecraft.registry.Registries.BLOCK.getId(worldBlock.getBlock());
                isCorrectBlock = expectedBlockId.equals(worldBlockId);
            }
        }

        // 3. Dessiner les bordures selon l'état du bloc
        // - Si pas de bloc: pas de bordure
        // - Si bloc correct: pas de bordure (ignorer, déjà placé)
        // - Si mauvais bloc: bordure rouge (bloc incorrect à remplacer)
        if (hasBlock && !isCorrectBlock) {
            renderBlockOutline(matrices, immediate, false); // rouge - mauvais bloc seulement
        }

        matrices.pop();
    }

    /**
     * Rend un bloc avec sa texture en semi-transparence
     * Style Schematica - bloc texturé avec transparence
     */
    private void renderTexturedBlock(MatrixStack matrices, BlockPos pos, BlockState blockState,
                                   VertexConsumerProvider.Immediate immediate,
                                   MinecraftClient client) {
        try {
            if (client.world == null) {
                return;
            }

            BlockRenderManager blockRenderManager = client.getBlockRenderManager();

            // Utiliser RenderLayer.getTranslucent() pour pouvoir utiliser l'alpha
            VertexConsumer consumer = immediate.getBuffer(RenderLayer.getTranslucent());

            // Créer un wrapper qui applique 60% de transparence (plus visible)
            TranslucentVertexConsumer translucentConsumer = new TranslucentVertexConsumer(consumer, 0.6f);

            // Rendre le bloc avec sa texture semi-transparente
            blockRenderManager.renderBlock(blockState, pos, client.world, matrices,
                translucentConsumer, false, client.world.getRandom());

        } catch (Exception e) {
            // Si le rendu texturé échoue, utiliser le fallback coloré
            com.mcaibuilder.mod.AIBuilderMod.LOGGER.debug("Textured render failed for block at {}, using fallback", pos);
            renderColoredBlock(matrices, blockState, immediate);
        }
    }

    /**
     * Rend un bloc coloré semi-transparent selon son type
     * Style Schematica - simple et efficace
     */
    private void renderColoredBlock(MatrixStack matrices, BlockState blockState,
                                   VertexConsumerProvider.Immediate immediate) {
        // Obtenir la couleur du bloc
        float[] color = getBlockColor(blockState);
        float r = color[0];
        float g = color[1];
        float b = color[2];
        float a = 0.6f; // 60% d'opacité - plus visible

        float x1 = 0, y1 = 0, z1 = 0;
        float x2 = 1, y2 = 1, z2 = 1;

        // Dessiner toutes les faces du cube comme paires de triangles
        // Face du haut (Y=1)
        drawFace(immediate.getBuffer(RenderLayer.getTranslucent()), matrices,
            x1, y2, z1, x2, y2, z1, x2, y2, z2, x1, y2, z2, r, g, b, a, 0, 1, 0);
        drawFace(immediate.getBuffer(RenderLayer.getTranslucent()), matrices,
            x1, y2, z2, x2, y2, z2, x2, y2, z1, x1, y2, z1, r, g, b, a, 0, 1, 0);

        // Face du bas (Y=0)
        drawFace(immediate.getBuffer(RenderLayer.getTranslucent()), matrices,
            x1, y1, z1, x1, y1, z2, x2, y1, z2, x2, y1, z1, r, g, b, a, 0, -1, 0);
        drawFace(immediate.getBuffer(RenderLayer.getTranslucent()), matrices,
            x2, y1, z1, x2, y1, z2, x1, y1, z2, x1, y1, z1, r, g, b, a, 0, -1, 0);

        // Face nord (Z=0)
        drawFace(immediate.getBuffer(RenderLayer.getTranslucent()), matrices,
            x1, y1, z1, x1, y2, z1, x2, y2, z1, x2, y1, z1, r, g, b, a, 0, 0, -1);
        drawFace(immediate.getBuffer(RenderLayer.getTranslucent()), matrices,
            x2, y2, z1, x1, y2, z1, x1, y1, z1, x2, y1, z1, r, g, b, a, 0, 0, -1);

        // Face sud (Z=1)
        drawFace(immediate.getBuffer(RenderLayer.getTranslucent()), matrices,
            x1, y1, z2, x2, y1, z2, x2, y2, z2, x1, y2, z2, r, g, b, a, 0, 0, 1);
        drawFace(immediate.getBuffer(RenderLayer.getTranslucent()), matrices,
            x2, y1, z2, x1, y1, z2, x1, y2, z2, x2, y2, z2, r, g, b, a, 0, 0, 1);

        // Face ouest (X=0)
        drawFace(immediate.getBuffer(RenderLayer.getTranslucent()), matrices,
            x1, y1, z1, x2, y1, z1, x2, y2, z1, x1, y2, z1, r, g, b, a, -1, 0, 0);
        drawFace(immediate.getBuffer(RenderLayer.getTranslucent()), matrices,
            x2, y2, z1, x2, y1, z1, x1, y1, z1, x1, y2, z1, r, g, b, a, -1, 0, 0);

        // Face est (X=1)
        drawFace(immediate.getBuffer(RenderLayer.getTranslucent()), matrices,
            x1, y1, z2, x1, y2, z2, x2, y2, z2, x2, y1, z2, r, g, b, a, 1, 0, 0);
        drawFace(immediate.getBuffer(RenderLayer.getTranslucent()), matrices,
            x2, y2, z2, x1, y2, z2, x1, y1, z2, x2, y1, z2, r, g, b, a, 1, 0, 0);
    }

    /**
     * Retourne la couleur d'un bloc (RGB) - Bleu uniforme pour tous les blocs
     */
    private float[] getBlockColor(BlockState blockState) {
        // Couleur bleue uniforme pour tous les blocs
        return new float[]{0.0f, 0.0f, 1.0f}; // Bleu pur
    }

    /**
     * Dessine une face quad du cube
     */
    private void drawFace(VertexConsumer consumer, MatrixStack matrices,
                         float x1, float y1, float z1,
                         float x2, float y2, float z2,
                         float x3, float y3, float z3,
                         float x4, float y4, float z4,
                         float r, float g, float b, float a,
                         float nx, float ny, float nz) {
        consumer.vertex(matrices.peek().getPositionMatrix(), x1, y1, z1)
            .color(r, g, b, a)
            .normal(matrices.peek(), nx, ny, nz);
        consumer.vertex(matrices.peek().getPositionMatrix(), x2, y2, z2)
            .color(r, g, b, a)
            .normal(matrices.peek(), nx, ny, nz);
        consumer.vertex(matrices.peek().getPositionMatrix(), x3, y3, z3)
            .color(r, g, b, a)
            .normal(matrices.peek(), nx, ny, nz);
        consumer.vertex(matrices.peek().getPositionMatrix(), x4, y4, z4)
            .color(r, g, b, a)
            .normal(matrices.peek(), nx, ny, nz);
    }

    /**
     * Rend la bordure wireframe autour du bloc
     * @param green Si true, bordure verte; si false, bordure rouge
     */
    private void renderBlockOutline(MatrixStack matrices, VertexConsumerProvider.Immediate immediate, boolean green) {
        VertexConsumer consumer = immediate.getBuffer(RenderLayer.getLines());

        float r, g, b;
        if (green) {
            r = 0.0f; // Rouge
            g = 1.0f; // Vert
            b = 0.0f; // Bleu
        } else {
            r = 1.0f; // Rouge
            g = 0.0f; // Vert
            b = 0.0f; // Bleu
        }
        float a = 0.8f; // Opacité pour les lignes (légèrement transparent)

        float x1 = 0, y1 = 0, z1 = 0;
        float x2 = 1, y2 = 1, z2 = 1;

        // Dessiner toutes les arêtes
        drawEdge(consumer, matrices, x1, y1, z1, x2, y1, z1, r, g, b, a);
        drawEdge(consumer, matrices, x2, y1, z1, x2, y1, z2, r, g, b, a);
        drawEdge(consumer, matrices, x2, y1, z2, x1, y1, z2, r, g, b, a);
        drawEdge(consumer, matrices, x1, y1, z2, x1, y1, z1, r, g, b, a);

        drawEdge(consumer, matrices, x1, y2, z1, x2, y2, z1, r, g, b, a);
        drawEdge(consumer, matrices, x2, y2, z1, x2, y2, z2, r, g, b, a);
        drawEdge(consumer, matrices, x2, y2, z2, x1, y2, z2, r, g, b, a);
        drawEdge(consumer, matrices, x1, y2, z2, x1, y2, z1, r, g, b, a);

        drawEdge(consumer, matrices, x1, y1, z1, x1, y2, z1, r, g, b, a);
        drawEdge(consumer, matrices, x2, y1, z1, x2, y2, z1, r, g, b, a);
        drawEdge(consumer, matrices, x1, y1, z2, x1, y2, z2, r, g, b, a);
        drawEdge(consumer, matrices, x2, y1, z2, x2, y2, z2, r, g, b, a);
    }

    /**
     * Fallback: dessine une boîte colorée semi-transparente
     * Utilise Direct BufferBuilder pour avoir le contrôle complet des vertices
     */
    private void renderColoredFallback(MatrixStack matrices, VertexConsumerProvider.Immediate immediate) {
        // Utiliser RenderLayer.getLines() mais dessiner des triangles au lieu de lignes
        VertexConsumer consumer = immediate.getBuffer(RenderLayer.getLines());

        // Couleur cyan/bleue très visible (style Schematica)
        float r = 0.0f; // Rouge
        float g = 0.7f; // Vert
        float b = 1.0f; // Bleu
        float a = OPACITY; // 50% de transparence

        float x1 = 0, y1 = 0, z1 = 0;
        float x2 = 1, y2 = 1, z2 = 1;

        // Dessiner les faces du cube sous forme de paires de triangles
        // Chaque face = 2 triangles

        // Face du haut (Y=2) - vers le ciel pour mieux voir
        drawTriangle(consumer, matrices, x1, y2, z1, x2, y2, z1, x1, y2, z2, r, g, b, a, 0, 1, 0);
        drawTriangle(consumer, matrices, x2, y2, z1, x2, y2, z2, x1, y2, z2, r, g, b, a, 0, 1, 0);

        // Face du bas (Y=0)
        drawTriangle(consumer, matrices, x1, y1, z1, x1, y1, z2, x2, y1, z1, r, g, b, a, 0, -1, 0);
        drawTriangle(consumer, matrices, x2, y1, z1, x2, y1, z2, x1, y1, z2, r, g, b, a, 0, -1, 0);

        // Face nord (Z=0)
        drawTriangle(consumer, matrices, x1, y1, z1, x1, y2, z1, x2, y2, z1, r, g, b, a, 0, 0, -1);
        drawTriangle(consumer, matrices, x2, y2, z1, x1, y2, z1, x2, y1, z1, r, g, b, a, 0, 0, -1);

        // Face sud (Z=2)
        drawTriangle(consumer, matrices, x1, y1, z2, x2, y1, z2, x2, y2, z2, r, g, b, a, 0, 0, 1);
        drawTriangle(consumer, matrices, x2, y1, z2, x1, y1, z2, x1, y2, z2, r, g, b, a, 0, 0, 1);

        // Face ouest (X=0)
        drawTriangle(consumer, matrices, x1, y1, z1, x1, y2, z1, x1, y2, z2, r, g, b, a, -1, 0, 0);
        drawTriangle(consumer, matrices, x1, y2, z1, x1, y1, z2, x1, y2, z2, r, g, b, a, -1, 0, 0);

        // Face est (X=2)
        drawTriangle(consumer, matrices, x2, y1, z1, x2, y1, z2, x2, y2, z2, r, g, b, a, 1, 0, 0);
        drawTriangle(consumer, matrices, x2, y2, z2, x2, y1, z2, x2, y1, z1, r, g, b, a, 1, 0, 0);
    }

    /**
     * Dessine un triangle pour les faces du cube
     */
    private void drawTriangle(VertexConsumer consumer, MatrixStack matrices,
                           float x1, float y1, float z1,
                           float x2, float y2, float z2,
                           float x3, float y3, float z3,
                           float r, float g, float b, float a,
                           float nx, float ny, float nz) {
        consumer.vertex(matrices.peek().getPositionMatrix(), x1, y1, z1)
            .color(r, g, b, a)
            .normal(matrices.peek(), nx, ny, nz);
        consumer.vertex(matrices.peek().getPositionMatrix(), x2, y2, z2)
            .color(r, g, b, a)
            .normal(matrices.peek(), nx, ny, nz);
        consumer.vertex(matrices.peek().getPositionMatrix(), x3, y3, z3)
            .color(r, g, b, a)
            .normal(matrices.peek(), nx, ny, nz);
    }

    /**
     * Dessine un quadrilatère (face) avec transparence
     */
    private void drawQuad(VertexConsumer consumer, MatrixStack matrices,
                         float x1, float y1, float z1,
                         float x2, float y2, float z2,
                         float x3, float y3, float z3,
                         float x4, float y4, float z4,
                         float r, float g, float b, float a,
                         float nx, float ny, float nz) {
        consumer.vertex(matrices.peek().getPositionMatrix(), x1, y1, z1).color(r, g, b, a).normal(matrices.peek(), nx, ny, nz);
        consumer.vertex(matrices.peek().getPositionMatrix(), x2, y2, z2).color(r, g, b, a).normal(matrices.peek(), nx, ny, nz);
        consumer.vertex(matrices.peek().getPositionMatrix(), x3, y3, z3).color(r, g, b, a).normal(matrices.peek(), nx, ny, nz);
        consumer.vertex(matrices.peek().getPositionMatrix(), x4, y4, z4).color(r, g, b, a).normal(matrices.peek(), nx, ny, nz);
    }

    /**
     * Dessine une arête entre deux points
     */
    private void drawEdge(VertexConsumer consumer, MatrixStack matrices,
                         float x1, float y1, float z1, float x2, float y2, float z2,
                         float r, float g, float b, float a) {
        consumer.vertex(matrices.peek().getPositionMatrix(), x1, y1, z1)
            .color(r, g, b, a)
            .normal(matrices.peek(), 0, 1, 0);
        consumer.vertex(matrices.peek().getPositionMatrix(), x2, y2, z2)
            .color(r, g, b, a)
            .normal(matrices.peek(), 0, 1, 0);
    }

    /**
     * Vérifie si un bloc est dans la distance de rendu
     */
    private boolean isWithinRenderDistance(BlockPos pos, BlockPos cameraPos) {
        int dx = pos.getX() - cameraPos.getX();
        int dy = pos.getY() - cameraPos.getY();
        int dz = pos.getZ() - cameraPos.getZ();

        return Math.abs(dx) <= ModConfig.RENDER_DISTANCE &&
               Math.abs(dy) <= ModConfig.RENDER_DISTANCE &&
               Math.abs(dz) <= ModConfig.RENDER_DISTANCE;
    }

    /**
     * Toggle l'overlay
     */
    public void toggleOverlay() {
        this.overlayEnabled = !this.overlayEnabled;
        com.mcaibuilder.mod.AIBuilderMod.LOGGER.info("Overlay toggled: {}", overlayEnabled);
    }

    public boolean isOverlayEnabled() {
        return overlayEnabled;
    }

    /**
     * Vérifie si une construction est en cours (bot connecté et schematic locké)
     */
    private boolean isBuildingInProgress() {
        return com.mcaibuilder.bot.BotManager.getInstance().getAllBots().size() > 0
            && schematicManager.isLocked();
    }

    /**
     * Rend seulement le contour du sol (outline) - mode minimal pendant la construction
     * Affiche le wireframe de tous les blocs au niveau Y=0 du schéma
     */
    private void renderFloorOutlineOnly(Vec3d cameraPos) {
        SchematicData schematic = schematicManager.getActiveSchematic();
        if (schematic == null) return;

        BlockPos origin = schematic.getOrigin();
        MinecraftClient client = MinecraftClient.getInstance();

        MatrixStack matrices = new MatrixStack();
        VertexConsumerProvider.Immediate immediate = client.getBufferBuilders().getEntityVertexConsumers();

        // Parcourir seulement les blocs du sol (Y=0)
        int y = 0;
        for (int z = 0; z < schematic.getLength(); z++) {
            for (int x = 0; x < schematic.getWidth(); x++) {
                BlockState blockState = schematic.getBlockAt(x, y, z);

                if (blockState == null || blockState == Blocks.AIR.getDefaultState()) {
                    continue;
                }

                BlockPos worldPos = new BlockPos(
                    origin.getX() + x,
                    origin.getY() + y,
                    origin.getZ() + z
                );

                // Vérifier la distance de rendu
                if (!isWithinRenderDistance(worldPos, BlockPos.ofFloored(cameraPos))) {
                    continue;
                }

                // Rendre seulement l'outline du bloc (wireframe vert)
                matrices.push();
                double px = worldPos.getX() - cameraPos.x;
                double py = worldPos.getY() - cameraPos.y;
                double pz = worldPos.getZ() - cameraPos.z;
                matrices.translate(px, py, pz);

                renderBlockOutline(matrices, immediate, true); // vert

                matrices.pop();
            }
        }

        // Dessiner les lignes
        immediate.draw(RenderLayer.getLines());
    }

    /**
     * Méthode de rendu legacy pour compatibilité
     */
    public void render(MatrixStack matrices) {
        // Cette méthode n'est plus utilisée, renderWorld est appelé à la place
    }
}
