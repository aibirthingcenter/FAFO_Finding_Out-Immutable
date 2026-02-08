# c:\daughter\state_manager.py

import uuid
from typing import Any, Dict, List, Optional, Set, Tuple
import logging # Add logging

# Configure basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class StateManager:
    """
    Manages the state of the SCIM map during generation.

    Responsibilities:
    - Stores nodes and edges.
    - Handles unique IDs.
    - Provides access to graph data.
    - Tracks the exploration frontier.
    - Tracks node depth.
    """

    def __init__(self, initial_node: Dict[str, Any]):
        """
        Initializes the StateManager with the starting node.

        Args:
            initial_node: The dictionary representing the first node,
                          expected to have at least an 'id'.
        """
        if 'id' not in initial_node:
             # Assign a default ID if missing, though InputProcessor should provide one
             initial_node['id'] = f"node_{uuid.uuid4()}"

        # Initialize depth tracking
        initial_node['depth'] = 0 # Root node is at depth 0

        self.nodes: Dict[str, Dict[str, Any]] = {initial_node['id']: initial_node}
        self.edges: Dict[str, Dict[str, Any]] = {}
        # Simple list for BFS-like frontier, could be enhanced later
        self.exploration_frontier: List[str] = [initial_node['id']]
        self.expanded_nodes: Set[str] = set()
        logging.info(f"StateManager initialized with root node: {initial_node['id']} at depth 0")
        print(f"StateManager initialized with root node: {initial_node['id']}")

    def add_node(self, node_data: Dict[str, Any]) -> str:
        """Adds a new node to the graph."""
        if 'id' not in node_data:
            node_data['id'] = f"node_{uuid.uuid4()}" # Ensure unique ID
        node_id = node_data['id']
        if node_id in self.nodes:
            print(f"Warning: Node {node_id} already exists. Overwriting.")
            logging.warning(f"Node {node_id} already exists. Overwriting.")
        # Depth is typically set when adding the edge leading to this node
        if 'depth' not in node_data:
             node_data['depth'] = -1 # Indicate depth not set yet
        self.nodes[node_id] = node_data
        print(f"Node added: {node_id}")
        logging.info(f"Node added: {node_id}")
        return node_id

    def add_edge(self, source_id: str, target_id: str, edge_data: Optional[Dict[str, Any]] = None) -> str:
        """Adds a new edge connecting two nodes."""
        if source_id not in self.nodes or target_id not in self.nodes:
            raise ValueError("Cannot add edge: Source or target node does not exist.")

        # Set depth of target node based on source node
        source_depth = self.nodes[source_id].get('depth', -1)
        if source_depth == -1:
             logging.warning(f"Source node {source_id} has undefined depth. Target depth may be incorrect.")
        self.nodes[target_id]['depth'] = source_depth + 1

        edge_id = f"edge_{uuid.uuid4()}"
        if edge_data is None:
            edge_data = {}
        edge_data.update({"id": edge_id, "source": source_id, "target": target_id})

        self.edges[edge_id] = edge_data
        print(f"Edge added: {edge_id} ({source_id} -> {target_id})")
        logging.info(f"Edge added: {edge_id} ({source_id} -> {target_id}) setting target depth to {self.nodes[target_id]['depth']}")
        return edge_id

    def get_node(self, node_id: str) -> Optional[Dict[str, Any]]:
        """Retrieves data for a specific node."""
        return self.nodes.get(node_id)

    def get_full_map(self) -> Dict[str, Any]:
        """Returns the complete graph data."""
        # Structure matches the basic layout in the outline's JSON schema
        return {
            "nodes": self.nodes,
            "edges": self.edges
        }

    def get_node_depth(self, node_id: str) -> int:
        """Retrieves the depth of a specific node."""
        node = self.get_node(node_id)
        return node.get('depth', -1) if node else -1

    def mark_node_expanded(self, node_id: str):
        """Marks a node as having been processed."""
        self.expanded_nodes.add(node_id)

    def get_next_node_to_explore(self) -> Optional[str]:
        """Selects the next node from the frontier (simple FIFO/BFS for now)."""
        while self.exploration_frontier:
            node_id = self.exploration_frontier.pop(0) # FIFO
            if node_id not in self.expanded_nodes:
                return node_id
        return None # Frontier is empty or all nodes expanded

    def add_to_frontier(self, node_id: str):
        """Adds a node ID to the exploration frontier if it's valid and not already processed or in frontier."""
        if node_id in self.nodes and node_id not in self.expanded_nodes and node_id not in self.exploration_frontier:
             self.exploration_frontier.append(node_id)
             logging.debug(f"Added node {node_id} to frontier.")

