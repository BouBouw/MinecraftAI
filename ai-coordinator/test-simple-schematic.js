/**
 * Create a simple test schematic in Sponge format
 */
import fs from 'fs';

// Create a minimal 3x3x3 stone schematic
const schematicData = {
    name: 'test_3x3x3',
    width: 3,
    height: 3,
    length: 3,
    blocks: [
        // Layer 1 (bottom)
        { x: 0, y: 0, z: 0, block: 'stone' },
        { x: 1, y: 0, z: 0, block: 'stone' },
        { x: 2, y: 0, z: 0, block: 'stone' },
        { x: 0, y: 0, z: 1, block: 'stone' },
        { x: 1, y: 0, z: 1, block: 'stone' },
        { x: 2, y: 0, z: 1, block: 'stone' },
        { x: 0, y: 0, z: 2, block: 'stone' },
        { x: 1, y: 0, z: 2, block: 'stone' },
        { x: 2, y: 0, z: 2, block: 'stone' },
        // Layer 2
        { x: 1, y: 1, z: 1, block: 'stone' },
        // Layer 3 (top)
        { x: 0, y: 2, z: 0, block: 'stone' },
        { x: 1, y: 2, z: 0, block: 'stone' },
        { x: 2, y: 2, z: 0, block: 'stone' },
        { x: 0, y: 2, z: 1, block: 'stone' },
        { x: 2, y: 2, z: 1, block: 'stone' },
        { x: 0, y: 2, z: 2, block: 'stone' },
        { x: 1, y: 2, z: 2, block: 'stone' },
        { x: 2, y: 2, z: 2, block: 'stone' },
    ]
};

console.log('Simple schematic data created');
console.log(JSON.stringify(schematicData, null, 2));
