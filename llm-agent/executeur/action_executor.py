"""
EXÉCUTEUR - Convertit les décisions LLM en actions RL

Ce module prend les décisions du Raisonneur (LLM) et les traduit
en séquences d'actions RL compréhensibles par le système existant.
"""

import asyncio
from typing import Dict, Any, List
from bridge.minecraft_bot_bridge import MinecraftBotBridge

from utils.logger import get_logger

logger = get_logger(__name__)


class ActionExecutor:
    """
    Exécuteur d'actions - Traduit décisions LLM en actions RL

    Connecte le système LLM au système RL existant.
    """

    # Mapping actions LLM vers séquences RL (action IDs JavaScript)
    ACTION_MAPPINGS = {
        "move_to": {
            "description": "Se déplacer vers un endroit",
            "implementer": "_execute_move_to"
        },
        "follow_path": {
            "description": "Suivre un chemin",
            "implementer": "_execute_follow_path"
        },
        "mine_block": {
            "description": "Miner un bloc",
            "implementer": "_execute_mine"
        },
        "collect_drops": {
            "description": "Ramasser items",
            "implementer": "_execute_collect"
        },
        "craft_item": {
            "description": "Fabriquer un objet",
            "implementer": "_execute_craft"
        },
        "place_block": {
            "description": "Placer un bloc",
            "implementer": "_execute_place"
        },
        "attack_entity": {
            "description": "Attaquer",
            "implementer": "_execute_attack"
        },
        "eat_food": {
            "description": "Manger",
            "implementer": "_execute_eat"
        },
        "equip_item": {
            "description": "Équiper item",
            "implementer": "_execute_equip"
        },
        "wait": {
            "description": "Attendre",
            "implementer": "_execute_wait"
        }
    }

    # Actions RL basiques (IDs serveur JavaScript)
    RL_ACTIONS = {
        "forward": 1,
        "backward": 2,
        "left": 3,
        "right": 4,
        "jump": 5,
        "sneak": 6,
        "sprint": 7,
        "look_left": 8,
        "look_right": 9,
        "look_up": 10,
        "look_down": 11,
        "attack": 12,
        "drop_item": 18,
        "place_block": 19,
        "craft": 27,
        "use_item": 29,
        "eat": 31
    }

    def __init__(self, bridge: MinecraftBotBridge):
        """
        Initialize Action Executor

        Args:
            bridge: Bridge vers le serveur Minecraft
        """
        self.bridge = bridge
        self.execution_history = []

    async def executer_decision(self, decision: Dict[str, Any]) -> bool:
        """
        Exécute une décision du LLM

        Args:
            decision: Décision du Raisonneur
                {
                    "action": "nom_action",
                    "parametres": {},
                    "priorite": "haute|moyenne|basse"
                }

        Returns:
            True si succès, False sinon
        """
        action_name = decision.get("action")
        parametres = decision.get("parametres", {})

        logger.info(f"⚡ Exécution: {action_name} {parametres}")

        if action_name not in self.ACTION_MAPPINGS:
            logger.error(f"❌ Action inconnue: {action_name}")
            return False

        # Récupérer la méthode d'implémentation
        implementer_name = self.ACTION_MAPPINGS[action_name]["implementer"]
        implementer = getattr(self, implementer_name, None)

        if not implementer:
            logger.error(f"❌ Implémentation manquante: {implementer_name}")
            return False

        try:
            # Exécuter l'action
            succes = await implementer(parametres)

            # Enregistrer dans l'historique
            self.execution_history.append({
                "action": action_name,
                "parametres": parametres,
                "succes": succes,
                "timestamp": __import__('datetime').datetime.now().isoformat()
            })

            return succes

        except Exception as e:
            logger.error(f"❌ Erreur exécution {action_name}: {e}")
            return False

    # ========== IMPLÉMENTATIONS DES ACTIONS ==========

    async def _execute_move_to(self, params: Dict) -> bool:
        """Se déplacer vers des coordonnées"""
        target = params.get("target", params.get("coordinates", {}))

        if "direction" in params and params["direction"] == "random":
            # Mouvement aléatoire
            distance = params.get("distance", 10)
            logger.info(f"🚶 Mouvement aléatoire: {distance} blocs")

            # Avancer + aléatoire
            for _ in range(distance):
                await self._send_rl_action(self.RL_ACTIONS["forward"])
                await asyncio.sleep(0.1)

                # Petite variation aléatoire
                if _ % 5 == 0:
                    await self._send_rl_action(self.RL_ACTIONS["look_left"])
                elif _ % 5 == 2:
                    await self._send_rl_action(self.RL_ACTIONS["look_right"])

            return True

        # Mouvement vers coordonnées spécifiques
        x, y, z = target.get("x", 0), target.get("y", 64), target.get("z", 0)

        logger.info(f"🚶 Déplacement vers [{x}, {y}, {z}]")

        # Pour l'instant, mouvement simplifié
        # TODO: Implémenter pathfinding intelligent
        steps = 20
        for _ in range(steps):
            await self._send_rl_action(self.RL_ACTIONS["forward"])
            await asyncio.sleep(0.1)

        return True

    async def _execute_mine(self, params: Dict) -> bool:
        """Miner un bloc"""
        block_type = params.get("block_type", "stone")

        logger.info(f"⛏️  Mining: {block_type}")

        # Regarder vers le bas
        await self._send_rl_action(self.RL_ACTIONS["look_down"])
        await asyncio.sleep(0.2)

        # Miner plusieurs fois
        for _ in range(5):
            await self._send_rl_action(self.RL_ACTIONS["attack"])
            await asyncio.sleep(0.1)

        return True

    async def _execute_collect(self, params: Dict) -> bool:
        """Ramasser les items au sol"""
        logger.info("📦 Ramassage des items")

        # Regarder autour et se déplacer
        await self._send_rl_action(self.RL_ACTIONS["look_left"])
        await asyncio.sleep(0.1)
        await self._send_rl_action(self.RL_ACTIONS["look_right"])
        await asyncio.sleep(0.1)

        # Avancer vers les items
        for _ in range(5):
            await self._send_rl_action(self.RL_ACTIONS["forward"])
            await asyncio.sleep(0.1)

        return True

    async def _execute_craft(self, params: Dict) -> bool:
        """Fabriquer un objet"""
        item = params.get("item", "planks")

        logger.info(f"🔨 Craft: {item}")

        # Action craft (ID 27 dans le serveur JS)
        await self._send_rl_action(self.RL_ACTIONS["craft"])
        await asyncio.sleep(0.5)

        return True

    async def _execute_attack(self, params: Dict) -> bool:
        """Attaquer une entité"""
        logger.info("⚔️  Attaque")

        # Attaquer plusieurs fois
        for _ in range(3):
            await self._send_rl_action(self.RL_ACTIONS["attack"])
            await asyncio.sleep(0.1)

        return True

    async def _execute_eat(self, params: Dict) -> bool:
        """Manger"""
        logger.info("🍖 Manger")

        # Action eat (ID 31 dans le serveur JS)
        await self._send_rl_action(self.RL_ACTIONS["eat"])
        await asyncio.sleep(1.0)

        return True

    async def _execute_place(self, params: Dict) -> bool:
        """Placer un bloc"""
        logger.info("🧱 Placement bloc")

        await self._send_rl_action(self.RL_ACTIONS["place_block"])
        await asyncio.sleep(0.3)

        return True

    async def _execute_equip(self, params: Dict) -> bool:
        """Équiper un item"""
        logger.info("🛡️  Équipement")

        # Pour l'instant, simple action
        await asyncio.sleep(0.2)
        return True

    async def _execute_wait(self, params: Dict) -> bool:
        """Attendre"""
        duration = params.get("duration", 2.0)

        logger.info(f"⏳ Attente {duration}s")
        await asyncio.sleep(duration)

        return True

    async def _execute_follow_path(self, params: Dict) -> bool:
        """Suivre un chemin"""
        logger.info("🛤️  Suivre chemin")

        # Implémentation simplifiée
        for _ in range(10):
            await self._send_rl_action(self.RL_ACTIONS["forward"])
            await asyncio.sleep(0.1)

        return True

    # ========== METHODES UTILITAIRES ==========

    async def _send_rl_action(self, action_id: int):
        """
        Envoie une action RL au bridge

        Args:
            action_id: ID de l'action (selon mapping JS serveur)
        """
        try:
            result = await self.bridge.send_action(action_id)

            if not result.get("success"):
                logger.warning(f"⚠️  Action {action_id} échouée")

        except Exception as e:
            logger.error(f"❌ Erreur envoi action {action_id}: {e}")

    def get_execution_history(self) -> List[Dict]:
        """Retourne l'historique d'exécution"""
        return self.execution_history


# Test
if __name__ == "__main__":
    async def test():
        from bridge.minecraft_bot_bridge import MinecraftBotBridge

        bridge = MinecraftBotBridge(host="localhost", port=8765)
        await bridge.connect()

        executor = ActionExecutor(bridge)

        decision = {
            "action": "move_to",
            "parametres": {"direction": "random", "distance": 5},
            "priorite": "moyenne"
        }

        succes = await executor.executer_decision(decision)
        print(f"Succès: {succes}")

    # asyncio.run(test())
