---
inclusion: manual
contextKey: structure-template
---

# Project Structure Task Template

## Purpose

This template provides a ready-to-use task definition for setting up proper project structure. Copy this into your `tasks.md` file at the beginning of any new project.

---

## Task Template for tasks.md

Copy the following into your project's `.kiro/specs/project-name/tasks.md` file:

```markdown
## Initial Setup Tasks

- [ ] 0. Project Structure and Foundation Setup
  - Create professional directory structure following best practices
  - Set up configuration management system
  - Create entry point scripts with CLI
  - Establish testing framework
  - Set up documentation structure
  - Configure package installation
  - _Requirements: Project Organization and Maintainability_

- [ ] 0.1 Create core directory structure
  - Create src/ for all source code
  - Create tests/ with unit/ and integration/ subdirectories
  - Create docs/ for all documentation
  - Create examples/ for example scripts
  - Create scripts/ for utility and entry point scripts
  - Create config/ for configuration files
  - Create data/ or test-data/ for data files
  - Add __init__.py files to all Python packages
  - _Requirements: Clear separation of concerns_

- [ ] 0.2 Set up version control and ignore patterns
  - Create .gitignore with appropriate patterns
  - Exclude __pycache__/, *.pyc, .env files
  - Exclude output directories and temporary files
  - Exclude IDE-specific files (.vscode/, .idea/)
  - Create .env.example for environment variable template
  - _Requirements: Version control best practices_

- [ ] 0.3 Implement configuration management
  - Create config/default.yaml with all system settings
  - Create config/development.yaml for dev settings
  - Create config/production.yaml for prod settings
  - Implement src/utils/config.py with Config class
  - Add support for environment variable overrides
  - Add configuration validation
  - Ensure no hardcoded paths in source code
  - _Requirements: Configuration management, no hardcoded values_

- [ ] 0.4 Set up testing framework
  - Create tests/conftest.py with pytest configuration
  - Create tests/unit/ for unit tests
  - Create tests/integration/ for integration tests
  - Create tests/fixtures/ for test data and mocks
  - Configure pytest.ini or pyproject.toml for test settings
  - Ensure tests can be run with: pytest tests/
  - _Requirements: Organized test structure_

- [ ] 0.5 Create documentation structure
  - Create root README.md as quick start guide (< 200 lines)
  - Create docs/README.md as comprehensive documentation
  - Create docs/SETUP_GUIDE.md with installation instructions
  - Create docs/API_REFERENCE.md for API documentation
  - Create docs/ARCHITECTURE.md for system design
  - Create docs/USER_GUIDE.md for usage examples
  - Create docs/TROUBLESHOOTING.md for common issues
  - Create docs/CONTRIBUTING.md for contribution guidelines
  - Create docs/CHANGELOG.md for version history
  - _Requirements: Centralized documentation_

- [ ] 0.6 Create entry point scripts with CLI
  - Create scripts/ directory for utility scripts
  - Create main entry point script with argparse
  - Add --help documentation with usage examples
  - Add --config option for custom configuration files
  - Add --dry-run option for validation without execution
  - Add --verbose option for detailed logging
  - Implement input validation and error handling
  - _Requirements: Clear entry points, user-friendly CLI_

- [ ] 0.7 Set up Python package structure
  - Create setup.py with package metadata
  - Create pyproject.toml for modern Python packaging
  - Create requirements.txt with production dependencies
  - Create requirements-dev.txt with development dependencies
  - Configure package to install entry point scripts
  - Test installation with: pip install -e .
  - Verify package imports work correctly
  - _Requirements: Standard package installation_

- [ ] 0.8 Create example scripts
  - Create examples/ directory
  - Create examples/README.md with guide to all examples
  - Create basic_usage.py with simple example
  - Create advanced_usage.py with complex example
  - Ensure examples use configuration management
  - Add comprehensive comments to each example
  - Test all examples run successfully
  - _Requirements: Organized examples, learning resources_

- [ ] 0.9 Create utility scripts
  - Create scripts/setup_environment.py for environment validation
  - Create scripts/validate_installation.py to check dependencies
  - Create scripts/cleanup_outputs.py for cleaning test outputs
  - Add help text and documentation to all scripts
  - Test all utility scripts work correctly
  - _Requirements: Developer tools, environment setup_

- [ ] 0.10 Validate complete structure
  - Run all tests: pytest tests/
  - Verify package installs: pip install -e .
  - Test all entry point scripts work
  - Test all examples run successfully
  - Verify all documentation links are valid
  - Run linting and code quality checks
  - Ensure no hardcoded paths remain in code
  - Verify .gitignore excludes appropriate files
  - _Requirements: Complete validation of project structure_
```

---

## Requirement Template for requirements.md

Copy the following into your project's `.kiro/specs/project-name/requirements.md` file:

```markdown
### Requirement X: Project Organization and Maintainability

**User Story:** As a developer or new user, I want a well-organized codebase with clear structure, so that I can easily understand, navigate, maintain, and extend the system.

#### Acceptance Criteria

1. WHEN exploring the project, THE System SHALL have clear separation between source code, tests, documentation, examples, and configuration
2. WHEN reading documentation, THE System SHALL provide centralized, non-redundant documentation in a dedicated docs/ directory
3. WHEN running tests, THE System SHALL organize all tests in a tests/ directory with clear separation between unit and integration tests
4. WHEN configuring the system, THE System SHALL use YAML configuration files instead of hardcoded paths in source code
5. WHEN starting to use the system, THE System SHALL provide clear entry point scripts with command-line interfaces
6. WHEN examining code modules, THE System SHALL have logical separation of concerns (processors, generators, utilities)
7. WHEN looking for examples, THE System SHALL provide organized example scripts in a dedicated examples/ directory
8. WHEN installing the system, THE System SHALL support standard Python package installation with pip
9. WHEN importing modules, THE System SHALL use consistent naming conventions and proper package structure
10. THE System SHALL follow Python best practices for project structure and organization

#### Glossary Terms

- **Configuration_File**: YAML file containing system settings and paths
- **Entry_Point_Script**: Command-line script providing user-friendly interface to system functionality
- **Module**: Logical grouping of related code (processors, generators, utilities)
- **Test_Suite**: Collection of automated tests organized by type (unit, integration, e2e)
```

---

## Customization Guide

### Adjust for Project Size

**Small Project (< 1000 lines):**
- Simplify to tasks 0.1, 0.3, 0.4, 0.5, 0.10
- Combine documentation into fewer files
- Skip advanced examples

**Medium Project (1000-10000 lines):**
- Use all tasks as written
- Add more specific module organization
- Include comprehensive examples

**Large Project (> 10000 lines):**
- Add more granular tasks
- Include architecture documentation task
- Add performance testing setup
- Include CI/CD pipeline setup

### Adjust for Language

**Python:**
- Use tasks as written
- Add type checking setup (mypy)
- Add code formatting (black, isort)

**JavaScript/TypeScript:**
- Replace setup.py with package.json
- Replace pytest with jest/mocha
- Add build step (webpack, rollup)
- Add TypeScript configuration

**Java:**
- Replace setup.py with pom.xml or build.gradle
- Replace pytest with JUnit
- Adjust directory structure (src/main/java, src/test/java)

**Go:**
- Simplify structure (Go has conventions)
- Use go.mod for dependencies
- Use built-in testing framework

### Adjust for Team Size

**Solo Developer:**
- Can skip some documentation
- Focus on code organization
- Minimal examples needed

**Small Team (2-5):**
- Use all tasks
- Emphasize documentation
- Include contribution guide

**Large Team (5+):**
- Add code review guidelines
- Add architecture decision records
- Include detailed contribution guide
- Add onboarding documentation

---

## Integration with Spec-Driven Development

### Step 1: Create Specs First
1. Create `.kiro/specs/project-name/` directory
2. Create `requirements.md` with project organization requirement
3. Create `tasks.md` with structure setup tasks
4. Create `architecture.md` with design overview

### Step 2: Execute Structure Tasks
1. Complete tasks 0.1-0.10 in order
2. Validate after each task
3. Update tasks.md as you complete items

### Step 3: Build on Foundation
1. Add feature-specific requirements
2. Add feature-specific tasks
3. Implement features in well-organized structure

---

## Success Criteria

After completing these tasks, you should have:

✅ **Professional Structure**
- Clear directory organization
- Logical separation of concerns
- Follows language best practices

✅ **Complete Documentation**
- Quick start guide
- Comprehensive documentation
- API reference
- Architecture overview

✅ **Working Tests**
- Test framework configured
- Can run all tests with one command
- Tests organized by type

✅ **Configuration Management**
- No hardcoded paths
- YAML configuration files
- Environment variable support

✅ **User-Friendly CLI**
- Clear entry points
- Help documentation
- Input validation

✅ **Package Installation**
- Installs with pip
- Dependencies managed
- Entry points configured

✅ **Quality Examples**
- Basic and advanced examples
- Examples use configuration
- All examples work

---

## Time Estimates

| Task | Estimated Time |
|------|----------------|
| 0.1 - Directory structure | 30 minutes |
| 0.2 - Version control | 15 minutes |
| 0.3 - Configuration | 1-2 hours |
| 0.4 - Testing framework | 1 hour |
| 0.5 - Documentation | 2-3 hours |
| 0.6 - Entry points | 1-2 hours |
| 0.7 - Package setup | 1 hour |
| 0.8 - Examples | 1-2 hours |
| 0.9 - Utility scripts | 1 hour |
| 0.10 - Validation | 1 hour |
| **Total** | **10-15 hours** |

**Note:** This is time well spent! It prevents weeks of reorganization later.

---

## Common Pitfalls to Avoid

### ❌ Skipping Structure Setup
**Problem:** "I'll organize it later"
**Result:** Technical debt, costly reorganization

**Solution:** Do it now, it's faster upfront

### ❌ Partial Implementation
**Problem:** "I'll just create the directories"
**Result:** Directories exist but aren't used properly

**Solution:** Complete all tasks, not just directory creation

### ❌ Hardcoded Paths
**Problem:** "I'll add configuration later"
**Result:** Hardcoded paths throughout codebase

**Solution:** Implement configuration management immediately

### ❌ No Entry Points
**Problem:** "Users can just edit the script"
**Result:** Poor user experience, hard to use

**Solution:** Create CLI scripts from the start

### ❌ Scattered Documentation
**Problem:** "I'll add README files where needed"
**Result:** Duplicate, inconsistent documentation

**Solution:** Centralize all docs in docs/ directory

---

## Validation Checklist

Before moving on to feature development:

- [ ] All directories created
- [ ] All __init__.py files in place
- [ ] Configuration management working
- [ ] Tests can be run with pytest
- [ ] Package installs with pip
- [ ] CLI scripts work
- [ ] Examples run successfully
- [ ] Documentation is complete
- [ ] No hardcoded paths in code
- [ ] .gitignore excludes appropriate files

---

## Next Steps After Structure Setup

Once structure is complete:

1. **Add Feature Requirements** - Define what the system should do
2. **Create Feature Tasks** - Break down implementation
3. **Implement Features** - Build on solid foundation
4. **Write Tests** - Use established test structure
5. **Document Features** - Add to existing docs
6. **Create Examples** - Show how to use features

---

## Related Resources

- **Full Guide:** `.kiro/steering/project-structure-guide.md`
- **Quick Checklist:** `.kiro/steering/project-structure-checklist.md`
- **This Template:** `.kiro/steering/project-structure-task-template.md`

---

**Remember:** Structure is not overhead, it's foundation. Build on solid ground from day one.

---

**Last Updated:** 2025-01-31
**Version:** 1.0.0
