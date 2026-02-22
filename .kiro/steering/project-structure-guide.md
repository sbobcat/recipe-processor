---
inclusion: manual
contextKey: project-structure
---

# Project Structure Best Practices - Steering Guide

## Purpose

This steering guide ensures new projects start with professional, maintainable structure following industry best practices. Use this guide during project initialization and spec creation to avoid costly reorganization later.

## When to Use This Guide

- ✅ Starting a new project from scratch
- ✅ Creating initial project specifications
- ✅ Reviewing project structure during design phase
- ✅ Evaluating existing project organization
- ✅ Planning major refactoring or reorganization

## Core Principles

### 1. Separation of Concerns
**Principle:** Different types of files serve different purposes and should be organized accordingly.

**Implementation:**
- Source code separate from tests
- Documentation separate from code
- Examples separate from production code
- Configuration separate from implementation
- Test data separate from production data

### 2. Discoverability
**Principle:** Developers should easily find what they need without extensive searching.

**Implementation:**
- Predictable directory names (src/, tests/, docs/)
- Clear module boundaries
- Consistent naming conventions
- Centralized documentation
- Obvious entry points

### 3. Scalability
**Principle:** Structure should support growth without requiring reorganization.

**Implementation:**
- Modular architecture
- Clear extension points
- Logical grouping of related functionality
- Room for new features without structural changes

### 4. Professional Standards
**Principle:** Follow language-specific and industry best practices.

**Implementation:**
- Standard package structure for the language
- Conventional directory names
- Proper dependency management
- Version control best practices

---

## Standard Project Structure Template

### Python Projects

```
project-name/
├── .git/                           # Version control
├── .github/                        # GitHub-specific files
│   ├── workflows/                  # CI/CD workflows
│   └── ISSUE_TEMPLATE/            # Issue templates
│
├── docs/                           # 📚 All documentation
│   ├── README.md                  # Main documentation
│   ├── SETUP_GUIDE.md             # Quick setup
│   ├── USER_GUIDE.md              # Usage examples
│   ├── API_REFERENCE.md           # API documentation
│   ├── ARCHITECTURE.md            # System design
│   ├── CONTRIBUTING.md            # Contribution guide
│   ├── TROUBLESHOOTING.md         # Common issues
│   └── CHANGELOG.md               # Version history
│
├── src/                            # 🔧 Source code
│   ├── __init__.py
│   ├── core/                      # Core functionality
│   │   ├── __init__.py
│   │   └── ...
│   ├── processors/                # Processing modules
│   │   ├── __init__.py
│   │   └── ...
│   ├── generators/                # Generation modules
│   │   ├── __init__.py
│   │   └── ...
│   └── utils/                     # Shared utilities
│       ├── __init__.py
│       ├── config.py              # Configuration management
│       ├── logging_utils.py       # Logging setup
│       └── validation.py          # Input validation
│
├── tests/                          # 🧪 All tests
│   ├── __init__.py
│   ├── conftest.py                # Pytest configuration
│   ├── unit/                      # Unit tests
│   │   ├── test_core.py
│   │   ├── test_processors.py
│   │   └── ...
│   ├── integration/               # Integration tests
│   │   ├── test_workflows.py
│   │   └── ...
│   ├── e2e/                       # End-to-end tests
│   │   └── ...
│   └── fixtures/                  # Test fixtures
│       ├── sample_data/
│       └── mocks/
│
├── examples/                       # 📖 Example scripts
│   ├── README.md                  # Examples guide
│   ├── basic_usage.py
│   ├── advanced_usage.py
│   └── ...
│
├── scripts/                        # 🛠️ Utility scripts
│   ├── setup_environment.py       # Environment setup
│   ├── validate_installation.py   # Dependency check
│   └── ...
│
├── config/                         # ⚙️ Configuration
│   ├── default.yaml               # Default settings
│   ├── development.yaml           # Dev settings
│   └── production.yaml            # Prod settings
│
├── data/                           # 📦 Data files
│   ├── sample/                    # Sample data
│   ├── test/                      # Test data
│   └── fixtures/                  # Fixed datasets
│
├── .kiro/                          # Kiro IDE config
│   ├── specs/                     # Project specs
│   │   └── project-name/
│   │       ├── requirements.md
│   │       ├── tasks.md
│   │       └── architecture.md
│   └── steering/                  # Steering guides
│       └── ...
│
├── .gitignore                      # Git ignore rules
├── .env.example                    # Environment variables template
├── requirements.txt                # Production dependencies
├── requirements-dev.txt            # Development dependencies
├── setup.py                        # Package installation
├── pyproject.toml                  # Modern Python packaging
├── pytest.ini                      # Pytest configuration
├── README.md                       # Quick start guide
├── LICENSE                         # License file
└── VERSION                         # Version number
```

### JavaScript/TypeScript Projects

```
project-name/
├── src/                            # Source code
│   ├── core/
│   ├── components/
│   ├── utils/
│   └── index.ts
│
├── tests/                          # All tests
│   ├── unit/
│   ├── integration/
│   └── e2e/
│
├── docs/                           # Documentation
├── examples/                       # Examples
├── scripts/                        # Utility scripts
├── config/                         # Configuration
│
├── package.json                    # Dependencies
├── tsconfig.json                   # TypeScript config
├── jest.config.js                  # Jest config
└── README.md
```

---

## Critical Anti-Patterns to Avoid

### ❌ Anti-Pattern 1: Tests Mixed with Source Code
**Problem:**
```
src/
├── processor.py
├── test_processor.py          # ❌ Test in source directory
├── generator.py
└── test_generator.py          # ❌ Test in source directory
```

**Solution:**
```
src/
├── processor.py
└── generator.py

tests/
├── test_processor.py          # ✅ Tests separate
└── test_generator.py          # ✅ Tests separate
```

### ❌ Anti-Pattern 2: Scattered Documentation
**Problem:**
```
README.md
SETUP.md
src/
├── README.md                  # ❌ Duplicate docs
├── processors/
│   └── README.md              # ❌ Scattered docs
└── generators/
    └── README.md              # ❌ Scattered docs
```

**Solution:**
```
docs/
├── README.md                  # ✅ Main docs
├── SETUP_GUIDE.md            # ✅ Centralized
├── API_REFERENCE.md          # ✅ All API docs here
└── ARCHITECTURE.md           # ✅ Design docs

README.md                      # ✅ Quick start only
```

### ❌ Anti-Pattern 3: Examples Mixed with Production Code
**Problem:**
```
src/
├── processor.py
├── example_usage.py           # ❌ Example in source
├── generator.py
└── example_generator.py       # ❌ Example in source
```

**Solution:**
```
src/
├── processor.py
└── generator.py

examples/
├── basic_usage.py             # ✅ Examples separate
└── advanced_usage.py          # ✅ Examples separate
```

### ❌ Anti-Pattern 4: Hardcoded Configuration
**Problem:**
```python
# ❌ Hardcoded in source file
def process_file():
    input_path = "C:\\Users\\John\\Documents\\input.pdf"
    output_path = "C:\\Users\\John\\Documents\\output"
    api_key = "sk-1234567890"
```

**Solution:**
```python
# ✅ Configuration management
from src.utils.config import Config

def process_file():
    config = Config()
    input_path = config.get('paths.input')
    output_path = config.get('paths.output')
    api_key = config.get('api.key')  # From env var
```

### ❌ Anti-Pattern 5: No Clear Entry Points
**Problem:**
```
# User must know to edit and run specific file
python src/processors/aws_processor.py
```

**Solution:**
```bash
# Clear CLI entry point
python scripts/process.py --input file.pdf --output results/
```

### ❌ Anti-Pattern 6: Flat Structure
**Problem:**
```
project/
├── processor1.py
├── processor2.py
├── processor3.py
├── generator1.py
├── generator2.py
├── utils1.py
├── utils2.py
└── ... (50+ files)            # ❌ No organization
```

**Solution:**
```
project/
├── src/
│   ├── processors/            # ✅ Grouped by function
│   │   ├── processor1.py
│   │   ├── processor2.py
│   │   └── processor3.py
│   ├── generators/            # ✅ Grouped by function
│   │   ├── generator1.py
│   │   └── generator2.py
│   └── utils/                 # ✅ Grouped by function
│       ├── utils1.py
│       └── utils2.py
```

---

## Documentation Structure Best Practices

### Root README.md
**Purpose:** Quick start and navigation hub

**Contents:**
- Project name and brief description (1-2 sentences)
- Badges (build status, version, license)
- Quick installation instructions
- Minimal usage example
- Links to detailed documentation
- Links to contributing guide

**Length:** Keep under 200 lines

### docs/README.md
**Purpose:** Comprehensive main documentation

**Contents:**
- Detailed project description
- Features list
- Prerequisites and requirements
- Complete installation guide
- Usage examples
- Configuration options
- Troubleshooting section

### docs/API_REFERENCE.md
**Purpose:** Complete API documentation

**Contents:**
- All public classes and methods
- Parameters and return values
- Usage examples for each API
- Code snippets

### docs/ARCHITECTURE.md
**Purpose:** System design documentation

**Contents:**
- High-level architecture overview
- Component relationships
- Data flow diagrams
- Design decisions and rationale
- Extension points

### docs/USER_GUIDE.md
**Purpose:** Detailed usage examples

**Contents:**
- Real-world scenarios
- Step-by-step tutorials
- Best practices
- Common workflows
- Tips and tricks

---

## Configuration Management Best Practices

### Use Configuration Files, Not Hardcoded Values

**Bad:**
```python
class Processor:
    def __init__(self):
        self.api_key = "sk-1234567890"
        self.endpoint = "https://api.example.com"
        self.timeout = 30
```

**Good:**
```python
class Processor:
    def __init__(self, config):
        self.api_key = config.get('api.key')
        self.endpoint = config.get('api.endpoint')
        self.timeout = config.get('api.timeout', default=30)
```

### Configuration File Structure

**config/default.yaml:**
```yaml
# Application settings
app:
  name: "My Application"
  version: "1.0.0"
  debug: false

# API settings
api:
  endpoint: "https://api.example.com"
  timeout: 30
  retry_attempts: 3

# Paths (use relative paths)
paths:
  input: "data/input"
  output: "data/output"
  temp: "data/temp"

# Processing settings
processing:
  batch_size: 100
  parallel: true
  max_workers: 4
```

### Environment Variables for Secrets

**Never commit secrets to version control!**

**.env.example:**
```bash
# API Keys (DO NOT commit actual values)
API_KEY=your_api_key_here
SECRET_KEY=your_secret_key_here

# Database (for production)
DATABASE_URL=postgresql://user:pass@localhost/db
```

**Usage:**
```python
import os
from dotenv import load_dotenv

load_dotenv()  # Load from .env file

api_key = os.getenv('API_KEY')
```

---

## Test Organization Best Practices

### Test Directory Structure

```
tests/
├── conftest.py                 # Shared fixtures
├── unit/                       # Fast, isolated tests
│   ├── test_processors.py
│   ├── test_generators.py
│   └── test_utils.py
├── integration/                # Multi-component tests
│   ├── test_workflows.py
│   └── test_pipelines.py
├── e2e/                        # End-to-end tests
│   └── test_complete_flow.py
└── fixtures/                   # Test data
    ├── sample_data/
    └── expected_outputs/
```

### Test Naming Conventions

**File names:**
- `test_<module_name>.py`
- Example: `test_processor.py`, `test_generator.py`

**Test function names:**
- `test_<function>_<scenario>_<expected_result>`
- Example: `test_process_image_with_valid_input_returns_text()`
- Example: `test_process_image_with_invalid_format_raises_error()`

### Test Organization Principles

1. **Unit Tests** - Test individual functions/methods in isolation
   - Fast (< 1 second each)
   - No external dependencies
   - Use mocks for dependencies

2. **Integration Tests** - Test multiple components together
   - Moderate speed (< 10 seconds each)
   - May use real dependencies
   - Test component interactions

3. **End-to-End Tests** - Test complete workflows
   - Slower (< 60 seconds each)
   - Use real system
   - Test user scenarios

---

## Entry Points and CLI Best Practices

### Provide Clear Entry Points

**Bad:** Users must edit source files
```python
# user must edit this file
if __name__ == "__main__":
    input_file = "C:\\path\\to\\file.pdf"  # Edit this
    process(input_file)
```

**Good:** CLI with arguments
```python
# scripts/process.py
import argparse

def main():
    parser = argparse.ArgumentParser(description="Process documents")
    parser.add_argument("input", help="Input file path")
    parser.add_argument("-o", "--output", help="Output directory")
    parser.add_argument("-c", "--config", help="Config file")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    
    # Process with arguments
    process(args.input, args.output, args.config, args.dry_run)

if __name__ == "__main__":
    main()
```

### CLI Design Principles

1. **Help is Essential**
   ```bash
   python scripts/process.py --help
   ```
   Should show clear usage instructions

2. **Sensible Defaults**
   ```bash
   python scripts/process.py input.pdf
   # Uses default output directory, default config
   ```

3. **Validation and Feedback**
   ```bash
   python scripts/process.py missing.pdf
   # Error: File 'missing.pdf' not found
   ```

4. **Dry-Run Mode**
   ```bash
   python scripts/process.py input.pdf --dry-run
   # Shows what would happen without doing it
   ```

---

## Package Structure Best Practices

### Python Package Setup

**Minimal setup.py:**
```python
from setuptools import setup, find_packages

setup(
    name="project-name",
    version="1.0.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "dependency1>=1.0.0",
        "dependency2>=2.0.0",
    ],
    entry_points={
        "console_scripts": [
            "project-cli=src.cli:main",
        ],
    },
)
```

**Modern pyproject.toml:**
```toml
[build-system]
requires = ["setuptools>=45", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "project-name"
version = "1.0.0"
description = "Brief description"
authors = [{name = "Your Name", email = "you@example.com"}]
license = {text = "MIT"}
requires-python = ">=3.8"
dependencies = [
    "dependency1>=1.0.0",
    "dependency2>=2.0.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0.0",
    "black>=22.0.0",
    "mypy>=0.950",
]

[project.scripts]
project-cli = "src.cli:main"
```

### Dependency Management

**requirements.txt** (production):
```
dependency1>=1.0.0,<2.0.0
dependency2>=2.0.0,<3.0.0
```

**requirements-dev.txt** (development):
```
-r requirements.txt
pytest>=7.0.0
black>=22.0.0
mypy>=0.950
pylint>=2.0.0
```

---

## Specification-Driven Structure

### Include Structure in Requirements

**Add to requirements.md:**

```markdown
### Requirement X: Project Organization

**User Story:** As a developer, I want a well-organized codebase, so that I can easily understand and maintain the system.

#### Acceptance Criteria

1. WHEN exploring the project, THE System SHALL have clear separation between source code, tests, documentation, and examples
2. WHEN reading documentation, THE System SHALL provide centralized documentation in docs/ directory
3. WHEN running tests, THE System SHALL organize tests by type (unit, integration, e2e)
4. WHEN configuring the system, THE System SHALL use configuration files instead of hardcoded values
5. WHEN installing the system, THE System SHALL support standard package installation
```

### Include Structure in Initial Tasks

**Add to tasks.md:**

```markdown
- [ ] 0. Project Structure Setup
  - Create directory structure (src/, tests/, docs/, examples/, config/)
  - Create __init__.py files for all packages
  - Create configuration management system
  - Create entry point scripts
  - Set up package installation (setup.py, pyproject.toml)
  - Create initial documentation structure
  - _Requirements: Project Organization_
```

---

## Checklist for New Projects

Use this checklist when starting a new project:

### Directory Structure
- [ ] Created `src/` for source code
- [ ] Created `tests/` with `unit/` and `integration/` subdirectories
- [ ] Created `docs/` for all documentation
- [ ] Created `examples/` for example scripts
- [ ] Created `scripts/` for utility scripts
- [ ] Created `config/` for configuration files
- [ ] Created `data/` or `test-data/` for data files

### Documentation
- [ ] Created root `README.md` as quick start
- [ ] Created `docs/README.md` as main documentation
- [ ] Created `docs/SETUP_GUIDE.md`
- [ ] Created `docs/API_REFERENCE.md`
- [ ] Created `docs/ARCHITECTURE.md`
- [ ] Created `docs/CONTRIBUTING.md`
- [ ] Created `docs/CHANGELOG.md`

### Configuration
- [ ] Created `config/default.yaml` or similar
- [ ] Created `.env.example` for environment variables
- [ ] Implemented configuration management class
- [ ] No hardcoded paths in source code
- [ ] No secrets in version control

### Testing
- [ ] Created `tests/conftest.py` with pytest configuration
- [ ] Organized tests by type (unit, integration, e2e)
- [ ] Created test fixtures directory
- [ ] Can run all tests with single command

### Package Setup
- [ ] Created `setup.py` or `pyproject.toml`
- [ ] Created `requirements.txt`
- [ ] Created `requirements-dev.txt`
- [ ] Package installs with `pip install -e .`
- [ ] Entry point scripts configured

### Entry Points
- [ ] Created CLI scripts with argparse
- [ ] Added `--help` documentation
- [ ] Added `--config` option
- [ ] Added `--dry-run` option
- [ ] Validated user inputs

### Version Control
- [ ] Created `.gitignore` with appropriate rules
- [ ] Excluded `__pycache__/`, `*.pyc`, `.env`
- [ ] Excluded output directories
- [ ] Excluded IDE-specific files

### Specifications
- [ ] Added project organization requirement
- [ ] Added initial structure setup task
- [ ] Documented structure in architecture doc

---

## Language-Specific Variations

### Python
- Use `src/` for source code
- Use `tests/` for tests
- Use `setup.py` or `pyproject.toml`
- Use `requirements.txt` for dependencies

### JavaScript/TypeScript
- Use `src/` for source code
- Use `tests/` or `__tests__/` for tests
- Use `package.json` for dependencies
- Use `dist/` or `build/` for compiled output

### Java
- Use `src/main/java/` for source code
- Use `src/test/java/` for tests
- Use `pom.xml` or `build.gradle` for dependencies
- Use `target/` or `build/` for compiled output

### Go
- Use flat structure or `cmd/`, `pkg/`, `internal/`
- Use `_test.go` suffix for tests
- Use `go.mod` for dependencies

---

## Migration Strategy

If you have an existing project that doesn't follow these practices:

### Phase 1: Assessment
1. Document current structure
2. Identify issues (scattered tests, docs, hardcoded paths)
3. Create migration plan

### Phase 2: Non-Breaking Changes
1. Create new directories (don't move files yet)
2. Copy (don't move) files to new locations
3. Update imports in copied files
4. Test new structure works

### Phase 3: Breaking Changes
1. Move files to new locations
2. Update all imports
3. Remove old files
4. Update documentation

### Phase 4: Configuration
1. Implement configuration management
2. Remove hardcoded values
3. Create configuration files

### Phase 5: Validation
1. Run all tests
2. Verify package installation
3. Test all entry points
4. Update documentation

---

## Benefits of Proper Structure

### For Individual Developers
- ✅ Faster navigation and file discovery
- ✅ Easier to understand codebase
- ✅ Less time spent searching for files
- ✅ Clear separation of concerns

### For Teams
- ✅ Easier onboarding for new developers
- ✅ Consistent structure across projects
- ✅ Better collaboration
- ✅ Reduced merge conflicts

### For Projects
- ✅ Professional appearance
- ✅ Easier to maintain and extend
- ✅ Better testing practices
- ✅ Scalable architecture
- ✅ Easier to document

---

## Common Questions

**Q: Should I create all directories upfront?**
A: Create the main structure (src/, tests/, docs/) immediately. Add subdirectories as needed.

**Q: What if my project is small?**
A: Even small projects benefit from basic structure. Start with src/, tests/, and docs/.

**Q: Can I have multiple src/ directories?**
A: Generally no. Use subdirectories within src/ for different modules.

**Q: Where do scripts go?**
A: Utility scripts go in scripts/. Entry point scripts can be in scripts/ or configured in setup.py.

**Q: Should examples be in docs/?**
A: No. Examples are code and should be in examples/ directory. Docs should reference them.

**Q: What about notebooks?**
A: Create notebooks/ directory for Jupyter notebooks, separate from src/.

---

## Summary

**Key Takeaways:**

1. **Start with structure** - Don't wait until the project is messy
2. **Separate concerns** - Code, tests, docs, examples, config
3. **Centralize documentation** - One docs/ directory
4. **Use configuration files** - No hardcoded paths
5. **Provide entry points** - Clear CLI scripts
6. **Follow standards** - Language-specific best practices
7. **Include in specs** - Make structure a requirement

**Remember:** Time spent on proper structure upfront saves exponentially more time later in maintenance, debugging, and onboarding.

---

## References

- [Python Packaging User Guide](https://packaging.python.org/)
- [The Hitchhiker's Guide to Python](https://docs.python-guide.org/)
- [Cookiecutter Templates](https://github.com/cookiecutter/cookiecutter)
- [Structuring Your Project](https://docs.python-guide.org/writing/structure/)

---

**Last Updated:** 2025-01-31
**Version:** 1.0.0
