/**
 * Test script to verify bot reuse feature
 */
import WebSocket from 'ws';

console.log('🔍 Testing bot reuse...\n');

const ws = new WebSocket('ws://localhost:8080');
let messageCount = 0;

ws.on('open', () => {
    console.log('✅ Connected to Coordinator!');

    // Send second command - should reuse existing bot
    const testMessage = {
        type: 'bot_move_to_schematic',
        schematic_name: 'test2.schem',
        target_position: { x: 150, y: 70, z: 250 },
        dimensions: { width: 5, height: 4, length: 6 }
    };

    console.log('📤 Sending second command (should reuse bot):', testMessage);
    ws.send(JSON.stringify(testMessage));
});

ws.on('message', (data) => {
    const msg = JSON.parse(data.toString());
    console.log('📨 Message received:', msg);

    messageCount++;
    if (msg.type === 'bot_move_ack') {
        console.log('\n✅ Bot response:', msg.status);
        if (msg.status === 'redirecting') {
            console.log('🎉 SUCCESS! Bot is being reused (not recreated)');
        } else if (msg.status === 'connecting') {
            console.log('⚠️ Bot is being created (first time or was disconnected)');
        }
        setTimeout(() => ws.close(), 1000);
    }
});

ws.on('error', (error) => {
    console.error('❌ WebSocket error:', error.message);
    process.exit(1);
});

ws.on('close', () => {
    console.log('\n🔌 Connection closed');
    process.exit(0);
});

// Timeout after 5 seconds
setTimeout(() => {
    console.log('⏱️ Timeout');
    ws.close();
    process.exit(1);
}, 5000);
