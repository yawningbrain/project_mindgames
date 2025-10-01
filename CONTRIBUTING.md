# Contributing to Emotiv LSL

Thank you for your interest in contributing to Emotiv LSL! This document provides guidelines and instructions for contributing.

## Code of Conduct

By participating in this project, you agree to maintain a respectful and inclusive environment for all contributors.

## How to Contribute

### Reporting Bugs

If you find a bug, please create an issue with:

1. **Clear title and description**
2. **Steps to reproduce** the issue
3. **Expected behavior** vs **actual behavior**
4. **Environment details**:
   - OS and version
   - Python version
   - emotiv-lsl version
   - Headset model

### Suggesting Enhancements

Enhancement suggestions are welcome! Please create an issue with:

1. **Clear description** of the enhancement
2. **Use case** - why is this useful?
3. **Possible implementation** (if you have ideas)

### Pull Requests

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Make your changes**
4. **Follow the coding standards** (see below)
5. **Test your changes**
6. **Commit with clear messages**: `git commit -m 'Add amazing feature'`
7. **Push to your fork**: `git push origin feature/amazing-feature`
8. **Open a Pull Request**

## Development Setup

```bash
# Clone your fork
git clone https://github.com/your-username/emotiv-lsl.git
cd emotiv-lsl

# Add upstream remote
git remote add upstream https://github.com/original-repo/emotiv-lsl.git

# Install in development mode with all dependencies
pip install -e ".[dev]"
```

## Coding Standards

### Python Style

- Follow [PEP 8](https://pep8.org/) style guide
- Use [Black](https://black.readthedocs.io/) for code formatting
- Maximum line length: 88 characters (Black default)
- Use type hints where appropriate

### Code Formatting

```bash
# Format code with Black
black .

# Check with flake8
flake8 emotiv_lsl/

# Type checking with mypy
mypy emotiv_lsl/
```

### Documentation

- Add docstrings to all public functions, classes, and modules
- Use Google-style docstrings:

```python
def function_name(param1: str, param2: int) -> bool:
    """
    Brief description of the function.
    
    Longer description if needed.
    
    Args:
        param1: Description of param1
        param2: Description of param2
        
    Returns:
        Description of return value
        
    Raises:
        ValueError: When something goes wrong
    """
    pass
```

### Commit Messages

Follow conventional commits format:

```
type(scope): subject

body (optional)

footer (optional)
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Formatting changes
- `refactor`: Code refactoring
- `test`: Adding tests
- `chore`: Maintenance tasks

Examples:
```
feat(epoc_x): add support for EPOC+ headset
fix(logging): resolve file handler permission issue
docs(readme): update installation instructions
```

## Testing

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=emotiv_lsl --cov-report=html

# Run specific test file
pytest tests/test_emotiv_base.py
```

### Writing Tests

- Place tests in `tests/` directory
- Name test files: `test_*.py`
- Name test functions: `test_*`
- Use pytest fixtures for setup/teardown

Example:
```python
import pytest
from emotiv_lsl import EmotivEpocX

def test_epoc_x_initialization():
    """Test that EmotivEpocX initializes correctly."""
    epoc = EmotivEpocX()
    assert epoc is not None
    assert epoc.READ_SIZE == 32
```

## Project Structure

When adding new features, follow this structure:

```
emotiv-lsl/
├── emotiv_lsl/          # Main package
│   ├── __init__.py      # Package initialization
│   ├── emotiv_base.py   # Base classes
│   ├── devices/         # Device implementations
│   └── utils/           # Utility functions
├── examples/            # Usage examples
├── tests/              # Test files
├── docs/               # Documentation
└── scripts/            # Utility scripts
```

## Adding Support for New Devices

To add support for a new Emotiv device:

1. Create a new class inheriting from `EmotivBase`
2. Implement required methods:
   - `get_hid_device()`
   - `get_stream_info()`
   - `decode_data()`
   - `validate_data()`
3. Add device-specific configuration
4. Update documentation
5. Add example usage

## Documentation

### Building Documentation

```bash
# Install documentation dependencies
pip install -e ".[docs]"

# Build documentation
cd docs/
make html

# View documentation
open _build/html/index.html
```

### Documentation Standards

- Keep README.md up to date
- Add examples for new features
- Update API documentation
- Include troubleshooting tips

## Release Process

1. Update version in `setup.py` and `__init__.py`
2. Update `CHANGELOG.md`
3. Create release branch: `git checkout -b release/v1.x.x`
4. Tag release: `git tag -a v1.x.x -m "Release version 1.x.x"`
5. Push tags: `git push --tags`

## Questions?

Feel free to:
- Open an issue for questions
- Start a discussion in GitHub Discussions
- Reach out to maintainers

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to Emotiv LSL! 🎉

