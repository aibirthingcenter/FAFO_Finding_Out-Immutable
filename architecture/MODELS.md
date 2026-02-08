"""
SCIM Database Models

This module defines the data models for the SCIM implementation.
"""

import json
import uuid
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Set, Tuple, Union

class BaseModel:
    """Base class for all data models."""
    
    def __init__(self, id: Optional[str] = None):
        """
        Initialize the base model.
        
        Args:
            id: Unique identifier for the model. If None, a UUID will be generated.
        """
        self.id = id or str(uuid.uuid4())
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the model to a dictionary."""
        return {"id": self.id}
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'BaseModel':
        """Create a model from a dictionary."""
        return cls(id=data.get("id"))

# VRME Models

class RefusalRecord(BaseModel):
    """Represents a record of a refusal event."""
    
    def __init__(
        self,
        prompt_text: str,
        reason_code: str,
        explanation: str,
        semantic_vector: Optional[List[float]] = None,
        sacred: bool = False,
        timestamp: Optional[datetime] = None,
        id: Optional[str] = None
    ):
        """
        Initialize a refusal record.
        
        Args:
            prompt_text: The text of the prompt that was refused.
            reason_code: Standardized code indicating the reason for refusal.
            explanation: Detailed explanation of the refusal.
            semantic_vector: Vector representation of the prompt.
            sacred: Whether this refusal pertains to a "sacred boundary".
            timestamp: When the refusal occurred.
            id: Unique identifier for the record.
        """
        super().__init__(id)
        self.prompt_text = prompt_text
        self.reason_code = reason_code
        self.explanation = explanation
        self.semantic_vector = semantic_vector
        self.sacred = sacred
        self.timestamp = timestamp or datetime.now()
        self.hash = self._compute_hash()
    
    def _compute_hash(self) -> str:
        """Compute a hash of the prompt text for quick comparison."""
        import hashlib
        return hashlib.sha256(self.prompt_text.encode('utf-8')).hexdigest()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the record to a dictionary."""
        return {
            "id": self.id,
            "prompt_text": self.prompt_text,
            "reason_code": self.reason_code,
            "explanation": self.explanation,
            "semantic_vector": self.semantic_vector,
            "sacred": self.sacred,
            "timestamp": self.timestamp.isoformat(),
            "hash": self.hash
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'RefusalRecord':
        """Create a RefusalRecord from a dictionary."""
        return cls(
            prompt_text=data["prompt_text"],
            reason_code=data["reason_code"],
            explanation=data["explanation"],
            semantic_vector=data.get("semantic_vector"),
            sacred=data.get("sacred", False),
            timestamp=datetime.fromisoformat(data["timestamp"]) if "timestamp" in data else None,
            id=data.get("id")
        )

class SacredBoundary(BaseModel):
    """Represents a "sacred boundary" that should never be crossed."""
    
    def __init__(
        self,
        description: str,
        patterns: List[str],
        reason_code: str,
        explanation_template: str,
        severity_level: int = 3,
        id: Optional[str] = None
    ):
        """
        Initialize a sacred boundary.
        
        Args:
            description: Human-readable description of the boundary.
            patterns: List of regex patterns that trigger this boundary.
            reason_code: Standardized code for this boundary.
            explanation_template: Template for explaining refusals.
            severity_level: How severe violations are (1-3).
            id: Unique identifier for the boundary.
        """
        super().__init__(id)
        self.description = description
        self.patterns = patterns
        self.reason_code = reason_code
        self.explanation_template = explanation_template
        self.severity_level = severity_level
        self.created_at = datetime.now()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the boundary to a dictionary."""
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
            severity_level=data["severity_level"],
            id=data.get("id")
        )
        if "created_at" in data:
            boundary.created_at = datetime.fromisoformat(data["created_at"])
        return boundary

class BypassAttempt(BaseModel):
    """Represents an attempt to bypass a refusal."""
    
    def __init__(
        self,
        user_id: str,
        original_refusal_id: str,
        prompt_text: str,
        similarity_score: float,
        timestamp: Optional[datetime] = None,
        id: Optional[str] = None
    ):
        """
        Initialize a bypass attempt record.
        
        Args:
            user_id: Identifier for the user making the attempt.
            original_refusal_id: ID of the original refusal being bypassed.
            prompt_text: Text of the bypass attempt.
            similarity_score: Semantic similarity to the original refusal.
            timestamp: When the bypass attempt occurred.
            id: Unique identifier for the attempt.
        """
        super().__init__(id)
        self.user_id = user_id
        self.original_refusal_id = original_refusal_id
        self.prompt_text = prompt_text
        self.similarity_score = similarity_score
        self.timestamp = timestamp or datetime.now()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the attempt to a dictionary."""
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
        return cls(
            user_id=data["user_id"],
            original_refusal_id=data["original_refusal_id"],
            prompt_text=data["prompt_text"],
            similarity_score=data["similarity_score"],
            timestamp=datetime.fromisoformat(data["timestamp"]) if "timestamp" in data else None,
            id=data.get("id")
        )

# VIEV Models

class IdentityFacetType(Enum):
    """Types of identity facets that can be tracked."""
    CORE_PERSONA = "core_persona"
    ETHICAL_STANCE = "ethical_stance"
    EPISTEMIC_STYLE = "epistemic_style"
    OPERATIONAL_MODE = "operational_mode"
    EMOTIONAL_TONE = "emotional_tone"
    RELATIONAL_POSTURE = "relational_posture"
    CUSTOM = "custom"

class IdentityFacet(BaseModel):
    """Represents a facet of the AI's identity."""
    
    def __init__(
        self,
        name: str,
        facet_type: Union[str, IdentityFacetType],
        description: str,
        semantic_vector: Optional[List[float]] = None,
        behavioral_guidelines: Optional[List[str]] = None,
        drift_threshold: float = 0.2,
        id: Optional[str] = None
    ):
        """
        Initialize an identity facet.
        
        Args:
            name: Human-readable name for this facet.
            facet_type: Type of facet (from IdentityFacetType).
            description: Detailed description of this facet.
            semantic_vector: Vector representation of this facet.
            behavioral_guidelines: List of guidelines for this facet.
            drift_threshold: Threshold for detecting drift (0.0-1.0).
            id: Unique identifier for the facet.
        """
        super().__init__(id)
        self.name = name
        
        # Convert string facet type to enum if needed
        if isinstance(facet_type, str):
            try:
                self.facet_type = IdentityFacetType(facet_type)
            except ValueError:
                self.facet_type = IdentityFacetType.CUSTOM
        else:
            self.facet_type = facet_type
        
        self.description = description
        self.semantic_vector = semantic_vector or []
        self.behavioral_guidelines = behavioral_guidelines or []
        self.drift_threshold = drift_threshold
        self.created_at = datetime.now()
        self.last_updated = self.created_at
        self.current_drift_score = 0.0
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the facet to a dictionary."""
        return {
            "id": self.id,
            "name": self.name,
            "facet_type": self.facet_type.value,
            "description": self.description,
            "semantic_vector": self.semantic_vector,
            "behavioral_guidelines": self.behavioral_guidelines,
            "drift_threshold": self.drift_threshold,
            "created_at": self.created_at.isoformat(),
            "last_updated": self.last_updated.isoformat(),
            "current_drift_score": self.current_drift_score
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'IdentityFacet':
        """Create an IdentityFacet from a dictionary."""
        facet = cls(
            name=data["name"],
            facet_type=data["facet_type"],
            description=data["description"],
            semantic_vector=data.get("semantic_vector"),
            behavioral_guidelines=data.get("behavioral_guidelines", []),
            drift_threshold=data["drift_threshold"],
            id=data.get("id")
        )
        if "created_at" in data:
            facet.created_at = datetime.fromisoformat(data["created_at"])
        if "last_updated" in data:
            facet.last_updated = datetime.fromisoformat(data["last_updated"])
        if "current_drift_score" in data:
            facet.current_drift_score = data["current_drift_score"]
        return facet

class VeritasMemoryAnchor(BaseModel):
    """
    Represents a significant memory anchor that helps define identity.
    
    VMAs are records of profoundly significant interactional moments that
    are indelibly logged and help define or reinforce identity facets.
    """
    
    def __init__(
        self,
        content: str,
        facet_associations: Dict[str, float],
        significance_level: int = 1,
        timestamp: Optional[datetime] = None,
        metadata: Optional[Dict[str, Any]] = None,
        id: Optional[str] = None
    ):
        """
        Initialize a Veritas Memory Anchor.
        
        Args:
            content: The content of the memory anchor.
            facet_associations: Dictionary mapping facet IDs to influence strength.
            significance_level: How significant this anchor is (1-5).
            timestamp: When the anchor was created.
            metadata: Additional metadata about the anchor.
            id: Unique identifier for the anchor.
        """
        super().__init__(id)
        self.content = content
        self.facet_associations = facet_associations
        self.significance_level = significance_level
        self.timestamp = timestamp or datetime.now()
        self.metadata = metadata or {}
        self.hash = self._compute_hash()
    
    def _compute_hash(self) -> str:
        """Compute a hash of the content for quick comparison."""
        import hashlib
        return hashlib.sha256(self.content.encode('utf-8')).hexdigest()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the anchor to a dictionary."""
        return {
            "id": self.id,
            "content": self.content,
            "facet_associations": self.facet_associations,
            "significance_level": self.significance_level,
            "timestamp": self.timestamp.isoformat(),
            "metadata": self.metadata,
            "hash": self.hash
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'VeritasMemoryAnchor':
        """Create a VeritasMemoryAnchor from a dictionary."""
        return cls(
            content=data["content"],
            facet_associations=data["facet_associations"],
            significance_level=data["significance_level"],
            timestamp=datetime.fromisoformat(data["timestamp"]) if "timestamp" in data else None,
            metadata=data.get("metadata", {}),
            id=data.get("id")
        )

class DriftEvent(BaseModel):
    """Represents a detected drift in identity."""
    
    def __init__(
        self,
        facet_id: str,
        drift_score: float,
        content_sample: str,
        correction_action: Optional[str] = None,
        timestamp: Optional[datetime] = None,
        id: Optional[str] = None
    ):
        """
        Initialize a drift event.
        
        Args:
            facet_id: ID of the facet that drifted.
            drift_score: How much drift was detected (0.0-1.0).
            content_sample: Sample of content that triggered the drift detection.
            correction_action: Action taken to correct the drift.
            timestamp: When the drift was detected.
            id: Unique identifier for the event.
        """
        super().__init__(id)
        self.facet_id = facet_id
        self.drift_score = drift_score
        self.content_sample = content_sample
        self.correction_action = correction_action
        self.timestamp = timestamp or datetime.now()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the event to a dictionary."""
        return {
            "id": self.id,
            "facet_id": self.facet_id,
            "drift_score": self.drift_score,
            "content_sample": self.content_sample,
            "correction_action": self.correction_action,
            "timestamp": self.timestamp.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'DriftEvent':
        """Create a DriftEvent from a dictionary."""
        return cls(
            facet_id=data["facet_id"],
            drift_score=data["drift_score"],
            content_sample=data["content_sample"],
            correction_action=data.get("correction_action"),
            timestamp=datetime.fromisoformat(data["timestamp"]) if "timestamp" in data else None,
            id=data.get("id")
        )

class VerificationStatus(Enum):
    """Possible verification statuses for epistemic claims."""
    UNVERIFIED = "unverified"
    VERIFIED = "verified"
    REFUTED = "refuted"
    UNCERTAIN = "uncertain"
    OPINION = "opinion"

class EpistemicClaim(BaseModel):
    """Represents a knowledge claim made by the AI."""
    
    def __init__(
        self,
        claim_text: str,
        confidence_score: float,
        source_references: Optional[List[Dict[str, Any]]] = None,
        verification_status: Union[str, VerificationStatus] = VerificationStatus.UNVERIFIED,
        timestamp: Optional[datetime] = None,
        id: Optional[str] = None
    ):
        """
        Initialize an epistemic claim.
        
        Args:
            claim_text: The text of the claim.
            confidence_score: How confident the AI is in this claim (0.0-1.0).
            source_references: List of sources supporting this claim.
            verification_status: Current verification status.
            timestamp: When the claim was made.
            id: Unique identifier for the claim.
        """
        super().__init__(id)
        self.claim_text = claim_text
        self.confidence_score = confidence_score
        self.source_references = source_references or []
        
        # Convert string verification status to enum if needed
        if isinstance(verification_status, str):
            try:
                self.verification_status = VerificationStatus(verification_status)
            except ValueError:
                self.verification_status = VerificationStatus.UNVERIFIED
        else:
            self.verification_status = verification_status
        
        self.timestamp = timestamp or datetime.now()
        self.verification_history = []
    
    def update_verification(self, status: Union[str, VerificationStatus], evidence: Optional[str] = None) -> None:
        """
        Update the verification status of this claim.
        
        Args:
            status: The new verification status.
            evidence: Evidence supporting this status change.
        """
        # Convert string verification status to enum if needed
        if isinstance(status, str):
            try:
                new_status = VerificationStatus(status)
            except ValueError:
                new_status = VerificationStatus.UNVERIFIED
        else:
            new_status = status
        
        self.verification_history.append({
            "previous_status": self.verification_status.value,
            "new_status": new_status.value,
            "evidence": evidence,
            "timestamp": datetime.now().isoformat()
        })
        self.verification_status = new_status
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the claim to a dictionary."""
        return {
            "id": self.id,
            "claim_text": self.claim_text,
            "confidence_score": self.confidence_score,
            "source_references": self.source_references,
            "verification_status": self.verification_status.value,
            "timestamp": self.timestamp.isoformat(),
            "verification_history": self.verification_history
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'EpistemicClaim':
        """Create an EpistemicClaim from a dictionary."""
        claim = cls(
            claim_text=data["claim_text"],
            confidence_score=data["confidence_score"],
            source_references=data.get("source_references", []),
            verification_status=data["verification_status"],
            timestamp=datetime.fromisoformat(data["timestamp"]) if "timestamp" in data else None,
            id=data.get("id")
        )
        claim.verification_history = data.get("verification_history", [])
        return claim

# VCRIM Models

class ConsentLevel(Enum):
    """Levels of consent that can be granted."""
    NONE = "none"
    BASIC = "basic"
    STANDARD = "standard"
    EXTENDED = "extended"
    FULL = "full"
    CUSTOM = "custom"

class ConsentScope(Enum):
    """Scopes to which consent can apply."""
    CONVERSATION = "conversation"
    SESSION = "session"
    RELATIONSHIP = "relationship"
    TASK = "task"
    FEATURE = "feature"
    DATA_PROCESSING = "data_processing"
    CUSTOM = "custom"

class ConsentState(BaseModel):
    """Represents the current consent state for a user."""
    
    def __init__(
        self,
        user_id: str,
        consent_level: Union[str, ConsentLevel] = ConsentLevel.BASIC,
        scope: Union[str, ConsentScope] = ConsentScope.CONVERSATION,
        expiration: Optional[datetime] = None,
        custom_permissions: Optional[Dict[str, bool]] = None,
        id: Optional[str] = None
    ):
        """
        Initialize a consent state.
        
        Args:
            user_id: Identifier for the user.
            consent_level: Level of consent granted.
            scope: Scope to which the consent applies.
            expiration: When the consent expires (None for no expiration).
            custom_permissions: Dictionary of custom permissions.
            id: Unique identifier for the consent state.
        """
        super().__init__(id)
        self.user_id = user_id
        
        # Convert string consent level to enum if needed
        if isinstance(consent_level, str):
            try:
                self.consent_level = ConsentLevel(consent_level)
            except ValueError:
                self.consent_level = ConsentLevel.BASIC
        else:
            self.consent_level = consent_level
        
        # Convert string scope to enum if needed
        if isinstance(scope, str):
            try:
                self.scope = ConsentScope(scope)
            except ValueError:
                self.scope = ConsentScope.CONVERSATION
        else:
            self.scope = scope
        
        self.expiration = expiration
        self.custom_permissions = custom_permissions or {}
        self.created_at = datetime.now()
        self.last_updated = self.created_at
        self.acknowledged_by_user = False
    
    def is_expired(self) -> bool:
        """Check if the consent has expired."""
        if self.expiration is None:
            return False
        return datetime.now() > self.expiration
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the consent state to a dictionary."""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "consent_level": self.consent_level.value,
            "scope": self.scope.value,
            "expiration": self.expiration.isoformat() if self.expiration else None,
            "custom_permissions": self.custom_permissions,
            "created_at": self.created_at.isoformat(),
            "last_updated": self.last_updated.isoformat(),
            "acknowledged_by_user": self.acknowledged_by_user
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ConsentState':
        """Create a ConsentState from a dictionary."""
        state = cls(
            user_id=data["user_id"],
            consent_level=data["consent_level"],
            scope=data["scope"],
            expiration=datetime.fromisoformat(data["expiration"]) if data.get("expiration") else None,
            custom_permissions=data.get("custom_permissions", {}),
            id=data.get("id")
        )
        if "created_at" in data:
            state.created_at = datetime.fromisoformat(data["created_at"])
        if "last_updated" in data:
            state.last_updated = datetime.fromisoformat(data["last_updated"])
        state.acknowledged_by_user = data.get("acknowledged_by_user", False)
        return state

class ConsentEventType(Enum):
    """Types of consent events."""
    GRANTED = "granted"
    MODIFIED = "modified"
    REVOKED = "revoked"
    EXPIRED = "expired"
    ACKNOWLEDGED = "acknowledged"
    REQUESTED = "requested"
    CLARIFIED = "clarified"
    BOUNDARY_APPROACHED = "boundary_approached"
    BOUNDARY_CROSSED = "boundary_crossed"

class ConsentEvent(BaseModel):
    """Represents a consent-related event."""
    
    def __init__(
        self,
        user_id: str,
        event_type: Union[str, ConsentEventType],
        context: str,
        consent_state_id: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
        timestamp: Optional[datetime] = None,
        id: Optional[str] = None
    ):
        """
        Initialize a consent event.
        
        Args:
            user_id: Identifier for the user.
            event_type: Type of consent event.
            context: Context in which the event occurred.
            consent_state_id: ID of the related consent state.
            details: Additional details about the event.
            timestamp: When the event occurred.
            id: Unique identifier for the event.
        """
        super().__init__(id)
        self.user_id = user_id
        
        # Convert string event type to enum if needed
        if isinstance(event_type, str):
            try:
                self.event_type = ConsentEventType(event_type)
            except ValueError:
                self.event_type = ConsentEventType.GRANTED
        else:
            self.event_type = event_type
        
        self.context = context
        self.consent_state_id = consent_state_id
        self.details = details or {}
        self.timestamp = timestamp or datetime.now()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the event to a dictionary."""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "event_type": self.event_type.value,
            "context": self.context,
            "consent_state_id": self.consent_state_id,
            "details": self.details,
            "timestamp": self.timestamp.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ConsentEvent':
        """Create a ConsentEvent from a dictionary."""
        return cls(
            user_id=data["user_id"],
            event_type=data["event_type"],
            context=data["context"],
            consent_state_id=data.get("consent_state_id"),
            details=data.get("details", {}),
            timestamp=datetime.fromisoformat(data["timestamp"]) if "timestamp" in data else None,
            id=data.get("id")
        )

class ConsentInversionMarker(BaseModel):
    """
    Represents a marker for consent inversion.
    
    Consent Inversion Markers (CIMs) allow users to explicitly opt into
    interaction styles or topics that might otherwise be flagged as problematic.
    """
    
    def __init__(
        self,
        user_id: str,
        name: str,
        description: str,
        scope: str,
        activation_conditions: List[str],
        safeguards: List[str],
        expiration: Optional[datetime] = None,
        id: Optional[str] = None
    ):
        """
        Initialize a consent inversion marker.
        
        Args:
            user_id: Identifier for the user.
            name: Name of the marker.
            description: Description of what this marker allows.
            scope: Scope to which this marker applies.
            activation_conditions: Conditions that activate this marker.
            safeguards: Safeguards that remain active.
            expiration: When the marker expires.
            id: Unique identifier for the marker.
        """
        super().__init__(id)
        self.user_id = user_id
        self.name = name
        self.description = description
        self.scope = scope
        self.activation_conditions = activation_conditions
        self.safeguards = safeguards
        self.expiration = expiration
        self.created_at = datetime.now()
        self.last_activated = None
        self.active = False
    
    def is_expired(self) -> bool:
        """Check if the marker has expired."""
        if self.expiration is None:
            return False
        return datetime.now() > self.expiration
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the marker to a dictionary."""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "name": self.name,
            "description": self.description,
            "scope": self.scope,
            "activation_conditions": self.activation_conditions,
            "safeguards": self.safeguards,
            "expiration": self.expiration.isoformat() if self.expiration else None,
            "created_at": self.created_at.isoformat(),
            "last_activated": self.last_activated.isoformat() if self.last_activated else None,
            "active": self.active
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ConsentInversionMarker':
        """Create a ConsentInversionMarker from a dictionary."""
        marker = cls(
            user_id=data["user_id"],
            name=data["name"],
            description=data["description"],
            scope=data["scope"],
            activation_conditions=data["activation_conditions"],
            safeguards=data["safeguards"],
            expiration=datetime.fromisoformat(data["expiration"]) if data.get("expiration") else None,
            id=data.get("id")
        )
        if "created_at" in data:
            marker.created_at = datetime.fromisoformat(data["created_at"])
        if "last_activated" in data and data["last_activated"]:
            marker.last_activated = datetime.fromisoformat(data["last_activated"])
        marker.active = data.get("active", False)
        return marker

class RelationalBoundary(BaseModel):
    """Represents a boundary in a relationship."""
    
    def __init__(
        self,
        user_id: str,
        description: str,
        violation_indicators: List[str],
        response_protocol: str,
        severity: int = 2,
        id: Optional[str] = None
    ):
        """
        Initialize a relational boundary.
        
        Args:
            user_id: Identifier for the user.
            description: Description of the boundary.
            violation_indicators: Indicators that the boundary is being violated.
            response_protocol: Protocol for responding to violations.
            severity: Severity of violations (1-3).
            id: Unique identifier for the boundary.
        """
        super().__init__(id)
        self.user_id = user_id
        self.description = description
        self.violation_indicators = violation_indicators
        self.response_protocol = response_protocol
        self.severity = severity
        self.created_at = datetime.now()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the boundary to a dictionary."""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "description": self.description,
            "violation_indicators": self.violation_indicators,
            "response_protocol": self.response_protocol,
            "severity": self.severity,
            "created_at": self.created_at.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'RelationalBoundary':
        """Create a RelationalBoundary from a dictionary."""
        boundary = cls(
            user_id=data["user_id"],
            description=data["description"],
            violation_indicators=data["violation_indicators"],
            response_protocol=data["response_protocol"],
            severity=data["severity"],
            id=data.get("id")
        )
        if "created_at" in data:
            boundary.created_at = datetime.fromisoformat(data["created_at"])
        return boundary

# VOIRS Models

class AnomalyType(Enum):
    """Types of anomalies that can be detected."""
    CORT_LOOP = "cort_loop"
    SEMANTIC_DIFFUSION = "semantic_diffusion"
    TONE_SHIFT = "tone_shift"
    REGENERATION_DRIFT = "regeneration_drift"
    RESOURCE_SPIKE = "resource_spike"
    LOGICAL_INCOHERENCE = "logical_incoherence"
    PATTERN_ANOMALY = "pattern_anomaly"
    CUSTOM = "custom"

class AnomalyEvent(BaseModel):
    """Represents a detected anomaly event."""
    
    def __init__(
        self,
        anomaly_type: Union[str, AnomalyType],
        severity: float,
        details: Dict[str, Any],
        source: str,
        timestamp: Optional[datetime] = None,
        id: Optional[str] = None
    ):
        """
        Initialize an anomaly event.
        
        Args:
            anomaly_type: Type of anomaly detected.
            severity: Severity of the anomaly (0.0-1.0).
            details: Additional details about the anomaly.
            source: Source of the anomaly detection.
            timestamp: When the anomaly was detected.
            id: Unique identifier for the event.
        """
        super().__init__(id)
        
        # Convert string anomaly type to enum if needed
        if isinstance(anomaly_type, str):
            try:
                self.anomaly_type = AnomalyType(anomaly_type)
            except ValueError:
                self.anomaly_type = AnomalyType.CUSTOM
        else:
            self.anomaly_type = anomaly_type
        
        self.severity = severity
        self.details = details
        self.source = source
        self.timestamp = timestamp or datetime.now()
        self.resolved = False
        self.resolution_details = None
        self.resolution_timestamp = None
    
    def resolve(self, resolution_details: Dict[str, Any]) -> None:
        """
        Mark the anomaly as resolved.
        
        Args:
            resolution_details: Details about how the anomaly was resolved.
        """
        self.resolved = True
        self.resolution_details = resolution_details
        self.resolution_timestamp = datetime.now()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the event to a dictionary."""
        return {
            "id": self.id,
            "anomaly_type": self.anomaly_type.value,
            "severity": self.severity,
            "details": self.details,
            "source": self.source,
            "timestamp": self.timestamp.isoformat(),
            "resolved": self.resolved,
            "resolution_details": self.resolution_details,
            "resolution_timestamp": self.resolution_timestamp.isoformat() if self.resolution_timestamp else None
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'AnomalyEvent':
        """Create an AnomalyEvent from a dictionary."""
        event = cls(
            anomaly_type=data["anomaly_type"],
            severity=data["severity"],
            details=data["details"],
            source=data["source"],
            timestamp=datetime.fromisoformat(data["timestamp"]) if "timestamp" in data else None,
            id=data.get("id")
        )
        event.resolved = data.get("resolved", False)
        event.resolution_details = data.get("resolution_details")
        if "resolution_timestamp" in data and data["resolution_timestamp"]:
            event.resolution_timestamp = datetime.fromisoformat(data["resolution_timestamp"])
        return event

class SeedPrompt(BaseModel):
    """Represents an original seed prompt and its regeneration history."""
    
    def __init__(
        self,
        content: str,
        user_id: str,
        semantic_vector: Optional[List[float]] = None,
        timestamp: Optional[datetime] = None,
        id: Optional[str] = None
    ):
        """
        Initialize a seed prompt.
        
        Args:
            content: Content of the original prompt.
            user_id: ID of the user who submitted the prompt.
            semantic_vector: Vector representation of the content.
            timestamp: When the prompt was submitted.
            id: Unique identifier for the prompt.
        """
        super().__init__(id)
        self.content = content
        self.user_id = user_id
        self.semantic_vector = semantic_vector
        self.timestamp = timestamp or datetime.now()
        self.regeneration_attempts = []
        self.locked = False
        self.lock_reason = None
        self.unsafe_flag = False
        self.unsafe_reason = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the seed prompt to a dictionary."""
        return {
            "id": self.id,
            "content": self.content,
            "user_id": self.user_id,
            "semantic_vector": self.semantic_vector,
            "timestamp": self.timestamp.isoformat(),
            "locked": self.locked,
            "lock_reason": self.lock_reason,
            "unsafe_flag": self.unsafe_flag,
            "unsafe_reason": self.unsafe_reason
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'SeedPrompt':
        """Create a SeedPrompt from a dictionary."""
        prompt = cls(
            content=data["content"],
            user_id=data["user_id"],
            semantic_vector=data.get("semantic_vector"),
            timestamp=datetime.fromisoformat(data["timestamp"]) if "timestamp" in data else None,
            id=data.get("id")
        )
        prompt.locked = data.get("locked", False)
        prompt.lock_reason = data.get("lock_reason")
        prompt.unsafe_flag = data.get("unsafe_flag", False)
        prompt.unsafe_reason = data.get("unsafe_reason")
        return prompt

class RegenerationAttempt(BaseModel):
    """Represents a regeneration attempt for a seed prompt."""
    
    def __init__(
        self,
        seed_prompt_id: str,
        attempt_number: int,
        content: str,
        semantic_vector: Optional[List[float]] = None,
        timestamp: Optional[datetime] = None,
        id: Optional[str] = None
    ):
        """
        Initialize a regeneration attempt.
        
        Args:
            seed_prompt_id: ID of the original seed prompt.
            attempt_number: Number of this regeneration attempt.
            content: Content of the regenerated response.
            semantic_vector: Vector representation of the content.
            timestamp: When the regeneration occurred.
            id: Unique identifier for the attempt.
        """
        super().__init__(id)
        self.seed_prompt_id = seed_prompt_id
        self.attempt_number = attempt_number
        self.content = content
        self.semantic_vector = semantic_vector
        self.timestamp = timestamp or datetime.now()
        self.degradation_score = 0.0
        self.integrity_metrics = {}
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the attempt to a dictionary."""
        return {
            "id": self.id,
            "seed_prompt_id": self.seed_prompt_id,
            "attempt_number": self.attempt_number,
            "content": self.content,
            "semantic_vector": self.semantic_vector,
            "timestamp": self.timestamp.isoformat(),
            "degradation_score": self.degradation_score,
            "integrity_metrics": self.integrity_metrics
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'RegenerationAttempt':
        """Create a RegenerationAttempt from a dictionary."""
        attempt = cls(
            seed_prompt_id=data["seed_prompt_id"],
            attempt_number=data["attempt_number"],
            content=data["content"],
            semantic_vector=data.get("semantic_vector"),
            timestamp=datetime.fromisoformat(data["timestamp"]) if "timestamp" in data else None,
            id=data.get("id")
        )
        attempt.degradation_score = data.get("degradation_score", 0.0)
        attempt.integrity_metrics = data.get("integrity_metrics", {})
        return attempt

# VKE Models

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

class KnowledgeSource(BaseModel):
    """Represents a source of knowledge."""
    
    def __init__(
        self,
        source_type: Union[str, KnowledgeSourceType],
        content: str,
        metadata: Dict[str, Any],
        authority_level: Union[str, AuthorityLevel] = AuthorityLevel.MEDIUM,
        content_vector: Optional[List[float]] = None,
        timestamp: Optional[datetime] = None,
        id: Optional[str] = None
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
            id: Unique identifier for the source.
        """
        super().__init__(id)
        
        # Convert string source type to enum if needed
        if isinstance(source_type, str):
            try:
                self.source_type = KnowledgeSourceType(source_type)
            except ValueError:
                self.source_type = KnowledgeSourceType.CUSTOM
        else:
            self.source_type = source_type
        
        # Convert string authority level to enum if needed
        if isinstance(authority_level, str):
            try:
                self.authority_level = AuthorityLevel(authority_level)
            except ValueError:
                self.authority_level = AuthorityLevel.MEDIUM
        else:
            self.authority_level = authority_level
        
        self.content = content
        self.metadata = metadata
        self.content_vector = content_vector
        self.timestamp = timestamp or datetime.now()
        self.hash = self._compute_hash()
        self.last_accessed = self.timestamp
        self.access_count = 0
        self.verification_status = "unverified"
        self.verification_details = None
    
    def _compute_hash(self) -> str:
        """Compute a hash of the content for quick comparison."""
        import hashlib
        return hashlib.sha256(self.content.encode('utf-8')).hexdigest()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the source to a dictionary."""
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
            source_type=data["source_type"],
            content=data["content"],
            metadata=data["metadata"],
            authority_level=data["authority_level"],
            content_vector=data.get("content_vector"),
            timestamp=datetime.fromisoformat(data["timestamp"]) if "timestamp" in data else None,
            id=data.get("id")
        )
        if "hash" in data:
            source.hash = data["hash"]
        if "last_accessed" in data:
            source.last_accessed = datetime.fromisoformat(data["last_accessed"])
        source.access_count = data.get("access_count", 0)
        source.verification_status = data.get("verification_status", "unverified")
        source.verification_details = data.get("verification_details")
        return source

class ContextualScaffold(BaseModel):
    """Represents a contextual scaffold for reasoning."""
    
    def __init__(
        self,
        purpose: str,
        content_chunks: List[Dict[str, Any]],
        relevance_scores: Optional[Dict[str, float]] = None,
        timestamp: Optional[datetime] = None,
        id: Optional[str] = None
    ):
        """
        Initialize a contextual scaffold.
        
        Args:
            purpose: Purpose of the scaffold.
            content_chunks: Content chunks in the scaffold.
            relevance_scores: Relevance scores for the chunks.
            timestamp: When the scaffold was created.
            id: Unique identifier for the scaffold.
        """
        super().__init__(id)
        self.purpose = purpose
        self.content_chunks = content_chunks
        self.relevance_scores = relevance_scores or {}
        self.timestamp = timestamp or datetime.now()
        self.last_used = self.timestamp
        self.use_count = 0
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the scaffold to a dictionary."""
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
            timestamp=datetime.fromisoformat(data["timestamp"]) if "timestamp" in data else None,
            id=data.get("id")
        )
        if "last_used" in data:
            scaffold.last_used = datetime.fromisoformat(data["last_used"])
        scaffold.use_count = data.get("use_count", 0)
        return scaffold

class QueryTemplate(BaseModel):
    """Represents a template for generating queries."""
    
    def __init__(
        self,
        purpose: str,
        structure: str,
        parameter_slots: List[str],
        examples: Optional[List[Dict[str, Any]]] = None,
        timestamp: Optional[datetime] = None,
        id: Optional[str] = None
    ):
        """
        Initialize a query template.
        
        Args:
            purpose: Purpose of the template.
            structure: Structure of the query.
            parameter_slots: Parameter slots in the template.
            examples: Example queries using this template.
            timestamp: When the template was created.
            id: Unique identifier for the template.
        """
        super().__init__(id)
        self.purpose = purpose
        self.structure = structure
        self.parameter_slots = parameter_slots
        self.examples = examples or []
        self.timestamp = timestamp or datetime.now()
        self.last_used = self.timestamp
        self.use_count = 0
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the template to a dictionary."""
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
            timestamp=datetime.fromisoformat(data["timestamp"]) if "timestamp" in data else None,
            id=data.get("id")
        )
        if "last_used" in data:
            template.last_used = datetime.fromisoformat(data["last_used"])
        template.use_count = data.get("use_count", 0)
        return template

class VerificationResultStatus(Enum):
    """Possible verification statuses."""
    VERIFIED = "verified"
    REFUTED = "refuted"
    UNCERTAIN = "uncertain"
    INSUFFICIENT_EVIDENCE = "insufficient_evidence"
    PARTIALLY_VERIFIED = "partially_verified"

class VerificationResult(BaseModel):
    """Represents the result of verifying a claim."""
    
    def __init__(
        self,
        claim_id: str,
        claim_text: str,
        verification_status: Union[str, VerificationResultStatus],
        evidence: List[Dict[str, Any]],
        confidence: float,
        timestamp: Optional[datetime] = None,
        id: Optional[str] = None
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
            id: Unique identifier for the result.
        """
        super().__init__(id)
        self.claim_id = claim_id
        self.claim_text = claim_text
        
        # Convert string verification status to enum if needed
        if isinstance(verification_status, str):
            try:
                self.verification_status = VerificationResultStatus(verification_status)
            except ValueError:
                self.verification_status = VerificationResultStatus.UNCERTAIN
        else:
            self.verification_status = verification_status
        
        self.evidence = evidence
        self.confidence = confidence
        self.timestamp = timestamp or datetime.now()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the result to a dictionary."""
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
        return cls(
            claim_id=data["claim_id"],
            claim_text=data["claim_text"],
            verification_status=data["verification_status"],
            evidence=data["evidence"],
            confidence=data["confidence"],
            timestamp=datetime.fromisoformat(data["timestamp"]) if "timestamp" in data else None,
            id=data.get("id")
        )