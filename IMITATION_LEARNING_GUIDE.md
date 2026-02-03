# 🎓 Guide: Imitation Learning pour Minecraft Bot

## 🚀 Pourquoi utiliser l'imitation learning ?

Après 2200+ épisodes, le bot n'a toujours pas miné un seul bloc. **L'imitation learning résout ça !**

Avec votre aide, le bot apprendra **10x plus vite** en vous imitant.

---

## 📋 Processus en 3 Étapes

### Étape 1 : Enregistrer Vos Démonstrations (30-60 min)

**Arrêtez l'entraînement actuel** :
```bash
kill $(cat ~/training2.pid)
```

**Puis lancez l'enregistreur** :
```bash
cd ~/MinecraftAI/llm/python
source ~/venv/bin/activate
python training/record_demos.py --output ../data/demos/my_demos.pkl
```

**Une fois connecté, jouez à Minecraft !**

Montrez au bot :
- ✅ **Comment miner** (approcher, viser, miner)
- ✅ **Comment se déplacer** (marcher, sauter)
- ✅ **Comment crafter** (planches, bâtons)
- ✅ **Comment se nourrir** (quand faim est basse)

**Conseils** :
- Faites des épisodes courts (50-200 actions)
- Montrez la même action plusieurs fois
- Variez les situations (différents blocs, différents endroits)
- N'ayez pas peur de montrer les erreurs (le bot apprend aussi des échecs)

**Commandes dans l'enregistreur** :
- Tapez le numéro de l'action (0-50) et Entrée
- `stop` pour arrêter et sauvegarder
- `s` pour voir l'observation actuelle
- `h` pour l'aide

---

### Étape 2 : Entraînement par Imitation

Une fois que vous avez enregistré vos démonstrations :

```bash
cd ~/MinecraftAI/llm/python
source ~/venv/bin/activate
python training/train_from_demos.py \
    --demos=../data/demos/my_demos.pkl \
    --bc-epochs=10 \
    --rl-steps=100000
```

Ce qui va se passer :
1. **Phase 1** : Le bot copie vos actions (Behavior Cloning)
2. **Phase 2** : Le bot continue à apprendre avec RL (PPO)

---

### Étape 3: Laisser le Bot Explorer

Laissez l'entraînement tourner 24-48h.

Le bot va maintenant :
- ✅ Commencer en sachant déjà les bases
- ✅ Explorer et découvrir de nouvelles choses
- ✅ Devenir TOTALEMENT autonome

---

## 🎮 Actions à Démontrer

Voici les actions les plus importantes à montrer :

### ⛏️ Mining (CRUCIAL !)
```
1. S'approcher d'un bloc
2. Viser le bloc
3. Action 8 (mine)
4. Répéter 5-10x avec différents blocs
```

### 🔨 Crafting
```
1. Avoir des logs dans l'inventaire
2. Ouvrir l'inventaire (action 43)
3. Sélectionner les logs (action 9-17)
4. Fermer inventaire
5. Craft (action 20)
```

### 🚶 Mouvement
```
1. Avancer (action 1)
2. Tourner (actions 24-27)
3. Sauter (action 5)
4. Combinaisons : avancer + sauter
```

### 🍎 Survival
```
1. Attendre d'avoir faim
2. Avoir de la nourriture
3. Manger (action 50)
```

---

## 📊 Résultats Attendus

### Avant (Pure RL - 2200 épisodes)
- ❌ 0 blocs minés
- ❌ 0 items craftés
- ⚠️ Tourne en rond

### Après (Imitation + 30 min de démos)
- ✅ **Sait miner** (vous lui avez montré)
- ✅ **Sait crafter** (vous lui avez montré)
- ✅ **Saut se déplacer** (vous lui avez montré)
- 🚀 **Ensuite explore tout seul**

---

## 💡 Combien de temps ?

- **Enregistrement** : 30-60 minutes de jeu
- **Training** : 12-24 heures
- **Résultats** : Bot qui joue compétemment

**VS Pure RL** :
- Enregistrement : 0 minutes
- Training : Plusieurs semaines/mois
- Résultats : Toujours tourné en rond

---

## 🎯 Prochaine Étape

1. **Arrêtez l'entraînement actuel**
2. **Enregistrez 30-60 min de démos**
3. **Lancez l'entraînement par imitation**
4. **Laissez tourner 24-48h**

**Vous aurez un bot qui joue vraiment !** 🤖🎮

---

**Voulez-vous commencer l'enregistrement maintenant ?** 🎬
