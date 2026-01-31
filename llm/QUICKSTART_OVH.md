# 🚀 Démarrage Rapide - Minecraft RL IA sur OVH

## 🎯 En 3 Minutes Chrono

```bash
# 1. Connexion au serveur
ssh root@your-ovh-server

# 2. Télécharger et lancer (ONE-COMMAND)
cd /opt
curl -fsSL https://raw.githubusercontent.com/your-repo/MinecraftAI/main/llm/deploy_ovh.sh -o deploy.sh && chmod +x deploy.sh && ./deploy.sh
```

---

## 📋 Déploiement Complet (10 minutes)

### 1. Connexion au serveur
```bash
ssh root@your-ovh-server
```

### 2. Mise à jour système
```bash
apt update && apt upgrade -y
apt install -y python3 python3-venv python3-pip nodejs npm git curl htop
```

### 3. Upload du projet
```bash
# Depuis votre machine locale :
cd C:\Users\samy7\Documents\GitHub\MinecraftAI

# Via SCP (Git Bash ou PowerShell)
scp -r . root@your-ovh-server:/opt/MinecraftAI/

# Via rsync (plus rapide)
rsync -avz --exclude 'node_modules' --exclude 'venv' \
    --exclude '.git' --exclude '__pycache__' \
    /c/Users/samy7/Documents/GitHub/MinecraftAI/ \
    root@your-ovh-server:/opt/MinecraftAI/
```

### 4. Installation rapide
```bash
cd /opt/MinecraftAI

# Script de déploiement
chmod +x llm/deploy_ovh.sh
./llm/deploy_ovh.sh
```

---

## 🚀 Démarrer l'IA

### Option 1 : Tout démarrer (recommandé)
```bash
cd /opt/MinecraftAI
./llm/start-production.sh start
```

### Option 2 : Auto-restart (recommandé pour 24/7)
```bash
cd /opt/MinecraftAI
./llm/start-production.sh auto-start
```

---

## 📊 Surveillance

### Voir le statut
```bash
cd /opt/MinecraftAI
./llm/monitor.sh
```

### Monitoring temps réel
```bash
cd /opt/MinecraftAI
./llm/monitor.sh --live
```

### TensorBoard (depuis votre PC)
```bash
# SSH tunnel pour TensorBoard
ssh -L 6006:localhost:6006 root@your-ovh-server

# Ouvrir : http://localhost:6006
```

---

## 🛑 Arrêter / Redémarrer

```bash
cd /opt/MinecraftAI

# Arrêter tout
./llm/start-production.sh stop

# Redémarrer
./llm/start-production.sh restart
```

---

## 📈 Progression Attendue

| Durée | Steps | Phase | Accomplissements |
|-------|-------|-------|------------------|
| 24h | ~1M | Mouvement | Se déplace correctement |
| 3 jours | ~10M | Collecte | Mine efficacement, 5+ crafts |
| 7 jours | ~25M | Crafting | 20+ crafts, construit des abris |
| 14 jours | ~50M | Survie | Survit aux mobs, strategies avancées |
| 30 jours | ~100M | Maître | IA quasi-autonome, 50+ crafts |

---

## 🔧 Personnalisation

### Modifier la durée d'entraînement
```bash
# 50M steps au lieu de 100M
./llm/start-production.sh start --steps 50000000
```

### Configuration avancée
```bash
# Éditer la configuration
nano llm/config/rl_config.yaml

# Redémarrer avec la nouvelle config
./llm/start-production.sh restart
```

---

## 💾 Sauvegardes

### Sauvegarde automatique
```bash
# Les checkpoints sont dans :
ls -lh llm/data/models/

# Base de données :
ls -lh llm/data/memories/
```

### Sauvegarde manuelle
```bash
# Tout sauvegarder
tar -czf minecraft_ai_backup_$(date +%Y%m%d_%H%M%S).tar.gz \
    llm/data/ \
    venv/ \
    ai-coordinator/node_modules/

# Télécharger sur votre machine
scp root@your-ovh-server:/opt/MinecraftAI/minecraft_ai_backup_*.tar.gz .
```

---

## 🐛 Résolution de Problèmes

### Le bot ne bouge pas
```bash
# Vérifier les services
./llm/monitor.sh

# Voir les logs
tail -50 llm/data/logs/training.log
```

### Serveur lent
```bash
# Vérifier la charge
htop

# Tuer processus si nécessaire
killall python
./llm/start-production.sh restart
```

### Plein disque
```bash
# Nettoyer les vieux checkpoints
cd llm/data/models
ls -t model_step_*.pt | tail -n +6 | xargs rm -f

# Nettoyer les logs
find llm/data/logs -name "*.log" -mtime +3 -delete
```

---

## 📞 Aide

### Logs importants
```bash
llm/data/logs/training.log      # Entraînement
llm/data/logs/bridge.log         # Bridge
llm/data/logs/coordinator.log    # AI Coordinator
llm/data/logs/tensorboard/      # TensorBoard logs
```

### Support rapide
```bash
# Statut complet
./llm/monitor.sh --stats

# Erreurs récentes
./llm/monitor.sh --errors

# Processus actifs
ps aux | grep -E "python|node|train"
```

---

## ✅ Vérification

```bash
# Vérifier que tout tourne
./llm/monitor.sh

# Doit afficher :
# ✓ Bridge Server: RUNNING
# ✓ AI Coordinator: RUNNING
# ✓ RL Training: RUNNING
# ✓ TensorBoard: RUNNING
```

---

**🎉 Félicitations ! Votre IA Minecraft apprend maintenant 24/7 !**

Surveillez la progression via TensorBoard : http://localhost:6006
