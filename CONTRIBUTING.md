# Contributing to Allianza Blockchain

Thank you for your interest in contributing to Allianza Blockchain! We welcome contributions from the community.

## 🤝 How to Contribute

### Reporting Issues

If you find a bug or have a suggestion, please open an issue on GitHub:

1. Check if the issue already exists
2. Use a clear and descriptive title
3. Provide detailed information about the issue
4. Include steps to reproduce (for bugs)
5. Add relevant labels if applicable

### Security Issues

**Please do NOT open public issues for security vulnerabilities.**

Instead, report security issues privately:
- **Email:** security@allianza.tech
- **Subject:** `[SECURITY] Brief description`
- See [SECURITY.md](./SECURITY.md) for more details

### Code Contributions

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Make your changes**
   - Follow the code style guidelines
   - Add tests for new features
   - Update documentation as needed
4. **Commit your changes**
   ```bash
   git commit -m "Add: Description of your changes"
   ```
5. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```
6. **Open a Pull Request**
   - Provide a clear description
   - Reference related issues
   - Wait for review and feedback

## 📝 Code Style Guidelines

### Python Code Style

- Follow PEP 8 style guide
- Use type hints where appropriate
- Write docstrings for functions and classes
- Keep functions focused and small
- Use meaningful variable names

### Example

```python
def create_transfer(
    source_chain: str,
    target_chain: str,
    amount: int,
    recipient_address: str
) -> dict:
    """
    Create a cross-chain transfer using ALZ-NIEV protocol.
    
    Args:
        source_chain: Source blockchain identifier
        target_chain: Target blockchain identifier
        amount: Transfer amount in smallest unit
        recipient_address: Recipient address on target chain
        
    Returns:
        Dictionary containing transfer details and UChainID
    """
    # Implementation here
    pass
```

## 🧪 Testing

### Running Tests

```bash
# Run all tests
python -m pytest tests/

# Run specific test file
python -m pytest tests/test_specific.py

# Run with coverage
python -m pytest tests/ --cov=core
```

### Writing Tests

- Write tests for new features
- Ensure tests are deterministic
- Use descriptive test names
- Test edge cases and error conditions

## 📚 Documentation

### Code Documentation

- Add docstrings to all public functions and classes
- Use clear, concise descriptions
- Include parameter and return type information
- Add usage examples where helpful

### Documentation Updates

- Update relevant documentation when adding features
- Keep examples up to date
- Update README if adding major features
- Add to docs/ directory for technical documentation

## 🎯 Areas for Contribution

### High Priority

- **Documentation improvements** - Better examples, tutorials, guides
- **Test coverage** - More comprehensive test suite
- **Performance optimizations** - Improve speed and efficiency
- **Error handling** - Better error messages and handling

### Medium Priority

- **Additional blockchain support** - Add support for more chains
- **UI/UX improvements** - Better user interfaces
- **Developer tools** - CLI improvements, debugging tools
- **Examples** - More code examples and tutorials

### Low Priority

- **Code refactoring** - Clean up and improve code structure
- **Translation** - Translate documentation to other languages
- **Design improvements** - UI/UX enhancements

## 🔍 Pull Request Process

1. **Ensure your code follows style guidelines**
2. **Add tests for new features**
3. **Update documentation**
4. **Ensure all tests pass**
5. **Write a clear PR description**
6. **Wait for review and address feedback**

### PR Description Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Performance improvement
- [ ] Code refactoring

## Testing
How was this tested?

## Related Issues
Closes #issue_number
```

## 📋 Commit Message Guidelines

Use clear, descriptive commit messages:

- **Format:** `Type: Brief description`
- **Types:** `Add`, `Fix`, `Update`, `Remove`, `Refactor`, `Docs`
- **Examples:**
  - `Add: Support for Avalanche chain`
  - `Fix: UChainID generation for Solana addresses`
  - `Update: Documentation for ALZ-NIEV protocol`

## 🚫 What NOT to Contribute

Please do NOT contribute:

- **Commercial code** - Production bridge, testnet infrastructure
- **Deployment configs** - Production deployment files
- **Sensitive data** - API keys, private keys, credentials
- **Breaking changes** - Without discussion first

## ❓ Questions?

If you have questions about contributing:

- Open a discussion on GitHub
- Email: info@allianza.tech
- Check existing issues and discussions

## 🙏 Thank You!

We appreciate all contributions, big and small. Thank you for helping make Allianza Blockchain better!

---

**Note:** By contributing, you agree that your contributions will be licensed under the MIT License.

