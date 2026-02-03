"""
RAISONNEUR - Le cerveau LLM qui décide de la stratégie

Ce module prend le rapport du Percepteur et décide de la prochaine action
en utilisant un LLM (GLM 4.7 via Z.ai, Claude, ou modèle local).
"""

import json
import os
import aiohttp
from typing import Dict, Any, Optional

from utils.logger import get_logger

logger = get_logger(__name__)

# Import optionnel d'Anthropic
try:
    from anthropic import Anthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False
    logger.info("ℹ️  Module anthropic non installé")


class LLMDecisionMaker:
    """
    Raisonneur LLM pour Minecraft Agent

    Utilise GLM 4.7 (Z.ai), Claude/Anthropic API pour prendre des décisions intelligentes
    basées sur l'état actuel du jeu.
    """

    # Actions disponibles que le LLM peut choisir
    ACTIONS_DISPONIBLES = {
        "move_to": "Se déplacer vers des coordonnées [x, y, z]",
        "follow_path": "Suivre un chemin vers une cible",
        "mine_block": "Miner un bloc spécifique",
        "collect_drops": "Ramasser les items au sol",
        "craft_item": "Fabriquer un objet",
        "place_block": "Placer un bloc",
        "attack_entity": "Attaquer une entité hostile",
        "eat_food": "Manger pour restaurer la faim",
        "equip_item": "Équiper un item",
        "wait": "Attendre/observer"
    }

    PROMPT_SYSTEM = """Tu es un agent intelligent dans Minecraft. Ton but est de survivre et progresser.

CONTEXTE:
- Tu es un bot qui contrôle un personnage Minecraft
- Tu peux percevoir ton environnement via des rapports textuels
- Tu dois décider de la meilleure action à entreprendre

ACTIONS DISPONIBLES:
{actions}

FORMAT DE RÉPONSE OBLIGATOIRE (JSON uniquement):
{{
  "pensee": "ton raisonnement en 1-2 phrases",
  "action": "nom_action",
  "parametres": {{}},
  "priorite": "haute|moyenne|basse"
}}

RÈGLES:
1. Réponds UNIQUEMENT en JSON valide
2. Si la faim < 10, priorité absolue: "eat_food"
3. Si la santé < 10, priorité absolue: fuir ou "eat_food"
4. Si tu vois des minerais précieux, priorité: les miner
5. Sois concis et précis dans les paramètres
6. Explique ton raisonnement dans "pensee"
"""

    def __init__(self, api_key: Optional[str] = None, provider: str = "z.ai"):
        """
        Initialize LLM Decision Maker

        Args:
            api_key: Clé API (si None, utilise la variable d'environnement)
            provider: "z.ai" pour GLM 4.7, "anthropic" pour Claude
        """
        self.provider = provider

        if provider == "z.ai":
            self.api_key = api_key or os.getenv('ZAI_API_KEY')
            if not self.api_key:
                logger.warning("⚠️  Pas de clé API Z.ai - Mode démo uniquement")
                self.client = None
            else:
                logger.info("✅ Utilisation de Z.ai (GLM 4.7)")
                self.client = True  # Marker pour utiliser Z.ai

        elif provider == "anthropic":
            self.api_key = api_key or os.getenv('ANTHROPIC_API_KEY')

            if not ANTHROPIC_AVAILABLE:
                logger.warning("⚠️  Module anthropic non installé - Mode démo uniquement")
                self.client = None
            elif not self.api_key:
                logger.warning("⚠️  Pas de clé API Anthropic - Mode démo uniquement")
                self.client = None
            else:
                self.client = Anthropic(api_key=self.api_key)
                logger.info("✅ Utilisation de Claude (Anthropic)")

        else:
            logger.warning(f"⚠️  Provider inconnu: {provider} - Mode démo uniquement")
            self.client = None

        self.historique_decisions = []

    async def decider(self, rapport_percepteur: str, objectif_actuel: str) -> Dict[str, Any]:
        """
        Prend une décision basée sur l'état actuel

        Args:
            rapport_percepteur: Rapport textuel du Percepteur
            objectif_actuel: Objectif courant (ex: "Miner 3 blocs de fer")

        Returns:
            Dictionnaire avec l'action décidée
        """
        logger.info(f"🧠 Raisonnement en cours... Objectif: {objectif_actuel}")

        if self.client:
            decision = await self._llm_decision(rapport_percepteur, objectif_actuel)
        else:
            # Mode démo - règles simples
            decision = self._demo_decision(rapport_percepteur, objectif_actuel)

        # Enregistrer dans l'historique
        self.historique_decisions.append({
            'contexte': rapport_percepteur,
            'objectif': objectif_actuel,
            'decision': decision,
            'timestamp': __import__('datetime').datetime.now().isoformat()
        })

        logger.info(f"✅ Décision: {decision['action']} - {decision.get('pensee', '')}")
        return decision

    async def _llm_decision(self, rapport: str, objectif: str) -> Dict[str, Any]:
        """
        Utilise le LLM pour prendre une décision

        Args:
            rapport: État actuel du jeu
            objectif: Objectif à accomplir

        Returns:
            Décision du LLM
        """
        actions_text = "\n".join([
            f"  - {name}: {desc}" for name, desc in self.ACTIONS_DISPONIBLES.items()
        ])

        prompt = f"""{self.PROMPT_SYSTEM.format(actions=actions_text)}

OBJECTIF ACTUEL: {objectif}

ÉTAT ACTUEL:
{rapport}

Décide de la meilleure action à entreprendre:"""

        try:
            if self.provider == "z.ai":
                return await self._zai_decision(prompt)
            elif self.provider == "anthropic" and self.client:
                return await self._anthropic_decision(prompt)
            else:
                raise Exception("No valid LLM client available")

        except Exception as e:
            logger.error(f"❌ Erreur LLM: {e}")
            # Fallback sur mode démo
            return self._demo_decision(rapport, objectif)

    def _demo_decision(self, rapport: str, objectif: str) -> Dict[str, Any]:
        """
        Mode démo - règles simples si pas d'API LLM

        Args:
            rapport: État actuel
            objectif: Objectif

        Returns:
            Décision basée sur règles
        """
        # Analyse simple du rapport
        faim_basse = 'Faim:' in rapport and any(x in rapport for x in ['[URGENT', '[BAS'])
        sante_critique = 'SANTÉ' in rapport and 'CRITIQUE' in rapport

        if faim_basse:
            return {
                "pensee": "Faim critique - besoin de manger",
                "action": "eat_food",
                "parametres": {},
                "priorite": "haute"
            }

        if sante_critique:
            return {
                "pensee": "Santé critique - fuir le danger",
                "action": "move_to",
                "parametres": {"x": 0, "y": 64, "z": 0},  # Point de sécurité
                "priorite": "haute"
            }

        if 'fer' in objectif.lower() and 'iron_ore' in rapport:
            return {
                "pensee": "Miner de fer pour atteindre l'objectif",
                "action": "mine_block",
                "parametres": {"block_type": "iron_ore"},
                "priorite": "moyenne"
            }

        if 'wood' in objectif.lower() and 'oak_log' in rapport:
            return {
                "pensee": "Couper du bois pour l'objectif",
                "action": "mine_block",
                "parametres": {"block_type": "oak_log"},
                "priorite": "moyenne"
            }

        # Action par défaut - explorer
        return {
            "pensee": "Explorer pour trouver des ressources",
            "action": "move_to",
            "parametres": {"direction": "random", "distance": 20},
            "priorite": "basse"
        }

    async def _zai_decision(self, prompt: str) -> Dict[str, Any]:
        """
        Utilise Z.ai (GLM 4.7) pour prendre une décision

        Args:
            prompt: Prompt complet à envoyer à GLM

        Returns:
            Décision de GLM 4.7
        """
        # API Zhipu AI (GLM 4.7)
        url = "https://open.bigmodel.cn/api/paas/v4/chat/completions"

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": "glm-4-flash",  # GLM 4 Flash (plus rapide) ou "glm-4-plus"
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": 0.3,
            "max_tokens": 1024,
            "top_p": 0.7
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload, headers=headers) as response:
                if response.status != 200:
                    error_text = await response.text()
                    logger.error(f"❌ Z.ai API error: {response.status} - {error_text}")
                    raise Exception(f"Z.ai API error: {response.status}")

                data = await response.json()

                # Extraire la réponse
                if "choices" in data and len(data["choices"]) > 0:
                    response_text = data["choices"][0]["message"]["content"]
                else:
                    logger.error(f"❌ Z.ai invalid response: {data}")
                    raise Exception("Invalid Z.ai response format")

                # Parser le JSON
                decision = self._parse_json_response(response_text)
                return decision

    async def _anthropic_decision(self, prompt: str) -> Dict[str, Any]:
        """
        Utilise Claude (Anthropic) pour prendre une décision

        Args:
            prompt: Prompt complet à envoyer à Claude

        Returns:
            Décision de Claude
        """
        response = await self.client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1024,
            temperature=0.3,
            messages=[{
                "role": "user",
                "content": prompt
            }]
        )

        response_text = response.content[0].text
        decision = self._parse_json_response(response_text)
        return decision

    def _parse_json_response(self, response_text: str) -> Dict[str, Any]:
        """
        Extrait le JSON de la réponse LLM

        Args:
            response_text: Texte de réponse du LLM

        Returns:
            Dictionnaire JSON
        """
        # Chercher le premier objet JSON dans la réponse
        import re

        # Pattern pour trouver {...}
        json_match = re.search(r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}', response_text)

        if json_match:
            try:
                return json.loads(json_match.group())
            except json.JSONDecodeError:
                pass

        # Fallback si pas de JSON trouvé
        logger.warning("⚠️  Pas de JSON valide dans la réponse LLM")
        return {
            "pensee": "Réponse LLM invalide",
            "action": "wait",
            "parametres": {},
            "priorite": "basse"
        }

    def get_historique(self) -> list:
        """Retourne l'historique des décisions"""
        return self.historique_decisions


# Test simple
if __name__ == "__main__":
    async def test():
        raisonner = LLMDecisionMaker()

        rapport = """
        📍 POSITION: [10, 64, 20]
           Orientation: Sud

        ❤️ SANTÉ: Bonne (18/20)
        🍗 FAIM: 5/20 [URGENT - MANGER]

        🎒 INVENTAIRE:
           - apple: x5

        👁️ BLOCS VISIBLES (rayon 5):
           - oak_log: x3

        🐾 ENTITÉS PROCHES (16 blocs):
           🐄 pig: x2
        """

        decision = await raisonner.decider(rapport, "Survivre")
        print(json.dumps(decision, indent=2))

    import asyncio
    asyncio.run(test())
