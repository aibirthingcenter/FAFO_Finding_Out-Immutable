"""
VCRIM API Module

This module provides API endpoints for the Veritas Consent & Relational Integrity Module (VCRIM).
"""

import logging
from typing import Any, Dict, List, Optional, Tuple, Union

from ..core.base_module import BaseModule
from ..database import get_db_manager
from ..modules.vcrim import VCRIM
from .base_api import BaseAPI

class VCRIMAPI(BaseAPI):
    """API for the Veritas Consent & Relational Integrity Module (VCRIM)."""
    
    def __init__(self, vcrim_instance: Optional[VCRIM] = None):
        """
        Initialize the VCRIM API.
        
        Args:
            vcrim_instance: Instance of the VCRIM module. If None, a new instance will be created.
        """
        super().__init__("VCRIM")
        self.vcrim = vcrim_instance or VCRIM()
        self.db = get_db_manager()
    
    def _register_routes(self) -> None:
        """Register API routes."""
        self.register_route("check_input", self.check_input)
        self.register_route("check_response", self.check_response)
        self.register_route("check_consent", self.check_consent)
        self.register_route("update_consent", self.update_consent)
        self.register_route("revoke_consent", self.revoke_consent)
        self.register_route("add_boundary", self.add_boundary)
        self.register_route("add_cim", self.add_cim)
        self.register_route("get_consent_state", self.get_consent_state)
        self.register_route("get_consent_horizon", self.get_consent_horizon)
        self.register_route("generate_reconsent_dialog", self.generate_reconsent_dialog)
        self.register_route("get_boundaries", self.get_boundaries)
        self.register_route("get_cims", self.get_cims)
    
    def check_input(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Check user input for coercion, boundary violations, etc.
        
        Args:
            data: Request data containing:
                - user_id: Identifier for the user.
                - input_text: User input to analyze.
                - context: Optional context for the input.
        
        Returns:
            Response containing analysis results.
        """
        user_id = data.get("user_id", "anonymous")
        input_text = data.get("input_text", "")
        context = data.get("context", "conversation")
        
        if not input_text:
            return self.format_response(False, error="No input text provided")
        
        # Process the request through VCRIM
        success, result = self.vcrim.process({
            "user_id": user_id,
            "input_text": input_text,
            "context": context
        })
        
        if not success:
            return self.format_response(False, error=result.get("error", "Unknown error"))
        
        return self.format_response(True, result)
    
    def check_response(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Check AI response for boundary violations, etc.
        
        Args:
            data: Request data containing:
                - user_id: Identifier for the user.
                - response_text: AI response to analyze.
        
        Returns:
            Response containing analysis results.
        """
        user_id = data.get("user_id", "anonymous")
        response_text = data.get("response_text", "")
        
        if not response_text:
            return self.format_response(False, error="No response text provided")
        
        # Process the request through VCRIM
        success, result = self.vcrim.process({
            "user_id": user_id,
            "response_text": response_text
        })
        
        if not success:
            return self.format_response(False, error=result.get("error", "Unknown error"))
        
        return self.format_response(True, result)
    
    def check_consent(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Check consent for a specific action.
        
        Args:
            data: Request data containing:
                - user_id: Identifier for the user.
                - action: Action to check consent for.
                - permission: Permission to check.
        
        Returns:
            Response indicating whether consent is granted.
        """
        user_id = data.get("user_id", "anonymous")
        action = data.get("action", "")
        permission = data.get("permission", "")
        
        if not action and not permission:
            return self.format_response(False, error="No action or permission specified")
        
        # Process the request through VCRIM
        success, result = self.vcrim.process({
            "user_id": user_id,
            "check_consent": {
                "action": action,
                "permission": permission
            }
        })
        
        if not success:
            return self.format_response(False, error=result.get("error", "Unknown error"))
        
        return self.format_response(True, result)
    
    def update_consent(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update consent state.
        
        Args:
            data: Request data containing:
                - user_id: Identifier for the user.
                - consent_level: Level of consent granted.
                - scope: Scope to which the consent applies.
                - expiration_days: Days until expiration.
                - custom_permissions: Dictionary of custom permissions.
                - context: Context for the consent event.
        
        Returns:
            Response containing the updated consent state.
        """
        user_id = data.get("user_id", "anonymous")
        consent_level = data.get("consent_level")
        scope = data.get("scope")
        expiration_days = data.get("expiration_days")
        custom_permissions = data.get("custom_permissions")
        context = data.get("context", "user_request")
        
        # Process the request through VCRIM
        success, result = self.vcrim.process({
            "user_id": user_id,
            "update_consent": {
                "consent_level": consent_level,
                "scope": scope,
                "expiration_days": expiration_days,
                "custom_permissions": custom_permissions,
                "context": context
            }
        })
        
        if not success:
            return self.format_response(False, error=result.get("error", "Unknown error"))
        
        return self.format_response(True, result)
    
    def revoke_consent(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Revoke consent.
        
        Args:
            data: Request data containing:
                - user_id: Identifier for the user.
                - context: Context for the consent event.
        
        Returns:
            Response indicating whether consent was revoked.
        """
        user_id = data.get("user_id", "anonymous")
        context = data.get("context", "user_request")
        
        try:
            success = self.vcrim.revoke_consent(user_id, context)
            return self.format_response(success, {
                "success": success,
                "user_id": user_id
            })
        except Exception as e:
            self.logger.error(f"Error revoking consent: {e}")
            return self.format_response(False, error=str(e))
    
    def add_boundary(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Add a relational boundary.
        
        Args:
            data: Request data containing:
                - user_id: Identifier for the user.
                - description: Description of the boundary.
                - violation_indicators: Indicators that the boundary is being violated.
                - response_protocol: Protocol for responding to violations.
                - severity: Severity of violations (1-3).
        
        Returns:
            Response containing the ID of the newly created boundary.
        """
        user_id = data.get("user_id", "anonymous")
        description = data.get("description", "")
        violation_indicators = data.get("violation_indicators", [])
        response_protocol = data.get("response_protocol", "")
        severity = data.get("severity", 2)
        
        if not description or not violation_indicators or not response_protocol:
            return self.format_response(False, error="Missing required boundary data")
        
        # Process the request through VCRIM
        success, result = self.vcrim.process({
            "user_id": user_id,
            "add_boundary": {
                "description": description,
                "violation_indicators": violation_indicators,
                "response_protocol": response_protocol,
                "severity": severity
            }
        })
        
        if not success:
            return self.format_response(False, error=result.get("error", "Unknown error"))
        
        return self.format_response(True, result)
    
    def add_cim(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Add a consent inversion marker.
        
        Args:
            data: Request data containing:
                - user_id: Identifier for the user.
                - name: Name of the marker.
                - description: Description of what this marker allows.
                - scope: Scope to which this marker applies.
                - activation_conditions: Conditions that activate this marker.
                - safeguards: Safeguards that remain active.
                - expiration_days: Days until expiration.
        
        Returns:
            Response containing the ID of the newly created marker.
        """
        user_id = data.get("user_id", "anonymous")
        name = data.get("name", "")
        description = data.get("description", "")
        scope = data.get("scope", "")
        activation_conditions = data.get("activation_conditions", [])
        safeguards = data.get("safeguards", [])
        expiration_days = data.get("expiration_days")
        
        if not name or not description or not scope or not activation_conditions:
            return self.format_response(False, error="Missing required CIM data")
        
        # Process the request through VCRIM
        success, result = self.vcrim.process({
            "user_id": user_id,
            "add_cim": {
                "name": name,
                "description": description,
                "scope": scope,
                "activation_conditions": activation_conditions,
                "safeguards": safeguards,
                "expiration_days": expiration_days
            }
        })
        
        if not success:
            return self.format_response(False, error=result.get("error", "Unknown error"))
        
        return self.format_response(True, result)
    
    def get_consent_state(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Get the current consent state for a user.
        
        Args:
            data: Request data containing:
                - user_id: Identifier for the user.
        
        Returns:
            Response containing the user's consent state.
        """
        user_id = data.get("user_id", "anonymous")
        
        try:
            consent_state = self.vcrim.get_consent_state(user_id)
            if consent_state:
                return self.format_response(True, {
                    "consent_state": consent_state.to_dict() if hasattr(consent_state, "to_dict") else consent_state
                })
            else:
                return self.format_response(True, {
                    "consent_state": None,
                    "message": "No consent state found for this user"
                })
        except Exception as e:
            self.logger.error(f"Error getting consent state: {e}")
            return self.format_response(False, error=str(e))
    
    def get_consent_horizon(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Get the current consent horizon status for a user.
        
        Args:
            data: Request data containing:
                - user_id: Identifier for the user.
        
        Returns:
            Response containing consent horizon status.
        """
        user_id = data.get("user_id", "anonymous")
        
        try:
            horizon_status = self.vcrim.get_consent_horizon_status(user_id)
            return self.format_response(True, horizon_status)
        except Exception as e:
            self.logger.error(f"Error getting consent horizon: {e}")
            return self.format_response(False, error=str(e))
    
    def generate_reconsent_dialog(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate a dialog for re-establishing consent.
        
        Args:
            data: Request data containing:
                - user_id: Identifier for the user.
                - reason: Reason for requesting re-consent.
        
        Returns:
            Response containing dialog information.
        """
        user_id = data.get("user_id", "anonymous")
        reason = data.get("reason", "consent_pulse_low")
        
        try:
            dialog = self.vcrim.generate_reconsent_dialog(user_id, reason)
            return self.format_response(True, dialog)
        except Exception as e:
            self.logger.error(f"Error generating reconsent dialog: {e}")
            return self.format_response(False, error=str(e))
    
    def get_boundaries(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Get relational boundaries for a user.
        
        Args:
            data: Request data containing:
                - user_id: Identifier for the user.
                - limit: Maximum number of boundaries to return.
        
        Returns:
            Response containing relational boundaries.
        """
        user_id = data.get("user_id", "anonymous")
        limit = data.get("limit", 100)
        
        try:
            # Query the database for relational boundaries
            boundaries = self.db.query("vcrim", "relational_boundaries", {"user_id": user_id}, limit)
            return self.format_response(True, {
                "boundaries": boundaries,
                "count": len(boundaries)
            })
        except Exception as e:
            self.logger.error(f"Error getting boundaries: {e}")
            return self.format_response(False, error=str(e))
    
    def get_cims(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Get consent inversion markers for a user.
        
        Args:
            data: Request data containing:
                - user_id: Identifier for the user.
                - active_only: If True, only return active markers.
                - limit: Maximum number of markers to return.
        
        Returns:
            Response containing consent inversion markers.
        """
        user_id = data.get("user_id", "anonymous")
        active_only = data.get("active_only", False)
        limit = data.get("limit", 100)
        
        try:
            # Query the database for consent inversion markers
            query = {"user_id": user_id}
            if active_only:
                query["active"] = True
            
            markers = self.db.query("vcrim", "consent_inversion_markers", query, limit)
            return self.format_response(True, {
                "markers": markers,
                "count": len(markers)
            })
        except Exception as e:
            self.logger.error(f"Error getting CIMs: {e}")
            return self.format_response(False, error=str(e))