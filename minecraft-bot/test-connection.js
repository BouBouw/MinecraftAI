/**
 * Script de test simple pour vérifier la connexion
 */
import mineflayer from 'mineflayer';

console.log('🔍 Test de connexion Minecraft...\n');

// Demander les infos de connexion
const host = process.env.MC_HOST || 'localhost';
const port = parseInt(process.env.MC_PORT) || 25565;
const username = process.env.MC_USERNAME || 'TestBot';

console.log(`📍 Hôte: ${host}:${port}`);
console.log(`👤 Nom du bot: ${username}`);
console.log(`\n⚠️  Assurez-vous d'avoir ouvert votre monde sur le réseau LAN !\n`);

const bot = mineflayer.createBot({
    host: host,
    port: port,
    username: username,
    auth: 'offline', // Mode offline
    version: false
});

bot.on('connect', () => {
    console.log('✅ Connexion au serveur réussie !');
});

bot.on('spawn', () => {
    console.log(`✅ Bot spawned !`);
    console.log(`   Position: ${bot.entity.position}`);
    console.log(`   Santé: ${bot.health}/20`);
    console.log(`   Mode: ${bot.game.gameMode}`);
    console.log('\n🎉 Le bot fonctionne ! Appuyez sur Ctrl+C pour arrêter.\n');
});

bot.on('error', (err) => {
    console.error('❌ Erreur de connexion:', err.message);
    console.error('\n💡 Solutions possibles:');
    console.error('   1. Vérifiez que Minecraft est ouvert');
    console.error('   2. Ouvrez votre monde sur le réseau LAN');
    console.error('   3. Vérifiez que le port dans .env correspond au port LAN\n');
    process.exit(1);
});

bot.on('end', () => {
    console.log('🔌 Bot déconnecté');
    process.exit(0);
});

// Gestion de l'arrêt propre
process.on('SIGINT', () => {
    console.log('\n\n🛑 Arrêt du bot...');
    bot.quit();
});
