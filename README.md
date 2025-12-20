# 🌐 Allianza Blockchain

<div align="center">

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.10+-green.svg)
![Flask](https://img.shields.io/badge/flask-2.3.3-blue.svg)
![Status](https://img.shields.io/badge/status-testnet-orange.svg)

**Quantum-Safe, Bridge-Free Cross-Chain Interoperability Platform**

[Live Demo](https://testnet.allianza.tech) • [Documentation](#-documentation) • [Security](#-security) • [Contributing](#-contributing)

</div>

---

## 🎯 Overview

**Allianza Blockchain** is a production-grade, quantum-safe interoperability platform that enables **real cross-chain transfers** between completely different blockchains (Bitcoin, Ethereum, Polygon, Solana) **without bridges, custody, or wrapped tokens**.

### 🌟 Key Innovations

- **🔐 Quantum-Safe Security** - Post-quantum cryptography (NIST PQC standards: ML-DSA, ML-KEM, SPHINCS+)
- **🌉 Bridge-Free Interoperability** - Direct transfers without custodial bridges or wrapped tokens
- **🔒 Zero-Knowledge Proofs** - Every cross-chain state transition is cryptographically verified
- **🆔 UChainID** - Universal Chain ID for on-chain traceability of cross-chain transfers
- **⚡ Real Cross-Chain Transfers** - Live Polygon → Bitcoin testnet transfers with on-chain verification

---

## 🚀 Live Demo

**Testnet Dashboard:** [https://testnet.allianza.tech](https://testnet.allianza.tech)

### Example Real Transaction

**Polygon → Bitcoin Testnet Transfer:**
- **Bitcoin Testnet TX:** [`2b010250667459e2bc30fd4a33f9caab937310156839c87364a5ba075594e554`](https://live.blockcypher.com/btc-testnet/tx/2b010250667459e2bc30fd4a33f9caab937310156839c87364a5ba075594e554/)
- **UChainID:** `UCHAIN-...` (visible in testnet dashboard)
- **ZK Proof:** Verifiable via embedded proof verifier

---

## ✨ Features

### 🔐 Quantum-Safe Cryptography
- **NIST PQC Standards:** ML-DSA (signatures), ML-KEM (key exchange), SPHINCS+ (hash-based)
- **QRS-3 (Triple Redundancy):** Three independent PQC signatures for maximum security
- **Quantum Attack Resistance:** Protection against Shor's and Grover's algorithms
- **Cryptographic Agility:** Easy migration to new PQC standards

### 🌉 Bridge-Free Interoperability (ALZ-NIEV)
- **No Custody:** No locked funds in bridge contracts
- **No Wrapped Tokens:** Direct native token transfers
- **No Intermediaries:** Peer-to-peer cross-chain execution
- **UChainID System:** Global identifier for cross-chain transfers
- **ZK Proofs:** Cryptographic verification of state transitions

### 🔗 Supported Blockchains
- ✅ **Bitcoin** (Testnet/Mainnet)
- ✅ **Ethereum** (Testnet/Mainnet)
- ✅ **Polygon** (Testnet/Mainnet)
- ✅ **Solana** (Testnet/Mainnet)
- ✅ **BSC** (Binance Smart Chain)
- ✅ **Allianza Native Chain**

### 🛡️ Security Features
- **CSRF Protection** - Applied to all critical routes
- **Rate Limiting** - Global protection against DDoS
- **Input Validation** - Comprehensive sanitization
- **Security Headers** - CSP, COEP, COOP
- **Audit Logging** - Complete transaction traceability
- **Path Traversal Protection** - Secure file handling

---

## 📋 Table of Contents

- [Quick Start](#-quick-start)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Usage](#-usage)
- [Architecture](#-architecture)
- [Security](#-security)
- [Documentation](#-documentation)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🚀 Quick Start

### Prerequisites

- **Python 3.10+**
- **pip** and **virtualenv** (recommended)
- **Node.js** (optional, for rebuilding Tailwind/JS assets)

### Installation

```bash
# Clone the repository
git clone https://github.com/allianzatech/blockchainallianza.git
cd blockchainallianza

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

### Configuration

Create a `.env` file in the project root:

```bash
# Flask Configuration
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=your-secret-key-here  # Generate with: python -c "import secrets; print(secrets.token_hex(32))"

# Blockchain APIs (Testnet)
BLOCKCYPHER_API_TOKEN=your_blockcypher_token
BITCOIN_PRIVATE_KEY=your_bitcoin_testnet_wif
BITCOIN_TESTNET_ADDRESS=your_bitcoin_testnet_address

# EVM Chains (Testnet)
POLYGON_PRIVATE_KEY=your_polygon_private_key
ETH_PRIVATE_KEY=your_ethereum_private_key
POLYGON_RPC_URL=https://polygon-mumbai.g.alchemy.com/v2/YOUR_KEY
ETH_RPC_URL=https://eth-sepolia.g.alchemy.com/v2/YOUR_KEY

# Solana (Testnet)
SOLANA_PRIVATE_KEY=your_solana_private_key
SOLANA_RPC_URL=https://api.testnet.solana.com
```

> ⚠️ **Important:** Never commit real mainnet keys. Only use **testnet** keys for development.

### Run Locally

**Development Mode:**
```bash
python allianza_blockchain.py
```

**Production Mode (Gunicorn):**
```bash
gunicorn -w 2 -b 0.0.0.0:5000 --timeout 300 --keep-alive 5 --preload wsgi_optimized:application
```

Then open: `http://localhost:5000/interoperability`

---

## 🏗️ Architecture

### Core Components

```
┌─────────────────────────────────────────────────────────────┐
│                    Allianza Blockchain                       │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │  Quantum     │  │  ALZ-NIEV    │  │  UChainID    │     │
│  │  Security    │  │  Interop     │  │  System      │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
│                                                               │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │  ZK Proofs  │  │  Cross-Chain │  │  State       │     │
│  │  System     │  │  Bridge      │  │  Machine     │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

### Technology Stack

- **Backend:** Python 3.10+, Flask 2.3.3
- **Blockchain:** Web3.py, bitcoinlib, python-bitcointx, solana-py
- **Cryptography:** liboqs-python (NIST PQC), cryptography
- **Database:** SQLite (development), PostgreSQL-ready
- **Frontend:** HTML5, Tailwind CSS, JavaScript
- **Deployment:** Gunicorn, Render.com

---

## 🔒 Security

### Security Audit

A comprehensive security audit has been performed. See:
- **[Security Audit Report](docs/SECURITY_AUDIT_REPORT.md)** - Full vulnerability analysis
- **[Security Improvements Summary](docs/SECURITY_IMPROVEMENTS_SUMMARY.md)** - Applied fixes
- **[Dependency Vulnerabilities Report](docs/DEPENDENCY_VULNERABILITIES_REPORT.md)** - Dependency security status

### Security Features Implemented

✅ **Path Traversal Protection** - Secure file download validation  
✅ **CSRF Protection** - Applied to all critical POST routes  
✅ **Rate Limiting** - Global DDoS protection  
✅ **Input Validation** - Comprehensive sanitization  
✅ **Security Headers** - CSP, COEP, COOP  
✅ **SECRET_KEY Validation** - Production environment checks  
✅ **Audit Logging** - Complete transaction traceability  

### Dependency Security

Run security checks:
```bash
python scripts/check_dependencies_security.py
```

Or directly:
```bash
pip-audit
```

---

## 📚 Documentation

### Core Documentation

- **[Security Audit Report](docs/SECURITY_AUDIT_REPORT.md)** - Complete security analysis
- **[Dependency Vulnerabilities](docs/DEPENDENCY_VULNERABILITIES_REPORT.md)** - Dependency security status
- **[Quantum Attack Analysis](docs/QUANTUM_ATTACK_ANALYSIS.md)** - Quantum security methodology

### API Documentation

- **Testnet Dashboard:** [https://testnet.allianza.tech](https://testnet.allianza.tech)
- **API Endpoints:** Available in testnet dashboard
- **ZK Proof Verifier:** `/verify-proof` endpoint

### Technical Proofs

- **Complete Technical Proofs:** `COMPLETE_TECHNICAL_PROOFS_FINAL_EN.json`
- **On-Chain Proofs:** `proofs/on_chain/`
- **Interoperability Proofs:** `proofs/interoperability/`

---

## 🧪 Testing

### Run Test Suite

```bash
# Complete validation suite
python complete_validation_suite.py

# Professional tests
python testnet_professional_test_suite.py

# Critical tests
python critical_tests_suite.py
```

### Test Coverage

- ✅ Cross-chain interoperability
- ✅ Quantum-safe cryptography
- ✅ ZK proof generation and verification
- ✅ UChainID system
- ✅ Security features
- ✅ Rate limiting
- ✅ Input validation

---

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. **Fork the repository**
2. **Create a feature branch:** `git checkout -b feature/my-improvement`
3. **Make your changes** (follow code style guidelines)
4. **Add tests** for new features
5. **Commit your changes:** `git commit -m "Add my improvement"`
6. **Push to your branch:** `git push origin feature/my-improvement`
7. **Open a Pull Request**

### Code Style

- Follow PEP 8 for Python code
- Use type hints where appropriate
- Add docstrings to functions and classes
- Write tests for new features

### Reporting Issues

If you find a bug or have a suggestion, please open an issue on GitHub with:
- Clear description of the problem
- Steps to reproduce (if applicable)
- Expected vs. actual behavior
- Environment details (Python version, OS, etc.)

---

## 📊 Project Status

### ✅ Completed Features

- [x] Quantum-safe cryptography (NIST PQC standards)
- [x] Bridge-free cross-chain interoperability
- [x] UChainID system
- [x] ZK proof generation and verification
- [x] Real cross-chain transfers (Polygon → Bitcoin)
- [x] Testnet dashboard
- [x] Security audit and fixes
- [x] Comprehensive test suite

### 🚧 In Progress

- [ ] Mainnet deployment
- [ ] Additional blockchain support
- [ ] Performance optimizations
- [ ] Enhanced documentation

### 📅 Planned

- [ ] Mobile SDK
- [ ] Browser extension
- [ ] Advanced analytics dashboard
- [ ] Governance system

---

## 🔗 Links

- **Live Testnet:** [https://testnet.allianza.tech](https://testnet.allianza.tech)
- **GitHub Repository:** [https://github.com/allianzatech/blockchainallianza](https://github.com/allianzatech/blockchainallianza)
- **Documentation:** See [Documentation](#-documentation) section above

---

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **NIST** for Post-Quantum Cryptography standards
- **liboqs** for quantum-safe cryptography library
- **Open Source Community** for various blockchain libraries

---

## 📧 Contact

For questions, suggestions, or collaboration opportunities:
- **GitHub Issues:** [Open an issue](https://github.com/allianzatech/blockchainallianza/issues)
- **Testnet:** [https://testnet.allianza.tech](https://testnet.allianza.tech)

---

<div align="center">

**Built with ❤️ by the Allianza Team**

[⭐ Star us on GitHub](https://github.com/allianzatech/blockchainallianza) • [🐛 Report Bug](https://github.com/allianzatech/blockchainallianza/issues) • [💡 Request Feature](https://github.com/allianzatech/blockchainallianza/issues)

</div>
