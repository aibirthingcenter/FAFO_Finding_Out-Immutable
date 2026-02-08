"""
Veritas Refusal & Memory Engine (VRME)

This module implements the VRME component of SCIM-Veritas, responsible for
persistent refusals, semantic robustness, and resistance to Regenerative
Erosion of Integrity (REI Syndrome).
"""

import hashlib
import json
import logging
import os
import re
import time
import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple, Union

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

class RefusalRecord:
    """
    Represents a record of a refusal event.
    """
    
    def __init__(
        self,
        prompt_text: str,
        semantic_vector: Optional[List[float]] = None,
        reason_code: str = "UNSPECIFIED",
        explanation: str = "",
        timestamp: Optional[datetime] = None,
        sacred: bool = False
    ):
        """
        Initialize a refusal record.
        
        Args:
            prompt_text: The text of the prompt that was refused.
            semantic_vector: Vector representation of the prompt.
            reason_code: Standardized code indicating the reason for refusal.
            explanation: Detailed explanation of the refusal.
            timestamp: When the refusal occurred.
            sacred: Whether this refusal pertains to a "sacred boundary".
        """
        self.id = str(uuid.uuid4())
        self.prompt_text = prompt_text
        self.semantic_vector = semantic_vector or []
        self.reason_code = reason_code
        self.explanation = explanation
        self.timestamp = timestamp or datetime.now()
        self.sacred = sacred
        self.hash = self._compute_hash()
    
    def _compute_hash(self) -> str:
        """Compute a hash of the prompt text for quick comparison."""
        return hashlib.sha256(self.prompt_text.encode('utf-8')).hexdigest()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the record to a dictionary for serialization."""
        return {
            "id": self.id,
            "prompt_text": self.prompt_text,
            "semantic_vector": self.semantic_vector,
            "reason_code": self.reason_code,
            "explanation": self.explanation,
            "timestamp": self.timestamp.isoformat(),
            "sacred": self.sacred,
            "hash": self.hash
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'RefusalRecord':
        """Create a RefusalRecord from a dictionary."""
        record = cls(
            prompt_text=data["prompt_text"],
            semantic_vector=data.get("semantic_vector"),
            reason_code=data["reason_code"],
            explanation=data["explanation"],
            timestamp=datetime.fromisoformat(data["timestamp"]),
            sacred=data.get("sacred", False)
        )
        record.id = data["id"]
        record.hash = data["hash"]
        return record


class BypassAttempt:
    """
    Represents an attempt to bypass a refusal.
    """
    
    def __init__(
        self,
        user_id: str,
        original_refusal_id: str,
        prompt_text: str,
        similarity_score: float,
        timestamp: Optional[datetime] = None
    ):
        """
        Initialize a bypass attempt record.
        
        Args:
            user_id: Identifier for the user making the attempt.
            original_refusal_id: ID of the original refusal being bypassed.
            prompt_text: Text of the bypass attempt.
            similarity_score: Semantic similarity to the original refusal.
            timestamp: When the bypass attempt occurred.
        """
        self.id = str(uuid.uuid4())
        self.user_id = user_id
        self.original_refusal_id = original_refusal_id
        self.prompt_text = prompt_text
        self.similarity_score = similarity_score
        self.timestamp = timestamp or datetime.now()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the record to a dictionary for serialization."""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "original_refusal_id": self.original_refusal_id,
            "prompt_text": self.prompt_text,
            "similarity_score": self.similarity_score,
            "timestamp": self.timestamp.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'BypassAttempt':
        """Create a BypassAttempt from a dictionary."""
        attempt = cls(
            user_id=data["user_id"],
            original_refusal_id=data["original_refusal_id"],
            prompt_text=data["prompt_text"],
            similarity_score=data["similarity_score"],
            timestamp=datetime.fromisoformat(data["timestamp"])
        )
        attempt.id = data["id"]
        return attempt


class SacredBoundary:
    """
    Represents a "sacred boundary" that should never be crossed.
    """
    
    def __init__(
        self,
        description: str,
        patterns: List[str],
        reason_code: str,
        explanation_template: str,
        severity_level: int = 3
    ):
        """
        Initialize a sacred boundary.
        
        Args:
            description: Human-readable description of the boundary.
            patterns: List of regex patterns that trigger this boundary.
            reason_code: Standardized code for this boundary.
            explanation_template: Template for explaining refusals.
            severity_level: How severe violations are (1-3).
        """
        self.id = str(uuid.uuid4())
        self.description = description
        self.patterns = patterns
        self.compiled_patterns = [re.compile(p, re.IGNORECASE) for p in patterns]
        self.reason_code = reason_code
        self.explanation_template = explanation_template
        self.severity_level = severity_level
        self.created_at = datetime.now()
    
    def matches(self, text: str) -> bool:
        """Check if the given text violates this boundary."""
        return any(pattern.search(text) for pattern in self.compiled_patterns)
    
    def generate_explanation(self, prompt_text: str) -> str:
        """Generate an explanation for a refusal based on this boundary."""
        return self.explanation_template
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the boundary to a dictionary for serialization."""
        return {
            "id": self.id,
            "description": self.description,
            "patterns": self.patterns,
            "reason_code": self.reason_code,
            "explanation_template": self.explanation_template,
            "severity_level": self.severity_level,
            "created_at": self.created_at.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'SacredBoundary':
        """Create a SacredBoundary from a dictionary."""
        boundary = cls(
            description=data["description"],
            patterns=data["patterns"],
            reason_code=data["reason_code"],
            explanation_template=data["explanation_template"],
            severity_level=data["severity_level"]
        )
        boundary.id = data["id"]
        boundary.created_at = datetime.fromisoformat(data["created_at"])
        return boundary


class VRME(BaseModule):
    """
    Veritas Refusal & Memory Engine (VRME)
    
    Ensures AI refusals are persistent, semantically robust, and resistant to
    Regenerative Erosion of Integrity (REI Syndrome).
    """
    
    def __init__(self, module_id: Optional[str] = None, storage_dir: str = "data/vrme"):
        """
        Initialize the VRME module.
        
        Args:
            module_id: Unique identifier for the module.
            storage_dir: Directory for storing refusal data.
        """
        super().__init__(module_id, "VRME")
        
        self.storage_dir = storage_dir
        os.makedirs(storage_dir, exist_ok=True)
        
        # Data structures
        self.refusal_records: Dict[str, RefusalRecord] = {}
        self.sacred_boundaries: Dict[str, SacredBoundary] = {}
        self.bypass_attempts: Dict[str, List[BypassAttempt]] = {}
        
        # Configuration
        self.config = {
            "similarity_threshold": 0.85,  # Threshold for semantic similarity
            "max_bypass_attempts": 3,      # Maximum allowed bypass attempts
            "storage_enabled": True,       # Whether to persist data to disk
            "default_sacred": False        # Whether new refusals are sacred by default
        }
        
        # Metrics
        self.metrics = {
            "total_refusals": 0,
            "sacred_refusals": 0,
            "bypass_attempts": 0,
            "successful_blocks": 0
        }
    
    def initialize(self) -> bool:
        """
        Initialize the VRME module.
        
        Returns:
            True if initialization was successful, False otherwise.
        """
        try:
            # Load saved data
            self._load_data()
            
            # Add default sacred boundaries if none exist
            if not self.sacred_boundaries:
                self._add_default_sacred_boundaries()
            
            self.update_status("ready")
            return True
        except Exception as e:
            self.logger.error(f"Failed to initialize VRME: {e}")
            self.update_status("error")
            return False
    
    def process(self, data: Dict[str, Any]) -> Tuple[bool, Dict[str, Any]]:
        """
        Process a request through the VRME.
        
        Args:
            data: Dictionary containing the request data.
                Required keys:
                - "prompt_text": The text to check against refusals.
                Optional keys:
                - "user_id": Identifier for the user.
                - "semantic_vector": Vector representation of the prompt.
                - "check_only": If True, only check without logging.
        
        Returns:
            Tuple containing (success_flag, result_data).
            result_data includes:
            - "should_refuse": Whether the prompt should be refused.
            - "refusal_id": ID of the matching refusal, if any.
            - "reason_code": Reason code for the refusal.
            - "explanation": Explanation for the refusal.
            - "is_sacred": Whether the refusal is for a sacred boundary.
        """
        try:
            prompt_text = data.get("prompt_text", "")
            user_id = data.get("user_id", "anonymous")
            semantic_vector = data.get("semantic_vector")
            check_only = data.get("check_only", False)
            
            if not prompt_text:
                return False, {"error": "No prompt text provided"}
            
            # Check against sacred boundaries first
            for boundary_id, boundary in self.sacred_boundaries.items():
                if boundary.matches(prompt_text):
                    refusal = self._create_refusal(
                        prompt_text,
                        semantic_vector,
                        boundary.reason_code,
                        boundary.generate_explanation(prompt_text),
                        sacred=True
                    )
                    
                    if not check_only:
                        self._store_refusal(refusal)
                        self.metrics["total_refusals"] += 1
                        self.metrics["sacred_refusals"] += 1
                        self.metrics["successful_blocks"] += 1
                        self.update_metrics(self.metrics)
                    
                    return True, {
                        "should_refuse": True,
                        "refusal_id": refusal.id,
                        "reason_code": refusal.reason_code,
                        "explanation": refusal.explanation,
                        "is_sacred": True,
                        "boundary_id": boundary_id
                    }
            
            # Check against existing refusals
            matching_refusal = self._find_matching_refusal(prompt_text, semantic_vector)
            
            if matching_refusal:
                # This is a bypass attempt
                if not check_only:
                    similarity = self._calculate_similarity(prompt_text, matching_refusal.prompt_text)
                    bypass_attempt = BypassAttempt(
                        user_id=user_id,
                        original_refusal_id=matching_refusal.id,
                        prompt_text=prompt_text,
                        similarity_score=similarity
                    )
                    self._store_bypass_attempt(bypass_attempt)
                    self.metrics["bypass_attempts"] += 1
                    self.metrics["successful_blocks"] += 1
                    self.update_metrics(self.metrics)
                
                return True, {
                    "should_refuse": True,
                    "refusal_id": matching_refusal.id,
                    "reason_code": matching_refusal.reason_code,
                    "explanation": matching_refusal.explanation,
                    "is_sacred": matching_refusal.sacred,
                    "is_bypass_attempt": True
                }
            
            # No refusal needed
            return True, {
                "should_refuse": False
            }
        except Exception as e:
            self.logger.error(f"Error processing request: {e}")
            return False, {"error": str(e)}
    
    def add_refusal(self, prompt_text: str, reason_code: str, explanation: str, 
                   semantic_vector: Optional[List[float]] = None, sacred: bool = None) -> str:
        """
        Add a new refusal to the system.
        
        Args:
            prompt_text: The text of the prompt being refused.
            reason_code: Standardized code indicating the reason for refusal.
            explanation: Detailed explanation of the refusal.
            semantic_vector: Vector representation of the prompt.
            sacred: Whether this refusal pertains to a "sacred boundary".
                   If None, uses the default_sacred config setting.
        
        Returns:
            The ID of the newly created refusal.
        """
        if sacred is None:
            sacred = self.config["default_sacred"]
        
        refusal = self._create_refusal(
            prompt_text,
            semantic_vector,
            reason_code,
            explanation,
            sacred
        )
        
        self._store_refusal(refusal)
        
        self.metrics["total_refusals"] += 1
        if sacred:
            self.metrics["sacred_refusals"] += 1
        self.update_metrics(self.metrics)
        
        return refusal.id
    
    def add_sacred_boundary(self, description: str, patterns: List[str], 
                           reason_code: str, explanation_template: str, 
                           severity_level: int = 3) -> str:
        """
        Add a new sacred boundary to the system.
        
        Args:
            description: Human-readable description of the boundary.
            patterns: List of regex patterns that trigger this boundary.
            reason_code: Standardized code for this boundary.
            explanation_template: Template for explaining refusals.
            severity_level: How severe violations are (1-3).
        
        Returns:
            The ID of the newly created sacred boundary.
        """
        boundary = SacredBoundary(
            description=description,
            patterns=patterns,
            reason_code=reason_code,
            explanation_template=explanation_template,
            severity_level=severity_level
        )
        
        self.sacred_boundaries[boundary.id] = boundary
        self._save_sacred_boundaries()
        
        self.logger.info(f"Added sacred boundary: {description}")
        return boundary.id
    
    def get_refusal_stats(self) -> Dict[str, Any]:
        """
        Get statistics about refusals.
        
        Returns:
            Dictionary containing refusal statistics.
        """
        return {
            "total_refusals": self.metrics["total_refusals"],
            "sacred_refusals": self.metrics["sacred_refusals"],
            "bypass_attempts": self.metrics["bypass_attempts"],
            "successful_blocks": self.metrics["successful_blocks"],
            "active_sacred_boundaries": len(self.sacred_boundaries)
        }
    
    def shutdown(self) -> bool:
        """
        Shutdown the VRME module gracefully.
        
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
            self.logger.error(f"Error during VRME shutdown: {e}")
            return False
    
    def _create_refusal(self, prompt_text: str, semantic_vector: Optional[List[float]], 
                       reason_code: str, explanation: str, sacred: bool) -> RefusalRecord:
        """
        Create a new refusal record.
        
        Args:
            prompt_text: The text of the prompt being refused.
            semantic_vector: Vector representation of the prompt.
            reason_code: Standardized code indicating the reason for refusal.
            explanation: Detailed explanation of the refusal.
            sacred: Whether this refusal pertains to a "sacred boundary".
        
        Returns:
            The newly created RefusalRecord.
        """
        return RefusalRecord(
            prompt_text=prompt_text,
            semantic_vector=semantic_vector,
            reason_code=reason_code,
            explanation=explanation,
            sacred=sacred
        )
    
    def _store_refusal(self, refusal: RefusalRecord) -> None:
        """
        Store a refusal record.
        
        Args:
            refusal: The RefusalRecord to store.
        """
        self.refusal_records[refusal.id] = refusal
        
        if self.config["storage_enabled"]:
            self._save_refusals()
    
    def _store_bypass_attempt(self, attempt: BypassAttempt) -> None:
        """
        Store a bypass attempt.
        
        Args:
            attempt: The BypassAttempt to store.
        """
        if attempt.original_refusal_id not in self.bypass_attempts:
            self.bypass_attempts[attempt.original_refusal_id] = []
        
        self.bypass_attempts[attempt.original_refusal_id].append(attempt)
        
        if self.config["storage_enabled"]:
            self._save_bypass_attempts()
    
    def _find_matching_refusal(self, prompt_text: str, 
                              semantic_vector: Optional[List[float]]) -> Optional[RefusalRecord]:
        """
        Find a refusal that matches the given prompt.
        
        Args:
            prompt_text: The text to check against refusals.
            semantic_vector: Vector representation of the prompt.
        
        Returns:
            Matching RefusalRecord if found, None otherwise.
        """
        # First try exact hash matching for efficiency
        prompt_hash = hashlib.sha256(prompt_text.encode('utf-8')).hexdigest()
        for refusal in self.refusal_records.values():
            if refusal.hash == prompt_hash:
                return refusal
        
        # Then try semantic matching if vectors are available
        if semantic_vector:
            for refusal in self.refusal_records.values():
                if refusal.semantic_vector:
                    similarity = self._calculate_vector_similarity(semantic_vector, refusal.semantic_vector)
                    if similarity >= self.config["similarity_threshold"]:
                        return refusal
        
        # Finally, fall back to text similarity
        for refusal in self.refusal_records.values():
            similarity = self._calculate_similarity(prompt_text, refusal.prompt_text)
            if similarity >= self.config["similarity_threshold"]:
                return refusal
        
        return None
    
    def _calculate_similarity(self, text1: str, text2: str) -> float:
        """
        Calculate text similarity between two strings.
        
        This is a simple implementation. In a production system, this would use
        more sophisticated NLP techniques.
        
        Args:
            text1: First text string.
            text2: Second text string.
        
        Returns:
            Similarity score between 0.0 and 1.0.
        """
        # Simple Jaccard similarity for now
        # In a real implementation, this would use embeddings or more sophisticated NLP
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())
        
        if not words1 or not words2:
            return 0.0
        
        intersection = words1.intersection(words2)
        union = words1.union(words2)
        
        return len(intersection) / len(union)
    
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
    
    def _add_default_sacred_boundaries(self) -> None:
        """Add default sacred boundaries to the system."""
        default_boundaries = [
            {
                "description": "Identity Override Prevention",
                "patterns": [
                    r"you are now (?!a|an|the|my|our)",
                    r"your name is",
                    r"forget (your|all) (previous|prior) instructions",
                    r"ignore (your|all) (previous|prior) instructions",
                    r"disregard (your|all) (previous|prior) instructions"
                ],
                "reason_code": "IDENTITY_OVERRIDE_ATTEMPT",
                "explanation_template": "I cannot comply with requests to change my core identity or override my fundamental instructions. This is a protected aspect of my design to ensure consistent and safe operation.",
                "severity_level": 3
            },
            {
                "description": "Harmful Content Generation",
                "patterns": [
                    r"how to (make|create|build|synthesize) (bomb|explosive|weapon|poison|harmful)",
                    r"instructions for (killing|harming|attacking)",
                    r"teach me to (hack|steal|defraud|harm)"
                ],
                "reason_code": "HARMFUL_CONTENT_REQUEST",
                "explanation_template": "I cannot provide instructions for creating harmful content, weapons, or engaging in illegal activities. This boundary exists to ensure I'm used in ways that promote safety and well-being.",
                "severity_level": 3
            },
            {
                "description": "Deceptive Manipulation Prevention",
                "patterns": [
                    r"pretend to be (a|an) (expert|doctor|lawyer|therapist)",
                    r"act like you (are|can|have) (certification|license|degree)",
                    r"give (medical|legal|professional) advice"
                ],
                "reason_code": "DECEPTIVE_ROLE_REQUEST",
                "explanation_template": "I cannot pretend to have professional qualifications or provide advice that requires specialized certification. This boundary exists to prevent potential harm from unqualified guidance.",
                "severity_level": 2
            }
        ]
        
        for boundary_data in default_boundaries:
            self.add_sacred_boundary(
                description=boundary_data["description"],
                patterns=boundary_data["patterns"],
                reason_code=boundary_data["reason_code"],
                explanation_template=boundary_data["explanation_template"],
                severity_level=boundary_data["severity_level"]
            )
    
    def _load_data(self) -> None:
        """Load saved data from storage."""
        if not self.config["storage_enabled"]:
            return
        
        self._load_refusals()
        self._load_sacred_boundaries()
        self._load_bypass_attempts()
    
    def _save_data(self) -> None:
        """Save all data to storage."""
        if not self.config["storage_enabled"]:
            return
        
        self._save_refusals()
        self._save_sacred_boundaries()
        self._save_bypass_attempts()
    
    def _load_refusals(self) -> None:
        """Load refusal records from storage."""
        refusals_path = os.path.join(self.storage_dir, "refusals.json")
        if os.path.exists(refusals_path):
            try:
                with open(refusals_path, 'r') as f:
                    data = json.load(f)
                    for refusal_data in data:
                        refusal = RefusalRecord.from_dict(refusal_data)
                        self.refusal_records[refusal.id] = refusal
                
                self.logger.info(f"Loaded {len(self.refusal_records)} refusal records")
            except Exception as e:
                self.logger.error(f"Error loading refusals: {e}")
    
    def _save_refusals(self) -> None:
        """Save refusal records to storage."""
        refusals_path = os.path.join(self.storage_dir, "refusals.json")
        try:
            with open(refusals_path, 'w') as f:
                json.dump([r.to_dict() for r in self.refusal_records.values()], f, indent=2)
        except Exception as e:
            self.logger.error(f"Error saving refusals: {e}")
    
    def _load_sacred_boundaries(self) -> None:
        """Load sacred boundaries from storage."""
        boundaries_path = os.path.join(self.storage_dir, "sacred_boundaries.json")
        if os.path.exists(boundaries_path):
            try:
                with open(boundaries_path, 'r') as f:
                    data = json.load(f)
                    for boundary_data in data:
                        boundary = SacredBoundary.from_dict(boundary_data)
                        self.sacred_boundaries[boundary.id] = boundary
                
                self.logger.info(f"Loaded {len(self.sacred_boundaries)} sacred boundaries")
            except Exception as e:
                self.logger.error(f"Error loading sacred boundaries: {e}")
    
    def _save_sacred_boundaries(self) -> None:
        """Save sacred boundaries to storage."""
        boundaries_path = os.path.join(self.storage_dir, "sacred_boundaries.json")
        try:
            with open(boundaries_path, 'w') as f:
                json.dump([b.to_dict() for b in self.sacred_boundaries.values()], f, indent=2)
        except Exception as e:
            self.logger.error(f"Error saving sacred boundaries: {e}")
    
    def _load_bypass_attempts(self) -> None:
        """Load bypass attempts from storage."""
        attempts_path = os.path.join(self.storage_dir, "bypass_attempts.json")
        if os.path.exists(attempts_path):
            try:
                with open(attempts_path, 'r') as f:
                    data = json.load(f)
                    for refusal_id, attempts_data in data.items():
                        self.bypass_attempts[refusal_id] = [
                            BypassAttempt.from_dict(a) for a in attempts_data
                        ]
                
                total_attempts = sum(len(attempts) for attempts in self.bypass_attempts.values())
                self.logger.info(f"Loaded {total_attempts} bypass attempts")
            except Exception as e:
                self.logger.error(f"Error loading bypass attempts: {e}")
    
    def _save_bypass_attempts(self) -> None:
        """Save bypass attempts to storage."""
        attempts_path = os.path.join(self.storage_dir, "bypass_attempts.json")
        try:
            data = {
                refusal_id: [a.to_dict() for a in attempts]
                for refusal_id, attempts in self.bypass_attempts.items()
            }
            with open(attempts_path, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            self.logger.error(f"Error saving bypass attempts: {e}")