import os
import json
from typing import Dict, Any
from dataclasses import dataclass

@dataclass
class DBTNode:
    name: str
    resource_type: str
    depends_on: list
    columns: Dict[str, Any]

class ManifestParser:
    def parse(self, project_dir: str) -> Dict[str, DBTNode]:
        """Parse dbt manifest.json file"""
        manifest_path = os.path.join(project_dir, 'target', 'manifest.json')
        if not os.path.exists(manifest_path):
            raise FileNotFoundError(f"Manifest file not found at {manifest_path}")
            
        with open(manifest_path, 'r') as f:
            manifest_data = json.load(f)
            
        nodes = {}
        for node_id, node_data in manifest_data.get('nodes', {}).items():
            if node_data['resource_type'] == 'model':
                nodes[node_id] = DBTNode(
                    name=node_data['name'],
                    resource_type=node_data['resource_type'],
                    depends_on=node_data.get('depends_on', {}).get('nodes', []),
                    columns=node_data.get('columns', {})
                )
                
        return nodes