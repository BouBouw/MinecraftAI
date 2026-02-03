"""
LLM-Agent - Agent Hybride RL + LLM pour Minecraft

Architecture modulaire à 3 couches:
1. Percepteur: Minecraft → Texte
2. Raisonneur: LLM (Claude/GPT)
3. Exécuteur: LLM → Actions RL
"""

__version__ = "0.1.0"
__author__ = "MinecraftAI Project"

from .raisonner.llm_decision import LLMDecisionMaker
from .executeur.action_executor import ActionExecutor

__all__ = [
    "LLMDecisionMaker",
    "ActionExecutor",
    "HybridAgent"
]
