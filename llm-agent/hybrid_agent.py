"""
AGENT HYBRIDE RL + LLM

Architecture à 3 modules:
1. PERCEPTEUR: Minecraft → Texte
2. RAISONNEUR: LLM décide de la stratégie
3. EXÉCUTEUR: Décision → Actions RL

Usage:
    python hybrid_agent.py --objectif "Miner 5 blocs de fer"
"""

import asyncio
import json
from pathlib import Path
from typing import Dict, Any

from bridge.minecraft_bot_bridge import MinecraftBotBridge
from gym_env.minecraft_env import create_minecraft_env
from utils.config import get_config
from utils.logger import get_logger

# Import des 3 modules
try:
    from llm_agent.raisonner.llm_decision import LLMDecisionMaker
    from llm_agent.executeur.action_executor import ActionExecutor
except ImportError:
    # Fallback pour exécution directe depuis llm-agent/
    import sys
    from pathlib import Path
    # Ajouter le répertoire parent au Python path
    parent_dir = Path(__file__).parent.parent
    if str(parent_dir) not in sys.path:
        sys.path.insert(0, str(parent_dir))
    # Essayer l'import avec le module
    try:
        from llm_agent.raisonner.llm_decision import LLMDecisionMaker
        from llm_agent.executeur.action_executor import ActionExecutor
    except ImportError:
        # Dernier fallback: imports directs
        from raisonner.llm_decision import LLMDecisionMaker
        from executeur.action_executor import ActionExecutor

logger = get_logger(__name__)


class HybridAgent:
    """
    Agent Hybride RL + LLM

    Combine:
    - RL pour les réflexes (mouvement, mining)
    - LLM pour la planification (stratégie, objectifs)
    """

    def __init__(self, config: Dict[str, Any], objectif: str):
        """
        Initialize l'agent hybride

        Args:
            config: Configuration du système
            objectif: Objectif principal de l'agent
        """
        self.config = config
        self.objectif = objectif
        self.episode_count = 0

        logger.info(f"🤖 Initialisation Agent Hybride")
        logger.info(f"🎯 Objectif: {objectif}")

    async def setup(self):
        """Configure les composants de l'agent"""
        # Créer le bridge
        bridge_config = self.config.get('bridge', {})
        self.bridge = MinecraftBotBridge(
            host=bridge_config.get('host', 'localhost'),
            port=bridge_config.get('port', 8765)
        )
        await self.bridge.connect()
        logger.info("✅ Bridge connecté")

        # Créer l'environnement RL
        self.env = create_minecraft_env(config=self.config, bridge_client=self.bridge)
        logger.info("✅ Environnement RL créé")

        # Initialiser le Raisonneur (LLM)
        self.llm = LLMDecisionMaker()
        logger.info("✅ Raisonneur LLM initialisé")

        # Initialiser l'Exécuteur
        self.executor = ActionExecutor(self.bridge)
        logger.info("✅ Exécuteur initialisé")

    async def run(self, max_steps: int = 100):
        """
        Lance la boucle principale de l'agent hybride

        Args:
            max_steps: Nombre maximum d'étapes
        """
        logger.info(f"🚀 Démarrage agent hybride (max {max_steps} steps)")

        obs, info = self.env.reset()

        for step in range(max_steps):
            logger.info(f"\n{'='*60}")
            logger.info(f"ÉTAPE {step + 1}/{max_steps}")
            logger.info(f"{'='*60}")

            # PHASE 1: PERCEPTRON - Observer l'environnement
            logger.info("📡 PHASE 1: Perception...")
            rapport = await self._percevoir()
            logger.info(f"\n{rapport}\n")

            # PHASE 2: RAISONNEUR - Décider de l'action
            logger.info("🧠 PHASE 2: Raisonnement...")
            decision = await self.llm.decider(rapport, self.objectif)
            logger.info(f"Décision: {decision['action']}")
            logger.info(f"Raison: {decision.get('pensee', '')}")

            # PHASE 3: EXÉCUTEUR - Exécuter l'action
            logger.info("⚡ PHASE 3: Exécution...")
            succes = await self.executor.executer_decision(decision)

            if succes:
                logger.info("✅ Action exécutée avec succès")
            else:
                logger.warning("⚠️  Action échouée")

            # Pause entre les étapes
            await asyncio.sleep(0.5)

        logger.info(f"\n{'='*60}")
        logger.info(f"🏁 Épisode terminé après {step + 1} steps")
        logger.info(f"{'='*60}")

        # Résumé
        self._afficher_resumen()

    async def _percevoir(self) -> str:
        """
        Génère un rapport de l'état actuel

        Returns:
            Rapport textuel pour le LLM
        """
        # Pour l'instant, utilise le bridge pour obtenir l'état
        state = await self.bridge.get_observation()

        # Formater en rapport textuel
        rapport = self._formatter_rapport(state)
        return rapport

    def _formatter_rapport(self, state: Dict) -> str:
        """
        Formate l'état en rapport textuel

        Args:
            state: État du bot

        Returns:
            Rapport textuel
        """
        pos = state.get('position', [0, 64, 0])
        health = state.get('health', 20)
        food = state.get('food', 20)

        rapport = f"""
📍 POSITION: [{pos[0]:.0f}, {pos[1]:.0f}, {pos[2]:.0f}]

❤️ SANTÉ: {health}/20 {'🟢' if health > 15 else '🟡' if health > 8 else '🔴'}
🍗 FAIM: {food}/20 {'🟢' if food > 15 else '🟡' if food > 8 else '🔴 URGENT'}

🎒 INVENTAIRE: (Vide - à implémenter)

👁️ ENVIRONNEMENT: (À compléter avec vision)

🐾 ENTITÉS: (À compléter)
""".strip()

        return rapport

    def _afficher_resumen(self):
        """Affiche le résumé de l'épisode"""
        logger.info("\n📊 RÉSUMÉ DE L'ÉPISODE")

        # Statistiques LLM
        historique_llm = self.llm.get_historique()
        logger.info(f"   Décisions LLM: {len(historique_llm)}")

        # Actions par type
        if historique_llm:
            actions = {}
            for dec in historique_llm:
                action = dec['decision']['action']
                actions[action] = actions.get(action, 0) + 1

            logger.info("   Actions exécutées:")
            for action, count in actions.items():
                logger.info(f"      - {action}: x{count}")

        # Statistiques exécuteur
        historique_exec = self.executor.get_execution_history()
        succes = sum(1 for h in historique_exec if h['succes'])
        taux = (succes / len(historique_exec) * 100) if historique_exec else 0

        logger.info(f"   Taux de succès: {taux:.1f}%")


async def main():
    """Point d'entrée principal"""
    import sys

    # Parser arguments
    objectif = "Survivre et explorer"  # Objectif par défaut
    config_path = '../config/rl_config.yaml'
    max_steps = 100

    if len(sys.argv) > 1:
        for arg in sys.argv[1:]:
            if arg.startswith('--objectif='):
                objectif = arg.split('=', 1)[1]
            elif arg.startswith('--config='):
                config_path = arg.split('=', 1)[1]
            elif arg.startswith('--steps='):
                max_steps = int(arg.split('=', 1)[1])

    logger.info("="*60)
    logger.info("🤖 AGENT HYBRIDE RL + LLM")
    logger.info("="*60)
    logger.info(f"Objectif: {objectif}")
    logger.info(f"Max steps: {max_steps}")
    logger.info("="*60)

    # Charger la config
    config = get_config(config_path)

    # Créer l'agent
    agent = HybridAgent(config, objectif)

    # Setup
    await agent.setup()

    # Run
    try:
        await agent.run(max_steps=max_steps)
    except KeyboardInterrupt:
        logger.info("\n⏸️  Arrêt par l'utilisateur")
    except Exception as e:
        logger.error(f"\n❌ Erreur: {e}")
        import traceback
        logger.debug(traceback.format_exc())


if __name__ == "__main__":
    asyncio.run(main())
