---
title: Python Best Practices
inclusion: fileMatch
fileMatchPattern: '*.py'
---

# Python Best Practices

## General

- Use flake8 for checking code
- Follow PEP 8 style guide with 88-character line limit (Black formatter)
- Use meaningful variable and function names that describe their purpose

## Code Style

- Use snake_case for variables and functions
- Use PascalCase for classes
- Use UPPER_SNAKE_CASE for constants
- Limit line length to 88 characters (Black formatter)
- Use descriptive docstrings for modules, classes, and functions
- Include shebang line (`#!/usr/bin/env python3`) for executable scripts

## Type Hints

- Use type hints for function parameters and return values
- Import types from `typing` module when needed
- Use `Optional` for nullable values
- Use `Union` for multiple possible types
- Use `Dict[str, Any]` for flexible dictionary structures
- Use `List[Type]` for typed lists

## Error Handling

- Use specific exception types rather than bare `except:`
- Handle exceptions at appropriate levels
- Use context managers (`with` statements) for resource management
- Log errors with appropriate detail using the `logging` module
- Provide meaningful error messages to users
- Use try-except blocks for external dependencies and file operations

## Code Organization

- Use virtual environments for dependencies
- Create requirements.txt with pinned versions
- Organize code into modules and packages
- Use `__init__.py` files appropriately
- Separate configuration from code (use config files or environment variables)
- Create utility functions for common operations

## File and Path Handling

- Use `pathlib.Path` instead of `os.path` for path operations
- Use `Path.exists()`, `Path.mkdir(exist_ok=True)` for file system operations
- Handle both Windows and Unix path separators with pathlib
- Use context managers for file operations (`with open()`)
- Specify encoding explicitly when reading/writing text files (`encoding='utf-8'`)

## External Process Integration

- Use `subprocess.run()` with proper error handling
- Capture both stdout and stderr for debugging
- Set timeouts for external processes to prevent hanging
- Check return codes and handle failures gracefully
- Use `shutil.which()` to verify external tools are available

## AWS and Cloud Integration

- Use boto3 sessions for AWS service clients
- Handle AWS service exceptions specifically (ClientError, etc.)
- Implement retry logic for transient failures
- Use environment variables or AWS profiles for credentials
- Test AWS connectivity before processing large batches

## Testing

- Write unit tests using pytest
- Use descriptive test function names that explain what is being tested
- Mock external dependencies (AWS services, file system, subprocess calls)
- Aim for high test coverage of core business logic
- Use fixtures for test setup and teardown
- Run tests with minimal output: `pytest -q` or `python -m pytest --tb=short -q`
- Filter specific tests: `pytest -k "test_name"` to avoid running full suites
- Test both success and failure scenarios

## Performance

- Use list comprehensions over loops when appropriate
- Use generators for large datasets to manage memory
- Profile code before optimizing
- Use appropriate data structures (sets for membership tests, dicts for lookups)
- Process large files in chunks rather than loading entirely into memory
- Use `pathlib` operations which are generally faster than string manipulation

## Logging and Debugging

- Use the `logging` module instead of print statements for debugging
- Configure logging levels appropriately (INFO for user messages, DEBUG for development)
- Include context in log messages (file names, page numbers, etc.)
- Use structured logging for complex applications
- Log both successes and failures for audit trails

## Configuration Management

- Use configuration files (JSON, YAML) or environment variables
- Provide sensible defaults for all configuration options
- Validate configuration at startup
- Document all configuration options
- Use type hints for configuration classes/functions

## Documentation

- Write clear docstrings for all public functions and classes
- Include parameter types and return types in docstrings
- Provide usage examples in module docstrings
- Document any external dependencies or setup requirements
- Use inline comments for complex logic or business rules

## Security

- Never hardcode credentials or sensitive information
- Use environment variables or secure credential stores
- Validate all user inputs
- Be careful with file paths to prevent directory traversal
- Use secure temporary file creation when needed

## Cross-Platform Compatibility

- Use `pathlib.Path` for cross-platform path handling
- Test on both Windows and Unix-like systems when possible
- Handle different line endings appropriately
- Use `shutil.which()` to find executables across platforms
- Consider WSL integration for Windows users needing Unix tools