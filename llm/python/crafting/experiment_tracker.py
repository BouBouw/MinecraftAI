"""
Experiment Tracker - Tracks and analyzes crafting experiments.
Records outcomes and identifies patterns.
"""

import numpy as np
from typing import Dict, Any, List, Tuple
from collections import defaultdict
from datetime import datetime

from utils.logger import get_logger

logger = get_logger(__name__)


class ExperimentTracker:
    """
    Tracks crafting experiments and analyzes outcomes

    Features:
    - Records all craft attempts (success and failure)
    - Identifies promising patterns
    - Tracks materials efficiency
    - Suggests optimal experiments
    """

    def __init__(self):
        """Initialize experiment tracker"""
        # Experiment history
        self.experiments: List[Dict[str, Any]] = []

        # Success/failure tracking by pattern
        self.pattern_stats: Dict[str, Dict[str, int]] = defaultdict(
            lambda: {'success': 0, 'failure': 0, 'total': 0}
        )

        # Material tracking
        self.material_usage: Dict[int, int] = defaultdict(int)

        # Best recipes discovered
        self.best_recipes: List[Dict[str, Any]] = []

        logger.info("Experiment Tracker initialized")

    def record_experiment(
        self,
        input_grid: List[List[int]],
        result: Dict[str, Any],
        episode_id: int = None
    ):
        """
        Record a crafting experiment

        Args:
            input_grid: Input crafting grid
            result: Crafting result
            episode_id: Associated episode
        """
        # Extract pattern
        pattern = self._extract_simple_pattern(input_grid)

        # Record experiment
        experiment = {
            'timestamp': datetime.now().isoformat(),
            'episode_id': episode_id,
            'input_grid': input_grid,
            'pattern': pattern,
            'success': result.get('success', False),
            'output': result.get('output'),
            'output_count': result.get('count', 1),
            'error': result.get('error')
        }

        self.experiments.append(experiment)

        # Update pattern stats
        self.pattern_stats[pattern]['total'] += 1
        if result.get('success'):
            self.pattern_stats[pattern]['success'] += 1
        else:
            self.pattern_stats[pattern]['failure'] += 1

        # Track material usage
        for row in input_grid:
            for item_id in row:
                if item_id > 0:
                    self.material_usage[item_id] += 1

        # Update best recipes if successful
        if result.get('success'):
            self._update_best_recipes(experiment)

        logger.debug(f"Recorded experiment: {pattern} - {'SUCCESS' if result.get('success') else 'FAILURE'}")

    def _extract_simple_pattern(self, grid: List[List[int]]) -> str:
        """
        Extract simple pattern key from grid

        Args:
            grid: Crafting grid

        Returns:
            Pattern key string
        """
        # Count non-empty cells
        cells = sum(1 for row in grid for item in row if item != 0)

        # Get dimensions
        min_row, max_row = 3, 0
        min_col, max_col = 3, 0

        for i in range(3):
            for j in range(3):
                if grid[i][j] != 0:
                    min_row = min(min_row, i)
                    max_row = max(max_row, i)
                    min_col = min(min_col, j)
                    max_col = max(max_col, j)

        width = max_col - min_col + 1
        height = max_row - min_row + 1

        return f"{cells}_{width}x{height}"

    def _update_best_recipes(self, experiment: Dict[str, Any]):
        """
        Update best recipes list

        Args:
            experiment: Successful experiment
        """
        # Keep track of most efficient recipes (most output per input)
        output_ratio = experiment['output_count'] / sum(
            1 for row in experiment['input_grid'] for item in row if item != 0
        )

        self.best_recipes.append({
            'experiment': experiment,
            'efficiency': output_ratio,
            'timestamp': experiment['timestamp']
        })

        # Keep only top 10
        self.best_recipes.sort(key=lambda x: x['efficiency'], reverse=True)
        self.best_recipes = self.best_recipes[:10]

    def get_pattern_statistics(self) -> Dict[str, Dict[str, Any]]:
        """
        Get statistics for each pattern type

        Returns:
            Dictionary with pattern stats
        """
        stats = {}

        for pattern, counts in self.pattern_stats.items():
            success_rate = (
                counts['success'] / counts['total']
                if counts['total'] > 0
                else 0
            )

            stats[pattern] = {
                'total': counts['total'],
                'success': counts['success'],
                'failure': counts['failure'],
                'success_rate': success_rate
            }

        return stats

    def get_promising_patterns(self, min_confidence: float = 0.3) -> List[str]:
        """
        Get patterns that show promise (have had some success)

        Args:
            min_confidence: Minimum success rate

        Returns:
            List of promising pattern keys
        """
        promising = []

        for pattern, counts in self.pattern_stats.items():
            if counts['total'] >= 3:  # Need at least 3 attempts
                success_rate = counts['success'] / counts['total']
                if success_rate >= min_confidence:
                    promising.append(pattern)

        return sorted(promising, key=lambda p: self.pattern_stats[p]['success'] / self.pattern_stats[p]['total'])

    def get_underexplored_patterns(self, min_attempts: int = 5) -> List[str]:
        """
        Get patterns that haven't been tried much

        Args:
            min_attempts: Minimum attempts to be considered "explored"

        Returns:
            List of underexplored pattern keys
        """
        underexplored = []

        for pattern, counts in self.pattern_stats.items():
            if counts['total'] < min_attempts:
                underexplored.append(pattern)

        return sorted(underexplored, key=lambda p: self.pattern_stats[p]['total'])

    def suggest_experiments(
        self,
        available_items: List[int],
        num_suggestions: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Suggest new experiments based on tracking data

        Args:
            available_items: Available items
            num_suggestions: Number of suggestions

        Returns:
            List of suggested experiments
        """
        suggestions = []

        # Strategy 1: Focus on promising patterns
        promising_patterns = self.get_promising_patterns(min_confidence=0.3)

        for pattern in promising_patterns[:5]:
            # Suggest trying this pattern with new materials
            suggestions.append({
                'strategy': 'promising_pattern',
                'pattern': pattern,
                'confidence': self.pattern_stats[pattern]['success'] / self.pattern_stats[pattern]['total']
            })

        # Strategy 2: Explore underexplored patterns
        underexplored = self.get_underexplored_patterns()

        for pattern in underexplored[:5]:
            suggestions.append({
                'strategy': 'exploration',
                'pattern': pattern,
                'confidence': 0.5  # Neutral confidence for exploration
            })

        # Sort by confidence
        suggestions.sort(key=lambda x: x.get('confidence', 0), reverse=True)

        return suggestions[:num_suggestions]

    def get_material_efficiency(self) -> Dict[int, Dict[str, Any]]:
        """
        Get material usage efficiency

        Returns:
            Dictionary with material stats
        """
        material_stats = {}

        for item_id, usage_count in self.material_usage.items():
            # Find successful uses of this material
            successful_uses = 0

            for exp in self.experiments:
                if exp['success']:
                    for row in exp['input_grid']:
                        if item_id in row:
                            successful_uses += 1

            efficiency = (
                successful_uses / usage_count
                if usage_count > 0
                else 0
            )

            material_stats[item_id] = {
                'total_uses': usage_count,
                'successful_uses': successful_uses,
                'efficiency': efficiency
            }

        return material_stats

    def get_recent_successes(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get recent successful experiments

        Args:
            limit: Number of results

        Returns:
            List of successful experiments
        """
        successes = [exp for exp in self.experiments if exp['success']]

        # Sort by timestamp (most recent first)
        successes.sort(key=lambda x: x['timestamp'], reverse=True)

        return successes[:limit]

    def get_learning_curve(self) -> Dict[str, List]:
        """
        Get learning curve data over time

        Returns:
            Dictionary with timestamps and success rates
        """
        # Group experiments by time windows
        window_size = 100  # experiments per window
        windows = []

        for i in range(0, len(self.experiments), window_size):
            window = self.experiments[i:i + window_size]

            if window:
                success_count = sum(1 for exp in window if exp['success'])
                success_rate = success_count / len(window)

                windows.append({
                    'window': i // window_size,
                    'success_rate': success_rate,
                    'total': len(window)
                })

        return {
            'windows': windows,
            'improvement': (
                windows[-1]['success_rate'] - windows[0]['success_rate']
                if len(windows) > 1
                else 0
            )
        }

    def get_statistics(self) -> Dict[str, Any]:
        """Get tracker statistics"""
        total = len(self.experiments)
        successful = sum(1 for exp in self.experiments if exp['success'])

        return {
            'total_experiments': total,
            'successful': successful,
            'failed': total - successful,
            'success_rate': successful / total if total > 0 else 0,
            'unique_patterns': len(self.pattern_stats),
            'materials_used': len(self.material_usage),
            'best_recipes': len(self.best_recipes),
        }

    def export_data(self) -> Dict[str, Any]:
        """
        Export all tracking data

        Returns:
            Dictionary with all data
        """
        return {
            'experiments': self.experiments,
            'pattern_stats': dict(self.pattern_stats),
            'material_usage': dict(self.material_usage),
            'best_recipes': self.best_recipes,
            'statistics': self.get_statistics()
        }

    def reset(self):
        """Reset all tracking data"""
        self.experiments.clear()
        self.pattern_stats.clear()
        self.material_usage.clear()
        self.best_recipes.clear()

        logger.info("Experiment tracker reset")

    def __repr__(self) -> str:
        stats = self.get_statistics()
        return f"ExperimentTracker(total={stats['total_experiments']}, rate={stats['success_rate']:.2%})"
