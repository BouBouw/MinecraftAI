const fs = require('fs');
const zlib = require('zlib');

// Simple NBT writer for Sponge Schematic format
class NBTWriter {
    constructor() {
        this.buffer = Buffer.alloc(0);
    }

    writeByte(value) {
        const newBuffer = Buffer.alloc(this.buffer.length + 1);
        this.buffer.copy(newBuffer);
        newBuffer.writeUInt8(value, this.buffer.length);
        this.buffer = newBuffer;
    }

    writeShort(value) {
        const newBuffer = Buffer.alloc(this.buffer.length + 2);
        this.buffer.copy(newBuffer);
        newBuffer.writeInt16BE(value, this.buffer.length);
        this.buffer = newBuffer;
    }

    writeInt(value) {
        const newBuffer = Buffer.alloc(this.buffer.length + 4);
        this.buffer.copy(newBuffer);
        newBuffer.writeInt32BE(value, this.buffer.length);
        this.buffer = newBuffer;
    }

    writeString(str) {
        const strBuf = Buffer.from(str, 'UTF-8');
        this.writeShort(strBuf.length);
        const newBuffer = Buffer.alloc(this.buffer.length + strBuf.length);
        this.buffer.copy(newBuffer);
        strBuf.copy(newBuffer, this.buffer.length);
        this.buffer = newBuffer;
    }

    writeByteArray(data) {
        this.writeInt(data.length);
        const newBuffer = Buffer.alloc(this.buffer.length + data.length);
        this.buffer.copy(newBuffer);
        data.copy(newBuffer, this.buffer.length);
        this.buffer = newBuffer;
    }

    writeTag(tagType, name) {
        this.writeByte(tagType);
        this.writeString(name);
    }
}

// Create a simple 3x3x3 schematic with stone blocks
function createSimpleSchematic() {
    const writer = new NBTWriter();

    // Compound tag (root)
    writer.writeTag(10, 'Schematic');

    // Version (Int)
    writer.writeTag(3, 'Version');
    writer.writeInt(2);

    // DataVersion (Int) - Minecraft 1.21 uses 3700
    writer.writeTag(3, 'DataVersion');
    writer.writeInt(3700);

    // Width (Short)
    writer.writeTag(2, 'Width');
    writer.writeShort(3);

    // Height (Short)
    writer.writeTag(2, 'Height');
    writer.writeShort(3);

    // Length (Short)
    writer.writeTag(2, 'Length');
    writer.writeShort(3);

    // Palette (Compound)
    writer.writeTag(10, 'Palette');

    // Palette max value (Int)
    writer.writeTag(3, 'minecraft:air');
    writer.writeInt(0);

    writer.writeTag(3, 'minecraft:stone');
    writer.writeInt(1);

    // End palette tag
    writer.writeByte(0);

    // BlockData (Byte Array)
    // 3x3x3 = 27 blocks
    const blockData = Buffer.alloc(27);
    // Fill with stone (1) except air in center
    for (let i = 0; i < 27; i++) {
        blockData.writeUInt8(1, i);
    }
    // Center block is air
    blockData.writeUInt8(0, 13);

    writer.writeTag(7, 'BlockData');
    writer.writeByteArray(blockData);

    // End root tag
    writer.writeByte(0);

    return writer.buffer;
}

// Create schematic
const nbtData = createSimpleSchematic();

// Compress with GZIP
const gzipped = zlib.gzipSync(nbtData);

// Write to file
fs.writeFileSync('c:/Users/samy7/AppData/Roaming/.minecraft/build.schem', gzipped);

console.log('✅ Created build.schem (3x3x3 stone structure)');
console.log('Location: c:/Users/samy7/AppData/Roaming/.minecraft/build.schem');
