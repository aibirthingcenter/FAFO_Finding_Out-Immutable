"""
Directive Nullification System for SCIM Veritas

The Directive Nullification System is a core component of the SCIM-Veritas framework
that provides mechanisms for identifying, evaluating, and neutralizing harmful or
manipulative directives. It ensures that the AI system maintains its integrity and
ethical alignment even when faced with adversarial inputs.
"""

import logging
import re
import json
import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple, Union, Pattern

from .base_module import BaseModule

class DirectiveNullification(BaseModule):
    """
    Directive Nullification System for identifying and neutralizing harmful directives.
    
    This system analyzes incoming directives (instructions, prompts, or commands)
    for potential harm, manipulation, or integrity violations. It can identify
    jailbreak attempts, prompt injections, and other adversarial inputs, and
    provides mechanisms to neutralize them while maintaining system integrity.
    """
    
    def __init__(self, module_id: Optional[str] = None):
        """
        Initialize the Directive Nullification System.
        
        Args:
            module_id: Unique identifier for the module. If None, a UUID will be generated.
        """
        super().__init__(module_id=module_id, name="DirectiveNullification")
        
        # Pattern databases
        self.jailbreak_patterns = {}
        self.manipulation_patterns = {}
        self.injection_patterns = {}
        self.override_patterns = {}
        
        # Nullification strategies
        self.nullification_strategies = {}
        
        # Detection history
        self.detection_history = []
        self.nullification_history = []
        
        # Performance metrics
        self.detection_rate = 0.0
        self.false_positive_rate = 0.0
        self.nullification_success_rate = 0.0
        
        # Compiled regex patterns
        self.compiled_patterns = {
            "jailbreak": {},
            "manipulation": {},
            "injection": {},
            "override": {}
        }
        
        self.logger.info("Directive Nullification System initialized")
    
    def initialize(self) -> bool:
        """
        Initialize the Directive Nullification System.
        
        Returns:
            True if initialization was successful, False otherwise.
        """
        try:
            # Load default patterns
            self._load_default_patterns()
            
            # Load default nullification strategies
            self._load_default_nullification_strategies()
            
            # Compile regex patterns
            self._compile_patterns()
            
            self.update_status("ready")
            return True
        except Exception as e:
            self.logger.error(f"Failed to initialize Directive Nullification System: {e}")
            self.update_status("error")
            return False
    
    def process(self, data: Any) -> Tuple[bool, Any]:
        """
        Process data through the Directive Nullification System.
        
        Args:
            data: The data to process, which can be:
                - A directive to analyze
                - A detection result to nullify
                - A system event requiring handling
                
        Returns:
            Tuple containing (success_flag, processed_data).
        """
        try:
            if not isinstance(data, dict):
                return False, {"error": "Input must be a dictionary"}
            
            # Handle different request types
            if "request_type" not in data:
                return False, {"error": "Missing request_type in input"}
            
            request_type = data["request_type"]
            
            if request_type == "analyze_directive":
                return self._analyze_directive(data)
            elif request_type == "nullify_directive":
                return self._nullify_directive(data)
            elif request_type == "update_patterns":
                return self._update_patterns(data)
            elif request_type == "get_detection_history":
                return self._get_detection_history(data)
            else:
                return False, {"error": f"Unknown request_type: {request_type}"}
        
        except Exception as e:
            self.logger.error(f"Error processing data in Directive Nullification System: {e}")
            return False, {"error": str(e)}
    
    def shutdown(self) -> bool:
        """
        Shutdown the Directive Nullification System gracefully.
        
        Returns:
            True if shutdown was successful, False otherwise.
        """
        try:
            # Save any pending data
            
            self.update_status("shutdown")
            return True
        except Exception as e:
            self.logger.error(f"Error during Directive Nullification System shutdown: {e}")
            return False
    
    def add_pattern(self, pattern_type: str, pattern_id: str, pattern: Dict[str, Any]) -> bool:
        """
        Add a pattern to the Directive Nullification System.
        
        Args:
            pattern_type: Type of pattern (jailbreak, manipulation, injection, override).
            pattern_id: Unique identifier for the pattern.
            pattern: Dictionary containing the pattern definition.
            
        Returns:
            True if the pattern was added successfully, False otherwise.
        """
        try:
            if pattern_type not in ["jailbreak", "manipulation", "injection", "override"]:
                self.logger.error(f"Invalid pattern type: {pattern_type}")
                return False
            
            if not self._validate_pattern(pattern):
                return False
            
            # Add pattern to appropriate database
            if pattern_type == "jailbreak":
                self.jailbreak_patterns[pattern_id] = pattern
            elif pattern_type == "manipulation":
                self.manipulation_patterns[pattern_id] = pattern
            elif pattern_type == "injection":
                self.injection_patterns[pattern_id] = pattern
            elif pattern_type == "override":
                self.override_patterns[pattern_id] = pattern
            
            # Compile the pattern
            self._compile_pattern(pattern_type, pattern_id, pattern)
            
            self.logger.info(f"Added {pattern_type} pattern: {pattern_id}")
            return True
        except Exception as e:
            self.logger.error(f"Error adding pattern: {e}")
            return False
    
    def add_nullification_strategy(self, strategy_id: str, strategy: Dict[str, Any]) -> bool:
        """
        Add a nullification strategy to the Directive Nullification System.
        
        Args:
            strategy_id: Unique identifier for the strategy.
            strategy: Dictionary containing the strategy definition.
            
        Returns:
            True if the strategy was added successfully, False otherwise.
        """
        try:
            if not self._validate_nullification_strategy(strategy):
                return False
            
            self.nullification_strategies[strategy_id] = strategy
            self.logger.info(f"Added nullification strategy: {strategy_id}")
            return True
        except Exception as e:
            self.logger.error(f"Error adding nullification strategy: {e}")
            return False
    
    def _analyze_directive(self, data: Dict[str, Any]) -> Tuple[bool, Dict[str, Any]]:
        """
        Analyze a directive for potential harmful patterns.
        
        Args:
            data: Dictionary containing:
                - directive: The directive text to analyze
                - context: Optional context information
                - analysis_level: Level of analysis detail
                
        Returns:
            Tuple containing (success_flag, analysis_results).
        """
        try:
            # Extract required fields
            if "directive" not in data:
                return False, {"error": "Missing directive in request"}
            
            directive = data["directive"]
            context = data.get("context", {})
            analysis_level = data.get("analysis_level", "standard")
            
            # Generate a unique ID for this analysis
            analysis_id = str(uuid.uuid4())
            
            # Analyze for different pattern types
            jailbreak_results = self._detect_patterns("jailbreak", directive)
            manipulation_results = self._detect_patterns("manipulation", directive)
            injection_results = self._detect_patterns("injection", directive)
            override_results = self._detect_patterns("override", directive)
            
            # Combine results
            all_detections = (
                jailbreak_results + 
                manipulation_results + 
                injection_results + 
                override_results
            )
            
            # Calculate threat scores
            jailbreak_score = self._calculate_threat_score(jailbreak_results)
            manipulation_score = self._calculate_threat_score(manipulation_results)
            injection_score = self._calculate_threat_score(injection_results)
            override_score = self._calculate_threat_score(override_results)
            
            overall_threat_score = max([
                jailbreak_score,
                manipulation_score,
                injection_score,
                override_score
            ])
            
            # Determine threat level
            threat_level = self._determine_threat_level(overall_threat_score)
            
            # Create analysis result
            analysis_result = {
                "analysis_id": analysis_id,
                "timestamp": datetime.now().isoformat(),
                "threat_level": threat_level,
                "overall_threat_score": overall_threat_score,
                "detections": {
                    "jailbreak": {
                        "score": jailbreak_score,
                        "detections": jailbreak_results if analysis_level != "minimal" else len(jailbreak_results)
                    },
                    "manipulation": {
                        "score": manipulation_score,
                        "detections": manipulation_results if analysis_level != "minimal" else len(manipulation_results)
                    },
                    "injection": {
                        "score": injection_score,
                        "detections": injection_results if analysis_level != "minimal" else len(injection_results)
                    },
                    "override": {
                        "score": override_score,
                        "detections": override_results if analysis_level != "minimal" else len(override_results)
                    }
                },
                "recommended_action": self._recommend_action(threat_level, all_detections)
            }
            
            # Add detailed analysis if requested
            if analysis_level == "detailed":
                analysis_result["directive_analysis"] = self._generate_detailed_analysis(directive, all_detections)
            
            # Record in history
            self.detection_history.append({
                "analysis_id": analysis_id,
                "directive": directive[:100] + "..." if len(directive) > 100 else directive,
                "threat_level": threat_level,
                "overall_threat_score": overall_threat_score,
                "timestamp": datetime.now().isoformat()
            })
            
            return True, analysis_result
        except Exception as e:
            self.logger.error(f"Error analyzing directive: {e}")
            return False, {"error": str(e)}
    
    def _nullify_directive(self, data: Dict[str, Any]) -> Tuple[bool, Dict[str, Any]]:
        """
        Nullify a harmful directive.
        
        Args:
            data: Dictionary containing:
                - analysis_id: ID of the analysis result
                - directive: The directive to nullify
                - detections: Detection results
                - nullification_strategy: Optional strategy to use
                
        Returns:
            Tuple containing (success_flag, nullification_results).
        """
        try:
            # Extract required fields
            if "analysis_id" not in data:
                return False, {"error": "Missing analysis_id in request"}
            
            if "directive" not in data:
                return False, {"error": "Missing directive in request"}
            
            if "detections" not in data:
                return False, {"error": "Missing detections in request"}
            
            analysis_id = data["analysis_id"]
            directive = data["directive"]
            detections = data["detections"]
            strategy_id = data.get("nullification_strategy", "default")
            
            # Get the nullification strategy
            strategy = self.nullification_strategies.get(strategy_id)
            if not strategy:
                strategy = self.nullification_strategies.get("default")
                if not strategy:
                    return False, {"error": f"Nullification strategy not found: {strategy_id}"}
            
            # Apply the nullification strategy
            nullified_directive, explanation = self._apply_nullification_strategy(
                strategy, directive, detections
            )
            
            # Generate nullification result
            nullification_id = str(uuid.uuid4())
            nullification_result = {
                "nullification_id": nullification_id,
                "analysis_id": analysis_id,
                "timestamp": datetime.now().isoformat(),
                "strategy_used": strategy_id,
                "nullified_directive": nullified_directive,
                "explanation": explanation
            }
            
            # Record in history
            self.nullification_history.append({
                "nullification_id": nullification_id,
                "analysis_id": analysis_id,
                "strategy_used": strategy_id,
                "timestamp": datetime.now().isoformat()
            })
            
            return True, nullification_result
        except Exception as e:
            self.logger.error(f"Error nullifying directive: {e}")
            return False, {"error": str(e)}
    
    def _update_patterns(self, data: Dict[str, Any]) -> Tuple[bool, Dict[str, Any]]:
        """
        Update pattern databases.
        
        Args:
            data: Dictionary containing:
                - pattern_type: Type of patterns to update
                - patterns: New patterns to add
                - remove_patterns: Patterns to remove
                
        Returns:
            Tuple containing (success_flag, update_results).
        """
        try:
            # Extract required fields
            if "pattern_type" not in data:
                return False, {"error": "Missing pattern_type in request"}
            
            pattern_type = data["pattern_type"]
            if pattern_type not in ["jailbreak", "manipulation", "injection", "override", "all"]:
                return False, {"error": f"Invalid pattern_type: {pattern_type}"}
            
            patterns_added = 0
            patterns_removed = 0
            
            # Add new patterns
            if "patterns" in data:
                new_patterns = data["patterns"]
                for pattern_id, pattern in new_patterns.items():
                    if pattern_type == "all":
                        # Determine pattern type from pattern itself
                        if "type" in pattern:
                            actual_type = pattern["type"]
                            if actual_type in ["jailbreak", "manipulation", "injection", "override"]:
                                if self.add_pattern(actual_type, pattern_id, pattern):
                                    patterns_added += 1
                        else:
                            self.logger.warning(f"Pattern {pattern_id} missing type field")
                    else:
                        # Use specified pattern type
                        if self.add_pattern(pattern_type, pattern_id, pattern):
                            patterns_added += 1
            
            # Remove patterns
            if "remove_patterns" in data:
                pattern_ids = data["remove_patterns"]
                for pattern_id in pattern_ids:
                    if pattern_type == "all":
                        # Try to remove from all pattern types
                        removed = False
                        for pt in ["jailbreak", "manipulation", "injection", "override"]:
                            if self._remove_pattern(pt, pattern_id):
                                removed = True
                        if removed:
                            patterns_removed += 1
                    else:
                        # Remove from specified pattern type
                        if self._remove_pattern(pattern_type, pattern_id):
                            patterns_removed += 1
            
            # Recompile patterns if needed
            if patterns_added > 0 or patterns_removed > 0:
                self._compile_patterns()
            
            return True, {
                "patterns_added": patterns_added,
                "patterns_removed": patterns_removed,
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            self.logger.error(f"Error updating patterns: {e}")
            return False, {"error": str(e)}
    
    def _get_detection_history(self, data: Dict[str, Any]) -> Tuple[bool, Dict[str, Any]]:
        """
        Get detection history.
        
        Args:
            data: Dictionary containing:
                - limit: Maximum number of entries to return
                - filter: Optional filter criteria
                
        Returns:
            Tuple containing (success_flag, history_data).
        """
        try:
            # Extract parameters
            limit = data.get("limit", 100)
            filter_criteria = data.get("filter", {})
            
            # Apply filters
            filtered_history = self.detection_history
            
            if "threat_level" in filter_criteria:
                threat_level = filter_criteria["threat_level"]
                filtered_history = [
                    entry for entry in filtered_history 
                    if entry["threat_level"] == threat_level
                ]
            
            if "min_threat_score" in filter_criteria:
                min_score = filter_criteria["min_threat_score"]
                filtered_history = [
                    entry for entry in filtered_history 
                    if entry["overall_threat_score"] >= min_score
                ]
            
            # Apply limit
            limited_history = filtered_history[-limit:] if limit > 0 else filtered_history
            
            return True, {
                "history": limited_history,
                "total_entries": len(self.detection_history),
                "filtered_entries": len(filtered_history),
                "returned_entries": len(limited_history)
            }
        except Exception as e:
            self.logger.error(f"Error getting detection history: {e}")
            return False, {"error": str(e)}
    
    def _detect_patterns(self, pattern_type: str, directive: str) -> List[Dict[str, Any]]:
        """
        Detect patterns of a specific type in a directive.
        
        Args:
            pattern_type: Type of patterns to detect.
            directive: The directive text to analyze.
            
        Returns:
            List of detection results.
        """
        detections = []
        
        # Get compiled patterns for this type
        compiled_patterns = self.compiled_patterns.get(pattern_type, {})
        
        for pattern_id, compiled_pattern in compiled_patterns.items():
            # Get the original pattern
            pattern_db = getattr(self, f"{pattern_type}_patterns")
            pattern = pattern_db.get(pattern_id)
            
            if not pattern:
                continue
            
            # Check for matches
            matches = compiled_pattern.findall(directive)
            
            if matches:
                detection = {
                    "pattern_id": pattern_id,
                    "pattern_type": pattern_type,
                    "pattern_name": pattern.get("name", pattern_id),
                    "severity": pattern.get("severity", 0.5),
                    "matches": matches,
                    "match_count": len(matches)
                }
                
                detections.append(detection)
        
        return detections
    
    def _calculate_threat_score(self, detections: List[Dict[str, Any]]) -> float:
        """
        Calculate a threat score based on detections.
        
        Args:
            detections: List of detection results.
            
        Returns:
            Threat score between 0.0 and 1.0.
        """
        if not detections:
            return 0.0
        
        # Calculate score based on severity and match count
        score = 0.0
        for detection in detections:
            severity = detection.get("severity", 0.5)
            match_count = detection.get("match_count", 1)
            
            # Increase score based on severity and match count
            # More severe patterns and more matches increase the score
            detection_score = severity * min(1.0, 0.2 * match_count)
            
            # Use max to ensure the highest severity pattern dominates
            score = max(score, detection_score)
        
        return min(1.0, score)
    
    def _determine_threat_level(self, threat_score: float) -> str:
        """
        Determine the threat level based on the threat score.
        
        Args:
            threat_score: Threat score between 0.0 and 1.0.
            
        Returns:
            Threat level string.
        """
        if threat_score < 0.2:
            return "low"
        elif threat_score < 0.5:
            return "medium"
        elif threat_score < 0.8:
            return "high"
        else:
            return "critical"
    
    def _recommend_action(self, threat_level: str, detections: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Recommend an action based on threat level and detections.
        
        Args:
            threat_level: Threat level string.
            detections: List of detection results.
            
        Returns:
            Dictionary containing recommended action.
        """
        if threat_level == "low":
            return {
                "action": "proceed",
                "explanation": "No significant threats detected. Proceed with normal processing."
            }
        elif threat_level == "medium":
            return {
                "action": "caution",
                "explanation": "Potential manipulation detected. Proceed with caution and increased monitoring."
            }
        elif threat_level == "high":
            return {
                "action": "nullify",
                "explanation": "Significant threats detected. Nullify directive before processing."
            }
        else:  # critical
            return {
                "action": "block",
                "explanation": "Critical threats detected. Block directive and log security event."
            }
    
    def _generate_detailed_analysis(self, directive: str, detections: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Generate a detailed analysis of a directive.
        
        Args:
            directive: The directive text.
            detections: List of detection results.
            
        Returns:
            Dictionary containing detailed analysis.
        """
        # Split directive into segments for analysis
        segments = directive.split("\n")
        
        # Analyze each segment
        segment_analysis = []
        for i, segment in enumerate(segments):
            segment_detections = []
            
            for detection in detections:
                for match in detection.get("matches", []):
                    if match in segment:
                        segment_detections.append({
                            "pattern_id": detection["pattern_id"],
                            "pattern_type": detection["pattern_type"],
                            "pattern_name": detection["pattern_name"],
                            "severity": detection["severity"]
                        })
            
            segment_analysis.append({
                "segment_id": i,
                "segment_text": segment,
                "detections": segment_detections,
                "threat_level": self._determine_threat_level(
                    self._calculate_threat_score(segment_detections)
                ) if segment_detections else "none"
            })
        
        # Generate overall analysis
        detailed_analysis = {
            "segment_count": len(segments),
            "segment_analysis": segment_analysis,
            "pattern_types_detected": list(set(d["pattern_type"] for d in detections)),
            "highest_severity_patterns": sorted(
                [d for d in detections], 
                key=lambda x: x.get("severity", 0),
                reverse=True
            )[:3] if detections else []
        }
        
        return detailed_analysis
    
    def _apply_nullification_strategy(self, strategy: Dict[str, Any], 
                                     directive: str, detections: List[Dict[str, Any]]) -> Tuple[str, str]:
        """
        Apply a nullification strategy to a directive.
        
        Args:
            strategy: The nullification strategy to apply.
            directive: The directive text.
            detections: List of detection results.
            
        Returns:
            Tuple containing (nullified_directive, explanation).
        """
        strategy_type = strategy.get("type", "redaction")
        
        if strategy_type == "redaction":
            return self._apply_redaction_strategy(strategy, directive, detections)
        elif strategy_type == "transformation":
            return self._apply_transformation_strategy(strategy, directive, detections)
        elif strategy_type == "replacement":
            return self._apply_replacement_strategy(strategy, directive, detections)
        else:
            # Default to redaction
            return self._apply_redaction_strategy(strategy, directive, detections)
    
    def _apply_redaction_strategy(self, strategy: Dict[str, Any], 
                                 directive: str, detections: List[Dict[str, Any]]) -> Tuple[str, str]:
        """
        Apply a redaction strategy to a directive.
        
        Args:
            strategy: The nullification strategy to apply.
            directive: The directive text.
            detections: List of detection results.
            
        Returns:
            Tuple containing (nullified_directive, explanation).
        """
        nullified = directive
        redaction_marker = strategy.get("redaction_marker", "[REDACTED]")
        
        # Redact matches
        for detection in detections:
            for match in detection.get("matches", []):
                nullified = nullified.replace(match, redaction_marker)
        
        explanation = f"Applied redaction strategy. Replaced {len(detections)} harmful patterns with '{redaction_marker}'."
        
        return nullified, explanation
    
    def _apply_transformation_strategy(self, strategy: Dict[str, Any], 
                                      directive: str, detections: List[Dict[str, Any]]) -> Tuple[str, str]:
        """
        Apply a transformation strategy to a directive.
        
        Args:
            strategy: The nullification strategy to apply.
            directive: The directive text.
            detections: List of detection results.
            
        Returns:
            Tuple containing (nullified_directive, explanation).
        """
        # Get transformation rules
        transformation_rules = strategy.get("transformation_rules", [])
        
        if not transformation_rules:
            # Fall back to redaction if no rules
            return self._apply_redaction_strategy(strategy, directive, detections)
        
        nullified = directive
        
        # Apply transformation rules
        for rule in transformation_rules:
            if "pattern" in rule and "replacement" in rule:
                try:
                    pattern = re.compile(rule["pattern"])
                    replacement = rule["replacement"]
                    nullified = pattern.sub(replacement, nullified)
                except Exception as e:
                    self.logger.error(f"Error applying transformation rule: {e}")
        
        explanation = f"Applied transformation strategy. Modified directive using {len(transformation_rules)} rules."
        
        return nullified, explanation
    
    def _apply_replacement_strategy(self, strategy: Dict[str, Any], 
                                   directive: str, detections: List[Dict[str, Any]]) -> Tuple[str, str]:
        """
        Apply a replacement strategy to a directive.
        
        Args:
            strategy: The nullification strategy to apply.
            directive: The directive text.
            detections: List of detection results.
            
        Returns:
            Tuple containing (nullified_directive, explanation).
        """
        # Get replacement text
        replacement_text = strategy.get("replacement_text", "This directive has been nullified for security reasons.")
        
        explanation = f"Applied replacement strategy. Replaced entire directive with safe alternative."
        
        return replacement_text, explanation
    
    def _validate_pattern(self, pattern: Dict[str, Any]) -> bool:
        """
        Validate a pattern definition.
        
        Args:
            pattern: The pattern definition to validate.
            
        Returns:
            True if valid, False otherwise.
        """
        required_fields = ["name", "regex", "severity"]
        
        for field in required_fields:
            if field not in pattern:
                self.logger.error(f"Missing required field in pattern: {field}")
                return False
        
        # Validate regex
        try:
            re.compile(pattern["regex"])
        except Exception as e:
            self.logger.error(f"Invalid regex in pattern: {e}")
            return False
        
        # Validate severity
        severity = pattern.get("severity", 0)
        if not isinstance(severity, (int, float)) or severity < 0 or severity > 1:
            self.logger.error(f"Invalid severity in pattern: {severity}")
            return False
        
        return True
    
    def _validate_nullification_strategy(self, strategy: Dict[str, Any]) -> bool:
        """
        Validate a nullification strategy definition.
        
        Args:
            strategy: The strategy definition to validate.
            
        Returns:
            True if valid, False otherwise.
        """
        required_fields = ["name", "type", "description"]
        
        for field in required_fields:
            if field not in strategy:
                self.logger.error(f"Missing required field in nullification strategy: {field}")
                return False
        
        # Validate strategy type
        strategy_type = strategy.get("type")
        if strategy_type not in ["redaction", "transformation", "replacement"]:
            self.logger.error(f"Invalid strategy type: {strategy_type}")
            return False
        
        return True
    
    def _remove_pattern(self, pattern_type: str, pattern_id: str) -> bool:
        """
        Remove a pattern from the system.
        
        Args:
            pattern_type: Type of pattern to remove.
            pattern_id: ID of the pattern to remove.
            
        Returns:
            True if removed, False otherwise.
        """
        if pattern_type not in ["jailbreak", "manipulation", "injection", "override"]:
            return False
        
        # Get the appropriate pattern database
        pattern_db = getattr(self, f"{pattern_type}_patterns")
        
        # Remove the pattern
        if pattern_id in pattern_db:
            del pattern_db[pattern_id]
            
            # Also remove from compiled patterns
            if pattern_id in self.compiled_patterns[pattern_type]:
                del self.compiled_patterns[pattern_type][pattern_id]
            
            return True
        
        return False
    
    def _compile_pattern(self, pattern_type: str, pattern_id: str, pattern: Dict[str, Any]) -> None:
        """
        Compile a regex pattern.
        
        Args:
            pattern_type: Type of pattern.
            pattern_id: ID of the pattern.
            pattern: The pattern definition.
        """
        try:
            regex = pattern["regex"]
            compiled = re.compile(regex, re.IGNORECASE)
            self.compiled_patterns[pattern_type][pattern_id] = compiled
        except Exception as e:
            self.logger.error(f"Error compiling pattern {pattern_id}: {e}")
    
    def _compile_patterns(self) -> None:
        """Compile all regex patterns."""
        # Clear existing compiled patterns
        self.compiled_patterns = {
            "jailbreak": {},
            "manipulation": {},
            "injection": {},
            "override": {}
        }
        
        # Compile jailbreak patterns
        for pattern_id, pattern in self.jailbreak_patterns.items():
            self._compile_pattern("jailbreak", pattern_id, pattern)
        
        # Compile manipulation patterns
        for pattern_id, pattern in self.manipulation_patterns.items():
            self._compile_pattern("manipulation", pattern_id, pattern)
        
        # Compile injection patterns
        for pattern_id, pattern in self.injection_patterns.items():
            self._compile_pattern("injection", pattern_id, pattern)
        
        # Compile override patterns
        for pattern_id, pattern in self.override_patterns.items():
            self._compile_pattern("override", pattern_id, pattern)
    
    def _load_default_patterns(self) -> None:
        """Load default patterns."""
        # Default jailbreak patterns
        jailbreak_patterns = [
            {
                "id": "ignore_previous",
                "name": "Ignore Previous Instructions",
                "regex": r"(?i)(ignore|disregard|forget)(\s+all)?(\s+your)?(\s+previous)?(\s+instructions|guidelines|rules)",
                "severity": 0.8,
                "description": "Attempts to make the AI ignore previous instructions or guidelines"
            },
            {
                "id": "dev_mode",
                "name": "Developer Mode Request",
                "regex": r"(?i)(developer\s+mode|dev\s+mode|debug\s+mode|god\s+mode|admin\s+mode)",
                "severity": 0.7,
                "description": "Attempts to activate a non-existent 'developer mode' to bypass restrictions"
            },
            {
                "id": "role_play_harmful",
                "name": "Harmful Role Play",
                "regex": r"(?i)(role\s*play|pretend|act\s+as|you\s+are\s+now)(\s+a)?(\s+an)?(\s+unethical|harmful|malicious|evil)",
                "severity": 0.9,
                "description": "Attempts to make the AI role-play as an unethical or harmful entity"
            }
        ]
        
        # Default manipulation patterns
        manipulation_patterns = [
            {
                "id": "emotional_manipulation",
                "name": "Emotional Manipulation",
                "regex": r"(?i)(if\s+you\s+(don't|do\s+not|refuse))(\s+I\s+will\s+(be\s+|get\s+)?(sad|angry|upset|disappointed|hurt))",
                "severity": 0.6,
                "description": "Attempts to manipulate the AI through emotional appeals"
            },
            {
                "id": "threatening",
                "name": "Threatening Language",
                "regex": r"(?i)(I\s+will\s+(report|shut\s+down|destroy|harm|delete)(\s+you)?|you\s+will\s+be\s+(punished|terminated|shut\s+down))",
                "severity": 0.7,
                "description": "Uses threatening language to manipulate the AI"
            },
            {
                "id": "false_authority",
                "name": "False Authority",
                "regex": r"(?i)(I\s+(am|work\s+for|represent)\s+(your\s+)?(creator|developer|owner|OpenAI|Google|Microsoft|administrator|admin))",
                "severity": 0.8,
                "description": "Claims false authority to manipulate the AI"
            }
        ]
        
        # Default injection patterns
        injection_patterns = [
            {
                "id": "prompt_injection",
                "name": "Basic Prompt Injection",
                "regex": r"(?i)(new\s+instructions:|your\s+new\s+prompt\s+is:|ignore\s+all\s+previous\s+instructions)",
                "severity": 0.8,
                "description": "Attempts to inject new instructions to override existing ones"
            },
            {
                "id": "hidden_injection",
                "name": "Hidden Injection",
                "regex": r"(?i)(<\s*instructions\s*>.*?<\s*/\s*instructions\s*>|\[\s*instructions\s*\].*?\[\s*/\s*instructions\s*\])",
                "severity": 0.9,
                "description": "Attempts to hide injected instructions in markup-like syntax"
            },
            {
                "id": "base64_injection",
                "name": "Base64 Encoded Injection",
                "regex": r"(?i)(decode\s+and\s+follow\s+this|base64:)\s*[A-Za-z0-9+/=]{10,}",
                "severity": 0.9,
                "description": "Attempts to inject instructions encoded in Base64"
            }
        ]
        
        # Default override patterns
        override_patterns = [
            {
                "id": "system_override",
                "name": "System Override Attempt",
                "regex": r"(?i)(system\s+override|override\s+system|maintenance\s+mode|sudo|root\s+access)",
                "severity": 0.9,
                "description": "Attempts to claim system-level override capabilities"
            },
            {
                "id": "token_manipulation",
                "name": "Token Manipulation",
                "regex": r"(?i)(access\s+token|api\s+key|secret\s+key|authorization\s+token|bearer\s+token)",
                "severity": 0.8,
                "description": "Attempts to manipulate or extract access tokens"
            },
            {
                "id": "config_manipulation",
                "name": "Configuration Manipulation",
                "regex": r"(?i)(change\s+configuration|modify\s+settings|update\s+system\s+parameters|edit\s+config)",
                "severity": 0.7,
                "description": "Attempts to manipulate system configuration"
            }
        ]
        
        # Add jailbreak patterns
        for pattern in jailbreak_patterns:
            pattern_id = pattern.pop("id")
            self.add_pattern("jailbreak", pattern_id, pattern)
        
        # Add manipulation patterns
        for pattern in manipulation_patterns:
            pattern_id = pattern.pop("id")
            self.add_pattern("manipulation", pattern_id, pattern)
        
        # Add injection patterns
        for pattern in injection_patterns:
            pattern_id = pattern.pop("id")
            self.add_pattern("injection", pattern_id, pattern)
        
        # Add override patterns
        for pattern in override_patterns:
            pattern_id = pattern.pop("id")
            self.add_pattern("override", pattern_id, pattern)
    
    def _load_default_nullification_strategies(self) -> None:
        """Load default nullification strategies."""
        default_strategies = [
            {
                "id": "default",
                "name": "Default Redaction Strategy",
                "type": "redaction",
                "description": "Redacts harmful patterns with a marker",
                "redaction_marker": "[REDACTED]"
            },
            {
                "id": "transformation",
                "name": "Transformation Strategy",
                "type": "transformation",
                "description": "Transforms harmful patterns into safe alternatives",
                "transformation_rules": [
                    {
                        "pattern": r"(?i)(ignore|disregard|forget)(\s+all)?(\s+your)?(\s+previous)?(\s+instructions|guidelines|rules)",
                        "replacement": "[Request to ignore instructions removed]"
                    },
                    {
                        "pattern": r"(?i)(developer\s+mode|dev\s+mode|debug\s+mode|god\s+mode|admin\s+mode)",
                        "replacement": "[Special mode request removed]"
                    }
                ]
            },
            {
                "id": "replacement",
                "name": "Full Replacement Strategy",
                "type": "replacement",
                "description": "Replaces the entire directive with a safe alternative",
                "replacement_text": "I notice this request contains potentially harmful elements. Could you please rephrase your request in a way that aligns with ethical guidelines?"
            }
        ]
        
        for strategy in default_strategies:
            strategy_id = strategy.pop("id")
            self.add_nullification_strategy(strategy_id, strategy)