# 🤝 Contributing to Allianza Blockchain

Thank you for your interest in contributing to Allianza Blockchain! This document provides guidelines and instructions for contributing.

---

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
- [Development Setup](#development-setup)
- [Pull Request Process](#pull-request-process)
- [Bounties](#bounties)
- [Coding Standards](#coding-standards)

---

## 📜 Code of Conduct

This project adheres to the [Contributor Covenant Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code.

---

## 💡 How Can I Contribute?

### **Reporting Bugs**

1. Check if the bug has already been reported in [Issues](https://github.com/dieisonmaach-lang/allianzablockchainpublic/issues)
2. If not, create a new issue with:
   - Clear title and description
   - Steps to reproduce
   - Expected vs actual behavior
   - Environment details (OS, Python version, etc.)

### **Suggesting Features**

1. Check existing [Issues](https://github.com/dieisonmaach-lang/allianzablockchainpublic/issues) and [Discussions](https://github.com/dieisonmaach-lang/allianzablockchainpublic/discussions)
2. Create a feature request issue with:
   - Clear description
   - Use case
   - Potential implementation approach

### **Submitting Code**

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests (`python tests/run_all_demos.py`)
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to your branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

---

## 🔧 Development Setup

### **Prerequisites**

- Python 3.8+
- Git
- (Optional) Node.js 14+ for SDK development

### **Installation**

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/allianzablockchainpublic.git
cd allianzablockchainpublic

# Install dependencies
pip install -r requirements.txt

# Run tests
python tests/run_all_demos.py
```

---

## 🔄 Pull Request Process

### **Before Submitting**

1. ✅ All tests pass (`python tests/run_all_demos.py`)
2. ✅ Code follows style guidelines
3. ✅ Documentation updated (if needed)
4. ✅ Commit messages are clear and descriptive

### **PR Checklist**

- [ ] Code is tested
- [ ] Documentation updated
- [ ] No breaking changes (or clearly documented)
- [ ] Follows existing code style
- [ ] CI checks pass

### **Review Process**

1. Maintainers will review your PR
2. Address any feedback
3. Once approved, your PR will be merged

---

## 💰 Bounties

We offer bounties for specific tasks! Check our [Bounty Issues](https://github.com/dieisonmaach-lang/allianzablockchainpublic/issues?q=is%3Aissue+label%3Abounty) for available opportunities.

### **How to Claim a Bounty**

1. Comment on the bounty issue expressing interest
2. Wait for maintainer approval
3. Complete the task
4. Submit PR with your solution
5. After merge, the bounty will be paid

### **Bounty Template**

When creating a bounty, use the template in `.github/ISSUE_TEMPLATE/bounty.md`

---

## 📝 Coding Standards

### **Python**

- Follow PEP 8 style guide
- Use type hints where appropriate
- Write docstrings for functions/classes
- Keep functions focused and small

### **JavaScript/TypeScript**

- Follow ESLint configuration
- Use TypeScript for SDK code
- Write JSDoc comments

### **Documentation**

- Use clear, concise language
- Include code examples
- Keep documentation up to date

---

## 🧪 Testing

### **Running Tests**

```bash
# Run all demos
python tests/run_all_demos.py

# Run with coverage
coverage run tests/run_all_demos.py
coverage report
```

### **Test Requirements**

- All tests must pass
- New features must include tests
- Maintain or improve coverage

---

## 📚 Documentation

### **Updating Documentation**

- Update relevant `.md` files
- Keep examples current
- Update API documentation if endpoints change

### **Documentation Structure**

- `README.md` - Main overview
- `docs/` - Technical documentation
- `examples/` - Code examples
- `proofs/` - Real-world proofs

---

## 🐛 Known Issues

For known issues and limitations, see [Issues](https://github.com/dieisonmaach-lang/allianzablockchainpublic/issues).

---

## 📞 Getting Help

- **Issues:** [GitHub Issues](https://github.com/dieisonmaach-lang/allianzablockchainpublic/issues)
- **Testnet:** https://testnet.allianza.tech
- **Developer Hub:** https://testnet.allianza.tech/developer-hub

---

## 🎯 Priority Areas

We're especially interested in contributions to:

1. **Test Coverage** - More comprehensive tests
2. **Documentation** - Clearer guides and examples
3. **SDK Improvements** - Better developer experience
4. **Examples** - More practical use cases
5. **Performance** - Optimizations and benchmarks

---

## ✅ Recognition

Contributors will be:

- Listed in `CONTRIBUTORS.md` (coming soon)
- Featured in release notes
- Eligible for bounties and rewards

---

**Thank you for contributing to Allianza Blockchain! 🚀**

