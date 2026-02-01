"""
Craft Discovery System for Minecraft RL Agent.
Autonomously discovers and learns crafting recipes through experimentation.
"""

import numpy as np
from typing import Dict, Any, List, Optional, Tuple
from collections import defaultdict, deque
from dataclasses import dataclass
from datetime import datetime
import json

from memory.database import DatabaseManager, get_database_manager
from utils.config import get_config
from utils.logger import get_logger

logger = get_logger(__name__)


@dataclass
class CraftExperiment:
    """A single crafting experiment"""
    input_grid: List[List[int]]  # 3x3 grid
    expected_output: Optional[int] = None
    confidence: float = 0.0
    tries: int = 0


class CraftDiscoverySystem:
    """
    Autonomous craft discovery system

    Discovers Minecraft crafting recipes through:
    - Intelligent experimentation based on inventory
    - Pattern recognition (similar items → similar recipes)
    - Statistical learning from success/failure
    - Transfer learning between similar items
    """

    def __init__(self, db_manager: DatabaseManager = None):
        """
        Initialize craft discovery system

        Args:
            db_manager: Database manager instance
        """
        self.db = db_manager or get_database_manager()
        config = get_config()

        self.craft_config = config.get('craft_discovery', {})
        self.max_experiments = self.craft_config.get('max_experiments_per_episode', 50)
        self.strategy = self.craft_config.get('experiment_strategy', 'curiosity')

        # Known recipes (discovered so far)
        self.known_recipes: Dict[str, Dict[str, Any]] = {}

        # Experiment tracking
        self.experiment_history: deque = deque(maxlen=10000)
        self.success_count = 0
        self.failure_count = 0

        # Item relationships for inference
        self.item_relationships: Dict[str, List[str]] = defaultdict(list)

        # Load previously discovered recipes
        self._load_known_recipes()

        logger.info("Craft Discovery System initialized")

    def _load_known_recipes(self):
        """Load previously discovered recipes from database"""
        recipes = self.db.get_discovered_recipes()

        for recipe in recipes:
            input_grid = json.loads(recipe['input_grid'])
            output = recipe['output_item']

            # Create key from input grid
            key = self._grid_to_key(input_grid)

            self.known_recipes[key] = {
                'input_grid': input_grid,
                'output': output,
                'output_count': recipe['output_count'],
                'confidence': recipe['confidence'],
                'success_count': recipe['success_count'],
                'discovery_method': recipe['discovery_method']
            }

        logger.info(f"Loaded {len(self.known_recipes)} known recipes")

    def _grid_to_key(self, grid: List[List[int]]) -> str:
        """
        Convert crafting grid to string key

        Args:
            grid: 3x3 crafting grid

        Returns:
            String key
        """
        return json.dumps(grid)

    def suggest_experiment(self, inventory: List[Dict]) -> Optional[CraftExperiment]:
        """
        Suggest a crafting experiment to try

        Args:
            inventory: Current inventory state

        Returns:
            Craft experiment to try, or None if no good experiments
        """
        if self.experiment_history.__len__() >= self.max_experiments:
            logger.debug("Max experiments reached for this episode")
            return None

        # Get available items
        available_items = self._get_available_items(inventory)

        if not available_items:
            return None

        # Select experiment strategy
        if self.strategy == 'curiosity':
            return self._suggest_curiosity_experiment(available_items, inventory)
        elif self.strategy == 'random':
            return self._suggest_random_experiment(available_items)
        elif self.strategy == 'guided':
            return self._suggest_guided_experiment(available_items, inventory)
        else:
            return self._suggest_curiosity_experiment(available_items, inventory)

    def _get_available_items(self, inventory: List[Dict]) -> List[int]:
        """
        Get list of available item IDs from inventory

        Args:
            inventory: Inventory state

        Returns:
            List of available item IDs
        """
        available = []

        for slot in inventory:
            if slot and slot.get('count', 0) > 0:
                item_id = slot.get('item_id', 0)
                if item_id > 0 and item_id not in available:
                    available.append(item_id)

        return available

    def _suggest_curiosity_experiment(
        self,
        available_items: List[int],
        inventory: List[Dict]
    ) -> Optional[CraftExperiment]:
        """
        Suggest experiment based on curiosity (novelty-seeking)

        Args:
            available_items: Available item IDs
            inventory: Full inventory state

        Returns:
            Craft experiment
        """
        # Strategy 1: Try combinations of similar items
        # Strategy 2: Try patterns that worked before with different items
        # Strategy 3: Try new arrangements of known crafting materials

        experiments = []

        # Try 2x2 patterns (planks, sticks, etc.)
        if len(available_items) >= 1:
            item = available_items[0]
            experiments.append(self._create_2x2_pattern(item))

        # Try line patterns
        if len(available_items) >= 3:
            experiments.append(self._create_line_pattern(available_items[:3]))

        # Try L-shapes
        if len(available_items) >= 3:
            experiments.append(self._create_l_shape(available_items[:3]))

        # Select most novel experiment
        best_experiment = None
        best_novelty = 0

        for exp in experiments:
            novelty = self._calculate_novelty(exp)
            if novelty > best_novelty:
                best_novelty = novelty
                best_experiment = exp

        return best_experiment

    def _suggest_random_experiment(
        self,
        available_items: List[int]
    ) -> Optional[CraftExperiment]:
        """
        Suggest random crafting experiment

        Args:
            available_items: Available item IDs

        Returns:
            Craft experiment
        """
        if len(available_items) < 1:
            return None

        # Random grid size (1x1, 2x2, or 3x3)
        grid_size = np.random.choice([1, 2, 3])

        # Create random pattern
        grid = [[0] * 3 for _ in range(3)]

        for i in range(grid_size):
            for j in range(grid_size):
                if np.random.random() > 0.3:  # 70% chance to place item
                    grid[i][j] = np.random.choice(available_items)

        return CraftExperiment(
            input_grid=grid,
            confidence=0.5,
            tries=0
        )

    def _suggest_guided_experiment(
        self,
        available_items: List[int],
        inventory: List[Dict]
    ) -> Optional[CraftExperiment]:
        """
        Suggest experiment based on known patterns

        Args:
            available_items: Available item IDs
            inventory: Full inventory state

        Returns:
            Craft experiment
        """
        # Try known patterns with new materials
        # E.g., if "wood -> planks" works, try "stone -> something"

        # Get high-confidence recipes
        confident_recipes = [
            r for r in self.known_recipes.values()
            if r['confidence'] > 0.8
        ]

        if not confident_recipes:
            return self._suggest_curiosity_experiment(available_items, inventory)

        # Pick a random successful pattern and try with different materials
        base_recipe = np.random.choice(confident_recipes)
        base_grid = base_recipe['input_grid']

        # Find items used in base recipe
        used_items = set()
        for row in base_grid:
            for item_id in row:
                if item_id > 0:
                    used_items.add(item_id)

        # Try to substitute with similar items
        new_grid = [[0] * 3 for _ in range(3)]

        for i in range(3):
            for j in range(3):
                original_item = base_grid[i][j]
                if original_item in used_items:
                    # Try to find a similar item in inventory
                    similar = self._find_similar_item(original_item, available_items)
                    new_grid[i][j] = similar if similar else original_item
                else:
                    new_grid[i][j] = original_item

        return CraftExperiment(
            input_grid=new_grid,
            expected_output=None,
            confidence=0.6,
            tries=0
        )

    def _create_2x2_pattern(self, item_id: int) -> CraftExperiment:
        """Create a 2x2 crafting pattern"""
        grid = [[0] * 3 for _ in range(3)]
        grid[0][0] = item_id
        grid[0][1] = item_id
        grid[1][0] = item_id
        grid[1][1] = item_id

        return CraftExperiment(
            input_grid=grid,
            expected_output=None,
            confidence=0.7,
            tries=0
        )

    def _create_line_pattern(self, items: List[int]) -> CraftExperiment:
        """Create a line crafting pattern"""
        grid = [[0] * 3 for _ in range(3)]
        for i in range(min(3, len(items))):
            grid[1][i] = items[i]

        return CraftExperiment(
            input_grid=grid,
            expected_output=None,
            confidence=0.6,
            tries=0
        )

    def _create_l_shape(self, items: List[int]) -> CraftExperiment:
        """Create an L-shaped crafting pattern"""
        grid = [[0] * 3 for _ in range(3)]
        if len(items) >= 3:
            grid[0][0] = items[0]
            grid[1][0] = items[1]
            grid[2][0] = items[2]
            grid[2][1] = items[0]  # Reuse first item

        return CraftExperiment(
            input_grid=grid,
            expected_output=None,
            confidence=0.5,
            tries=0
        )

    def _calculate_novelty(self, experiment: CraftExperiment) -> float:
        """
        Calculate novelty score for an experiment

        Args:
            experiment: Craft experiment

        Returns:
            Novelty score (0-1)
        """
        key = self._grid_to_key(experiment.input_grid)

        # If we've tried this exact pattern, low novelty
        if key in self.known_recipes:
            return 0.1

        # Check if we've tried similar patterns
        for known_key, known_recipe in self.known_recipes.items():
            similarity = self._pattern_similarity(experiment.input_grid, known_recipe['input_grid'])
            if similarity > 0.8:
                # Very similar pattern exists, lower novelty
                return 0.3

        # Completely new pattern
        return 1.0

    def _pattern_similarity(self, grid1: List[List[int]], grid2: List[List[int]]) -> float:
        """
        Calculate similarity between two crafting patterns

        Args:
            grid1: First crafting grid
            grid2: Second crafting grid

        Returns:
            Similarity score (0-1)
        """
        matches = 0
        total = 0

        for i in range(3):
            for j in range(3):
                if grid1[i][j] == grid2[i][j] and grid1[i][j] != 0:
                    matches += 1
                if grid1[i][j] != 0 or grid2[i][j] != 0:
                    total += 1

        if total == 0:
            return 0.0

        return matches / total

    def _find_similar_item(self, item_id: int, available_items: List[int]) -> Optional[int]:
        """
        Find similar item in available items

        Args:
            item_id: Item to find similar for
            available_items: Available items

        Returns:
            Similar item ID or None
        """
        # Simple similarity: same item type (e.g., different wood types)
        # In a full implementation, this would use embeddings or item properties

        # For now, just return a different item if available
        for item in available_items:
            if item != item_id:
                return item

        return None

    def execute_experiment(
        self,
        experiment: CraftExperiment,
        bot_client
    ) -> Dict[str, Any]:
        """
        Execute a crafting experiment

        Args:
            experiment: Craft experiment to execute
            bot_client: Bot client to execute craft

        Returns:
            Result dictionary
        """
        experiment.tries += 1

        # Try to execute the craft
        try:
            result = self._try_craft(experiment.input_grid, bot_client)

            if result['success']:
                self.success_count += 1
                self._learn_recipe(experiment.input_grid, result['output'], result['count'])

                logger.info(f"✅ New recipe discovered: {result['output']} x{result['count']}")
            else:
                self.failure_count += 1

            # Record experiment
            self.experiment_history.append({
                'input_grid': experiment.input_grid,
                'output': result.get('output'),
                'success': result['success'],
                'timestamp': datetime.now().isoformat()
            })

            return result

        except Exception as e:
            logger.error(f"Error executing craft experiment: {e}")
            return {
                'success': False,
                'error': str(e)
            }

    def _try_craft(self, grid: List[List[int]], bot_client) -> Dict[str, Any]:
        """
        Attempt to craft with given grid

        Args:
            grid: Crafting grid
            bot_client: Bot to execute craft

        Returns:
            Result dictionary
        """
        # This would call the bot's crafting interface
        # For now, return a mock result

        # Check if this is a known recipe
        key = self._grid_to_key(grid)

        if key in self.known_recipes:
            recipe = self.known_recipes[key]
            return {
                'success': True,
                'output': recipe['output'],
                'count': recipe['output_count']
            }

        # Unknown recipe - try anyway
        # In a real implementation, this would call the bot

        return {
            'success': False,
            'output': None
        }

    def _learn_recipe(
        self,
        input_grid: List[List[int]],
        output_item: str,
        output_count: int
    ):
        """
        Learn a new recipe

        Args:
            input_grid: Input crafting grid
            output_item: Output item name
            output_count: Output item count
        """
        key = self._grid_to_key(input_grid)

        # Store in memory
        self.known_recipes[key] = {
            'input_grid': input_grid,
            'output': output_item,
            'output_count': output_count,
            'confidence': 1.0,
            'success_count': 1,
            'discovery_method': 'experiment'
        }

        # Store in database
        self.db.store_discovered_recipe(
            input_grid=input_grid,
            output_item=output_item,
            output_count=output_count,
            discovery_method='experiment'
        )

        # Update item relationships
        self._update_item_relationships(input_grid, output_item)

    def _update_item_relationships(self, input_grid: List[List[int]], output_item: str):
        """
        Update item relationship graph

        Args:
            input_grid: Input crafting grid
            output_item: Output item name
        """
        # Extract input items
        input_items = set()
        for row in input_grid:
            for item_id in row:
                if item_id > 0:
                    input_items.add(item_id)

        # Record relationships
        for item_id in input_items:
            self.item_relationships[str(item_id)].append(output_item)

    def get_known_recipes(self) -> List[Dict[str, Any]]:
        """Get all known recipes"""
        return list(self.known_recipes.values())

    def get_recipes_for_item(self, item_name: str) -> List[Dict[str, Any]]:
        """
        Get all recipes that produce an item

        Args:
            item_name: Item name to search for

        Returns:
            List of recipes
        """
        return [
            recipe for recipe in self.known_recipes.values()
            if recipe['output'] == item_name
        ]

    def can_craft(self, item_name: str, inventory: List[Dict]) -> bool:
        """
        Check if we can craft an item with current inventory

        Args:
            item_name: Item to craft
            inventory: Current inventory

        Returns:
            True if craftable
        """
        recipes = self.get_recipes_for_item(item_name)

        if not recipes:
            return False

        # Check if we have ingredients for any recipe
        available_items = self._get_available_items(inventory)

        for recipe in recipes:
            required_items = set()
            for row in recipe['input_grid']:
                for item_id in row:
                    if item_id > 0:
                        required_items.add(item_id)

            if required_items.issubset(set(available_items)):
                return True

        return False

    def get_statistics(self) -> Dict[str, Any]:
        """Get discovery system statistics"""
        return {
            'total_recipes': len(self.known_recipes),
            'success_count': self.success_count,
            'failure_count': self.failure_count,
            'experiments_this_episode': len(self.experiment_history),
            'success_rate': (
                self.success_count / (self.success_count + self.failure_count)
                if (self.success_count + self.failure_count) > 0
                else 0
            ),
            'item_relationships': len(self.item_relationships),
        }

    def __repr__(self) -> str:
        stats = self.get_statistics()
        return f"CraftDiscoverySystem(recipes={stats['total_recipes']}, rate={stats['success_rate']:.2%})"
