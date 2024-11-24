# DBT Breaking Change Detector

[![PyPI version](https://badge.fury.io/py/dbt-break-detector.svg)](https://badge.fury.io/py/dbt-break-detector)
[![Python versions](https://img.shields.io/pypi/pyversions/dbt-break-detector.svg)](https://pypi.org/project/dbt-break-detector/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![CI/CD](https://github.com/yourusername/dbt-break-detector/actions/workflows/main.yml/badge.svg)](https://github.com/yourusername/dbt-break-detector/actions)
[![Documentation Status](https://readthedocs.org/projects/dbt-break-detector/badge/?version=latest)](https://dbt-break-detector.readthedocs.io/en/latest/?badge=latest)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Coverage Status](https://coveralls.io/repos/github/yourusername/dbt-break-detector/badge.svg?branch=main)](https://coveralls.io/github/yourusername/dbt-break-detector?branch=main)
[![security: bandit](https://img.shields.io/badge/security-bandit-yellow.svg)](https://github.com/PyCQA/bandit)

A sophisticated tool for detecting and preventing breaking changes in dbt projects during the code review process. This tool helps data teams maintain data quality and prevent unexpected issues in production by automatically analyzing Pull Requests for potential breaking changes.

## 🌟 Key Features

### 🔍 Breaking Change Detection
- **Column Analysis**
  - Detection of removed columns
  - Identification of renamed columns
  - Analysis of data type changes
  - Validation of column constraints

### 📊 Schema Validation
- **Structural Changes**
  - Primary key modifications
  - Foreign key relationship changes
  - Unique constraint alterations
  - Not-null constraint changes

### 🔄 Dependency Management
- **Impact Analysis**
  - Upstream dependency tracking
  - Downstream impact assessment
  - Circular dependency detection
  - Change propagation analysis

### 🤖 GitHub Integration
- **Automated PR Analysis**
  - Detailed PR description updates
  - Inline code comments
  - Status check integration
  - Breaking change summaries
  - Impact assessment reports

## 🚀 Quick Start

### Installation

```bash
# Using pip
pip install dbt-break-detector

# Using poetry
poetry add dbt-break-detector

# From source
git clone https://github.com/yourusername/dbt-break-detector.git
cd dbt-break-detector
pip install -e .
```

### Basic Usage

```bash
# Run analysis on a dbt project
dbt-break-detector --project-dir /path/to/dbt/project

# Analyze with custom base branch
dbt-break-detector --project-dir /path/to/dbt/project --base-branch develop

# Output results as JSON
dbt-break-detector --project-dir /path/to/dbt/project --output-json

# Update PR description with results
dbt-break-detector \
  --project-dir /path/to/dbt/project \
  --update-pr \
  --repo-name org/repo \
  --pr-number 123
```

## 🔧 Configuration

### Project Configuration
Create a `.dbt-break-detector.yml` file in your project root:

```yaml
# Core settings
version: 1
project_name: your_project_name

# Analysis settings
analysis:
  check_columns: true
  check_types: true
  check_dependencies: true
  check_constraints: true

# Dependency settings
dependencies:
  max_depth: 5
  include_indirect: true
  track_downstream: true

# GitHub integration
github:
  update_pr: true
  add_comments: true
  fail_on_breaking: true
  comment_threshold: warning

# Ignore patterns
ignore:
  paths:
    - 'models/staging/**'
    - 'analysis/**'
  changes:
    - type: column_removal
      pattern: '_deprecated$'
    - type: type_change
      from: 'varchar'
      to: 'text'

# Custom rules
rules:
  - name: no_float_columns
    type: column_type
    pattern: 'float'
    level: error
    message: 'Float columns are not allowed, use decimal instead'
```

### GitHub Action
Add to your workflow (`.github/workflows/dbt-break-check.yml`):

```yaml
name: DBT Breaking Change Check
on:
  pull_request:
    paths:
      - '**.sql'
      - 'models/**'
      - 'dbt_project.yml'

jobs:
  check-breaking-changes:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
        with:
          fetch-depth: 0
      
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      
      - name: Install dependencies
        run: pip install dbt-break-detector
      
      - name: Check for breaking changes
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: |
          dbt-break-detector \
            --project-dir . \
            --base-branch ${{ github.base_ref }} \
            --update-pr \
            --repo-name ${{ github.repository }} \
            --pr-number ${{ github.event.pull_request.number }}
```

## 📊 Example Output

### PR Description Update
```markdown
## DBT Breaking Change Analysis

### Summary
🔍 Found 3 potential breaking changes

### Detailed Analysis

#### Column Removals
- **File**: `models/mart/customer_metrics.sql`
  ```
  columns: ['last_purchase_date', 'customer_segment']
  impact: high
  affected_models: 2
  ```

#### Type Changes
- **File**: `models/mart/order_facts.sql`
  ```
  column: order_amount
  old_type: decimal(10,2)
  new_type: float
  impact: medium
  ```

### Impact Assessment
The following areas might be affected:
- `models/mart/customer_segmentation`
- `models/mart/revenue_analysis`

### Recommendations
1. 🔍 Verify column removals are intentional
2. 📊 Review type changes for data loss
3. 🔄 Check downstream dependencies
4. 📝 Update documentation
```

## 🛠 Development

### Setting Up Development Environment

```bash
# Clone repository
git clone https://github.com/yourusername/dbt-break-detector.git
cd dbt-break-detector

# Create virtual environment
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows

# Install development dependencies
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src

# Run specific test categories
pytest tests/test_analyzer.py
pytest -m "not slow"
```

### Code Quality

```bash
# Format code
black src tests

# Sort imports
isort src tests

# Type checking
mypy src

# Lint
flake8 src tests

# Security checks
bandit -r src
```

## 📚 Documentation

### Building Documentation
```bash
# Install documentation dependencies
pip install -e ".[docs]"

# Build documentation
cd docs
make html
```

### API Documentation
Full API documentation is available at [Read the Docs](https://dbt-break-detector.readthedocs.io/).

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### Development Process
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and linting
5. Submit a pull request

### Commit Messages
We follow the [Conventional Commits](https://www.conventionalcommits.org/) specification:
```
feat: add column constraint detection
fix: correct dependency cycle detection
docs: update configuration examples
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- DBT Labs for creating dbt
- NetworkX team for graph analysis capabilities
- All our contributors

## 📬 Contact & Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/dbt-break-detector/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/dbt-break-detector/discussions)
- **Slack**: [Join our community](https://join.slack.com/t/dbt-break-detector/shared_invite/...)
- **Twitter**: [@dbtbreakdetector](https://twitter.com/dbtbreakdetector)

## 🗺 Roadmap

### Upcoming Features
- [ ] dbt Cloud integration
- [ ] Custom rule engine
- [ ] Web interface
- [ ] Real-time monitoring
- [ ] AI-powered impact prediction

### Future Enhancements
- Enhanced visualization of dependencies
- Integration with more CI/CD platforms
- Advanced schema evolution detection
- Performance optimization for large projects