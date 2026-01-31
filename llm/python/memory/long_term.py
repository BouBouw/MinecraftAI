"""
Long-term memory for Minecraft RL agent.
Persistent storage of important knowledge in SQLite database.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta

from .database import DatabaseManager, get_database_manager
from ..utils.config import get_config
from ..utils.logger import get_logger

logger = get_logger(__name__)


class LongTermMemory:
    """
    Long-term memory (LTM) - persistent knowledge storage

    Stores important information across episodes:
    - Successful strategies
    - Important locations
    - Crafting recipes discovered
    - Death causes and lessons
    - Building techniques
    - Resource locations
    """

    def __init__(self, db_manager: DatabaseManager = None):
        """
        Initialize long-term memory

        Args:
            db_manager: Database manager instance. If None, uses global instance
        """
        self.db = db_manager or get_database_manager()
        config = get_config()

        # Maximum memories to retrieve
        self.max_memories = config.get('memory.long_term.max_memories', 1000000)
        self.retrieval_top_k = config.get('memory.long_term.retrieval_top_k', 10)

        logger.info("Long-term memory initialized")

    # ==================== Memory Storage ====================

    def store_craft(
        self,
        recipe: Dict[str, Any],
        importance: float = 1.0,
        episode_id: int = None
    ) -> int:
        """
        Store a discovered crafting recipe

        Args:
            recipe: Recipe data (input, output, etc.)
            importance: Recipe importance
            episode_id: Episode where recipe was discovered

        Returns:
            Memory ID
        """
        key = f"craft_{recipe.get('output_item', 'unknown')}"

        return self.db.store_long_term_memory(
            memory_type='craft',
            key=key,
            value=recipe,
            episode_id=episode_id,
            importance=importance
        )

    def store_location(
        self,
        location_name: str,
        position: Dict[str, float],
        location_type: str,
        importance: float = 0.8,
        episode_id: int = None
    ) -> int:
        """
        Store an important location

        Args:
            location_name: Name of location
            position: {x, y, z} coordinates
            location_type: Type (spawn, base, resource, structure)
            importance: Location importance
            episode_id: Episode where discovered

        Returns:
            Memory ID
        """
        key = f"location_{location_type}_{location_name}"

        return self.db.store_long_term_memory(
            memory_type='location',
            key=key,
            value={
                'name': location_name,
                'position': position,
                'type': location_type
            },
            episode_id=episode_id,
            importance=importance
        )

    def store_strategy(
        self,
        strategy_name: str,
        description: str,
        effectiveness: float,
        episode_id: int = None
    ) -> int:
        """
        Store a successful strategy

        Args:
            strategy_name: Strategy name
            description: Strategy description
            effectiveness: Effectiveness score (0-1)
            episode_id: Episode where used

        Returns:
            Memory ID
        """
        key = f"strategy_{strategy_name}"

        return self.db.store_long_term_memory(
            memory_type='strategy',
            key=key,
            value={
                'name': strategy_name,
                'description': description,
                'effectiveness': effectiveness
            },
            episode_id=episode_id,
            importance=effectiveness
        )

    def store_death(
        self,
        death_cause: str,
        context: Dict[str, Any],
        lesson: str = None,
        episode_id: int = None
    ) -> int:
        """
        Store information about a death

        Args:
            death_cause: What caused the death
            context: Context of death (position, health, etc.)
            lesson: Lesson learned
            episode_id: Episode where death occurred

        Returns:
            Memory ID
        """
        key = f"death_{episode_id or 'unknown'}"

        return self.db.store_long_term_memory(
            memory_type='death',
            key=key,
            value={
                'cause': death_cause,
                'context': context,
                'lesson': lesson,
                'timestamp': datetime.now().isoformat()
            },
            episode_id=episode_id,
            importance=0.9  # Deaths are important
        )

    def store_resource(
        self,
        resource_type: str,
        position: Dict[str, float],
        quantity: int,
        episode_id: int = None
    ) -> int:
        """
        Store a resource location

        Args:
            resource_type: Type of resource (iron, coal, diamond)
            position: Resource position
            quantity: Estimated quantity
            episode_id: Episode where discovered

        Returns:
            Memory ID
        """
        key = f"resource_{resource_type}_{position['x']}_{position['z']}"

        return self.db.store_long_term_memory(
            memory_type='resource',
            key=key,
            value={
                'type': resource_type,
                'position': position,
                'quantity': quantity
            },
            episode_id=episode_id,
            importance=0.6
        )

    def store_building_technique(
        self,
        technique_name: str,
        description: str,
        effectiveness: float,
        episode_id: int = None
    ) -> int:
        """
        Store a building technique

        Args:
            technique_name: Technique name
            description: Technique description
            effectiveness: Effectiveness score (0-1)
            episode_id: Episode where used

        Returns:
            Memory ID
        """
        key = f"building_{technique_name}"

        return self.db.store_long_term_memory(
            memory_type='building',
            key=key,
            value={
                'name': technique_name,
                'description': description,
                'effectiveness': effectiveness
            },
            episode_id=episode_id,
            importance=effectiveness
        )

    # ==================== Memory Retrieval ====================

    def retrieve_crafts(self, output_item: str = None) -> List[Dict[str, Any]]:
        """
        Retrieve crafting memories

        Args:
            output_item: Filter by output item (optional)

        Returns:
            List of craft memories
        """
        return self.db.retrieve_long_term_memory(
            memory_type='craft',
            key=output_item,
            limit=self.retrieval_top_k
        )

    def retrieve_locations(
        self,
        location_type: str = None,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Retrieve location memories

        Args:
            location_type: Filter by location type
            limit: Maximum results

        Returns:
            List of location memories
        """
        return self.db.retrieve_long_term_memory(
            memory_type='location',
            key=location_type,
            limit=limit
        )

    def retrieve_strategies(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Retrieve strategy memories

        Args:
            limit: Maximum results

        Returns:
            List of strategy memories
        """
        return self.db.retrieve_long_term_memory(
            memory_type='strategy',
            limit=limit
        )

    def retrieve_deaths(self, limit: int = 20) -> List[Dict[str, Any]]:
        """
        Retrieve death memories (for learning from mistakes)

        Args:
            limit: Maximum results

        Returns:
            List of death memories
        """
        return self.db.retrieve_long_term_memory(
            memory_type='death',
            limit=limit
        )

    def retrieve_resources(
        self,
        resource_type: str = None,
        near_position: Dict[str, float] = None,
        limit: int = 20
    ) -> List[Dict[str, Any]]:
        """
        Retrieve resource memories

        Args:
            resource_type: Filter by resource type
            near_position: Find resources near this position
            limit: Maximum results

        Returns:
            List of resource memories
        """
        memories = self.db.retrieve_long_term_memory(
            memory_type='resource',
            key=resource_type,
            limit=limit * 2  # Get more to filter by distance
        )

        # Filter by distance if position specified
        if near_position:
            memories = self._filter_by_distance(memories, near_position, limit)

        return memories[:limit]

    def retrieve_building_techniques(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Retrieve building technique memories

        Args:
            limit: Maximum results

        Returns:
            List of building technique memories
        """
        return self.db.retrieve_long_term_memory(
            memory_type='building',
            limit=limit
        )

    # ==================== Utility Methods ====================

    def _filter_by_distance(
        self,
        memories: List[Dict[str, Any]],
        position: Dict[str, float],
        limit: int
    ) -> List[Dict[str, Any]]:
        """
        Filter memories by distance from position

        Args:
            memories: List of memories with position data
            position: Reference position {x, y, z}
            limit: Maximum results

        Returns:
            Sorted and filtered memories
        """
        memories_with_dist = []

        for memory in memories:
            try:
                value = memory.get('value', {})
                if isinstance(value, str):
                    import json
                    value = json.loads(value)

                mem_pos = value.get('position', {})

                dist = (
                    (mem_pos.get('x', 0) - position['x']) ** 2 +
                    (mem_pos.get('y', 0) - position['y']) ** 2 +
                    (mem_pos.get('z', 0) - position['z']) ** 2
                ) ** 0.5

                memories_with_dist.append((memory, dist))
            except Exception:
                pass

        # Sort by distance
        memories_with_dist.sort(key=lambda x: x[1])

        # Return top N
        return [m[0] for m in memories_with_dist[:limit]]

    def get_important_memories(self, limit: int = 20) -> List[Dict[str, Any]]:
        """
        Get most important memories across all types

        Args:
            limit: Maximum results

        Returns:
            List of important memories
        """
        return self.db.retrieve_long_term_memory(limit=limit)

    def get_statistics(self) -> Dict[str, Any]:
        """
        Get long-term memory statistics

        Returns:
            Dictionary with statistics
        """
        stats = {
            'total_memories': 0,
            'by_type': {}
        }

        for memory_type in ['craft', 'location', 'strategy', 'death', 'resource', 'building']:
            memories = self.db.retrieve_long_term_memory(memory_type=memory_type, limit=1000000)
            stats['by_type'][memory_type] = len(memories)
            stats['total_memories'] += len(memories)

        return stats

    def __repr__(self) -> str:
        return f"LongTermMemory(total={self.get_statistics()['total_memories']})"
