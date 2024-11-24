import pytest
import os
import tempfile
import shutil

@pytest.fixture
def sample_project_dir():
    """Create a temporary directory with sample dbt project structure"""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create basic dbt project structure
        os.makedirs(os.path.join(tmpdir, 'models'))
        os.makedirs(os.path.join(tmpdir, 'target'))
        
        # Create sample manifest.json
        manifest_content = {
            "nodes": {
                "model.test.model1": {
                    "name": "model1",
                    "resource_type": "model",
                    "depends_on": {"nodes": []},
                    "columns": {"col1": {"name": "col1", "data_type": "text"}}
                }
            }
        }
        
        with open(os.path.join(tmpdir, 'target', 'manifest.json'), 'w') as f:
            json.dump(manifest_content, f)
            
        yield tmpdir

@pytest.fixture
def sample_sql_file(sample_project_dir):
    """Create a sample SQL file"""
    sql_content = """
    SELECT
        column1,
        column2,
        column3
    FROM source_table
    """
    
    file_path = os.path.join(sample_project_dir, 'models', 'test_model.sql')
    with open(file_path, 'w') as f:
        f.write(sql_content)
        
    return file_path