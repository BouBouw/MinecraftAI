# Architecture du système Minecraft AI Builder

## Vue d'ensemble

Le système est composé de trois composants principaux qui communiquent entre eux via WebSocket :

```
┌──────────────────┐      WebSocket       ┌──────────────────┐
│   Mod Fabric     │◄────────────────────►│   Serveur WS     │
│   (Minecraft)    │                       │   (Node.js)     │
│                  │                       │                  │
│ - Visualisation  │                       │ - Coordination  │
│ - Validation     │                       │ - Parsing       │
└──────────────────┘                       └────────┬─────────┘
                                                    │
                                                    ▼
                                          ┌──────────────────┐
                                          │  Bot Mineflayer  │
                                          │   (Node.js)      │
                                          │                  │
                                          │ - Mining         │
                                          │ - Crafting       │
                                          │ - Building       │
                                          └────────┬─────────┘
                                                   │
                                                   ▼
                                          ┌──────────────────┐
                                          │   IA RL          │
                                          │   (Python)       │
                                          │                  │
                                          │ - Apprentissage  │
                                          │ - Décision       │
                                          └──────────────────┘
```

## Composant 1 : Mod Fabric 1.21

### Responsabilités

- Charger et parser les fichiers de schematics
- Afficher un overlay 3D transparent du schematic
- Permettre le déplacement du schematic
- Valider et envoyer les données au serveur WebSocket
- Afficher la progression de la construction

### Architecture

```
com.mcaibuilder/
├── mod/
│   ├── AIBuilderMod.java          # Point d'entrée principal
│   └── AIBuilderClient.java       # Initialisation côté client
├── schematic/
│   ├── SchematicData.java         # Structure de données
│   ├── SchematicLoader.java       # Parser Sponge Schematic
│   └── SchematicManager.java      # Gestion du schematic actif
├── renderer/
│   └── SchematicRenderer.java     # Rendu 3D de l'overlay
├── network/
│   └── ModWebSocketClient.java    # Communication WebSocket
├── gui/
│   └── SchematicHUD.java          # Interface utilisateur
└── config/
    └── ModConfig.java             # Configuration
```

### Flux de données

1. Le joueur charge un fichier `.schem`
2. `SchematicLoader` parse le fichier et crée un `SchematicData`
3. `SchematicRenderer` affiche l'overlay en 3D
4. Le joueur ajuste la position avec les touches
5. Sur validation, `ModWebSocketClient` envoie les données au serveur

### Messages envoyés au serveur

```json
{
  "type": "schematic_validation",
  "name": "ma_maison.schem",
  "position": { "x": 100, "y": 64, "z": -200 },
  "dimensions": { "width": 10, "height": 8, "length": 12 },
  "materials": {
    "minecraft:oak_planks": 150,
    "minecraft:stone": 80,
    "minecraft:glass": 20
  }
}
```

## Composant 2 : Serveur WebSocket (Node.js)

### Responsabilités

- Recevoir les schematics validés du mod
- Parser et analyser les matériaux nécessaires
- Générer un plan de construction optimisé
- Coordonner les tâches du bot
- Relayer les messages entre mod et bot

### Architecture

```
src/
├── server.js               # Serveur WebSocket principal
├── schematic-parser.js     # Parser et analyse de schematics
├── task-planner.js         # Planificateur de tâches
└── communication.js        # Gestion de la communication avec le bot
```

### Planificateur de tâches

Le planificateur divise la construction en plusieurs étapes :

1. **Gather Resources** - Récolter les matériaux nécessaires
2. **Craft Items** - Fabriquer les outils et items
3. **Move to Site** - Se rendre au lieu de construction
4. **Build Layers** - Construire couche par couche
5. **Cleanup** - Nettoyage final

Exemple de tâche générée :

```json
{
  "id": 1,
  "type": "gather_resources",
  "priority": 1,
  "description": "Gather required materials",
  "materials": {
    "minecraft:oak_planks": 150
  },
  "estimatedTime": 300
}
```

## Composant 3 : Bot Mineflayer

### Responsabilités

- Se connecter au serveur Minecraft comme un joueur
- Exécuter les tâches reçues du coordinateur
- Naviguer dans le monde avec pathfinding
- Interagir avec les blocs et entités
- Gérer l'inventaire

### Architecture des agents

```
src/
├── bot.js                 # Bot principal
├── agents/
│   ├── base-agent.js      # Classe de base
│   ├── mining-agent.js    # Récolte de ressources
│   ├── crafting-agent.js  # Craft d'items
│   ├── inventory-agent.js # Gestion inventaire
│   └── building-agent.js  # Construction
└── rl/
    ├── environment.js     # Environnement RL
    ├── model.py          # Modèle d'IA
    └── trainer.py        # Entraînement
```

### Agents spécialisés

#### MiningAgent

Responsable de la récolte de ressources :
- Trouver des minerais et arbres
- Miner avec les bons outils
- Gérer l'amélioration progressive des outils
- Créer des mineshafts

#### CraftingAgent

Responsable du craft :
- Connaître les recettes du jeu
- Utiliser les tables de craft et fours
- Fabriquer des outils et matériaux

#### InventoryAgent

Responsable de l'inventaire :
- Organiser les items
- Gérer les coffres
- Gérer l'espace de stockage

#### BuildingAgent

Responsable de la construction :
- Placer les blocs précisément
- Construire couche par couche
- Créer des échafaudages si nécessaire

### Communication avec le serveur

```json
// Message de statut envoyé au serveur
{
  "type": "status_update",
  "status": "building",
  "progress": 45,
  "currentBlock": "minecraft:oak_planks"
}
```

## Composant 4 : IA Reinforcement Learning

### Architecture

L'IA RL utilise une architecture basée sur **Stable Baselines3** avec l'algorithme **PPO** (Proximal Policy Optimization).

### Environment

L'environnement est défini comme un problème de Markov :

```
Observation Space:
- Position du bot (x, y, z)
- Inventaire (items et quantités)
- Blocs environnants (3x3x3)
- Objectif actuel
- Équipement actuel

Action Space:
- Mouvements (avant, arrière, gauche, droite, saut)
- Actions (miner, placer, craft)
- Sélection d'item

Reward:
- +Positif: Bloc placé, item crafté, objectif atteint
- -Négatif: Action invalide, mort, temps perdu
```

### Curriculum Learning

L'entraînement suit une progression :

```
Niveau 1: Tâches basiques
- Miner 10 blocs de bois
- Craft une pioche en bois
- Se déplacer vers un point

Niveau 2: Tâches intermédiaires
- Explorer une grotte
- Collecter du fer
- Construire un mur simple

Niveau 3: Tâches complexes
- Construire depuis un schematic
- Multi-objectifs
- Optimisation de ressources
```

### Entraînement

```bash
# Entraîner sur une tâche simple
python src/rl/trainer.py --task gather_wood --timesteps 100000

# Entraîner sur la construction
python src/rl/trainer.py --task build_structure --timesteps 1000000

# Continuer l'entraînement d'un modèle existant
python src/rl/trainer.py --task build_structure --load ./models/checkpoint.zip
```

## Communication entre composants

### Protocol WebSocket

Le système utilise un protocol WebSocket bidirectionnel :

```
Mod → Serveur:
- schematic_validation: Envoi d'un schematic à construire
- ping: Test de connexion

Serveur → Mod:
- bot_progress: Mise à jour de la progression
- build_complete: Construction terminée
- bot_error: Erreur du bot

Serveur → Bot:
- build_task: Nouvelle tâche de construction
- ping: Test de connexion

Bot → Serveur:
- status_update: Mise à jour du statut
- build_complete: Tâche terminée
- error: Erreur lors de l'exécution
```

### Format des messages

Tous les messages suivent ce format :

```json
{
  "type": "message_type",
  "timestamp": 1234567890,
  "data": {
    // Données spécifiques au type
  }
}
```

## Sécurité

### Authentification

- Le bot utilise l'authentification Microsoft pour se connecter
- Le serveur WebSocket peut être protégé avec une clé API
- Validation des messages entrants

### Rate Limiting

- Limitation du nombre de messages par seconde
- Timeout sur les opérations longues

## Performance

### Optimisations

- **Pathfinding**: Utilisation de l'algorithme A* avec cache
- **Rendu**: Frustum culling pour ne rendre que ce qui est visible
- **Communication**: Compression des messages pour les grands schematics
- **RL**: Vectorisation des actions pour un entraînement plus rapide

### Scalabilité

Le système peut être étendu pour supporter :
- Plusieurs bots travaillant en parallèle
- Plusieurs joueurs avec le mod
- Queue de construction multiple

## Monitoring

### Logs

Chaque composant génère des logs structurés :

```
[2024-01-30 15:30:45] [INFO] Bot spawned
[2024-01-30 15:30:46] [INFO] Gathering resources...
[2024-01-30 15:30:50] [INFO] Mined 10 oak logs
```

### Métriques

Le système expose des métriques :
- Taux de construction (blocs/seconde)
- Temps par tâche
- Taux de réussite
- Utilisation des ressources

## Dépannage

### Problèmes courants

1. **Bot se coince** : Le pathfinding peut échouer dans des zones complexes
2. **Items manquants** : Le bot peut ne pas trouver certaines ressources
3. **Performance** : Les grands schematics peuvent prendre du temps

### Solutions

- Timeout automatique sur les opérations
- Retry logic pour les actions échouées
- Fallback sur des actions plus simples

## Extensions futures

- Support de la redstone dans les schematics
- Multi-bots coordonnés
- Interface web de monitoring
- Mode créatif pour tests rapides
- Export des constructions en fichiers
