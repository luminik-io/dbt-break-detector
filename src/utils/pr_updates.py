from typing import List, Optional
import os
from github import Github
from github.PullRequest import PullRequest
from ..models.breaking_change import BreakingChange

class PRDescriptionUpdater:
    def __init__(self, token: Optional[str] = None):
        """Initialize with GitHub token from env or passed directly"""
        self.token = token or os.getenv('GITHUB_TOKEN')
        if not self.token:
            raise ValueError("GitHub token not found. Set GITHUB_TOKEN environment variable.")
        self.github = Github(self.token)

    def update_pr_description(self, 
                            repo_name: str, 
                            pr_number: int, 
                            breaking_changes: List[BreakingChange]) -> None:
        """Update PR description with breaking change analysis results"""
        try:
            repo = self.github.get_repo(repo_name)
            pr = repo.get_pull(pr_number)
            
            # Generate new description content
            new_description = self._merge_descriptions(pr.body or "", breaking_changes)
            
            # Update PR description
            pr.edit(body=new_description)
            
        except Exception as e:
            raise Exception(f"Failed to update PR description: {str(e)}")

    def _merge_descriptions(self, 
                          current_description: str, 
                          breaking_changes: List[BreakingChange]) -> str:
        """Merge existing description with breaking change analysis"""
        # Remove old analysis section if it exists
        description_parts = current_description.split("## DBT Breaking Change Analysis")
        base_description = description_parts[0].strip()

        # Generate new analysis section
        analysis_section = self._generate_analysis_section(breaking_changes)

        # Combine sections
        return f"{base_description}\n\n{analysis_section}"

    def _generate_analysis_section(self, breaking_changes: List[BreakingChange]) -> str:
        """Generate formatted analysis section"""
        section = "## DBT Breaking Change Analysis\n\n"
        
        if not breaking_changes:
            return f"{section}✅ No breaking changes detected\n"

        # Add summary
        section += "### Summary\n"
        section += f"🔍 Found {len(breaking_changes)} potential breaking changes\n\n"

        # Group changes by type
        changes_by_type = {}
        for change in breaking_changes:
            if change.change_type.value not in changes_by_type:
                changes_by_type[change.change_type.value] = []
            changes_by_type[change.change_type.value].append(change)

        # Add detailed analysis
        section += "### Detailed Analysis\n\n"
        for change_type, changes in changes_by_type.items():
            section += f"#### {change_type.replace('_', ' ').title()}\n"
            for change in changes:
                section += f"- **File**: `{change.file_path}`\n"
                section += "  ```\n"
                for key, value in change.details.items():
                    section += f"  {key}: {value}\n"
                section += "  ```\n"

        # Add impact assessment
        section += "\n### Impact Assessment\n"
        section += "The following areas might be affected:\n\n"
        
        affected_areas = set()
        for change in breaking_changes:
            if 'affected_models' in change.details:
                affected_areas.update(change.details['affected_models'])
        
        for area in affected_areas:
            section += f"- `{area}`\n"

        # Add recommendations
        section += "\n### Recommendations\n"
        section += "Please review the following before merging:\n\n"
        section += "1. 🔍 Verify all column removals are intentional\n"
        section += "2. 📊 Check data type changes for potential data loss\n"
        section += "3. 🔄 Review affected downstream dependencies\n"
        section += "4. 📝 Update documentation if necessary\n"

        return section