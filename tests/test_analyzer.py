import pytest
from src.analyzer import BreakingChangeAnalyzer
from src.models.breaking_change import ChangeType

def test_analyzer_initialization(sample_project_dir):
    analyzer = BreakingChangeAnalyzer(sample_project_dir)
    assert analyzer.project_dir == sample_project_dir

def test_analyze_sql_file_no_changes(sample_sql_file):
    analyzer = BreakingChangeAnalyzer(os.path.dirname(os.path.dirname(sample_sql_file)))
    changes = analyzer._analyze_sql_file(sample_sql_file)
    assert len(changes) == 0

def test_detect_column_removal(sample_project_dir):
    # Setup
    old_content = "SELECT col1, col2 FROM table"
    new_content = "SELECT col1 FROM table"
    
    # Create test files
    old_file = os.path.join(sample_project_dir, "old.sql")
    new_file = os.path.join(sample_project_dir, "new.sql")
    
    with open(old_file, 'w') as f:
        f.write(old_content)
    with open(new_file, 'w') as f:
        f.write(new_content)
        
    analyzer = BreakingChangeAnalyzer(sample_project_dir)
    changes = analyzer.analyze()
    
    assert any(c.change_type == ChangeType.COLUMN_REMOVED for c in changes)