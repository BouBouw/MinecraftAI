package com.mcaibuilder.renderer;

import net.minecraft.client.render.VertexConsumer;
import org.joml.Matrix4f;

/**
 * VertexConsumer qui applique une transparence à tous les vertices
 */
public class TranslucentVertexConsumer implements VertexConsumer {

    private final VertexConsumer delegate;
    private final float alpha;

    public TranslucentVertexConsumer(VertexConsumer delegate, float alpha) {
        this.delegate = delegate;
        this.alpha = alpha;
    }

    @Override
    public VertexConsumer vertex(float x, float y, float z) {
        delegate.vertex(x, y, z);
        return this;
    }

    @Override
    public VertexConsumer color(int red, int green, int blue, int alpha) {
        int newAlpha = (int)(alpha * this.alpha);
        return delegate.color(red, green, blue, newAlpha);
    }

    @Override
    public VertexConsumer color(float red, float green, float blue, float alpha) {
        float newAlpha = alpha * this.alpha;
        return delegate.color(red, green, blue, newAlpha);
    }

    @Override
    public VertexConsumer texture(float u, float v) {
        return delegate.texture(u, v);
    }

    @Override
    public VertexConsumer overlay(int u, int v) {
        return delegate.overlay(u, v);
    }

    @Override
    public VertexConsumer light(int u, int v) {
        return delegate.light(u, v);
    }

    @Override
    public VertexConsumer normal(float x, float y, float z) {
        return delegate.normal(x, y, z);
    }

    @Override
    public VertexConsumer vertex(Matrix4f matrix, float x, float y, float z) {
        return delegate.vertex(matrix, x, y, z);
    }
}
