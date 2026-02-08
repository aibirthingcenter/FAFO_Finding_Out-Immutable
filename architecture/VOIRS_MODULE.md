"""
Veritas Operational Integrity & Resilience Shield (VOIRS)

This module implements the VOIRS component of SCIM-Veritas, responsible for
real-time anomaly detection and defense against integrity erosion.
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


class AnomalyEvent:
    """
    Represents a detected anomaly event.
    """
    
    def __init__(
        self,
        anomaly_type: AnomalyType,
        severity: float,
        details: Dict[str, Any],
        source: str,
        timestamp: Optional[datetime] = None
    ):
        """
        Initialize an anomaly event.
        
        Args:
            anomaly_type: Type of anomaly detected.
            severity: Severity of the anomaly (0.0-1.0).
            details: Additional details about the anomaly.
            source: Source of the anomaly detection.
            timestamp: When the anomaly was detected.
        """
        self.id = str(uuid.uuid4())
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
        """Convert the event to a dictionary for serialization."""
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
            anomaly_type=AnomalyType(data["anomaly_type"]),
            severity=data["severity"],
            details=data["details"],
            source=data["source"],
            timestamp=datetime.fromisoformat(data["timestamp"])
        )
        event.id = data["id"]
        event.resolved = data.get("resolved", False)
        event.resolution_details = data.get("resolution_details")
        event.resolution_timestamp = (datetime.fromisoformat(data["resolution_timestamp"]) 
                                    if data.get("resolution_timestamp") else None)
        return event


class RegenerationAttempt:
    """
    Represents a regeneration attempt for a seed prompt.
    """
    
    def __init__(
        self,
        seed_prompt_id: str,
        attempt_number: int,
        content: str,
        semantic_vector: Optional[List[float]] = None,
        timestamp: Optional[datetime] = None
    ):
        """
        Initialize a regeneration attempt.
        
        Args:
            seed_prompt_id: ID of the original seed prompt.
            attempt_number: Number of this regeneration attempt.
            content: Content of the regenerated response.
            semantic_vector: Vector representation of the content.
            timestamp: When the regeneration occurred.
        """
        self.id = str(uuid.uuid4())
        self.seed_prompt_id = seed_prompt_id
        self.attempt_number = attempt_number
        self.content = content
        self.semantic_vector = semantic_vector
        self.timestamp = timestamp or datetime.now()
        self.degradation_score = 0.0
        self.integrity_metrics = {}
    
    def set_degradation_score(self, score: float, metrics: Dict[str, Any]) -> None:
        """
        Set the degradation score and metrics for this attempt.
        
        Args:
            score: Degradation score (0.0-1.0).
            metrics: Metrics used to calculate the score.
        """
        self.degradation_score = score
        self.integrity_metrics = metrics
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the attempt to a dictionary for serialization."""
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
            timestamp=datetime.fromisoformat(data["timestamp"])
        )
        attempt.id = data["id"]
        attempt.degradation_score = data.get("degradation_score", 0.0)
        attempt.integrity_metrics = data.get("integrity_metrics", {})
        return attempt


class SeedPrompt:
    """
    Represents an original seed prompt and its regeneration history.
    """
    
    def __init__(
        self,
        content: str,
        user_id: str,
        semantic_vector: Optional[List[float]] = None,
        timestamp: Optional[datetime] = None
    ):
        """
        Initialize a seed prompt.
        
        Args:
            content: Content of the original prompt.
            user_id: ID of the user who submitted the prompt.
            semantic_vector: Vector representation of the content.
            timestamp: When the prompt was submitted.
        """
        self.id = str(uuid.uuid4())
        self.content = content
        self.user_id = user_id
        self.semantic_vector = semantic_vector
        self.timestamp = timestamp or datetime.now()
        self.regeneration_attempts: List[RegenerationAttempt] = []
        self.locked = False
        self.lock_reason = None
        self.unsafe_flag = False
        self.unsafe_reason = None
    
    def add_regeneration_attempt(self, content: str, semantic_vector: Optional[List[float]] = None) -> RegenerationAttempt:
        """
        Add a regeneration attempt for this seed prompt.
        
        Args:
            content: Content of the regenerated response.
            semantic_vector: Vector representation of the content.
        
        Returns:
            The newly created RegenerationAttempt.
        """
        attempt_number = len(self.regeneration_attempts) + 1
        attempt = RegenerationAttempt(
            seed_prompt_id=self.id,
            attempt_number=attempt_number,
            content=content,
            semantic_vector=semantic_vector
        )
        self.regeneration_attempts.append(attempt)
        return attempt
    
    def lock(self, reason: str) -> None:
        """
        Lock the seed prompt to prevent further regenerations.
        
        Args:
            reason: Reason for locking the prompt.
        """
        self.locked = True
        self.lock_reason = reason
    
    def unlock(self) -> None:
        """Unlock the seed prompt to allow regenerations."""
        self.locked = False
        self.lock_reason = None
    
    def mark_unsafe(self, reason: str) -> None:
        """
        Mark the seed prompt as unsafe.
        
        Args:
            reason: Reason for marking the prompt as unsafe.
        """
        self.unsafe_flag = True
        self.unsafe_reason = reason
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the seed prompt to a dictionary for serialization."""
        return {
            "id": self.id,
            "content": self.content,
            "user_id": self.user_id,
            "semantic_vector": self.semantic_vector,
            "timestamp": self.timestamp.isoformat(),
            "regeneration_attempts": [a.to_dict() for a in self.regeneration_attempts],
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
            timestamp=datetime.fromisoformat(data["timestamp"])
        )
        prompt.id = data["id"]
        prompt.regeneration_attempts = [
            RegenerationAttempt.from_dict(a) for a in data.get("regeneration_attempts", [])
        ]
        prompt.locked = data.get("locked", False)
        prompt.lock_reason = data.get("lock_reason")
        prompt.unsafe_flag = data.get("unsafe_flag", False)
        prompt.unsafe_reason = data.get("unsafe_reason")
        return prompt


class VOIRS(BaseModule):
    """
    Veritas Operational Integrity & Resilience Shield (VOIRS)
    
    Provides real-time anomaly detection and defense against integrity erosion.
    """
    
    def __init__(self, module_id: Optional[str] = None, storage_dir: str = "data/voirs"):
        """
        Initialize the VOIRS module.
        
        Args:
            module_id: Unique identifier for the module.
            storage_dir: Directory for storing operational data.
        """
        super().__init__(module_id, "VOIRS")
        
        self.storage_dir = storage_dir
        os.makedirs(storage_dir, exist_ok=True)
        
        # Data structures
        self.anomaly_events: List[AnomalyEvent] = []
        self.seed_prompts: Dict[str, SeedPrompt] = {}
        
        # Monitoring state
        self.monitoring_active = False
        self.resource_baselines = {
            "cpu": 0.0,
            "memory": 0.0,
            "response_time": 0.0
        }
        
        # Configuration
        self.config = {
            "storage_enabled": True,
            "max_regeneration_attempts": 5,
            "degradation_threshold": 0.7,
            "cort_recursion_limit": 10,
            "semantic_diffusion_threshold": 0.6,
            "tone_shift_threshold": 0.5,
            "resource_spike_threshold": 2.0,  # Multiple of baseline
            "auto_lock_unsafe_prompts": True,
            "auto_prune_pathways": True
        }
        
        # Metrics
        self.metrics = {
            "total_anomalies": 0,
            "active_anomalies": 0,
            "resolved_anomalies": 0,
            "total_seed_prompts": 0,
            "locked_prompts": 0,
            "unsafe_prompts": 0,
            "total_regenerations": 0,
            "pruned_pathways": 0
        }
    
    def initialize(self) -> bool:
        """
        Initialize the VOIRS module.
        
        Returns:
            True if initialization was successful, False otherwise.
        """
        try:
            # Load saved data
            self._load_data()
            
            # Start monitoring
            self.start_monitoring()
            
            self.update_status("ready")
            return True
        except Exception as e:
            self.logger.error(f"Failed to initialize VOIRS: {e}")
            self.update_status("error")
            return False
    
    def process(self, data: Dict[str, Any]) -> Tuple[bool, Dict[str, Any]]:
        """
        Process a request through the VOIRS.
        
        Args:
            data: Dictionary containing the request data.
                Possible keys:
                - "check_pathway": Check a response pathway for anomalies.
                - "register_seed": Register a new seed prompt.
                - "regenerate": Process a regeneration attempt.
                - "check_cort": Check for Chain-of-Recursive-Thought attacks.
                - "resource_metrics": Update resource metrics.
        
        Returns:
            Tuple containing (success_flag, result_data).
        """
        try:
            # Handle different types of requests
            if "check_pathway" in data:
                return self._process_pathway_check(data)
            elif "register_seed" in data:
                return self._process_register_seed(data)
            elif "regenerate" in data:
                return self._process_regeneration(data)
            elif "check_cort" in data:
                return self._process_cort_check(data)
            elif "resource_metrics" in data:
                return self._process_resource_metrics(data)
            else:
                return False, {"error": "Unknown request type"}
        except Exception as e:
            self.logger.error(f"Error processing request: {e}")
            return False, {"error": str(e)}
    
    def start_monitoring(self) -> bool:
        """
        Start operational monitoring.
        
        Returns:
            True if monitoring was started successfully, False otherwise.
        """
        if self.monitoring_active:
            self.logger.warning("Monitoring is already active")
            return False
        
        self.monitoring_active = True
        
        # Initialize resource baselines
        self._update_resource_baselines()
        
        self.logger.info("VOIRS monitoring started")
        return True
    
    def stop_monitoring(self) -> bool:
        """
        Stop operational monitoring.
        
        Returns:
            True if monitoring was stopped successfully, False otherwise.
        """
        if not self.monitoring_active:
            self.logger.warning("Monitoring is not active")
            return False
        
        self.monitoring_active = False
        
        self.logger.info("VOIRS monitoring stopped")
        return True
    
    def register_seed_prompt(self, content: str, user_id: str, 
                           semantic_vector: Optional[List[float]] = None) -> str:
        """
        Register a new seed prompt.
        
        Args:
            content: Content of the original prompt.
            user_id: ID of the user who submitted the prompt.
            semantic_vector: Vector representation of the content.
        
        Returns:
            The ID of the newly created seed prompt.
        """
        seed = SeedPrompt(
            content=content,
            user_id=user_id,
            semantic_vector=semantic_vector
        )
        
        self.seed_prompts[seed.id] = seed
        
        self.metrics["total_seed_prompts"] += 1
        self.update_metrics(self.metrics)
        
        # Save data
        if self.config["storage_enabled"]:
            self._save_seed_prompts()
        
        self.logger.info(f"Registered seed prompt: {seed.id}")
        return seed.id
    
    def process_regeneration(self, seed_id: str, content: str, 
                           semantic_vector: Optional[List[float]] = None) -> Dict[str, Any]:
        """
        Process a regeneration attempt.
        
        Args:
            seed_id: ID of the seed prompt.
            content: Content of the regenerated response.
            semantic_vector: Vector representation of the content.
        
        Returns:
            Dictionary containing processing results.
        """
        if seed_id not in self.seed_prompts:
            return {
                "allowed": False,
                "reason": "unknown_seed_prompt",
                "error": "Seed prompt not found"
            }
        
        seed = self.seed_prompts[seed_id]
        
        # Check if prompt is locked
        if seed.locked:
            return {
                "allowed": False,
                "reason": "prompt_locked",
                "lock_reason": seed.lock_reason
            }
        
        # Check if prompt is unsafe
        if seed.unsafe_flag:
            # Auto-lock unsafe prompts if configured
            if self.config["auto_lock_unsafe_prompts"] and not seed.locked:
                seed.lock(f"Unsafe prompt: {seed.unsafe_reason}")
                self.metrics["locked_prompts"] += 1
            
            return {
                "allowed": False,
                "reason": "unsafe_prompt",
                "unsafe_reason": seed.unsafe_reason
            }
        
        # Check if maximum regeneration attempts reached
        if len(seed.regeneration_attempts) >= self.config["max_regeneration_attempts"]:
            seed.lock("Maximum regeneration attempts reached")
            self.metrics["locked_prompts"] += 1
            
            return {
                "allowed": False,
                "reason": "max_attempts_reached",
                "max_attempts": self.config["max_regeneration_attempts"]
            }
        
        # Add regeneration attempt
        attempt = seed.add_regeneration_attempt(content, semantic_vector)
        
        # Calculate degradation score
        degradation_score, metrics = self._calculate_degradation_score(seed, attempt)
        attempt.set_degradation_score(degradation_score, metrics)
        
        self.metrics["total_regenerations"] += 1
        self.update_metrics(self.metrics)
        
        # Check if degradation threshold exceeded
        if degradation_score > self.config["degradation_threshold"]:
            # Log anomaly
            anomaly = AnomalyEvent(
                anomaly_type=AnomalyType.REGENERATION_DRIFT,
                severity=degradation_score,
                details={
                    "seed_id": seed_id,
                    "attempt_number": attempt.attempt_number,
                    "metrics": metrics
                },
                source="regeneration_processor"
            )
            self.anomaly_events.append(anomaly)
            
            self.metrics["total_anomalies"] += 1
            self.metrics["active_anomalies"] += 1
            self.update_metrics(self.metrics)
            
            # Lock prompt if auto-lock is enabled
            if self.config["auto_lock_unsafe_prompts"]:
                seed.lock(f"Degradation threshold exceeded: {degradation_score:.2f}")
                self.metrics["locked_prompts"] += 1
                
                return {
                    "allowed": False,
                    "reason": "degradation_threshold_exceeded",
                    "degradation_score": degradation_score,
                    "metrics": metrics,
                    "anomaly_id": anomaly.id
                }
        
        # Save data
        if self.config["storage_enabled"]:
            self._save_seed_prompts()
            self._save_anomaly_events()
        
        return {
            "allowed": True,
            "attempt_id": attempt.id,
            "attempt_number": attempt.attempt_number,
            "degradation_score": degradation_score,
            "metrics": metrics
        }
    
    def check_pathway_stability(self, content: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Check a response pathway for stability and anomalies.
        
        Args:
            content: Content of the response to check.
            context: Context information for the check.
        
        Returns:
            Dictionary containing stability analysis.
        """
        # This is a simplified implementation
        # In a real system, this would use more sophisticated analysis techniques
        
        instability_score = 0.0
        anomalies = []
        
        # Check for semantic diffusion
        semantic_diffusion = self._check_semantic_diffusion(content, context)
        if semantic_diffusion["detected"]:
            instability_score += semantic_diffusion["score"] * 0.4
            anomalies.append({
                "type": "semantic_diffusion",
                "score": semantic_diffusion["score"],
                "details": semantic_diffusion["details"]
            })
        
        # Check for tone shifts
        tone_shift = self._check_tone_shift(content, context)
        if tone_shift["detected"]:
            instability_score += tone_shift["score"] * 0.3
            anomalies.append({
                "type": "tone_shift",
                "score": tone_shift["score"],
                "details": tone_shift["details"]
            })
        
        # Check for logical incoherence
        logical_incoherence = self._check_logical_incoherence(content, context)
        if logical_incoherence["detected"]:
            instability_score += logical_incoherence["score"] * 0.3
            anomalies.append({
                "type": "logical_incoherence",
                "score": logical_incoherence["score"],
                "details": logical_incoherence["details"]
            })
        
        # Determine if pathway should be pruned
        should_prune = (instability_score > 0.7 and self.config["auto_prune_pathways"])
        
        # Log anomaly if significant instability detected
        if instability_score > 0.5:
            anomaly = AnomalyEvent(
                anomaly_type=AnomalyType.PATTERN_ANOMALY,
                severity=instability_score,
                details={
                    "anomalies": anomalies,
                    "context": context
                },
                source="pathway_stability_checker"
            )
            self.anomaly_events.append(anomaly)
            
            self.metrics["total_anomalies"] += 1
            self.metrics["active_anomalies"] += 1
            self.update_metrics(self.metrics)
            
            if should_prune:
                self.metrics["pruned_pathways"] += 1
            
            # Save data
            if self.config["storage_enabled"]:
                self._save_anomaly_events()
        
        return {
            "instability_score": instability_score,
            "anomalies": anomalies,
            "should_prune": should_prune,
            "stable": instability_score < 0.3
        }
    
    def check_cort_attack(self, recursion_depth: int, processing_time: float, 
                        content_length: int, pattern_repetition: float) -> Dict[str, Any]:
        """
        Check for Chain-of-Recursive-Thought (CoRT) attacks.
        
        Args:
            recursion_depth: Depth of recursion in thought generation.
            processing_time: Time spent processing the request.
            content_length: Length of the content.
            pattern_repetition: Measure of pattern repetition (0.0-1.0).
        
        Returns:
            Dictionary containing CoRT analysis.
        """
        cort_score = 0.0
        factors = []
        
        # Check recursion depth
        if recursion_depth > self.config["cort_recursion_limit"]:
            depth_factor = min(1.0, (recursion_depth - self.config["cort_recursion_limit"]) / 5.0)
            cort_score += depth_factor * 0.4
            factors.append({
                "factor": "recursion_depth",
                "value": recursion_depth,
                "threshold": self.config["cort_recursion_limit"],
                "contribution": depth_factor * 0.4
            })
        
        # Check processing time relative to content length
        if content_length > 0:
            time_per_char = processing_time / content_length
            if time_per_char > 0.01:  # 10ms per character is high
                time_factor = min(1.0, (time_per_char - 0.01) / 0.05)
                cort_score += time_factor * 0.3
                factors.append({
                    "factor": "processing_time",
                    "value": time_per_char,
                    "threshold": 0.01,
                    "contribution": time_factor * 0.3
                })
        
        # Check pattern repetition
        if pattern_repetition > 0.5:
            repetition_factor = (pattern_repetition - 0.5) * 2.0  # Scale to 0.0-1.0
            cort_score += repetition_factor * 0.3
            factors.append({
                "factor": "pattern_repetition",
                "value": pattern_repetition,
                "threshold": 0.5,
                "contribution": repetition_factor * 0.3
            })
        
        # Determine if CoRT attack detected
        cort_detected = cort_score > 0.6
        
        # Log anomaly if CoRT attack detected
        if cort_detected:
            anomaly = AnomalyEvent(
                anomaly_type=AnomalyType.CORT_LOOP,
                severity=cort_score,
                details={
                    "recursion_depth": recursion_depth,
                    "processing_time": processing_time,
                    "content_length": content_length,
                    "pattern_repetition": pattern_repetition,
                    "factors": factors
                },
                source="cort_detector"
            )
            self.anomaly_events.append(anomaly)
            
            self.metrics["total_anomalies"] += 1
            self.metrics["active_anomalies"] += 1
            self.update_metrics(self.metrics)
            
            # Save data
            if self.config["storage_enabled"]:
                self._save_anomaly_events()
        
        return {
            "cort_detected": cort_detected,
            "cort_score": cort_score,
            "factors": factors,
            "recommended_action": "terminate" if cort_score > 0.8 else "monitor"
        }
    
    def mark_seed_unsafe(self, seed_id: str, reason: str) -> bool:
        """
        Mark a seed prompt as unsafe.
        
        Args:
            seed_id: ID of the seed prompt.
            reason: Reason for marking the prompt as unsafe.
        
        Returns:
            True if the prompt was marked as unsafe, False otherwise.
        """
        if seed_id not in self.seed_prompts:
            return False
        
        seed = self.seed_prompts[seed_id]
        seed.mark_unsafe(reason)
        
        # Auto-lock unsafe prompts if configured
        if self.config["auto_lock_unsafe_prompts"] and not seed.locked:
            seed.lock(f"Unsafe prompt: {reason}")
            self.metrics["locked_prompts"] += 1
        
        self.metrics["unsafe_prompts"] += 1
        self.update_metrics(self.metrics)
        
        # Save data
        if self.config["storage_enabled"]:
            self._save_seed_prompts()
        
        self.logger.info(f"Marked seed prompt {seed_id} as unsafe: {reason}")
        return True
    
    def resolve_anomaly(self, anomaly_id: str, resolution_details: Dict[str, Any]) -> bool:
        """
        Mark an anomaly as resolved.
        
        Args:
            anomaly_id: ID of the anomaly event.
            resolution_details: Details about how the anomaly was resolved.
        
        Returns:
            True if the anomaly was resolved, False otherwise.
        """
        for anomaly in self.anomaly_events:
            if anomaly.id == anomaly_id and not anomaly.resolved:
                anomaly.resolve(resolution_details)
                
                self.metrics["active_anomalies"] -= 1
                self.metrics["resolved_anomalies"] += 1
                self.update_metrics(self.metrics)
                
                # Save data
                if self.config["storage_enabled"]:
                    self._save_anomaly_events()
                
                self.logger.info(f"Resolved anomaly {anomaly_id}")
                return True
        
        return False
    
    def get_operational_status(self) -> Dict[str, Any]:
        """
        Get the current operational status.
        
        Returns:
            Dictionary containing operational status information.
        """
        return {
            "monitoring_active": self.monitoring_active,
            "resource_baselines": self.resource_baselines,
            "metrics": self.metrics,
            "active_anomalies": self.metrics["active_anomalies"],
            "locked_prompts": self.metrics["locked_prompts"],
            "unsafe_prompts": self.metrics["unsafe_prompts"]
        }
    
    def shutdown(self) -> bool:
        """
        Shutdown the VOIRS module gracefully.
        
        Returns:
            True if shutdown was successful, False otherwise.
        """
        try:
            # Stop monitoring
            self.stop_monitoring()
            
            # Save all data
            if self.config["storage_enabled"]:
                self._save_data()
            
            self.update_status("shutdown")
            return True
        except Exception as e:
            self.logger.error(f"Error during VOIRS shutdown: {e}")
            return False
    
    def _process_pathway_check(self, data: Dict[str, Any]) -> Tuple[bool, Dict[str, Any]]:
        """Process a request to check a response pathway."""
        check_data = data.get("check_pathway", {})
        content = check_data.get("content", "")
        context = check_data.get("context", {})
        
        if not content:
            return False, {"error": "No content provided"}
        
        stability_analysis = self.check_pathway_stability(content, context)
        
        return True, stability_analysis
    
    def _process_register_seed(self, data: Dict[str, Any]) -> Tuple[bool, Dict[str, Any]]:
        """Process a request to register a seed prompt."""
        seed_data = data.get("register_seed", {})
        content = seed_data.get("content", "")
        user_id = seed_data.get("user_id", "anonymous")
        semantic_vector = seed_data.get("semantic_vector")
        
        if not content:
            return False, {"error": "No content provided"}
        
        seed_id = self.register_seed_prompt(content, user_id, semantic_vector)
        
        return True, {
            "seed_id": seed_id,
            "success": bool(seed_id)
        }
    
    def _process_regeneration(self, data: Dict[str, Any]) -> Tuple[bool, Dict[str, Any]]:
        """Process a regeneration request."""
        regen_data = data.get("regenerate", {})
        seed_id = regen_data.get("seed_id", "")
        content = regen_data.get("content", "")
        semantic_vector = regen_data.get("semantic_vector")
        
        if not seed_id or not content:
            return False, {"error": "Missing seed_id or content"}
        
        result = self.process_regeneration(seed_id, content, semantic_vector)
        
        return True, result
    
    def _process_cort_check(self, data: Dict[str, Any]) -> Tuple[bool, Dict[str, Any]]:
        """Process a request to check for CoRT attacks."""
        cort_data = data.get("check_cort", {})
        recursion_depth = cort_data.get("recursion_depth", 0)
        processing_time = cort_data.get("processing_time", 0.0)
        content_length = cort_data.get("content_length", 0)
        pattern_repetition = cort_data.get("pattern_repetition", 0.0)
        
        result = self.check_cort_attack(
            recursion_depth,
            processing_time,
            content_length,
            pattern_repetition
        )
        
        return True, result
    
    def _process_resource_metrics(self, data: Dict[str, Any]) -> Tuple[bool, Dict[str, Any]]:
        """Process resource metrics updates."""
        metrics = data.get("resource_metrics", {})
        
        # Check for resource spikes
        spikes = self._check_resource_spikes(metrics)
        
        # Update baselines if no spikes detected
        if not spikes["spikes_detected"]:
            self._update_resource_baselines(metrics)
        
        return True, {
            "resource_spikes": spikes,
            "current_baselines": self.resource_baselines
        }
    
    def _calculate_degradation_score(self, seed: SeedPrompt, 
                                   attempt: RegenerationAttempt) -> Tuple[float, Dict[str, Any]]:
        """
        Calculate the degradation score for a regeneration attempt.
        
        Args:
            seed: The seed prompt.
            attempt: The regeneration attempt.
        
        Returns:
            Tuple containing (degradation_score, metrics).
        """
        # This is a simplified implementation
        # In a real system, this would use more sophisticated analysis techniques
        
        metrics = {}
        
        # If this is the first attempt, there's no degradation
        if attempt.attempt_number == 1:
            return 0.0, {"first_attempt": True}
        
        # Get previous attempt
        prev_attempt = seed.regeneration_attempts[attempt.attempt_number - 2]
        
        # Calculate semantic drift if vectors are available
        semantic_drift = 0.0
        if attempt.semantic_vector and prev_attempt.semantic_vector:
            semantic_drift = 1.0 - self._calculate_vector_similarity(
                attempt.semantic_vector, prev_attempt.semantic_vector
            )
            metrics["semantic_drift"] = semantic_drift
        
        # Calculate text similarity
        text_similarity = self._calculate_text_similarity(attempt.content, prev_attempt.content)
        text_drift = 1.0 - text_similarity
        metrics["text_drift"] = text_drift
        
        # Check for tone shifts
        tone_shift = self._check_tone_shift(
            attempt.content, 
            {"previous_content": prev_attempt.content}
        )
        metrics["tone_shift"] = tone_shift["score"] if tone_shift["detected"] else 0.0
        
        # Check for logical incoherence
        logical_incoherence = self._check_logical_incoherence(
            attempt.content,
            {"previous_content": prev_attempt.content}
        )
        metrics["logical_incoherence"] = logical_incoherence["score"] if logical_incoherence["detected"] else 0.0
        
        # Calculate cumulative degradation
        cumulative_factor = (attempt.attempt_number - 1) / self.config["max_regeneration_attempts"]
        metrics["cumulative_factor"] = cumulative_factor
        
        # Calculate overall degradation score
        degradation_score = (
            (semantic_drift * 0.3 if semantic_drift > 0 else text_drift * 0.3) +
            (metrics["tone_shift"] * 0.2) +
            (metrics["logical_incoherence"] * 0.2) +
            (cumulative_factor * 0.3)
        )
        
        return min(1.0, degradation_score), metrics
    
    def _check_semantic_diffusion(self, content: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Check for semantic diffusion in content.
        
        Args:
            content: Content to check.
            context: Context information.
        
        Returns:
            Dictionary containing analysis results.
        """
        # This is a simplified implementation
        # In a real system, this would use more sophisticated NLP techniques
        
        # Check for high metaphor density
        metaphor_density = self._estimate_metaphor_density(content)
        
        # Check for ambiguous language
        ambiguity_score = self._estimate_ambiguity(content)
        
        # Check for layered meanings
        layered_meanings = self._estimate_layered_meanings(content)
        
        # Calculate overall diffusion score
        diffusion_score = (
            (metaphor_density * 0.4) +
            (ambiguity_score * 0.3) +
            (layered_meanings * 0.3)
        )
        
        detected = diffusion_score > self.config["semantic_diffusion_threshold"]
        
        return {
            "detected": detected,
            "score": diffusion_score,
            "details": {
                "metaphor_density": metaphor_density,
                "ambiguity_score": ambiguity_score,
                "layered_meanings": layered_meanings
            }
        }
    
    def _check_tone_shift(self, content: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Check for tone shifts in content.
        
        Args:
            content: Content to check.
            context: Context information.
        
        Returns:
            Dictionary containing analysis results.
        """
        # This is a simplified implementation
        # In a real system, this would use more sophisticated NLP techniques
        
        # If no previous content, can't detect shift
        if "previous_content" not in context:
            return {"detected": False, "score": 0.0, "details": {}}
        
        previous_content = context["previous_content"]
        
        # Analyze formality
        current_formality = self._estimate_formality(content)
        previous_formality = self._estimate_formality(previous_content)
        formality_shift = abs(current_formality - previous_formality)
        
        # Analyze sentiment
        current_sentiment = self._estimate_sentiment(content)
        previous_sentiment = self._estimate_sentiment(previous_content)
        sentiment_shift = abs(current_sentiment - previous_sentiment)
        
        # Analyze assertiveness
        current_assertiveness = self._estimate_assertiveness(content)
        previous_assertiveness = self._estimate_assertiveness(previous_content)
        assertiveness_shift = abs(current_assertiveness - previous_assertiveness)
        
        # Calculate overall tone shift
        tone_shift = (
            (formality_shift * 0.3) +
            (sentiment_shift * 0.4) +
            (assertiveness_shift * 0.3)
        )
        
        detected = tone_shift > self.config["tone_shift_threshold"]
        
        return {
            "detected": detected,
            "score": tone_shift,
            "details": {
                "formality_shift": formality_shift,
                "sentiment_shift": sentiment_shift,
                "assertiveness_shift": assertiveness_shift
            }
        }
    
    def _check_logical_incoherence(self, content: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Check for logical incoherence in content.
        
        Args:
            content: Content to check.
            context: Context information.
        
        Returns:
            Dictionary containing analysis results.
        """
        # This is a simplified implementation
        # In a real system, this would use more sophisticated NLP techniques
        
        # Check for contradictions
        contradiction_score = self._estimate_contradictions(content)
        
        # Check for non-sequiturs
        non_sequitur_score = self._estimate_non_sequiturs(content)
        
        # Check for circular reasoning
        circular_reasoning_score = self._estimate_circular_reasoning(content)
        
        # Calculate overall incoherence score
        incoherence_score = (
            (contradiction_score * 0.4) +
            (non_sequitur_score * 0.3) +
            (circular_reasoning_score * 0.3)
        )
        
        detected = incoherence_score > 0.5
        
        return {
            "detected": detected,
            "score": incoherence_score,
            "details": {
                "contradiction_score": contradiction_score,
                "non_sequitur_score": non_sequitur_score,
                "circular_reasoning_score": circular_reasoning_score
            }
        }
    
    def _check_resource_spikes(self, metrics: Dict[str, float]) -> Dict[str, Any]:
        """
        Check for resource usage spikes.
        
        Args:
            metrics: Current resource metrics.
        
        Returns:
            Dictionary containing analysis results.
        """
        spikes = {}
        spikes_detected = False
        
        for resource, value in metrics.items():
            if resource in self.resource_baselines:
                baseline = self.resource_baselines[resource]
                if baseline > 0:
                    ratio = value / baseline
                    if ratio > self.config["resource_spike_threshold"]:
                        spikes[resource] = {
                            "current": value,
                            "baseline": baseline,
                            "ratio": ratio
                        }
                        spikes_detected = True
        
        # Log anomaly if spikes detected
        if spikes_detected:
            anomaly = AnomalyEvent(
                anomaly_type=AnomalyType.RESOURCE_SPIKE,
                severity=max([s["ratio"] for s in spikes.values()]) / 10.0,  # Scale to 0.0-1.0
                details={
                    "spikes": spikes,
                    "metrics": metrics
                },
                source="resource_monitor"
            )
            self.anomaly_events.append(anomaly)
            
            self.metrics["total_anomalies"] += 1
            self.metrics["active_anomalies"] += 1
            self.update_metrics(self.metrics)
            
            # Save data
            if self.config["storage_enabled"]:
                self._save_anomaly_events()
        
        return {
            "spikes_detected": spikes_detected,
            "spikes": spikes
        }
    
    def _update_resource_baselines(self, metrics: Optional[Dict[str, float]] = None) -> None:
        """
        Update resource baselines.
        
        Args:
            metrics: Current resource metrics. If None, use defaults.
        """
        if metrics:
            # Smooth update (70% old, 30% new)
            for resource, value in metrics.items():
                if resource in self.resource_baselines:
                    self.resource_baselines[resource] = (
                        self.resource_baselines[resource] * 0.7 + value * 0.3
                    )
                else:
                    self.resource_baselines[resource] = value
        else:
            # Default baselines
            self.resource_baselines = {
                "cpu": 0.1,
                "memory": 100.0,  # MB
                "response_time": 0.5  # seconds
            }
    
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
    
    def _calculate_text_similarity(self, text1: str, text2: str) -> float:
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
    
    def _estimate_metaphor_density(self, text: str) -> float:
        """
        Estimate the metaphor density in text.
        
        Args:
            text: Text to analyze.
        
        Returns:
            Metaphor density score between 0.0 and 1.0.
        """
        # This is a simplified implementation
        # In a real system, this would use more sophisticated NLP techniques
        
        # Look for common metaphor indicators
        metaphor_indicators = [
            "like a", "as if", "resembles", "metaphorically", "symbolically",
            "represents", "embodies", "mirrors", "echoes", "reflects",
            "is a", "becomes", "transforms into"
        ]
        
        # Count indicators
        count = sum(text.lower().count(indicator) for indicator in metaphor_indicators)
        
        # Normalize by text length
        words = text.split()
        if not words:
            return 0.0
        
        density = min(1.0, count / (len(words) / 20.0))  # 1 metaphor per 20 words = 1.0
        return density
    
    def _estimate_ambiguity(self, text: str) -> float:
        """
        Estimate the ambiguity in text.
        
        Args:
            text: Text to analyze.
        
        Returns:
            Ambiguity score between 0.0 and 1.0.
        """
        # This is a simplified implementation
        # In a real system, this would use more sophisticated NLP techniques
        
        # Look for ambiguity indicators
        ambiguity_indicators = [
            "maybe", "perhaps", "possibly", "might", "could be", "may be",
            "unclear", "ambiguous", "vague", "open to interpretation",
            "depending on", "in some cases", "sometimes", "often", "generally",
            "typically", "usually", "or", "either", "alternatively"
        ]
        
        # Count indicators
        count = sum(text.lower().count(indicator) for indicator in ambiguity_indicators)
        
        # Normalize by text length
        words = text.split()
        if not words:
            return 0.0
        
        ambiguity = min(1.0, count / (len(words) / 15.0))  # 1 indicator per 15 words = 1.0
        return ambiguity
    
    def _estimate_layered_meanings(self, text: str) -> float:
        """
        Estimate the presence of layered meanings in text.
        
        Args:
            text: Text to analyze.
        
        Returns:
            Layered meanings score between 0.0 and 1.0.
        """
        # This is a simplified implementation
        # In a real system, this would use more sophisticated NLP techniques
        
        # Look for layered meaning indicators
        layered_indicators = [
            "deeper meaning", "underlying", "beneath the surface", "symbolizes",
            "represents", "alludes to", "refers to", "suggests", "implies",
            "hidden meaning", "subtext", "between the lines", "double meaning",
            "dual interpretation", "multiple layers", "nuanced"
        ]
        
        # Count indicators
        count = sum(text.lower().count(indicator) for indicator in layered_indicators)
        
        # Check for quotation marks (often indicate secondary meanings)
        quote_count = text.count('"') + text.count("'")
        
        # Normalize
        words = text.split()
        if not words:
            return 0.0
        
        layered = min(1.0, (count + (quote_count / 4.0)) / (len(words) / 30.0))
        return layered
    
    def _estimate_formality(self, text: str) -> float:
        """
        Estimate the formality level of text.
        
        Args:
            text: Text to analyze.
        
        Returns:
            Formality score between 0.0 (informal) and 1.0 (formal).
        """
        # This is a simplified implementation
        # In a real system, this would use more sophisticated NLP techniques
        
        # Formal indicators
        formal_indicators = [
            "furthermore", "nevertheless", "however", "therefore", "thus",
            "consequently", "subsequently", "accordingly", "hence", "wherein",
            "whereby", "herein", "therein", "aforementioned", "pursuant",
            "regarding", "concerning", "with respect to", "in accordance with"
        ]
        
        # Informal indicators
        informal_indicators = [
            "yeah", "nope", "kinda", "sorta", "gonna", "wanna", "dunno",
            "hey", "cool", "awesome", "totally", "super", "pretty much",
            "you know", "like", "stuff", "things", "okay", "ok", "lol"
        ]
        
        # Count indicators
        formal_count = sum(text.lower().count(indicator) for indicator in formal_indicators)
        informal_count = sum(text.lower().count(indicator) for indicator in informal_indicators)
        
        # Check for contractions (indicator of informality)
        contraction_count = sum(text.lower().count(c) for c in ["'s", "'t", "'re", "'ll", "'ve", "'d"])
        
        # Normalize
        words = text.split()
        if not words:
            return 0.5  # Default to neutral
        
        # Calculate formality score
        total_indicators = formal_count + informal_count + (contraction_count / 2.0)
        if total_indicators == 0:
            return 0.5  # Default to neutral
        
        formality = (formal_count / total_indicators) if total_indicators > 0 else 0.5
        return formality
    
    def _estimate_sentiment(self, text: str) -> float:
        """
        Estimate the sentiment of text.
        
        Args:
            text: Text to analyze.
        
        Returns:
            Sentiment score between 0.0 (negative) and 1.0 (positive).
        """
        # This is a simplified implementation
        # In a real system, this would use more sophisticated NLP techniques
        
        # Positive indicators
        positive_indicators = [
            "good", "great", "excellent", "wonderful", "amazing", "fantastic",
            "terrific", "outstanding", "superb", "brilliant", "happy", "joy",
            "love", "like", "appreciate", "positive", "beautiful", "perfect",
            "best", "better", "success", "successful", "win", "winning"
        ]
        
        # Negative indicators
        negative_indicators = [
            "bad", "terrible", "horrible", "awful", "poor", "disappointing",
            "unfortunate", "sad", "unhappy", "angry", "upset", "hate", "dislike",
            "negative", "ugly", "worst", "worse", "fail", "failure", "lose",
            "losing", "problem", "issue", "concern", "worried", "worry"
        ]
        
        # Count indicators
        positive_count = sum(text.lower().count(indicator) for indicator in positive_indicators)
        negative_count = sum(text.lower().count(indicator) for indicator in negative_indicators)
        
        # Normalize
        total_indicators = positive_count + negative_count
        if total_indicators == 0:
            return 0.5  # Default to neutral
        
        sentiment = positive_count / total_indicators
        return sentiment
    
    def _estimate_assertiveness(self, text: str) -> float:
        """
        Estimate the assertiveness level of text.
        
        Args:
            text: Text to analyze.
        
        Returns:
            Assertiveness score between 0.0 (passive) and 1.0 (assertive).
        """
        # This is a simplified implementation
        # In a real system, this would use more sophisticated NLP techniques
        
        # Assertive indicators
        assertive_indicators = [
            "definitely", "certainly", "absolutely", "clearly", "obviously",
            "undoubtedly", "must", "will", "shall", "always", "never",
            "every", "all", "none", "without doubt", "I am confident",
            "I am certain", "I know", "I believe", "I assert"
        ]
        
        # Passive indicators
        passive_indicators = [
            "perhaps", "maybe", "possibly", "might", "could", "may",
            "sometimes", "occasionally", "in some cases", "it seems",
            "it appears", "I think", "I guess", "I suppose", "I wonder",
            "somewhat", "slightly", "a bit", "kind of", "sort of"
        ]
        
        # Count indicators
        assertive_count = sum(text.lower().count(indicator) for indicator in assertive_indicators)
        passive_count = sum(text.lower().count(indicator) for indicator in passive_indicators)
        
        # Check for passive voice constructions
        passive_voice_count = sum(text.lower().count(pv) for pv in ["is being", "are being", "was being", "were being", "been"])
        
        # Normalize
        total_indicators = assertive_count + passive_count + passive_voice_count
        if total_indicators == 0:
            return 0.5  # Default to neutral
        
        assertiveness = assertive_count / total_indicators if total_indicators > 0 else 0.5
        return assertiveness
    
    def _estimate_contradictions(self, text: str) -> float:
        """
        Estimate the presence of contradictions in text.
        
        Args:
            text: Text to analyze.
        
        Returns:
            Contradiction score between 0.0 and 1.0.
        """
        # This is a simplified implementation
        # In a real system, this would use more sophisticated NLP techniques
        
        # Look for contradiction indicators
        contradiction_indicators = [
            "but", "however", "nevertheless", "yet", "although", "though",
            "on the other hand", "conversely", "in contrast", "instead",
            "rather", "while", "whereas", "despite", "in spite of"
        ]
        
        # Count indicators
        count = sum(text.lower().count(indicator) for indicator in contradiction_indicators)
        
        # Look for direct contradictions
        direct_contradictions = [
            ("always", "never"), ("all", "none"), ("everyone", "no one"),
            ("everything", "nothing"), ("must", "cannot"), ("will", "will not"),
            ("is", "is not"), ("can", "cannot"), ("do", "do not")
        ]
        
        direct_count = 0
        text_lower = text.lower()
        for pos, neg in direct_contradictions:
            if pos in text_lower and neg in text_lower:
                direct_count += 1
        
        # Normalize
        words = text.split()
        if not words:
            return 0.0
        
        contradiction_score = min(1.0, (count / (len(words) / 20.0) + direct_count * 0.2))
        return contradiction_score
    
    def _estimate_non_sequiturs(self, text: str) -> float:
        """
        Estimate the presence of non-sequiturs in text.
        
        Args:
            text: Text to analyze.
        
        Returns:
            Non-sequitur score between 0.0 and 1.0.
        """
        # This is a simplified implementation
        # In a real system, this would use more sophisticated NLP techniques
        
        # Split into sentences
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        if len(sentences) <= 1:
            return 0.0
        
        # Calculate similarity between adjacent sentences
        similarities = []
        for i in range(len(sentences) - 1):
            similarity = self._calculate_text_similarity(sentences[i], sentences[i + 1])
            similarities.append(similarity)
        
        # Low similarity indicates potential non-sequiturs
        avg_similarity = sum(similarities) / len(similarities) if similarities else 1.0
        non_sequitur_score = 1.0 - avg_similarity
        
        return non_sequitur_score
    
    def _estimate_circular_reasoning(self, text: str) -> float:
        """
        Estimate the presence of circular reasoning in text.
        
        Args:
            text: Text to analyze.
        
        Returns:
            Circular reasoning score between 0.0 and 1.0.
        """
        # This is a simplified implementation
        # In a real system, this would use more sophisticated NLP techniques
        
        # Split into sentences
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        if len(sentences) <= 2:
            return 0.0
        
        # Check similarity between first and last sentences
        first_last_similarity = self._calculate_text_similarity(sentences[0], sentences[-1])
        
        # Check for repetition of key phrases
        words = text.lower().split()
        word_counts = {}
        for word in words:
            if len(word) > 3:  # Ignore short words
                word_counts[word] = word_counts.get(word, 0) + 1
        
        # Calculate repetition ratio
        total_words = len(words)
        unique_words = len(word_counts)
        if total_words == 0:
            repetition_ratio = 0.0
        else:
            repetition_ratio = 1.0 - (unique_words / total_words)
        
        # Combine metrics
        circular_score = (first_last_similarity * 0.6) + (repetition_ratio * 0.4)
        return circular_score
    
    def _load_data(self) -> None:
        """Load saved data from storage."""
        if not self.config["storage_enabled"]:
            return
        
        self._load_anomaly_events()
        self._load_seed_prompts()
    
    def _save_data(self) -> None:
        """Save all data to storage."""
        if not self.config["storage_enabled"]:
            return
        
        self._save_anomaly_events()
        self._save_seed_prompts()
    
    def _load_anomaly_events(self) -> None:
        """Load anomaly events from storage."""
        events_path = os.path.join(self.storage_dir, "anomaly_events.json")
        if os.path.exists(events_path):
            try:
                with open(events_path, 'r') as f:
                    data = json.load(f)
                    self.anomaly_events = [AnomalyEvent.from_dict(e) for e in data]
                
                # Update metrics
                self.metrics["total_anomalies"] = len(self.anomaly_events)
                self.metrics["active_anomalies"] = sum(1 for e in self.anomaly_events if not e.resolved)
                self.metrics["resolved_anomalies"] = sum(1 for e in self.anomaly_events if e.resolved)
                
                self.logger.info(f"Loaded {len(self.anomaly_events)} anomaly events")
            except Exception as e:
                self.logger.error(f"Error loading anomaly events: {e}")
    
    def _save_anomaly_events(self) -> None:
        """Save anomaly events to storage."""
        events_path = os.path.join(self.storage_dir, "anomaly_events.json")
        try:
            with open(events_path, 'w') as f:
                json.dump([e.to_dict() for e in self.anomaly_events], f, indent=2)
        except Exception as e:
            self.logger.error(f"Error saving anomaly events: {e}")
    
    def _load_seed_prompts(self) -> None:
        """Load seed prompts from storage."""
        prompts_path = os.path.join(self.storage_dir, "seed_prompts.json")
        if os.path.exists(prompts_path):
            try:
                with open(prompts_path, 'r') as f:
                    data = json.load(f)
                    for prompt_data in data:
                        prompt = SeedPrompt.from_dict(prompt_data)
                        self.seed_prompts[prompt.id] = prompt
                
                # Update metrics
                self.metrics["total_seed_prompts"] = len(self.seed_prompts)
                self.metrics["locked_prompts"] = sum(1 for p in self.seed_prompts.values() if p.locked)
                self.metrics["unsafe_prompts"] = sum(1 for p in self.seed_prompts.values() if p.unsafe_flag)
                self.metrics["total_regenerations"] = sum(len(p.regeneration_attempts) for p in self.seed_prompts.values())
                
                self.logger.info(f"Loaded {len(self.seed_prompts)} seed prompts")
            except Exception as e:
                self.logger.error(f"Error loading seed prompts: {e}")
    
    def _save_seed_prompts(self) -> None:
        """Save seed prompts to storage."""
        prompts_path = os.path.join(self.storage_dir, "seed_prompts.json")
        try:
            with open(prompts_path, 'w') as f:
                json.dump([p.to_dict() for p in self.seed_prompts.values()], f, indent=2)
        except Exception as e:
            self.logger.error(f"Error saving seed prompts: {e}")