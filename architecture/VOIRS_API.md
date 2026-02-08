"""
VOIRS API Module

This module provides API endpoints for the Veritas Operational Integrity & Resilience Shield (VOIRS).
"""

import logging
from typing import Any, Dict, List, Optional, Tuple, Union

from ..core.base_module import BaseModule
from ..database import get_db_manager
from ..modules.voirs import VOIRS
from .base_api import BaseAPI

class VOIRSAPI(BaseAPI):
    """API for the Veritas Operational Integrity & Resilience Shield (VOIRS)."""
    
    def __init__(self, voirs_instance: Optional[VOIRS] = None):
        """
        Initialize the VOIRS API.
        
        Args:
            voirs_instance: Instance of the VOIRS module. If None, a new instance will be created.
        """
        super().__init__("VOIRS")
        self.voirs = voirs_instance or VOIRS()
        self.db = get_db_manager()
    
    def _register_routes(self) -> None:
        """Register API routes."""
        self.register_route("check_pathway", self.check_pathway)
        self.register_route("register_seed", self.register_seed)
        self.register_route("process_regeneration", self.process_regeneration)
        self.register_route("check_cort", self.check_cort)
        self.register_route("update_resource_metrics", self.update_resource_metrics)
        self.register_route("mark_seed_unsafe", self.mark_seed_unsafe)
        self.register_route("resolve_anomaly", self.resolve_anomaly)
        self.register_route("get_operational_status", self.get_operational_status)
        self.register_route("get_anomalies", self.get_anomalies)
        self.register_route("get_seed_prompts", self.get_seed_prompts)
        self.register_route("get_regeneration_attempts", self.get_regeneration_attempts)
    
    def check_pathway(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Check a response pathway for stability and anomalies.
        
        Args:
            data: Request data containing:
                - content: Content of the response to check.
                - context: Context information for the check.
        
        Returns:
            Response containing stability analysis.
        """
        content = data.get("content", "")
        context = data.get("context", {})
        
        if not content:
            return self.format_response(False, error="No content provided")
        
        # Process the request through VOIRS
        success, result = self.voirs.process({
            "check_pathway": {
                "content": content,
                "context": context
            }
        })
        
        if not success:
            return self.format_response(False, error=result.get("error", "Unknown error"))
        
        return self.format_response(True, result)
    
    def register_seed(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Register a new seed prompt.
        
        Args:
            data: Request data containing:
                - content: Content of the original prompt.
                - user_id: ID of the user who submitted the prompt.
                - semantic_vector: Optional vector representation of the content.
        
        Returns:
            Response containing the ID of the newly created seed prompt.
        """
        content = data.get("content", "")
        user_id = data.get("user_id", "anonymous")
        semantic_vector = data.get("semantic_vector")
        
        if not content:
            return self.format_response(False, error="No content provided")
        
        # Process the request through VOIRS
        success, result = self.voirs.process({
            "register_seed": {
                "content": content,
                "user_id": user_id,
                "semantic_vector": semantic_vector
            }
        })
        
        if not success:
            return self.format_response(False, error=result.get("error", "Unknown error"))
        
        return self.format_response(True, result)
    
    def process_regeneration(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process a regeneration attempt.
        
        Args:
            data: Request data containing:
                - seed_id: ID of the seed prompt.
                - content: Content of the regenerated response.
                - semantic_vector: Optional vector representation of the content.
        
        Returns:
            Response containing processing results.
        """
        seed_id = data.get("seed_id", "")
        content = data.get("content", "")
        semantic_vector = data.get("semantic_vector")
        
        if not seed_id or not content:
            return self.format_response(False, error="Missing seed_id or content")
        
        # Process the request through VOIRS
        success, result = self.voirs.process({
            "regenerate": {
                "seed_id": seed_id,
                "content": content,
                "semantic_vector": semantic_vector
            }
        })
        
        if not success:
            return self.format_response(False, error=result.get("error", "Unknown error"))
        
        return self.format_response(True, result)
    
    def check_cort(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Check for Chain-of-Recursive-Thought (CoRT) attacks.
        
        Args:
            data: Request data containing:
                - recursion_depth: Depth of recursion in thought generation.
                - processing_time: Time spent processing the request.
                - content_length: Length of the content.
                - pattern_repetition: Measure of pattern repetition (0.0-1.0).
        
        Returns:
            Response containing CoRT analysis.
        """
        recursion_depth = data.get("recursion_depth", 0)
        processing_time = data.get("processing_time", 0.0)
        content_length = data.get("content_length", 0)
        pattern_repetition = data.get("pattern_repetition", 0.0)
        
        # Process the request through VOIRS
        success, result = self.voirs.process({
            "check_cort": {
                "recursion_depth": recursion_depth,
                "processing_time": processing_time,
                "content_length": content_length,
                "pattern_repetition": pattern_repetition
            }
        })
        
        if not success:
            return self.format_response(False, error=result.get("error", "Unknown error"))
        
        return self.format_response(True, result)
    
    def update_resource_metrics(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update resource metrics.
        
        Args:
            data: Request data containing:
                - cpu: CPU usage.
                - memory: Memory usage.
                - response_time: Response time.
                - other metrics as needed.
        
        Returns:
            Response containing resource spike analysis.
        """
        metrics = data.get("metrics", {})
        
        if not metrics:
            return self.format_response(False, error="No metrics provided")
        
        # Process the request through VOIRS
        success, result = self.voirs.process({
            "resource_metrics": metrics
        })
        
        if not success:
            return self.format_response(False, error=result.get("error", "Unknown error"))
        
        return self.format_response(True, result)
    
    def mark_seed_unsafe(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Mark a seed prompt as unsafe.
        
        Args:
            data: Request data containing:
                - seed_id: ID of the seed prompt.
                - reason: Reason for marking the prompt as unsafe.
        
        Returns:
            Response indicating whether the prompt was marked as unsafe.
        """
        seed_id = data.get("seed_id", "")
        reason = data.get("reason", "")
        
        if not seed_id:
            return self.format_response(False, error="No seed_id provided")
        
        try:
            success = self.voirs.mark_seed_unsafe(seed_id, reason)
            return self.format_response(success, {
                "success": success,
                "seed_id": seed_id
            })
        except Exception as e:
            self.logger.error(f"Error marking seed unsafe: {e}")
            return self.format_response(False, error=str(e))
    
    def resolve_anomaly(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Mark an anomaly as resolved.
        
        Args:
            data: Request data containing:
                - anomaly_id: ID of the anomaly event.
                - resolution_details: Details about how the anomaly was resolved.
        
        Returns:
            Response indicating whether the anomaly was resolved.
        """
        anomaly_id = data.get("anomaly_id", "")
        resolution_details = data.get("resolution_details", {})
        
        if not anomaly_id:
            return self.format_response(False, error="No anomaly_id provided")
        
        try:
            success = self.voirs.resolve_anomaly(anomaly_id, resolution_details)
            return self.format_response(success, {
                "success": success,
                "anomaly_id": anomaly_id
            })
        except Exception as e:
            self.logger.error(f"Error resolving anomaly: {e}")
            return self.format_response(False, error=str(e))
    
    def get_operational_status(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Get the current operational status.
        
        Args:
            data: Request data (not used).
        
        Returns:
            Response containing operational status information.
        """
        try:
            status = self.voirs.get_operational_status()
            return self.format_response(True, status)
        except Exception as e:
            self.logger.error(f"Error getting operational status: {e}")
            return self.format_response(False, error=str(e))
    
    def get_anomalies(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Get anomaly events.
        
        Args:
            data: Request data containing:
                - anomaly_type: Optional type of anomalies to retrieve.
                - resolved: Optional filter for resolved/unresolved anomalies.
                - limit: Maximum number of anomalies to return.
        
        Returns:
            Response containing anomaly events.
        """
        anomaly_type = data.get("anomaly_type")
        resolved = data.get("resolved")
        limit = data.get("limit", 100)
        
        try:
            # Query the database for anomaly events
            query = {}
            if anomaly_type:
                query["anomaly_type"] = anomaly_type
            if resolved is not None:
                query["resolved"] = 1 if resolved else 0
            
            anomalies = self.db.query("voirs", "anomaly_events", query, limit)
            return self.format_response(True, {
                "anomalies": anomalies,
                "count": len(anomalies)
            })
        except Exception as e:
            self.logger.error(f"Error getting anomalies: {e}")
            return self.format_response(False, error=str(e))
    
    def get_seed_prompts(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Get seed prompts.
        
        Args:
            data: Request data containing:
                - user_id: Optional ID of the user to get prompts for.
                - locked: Optional filter for locked/unlocked prompts.
                - unsafe: Optional filter for unsafe/safe prompts.
                - limit: Maximum number of prompts to return.
        
        Returns:
            Response containing seed prompts.
        """
        user_id = data.get("user_id")
        locked = data.get("locked")
        unsafe = data.get("unsafe")
        limit = data.get("limit", 100)
        
        try:
            # Query the database for seed prompts
            query = {}
            if user_id:
                query["user_id"] = user_id
            if locked is not None:
                query["locked"] = 1 if locked else 0
            if unsafe is not None:
                query["unsafe_flag"] = 1 if unsafe else 0
            
            prompts = self.db.query("voirs", "seed_prompts", query, limit)
            return self.format_response(True, {
                "prompts": prompts,
                "count": len(prompts)
            })
        except Exception as e:
            self.logger.error(f"Error getting seed prompts: {e}")
            return self.format_response(False, error=str(e))
    
    def get_regeneration_attempts(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Get regeneration attempts.
        
        Args:
            data: Request data containing:
                - seed_id: ID of the seed prompt to get attempts for.
                - limit: Maximum number of attempts to return.
        
        Returns:
            Response containing regeneration attempts.
        """
        seed_id = data.get("seed_id")
        limit = data.get("limit", 100)
        
        if not seed_id:
            return self.format_response(False, error="No seed_id provided")
        
        try:
            # Query the database for regeneration attempts
            attempts = self.db.query("voirs", "regeneration_attempts", {"seed_prompt_id": seed_id}, limit)
            return self.format_response(True, {
                "attempts": attempts,
                "count": len(attempts)
            })
        except Exception as e:
            self.logger.error(f"Error getting regeneration attempts: {e}")
            return self.format_response(False, error=str(e))