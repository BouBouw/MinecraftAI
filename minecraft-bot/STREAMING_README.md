# 🎬 Minecraft Bot Streaming Setup

**Stream 24/7 depuis votre VPS vers Twitch & TikTok en simultané - Sans PC allumé !**

## 📋 Prérequis

### VPS Recommandé:
- **CPU**: 4+ vCPUs (8+ recommandés pour encodage)
- **RAM**: 8GB+ (16GB recommandé)
- **Upload**: 10 Mbps+ minimum (20 Mbps+ pour 1080p)
- **OS**: Ubuntu 22.04 LTS

### Logiciels nécessaires:
```bash
sudo apt update
sudo apt install -y xvfb ffmpeg obs-studio pulseaudio
```

## 🚀 Installation Rapide

### 1. Exécuter le script d'installation

```bash
cd ~/MinecraftAI/minecraft-bot
chmod +x setup-vps-streaming.sh
sudo ./setup-vps-streaming.sh
```

### 2. Configurer les clés de stream

Éditer le fichier de configuration:
```bash
nano /home/server/minecraft-stream/.env
```

Ajouter vos clés:
```env
# Stream Configuration
STREAM_RESOLUTION=1920x1080
STREAM_FPS=30
STREAM_BITRATE=4500k

# Twitch Stream Key (Get from: https://dashboard.twitch.tv/u/username/stream/key)
TWITCH_ENABLED=true
TWITCH_STREAM_KEY=live_1234567890_ABCDEFGHIJ

# TikTok Stream Key (Use TikTok Live Studio app to get it)
TIKTOK_ENABLED=true
TIKTOK_STREAM_KEY=your_tiktok_stream_key
```

### 3. Démarrer le stream

```bash
# Méthode 1: Script de contrôle
/home/server/minecraft-stream/stream-control.sh start

# Méthode 2: Node.js manager
cd ~/MinecraftAI/minecraft-bot
node stream-manager.js start
```

### 4. Vérifier le statut

```bash
/home/server/minecraft-stream/stream-control.sh status
```

## 📺 Commandes Disponibles

### Contrôle du Stream

```bash
# Démarrer
/home/server/minecraft-stream/stream-control.sh start

# Arrêter
/home/server/minecraft-stream/stream-control.sh stop

# Statut
/home/server/minecraft-stream/stream-control.sh status

# Redémarrer
/home/server/minecraft-stream/stream-control.sh restart
```

### Logs

```bash
# Voir les logs en temps réel
tail -f /home/server/minecraft-stream/logs/bot.log

# Erreurs
tail -f /home/server/minecraft-stream/logs/bot-error.log
```

## 🔧 Architecture

```
Minecraft Server (151.241.161.51:25566)
         ↓
Mineflayer Bot (sur VPS)
         ↓
Virtual Display (Xvfb :99)
         ↓
ffmpeg / OBS (encodage)
         ↓
    ├─────────┤
    ↓         ↓
  Twitch   TikTok
```

## 💡 Optimisations

### Adapter la qualité à votre upload

```env
# 1080p @ 30fps (nécessite ~5 Mbps upload)
STREAM_RESOLUTION=1920x1080
STREAM_FPS=30
STREAM_BITRATE=4500k

# 720p @ 30fps (nécessite ~3 Mbps upload)
STREAM_RESOLUTION=1280x720
STREAM_FPS=30
STREAM_BITRATE=3000k

# 720p @ 60fps (nécessite ~4.5 Mbps upload)
STREAM_RESOLUTION=1280x720
STREAM_FPS=60
STREAM_BITRATE=4500k
```

### GPU Encoding (si GPU disponible)

Remplacer `-preset veryfast` par:
- NVIDIA GPU: `-vcodec h264_nvenc`
- AMD GPU: `-vcodec h264_amf`
- Intel GPU: `-vcodec h264_qsv`

## 🎨 Customisation

### Ajouter un overlay de stats

Le stream inclut automatiquement un overlay avec:
- Numéro d'épisode actuel
- Reward de l'épisode
- Stage du curriculum
- Temps d'entraînement

Pour personnaliser, éditer `stream-bot-viewer.js`.

### Ajouter un watermark

Placer votre image:
```bash
cp watermark.png /home/server/minecraft-stream/watermark.png
```

## 📊 Monitoring

### Vérifier l'utilisation CPU/Memory

```bash
htop
# ou
nvidia-smi  # Si GPU NVIDIA
```

### Vérifier l'upload en cours

```bash
iftop -i eth0
```

### Vérifier les processus actifs

```bash
ps aux | grep -E "ffmpeg|obs|mineflayer"
```

## 🐛 Dépannage

### Le stream ne démarre pas

```bash
# Vérifier que Xvfb tourne
systemctl status xvfb

# Vérifier que le bot est connecté
ps aux | grep stream-bot-viewer

# Tester le display virtuel
export DISPLAY=:99
xdpyinfo
```

### Qualité mauvaise / lag

```bash
# Réduire le bitrate dans .env
STREAM_BITRATE=3000k

# Réduire les FPS
STREAM_FPS=24
```

### Le stream coupe

```bash
# Vérifier la connexion internet
ping -c 10 twitch.tv

# Augmenter le buffer dans ffmpeg (éditer stream-manager.js)
'-bufsize', '18000k',  # Au lieu de 9000k
```

## 🔐 Sécurité

**NE JAMAIS COMMIT vos stream keys !**

Ajouter à `.gitignore`:
```
.env.stream
.env
/home/server/minecraft-stream/.env
```

## 📱 Liens Utiles

- **Twitch Stream Key**: https://dashboard.twitch.tv/u/username/stream/key
- **TikTok Stream Key**: Utiliser TikTok Live Studio app
- **RTMP URLs**:
  - Twitch: `rtmp://live.twitch.tv/app/`
  - TikTok: `rtmp://push.tiktok.com/live/`

## 🎯 Prochaines Étapes

1. ✅ Installation complète
2. ✅ Configuration des stream keys
3. ✅ Premier stream test
4. ⬜ Overlay personnalisé
5. ⬜ Chat bot intégré
6. ⬜ Alerts pour les dons/follows
7. ⬜ Multi-bot streaming (plusieurs bots sur le même stream)

---

**Support**: Si vous rencontrez des problèmes, vérifiez d'abord les logs dans `/home/server/minecraft-stream/logs/`
