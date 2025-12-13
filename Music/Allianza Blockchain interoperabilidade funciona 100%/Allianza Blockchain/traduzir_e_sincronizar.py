#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🌐 Traduzir Documentação para Inglês e Sincronizar com GitHub Público
Traduz todos os arquivos .md e faz commit/push automático
"""

import os
import shutil
import subprocess
from pathlib import Path
from datetime import datetime

# Configuração
REPO_PRIVADO = Path(".")
REPO_PUBLICO = Path("../allianzablockchain-public")

# Arquivos principais para traduzir (manter nomes em inglês)
MAIN_FILES_TO_TRANSLATE = [
    "README.md",
    "CONTRIBUTING.md",
    "CODE_OF_CONDUCT.md",
    "CHANGELOG.md",
    "SECURITY_AUDIT.md",
    "examples/README.md",
    "tests/README.md",
]

def translate_readme():
    """Traduz README.md para inglês"""
    content = """# 🔐 Allianza Blockchain - Quantum-Safe Blockchain

[![npm version](https://img.shields.io/npm/v/allianza-qss-js)](https://www.npmjs.com/package/allianza-qss-js)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Testnet](https://img.shields.io/badge/Testnet-Active-green)](https://testnet.allianza.tech)
[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.0+-blue.svg)](https://www.typescriptlang.org/)
[![CI](https://github.com/allianzatoken-png/allianzablockchain/workflows/CI/badge.svg)](https://github.com/allianzatoken-png/allianzablockchain/actions)
[![Tests](https://img.shields.io/badge/Tests-Passing-brightgreen)](https://github.com/allianzatoken-png/allianzablockchain/actions)

## 🌟 About

Allianza Blockchain is a post-quantum blockchain with cross-chain interoperability and integrated quantum security.

> 🔬 **World's first blockchain** with triple redundancy signature system (QRS-3) and no-intermediary interoperability (ALZ-NIEV).

### ✨ Key Features

- 🔐 **Post-Quantum Security**: Protection against quantum computers
- 🌉 **Cross-Chain Interoperability**: Connects Bitcoin, Ethereum, Polygon and more
- 🚀 **Quantum Security Service (QSS)**: Public API for other blockchains
- ✅ **41 Technical Proofs**: Complete validation of all functionalities

## 🚀 Quick Start

### Install SDK

```bash
npm install allianza-qss-js
```

### Generate Quantum Proof

```javascript
import QSS from 'allianza-qss-js';

const proof = await QSS.generateProof('bitcoin', txHash);
console.log('Proof Hash:', proof.proof_hash);
```

## 📚 Documentation

- [API Reference](docs/API_REFERENCE.md)
- [Quick Start Guide](docs/QUICK_START.md)
- [QSS for Other Blockchains](GUIA_QSS_PARA_OUTRAS_BLOCKCHAINS.md)

## 🧪 Testnet

Access our public testnet: **https://testnet.allianza.tech**

- ✅ Faucet for testing
- ✅ Block explorer
- ✅ Functional QSS API
- ✅ 41 technical tests available

## 💻 Usage Examples

See practical examples of how to use Allianza technologies:

- 🔐 **QSS Demo** (`examples/qss_demo.py`) - How to use Quantum Security Service
- 🔐 **QRS-3 Demo** (`examples/qrs3_demo.py`) - Triple redundancy signature system
- 🌐 **ALZ-NIEV Demo** (`examples/alz_niev_demo.py`) - Cross-chain interoperability
- 🌉 **Interoperability Demo** (`examples/interoperability_demo.py`) - Practical use cases

### Run an Example

```bash
python examples/qss_demo.py
```

### Run All Tests

```bash
python tests/run_all_demos.py
```

This runs all demos and generates a complete report in `tests/demo_test_report_*.json`.

See [examples/README.md](examples/README.md) for more details.

## 📊 Technical Proofs

This repository contains the **41 technical proofs** that validate all Allianza Blockchain functionalities:

- ✅ ML-DSA signature generation and verification
- ✅ Cross-chain interoperability
- ✅ Quantum Security Service (QSS)
- ✅ Quantum proof validation
- ✅ And much more...

See complete results in: `proofs/PROVAS_TECNICAS_COMPLETAS_FINAL.json`

## 🔗 Useful Links

- **Testnet**: https://testnet.allianza.tech
- **npm SDK**: https://www.npmjs.com/package/allianza-qss-js
- **Developer Hub**: https://testnet.allianza.tech/developer-hub
- **Leaderboard**: https://testnet.allianza.tech/leaderboard

## 📦 Repository Structure

```
allianzablockchain/
├── docs/              # Technical documentation
├── proofs/            # 41 technical proofs
├── qss-sdk/          # JavaScript/TypeScript SDK
├── templates/        # Frontend templates
├── examples/          # Usage examples
│   ├── qss_demo.py              # QSS demonstration
│   ├── qrs3_demo.py             # QRS-3 demonstration
│   ├── alz_niev_demo.py         # ALZ-NIEV demonstration
│   ├── interoperability_demo.py # Practical examples
│   └── README.md                # Examples guide
└── tests/             # Tests and validation
    ├── run_all_demos.py         # Unified test runner
    └── README.md                # Test documentation
```

## 🤝 Contributing

Contributions are welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for more details.

## 📞 Communication

- **Issues:** Use GitHub Issues to report bugs and suggest features
- **Testnet:** https://testnet.allianza.tech
- **Developer Hub:** https://testnet.allianza.tech/developer-hub

## 📜 Code of Conduct

This project follows the [Contributor Covenant Code of Conduct](CODE_OF_CONDUCT.md).

## 📄 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) for details.

## ⚠️ Disclaimer

This repository contains only public code and documentation. The blockchain core and proprietary algorithms remain private.

---

**Developed with ❤️ by the Allianza Blockchain team**
"""
    
    readme_path = REPO_PUBLICO / "README.md"
    readme_path.parent.mkdir(parents=True, exist_ok=True)
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("✅ README.md translated to English")

def translate_contributing():
    """Traduz CONTRIBUTING.md para inglês"""
    content = """# Contributing to Allianza Blockchain

Thank you for considering contributing to Allianza Blockchain! 🎉

## 🚀 How to Contribute

### 1. Fork the Repository

1. Visit: https://github.com/allianzatoken-png/allianzablockchain
2. Click **"Fork"** (top right corner)
3. This will create a copy of the repository in your account

### 2. Clone Your Fork

```bash
git clone https://github.com/YOUR_USERNAME/allianzablockchain.git
cd allianzablockchain
```

### 3. Create a Branch

```bash
git checkout -b my-feature
```

**Naming convention:**
- `feature/feature-name` - New feature
- `fix/bug-name` - Bug fix
- `docs/doc-name` - Documentation improvements
- `test/test-name` - Add tests

### 4. Make Your Changes

- Write clean and well-documented code
- Follow project standards
- Add tests if possible
- Update documentation if necessary

### 5. Run Tests

**Before committing, always run:**

```bash
python tests/run_all_demos.py
```

**All tests must pass!** ✅

### 6. Commit Your Changes

```bash
git add .
git commit -m "feat: add Solana support"
```

**Commit convention:**
- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation
- `test:` - Tests
- `refactor:` - Refactoring
- `style:` - Formatting

### 7. Push to Your Fork

```bash
git push origin my-feature
```

### 8. Open a Pull Request

1. Visit: https://github.com/allianzatoken-png/allianzablockchain
2. Click **"Pull requests"**
3. Click **"New pull request"**
4. Select your branch
5. Fill out the PR template
6. Click **"Create pull request"**

---

## ✅ Pull Request Checklist

Before submitting, make sure:

- [ ] Code follows project standards
- [ ] Tests pass (`python tests/run_all_demos.py`)
- [ ] Documentation updated (if necessary)
- [ ] Commits follow convention
- [ ] Branch updated with `main`
- [ ] Clear description of what was done

---

## 🧪 Running Tests

### Test All Demos

```bash
python tests/run_all_demos.py
```

### Test a Specific Demo

```bash
python examples/qss_demo.py
python examples/qrs3_demo.py
python examples/alz_niev_demo.py
python examples/interoperability_demo.py
```

---

## 📝 Code Standards

### Python
- Use Python 3.8+
- Follow PEP 8
- Add docstrings
- Use type hints when possible

### TypeScript/JavaScript
- Use TypeScript when possible
- Follow ESLint
- Add JSDoc comments

---

## 🎯 Areas Needing Contributions

### High Priority
- ✅ Add support for more blockchains (Solana, Avalanche)
- ✅ Improve API documentation
- ✅ Add more test cases
- ✅ Create video tutorials

### Medium Priority
- ✅ Performance optimizations
- ✅ UI improvements in templates
- ✅ Translations (English/Spanish)
- ✅ Additional examples

### Low Priority
- ✅ Accessibility improvements
- ✅ Support for more languages
- ✅ Integrations with other tools

---

## 💰 Bounties

Some contributions may have associated bounties! See:
- Issues with `bounty` label
- Template: `.github/ISSUE_TEMPLATE/bounty.md`
- Gitcoin: https://gitcoin.co

---

## 📚 Resources

- **Documentation:** [docs/](docs/)
- **API Reference:** [docs/API_REFERENCE.md](docs/API_REFERENCE.md)
- **Quick Start:** [docs/QUICK_START.md](docs/QUICK_START.md)
- **Examples:** [examples/](examples/)

---

## ❓ Questions?

- Open an **Issue** on GitHub
- Contact via testnet: https://testnet.allianza.tech
- See complete documentation

---

## 📄 License

By contributing, you agree that your contributions will be licensed under the [MIT License](LICENSE).

---

**Thank you for contributing!** ❤️
"""
    
    contributing_path = REPO_PUBLICO / "CONTRIBUTING.md"
    with open(contributing_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("✅ CONTRIBUTING.md translated to English")

def translate_code_of_conduct():
    """Traduz CODE_OF_CONDUCT.md para inglês"""
    # CODE_OF_CONDUCT já está em inglês (Contributor Covenant)
    # Apenas verificar se existe
    coc_path = REPO_PUBLICO / "CODE_OF_CONDUCT.md"
    if coc_path.exists():
        print("✅ CODE_OF_CONDUCT.md already in English")
    else:
        # Copiar do repositório privado se necessário
        source = REPO_PRIVADO / "CODE_OF_CONDUCT.md"
        if source.exists():
            shutil.copy2(source, coc_path)
            print("✅ CODE_OF_CONDUCT.md copied")

def translate_examples_readme():
    """Traduz examples/README.md para inglês"""
    content = """# 📚 Usage Examples - Allianza Blockchain

This directory contains practical examples of how to use Allianza Blockchain technologies.

## 📋 Available Files

### 🔐 `qss_demo.py` - Quantum Security Service
Demonstrates how to use QSS to add quantum security to any blockchain.

**What you'll learn:**
- How to generate quantum proofs for transactions
- How to verify quantum proofs
- How to anchor proofs on different blockchains
- Practical use cases (exchanges, bridges, DeFi)

**How to run:**
```bash
python examples/qss_demo.py
```

---

### 🔐 `qrs3_demo.py` - Quantum Redundancy System (Triple)
Demonstrates the triple redundancy signature system QRS-3.

**What you'll learn:**
- How QRS-3 works (ECDSA + ML-DSA + SPHINCS+)
- Adaptive signing based on transaction value
- Intelligent fallback to QRS-2
- Advantages of triple redundancy

**How to run:**
```bash
python examples/qrs3_demo.py
```

---

### 🌐 `alz_niev_demo.py` - Cross-Chain Interoperability
Demonstrates the ALZ-NIEV system with its 5 layers of interoperability.

**What you'll learn:**
- ELNI: Native execution without transferring assets
- ZKEF: Zero-Knowledge proofs
- UP-NMT: Universal proof normalization
- MCL: Multi-consensus support
- AES: Atomic execution with rollback

**How to run:**
```bash
python examples/alz_niev_demo.py
```

---

### 🌉 `interoperability_demo.py` - Practical Examples
Demonstrates real-world use cases of cross-chain interoperability.

**What you'll learn:**
- Bitcoin ↔ Ethereum transfers
- Multi-chain DEX
- Cross-chain oracles
- Quantum-safe bridges
- Supported blockchains

**How to run:**
```bash
python examples/interoperability_demo.py
```

---

## 🚀 Quick Start

### Prerequisites

```bash
pip install requests
```

### Run All Examples

```bash
# Windows
python examples\\qss_demo.py
python examples\\qrs3_demo.py
python examples\\alz_niev_demo.py
python examples\\interoperability_demo.py

# Linux/Mac
python examples/qss_demo.py
python examples/qrs3_demo.py
python examples/alz_niev_demo.py
python examples/interoperability_demo.py
```

---

## 📖 Complete Documentation

For more information, see:

- [API Reference](../docs/API_REFERENCE.md)
- [Quick Start Guide](../docs/QUICK_START.md)
- [QSS for Other Blockchains](../GUIA_QSS_PARA_OUTRAS_BLOCKCHAINS.md)
- [Whitepaper](../WHITEPAPER_ALLIANZA_BLOCKCHAIN.md)

---

## 🔗 Useful Links

- **Testnet**: https://testnet.allianza.tech
- **Developer Hub**: https://testnet.allianza.tech/developer-hub
- **npm SDK**: https://www.npmjs.com/package/allianza-qss-js
- **QSS API**: https://testnet.allianza.tech/api/qss

---

## ⚠️ Important Note

These examples are **educational demonstrations** that show:
- ✅ How to use the technologies
- ✅ Structure and concepts
- ✅ Integration with other blockchains
- ❌ **DO NOT** expose the complete core code

The complete core code (ALZ-NIEV, QRS-3, QSS) remains private and protected.

---

**Developed with ❤️ by the Allianza Blockchain team**
"""
    
    examples_readme_path = REPO_PUBLICO / "examples" / "README.md"
    examples_readme_path.parent.mkdir(parents=True, exist_ok=True)
    with open(examples_readme_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("✅ examples/README.md translated to English")

def translate_tests_readme():
    """Traduz tests/README.md para inglês"""
    content = """# 🧪 Tests - Allianza Blockchain

This directory contains test scripts and validation for the public repository.

## 📋 Files

### `run_all_demos.py` - Unified Test Runner

Runs all demos in `examples/` and generates a complete report.

**Usage:**
```bash
python tests/run_all_demos.py
```

**Output:**
- JSON Report: `tests/demo_test_report_YYYYMMDD_HHMMSS.json`
- Text Summary: `tests/demo_test_summary_YYYYMMDD_HHMMSS.txt`

**What it tests:**
- ✅ `examples/qss_demo.py` - Quantum Security Service
- ✅ `examples/qrs3_demo.py` - Quantum Redundancy System
- ✅ `examples/alz_niev_demo.py` - ALZ-NIEV Interoperability
- ✅ `examples/interoperability_demo.py` - Practical examples

**Example Report:**
```json
{
  "test_suite": "Allianza Blockchain - Demo Tests",
  "summary": {
    "total_demos": 4,
    "successful": 4,
    "failed": 0,
    "success_rate": 100.0,
    "total_execution_time_ms": 1234.56
  },
  "results": [...]
}
```

## 🎯 Use Cases

### For Developers
- Validate that all examples work
- Check compatibility after changes
- Prepare for contributions

### For Audits
- End-to-end functionality proof
- Structured reports for analysis
- Validation of all technologies

### For CI/CD
- Continuous integration (future)
- Automatic PR validation
- Quality reports

## 📊 Metrics

The test runner provides:
- ✅ Success rate
- ⏱️ Execution time
- 📝 Complete output from each demo
- ❌ Detailed errors (if any)

## 🔗 Related Links

- [Examples](../examples/README.md)
- [Documentation](../docs/API_REFERENCE.md)
- [Testnet](https://testnet.allianza.tech)

---

**Last updated:** 2025-12-05
"""
    
    tests_readme_path = REPO_PUBLICO / "tests" / "README.md"
    tests_readme_path.parent.mkdir(parents=True, exist_ok=True)
    with open(tests_readme_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("✅ tests/README.md translated to English")

def git_commit_and_push():
    """Faz commit e push automático"""
    print()
    print("=" * 70)
    print("📤 COMMITTING AND PUSHING TO GITHUB")
    print("=" * 70)
    print()
    
    os.chdir(REPO_PUBLICO)
    
    try:
        # Verificar se há mudanças
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            capture_output=True,
            text=True,
            check=True
        )
        
        if not result.stdout.strip():
            print("ℹ️  No changes to commit")
            return True
        
        # Adicionar todos os arquivos
        subprocess.run(["git", "add", "."], check=True)
        print("✅ Files added to staging")
        
        # Commit
        commit_message = f"docs: translate all documentation to English - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        subprocess.run(
            ["git", "commit", "-m", commit_message],
            check=True
        )
        print(f"✅ Commit created: {commit_message}")
        
        # Push
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("✅ Push successful!")
        print()
        print("🔗 Repository: https://github.com/allianzatoken-png/allianzablockchain")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Git error: {e}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    finally:
        os.chdir(REPO_PRIVADO)

def main():
    """Função principal"""
    print("=" * 70)
    print("🌐 TRANSLATING DOCUMENTATION TO ENGLISH AND SYNCING")
    print("=" * 70)
    print()
    
    if not REPO_PUBLICO.exists():
        print(f"❌ Public repository not found: {REPO_PUBLICO}")
        return
    
    print(f"📁 Public repository: {REPO_PUBLICO.absolute()}")
    print()
    
    # Traduzir arquivos principais
    print("🔄 Translating main documentation files...")
    translate_readme()
    translate_contributing()
    translate_code_of_conduct()
    translate_examples_readme()
    translate_tests_readme()
    
    print()
    print("=" * 70)
    print("✅ TRANSLATION COMPLETE!")
    print("=" * 70)
    
    # Fazer commit e push automaticamente
    print("\n📤 Committing and pushing automatically...")
    git_commit_and_push()
    
    print()
    print("=" * 70)
    print("✅ PROCESS COMPLETE!")
    print("=" * 70)

if __name__ == "__main__":
    main()

