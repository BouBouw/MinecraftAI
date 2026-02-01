# 🎬 Twitch Streaming - VPS Headless Setup

**Stream 24/7 depuis votre VPS vers Twitch - Sans PC allumé !**

## 🚀 Installation Rapide (2 minutes)

### 1. Créer le dossier et la config

```bash
# Sur votre VPS
mkdir -p ~/minecraft-stream/logs
cd ~/MinecraftAI/minecraft-bot
```

### 2. Créer le fichier de configuration

```bash
nano ~/minecraft-stream/.env
```

Coller ceci (remplacer YOUR_KEY par votre vraie clé):

```bash
# Stream Configuration
STREAM_RESOLUTION=1280x720
STREAM_FPS=30
STREAM_BITRATE=3000k

# Twitch Stream Key
TWITCH_STREAM_KEY=live_1234567890_ABCDEFGHIJ
```

**Pour trouver votre clé Twitch:** https://dashboard.twitch.tv/votre-username/stream/key

### 3. Rendre le script exécutable

```bash
chmod +x ~/MinecraftAI/minecraft-bot/start-twitch-stream.sh
```

### 4. Démarrer le stream

```bash
bash ~/MinecraftAI/minecraft-bot/start-twitch-stream.sh
```

### 5. Vérifier que ça marche

```bash
ps aux | grep ffmpeg
```

Vous devriez voir un processus ffmpeg qui tourne.

## 📺 Commandes Utiles

```bash
# Démarrer le stream
bash ~/MinecraftAI/minecraft-bot/start-twitch-stream.sh

# Arrêter le stream
pkill -f 'ffmpeg.*rtmp'

# Voir les logs
tail -f ~/minecraft-stream/logs/ffmpeg.log

# Vérifier le statut
ps aux | grep ffmpeg
```

## ⚙️ Paramètres de Qualité

Éditez `~/minecraft-stream/.env`:

```bash
# 1080p @ 30fps (nécessite ~5 Mbps upload)
STREAM_RESOLUTION=1920x1080
STREAM_FPS=30
STREAM_BITRATE=4500k

# 720p @ 30fps (recommandé, ~3 Mbps upload)
STREAM_RESOLUTION=1280x720
STREAM_FPS=30
STREAM_BITRATE=3000k

# 720p @ 60fps (~4.5 Mbps upload)
STREAM_RESOLUTION=1280x720
STREAM_FPS=60
STREAM_BITRATE=4500k

# 480p @ 30fps (bas débit, ~1.5 Mbps upload)
STREAM_RESOLUTION=854x480
STREAM_FPS=30
STREAM_BITRATE=1500k
```

## 🖥️ Actuel: Pattern de Test

Le stream affiche actuellement un écran noir avec un overlay texte:

```
🤖 Minecraft AI Bot Training

🎓 Training RL agent to play Minecraft
📊 Episode: N/A | Reward: N/A
📈 Stage: gathering (basic)

⏳ Training 24/7 on VPS

Powered by: PPO + Curriculum Learning
```

## 🎯 Pour Avoir le VRAI POV du Bot

Pour streamer le vrai gameplay du bot, il faut implémenter la capture de screenshots.

**Option 1: Rapide (test pattern actuel)**
- ✅ Fonctionne maintenant
- ✅ Pas de charge CPU supplémentaire
- ❌ Pas de vrai gameplay

**Option 2: Vrai POV (à implémenter)**
- ✅ Vrai gameplay du bot
- ✅ Plus intéressant à regarder
- ❌ CPU intensive (encodage screenshots)
- ❌ Délai de 2-3 secondes

Pour implémenter le vrai POV, il faut:
1. Installer `prismarine-viewer` dans minecraft-bot
2. Capturer des screenshots régulièrement
3. Les encoder en vidéo avec ffmpeg

## 🐛 Dépannage

### Le stream ne démarre pas

```bash
# Vérifier votre clé Twitch
cat ~/minecraft-stream/.env

# Vérifier que ffmpeg est installé
which ffmpeg

# Tester manuellement
ffmpeg -f lavfi -i testsrc -f flv rtmp://live.twitch.tv/app/VOTRE_CLE
```

### Qualité mauvaise / lag

```bash
# Réduire le bitrate dans .env
nano ~/minecraft-stream/.env
# Changez: STREAM_BITRATE=2000k
```

### Le stream coupe

Vérifiez votre connexion internet:
```bash
ping -c 10 twitch.tv
```

## 📊 Monitoring CPU/Mémoire

```bash
# Usage CPU
top

# Si CPU à 100%, réduire la qualité
STREAM_FPS=24
STREAM_BITRATE=2000k
```

## ✅ Checklist

- [ ] Clé Twitch configurée dans `.env`
- [ ] ffmpeg installé (`which ffmpeg`)
- [ ] Stream démarre sans erreur
- [ ] Stream visible sur Twitch
- [ ] CPU usage acceptable (< 80%)

---

**Besoin d'aide?** Vérifiez les logs: `tail -f ~/minecraft-stream/logs/ffmpeg.log`
