# Minecraft AI Bot Bridge

Serveur WebSocket pour connecter le training RL Python au bot Minecraft.

## 🚀 Usage

### Sur le VPS - Démarrage 24/7

```bash
cd ~/MinecraftAI/minecraft-bot

# Une seule fois - setup avec systemd
chmod +x start-24-7.sh bridge-control.sh
sudo bash start-24-7.sh
```

### Contrôle

```bash
./bridge-control.sh status   # Statut
./bridge-control.sh logs     # Logs
./bridge-control.sh restart  # Redémarrer
./bridge-control.sh stop     # Arrêter
```

## 📁 Configuration

Le fichier `.env` contient:
- `MC_HOST` - IP du serveur Minecraft
- `MC_PORT` - Port Minecraft
- `MC_USERNAME` - Nom du bot
- `WS_PORT` - Port WebSocket (défaut: 8765)

## 📊 Ports

- **8765** - WebSocket (Python ↔ Bot)
- **3000** - HTTP (health checks)

---

**Simple et efficace pour le training RL 24/7**
