"""
Recipe Learner - Learns crafting patterns and infers new recipes.
Uses pattern recognition to infer similar recipes.
"""

import numpy as np
from typing import Dict, Any, List, Tuple, Optional
from collections import defaultdict
import json

from utils.config import get_config
from utils.logger import get_logger

logger = get_logger(__name__)


class RecipeLearner:
    """
    Learns and generalizes from discovered recipes

    Features:
    - Pattern extraction from successful recipes
    - Item similarity detection
    - Recipe inference for similar items
    - Confidence scoring for inferred recipes
    """

    def __init__(self):
        """Initialize recipe learner"""
        self.config = get_config()

        # Recipe patterns discovered
        self.patterns: Dict[str, List[Dict]] = defaultdict(list)

        # Item embeddings (simplified - would use real embeddings in production)
        self.item_embeddings: Dict[str, np.ndarray] = {}

        # Recipe templates
        self.templates: List[Dict] = []

        # Statistics
        self.inference_success = 0
        self.inference_failure = 0

        logger.info("Recipe Learner initialized")

    def learn_from_recipe(
        self,
        input_grid: List[List[int]],
        output_item: str,
        output_count: int
    ):
        """
        Learn from a newly discovered recipe

        Args:
            input_grid: Input crafting grid
            output_item: Output item name
            output_count: Output item count
        """
        # Extract pattern
        pattern = self._extract_pattern(input_grid)

        # Store pattern
        pattern_key = self._pattern_to_key(pattern)
        self.patterns[pattern_key].append({
            'input_grid': input_grid,
            'output': output_item,
            'output_count': output_count,
            'pattern': pattern
        })

        # Update templates if this is a common pattern
        self._update_templates(pattern_key, pattern)

        logger.debug(f"Learned from recipe: {output_item}")

    def _extract_pattern(self, grid: List[List[int]]) -> Dict[str, Any]:
        """
        Extract abstract pattern from crafting grid

        Args:
            grid: 3x3 crafting grid

        Returns:
            Pattern dictionary
        """
        # Find bounding box of non-empty cells
        min_row, max_row = 3, 0
        min_col, max_col = 3, 0

        for i in range(3):
            for j in range(3):
                if grid[i][j] != 0:
                    min_row = min(min_row, i)
                    max_row = max(max_row, i)
                    min_col = min(min_col, j)
                    max_col = max(max_col, j)

        # Extract pattern within bounding box
        shape = (max_row - min_row + 1, max_col - min_col + 1)
        pattern = {
            'shape': shape,
            'grid_size': sum(1 for i in range(3) for j in range(3) if grid[i][j] != 0),
            'symmetric': self._check_symmetry(grid, min_row, max_row, min_col, max_col),
            'pattern_type': self._classify_pattern(grid, min_row, max_row, min_col, max_col)
        }

        return pattern

    def _pattern_to_key(self, pattern: Dict) -> str:
        """Convert pattern to string key"""
        return f"{pattern['shape'][0]}x{pattern['shape'][1]}_{pattern['pattern_type']}"

    def _check_symmetry(
        self,
        grid: List[List[int]],
        min_row: int,
        max_row: int,
        min_col: int,
        max_col: int
    ) -> str:
        """
        Check pattern symmetry

        Returns:
            'none', 'horizontal', 'vertical', 'both'
        """
        # Simplified symmetry check
        return 'none'

    def _classify_pattern(
        self,
        grid: List[List[int]],
        min_row: int,
        max_row: int,
        min_col: int,
        max_col: int
    ) -> str:
        """
        Classify pattern type

        Returns:
            Pattern type string
        """
        height = max_row - min_row + 1
        width = max_col - min_col + 1
        cells = height * width

        if cells == 1:
            return 'single'
        elif cells == 4 and height == 2 and width == 2:
            return 'square_2x2'
        elif height == 1:
            return 'line_horizontal'
        elif width == 1:
            return 'line_vertical'
        elif cells <= 4:
            return 'shape_l'
        else:
            return 'complex'

    def _update_templates(self, pattern_key: str, pattern: Dict):
        """
        Update recipe templates based on pattern frequency

        Args:
            pattern_key: Pattern key
            pattern: Pattern data
        """
        examples = self.patterns[pattern_key]

        # If we've seen this pattern multiple times with different items,
        # it might be a template
        if len(examples) >= 3:
            # Check if outputs are similar
            outputs = [ex['output'] for ex in examples]

            # This would need more sophisticated analysis
            # For now, just note that it's a potential template
            pass

    def infer_similar_recipes(
        self,
        known_recipe: Dict[str, Any],
        available_items: List[int]
    ) -> List[Dict[str, Any]]:
        """
        Infer similar recipes based on a known successful recipe

        Args:
            known_recipe: Known recipe to generalize from
            available_items: Items available for substitution

        Returns:
            List of inferred recipes with confidence scores
        """
        inferences = []

        input_grid = known_recipe['input_grid']

        # Get unique items used in the recipe
        used_items = set()
        for row in input_grid:
            for item_id in row:
                if item_id != 0:
                    used_items.add(item_id)

        # For each item, try to find similar items
        for item_id in used_items:
            similar_items = self._find_similar_items(item_id, available_items)

            for similar_item in similar_items:
                # Create new recipe by substituting item
                new_grid = [[0] * 3 for _ in range(3)]

                for i in range(3):
                    for j in range(3):
                        if input_grid[i][j] == item_id:
                            new_grid[i][j] = similar_item
                        else:
                            new_grid[i][j] = input_grid[i][j]

                # Calculate confidence based on similarity
                confidence = self._calculate_inference_confidence(
                    item_id,
                    similar_item,
                    known_recipe
                )

                if confidence > 0.5:
                    inferences.append({
                        'input_grid': new_grid,
                        'expected_output': self._infer_output(known_recipe, item_id, similar_item),
                        'confidence': confidence,
                        'based_on': known_recipe['output'],
                        'substitution': {item_id: similar_item}
                    })

        # Sort by confidence
        inferences.sort(key=lambda x: x['confidence'], reverse=True)

        return inferences[:10]  # Return top 10

    def _find_similar_items(
        self,
        item_id: int,
        available_items: List[int]
    ) -> List[int]:
        """
        Find items similar to given item

        Args:
            item_id: Item to find similar for
            available_items: Available items to search

        Returns:
            List of similar item IDs
        """
        # Simplified similarity based on item ID ranges
        # In production, would use item properties or embeddings

        similar = []

        # Same "type" of item (close IDs)
        for other_id in available_items:
            if other_id != item_id:
                if abs(other_id - item_id) < 10:
                    similar.append(other_id)

        return similar

    def _calculate_inference_confidence(
        self,
        original_item: int,
        new_item: int,
        base_recipe: Dict[str, Any]
    ) -> float:
        """
        Calculate confidence for an inferred recipe

        Args:
            original_item: Original item being substituted
            new_item: New item to substitute
            base_recipe: Base recipe

        Returns:
            Confidence score (0-1)
        """
        # Base confidence
        confidence = 0.5

        # Increase confidence if items are very similar
        if abs(new_item - original_item) < 5:
            confidence += 0.2

        # Increase confidence if base recipe is high confidence
        if base_recipe.get('confidence', 0) > 0.9:
            confidence += 0.1

        # Increase confidence if base recipe has been successful many times
        if base_recipe.get('success_count', 0) > 10:
            confidence += 0.1

        return min(confidence, 1.0)

    def _infer_output(
        self,
        base_recipe: Dict[str, Any],
        original_item: int,
        new_item: int
    ) -> Optional[str]:
        """
        Infer what the output would be for a substituted recipe

        Args:
            base_recipe: Base recipe
            original_item: Original item
            new_item: New substituted item

        Returns:
            Inferred output item name
        """
        # Simple inference: output follows the input item type
        # E.g., if "oak_planks" comes from "oak_logs",
        # then "birch_planks" might come from "birch_logs"

        base_output = base_recipe['output']

        # This is very simplified - in production would use NLP or item ID patterns
        return f"inferred_{base_output}"

    def suggest_next_experiments(
        self,
        current_inventory: List[Dict],
        known_recipes: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Suggest experiments based on recipe learning

        Args:
            current_inventory: Current inventory state
            known_recipes: Known recipes

        Returns:
            List of suggested experiments
        """
        suggestions = []

        # For each known recipe, try to infer similar recipes
        for recipe in known_recipes:
            if recipe.get('confidence', 0) > 0.8:  # Only use high-confidence recipes
                available_items = self._get_available_items(current_inventory)

                inferences = self.infer_similar_recipes(recipe, available_items)

                for inference in inferences:
                    if inference['confidence'] > 0.6:
                        suggestions.append(inference)

        # Sort by confidence
        suggestions.sort(key=lambda x: x['confidence'], reverse=True)

        return suggestions[:20]  # Return top 20 suggestions

    def _get_available_items(self, inventory: List[Dict]) -> List[int]:
        """Get available item IDs from inventory"""
        available = []

        for slot in inventory:
            if slot and slot.get('count', 0) > 0:
                item_id = slot.get('item_id', 0)
                if item_id > 0 and item_id not in available:
                    available.append(item_id)

        return available

    def validate_inference(
        self,
        inference: Dict[str, Any],
        actual_result: Dict[str, Any]
    ):
        """
        Validate an inferred recipe against actual result

        Args:
            inference: Inferred recipe
            actual_result: Actual crafting result
        """
        if actual_result.get('success'):
            self.inference_success += 1

            # Boost confidence for this type of inference
            # This would update the model in production
        else:
            self.inference_failure += 1

    def get_statistics(self) -> Dict[str, Any]:
        """Get learner statistics"""
        return {
            'patterns_learned': len(self.patterns),
            'inference_success': self.inference_success,
            'inference_failure': self.inference_failure,
            'inference_accuracy': (
                self.inference_success / (self.inference_success + self.inference_failure)
                if (self.inference_success + self.inference_failure) > 0
                else 0
            ),
            'templates': len(self.templates),
        }

    def export_patterns(self) -> Dict[str, Any]:
        """
        Export learned patterns

        Returns:
            Dictionary of learned patterns
        """
        return {
            'patterns': dict(self.patterns),
            'templates': self.templates,
            'statistics': self.get_statistics()
        }

    def __repr__(self) -> str:
        stats = self.get_statistics()
        return f"RecipeLearner(patterns={stats['patterns_learned']}, accuracy={stats['inference_accuracy']:.2%})"
