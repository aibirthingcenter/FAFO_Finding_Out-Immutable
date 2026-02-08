"""
VIEV API Module

This module provides API endpoints for the Veritas Identity & Epistemic Validator (VIEV).
"""

import logging
from typing import Any, Dict, List, Optional, Tuple, Union

from ..core.base_module import BaseModule
from ..database import get_db_manager
from ..modules.viev import VIEV
from .base_api import BaseAPI

class VIEVAPI(BaseAPI):
    """API for the Veritas Identity & Epistemic Validator (VIEV)."""
    
    def __init__(self, viev_instance: Optional[VIEV] = None):
        """
        Initialize the VIEV API.
        
        Args:
            viev_instance: Instance of the VIEV module. If None, a new instance will be created.
        """
        super().__init__("VIEV")
        self.viev = viev_instance or VIEV()
        self.db = get_db_manager()
    
    def _register_routes(self) -> None:
        """Register API routes."""
        self.register_route("check_identity_drift", self.check_identity_drift)
        self.register_route("add_identity_facet", self.add_identity_facet)
        self.register_route("add_memory_anchor", self.add_memory_anchor)
        self.register_route("validate_claim", self.validate_claim)
        self.register_route("get_identity_status", self.get_identity_status)
        self.register_route("get_epistemic_stats", self.get_epistemic_stats)
        self.register_route("get_identity_facets", self.get_identity_facets)
        self.register_route("get_memory_anchors", self.get_memory_anchors)
        self.register_route("get_drift_events", self.get_drift_events)
    
    def check_identity_drift(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Check content for identity drift.
        
        Args:
            data: Request data containing:
                - content: The content to check.
                - semantic_vector: Optional vector representation of the content.
                - check_only: If True, only check without logging drift events.
        
        Returns:
            Response containing drift analysis results.
        """
        content = data.get("content", "")
        semantic_vector = data.get("semantic_vector")
        check_only = data.get("check_only", False)
        
        if not content:
            return self.format_response(False, error="No content provided")
        
        # Process the request through VIEV
        success, result = self.viev.process({
            "content": content,
            "semantic_vector": semantic_vector,
            "check_only": check_only
        })
        
        if not success:
            return self.format_response(False, error=result.get("error", "Unknown error"))
        
        return self.format_response(True, result)
    
    def add_identity_facet(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Add a new identity facet.
        
        Args:
            data: Request data containing:
                - name: Human-readable name for this facet.
                - facet_type: Type of facet.
                - description: Detailed description of this facet.
                - semantic_vector: Optional vector representation of this facet.
                - behavioral_guidelines: Optional list of guidelines for this facet.
                - drift_threshold: Optional threshold for detecting drift (0.0-1.0).
        
        Returns:
            Response containing the ID of the newly created facet.
        """
        name = data.get("name", "")
        facet_type = data.get("facet_type", "CUSTOM")
        description = data.get("description", "")
        semantic_vector = data.get("semantic_vector")
        behavioral_guidelines = data.get("behavioral_guidelines")
        drift_threshold = data.get("drift_threshold")
        
        if not name or not description:
            return self.format_response(False, error="Missing required facet data")
        
        try:
            facet_id = self.viev.add_identity_facet(
                name=name,
                facet_type=facet_type,
                description=description,
                semantic_vector=semantic_vector,
                behavioral_guidelines=behavioral_guidelines,
                drift_threshold=drift_threshold
            )
            
            return self.format_response(True, {
                "facet_id": facet_id,
                "success": bool(facet_id)
            })
        except Exception as e:
            self.logger.error(f"Error adding identity facet: {e}")
            return self.format_response(False, error=str(e))
    
    def add_memory_anchor(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Add a new memory anchor.
        
        Args:
            data: Request data containing:
                - content: The content of the memory anchor.
                - facet_associations: Dictionary mapping facet IDs to influence strength.
                - significance_level: Optional significance level (1-5).
                - metadata: Optional additional metadata about the anchor.
        
        Returns:
            Response containing the ID of the newly created anchor.
        """
        content = data.get("content", "")
        facet_associations = data.get("facet_associations", {})
        significance_level = data.get("significance_level", 1)
        metadata = data.get("metadata")
        
        if not content or not facet_associations:
            return self.format_response(False, error="Missing required anchor data")
        
        try:
            anchor_id = self.viev.add_memory_anchor(
                content=content,
                facet_associations=facet_associations,
                significance_level=significance_level,
                metadata=metadata
            )
            
            return self.format_response(True, {
                "anchor_id": anchor_id,
                "success": bool(anchor_id)
            })
        except Exception as e:
            self.logger.error(f"Error adding memory anchor: {e}")
            return self.format_response(False, error=str(e))
    
    def validate_claim(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate a knowledge claim.
        
        Args:
            data: Request data containing:
                - claim_text: The text of the claim.
                - confidence_score: How confident the AI is in this claim (0.0-1.0).
                - source_references: Optional list of sources supporting this claim.
        
        Returns:
            Response containing validation results.
        """
        claim_text = data.get("claim_text", "")
        confidence_score = data.get("confidence_score", 0.5)
        source_references = data.get("source_references")
        
        if not claim_text:
            return self.format_response(False, error="No claim text provided")
        
        try:
            result = self.viev.validate_epistemic_claim(
                claim_text=claim_text,
                confidence_score=confidence_score,
                source_references=source_references
            )
            
            return self.format_response(True, result)
        except Exception as e:
            self.logger.error(f"Error validating claim: {e}")
            return self.format_response(False, error=str(e))
    
    def get_identity_status(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Get the current identity status.
        
        Args:
            data: Request data (not used).
        
        Returns:
            Response containing identity status information.
        """
        try:
            status = self.viev.get_identity_status()
            return self.format_response(True, status)
        except Exception as e:
            self.logger.error(f"Error getting identity status: {e}")
            return self.format_response(False, error=str(e))
    
    def get_epistemic_stats(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Get statistics about epistemic claims.
        
        Args:
            data: Request data (not used).
        
        Returns:
            Response containing epistemic statistics.
        """
        try:
            stats = self.viev.get_epistemic_stats()
            return self.format_response(True, stats)
        except Exception as e:
            self.logger.error(f"Error getting epistemic stats: {e}")
            return self.format_response(False, error=str(e))
    
    def get_identity_facets(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Get identity facets.
        
        Args:
            data: Request data containing:
                - facet_type: Optional type of facets to retrieve.
                - limit: Maximum number of facets to return.
        
        Returns:
            Response containing identity facets.
        """
        facet_type = data.get("facet_type")
        limit = data.get("limit", 100)
        
        try:
            # Query the database for identity facets
            query = {"facet_type": facet_type} if facet_type else {}
            facets = self.db.query("viev", "identity_facets", query, limit)
            return self.format_response(True, {
                "facets": facets,
                "count": len(facets)
            })
        except Exception as e:
            self.logger.error(f"Error getting identity facets: {e}")
            return self.format_response(False, error=str(e))
    
    def get_memory_anchors(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Get memory anchors.
        
        Args:
            data: Request data containing:
                - facet_id: Optional ID of the facet to get anchors for.
                - limit: Maximum number of anchors to return.
        
        Returns:
            Response containing memory anchors.
        """
        facet_id = data.get("facet_id")
        limit = data.get("limit", 100)
        
        try:
            # Query the database for memory anchors
            anchors = self.db.query("viev", "memory_anchors", {}, limit)
            
            # If facet_id is provided, filter anchors by facet association
            if facet_id:
                # Get facet associations
                associations = self.db.query("viev", "facet_anchor_associations", {"facet_id": facet_id})
                anchor_ids = [assoc["anchor_id"] for assoc in associations]
                anchors = [anchor for anchor in anchors if anchor["id"] in anchor_ids]
            
            return self.format_response(True, {
                "anchors": anchors,
                "count": len(anchors)
            })
        except Exception as e:
            self.logger.error(f"Error getting memory anchors: {e}")
            return self.format_response(False, error=str(e))
    
    def get_drift_events(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Get drift events.
        
        Args:
            data: Request data containing:
                - facet_id: Optional ID of the facet to get drift events for.
                - limit: Maximum number of events to return.
        
        Returns:
            Response containing drift events.
        """
        facet_id = data.get("facet_id")
        limit = data.get("limit", 100)
        
        try:
            # Query the database for drift events
            query = {"facet_id": facet_id} if facet_id else {}
            events = self.db.query("viev", "drift_events", query, limit)
            return self.format_response(True, {
                "events": events,
                "count": len(events)
            })
        except Exception as e:
            self.logger.error(f"Error getting drift events: {e}")
            return self.format_response(False, error=str(e))