# Minecraft AI Builder

Un système complet d'IA capable de construire automatiquement des structures Minecraft à partir de schematics. Le projet se compose de trois composants principaux :

- **Mod Fabric 1.21** (Client-side) - Pour visualiser et valider les schematics
- **Serveur WebSocket** (Node.js) - Pour coordonner la communication
- **Bot Mineflayer** (Node.js) - Un bot IA qui se connecte comme un joueur

## 🎯 Fonctionnalités

- ✅ Visualisation de schematics dans le jeu (overlay transparent)
- ✅ Déplacement du schematic avec les touches
- ✅ Validation et envoi au bot
- ✅ Bot capable de miner, crafter et construire
- ✅ IA par Reinforcement Learning (en développement)
- ✅ Communication WebSocket temps réel
- ✅ Mode "from scratch" ou avec équipement
- ✅ Support des différentes dimensions

## 📋 Prérequis

### Logiciels requis

- **Java 21** - Pour le mod Fabric
- **Node.js 20+** - Pour le serveur et le bot
- **Python 3.10+** - Pour l'entraînement RL (optionnel)
- **Minecraft 1.21** - Avec Fabric
- Un compte Minecraft (pour le bot)

### Dépendances

```bash
# Node.js packages
npm install ws mineflayer express

# Python packages (pour l'IA RL)
pip install gymnasium stable-baselines3 torch numpy
```

## 🚀 Installation

### 1. Cloner le repository

```bash
git clone https://github.com/votre-username/MinecraftAI.git
cd MinecraftAI
```

### 2. Installer le serveur WebSocket

```bash
cd ai-coordinator
npm install
```

### 3. Installer le bot Mineflayer

```bash
cd ../minecraft-bot
npm install
```

### 4. Compiler le mod Fabric

```bash
cd ../minecraft-fabric-mod
./gradlew build
```

**Sur Windows** :
```cmd
gradlew.bat build
```

Le mod compilé sera dans `minecraft-fabric-mod/build/libs/`

## ⚙️ Configuration

### Serveur WebSocket

Le fichier `ai-coordinator/src/server.js` utilise le port 8080 par défaut.

Pour changer le port :
```javascript
const server = new AIServer(3000); // Changez 3000 par votre port
```

### Bot Mineflayer

Créez un fichier `.env` dans `minecraft-bot/` :

```env
# Serveur Minecraft
MC_HOST=localhost
MC_PORT=25565

# Compte du bot
MC_USERNAME=VotreBotName
MC_PASSWORD=votre_mot_de_passe  # Optionnel si offline
MC_AUTH=microsoft  # ou 'offline'

# URL du coordinateur
COORDINATOR_URL=ws://localhost:8080/bot
```

### Mod Fabric

Le fichier `minecraft-fabric-mod/src/main/java/com/mcaibuilder/config/ModConfig.java` contient la configuration :

```java
public static final String WEBSOCKET_SERVER_URL = "ws://localhost:8080";
```

## 🎮 Utilisation

### Démarrage rapide

1. **Lancer le serveur de coordination** :
```bash
cd ai-coordinator
npm start
```

2. **Lancer le bot** (dans un autre terminal) :
```bash
cd minecraft-bot
npm start
```

3. **Installer et lancer le mod Fabric** :
   - Copiez `minecraft-fabric-mod/build/libs/ai-builder-mod-1.0.0.jar` dans votre dossier `.minecraft/mods`
   - Lancez Minecraft avec le Fabric Loader 1.21
   - Rejoignez un monde (singleplayer ou serveur)

4. **Utiliser le mod dans le jeu** :
   - Placez un fichier `.schem` dans `.minecraft/schematics/`
   - Chargez le schematic (commande prévue)
   - Utilisez les touches pour le déplacer
   - Appuyez sur **ENTER** pour valider et lancer le bot

### Commandes du bot (chat)

Le bot répond aux commandes par whisper (`/whisper BotName commande`) :

- `!status` - Affiche le statut actuel
- `!follow` - Le bot vous suit
- `!stop` - Arrête les actions en cours

### Touches du mod

- **R** - Activer/désactiver l'overlay du schematic
- **ENTER** - Valider et envoyer au bot
- **LEFT SHIFT** - Déplacer le schematic vers le haut
- **LEFT CONTROL** - Déplacer le schematic vers le bas

## 🧠 Entraînement de l'IA (Reinforcement Learning)

Le système utilise Stable Baselines3 pour l'entraînement RL.

### Préparer l'environnement

```bash
cd minecraft-bot
pip install -r requirements.txt
```

### Entraîner sur des tâches simples

```bash
python src/rl/trainer.py --task gather_wood --timesteps 100000
```

### Tâches disponibles

- `gather_wood` - Récolter du bois
- `mine_stone` - Miner de la pierre
- `craft_tool` - Crafter un outil
- `build_simple` - Construire une structure simple

### Utiliser un modèle entraîné

Déplacez le modèle vers `minecraft-bot/models/best_model.zip` et configurez le bot pour l'utiliser :

```javascript
// config.js
useRL: true,
rlModel: './models/best_model.zip'
```

## 📁 Structure du projet

```
MinecraftAI/
├── minecraft-fabric-mod/     # Mod Fabric 1.21
│   ├── src/main/java/        # Code source Java
│   ├── build.gradle          # Configuration Gradle
│   └── build/libs/           # Mod compilé
├── ai-coordinator/           # Serveur WebSocket
│   ├── src/
│   │   ├── server.js         # Serveur principal
│   │   ├── schematic-parser.js
│   │   ├── task-planner.js
│   │   └── communication.js
│   └── package.json
├── minecraft-bot/            # Bot Mineflayer
│   ├── src/
│   │   ├── bot.js            # Bot principal
│   │   ├── agents/           # Agents spécialisés
│   │   ├── rl/               # Code RL
│   │   └── utils/            # Utilitaires
│   ├── models/               # Modèles RL entraînés
│   ├── config.js             # Configuration
│   └── package.json
└── README.md
```

## 🔧 Développement

### Compiler le mod en mode dev

```bash
cd minecraft-fabric-mod
./gradlew genSources
./gradlew build
```

### Lancer le serveur WebSocket en mode dev

```bash
cd ai-coordinator
npm run dev  # Auto-reload sur changements
```

### Lancer le bot en mode test

```bash
cd minecraft-bot
npm test
```

## 🐛 Dépannage

### Le mod ne se charge pas

- Vérifiez que vous utilisez Minecraft 1.21 avec Fabric
- Vérifiez que Java 21 est installé
- Regardez les logs dans `.minecraft/logs/latest.log`

### Le bot ne se connecte pas

- Vérifiez que le serveur WebSocket est lancé
- Vérifiez les paramètres de connexion dans `config.js`
- Assurez-vous que le compte Minecraft est valide

### L'IA RL n'apprend pas

- Augmentez le nombre de timesteps
- Vérifiez les récompenses dans les logs
- Essayez différents hyperparamètres

## 📚 Documentation supplémentaire

- [Fabric Documentation](https://fabricmc.net/wiki/start:introduction)
- [Mineflayer Documentation](https://github.com/PrismarineJS/mineflayer)
- [Stable Baselines3](https://stable-baselines3.readthedocs.io/)
- [Sponge Schematic Format](https://github.com/SpongePowered/Schematic-Specification)

## 🤝 Contribution

Les contributions sont les bienvenues ! N'hésitez pas à :

1. Fork le projet
2. Créer une branche (`git checkout -b feature/AmazingFeature`)
3. Commit (`git commit -m 'Add some AmazingFeature'`)
4. Push (`git push origin feature/AmazingFeature`)
5. Ouvrir une Pull Request

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

## 🙏 Remerciements

- FabricMC pour le mod loader
- PrismarineJS pour Mineflayer
- Stable Baselines3 pour l'IA RL
- La communauté Minecraft open source

---

**Note** : Ce projet est en développement actif. Certaines fonctionnalités peuvent ne pas encore être complètes.
