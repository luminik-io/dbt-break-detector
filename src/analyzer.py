import os
from typing import Dict, List, Set, Tuple
import networkx as nx
from .parsers.sql_parser import SQLParser
from .parsers.manifest_parser import ManifestParser
from .utils.git_utils import GitHandler
from .utils.dag_utils import DAGAnalyzer
from .models.breaking_change import BreakingChange, ChangeType

class BreakingChangeAnalyzer:
    def __init__(self, project_dir: str, base_branch: str = "main"):
        self.project_dir = project_dir
        self.base_branch = base_branch
        self.sql_parser = SQLParser()
        self.manifest_parser = ManifestParser()
        self.git_handler = GitHandler(project_dir)
        self.dag_analyzer = DAGAnalyzer()

    def analyze(self) -> List[BreakingChange]:
        """Main analysis method that coordinates all checks"""
        breaking_changes = []
        
        # Get changed files
        changed_files = self.git_handler.get_changed_files()
        
        # Analyze each changed file
        for file_path in changed_files:
            if file_path.endswith('.sql'):
                changes = self._analyze_sql_file(file_path)
                breaking_changes.extend(changes)
        
        # Check for cyclic dependencies
        cycles = self._check_dependencies()
        if cycles:
            breaking_changes.extend(self._create_cycle_changes(cycles))
        
        return breaking_changes

    def _analyze_sql_file(self, file_path: str) -> List[BreakingChange]:
        """Analyze a single SQL file for breaking changes"""
        changes = []
        
        # Get old and new content
        old_content = self.git_handler.get_old_content(file_path)
        new_content = self.git_handler.get_new_content(file_path)
        
        # Parse both versions
        old_model = self.sql_parser.parse(old_content)
        new_model = self.sql_parser.parse(new_content)
        
        # Check for column removals
        removed_cols = old_model.columns - new_model.columns
        if removed_cols:
            changes.append(
                BreakingChange(
                    file_path=file_path,
                    change_type=ChangeType.COLUMN_REMOVED,
                    details={"columns": list(removed_cols)}
                )
            )
        
        # Check for type changes
        type_changes = self._check_type_changes(old_model, new_model)
        if type_changes:
            changes.append(
                BreakingChange(
                    file_path=file_path,
                    change_type=ChangeType.TYPE_CHANGED,
                    details={"changes": type_changes}
                )
            )
        
        return changes

    def _check_dependencies(self) -> List[List[str]]:
        """Check for cyclic dependencies in the project"""
        manifest = self.manifest_parser.parse(self.project_dir)
        return self.dag_analyzer.find_cycles(manifest.nodes)

    def _create_cycle_changes(self, cycles: List[List[str]]) -> List[BreakingChange]:
        """Convert cycle information into BreakingChange objects"""
        return [
            BreakingChange(
                file_path="project_structure",
                change_type=ChangeType.CYCLIC_DEPENDENCY,
                details={"cycle": cycle}
            )
            for cycle in cycles
        ]