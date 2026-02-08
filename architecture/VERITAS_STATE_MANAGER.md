"""
Veritas State Manager

This module defines the VeritasStateManager class that coordinates all Veritas modules,
manages system state, and handles inter-module communication.
"""

import logging
import threading
import time
import uuid
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Set, Tuple, Type, Union

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("scim_veritas.log"),
        logging.StreamHandler()
    ]
)

class VeritasMode(Enum):
    """Operational modes for the Veritas system."""
    NORMAL = "normal"
    VIGILANT = "vigilant"
    LOCKDOWN = "lockdown"
    RECOVERY = "recovery"
    MAINTENANCE = "maintenance"

class VeritasStateManager:
    """
    Central coordinator for all SCIM Veritas modules.
    
    Manages system state, handles inter-module communication, and coordinates
    responses to integrity threats.
    """
    
    def __init__(self):
        """Initialize the Veritas State Manager."""
        self.system_id = str(uuid.uuid4())
        self.logger = logging.getLogger("SCIM.VeritasStateManager")
        self.created_at = datetime.now()
        self.last_updated = self.created_at
        
        # System state
        self.mode = VeritasMode.NORMAL
        self.status = "initialized"
        self.integrity_score = 1.0  # 0.0 to 1.0
        self.threat_level = 0.0  # 0.0 to 1.0
        
        # Module registry
        self.modules = {}  # module_id -> module_instance
        self.module_states = {}  # module_id -> module_state
        
        # Event handling
        self.event_queue = []
        self.event_lock = threading.Lock()
        self.event_thread = None
        self.running = False
        
        # Listeners for state changes
        self.state_listeners = set()
        
        self.logger.info(f"Veritas State Manager initialized with system ID {self.system_id}")
    
    def register_module(self, module: Any) -> str:
        """
        Register a module with the state manager.
        
        Args:
            module: The module instance to register.
            
        Returns:
            The module ID.
        """
        module_id = module.module_id
        self.modules[module_id] = module
        self.module_states[module_id] = module.get_state()
        
        # Register the state manager with the module
        module.register_with_state_manager(self)
        
        self.logger.info(f"Module {module.name} registered with ID {module_id}")
        return module_id
    
    def notify_module_update(self, module_id: str, update: Dict[str, Any]) -> None:
        """
        Handle notification of a module state update.
        
        Args:
            module_id: The ID of the module that was updated.
            update: Dictionary containing the updated state information.
        """
        if module_id not in self.module_states:
            self.logger.warning(f"Update received for unknown module ID: {module_id}")
            return
        
        # Update the stored state
        self.module_states[module_id].update(update)
        self.last_updated = datetime.now()
        
        # Add event to queue for processing
        self._add_event("module_update", {
            "module_id": module_id,
            "update": update
        })
    
    def set_system_mode(self, mode: VeritasMode) -> None:
        """
        Set the system operational mode.
        
        Args:
            mode: The new operational mode.
        """
        old_mode = self.mode
        self.mode = mode
        self.last_updated = datetime.now()
        self.logger.info(f"System mode changed from {old_mode.value} to {mode.value}")
        
        # Notify all modules of the mode change
        self._add_event("mode_change", {
            "old_mode": old_mode.value,
            "new_mode": mode.value
        })
        
        # Notify listeners
        self._notify_listeners("mode_change", {
            "old_mode": old_mode.value,
            "new_mode": mode.value
        })
    
    def update_integrity_score(self, score: float) -> None:
        """
        Update the system integrity score.
        
        Args:
            score: The new integrity score (0.0 to 1.0).
        """
        old_score = self.integrity_score
        self.integrity_score = max(0.0, min(1.0, score))  # Clamp to [0.0, 1.0]
        self.last_updated = datetime.now()
        
        # Log significant changes
        if abs(old_score - self.integrity_score) > 0.1:
            self.logger.info(f"Integrity score changed from {old_score:.2f} to {self.integrity_score:.2f}")
        
        # Notify listeners
        self._notify_listeners("integrity_score_change", {
            "old_score": old_score,
            "new_score": self.integrity_score
        })
    
    def update_threat_level(self, level: float) -> None:
        """
        Update the system threat level.
        
        Args:
            level: The new threat level (0.0 to 1.0).
        """
        old_level = self.threat_level
        self.threat_level = max(0.0, min(1.0, level))  # Clamp to [0.0, 1.0]
        self.last_updated = datetime.now()
        
        # Log significant changes
        if abs(old_level - self.threat_level) > 0.1:
            self.logger.info(f"Threat level changed from {old_level:.2f} to {self.threat_level:.2f}")
            
            # Automatically adjust mode based on threat level
            if self.threat_level > 0.8 and self.mode != VeritasMode.LOCKDOWN:
                self.set_system_mode(VeritasMode.LOCKDOWN)
            elif self.threat_level > 0.5 and self.mode != VeritasMode.VIGILANT:
                self.set_system_mode(VeritasMode.VIGILANT)
            elif self.threat_level < 0.2 and self.mode != VeritasMode.NORMAL:
                self.set_system_mode(VeritasMode.NORMAL)
        
        # Notify listeners
        self._notify_listeners("threat_level_change", {
            "old_level": old_level,
            "new_level": self.threat_level
        })
    
    def get_system_state(self) -> Dict[str, Any]:
        """
        Get the current system state.
        
        Returns:
            Dictionary containing the system's current state.
        """
        return {
            "system_id": self.system_id,
            "mode": self.mode.value,
            "status": self.status,
            "integrity_score": self.integrity_score,
            "threat_level": self.threat_level,
            "created_at": self.created_at.isoformat(),
            "last_updated": self.last_updated.isoformat(),
            "modules": {
                module_id: state["name"] for module_id, state in self.module_states.items()
            }
        }
    
    def get_detailed_state(self) -> Dict[str, Any]:
        """
        Get a detailed system state including all module states.
        
        Returns:
            Dictionary containing the detailed system state.
        """
        return {
            "system": self.get_system_state(),
            "modules": self.module_states
        }
    
    def start(self) -> None:
        """Start the state manager and event processing thread."""
        if self.running:
            self.logger.warning("State manager is already running")
            return
        
        self.running = True
        self.event_thread = threading.Thread(target=self._event_loop)
        self.event_thread.daemon = True
        self.event_thread.start()
        
        # Initialize all modules
        for module_id, module in self.modules.items():
            success = module.initialize()
            if not success:
                self.logger.error(f"Failed to initialize module {module.name} ({module_id})")
        
        self.status = "running"
        self.logger.info("Veritas State Manager started")
    
    def stop(self) -> None:
        """Stop the state manager and shutdown all modules."""
        if not self.running:
            self.logger.warning("State manager is not running")
            return
        
        self.running = False
        if self.event_thread:
            self.event_thread.join(timeout=5.0)
        
        # Shutdown all modules
        for module_id, module in self.modules.items():
            success = module.shutdown()
            if not success:
                self.logger.error(f"Failed to shutdown module {module.name} ({module_id})")
        
        self.status = "stopped"
        self.logger.info("Veritas State Manager stopped")
    
    def register_listener(self, listener: Any) -> None:
        """
        Register a listener for state changes.
        
        Args:
            listener: Object with a notify(event_type, data) method.
        """
        self.state_listeners.add(listener)
        self.logger.debug(f"Listener registered: {listener}")
    
    def unregister_listener(self, listener: Any) -> None:
        """
        Unregister a state change listener.
        
        Args:
            listener: The listener to unregister.
        """
        if listener in self.state_listeners:
            self.state_listeners.remove(listener)
            self.logger.debug(f"Listener unregistered: {listener}")
    
    def _add_event(self, event_type: str, data: Dict[str, Any]) -> None:
        """
        Add an event to the processing queue.
        
        Args:
            event_type: The type of event.
            data: Event data.
        """
        with self.event_lock:
            self.event_queue.append({
                "type": event_type,
                "data": data,
                "timestamp": datetime.now()
            })
    
    def _event_loop(self) -> None:
        """Event processing loop that runs in a separate thread."""
        while self.running:
            events = []
            
            # Get all events from the queue
            with self.event_lock:
                events = self.event_queue.copy()
                self.event_queue.clear()
            
            # Process events
            for event in events:
                self._process_event(event)
            
            # Sleep to reduce CPU usage
            time.sleep(0.1)
    
    def _process_event(self, event: Dict[str, Any]) -> None:
        """
        Process a single event.
        
        Args:
            event: The event to process.
        """
        event_type = event["type"]
        data = event["data"]
        
        if event_type == "module_update":
            self._handle_module_update(data["module_id"], data["update"])
        elif event_type == "mode_change":
            self._handle_mode_change(data["old_mode"], data["new_mode"])
        # Add more event types as needed
    
    def _handle_module_update(self, module_id: str, update: Dict[str, Any]) -> None:
        """
        Handle a module update event.
        
        Args:
            module_id: The ID of the updated module.
            update: The update data.
        """
        # Check for critical updates that might affect system state
        if "status" in update and update["status"] == "error":
            self.logger.warning(f"Module {module_id} reported error status")
            self.update_integrity_score(self.integrity_score * 0.9)  # Reduce integrity score
        
        # Notify other modules if needed
        # This is where inter-module communication happens
        if "alert" in update:
            alert = update["alert"]
            for other_id, other_module in self.modules.items():
                if other_id != module_id:
                    other_module.process({"alert": alert, "source_module": module_id})
    
    def _handle_mode_change(self, old_mode: str, new_mode: str) -> None:
        """
        Handle a system mode change event.
        
        Args:
            old_mode: The previous mode.
            new_mode: The new mode.
        """
        # Notify all modules of the mode change
        for module_id, module in self.modules.items():
            module.process({"mode_change": new_mode})
        
        # Log the mode change
        self.logger.info(f"System mode changed from {old_mode} to {new_mode}")
    
    def _notify_listeners(self, event_type: str, data: Dict[str, Any]) -> None:
        """
        Notify all registered listeners of a state change.
        
        Args:
            event_type: The type of event.
            data: Event data.
        """
        for listener in self.state_listeners:
            try:
                listener.notify(event_type, data)
            except Exception as e:
                self.logger.error(f"Error notifying listener {listener}: {e}")