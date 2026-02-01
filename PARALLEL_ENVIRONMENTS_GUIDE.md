# 🚀 Guide: Lancer les Environnements Parallèles

## ⚡ Quick Start

### 1. Lancer les 8 serveurs WebSocket

```bash
./minecraft-bot/launch-parallel-bridges.sh
```

Cela va lancer **8 bots Minecraft simultanés** sur les ports 8765-8772.

### 2. Vérifier que tout fonctionne

```bash
./minecraft-bot/check-bridges.sh
```

Vous devriez voir :
```
✅ Port 8765: RUNNING (PID: XXXX)
✅ Port 8766: RUNNING (PID: XXXX)
...
📊 Summary:
   Running: 8/8
```

### 3. Lancer l'entraînement

```bash
cd llm/python
python train.py --config ../config/rl_config.yaml
```

### 4. Arrêter tout quand vous avez fini

```bash
./minecraft-bot/stop-parallel-bridges.sh
```

---

## 📋 Détails

### Ce que fait le script de lancement

1. **Crée les répertoires** `logs/` et `pids/`
2. **Nettoie** les serveurs existants sur les ports 8765-8772
3. **Lance 8 serveurs** avec:
   - **Ports différents**: 8765, 8766, 8767, ..., 8772
   - **Noms de bots uniques**: RLAgent_1, RLAgent_2, ..., RLAgent_8
   - **Fichiers log séparés**: `logs/bridge-8765.log`, etc.

### Choisir le nombre de serveurs

Par défaut, 8 serveurs sont lancés. Pour changer ça :

```bash
# Lancer seulement 4 serveurs
NUM_SERVERS=4 ./minecraft-bot/launch-parallel-bridges.sh

# Lancer 16 serveurs (si votre machine peut gérer)
NUM_SERVERS=16 ./minecraft-bot/launch-parallel-bridges.sh
```

### Changer les ports

```bash
# Utiliser les ports 9000-9007
BASE_PORT=9000 ./minecraft-bot/launch-parallel-bridges.sh
```

### Changer le serveur Minecraft

```bash
# Se connecter à un autre serveur Minecraft
MC_HOST=192.168.1.100 MC_PORT=25565 ./minecraft-bot/launch-parallel-bridges.sh
```

---

## 📊 Voir les Logs

### Voir tous les logs en temps réel

```bash
# Dans un terminal séparé
tail -f logs/bridge-*.log
```

### Voir un log spécifique

```bash
# Log du serveur 1 (port 8765)
tail -f logs/bridge-8765.log

# Log du serveur 5 (port 8769)
tail -f logs/bridge-8769.log
```

### Chercher des erreurs

```bash
grep -i error logs/bridge-*.log
```

---

## 🛑 Gestion des Serveurs

### Vérifier le statut

```bash
./minecraft-bot/check-bridges.sh
```

Sortie exemple :
```
🔍 Checking Parallel RL Bridge Servers Status...
==============================================
  ✅ Port 8765: RUNNING (PID: 12345)
  ✅ Port 8766: RUNNING (PID: 12346)
  ✅ Port 8767: RUNNING (PID: 12347)
  ✅ Port 8768: RUNNING (PID: 12348)
  ✅ Port 8769: RUNNING (PID: 12349)
  ✅ Port 8770: RUNNING (PID: 12350)
  ✅ Port 8771: RUNNING (PID: 12351)
  ✅ Port 8772: RUNNING (PID: 12352)

==============================================
📊 Summary:
   Running: 8/8
   Stopped: 0/8

✅ All servers are running!
```

### Arrêter tous les serveurs

```bash
./minecraft-bot/stop-parallel-bridges.sh
```

### Redémarrer un serveur spécifique

```bash
# Arrêter le serveur sur le port 8766
kill $(cat pids/bridge-8766.pid)

# Le relancer
MC_USERNAME="RLAgent_2" WS_PORT=8766 node minecraft-bot/rl-bridge-server.js &
```

---

## 🔧 Dépannage

### Problème: "Port already in use"

**Cause**: Un serveur est déjà en cours sur ce port

**Solution**:
```bash
# Arrêter tous les serveurs
./minecraft-bot/stop-parallel-bridges.sh

# Les relancer
./minecraft-bot/launch-parallel-bridges.sh
```

### Problème: "Cannot connect to Minecraft"

**Cause**: Le serveur Minecraft n'est pas accessible

**Solution**:
1. Vérifier que le serveur Minecraft est en ligne
2. Vérifier les paramètres MC_HOST et MC_PORT
3. Vérifier les logs: `tail -f logs/bridge-8765.log`

### Problème: Trop de RAM utilisée

**Cause**: 8 bots Minecraft + 8 serveurs WebSocket = beaucoup de mémoire

**Solution**:
```bash
# Réduire à 4 serveurs
NUM_SERVERS=4 ./minecraft-bot/launch-parallel-bridges.sh
```

Et mettre à jour la config :
```yaml
# Dans llm/config/rl_config.yaml
training:
  parallel_envs:
    num_envs: 4  # Au lieu de 8
```

---

## 🎓 Comprendre l'Architecture

```
┌─────────────────────────────────────────────────────────┐
│                   Python Training                       │
│                 (llm/python/train.py)                   │
└────────────────────┬────────────────────────────────────┘
                     │
        ┌────────────┴────────────┐
        │                         │
        ▼                         ▼
┌──────────────┐          ┌──────────────┐
│   Bridge 1   │          │   Bridge 2   │
│   Port 8765  │    ...   │   Port 8766  │
│   Bot: RLA_1 │          │   Bot: RLA_2 │
└──────┬───────┘          └──────┬───────┘
       │                         │
       └────────────┬────────────┘
                    ▼
         ┌────────────────────┐
         │  Minecraft Server  │
         │  (MC_HOST:MC_PORT) │
         └────────────────────┘
```

Chaque bridge :
1. Connecte un bot Minecraft au serveur
2. Expose une API WebSocket sur un port unique
3. Permet à Python de contrôler le bot
4. Envoie les observations reçues du bot

---

## 💻 Configuration Requise

**Minimum** :
- 4GB RAM
- 2 CPU cores
- 8 bots = 4 serveurs

**Recommandé** :
- 16GB RAM
- 8+ CPU cores
- 8 bots = 8 serveurs

**Optimal** :
- 32GB RAM
- 16+ CPU cores
- 16+ bots

---

## 📈 Performance

| # Serveurs | Vitesse d'Apprentissage | RAM Utilisée |
|-----------|-------------------------|--------------|
| 1         | 1x (baseline)           | ~500MB       |
| 4         | 4x                      | ~2GB         |
| 8         | 8x                      | ~4GB         |
| 16        | 16x                     | ~8GB         |

---

## ✅ Checklist

Avant de lancer l'entraînement :

- [ ] Serveur Minecraft accessible
- [ ] Scripts exécutables (`chmod +x *.sh`)
- [ ] Ports 8765-8772 disponibles
- [ ] RAM suffisante (4GB+ pour 8 serveurs)
- [ ] Configuration Python à jour (`num_envs: 8`)

---

## 🎉 Vous êtes Prêt !

Lancez maintenant :

```bash
# 1. Démarrer les 8 bots
./minecraft-bot/launch-parallel-bridges.sh

# 2. Vérifier que tout fonctionne
./minecraft-bot/check-bridges.sh

# 3. Lancer l'entraînement ultra-rapide
cd llm/python
python train.py --config ../config/rl_config.yaml
```

**Votre bot va maintenant apprendre 8x plus vite !** 🚀
