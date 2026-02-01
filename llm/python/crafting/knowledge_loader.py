"""
Knowledge Loader for Minecraft AI
Loads and integrates all Minecraft knowledge into semantic memory
"""

from typing import Dict, List, Any
import json

# Import all knowledge modules
from . import base_knowledge
from . import mob_knowledge
from . import block_knowledge
from . import vanilla_recipes


class KnowledgeLoader:
    """Loads and integrates all Minecraft knowledge"""

    def __init__(self):
        self.base_knowledge = base_knowledge
        self.mob_knowledge = mob_knowledge
        self.block_knowledge = block_knowledge
        self.vanilla_recipes = vanilla_recipes
        self._integrated_knowledge = {}

    def load_all_knowledge(self) -> Dict[str, Any]:
        """Load all knowledge into a unified structure"""

        return {
            'base_recipes': self._load_base_recipes(),
            'block_info': self._load_block_knowledge(),
            'mob_info': self._load_mob_knowledge(),
            'vanilla_recipes': self._load_vanilla_recipes(),
            'survival_rules': self._load_survival_rules(),
            'action_sequences': self._load_action_sequences(),
            'resource_priorities': self._load_resource_priorities(),
            'biome_info': self._load_biome_knowledge(),
        }

    def _load_base_recipes(self) -> Dict:
        """Load basic crafting recipes"""
        return self.base_knowledge.BASE_RECIPES

    def _load_block_knowledge(self) -> Dict:
        """Load block database"""
        return self.block_knowledge.BLOCK_DATABASE

    def _load_mob_knowledge(self) -> Dict:
        """Load mob database"""
        return self.mob_knowledge.MOB_DATABASE

    def _load_vanilla_recipes(self) -> Dict:
        """Load all vanilla recipes"""
        return self.vanilla_recipes.VANILLA_RECIPES

    def _load_survival_rules(self) -> Dict:
        """Load survival rules"""
        return self.base_knowledge.SURVIVAL_RULES

    def _load_action_sequences(self) -> Dict:
        """Load action sequences"""
        return self.base_knowledge.ACTION_SEQUENCES

    def _load_resource_priorities(self) -> Dict:
        """Load resource priorities"""
        return self.base_knowledge.RESOURCE_PRIORITIES

    def _load_biome_knowledge(self) -> Dict:
        """Load biome information"""
        return self.base_knowledge.BIOME_KNOWLEDGE

    # ============================================================
    # INTEGRATED QUERIES
    # ============================================================

    def get_recipe_for_item(self, item_name: str) -> Dict:
        """Get recipe to craft an item"""
        # Check vanilla recipes first
        for recipe_name, recipe in self.vanilla_recipes.VANILLA_RECIPES.items():
            if recipe['output'][0] == item_name:
                return recipe

        # Check base recipes
        return self.base_knowledge.get_recipe_for_item(item_name)

    def get_block_info(self, block_name: str) -> Dict:
        """Get information about a block"""
        return self.block_knowledge.get_block_info(block_name)

    def get_mob_info(self, mob_name: str) -> Dict:
        """Get information about a mob"""
        return self.mob_knowledge.get_mob_info(mob_name)

    def get_mob_danger(self, mob_name: str) -> str:
        """Get danger level of a mob"""
        return self.mob_knowledge.get_mob_danger_level(mob_name)

    def is_mob_hostile(self, mob_name: str) -> bool:
        """Check if a mob is hostile"""
        return self.mob_knowledge.is_mob_hostile(mob_name)

    def get_mob_strategies(self, mob_name: str) -> List:
        """Get combat strategies against a mob"""
        return self.mob_knowledge.get_mob_strategies(mob_name)

    def should_avoid_block(self, block_name: str) -> bool:
        """Check if a block should be avoided"""
        return self.block_knowledge.should_avoid(block_name)

    def should_avoid_mob(self, mob_name: str) -> bool:
        """Check if a mob should be avoided"""
        return self.mob_knowledge.should_avoid_mob(mob_name)

    # ============================================================
    # SEMANTIC MEMORY EXPORT
    # ============================================================

    def export_for_semantic_memory(self, format: str = 'dict') -> Any:
        """
        Export knowledge in a format suitable for semantic memory

        Args:
            format: 'dict', 'json', or 'text'

        Returns:
            Knowledge in the specified format
        """
        knowledge = self.load_all_knowledge()

        if format == 'json':
            return json.dumps(knowledge, indent=2)
        elif format == 'text':
            return self._format_as_text(knowledge)
        else:
            return knowledge

    def _format_as_text(self, knowledge: Dict) -> str:
        """Format knowledge as readable text"""
        sections = []

        # Basic recipes
        sections.append("=== BASIC RECIPES ===")
        for name, recipe in knowledge['base_recipes'].items():
            sections.append(f"\n{name}:")
            sections.append(f"  {recipe.get('description', 'No description')}")
            sections.append(f"  Output: {recipe['output']}")

        # Block knowledge
        sections.append("\n\n=== BLOCK KNOWLEDGE ===")
        for block_name, info in list(knowledge['block_info'].items())[:10]:  # First 10
            sections.append(f"\n{block_name}:")
            sections.append(f"  Priority: {info.get('priority', 'unknown')}")
            sections.append(f"  Description: {info.get('description', 'No description')}")
            sections.append(f"  Uses: {', '.join(info.get('uses', []))}")

        # Mob knowledge
        sections.append("\n\n=== MOB KNOWLEDGE ===")
        for mob_name, info in list(knowledge['mob_info'].items())[:10]:  # First 10
            sections.append(f"\n{mob_name}:")
            sections.append(f"  Type: {info.get('type', 'unknown')}")
            sections.append(f"  Danger: {info.get('danger_level', 'unknown')}")
            sections.append(f"  Health: {info.get('health', 'unknown')}")
            sections.append(f"  Damage: {info.get('damage', 'unknown')}")
            sections.append(f"  Strategies: {', '.join(info.get('strategies', []))}")
            sections.append(f"  Description: {info.get('description', 'No description')}")

        # Survival rules
        sections.append("\n\n=== SURVIVAL RULES ===")
        for rule_name, rule in knowledge['survival_rules'].items():
            sections.append(f"\n{rule_name}:")
            sections.append(f"  Priority: {rule.get('priority', 'unknown')}")
            sections.append(f"  Message: {rule.get('message', 'No message')}")

        # Resource priorities
        sections.append("\n\n=== RESOURCE PRIORITIES ===")
        for resource, priority in sorted(
            knowledge['resource_priorities'].items(),
            key=lambda x: x[1],
            reverse=True
        ):
            sections.append(f"{resource}: {priority}")

        return "\n".join(sections)

    # ============================================================
    # KNOWLEDGE VALIDATION
    # ============================================================

    def validate_knowledge(self) -> Dict[str, List[str]]:
        """Validate knowledge base for errors and inconsistencies"""
        errors = {
            'missing_fields': [],
            'inconsistencies': [],
            'warnings': []
        }

        # Validate mob knowledge
        for mob_name, mob in self.mob_knowledge.MOB_DATABASE.items():
            required_fields = ['type', 'health', 'categories', 'danger_level']
            for field in required_fields:
                if field not in mob:
                    errors['missing_fields'].append(
                        f"Mob {mob_name} missing field: {field}"
                    )

            # Warn if no strategies for dangerous mobs
            if mob.get('danger_level') in ['high', 'very_high', 'extreme']:
                if not mob.get('strategies'):
                    errors['warnings'].append(
                        f"Dangerous mob {mob_name} has no combat strategies"
                    )

        # Validate block knowledge
        for block_name, block in self.block_knowledge.BLOCK_DATABASE.items():
            if 'hardness' not in block:
                errors['missing_fields'].append(
                    f"Block {block_name} missing hardness"
                )

        return errors

    # ============================================================
    # SMART QUERIES
    # ============================================================

    def get_early_game_goals(self) -> List[Dict]:
        """Get recommended early game goals"""
        return self.base_knowledge.ACTION_SEQUENCES.get('early_game', [])

    def get_mid_game_goals(self) -> List[Dict]:
        """Get recommended mid game goals"""
        return self.base_knowledge.ACTION_SEQUENCES.get('mid_game', [])

    def get_survival_priority(self) -> List[str]:
        """Get survival actions in priority order"""
        rules = self.base_knowledge.SURVIVAL_RULES
        priority_order = {
            'critical': 0,
            'high': 1,
            'medium': 2,
            'low': 3
        }

        return [
            name for name, rule in sorted(
                rules.items(),
                key=lambda x: priority_order.get(x[1].get('priority', 'low'), 99)
            )
        ]

    def get_essential_resources(self) -> List[str]:
        """Get most essential resources to gather"""
        priorities = self.base_knowledge.RESOURCE_PRIORITIES
        threshold = 8  # High priority threshold
        return [
            resource for resource, priority in priorities.items()
            if priority >= threshold
        ]

    def get_dangerous_mobs(self, min_danger: str = 'high') -> List[str]:
        """Get all mobs above a certain danger level"""
        danger_levels = {
            'none': 0,
            'low': 1,
            'medium': 2,
            'high': 3,
            'very_high': 4,
            'extreme': 5
        }

        threshold = danger_levels.get(min_danger, 2)

        return [
            mob_name for mob_name, mob in self.mob_knowledge.MOB_DATABASE.items()
            if danger_levels.get(mob.get('danger_level', 'none'), 0) >= threshold
        ]

    def get_safe_blocks(self) -> List[str]:
        """Get all safe blocks to walk on"""
        return [
            block_name for block_name in self.block_knowledge.BLOCK_DATABASE
            if not self.block_knowledge.should_avoid(block_name)
        ]

    def get_tameable_animals(self) -> List[str]:
        """Get all tameable animals"""
        return [
            mob_name for mob_name, mob in self.mob_knowledge.MOB_DATABASE.items()
            if mob.get('tamable', False)
        ]

    def get_farm_animals(self) -> List[str]:
        """Get all farm animals"""
        return self.mob_knowledge.get_mobs_by_category('farm')

    def get_aquatic_mobs(self) -> List[str]:
        """Get all aquatic mobs"""
        return self.mob_knowledge.get_mobs_by_category('aquatic')

    def get_nether_mobs(self) -> List[str]:
        """Get all nether mobs"""
        return self.mob_knowledge.get_mobs_by_category('nether')

    def get_boss_mobs(self) -> List[str]:
        """Get all boss mobs"""
        return self.mob_knowledge.get_boss_mobs()


# Singleton instance
_knowledge_loader = None

def get_knowledge_loader() -> KnowledgeLoader:
    """Get the singleton knowledge loader instance"""
    global _knowledge_loader
    if _knowledge_loader is None:
        _knowledge_loader = KnowledgeLoader()
    return _knowledge_loader


# Convenience functions
def get_all_knowledge() -> Dict:
    """Get all integrated knowledge"""
    return get_knowledge_loader().load_all_knowledge()


def get_mob_info(mob_name: str) -> Dict:
    """Get information about a mob"""
    return get_knowledge_loader().get_mob_info(mob_name)


def get_block_info(block_name: str) -> Dict:
    """Get information about a block"""
    return get_knowledge_loader().get_block_info(block_name)


def get_recipe(item_name: str) -> Dict:
    """Get recipe for an item"""
    return get_knowledge_loader().get_recipe_for_item(item_name)


def is_dangerous_mob(mob_name: str) -> bool:
    """Check if a mob is dangerous"""
    return get_knowledge_loader().should_avoid_mob(mob_name)


def is_dangerous_block(block_name: str) -> bool:
    """Check if a block is dangerous"""
    return get_knowledge_loader().should_avoid_block(block_name)


def get_combat_strategies(mob_name: str) -> List:
    """Get combat strategies against a mob"""
    return get_knowledge_loader().get_mob_strategies(mob_name)


if __name__ == '__main__':
    # Test the knowledge loader
    loader = get_knowledge_loader()

    # Validate knowledge
    errors = loader.validate_knowledge()
    print("Knowledge Validation:")
    print(f"  Missing fields: {len(errors['missing_fields'])}")
    print(f"  Inconsistencies: {len(errors['inconsistencies'])}")
    print(f"  Warnings: {len(errors['warnings'])}")

    # Print some stats
    all_knowledge = loader.load_all_knowledge()
    print(f"\nKnowledge Stats:")
    print(f"  Base recipes: {len(all_knowledge['base_recipes'])}")
    print(f"  Vanilla recipes: {len(all_knowledge['vanilla_recipes'])}")
    print(f"  Blocks: {len(all_knowledge['block_info'])}")
    print(f"  Mobs: {len(all_knowledge['mob_info'])}")
    print(f"  Survival rules: {len(all_knowledge['survival_rules'])}")

    # Get some examples
    print(f"\nDangerous mobs: {loader.get_dangerous_mobs('high')[:5]}")
    print(f"Tameable animals: {loader.get_tameable_animals()}")
    print(f"Essential resources: {loader.get_essential_resources()}")
