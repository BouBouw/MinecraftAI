# Minecraft AI - Reinforcement Learning System

Une IA 100% autonome qui apprend à jouer à Minecraft en mode survival grâce au Reinforcement Learning, avec un système de mémoire complet et découverte autonome des crafts.

## 🏗️ Architecture

```
Minecraft (Fabric Mod) ←→ AI Coordinator (Node.js) ←→ Mineflayer Bot (Node.js)
                                              ↓
                                        RL Bridge Server
                                              ↓
                                   Python RL Agent (PPO)
                                              ↓
                            ┌─────────────────────────────────┐
                            │  Systèmes d'Apprentissage       │
                            │  - Mémoire (4 types)            │
                            │  - Découverte de Crafts         │
                            │  - Curriculum Learning          │
                            └─────────────────────────────────┘
```

## 📁 Structure

```
/llm/
├── python/                    # Code Python RL
│   ├── gym_env/              # Environnement Gymnasium
│   │   ├── minecraft_env.py  # Environnement principal
│   │   ├── observations.py   # Espace d'observation
│   │   ├── actions.py        # Espace d'action
│   │   └── rewards.py        # Système de récompense
│   ├── memory/               # Système de mémoire (TODO)
│   ├── crafting/             # Découverte de crafts (TODO)
│   ├── agents/               # Agent PPO (TODO)
│   └── utils/                # Utilitaires (config, logger)
├── node/                     # Code Node.js
│   └── bridge-server.js      # Serveur de communication
├── config/
│   └── rl_config.yaml        # Configuration complète
└── data/                     # Données persistantes
    ├── memories/             # Base SQLite
    ├── experiences/          # Replay buffers
    └── models/               # Modèles entraînés
```

## 🚀 Installation

### Prérequis

- Python 3.10+
- Node.js 18+
- Minecraft avec Fabric mod
- SQLite 3

### Dépendances Python

```bash
pip install gymnasium
pip install stable-baselines3
pip install torch
pip install numpy
pip install pyyaml
pip install websockets
pip install tensorboard
pip install sentence-transformers  # Pour la mémoire sémantique
```

### Dépendances Node.js

```bash
cd llm/node
npm install ws
```

## 🎮 Utilisation

### 1. Démarrer le serveur Minecraft

Lancez votre serveur Minecraft avec le fabric mod.

### 2. Démarrer l'AI Coordinator

```bash
cd ai-coordinator
npm start
```

### 3. Démarrer le Bridge Server

```bash
cd llm/node
node bridge-server.js
```

Le bridge serveur écoutera sur le port 8765.

### 4. Lancer l'entraînement

```bash
cd llm/python
python training/trainer.py --config ../config/rl_config.yaml
```

## 📊 Monitoring

### TensorBoard

```bash
tensorboard --logdir llm/data/logs/tensorboard
```

Ouvrez http://localhost:6006 dans votre navigateur.

### Logs

Les logs sont sauvegardés dans `llm/data/logs/minecraft_rl.log`.

### Base de données SQLite

```bash
sqlite3 llm/data/memories/minecraft_rl.db
```

Requêtes utiles :
```sql
-- Voir toutes les mémoires
SELECT * FROM long_term_memory ORDER BY timestamp DESC LIMIT 10;

-- Voir les épisodes
SELECT * FROM episodes ORDER BY start_time DESC LIMIT 10;

-- Voir les recettes découvertes
SELECT * FROM discovered_recipes ORDER BY discovered_at DESC;
```

## 🧠 Fonctionnalités

### 1. Système de Mémoire Complet

- **Mémoire à Court Terme** : Dernières 1000 actions/observations
- **Mémoire à Long Terme** : Stockage persistant SQLite
- **Mémoire Épisodique** : Événements marquants (mort, découvertes)
- **Mémoire Sémantique** : Concepts et règles Minecraft

### 2. Découverte Autonome de Crafts

- Expérimentation intelligente des combinaisons
- Apprentissage par similarité (bois → planches)
- Base de données des recettes découvertes
- Inférence de nouveaux crafts

### 3. Curriculum Learning

1. **Basique** (0-10k steps) : Déplacement
2. **Collecte** (10k-50k) : Minage
3. **Crafting** (50k-100k) : Découverte des crafts
4. **Survie** (100k-500k) : Survivre la nuit
5. **Construction** (500k+) : Bâtir des abris

### 4. Architecture PPO

- Actor-Critic avec 512 neurones cachés
- Replay buffer pour l'efficacité
- Reward shaping par curriculum
- Embeddings pour la mémoire sémantique

## ⚙️ Configuration

Éditez `llm/config/rl_config.yaml` pour configurer :

- Paramètres de l'agent (learning rate, gamma, etc.)
- Configuration du curriculum
- Système de récompense
- Paramètres de mémoire
- Logs et checkpointing

## 📈 Progression

L'IA progresse à travers ces étapes :

1. Apprend à se déplacer sans tomber
2. Apprend à miner des blocs
3. Découvre des crafts par expérimentation
4. Survive aux mobs et à la nuit
5. Construit des abris et structures

## 🔧 Développement

### Tests

```bash
# Tests unitaires
pytest llm/python/memory/test_memory.py
pytest llm/python/crafting/test_craft_discovery.py

# Test d'intégration
pytest llm/python/tests/test_integration.py
```

### Ajouter de nouvelles actions

Éditez `llm/python/gym_env/actions.py` et `llm/node/bridge-server.js`.

### Modifier les récompenses

Éditez `llm/python/gym_env/rewards.py`.

## 📝 Plan d'Implémentation

- ✅ **Phase 1**: Infrastructure de base
- 🔄 **Phase 2**: Environnement RL complet
- ⏳ **Phase 3**: Système de Mémoire
- ⏳ **Phase 4**: Craft Discovery
- ⏳ **Phase 5**: Agent PPO
- ⏳ **Phase 6**: Curriculum Training
- ⏳ **Phase 7**: Intégration

## 🤝 Contribution

Ce projet est en développement actif. Les contributions sont les bienvenues !

## 📄 Licence

MIT

---

**Note**: Ce système utilise l'architecture existante de MinecraftAI et s'intègre avec l'AI Coordinator et le bot Mineflayer.
