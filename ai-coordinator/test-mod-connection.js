/**
 * Script de test pour vérifier que le coordinateur fonctionne
 */
import WebSocket from 'ws';

console.log('🔍 Test de connexion au Coordinateur...\n');

const ws = new WebSocket('ws://localhost:8080');

ws.on('open', () => {
    console.log('✅ Connecté au Coordinateur!');

    // Simuler un message du mod
    const testMessage = {
        type: 'bot_move_to_schematic',
        schematic_name: 'test.schem',
        target_position: { x: 100, y: 64, z: 200 },
        dimensions: { width: 3, height: 3, length: 3 }
    };

    console.log('📤 Envoi du message test:', testMessage);
    ws.send(JSON.stringify(testMessage));
});

ws.on('message', (data) => {
    const msg = JSON.parse(data.toString());
    console.log('📨 Message reçu:', msg);
});

ws.on('error', (error) => {
    console.error('❌ Erreur WebSocket:', error.message);
    console.error('\n💡 Assurez-vous que l\'AI Coordinator est démarré avec: npm start');
    process.exit(1);
});

ws.on('close', () => {
    console.log('🔌 Connexion fermée');
    process.exit(0);
});

// Timeout après 10 secondes
setTimeout(() => {
    console.log('⏱️ Timeout - aucun bot n\'a rejoint le serveur');
    console.log('\n💡 Vérifiez:');
    console.log('   1. L\'AI Coordinator est-il démarré? (npm start)');
    console.log('   2. Le port MC_PORT dans .env est-il correct?');
    console.log('   3. Le monde Minecraft est-il ouvert sur le réseau LAN?');
    ws.close();
    process.exit(1);
}, 10000);
