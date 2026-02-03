# 🤖 Agent Hybride RL + LLM pour Minecraft

Architecture combinant **Reinforcement Learning** et **LLM** pour créer un agent Minecraft intelligent.

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    AGENT HYBRIDE                        │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  ┌──────────────┐      ┌──────────────┐               │
│  │ PERCEPTEUR   │─────>│  RAISONNEUR  │               │
│  │ Minecraft →  │      │  (LLM)       │               │
│  │ Texte        │      │  Claude/GPT  │               │
│  └──────────────┘      └──────┬───────┘               │
│                                │                        │
│                                ▼                        │
│                        ┌──────────────┐               │
│                        │  EXÉCUTEUR   │               │
│                        │  LLM → RL    │               │
│                        └──────┬───────┘               │
│                               │                        │
│                               ▼                        │
│                        ┌──────────────┐               │
│                        │  Système RL  │               │
│                        │  (Existant)  │               │
│                        └──────────────┘               │
└─────────────────────────────────────────────────────────┘
```

## 📁 Structure

```
llm-agent/
├── percepteur/
│   └── minecraft_percepteur.js    # Data → Texte
├── raisonner/
│   └── llm_decision.py            # LLM Decision Maker
├── executeur/
│   └── action_executor.py         # LLM → Actions RL
└── hybrid_agent.py                # Chef d'orchestre
```

## 🚀 Installation

### 1. Dépendances Python

```bash
pip install anthropic aiohttp
```

### 2. Clé API (Optionnel)

**Option A: Z.ai (GLM-4) - Recommandé**

```bash
export ZAI_API_KEY="votre_clé_zai_ici"
```

Obtenez votre clé sur: https://open.bigmodel.cn/

**Modèles disponibles:**
- `glm-4` - Modèle standard (par défaut)
- `glm-4-plus` - Version améliorée
- `glm-4-air` - Modèle ultra-rapide

**Option B: Anthropic Claude**

```bash
export ANTHROPIC_API_KEY="votre_clé_anthropic_ici"
```

**Sans clé API** : Mode démo avec règles simples

## 🎮 Utilisation

### Lancer l'agent hybride

```bash
cd llm/python

# Avec Z.ai (GLM 4.7) - Recommandé
export ZAI_API_KEY="votre_clé"
python ../llm-agent/hybrid_agent.py --provider z.ai --objectif "Miner 5 blocs de fer" --steps 100

# Avec Claude (Anthropic)
export ANTHROPIC_API_KEY="votre_clé"
python ../llm-agent/hybrid_agent.py --provider anthropic --objectif "Miner 5 blocs de fer" --steps 100

# Mode démo (sans API)
python ../llm-agent/hybrid_agent.py --objectif "Survivre et manger quand faim < 10" --steps 200

# Exploration
python ../llm-agent/hybrid_agent.py --objectif "Explorer et trouver des minerais" --steps 150
```

### Options

```
--provider="z.ai"      Utiliser Z.ai GLM 4.7 (défaut)
--provider="anthropic"  Utiliser Claude Anthropic
--objectif="..."    Objectif de l'agent (défaut: "Survivre et explorer")
--config=...        Fichier de config (défaut: ../config/rl_config.yaml)
--steps=N          Nombre max d'étapes (défaut: 100)
```

## 🧠 Comment ça marche

### PHASE 1: PERCEPTION 📡

Le bot observe Minecraft et génère un rapport:

```
📍 POSITION: [10, 64, 20]

❤️ SANTÉ: 18/20 🟢
🍗 FAIM: 5/20 🔴 URGENT

🎒 INVENTAIRE:
   - apple: x5

👁️ ENVIRONNEMENT:
   - oak_log: x3

🐾 ENTITÉS:
   🐄 pig: x2
```

### PHASE 2: RAISONNEMENT 🧠

Le LLM analyse et décide:

```json
{
  "pensee": "Faim critique - besoin de manger",
  "action": "eat_food",
  "parametres": {},
  "priorite": "haute"
}
```

### PHASE 3: EXÉCUTION ⚡

L'Exécuteur convertit en actions RL:

```
Decision: eat_food
→ Actions RL: [31] (eat)
→ Bot mange pomme 🍎
```

## 🎯 Actions Disponibles

| Action | Description | Priorité |
|--------|-------------|----------|
| `move_to` | Se déplacer vers coordonnées | Variable |
| `mine_block` | Miner un bloc spécifique | Moyenne |
| `collect_drops` | Ramasser items | Basse |
| `craft_item` | Fabriquer objet | Moyenne |
| `attack_entity` | Attaquer mob | Haute |
| `eat_food` | Manger | Haute si faim < 10 |
| `equip_item` | Équiper item | Moyenne |
| `wait` | Attendre | Basse |

## 🔄 Différence avec le RL pur

### RL Pur (Existant)
- ✅ Apprend par essai-erreur
- ✅ Réflexes rapides
- ❌ Long à entraîner
- ❌ Pas de compréhension

### LLM Pur
- ✅ Comprend le langage
- ✅ Planification intelligente
- ❌ Pas d'apprentissage
- ❌ Actions lentes

### HYBRIDE ⭐ (Nouveau)
- ✅ RL pour les réflexes (vitesse)
- ✅ LLM pour la stratégie (intelligence)
- ✅ Compréhension + Apprentissage
- ✅ Meilleur des deux mondes

## 📊 Exemple de Session

```bash
$ python hybrid_agent.py --objectif "Miner du fer" --steps 50

============================================================
🤖 AGENT HYBRIDE RL + LLM
============================================================
Objectif: Miner du fer
Max steps: 50
============================================================
✅ Bridge connecté
✅ Environnement RL créé
✅ Raisonneur LLM initialisé
✅ Exécuteur initialisé
🚀 Démarrage agent hybride (max 50 steps)

============================================================
ÉTAPE 1/50
============================================================
📡 PHASE 1: Perception...

📍 POSITION: [10, 64, 20]
❤️ SANTÉ: 18/20 🟢
🍗 FAIM: 15/20 🟡
🎒 INVENTAIRE: Vide
👁️ ENVIRONNEMENT: oak_log: x3

🧠 PHASE 2: Raisonnement...
Décision: move_to
Raison: Explorer pour trouver du fer

⚡ PHASE 3: Exécution...
✅ Action exécutée avec succès
```

## 🔧 Configuration

### Avec API Claude (Recommandé)

Créez un fichier `.env`:
```bash
ANTHROPIC_API_KEY="sk-ant-..."
```

### Sans API (Mode Démo)

Le système utilise des règles simples:
- Faim < 10 → eat_food
- Santé < 10 → fuir
- Vue fer → mine_block
- Défaut → explorer

## 🐛 Dépannage

### Erreur: "Not connected to bot"

```bash
# Vérifier que le bridge tourne
cd ~/MinecraftAI
./minecraft-bot/check-bridges.sh

# Le lancer si nécessaire
./minecraft-bot/launch-parallel-bridges.sh
```

### Erreur: "Pas de clé API"

Normal ! Le système fonctionne en **mode démo** sans clé API.

### Le bot ne bouge pas

Vérifiez les logs du bridge:
```bash
tail -f logs/bridge-8765.log
```

## 🚀 Prochaines Étapes

### Niveau 1: Réflexe ✅
- [x] Déplacement simple
- [x] Actions basiques
- [x] Boucle perception → décision → action

### Niveau 2: Survie 🔄
- [ ] Gérer la faim automatiquement
- [ ] Fuir les mobs hostiles
- [ ] Trouver à manger

### Niveau 3: Planification 📋
- [ ] Arbre technologique
- [ ] Objectifs complexes
- [ ] Planification multi-étapes

## 📚 Ressources

- [Mineflayer](https://github.com/PrismarineJS/mineflayer)
- [Anthropic API](https://docs.anthropic.com/)
- [PPO Trainer](../llm/python/training/trainer.py)

## 🤝 Contribution

Pour ajouter une nouvelle action:

1. Ajouter dans `ACTION_MAPPINGS` (executeur)
2. Implémenter `_execute_nom_action()`
3. Ajouter dans `ACTIONS_DISPONIBLES` (raisonneur)

## 📝 License

MIT License - Voir LICENSE
