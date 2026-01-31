# AI Builder - Système de Construction Automatique

## Vue d'ensemble

Ce système permet à un bot Minecraft de construire automatiquement des schématiques bloc par bloc en mode créatif.

## Fonctionnalités implémentées

### 1. Détection automatique du mode de jeu
Le bot détecte automatiquement son mode de jeu au spawn:
- **Survie**: Marche + sprint avec gestion de la faim
- **Créatif**: Vol + construction bloc par bloc
- **Aventure**: Similaire à survie
- **Spectateur**: Non implémenté
- **OP**: Téléportation directe avec `/tp`

### 2. Système de construction (Mode Créatif uniquement)

Le bot construit les schématiques en:
1. **Volant** jusqu'à la position de chaque bloc (3 blocs de distance, 2 blocs au-dessus)
2. **Plaçant** chaque bloc un par un avec `/setblock`
3. **Se déplaçant** comme un joueur réel (pas de téléportation entre les blocs)
4. **Construisant** du bas vers le haut (tri par coordonnée Y)

### 3. Format de schématique supporté

- **Sponge Schematic format** (.schem)
- Supporte les palettes de blocs
- Ignore les blocs d'air
- Tri automatique pour une construction stable

## Architecture

### Fichiers principaux

```
ai-coordinator/
├── src/
│   ├── server.js              # Coordinateur WebSocket principal
│   ├── schematic-builder.js   # Logique de construction
│   ├── schematic-parser.js    # Parser de schématiques
│   ├── task-planner.js        # Planificateur de tâches
│   └── communication.js       # Communication bot
├── schematics/                # Dossier des schématiques
│   ├── build.schem
│   └── test-house.schem
└── .env                       # Configuration
```

### Flux de communication

```
Minecraft Mod (V key)
    ↓ WebSocket
AI Coordinator
    ↓ Détection du mode
    ↓ Créatif?
    ↓ Oui → SchematicBuilder
    ↓ Non → Navigation simple
Mineflayer Bot
    ↓
Minecraft Server
```

## Utilisation

### 1. Configuration

Éditez `.env`:
```env
MC_HOST=localhost
MC_PORT=25565  # Port de votre monde LAN
MC_USERNAME=Booh
```

### 2. Dans Minecraft

1. **Chargez un schématique** dans le mod (fichier `.schem` dans le dossier racine)
2. **Appuyez sur R** pour activer l'overlay
3. **Positionnez** le schématique avec les flèches directionnelles
4. **Appuyez sur V** pour verrouiller et lancer le bot

### 3. Ce qui se passe

En **mode créatif**:
```
✅ Bot rejoint le serveur
🦅 Vol vers la position du schématique
🔨 Commence la construction bloc par bloc
📊 Progression envoyée au mod (chat Minecraft)
✅ Construction terminée
```

En **mode survie**:
```
✅ Bot rejoint le serveur
🚶 Marche vers la position
⏸️ Arrivé (pas de construction en survie)
```

En **mode OP**:
```
✅ Bot rejoint le serveur
⚡ Téléportation instantanée
🔨 Commence la construction (si créatif)
```

## Messages dans le chat

Le bot communique sa progression:

```
§bBot: Bot already connected, moving to new target...
§aBot spawned: Bot connected to server
§aBot arrived: Bot flew to position (100, 64, 200)
§aBot building: Starting construction of build.schem...
🔨 Placing block 15/100 (15%)
✅ Construction completed! 100 blocks placed.
```

## Limitations actuelles

1. **Construction uniquement en mode créatif**
   - Le mode survie ne construit pas (seulement navigation)
   - Nécessite d'être OP pour utiliser `/setblock`

2. **Performance**
   - Construction bloc par bloc (peut être lent pour grandes structures)
   - 50ms de délai entre chaque bloc pour paraître naturel

3. **Dépendances**
   - Le fichier `.schem` doit exister dans `ai-coordinator/schematics/`
   - Le même nom doit être utilisé dans le mod

## Améliorations futures

- [ ] Mode survie: collecter et placer les blocs manuellement
- [ ] Construction parallèle (plusieurs blocs en même temps)
- [ ] Support des blocs orientés (escaliers, coffres, etc.)
- [ ] Gestion des entités (creation de NPC, panneaux, etc.)
- [ ] Undo/Redo des constructions
- [ ] Sauvegarde de la progression

## Dépendances

```json
{
  "mineflayer": "^4.20.1",
  "mineflayer-pathfinder": "^2.4.4",
  "prismarine-nbt": "^2.8.0",
  "prismarine-block": "^1.22.0",
  "ws": "^8.16.0"
}
```

## Debug

### Vérifier que le bot est en créatif
```bash
# Dans les logs du coordinateur
✅ Bot spawned!
   Game Mode: creative
   OP Status: Yes - can use /tp
```

### Logs de construction
```bash
🔨 Placing block 1/100 (1%)
   Position: (100, 64, 200)
   Type: stone
   ✅ Block placed: stone
```

### Erreurs courantes
- `Schematic file not found`: Le fichier n'est pas dans `schematics/`
- `Unknown block type`: Bloc non supporté par cette version
- `No adjacent block found`: Pas de bloc solide pour poser contre

## Auteur

Système développé pour Minecraft 1.21 avec Fabric Mod et Mineflayer.
