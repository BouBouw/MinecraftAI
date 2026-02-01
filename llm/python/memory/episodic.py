"""
Episodic memory for Minecraft RL agent.
Stores memories of specific events and episodes.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime

from .database import DatabaseManager, get_database_manager
from utils.config import get_config
from utils.logger import get_logger

logger = get_logger(__name__)


class EpisodicMemory:
    """
    Episodic memory - stores memories of specific events and episodes

    Remembers:
    - Complete episodes (from start to death/timeout)
    - Significant events (first discovery, death, milestone)
    - Episode outcomes and lessons learned
    - Context around important moments
    """

    def __init__(self, db_manager: DatabaseManager = None):
        """
        Initialize episodic memory

        Args:
            db_manager: Database manager instance. If None, uses global instance
        """
        self.db = db_manager or get_database_manager()
        config = get_config()

        self.max_episodes = config.get('memory.episodic.max_episodes', 10000)
        self.episode_length = config.get('memory.episodic.episode_length', 10000)

        # Current episode tracking
        self.current_episode_id = None

        logger.info("Episodic memory initialized")

    # ==================== Episode Management ====================

    def start_episode(self, curriculum_stage: int = 0) -> int:
        """
        Start a new episode

        Args:
            curriculum_stage: Current curriculum stage

        Returns:
            Episode ID
        """
        self.current_episode_id = self.db.create_episode(curriculum_stage)

        logger.info(f"Started episode {self.current_episode_id} (stage={curriculum_stage})")
        return self.current_episode_id

    def end_episode(
        self,
        total_reward: float = 0.0,
        death_cause: str = None,
        final_inventory: Dict = None
    ):
        """
        End the current episode

        Args:
            total_reward: Total reward for the episode
            death_cause: Cause of death (if applicable)
            final_inventory: Final inventory state
        """
        if self.current_episode_id is None:
            logger.warning("No active episode to end")
            return

        self.db.update_episode(
            self.current_episode_id,
            total_reward=total_reward,
            death_cause=death_cause,
            final_inventory=final_inventory
        )

        logger.info(
            f"Ended episode {self.current_episode_id} "
            f"(reward={total_reward:.2f}, cause={death_cause})"
        )

        self.current_episode_id = None

    def get_current_episode_id(self) -> Optional[int]:
        """Get current episode ID"""
        return self.current_episode_id

    # ==================== Event Recording ====================

    def record_death(
        self,
        cause: str,
        position: Dict[str, float] = None,
        context: Dict = None
    ) -> int:
        """
        Record a death event

        Args:
            cause: Cause of death
            position: Death position
            context: Additional context (health, nearby entities, etc.)

        Returns:
            Event ID
        """
        if self.current_episode_id is None:
            logger.warning("No active episode, cannot record death")
            return -1

        description = f"Died from {cause}"

        event_id = self.db.record_event(
            episode_id=self.current_episode_id,
            event_type='death',
            description=description,
            importance=1.0,  # Deaths are very important
            data={
                'cause': cause,
                'position': position,
                'context': context or {}
            }
        )

        logger.warning(f"Episode {self.current_episode_id}: {description}")
        return event_id

    def record_craft_discovery(
        self,
        recipe: Dict[str, Any],
        success: bool = True
    ) -> int:
        """
        Record a craft discovery event

        Args:
            recipe: Recipe data
            success: Whether craft was successful

        Returns:
            Event ID
        """
        if self.current_episode_id is None:
            logger.warning("No active episode, cannot record craft")
            return -1

        output = recipe.get('output_item', 'unknown')
        description = f"Discovered craft: {output}" if success else f"Failed craft: {output}"

        event_id = self.db.record_event(
            episode_id=self.current_episode_id,
            event_type='craft_discovery',
            description=description,
            importance=0.8 if success else 0.3,
            data=recipe
        )

        logger.info(f"Episode {self.current_episode_id}: {description}")
        return event_id

    def record_milestone(
        self,
        milestone_name: str,
        description: str,
        data: Dict = None
    ) -> int:
        """
        Record a milestone event

        Args:
            milestone_name: Name of milestone
            description: Milestone description
            data: Additional data

        Returns:
            Event ID
        """
        if self.current_episode_id is None:
            logger.warning("No active episode, cannot record milestone")
            return -1

        event_id = self.db.record_event(
            episode_id=self.current_episode_id,
            event_type='milestone',
            description=f"Milestone: {milestone_name}",
            importance=0.7,
            data={
                'name': milestone_name,
                'description': description,
                'data': data or {}
            }
        )

        logger.info(f"Episode {self.current_episode_id}: Milestone - {milestone_name}")
        return event_id

    def record_discovery(
        self,
        discovery_type: str,
        description: str,
        data: Dict = None
    ) -> int:
        """
        Record a discovery event

        Args:
            discovery_type: Type of discovery (biome, structure, resource)
            description: Discovery description
            data: Additional data

        Returns:
            Event ID
        """
        if self.current_episode_id is None:
            logger.warning("No active episode, cannot record discovery")
            return -1

        event_id = self.db.record_event(
            episode_id=self.current_episode_id,
            event_type='discovery',
            description=f"Discovered: {discovery_type}",
            importance=0.6,
            data={
                'type': discovery_type,
                'description': description,
                'data': data or {}
            }
        )

        logger.info(f"Episode {self.current_episode_id}: Discovery - {discovery_type}")
        return event_id

    def record_building_event(
        self,
        action: str,
        description: str,
        data: Dict = None
    ) -> int:
        """
        Record a building event

        Args:
            action: Building action (placed_block, completed_structure)
            description: Event description
            data: Additional data

        Returns:
            Event ID
        """
        if self.current_episode_id is None:
            logger.warning("No active episode, cannot record building event")
            return -1

        event_id = self.db.record_event(
            episode_id=self.current_episode_id,
            event_type='building',
            description=f"Building: {action}",
            importance=0.5,
            data={
                'action': action,
                'description': description,
                'data': data or {}
            }
        )

        logger.debug(f"Episode {self.current_episode_id}: Building - {action}")
        return event_id

    # ==================== Episode Retrieval ====================

    def get_episode(self, episode_id: int) -> Optional[Dict[str, Any]]:
        """
        Get complete episode information

        Args:
            episode_id: Episode ID

        Returns:
            Episode data or None
        """
        cursor = self.db.connection.cursor()

        cursor.execute("""
            SELECT * FROM episodes WHERE id = ?
        """, (episode_id,))

        row = cursor.fetchone()

        if row:
            episode = dict(row)
            # Parse JSON fields
            if episode.get('final_inventory'):
                import json
                episode['final_inventory'] = json.loads(episode['final_inventory'])
            return episode

        return None

    def get_recent_episodes(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get recent episodes

        Args:
            limit: Maximum number of episodes

        Returns:
            List of episodes
        """
        cursor = self.db.connection.cursor()

        cursor.execute("""
            SELECT * FROM episodes
            ORDER BY start_time DESC
            LIMIT ?
        """, (limit,))

        rows = cursor.fetchall()

        episodes = []
        for row in rows:
            episode = dict(row)
            # Parse JSON fields
            if episode.get('final_inventory'):
                import json
                episode['final_inventory'] = json.loads(episode['final_inventory'])
            episodes.append(episode)

        return episodes

    def get_best_episodes(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get episodes with highest rewards

        Args:
            limit: Maximum number of episodes

        Returns:
            List of episodes sorted by reward
        """
        cursor = self.db.connection.cursor()

        cursor.execute("""
            SELECT * FROM episodes
            WHERE total_reward IS NOT NULL
            ORDER BY total_reward DESC
            LIMIT ?
        """, (limit,))

        rows = cursor.fetchall()

        episodes = []
        for row in rows:
            episode = dict(row)
            if episode.get('final_inventory'):
                import json
                episode['final_inventory'] = json.loads(episode['final_inventory'])
            episodes.append(episode)

        return episodes

    def get_episode_events(
        self,
        episode_id: int,
        event_type: str = None
    ) -> List[Dict[str, Any]]:
        """
        Get events for an episode

        Args:
            episode_id: Episode ID
            event_type: Filter by event type (optional)

        Returns:
            List of events
        """
        return self.db.get_episode_events(episode_id, event_type)

    # ==================== Analysis Methods ====================

    def get_death_summary(self, limit: int = 20) -> Dict[str, Any]:
        """
        Get summary of death causes

        Args:
            limit: Number of recent episodes to analyze

        Returns:
            Dictionary with death statistics
        """
        cursor = self.db.connection.cursor()

        # Get death events
        cursor.execute("""
            SELECT e.data FROM episode_events e
            JOIN episodes ep ON e.episode_id = ep.id
            WHERE e.event_type = 'death'
            ORDER BY ep.start_time DESC
            LIMIT ?
        """, (limit,))

        rows = cursor.fetchall()

        death_causes = {}
        death_positions = []

        for row in rows:
            import json
            data = json.loads(row['data'])
            cause = data.get('cause', 'unknown')

            death_causes[cause] = death_causes.get(cause, 0) + 1

            position = data.get('position')
            if position:
                death_positions.append(position)

        return {
            'total_deaths': len(rows),
            'causes': death_causes,
            'most_common': max(death_causes.items(), key=lambda x: x[1])[0] if death_causes else None,
            'positions': death_positions
        }

    def get_learning_progress(self) -> Dict[str, Any]:
        """
        Get learning progress over time

        Returns:
            Dictionary with progress metrics
        """
        cursor = self.db.connection.cursor()

        # Get recent episodes
        cursor.execute("""
            SELECT
                curriculum_stage,
                AVG(total_reward) as avg_reward,
                AVG(length) as avg_length,
                COUNT(*) as num_episodes
            FROM episodes
            WHERE total_reward IS NOT NULL
            GROUP BY curriculum_stage
            ORDER BY curriculum_stage
        """)

        rows = cursor.fetchall()

        progress_by_stage = []
        for row in rows:
            progress_by_stage.append({
                'stage': row['curriculum_stage'],
                'avg_reward': row['avg_reward'],
                'avg_length': row['avg_length'],
                'num_episodes': row['num_episodes']
            })

        # Get overall trend
        cursor.execute("""
            SELECT
                SUBSTR(start_time, 1, 10) as date,
                AVG(total_reward) as avg_reward
            FROM episodes
            WHERE total_reward IS NOT NULL
            GROUP BY date
            ORDER BY date DESC
            LIMIT 30
        """)

        trend_rows = cursor.fetchall()

        recent_trend = []
        for row in trend_rows:
            recent_trend.append({
                'date': row['date'],
                'avg_reward': row['avg_reward']
            })

        return {
            'by_stage': progress_by_stage,
            'recent_trend': list(reversed(recent_trend))
        }

    def get_statistics(self) -> Dict[str, Any]:
        """
        Get episodic memory statistics

        Returns:
            Dictionary with statistics
        """
        cursor = self.db.connection.cursor()

        stats = {}

        # Episode counts
        cursor.execute("SELECT COUNT(*) as count FROM episodes")
        stats['total_episodes'] = cursor.fetchone()['count']

        # Event counts by type
        cursor.execute("""
            SELECT event_type, COUNT(*) as count
            FROM episode_events
            GROUP BY event_type
        """)

        event_counts = {}
        for row in cursor.fetchall():
            event_counts[row['event_type']] = row['count']

        stats['events_by_type'] = event_counts
        stats['total_events'] = sum(event_counts.values())

        # Average episode metrics
        cursor.execute("""
            SELECT
                AVG(total_reward) as avg_reward,
                AVG(length) as avg_length,
                MAX(total_reward) as max_reward
            FROM episodes
            WHERE total_reward IS NOT NULL
        """)

        row = cursor.fetchone()
        stats['avg_reward'] = row['avg_reward'] or 0
        stats['avg_length'] = row['avg_length'] or 0
        stats['max_reward'] = row['max_reward'] or 0

        return stats

    def __repr__(self) -> str:
        stats = self.get_statistics()
        return f"EpisodicMemory(episodes={stats['total_episodes']}, events={stats['total_events']})"
