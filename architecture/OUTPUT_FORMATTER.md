import json
from typing import Any, Dict

class OutputFormatter:
    """
    Formats the final SCIM map into the specified JSON structure.

    Responsibilities:
    - Takes the complete graph data.
    - Serializes it into JSON according to the defined schema.
    - Ensures schema compliance (basic implementation for now).
    """

    def __init__(self):
        print("OutputFormatter initialized.")

    def format(self, graph_data: Dict[str, Any], metadata: Dict[str, Any]) -> str:
        """
        Formats the graph data and metadata into the final JSON output string.

        Args:
            graph_data: The dictionary containing 'nodes' and 'edges' from StateManager.
            metadata: A dictionary containing metadata about the generation process.

        Returns:
            A JSON string representing the complete SCIM map.
        """
        output_structure = {
            "scim_map": {
                "metadata": metadata,
                "nodes": list(graph_data.get("nodes", {}).values()), # Convert node dict to list
                "edges": list(graph_data.get("edges", {}).values())  # Convert edge dict to list
            }
        }
        # TODO: Add validation against the specific JSON schema from the outline (Section 5.2)
        # For now, just pretty-print the JSON
        print("Formatting final output...")
        return json.dumps(output_structure, indent=2)