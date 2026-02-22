---
inclusion: manual
contextKey: project-checklist
---

# Project Structure Quick Reference Checklist

## 🚀 New Project Setup Checklist

Use this checklist when starting any new project to ensure proper structure from day one.

---

## Phase 1: Initial Structure (Day 1)

### Core Directories
```bash
mkdir -p src tests docs examples scripts config data
```

- [ ] `src/` - Source code
- [ ] `tests/` - All tests
- [ ] `docs/` - All documentation
- [ ] `examples/` - Example scripts
- [ ] `scripts/` - Utility scripts
- [ ] `config/` - Configuration files
- [ ] `data/` or `test-data/` - Data files

### Python Package Files
- [ ] `src/__init__.py` - Make src a package
- [ ] `setup.py` or `pyproject.toml` - Package configuration
- [ ] `requirements.txt` - Production dependencies
- [ ] `requirements-dev.txt` - Development dependencies

### Version Control
- [ ] `.gitignore` - Ignore patterns
- [ ] `.env.example` - Environment variable template
- [ ] `LICENSE` - License file
- [ ] `VERSION` - Version number file

### Documentation Files
- [ ] Root `README.md` - Quick start (< 200 lines)
- [ ] `docs/README.md` - Main documentation
- [ ] `docs/SETUP_GUIDE.md` - Installation guide
- [ ] `docs/CONTRIBUTING.md` - Contribution guide
- [ ] `docs/CHANGELOG.md` - Version history

---

## Phase 2: Source Code Organization

### Module Structure
```
src/
├── __init__.py
├── core/              # Core functionality
├── processors/        # Processing modules
├── generators/        # Generation modules
└── utils/             # Shared utilities
    ├── config.py      # Configuration management
    ├── logging_utils.py
    └── validation.py
```

- [ ] Created logical module groupings
- [ ] Added `__init__.py` to all packages
- [ ] Created `utils/` for shared code
- [ ] Implemented configuration management

### Configuration Management
- [ ] Created `config/default.yaml` or similar
- [ ] Implemented `Config` class in `src/utils/config.py`
- [ ] Removed all hardcoded paths from source
- [ ] Created `.env.example` for secrets
- [ ] Added environment variable support

---

## Phase 3: Testing Setup

### Test Structure
```
tests/
├── __init__.py
├── conftest.py        # Pytest configuration
├── unit/              # Fast, isolated tests
├── integration/       # Multi-component tests
├── e2e/              # End-to-end tests
└── fixtures/         # Test data
```

- [ ] Created `tests/unit/` directory
- [ ] Created `tests/integration/` directory
- [ ] Created `tests/conftest.py` with fixtures
- [ ] Created `tests/fixtures/` for test data
- [ ] Can run all tests: `pytest tests/`
- [ ] Can run unit tests: `pytest tests/unit/`

### Test Files
- [ ] Named as `test_<module>.py`
- [ ] Test functions named `test_<function>_<scenario>_<result>()`
- [ ] No test files in `src/` directory
- [ ] All tests pass

---

## Phase 4: Documentation

### Essential Documentation
- [ ] `README.md` - Quick start with badges
- [ ] `docs/README.md` - Comprehensive guide
- [ ] `docs/SETUP_GUIDE.md` - Installation steps
- [ ] `docs/API_REFERENCE.md` - API documentation
- [ ] `docs/ARCHITECTURE.md` - System design
- [ ] `docs/USER_GUIDE.md` - Usage examples
- [ ] `docs/TROUBLESHOOTING.md` - Common issues
- [ ] `docs/CHANGELOG.md` - Version history

### Documentation Quality
- [ ] No duplicate documentation
- [ ] All docs in `docs/` directory
- [ ] Root README links to detailed docs
- [ ] API reference is complete
- [ ] Examples are tested and working

---

## Phase 5: Entry Points & CLI

### Entry Point Scripts
```
scripts/
├── main_workflow.py       # Primary entry point
├── setup_environment.py   # Environment setup
└── validate_installation.py  # Dependency check
```

- [ ] Created CLI scripts with `argparse`
- [ ] Added `--help` documentation
- [ ] Added `--config` option for config file
- [ ] Added `--dry-run` option
- [ ] Added `--verbose` option for logging
- [ ] Validated all user inputs
- [ ] Provided clear error messages

### CLI Quality Checks
- [ ] `python scripts/main.py --help` shows usage
- [ ] Works with default configuration
- [ ] Validates input files exist
- [ ] Provides progress feedback
- [ ] Handles errors gracefully

---

## Phase 6: Examples

### Example Scripts
```
examples/
├── README.md              # Guide to examples
├── basic_usage.py         # Simple example
├── advanced_usage.py      # Complex example
└── batch_processing.py    # Batch example
```

- [ ] Created `examples/` directory
- [ ] Created `examples/README.md`
- [ ] Examples use configuration management
- [ ] Examples have clear comments
- [ ] All examples run successfully
- [ ] Examples demonstrate key features

---

## Phase 7: Package Setup

### Python Package Configuration

**setup.py:**
- [ ] Package name defined
- [ ] Version number defined
- [ ] Dependencies listed
- [ ] Entry points configured
- [ ] Package installs: `pip install -e .`

**pyproject.toml:**
- [ ] Build system configured
- [ ] Project metadata complete
- [ ] Dependencies listed
- [ ] Optional dependencies (dev) listed

### Dependency Management
- [ ] `requirements.txt` has production deps
- [ ] `requirements-dev.txt` has dev deps
- [ ] Versions pinned appropriately
- [ ] No unnecessary dependencies

---

## Phase 8: Specifications

### Spec-Driven Development
- [ ] Created `.kiro/specs/project-name/` directory
- [ ] Created `requirements.md` with all requirements
- [ ] Created `tasks.md` with implementation tasks
- [ ] Created `architecture.md` with design
- [ ] Added project organization requirement
- [ ] Added structure setup task

### Requirements Document
- [ ] Includes project organization requirement
- [ ] All requirements have acceptance criteria
- [ ] Requirements are testable
- [ ] Requirements reference tasks

### Tasks Document
- [ ] Initial structure setup task included
- [ ] Tasks reference requirements
- [ ] Tasks have clear completion criteria
- [ ] Tasks are in logical order

---

## Anti-Pattern Checks

### ❌ Things to Avoid

- [ ] ✅ No tests in `src/` directory
- [ ] ✅ No hardcoded paths in source code
- [ ] ✅ No secrets in version control
- [ ] ✅ No duplicate documentation
- [ ] ✅ No examples in `src/` directory
- [ ] ✅ No flat structure (50+ files in root)
- [ ] ✅ No scattered README files
- [ ] ✅ No configuration in source files

---

## Quality Checks

### Code Quality
- [ ] All imports work correctly
- [ ] No circular dependencies
- [ ] Consistent naming conventions
- [ ] Code follows style guide (PEP 8 for Python)
- [ ] Linting passes (pylint, flake8, etc.)

### Documentation Quality
- [ ] All links work
- [ ] No broken references
- [ ] Examples are accurate
- [ ] API docs are complete
- [ ] Troubleshooting covers common issues

### Test Quality
- [ ] All tests pass
- [ ] Test coverage > 80%
- [ ] Tests are fast (unit tests < 1s each)
- [ ] Tests are isolated
- [ ] Tests have clear names

### User Experience
- [ ] Installation is straightforward
- [ ] Quick start works
- [ ] Error messages are helpful
- [ ] CLI is intuitive
- [ ] Examples demonstrate features

---

## Language-Specific Additions

### Python
- [ ] `__init__.py` in all packages
- [ ] `setup.py` or `pyproject.toml`
- [ ] `requirements.txt`
- [ ] `pytest.ini` or `pyproject.toml` test config
- [ ] Type hints (optional but recommended)

### JavaScript/TypeScript
- [ ] `package.json`
- [ ] `tsconfig.json` (TypeScript)
- [ ] `jest.config.js` or similar
- [ ] `dist/` or `build/` in `.gitignore`
- [ ] `.npmignore` or `files` in package.json

### Java
- [ ] `pom.xml` or `build.gradle`
- [ ] `src/main/java/` structure
- [ ] `src/test/java/` structure
- [ ] `target/` or `build/` in `.gitignore`

---

## Final Validation

### Installation Test
```bash
# Clone fresh copy
git clone <repo>
cd <repo>

# Install
pip install -e .

# Run tests
pytest tests/

# Try examples
python examples/basic_usage.py

# Try CLI
python scripts/main.py --help
```

- [ ] Fresh clone works
- [ ] Installation succeeds
- [ ] All tests pass
- [ ] Examples run
- [ ] CLI works

### Documentation Test
- [ ] New user can follow README
- [ ] Setup guide is complete
- [ ] Examples work as documented
- [ ] Troubleshooting helps with issues
- [ ] API reference is accurate

---

## Maintenance Checklist

### Regular Maintenance
- [ ] Update CHANGELOG.md for each release
- [ ] Update VERSION file
- [ ] Update dependencies periodically
- [ ] Run security audits
- [ ] Update documentation as features change
- [ ] Add tests for new features
- [ ] Keep examples up to date

---

## Quick Reference: Directory Purposes

| Directory | Purpose | What Goes Here |
|-----------|---------|----------------|
| `src/` | Source code | All production code |
| `tests/` | Tests | Unit, integration, e2e tests |
| `docs/` | Documentation | All documentation files |
| `examples/` | Examples | Example scripts |
| `scripts/` | Utilities | CLI scripts, setup scripts |
| `config/` | Configuration | YAML/JSON config files |
| `data/` | Data | Sample data, test data |
| `.kiro/specs/` | Specifications | Requirements, tasks, architecture |

---

## Quick Reference: File Purposes

| File | Purpose |
|------|---------|
| `README.md` (root) | Quick start guide |
| `setup.py` | Package installation |
| `requirements.txt` | Production dependencies |
| `requirements-dev.txt` | Development dependencies |
| `.gitignore` | Git ignore patterns |
| `.env.example` | Environment variable template |
| `LICENSE` | License information |
| `VERSION` | Version number |

---

## When to Use This Checklist

✅ **Use at project start:**
- Starting a new project from scratch
- Creating initial project structure
- Setting up spec-driven development

✅ **Use during development:**
- Adding new modules or features
- Reviewing project organization
- Onboarding new team members

✅ **Use before release:**
- Preparing for v1.0 release
- Ensuring professional structure
- Validating documentation completeness

---

## Time Estimates

- **Phase 1-2** (Structure & Code): 2-4 hours
- **Phase 3** (Testing): 1-2 hours
- **Phase 4** (Documentation): 2-4 hours
- **Phase 5-6** (CLI & Examples): 2-3 hours
- **Phase 7-8** (Package & Specs): 1-2 hours

**Total:** 8-15 hours for complete professional setup

**ROI:** Saves weeks of reorganization later!

---

## Print-Friendly Version

For a quick reference, print this checklist and check off items as you complete them. The structure you create on day 1 will serve your project for its entire lifetime.

---

**Remember:** Good structure is an investment, not overhead. Every hour spent on proper organization saves 10 hours of maintenance later.

---

**Related Documents:**
- Full guide: `.kiro/steering/project-structure-guide.md`
- Project specs: `.kiro/specs/project-name/`

**Last Updated:** 2025-01-31
**Version:** 1.0.0
