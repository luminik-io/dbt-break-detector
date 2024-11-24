import networkx as nx
from typing import Dict, List, Any

class DAGAnalyzer:
    def find_cycles(self, nodes: Dict[str, Any]) -> List[List[str]]:
        """Find cycles in the dependency graph"""
        # Create directed graph
        G = nx.DiGraph()
        
        # Add edges from dependencies
        for node_id, node_data in nodes.items():
            for dependency in node_data.depends_on:
                G.add_edge(dependency, node_id)
        
        # Find cycles
        try:
            return list(nx.simple_cycles(G))
        except nx.NetworkXNoCycle:
            return []

    def get_affected_nodes(self, changed_nodes: List[str], nodes: Dict[str, Any]) -> List[str]:
        """Get all nodes affected by changes in the given nodes"""
        G = nx.DiGraph()
        
        # Build graph
        for node_id, node_data in nodes.items():
            for dependency in node_data.depends_on:
                G.add_edge(dependency, node_id)
        
        # Get all descendants of changed nodes
        affected = set()
        for node in changed_nodes:
            affected.update(nx.descendants(G, node))
            
        return list(affected)