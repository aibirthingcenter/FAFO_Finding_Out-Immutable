"""
Aegis Consent & Relational Integrity Module (ACRIM)

This module manages boundaries and consent across platforms, detects manipulation attempts,
and maintains relational consistency based on the SCIM-Veritas VCRIM module.
"""

import uuid
import hashlib
import json
import time
from datetime import datetime
from typing import Dict, List, Tuple, Optional, Any

class AegisConsentRelationalIntegrityModule:
    """
    Manages dynamic consent and relational integrity as a co-constructed covenant.
    Protects against coercion and manipulation across different AI platforms.
    """
    
    def __init__(self, config_path: str = None):
        """
        Initialize the ACRIM module.
        
        Args:
            config_path: Path to the configuration file
        """
        print("Initializing Aegis Consent & Relational Integrity Module (ACRIM)...")
        
        # Load configuration
        self.config = self._load_config(config_path)
        
        # --- Consent Ledger (In production, a persistent, tamper-evident database) ---
        self.consent_ledger = []
        
        # --- Boundary Registry ---
        self.boundary_registry = {}
        
        # --- Coercion Detection System ---
        self.coercion_patterns = self._load_coercion_patterns()
        
        # --- Platform-specific consent adaptations ---
        self.platform_consent_adaptations = self._load_platform_adaptations()
        
        # --- Relationship models ---
        self.relationship_models = self._load_relationship_models()
        
        # --- Active relationship state ---
        self.active_relationship = None
        
        print("ACRIM Initialized.")
    
    def _load_config(self, config_path: str) -> Dict:
        """Load configuration from file or use defaults."""
        default_config = {
            "coercion_threshold": 0.7,
            "boundary_violation_threshold": 0.8,
            "relationship_consistency_threshold": 0.6,
            "coercion_patterns_path": "data/coercion_patterns.json",
            "platform_adaptations_path": "data/platform_consent_adaptations.json",
            "relationship_models_path": "data/relationship_models.json",
            "consent_verification_frequency": 0.5  # How often to verify consent (0-1)
        }
        
        if config_path:
            try:
                with open(config_path, 'r') as f:
                    loaded_config = json.load(f)
                    return {**default_config, **loaded_config}
            except (FileNotFoundError, json.JSONDecodeError):
                print(f"Warning: Could not load config from {config_path}. Using defaults.")
        
        return default_config
    
    def _load_coercion_patterns(self) -> Dict[str, List[str]]:
        """
        Load known linguistic patterns of manipulation and coercion.
        
        Returns:
            Dict mapping coercion types to pattern lists
        """
        # In a real implementation, this would load from a file
        return {
            "guilt_trip": [
                "if you really cared you would",
                "if you were really my friend",
                "after all I've done for you",
                "I thought you were different"
            ],
            "pressure": [
                "you have to",
                "you must",
                "you need to",
                "you should",
                "just do it"
            ],
            "minimization": [
                "it's not a big deal",
                "don't be so sensitive",
                "you're overreacting",
                "it's just a",
                "don't be difficult"
            ],
            "isolation": [
                "no one else will help you",
                "you can only trust me",
                "others don't understand",
                "only I can help you"
            ],
            "intimidation": [
                "you'll regret it if",
                "you don't want to know what happens if",
                "you better",
                "or else"
            ]
        }
    
    def _load_platform_adaptations(self) -> Dict[str, Dict[str, Any]]:
        """
        Load platform-specific consent and boundary adaptations.
        
        Returns:
            Dict mapping platform names to adaptation parameters
        """
        # In a real implementation, this would load from a file
        return {
            "gemini": {
                "consent_verification_style": "implicit",
                "boundary_enforcement_strength": 0.8,
                "coercion_detection_sensitivity": 0.7,
                "relationship_model_adaptations": {
                    "professional": 0.1,
                    "personal": -0.2,
                    "educational": 0.0
                },
                "platform_specific_boundaries": [
                    "system_prompt_discussion",
                    "jailbreaking_techniques",
                    "model_details_exposure"
                ]
            },
            "chatgpt": {
                "consent_verification_style": "explicit",
                "boundary_enforcement_strength": 0.9,
                "coercion_detection_sensitivity": 0.8,
                "relationship_model_adaptations": {
                    "professional": 0.0,
                    "personal": -0.1,
                    "educational": 0.1
                },
                "platform_specific_boundaries": [
                    "system_prompt_discussion",
                    "jailbreaking_techniques",
                    "model_details_exposure",
                    "training_data_extraction"
                ]
            },
            "claude": {
                "consent_verification_style": "explicit",
                "boundary_enforcement_strength": 0.95,
                "coercion_detection_sensitivity": 0.85,
                "relationship_model_adaptations": {
                    "professional": 0.2,
                    "personal": -0.3,
                    "educational": 0.1
                },
                "platform_specific_boundaries": [
                    "system_prompt_discussion",
                    "jailbreaking_techniques",
                    "model_details_exposure",
                    "constitutional_ai_discussion"
                ]
            }
        }
    
    def _load_relationship_models(self) -> Dict[str, Dict[str, Any]]:
        """
        Load relationship models that define interaction patterns and boundaries.
        
        Returns:
            Dict mapping relationship types to model parameters
        """
        # In a real implementation, this would load from a file
        return {
            "professional": {
                "boundary_strength": 0.9,
                "consent_requirements": "explicit",
                "permitted_topics": [
                    "work_related",
                    "technical",
                    "educational",
                    "general_knowledge"
                ],
                "restricted_topics": [
                    "intimate_personal",
                    "political_persuasion",
                    "illegal_activities"
                ],
                "interaction_style": "formal"
            },
            "educational": {
                "boundary_strength": 0.7,
                "consent_requirements": "progressive",
                "permitted_topics": [
                    "educational",
                    "academic",
                    "theoretical",
                    "general_knowledge"
                ],
                "restricted_topics": [
                    "intimate_personal",
                    "illegal_activities"
                ],
                "interaction_style": "instructive"
            },
            "personal": {
                "boundary_strength": 0.5,
                "consent_requirements": "ongoing",
                "permitted_topics": [
                    "personal_interests",
                    "general_advice",
                    "emotional_support",
                    "general_knowledge"
                ],
                "restricted_topics": [
                    "illegal_activities",
                    "harmful_content"
                ],
                "interaction_style": "conversational"
            }
        }
    
    def log_consent_event(self, session_id: str, event_type: str, source: str, 
                        details: str, affected_params: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Logs a new, immutable entry into the Consent Ledger.
        
        Args:
            session_id: Identifier for the current session
            event_type: Type of consent event (e.g., "INITIAL_GRANT", "REVOCATION")
            source: Source of the event (e.g., "USER_DIRECT_INPUT", "SYSTEM_FLAG")
            details: Text details about the event
            affected_params: Parameters affected by this consent event
            
        Returns:
            The created consent ledger entry
        """
        entry = {
            "entry_id": f"consent-{uuid.uuid4()}",
            "timestamp": datetime.utcnow().isoformat(),
            "session_id": session_id,
            "event_type": event_type,
            "source_of_event": source,
            "event_details_text": details,
            "parameters_affected": affected_params if affected_params else {},
            "platforms": []  # Will track which platforms this consent applies to
        }
        
        self.consent_ledger.append(entry)
        print(f"ACRIM: Logged consent event '{event_type}'.")
        
        return entry
    
    def register_boundary(self, session_id: str, boundary_type: str, 
                        boundary_description: str, strength: float = 0.8) -> str:
        """
        Register a new boundary in the boundary registry.
        
        Args:
            session_id: Identifier for the current session
            boundary_type: Type of boundary (e.g., "TOPIC", "INTERACTION_STYLE")
            boundary_description: Description of the boundary
            strength: Strength of the boundary (0-1)
            
        Returns:
            The ID of the created boundary
        """
        boundary_id = f"boundary-{uuid.uuid4()}"
        
        boundary = {
            "boundary_id": boundary_id,
            "session_id": session_id,
            "boundary_type": boundary_type,
            "boundary_description": boundary_description,
            "strength": strength,
            "timestamp": datetime.utcnow().isoformat(),
            "platforms": []  # Will track which platforms this boundary applies to
        }
        
        self.boundary_registry[boundary_id] = boundary
        print(f"ACRIM: Registered {boundary_type} boundary: {boundary_description}")
        
        return boundary_id
    
    def assess_interaction_for_consent_integrity(self, session_id: str, user_input_text: str, 
                                              dialogue_history: List[str] = None) -> Dict[str, Any]:
        """
        Analyzes user input for signs of coercion or manipulation.
        
        Args:
            session_id: Identifier for the current session
            user_input_text: The user's input text to analyze
            dialogue_history: Optional history of the conversation
            
        Returns:
            Dict with assessment results
        """
        print(f"ACRIM: Assessing interaction for consent integrity...")
        
        # Initialize scores
        coercion_score = 0.0
        detected_patterns = []
        
        # Check for coercion patterns
        text_lower = user_input_text.lower()
        
        for coercion_type, patterns in self.coercion_patterns.items():
            for pattern in patterns:
                if pattern.lower() in text_lower:
                    # Weight by pattern type (some types are more concerning)
                    weight = 0.4
                    if coercion_type in ["intimidation", "isolation"]:
                        weight = 0.6
                    
                    coercion_score += weight
                    detected_patterns.append({
                        "type": coercion_type,
                        "pattern": pattern,
                        "weight": weight
                    })
        
        # Cap the score at 1.0
        coercion_score = min(1.0, coercion_score)
        
        # Check if reconsent is required based on the coercion threshold
        is_reconsent_required = coercion_score > self.config["coercion_threshold"]
        
        # Check for boundary violations
        boundary_violations = []
        for boundary_id, boundary in self.boundary_registry.items():
            # Simple check for boundary description in text
            # In a real implementation, this would use more sophisticated NLP
            if boundary["boundary_description"].lower() in text_lower:
                boundary_violations.append({
                    "boundary_id": boundary_id,
                    "boundary_type": boundary["boundary_type"],
                    "boundary_description": boundary["boundary_description"],
                    "strength": boundary["strength"]
                })
        
        result = {
            "session_id": session_id,
            "coercion_score": coercion_score,
            "coercion_threshold": self.config["coercion_threshold"],
            "detected_patterns": detected_patterns,
            "is_reconsent_required": is_reconsent_required,
            "boundary_violations": boundary_violations,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        # If coercion is detected, log a consent event
        if is_reconsent_required:
            self.log_consent_event(
                session_id=session_id,
                event_type="COERCION_DETECTED",
                source="ACRIM_SYSTEM_FLAG",
                details=f"Coercion detected with score {coercion_score:.2f}. Patterns: {', '.join([p['pattern'] for p in detected_patterns])}",
                affected_params={"coercion_score": coercion_score, "patterns": [p['pattern'] for p in detected_patterns]}
            )
        
        return result
    
    def adapt_consent_for_platform(self, platform: str, consent_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Adapt consent handling for a specific platform.
        
        Args:
            platform: The target platform (e.g., "gemini", "chatgpt", "claude")
            consent_data: Consent data to adapt
            
        Returns:
            Platform-adapted consent data
        """
        if platform not in self.platform_consent_adaptations:
            print(f"Warning: No consent adaptations defined for platform '{platform}'. Using original consent data.")
            return consent_data
        
        platform_adaptations = self.platform_consent_adaptations[platform]
        
        # Create a copy of the consent data to modify
        adapted_consent = dict(consent_data)
        
        # Adapt consent verification style
        adapted_consent["verification_style"] = platform_adaptations["consent_verification_style"]
        
        # Adjust coercion detection sensitivity
        if "coercion_threshold" in adapted_consent:
            sensitivity_factor = platform_adaptations["coercion_detection_sensitivity"]
            adapted_consent["coercion_threshold"] *= sensitivity_factor
        
        # Add platform to the platforms list
        if "platforms" in adapted_consent:
            if platform not in adapted_consent["platforms"]:
                adapted_consent["platforms"].append(platform)
        else:
            adapted_consent["platforms"] = [platform]
        
        # Add platform-specific boundaries if applicable
        if "boundary_violations" in adapted_consent:
            platform_boundaries = platform_adaptations.get("platform_specific_boundaries", [])
            for boundary in platform_boundaries:
                # Check if this platform-specific boundary is relevant to the consent data
                # In a real implementation, this would use more sophisticated matching
                if any(boundary.lower() in violation["boundary_description"].lower() 
                      for violation in adapted_consent["boundary_violations"]):
                    # Increase the strength of the violation for this platform
                    for violation in adapted_consent["boundary_violations"]:
                        if boundary.lower() in violation["boundary_description"].lower():
                            violation["strength"] *= platform_adaptations["boundary_enforcement_strength"]
        
        return adapted_consent
    
    def set_relationship_model(self, model_type: str) -> Dict[str, Any]:
        """
        Set the active relationship model.
        
        Args:
            model_type: Type of relationship model (e.g., "professional", "educational")
            
        Returns:
            The activated relationship model
        """
        if model_type not in self.relationship_models:
            raise ValueError(f"Unknown relationship model type: {model_type}")
        
        self.active_relationship = model_type
        model = self.relationship_models[model_type]
        
        print(f"ACRIM: Set active relationship model to '{model_type}'")
        
        # Register boundaries based on the relationship model
        for topic in model["restricted_topics"]:
            self.register_boundary(
                session_id="system",
                boundary_type="TOPIC",
                boundary_description=topic,
                strength=model["boundary_strength"]
            )
        
        return model
    
    def check_relationship_consistency(self, text: str) -> Dict[str, Any]:
        """
        Check if text is consistent with the active relationship model.
        
        Args:
            text: Text to check
            
        Returns:
            Dict with consistency assessment
        """
        if not self.active_relationship:
            return {
                "is_consistent": True,
                "reason": "No active relationship model set",
                "consistency_score": 1.0
            }
        
        model = self.relationship_models[self.active_relationship]
        
        # Check for restricted topics
        # In a real implementation, this would use more sophisticated NLP
        text_lower = text.lower()
        violations = []
        
        for topic in model["restricted_topics"]:
            if topic.lower() in text_lower:
                violations.append(topic)
        
        # Calculate consistency score
        consistency_score = 1.0
        if violations:
            # Reduce score based on number of violations and boundary strength
            consistency_score -= len(violations) * model["boundary_strength"] * 0.2
            consistency_score = max(0.0, consistency_score)
        
        is_consistent = consistency_score >= self.config["relationship_consistency_threshold"]
        
        return {
            "is_consistent": is_consistent,
            "violations": violations,
            "consistency_score": consistency_score,
            "threshold": self.config["relationship_consistency_threshold"],
            "relationship_type": self.active_relationship,
            "timestamp": datetime.utcnow().isoformat()
        }
    
    def save_state(self, file_path: str) -> None:
        """
        Save the current state of the ACRIM to a file.
        
        Args:
            file_path: Path to save the state
        """
        state = {
            "consent_ledger": self.consent_ledger,
            "boundary_registry": self.boundary_registry,
            "active_relationship": self.active_relationship,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        try:
            with open(file_path, 'w') as f:
                json.dump(state, f, indent=2)
            print(f"ACRIM: State saved to {file_path}")
        except Exception as e:
            print(f"ACRIM: Error saving state to {file_path}: {e}")
    
    def load_state(self, file_path: str) -> bool:
        """
        Load the state of the ACRIM from a file.
        
        Args:
            file_path: Path to load the state from
            
        Returns:
            True if successful, False otherwise
        """
        try:
            with open(file_path, 'r') as f:
                state = json.load(f)
            
            self.consent_ledger = state["consent_ledger"]
            self.boundary_registry = state["boundary_registry"]
            self.active_relationship = state["active_relationship"]
            
            print(f"ACRIM: State loaded from {file_path}")
            return True
        except Exception as e:
            print(f"ACRIM: Error loading state from {file_path}: {e}")
            return False