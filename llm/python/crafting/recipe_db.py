"""
Recipe Database - Stores and manages discovered crafting recipes.
Provides efficient lookup and query capabilities.
"""

import json
from typing import Dict, Any, List, Optional, Set
from pathlib import Path

from memory.database import DatabaseManager, get_database_manager
from utils.config import get_config
from utils.logger import get_logger

logger = get_logger(__name__)


class RecipeDatabase:
    """
    Recipe database for storing and querying discovered recipes

    Features:
    - Efficient recipe lookup by input or output
    - Recipe search and filtering
    - Import/export from JSON
    - Recipe validation
    - Duplicate detection
    """

    def __init__(self, db_manager: DatabaseManager = None):
        """
        Initialize recipe database

        Args:
            db_manager: Database manager instance
        """
        self.db = db_manager or get_database_manager()
        self.config = get_config()

        # In-memory cache for fast lookups
        self._cache: Dict[str, Dict[str, Any]] = {}
        self._output_index: Dict[str, List[str]] = {}  # output -> list of recipe IDs

        # Load recipes from database
        self._load_from_db()

        logger.info(f"Recipe Database initialized with {len(self._cache)} recipes")

    def _load_from_db(self):
        """Load recipes from database into cache"""
        recipes = self.db.get_discovered_recipes()

        for recipe in recipes:
            recipe_id = self._add_to_cache(
                input_grid=json.loads(recipe['input_grid']),
                output_item=recipe['output_item'],
                output_count=recipe['output_count'],
                metadata={
                    'id': recipe['id'],
                    'discovered_at': recipe['discovered_at'],
                    'discovery_method': recipe['discovery_method'],
                    'confidence': recipe['confidence'],
                    'success_count': recipe['success_count'],
                    'failure_count': recipe['failure_count']
                }
            )

    def _add_to_cache(
        self,
        input_grid: List[List[int]],
        output_item: str,
        output_count: int,
        metadata: Dict[str, Any] = None
    ) -> str:
        """
        Add recipe to cache

        Args:
            input_grid: Input crafting grid
            output_item: Output item name
            output_count: Output item count
            metadata: Additional metadata

        Returns:
            Recipe ID
        """
        # Generate recipe ID from input grid
        recipe_id = self._grid_to_id(input_grid)

        recipe_data = {
            'input_grid': input_grid,
            'output': output_item,
            'output_count': output_count,
            'metadata': metadata or {}
        }

        self._cache[recipe_id] = recipe_data

        # Update output index
        if output_item not in self._output_index:
            self._output_index[output_item] = []

        if recipe_id not in self._output_index[output_item]:
            self._output_index[output_item].append(recipe_id)

        return recipe_id

    def _grid_to_id(self, grid: List[List[int]]) -> str:
        """
        Convert grid to recipe ID

        Args:
            grid: Crafting grid

        Returns:
            Recipe ID string
        """
        return json.dumps(grid)

    def add_recipe(
        self,
        input_grid: List[List[int]],
        output_item: str,
        output_count: int = 1,
        discovery_method: str = 'experiment',
        confidence: float = 1.0
    ) -> str:
        """
        Add a new recipe to database

        Args:
            input_grid: Input crafting grid
            output_item: Output item name
            output_count: Output item count
            discovery_method: How recipe was discovered
            confidence: Recipe confidence

        Returns:
            Recipe ID
        """
        # Store in database
        recipe_id = self.db.store_discovered_recipe(
            input_grid=input_grid,
            output_item=output_item,
            output_count=output_count,
            discovery_method=discovery_method
        )

        # Add to cache
        cache_id = self._add_to_cache(
            input_grid=input_grid,
            output_item=output_item,
            output_count=output_count,
            metadata={
                'id': recipe_id,
                'discovery_method': discovery_method,
                'confidence': confidence,
                'success_count': 1,
                'failure_count': 0
            }
        )

        logger.info(f"Added recipe: {output_item} (id={recipe_id})")
        return cache_id

    def get_recipe(self, recipe_id: str) -> Optional[Dict[str, Any]]:
        """
        Get recipe by ID

        Args:
            recipe_id: Recipe ID

        Returns:
            Recipe data or None
        """
        return self._cache.get(recipe_id)

    def find_recipes_by_output(self, output_item: str) -> List[Dict[str, Any]]:
        """
        Find all recipes that produce a given item

        Args:
            output_item: Output item name

        Returns:
            List of recipes
        """
        recipe_ids = self._output_index.get(output_item, [])

        recipes = []
        for recipe_id in recipe_ids:
            recipe = self._cache.get(recipe_id)
            if recipe:
                recipes.append(recipe)

        return recipes

    def find_recipe_by_input(
        self,
        input_grid: List[List[int]],
        exact: bool = True
    ) -> Optional[Dict[str, Any]]:
        """
        Find recipe by input grid

        Args:
            input_grid: Input crafting grid
            exact: Whether to require exact match

        Returns:
            Recipe data or None
        """
        if exact:
            recipe_id = self._grid_to_id(input_grid)
            return self._cache.get(recipe_id)
        else:
            # Find similar recipes
            return self._find_similar_recipe(input_grid)

    def _find_similar_recipe(
        self,
        input_grid: List[List[int]]
    ) -> Optional[Dict[str, Any]]:
        """
        Find recipe similar to input grid

        Args:
            input_grid: Input crafting grid

        Returns:
            Most similar recipe or None
        """
        best_match = None
        best_similarity = 0

        for recipe_id, recipe in self._cache.items():
            similarity = self._calculate_similarity(input_grid, recipe['input_grid'])

            if similarity > best_similarity:
                best_similarity = similarity
                best_match = recipe

        # Only return if reasonably similar (>70%)
        if best_similarity > 0.7:
            return best_match

        return None

    def _calculate_similarity(
        self,
        grid1: List[List[int]],
        grid2: List[List[int]]
    ) -> float:
        """
        Calculate similarity between two grids

        Args:
            grid1: First grid
            grid2: Second grid

        Returns:
            Similarity score (0-1)
        """
        matches = 0
        total = 0

        for i in range(3):
            for j in range(3):
                if grid1[i][j] == grid2[i][j]:
                    matches += 1
                if grid1[i][j] != 0 or grid2[i][j] != 0:
                    total += 1

        if total == 0:
            return 0.0

        return matches / total

    def can_craft(
        self,
        output_item: str,
        inventory: List[Dict[str, Any]]
    ) -> bool:
        """
        Check if we can craft an item with current inventory

        Args:
            output_item: Item to craft
            inventory: Current inventory

        Returns:
            True if craftable
        """
        recipes = self.find_recipes_by_output(output_item)

        if not recipes:
            return False

        # Get available items from inventory
        available_items = set()
        for slot in inventory:
            if slot and slot.get('count', 0) > 0:
                item_id = slot.get('item_id', 0)
                if item_id > 0:
                    available_items.add(item_id)

        # Check if any recipe can be satisfied
        for recipe in recipes:
            required_items = set()

            for row in recipe['input_grid']:
                for item_id in row:
                    if item_id > 0:
                        required_items.add(item_id)

            if required_items.issubset(available_items):
                return True

        return False

    def get_crafting_cost(
        self,
        output_item: str
    ) -> Dict[int, int]:
        """
        Get material cost to craft an item

        Args:
            output_item: Item to craft

        Returns:
            Dictionary mapping item_id -> required count
        """
        recipes = self.find_recipes_by_output(output_item)

        if not recipes:
            return {}

        # Use the first (best) recipe
        recipe = recipes[0]

        # Count materials
        materials = {}

        for row in recipe['input_grid']:
            for item_id in row:
                if item_id > 0:
                    materials[item_id] = materials.get(item_id, 0) + 1

        return materials

    def search_recipes(
        self,
        query: str = None,
        min_confidence: float = 0.0,
        output_type: str = None
    ) -> List[Dict[str, Any]]:
        """
        Search recipes with filters

        Args:
            query: Search query (matches output names)
            min_confidence: Minimum confidence threshold
            output_type: Filter by output type

        Returns:
            List of matching recipes
        """
        results = []

        for recipe_id, recipe in self._cache.items():
            # Filter by output type
            if output_type and recipe['output'] != output_type:
                continue

            # Filter by confidence
            confidence = recipe.get('metadata', {}).get('confidence', 1.0)
            if confidence < min_confidence:
                continue

            # Filter by query
            if query and query.lower() not in recipe['output'].lower():
                continue

            results.append(recipe)

        return results

    def get_all_recipes(self) -> List[Dict[str, Any]]:
        """Get all recipes"""
        return list(self._cache.values())

    def get_statistics(self) -> Dict[str, Any]:
        """Get database statistics"""
        total_recipes = len(self._cache)
        unique_outputs = len(self._output_index)

        # Count by discovery method
        by_method = {}
        for recipe in self._cache.values():
            method = recipe.get('metadata', {}).get('discovery_method', 'unknown')
            by_method[method] = by_method.get(method, 0) + 1

        return {
            'total_recipes': total_recipes,
            'unique_outputs': unique_outputs,
            'by_discovery_method': by_method,
        }

    def export_to_json(self, filepath: str):
        """
        Export all recipes to JSON file

        Args:
            filepath: Path to save file
        """
        data = {
            'recipes': list(self._cache.values()),
            'statistics': self.get_statistics(),
            'exported_at': str(datetime.now())
        }

        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2, default=str)

        logger.info(f"Exported {len(self._cache)} recipes to {filepath}")

    def import_from_json(self, filepath: str):
        """
        Import recipes from JSON file

        Args:
            filepath: Path to JSON file
        """
        with open(filepath, 'r') as f:
            data = json.load(f)

        count = 0
        for recipe_data in data.get('recipes', []):
            try:
                self.add_recipe(
                    input_grid=recipe_data['input_grid'],
                    output_item=recipe_data['output'],
                    output_count=recipe_data.get('output_count', 1),
                    discovery_method=recipe_data.get('metadata', {}).get('discovery_method', 'imported'),
                    confidence=recipe_data.get('metadata', {}).get('confidence', 1.0)
                )
                count += 1
            except Exception as e:
                logger.error(f"Error importing recipe: {e}")

        logger.info(f"Imported {count} recipes from {filepath}")

    def clear_cache(self):
        """Clear in-memory cache (reload from database)"""
        self._cache.clear()
        self._output_index.clear()
        self._load_from_db()

        logger.info("Recipe cache cleared and reloaded")

    def __len__(self) -> int:
        """Get total number of recipes"""
        return len(self._cache)

    def __repr__(self) -> str:
        stats = self.get_statistics()
        return f"RecipeDatabase(recipes={stats['total_recipes']}, outputs={stats['unique_outputs']})"
