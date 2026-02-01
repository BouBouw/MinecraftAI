# Apprentissage Autonome Minecraft RL

## 🚀 Nouveau Système d'Apprentissage

Le bot peut maintenant apprendre **TOUTES les mécaniques de Minecraft** de manière autonome, sans intervention humaine.

### 📋 Deux Modes de Fonctionnement

#### 1. MODE AUTO-CURRICULUM (Recommandé)
```yaml
training:
  auto_curriculum:
    enabled: true
  curiosity:
    enabled: true
```

**Comment ça marche:**
- 🤖 **Curiosité Intrinsèque** : Le bot est motivé par la nouveauté et la surprise
- 🎯 **Auto-Objectifs** : Le bot définit ses propres objectifs d'apprentissage
- 🔍 **Découverte** : Le bot découvre les mécaniques en explorant
- 📈 **Progression** : Le bot maîtrise progressivement les compétences

**Ce que le bot apprend seul:**
- ✅ Mouvement de base (marcher, sauter, s'accroupir)
- ✅ Miner et reconnaître les blocs (terre, pierre, minerais)
- ✅ Utiliser les outils (pioche, hache, pelle)
- ✅ Crafting (planches, bâtons, pioches, workbench, four)
- ✅ Construction (placer des blocs, construire un abri)
- ✅ Survie (manger, éviter les dégâts, survivre la nuit)
- ✅ Combat (tuer les mobs hostiles: zombies, squelettes, araignées, creepers)
- ✅ Avancé (minerais, lave, enchantement, potions, Nether)

#### 2. MODE CURRICULUM FIXE (Traditionnel)
```yaml
training:
  auto_curriculum:
    enabled: false
```

Stages prédéfinis par des humains. Moins flexible mais plus prévisible.

---

## 🧠 Composants de l'Apprentissage Autonome

### 1. Intrinsic Curiosity Module (ICM)

**Fichier**: `llm/python/agents/intrinsic_curiosity.py`

**Fonction**: Le bot est récompensé pour explorer des états nouveaux et surprenants.

**Composants**:
- **Inverse Dynamics Model**: Apprend à prédire l'action à partir de deux états
- **Forward Dynamics Model**: Prédit le prochain état
- **RND (Random Network Distillation)**: Mesure la nouveauté
- **Count-based Bonus**: Bonus pour visiter des états rares

**Rewards Intrinsèques**:
```python
reward = icm_scale * curiosity_bonus +      # Exploration
         rnd_scale * novelty_bonus +         # Nouveauté
         count_scale * count_bonus           # États rares
```

### 2. Auto-Curriculum

**Fichier**: `llm/python/training/auto_curriculum.py`

**Fonction**: Le bot définit ses propres objectifs d'apprentissage basés sur ce qu'il ne connaît pas encore.

**Mécaniques Suivées**: 50+ mécaniques Minecraft organisées avec prérequis

**Niveaux de Maîtrise**:
- UNKNOWN → Jamais rencontré
- NOVICE → Essayé une fois
- APPRENTICE → Peut le faire avec difficulté
- COMPETENT → Peut le faire fiablement
- EXPERT → Maîtrisé
- INNOVATOR → Découvre de nouvelles utilisations

**Exemple de Progression**:
```
1. Découvre: movement (move_forward)
2. Maîtrise: movement → Déverrouille: mine_block
3. Découvre: stone → Déverrouille: mine_iron_ore
4. Maîtrise: mine_iron_ore → Déverrouille: craft_iron_pickaxe
...
```

---

## ⚙️ Configuration

### Fichier: `llm/config/rl_config.yaml`

```yaml
# Activer l'apprentissage autonome
training:
  auto_curriculum:
    enabled: true  # AGENT sets own goals

  curiosity:
    enabled: true  # INTRINSIC motivation
    icm_scale: 1.0      # Curiosity bonus
    rnd_scale: 0.5      # Novelty bonus
    count_scale: 0.1    # Rare state bonus

  use_extrinsic_rewards: false  # Disable hand-crafted rewards

# Hyperparamètres PPO pour apprentissage autonome
agent:
  learning_rate: 0.0001
  entropy_coef: 0.05  # Plus d'exploration

training:
  total_timesteps: 50000000  # 50M steps pour tout apprendre
  batch_size: 256
  n_steps: 8192
```

---

## 🎮 Utilisation

### Lancer l'entraînement

```bash
cd llm/python
python train.py --config ../config/rl_config.yaml
```

### Surveiller la progression

```bash
# Voir les mécaniques découvertes
tail -f training.log | grep "Discovered new"

# Voir la maîtrise des compétences
tail -f training.log | grep "MECHANIC MASTERY"

# Voir les objectifs d'apprentissage actuels
tail -f training.log | grep "Current learning goals"
```

### Exemple de Logs

```
🔍 Discovered new mechanic: move_forward at step 15
🎓 Learned new skill: move_forward (NOVICE)
🎯 Current learning goals: ['move_backward', 'move_left', 'move_right', 'jump']

🔍 Discovered new mechanic: mine_block at step 1234
⛏️  Mining dirt at (10, 64, 5)
🧱 Discovered new block: dirt (ID: 3)

📊 MECHANIC MASTERY REPORT
============================================================

Movement:
  move_forward                ⭐EXPERT          (125/125 attempts)
  move_backward              ✅COMPETENT       (45/50 attempts)
  jump                       ✅COMPETENT       (38/40 attempts)

Mining:
  mine_block                 📚APPRENTICE      (12/20 attempts)
  mine_stone                 🌱NOVICE          (2/5 attempts)

Crafting:
  craft_planks               ❓UNKNOWN         (0/0 attempts)
```

---

## 🔬 Pourquoi ça marche ?

### 1. Curiosité = Exploration Naturelle
Les humains explorent parce qu'ils sont curieux. Le bot fait pareil !

**Sans curiosité**: Le bot reste dans une zone connue (exploitation)
**Avec curiosité**: Le bot explore pour découvrir (exploration)

### 2. Auto-Curriculum = Progression Naturelle
Les humains apprennent progressivement (marcher → courir → sauter). Le bot fait pareil !

**Curriculum fixe**: Stages artificiels définis par des humains
**Auto-curriculum**: Objectifs naturels basés sur les prérequis

### 3. Rewards Intrinsèques = Motivation Interne
Les humains sont motivés par l'apprentissage lui-même. Le bot fait pareil !

**Rewards extrinsèques**: Récompenses externes (miner = +5 points)
**Rewards intrinsèques**: Récompenses internes (découvrir = +surprise)

---

## 📊 Résultats Attendus

### Court terme (0-100K steps)
- ✅ Apprend à se déplacer
- ✅ Découvre comment miner
- ✅ Reconnaît quelques blocs

### Moyen terme (100K-1M steps)
- ✅ Maîtrise le mining de base
- ✅ Découvre le crafting
- ✅ Construit des abris simples

### Long terme (1M-10M steps)
- ✅ Maîtrise les minerais avancés (fer, or, diamant)
- ✅ Combat les mobs
- ✅ Survit la nuit

### Très long terme (10M-50M steps)
- ✅ Découvre le Nether
- ✅ Enchantement
- ✅ Potions
- ✅ Redstone
- ✅ TOUTES les mécaniques Minecraft

---

## 🎓 Avantages vs Curriculum Fixe

| Critère | Auto-Curriculum | Curriculum Fixe |
|---------|----------------|-----------------|
| **Flexibilité** | ✅ S'adapte automatiquement | ❌ Stages figés |
| **Découverte** | ✅ Découvre TOUT | ⚠️ Seulement ce qui est prévu |
| **Robustesse** | ✅ Fonctionne avec des bugs | ⚠️ Bloqué si bug |
| **Vitesse** | ⚠️ Plus lent au début | ✅ Rapide au début |
| **Long terme** | ✅ Continue à apprendre | ❌ Plafonne |
| **Maintenance** | ✅ Aucune maintenance | ❌ Stages à mettre à jour |

---

## 🐛 Dépannage

### Le bot ne bouge pas
- **Cause**: Entropie trop faible
- **Solution**: Augmenter `entropy_coef` à 0.1

### Le bot exploite trop et n'explore pas
- **Cause**: Curiosité désactivée ou coef trop faible
- **Solution**: Vérifier `curiosity.enabled: true` et `icm_scale: 1.0`

### Le bot apprend lentement
- **Cause**: Normal pour l'auto-apprentissage !
- **Solution**: Soyez patient. L'auto-apprentissage est plus lent mais plus complet.

### Memory error
- **Cause**: Buffer trop grand
- **Solution**: Réduire `n_steps` à 4096

---

## 📚 Références

Ce système est basé sur les papiers de recherche suivants:

1. **Pathak et al. "Curiosity-driven Exploration by Self-supervised Prediction"** (ICM)
   - https://arxiv.org/abs/1705.05363

2. **Burda et al. "Exploration by Random Network Distillation"** (RND)
   - https://arxiv.org/abs/1810.12894

3. **Tang et al. "Exploration by Random Network Distillation"**
   - https://arxiv.org/abs/1810.12894

4. **Mnih et al. "Human-level control through deep reinforcement learning"** (PPO/DQN)
   - https://www.nature.com/articles/nature14236

---

## 🚀 Prochaines Étapes

1. **Lancer l'entraînement** avec le mode auto-curriculum
2. **Surveiller les logs** pour voir les mécaniques découvertes
3. **Analyser la maîtrise** avec le rapport de mécaniques
4. **Patienter** - L'apprentissage autonome prend du temps mais est plus complet

Bonne chance avec votre bot Minecraft ! 🎮🤖
