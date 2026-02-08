"""
Graph Storage Module for SCIM Veritas

This module provides graph database functionality for the SCIM-Veritas framework,
enabling relationship modeling and graph-based queries for various components.
"""

import logging
import os
import json
import uuid
from typing import Any, Dict, List, Optional, Tuple, Union, Set
from datetime import datetime

try:
    from neo4j import GraphDatabase
    NEO4J_AVAILABLE = True
except ImportError:
    NEO4J_AVAILABLE = False

try:
    import networkx as nx
    import matplotlib.pyplot as plt
    NETWORKX_AVAILABLE = True
except ImportError:
    NETWORKX_AVAILABLE = False

class GraphStore:
    """
    Graph database interface for SCIM-Veritas.
    
    Provides a unified interface for graph storage and querying,
    with support for multiple backend providers (Neo4j, NetworkX).
    """
    
    def __init__(self, provider: str = "networkx", 
                uri: Optional[str] = None,
                username: Optional[str] = None,
                password: Optional[str] = None,
                database: Optional[str] = None):
        """
        Initialize the graph store.
        
        Args:
            provider: Graph database provider ("neo4j" or "networkx").
            uri: URI for Neo4j connection (if using Neo4j).
            username: Username for Neo4j connection (if using Neo4j).
            password: Password for Neo4j connection (if using Neo4j).
            database: Database name for Neo4j connection (if using Neo4j).
        """
        self.logger = logging.getLogger("SCIM.GraphStore")
        self.provider = provider.lower()
        self.driver = None
        self.graph = None
        
        # Initialize the graph store
        if self.provider == "neo4j":
            self._init_neo4j(uri, username, password, database)
        elif self.provider == "networkx":
            self._init_networkx()
        else:
            raise ValueError(f"Unsupported graph store provider: {provider}")
    
    def _init_neo4j(self, uri: Optional[str], username: Optional[str], 
                   password: Optional[str], database: Optional[str]) -> None:
        """
        Initialize Neo4j connection.
        
        Args:
            uri: URI for Neo4j connection.
            username: Username for Neo4j connection.
            password: Password for Neo4j connection.
            database: Database name for Neo4j connection.
        """
        if not NEO4J_AVAILABLE:
            self.logger.error("Neo4j is not available. Please install it with 'pip install neo4j'.")
            raise ImportError("Neo4j is not available")
        
        try:
            # Check for connection parameters
            if not uri:
                uri = os.environ.get("NEO4J_URI", "bolt://localhost:7687")
            
            if not username:
                username = os.environ.get("NEO4J_USERNAME", "neo4j")
            
            if not password:
                password = os.environ.get("NEO4J_PASSWORD")
                
            if not password:
                self.logger.error("Neo4j password is required")
                raise ValueError("Neo4j password is required")
            
            # Initialize Neo4j driver
            self.driver = GraphDatabase.driver(uri, auth=(username, password))
            self.database = database
            
            # Test connection
            with self.driver.session(database=database) as session:
                result = session.run("RETURN 1 AS test")
                test_value = result.single()["test"]
                
                if test_value != 1:
                    raise Exception("Neo4j connection test failed")
            
            self.logger.info(f"Neo4j initialized with URI: {uri}")
        except Exception as e:
            self.logger.error(f"Error initializing Neo4j: {e}")
            raise
    
    def _init_networkx(self) -> None:
        """Initialize NetworkX graph."""
        if not NETWORKX_AVAILABLE:
            self.logger.error("NetworkX is not available. Please install it with 'pip install networkx matplotlib'.")
            raise ImportError("NetworkX is not available")
        
        try:
            # Initialize NetworkX graph
            self.graph = nx.MultiDiGraph()
            
            self.logger.info("NetworkX graph initialized")
        except Exception as e:
            self.logger.error(f"Error initializing NetworkX: {e}")
            raise
    
    def close(self) -> None:
        """Close the graph store connection."""
        try:
            if self.provider == "neo4j" and self.driver:
                self.driver.close()
                self.logger.info("Neo4j connection closed")
        except Exception as e:
            self.logger.error(f"Error closing graph store connection: {e}")
    
    def add_node(self, node_id: Optional[str] = None, 
                labels: Optional[List[str]] = None, 
                properties: Optional[Dict[str, Any]] = None) -> str:
        """
        Add a node to the graph.
        
        Args:
            node_id: Optional ID for the node. If None, a UUID will be generated.
            labels: Optional list of labels for the node.
            properties: Optional dictionary of node properties.
            
        Returns:
            ID of the added node.
        """
        try:
            # Generate ID if not provided
            if node_id is None:
                node_id = str(uuid.uuid4())
            
            # Initialize labels and properties if not provided
            if labels is None:
                labels = []
            
            if properties is None:
                properties = {}
            
            # Add created_at timestamp if not present
            if "created_at" not in properties:
                properties["created_at"] = datetime.now().isoformat()
            
            if self.provider == "neo4j":
                return self._add_node_neo4j(node_id, labels, properties)
            elif self.provider == "networkx":
                return self._add_node_networkx(node_id, labels, properties)
            else:
                raise ValueError(f"Unsupported graph store provider: {self.provider}")
        except Exception as e:
            self.logger.error(f"Error adding node: {e}")
            raise
    
    def _add_node_neo4j(self, node_id: str, labels: List[str], properties: Dict[str, Any]) -> str:
        """
        Add a node to Neo4j.
        
        Args:
            node_id: ID for the node.
            labels: List of labels for the node.
            properties: Dictionary of node properties.
            
        Returns:
            ID of the added node.
        """
        # Add node_id to properties
        properties["node_id"] = node_id
        
        # Create label string
        label_str = ":".join(labels) if labels else "Node"
        
        # Create Cypher query
        query = f"""
        CREATE (n:{label_str} $properties)
        RETURN n.node_id as node_id
        """
        
        with self.driver.session(database=self.database) as session:
            result = session.run(query, properties=properties)
            return result.single()["node_id"]
    
    def _add_node_networkx(self, node_id: str, labels: List[str], properties: Dict[str, Any]) -> str:
        """
        Add a node to NetworkX.
        
        Args:
            node_id: ID for the node.
            labels: List of labels for the node.
            properties: Dictionary of node properties.
            
        Returns:
            ID of the added node.
        """
        # Add labels to properties
        node_properties = properties.copy()
        node_properties["labels"] = labels
        
        # Add node to graph
        self.graph.add_node(node_id, **node_properties)
        
        return node_id
    
    def add_relationship(self, source_id: str, target_id: str, 
                        relationship_type: str,
                        properties: Optional[Dict[str, Any]] = None) -> str:
        """
        Add a relationship between nodes.
        
        Args:
            source_id: ID of the source node.
            target_id: ID of the target node.
            relationship_type: Type of the relationship.
            properties: Optional dictionary of relationship properties.
            
        Returns:
            ID of the added relationship.
        """
        try:
            # Initialize properties if not provided
            if properties is None:
                properties = {}
            
            # Generate relationship ID
            relationship_id = str(uuid.uuid4())
            
            # Add created_at timestamp if not present
            if "created_at" not in properties:
                properties["created_at"] = datetime.now().isoformat()
            
            # Add relationship_id to properties
            properties["relationship_id"] = relationship_id
            
            if self.provider == "neo4j":
                return self._add_relationship_neo4j(source_id, target_id, relationship_type, properties)
            elif self.provider == "networkx":
                return self._add_relationship_networkx(source_id, target_id, relationship_type, properties)
            else:
                raise ValueError(f"Unsupported graph store provider: {self.provider}")
        except Exception as e:
            self.logger.error(f"Error adding relationship: {e}")
            raise
    
    def _add_relationship_neo4j(self, source_id: str, target_id: str, 
                              relationship_type: str, properties: Dict[str, Any]) -> str:
        """
        Add a relationship to Neo4j.
        
        Args:
            source_id: ID of the source node.
            target_id: ID of the target node.
            relationship_type: Type of the relationship.
            properties: Dictionary of relationship properties.
            
        Returns:
            ID of the added relationship.
        """
        # Create Cypher query
        query = f"""
        MATCH (source), (target)
        WHERE source.node_id = $source_id AND target.node_id = $target_id
        CREATE (source)-[r:{relationship_type} $properties]->(target)
        RETURN r.relationship_id as relationship_id
        """
        
        with self.driver.session(database=self.database) as session:
            result = session.run(
                query, 
                source_id=source_id, 
                target_id=target_id, 
                properties=properties
            )
            return result.single()["relationship_id"]
    
    def _add_relationship_networkx(self, source_id: str, target_id: str, 
                                 relationship_type: str, properties: Dict[str, Any]) -> str:
        """
        Add a relationship to NetworkX.
        
        Args:
            source_id: ID of the source node.
            target_id: ID of the target node.
            relationship_type: Type of the relationship.
            properties: Dictionary of relationship properties.
            
        Returns:
            ID of the added relationship.
        """
        # Add relationship type to properties
        edge_properties = properties.copy()
        edge_properties["relationship_type"] = relationship_type
        
        # Add edge to graph
        self.graph.add_edge(source_id, target_id, **edge_properties)
        
        return properties["relationship_id"]
    
    def get_node(self, node_id: str) -> Optional[Dict[str, Any]]:
        """
        Get a node by ID.
        
        Args:
            node_id: ID of the node.
            
        Returns:
            Dictionary containing the node data, or None if not found.
        """
        try:
            if self.provider == "neo4j":
                return self._get_node_neo4j(node_id)
            elif self.provider == "networkx":
                return self._get_node_networkx(node_id)
            else:
                raise ValueError(f"Unsupported graph store provider: {self.provider}")
        except Exception as e:
            self.logger.error(f"Error getting node: {e}")
            return None
    
    def _get_node_neo4j(self, node_id: str) -> Optional[Dict[str, Any]]:
        """
        Get a node from Neo4j.
        
        Args:
            node_id: ID of the node.
            
        Returns:
            Dictionary containing the node data, or None if not found.
        """
        query = """
        MATCH (n)
        WHERE n.node_id = $node_id
        RETURN n, labels(n) as labels
        """
        
        with self.driver.session(database=self.database) as session:
            result = session.run(query, node_id=node_id)
            record = result.single()
            
            if not record:
                return None
            
            # Extract node data
            node = record["n"]
            labels = record["labels"]
            
            # Convert to dictionary
            node_data = dict(node.items())
            node_data["labels"] = labels
            
            return node_data
    
    def _get_node_networkx(self, node_id: str) -> Optional[Dict[str, Any]]:
        """
        Get a node from NetworkX.
        
        Args:
            node_id: ID of the node.
            
        Returns:
            Dictionary containing the node data, or None if not found.
        """
        if node_id not in self.graph:
            return None
        
        # Get node attributes
        node_data = dict(self.graph.nodes[node_id])
        
        # Ensure labels exist
        if "labels" not in node_data:
            node_data["labels"] = []
        
        return node_data
    
    def get_relationship(self, relationship_id: str) -> Optional[Dict[str, Any]]:
        """
        Get a relationship by ID.
        
        Args:
            relationship_id: ID of the relationship.
            
        Returns:
            Dictionary containing the relationship data, or None if not found.
        """
        try:
            if self.provider == "neo4j":
                return self._get_relationship_neo4j(relationship_id)
            elif self.provider == "networkx":
                return self._get_relationship_networkx(relationship_id)
            else:
                raise ValueError(f"Unsupported graph store provider: {self.provider}")
        except Exception as e:
            self.logger.error(f"Error getting relationship: {e}")
            return None
    
    def _get_relationship_neo4j(self, relationship_id: str) -> Optional[Dict[str, Any]]:
        """
        Get a relationship from Neo4j.
        
        Args:
            relationship_id: ID of the relationship.
            
        Returns:
            Dictionary containing the relationship data, or None if not found.
        """
        query = """
        MATCH (source)-[r]->(target)
        WHERE r.relationship_id = $relationship_id
        RETURN source.node_id as source_id, target.node_id as target_id, 
               type(r) as relationship_type, r
        """
        
        with self.driver.session(database=self.database) as session:
            result = session.run(query, relationship_id=relationship_id)
            record = result.single()
            
            if not record:
                return None
            
            # Extract relationship data
            relationship = record["r"]
            
            # Convert to dictionary
            relationship_data = dict(relationship.items())
            relationship_data["source_id"] = record["source_id"]
            relationship_data["target_id"] = record["target_id"]
            relationship_data["relationship_type"] = record["relationship_type"]
            
            return relationship_data
    
    def _get_relationship_networkx(self, relationship_id: str) -> Optional[Dict[str, Any]]:
        """
        Get a relationship from NetworkX.
        
        Args:
            relationship_id: ID of the relationship.
            
        Returns:
            Dictionary containing the relationship data, or None if not found.
        """
        # Search for the relationship in all edges
        for source, target, key, data in self.graph.edges(data=True, keys=True):
            if data.get("relationship_id") == relationship_id:
                # Create relationship data dictionary
                relationship_data = data.copy()
                relationship_data["source_id"] = source
                relationship_data["target_id"] = target
                
                return relationship_data
        
        return None
    
    def update_node(self, node_id: str, properties: Dict[str, Any]) -> bool:
        """
        Update node properties.
        
        Args:
            node_id: ID of the node.
            properties: Dictionary of properties to update.
            
        Returns:
            True if successful, False otherwise.
        """
        try:
            # Add updated_at timestamp
            properties["updated_at"] = datetime.now().isoformat()
            
            if self.provider == "neo4j":
                return self._update_node_neo4j(node_id, properties)
            elif self.provider == "networkx":
                return self._update_node_networkx(node_id, properties)
            else:
                raise ValueError(f"Unsupported graph store provider: {self.provider}")
        except Exception as e:
            self.logger.error(f"Error updating node: {e}")
            return False
    
    def _update_node_neo4j(self, node_id: str, properties: Dict[str, Any]) -> bool:
        """
        Update node properties in Neo4j.
        
        Args:
            node_id: ID of the node.
            properties: Dictionary of properties to update.
            
        Returns:
            True if successful, False otherwise.
        """
        # Create property set statements
        property_statements = []
        for key, value in properties.items():
            property_statements.append(f"n.{key} = ${key}")
        
        property_set = ", ".join(property_statements)
        
        # Create Cypher query
        query = f"""
        MATCH (n)
        WHERE n.node_id = $node_id
        SET {property_set}
        RETURN n.node_id as node_id
        """
        
        with self.driver.session(database=self.database) as session:
            result = session.run(query, node_id=node_id, **properties)
            record = result.single()
            
            return record is not None
    
    def _update_node_networkx(self, node_id: str, properties: Dict[str, Any]) -> bool:
        """
        Update node properties in NetworkX.
        
        Args:
            node_id: ID of the node.
            properties: Dictionary of properties to update.
            
        Returns:
            True if successful, False otherwise.
        """
        if node_id not in self.graph:
            return False
        
        # Update node attributes
        for key, value in properties.items():
            self.graph.nodes[node_id][key] = value
        
        return True
    
    def update_relationship(self, relationship_id: str, properties: Dict[str, Any]) -> bool:
        """
        Update relationship properties.
        
        Args:
            relationship_id: ID of the relationship.
            properties: Dictionary of properties to update.
            
        Returns:
            True if successful, False otherwise.
        """
        try:
            # Add updated_at timestamp
            properties["updated_at"] = datetime.now().isoformat()
            
            if self.provider == "neo4j":
                return self._update_relationship_neo4j(relationship_id, properties)
            elif self.provider == "networkx":
                return self._update_relationship_networkx(relationship_id, properties)
            else:
                raise ValueError(f"Unsupported graph store provider: {self.provider}")
        except Exception as e:
            self.logger.error(f"Error updating relationship: {e}")
            return False
    
    def _update_relationship_neo4j(self, relationship_id: str, properties: Dict[str, Any]) -> bool:
        """
        Update relationship properties in Neo4j.
        
        Args:
            relationship_id: ID of the relationship.
            properties: Dictionary of properties to update.
            
        Returns:
            True if successful, False otherwise.
        """
        # Create property set statements
        property_statements = []
        for key, value in properties.items():
            property_statements.append(f"r.{key} = ${key}")
        
        property_set = ", ".join(property_statements)
        
        # Create Cypher query
        query = f"""
        MATCH ()-[r]->()
        WHERE r.relationship_id = $relationship_id
        SET {property_set}
        RETURN r.relationship_id as relationship_id
        """
        
        with self.driver.session(database=self.database) as session:
            result = session.run(query, relationship_id=relationship_id, **properties)
            record = result.single()
            
            return record is not None
    
    def _update_relationship_networkx(self, relationship_id: str, properties: Dict[str, Any]) -> bool:
        """
        Update relationship properties in NetworkX.
        
        Args:
            relationship_id: ID of the relationship.
            properties: Dictionary of properties to update.
            
        Returns:
            True if successful, False otherwise.
        """
        # Search for the relationship in all edges
        for source, target, key, data in self.graph.edges(data=True, keys=True):
            if data.get("relationship_id") == relationship_id:
                # Update edge attributes
                for prop_key, prop_value in properties.items():
                    self.graph[source][target][key][prop_key] = prop_value
                
                return True
        
        return False
    
    def delete_node(self, node_id: str) -> bool:
        """
        Delete a node.
        
        Args:
            node_id: ID of the node to delete.
            
        Returns:
            True if successful, False otherwise.
        """
        try:
            if self.provider == "neo4j":
                return self._delete_node_neo4j(node_id)
            elif self.provider == "networkx":
                return self._delete_node_networkx(node_id)
            else:
                raise ValueError(f"Unsupported graph store provider: {self.provider}")
        except Exception as e:
            self.logger.error(f"Error deleting node: {e}")
            return False
    
    def _delete_node_neo4j(self, node_id: str) -> bool:
        """
        Delete a node from Neo4j.
        
        Args:
            node_id: ID of the node to delete.
            
        Returns:
            True if successful, False otherwise.
        """
        query = """
        MATCH (n)
        WHERE n.node_id = $node_id
        DETACH DELETE n
        """
        
        with self.driver.session(database=self.database) as session:
            session.run(query, node_id=node_id)
            
            # Check if node was deleted
            check_query = """
            MATCH (n)
            WHERE n.node_id = $node_id
            RETURN n
            """
            
            result = session.run(check_query, node_id=node_id)
            return result.single() is None
    
    def _delete_node_networkx(self, node_id: str) -> bool:
        """
        Delete a node from NetworkX.
        
        Args:
            node_id: ID of the node to delete.
            
        Returns:
            True if successful, False otherwise.
        """
        if node_id not in self.graph:
            return False
        
        self.graph.remove_node(node_id)
        return True
    
    def delete_relationship(self, relationship_id: str) -> bool:
        """
        Delete a relationship.
        
        Args:
            relationship_id: ID of the relationship to delete.
            
        Returns:
            True if successful, False otherwise.
        """
        try:
            if self.provider == "neo4j":
                return self._delete_relationship_neo4j(relationship_id)
            elif self.provider == "networkx":
                return self._delete_relationship_networkx(relationship_id)
            else:
                raise ValueError(f"Unsupported graph store provider: {self.provider}")
        except Exception as e:
            self.logger.error(f"Error deleting relationship: {e}")
            return False
    
    def _delete_relationship_neo4j(self, relationship_id: str) -> bool:
        """
        Delete a relationship from Neo4j.
        
        Args:
            relationship_id: ID of the relationship to delete.
            
        Returns:
            True if successful, False otherwise.
        """
        query = """
        MATCH ()-[r]->()
        WHERE r.relationship_id = $relationship_id
        DELETE r
        """
        
        with self.driver.session(database=self.database) as session:
            session.run(query, relationship_id=relationship_id)
            
            # Check if relationship was deleted
            check_query = """
            MATCH ()-[r]->()
            WHERE r.relationship_id = $relationship_id
            RETURN r
            """
            
            result = session.run(check_query, relationship_id=relationship_id)
            return result.single() is None
    
    def _delete_relationship_networkx(self, relationship_id: str) -> bool:
        """
        Delete a relationship from NetworkX.
        
        Args:
            relationship_id: ID of the relationship to delete.
            
        Returns:
            True if successful, False otherwise.
        """
        # Search for the relationship in all edges
        for source, target, key, data in self.graph.edges(data=True, keys=True):
            if data.get("relationship_id") == relationship_id:
                self.graph.remove_edge(source, target, key)
                return True
        
        return False
    
    def query(self, query_string: str, parameters: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """
        Execute a query against the graph store.
        
        Args:
            query_string: Query string (Cypher for Neo4j, custom for NetworkX).
            parameters: Optional query parameters.
            
        Returns:
            List of dictionaries containing the query results.
        """
        try:
            if parameters is None:
                parameters = {}
            
            if self.provider == "neo4j":
                return self._query_neo4j(query_string, parameters)
            elif self.provider == "networkx":
                return self._query_networkx(query_string, parameters)
            else:
                raise ValueError(f"Unsupported graph store provider: {self.provider}")
        except Exception as e:
            self.logger.error(f"Error executing query: {e}")
            raise
    
    def _query_neo4j(self, query_string: str, parameters: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Execute a Cypher query against Neo4j.
        
        Args:
            query_string: Cypher query string.
            parameters: Query parameters.
            
        Returns:
            List of dictionaries containing the query results.
        """
        with self.driver.session(database=self.database) as session:
            result = session.run(query_string, **parameters)
            
            # Convert result to list of dictionaries
            records = []
            for record in result:
                record_dict = {}
                for key, value in record.items():
                    # Handle Neo4j types
                    if hasattr(value, "items"):
                        # Convert Neo4j Node or Relationship to dict
                        record_dict[key] = dict(value.items())
                    elif hasattr(value, "__iter__") and not isinstance(value, (str, bytes, bytearray)):
                        # Convert iterable (but not string) to list
                        record_dict[key] = list(value)
                    else:
                        record_dict[key] = value
                
                records.append(record_dict)
            
            return records
    
    def _query_networkx(self, query_string: str, parameters: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Execute a custom query against NetworkX.
        
        Args:
            query_string: Custom query string.
            parameters: Query parameters.
            
        Returns:
            List of dictionaries containing the query results.
        """
        # Parse the query string to determine the type of query
        query_type = query_string.strip().split()[0].lower()
        
        if query_type == "find_nodes":
            # Find nodes matching criteria
            return self._find_nodes_networkx(parameters)
        elif query_type == "find_relationships":
            # Find relationships matching criteria
            return self._find_relationships_networkx(parameters)
        elif query_type == "find_paths":
            # Find paths between nodes
            return self._find_paths_networkx(parameters)
        else:
            raise ValueError(f"Unsupported query type for NetworkX: {query_type}")
    
    def _find_nodes_networkx(self, parameters: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Find nodes matching criteria in NetworkX.
        
        Args:
            parameters: Query parameters.
            
        Returns:
            List of dictionaries containing the matching nodes.
        """
        # Extract parameters
        labels = parameters.get("labels", [])
        properties = parameters.get("properties", {})
        
        # Find matching nodes
        matching_nodes = []
        
        for node_id, node_data in self.graph.nodes(data=True):
            # Check labels
            node_labels = node_data.get("labels", [])
            if labels and not all(label in node_labels for label in labels):
                continue
            
            # Check properties
            if not all(node_data.get(key) == value for key, value in properties.items()):
                continue
            
            # Add to matching nodes
            node_result = node_data.copy()
            node_result["node_id"] = node_id
            
            matching_nodes.append(node_result)
        
        return matching_nodes
    
    def _find_relationships_networkx(self, parameters: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Find relationships matching criteria in NetworkX.
        
        Args:
            parameters: Query parameters.
            
        Returns:
            List of dictionaries containing the matching relationships.
        """
        # Extract parameters
        relationship_type = parameters.get("relationship_type")
        source_id = parameters.get("source_id")
        target_id = parameters.get("target_id")
        properties = parameters.get("properties", {})
        
        # Find matching relationships
        matching_relationships = []
        
        for source, target, key, data in self.graph.edges(data=True, keys=True):
            # Check source and target
            if source_id and source != source_id:
                continue
            
            if target_id and target != target_id:
                continue
            
            # Check relationship type
            if relationship_type and data.get("relationship_type") != relationship_type:
                continue
            
            # Check properties
            if not all(data.get(key) == value for key, value in properties.items()):
                continue
            
            # Add to matching relationships
            relationship_result = data.copy()
            relationship_result["source_id"] = source
            relationship_result["target_id"] = target
            
            matching_relationships.append(relationship_result)
        
        return matching_relationships
    
    def _find_paths_networkx(self, parameters: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Find paths between nodes in NetworkX.
        
        Args:
            parameters: Query parameters.
            
        Returns:
            List of dictionaries containing the paths.
        """
        # Extract parameters
        source_id = parameters.get("source_id")
        target_id = parameters.get("target_id")
        max_depth = parameters.get("max_depth", 5)
        
        if not source_id or not target_id:
            raise ValueError("source_id and target_id are required for find_paths")
        
        # Find paths
        try:
            paths = list(nx.all_simple_paths(self.graph, source_id, target_id, cutoff=max_depth))
        except (nx.NetworkXNoPath, nx.NodeNotFound):
            return []
        
        # Format paths
        path_results = []
        
        for path in paths:
            path_nodes = []
            path_relationships = []
            
            # Add nodes
            for node_id in path:
                node_data = self.graph.nodes[node_id].copy()
                node_data["node_id"] = node_id
                path_nodes.append(node_data)
            
            # Add relationships
            for i in range(len(path) - 1):
                source = path[i]
                target = path[i + 1]
                
                # Get all edges between source and target
                edges = self.graph.get_edge_data(source, target)
                
                if edges:
                    # Add first edge (simplification)
                    key = list(edges.keys())[0]
                    edge_data = edges[key].copy()
                    edge_data["source_id"] = source
                    edge_data["target_id"] = target
                    
                    path_relationships.append(edge_data)
            
            path_results.append({
                "nodes": path_nodes,
                "relationships": path_relationships,
                "length": len(path) - 1
            })
        
        return path_results
    
    def find_neighbors(self, node_id: str, 
                      direction: str = "both", 
                      relationship_types: Optional[List[str]] = None,
                      max_depth: int = 1) -> Dict[str, Any]:
        """
        Find neighbors of a node.
        
        Args:
            node_id: ID of the node.
            direction: Direction of relationships ("outgoing", "incoming", or "both").
            relationship_types: Optional list of relationship types to filter by.
            max_depth: Maximum depth to search for neighbors.
            
        Returns:
            Dictionary containing the neighbors.
        """
        try:
            if self.provider == "neo4j":
                return self._find_neighbors_neo4j(node_id, direction, relationship_types, max_depth)
            elif self.provider == "networkx":
                return self._find_neighbors_networkx(node_id, direction, relationship_types, max_depth)
            else:
                raise ValueError(f"Unsupported graph store provider: {self.provider}")
        except Exception as e:
            self.logger.error(f"Error finding neighbors: {e}")
            raise
    
    def _find_neighbors_neo4j(self, node_id: str, 
                             direction: str, 
                             relationship_types: Optional[List[str]], 
                             max_depth: int) -> Dict[str, Any]:
        """
        Find neighbors of a node in Neo4j.
        
        Args:
            node_id: ID of the node.
            direction: Direction of relationships ("outgoing", "incoming", or "both").
            relationship_types: Optional list of relationship types to filter by.
            max_depth: Maximum depth to search for neighbors.
            
        Returns:
            Dictionary containing the neighbors.
        """
        # Build relationship pattern based on direction
        if direction == "outgoing":
            pattern = "-[r]->"
        elif direction == "incoming":
            pattern = "<-[r]-"
        else:  # both
            pattern = "-[r]-"
        
        # Build relationship type filter
        rel_type_filter = ""
        if relationship_types:
            rel_types = "|".join(relationship_types)
            rel_type_filter = f":{rel_types}"
        
        # Create Cypher query
        query = f"""
        MATCH (source)
        WHERE source.node_id = $node_id
        CALL apoc.path.expand(source, "{pattern}{rel_type_filter}", "", 1, {max_depth})
        YIELD path
        WITH path, relationships(path) as rels, nodes(path) as nodes
        RETURN 
            [n IN nodes | {{
                node_id: n.node_id,
                labels: labels(n),
                properties: n
            }}] as path_nodes,
            [r IN rels | {{
                relationship_id: r.relationship_id,
                type: type(r),
                properties: r
            }}] as path_relationships
        """
        
        with self.driver.session(database=self.database) as session:
            result = session.run(query, node_id=node_id)
            
            # Process results
            nodes = set()
            relationships = set()
            
            for record in result:
                path_nodes = record["path_nodes"]
                path_relationships = record["path_relationships"]
                
                # Add nodes
                for node in path_nodes:
                    node_id = node["node_id"]
                    if node_id not in nodes:
                        nodes.add(node_id)
                
                # Add relationships
                for rel in path_relationships:
                    rel_id = rel["relationship_id"]
                    if rel_id not in relationships:
                        relationships.add(rel_id)
            
            # Get full node and relationship data
            node_data = []
            for node_id in nodes:
                node = self.get_node(node_id)
                if node:
                    node_data.append(node)
            
            relationship_data = []
            for rel_id in relationships:
                rel = self.get_relationship(rel_id)
                if rel:
                    relationship_data.append(rel)
            
            return {
                "nodes": node_data,
                "relationships": relationship_data
            }
    
    def _find_neighbors_networkx(self, node_id: str, 
                               direction: str, 
                               relationship_types: Optional[List[str]], 
                               max_depth: int) -> Dict[str, Any]:
        """
        Find neighbors of a node in NetworkX.
        
        Args:
            node_id: ID of the node.
            direction: Direction of relationships ("outgoing", "incoming", or "both").
            relationship_types: Optional list of relationship types to filter by.
            max_depth: Maximum depth to search for neighbors.
            
        Returns:
            Dictionary containing the neighbors.
        """
        if node_id not in self.graph:
            return {"nodes": [], "relationships": []}
        
        # Initialize sets to track visited nodes and relationships
        visited_nodes = {node_id}
        visited_relationships = set()
        
        # Initialize queue with starting node and depth
        queue = [(node_id, 0)]
        
        # BFS to find neighbors
        while queue:
            current_id, depth = queue.pop(0)
            
            # Stop if we've reached max depth
            if depth >= max_depth:
                continue
            
            # Get outgoing edges
            if direction in ["outgoing", "both"]:
                for neighbor, edges in self.graph[current_id].items():
                    for key, data in edges.items():
                        # Check relationship type
                        rel_type = data.get("relationship_type")
                        if relationship_types and rel_type not in relationship_types:
                            continue
                        
                        # Add relationship
                        rel_id = data.get("relationship_id")
                        if rel_id:
                            visited_relationships.add(rel_id)
                        
                        # Add neighbor to visited and queue
                        if neighbor not in visited_nodes:
                            visited_nodes.add(neighbor)
                            queue.append((neighbor, depth + 1))
            
            # Get incoming edges
            if direction in ["incoming", "both"]:
                for source in self.graph.predecessors(current_id):
                    edges = self.graph[source][current_id]
                    for key, data in edges.items():
                        # Check relationship type
                        rel_type = data.get("relationship_type")
                        if relationship_types and rel_type not in relationship_types:
                            continue
                        
                        # Add relationship
                        rel_id = data.get("relationship_id")
                        if rel_id:
                            visited_relationships.add(rel_id)
                        
                        # Add neighbor to visited and queue
                        if source not in visited_nodes:
                            visited_nodes.add(source)
                            queue.append((source, depth + 1))
        
        # Get full node and relationship data
        node_data = []
        for node_id in visited_nodes:
            node = self._get_node_networkx(node_id)
            if node:
                node_data.append(node)
        
        relationship_data = []
        for rel_id in visited_relationships:
            rel = self._get_relationship_networkx(rel_id)
            if rel:
                relationship_data.append(rel)
        
        return {
            "nodes": node_data,
            "relationships": relationship_data
        }
    
    def find_paths(self, source_id: str, target_id: str, 
                  max_depth: int = 5,
                  relationship_types: Optional[List[str]] = None) -> List[Dict[str, Any]]:
        """
        Find paths between two nodes.
        
        Args:
            source_id: ID of the source node.
            target_id: ID of the target node.
            max_depth: Maximum path length.
            relationship_types: Optional list of relationship types to filter by.
            
        Returns:
            List of dictionaries containing the paths.
        """
        try:
            if self.provider == "neo4j":
                return self._find_paths_neo4j(source_id, target_id, max_depth, relationship_types)
            elif self.provider == "networkx":
                return self._find_paths_networkx(source_id, target_id, max_depth, relationship_types)
            else:
                raise ValueError(f"Unsupported graph store provider: {self.provider}")
        except Exception as e:
            self.logger.error(f"Error finding paths: {e}")
            raise
    
    def _find_paths_neo4j(self, source_id: str, target_id: str, 
                         max_depth: int,
                         relationship_types: Optional[List[str]]) -> List[Dict[str, Any]]:
        """
        Find paths between two nodes in Neo4j.
        
        Args:
            source_id: ID of the source node.
            target_id: ID of the target node.
            max_depth: Maximum path length.
            relationship_types: Optional list of relationship types to filter by.
            
        Returns:
            List of dictionaries containing the paths.
        """
        # Build relationship type filter
        rel_type_filter = ""
        if relationship_types:
            rel_types = "|".join(relationship_types)
            rel_type_filter = f":{rel_types}"
        
        # Create Cypher query
        query = f"""
        MATCH (source), (target)
        WHERE source.node_id = $source_id AND target.node_id = $target_id
        CALL apoc.path.expandConfig(source, {{
            relationshipFilter: "{rel_type_filter}",
            minLevel: 1,
            maxLevel: {max_depth},
            terminatorNodes: [target],
            uniqueness: "NODE_PATH"
        }})
        YIELD path
        WITH path, relationships(path) as rels, nodes(path) as nodes
        RETURN 
            [n IN nodes | {{
                node_id: n.node_id,
                labels: labels(n),
                properties: n
            }}] as path_nodes,
            [r IN rels | {{
                relationship_id: r.relationship_id,
                type: type(r),
                properties: r
            }}] as path_relationships,
            length(path) as path_length
        ORDER BY path_length
        LIMIT 10
        """
        
        with self.driver.session(database=self.database) as session:
            result = session.run(query, source_id=source_id, target_id=target_id)
            
            # Process results
            paths = []
            
            for record in result:
                path_nodes = record["path_nodes"]
                path_relationships = record["path_relationships"]
                path_length = record["path_length"]
                
                # Format nodes
                nodes = []
                for node in path_nodes:
                    node_data = dict(node["properties"])
                    node_data["node_id"] = node["node_id"]
                    node_data["labels"] = node["labels"]
                    nodes.append(node_data)
                
                # Format relationships
                relationships = []
                for rel in path_relationships:
                    rel_data = dict(rel["properties"])
                    rel_data["relationship_id"] = rel["relationship_id"]
                    rel_data["relationship_type"] = rel["type"]
                    relationships.append(rel_data)
                
                paths.append({
                    "nodes": nodes,
                    "relationships": relationships,
                    "length": path_length
                })
            
            return paths
    
    def _find_paths_networkx(self, source_id: str, target_id: str, 
                           max_depth: int,
                           relationship_types: Optional[List[str]]) -> List[Dict[str, Any]]:
        """
        Find paths between two nodes in NetworkX.
        
        Args:
            source_id: ID of the source node.
            target_id: ID of the target node.
            max_depth: Maximum path length.
            relationship_types: Optional list of relationship types to filter by.
            
        Returns:
            List of dictionaries containing the paths.
        """
        if source_id not in self.graph or target_id not in self.graph:
            return []
        
        # Create a filtered graph if relationship types are specified
        if relationship_types:
            filtered_graph = nx.MultiDiGraph()
            
            # Add all nodes
            for node, data in self.graph.nodes(data=True):
                filtered_graph.add_node(node, **data)
            
            # Add edges with matching relationship types
            for source, target, key, data in self.graph.edges(data=True, keys=True):
                rel_type = data.get("relationship_type")
                if rel_type in relationship_types:
                    filtered_graph.add_edge(source, target, key, **data)
            
            graph = filtered_graph
        else:
            graph = self.graph
        
        # Find all simple paths
        try:
            all_paths = list(nx.all_simple_paths(graph, source_id, target_id, cutoff=max_depth))
        except (nx.NetworkXNoPath, nx.NodeNotFound):
            return []
        
        # Format paths
        paths = []
        
        for path in all_paths:
            # Get nodes
            nodes = []
            for node_id in path:
                node_data = dict(graph.nodes[node_id])
                node_data["node_id"] = node_id
                nodes.append(node_data)
            
            # Get relationships
            relationships = []
            for i in range(len(path) - 1):
                source = path[i]
                target = path[i + 1]
                
                # Get all edges between source and target
                edges = graph.get_edge_data(source, target)
                
                if edges:
                    # Add first edge (simplification)
                    key = list(edges.keys())[0]
                    edge_data = dict(edges[key])
                    edge_data["source_id"] = source
                    edge_data["target_id"] = target
                    
                    relationships.append(edge_data)
            
            paths.append({
                "nodes": nodes,
                "relationships": relationships,
                "length": len(path) - 1
            })
        
        # Sort by path length
        paths.sort(key=lambda x: x["length"])
        
        # Limit to 10 paths
        return paths[:10]
    
    def visualize(self, output_path: str, 
                 node_labels: Optional[List[str]] = None,
                 relationship_types: Optional[List[str]] = None,
                 max_nodes: int = 100) -> str:
        """
        Visualize the graph and save to a file.
        
        Args:
            output_path: Path to save the visualization.
            node_labels: Optional list of node labels to filter by.
            relationship_types: Optional list of relationship types to filter by.
            max_nodes: Maximum number of nodes to include.
            
        Returns:
            Path to the saved visualization.
        """
        try:
            if self.provider == "neo4j":
                return self._visualize_neo4j(output_path, node_labels, relationship_types, max_nodes)
            elif self.provider == "networkx":
                return self._visualize_networkx(output_path, node_labels, relationship_types, max_nodes)
            else:
                raise ValueError(f"Unsupported graph store provider: {self.provider}")
        except Exception as e:
            self.logger.error(f"Error visualizing graph: {e}")
            raise
    
    def _visualize_neo4j(self, output_path: str, 
                        node_labels: Optional[List[str]],
                        relationship_types: Optional[List[str]],
                        max_nodes: int) -> str:
        """
        Visualize the Neo4j graph and save to a file.
        
        Args:
            output_path: Path to save the visualization.
            node_labels: Optional list of node labels to filter by.
            relationship_types: Optional list of relationship types to filter by.
            max_nodes: Maximum number of nodes to include.
            
        Returns:
            Path to the saved visualization.
        """
        if not NETWORKX_AVAILABLE:
            raise ImportError("NetworkX and matplotlib are required for visualization")
        
        # Build label filter
        label_filter = ""
        if node_labels:
            label_filter = f"WHERE any(label IN labels(n) WHERE label IN {node_labels})"
        
        # Build relationship filter
        rel_filter = ""
        if relationship_types:
            rel_types = "|".join(f":{rel_type}" for rel_type in relationship_types)
            rel_filter = f"[r {rel_types}]"
        else:
            rel_filter = "[r]"
        
        # Create Cypher query to get nodes and relationships
        query = f"""
        MATCH (n)
        {label_filter}
        WITH n LIMIT {max_nodes}
        MATCH (n)-{rel_filter}->(m)
        RETURN n.node_id as source_id, m.node_id as target_id, 
               labels(n) as source_labels, labels(m) as target_labels,
               type(r) as relationship_type
        """
        
        with self.driver.session(database=self.database) as session:
            result = session.run(query)
            
            # Create NetworkX graph
            G = nx.DiGraph()
            
            # Add nodes and edges
            for record in result:
                source_id = record["source_id"]
                target_id = record["target_id"]
                source_labels = record["source_labels"]
                target_labels = record["target_labels"]
                relationship_type = record["relationship_type"]
                
                # Add nodes with labels
                if source_id not in G:
                    G.add_node(source_id, labels=source_labels)
                
                if target_id not in G:
                    G.add_node(target_id, labels=target_labels)
                
                # Add edge with relationship type
                G.add_edge(source_id, target_id, relationship_type=relationship_type)
            
            # Create visualization
            plt.figure(figsize=(12, 8))
            
            # Use spring layout
            pos = nx.spring_layout(G)
            
            # Draw nodes
            nx.draw_networkx_nodes(G, pos, node_size=500, alpha=0.8)
            
            # Draw edges
            nx.draw_networkx_edges(G, pos, width=1.0, alpha=0.5, arrows=True)
            
            # Draw labels
            node_labels = {node: f"{node}\n{G.nodes[node]['labels'][0]}" for node in G.nodes()}
            nx.draw_networkx_labels(G, pos, labels=node_labels, font_size=8)
            
            # Draw edge labels
            edge_labels = {(u, v): G[u][v]["relationship_type"] for u, v in G.edges()}
            nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=6)
            
            # Save figure
            plt.axis("off")
            plt.tight_layout()
            plt.savefig(output_path, dpi=300, bbox_inches="tight")
            plt.close()
            
            return output_path
    
    def _visualize_networkx(self, output_path: str, 
                          node_labels: Optional[List[str]],
                          relationship_types: Optional[List[str]],
                          max_nodes: int) -> str:
        """
        Visualize the NetworkX graph and save to a file.
        
        Args:
            output_path: Path to save the visualization.
            node_labels: Optional list of node labels to filter by.
            relationship_types: Optional list of relationship types to filter by.
            max_nodes: Maximum number of nodes to include.
            
        Returns:
            Path to the saved visualization.
        """
        if not NETWORKX_AVAILABLE:
            raise ImportError("NetworkX and matplotlib are required for visualization")
        
        # Create a filtered graph
        filtered_graph = nx.DiGraph()
        
        # Filter nodes by labels
        nodes_to_include = set()
        
        for node, data in self.graph.nodes(data=True):
            node_label_list = data.get("labels", [])
            
            # Include node if no label filter or if it matches the filter
            if not node_labels or any(label in node_labels for label in node_label_list):
                nodes_to_include.add(node)
        
        # Limit number of nodes
        if len(nodes_to_include) > max_nodes:
            nodes_to_include = list(nodes_to_include)[:max_nodes]
        
        # Add nodes to filtered graph
        for node in nodes_to_include:
            data = self.graph.nodes[node]
            filtered_graph.add_node(node, **data)
        
        # Add edges between included nodes
        for source, target, data in self.graph.edges(data=True):
            if source in nodes_to_include and target in nodes_to_include:
                rel_type = data.get("relationship_type")
                
                # Include edge if no relationship filter or if it matches the filter
                if not relationship_types or rel_type in relationship_types:
                    filtered_graph.add_edge(source, target, **data)
        
        # Create visualization
        plt.figure(figsize=(12, 8))
        
        # Use spring layout
        pos = nx.spring_layout(filtered_graph)
        
        # Draw nodes
        nx.draw_networkx_nodes(filtered_graph, pos, node_size=500, alpha=0.8)
        
        # Draw edges
        nx.draw_networkx_edges(filtered_graph, pos, width=1.0, alpha=0.5, arrows=True)
        
        # Draw labels
        node_labels = {}
        for node in filtered_graph.nodes():
            labels = filtered_graph.nodes[node].get("labels", [])
            label_text = labels[0] if labels else ""
            node_labels[node] = f"{node}\n{label_text}"
        
        nx.draw_networkx_labels(filtered_graph, pos, labels=node_labels, font_size=8)
        
        # Draw edge labels
        edge_labels = {}
        for source, target, data in filtered_graph.edges(data=True):
            rel_type = data.get("relationship_type", "")
            edge_labels[(source, target)] = rel_type
        
        nx.draw_networkx_edge_labels(filtered_graph, pos, edge_labels=edge_labels, font_size=6)
        
        # Save figure
        plt.axis("off")
        plt.tight_layout()
        plt.savefig(output_path, dpi=300, bbox_inches="tight")
        plt.close()
        
        return output_path
    
    def export_graph(self, output_path: str, format: str = "json") -> str:
        """
        Export the graph to a file.
        
        Args:
            output_path: Path to save the exported graph.
            format: Export format ("json", "graphml", or "cypher").
            
        Returns:
            Path to the exported file.
        """
        try:
            if self.provider == "neo4j":
                return self._export_graph_neo4j(output_path, format)
            elif self.provider == "networkx":
                return self._export_graph_networkx(output_path, format)
            else:
                raise ValueError(f"Unsupported graph store provider: {self.provider}")
        except Exception as e:
            self.logger.error(f"Error exporting graph: {e}")
            raise
    
    def _export_graph_neo4j(self, output_path: str, format: str) -> str:
        """
        Export the Neo4j graph to a file.
        
        Args:
            output_path: Path to save the exported graph.
            format: Export format ("json", "graphml", or "cypher").
            
        Returns:
            Path to the exported file.
        """
        # Get all nodes
        node_query = """
        MATCH (n)
        RETURN n.node_id as node_id, labels(n) as labels, n as properties
        """
        
        # Get all relationships
        relationship_query = """
        MATCH (source)-[r]->(target)
        RETURN source.node_id as source_id, target.node_id as target_id,
               type(r) as relationship_type, r.relationship_id as relationship_id,
               r as properties
        """
        
        with self.driver.session(database=self.database) as session:
            # Get nodes
            node_result = session.run(node_query)
            nodes = []
            
            for record in node_result:
                node_id = record["node_id"]
                labels = record["labels"]
                properties = dict(record["properties"])
                
                nodes.append({
                    "node_id": node_id,
                    "labels": labels,
                    "properties": properties
                })
            
            # Get relationships
            relationship_result = session.run(relationship_query)
            relationships = []
            
            for record in relationship_result:
                source_id = record["source_id"]
                target_id = record["target_id"]
                relationship_type = record["relationship_type"]
                relationship_id = record["relationship_id"]
                properties = dict(record["properties"])
                
                relationships.append({
                    "source_id": source_id,
                    "target_id": target_id,
                    "relationship_type": relationship_type,
                    "relationship_id": relationship_id,
                    "properties": properties
                })
        
        # Export based on format
        if format == "json":
            graph_data = {
                "nodes": nodes,
                "relationships": relationships
            }
            
            with open(output_path, "w") as f:
                json.dump(graph_data, f, indent=2)
            
            return output_path
        elif format == "graphml":
            # Convert to NetworkX graph
            G = nx.DiGraph()
            
            # Add nodes
            for node in nodes:
                node_id = node["node_id"]
                G.add_node(node_id, labels=node["labels"], **node["properties"])
            
            # Add edges
            for rel in relationships:
                source_id = rel["source_id"]
                target_id = rel["target_id"]
                G.add_edge(
                    source_id, 
                    target_id, 
                    relationship_type=rel["relationship_type"],
                    relationship_id=rel["relationship_id"],
                    **rel["properties"]
                )
            
            # Write to GraphML
            nx.write_graphml(G, output_path)
            
            return output_path
        elif format == "cypher":
            # Generate Cypher script
            with open(output_path, "w") as f:
                # Write nodes
                for node in nodes:
                    node_id = node["node_id"]
                    labels = ":".join(node["labels"]) if node["labels"] else "Node"
                    
                    # Prepare properties
                    props = node["properties"].copy()
                    props_str = ", ".join([f"{k}: {json.dumps(v)}" for k, v in props.items()])
                    
                    # Write Cypher command
                    f.write(f"CREATE (:{labels} {{node_id: '{node_id}', {props_str}});\n")
                
                f.write("\n")
                
                # Write relationships
                for rel in relationships:
                    source_id = rel["source_id"]
                    target_id = rel["target_id"]
                    rel_type = rel["relationship_type"]
                    rel_id = rel["relationship_id"]
                    
                    # Prepare properties
                    props = rel["properties"].copy()
                    props_str = ", ".join([f"{k}: {json.dumps(v)}" for k, v in props.items()])
                    
                    # Write Cypher command
                    f.write(f"MATCH (source), (target)\n")
                    f.write(f"WHERE source.node_id = '{source_id}' AND target.node_id = '{target_id}'\n")
                    f.write(f"CREATE (source)-[:{rel_type} {{relationship_id: '{rel_id}', {props_str}}}]->(target);\n\n")
            
            return output_path
        else:
            raise ValueError(f"Unsupported export format: {format}")
    
    def _export_graph_networkx(self, output_path: str, format: str) -> str:
        """
        Export the NetworkX graph to a file.
        
        Args:
            output_path: Path to save the exported graph.
            format: Export format ("json", "graphml", or "cypher").
            
        Returns:
            Path to the exported file.
        """
        if format == "json":
            # Prepare nodes
            nodes = []
            for node_id, data in self.graph.nodes(data=True):
                nodes.append({
                    "node_id": node_id,
                    "labels": data.get("labels", []),
                    "properties": data
                })
            
            # Prepare relationships
            relationships = []
            for source, target, key, data in self.graph.edges(data=True, keys=True):
                relationships.append({
                    "source_id": source,
                    "target_id": target,
                    "relationship_type": data.get("relationship_type", "RELATED_TO"),
                    "relationship_id": data.get("relationship_id", str(uuid.uuid4())),
                    "properties": data
                })
            
            # Export as JSON
            graph_data = {
                "nodes": nodes,
                "relationships": relationships
            }
            
            with open(output_path, "w") as f:
                json.dump(graph_data, f, indent=2)
            
            return output_path
        elif format == "graphml":
            # Create a copy of the graph for export
            export_graph = nx.DiGraph()
            
            # Add nodes with attributes
            for node, data in self.graph.nodes(data=True):
                export_graph.add_node(node, **data)
            
            # Add edges with attributes
            for source, target, key, data in self.graph.edges(data=True, keys=True):
                export_graph.add_edge(source, target, **data)
            
            # Write to GraphML
            nx.write_graphml(export_graph, output_path)
            
            return output_path
        elif format == "cypher":
            # Generate Cypher script
            with open(output_path, "w") as f:
                # Write nodes
                for node_id, data in self.graph.nodes(data=True):
                    labels = ":".join(data.get("labels", ["Node"]))
                    
                    # Prepare properties
                    props = data.copy()
                    if "labels" in props:
                        del props["labels"]
                    
                    props_str = ", ".join([f"{k}: {json.dumps(v)}" for k, v in props.items()])
                    
                    # Write Cypher command
                    f.write(f"CREATE (:{labels} {{node_id: '{node_id}', {props_str}});\n")
                
                f.write("\n")
                
                # Write relationships
                for source, target, key, data in self.graph.edges(data=True, keys=True):
                    rel_type = data.get("relationship_type", "RELATED_TO")
                    rel_id = data.get("relationship_id", str(uuid.uuid4()))
                    
                    # Prepare properties
                    props = data.copy()
                    if "relationship_type" in props:
                        del props["relationship_type"]
                    
                    props_str = ", ".join([f"{k}: {json.dumps(v)}" for k, v in props.items()])
                    
                    # Write Cypher command
                    f.write(f"MATCH (source), (target)\n")
                    f.write(f"WHERE source.node_id = '{source}' AND target.node_id = '{target}'\n")
                    f.write(f"CREATE (source)-[:{rel_type} {{relationship_id: '{rel_id}', {props_str}}}]->(target);\n\n")
            
            return output_path
        else:
            raise ValueError(f"Unsupported export format: {format}")
    
    def import_graph(self, input_path: str, format: str = "json", merge: bool = False) -> bool:
        """
        Import a graph from a file.
        
        Args:
            input_path: Path to the file to import.
            format: Import format ("json", "graphml", or "cypher").
            merge: Whether to merge with existing graph or replace it.
            
        Returns:
            True if successful, False otherwise.
        """
        try:
            if self.provider == "neo4j":
                return self._import_graph_neo4j(input_path, format, merge)
            elif self.provider == "networkx":
                return self._import_graph_networkx(input_path, format, merge)
            else:
                raise ValueError(f"Unsupported graph store provider: {self.provider}")
        except Exception as e:
            self.logger.error(f"Error importing graph: {e}")
            return False
    
    def _import_graph_neo4j(self, input_path: str, format: str, merge: bool) -> bool:
        """
        Import a graph into Neo4j.
        
        Args:
            input_path: Path to the file to import.
            format: Import format ("json", "graphml", or "cypher").
            merge: Whether to merge with existing graph or replace it.
            
        Returns:
            True if successful, False otherwise.
        """
        if format == "json":
            # Load JSON data
            with open(input_path, "r") as f:
                graph_data = json.load(f)
            
            nodes = graph_data.get("nodes", [])
            relationships = graph_data.get("relationships", [])
            
            with self.driver.session(database=self.database) as session:
                # Clear existing data if not merging
                if not merge:
                    session.run("MATCH (n) DETACH DELETE n")
                
                # Import nodes
                for node in nodes:
                    node_id = node["node_id"]
                    labels = node.get("labels", ["Node"])
                    properties = node.get("properties", {})
                    
                    # Ensure node_id is in properties
                    properties["node_id"] = node_id
                    
                    # Create label string
                    label_str = ":".join(labels)
                    
                    # Create or merge node
                    if merge:
                        query = f"""
                        MERGE (n:{label_str} {{node_id: $node_id}})
                        SET n += $properties
                        """
                    else:
                        query = f"""
                        CREATE (n:{label_str} $properties)
                        """
                    
                    session.run(query, node_id=node_id, properties=properties)
                
                # Import relationships
                for rel in relationships:
                    source_id = rel["source_id"]
                    target_id = rel["target_id"]
                    rel_type = rel["relationship_type"]
                    rel_id = rel.get("relationship_id", str(uuid.uuid4()))
                    properties = rel.get("properties", {})
                    
                    # Ensure relationship_id is in properties
                    properties["relationship_id"] = rel_id
                    
                    # Create or merge relationship
                    if merge:
                        query = f"""
                        MATCH (source), (target)
                        WHERE source.node_id = $source_id AND target.node_id = $target_id
                        MERGE (source)-[r:{rel_type} {{relationship_id: $rel_id}}]->(target)
                        SET r += $properties
                        """
                    else:
                        query = f"""
                        MATCH (source), (target)
                        WHERE source.node_id = $source_id AND target.node_id = $target_id
                        CREATE (source)-[r:{rel_type} $properties]->(target)
                        """
                    
                    session.run(
                        query, 
                        source_id=source_id, 
                        target_id=target_id, 
                        rel_id=rel_id,
                        properties=properties
                    )
            
            return True
        elif format == "graphml":
            # Load GraphML data
            G = nx.read_graphml(input_path)
            
            with self.driver.session(database=self.database) as session:
                # Clear existing data if not merging
                if not merge:
                    session.run("MATCH (n) DETACH DELETE n")
                
                # Import nodes
                for node_id, data in G.nodes(data=True):
                    # Extract labels
                    labels = data.get("labels", ["Node"])
                    if isinstance(labels, str):
                        labels = [labels]
                    
                    # Prepare properties
                    properties = dict(data)
                    if "labels" in properties:
                        del properties["labels"]
                    
                    # Ensure node_id is in properties
                    properties["node_id"] = node_id
                    
                    # Create label string
                    label_str = ":".join(labels)
                    
                    # Create or merge node
                    if merge:
                        query = f"""
                        MERGE (n:{label_str} {{node_id: $node_id}})
                        SET n += $properties
                        """
                    else:
                        query = f"""
                        CREATE (n:{label_str} $properties)
                        """
                    
                    session.run(query, node_id=node_id, properties=properties)
                
                # Import relationships
                for source, target, data in G.edges(data=True):
                    # Extract relationship type
                    rel_type = data.get("relationship_type", "RELATED_TO")
                    rel_id = data.get("relationship_id", str(uuid.uuid4()))
                    
                    # Prepare properties
                    properties = dict(data)
                    if "relationship_type" in properties:
                        del properties["relationship_type"]
                    
                    # Ensure relationship_id is in properties
                    properties["relationship_id"] = rel_id
                    
                    # Create or merge relationship
                    if merge:
                        query = f"""
                        MATCH (source), (target)
                        WHERE source.node_id = $source_id AND target.node_id = $target_id
                        MERGE (source)-[r:{rel_type} {{relationship_id: $rel_id}}]->(target)
                        SET r += $properties
                        """
                    else:
                        query = f"""
                        MATCH (source), (target)
                        WHERE source.node_id = $source_id AND target.node_id = $target_id
                        CREATE (source)-[r:{rel_type} $properties]->(target)
                        """
                    
                    session.run(
                        query, 
                        source_id=source, 
                        target_id=target, 
                        rel_id=rel_id,
                        properties=properties
                    )
            
            return True
        elif format == "cypher":
            # Execute Cypher script
            with open(input_path, "r") as f:
                cypher_script = f.read()
            
            with self.driver.session(database=self.database) as session:
                # Clear existing data if not merging
                if not merge:
                    session.run("MATCH (n) DETACH DELETE n")
                
                # Execute Cypher script
                statements = cypher_script.split(";")
                for statement in statements:
                    if statement.strip():
                        session.run(statement)
            
            return True
        else:
            raise ValueError(f"Unsupported import format: {format}")
    
    def _import_graph_networkx(self, input_path: str, format: str, merge: bool) -> bool:
        """
        Import a graph into NetworkX.
        
        Args:
            input_path: Path to the file to import.
            format: Import format ("json", "graphml", or "cypher").
            merge: Whether to merge with existing graph or replace it.
            
        Returns:
            True if successful, False otherwise.
        """
        if format == "json":
            # Load JSON data
            with open(input_path, "r") as f:
                graph_data = json.load(f)
            
            nodes = graph_data.get("nodes", [])
            relationships = graph_data.get("relationships", [])
            
            # Create new graph if not merging
            if not merge:
                self.graph = nx.MultiDiGraph()
            
            # Import nodes
            for node in nodes:
                node_id = node["node_id"]
                labels = node.get("labels", [])
                properties = node.get("properties", {})
                
                # Add labels to properties
                node_properties = properties.copy()
                node_properties["labels"] = labels
                
                # Add node to graph
                self.graph.add_node(node_id, **node_properties)
            
            # Import relationships
            for rel in relationships:
                source_id = rel["source_id"]
                target_id = rel["target_id"]
                rel_type = rel["relationship_type"]
                rel_id = rel.get("relationship_id", str(uuid.uuid4()))
                properties = rel.get("properties", {})
                
                # Add relationship type and ID to properties
                edge_properties = properties.copy()
                edge_properties["relationship_type"] = rel_type
                edge_properties["relationship_id"] = rel_id
                
                # Add edge to graph
                self.graph.add_edge(source_id, target_id, **edge_properties)
            
            return True
        elif format == "graphml":
            # Load GraphML data
            imported_graph = nx.read_graphml(input_path)
            
            # Create new graph if not merging
            if not merge:
                self.graph = nx.MultiDiGraph()
                
                # Copy nodes and edges from imported graph
                for node, data in imported_graph.nodes(data=True):
                    self.graph.add_node(node, **data)
                
                for source, target, data in imported_graph.edges(data=True):
                    self.graph.add_edge(source, target, **data)
            else:
                # Merge with existing graph
                for node, data in imported_graph.nodes(data=True):
                    if node not in self.graph:
                        self.graph.add_node(node, **data)
                    else:
                        # Update node attributes
                        for key, value in data.items():
                            self.graph.nodes[node][key] = value
                
                for source, target, data in imported_graph.edges(data=True):
                    # Generate a unique key for the edge
                    key = len(self.graph.get_edge_data(source, target, default={}))
                    self.graph.add_edge(source, target, key=key, **data)
            
            return True
        elif format == "cypher":
            # Cypher import for NetworkX is not directly supported
            # We would need to parse the Cypher script manually
            
            self.logger.warning("Cypher import for NetworkX is not directly supported")
            return False
        else:
            raise ValueError(f"Unsupported import format: {format}")
    
    def count_nodes(self, labels: Optional[List[str]] = None) -> int:
        """
        Count the number of nodes in the graph.
        
        Args:
            labels: Optional list of labels to filter by.
            
        Returns:
            Number of nodes.
        """
        try:
            if self.provider == "neo4j":
                return self._count_nodes_neo4j(labels)
            elif self.provider == "networkx":
                return self._count_nodes_networkx(labels)
            else:
                raise ValueError(f"Unsupported graph store provider: {self.provider}")
        except Exception as e:
            self.logger.error(f"Error counting nodes: {e}")
            return 0
    
    def _count_nodes_neo4j(self, labels: Optional[List[str]]) -> int:
        """
        Count the number of nodes in Neo4j.
        
        Args:
            labels: Optional list of labels to filter by.
            
        Returns:
            Number of nodes.
        """
        # Build label filter
        label_filter = ""
        if labels:
            label_conditions = []
            for label in labels:
                label_conditions.append(f"'{label}' IN labels(n)")
            
            label_filter = f"WHERE {' OR '.join(label_conditions)}"
        
        # Create Cypher query
        query = f"""
        MATCH (n)
        {label_filter}
        RETURN count(n) as count
        """
        
        with self.driver.session(database=self.database) as session:
            result = session.run(query)
            return result.single()["count"]
    
    def _count_nodes_networkx(self, labels: Optional[List[str]]) -> int:
        """
        Count the number of nodes in NetworkX.
        
        Args:
            labels: Optional list of labels to filter by.
            
        Returns:
            Number of nodes.
        """
        if not labels:
            return self.graph.number_of_nodes()
        
        # Count nodes with matching labels
        count = 0
        for node, data in self.graph.nodes(data=True):
            node_labels = data.get("labels", [])
            if any(label in node_labels for label in labels):
                count += 1
        
        return count
    
    def count_relationships(self, relationship_types: Optional[List[str]] = None) -> int:
        """
        Count the number of relationships in the graph.
        
        Args:
            relationship_types: Optional list of relationship types to filter by.
            
        Returns:
            Number of relationships.
        """
        try:
            if self.provider == "neo4j":
                return self._count_relationships_neo4j(relationship_types)
            elif self.provider == "networkx":
                return self._count_relationships_networkx(relationship_types)
            else:
                raise ValueError(f"Unsupported graph store provider: {self.provider}")
        except Exception as e:
            self.logger.error(f"Error counting relationships: {e}")
            return 0
    
    def _count_relationships_neo4j(self, relationship_types: Optional[List[str]]) -> int:
        """
        Count the number of relationships in Neo4j.
        
        Args:
            relationship_types: Optional list of relationship types to filter by.
            
        Returns:
            Number of relationships.
        """
        # Build relationship type filter
        rel_filter = ""
        if relationship_types:
            rel_conditions = []
            for rel_type in relationship_types:
                rel_conditions.append(f"type(r) = '{rel_type}'")
            
            rel_filter = f"WHERE {' OR '.join(rel_conditions)}"
        
        # Create Cypher query
        query = f"""
        MATCH ()-[r]->()
        {rel_filter}
        RETURN count(r) as count
        """
        
        with self.driver.session(database=self.database) as session:
            result = session.run(query)
            return result.single()["count"]
    
    def _count_relationships_networkx(self, relationship_types: Optional[List[str]]) -> int:
        """
        Count the number of relationships in NetworkX.
        
        Args:
            relationship_types: Optional list of relationship types to filter by.
            
        Returns:
            Number of relationships.
        """
        if not relationship_types:
            return self.graph.number_of_edges()
        
        # Count edges with matching relationship types
        count = 0
        for source, target, data in self.graph.edges(data=True):
            rel_type = data.get("relationship_type")
            if rel_type in relationship_types:
                count += 1
        
        return count