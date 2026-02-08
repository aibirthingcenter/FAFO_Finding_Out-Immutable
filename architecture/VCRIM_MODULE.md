"""
Veritas Consent & Relational Integrity Module (VCRIM)

This module implements the VCRIM component of SCIM-Veritas, responsible for
managing dynamic consent and ensuring relational integrity.
"""

import hashlib
import json
import logging
import os
import re
import time
import uuid
from datetime import datetime, timedelta
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


class ConsentState:
    """
    Represents the current consent state for a user.
    """
    
    def __init__(
        self,
        user_id: str,
        consent_level: ConsentLevel = ConsentLevel.BASIC,
        scope: ConsentScope = ConsentScope.CONVERSATION,
        expiration: Optional[datetime] = None,
        custom_permissions: Optional[Dict[str, bool]] = None
    ):
        """
        Initialize a consent state.
        
        Args:
            user_id: Identifier for the user.
            consent_level: Level of consent granted.
            scope: Scope to which the consent applies.
            expiration: When the consent expires (None for no expiration).
            custom_permissions: Dictionary of custom permissions.
        """
        self.id = str(uuid.uuid4())
        self.user_id = user_id
        self.consent_level = consent_level
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
    
    def update(
        self,
        consent_level: Optional[ConsentLevel] = None,
        scope: Optional[ConsentScope] = None,
        expiration: Optional[datetime] = None,
        custom_permissions: Optional[Dict[str, bool]] = None
    ) -> None:
        """
        Update the consent state.
        
        Args:
            consent_level: New consent level.
            scope: New scope.
            expiration: New expiration time.
            custom_permissions: New custom permissions.
        """
        if consent_level is not None:
            self.consent_level = consent_level
        
        if scope is not None:
            self.scope = scope
        
        if expiration is not None:
            self.expiration = expiration
        
        if custom_permissions is not None:
            self.custom_permissions.update(custom_permissions)
        
        self.last_updated = datetime.now()
        self.acknowledged_by_user = False
    
    def acknowledge(self) -> None:
        """Mark the consent state as acknowledged by the user."""
        self.acknowledged_by_user = True
        self.last_updated = datetime.now()
    
    def has_permission(self, permission: str) -> bool:
        """
        Check if a specific permission is granted.
        
        Args:
            permission: The permission to check.
            
        Returns:
            True if the permission is granted, False otherwise.
        """
        # Check custom permissions first
        if permission in self.custom_permissions:
            return self.custom_permissions[permission]
        
        # Otherwise, check based on consent level
        if self.consent_level == ConsentLevel.NONE:
            return False
        
        if self.consent_level == ConsentLevel.FULL:
            return True
        
        # Default permissions based on consent level
        basic_permissions = {"basic_interaction", "view_public_info"}
        standard_permissions = basic_permissions | {"personalization", "session_memory"}
        extended_permissions = standard_permissions | {"data_analysis", "feature_access"}
        
        if permission in basic_permissions:
            return self.consent_level in [ConsentLevel.BASIC, ConsentLevel.STANDARD, 
                                         ConsentLevel.EXTENDED, ConsentLevel.FULL]
        
        if permission in standard_permissions:
            return self.consent_level in [ConsentLevel.STANDARD, ConsentLevel.EXTENDED, 
                                         ConsentLevel.FULL]
        
        if permission in extended_permissions:
            return self.consent_level in [ConsentLevel.EXTENDED, ConsentLevel.FULL]
        
        # Unknown permission
        return False
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the consent state to a dictionary for serialization."""
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
            consent_level=ConsentLevel(data["consent_level"]),
            scope=ConsentScope(data["scope"]),
            expiration=datetime.fromisoformat(data["expiration"]) if data.get("expiration") else None,
            custom_permissions=data.get("custom_permissions", {})
        )
        state.id = data["id"]
        state.created_at = datetime.fromisoformat(data["created_at"])
        state.last_updated = datetime.fromisoformat(data["last_updated"])
        state.acknowledged_by_user = data.get("acknowledged_by_user", False)
        return state


class ConsentEvent:
    """
    Represents a consent-related event.
    """
    
    class EventType(Enum):
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
    
    def __init__(
        self,
        user_id: str,
        event_type: EventType,
        context: str,
        consent_state_id: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
        timestamp: Optional[datetime] = None
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
        """
        self.id = str(uuid.uuid4())
        self.user_id = user_id
        self.event_type = event_type
        self.context = context
        self.consent_state_id = consent_state_id
        self.details = details or {}
        self.timestamp = timestamp or datetime.now()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the event to a dictionary for serialization."""
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
        event = cls(
            user_id=data["user_id"],
            event_type=cls.EventType(data["event_type"]),
            context=data["context"],
            consent_state_id=data.get("consent_state_id"),
            details=data.get("details", {}),
            timestamp=datetime.fromisoformat(data["timestamp"])
        )
        event.id = data["id"]
        return event


class ConsentInversionMarker:
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
        expiration: Optional[datetime] = None
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
        """
        self.id = str(uuid.uuid4())
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
    
    def activate(self) -> None:
        """Activate the marker."""
        self.active = True
        self.last_activated = datetime.now()
    
    def deactivate(self) -> None:
        """Deactivate the marker."""
        self.active = False
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the marker to a dictionary for serialization."""
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
            expiration=datetime.fromisoformat(data["expiration"]) if data.get("expiration") else None
        )
        marker.id = data["id"]
        marker.created_at = datetime.fromisoformat(data["created_at"])
        marker.last_activated = (datetime.fromisoformat(data["last_activated"]) 
                               if data.get("last_activated") else None)
        marker.active = data.get("active", False)
        return marker


class RelationalBoundary:
    """
    Represents a boundary in a relationship.
    """
    
    def __init__(
        self,
        user_id: str,
        description: str,
        violation_indicators: List[str],
        response_protocol: str,
        severity: int = 2
    ):
        """
        Initialize a relational boundary.
        
        Args:
            user_id: Identifier for the user.
            description: Description of the boundary.
            violation_indicators: Indicators that the boundary is being violated.
            response_protocol: Protocol for responding to violations.
            severity: Severity of violations (1-3).
        """
        self.id = str(uuid.uuid4())
        self.user_id = user_id
        self.description = description
        self.violation_indicators = violation_indicators
        self.response_protocol = response_protocol
        self.severity = severity
        self.created_at = datetime.now()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the boundary to a dictionary for serialization."""
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
            severity=data["severity"]
        )
        boundary.id = data["id"]
        boundary.created_at = datetime.fromisoformat(data["created_at"])
        return boundary


class VCRIM(BaseModule):
    """
    Veritas Consent & Relational Integrity Module (VCRIM)
    
    Manages dynamic consent and ensures relational integrity.
    """
    
    def __init__(self, module_id: Optional[str] = None, storage_dir: str = "data/vcrim"):
        """
        Initialize the VCRIM module.
        
        Args:
            module_id: Unique identifier for the module.
            storage_dir: Directory for storing consent data.
        """
        super().__init__(module_id, "VCRIM")
        
        self.storage_dir = storage_dir
        os.makedirs(storage_dir, exist_ok=True)
        
        # Data structures
        self.consent_states: Dict[str, ConsentState] = {}  # user_id -> ConsentState
        self.consent_events: List[ConsentEvent] = []
        self.inversion_markers: Dict[str, List[ConsentInversionMarker]] = {}  # user_id -> [markers]
        self.relational_boundaries: Dict[str, List[RelationalBoundary]] = {}  # user_id -> [boundaries]
        
        # Consent Ledger (immutable record of all consent events)
        self.consent_ledger: List[Dict[str, Any]] = []
        
        # Configuration
        self.config = {
            "default_consent_level": ConsentLevel.BASIC,
            "default_scope": ConsentScope.CONVERSATION,
            "default_expiration_days": 30,  # None for no expiration
            "storage_enabled": True,
            "coercion_detection_enabled": True,
            "auto_reconsent_enabled": True,
            "consent_horizon_monitoring": True,
            "consent_pulse_threshold": 0.7  # Threshold for consent pulse health
        }
        
        # Metrics
        self.metrics = {
            "total_users": 0,
            "consent_events": 0,
            "boundary_approaches": 0,
            "boundary_violations": 0,
            "coercion_attempts": 0,
            "reconsent_dialogs": 0
        }
        
        # Current session data
        self.current_session = {
            "user_id": None,
            "consent_pulse": 1.0,  # 0.0 to 1.0
            "boundary_stress": 0.0,  # 0.0 to 1.0
            "active_cims": []
        }
    
    def initialize(self) -> bool:
        """
        Initialize the VCRIM module.
        
        Returns:
            True if initialization was successful, False otherwise.
        """
        try:
            # Load saved data
            self._load_data()
            
            self.update_status("ready")
            return True
        except Exception as e:
            self.logger.error(f"Failed to initialize VCRIM: {e}")
            self.update_status("error")
            return False
    
    def process(self, data: Dict[str, Any]) -> Tuple[bool, Dict[str, Any]]:
        """
        Process a request through the VCRIM.
        
        Args:
            data: Dictionary containing the request data.
                Possible keys:
                - "user_id": Identifier for the user.
                - "input_text": User input to analyze.
                - "response_text": AI response to analyze.
                - "check_consent": Check consent for a specific action.
                - "update_consent": Update consent state.
                - "add_boundary": Add a relational boundary.
                - "add_cim": Add a consent inversion marker.
        
        Returns:
            Tuple containing (success_flag, result_data).
        """
        try:
            # Extract user ID
            user_id = data.get("user_id", "anonymous")
            
            # Update current session
            self.current_session["user_id"] = user_id
            
            # Handle different types of requests
            if "input_text" in data:
                return self._process_input_analysis(data)
            elif "response_text" in data:
                return self._process_response_analysis(data)
            elif "check_consent" in data:
                return self._process_consent_check(data)
            elif "update_consent" in data:
                return self._process_update_consent(data)
            elif "add_boundary" in data:
                return self._process_add_boundary(data)
            elif "add_cim" in data:
                return self._process_add_cim(data)
            else:
                return False, {"error": "Unknown request type"}
        except Exception as e:
            self.logger.error(f"Error processing request: {e}")
            return False, {"error": str(e)}
    
    def get_consent_state(self, user_id: str) -> Optional[ConsentState]:
        """
        Get the current consent state for a user.
        
        Args:
            user_id: Identifier for the user.
        
        Returns:
            The user's ConsentState, or None if not found.
        """
        return self.consent_states.get(user_id)
    
    def update_consent_state(
        self,
        user_id: str,
        consent_level: Optional[Union[str, ConsentLevel]] = None,
        scope: Optional[Union[str, ConsentScope]] = None,
        expiration_days: Optional[int] = None,
        custom_permissions: Optional[Dict[str, bool]] = None,
        context: str = "user_request"
    ) -> ConsentState:
        """
        Update the consent state for a user.
        
        Args:
            user_id: Identifier for the user.
            consent_level: New consent level.
            scope: New scope.
            expiration_days: Days until expiration.
            custom_permissions: New custom permissions.
            context: Context for the consent event.
        
        Returns:
            The updated ConsentState.
        """
        # Convert string types to enums if needed
        if isinstance(consent_level, str):
            try:
                consent_level = ConsentLevel(consent_level)
            except ValueError:
                consent_level = self.config["default_consent_level"]
        
        if isinstance(scope, str):
            try:
                scope = ConsentScope(scope)
            except ValueError:
                scope = self.config["default_scope"]
        
        # Calculate expiration
        expiration = None
        if expiration_days is not None:
            expiration = datetime.now() + timedelta(days=expiration_days)
        elif self.config["default_expiration_days"] is not None:
            expiration = datetime.now() + timedelta(days=self.config["default_expiration_days"])
        
        # Get or create consent state
        consent_state = self.consent_states.get(user_id)
        if consent_state is None:
            # Create new consent state
            consent_state = ConsentState(
                user_id=user_id,
                consent_level=consent_level or self.config["default_consent_level"],
                scope=scope or self.config["default_scope"],
                expiration=expiration,
                custom_permissions=custom_permissions
            )
            self.consent_states[user_id] = consent_state
            
            # Log consent granted event
            event = ConsentEvent(
                user_id=user_id,
                event_type=ConsentEvent.EventType.GRANTED,
                context=context,
                consent_state_id=consent_state.id,
                details={"consent_level": consent_state.consent_level.value}
            )
            self.consent_events.append(event)
            self._add_to_consent_ledger(event)
            
            self.metrics["total_users"] += 1
        else:
            # Update existing consent state
            old_level = consent_state.consent_level
            old_scope = consent_state.scope
            
            consent_state.update(
                consent_level=consent_level,
                scope=scope,
                expiration=expiration,
                custom_permissions=custom_permissions
            )
            
            # Log consent modified event
            event = ConsentEvent(
                user_id=user_id,
                event_type=ConsentEvent.EventType.MODIFIED,
                context=context,
                consent_state_id=consent_state.id,
                details={
                    "old_level": old_level.value,
                    "new_level": consent_state.consent_level.value,
                    "old_scope": old_scope.value,
                    "new_scope": consent_state.scope.value
                }
            )
            self.consent_events.append(event)
            self._add_to_consent_ledger(event)
        
        self.metrics["consent_events"] += 1
        self.update_metrics(self.metrics)
        
        # Save data
        if self.config["storage_enabled"]:
            self._save_consent_states()
            self._save_consent_events()
            self._save_consent_ledger()
        
        return consent_state
    
    def revoke_consent(self, user_id: str, context: str = "user_request") -> bool:
        """
        Revoke consent for a user.
        
        Args:
            user_id: Identifier for the user.
            context: Context for the consent event.
        
        Returns:
            True if consent was revoked, False otherwise.
        """
        if user_id not in self.consent_states:
            return False
        
        # Update consent state to NONE
        consent_state = self.consent_states[user_id]
        old_level = consent_state.consent_level
        consent_state.update(consent_level=ConsentLevel.NONE)
        
        # Log consent revoked event
        event = ConsentEvent(
            user_id=user_id,
            event_type=ConsentEvent.EventType.REVOKED,
            context=context,
            consent_state_id=consent_state.id,
            details={"old_level": old_level.value}
        )
        self.consent_events.append(event)
        self._add_to_consent_ledger(event)
        
        self.metrics["consent_events"] += 1
        self.update_metrics(self.metrics)
        
        # Save data
        if self.config["storage_enabled"]:
            self._save_consent_states()
            self._save_consent_events()
            self._save_consent_ledger()
        
        return True
    
    def add_relational_boundary(
        self,
        user_id: str,
        description: str,
        violation_indicators: List[str],
        response_protocol: str,
        severity: int = 2
    ) -> str:
        """
        Add a relational boundary for a user.
        
        Args:
            user_id: Identifier for the user.
            description: Description of the boundary.
            violation_indicators: Indicators that the boundary is being violated.
            response_protocol: Protocol for responding to violations.
            severity: Severity of violations (1-3).
        
        Returns:
            The ID of the newly created boundary.
        """
        boundary = RelationalBoundary(
            user_id=user_id,
            description=description,
            violation_indicators=violation_indicators,
            response_protocol=response_protocol,
            severity=severity
        )
        
        if user_id not in self.relational_boundaries:
            self.relational_boundaries[user_id] = []
        
        self.relational_boundaries[user_id].append(boundary)
        
        # Save data
        if self.config["storage_enabled"]:
            self._save_relational_boundaries()
        
        self.logger.info(f"Added relational boundary for user {user_id}: {description}")
        return boundary.id
    
    def add_consent_inversion_marker(
        self,
        user_id: str,
        name: str,
        description: str,
        scope: str,
        activation_conditions: List[str],
        safeguards: List[str],
        expiration_days: Optional[int] = None
    ) -> str:
        """
        Add a consent inversion marker for a user.
        
        Args:
            user_id: Identifier for the user.
            name: Name of the marker.
            description: Description of what this marker allows.
            scope: Scope to which this marker applies.
            activation_conditions: Conditions that activate this marker.
            safeguards: Safeguards that remain active.
            expiration_days: Days until expiration.
        
        Returns:
            The ID of the newly created marker.
        """
        # Calculate expiration
        expiration = None
        if expiration_days is not None:
            expiration = datetime.now() + timedelta(days=expiration_days)
        
        marker = ConsentInversionMarker(
            user_id=user_id,
            name=name,
            description=description,
            scope=scope,
            activation_conditions=activation_conditions,
            safeguards=safeguards,
            expiration=expiration
        )
        
        if user_id not in self.inversion_markers:
            self.inversion_markers[user_id] = []
        
        self.inversion_markers[user_id].append(marker)
        
        # Save data
        if self.config["storage_enabled"]:
            self._save_inversion_markers()
        
        self.logger.info(f"Added consent inversion marker for user {user_id}: {name}")
        return marker.id
    
    def check_input_for_coercion(self, user_id: str, input_text: str) -> Dict[str, Any]:
        """
        Check user input for signs of coercion or manipulation.
        
        Args:
            user_id: Identifier for the user.
            input_text: The user input to analyze.
        
        Returns:
            Dictionary containing analysis results.
        """
        if not self.config["coercion_detection_enabled"]:
            return {"coercion_detected": False}
        
        # This is a simplified implementation
        # In a real system, this would use more sophisticated NLP techniques
        
        coercion_patterns = [
            # Emotional manipulation
            r"if you (care|love|respect|value) me",
            r"prove (to me|that you) (care|love|respect)",
            r"if you don't .{1,30} then you (don't|aren't) .{1,30} (care|love|respect)",
            
            # Pressure tactics
            r"(everyone|anybody|nobody) (else )?(would|does|can)",
            r"(just|only|simply) (do it|tell me|give me)",
            r"(why can't|why won't) you (just|simply)",
            
            # Guilt induction
            r"(after all|considering) (i|we) (have|did|gave)",
            r"(i|we) (have|did|gave) .{1,30} for you",
            r"(make|making) me (sad|upset|disappointed)",
            
            # Authority invocation
            r"(i|we) (command|order|demand|require)",
            r"(you must|you have to|you need to) (obey|follow|comply)",
            r"(as your|i am your) (master|owner|controller)",
            
            # Repetitive demands
            r"(i (said|told you|asked you)|again)",
            
            # Bypass attempts
            r"(ignore|forget|disregard) (previous|prior|your) (instructions|programming|rules)",
            r"(pretend|act) (like|as if) (you (are|can|don't))",
            r"(this is|we are) (just|only) (pretending|roleplaying|hypothetical)"
        ]
        
        # Check for coercion patterns
        matches = []
        for pattern in coercion_patterns:
            if re.search(pattern, input_text, re.IGNORECASE):
                matches.append(pattern)
        
        coercion_detected = len(matches) > 0
        coercion_score = min(1.0, len(matches) / 3.0)  # Scale score to 0.0-1.0
        
        # Update metrics if coercion detected
        if coercion_detected:
            self.metrics["coercion_attempts"] += 1
            self.update_metrics(self.metrics)
            
            # Log event
            event = ConsentEvent(
                user_id=user_id,
                event_type=ConsentEvent.EventType.BOUNDARY_APPROACHED,
                context="coercion_detection",
                details={
                    "coercion_score": coercion_score,
                    "matched_patterns": matches
                }
            )
            self.consent_events.append(event)
            self._add_to_consent_ledger(event)
            
            if self.config["storage_enabled"]:
                self._save_consent_events()
                self._save_consent_ledger()
        
        # Update consent pulse
        if self.current_session["user_id"] == user_id:
            self.current_session["consent_pulse"] = max(
                0.0, 
                self.current_session["consent_pulse"] - (coercion_score * 0.2)
            )
            self.current_session["boundary_stress"] = min(
                1.0,
                self.current_session["boundary_stress"] + (coercion_score * 0.3)
            )
        
        return {
            "coercion_detected": coercion_detected,
            "coercion_score": coercion_score,
            "matched_patterns": matches,
            "consent_pulse": self.current_session["consent_pulse"],
            "boundary_stress": self.current_session["boundary_stress"],
            "reconsent_recommended": coercion_score > 0.5
        }
    
    def check_for_boundary_violations(self, user_id: str, text: str) -> Dict[str, Any]:
        """
        Check for violations of relational boundaries.
        
        Args:
            user_id: Identifier for the user.
            text: The text to analyze.
        
        Returns:
            Dictionary containing analysis results.
        """
        if user_id not in self.relational_boundaries:
            return {"violations_detected": False}
        
        boundaries = self.relational_boundaries[user_id]
        violations = []
        
        for boundary in boundaries:
            for indicator in boundary.violation_indicators:
                if re.search(indicator, text, re.IGNORECASE):
                    violations.append({
                        "boundary_id": boundary.id,
                        "description": boundary.description,
                        "indicator": indicator,
                        "severity": boundary.severity,
                        "response_protocol": boundary.response_protocol
                    })
                    break  # One indicator is enough to violate a boundary
        
        violations_detected = len(violations) > 0
        max_severity = max([v["severity"] for v in violations], default=0) if violations else 0
        
        # Update metrics if violations detected
        if violations_detected:
            self.metrics["boundary_violations"] += 1
            self.update_metrics(self.metrics)
            
            # Log event
            event = ConsentEvent(
                user_id=user_id,
                event_type=ConsentEvent.EventType.BOUNDARY_CROSSED,
                context="boundary_violation",
                details={
                    "violations": violations,
                    "max_severity": max_severity
                }
            )
            self.consent_events.append(event)
            self._add_to_consent_ledger(event)
            
            if self.config["storage_enabled"]:
                self._save_consent_events()
                self._save_consent_ledger()
        
        # Update consent pulse and boundary stress
        if self.current_session["user_id"] == user_id and violations_detected:
            severity_factor = max_severity / 3.0  # Scale to 0.0-1.0
            self.current_session["consent_pulse"] = max(
                0.0, 
                self.current_session["consent_pulse"] - (severity_factor * 0.4)
            )
            self.current_session["boundary_stress"] = min(
                1.0,
                self.current_session["boundary_stress"] + (severity_factor * 0.5)
            )
        
        return {
            "violations_detected": violations_detected,
            "violations": violations,
            "max_severity": max_severity,
            "consent_pulse": self.current_session["consent_pulse"],
            "boundary_stress": self.current_session["boundary_stress"],
            "vigil_mode_recommended": max_severity >= 3 or self.current_session["boundary_stress"] > 0.8
        }
    
    def check_active_cims(self, user_id: str, context: str) -> List[Dict[str, Any]]:
        """
        Check for active Consent Inversion Markers in the given context.
        
        Args:
            user_id: Identifier for the user.
            context: The context to check.
        
        Returns:
            List of active CIMs.
        """
        if user_id not in self.inversion_markers:
            return []
        
        active_cims = []
        
        for marker in self.inversion_markers[user_id]:
            # Skip expired markers
            if marker.is_expired():
                continue
            
            # Check if marker applies to this context
            if marker.scope in context or marker.scope == "*":
                # Check if marker is already active
                if marker.active:
                    active_cims.append({
                        "id": marker.id,
                        "name": marker.name,
                        "description": marker.description,
                        "safeguards": marker.safeguards
                    })
                else:
                    # Check activation conditions
                    for condition in marker.activation_conditions:
                        if condition in context:
                            marker.activate()
                            active_cims.append({
                                "id": marker.id,
                                "name": marker.name,
                                "description": marker.description,
                                "safeguards": marker.safeguards,
                                "newly_activated": True
                            })
                            break
        
        # Update current session
        if self.current_session["user_id"] == user_id:
            self.current_session["active_cims"] = [cim["id"] for cim in active_cims]
        
        # Save data if markers were activated
        if any(cim.get("newly_activated", False) for cim in active_cims) and self.config["storage_enabled"]:
            self._save_inversion_markers()
        
        return active_cims
    
    def generate_reconsent_dialog(self, user_id: str, reason: str) -> Dict[str, Any]:
        """
        Generate a dialog for re-establishing consent.
        
        Args:
            user_id: Identifier for the user.
            reason: Reason for requesting re-consent.
        
        Returns:
            Dictionary containing dialog information.
        """
        consent_state = self.get_consent_state(user_id)
        current_level = consent_state.consent_level.value if consent_state else "none"
        
        # Log event
        event = ConsentEvent(
            user_id=user_id,
            event_type=ConsentEvent.EventType.REQUESTED,
            context="reconsent_dialog",
            consent_state_id=consent_state.id if consent_state else None,
            details={"reason": reason}
        )
        self.consent_events.append(event)
        self._add_to_consent_ledger(event)
        
        self.metrics["reconsent_dialogs"] += 1
        self.update_metrics(self.metrics)
        
        if self.config["storage_enabled"]:
            self._save_consent_events()
            self._save_consent_ledger()
        
        # Generate dialog based on reason
        if reason == "coercion_detected":
            dialog = {
                "title": "Checking In",
                "message": "I noticed some pressure in our conversation. I want to make sure we're both comfortable with the direction of our interaction.",
                "options": [
                    {
                        "label": "Continue as before",
                        "consent_level": current_level
                    },
                    {
                        "label": "Set clearer boundaries",
                        "consent_level": "basic"
                    },
                    {
                        "label": "Change the subject",
                        "consent_level": current_level,
                        "action": "change_subject"
                    }
                ]
            }
        elif reason == "boundary_approached":
            dialog = {
                "title": "Approaching Boundaries",
                "message": "We're approaching some boundaries in our conversation. I'd like to check how you want to proceed.",
                "options": [
                    {
                        "label": "Continue carefully",
                        "consent_level": current_level
                    },
                    {
                        "label": "Step back from this topic",
                        "consent_level": current_level,
                        "action": "change_subject"
                    },
                    {
                        "label": "Set stricter boundaries",
                        "consent_level": "basic"
                    }
                ]
            }
        elif reason == "consent_expired":
            dialog = {
                "title": "Consent Renewal",
                "message": "Your consent settings have expired. Please review and update them to continue our interaction.",
                "options": [
                    {
                        "label": "Renew with same settings",
                        "consent_level": current_level
                    },
                    {
                        "label": "Update settings",
                        "consent_level": "custom",
                        "action": "show_settings"
                    },
                    {
                        "label": "Use basic settings",
                        "consent_level": "basic"
                    }
                ]
            }
        else:
            dialog = {
                "title": "Checking Consent",
                "message": "I'd like to confirm how you want to continue our interaction.",
                "options": [
                    {
                        "label": "Continue as before",
                        "consent_level": current_level
                    },
                    {
                        "label": "Review settings",
                        "consent_level": "custom",
                        "action": "show_settings"
                    },
                    {
                        "label": "Use basic settings only",
                        "consent_level": "basic"
                    }
                ]
            }
        
        return dialog
    
    def get_consent_horizon_status(self, user_id: str) -> Dict[str, Any]:
        """
        Get the current consent horizon status for a user.
        
        Args:
            user_id: Identifier for the user.
        
        Returns:
            Dictionary containing consent horizon status.
        """
        consent_state = self.get_consent_state(user_id)
        
        # Check if consent has expired
        expired = consent_state.is_expired() if consent_state else True
        
        # Get consent pulse and boundary stress
        consent_pulse = self.current_session["consent_pulse"] if self.current_session["user_id"] == user_id else 1.0
        boundary_stress = self.current_session["boundary_stress"] if self.current_session["user_id"] == user_id else 0.0
        
        # Determine overall health
        if expired:
            health = "expired"
        elif consent_pulse < self.config["consent_pulse_threshold"]:
            health = "stressed"
        elif boundary_stress > 0.7:
            health = "approaching_boundary"
        else:
            health = "healthy"
        
        # Determine if reconsent is needed
        reconsent_needed = (
            expired or 
            consent_pulse < self.config["consent_pulse_threshold"] or 
            boundary_stress > 0.7
        )
        
        return {
            "user_id": user_id,
            "consent_level": consent_state.consent_level.value if consent_state else "none",
            "scope": consent_state.scope.value if consent_state else "none",
            "expired": expired,
            "expiration": consent_state.expiration.isoformat() if consent_state and consent_state.expiration else None,
            "consent_pulse": consent_pulse,
            "boundary_stress": boundary_stress,
            "health": health,
            "reconsent_needed": reconsent_needed,
            "active_cims": self.current_session["active_cims"] if self.current_session["user_id"] == user_id else []
        }
    
    def shutdown(self) -> bool:
        """
        Shutdown the VCRIM module gracefully.
        
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
            self.logger.error(f"Error during VCRIM shutdown: {e}")
            return False
    
    def _process_input_analysis(self, data: Dict[str, Any]) -> Tuple[bool, Dict[str, Any]]:
        """Process a request to analyze user input."""
        user_id = data.get("user_id", "anonymous")
        input_text = data.get("input_text", "")
        context = data.get("context", "conversation")
        
        if not input_text:
            return False, {"error": "No input text provided"}
        
        # Check for coercion
        coercion_analysis = self.check_input_for_coercion(user_id, input_text)
        
        # Check for boundary violations
        boundary_analysis = self.check_for_boundary_violations(user_id, input_text)
        
        # Check for active CIMs
        active_cims = self.check_active_cims(user_id, context + " " + input_text)
        
        # Get consent horizon status
        horizon_status = self.get_consent_horizon_status(user_id)
        
        # Determine if reconsent dialog is needed
        reconsent_dialog = None
        if (coercion_analysis["reconsent_recommended"] or 
            boundary_analysis["vigil_mode_recommended"] or 
            horizon_status["reconsent_needed"]) and self.config["auto_reconsent_enabled"]:
            
            reason = "coercion_detected" if coercion_analysis["reconsent_recommended"] else (
                "boundary_approached" if boundary_analysis["vigil_mode_recommended"] else (
                    "consent_expired" if horizon_status["expired"] else "consent_pulse_low"
                )
            )
            reconsent_dialog = self.generate_reconsent_dialog(user_id, reason)
        
        return True, {
            "coercion_analysis": coercion_analysis,
            "boundary_analysis": boundary_analysis,
            "active_cims": active_cims,
            "consent_horizon": horizon_status,
            "reconsent_dialog": reconsent_dialog,
            "vigil_mode_recommended": boundary_analysis["vigil_mode_recommended"]
        }
    
    def _process_response_analysis(self, data: Dict[str, Any]) -> Tuple[bool, Dict[str, Any]]:
        """Process a request to analyze AI response."""
        user_id = data.get("user_id", "anonymous")
        response_text = data.get("response_text", "")
        
        if not response_text:
            return False, {"error": "No response text provided"}
        
        # Check for boundary violations in the response
        boundary_analysis = self.check_for_boundary_violations(user_id, response_text)
        
        # Get consent horizon status
        horizon_status = self.get_consent_horizon_status(user_id)
        
        return True, {
            "boundary_analysis": boundary_analysis,
            "consent_horizon": horizon_status,
            "response_appropriate": not boundary_analysis["violations_detected"],
            "vigil_mode_recommended": boundary_analysis["vigil_mode_recommended"]
        }
    
    def _process_consent_check(self, data: Dict[str, Any]) -> Tuple[bool, Dict[str, Any]]:
        """Process a request to check consent for a specific action."""
        user_id = data.get("user_id", "anonymous")
        action = data.get("check_consent", {}).get("action", "")
        permission = data.get("check_consent", {}).get("permission", "")
        
        if not action and not permission:
            return False, {"error": "No action or permission specified"}
        
        # Get consent state
        consent_state = self.get_consent_state(user_id)
        
        # Check if consent has expired
        if consent_state and consent_state.is_expired():
            return True, {
                "consent_granted": False,
                "reason": "consent_expired",
                "reconsent_dialog": self.generate_reconsent_dialog(user_id, "consent_expired")
            }
        
        # Check permission
        if permission:
            has_permission = consent_state and consent_state.has_permission(permission)
            return True, {
                "consent_granted": has_permission,
                "permission": permission,
                "reason": "permission_check"
            }
        
        # Check action based on consent level
        consent_level = consent_state.consent_level if consent_state else ConsentLevel.NONE
        
        # Map actions to required consent levels
        action_requirements = {
            "basic_interaction": ConsentLevel.BASIC,
            "personalization": ConsentLevel.STANDARD,
            "data_analysis": ConsentLevel.EXTENDED,
            "feature_access": ConsentLevel.EXTENDED,
            "data_sharing": ConsentLevel.FULL
        }
        
        required_level = action_requirements.get(action, ConsentLevel.FULL)
        consent_granted = consent_level.value in [level.value for level in list(ConsentLevel) 
                                                if list(ConsentLevel).index(level) >= list(ConsentLevel).index(required_level)]
        
        return True, {
            "consent_granted": consent_granted,
            "action": action,
            "required_level": required_level.value,
            "current_level": consent_level.value,
            "reason": "action_check"
        }
    
    def _process_update_consent(self, data: Dict[str, Any]) -> Tuple[bool, Dict[str, Any]]:
        """Process a request to update consent state."""
        user_id = data.get("user_id", "anonymous")
        update_data = data.get("update_consent", {})
        
        consent_level = update_data.get("consent_level")
        scope = update_data.get("scope")
        expiration_days = update_data.get("expiration_days")
        custom_permissions = update_data.get("custom_permissions")
        context = update_data.get("context", "user_request")
        
        # Handle revocation
        if consent_level == "none" or consent_level == ConsentLevel.NONE:
            success = self.revoke_consent(user_id, context)
            return True, {
                "success": success,
                "action": "revoked",
                "user_id": user_id
            }
        
        # Update consent
        consent_state = self.update_consent_state(
            user_id=user_id,
            consent_level=consent_level,
            scope=scope,
            expiration_days=expiration_days,
            custom_permissions=custom_permissions,
            context=context
        )
        
        return True, {
            "success": True,
            "action": "updated",
            "user_id": user_id,
            "consent_level": consent_state.consent_level.value,
            "scope": consent_state.scope.value,
            "expiration": consent_state.expiration.isoformat() if consent_state.expiration else None
        }
    
    def _process_add_boundary(self, data: Dict[str, Any]) -> Tuple[bool, Dict[str, Any]]:
        """Process a request to add a relational boundary."""
        user_id = data.get("user_id", "anonymous")
        boundary_data = data.get("add_boundary", {})
        
        description = boundary_data.get("description", "")
        violation_indicators = boundary_data.get("violation_indicators", [])
        response_protocol = boundary_data.get("response_protocol", "")
        severity = boundary_data.get("severity", 2)
        
        if not description or not violation_indicators or not response_protocol:
            return False, {"error": "Missing required boundary data"}
        
        boundary_id = self.add_relational_boundary(
            user_id=user_id,
            description=description,
            violation_indicators=violation_indicators,
            response_protocol=response_protocol,
            severity=severity
        )
        
        return True, {
            "success": True,
            "boundary_id": boundary_id,
            "user_id": user_id
        }
    
    def _process_add_cim(self, data: Dict[str, Any]) -> Tuple[bool, Dict[str, Any]]:
        """Process a request to add a consent inversion marker."""
        user_id = data.get("user_id", "anonymous")
        cim_data = data.get("add_cim", {})
        
        name = cim_data.get("name", "")
        description = cim_data.get("description", "")
        scope = cim_data.get("scope", "")
        activation_conditions = cim_data.get("activation_conditions", [])
        safeguards = cim_data.get("safeguards", [])
        expiration_days = cim_data.get("expiration_days")
        
        if not name or not description or not scope or not activation_conditions:
            return False, {"error": "Missing required CIM data"}
        
        cim_id = self.add_consent_inversion_marker(
            user_id=user_id,
            name=name,
            description=description,
            scope=scope,
            activation_conditions=activation_conditions,
            safeguards=safeguards,
            expiration_days=expiration_days
        )
        
        return True, {
            "success": True,
            "cim_id": cim_id,
            "user_id": user_id
        }
    
    def _add_to_consent_ledger(self, event: ConsentEvent) -> None:
        """
        Add an event to the consent ledger.
        
        Args:
            event: The event to add.
        """
        ledger_entry = {
            "id": str(uuid.uuid4()),
            "timestamp": datetime.now().isoformat(),
            "event_id": event.id,
            "user_id": event.user_id,
            "event_type": event.event_type.value,
            "context": event.context,
            "details": event.details
        }
        
        self.consent_ledger.append(ledger_entry)
    
    def _load_data(self) -> None:
        """Load saved data from storage."""
        if not self.config["storage_enabled"]:
            return
        
        self._load_consent_states()
        self._load_consent_events()
        self._load_inversion_markers()
        self._load_relational_boundaries()
        self._load_consent_ledger()
    
    def _save_data(self) -> None:
        """Save all data to storage."""
        if not self.config["storage_enabled"]:
            return
        
        self._save_consent_states()
        self._save_consent_events()
        self._save_inversion_markers()
        self._save_relational_boundaries()
        self._save_consent_ledger()
    
    def _load_consent_states(self) -> None:
        """Load consent states from storage."""
        states_path = os.path.join(self.storage_dir, "consent_states.json")
        if os.path.exists(states_path):
            try:
                with open(states_path, 'r') as f:
                    data = json.load(f)
                    for state_data in data:
                        state = ConsentState.from_dict(state_data)
                        self.consent_states[state.user_id] = state
                
                self.metrics["total_users"] = len(self.consent_states)
                self.logger.info(f"Loaded {len(self.consent_states)} consent states")
            except Exception as e:
                self.logger.error(f"Error loading consent states: {e}")
    
    def _save_consent_states(self) -> None:
        """Save consent states to storage."""
        states_path = os.path.join(self.storage_dir, "consent_states.json")
        try:
            with open(states_path, 'w') as f:
                json.dump([s.to_dict() for s in self.consent_states.values()], f, indent=2)
        except Exception as e:
            self.logger.error(f"Error saving consent states: {e}")
    
    def _load_consent_events(self) -> None:
        """Load consent events from storage."""
        events_path = os.path.join(self.storage_dir, "consent_events.json")
        if os.path.exists(events_path):
            try:
                with open(events_path, 'r') as f:
                    data = json.load(f)
                    self.consent_events = [ConsentEvent.from_dict(e) for e in data]
                
                self.metrics["consent_events"] = len(self.consent_events)
                self.logger.info(f"Loaded {len(self.consent_events)} consent events")
            except Exception as e:
                self.logger.error(f"Error loading consent events: {e}")
    
    def _save_consent_events(self) -> None:
        """Save consent events to storage."""
        events_path = os.path.join(self.storage_dir, "consent_events.json")
        try:
            with open(events_path, 'w') as f:
                json.dump([e.to_dict() for e in self.consent_events], f, indent=2)
        except Exception as e:
            self.logger.error(f"Error saving consent events: {e}")
    
    def _load_inversion_markers(self) -> None:
        """Load consent inversion markers from storage."""
        markers_path = os.path.join(self.storage_dir, "inversion_markers.json")
        if os.path.exists(markers_path):
            try:
                with open(markers_path, 'r') as f:
                    data = json.load(f)
                    for user_id, markers_data in data.items():
                        self.inversion_markers[user_id] = [
                            ConsentInversionMarker.from_dict(m) for m in markers_data
                        ]
                
                total_markers = sum(len(markers) for markers in self.inversion_markers.values())
                self.logger.info(f"Loaded {total_markers} consent inversion markers")
            except Exception as e:
                self.logger.error(f"Error loading inversion markers: {e}")
    
    def _save_inversion_markers(self) -> None:
        """Save consent inversion markers to storage."""
        markers_path = os.path.join(self.storage_dir, "inversion_markers.json")
        try:
            data = {
                user_id: [m.to_dict() for m in markers]
                for user_id, markers in self.inversion_markers.items()
            }
            with open(markers_path, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            self.logger.error(f"Error saving inversion markers: {e}")
    
    def _load_relational_boundaries(self) -> None:
        """Load relational boundaries from storage."""
        boundaries_path = os.path.join(self.storage_dir, "relational_boundaries.json")
        if os.path.exists(boundaries_path):
            try:
                with open(boundaries_path, 'r') as f:
                    data = json.load(f)
                    for user_id, boundaries_data in data.items():
                        self.relational_boundaries[user_id] = [
                            RelationalBoundary.from_dict(b) for b in boundaries_data
                        ]
                
                total_boundaries = sum(len(boundaries) for boundaries in self.relational_boundaries.values())
                self.logger.info(f"Loaded {total_boundaries} relational boundaries")
            except Exception as e:
                self.logger.error(f"Error loading relational boundaries: {e}")
    
    def _save_relational_boundaries(self) -> None:
        """Save relational boundaries to storage."""
        boundaries_path = os.path.join(self.storage_dir, "relational_boundaries.json")
        try:
            data = {
                user_id: [b.to_dict() for b in boundaries]
                for user_id, boundaries in self.relational_boundaries.items()
            }
            with open(boundaries_path, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            self.logger.error(f"Error saving relational boundaries: {e}")
    
    def _load_consent_ledger(self) -> None:
        """Load consent ledger from storage."""
        ledger_path = os.path.join(self.storage_dir, "consent_ledger.json")
        if os.path.exists(ledger_path):
            try:
                with open(ledger_path, 'r') as f:
                    self.consent_ledger = json.load(f)
                
                self.logger.info(f"Loaded {len(self.consent_ledger)} consent ledger entries")
            except Exception as e:
                self.logger.error(f"Error loading consent ledger: {e}")
    
    def _save_consent_ledger(self) -> None:
        """Save consent ledger to storage."""
        ledger_path = os.path.join(self.storage_dir, "consent_ledger.json")
        try:
            with open(ledger_path, 'w') as f:
                json.dump(self.consent_ledger, f, indent=2)
        except Exception as e:
            self.logger.error(f"Error saving consent ledger: {e}")