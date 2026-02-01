"""
Memory Manager - Unified interface for all memory systems.
Coordinates short-term, long-term, episodic, and semantic memory.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime

from .database import DatabaseManager, get_database_manager
from .short_term import ShortTermMemory
from .long_term import LongTermMemory
from .episodic import EpisodicMemory
from .semantic import SemanticMemory
from utils.config import get_config
from utils.logger import get_logger

logger = get_logger(__name__)


class MemoryManager:
    """
    Unified memory manager for Minecraft RL agent

    Coordinates all four memory types:
    - Short-term: Recent experiences (RAM)
    - Long-term: Important knowledge (SQLite)
    - Episodic: Events and episodes (SQLite)
    - Semantic: Concepts and rules (SQLite)
    """

    def __init__(self, db_manager: DatabaseManager = None):
        """
        Initialize memory manager

        Args:
            db_manager: Database manager instance
        """
        self.db = db_manager or get_database_manager()

        # Initialize all memory systems
        self.short_term = ShortTermMemory()
        self.long_term = LongTermMemory(self.db)
        self.episodic = EpisodicMemory(self.db)
        self.semantic = SemanticMemory(self.db)

        logger.info("Memory Manager initialized with all 4 memory systems")

    # ==================== Episode Management ====================

    def start_episode(self, curriculum_stage: int = 0) -> int:
        """
        Start a new episode

        Args:
            curriculum_stage: Current curriculum stage

        Returns:
            Episode ID
        """
        episode_id = self.episodic.start_episode(curriculum_stage)
        self.short_term.mark_episode_start()
        return episode_id

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
            death_cause: Cause of death
            final_inventory: Final inventory state
        """
        self.episodic.end_episode(total_reward, death_cause, final_inventory)

    def get_current_episode_id(self) -> Optional[int]:
        """Get current episode ID"""
        return self.episodic.get_current_episode_id()

    # ==================== Memory Storage ====================

    def remember_transition(
        self,
        state: Dict[str, Any],
        action: Dict[str, Any],
        reward: float,
        done: bool,
        next_state: Dict[str, Any] = None
    ):
        """
        Store a transition in short-term memory

        Args:
            state: Current state
            action: Action taken
            reward: Reward received
            done: Whether episode is done
            next_state: Next state (optional)
        """
        self.short_term.remember(state, action, reward, done)

    def remember_craft(
        self,
        recipe: Dict[str, Any],
        importance: float = 1.0
    ) -> int:
        """
        Store a craft in long-term and episodic memory

        Args:
            recipe: Recipe data
            importance: Craft importance

        Returns:
            Long-term memory ID
        """
        # Store in long-term memory
        ltm_id = self.long_term.store_craft(
            recipe=recipe,
            importance=importance,
            episode_id=self.get_current_episode_id()
        )

        # Record in episodic memory
        self.episodic.record_craft_discovery(recipe, success=True)

        return ltm_id

    def remember_death(
        self,
        cause: str,
        position: Dict[str, float] = None,
        context: Dict = None
    ) -> int:
        """
        Store a death in long-term and episodic memory

        Args:
            cause: Cause of death
            position: Death position
            context: Additional context

        Returns:
            Long-term memory ID
        """
        # Store in long-term memory
        ltm_id = self.long_term.store_death(
            death_cause=cause,
            context={'position': position, **(context or {})},
            episode_id=self.get_current_episode_id()
        )

        # Record in episodic memory
        self.episodic.record_death(cause, position, context)

        return ltm_id

    def remember_location(
        self,
        name: str,
        position: Dict[str, float],
        location_type: str,
        importance: float = 0.8
    ) -> int:
        """
        Store a location in long-term memory

        Args:
            name: Location name
            position: Position coordinates
            location_type: Location type
            importance: Location importance

        Returns:
            Long-term memory ID
        """
        return self.long_term.store_location(
            location_name=name,
            position=position,
            location_type=location_type,
            importance=importance,
            episode_id=self.get_current_episode_id()
        )

    def remember_strategy(
        self,
        name: str,
        description: str,
        effectiveness: float
    ) -> int:
        """
        Store a strategy in long-term memory

        Args:
            name: Strategy name
            description: Strategy description
            effectiveness: Effectiveness score

        Returns:
            Long-term memory ID
        """
        return self.long_term.store_strategy(
            strategy_name=name,
            description=description,
            effectiveness=effectiveness,
            episode_id=self.get_current_episode_id()
        )

    def remember_discovery(
        self,
        discovery_type: str,
        description: str,
        data: Dict = None
    ) -> int:
        """
        Record a discovery in episodic memory

        Args:
            discovery_type: Type of discovery
            description: Discovery description
            data: Additional data

        Returns:
            Event ID
        """
        return self.episodic.record_discovery(discovery_type, description, data)

    def remember_rule(
        self,
        rule: str,
        confidence: float = 1.0,
        source: str = 'discovered',
        examples: List[Dict] = None
    ) -> int:
        """
        Store a rule in semantic memory

        Args:
            rule: Rule description
            confidence: Rule confidence
            source: Rule source
            examples: Supporting examples

        Returns:
            Rule ID
        """
        return self.semantic.store_rule(rule, confidence, source, examples)

    # ==================== Memory Retrieval ====================

    def get_recent_context(self, n: int = 50) -> Dict[str, Any]:
        """
        Get recent context from short-term memory

        Args:
            n: Number of recent transitions

        Returns:
            Dictionary with recent states, actions, rewards
        """
        states, actions, rewards, dones = self.short_term.get_recent_context(n)

        return {
            'states': states,
            'actions': actions,
            'rewards': rewards,
            'dones': dones
        }

    def get_relevant_memories(
        self,
        context: Dict[str, Any] = None,
        limit: int = 10
    ) -> Dict[str, Any]:
        """
        Get relevant memories from all memory systems

        Args:
            context: Current context (position, etc.)
            limit: Maximum memories per type

        Returns:
            Dictionary with relevant memories from each system
        """
        relevant = {
            'short_term': {
                'recent_actions': self.short_term.get_recent_actions()[:limit],
                'recent_rewards': list(self.short_term.rewards)[-limit:],
            },
            'long_term': {
                'crafts': self.long_term.retrieve_crafts()[:limit],
                'strategies': self.long_term.retrieve_strategies()[:limit],
            },
            'episodic': {
                'recent_episodes': self.episodic.get_recent_episodes(limit),
            },
            'semantic': {
                'rules': self.semantic.get_rules(min_confidence=0.7)[:limit],
            }
        }

        # Add context-specific memories
        if context and 'position' in context:
            position = context['position']
            relevant['long_term']['nearby_resources'] = self.long_term.retrieve_resources(
                near_position=position,
                limit=limit
            )

        return relevant

    def get_knowledge_about(self, concept: str) -> Dict[str, Any]:
        """
        Get all knowledge about a concept

        Args:
            concept: Concept name or query

        Returns:
            Dictionary with relevant knowledge
        """
        knowledge = {
            'concept': concept,
            'semantic': None,
            'rules': [],
            'episodes': [],
        }

        # Get semantic concept
        semantic_concept = self.semantic.get_block(concept)
        if not semantic_concept:
            semantic_concept = self.semantic.get_item(concept)
        if not semantic_concept:
            semantic_concept = self.semantic.get_entity(concept)

        knowledge['semantic'] = semantic_concept

        # Get related rules
        knowledge['rules'] = self.semantic.get_rules_about(concept)

        return knowledge

    # ==================== Learning from Experience ====================

    def learn_from_episode(self, episode_data: Dict[str, Any]):
        """
        Consolidate learning from a completed episode

        Args:
            episode_data: Episode data including rewards, events, etc.
        """
        # Analyze episode for learnings
        total_reward = episode_data.get('total_reward', 0)
        death_cause = episode_data.get('death_cause')
        final_inventory = episode_data.get('final_inventory')

        # Learn from successful strategies
        if total_reward > 0:
            success_rate = min(total_reward / 1000, 1.0)  # Normalize to 0-1
            self.remember_strategy(
                name=f"successful_episode_{self.get_current_episode_id()}",
                description=f"Episode with reward {total_reward:.2f}",
                effectiveness=success_rate
            )

        # Learn from death
        if death_cause:
            lesson = self._generate_death_lesson(death_cause, episode_data)
            self.remember_death(
                cause=death_cause,
                context=episode_data.get('death_context'),
            )
            if lesson:
                self.remember_rule(
                    rule=lesson,
                    confidence=0.8,
                    source='experience',
                    examples=[{'episode': self.get_current_episode_id()}]
                )

    def _generate_death_lesson(self, cause: str, episode_data: Dict) -> Optional[str]:
        """Generate a lesson learned from death"""
        lessons = {
            'fall': "Always be careful when moving at heights. Use sneak mode.",
            'zombie': "Avoid zombies at night or have proper weapons and armor.",
            'hunger': "Always keep food available. Don't let saturation drop too low.",
            'lava': "Never dig directly down. Carry a water bucket.",
            'drowning': "Don't stay underwater too long. Use torches for air pockets.",
        }

        return lessons.get(cause)

    # ==================== Statistics and Monitoring ====================

    def get_statistics(self) -> Dict[str, Any]:
        """
        Get comprehensive statistics from all memory systems

        Returns:
            Dictionary with statistics from each system
        """
        return {
            'short_term': self.short_term.get_statistics(),
            'long_term': self.long_term.get_statistics(),
            'episodic': self.episodic.get_statistics(),
            'semantic': self.semantic.get_statistics(),
            'database': self.db.get_statistics(),
        }

    def get_learning_progress(self) -> Dict[str, Any]:
        """
        Get learning progress metrics

        Returns:
            Dictionary with progress metrics
        """
        episodic_progress = self.episodic.get_learning_progress()
        death_summary = self.episodic.get_death_summary()

        return {
            'by_stage': episodic_progress['by_stage'],
            'recent_trend': episodic_progress['recent_trend'],
            'death_summary': death_summary,
            'total_discovered_recipes': len(self.long_term.retrieve_crafts()),
            'total_learned_rules': len(self.semantic.get_rules()),
        }

    # ==================== Maintenance ====================

    def consolidate_memory(self):
        """
        Consolidate short-term memory into long-term memory

        Moves important experiences from STM to LTM
        """
        # Get statistics from short-term memory
        stats = self.short_term.get_statistics()

        # If memory is full, consider consolidation
        if self.short_term.is_full():
            logger.info("Short-term memory full, considering consolidation...")

            # Could implement smart consolidation here
            # For now, just log
            pass

    def cleanup_old_memories(self, max_age_days: int = 30):
        """
        Clean up old episodic memories

        Args:
            max_age_days: Maximum age of episodes to keep
        """
        cursor = self.db.connection.cursor()

        # Delete old episodes
        cursor.execute("""
            DELETE FROM episodes
            WHERE start_time < datetime('now', '-' || ? || ' days')
        """, (max_age_days,))

        deleted_count = cursor.rowcount
        self.db.connection.commit()

        if deleted_count > 0:
            logger.info(f"Cleaned up {deleted_count} old episodes")

    def save_recap(self, filepath: str):
        """
        Save a memory recap to file

        Args:
            filepath: Path to save recap
        """
        stats = self.get_statistics()
        progress = self.get_learning_progress()

        recap = {
            'timestamp': datetime.now().isoformat(),
            'statistics': stats,
            'progress': progress,
            'recent_episodes': self.episodic.get_recent_episodes(5),
            'best_episodes': self.episodic.get_best_episodes(5),
            'important_memories': self.long_term.get_important_memories(10),
        }

        import json
        with open(filepath, 'w') as f:
            json.dump(recap, f, indent=2, default=str)

        logger.info(f"Memory recap saved to {filepath}")

    def close(self):
        """Close database connection"""
        self.db.close()

    def __repr__(self) -> str:
        return f"MemoryManager(stm={len(self.short_term)}, episodes={self.episodic.get_statistics()['total_episodes']})"
