# 🚀 Démarrage Rapide - Apprentissage Autonome

## ⚡ Commandes Rapides

### 1. Tester le système

```bash
cd llm/python
python test_auto_learning.py
```

### 2. Lancer l'entraînement

```bash
cd llm/python
python train.py --config ../config/rl_config.yaml
```

### 3. Surveiller en temps réel

```bash
# Dans une autre console
tail -f training.log
```

---

## 📊 Ce que Vous Verrez dans les Logs

```
🚀 Minecraft RL Auto-Learning System Initialized
🤖 Intrinsic Curiosity Module: ENABLED
🎓 Auto-Curriculum: ENABLED

🔍 Discovered new mechanic: move_forward at step 15
🎓 Learned new skill: move_forward (NOVICE)
🎯 Current learning goals: ['move_backward', 'jump', 'look_around']

⛏️ Mining dirt at (10, 64, 5)
🧱 Discovered new block: dirt (ID: 3)

📊 MECHANIC MASTERY REPORT
Movement:
  move_forward                ✅COMPETENT       (45/50 attempts)
  jump                       🌱NOVICE          (3/5 attempts)
```

---

## ⏱️ Temps d'Apprentissage Estimé

| Durée | Ce que le bot apprend |
|-------|---------------------|
| **1-2 heures** (100K steps) | Mouvement de base, mining simple |
| **10-20 heures** (1M steps) | Mining + crafting de base |
| **100-200 heures** (10M steps) | Combat, survie, mining avancé |
| **500-1000 heures** (50M steps) | **TOUTES les mécaniques** |

---

## 🎯 Résultats Attendus

### Aprés 1-2 heures
- ✅ Se déplace correctement
- ✅ Minerais des blocs de base
- ✅ Reconnaît 5-10 types de blocs

### Après 10-20 heures
- ✅ Crafting de base (planches, bâtons, pioches)
- ✅ Construction d'abri simple
- ✅ Mining de pierre et minerais communs

### Après 100+ heures
- ✅ Mining avancé (fer, or, diamant)
- ✅ Combat les mobs
- ✅ Survie autonome

---

## 🛠️ Configuration

La configuration est déjà prête dans `llm/config/rl_config.yaml`:

```yaml
training:
  auto_curriculum:
    enabled: true  # ✅ Déjà activé !

  curiosity:
    enabled: true  # ✅ Déjà activé !

  use_extrinsic_rewards: false  # ✅ Rewards intrinsèques seulement
```

**Rien à changer, tout est déjà configuré !**

---

## 📚 Documentation

- **Guide complet**: `llm/AUTO_LEARNING_GUIDE.md`
- **Résumé technique**: `IMPLEMENTATION_SUMMARY.md`

---

## 🔧 Problèmes ?

**Le bot ne bouge pas** → Augmenter `entropy_coef: 0.1` dans la config

**Le bot n'explore pas** → Vérifier que `curiosity.enabled: true`

**Trop lent** → Normal ! L'auto-apprentissage est plus lent mais plus complet.

---

## ✅ C'est Parti !

```bash
cd llm/python
python train.py --config ../config/rl_config.yaml
```

**Votre bot va maintenant apprendre TOUTES les mécaniques de Minecraft tout seul !**

🚀🤖🎮
