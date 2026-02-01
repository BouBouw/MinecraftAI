# 🎬 Real Minecraft Bot POV Streaming

**Stream the ACTUAL bot gameplay to Twitch 24/7 !**

## 📦 Installation

### 1. Installer les dépendances Node.js

```bash
cd ~/MinecraftAI/minecraft-bot
npm install prismarine-viewer
```

### 2. Créer le dossier de screenshots

```bash
mkdir -p ~/minecraft-stream/screenshots
mkdir -p ~/minecraft-stream/logs
```

### 3. Configurer votre clé Twitch

```bash
nano ~/minecraft-stream/.env
```

```bash
STREAM_RESOLUTION=1280x720
STREAM_FPS=30
STREAM_BITRATE=3000k
TWITCH_STREAM_KEY=live_VOTRE_CLE_ICI
```

## 🚀 Démarrage

### Option 1: Stream complet (Vrai POV)

```bash
# 1. Arrêter l'ancien bridge server
pkill -f "rl-bridge-server"

# 2. Démarrer le nouveau serveur POV
cd ~/MinecraftAI/minecraft-bot
node rl-bridge-pov-server.js &

# 3. Attendre quelques secondes que les screenshots se génèrent
sleep 5

# 4. Démarrer le stream
bash ~/MinecraftAI/minecraft-bot/start-pov-stream.sh
```

### Option 2: Mode fallback (sans prismarine-viewer)

Si `prismarine-viewer` n'est pas installé, le serveur fonctionnera en mode fallback (observation data seulement).

## 📊 Vérification

```bash
# Vérifier les screenshots
ls -lh ~/minecraft-stream/screenshots/ | tail -10

# Compter les screenshots
ls -1 ~/minecraft-stream/screenshots/frame_*.jpg | wc -l

# Vérifier le stream
ps aux | grep ffmpeg

# Voir les logs
tail -f ~/minecraft-stream/logs/pov-stream.log
```

## 🔧 Paramètres

### Qualité d'image

Éditez `~/minecraft-stream/.env`:

```bash
# 1080p @ 30fps (haute qualité, CPU intensif)
STREAM_RESOLUTION=1920x1080
STREAM_FPS=30
STREAM_BITRATE=4500k

# 720p @ 30fps (recommandé)
STREAM_RESOLUTION=1280x720
STREAM_FPS=30
STREAM_BITRATE=3000k

# 720p @ 24fps (bas CPU)
STREAM_RESOLUTION=1280x720
STREAM_FPS=24
STREAM_BITRATE=2500k

# 480p @ 24fps (très léger)
STREAM_RESOLUTION=854x480
STREAM_FPS=24
STREAM_BITRATE=1500k
```

### Taux de capture de screenshots

Dans `rl-bridge-pov-server.js`, modifiez:

```javascript
const SCREENSHOT_INTERVAL = 100; // 10 FPS (par défaut)
// Pour plus de fluidité: 50ms = 20 FPS (plus CPU)
// Pour économiser du CPU: 200ms = 5 FPS (moins fluide)
```

## ⚠️ Notes importantes

### CPU Usage

Le streaming de vrais screenshots est **CPU intensive**:
- **1080p @ 30fps**: ~50-80% CPU
- **720p @ 30fps**: ~30-50% CPU
- **720p @ 24fps**: ~20-40% CPU

Si votre VPS est à 100% CPU:
- Réduire la résolution
- Réduire les FPS
- Arrêter le training pendant le stream

### Délai

Il y a un délai de **2-3 secondes** entre le jeu et le stream à cause de:
- Capture de screenshot
- Encodage JPEG
- Encodage vidéo ffmpeg
- Upload vers Twitch

C'est normal et acceptable pour du streaming.

### Stockage

Les screenshots temporaires occupent environ:
- **10 FPS**: ~50-100 MB pour 30 secondes
- Ils sont automatiquement nettoyés (gardés les 300 derniers = 30 sec)

## 🐛 Dépannage

### Pas de screenshots générés

```bash
# Vérifier que le serveur POV tourne
ps aux | grep rl-bridge-pov-server

# Vérifier les logs
# (Les logs sont dans la console du serveur POV)

# Réinstaller prismarine-viewer
cd ~/MinecraftAI/minecraft-bot
npm install prismarine-viewer
```

### Stream ne démarre pas

```bash
# Vérifier les screenshots
ls -1 ~/minecraft-stream/screenshots/frame_*.jpg | wc -l

# Si 0, attendez que le bot génère des screenshots

# Vérifier la clé Twitch
cat ~/minecraft-stream/.env
```

### CPU à 100%

```bash
# Arrêter le stream
pkill -f 'ffmpeg.*rtmp'

# Réduire la qualité
nano ~/minecraft-stream/.env
# Changez pour:
STREAM_RESOLUTION=854x480
STREAM_FPS=24
STREAM_BITRATE=1500k
```

### Image déformée

Le problème vient souvent de la taille des screenshots. Vérifiez que:
- La résolution dans `.env` matche la taille des screenshots
- Les screenshots sont bien 1280x720 ou 1920x1080

## 📈 Monitoring

### Surveiller en temps réel

```bash
# Terminal 1: Screenshots générés
watch -n 2 'ls -1 ~/minecraft-stream/screenshots/frame_*.jpg | wc -l'

# Terminal 2: Stream actif
ps aux | grep ffmpeg

# Terminal 3: CPU usage
htop
```

### Vérifier le stream sur Twitch

Allez sur votre chaîne Twitch: https://twitch.tv/votre_username

Vous devriez voir le **vrai gameplay du bot** en temps réel !

## 🎯 Prochaines étapes

Une fois que ça marche:

1. ✅ Ajuster la qualité selon votre CPU
2. ✅ Ajouter un overlay avec les stats d'entraînement
3. ✆ Automatiser le démarrage au boot du VPS
4. ✅ Ajouter des alerts pour les événements spéciaux

---

**Besoin d'aide?** Vérifiez toujours:
1. Le serveur POV tourne (`ps aux | grep rl-bridge-pov-server`)
2. Des screenshots existent (`ls ~/minecraft-stream/screenshots/`)
3. La clé Twitch est configurée (`cat ~/minecraft-stream/.env`)
