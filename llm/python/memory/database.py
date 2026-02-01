"""
Database manager for Minecraft RL memory system.
Handles SQLite database operations for all memory types.
"""

import sqlite3
import json
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime
import threading

from utils.config import get_config
from utils.logger import get_logger

logger = get_logger(__name__)


class DatabaseManager:
    """
    SQLite database manager for persistent memory storage

    Manages four types of memory:
    - Long-term memory (facts, strategies, locations)
    - Episodic memory (events, episodes)
    - Semantic memory (concepts, rules)
    - Indexed memories (embeddings for similarity search)
    """

    def __init__(self, db_path: str = None):
        """
        Initialize database manager

        Args:
            db_path: Path to SQLite database file. If None, uses config
        """
        if db_path is None:
            config = get_config()
            db_path = config.get('memory.long_term.database_path', './data/memories/minecraft_rl.db')

        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)

        self.connection = None
        self.lock = threading.Lock()

        self._initialize_database()

    def _initialize_database(self):
        """Initialize database schema"""
        with self.lock:
            self.connection = sqlite3.connect(
                self.db_path,
                check_same_thread=False,
                isolation_level=None  # Autocommit mode
            )
            self.connection.row_factory = sqlite3.Row  # Return rows as dictionaries

            self._create_tables()
            self._create_indexes()

        logger.info(f"Database initialized at {self.db_path}")

    def _create_tables(self):
        """Create all database tables"""
        cursor = self.connection.cursor()

        # Long-term memory table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS long_term_memory (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                episode_id INTEGER,
                memory_type TEXT NOT NULL,
                key TEXT NOT NULL,
                value TEXT,
                importance REAL DEFAULT 1.0,
                access_count INTEGER DEFAULT 0,
                last_accessed DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Indexed memories (for vector similarity search)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS indexed_memories (
                memory_id INTEGER PRIMARY KEY,
                embedding BLOB,
                FOREIGN KEY (memory_id) REFERENCES long_term_memory(id) ON DELETE CASCADE
            )
        """)

        # Episodic memory - episodes
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS episodes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                start_time DATETIME DEFAULT CURRENT_TIMESTAMP,
                end_time DATETIME,
                total_reward REAL DEFAULT 0.0,
                length INTEGER DEFAULT 0,
                max_health INTEGER DEFAULT 20,
                death_cause TEXT,
                final_inventory TEXT,
                curriculum_stage INTEGER DEFAULT 0
            )
        """)

        # Episodic memory - events
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS episode_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                episode_id INTEGER NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                event_type TEXT NOT NULL,
                description TEXT,
                importance REAL DEFAULT 1.0,
                data TEXT,
                FOREIGN KEY (episode_id) REFERENCES episodes(id) ON DELETE CASCADE
            )
        """)

        # Semantic memory - concepts
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS semantic_concepts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                concept_type TEXT NOT NULL,
                name TEXT NOT NULL UNIQUE,
                properties TEXT,
                relationships TEXT,
                last_updated DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Semantic memory - rules
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS semantic_rules (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                rule TEXT NOT NULL,
                confidence REAL DEFAULT 1.0,
                source TEXT,
                examples TEXT,
                last_validated DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Craft discovery - recipes
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS discovered_recipes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                input_grid TEXT NOT NULL,
                output_item TEXT NOT NULL,
                output_count INTEGER DEFAULT 1,
                discovered_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                discovery_method TEXT,
                confidence REAL DEFAULT 1.0,
                success_count INTEGER DEFAULT 0,
                failure_count INTEGER DEFAULT 0
            )
        """)

        self.connection.commit()

    def _create_indexes(self):
        """Create indexes for efficient queries"""
        cursor = self.connection.cursor()

        # Long-term memory indexes
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_ltm_type
            ON long_term_memory(memory_type)
        """)

        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_ltm_importance
            ON long_term_memory(importance DESC)
        """)

        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_ltm_episode
            ON long_term_memory(episode_id)
        """)

        # Episode events indexes
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_events_episode
            ON episode_events(episode_id)
        """)

        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_events_type
            ON episode_events(event_type)
        """)

        # Semantic concepts indexes
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_concepts_type
            ON semantic_concepts(concept_type)
        """)

        # Discovered recipes indexes
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_recipes_output
            ON discovered_recipes(output_item)
        """)

        self.connection.commit()

    # ==================== Long-term Memory Operations ====================

    def store_long_term_memory(
        self,
        memory_type: str,
        key: str,
        value: Any,
        episode_id: int = None,
        importance: float = 1.0
    ) -> int:
        """
        Store a long-term memory

        Args:
            memory_type: Type of memory (craft, location, strategy, death, etc.)
            key: Memory key
            value: Memory value (will be JSON serialized)
            episode_id: Associated episode ID
            importance: Importance score (0-1)

        Returns:
            Memory ID
        """
        cursor = self.connection.cursor()

        value_json = json.dumps(value) if not isinstance(value, str) else value

        cursor.execute("""
            INSERT INTO long_term_memory
            (episode_id, memory_type, key, value, importance)
            VALUES (?, ?, ?, ?, ?)
        """, (episode_id, memory_type, key, value_json, importance))

        self.connection.commit()
        memory_id = cursor.lastrowid

        logger.debug(f"Stored LTM: {memory_type}/{key} (id={memory_id})")
        return memory_id

    def retrieve_long_term_memory(
        self,
        memory_type: str = None,
        key: str = None,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Retrieve long-term memories

        Args:
            memory_type: Filter by memory type (optional)
            key: Filter by key (optional)
            limit: Maximum number of memories to return

        Returns:
            List of memories
        """
        cursor = self.connection.cursor()

        query = "SELECT * FROM long_term_memory WHERE 1=1"
        params = []

        if memory_type:
            query += " AND memory_type = ?"
            params.append(memory_type)

        if key:
            query += " AND key LIKE ?"
            params.append(f"%{key}%")

        query += " ORDER BY importance DESC, timestamp DESC LIMIT ?"
        params.append(limit)

        cursor.execute(query, params)
        rows = cursor.fetchall()

        # Update access count
        for row in rows:
            self._update_access_count(row['id'])

        return [dict(row) for row in rows]

    def _update_access_count(self, memory_id: int):
        """Update memory access count and timestamp"""
        cursor = self.connection.cursor()
        cursor.execute("""
            UPDATE long_term_memory
            SET access_count = access_count + 1,
                last_accessed = CURRENT_TIMESTAMP
            WHERE id = ?
        """, (memory_id,))
        self.connection.commit()

    # ==================== Episodic Memory Operations ====================

    def create_episode(
        self,
        curriculum_stage: int = 0
    ) -> int:
        """
        Create a new episode

        Args:
            curriculum_stage: Curriculum stage index

        Returns:
            Episode ID
        """
        cursor = self.connection.cursor()

        cursor.execute("""
            INSERT INTO episodes (curriculum_stage)
            VALUES (?)
        """, (curriculum_stage,))

        self.connection.commit()
        episode_id = cursor.lastrowid

        logger.debug(f"Created episode {episode_id}")
        return episode_id

    def update_episode(
        self,
        episode_id: int,
        total_reward: float = None,
        death_cause: str = None,
        final_inventory: Dict = None
    ):
        """
        Update episode information

        Args:
            episode_id: Episode ID
            total_reward: Total reward for episode
            death_cause: Cause of death
            final_inventory: Final inventory state
        """
        cursor = self.connection.cursor()

        updates = ["end_time = CURRENT_TIMESTAMP"]
        params = []

        if total_reward is not None:
            updates.append("total_reward = ?")
            params.append(total_reward)

        if death_cause is not None:
            updates.append("death_cause = ?")
            params.append(death_cause)

        if final_inventory is not None:
            updates.append("final_inventory = ?")
            params.append(json.dumps(final_inventory))

        params.append(episode_id)

        query = f"UPDATE episodes SET {', '.join(updates)} WHERE id = ?"
        cursor.execute(query, params)
        self.connection.commit()

    def record_event(
        self,
        episode_id: int,
        event_type: str,
        description: str,
        importance: float = 1.0,
        data: Dict = None
    ) -> int:
        """
        Record an episode event

        Args:
            episode_id: Episode ID
            event_type: Event type (death, craft, discovery, milestone)
            description: Event description
            importance: Event importance
            data: Additional event data

        Returns:
            Event ID
        """
        cursor = self.connection.cursor()

        data_json = json.dumps(data) if data else None

        cursor.execute("""
            INSERT INTO episode_events
            (episode_id, event_type, description, importance, data)
            VALUES (?, ?, ?, ?, ?)
        """, (episode_id, event_type, description, importance, data_json))

        self.connection.commit()
        event_id = cursor.lastrowid

        logger.debug(f"Recorded event: {event_type} for episode {episode_id}")
        return event_id

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
        cursor = self.connection.cursor()

        query = "SELECT * FROM episode_events WHERE episode_id = ?"
        params = [episode_id]

        if event_type:
            query += " AND event_type = ?"
            params.append(event_type)

        query += " ORDER BY timestamp ASC"

        cursor.execute(query, params)
        rows = cursor.fetchall()

        return [dict(row) for row in rows]

    # ==================== Semantic Memory Operations ====================

    def store_concept(
        self,
        concept_type: str,
        name: str,
        properties: Dict = None,
        relationships: Dict = None
    ) -> int:
        """
        Store a semantic concept

        Args:
            concept_type: Concept type (block, item, entity, biome, mechanic)
            name: Concept name
            properties: Concept properties
            relationships: Related concepts

        Returns:
            Concept ID
        """
        cursor = self.connection.cursor()

        cursor.execute("""
            INSERT OR REPLACE INTO semantic_concepts
            (concept_type, name, properties, relationships, last_updated)
            VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)
        """, (
            concept_type,
            name,
            json.dumps(properties) if properties else None,
            json.dumps(relationships) if relationships else None
        ))

        self.connection.commit()
        concept_id = cursor.lastrowid

        logger.debug(f"Stored concept: {concept_type}/{name}")
        return concept_id

    def get_concept(self, name: str) -> Optional[Dict[str, Any]]:
        """
        Get a semantic concept by name

        Args:
            name: Concept name

        Returns:
            Concept data or None
        """
        cursor = self.connection.cursor()

        cursor.execute("""
            SELECT * FROM semantic_concepts WHERE name = ?
        """, (name,))

        row = cursor.fetchone()

        if row:
            return dict(row)
        return None

    # ==================== Craft Discovery Operations ====================

    def store_discovered_recipe(
        self,
        input_grid: List[List],
        output_item: str,
        output_count: int = 1,
        discovery_method: str = "experiment"
    ) -> int:
        """
        Store a discovered recipe

        Args:
            input_grid: 3x3 crafting grid
            output_item: Output item name
            output_count: Number of items produced
            discovery_method: How recipe was discovered

        Returns:
            Recipe ID
        """
        cursor = self.connection.cursor()

        cursor.execute("""
            INSERT INTO discovered_recipes
            (input_grid, output_item, output_count, discovery_method)
            VALUES (?, ?, ?, ?)
        """, (
            json.dumps(input_grid),
            output_item,
            output_count,
            discovery_method
        ))

        self.connection.commit()
        recipe_id = cursor.lastrowid

        logger.info(f"Discovered recipe: {output_item} (method={discovery_method})")
        return recipe_id

    def get_discovered_recipes(
        self,
        output_item: str = None
    ) -> List[Dict[str, Any]]:
        """
        Get discovered recipes

        Args:
            output_item: Filter by output item (optional)

        Returns:
            List of recipes
        """
        cursor = self.connection.cursor()

        if output_item:
            cursor.execute("""
                SELECT * FROM discovered_recipes
                WHERE output_item = ?
                ORDER BY confidence DESC, success_count DESC
            """, (output_item,))
        else:
            cursor.execute("""
                SELECT * FROM discovered_recipes
                ORDER BY discovered_at DESC
            """)

        rows = cursor.fetchall()

        return [dict(row) for row in rows]

    # ==================== Utility Methods ====================

    def get_statistics(self) -> Dict[str, Any]:
        """
        Get database statistics

        Returns:
            Dictionary with statistics
        """
        cursor = self.connection.cursor()

        stats = {}

        # Long-term memory count
        cursor.execute("SELECT COUNT(*) as count FROM long_term_memory")
        stats['long_term_memories'] = cursor.fetchone()['count']

        # Episode count
        cursor.execute("SELECT COUNT(*) as count FROM episodes")
        stats['total_episodes'] = cursor.fetchone()['count']

        # Event count
        cursor.execute("SELECT COUNT(*) as count FROM episode_events")
        stats['total_events'] = cursor.fetchone()['count']

        # Concept count
        cursor.execute("SELECT COUNT(*) as count FROM semantic_concepts")
        stats['total_concepts'] = cursor.fetchone()['count']

        # Recipe count
        cursor.execute("SELECT COUNT(*) as count FROM discovered_recipes")
        stats['discovered_recipes'] = cursor.fetchone()['count']

        # Database size
        stats['db_size_bytes'] = self.db_path.stat().st_size

        return stats

    def close(self):
        """Close database connection"""
        if self.connection:
            self.connection.close()
            logger.info("Database connection closed")


# Singleton instance
_db_manager = None


def get_database_manager() -> DatabaseManager:
    """Get global database manager instance"""
    global _db_manager
    if _db_manager is None:
        _db_manager = DatabaseManager()
    return _db_manager
