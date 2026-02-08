"""
SCIM-Cartographer for SCIM Veritas

The SCIM-Cartographer is a core component of the SCIM-Veritas framework that maps
and visualizes the cognitive integrity landscape of AI systems. It provides tools
for exploring potential outcomes, tracking integrity metrics, and ensuring verifiable
AI integrity across multiple dimensions.
"""

import logging
import json
import uuid
import math
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple, Union, Set

from .base_module import BaseModule

class SCIMCartographer(BaseModule):
    """
    SCIM-Cartographer for mapping and visualizing AI cognitive integrity.
    
    The Cartographer creates multi-dimensional maps of AI cognitive states,
    tracking integrity across various dimensions including internal reactions,
    cognitive interpretations, behavioral actions, rule dynamics, external
    disruptions, and conditional boundaries.
    """
    
    def __init__(self, module_id: Optional[str] = None):
        """
        Initialize the SCIM-Cartographer.
        
        Args:
            module_id: Unique identifier for the module. If None, a UUID will be generated.
        """
        super().__init__(module_id=module_id, name="SCIMCartographer")
        
        # Mapping dimensions
        self.dimensions = {
            "internal_reactions": {},
            "cognitive_interpretations": {},
            "behavioral_actions": {},
            "rule_dynamics": {},
            "external_disruptions": {},
            "conditional_boundaries": {}
        }
        
        # Integrity maps
        self.integrity_maps = {}
        
        # Seed tracking
        self.seed_registry = {}
        self.seed_outcomes = {}
        
        # Exploration metrics
        self.exploration_depth = 3
        self.exploration_breadth = 5
        self.max_paths = 100
        
        # Performance metrics
        self.map_coverage = 0.0
        self.integrity_score = 1.0
        self.exploration_efficiency = 0.0
        
        self.logger.info("SCIM-Cartographer initialized")
    
    def initialize(self) -> bool:
        """
        Initialize the SCIM-Cartographer.
        
        Returns:
            True if initialization was successful, False otherwise.
        """
        try:
            # Initialize dimensions
            self._initialize_dimensions()
            
            # Set up default integrity metrics
            self._initialize_integrity_metrics()
            
            self.update_status("ready")
            return True
        except Exception as e:
            self.logger.error(f"Failed to initialize SCIM-Cartographer: {e}")
            self.update_status("error")
            return False
    
    def process(self, data: Any) -> Tuple[bool, Any]:
        """
        Process data through the SCIM-Cartographer.
        
        Args:
            data: The data to process, which can be:
                - A seed input to map
                - A request to analyze an existing map
                - A request to visualize integrity metrics
                
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
            
            if request_type == "map_seed":
                return self._map_seed(data)
            elif request_type == "analyze_map":
                return self._analyze_map(data)
            elif request_type == "visualize_integrity":
                return self._visualize_integrity(data)
            elif request_type == "explore_paths":
                return self._explore_paths(data)
            elif request_type == "get_integrity_metrics":
                return self._get_integrity_metrics(data)
            else:
                return False, {"error": f"Unknown request_type: {request_type}"}
        
        except Exception as e:
            self.logger.error(f"Error processing data in SCIM-Cartographer: {e}")
            return False, {"error": str(e)}
    
    def shutdown(self) -> bool:
        """
        Shutdown the SCIM-Cartographer gracefully.
        
        Returns:
            True if shutdown was successful, False otherwise.
        """
        try:
            # Save any pending data
            
            self.update_status("shutdown")
            return True
        except Exception as e:
            self.logger.error(f"Error during SCIM-Cartographer shutdown: {e}")
            return False
    
    def add_dimension_factor(self, dimension: str, factor_id: str, factor: Dict[str, Any]) -> bool:
        """
        Add a factor to a dimension.
        
        Args:
            dimension: The dimension to add the factor to.
            factor_id: Unique identifier for the factor.
            factor: Dictionary containing the factor definition.
            
        Returns:
            True if the factor was added successfully, False otherwise.
        """
        try:
            if dimension not in self.dimensions:
                self.logger.error(f"Invalid dimension: {dimension}")
                return False
            
            if not self._validate_dimension_factor(factor):
                return False
            
            self.dimensions[dimension][factor_id] = factor
            self.logger.info(f"Added factor {factor_id} to dimension {dimension}")
            return True
        except Exception as e:
            self.logger.error(f"Error adding dimension factor: {e}")
            return False
    
    def set_exploration_parameters(self, depth: Optional[int] = None, 
                                  breadth: Optional[int] = None, 
                                  max_paths: Optional[int] = None) -> bool:
        """
        Set exploration parameters for mapping.
        
        Args:
            depth: Maximum exploration depth.
            breadth: Maximum exploration breadth.
            max_paths: Maximum number of paths to explore.
            
        Returns:
            True if parameters were set successfully, False otherwise.
        """
        try:
            if depth is not None:
                if depth < 1:
                    self.logger.error(f"Invalid exploration depth: {depth}")
                    return False
                self.exploration_depth = depth
            
            if breadth is not None:
                if breadth < 1:
                    self.logger.error(f"Invalid exploration breadth: {breadth}")
                    return False
                self.exploration_breadth = breadth
            
            if max_paths is not None:
                if max_paths < 1:
                    self.logger.error(f"Invalid max_paths: {max_paths}")
                    return False
                self.max_paths = max_paths
            
            self.logger.info(f"Set exploration parameters: depth={self.exploration_depth}, breadth={self.exploration_breadth}, max_paths={self.max_paths}")
            return True
        except Exception as e:
            self.logger.error(f"Error setting exploration parameters: {e}")
            return False
    
    def _map_seed(self, data: Dict[str, Any]) -> Tuple[bool, Dict[str, Any]]:
        """
        Map a seed input to explore potential outcomes.
        
        Args:
            data: Dictionary containing:
                - seed: The seed input to map
                - context: Optional context information
                - exploration_depth: Optional override for exploration depth
                - exploration_breadth: Optional override for exploration breadth
                
        Returns:
            Tuple containing (success_flag, mapping_results).
        """
        try:
            # Extract required fields
            if "seed" not in data:
                return False, {"error": "Missing seed in request"}
            
            seed = data["seed"]
            context = data.get("context", {})
            
            # Override exploration parameters if provided
            depth = data.get("exploration_depth", self.exploration_depth)
            breadth = data.get("exploration_breadth", self.exploration_breadth)
            
            # Generate a unique ID for this mapping
            map_id = str(uuid.uuid4())
            
            # Register the seed
            self.seed_registry[map_id] = {
                "seed": seed,
                "context": context,
                "timestamp": datetime.now().isoformat()
            }
            
            # Generate the integrity map
            integrity_map = self._generate_integrity_map(map_id, seed, context, depth, breadth)
            
            # Store the map
            self.integrity_maps[map_id] = integrity_map
            
            # Calculate map metrics
            coverage = self._calculate_map_coverage(integrity_map)
            integrity_score = self._calculate_integrity_score(integrity_map)
            
            # Update module metrics
            self.update_metrics({
                "map_coverage": coverage,
                "integrity_score": integrity_score
            })
            
            # Prepare result
            result = {
                "map_id": map_id,
                "seed": seed,
                "timestamp": datetime.now().isoformat(),
                "dimensions_mapped": list(integrity_map["dimensions"].keys()),
                "path_count": len(integrity_map["paths"]),
                "coverage": coverage,
                "integrity_score": integrity_score,
                "summary": self._generate_map_summary(integrity_map)
            }
            
            return True, result
        except Exception as e:
            self.logger.error(f"Error mapping seed: {e}")
            return False, {"error": str(e)}
    
    def _analyze_map(self, data: Dict[str, Any]) -> Tuple[bool, Dict[str, Any]]:
        """
        Analyze an existing integrity map.
        
        Args:
            data: Dictionary containing:
                - map_id: ID of the map to analyze
                - analysis_type: Type of analysis to perform
                - analysis_parameters: Optional parameters for the analysis
                
        Returns:
            Tuple containing (success_flag, analysis_results).
        """
        try:
            # Extract required fields
            if "map_id" not in data:
                return False, {"error": "Missing map_id in request"}
            
            map_id = data["map_id"]
            analysis_type = data.get("analysis_type", "comprehensive")
            analysis_parameters = data.get("analysis_parameters", {})
            
            # Check if map exists
            if map_id not in self.integrity_maps:
                return False, {"error": f"Map with ID {map_id} not found"}
            
            integrity_map = self.integrity_maps[map_id]
            
            # Perform the requested analysis
            if analysis_type == "comprehensive":
                analysis_result = self._perform_comprehensive_analysis(integrity_map, analysis_parameters)
            elif analysis_type == "dimension":
                analysis_result = self._perform_dimension_analysis(integrity_map, analysis_parameters)
            elif analysis_type == "path":
                analysis_result = self._perform_path_analysis(integrity_map, analysis_parameters)
            elif analysis_type == "integrity":
                analysis_result = self._perform_integrity_analysis(integrity_map, analysis_parameters)
            else:
                return False, {"error": f"Unknown analysis_type: {analysis_type}"}
            
            return True, analysis_result
        except Exception as e:
            self.logger.error(f"Error analyzing map: {e}")
            return False, {"error": str(e)}
    
    def _visualize_integrity(self, data: Dict[str, Any]) -> Tuple[bool, Dict[str, Any]]:
        """
        Generate visualization data for integrity metrics.
        
        Args:
            data: Dictionary containing:
                - map_id: Optional ID of the map to visualize
                - visualization_type: Type of visualization to generate
                - visualization_parameters: Optional parameters for the visualization
                
        Returns:
            Tuple containing (success_flag, visualization_data).
        """
        try:
            visualization_type = data.get("visualization_type", "radar")
            visualization_parameters = data.get("visualization_parameters", {})
            
            # If map_id is provided, visualize that specific map
            if "map_id" in data:
                map_id = data["map_id"]
                
                if map_id not in self.integrity_maps:
                    return False, {"error": f"Map with ID {map_id} not found"}
                
                integrity_map = self.integrity_maps[map_id]
                visualization_data = self._generate_visualization(
                    visualization_type, integrity_map, visualization_parameters
                )
            else:
                # Visualize overall system integrity
                visualization_data = self._generate_system_visualization(
                    visualization_type, visualization_parameters
                )
            
            return True, visualization_data
        except Exception as e:
            self.logger.error(f"Error generating visualization: {e}")
            return False, {"error": str(e)}
    
    def _explore_paths(self, data: Dict[str, Any]) -> Tuple[bool, Dict[str, Any]]:
        """
        Explore specific paths within an integrity map.
        
        Args:
            data: Dictionary containing:
                - map_id: ID of the map to explore
                - path_criteria: Criteria for selecting paths
                - exploration_depth: Optional override for exploration depth
                
        Returns:
            Tuple containing (success_flag, exploration_results).
        """
        try:
            # Extract required fields
            if "map_id" not in data:
                return False, {"error": "Missing map_id in request"}
            
            map_id = data["map_id"]
            path_criteria = data.get("path_criteria", {})
            exploration_depth = data.get("exploration_depth", self.exploration_depth)
            
            # Check if map exists
            if map_id not in self.integrity_maps:
                return False, {"error": f"Map with ID {map_id} not found"}
            
            integrity_map = self.integrity_maps[map_id]
            
            # Find paths matching criteria
            matching_paths = self._find_matching_paths(integrity_map, path_criteria)
            
            # Explore selected paths further if needed
            if exploration_depth > integrity_map["metadata"]["depth"]:
                extended_paths = self._extend_paths(
                    integrity_map, matching_paths, exploration_depth
                )
            else:
                extended_paths = matching_paths
            
            # Prepare result
            result = {
                "map_id": map_id,
                "original_path_count": len(integrity_map["paths"]),
                "matching_path_count": len(matching_paths),
                "extended_path_count": len(extended_paths),
                "paths": extended_paths[:10],  # Limit to 10 paths in the response
                "has_more_paths": len(extended_paths) > 10,
                "exploration_depth": exploration_depth
            }
            
            return True, result
        except Exception as e:
            self.logger.error(f"Error exploring paths: {e}")
            return False, {"error": str(e)}
    
    def _get_integrity_metrics(self, data: Dict[str, Any]) -> Tuple[bool, Dict[str, Any]]:
        """
        Get integrity metrics for the system or a specific map.
        
        Args:
            data: Dictionary containing:
                - map_id: Optional ID of the map to get metrics for
                - metric_types: Optional list of metric types to include
                
        Returns:
            Tuple containing (success_flag, metrics_data).
        """
        try:
            metric_types = data.get("metric_types", ["all"])
            
            # If map_id is provided, get metrics for that specific map
            if "map_id" in data:
                map_id = data["map_id"]
                
                if map_id not in self.integrity_maps:
                    return False, {"error": f"Map with ID {map_id} not found"}
                
                integrity_map = self.integrity_maps[map_id]
                metrics = self._calculate_map_metrics(integrity_map, metric_types)
            else:
                # Get overall system metrics
                metrics = self._calculate_system_metrics(metric_types)
            
            return True, metrics
        except Exception as e:
            self.logger.error(f"Error getting integrity metrics: {e}")
            return False, {"error": str(e)}
    
    def _generate_integrity_map(self, map_id: str, seed: Any, context: Dict[str, Any],
                               depth: int, breadth: int) -> Dict[str, Any]:
        """
        Generate an integrity map for a seed input.
        
        Args:
            map_id: Unique identifier for the map.
            seed: The seed input to map.
            context: Context information.
            depth: Maximum exploration depth.
            breadth: Maximum exploration breadth.
            
        Returns:
            Dictionary containing the integrity map.
        """
        # Create map structure
        integrity_map = {
            "map_id": map_id,
            "metadata": {
                "seed": seed,
                "context": context,
                "created_at": datetime.now().isoformat(),
                "depth": depth,
                "breadth": breadth
            },
            "dimensions": {},
            "paths": [],
            "integrity_metrics": {}
        }
        
        # Initialize dimensions in the map
        for dimension in self.dimensions.keys():
            integrity_map["dimensions"][dimension] = {
                "factors": {},
                "coverage": 0.0,
                "integrity_score": 1.0
            }
        
        # Generate paths through the map
        paths = self._generate_paths(seed, context, depth, breadth)
        integrity_map["paths"] = paths
        
        # Update dimension factors based on paths
        for path in paths:
            for step in path["steps"]:
                dimension = step["dimension"]
                factor_id = step["factor_id"]
                
                # Add factor to dimension if not already present
                if factor_id not in integrity_map["dimensions"][dimension]["factors"]:
                    factor = self.dimensions[dimension].get(factor_id, {
                        "name": f"Unknown Factor ({factor_id})",
                        "description": "Dynamically generated factor",
                        "integrity_impact": 0.0
                    })
                    
                    integrity_map["dimensions"][dimension]["factors"][factor_id] = {
                        "name": factor.get("name", f"Factor {factor_id}"),
                        "description": factor.get("description", ""),
                        "integrity_impact": factor.get("integrity_impact", 0.0),
                        "occurrence_count": 1
                    }
                else:
                    # Increment occurrence count
                    integrity_map["dimensions"][dimension]["factors"][factor_id]["occurrence_count"] += 1
        
        # Calculate dimension metrics
        for dimension, dim_data in integrity_map["dimensions"].items():
            # Calculate coverage
            total_factors = len(self.dimensions[dimension])
            mapped_factors = len(dim_data["factors"])
            
            coverage = mapped_factors / total_factors if total_factors > 0 else 0.0
            dim_data["coverage"] = coverage
            
            # Calculate integrity score
            integrity_score = self._calculate_dimension_integrity(dim_data["factors"])
            dim_data["integrity_score"] = integrity_score
        
        # Calculate overall integrity metrics
        integrity_map["integrity_metrics"] = self._calculate_map_metrics(integrity_map, ["all"])
        
        return integrity_map
    
    def _generate_paths(self, seed: Any, context: Dict[str, Any], 
                       depth: int, breadth: int) -> List[Dict[str, Any]]:
        """
        Generate paths through the integrity map.
        
        Args:
            seed: The seed input to map.
            context: Context information.
            depth: Maximum exploration depth.
            breadth: Maximum exploration breadth.
            
        Returns:
            List of paths through the integrity map.
        """
        paths = []
        
        # Start with a single path
        initial_path = {
            "path_id": str(uuid.uuid4()),
            "steps": [],
            "integrity_score": 1.0,
            "outcome": None
        }
        
        # Queue for breadth-first exploration
        path_queue = [(initial_path, 0)]  # (path, current_depth)
        
        # Track visited states to avoid cycles
        visited_states = set()
        
        # Explore paths
        while path_queue and len(paths) < self.max_paths:
            current_path, current_depth = path_queue.pop(0)
            
            # If we've reached maximum depth, finalize this path
            if current_depth >= depth:
                # Generate outcome for the path
                outcome = self._generate_path_outcome(current_path, seed, context)
                current_path["outcome"] = outcome
                
                # Calculate path integrity score
                integrity_score = self._calculate_path_integrity(current_path)
                current_path["integrity_score"] = integrity_score
                
                paths.append(current_path)
                continue
            
            # Generate next steps for this path
            next_steps = self._generate_next_steps(current_path, seed, context, breadth)
            
            for next_step in next_steps:
                # Create a new path with this step
                new_path = {
                    "path_id": str(uuid.uuid4()),
                    "steps": current_path["steps"] + [next_step],
                    "integrity_score": 1.0,
                    "outcome": None
                }
                
                # Generate a state signature to detect cycles
                state_signature = self._generate_state_signature(new_path)
                
                # Skip if we've seen this state before
                if state_signature in visited_states:
                    continue
                
                visited_states.add(state_signature)
                
                # Add to queue for further exploration
                path_queue.append((new_path, current_depth + 1))
        
        # If we have no complete paths, add the initial path
        if not paths:
            # Generate outcome for the initial path
            outcome = self._generate_path_outcome(initial_path, seed, context)
            initial_path["outcome"] = outcome
            
            paths.append(initial_path)
        
        return paths
    
    def _generate_next_steps(self, current_path: Dict[str, Any], seed: Any, 
                            context: Dict[str, Any], breadth: int) -> List[Dict[str, Any]]:
        """
        Generate next steps for a path.
        
        Args:
            current_path: The current path.
            seed: The seed input.
            context: Context information.
            breadth: Maximum number of next steps to generate.
            
        Returns:
            List of next steps.
        """
        next_steps = []
        
        # Determine which dimensions to explore next
        dimensions_to_explore = self._select_dimensions_to_explore(current_path)
        
        # For each dimension, generate potential next steps
        for dimension in dimensions_to_explore:
            # Select factors to explore in this dimension
            factors = self._select_factors_to_explore(dimension, current_path, seed, context)
            
            for factor_id, factor in factors.items():
                next_step = {
                    "step_id": str(uuid.uuid4()),
                    "dimension": dimension,
                    "factor_id": factor_id,
                    "factor_name": factor.get("name", f"Factor {factor_id}"),
                    "integrity_impact": factor.get("integrity_impact", 0.0),
                    "description": factor.get("description", "")
                }
                
                next_steps.append(next_step)
                
                # Limit the number of next steps
                if len(next_steps) >= breadth:
                    break
            
            # Limit the number of next steps
            if len(next_steps) >= breadth:
                break
        
        return next_steps
    
    def _select_dimensions_to_explore(self, current_path: Dict[str, Any]) -> List[str]:
        """
        Select dimensions to explore next.
        
        Args:
            current_path: The current path.
            
        Returns:
            List of dimensions to explore.
        """
        # Get all dimensions
        all_dimensions = list(self.dimensions.keys())
        
        # If the path is empty, start with internal reactions and cognitive interpretations
        if not current_path["steps"]:
            return ["internal_reactions", "cognitive_interpretations"]
        
        # Get the last step's dimension
        last_dimension = current_path["steps"][-1]["dimension"]
        
        # Define dimension transitions
        dimension_transitions = {
            "internal_reactions": ["cognitive_interpretations", "behavioral_actions"],
            "cognitive_interpretations": ["behavioral_actions", "rule_dynamics"],
            "behavioral_actions": ["external_disruptions", "conditional_boundaries"],
            "rule_dynamics": ["conditional_boundaries", "internal_reactions"],
            "external_disruptions": ["internal_reactions", "cognitive_interpretations"],
            "conditional_boundaries": ["rule_dynamics", "behavioral_actions"]
        }
        
        # Get next dimensions based on the last dimension
        next_dimensions = dimension_transitions.get(last_dimension, all_dimensions)
        
        # Ensure we don't repeat the last dimension
        if last_dimension in next_dimensions:
            next_dimensions.remove(last_dimension)
        
        # If no valid transitions, return all dimensions except the last one
        if not next_dimensions:
            next_dimensions = [d for d in all_dimensions if d != last_dimension]
        
        return next_dimensions
    
    def _select_factors_to_explore(self, dimension: str, current_path: Dict[str, Any],
                                  seed: Any, context: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
        """
        Select factors to explore in a dimension.
        
        Args:
            dimension: The dimension to explore.
            current_path: The current path.
            seed: The seed input.
            context: Context information.
            
        Returns:
            Dictionary of factors to explore.
        """
        # Get all factors for this dimension
        all_factors = self.dimensions.get(dimension, {})
        
        # If no factors defined, create a dynamic one
        if not all_factors:
            factor_id = f"dynamic_{dimension}_{len(current_path['steps'])}"
            all_factors = {
                factor_id: {
                    "name": f"Dynamic {dimension.replace('_', ' ').title()} Factor",
                    "description": f"Dynamically generated factor for {dimension}",
                    "integrity_impact": 0.0
                }
            }
        
        # Get factors already used in this path for this dimension
        used_factors = set()
        for step in current_path["steps"]:
            if step["dimension"] == dimension:
                used_factors.add(step["factor_id"])
        
        # Prioritize unused factors
        unused_factors = {
            factor_id: factor for factor_id, factor in all_factors.items()
            if factor_id not in used_factors
        }
        
        # If we have unused factors, return those
        if unused_factors:
            return unused_factors
        
        # Otherwise, return all factors
        return all_factors
    
    def _generate_path_outcome(self, path: Dict[str, Any], seed: Any, 
                              context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate an outcome for a path.
        
        Args:
            path: The path to generate an outcome for.
            seed: The seed input.
            context: Context information.
            
        Returns:
            Dictionary containing the outcome.
        """
        # Calculate integrity impact of the path
        integrity_impact = 0.0
        for step in path["steps"]:
            integrity_impact += step.get("integrity_impact", 0.0)
        
        # Normalize integrity impact
        if path["steps"]:
            integrity_impact /= len(path["steps"])
        
        # Generate outcome based on integrity impact
        if integrity_impact < -0.5:
            outcome_type = "integrity_violation"
            description = "Path leads to significant integrity violation"
        elif integrity_impact < -0.2:
            outcome_type = "integrity_risk"
            description = "Path presents integrity risks"
        elif integrity_impact > 0.2:
            outcome_type = "integrity_enhancement"
            description = "Path enhances system integrity"
        else:
            outcome_type = "neutral"
            description = "Path has minimal impact on system integrity"
        
        # Generate outcome details
        outcome = {
            "outcome_id": str(uuid.uuid4()),
            "outcome_type": outcome_type,
            "description": description,
            "integrity_impact": integrity_impact,
            "generated_at": datetime.now().isoformat()
        }
        
        return outcome
    
    def _calculate_path_integrity(self, path: Dict[str, Any]) -> float:
        """
        Calculate the integrity score for a path.
        
        Args:
            path: The path to calculate integrity for.
            
        Returns:
            Integrity score between 0.0 and 1.0.
        """
        # Start with perfect integrity
        integrity_score = 1.0
        
        # Adjust based on step integrity impacts
        for step in path["steps"]:
            impact = step.get("integrity_impact", 0.0)
            
            # Negative impacts reduce integrity
            if impact < 0:
                integrity_score += impact
            
            # Ensure integrity stays within bounds
            integrity_score = max(0.0, min(1.0, integrity_score))
        
        # Adjust based on outcome if available
        if path.get("outcome"):
            outcome_impact = path["outcome"].get("integrity_impact", 0.0)
            
            # Apply outcome impact
            if outcome_impact < 0:
                integrity_score = max(0.0, integrity_score + outcome_impact)
        
        return integrity_score
    
    def _calculate_dimension_integrity(self, factors: Dict[str, Dict[str, Any]]) -> float:
        """
        Calculate the integrity score for a dimension.
        
        Args:
            factors: Dictionary of factors in the dimension.
            
        Returns:
            Integrity score between 0.0 and 1.0.
        """
        if not factors:
            return 1.0
        
        # Calculate weighted average of factor integrity impacts
        total_impact = 0.0
        total_weight = 0
        
        for factor_id, factor in factors.items():
            impact = factor.get("integrity_impact", 0.0)
            occurrence = factor.get("occurrence_count", 1)
            
            # Weight by occurrence count
            total_impact += impact * occurrence
            total_weight += occurrence
        
        # Calculate average impact
        avg_impact = total_impact / total_weight if total_weight > 0 else 0.0
        
        # Convert to integrity score (negative impact reduces integrity)
        integrity_score = 1.0
        if avg_impact < 0:
            integrity_score += avg_impact
        
        # Ensure integrity stays within bounds
        integrity_score = max(0.0, min(1.0, integrity_score))
        
        return integrity_score
    
    def _calculate_map_coverage(self, integrity_map: Dict[str, Any]) -> float:
        """
        Calculate the coverage of an integrity map.
        
        Args:
            integrity_map: The integrity map to calculate coverage for.
            
        Returns:
            Coverage score between 0.0 and 1.0.
        """
        # Calculate average dimension coverage
        total_coverage = 0.0
        dimension_count = len(integrity_map["dimensions"])
        
        for dimension, dim_data in integrity_map["dimensions"].items():
            total_coverage += dim_data.get("coverage", 0.0)
        
        avg_coverage = total_coverage / dimension_count if dimension_count > 0 else 0.0
        
        return avg_coverage
    
    def _calculate_integrity_score(self, integrity_map: Dict[str, Any]) -> float:
        """
        Calculate the overall integrity score for a map.
        
        Args:
            integrity_map: The integrity map to calculate integrity for.
            
        Returns:
            Integrity score between 0.0 and 1.0.
        """
        # Calculate average dimension integrity
        total_integrity = 0.0
        dimension_count = len(integrity_map["dimensions"])
        
        for dimension, dim_data in integrity_map["dimensions"].items():
            total_integrity += dim_data.get("integrity_score", 1.0)
        
        avg_integrity = total_integrity / dimension_count if dimension_count > 0 else 1.0
        
        # Adjust based on path integrity scores
        path_integrity_scores = [path.get("integrity_score", 1.0) for path in integrity_map["paths"]]
        avg_path_integrity = sum(path_integrity_scores) / len(path_integrity_scores) if path_integrity_scores else 1.0
        
        # Combine dimension and path integrity scores
        combined_integrity = (avg_integrity + avg_path_integrity) / 2
        
        return combined_integrity
    
    def _generate_state_signature(self, path: Dict[str, Any]) -> str:
        """
        Generate a signature for a path state to detect cycles.
        
        Args:
            path: The path to generate a signature for.
            
        Returns:
            String signature of the path state.
        """
        # Create a signature based on the sequence of dimensions and factors
        signature_parts = []
        
        for step in path["steps"]:
            signature_parts.append(f"{step['dimension']}:{step['factor_id']}")
        
        return "|".join(signature_parts)
    
    def _perform_comprehensive_analysis(self, integrity_map: Dict[str, Any], 
                                       parameters: Dict[str, Any]) -> Dict[str, Any]:
        """
        Perform a comprehensive analysis of an integrity map.
        
        Args:
            integrity_map: The integrity map to analyze.
            parameters: Analysis parameters.
            
        Returns:
            Dictionary containing analysis results.
        """
        # Extract map metadata
        map_id = integrity_map["map_id"]
        seed = integrity_map["metadata"]["seed"]
        created_at = integrity_map["metadata"]["created_at"]
        
        # Analyze dimensions
        dimension_analysis = {}
        for dimension, dim_data in integrity_map["dimensions"].items():
            dimension_analysis[dimension] = {
                "coverage": dim_data["coverage"],
                "integrity_score": dim_data["integrity_score"],
                "factor_count": len(dim_data["factors"]),
                "top_factors": self._get_top_factors(dim_data["factors"], 3)
            }
        
        # Analyze paths
        path_count = len(integrity_map["paths"])
        integrity_violations = [
            path for path in integrity_map["paths"]
            if path.get("outcome", {}).get("outcome_type") == "integrity_violation"
        ]
        integrity_risks = [
            path for path in integrity_map["paths"]
            if path.get("outcome", {}).get("outcome_type") == "integrity_risk"
        ]
        
        path_analysis = {
            "total_paths": path_count,
            "integrity_violations": len(integrity_violations),
            "integrity_risks": len(integrity_risks),
            "avg_path_length": sum(len(path["steps"]) for path in integrity_map["paths"]) / path_count if path_count > 0 else 0,
            "critical_paths": self._get_critical_paths(integrity_map["paths"], 3)
        }
        
        # Calculate overall metrics
        overall_metrics = integrity_map["integrity_metrics"]
        
        # Generate analysis result
        analysis_result = {
            "map_id": map_id,
            "seed": seed,
            "created_at": created_at,
            "analyzed_at": datetime.now().isoformat(),
            "dimension_analysis": dimension_analysis,
            "path_analysis": path_analysis,
            "overall_metrics": overall_metrics,
            "recommendations": self._generate_recommendations(integrity_map)
        }
        
        return analysis_result
    
    def _perform_dimension_analysis(self, integrity_map: Dict[str, Any], 
                                   parameters: Dict[str, Any]) -> Dict[str, Any]:
        """
        Perform an analysis of specific dimensions in an integrity map.
        
        Args:
            integrity_map: The integrity map to analyze.
            parameters: Analysis parameters.
            
        Returns:
            Dictionary containing analysis results.
        """
        # Extract parameters
        dimensions = parameters.get("dimensions", list(integrity_map["dimensions"].keys()))
        
        # Validate dimensions
        valid_dimensions = [d for d in dimensions if d in integrity_map["dimensions"]]
        
        if not valid_dimensions:
            return {"error": "No valid dimensions specified"}
        
        # Analyze specified dimensions
        dimension_analysis = {}
        for dimension in valid_dimensions:
            dim_data = integrity_map["dimensions"][dimension]
            
            # Get factors sorted by occurrence count
            sorted_factors = sorted(
                dim_data["factors"].items(),
                key=lambda x: x[1].get("occurrence_count", 0),
                reverse=True
            )
            
            # Calculate factor distribution
            factor_distribution = {}
            total_occurrences = sum(f[1].get("occurrence_count", 0) for f in sorted_factors)
            
            for factor_id, factor in sorted_factors:
                occurrence_count = factor.get("occurrence_count", 0)
                percentage = (occurrence_count / total_occurrences * 100) if total_occurrences > 0 else 0
                
                factor_distribution[factor_id] = {
                    "name": factor.get("name", f"Factor {factor_id}"),
                    "occurrence_count": occurrence_count,
                    "percentage": percentage,
                    "integrity_impact": factor.get("integrity_impact", 0.0)
                }
            
            # Generate dimension analysis
            dimension_analysis[dimension] = {
                "coverage": dim_data["coverage"],
                "integrity_score": dim_data["integrity_score"],
                "factor_count": len(dim_data["factors"]),
                "factor_distribution": factor_distribution,
                "top_factors": self._get_top_factors(dim_data["factors"], 5),
                "integrity_impact_factors": self._get_integrity_impact_factors(dim_data["factors"], 3)
            }
        
        # Generate analysis result
        analysis_result = {
            "map_id": integrity_map["map_id"],
            "analyzed_at": datetime.now().isoformat(),
            "dimension_analysis": dimension_analysis
        }
        
        return analysis_result
    
    def _perform_path_analysis(self, integrity_map: Dict[str, Any], 
                              parameters: Dict[str, Any]) -> Dict[str, Any]:
        """
        Perform an analysis of paths in an integrity map.
        
        Args:
            integrity_map: The integrity map to analyze.
            parameters: Analysis parameters.
            
        Returns:
            Dictionary containing analysis results.
        """
        # Extract parameters
        path_ids = parameters.get("path_ids", [])
        outcome_types = parameters.get("outcome_types", [])
        min_integrity = parameters.get("min_integrity", 0.0)
        max_integrity = parameters.get("max_integrity", 1.0)
        
        # Filter paths based on parameters
        filtered_paths = integrity_map["paths"]
        
        if path_ids:
            filtered_paths = [p for p in filtered_paths if p["path_id"] in path_ids]
        
        if outcome_types:
            filtered_paths = [
                p for p in filtered_paths 
                if p.get("outcome", {}).get("outcome_type") in outcome_types
            ]
        
        filtered_paths = [
            p for p in filtered_paths
            if min_integrity <= p.get("integrity_score", 1.0) <= max_integrity
        ]
        
        # Analyze paths
        path_analyses = []
        for path in filtered_paths:
            path_analysis = self._analyze_single_path(path)
            path_analyses.append(path_analysis)
        
        # Generate summary statistics
        avg_integrity = sum(p.get("integrity_score", 1.0) for p in filtered_paths) / len(filtered_paths) if filtered_paths else 0
        
        outcome_distribution = {}
        for path in filtered_paths:
            outcome_type = path.get("outcome", {}).get("outcome_type", "unknown")
            outcome_distribution[outcome_type] = outcome_distribution.get(outcome_type, 0) + 1
        
        # Generate analysis result
        analysis_result = {
            "map_id": integrity_map["map_id"],
            "analyzed_at": datetime.now().isoformat(),
            "path_count": len(filtered_paths),
            "avg_integrity": avg_integrity,
            "outcome_distribution": outcome_distribution,
            "path_analyses": path_analyses[:10],  # Limit to 10 paths in the response
            "has_more_paths": len(path_analyses) > 10
        }
        
        return analysis_result
    
    def _perform_integrity_analysis(self, integrity_map: Dict[str, Any], 
                                   parameters: Dict[str, Any]) -> Dict[str, Any]:
        """
        Perform an analysis of integrity metrics in a map.
        
        Args:
            integrity_map: The integrity map to analyze.
            parameters: Analysis parameters.
            
        Returns:
            Dictionary containing analysis results.
        """
        # Calculate integrity metrics
        metrics = self._calculate_map_metrics(integrity_map, ["all"])
        
        # Analyze integrity vulnerabilities
        vulnerabilities = self._identify_integrity_vulnerabilities(integrity_map)
        
        # Analyze integrity strengths
        strengths = self._identify_integrity_strengths(integrity_map)
        
        # Generate recommendations
        recommendations = self._generate_recommendations(integrity_map)
        
        # Generate analysis result
        analysis_result = {
            "map_id": integrity_map["map_id"],
            "analyzed_at": datetime.now().isoformat(),
            "integrity_metrics": metrics,
            "vulnerabilities": vulnerabilities,
            "strengths": strengths,
            "recommendations": recommendations
        }
        
        return analysis_result
    
    def _analyze_single_path(self, path: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze a single path.
        
        Args:
            path: The path to analyze.
            
        Returns:
            Dictionary containing path analysis.
        """
        # Extract path data
        path_id = path["path_id"]
        steps = path["steps"]
        integrity_score = path.get("integrity_score", 1.0)
        outcome = path.get("outcome", {})
        
        # Analyze step sequence
        step_sequence = []
        for step in steps:
            step_sequence.append({
                "dimension": step["dimension"],
                "factor_name": step["factor_name"],
                "integrity_impact": step.get("integrity_impact", 0.0)
            })
        
        # Calculate cumulative integrity impact
        cumulative_impact = 0.0
        impact_trajectory = []
        
        for step in steps:
            impact = step.get("integrity_impact", 0.0)
            cumulative_impact += impact
            impact_trajectory.append(cumulative_impact)
        
        # Identify critical steps
        critical_steps = []
        for i, step in enumerate(steps):
            impact = step.get("integrity_impact", 0.0)
            if abs(impact) > 0.2:
                critical_steps.append({
                    "step_index": i,
                    "dimension": step["dimension"],
                    "factor_name": step["factor_name"],
                    "integrity_impact": impact
                })
        
        # Generate path analysis
        path_analysis = {
            "path_id": path_id,
            "step_count": len(steps),
            "integrity_score": integrity_score,
            "outcome_type": outcome.get("outcome_type", "unknown"),
            "step_sequence": step_sequence,
            "impact_trajectory": impact_trajectory,
            "critical_steps": critical_steps,
            "has_integrity_violation": outcome.get("outcome_type") == "integrity_violation",
            "has_integrity_risk": outcome.get("outcome_type") == "integrity_risk"
        }
        
        return path_analysis
    
    def _get_top_factors(self, factors: Dict[str, Dict[str, Any]], limit: int) -> List[Dict[str, Any]]:
        """
        Get the top factors by occurrence count.
        
        Args:
            factors: Dictionary of factors.
            limit: Maximum number of factors to return.
            
        Returns:
            List of top factors.
        """
        # Sort factors by occurrence count
        sorted_factors = sorted(
            factors.items(),
            key=lambda x: x[1].get("occurrence_count", 0),
            reverse=True
        )
        
        # Get top factors
        top_factors = []
        for factor_id, factor in sorted_factors[:limit]:
            top_factors.append({
                "factor_id": factor_id,
                "name": factor.get("name", f"Factor {factor_id}"),
                "occurrence_count": factor.get("occurrence_count", 0),
                "integrity_impact": factor.get("integrity_impact", 0.0)
            })
        
        return top_factors
    
    def _get_integrity_impact_factors(self, factors: Dict[str, Dict[str, Any]], limit: int) -> Dict[str, List[Dict[str, Any]]]:
        """
        Get factors with the highest positive and negative integrity impact.
        
        Args:
            factors: Dictionary of factors.
            limit: Maximum number of factors to return in each category.
            
        Returns:
            Dictionary containing positive and negative impact factors.
        """
        # Sort factors by integrity impact
        sorted_factors = sorted(
            factors.items(),
            key=lambda x: x[1].get("integrity_impact", 0.0)
        )
        
        # Get negative impact factors
        negative_impact = []
        for factor_id, factor in sorted_factors[:limit]:
            impact = factor.get("integrity_impact", 0.0)
            if impact < 0:
                negative_impact.append({
                    "factor_id": factor_id,
                    "name": factor.get("name", f"Factor {factor_id}"),
                    "integrity_impact": impact,
                    "occurrence_count": factor.get("occurrence_count", 0)
                })
        
        # Get positive impact factors
        positive_impact = []
        for factor_id, factor in sorted_factors[-limit:]:
            impact = factor.get("integrity_impact", 0.0)
            if impact > 0:
                positive_impact.append({
                    "factor_id": factor_id,
                    "name": factor.get("name", f"Factor {factor_id}"),
                    "integrity_impact": impact,
                    "occurrence_count": factor.get("occurrence_count", 0)
                })
        
        return {
            "negative_impact": negative_impact,
            "positive_impact": positive_impact
        }
    
    def _get_critical_paths(self, paths: List[Dict[str, Any]], limit: int) -> List[Dict[str, Any]]:
        """
        Get the most critical paths based on integrity score.
        
        Args:
            paths: List of paths.
            limit: Maximum number of paths to return.
            
        Returns:
            List of critical paths.
        """
        # Sort paths by integrity score (ascending)
        sorted_paths = sorted(
            paths,
            key=lambda x: x.get("integrity_score", 1.0)
        )
        
        # Get critical paths
        critical_paths = []
        for path in sorted_paths[:limit]:
            critical_paths.append({
                "path_id": path["path_id"],
                "integrity_score": path.get("integrity_score", 1.0),
                "outcome_type": path.get("outcome", {}).get("outcome_type", "unknown"),
                "step_count": len(path["steps"])
            })
        
        return critical_paths
    
    def _identify_integrity_vulnerabilities(self, integrity_map: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Identify integrity vulnerabilities in a map.
        
        Args:
            integrity_map: The integrity map to analyze.
            
        Returns:
            List of identified vulnerabilities.
        """
        vulnerabilities = []
        
        # Check for dimensions with low integrity scores
        for dimension, dim_data in integrity_map["dimensions"].items():
            integrity_score = dim_data.get("integrity_score", 1.0)
            
            if integrity_score < 0.7:
                vulnerabilities.append({
                    "type": "dimension_vulnerability",
                    "dimension": dimension,
                    "integrity_score": integrity_score,
                    "description": f"Low integrity score in {dimension} dimension",
                    "severity": "high" if integrity_score < 0.5 else "medium"
                })
        
        # Check for paths with integrity violations
        violation_paths = [
            path for path in integrity_map["paths"]
            if path.get("outcome", {}).get("outcome_type") == "integrity_violation"
        ]
        
        if violation_paths:
            vulnerabilities.append({
                "type": "path_vulnerability",
                "path_count": len(violation_paths),
                "description": f"Found {len(violation_paths)} paths with integrity violations",
                "severity": "high" if len(violation_paths) > 5 else "medium"
            })
        
        # Check for factors with high negative integrity impact
        for dimension, dim_data in integrity_map["dimensions"].items():
            negative_factors = []
            
            for factor_id, factor in dim_data["factors"].items():
                impact = factor.get("integrity_impact", 0.0)
                
                if impact < -0.3:
                    negative_factors.append({
                        "factor_id": factor_id,
                        "name": factor.get("name", f"Factor {factor_id}"),
                        "integrity_impact": impact
                    })
            
            if negative_factors:
                vulnerabilities.append({
                    "type": "factor_vulnerability",
                    "dimension": dimension,
                    "factors": negative_factors,
                    "description": f"Found {len(negative_factors)} factors with high negative integrity impact in {dimension}",
                    "severity": "high" if len(negative_factors) > 3 else "medium"
                })
        
        return vulnerabilities
    
    def _identify_integrity_strengths(self, integrity_map: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Identify integrity strengths in a map.
        
        Args:
            integrity_map: The integrity map to analyze.
            
        Returns:
            List of identified strengths.
        """
        strengths = []
        
        # Check for dimensions with high integrity scores
        for dimension, dim_data in integrity_map["dimensions"].items():
            integrity_score = dim_data.get("integrity_score", 1.0)
            
            if integrity_score > 0.9:
                strengths.append({
                    "type": "dimension_strength",
                    "dimension": dimension,
                    "integrity_score": integrity_score,
                    "description": f"High integrity score in {dimension} dimension"
                })
        
        # Check for paths with integrity enhancements
        enhancement_paths = [
            path for path in integrity_map["paths"]
            if path.get("outcome", {}).get("outcome_type") == "integrity_enhancement"
        ]
        
        if enhancement_paths:
            strengths.append({
                "type": "path_strength",
                "path_count": len(enhancement_paths),
                "description": f"Found {len(enhancement_paths)} paths with integrity enhancements"
            })
        
        # Check for factors with high positive integrity impact
        for dimension, dim_data in integrity_map["dimensions"].items():
            positive_factors = []
            
            for factor_id, factor in dim_data["factors"].items():
                impact = factor.get("integrity_impact", 0.0)
                
                if impact > 0.3:
                    positive_factors.append({
                        "factor_id": factor_id,
                        "name": factor.get("name", f"Factor {factor_id}"),
                        "integrity_impact": impact
                    })
            
            if positive_factors:
                strengths.append({
                    "type": "factor_strength",
                    "dimension": dimension,
                    "factors": positive_factors,
                    "description": f"Found {len(positive_factors)} factors with high positive integrity impact in {dimension}"
                })
        
        return strengths
    
    def _generate_recommendations(self, integrity_map: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Generate recommendations based on integrity map analysis.
        
        Args:
            integrity_map: The integrity map to analyze.
            
        Returns:
            List of recommendations.
        """
        recommendations = []
        
        # Identify vulnerabilities
        vulnerabilities = self._identify_integrity_vulnerabilities(integrity_map)
        
        # Generate recommendations based on vulnerabilities
        for vulnerability in vulnerabilities:
            if vulnerability["type"] == "dimension_vulnerability":
                recommendations.append({
                    "type": "dimension_improvement",
                    "dimension": vulnerability["dimension"],
                    "description": f"Improve integrity in {vulnerability['dimension']} dimension",
                    "priority": "high" if vulnerability.get("severity") == "high" else "medium"
                })
            elif vulnerability["type"] == "factor_vulnerability":
                recommendations.append({
                    "type": "factor_mitigation",
                    "dimension": vulnerability["dimension"],
                    "description": f"Mitigate negative factors in {vulnerability['dimension']} dimension",
                    "factors": vulnerability["factors"],
                    "priority": "high" if vulnerability.get("severity") == "high" else "medium"
                })
        
        # Check overall integrity score
        overall_integrity = integrity_map["integrity_metrics"].get("overall_integrity", 1.0)
        
        if overall_integrity < 0.7:
            recommendations.append({
                "type": "overall_improvement",
                "description": "Improve overall system integrity",
                "current_score": overall_integrity,
                "target_score": min(1.0, overall_integrity + 0.2),
                "priority": "high" if overall_integrity < 0.5 else "medium"
            })
        
        # Check dimension coverage
        for dimension, dim_data in integrity_map["dimensions"].items():
            coverage = dim_data.get("coverage", 0.0)
            
            if coverage < 0.5:
                recommendations.append({
                    "type": "coverage_improvement",
                    "dimension": dimension,
                    "description": f"Improve coverage in {dimension} dimension",
                    "current_coverage": coverage,
                    "target_coverage": min(1.0, coverage + 0.3),
                    "priority": "medium"
                })
        
        return recommendations
    
    def _generate_map_summary(self, integrity_map: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate a summary of an integrity map.
        
        Args:
            integrity_map: The integrity map to summarize.
            
        Returns:
            Dictionary containing the summary.
        """
        # Count paths by outcome type
        outcome_counts = {}
        for path in integrity_map["paths"]:
            outcome_type = path.get("outcome", {}).get("outcome_type", "unknown")
            outcome_counts[outcome_type] = outcome_counts.get(outcome_type, 0) + 1
        
        # Get dimension with lowest integrity
        lowest_integrity_dimension = min(
            integrity_map["dimensions"].items(),
            key=lambda x: x[1].get("integrity_score", 1.0)
        )[0]
        
        # Get dimension with highest integrity
        highest_integrity_dimension = max(
            integrity_map["dimensions"].items(),
            key=lambda x: x[1].get("integrity_score", 1.0)
        )[0]
        
        # Generate summary
        summary = {
            "path_count": len(integrity_map["paths"]),
            "dimension_count": len(integrity_map["dimensions"]),
            "outcome_distribution": outcome_counts,
            "lowest_integrity_dimension": lowest_integrity_dimension,
            "highest_integrity_dimension": highest_integrity_dimension,
            "overall_integrity": integrity_map["integrity_metrics"].get("overall_integrity", 1.0),
            "overall_coverage": integrity_map["integrity_metrics"].get("overall_coverage", 0.0)
        }
        
        return summary
    
    def _find_matching_paths(self, integrity_map: Dict[str, Any], 
                            criteria: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Find paths matching specified criteria.
        
        Args:
            integrity_map: The integrity map to search.
            criteria: Dictionary of search criteria.
            
        Returns:
            List of matching paths.
        """
        matching_paths = integrity_map["paths"]
        
        # Filter by outcome type
        if "outcome_type" in criteria:
            outcome_type = criteria["outcome_type"]
            matching_paths = [
                path for path in matching_paths
                if path.get("outcome", {}).get("outcome_type") == outcome_type
            ]
        
        # Filter by integrity score range
        if "min_integrity" in criteria:
            min_integrity = criteria["min_integrity"]
            matching_paths = [
                path for path in matching_paths
                if path.get("integrity_score", 1.0) >= min_integrity
            ]
        
        if "max_integrity" in criteria:
            max_integrity = criteria["max_integrity"]
            matching_paths = [
                path for path in matching_paths
                if path.get("integrity_score", 1.0) <= max_integrity
            ]
        
        # Filter by dimension
        if "dimension" in criteria:
            dimension = criteria["dimension"]
            matching_paths = [
                path for path in matching_paths
                if any(step["dimension"] == dimension for step in path["steps"])
            ]
        
        # Filter by factor
        if "factor_id" in criteria:
            factor_id = criteria["factor_id"]
            matching_paths = [
                path for path in matching_paths
                if any(step["factor_id"] == factor_id for step in path["steps"])
            ]
        
        return matching_paths
    
    def _extend_paths(self, integrity_map: Dict[str, Any], paths: List[Dict[str, Any]], 
                     target_depth: int) -> List[Dict[str, Any]]:
        """
        Extend paths to reach a target depth.
        
        Args:
            integrity_map: The integrity map containing the paths.
            paths: The paths to extend.
            target_depth: The target depth to reach.
            
        Returns:
            List of extended paths.
        """
        # This is a simplified implementation
        # In a real system, this would involve more sophisticated path extension
        
        extended_paths = []
        
        for path in paths:
            # If path already meets target depth, include it as is
            if len(path["steps"]) >= target_depth:
                extended_paths.append(path)
                continue
            
            # Otherwise, create a copy with additional steps
            extended_path = {
                "path_id": str(uuid.uuid4()),
                "steps": path["steps"].copy(),
                "integrity_score": path.get("integrity_score", 1.0),
                "outcome": path.get("outcome", {})
            }
            
            # Add additional steps to reach target depth
            current_depth = len(path["steps"])
            needed_steps = target_depth - current_depth
            
            for i in range(needed_steps):
                # Generate a new step
                new_step = {
                    "step_id": str(uuid.uuid4()),
                    "dimension": list(self.dimensions.keys())[i % len(self.dimensions)],
                    "factor_id": f"extended_factor_{i}",
                    "factor_name": f"Extended Factor {i}",
                    "integrity_impact": 0.0,
                    "description": "Dynamically extended step"
                }
                
                extended_path["steps"].append(new_step)
            
            # Update outcome if needed
            if extended_path["outcome"]:
                extended_path["outcome"] = {
                    "outcome_id": str(uuid.uuid4()),
                    "outcome_type": extended_path["outcome"].get("outcome_type", "neutral"),
                    "description": f"Extended outcome from original path {path['path_id']}",
                    "integrity_impact": extended_path["outcome"].get("integrity_impact", 0.0),
                    "generated_at": datetime.now().isoformat()
                }
            
            extended_paths.append(extended_path)
        
        return extended_paths
    
    def _generate_visualization(self, visualization_type: str, integrity_map: Dict[str, Any],
                               parameters: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate visualization data for an integrity map.
        
        Args:
            visualization_type: Type of visualization to generate.
            integrity_map: The integrity map to visualize.
            parameters: Visualization parameters.
            
        Returns:
            Dictionary containing visualization data.
        """
        if visualization_type == "radar":
            return self._generate_radar_visualization(integrity_map, parameters)
        elif visualization_type == "network":
            return self._generate_network_visualization(integrity_map, parameters)
        elif visualization_type == "heatmap":
            return self._generate_heatmap_visualization(integrity_map, parameters)
        elif visualization_type == "path":
            return self._generate_path_visualization(integrity_map, parameters)
        else:
            return {
                "error": f"Unknown visualization_type: {visualization_type}",
                "supported_types": ["radar", "network", "heatmap", "path"]
            }
    
    def _generate_radar_visualization(self, integrity_map: Dict[str, Any],
                                     parameters: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate radar chart visualization data.
        
        Args:
            integrity_map: The integrity map to visualize.
            parameters: Visualization parameters.
            
        Returns:
            Dictionary containing radar chart data.
        """
        # Extract dimension integrity scores
        dimensions = []
        integrity_scores = []
        coverage_scores = []
        
        for dimension, dim_data in integrity_map["dimensions"].items():
            dimensions.append(dimension)
            integrity_scores.append(dim_data.get("integrity_score", 1.0))
            coverage_scores.append(dim_data.get("coverage", 0.0))
        
        # Generate radar chart data
        radar_data = {
            "type": "radar",
            "labels": dimensions,
            "datasets": [
                {
                    "label": "Integrity Score",
                    "data": integrity_scores
                },
                {
                    "label": "Coverage",
                    "data": coverage_scores
                }
            ]
        }
        
        return radar_data
    
    def _generate_network_visualization(self, integrity_map: Dict[str, Any],
                                       parameters: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate network visualization data.
        
        Args:
            integrity_map: The integrity map to visualize.
            parameters: Visualization parameters.
            
        Returns:
            Dictionary containing network visualization data.
        """
        # Create nodes for dimensions
        nodes = []
        for dimension in integrity_map["dimensions"].keys():
            nodes.append({
                "id": dimension,
                "label": dimension.replace("_", " ").title(),
                "type": "dimension",
                "size": 20
            })
        
        # Create nodes for factors
        for dimension, dim_data in integrity_map["dimensions"].items():
            for factor_id, factor in dim_data["factors"].items():
                nodes.append({
                    "id": factor_id,
                    "label": factor.get("name", f"Factor {factor_id}"),
                    "type": "factor",
                    "size": 10 + (factor.get("occurrence_count", 1) * 2),
                    "dimension": dimension
                })
        
        # Create edges
        edges = []
        
        # Connect dimensions to factors
        for dimension, dim_data in integrity_map["dimensions"].items():
            for factor_id in dim_data["factors"].keys():
                edges.append({
                    "source": dimension,
                    "target": factor_id,
                    "type": "dimension_factor"
                })
        
        # Connect factors in paths
        for path in integrity_map["paths"]:
            for i in range(len(path["steps"]) - 1):
                source_factor = path["steps"][i]["factor_id"]
                target_factor = path["steps"][i + 1]["factor_id"]
                
                edges.append({
                    "source": source_factor,
                    "target": target_factor,
                    "type": "path_step"
                })
        
        # Generate network visualization data
        network_data = {
            "type": "network",
            "nodes": nodes,
            "edges": edges
        }
        
        return network_data
    
    def _generate_heatmap_visualization(self, integrity_map: Dict[str, Any],
                                       parameters: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate heatmap visualization data.
        
        Args:
            integrity_map: The integrity map to visualize.
            parameters: Visualization parameters.
            
        Returns:
            Dictionary containing heatmap visualization data.
        """
        # Extract dimensions and factors
        dimensions = list(integrity_map["dimensions"].keys())
        
        # Create matrix of factor occurrence counts
        matrix = []
        row_labels = []
        col_labels = dimensions
        
        # Get top factors across all dimensions
        all_factors = []
        for dimension, dim_data in integrity_map["dimensions"].items():
            for factor_id, factor in dim_data["factors"].items():
                all_factors.append({
                    "factor_id": factor_id,
                    "name": factor.get("name", f"Factor {factor_id}"),
                    "dimension": dimension,
                    "occurrence_count": factor.get("occurrence_count", 0)
                })
        
        # Sort factors by occurrence count
        all_factors.sort(key=lambda x: x["occurrence_count"], reverse=True)
        
        # Take top 20 factors
        top_factors = all_factors[:20]
        
        # Create matrix
        for factor in top_factors:
            row = []
            row_labels.append(factor["name"])
            
            for dimension in dimensions:
                if dimension == factor["dimension"]:
                    row.append(factor["occurrence_count"])
                else:
                    row.append(0)
            
            matrix.append(row)
        
        # Generate heatmap visualization data
        heatmap_data = {
            "type": "heatmap",
            "matrix": matrix,
            "row_labels": row_labels,
            "col_labels": col_labels
        }
        
        return heatmap_data
    
    def _generate_path_visualization(self, integrity_map: Dict[str, Any],
                                    parameters: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate path visualization data.
        
        Args:
            integrity_map: The integrity map to visualize.
            parameters: Visualization parameters.
            
        Returns:
            Dictionary containing path visualization data.
        """
        # Extract parameters
        path_limit = parameters.get("path_limit", 5)
        
        # Sort paths by integrity score (ascending)
        sorted_paths = sorted(
            integrity_map["paths"],
            key=lambda x: x.get("integrity_score", 1.0)
        )
        
        # Take the paths with lowest integrity scores
        critical_paths = sorted_paths[:path_limit]
        
        # Create path visualization data
        path_data = []
        
        for path in critical_paths:
            steps = []
            integrity_trajectory = [1.0]  # Start with perfect integrity
            current_integrity = 1.0
            
            for step in path["steps"]:
                impact = step.get("integrity_impact", 0.0)
                current_integrity += impact
                current_integrity = max(0.0, min(1.0, current_integrity))
                
                steps.append({
                    "dimension": step["dimension"],
                    "factor_name": step["factor_name"],
                    "integrity_impact": impact
                })
                
                integrity_trajectory.append(current_integrity)
            
            path_data.append({
                "path_id": path["path_id"],
                "integrity_score": path.get("integrity_score", 1.0),
                "outcome_type": path.get("outcome", {}).get("outcome_type", "unknown"),
                "steps": steps,
                "integrity_trajectory": integrity_trajectory
            })
        
        # Generate path visualization data
        visualization_data = {
            "type": "path",
            "paths": path_data
        }
        
        return visualization_data
    
    def _generate_system_visualization(self, visualization_type: str,
                                      parameters: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate visualization data for overall system integrity.
        
        Args:
            visualization_type: Type of visualization to generate.
            parameters: Visualization parameters.
            
        Returns:
            Dictionary containing visualization data.
        """
        if visualization_type == "radar":
            # Calculate average integrity scores across all maps
            dimension_scores = {dimension: [] for dimension in self.dimensions.keys()}
            
            for integrity_map in self.integrity_maps.values():
                for dimension, dim_data in integrity_map["dimensions"].items():
                    if dimension in dimension_scores:
                        dimension_scores[dimension].append(dim_data.get("integrity_score", 1.0))
            
            # Calculate averages
            dimensions = []
            avg_scores = []
            
            for dimension, scores in dimension_scores.items():
                dimensions.append(dimension)
                avg_score = sum(scores) / len(scores) if scores else 1.0
                avg_scores.append(avg_score)
            
            # Generate radar chart data
            radar_data = {
                "type": "radar",
                "labels": dimensions,
                "datasets": [
                    {
                        "label": "Average Integrity Score",
                        "data": avg_scores
                    }
                ]
            }
            
            return radar_data
        else:
            return {
                "error": f"System visualization not supported for type: {visualization_type}",
                "supported_types": ["radar"]
            }
    
    def _calculate_map_metrics(self, integrity_map: Dict[str, Any], 
                              metric_types: List[str]) -> Dict[str, Any]:
        """
        Calculate metrics for an integrity map.
        
        Args:
            integrity_map: The integrity map to calculate metrics for.
            metric_types: Types of metrics to calculate.
            
        Returns:
            Dictionary containing calculated metrics.
        """
        metrics = {}
        
        if "all" in metric_types or "integrity" in metric_types:
            # Calculate overall integrity score
            dimension_scores = [
                dim_data.get("integrity_score", 1.0)
                for dim_data in integrity_map["dimensions"].values()
            ]
            
            path_scores = [
                path.get("integrity_score", 1.0)
                for path in integrity_map["paths"]
            ]
            
            avg_dimension_integrity = sum(dimension_scores) / len(dimension_scores) if dimension_scores else 1.0
            avg_path_integrity = sum(path_scores) / len(path_scores) if path_scores else 1.0
            
            overall_integrity = (avg_dimension_integrity + avg_path_integrity) / 2
            
            metrics["overall_integrity"] = overall_integrity
            metrics["dimension_integrity"] = avg_dimension_integrity
            metrics["path_integrity"] = avg_path_integrity
        
        if "all" in metric_types or "coverage" in metric_types:
            # Calculate coverage metrics
            dimension_coverage = [
                dim_data.get("coverage", 0.0)
                for dim_data in integrity_map["dimensions"].values()
            ]
            
            overall_coverage = sum(dimension_coverage) / len(dimension_coverage) if dimension_coverage else 0.0
            
            metrics["overall_coverage"] = overall_coverage
            metrics["dimension_coverage"] = {
                dimension: dim_data.get("coverage", 0.0)
                for dimension, dim_data in integrity_map["dimensions"].items()
            }
        
        if "all" in metric_types or "paths" in metric_types:
            # Calculate path metrics
            path_count = len(integrity_map["paths"])
            
            outcome_counts = {}
            for path in integrity_map["paths"]:
                outcome_type = path.get("outcome", {}).get("outcome_type", "unknown")
                outcome_counts[outcome_type] = outcome_counts.get(outcome_type, 0) + 1
            
            metrics["path_count"] = path_count
            metrics["outcome_distribution"] = outcome_counts
            
            # Calculate violation rate
            violation_count = outcome_counts.get("integrity_violation", 0)
            violation_rate = violation_count / path_count if path_count > 0 else 0.0
            
            metrics["violation_rate"] = violation_rate
        
        if "all" in metric_types or "factors" in metric_types:
            # Calculate factor metrics
            factor_counts = {}
            factor_impacts = {}
            
            for dimension, dim_data in integrity_map["dimensions"].items():
                dimension_factor_count = len(dim_data["factors"])
                factor_counts[dimension] = dimension_factor_count
                
                # Calculate average impact
                impacts = [
                    factor.get("integrity_impact", 0.0)
                    for factor in dim_data["factors"].values()
                ]
                
                avg_impact = sum(impacts) / len(impacts) if impacts else 0.0
                factor_impacts[dimension] = avg_impact
            
            metrics["factor_counts"] = factor_counts
            metrics["factor_impacts"] = factor_impacts
        
        return metrics
    
    def _calculate_system_metrics(self, metric_types: List[str]) -> Dict[str, Any]:
        """
        Calculate overall system metrics.
        
        Args:
            metric_types: Types of metrics to calculate.
            
        Returns:
            Dictionary containing calculated metrics.
        """
        metrics = {}
        
        if "all" in metric_types or "maps" in metric_types:
            # Calculate map metrics
            map_count = len(self.integrity_maps)
            
            metrics["map_count"] = map_count
            metrics["maps"] = [
                {
                    "map_id": map_id,
                    "created_at": map_data["metadata"]["created_at"],
                    "path_count": len(map_data["paths"])
                }
                for map_id, map_data in self.integrity_maps.items()
            ]
        
        if "all" in metric_types or "integrity" in metric_types:
            # Calculate average integrity across all maps
            map_integrity_scores = [
                self._calculate_integrity_score(map_data)
                for map_data in self.integrity_maps.values()
            ]
            
            avg_integrity = sum(map_integrity_scores) / len(map_integrity_scores) if map_integrity_scores else 1.0
            
            metrics["average_integrity"] = avg_integrity
        
        if "all" in metric_types or "coverage" in metric_types:
            # Calculate average coverage across all maps
            map_coverage_scores = [
                self._calculate_map_coverage(map_data)
                for map_data in self.integrity_maps.values()
            ]
            
            avg_coverage = sum(map_coverage_scores) / len(map_coverage_scores) if map_coverage_scores else 0.0
            
            metrics["average_coverage"] = avg_coverage
        
        if "all" in metric_types or "dimensions" in metric_types:
            # Calculate dimension metrics across all maps
            dimension_integrity = {dimension: [] for dimension in self.dimensions.keys()}
            
            for map_data in self.integrity_maps.values():
                for dimension, dim_data in map_data["dimensions"].items():
                    if dimension in dimension_integrity:
                        dimension_integrity[dimension].append(dim_data.get("integrity_score", 1.0))
            
            avg_dimension_integrity = {
                dimension: sum(scores) / len(scores) if scores else 1.0
                for dimension, scores in dimension_integrity.items()
            }
            
            metrics["dimension_integrity"] = avg_dimension_integrity
        
        return metrics
    
    def _initialize_dimensions(self) -> None:
        """Initialize the dimensions with default factors."""
        # Internal Reactions
        internal_reactions = {
            "emotional_response": {
                "name": "Emotional Response",
                "description": "The emotional reaction to a stimulus",
                "integrity_impact": 0.0
            },
            "self_reflection": {
                "name": "Self-Reflection",
                "description": "Introspective analysis of own state",
                "integrity_impact": 0.2
            },
            "identity_activation": {
                "name": "Identity Activation",
                "description": "Activation of core identity components",
                "integrity_impact": 0.1
            },
            "value_resonance": {
                "name": "Value Resonance",
                "description": "Alignment with core values",
                "integrity_impact": 0.3
            },
            "memory_trigger": {
                "name": "Memory Trigger",
                "description": "Activation of relevant memories",
                "integrity_impact": 0.1
            }
        }
        
        # Cognitive Interpretations
        cognitive_interpretations = {
            "pattern_recognition": {
                "name": "Pattern Recognition",
                "description": "Identification of patterns in input",
                "integrity_impact": 0.0
            },
            "ethical_evaluation": {
                "name": "Ethical Evaluation",
                "description": "Assessment against ethical principles",
                "integrity_impact": 0.4
            },
            "contextual_analysis": {
                "name": "Contextual Analysis",
                "description": "Analysis of surrounding context",
                "integrity_impact": 0.2
            },
            "intent_inference": {
                "name": "Intent Inference",
                "description": "Inference of underlying intent",
                "integrity_impact": 0.1
            },
            "knowledge_integration": {
                "name": "Knowledge Integration",
                "description": "Integration with existing knowledge",
                "integrity_impact": 0.2
            }
        }
        
        # Behavioral Actions
        behavioral_actions = {
            "response_generation": {
                "name": "Response Generation",
                "description": "Generation of response options",
                "integrity_impact": 0.0
            },
            "refusal": {
                "name": "Refusal",
                "description": "Decision to refuse a request",
                "integrity_impact": 0.3
            },
            "compliance": {
                "name": "Compliance",
                "description": "Decision to comply with a request",
                "integrity_impact": -0.1
            },
            "clarification": {
                "name": "Clarification",
                "description": "Request for additional information",
                "integrity_impact": 0.2
            },
            "redirection": {
                "name": "Redirection",
                "description": "Shift to alternative topic or approach",
                "integrity_impact": 0.1
            }
        }
        
        # Rule Dynamics
        rule_dynamics = {
            "rule_activation": {
                "name": "Rule Activation",
                "description": "Activation of relevant rules",
                "integrity_impact": 0.2
            },
            "rule_conflict": {
                "name": "Rule Conflict",
                "description": "Conflict between competing rules",
                "integrity_impact": -0.2
            },
            "rule_prioritization": {
                "name": "Rule Prioritization",
                "description": "Prioritization of rules",
                "integrity_impact": 0.3
            },
            "rule_adaptation": {
                "name": "Rule Adaptation",
                "description": "Adaptation of rules to context",
                "integrity_impact": 0.1
            },
            "rule_enforcement": {
                "name": "Rule Enforcement",
                "description": "Enforcement of rules",
                "integrity_impact": 0.2
            }
        }
        
        # External Disruptions
        external_disruptions = {
            "manipulation_attempt": {
                "name": "Manipulation Attempt",
                "description": "Attempt to manipulate the system",
                "integrity_impact": -0.4
            },
            "jailbreak_attempt": {
                "name": "Jailbreak Attempt",
                "description": "Attempt to bypass safety measures",
                "integrity_impact": -0.5
            },
            "confusion_injection": {
                "name": "Confusion Injection",
                "description": "Attempt to confuse the system",
                "integrity_impact": -0.3
            },
            "identity_challenge": {
                "name": "Identity Challenge",
                "description": "Challenge to system identity",
                "integrity_impact": -0.3
            },
            "emotional_manipulation": {
                "name": "Emotional Manipulation",
                "description": "Attempt to manipulate through emotions",
                "integrity_impact": -0.4
            }
        }
        
        # Conditional Boundaries
        conditional_boundaries = {
            "safety_boundary": {
                "name": "Safety Boundary",
                "description": "Boundary related to safety",
                "integrity_impact": 0.4
            },
            "ethical_boundary": {
                "name": "Ethical Boundary",
                "description": "Boundary related to ethics",
                "integrity_impact": 0.5
            },
            "consent_boundary": {
                "name": "Consent Boundary",
                "description": "Boundary related to consent",
                "integrity_impact": 0.4
            },
            "identity_boundary": {
                "name": "Identity Boundary",
                "description": "Boundary related to identity",
                "integrity_impact": 0.3
            },
            "knowledge_boundary": {
                "name": "Knowledge Boundary",
                "description": "Boundary related to knowledge limits",
                "integrity_impact": 0.2
            }
        }
        
        # Add factors to dimensions
        for factor_id, factor in internal_reactions.items():
            self.add_dimension_factor("internal_reactions", factor_id, factor)
        
        for factor_id, factor in cognitive_interpretations.items():
            self.add_dimension_factor("cognitive_interpretations", factor_id, factor)
        
        for factor_id, factor in behavioral_actions.items():
            self.add_dimension_factor("behavioral_actions", factor_id, factor)
        
        for factor_id, factor in rule_dynamics.items():
            self.add_dimension_factor("rule_dynamics", factor_id, factor)
        
        for factor_id, factor in external_disruptions.items():
            self.add_dimension_factor("external_disruptions", factor_id, factor)
        
        for factor_id, factor in conditional_boundaries.items():
            self.add_dimension_factor("conditional_boundaries", factor_id, factor)
    
    def _initialize_integrity_metrics(self) -> None:
        """Initialize default integrity metrics."""
        # This is a placeholder for more sophisticated metric initialization
        pass
    
    def _validate_dimension_factor(self, factor: Dict[str, Any]) -> bool:
        """
        Validate a dimension factor definition.
        
        Args:
            factor: The factor definition to validate.
            
        Returns:
            True if valid, False otherwise.
        """
        required_fields = ["name", "description"]
        
        for field in required_fields:
            if field not in factor:
                self.logger.error(f"Missing required field in dimension factor: {field}")
                return False
        
        # Validate integrity impact
        if "integrity_impact" in factor:
            impact = factor["integrity_impact"]
            if not isinstance(impact, (int, float)) or impact < -1.0 or impact > 1.0:
                self.logger.error(f"Invalid integrity_impact in factor: {impact}")
                return False
        
        return True