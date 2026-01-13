# 🤝 Contributing to Allianza Blockchain

Thank you for your interest in contributing to Allianza Blockchain! We welcome contributions from the community.

---

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How to Contribute](#how-to-contribute)
- [Development Setup](#development-setup)
- [Code Style](#code-style)
- [Testing](#testing)
- [Pull Request Process](#pull-request-process)
- [Reporting Issues](#reporting-issues)
- [Feature Requests](#feature-requests)

---

## 📜 Code of Conduct

By participating in this project, you agree to:

- Be respectful and inclusive
- Accept constructive criticism gracefully
- Focus on what is best for the community
- Show empathy towards other community members

---

## 🚀 How to Contribute

### Reporting Bugs

1. Check if the bug has already been reported in [Issues](https://github.com/allianzatech/blockchainallianza/issues)
2. If not, create a new issue using the [Bug Report template](.github/ISSUE_TEMPLATE/bug_report.md)
3. Include:
   - Clear description of the bug
   - Steps to reproduce
   - Expected vs. actual behavior
   - Environment details

### Suggesting Features

1. Check if the feature has already been suggested
2. Create a new issue using the [Feature Request template](.github/ISSUE_TEMPLATE/feature_request.md)
3. Include:
   - Clear description of the feature
   - Use case and impact
   - Proposed solution
   - Alternatives considered

### Code Contributions

1. **Fork the repository**
2. **Create a feature branch:**
   ```bash
   git checkout -b feature/my-improvement
   ```
3. **Make your changes** (follow code style guidelines)
4. **Add tests** for new features
5. **Run tests** to ensure everything passes
6. **Commit your changes:**
   ```bash
   git commit -m "Add: description of your change"
   ```
7. **Push to your branch:**
   ```bash
   git push origin feature/my-improvement
   ```
8. **Open a Pull Request**

---

## 🛠️ Development Setup

### Prerequisites

- Python 3.10 or higher
- pip
- Git

### Setup Steps

1. **Clone your fork:**
   ```bash
   git clone https://github.com/YOUR_USERNAME/blockchainallianza.git
   cd blockchainallianza
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

4. **Configure environment:**
   ```bash
   cp .env.example .env
   # Edit .env with testnet keys (NEVER use mainnet keys)
   ```

5. **Run tests:**
   ```bash
   python -m pytest tests/
   ```

---

## 📝 Code Style

### Python

- Follow **PEP 8** style guide
- Use **type hints** where appropriate
- Maximum line length: **127 characters**
- Use **descriptive variable names**
- Add **docstrings** to functions and classes

### Example

```python
def create_commitment(
    source_chain: str,
    target_chain: str,
    amount: float,
    recipient: str
) -> Dict[str, Any]:
    """
    Create a cross-chain commitment.
    
    Args:
        source_chain: Source blockchain identifier
        target_chain: Target blockchain identifier
        amount: Transfer amount
        recipient: Recipient address
        
    Returns:
        Dictionary containing commitment details
    """
    # Implementation
    pass
```

### Commit Messages

Use clear, descriptive commit messages:

- **Format:** `Type: Description`
- **Types:** `Add`, `Fix`, `Update`, `Remove`, `Refactor`, `Docs`, `Test`
- **Example:** `Add: PQC signature verification`

---

## 🧪 Testing

### Running Tests

```bash
# All tests
python -m pytest tests/

# Specific test file
python -m pytest tests/test_interoperability.py

# With coverage
python -m pytest tests/ --cov=. --cov-report=html
```

### Writing Tests

- Write tests for all new features
- Aim for >80% code coverage
- Test both success and failure cases
- Use descriptive test names

### Example

```python
def test_create_commitment_success():
    """Test successful commitment creation."""
    result = create_commitment(
        source_chain="polygon",
        target_chain="ethereum",
        amount=0.1,
        recipient="0x..."
    )
    assert result["success"] is True
    assert "commitment_hash" in result
```

---

## 🔄 Pull Request Process

### Before Submitting

1. ✅ All tests pass
2. ✅ Code follows style guidelines
3. ✅ Documentation updated (if needed)
4. ✅ No sensitive data (keys, addresses with funds)
5. ✅ Commit messages are clear

### PR Checklist

- [ ] Code follows style guidelines
- [ ] Tests added/updated
- [ ] Documentation updated
- [ ] No sensitive data exposed
- [ ] Commit messages are clear
- [ ] PR description explains changes

### Review Process

1. Maintainers will review your PR
2. Address any feedback
3. Once approved, your PR will be merged
4. Thank you for contributing! 🎉

---

## 🐛 Reporting Issues

### Security Issues

**⚠️ IMPORTANT:** Do NOT report security vulnerabilities publicly.

- Email: **security@allianza.tech**
- See [SECURITY.md](.github/SECURITY.md) for details

### Bug Reports

Use the [Bug Report template](.github/ISSUE_TEMPLATE/bug_report.md) and include:

- Clear description
- Steps to reproduce
- Expected vs. actual behavior
- Environment details
- Screenshots (if applicable)

### Feature Requests

Use the [Feature Request template](.github/ISSUE_TEMPLATE/feature_request.md) and include:

- Clear description
- Use case
- Proposed solution
- Impact assessment

---

## 🔒 Security Guidelines

### ⚠️ Never Commit

- Private keys
- Wallet addresses with funds
- API keys or secrets
- Personal information
- Mainnet credentials

### ✅ Always Use

- Testnet keys for development
- Environment variables for secrets
- `.env` file (already in `.gitignore`)

---

## 📚 Documentation

### Code Documentation

- Add docstrings to all functions and classes
- Use type hints
- Include examples for complex functions

### README Updates

- Update README if adding new features
- Keep installation instructions current
- Update examples if API changes

---

## 🎯 Areas for Contribution

We welcome contributions in:

- 🐛 **Bug fixes**
- ✨ **New features**
- 📚 **Documentation improvements**
- 🧪 **Test coverage**
- 🎨 **UI/UX improvements**
- 🔒 **Security enhancements**
- ⚡ **Performance optimizations**

---

## ❓ Questions?

- **GitHub Issues:** [Open an issue](https://github.com/allianzatech/blockchainallianza/issues)
- **Email:** contact@allianza.tech

---

## 🙏 Thank You!

Thank you for contributing to Allianza Blockchain! Your contributions help make cross-chain interoperability more secure and accessible.

**Built with ❤️ by the Allianza Team and Contributors**
