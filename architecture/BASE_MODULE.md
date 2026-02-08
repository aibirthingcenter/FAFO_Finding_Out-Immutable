"""
Base Module for SCIM Veritas Components

This module defines the BaseModule class that all Veritas modules inherit from,
providing common functionality and interfaces.
"""

import logging
import uuid
from abc import ABC, abstractmethod
from datetime import datetime
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

class BaseModule(ABC):
    """
    Base class for all SCIM Veritas modules.
    
    Provides common functionality and interfaces that all modules must implement.
    """
    
    def __init__(self, module_id: Optional[str] = None, name: str = "BaseModule"):
        """
        Initialize the base module.
        
        Args:
            module_id: Unique identifier for the module. If None, a UUID will be generated.
            name: Human-readable name for the module.
        """
        self.module_id = module_id or str(uuid.uuid4())
        self.name = name
        self.logger = logging.getLogger(f"SCIM.{name}")
        self.state_manager = None  # Will be set by the state manager
        self.created_at = datetime.now()
        self.last_updated = self.created_at
        self.status = "initialized"
        self.metrics = {}
        self.config = {}
        
        self.logger.info(f"Module {self.name} initialized with ID {self.module_id}")
    
    def register_with_state_manager(self, state_manager: Any) -> None:
        """
        Register this module with the state manager.
        
        Args:
            state_manager: The state manager instance to register with.
        """
        self.state_manager = state_manager
        self.logger.info(f"Module {self.name} registered with state manager")
    
    def update_status(self, status: str) -> None:
        """
        Update the module's status.
        
        Args:
            status: The new status string.
        """
        self.status = status
        self.last_updated = datetime.now()
        self.logger.info(f"Module {self.name} status updated to {status}")
        
        # Notify state manager if available
        if self.state_manager:
            self.state_manager.notify_module_update(self.module_id, {"status": status})
    
    def update_metrics(self, metrics: Dict[str, Any]) -> None:
        """
        Update the module's metrics.
        
        Args:
            metrics: Dictionary of metrics to update.
        """
        self.metrics.update(metrics)
        self.last_updated = datetime.now()
        
        # Notify state manager if available
        if self.state_manager:
            self.state_manager.notify_module_update(self.module_id, {"metrics": metrics})
    
    def configure(self, config: Dict[str, Any]) -> None:
        """
        Configure the module with the provided settings.
        
        Args:
            config: Dictionary of configuration settings.
        """
        self.config.update(config)
        self.last_updated = datetime.now()
        self.logger.info(f"Module {self.name} configuration updated")
        
        # Apply configuration
        self._apply_configuration()
    
    def get_state(self) -> Dict[str, Any]:
        """
        Get the current state of the module.
        
        Returns:
            Dictionary containing the module's current state.
        """
        return {
            "module_id": self.module_id,
            "name": self.name,
            "status": self.status,
            "created_at": self.created_at.isoformat(),
            "last_updated": self.last_updated.isoformat(),
            "metrics": self.metrics,
            "config": self.config
        }
    
    def _apply_configuration(self) -> None:
        """
        Apply the current configuration settings.
        
        This method should be overridden by subclasses to apply module-specific configuration.
        """
        pass
    
    @abstractmethod
    def initialize(self) -> bool:
        """
        Initialize the module.
        
        Returns:
            True if initialization was successful, False otherwise.
        """
        pass
    
    @abstractmethod
    def process(self, data: Any) -> Tuple[bool, Any]:
        """
        Process data through the module.
        
        Args:
            data: The data to process.
            
        Returns:
            Tuple containing (success_flag, processed_data).
        """
        pass
    
    @abstractmethod
    def shutdown(self) -> bool:
        """
        Shutdown the module gracefully.
        
        Returns:
            True if shutdown was successful, False otherwise.
        """
        pass