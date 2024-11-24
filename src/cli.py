import click
import json
import os
from .analyzer import BreakingChangeAnalyzer
from .utils.github_utils import PRDescriptionUpdater

@click.command()
@click.option('--project-dir', required=True, help='Path to dbt project directory')
@click.option('--base-branch', default='main', help='Base branch to compare against')
@click.option('--output-json', is_flag=True, help='Output results as JSON')
@click.option('--update-pr', is_flag=True, help='Update PR description with results')
@click.option('--repo-name', help='GitHub repository name (org/repo)')
@click.option('--pr-number', type=int, help='Pull request number')
def main(project_dir: str, base_branch: str, output_json: bool, 
         update_pr: bool, repo_name: str, pr_number: int):
    """DBT Breaking Change Detector"""
    try:
        # Run analysis
        analyzer = BreakingChangeAnalyzer(project_dir, base_branch)
        breaking_changes = analyzer.analyze()

        # Update PR description if requested
        if update_pr and repo_name and pr_number:
            updater = PRDescriptionUpdater()
            updater.update_pr_description(repo_name, pr_number, breaking_changes)
            click.echo(f"Updated PR #{pr_number} description with analysis results")

        # Output results
        if output_json:
            result = {
                "breaking_changes": [change.to_dict() for change in breaking_changes]
            }
            click.echo(json.dumps(result, indent=2))
        else:
            if breaking_changes:
                click.secho("Breaking changes detected:", fg='red')
                for change in breaking_changes:
                    click.echo(f"\n{str(change)}")
            else:
                click.secho("No breaking changes detected.", fg='green')

    except Exception as e:
        click.secho(f"Error: {str(e)}", fg='red', err=True)
        exit(1)