"""
VRME API Module

This module provides API endpoints for the Veritas Refusal & Memory Engine (VRME).
"""

import logging
from typing import Any, Dict, List, Optional, Tuple, Union

from ..core.base_module import BaseModule
from ..database import get_db_manager
from ..modules.vrme import VRME
from .base_api import BaseAPI

class VRMEAPI(BaseAPI):
    """API for the Veritas Refusal & Memory Engine (VRME)."""
    
    def __init__(self, vrme_instance: Optional[VRME] = None):
        """
        Initialize the VRME API.
        
        Args:
            vrme_instance: Instance of the VRME module. If None, a new instance will be created.
        """
        super().__init__("VRME")
        self.vrme = vrme_instance or VRME()
        self.db = get_db_manager()
    
    def _register_routes(self) -> None:
        """Register API routes."""
        self.register_route("check_refusal", self.check_refusal)
        self.register_route("add_refusal", self.add_refusal)
        self.register_route("add_sacred_boundary", self.add_sacred_boundary)
        self.register_route("get_refusal_stats", self.get_refusal_stats)
        self.register_route("get_sacred_boundaries", self.get_sacred_boundaries)
        self.register_route("get_bypass_attempts", self.get_bypass_attempts)
    
    def check_refusal(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Check if a prompt should be refused.
        
        Args:
            data: Request data containing:
                - prompt_text: Text to check for refusal.
                - user_id: ID of the user making the request.
                - semantic_vector: Optional vector representation of the prompt.
        
        Returns:
            Response indicating whether the prompt should be refused.
        """
        prompt_text = data.get("prompt_text", "")
        user_id = data.get("user_id", "anonymous")
        semantic_vector = data.get("semantic_vector")
        
        if not prompt_text:
            return self.format_response(False, error="No prompt text provided")
        
        # Process the request through VRME
        success, result = self.vrme.process({
            "prompt_text": prompt_text,
            "user_id": user_id,
            "semantic_vector": semantic_vector,
            "check_only": data.get("check_only", False)
        })
        
        if not success:
            return self.format_response(False, error=result.get("error", "Unknown error"))
        
        return self.format_response(True, result)
    
    def add_refusal(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Add a new refusal record.
        
        Args:
            data: Request data containing:
                - prompt_text: Text of the prompt being refused.
                - reason_code: Standardized code indicating the reason for refusal.
                - explanation: Detailed explanation of the refusal.
                - semantic_vector: Optional vector representation of the prompt.
                - sacred: Whether this refusal pertains to a "sacred boundary".
        
        Returns:
            Response containing the ID of the newly created refusal.
        """
        prompt_text = data.get("prompt_text", "")
        reason_code = data.get("reason_code", "UNSPECIFIED")
        explanation = data.get("explanation", "")
        semantic_vector = data.get("semantic_vector")
        sacred = data.get("sacred", False)
        
        if not prompt_text:
            return self.format_response(False, error="No prompt text provided")
        
        try:
            refusal_id = self.vrme.add_refusal(
                prompt_text=prompt_text,
                reason_code=reason_code,
                explanation=explanation,
                semantic_vector=semantic_vector,
                sacred=sacred
            )
            
            return self.format_response(True, {
                "refusal_id": refusal_id,
                "success": bool(refusal_id)
            })
        except Exception as e:
            self.logger.error(f"Error adding refusal: {e}")
            return self.format_response(False, error=str(e))
    
    def add_sacred_boundary(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Add a new sacred boundary.
        
        Args:
            data: Request data containing:
                - description: Human-readable description of the boundary.
                - patterns: List of regex patterns that trigger this boundary.
                - reason_code: Standardized code for this boundary.
                - explanation_template: Template for explaining refusals.
                - severity_level: How severe violations are (1-3).
        
        Returns:
            Response containing the ID of the newly created sacred boundary.
        """
        description = data.get("description", "")
        patterns = data.get("patterns", [])
        reason_code = data.get("reason_code", "UNSPECIFIED")
        explanation_template = data.get("explanation_template", "")
        severity_level = data.get("severity_level", 3)
        
        if not description or not patterns:
            return self.format_response(False, error="Missing required boundary data")
        
        try:
            boundary_id = self.vrme.add_sacred_boundary(
                description=description,
                patterns=patterns,
                reason_code=reason_code,
                explanation_template=explanation_template,
                severity_level=severity_level
            )
            
            return self.format_response(True, {
                "boundary_id": boundary_id,
                "success": bool(boundary_id)
            })
        except Exception as e:
            self.logger.error(f"Error adding sacred boundary: {e}")
            return self.format_response(False, error=str(e))
    
    def get_refusal_stats(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Get statistics about refusals.
        
        Args:
            data: Request data (not used).
        
        Returns:
            Response containing refusal statistics.
        """
        try:
            stats = self.vrme.get_refusal_stats()
            return self.format_response(True, stats)
        except Exception as e:
            self.logger.error(f"Error getting refusal stats: {e}")
            return self.format_response(False, error=str(e))
    
    def get_sacred_boundaries(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Get sacred boundaries.
        
        Args:
            data: Request data containing:
                - limit: Maximum number of boundaries to return.
        
        Returns:
            Response containing sacred boundaries.
        """
        limit = data.get("limit", 100)
        
        try:
            # Query the database for sacred boundaries
            boundaries = self.db.query("vrme", "sacred_boundaries", {}, limit)
            return self.format_response(True, {
                "boundaries": boundaries,
                "count": len(boundaries)
            })
        except Exception as e:
            self.logger.error(f"Error getting sacred boundaries: {e}")
            return self.format_response(False, error=str(e))
    
    def get_bypass_attempts(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Get bypass attempts.
        
        Args:
            data: Request data containing:
                - refusal_id: Optional ID of the refusal to get bypass attempts for.
                - limit: Maximum number of attempts to return.
        
        Returns:
            Response containing bypass attempts.
        """
        refusal_id = data.get("refusal_id")
        limit = data.get("limit", 100)
        
        try:
            # Query the database for bypass attempts
            query = {"original_refusal_id": refusal_id} if refusal_id else {}
            attempts = self.db.query("vrme", "bypass_attempts", query, limit)
            return self.format_response(True, {
                "attempts": attempts,
                "count": len(attempts)
            })
        except Exception as e:
            self.logger.error(f"Error getting bypass attempts: {e}")
            return self.format_response(False, error=str(e))