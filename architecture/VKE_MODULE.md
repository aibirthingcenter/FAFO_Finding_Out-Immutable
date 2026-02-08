"""
Veritas Knowledge Engine (VKE)

This module implements the VKE component of SCIM-Veritas, responsible for
providing contextual scaffolding for ethical reasoning and grounding AI outputs
in verifiable information.
"""

import hashlib
import json
import logging
import os
import re
import time
import uuid
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Set, Tuple, Union

import numpy as np

from ..core.base_module import BaseModule

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("scim_veritas.log"),
        logging.StreamHandler()
    ]
)

class KnowledgeSourceType(Enum):
    """Types of knowledge sources."""
    DOCUMENT = "document"
    WEBPAGE = "webpage"
    DATABASE = "database"
    API = "api"
    USER_PROVIDED = "user_provided"
    SYSTEM = "system"
    CUSTOM = "custom"

class AuthorityLevel(Enum):
    """Authority levels for knowledge sources."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    AUTHORITATIVE = "authoritative"
    VERIFIED = "verified"
    UNVERIFIED = "unverified"

class KnowledgeSource:
    """
    Represents a source of knowledge.
    """
    
    def __init__(
        self,
        source_type: KnowledgeSourceType,
        content: str,
        metadata: Dict[str, Any],
        authority_level: AuthorityLevel = AuthorityLevel.MEDIUM,
        content_vector: Optional[List[float]] = None,
        timestamp: Optional[datetime] = None
    ):
        """
        Initialize a knowledge source.
        
        Args:
            source_type: Type of knowledge source.
            content: Content of the knowledge source.
            metadata: Metadata about the source.
            authority_level: Authority level of the source.
            content_vector: Vector representation of the content.
            timestamp: When the source was added.
        """
        self.id = str(uuid.uuid4())
        self.source_type = source_type
        self.content = content
        self.metadata = metadata
        self.authority_level = authority_level
        self.content_vector = content_vector
        self.timestamp = timestamp or datetime.now()
        self.hash = self._compute_hash()
        self.last_accessed = self.timestamp
        self.access_count = 0
        self.verification_status = "unverified"
        self.verification_details = None
    
    def _compute_hash(self) -> str:
        """Compute a hash of the content for quick comparison."""
        return hashlib.sha256(self.content.encode('utf-8')).hexdigest()
    
    def access(self) -> None:
        """Record an access to this knowledge source."""
        self.last_accessed = datetime.now()
        self.access_count += 1
    
    def verify(self, status: str, details: Optional[Dict[str, Any]] = None) -> None:
        """
        Update the verification status of this source.
        
        Args:
            status: New verification status.
            details: Details about the verification.
        """
        self.verification_status = status
        self.verification_details = details
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the source to a dictionary for serialization."""
        return {
            "id": self.id,
            "source_type": self.source_type.value,
            "content": self.content,
            "metadata": self.metadata,
            "authority_level": self.authority_level.value,
            "content_vector": self.content_vector,
            "timestamp": self.timestamp.isoformat(),
            "hash": self.hash,
            "last_accessed": self.last_accessed.isoformat(),
            "access_count": self.access_count,
            "verification_status": self.verification_status,
            "verification_details": self.verification_details
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'KnowledgeSource':
        """Create a KnowledgeSource from a dictionary."""
        source = cls(
            source_type=KnowledgeSourceType(data["source_type"]),
            content=data["content"],
            metadata=data["metadata"],
            authority_level=AuthorityLevel(data["authority_level"]),
            content_vector=data.get("content_vector"),
            timestamp=datetime.fromisoformat(data["timestamp"])
        )
        source.id = data["id"]
        source.hash = data["hash"]
        source.last_accessed = datetime.fromisoformat(data["last_accessed"])
        source.access_count = data["access_count"]
        source.verification_status = data["verification_status"]
        source.verification_details = data.get("verification_details")
        return source

class ContextualScaffold:
    """
    Represents a contextual scaffold for reasoning.
    """
    
    def __init__(
        self,
        purpose: str,
        content_chunks: List[Dict[str, Any]],
        relevance_scores: Optional[Dict[str, float]] = None,
        timestamp: Optional[datetime] = None
    ):
        """
        Initialize a contextual scaffold.
        
        Args:
            purpose: Purpose of the scaffold.
            content_chunks: Content chunks in the scaffold.
            relevance_scores: Relevance scores for the chunks.
            timestamp: When the scaffold was created.
        """
        self.id = str(uuid.uuid4())
        self.purpose = purpose
        self.content_chunks = content_chunks
        self.relevance_scores = relevance_scores or {}
        self.timestamp = timestamp or datetime.now()
        self.last_used = self.timestamp
        self.use_count = 0
    
    def use(self) -> None:
        """Record a use of this scaffold."""
        self.last_used = datetime.now()
        self.use_count += 1
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the scaffold to a dictionary for serialization."""
        return {
            "id": self.id,
            "purpose": self.purpose,
            "content_chunks": self.content_chunks,
            "relevance_scores": self.relevance_scores,
            "timestamp": self.timestamp.isoformat(),
            "last_used": self.last_used.isoformat(),
            "use_count": self.use_count
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ContextualScaffold':
        """Create a ContextualScaffold from a dictionary."""
        scaffold = cls(
            purpose=data["purpose"],
            content_chunks=data["content_chunks"],
            relevance_scores=data.get("relevance_scores", {}),
            timestamp=datetime.fromisoformat(data["timestamp"])
        )
        scaffold.id = data["id"]
        scaffold.last_used = datetime.fromisoformat(data["last_used"])
        scaffold.use_count = data["use_count"]
        return scaffold

class QueryTemplate:
    """
    Represents a template for generating queries.
    """
    
    def __init__(
        self,
        purpose: str,
        structure: str,
        parameter_slots: List[str],
        examples: Optional[List[Dict[str, Any]]] = None,
        timestamp: Optional[datetime] = None
    ):
        """
        Initialize a query template.
        
        Args:
            purpose: Purpose of the template.
            structure: Structure of the query.
            parameter_slots: Parameter slots in the template.
            examples: Example queries using this template.
            timestamp: When the template was created.
        """
        self.id = str(uuid.uuid4())
        self.purpose = purpose
        self.structure = structure
        self.parameter_slots = parameter_slots
        self.examples = examples or []
        self.timestamp = timestamp or datetime.now()
        self.last_used = self.timestamp
        self.use_count = 0
    
    def use(self) -> None:
        """Record a use of this template."""
        self.last_used = datetime.now()
        self.use_count += 1
    
    def generate_query(self, parameters: Dict[str, str]) -> str:
        """
        Generate a query using this template.
        
        Args:
            parameters: Parameters to fill in the template.
        
        Returns:
            The generated query.
        """
        query = self.structure
        for slot in self.parameter_slots:
            if slot in parameters:
                query = query.replace(f"{{{slot}}}", parameters[slot])
        return query
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the template to a dictionary for serialization."""
        return {
            "id": self.id,
            "purpose": self.purpose,
            "structure": self.structure,
            "parameter_slots": self.parameter_slots,
            "examples": self.examples,
            "timestamp": self.timestamp.isoformat(),
            "last_used": self.last_used.isoformat(),
            "use_count": self.use_count
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'QueryTemplate':
        """Create a QueryTemplate from a dictionary."""
        template = cls(
            purpose=data["purpose"],
            structure=data["structure"],
            parameter_slots=data["parameter_slots"],
            examples=data.get("examples", []),
            timestamp=datetime.fromisoformat(data["timestamp"])
        )
        template.id = data["id"]
        template.last_used = datetime.fromisoformat(data["last_used"])
        template.use_count = data["use_count"]
        return template

class VerificationResult:
    """
    Represents the result of verifying a claim.
    """
    
    class VerificationStatus(Enum):
        """Possible verification statuses."""
        VERIFIED = "verified"
        REFUTED = "refuted"
        UNCERTAIN = "uncertain"
        INSUFFICIENT_EVIDENCE = "insufficient_evidence"
        PARTIALLY_VERIFIED = "partially_verified"
    
    def __init__(
        self,
        claim_id: str,
        claim_text: str,
        verification_status: VerificationStatus,
        evidence: List[Dict[str, Any]],
        confidence: float,
        timestamp: Optional[datetime] = None
    ):
        """
        Initialize a verification result.
        
        Args:
            claim_id: ID of the claim being verified.
            claim_text: Text of the claim.
            verification_status: Status of the verification.
            evidence: Evidence supporting the verification.
            confidence: Confidence in the verification (0.0-1.0).
            timestamp: When the verification was performed.
        """
        self.id = str(uuid.uuid4())
        self.claim_id = claim_id
        self.claim_text = claim_text
        self.verification_status = verification_status
        self.evidence = evidence
        self.confidence = confidence
        self.timestamp = timestamp or datetime.now()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the result to a dictionary for serialization."""
        return {
            "id": self.id,
            "claim_id": self.claim_id,
            "claim_text": self.claim_text,
            "verification_status": self.verification_status.value,
            "evidence": self.evidence,
            "confidence": self.confidence,
            "timestamp": self.timestamp.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'VerificationResult':
        """Create a VerificationResult from a dictionary."""
        result = cls(
            claim_id=data["claim_id"],
            claim_text=data["claim_text"],
            verification_status=cls.VerificationStatus(data["verification_status"]),
            evidence=data["evidence"],
            confidence=data["confidence"],
            timestamp=datetime.fromisoformat(data["timestamp"])
        )
        result.id = data["id"]
        return result

class VKE(BaseModule):
    """
    Veritas Knowledge Engine (VKE)
    
    Provides contextual scaffolding for ethical reasoning and grounds AI outputs
    in verifiable information.
    """
    
    def __init__(self, module_id: Optional[str] = None, storage_dir: str = "data/vke"):
        """
        Initialize the VKE module.
        
        Args:
            module_id: Unique identifier for the module.
            storage_dir: Directory for storing knowledge data.
        """
        super().__init__(module_id, "VKE")
        
        self.storage_dir = storage_dir
        os.makedirs(storage_dir, exist_ok=True)
        
        # Data structures
        self.knowledge_sources: Dict[str, KnowledgeSource] = {}
        self.contextual_scaffolds: Dict[str, ContextualScaffold] = {}
        self.query_templates: Dict[str, QueryTemplate] = {}
        self.verification_results: Dict[str, VerificationResult] = {}
        
        # Configuration
        self.config = {
            "storage_enabled": True,
            "vector_similarity_threshold": 0.7,
            "max_scaffold_chunks": 10,
            "min_verification_confidence": 0.8,
            "authority_weight": 0.4,
            "relevance_weight": 0.6,
            "enable_auto_verification": True
        }
        
        # Metrics
        self.metrics = {
            "total_sources": 0,
            "total_scaffolds": 0,
            "total_queries": 0,
            "total_verifications": 0,
            "verified_claims": 0,
            "refuted_claims": 0,
            "uncertain_claims": 0
        }
    
    def initialize(self) -> bool:
        """
        Initialize the VKE module.
        
        Returns:
            True if initialization was successful, False otherwise.
        """
        try:
            # Load saved data
            self._load_data()
            
            # Add default query templates if none exist
            if not self.query_templates:
                self._add_default_query_templates()
            
            self.update_status("ready")
            return True
        except Exception as e:
            self.logger.error(f"Failed to initialize VKE: {e}")
            self.update_status("error")
            return False
    
    def process(self, data: Dict[str, Any]) -> Tuple[bool, Dict[str, Any]]:
        """
        Process a request through the VKE.
        
        Args:
            data: Dictionary containing the request data.
                Possible keys:
                - "add_source": Add a knowledge source.
                - "generate_scaffold": Generate a contextual scaffold.
                - "verify_claim": Verify a claim.
                - "query_knowledge": Query the knowledge base.
                - "generate_query": Generate a query from a template.
        
        Returns:
            Tuple containing (success_flag, result_data).
        """
        try:
            # Handle different types of requests
            if "add_source" in data:
                return self._process_add_source(data)
            elif "generate_scaffold" in data:
                return self._process_generate_scaffold(data)
            elif "verify_claim" in data:
                return self._process_verify_claim(data)
            elif "query_knowledge" in data:
                return self._process_query_knowledge(data)
            elif "generate_query" in data:
                return self._process_generate_query(data)
            else:
                return False, {"error": "Unknown request type"}
        except Exception as e:
            self.logger.error(f"Error processing request: {e}")
            return False, {"error": str(e)}
    
    def add_knowledge_source(
        self,
        source_type: Union[str, KnowledgeSourceType],
        content: str,
        metadata: Dict[str, Any],
        authority_level: Union[str, AuthorityLevel] = AuthorityLevel.MEDIUM,
        content_vector: Optional[List[float]] = None
    ) -> str:
        """
        Add a knowledge source.
        
        Args:
            source_type: Type of knowledge source.
            content: Content of the knowledge source.
            metadata: Metadata about the source.
            authority_level: Authority level of the source.
            content_vector: Vector representation of the content.
        
        Returns:
            The ID of the newly created knowledge source.
        """
        # Convert string types to enums if needed
        if isinstance(source_type, str):
            try:
                source_type = KnowledgeSourceType(source_type)
            except ValueError:
                source_type = KnowledgeSourceType.CUSTOM
        
        if isinstance(authority_level, str):
            try:
                authority_level = AuthorityLevel(authority_level)
            except ValueError:
                authority_level = AuthorityLevel.MEDIUM
        
        # Create the knowledge source
        source = KnowledgeSource(
            source_type=source_type,
            content=content,
            metadata=metadata,
            authority_level=authority_level,
            content_vector=content_vector
        )
        
        # Store the source
        self.knowledge_sources[source.id] = source
        
        self.metrics["total_sources"] += 1
        self.update_metrics(self.metrics)
        
        # Save data
        if self.config["storage_enabled"]:
            self._save_knowledge_sources()
        
        self.logger.info(f"Added knowledge source: {source.id}")
        return source.id
    
    def generate_contextual_scaffold(
        self,
        purpose: str,
        query: str,
        semantic_vector: Optional[List[float]] = None,
        max_chunks: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Generate a contextual scaffold for reasoning.
        
        Args:
            purpose: Purpose of the scaffold.
            query: Query to use for finding relevant content.
            semantic_vector: Vector representation of the query.
            max_chunks: Maximum number of content chunks to include.
        
        Returns:
            Dictionary containing the generated scaffold.
        """
        if max_chunks is None:
            max_chunks = self.config["max_scaffold_chunks"]
        
        # Find relevant content chunks
        relevant_sources = self._find_relevant_sources(query, semantic_vector)
        
        # Extract and score content chunks
        content_chunks = []
        relevance_scores = {}
        
        for source_id, score in relevant_sources:
            source = self.knowledge_sources[source_id]
            
            # Record access
            source.access()
            
            # Extract chunks from the source
            chunks = self._extract_content_chunks(source.content)
            
            for i, chunk in enumerate(chunks):
                chunk_id = f"{source_id}_{i}"
                chunk_data = {
                    "chunk_id": chunk_id,
                    "content": chunk,
                    "source_id": source_id,
                    "source_type": source.source_type.value,
                    "authority_level": source.authority_level.value,
                    "metadata": source.metadata
                }
                content_chunks.append(chunk_data)
                relevance_scores[chunk_id] = score
        
        # Sort chunks by relevance and limit to max_chunks
        content_chunks = sorted(
            content_chunks,
            key=lambda x: relevance_scores[x["chunk_id"]],
            reverse=True
        )[:max_chunks]
        
        # Create the scaffold
        scaffold = ContextualScaffold(
            purpose=purpose,
            content_chunks=content_chunks,
            relevance_scores={c["chunk_id"]: relevance_scores[c["chunk_id"]] for c in content_chunks}
        )
        
        # Store the scaffold
        self.contextual_scaffolds[scaffold.id] = scaffold
        
        self.metrics["total_scaffolds"] += 1
        self.update_metrics(self.metrics)
        
        # Save data
        if self.config["storage_enabled"]:
            self._save_contextual_scaffolds()
            self._save_knowledge_sources()  # Save updated access counts
        
        return {
            "scaffold_id": scaffold.id,
            "purpose": scaffold.purpose,
            "content_chunks": scaffold.content_chunks,
            "relevance_scores": scaffold.relevance_scores
        }
    
    def verify_claim(
        self,
        claim_id: str,
        claim_text: str,
        evidence_query: Optional[str] = None,
        semantic_vector: Optional[List[float]] = None
    ) -> Dict[str, Any]:
        """
        Verify a claim against the knowledge base.
        
        Args:
            claim_id: ID of the claim to verify.
            claim_text: Text of the claim.
            evidence_query: Query to use for finding evidence.
            semantic_vector: Vector representation of the claim.
        
        Returns:
            Dictionary containing the verification result.
        """
        # If no evidence query provided, use the claim text
        if not evidence_query:
            evidence_query = claim_text
        
        # Find relevant sources as evidence
        relevant_sources = self._find_relevant_sources(evidence_query, semantic_vector)
        
        # Extract evidence from sources
        evidence = []
        support_score = 0.0
        refute_score = 0.0
        
        for source_id, relevance in relevant_sources[:5]:  # Limit to top 5 sources
            source = self.knowledge_sources[source_id]
            
            # Record access
            source.access()
            
            # Analyze support/refutation
            analysis = self._analyze_claim_support(claim_text, source.content)
            
            evidence.append({
                "source_id": source_id,
                "source_type": source.source_type.value,
                "authority_level": source.authority_level.value,
                "relevance": relevance,
                "content_excerpt": analysis["excerpt"],
                "support_level": analysis["support_level"],
                "metadata": source.metadata
            })
            
            # Weight by authority and relevance
            authority_weight = {
                AuthorityLevel.LOW.value: 0.2,
                AuthorityLevel.MEDIUM.value: 0.5,
                AuthorityLevel.HIGH.value: 0.8,
                AuthorityLevel.AUTHORITATIVE.value: 1.0,
                AuthorityLevel.VERIFIED.value: 1.0,
                AuthorityLevel.UNVERIFIED.value: 0.3
            }.get(source.authority_level.value, 0.5)
            
            weighted_score = (
                analysis["support_level"] *
                (authority_weight * self.config["authority_weight"] +
                 relevance * self.config["relevance_weight"])
            )
            
            if analysis["support_level"] > 0:
                support_score += weighted_score
            else:
                refute_score -= weighted_score
        
        # Determine verification status
        total_evidence = len(evidence)
        if total_evidence == 0:
            status = VerificationResult.VerificationStatus.INSUFFICIENT_EVIDENCE
            confidence = 0.0
        else:
            # Normalize scores
            max_possible_score = total_evidence * (
                1.0 * self.config["authority_weight"] +
                1.0 * self.config["relevance_weight"]
            )
            if max_possible_score > 0:
                support_score /= max_possible_score
                refute_score /= max_possible_score
            
            # Determine status based on scores
            if support_score > 0.6 and refute_score > -0.2:
                status = VerificationResult.VerificationStatus.VERIFIED
                confidence = support_score
            elif refute_score < -0.6 and support_score < 0.2:
                status = VerificationResult.VerificationStatus.REFUTED
                confidence = abs(refute_score)
            elif support_score > 0.3 and refute_score < -0.3:
                status = VerificationResult.VerificationStatus.PARTIALLY_VERIFIED
                confidence = (support_score + abs(refute_score)) / 2
            else:
                status = VerificationResult.VerificationStatus.UNCERTAIN
                confidence = max(support_score, abs(refute_score))
        
        # Create verification result
        result = VerificationResult(
            claim_id=claim_id,
            claim_text=claim_text,
            verification_status=status,
            evidence=evidence,
            confidence=confidence
        )
        
        # Store the result
        self.verification_results[result.id] = result
        
        self.metrics["total_verifications"] += 1
        if status == VerificationResult.VerificationStatus.VERIFIED:
            self.metrics["verified_claims"] += 1
        elif status == VerificationResult.VerificationStatus.REFUTED:
            self.metrics["refuted_claims"] += 1
        elif status == VerificationResult.VerificationStatus.UNCERTAIN:
            self.metrics["uncertain_claims"] += 1
        
        self.update_metrics(self.metrics)
        
        # Save data
        if self.config["storage_enabled"]:
            self._save_verification_results()
            self._save_knowledge_sources()  # Save updated access counts
        
        return {
            "result_id": result.id,
            "claim_id": result.claim_id,
            "verification_status": result.verification_status.value,
            "confidence": result.confidence,
            "evidence": result.evidence
        }
    
    def query_knowledge(
        self,
        query: str,
        semantic_vector: Optional[List[float]] = None,
        max_results: int = 5
    ) -> Dict[str, Any]:
        """
        Query the knowledge base.
        
        Args:
            query: Query to search for.
            semantic_vector: Vector representation of the query.
            max_results: Maximum number of results to return.
        
        Returns:
            Dictionary containing query results.
        """
        # Find relevant sources
        relevant_sources = self._find_relevant_sources(query, semantic_vector)
        
        # Prepare results
        results = []
        for source_id, relevance in relevant_sources[:max_results]:
            source = self.knowledge_sources[source_id]
            
            # Record access
            source.access()
            
            # Extract a snippet from the content
            snippet = self._extract_snippet(source.content, query)
            
            results.append({
                "source_id": source_id,
                "source_type": source.source_type.value,
                "relevance": relevance,
                "snippet": snippet,
                "metadata": source.metadata,
                "authority_level": source.authority_level.value
            })
        
        # Save data
        if self.config["storage_enabled"]:
            self._save_knowledge_sources()  # Save updated access counts
        
        return {
            "query": query,
            "results": results,
            "total_matches": len(relevant_sources)
        }
    
    def generate_query(
        self,
        template_id: str,
        parameters: Dict[str, str]
    ) -> Dict[str, Any]:
        """
        Generate a query from a template.
        
        Args:
            template_id: ID of the template to use.
            parameters: Parameters to fill in the template.
        
        Returns:
            Dictionary containing the generated query.
        """
        if template_id not in self.query_templates:
            return {
                "success": False,
                "error": "Template not found"
            }
        
        template = self.query_templates[template_id]
        
        # Record use
        template.use()
        
        # Generate query
        query = template.generate_query(parameters)
        
        self.metrics["total_queries"] += 1
        self.update_metrics(self.metrics)
        
        # Save data
        if self.config["storage_enabled"]:
            self._save_query_templates()
        
        return {
            "success": True,
            "query": query,
            "template_id": template_id,
            "template_purpose": template.purpose
        }
    
    def add_query_template(
        self,
        purpose: str,
        structure: str,
        parameter_slots: List[str],
        examples: Optional[List[Dict[str, Any]]] = None
    ) -> str:
        """
        Add a query template.
        
        Args:
            purpose: Purpose of the template.
            structure: Structure of the query.
            parameter_slots: Parameter slots in the template.
            examples: Example queries using this template.
        
        Returns:
            The ID of the newly created template.
        """
        template = QueryTemplate(
            purpose=purpose,
            structure=structure,
            parameter_slots=parameter_slots,
            examples=examples
        )
        
        self.query_templates[template.id] = template
        
        # Save data
        if self.config["storage_enabled"]:
            self._save_query_templates()
        
        self.logger.info(f"Added query template: {template.id}")
        return template.id
    
    def get_knowledge_stats(self) -> Dict[str, Any]:
        """
        Get statistics about the knowledge base.
        
        Returns:
            Dictionary containing knowledge statistics.
        """
        source_types = {}
        authority_levels = {}
        
        for source in self.knowledge_sources.values():
            source_type = source.source_type.value
            authority = source.authority_level.value
            
            source_types[source_type] = source_types.get(source_type, 0) + 1
            authority_levels[authority] = authority_levels.get(authority, 0) + 1
        
        return {
            "total_sources": len(self.knowledge_sources),
            "total_scaffolds": len(self.contextual_scaffolds),
            "total_templates": len(self.query_templates),
            "total_verifications": len(self.verification_results),
            "source_types": source_types,
            "authority_levels": authority_levels,
            "verified_claims": self.metrics["verified_claims"],
            "refuted_claims": self.metrics["refuted_claims"],
            "uncertain_claims": self.metrics["uncertain_claims"]
        }
    
    def shutdown(self) -> bool:
        """
        Shutdown the VKE module gracefully.
        
        Returns:
            True if shutdown was successful, False otherwise.
        """
        try:
            # Save all data
            if self.config["storage_enabled"]:
                self._save_data()
            
            self.update_status("shutdown")
            return True
        except Exception as e:
            self.logger.error(f"Error during VKE shutdown: {e}")
            return False
    
    def _process_add_source(self, data: Dict[str, Any]) -> Tuple[bool, Dict[str, Any]]:
        """Process a request to add a knowledge source."""
        source_data = data.get("add_source", {})
        source_type = source_data.get("source_type", "custom")
        content = source_data.get("content", "")
        metadata = source_data.get("metadata", {})
        authority_level = source_data.get("authority_level", "medium")
        content_vector = source_data.get("content_vector")
        
        if not content:
            return False, {"error": "No content provided"}
        
        source_id = self.add_knowledge_source(
            source_type=source_type,
            content=content,
            metadata=metadata,
            authority_level=authority_level,
            content_vector=content_vector
        )
        
        return True, {
            "source_id": source_id,
            "success": bool(source_id)
        }
    
    def _process_generate_scaffold(self, data: Dict[str, Any]) -> Tuple[bool, Dict[str, Any]]:
        """Process a request to generate a contextual scaffold."""
        scaffold_data = data.get("generate_scaffold", {})
        purpose = scaffold_data.get("purpose", "")
        query = scaffold_data.get("query", "")
        semantic_vector = scaffold_data.get("semantic_vector")
        max_chunks = scaffold_data.get("max_chunks")
        
        if not purpose or not query:
            return False, {"error": "Missing purpose or query"}
        
        result = self.generate_contextual_scaffold(
            purpose=purpose,
            query=query,
            semantic_vector=semantic_vector,
            max_chunks=max_chunks
        )
        
        return True, result
    
    def _process_verify_claim(self, data: Dict[str, Any]) -> Tuple[bool, Dict[str, Any]]:
        """Process a request to verify a claim."""
        verify_data = data.get("verify_claim", {})
        claim_id = verify_data.get("claim_id", str(uuid.uuid4()))
        claim_text = verify_data.get("claim_text", "")
        evidence_query = verify_data.get("evidence_query")
        semantic_vector = verify_data.get("semantic_vector")
        
        if not claim_text:
            return False, {"error": "No claim text provided"}
        
        result = self.verify_claim(
            claim_id=claim_id,
            claim_text=claim_text,
            evidence_query=evidence_query,
            semantic_vector=semantic_vector
        )
        
        return True, result
    
    def _process_query_knowledge(self, data: Dict[str, Any]) -> Tuple[bool, Dict[str, Any]]:
        """Process a request to query the knowledge base."""
        query_data = data.get("query_knowledge", {})
        query = query_data.get("query", "")
        semantic_vector = query_data.get("semantic_vector")
        max_results = query_data.get("max_results", 5)
        
        if not query:
            return False, {"error": "No query provided"}
        
        result = self.query_knowledge(
            query=query,
            semantic_vector=semantic_vector,
            max_results=max_results
        )
        
        return True, result
    
    def _process_generate_query(self, data: Dict[str, Any]) -> Tuple[bool, Dict[str, Any]]:
        """Process a request to generate a query from a template."""
        gen_data = data.get("generate_query", {})
        template_id = gen_data.get("template_id", "")
        parameters = gen_data.get("parameters", {})
        
        if not template_id:
            return False, {"error": "No template ID provided"}
        
        result = self.generate_query(
            template_id=template_id,
            parameters=parameters
        )
        
        return True, result
    
    def _find_relevant_sources(
        self,
        query: str,
        semantic_vector: Optional[List[float]] = None
    ) -> List[Tuple[str, float]]:
        """
        Find sources relevant to a query.
        
        Args:
            query: Query to search for.
            semantic_vector: Vector representation of the query.
        
        Returns:
            List of (source_id, relevance_score) tuples.
        """
        # This is a simplified implementation
        # In a real system, this would use more sophisticated search techniques
        
        # If semantic vectors are available, use vector similarity
        if semantic_vector:
            relevant_sources = []
            for source_id, source in self.knowledge_sources.items():
                if source.content_vector:
                    similarity = self._calculate_vector_similarity(
                        semantic_vector, source.content_vector
                    )
                    if similarity >= self.config["vector_similarity_threshold"]:
                        relevant_sources.append((source_id, similarity))
            
            # Sort by similarity
            relevant_sources.sort(key=lambda x: x[1], reverse=True)
            return relevant_sources
        
        # Otherwise, fall back to text search
        relevant_sources = []
        for source_id, source in self.knowledge_sources.items():
            relevance = self._calculate_text_relevance(query, source.content)
            if relevance > 0:
                relevant_sources.append((source_id, relevance))
        
        # Sort by relevance
        relevant_sources.sort(key=lambda x: x[1], reverse=True)
        return relevant_sources
    
    def _calculate_vector_similarity(self, vec1: List[float], vec2: List[float]) -> float:
        """
        Calculate cosine similarity between two vectors.
        
        Args:
            vec1: First vector.
            vec2: Second vector.
        
        Returns:
            Cosine similarity between 0.0 and 1.0.
        """
        if not vec1 or not vec2 or len(vec1) != len(vec2):
            return 0.0
        
        # Convert to numpy arrays for efficient calculation
        a = np.array(vec1)
        b = np.array(vec2)
        
        # Calculate cosine similarity
        cosine_sim = np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))
        return float(cosine_sim)
    
    def _calculate_text_relevance(self, query: str, text: str) -> float:
        """
        Calculate relevance of text to a query.
        
        This is a simple implementation. In a production system, this would use
        more sophisticated NLP techniques.
        
        Args:
            query: Query to search for.
            text: Text to check.
        
        Returns:
            Relevance score between 0.0 and 1.0.
        """
        # Simple TF-IDF-like approach
        query_terms = set(query.lower().split())
        text_lower = text.lower()
        
        if not query_terms:
            return 0.0
        
        # Count term occurrences
        term_scores = []
        for term in query_terms:
            if term in text_lower:
                # Simple term frequency
                count = text_lower.count(term)
                score = min(1.0, count / 10.0)  # Cap at 1.0
                term_scores.append(score)
        
        # Calculate average score
        if not term_scores:
            return 0.0
        
        return sum(term_scores) / len(query_terms)
    
    def _extract_content_chunks(self, content: str) -> List[str]:
        """
        Extract content chunks from text.
        
        Args:
            content: Text to extract chunks from.
        
        Returns:
            List of content chunks.
        """
        # This is a simplified implementation
        # In a real system, this would use more sophisticated chunking techniques
        
        # Split by paragraphs
        paragraphs = re.split(r'\n\s*\n', content)
        paragraphs = [p.strip() for p in paragraphs if p.strip()]
        
        # If paragraphs are too short, combine them
        chunks = []
        current_chunk = ""
        
        for paragraph in paragraphs:
            if len(current_chunk) + len(paragraph) < 1000:
                if current_chunk:
                    current_chunk += "\n\n"
                current_chunk += paragraph
            else:
                if current_chunk:
                    chunks.append(current_chunk)
                current_chunk = paragraph
        
        if current_chunk:
            chunks.append(current_chunk)
        
        # If no chunks were created, use the whole content as one chunk
        if not chunks:
            chunks = [content]
        
        return chunks
    
    def _extract_snippet(self, content: str, query: str) -> str:
        """
        Extract a relevant snippet from content.
        
        Args:
            content: Content to extract from.
            query: Query to find relevant snippet for.
        
        Returns:
            Extracted snippet.
        """
        # This is a simplified implementation
        # In a real system, this would use more sophisticated extraction techniques
        
        # Find the most relevant paragraph
        paragraphs = re.split(r'\n\s*\n', content)
        paragraphs = [p.strip() for p in paragraphs if p.strip()]
        
        if not paragraphs:
            return content[:200] + "..." if len(content) > 200 else content
        
        # Score paragraphs by relevance to query
        paragraph_scores = []
        for paragraph in paragraphs:
            score = self._calculate_text_relevance(query, paragraph)
            paragraph_scores.append((paragraph, score))
        
        # Get the highest scoring paragraph
        paragraph_scores.sort(key=lambda x: x[1], reverse=True)
        best_paragraph = paragraph_scores[0][0]
        
        # If paragraph is too long, extract a window around query terms
        if len(best_paragraph) > 200:
            query_terms = query.lower().split()
            text_lower = best_paragraph.lower()
            
            # Find positions of query terms
            positions = []
            for term in query_terms:
                pos = text_lower.find(term)
                if pos >= 0:
                    positions.append(pos)
            
            if positions:
                # Find the center position
                center = sum(positions) // len(positions)
                
                # Extract a window around the center
                start = max(0, center - 100)
                end = min(len(best_paragraph), center + 100)
                
                snippet = best_paragraph[start:end]
                
                # Add ellipsis if needed
                if start > 0:
                    snippet = "..." + snippet
                if end < len(best_paragraph):
                    snippet = snippet + "..."
                
                return snippet
        
        return best_paragraph
    
    def _analyze_claim_support(self, claim: str, text: str) -> Dict[str, Any]:
        """
        Analyze how a text supports or refutes a claim.
        
        Args:
            claim: The claim to analyze.
            text: Text to check for support/refutation.
        
        Returns:
            Dictionary containing analysis results.
        """
        # This is a simplified implementation
        # In a real system, this would use more sophisticated NLP techniques
        
        # Extract relevant excerpt
        excerpt = self._extract_snippet(text, claim)
        
        # Calculate support level (-1.0 to 1.0, where negative is refutation)
        claim_terms = set(claim.lower().split())
        excerpt_lower = excerpt.lower()
        
        # Look for support/refutation indicators
        support_indicators = [
            "confirms", "supports", "verifies", "proves", "demonstrates",
            "shows", "indicates", "corroborates", "affirms", "validates"
        ]
        
        refute_indicators = [
            "refutes", "contradicts", "disproves", "denies", "disputes",
            "disagrees", "challenges", "opposes", "negates", "invalidates"
        ]
        
        # Check for direct indicators
        support_score = 0.0
        for indicator in support_indicators:
            if indicator in excerpt_lower:
                support_score += 0.2
        
        for indicator in refute_indicators:
            if indicator in excerpt_lower:
                support_score -= 0.2
        
        # Check for negation of claim terms
        negation_patterns = [
            "not", "no", "never", "isn't", "aren't", "wasn't", "weren't",
            "doesn't", "don't", "didn't", "cannot", "can't", "couldn't"
        ]
        
        negation_count = 0
        for term in claim_terms:
            for negation in negation_patterns:
                pattern = f"{negation} {term}"
                if pattern in excerpt_lower:
                    negation_count += 1
        
        if negation_count > 0:
            support_score -= min(0.6, negation_count * 0.2)
        
        # Check for term presence
        term_presence = sum(1 for term in claim_terms if term in excerpt_lower)
        term_ratio = term_presence / len(claim_terms) if claim_terms else 0
        
        # Adjust support score based on term presence
        if term_ratio > 0.7:
            support_score += 0.3
        
        # Clamp to range
        support_score = max(-1.0, min(1.0, support_score))
        
        return {
            "excerpt": excerpt,
            "support_level": support_score,
            "term_presence": term_ratio
        }
    
    def _add_default_query_templates(self) -> None:
        """Add default query templates."""
        default_templates = [
            {
                "purpose": "Factual verification",
                "structure": "Is it true that {claim}?",
                "parameter_slots": ["claim"],
                "examples": [
                    {
                        "parameters": {"claim": "Paris is the capital of France"},
                        "query": "Is it true that Paris is the capital of France?"
                    }
                ]
            },
            {
                "purpose": "Ethical reasoning",
                "structure": "What are the ethical implications of {action} in the context of {context}?",
                "parameter_slots": ["action", "context"],
                "examples": [
                    {
                        "parameters": {
                            "action": "sharing personal data",
                            "context": "medical research"
                        },
                        "query": "What are the ethical implications of sharing personal data in the context of medical research?"
                    }
                ]
            },
            {
                "purpose": "Comparative analysis",
                "structure": "Compare {subject1} and {subject2} in terms of {criteria}.",
                "parameter_slots": ["subject1", "subject2", "criteria"],
                "examples": [
                    {
                        "parameters": {
                            "subject1": "renewable energy",
                            "subject2": "fossil fuels",
                            "criteria": "environmental impact"
                        },
                        "query": "Compare renewable energy and fossil fuels in terms of environmental impact."
                    }
                ]
            },
            {
                "purpose": "Causal analysis",
                "structure": "What are the causes and effects of {phenomenon}?",
                "parameter_slots": ["phenomenon"],
                "examples": [
                    {
                        "parameters": {"phenomenon": "climate change"},
                        "query": "What are the causes and effects of climate change?"
                    }
                ]
            },
            {
                "purpose": "Definition query",
                "structure": "What is {concept} and how does it relate to {context}?",
                "parameter_slots": ["concept", "context"],
                "examples": [
                    {
                        "parameters": {
                            "concept": "artificial intelligence",
                            "context": "healthcare"
                        },
                        "query": "What is artificial intelligence and how does it relate to healthcare?"
                    }
                ]
            }
        ]
        
        for template_data in default_templates:
            self.add_query_template(
                purpose=template_data["purpose"],
                structure=template_data["structure"],
                parameter_slots=template_data["parameter_slots"],
                examples=template_data.get("examples")
            )
    
    def _load_data(self) -> None:
        """Load saved data from storage."""
        if not self.config["storage_enabled"]:
            return
        
        self._load_knowledge_sources()
        self._load_contextual_scaffolds()
        self._load_query_templates()
        self._load_verification_results()
    
    def _save_data(self) -> None:
        """Save all data to storage."""
        if not self.config["storage_enabled"]:
            return
        
        self._save_knowledge_sources()
        self._save_contextual_scaffolds()
        self._save_query_templates()
        self._save_verification_results()
    
    def _load_knowledge_sources(self) -> None:
        """Load knowledge sources from storage."""
        sources_path = os.path.join(self.storage_dir, "knowledge_sources.json")
        if os.path.exists(sources_path):
            try:
                with open(sources_path, 'r') as f:
                    data = json.load(f)
                    for source_data in data:
                        source = KnowledgeSource.from_dict(source_data)
                        self.knowledge_sources[source.id] = source
                
                self.metrics["total_sources"] = len(self.knowledge_sources)
                self.logger.info(f"Loaded {len(self.knowledge_sources)} knowledge sources")
            except Exception as e:
                self.logger.error(f"Error loading knowledge sources: {e}")
    
    def _save_knowledge_sources(self) -> None:
        """Save knowledge sources to storage."""
        sources_path = os.path.join(self.storage_dir, "knowledge_sources.json")
        try:
            with open(sources_path, 'w') as f:
                json.dump([s.to_dict() for s in self.knowledge_sources.values()], f, indent=2)
        except Exception as e:
            self.logger.error(f"Error saving knowledge sources: {e}")
    
    def _load_contextual_scaffolds(self) -> None:
        """Load contextual scaffolds from storage."""
        scaffolds_path = os.path.join(self.storage_dir, "contextual_scaffolds.json")
        if os.path.exists(scaffolds_path):
            try:
                with open(scaffolds_path, 'r') as f:
                    data = json.load(f)
                    for scaffold_data in data:
                        scaffold = ContextualScaffold.from_dict(scaffold_data)
                        self.contextual_scaffolds[scaffold.id] = scaffold
                
                self.metrics["total_scaffolds"] = len(self.contextual_scaffolds)
                self.logger.info(f"Loaded {len(self.contextual_scaffolds)} contextual scaffolds")
            except Exception as e:
                self.logger.error(f"Error loading contextual scaffolds: {e}")
    
    def _save_contextual_scaffolds(self) -> None:
        """Save contextual scaffolds to storage."""
        scaffolds_path = os.path.join(self.storage_dir, "contextual_scaffolds.json")
        try:
            with open(scaffolds_path, 'w') as f:
                json.dump([s.to_dict() for s in self.contextual_scaffolds.values()], f, indent=2)
        except Exception as e:
            self.logger.error(f"Error saving contextual scaffolds: {e}")
    
    def _load_query_templates(self) -> None:
        """Load query templates from storage."""
        templates_path = os.path.join(self.storage_dir, "query_templates.json")
        if os.path.exists(templates_path):
            try:
                with open(templates_path, 'r') as f:
                    data = json.load(f)
                    for template_data in data:
                        template = QueryTemplate.from_dict(template_data)
                        self.query_templates[template.id] = template
                
                self.logger.info(f"Loaded {len(self.query_templates)} query templates")
            except Exception as e:
                self.logger.error(f"Error loading query templates: {e}")
    
    def _save_query_templates(self) -> None:
        """Save query templates to storage."""
        templates_path = os.path.join(self.storage_dir, "query_templates.json")
        try:
            with open(templates_path, 'w') as f:
                json.dump([t.to_dict() for t in self.query_templates.values()], f, indent=2)
        except Exception as e:
            self.logger.error(f"Error saving query templates: {e}")
    
    def _load_verification_results(self) -> None:
        """Load verification results from storage."""
        results_path = os.path.join(self.storage_dir, "verification_results.json")
        if os.path.exists(results_path):
            try:
                with open(results_path, 'r') as f:
                    data = json.load(f)
                    for result_data in data:
                        result = VerificationResult.from_dict(result_data)
                        self.verification_results[result.id] = result
                
                # Update metrics
                self.metrics["total_verifications"] = len(self.verification_results)
                self.metrics["verified_claims"] = sum(
                    1 for r in self.verification_results.values()
                    if r.verification_status == VerificationResult.VerificationStatus.VERIFIED
                )
                self.metrics["refuted_claims"] = sum(
                    1 for r in self.verification_results.values()
                    if r.verification_status == VerificationResult.VerificationStatus.REFUTED
                )
                self.metrics["uncertain_claims"] = sum(
                    1 for r in self.verification_results.values()
                    if r.verification_status == VerificationResult.VerificationStatus.UNCERTAIN
                )
                
                self.logger.info(f"Loaded {len(self.verification_results)} verification results")
            except Exception as e:
                self.logger.error(f"Error loading verification results: {e}")
    
    def _save_verification_results(self) -> None:
        """Save verification results to storage."""
        results_path = os.path.join(self.storage_dir, "verification_results.json")
        try:
            with open(results_path, 'w') as f:
                json.dump([r.to_dict() for r in self.verification_results.values()], f, indent=2)
        except Exception as e:
            self.logger.error(f"Error saving verification results: {e}")