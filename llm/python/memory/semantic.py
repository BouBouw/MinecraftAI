"""
Semantic memory for Minecraft RL agent.
Stores concepts, rules, and knowledge about Minecraft.
"""

from typing import Dict, Any, List, Optional
import json

from .database import DatabaseManager, get_database_manager
from utils.config import get_config
from utils.logger import get_logger

logger = get_logger(__name__)


class SemanticMemory:
    """
    Semantic memory - stores concepts and rules about Minecraft

    Remembers:
    - Block properties and behaviors
    - Item uses and characteristics
    - Entity behaviors and interactions
    - Biome features
    - Game mechanics (physics, crafting, etc.)
    - Rules and patterns discovered
    """

    def __init__(self, db_manager: DatabaseManager = None):
        """
        Initialize semantic memory

        Args:
            db_manager: Database manager instance. If None, uses global instance
        """
        self.db = db_manager or get_database_manager()
        config = get_config()

        # Embedding model for semantic similarity
        self.embedding_model_name = config.get('memory.semantic.embedding_model', 'all-MiniLM-L6-v2')
        self.embedding_model = None  # Lazy loaded

        logger.info("Semantic memory initialized")

    # ==================== Concept Storage ====================

    def store_block(
        self,
        block_name: str,
        properties: Dict[str, Any] = None,
        relationships: Dict[str, Any] = None
    ) -> int:
        """
        Store a block concept

        Args:
            block_name: Block name (e.g., "oak_log")
            properties: Block properties (hardness, drops, etc.)
            relationships: Related blocks/items

        Returns:
            Concept ID
        """
        return self.db.store_concept(
            concept_type='block',
            name=block_name,
            properties=properties,
            relationships=relationships
        )

    def store_item(
        self,
        item_name: str,
        properties: Dict[str, Any] = None,
        relationships: Dict[str, Any] = None
    ) -> int:
        """
        Store an item concept

        Args:
            item_name: Item name
            properties: Item properties (stackable, edible, etc.)
            relationships: Related items/blocks

        Returns:
            Concept ID
        """
        return self.db.store_concept(
            concept_type='item',
            name=item_name,
            properties=properties,
            relationships=relationships
        )

    def store_entity(
        self,
        entity_name: str,
        properties: Dict[str, Any] = None,
        relationships: Dict[str, Any] = None
    ) -> int:
        """
        Store an entity concept

        Args:
            entity_name: Entity name (e.g., "zombie", "villager")
            properties: Entity properties (hostile, health, etc.)
            relationships: Related entities/items

        Returns:
            Concept ID
        """
        return self.db.store_concept(
            concept_type='entity',
            name=entity_name,
            properties=properties,
            relationships=relationships
        )

    def store_biome(
        self,
        biome_name: str,
        properties: Dict[str, Any] = None,
        relationships: Dict[str, Any] = None
    ) -> int:
        """
        Store a biome concept

        Args:
            biome_name: Biome name
            properties: Biome properties (temperature, vegetation, etc.)
            relationships: Related biomes/blocks

        Returns:
            Concept ID
        """
        return self.db.store_concept(
            concept_type='biome',
            name=biome_name,
            properties=properties,
            relationships=relationships
        )

    def store_mechanic(
        self,
        mechanic_name: str,
        properties: Dict[str, Any] = None,
        relationships: Dict[str, Any] = None
    ) -> int:
        """
        Store a game mechanic concept

        Args:
            mechanic_name: Mechanic name (e.g., "gravity", "crafting")
            properties: Mechanic properties
            relationships: Related mechanics/concepts

        Returns:
            Concept ID
        """
        return self.db.store_concept(
            concept_type='mechanic',
            name=mechanic_name,
            properties=properties,
            relationships=relationships
        )

    # ==================== Concept Retrieval ====================

    def get_block(self, block_name: str) -> Optional[Dict[str, Any]]:
        """Get block concept"""
        concept = self.db.get_concept(block_name)
        if concept:
            return self._parse_concept(concept)
        return None

    def get_item(self, item_name: str) -> Optional[Dict[str, Any]]:
        """Get item concept"""
        concept = self.db.get_concept(item_name)
        if concept:
            return self._parse_concept(concept)
        return None

    def get_entity(self, entity_name: str) -> Optional[Dict[str, Any]]:
        """Get entity concept"""
        concept = self.db.get_concept(entity_name)
        if concept:
            return self._parse_concept(concept)
        return None

    def get_biome(self, biome_name: str) -> Optional[Dict[str, Any]]:
        """Get biome concept"""
        concept = self.db.get_concept(biome_name)
        if concept:
            return self._parse_concept(concept)
        return None

    def get_mechanic(self, mechanic_name: str) -> Optional[Dict[str, Any]]:
        """Get mechanic concept"""
        concept = self.db.get_concept(mechanic_name)
        if concept:
            return self._parse_concept(concept)
        return None

    def _parse_concept(self, concept: Dict) -> Dict[str, Any]:
        """Parse concept JSON fields"""
        if concept.get('properties'):
            concept['properties'] = json.loads(concept['properties'])
        if concept.get('relationships'):
            concept['relationships'] = json.loads(concept['relationships'])
        return concept

    # ==================== Rule Storage ====================

    def store_rule(
        self,
        rule: str,
        confidence: float = 1.0,
        source: str = 'discovered',
        examples: List[Dict] = None
    ) -> int:
        """
        Store a learned rule

        Args:
            rule: Rule description (e.g., "wood logs can be crafted into planks")
            confidence: Rule confidence (0-1)
            source: How rule was learned (discovered, experimented, inferred)
            examples: Examples supporting the rule

        Returns:
            Rule ID
        """
        cursor = self.db.connection.cursor()

        cursor.execute("""
            INSERT INTO semantic_rules
            (rule, confidence, source, examples)
            VALUES (?, ?, ?, ?)
        """, (
            rule,
            confidence,
            source,
            json.dumps(examples) if examples else None
        ))

        self.db.connection.commit()
        rule_id = cursor.lastrowid

        logger.info(f"Stored rule: {rule} (confidence={confidence})")
        return rule_id

    def get_rules(
        self,
        min_confidence: float = 0.5,
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        """
        Get learned rules

        Args:
            min_confidence: Minimum confidence threshold
            limit: Maximum results

        Returns:
            List of rules
        """
        cursor = self.db.connection.cursor()

        cursor.execute("""
            SELECT * FROM semantic_rules
            WHERE confidence >= ?
            ORDER BY confidence DESC
            LIMIT ?
        """, (min_confidence, limit))

        rows = cursor.fetchall()

        rules = []
        for row in rows:
            rule = dict(row)
            if rule.get('examples'):
                rule['examples'] = json.loads(rule['examples'])
            rules.append(rule)

        return rules

    def get_rules_about(self, concept_name: str) -> List[Dict[str, Any]]:
        """
        Get rules related to a concept

        Args:
            concept_name: Concept to search for

        Returns:
            List of related rules
        """
        all_rules = self.get_rules()

        related_rules = []
        for rule in all_rules:
            if concept_name.lower() in rule['rule'].lower():
                related_rules.append(rule)

        return related_rules

    # ==================== Knowledge Queries ====================

    def what_can_be_made_from(self, item_name: str) -> List[str]:
        """
        Query: What can be made from this item?

        Args:
            item_name: Input item name

        Returns:
            List of possible outputs
        """
        rules = self.get_rules_about(item_name)

        outputs = []
        for rule in rules:
            # Parse rules like "X can be crafted into Y"
            rule_text = rule['rule'].lower()
            if f"{item_name.lower()} can" in rule_text or f"{item_name.lower()} crafts into" in rule_text:
                outputs.append(rule['rule'])

        return outputs

    def what_is_needed_for(self, output_item: str) -> List[str]:
        """
        Query: What is needed to make this item?

        Args:
            output_item: Output item name

        Returns:
            List of required inputs
        """
        rules = self.get_rules_about(output_item)

        inputs = []
        for rule in rules:
            rule_text = rule['rule'].lower()
            if f"to make {output_item.lower()}" in rule_text or f"{output_item.lower()} requires" in rule_text:
                inputs.append(rule['rule'])

        return inputs

    def get_block_property(self, block_name: str, property_name: str) -> Any:
        """
        Get a specific property of a block

        Args:
            block_name: Block name
            property_name: Property name (hardness, blast_resistance, etc.)

        Returns:
            Property value or None
        """
        block = self.get_block(block_name)

        if block and block.get('properties'):
            return block['properties'].get(property_name)

        return None

    def get_entity_behavior(self, entity_name: str) -> Optional[Dict[str, Any]]:
        """
        Get behavior information for an entity

        Args:
            entity_name: Entity name

        Returns:
            Entity behavior data or None
        """
        entity = self.get_entity(entity_name)

        if entity and entity.get('properties'):
            return entity['properties'].get('behavior')

        return None

    # ==================== Semantic Similarity ====================

    def _load_embedding_model(self):
        """Lazy load the sentence transformer model"""
        if self.embedding_model is None:
            try:
                from sentence_transformers import SentenceTransformer
                self.embedding_model = SentenceTransformer(self.embedding_model_name)
                logger.info(f"Loaded embedding model: {self.embedding_model_name}")
            except ImportError:
                logger.warning("sentence_transformers not available, semantic similarity disabled")
                self.embedding_model = False  # Mark as unavailable

    def find_similar_concepts(
        self,
        query: str,
        concept_type: str = None,
        top_k: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Find concepts similar to query text

        Args:
            query: Query text
            concept_type: Filter by concept type (optional)
            top_k: Number of results to return

        Returns:
            List of similar concepts with scores
        """
        if self.embedding_model is False:
            # Model not available
            return []

        self._load_embedding_model()

        if self.embedding_model is None or self.embedding_model is False:
            return []

        # Get all concepts
        cursor = self.db.connection.cursor()

        if concept_type:
            cursor.execute("""
                SELECT * FROM semantic_concepts
                WHERE concept_type = ?
            """, (concept_type,))
        else:
            cursor.execute("SELECT * FROM semantic_concepts")

        concepts = [dict(row) for row in cursor.fetchall()]

        if not concepts:
            return []

        # Encode query
        query_embedding = self.embedding_model.encode(query)

        # Encode concepts and find similarities
        similarities = []
        for concept in concepts:
            # Encode concept name and description
            concept_text = f"{concept['name']} {concept.get('properties', '')}"
            concept_embedding = self.embedding_model.encode(concept_text)

            # Calculate cosine similarity
            from sklearn.metrics.pairwise import cosine_similarity
            similarity = cosine_similarity(
                [query_embedding],
                [concept_embedding]
            )[0][0]

            similarities.append((concept, similarity))

        # Sort by similarity
        similarities.sort(key=lambda x: x[1], reverse=True)

        # Return top K
        return [
            {
                'concept': self._parse_concept(s[0]),
                'similarity': float(s[1])
            }
            for s in similarities[:top_k]
        ]

    # ==================== Statistics ====================

    def get_statistics(self) -> Dict[str, Any]:
        """
        Get semantic memory statistics

        Returns:
            Dictionary with statistics
        """
        cursor = self.db.connection.cursor()

        stats = {}

        # Count by concept type
        cursor.execute("""
            SELECT concept_type, COUNT(*) as count
            FROM semantic_concepts
            GROUP BY concept_type
        """)

        concept_counts = {}
        for row in cursor.fetchall():
            concept_counts[row['concept_type']] = row['count']

        stats['concepts_by_type'] = concept_counts
        stats['total_concepts'] = sum(concept_counts.values())

        # Rule count
        cursor.execute("SELECT COUNT(*) as count FROM semantic_rules")
        stats['total_rules'] = cursor.fetchone()['count']

        # Average rule confidence
        cursor.execute("SELECT AVG(confidence) as avg_conf FROM semantic_rules")
        stats['avg_rule_confidence'] = cursor.fetchone()['avg_conf'] or 0

        return stats

    def __repr__(self) -> str:
        stats = self.get_statistics()
        return f"SemanticMemory(concepts={stats['total_concepts']}, rules={stats['total_rules']})"
