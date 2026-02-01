#!/bin/bash
# Installation rapide du streaming Twitch sur VPS

echo "🚀 Installation Twitch Streaming pour VPS"
echo "==========================================="
echo ""

# Vérifier ffmpeg
if ! command -v ffmpeg &> /dev/null; then
    echo "📦 Installation de ffmpeg..."
    sudo apt-get update -y
    sudo apt-get install -y ffmpeg
else
    echo "✅ ffmpeg déjà installé"
fi

# Créer les dossiers
echo "📁 Création des dossiers..."
mkdir -p "$HOME/minecraft-stream/logs"
mkdir -p "$HOME/minecraft-stream/screenshots"

# Créer la configuration par défaut
if [ ! -f "$HOME/minecraft-stream/.env" ]; then
    echo "📝 Création de la configuration..."
    cat > "$HOME/minecraft-stream/.env" << 'EOF'
# Configuration du Stream
STREAM_RESOLUTION=1280x720
STREAM_FPS=30
STREAM_BITRATE=3000k

# Clé Twitch Stream (OBTENEZ-LA ICI: https://dashboard.twitch.tv/votre-username/stream/key)
TWITCH_STREAM_KEY=live_VOTRE_CLE_ICI
EOF
    echo "✅ Configuration créée"
else
    echo "✅ Configuration existe déjà"
fi

echo ""
echo "✅ Installation terminée!"
echo ""
echo "📝 PROCHAINE ÉTAPE:"
echo "==================="
echo "1. Obtenez votre clé Twitch ici:"
echo "   https://dashboard.twitch.tv/votre-username/stream/key"
echo ""
echo "2. Éditez la configuration:"
echo "   nano /home/server/minecraft-stream/.env"
echo "   Remplacez: live_VOTRE_CLE_ICI"
echo "   Par: live_1234567890_ABCDEFGHIJ"
echo ""
echo "3. Démarrez le stream:"
echo "   bash ~/MinecraftAI/minecraft-bot/start-twitch-stream.sh"
echo ""
