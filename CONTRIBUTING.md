# 🤝 Contributing to Allianza Blockchain

Thank you for your interest in contributing to Allianza Blockchain! This document provides guidelines and instructions for contributing to the project.

---

## 📋 Table of Contents

- [Code of Conduct](#-code-of-conduct)
- [Getting Started](#-getting-started)
- [Development Workflow](#-development-workflow)
- [Coding Standards](#-coding-standards)
- [Testing](#-testing)
- [Documentation](#-documentation)
- [Pull Request Process](#-pull-request-process)
- [Issue Reporting](#-issue-reporting)

---

## 📜 Code of Conduct

By participating in this project, you agree to:

- Be respectful and inclusive
- Welcome newcomers and help them learn
- Focus on constructive feedback
- Respect different viewpoints and experiences

---

## 🚀 Getting Started

### 1. Fork and Clone

```bash
# Fork the repository on GitHub
# Then clone your fork
git clone https://github.com/YOUR_USERNAME/blockchainallianza.git
cd blockchainallianza
```

### 2. Set Up Development Environment

```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Install development dependencies (if any)
pip install pytest pytest-cov black flake8 mypy
```

### 3. Create a Branch

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/your-bug-fix
```

---

## 🔄 Development Workflow

### Branch Naming Convention

- `feature/` - New features
- `fix/` - Bug fixes
- `docs/` - Documentation updates
- `refactor/` - Code refactoring
- `test/` - Test additions/updates
- `chore/` - Maintenance tasks

### Commit Messages

Follow [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `style`: Code style (formatting)
- `refactor`: Code refactoring
- `test`: Tests
- `chore`: Maintenance

**Examples:**
```
feat(interop): add Solana cross-chain support
fix(security): prevent path traversal in file downloads
docs(readme): update installation instructions
```

---

## 💻 Coding Standards

### Python Style Guide

- Follow **PEP 8** style guide
- Use **type hints** for function parameters and return values
- Maximum line length: **100 characters** (soft limit)
- Use **4 spaces** for indentation (no tabs)

### Code Formatting

We use **Black** for code formatting:

```bash
# Format code
black .

# Check formatting
black --check .
```

### Linting

We use **flake8** for linting:

```bash
# Run linter
flake8 .

# With configuration
flake8 . --max-line-length=100 --extend-ignore=E203
```

### Type Checking

We use **mypy** for type checking:

```bash
# Type check
mypy .
```

### Example Code Structure

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module description here.
"""

from typing import Dict, Optional, List
import logging

logger = logging.getLogger(__name__)


class ExampleClass:
    """
    Class description.
    
    Args:
        param1: Description of param1
        param2: Description of param2
    """
    
    def __init__(self, param1: str, param2: Optional[int] = None):
        """Initialize the class."""
        self.param1 = param1
        self.param2 = param2
    
    def example_method(self, value: str) -> Dict[str, str]:
        """
        Method description.
        
        Args:
            value: Input value
            
        Returns:
            Dictionary with results
            
        Raises:
            ValueError: If value is invalid
        """
        if not value:
            raise ValueError("Value cannot be empty")
        
        return {"result": value}
```

---

## 🧪 Testing

### Running Tests

```bash
# Run all tests
python -m pytest tests/

# Run specific test file
python -m pytest tests/test_interoperability.py

# Run with coverage
python -m pytest tests/ --cov=. --cov-report=html

# Run professional test suite
python testnet_professional_test_suite.py

# Run critical tests
python critical_tests_suite.py
```

### Writing Tests

- Write tests for all new features
- Aim for **>80% code coverage**
- Use descriptive test names
- Test both success and failure cases
- Mock external dependencies

**Example:**
```python
import pytest
from unittest.mock import Mock, patch
from my_module import MyClass

def test_example_success():
    """Test successful execution."""
    obj = MyClass("test")
    result = obj.example_method("value")
    assert result["result"] == "value"

def test_example_failure():
    """Test failure case."""
    obj = MyClass("test")
    with pytest.raises(ValueError):
        obj.example_method("")
```

---

## 📚 Documentation

### Code Documentation

- Add **docstrings** to all functions and classes
- Use **Google-style** docstrings
- Document parameters, return values, and exceptions
- Include usage examples for complex functions

### Documentation Updates

When adding new features:
1. Update relevant documentation in `docs/`
2. Update README.md if needed
3. Add examples if applicable
4. Update API documentation

---

## 🔀 Pull Request Process

### Before Submitting

1. ✅ **Update tests** - Ensure all tests pass
2. ✅ **Update documentation** - Update relevant docs
3. ✅ **Run linters** - Fix any linting issues
4. ✅ **Check formatting** - Run Black formatter
5. ✅ **Test locally** - Verify everything works

### PR Checklist

- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Comments added for complex code
- [ ] Documentation updated
- [ ] Tests added/updated
- [ ] All tests pass
- [ ] No merge conflicts
- [ ] Branch is up to date with main

### PR Description Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
How was this tested?

## Checklist
- [ ] Tests pass
- [ ] Documentation updated
- [ ] Code follows style guide
```

---

## 🐛 Issue Reporting

### Before Creating an Issue

1. Search existing issues to avoid duplicates
2. Check if it's already fixed in the latest version
3. Gather relevant information

### Issue Template

**Bug Report:**
```markdown
**Describe the bug**
Clear description of the bug

**To Reproduce**
Steps to reproduce:
1. ...
2. ...

**Expected behavior**
What you expected to happen

**Environment:**
- OS: [e.g., Windows 10]
- Python version: [e.g., 3.10]
- Version: [e.g., 1.0.0]

**Additional context**
Any other relevant information
```

**Feature Request:**
```markdown
**Is your feature request related to a problem?**
Clear description of the problem

**Describe the solution you'd like**
What you want to happen

**Describe alternatives considered**
Other solutions you've considered

**Additional context**
Any other relevant information
```

---

## 🎯 Areas for Contribution

We welcome contributions in:

- **🐛 Bug Fixes** - Fix reported issues
- **✨ New Features** - Add new functionality
- **📚 Documentation** - Improve docs
- **🧪 Tests** - Add test coverage
- **🔒 Security** - Security improvements
- **⚡ Performance** - Performance optimizations
- **🌐 Translations** - i18n support

---

## 📞 Getting Help

- **GitHub Issues** - For bug reports and feature requests
- **Discussions** - For questions and discussions
- **Documentation** - Check `docs/` folder

---

## 🙏 Thank You!

Your contributions make Allianza Blockchain better for everyone. Thank you for taking the time to contribute!

---

**Questions?** Open an issue or start a discussion on GitHub.

