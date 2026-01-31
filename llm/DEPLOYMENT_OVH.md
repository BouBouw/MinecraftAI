# 🚀 Guide de Déploiement OVH - Minecraft RL IA 24/7

## 📋 Prérequis

- **Serveur OVH** :
  - 60 Go RAM ✅
  - 16 vCores ✅
  - 400 Go SSD ✅
  - 1000 Mbit/s ✅

- **Logiciels nécessaires** :
  - Python 3.10+
  - Node.js 18+
  - Minecraft Server (avec Fabric mod)
  - Mineflayer bot

---

## 🛠️ Étape 1 : Connexion au serveur

```bash
# SSH vers votre serveur OVH
ssh root@your-ovh-server

# Mettre à jour le système
apt update && apt upgrade -y

# Installer les dépendances de base
apt install -y python3 python3-venv python3-pip nodejs npm sqlite3 git curl wget htop
```

---

## 📦 Étape 2 : Télécharger le projet

```bash
# Cloner le projet (ou utiliser votre méthode préférée)
cd /opt
git clone https://github.com/votre-username/MinecraftAI.git
cd MinecraftAI

# OU uploader via SCP/Rsync depuis votre machine locale
# rsync -avz ./MinecraftAI root@your-ovh-server:/opt/MinecraftAI/
```

---

## 🔧 Étape 3 : Installation rapide

```bash
# Se rendre dans le projet
cd /opt/MinecraftAI

# Rendre les scripts exécutables
chmod +x llm/*.sh
chmod +x llm/monitor.sh

# Créer l'environnement Python
cd llm/python
python3 -m venv ../../venv
source ../../venv/bin/activate

# Installer les dépendances Python
pip install -r requirements.txt

# Installer les dépendances Node.js (pour AI Coordinator)
cd ../../ai-coordinator
npm install
```

---

## 🎮 Étape 4 : Démarrer Minecraft Server

```bash
# Option 1: Utiliser un serveur Minecraft existant
# (installer le Fabric mod et configurer)

# Option 2: Démarrer un serveur local pour tests
cd /opt
wget https://launcher.mojang.com/v1/objects/8a30bed532c0bbe226f9e8f5e9fb63c3d04f6/server.jar
java -Xmx4G -Xms4G -jar server.jar nogui

# Ou utiliser votre propre configuration
```

---

## 🚀 Étape 5 : Démarrer l'IA (Production)

```bash
cd /opt/MinecraftAI

# Démarrer tous les services
./llm/start-production.sh start
```

Cela va démarrer :
- ✅ Bridge Server (port 8765)
- ✅ AI Coordinator
- ✅ RL Training (100M steps)
- ✅ TensorBoard (port 6006)

---

## 📊 Étape 6 : Monitoring

### Sur le serveur (SSH)
```bash
# Voir le statut en temps réel
./llm/monitor.sh

# Monitoring continu (rafraîchit toutes les 5s)
./llm/monitor.sh --live
```

### Depuis votre machine locale
```bash
# Accéder à TensorBoard via SSH tunnel
ssh -L 6006:localhost:6006 root@your-ovh-server

# Puis ouvrir dans le navigateur
http://localhost:6006
```

---

## 🎯 Commandes Utiles

### Gestion des services
```bash
# Voir le statut
./llm/start-production.sh status

# Arrêter tout
./llm/start-production.sh stop

# Redémarrer
./llm/start-production.sh restart

# Voir les logs
./llm/start-production.sh logs
```

### Monitoring
```bash
# Statistiques détaillées
./llm/monitor.sh --stats

# Voir les checkpoints
./llm/monitor.sh --checkpoints

# Voir les erreurs récentes
./llm/monitor.sh --errors
```

### Entraînement personnalisé
```bash
# 50M steps au lieu de 100M
./llm/start-production.sh start --steps 50000000

# Sans TensorBoard
./llm/start-production.sh start --no-tb
```

---

## 📈 Optimisations pour 24/7

### CPU (16 cœurs)
```bash
# Le script configure automatiquement :
- OMP_NUM_THREADS=16
- MKL_NUM_THREADS=16
- OPENBLAS_NUM_THREADS=16
```

### Mémoire (60 Go RAM)
```bash
# La configuration utilise :
- Batch size: 256 (optimisé)
- Short-term memory: 10,000 transitions
- Pas de limite de mémoirelong terme
```

### Stockage (400 Go SSD)
```bash
# Points à surveiller :
# - Models: ~500MB par checkpoint
# - Logs: Limite à 50MB par fichier
# - Database: Croît avec le temps

# Surveillance
df -h
```

### Auto-restart en cas de crash
```bash
# Lancer avec auto-restart
./llm/start-production.sh auto-start
```

Cela redémarre automatiquement l'entraînement si :
- Crash Python
- Erreur mémoire
- Problème réseau
- (jusqu'à 10 tentatives)

---

## 🔍 Surveillance

### Vérifier que tout tourne
```bash
./llm/monitor.sh
```

Doit afficher :
```
✓ Bridge Server: RUNNING (PID: 12345)
✓ AI Coordinator: RUNNING (PID: 12346)
✓ RL Training: RUNNING (PID: 12347)
✓ TensorBoard: RUNNING (PID: 12348)
```

### Logs en temps réel
```bash
# Terminal 1 : Logs d'entraînement
tail -f llm/data/logs/training.log

# Terminal 2 : Logs système
tail -f llm/data/logs/bridge.log
tail -f llm/data/logs/coordinator.log
```

---

## 📊 Résultats Attendus

### Court terme (24h ~1M steps)
- ✅ Apprend à se déplacer sans tomber
- ✅ Mine efficacement les premiers blocs
- ✅ A découvert 5-10 crafts de base

### Moyen terme (3-7 jours ~10M steps)
- ✅ Maîtrise complète du déplacement
- ✅ 20+ crafts découverts
- ✅ Survie à plusieurs nuits
- ✅ Commence à construire des abris

### Long terme (2-4 semaines ~100M steps)
- ✅ IA quasi-autonome
- ✅ 50+ crafts découverts
- ✅ Construction de structures complexes
- ✅ Stratégies avancées de survie

---

## 🛡️ Sécurité et Maintenance

### Sauvegardes automatiques
```bash
# Les checkpoints sont sauvegardés dans :
llm/data/models/model_step_*.pt

# Base de données SQLite :
llm/data/memories/minecraft_rl.db

# Sauvegarde manuelle
tar -czf minecraft_ai_backup_$(date +%Y%m%d).tar.gz \
    llm/data/ \
    venv/
    ai-coordinator/node_modules/
```

### Nettoyer les vieux logs
```bash
# Logs de plus de 7 jours
find llm/data/logs/ -name "*.log" -mtime +7 -delete

# Anciens checkpoints (garder les 5 plus récents)
cd llm/data/models
ls -t model_step_*.pt | tail -n +6 | xargs rm -f
```

---

## 🎛️ Résolution de Problèmes

### Le bot se connecte mais ne bouge pas
```bash
# Vérifier que le bot est en mode créatif
# Vérifier les logs dans : llm/data/logs/training.log
```

### Erreur "CUDA out of memory"
```bash
# Sur CPU, changer dans rl_config_ovh.yaml :
device: cpu  # (pas cuda)
```

### Le bot crash souvent
```bash
# Voir les erreurs :
./llm/monitor.sh --errors

# Redémarrer avec auto-restart :
./llm/start-production.sh auto-start
```

### Disque plein
```bash
# Nettoyer les vieux checkpoints
cd llm/data/models
ls -t model_step_*.pt | tail -n +6 | xargs rm -f

# Nettoyer les logs
find llm/data/logs/ -name "*.log" -mtime +3 -delete
```

---

## 🎉 Prochaines Étapes

Une fois l'IA entraînée :

1. **Exporter le modèle** entraîné
2. **Partager la base de données** des crafts découverts
3. **Créer des vidéos** de l'IA en action
4. **Publier les résultats** (paper, GitHub)

---

## 📞 Support

En cas de problème :
1. Voir les logs : `./llm/monitor.sh --errors`
2. Vérifier le statut : `./llm/monitor.sh --stats`
3. Redémarrer : `./llm/start-production.sh restart`

---

**Bonne chance avec votre IA Minecraft 24/7 ! 🚀🤖✨**
