# Contributing to Backpack

Thank you for your interest in contributing to Backpack! This document provides guidelines and instructions for contributing.

## Code of Conduct

- Be respectful and inclusive
- Welcome newcomers and help them learn
- Focus on constructive feedback
- Respect different viewpoints and experiences

## Getting Started

### Prerequisites

- Python 3.7 or higher
- pip
- Git

### Development Setup

1. **Fork and clone the repository:**
   ```bash
   git clone https://github.com/yourusername/backpack.git
   cd backpack
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Verify installation:**
   ```bash
   python backpack.py --help
   ```

## Development Workflow

### Branch Strategy

- `main`: Stable, production-ready code
- `develop`: Integration branch for features
- `feature/*`: New features
- `fix/*`: Bug fixes
- `docs/*`: Documentation updates

### Making Changes

1. **Create a feature branch:**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes:**
   - Write clear, readable code
   - Follow existing code style
   - Add docstrings to new functions/classes
   - Update documentation as needed

3. **Test your changes:**
   ```bash
   # Test the CLI
   python backpack.py --help
   python backpack.py key list
   
   # Test with example agent
   python backpack.py init --credentials "TEST_KEY" --personality "Test agent"
   python backpack.py run example_agent.py
   ```

4. **Commit your changes:**
   ```bash
   git add .
   git commit -m "Description of your changes"
   ```

5. **Push and create a pull request:**
   ```bash
   git push origin feature/your-feature-name
   ```

## Code Style

### Python Style Guide

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/)
- Use type hints where appropriate
- Maximum line length: 100 characters
- Use descriptive variable and function names

### Docstring Format

Use Google-style docstrings:

```python
def function_name(param1: str, param2: int) -> bool:
    """
    Brief description of the function.
    
    Args:
        param1: Description of param1
        param2: Description of param2
    
    Returns:
        Description of return value
    
    Raises:
        ExceptionType: When this exception is raised
    """
    pass
```

### Import Organization

1. Standard library imports
2. Third-party imports
3. Local application imports

Example:
```python
import os
import json
from typing import Dict, Optional

import click
from cryptography.fernet import Fernet

from .agent_lock import AgentLock
from .keychain import store_key
```

## Testing

### Manual Testing

Before submitting a pull request, test:

1. **Key management:**
   ```bash
   python backpack.py key add TEST_KEY
   python backpack.py key list
   python backpack.py key remove TEST_KEY
   ```

2. **Agent initialization:**
   ```bash
   python backpack.py init --credentials "KEY1,KEY2" --personality "Test"
   ```

3. **Agent execution:**
   ```bash
   python backpack.py run example_agent.py
   ```

4. **Error handling:**
   - Missing agent.lock file
   - Missing keys in keychain
   - Invalid master key
   - Corrupted agent.lock file

### Test Checklist

- [ ] All existing functionality works
- [ ] New features work as expected
- [ ] Error cases handled gracefully
- [ ] Documentation updated
- [ ] No linter errors
- [ ] Code follows style guide

## Documentation

### When to Update Documentation

- Adding new features
- Changing existing behavior
- Fixing bugs that affect usage
- Adding new CLI commands
- Changing architecture

### Documentation Files

- **README.md**: Overview, installation, quick start
- **USAGE.md**: Detailed usage guide with examples
- **ARCHITECTURE.md**: System design and architecture
- **SECURITY.md**: Security considerations
- **CONTRIBUTING.md**: This file
- **Docstrings**: Inline code documentation

## Pull Request Process

### Before Submitting

1. **Ensure your code works:**
   - Test all functionality
   - Check for linter errors
   - Verify documentation is updated

2. **Write a clear description:**
   - What changes were made
   - Why the changes were needed
   - How to test the changes

3. **Keep PRs focused:**
   - One feature or fix per PR
   - Keep changes small and reviewable
   - Split large changes into multiple PRs

### PR Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Refactoring
- [ ] Other (please describe)

## Testing
How was this tested?

## Checklist
- [ ] Code follows style guide
- [ ] Documentation updated
- [ ] Tests pass
- [ ] No breaking changes (or documented)
```

### Review Process

1. Maintainers will review your PR
2. Address any feedback or requested changes
3. Once approved, your PR will be merged
4. Thank you for contributing!

## Areas for Contribution

### High Priority

- [ ] Unit tests and test framework
- [ ] Key rotation utility
- [ ] Better error messages
- [ ] Windows-specific improvements
- [ ] Performance optimizations

### Medium Priority

- [ ] Additional encryption algorithms
- [ ] Cloud keychain integration
- [ ] Agent state management utilities
- [ ] CLI improvements (progress bars, colors)
- [ ] Configuration file support

### Low Priority

- [ ] GUI interface
- [ ] Web dashboard
- [ ] Plugin system
- [ ] Multi-language support

## Questions?

- Open an issue for bugs or feature requests
- Start a discussion for questions
- Check existing issues before creating new ones

## License

By contributing, you agree that your contributions will be licensed under the same license as the project.

Thank you for contributing to Backpack! 🎒
