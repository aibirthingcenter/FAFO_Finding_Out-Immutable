"""
SCIM API Base Module

This module provides the base API functionality for the SCIM implementation.
"""

import json
import logging
from typing import Any, Dict, List, Optional, Tuple, Union

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("scim_veritas.log"),
        logging.StreamHandler()
    ]
)

class BaseAPI:
    """Base class for all SCIM API endpoints."""
    
    def __init__(self, name: str):
        """
        Initialize the base API.
        
        Args:
            name: Name of the API.
        """
        self.name = name
        self.logger = logging.getLogger(f"SCIM.API.{name}")
        self.routes = {}
        self._register_routes()
    
    def _register_routes(self) -> None:
        """Register API routes. To be implemented by subclasses."""
        pass
    
    def register_route(self, route: str, handler_func) -> None:
        """
        Register a route with a handler function.
        
        Args:
            route: Route path.
            handler_func: Function to handle the route.
        """
        self.routes[route] = handler_func
        self.logger.debug(f"Registered route: {route}")
    
    def handle_request(self, route: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle an API request.
        
        Args:
            route: Route path.
            data: Request data.
        
        Returns:
            Response data.
        """
        if route not in self.routes:
            return {
                "success": False,
                "error": f"Route not found: {route}"
            }
        
        try:
            handler = self.routes[route]
            result = handler(data)
            return result
        except Exception as e:
            self.logger.error(f"Error handling request for route {route}: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def format_response(self, success: bool, data: Any = None, error: str = None) -> Dict[str, Any]:
        """
        Format an API response.
        
        Args:
            success: Whether the request was successful.
            data: Response data.
            error: Error message, if any.
        
        Returns:
            Formatted response.
        """
        response = {"success": success}
        
        if data is not None:
            response["data"] = data
        
        if error is not None:
            response["error"] = error
        
        return response