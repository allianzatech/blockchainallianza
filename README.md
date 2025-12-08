# Allianza Blockchain - Universal Execution Chain (UEC)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Testnet Status](https://img.shields.io/badge/Testnet-Active-success)](https://testnet.allianza.tech)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![CI Status](https://img.shields.io/badge/CI-Passing-success)](https://github.com/dieisonmaach-lang/allianzablockchain/actions)
[![Security](https://img.shields.io/badge/Security-Audited-blue)](SECURITY.md)

> **Post-quantum and interoperable blockchain** with quantum security (QRS-3), bridge-free interoperability, and adaptive consensus (ALZ-NIEV Protocol).

## 🚀 Quick Start

### For Developers

1. **Clone the repository**
   ```bash
   git clone https://github.com/dieisonmaach-lang/allianzablockchain.git
   cd allianzablockchain
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run verification tests**
   ```bash
   python tests/public/run_verification_tests.py
   ```

4. **Access Public Testnet**
   - 🌐 **Dashboard**: https://testnet.allianza.tech
   - 🔍 **Explorer**: https://testnet.allianza.tech/explorer
   - 🚰 **Faucet**: https://testnet.allianza.tech/faucet

### For Auditors and Verifiers

📋 **Read first**: [VERIFICATION.md](VERIFICATION.md) - Complete independent verification guide

🧪 **Run tests**: [TESTING.md](TESTING.md) - How to run and reproduce tests

## 📊 Technical Proof

### Published Technical Proofs

- ✅ **Complete Proofs**: [`COMPLETE_TECHNICAL_PROOFS_FINAL.json`](COMPLETE_TECHNICAL_PROOFS_FINAL.json)
- ✅ **Test Scripts**: [`tests/public/`](tests/public/) - All scripts that generated the proofs
- ✅ **Active Testnet**: https://testnet.allianza.tech - Test in real-time

### Validated Technologies

| Technology | Status | Proof |
|------------|--------|------|
| **QRS-3 (PQC)** | ✅ Validated | ML-DSA, SPHINCS+ implemented |
| **Bridge-Free Interoperability** | ✅ Validated | Real cross-chain transfers |
| **ALZ-NIEV Protocol** | ✅ Validated | Adaptive consensus functional |
| **Quantum Security Service** | ✅ Validated | QSS Dashboard active |

## 🏗️ Architecture

```
allianzablockchain/
├── core/                    # Main source code
│   ├── consensus/          # ALZ-NIEV Protocol
│   ├── crypto/             # QRS-3, PQC algorithms
│   └── interoperability/   # Bridge-free interop
├── contracts/              # Smart contracts
│   ├── evm/               # Solidity contracts
│   └── proof-of-lock/     # Proof-of-Lock implementation
├── sdk/                    # Public SDKs
│   ├── qss-sdk/          # Quantum Security Service SDK
│   └── qss-verifier/     # QSS Verifier
├── tests/                  # Public tests
│   └── public/           # Verification scripts
├── docs/                   # Technical documentation
└── proofs/                 # Technical proofs and reports
```

## 🔐 Security

- 🔒 **Private Keys**: Never committed (protected by `.gitignore`)
- 🛡️ **Secrets**: Managed via environment variables
- 📋 **Security Policy**: [SECURITY.md](SECURITY.md)

**⚠️ IMPORTANT**: This repository contains public source code. Never expose:
- Private keys
- Wallet seeds
- API tokens
- Database credentials

## 📚 Documentation

### Core Documentation
- 📖 [Technical Whitepaper](docs/WHITEPAPER.md)
- 🏗️ [Architecture](docs/ARCHITECTURE.md)
- 🔍 [API Reference](docs/API_REFERENCE.md)
- 🚀 [Quick Start Guide](docs/QUICK_START.md)

### Testing & Verification
- 🧪 [Testing Guide](TESTING.md)
- ✅ [Verification Guide](VERIFICATION.md)
- 🔐 [Security Policy](SECURITY.md)

### Project Information
- 🗺️ [Roadmap](ROADMAP.md)
- 📝 [Changelog](CHANGELOG.md)
- 🤝 [Contributing](CONTRIBUTING.md)
- 📋 [Code of Conduct](CODE_OF_CONDUCT.md)

## 🧪 Tests and Verification

### Run Public Tests

```bash
# Basic verification tests
python tests/public/run_verification_tests.py

# Complete tests (reproduce technical proofs)
python tests/public/run_all_tests.py

# Specific tests
python tests/public/test_qrs3_verification.py
python tests/public/test_interoperability.py
python tests/public/test_consensus.py
```

### Verify Technical Proofs

1. Run scripts in [`tests/public/`](tests/public/)
2. Compare results with [`COMPLETE_TECHNICAL_PROOFS_FINAL.json`](COMPLETE_TECHNICAL_PROOFS_FINAL.json)
3. Verify transactions on testnet: https://testnet.allianza.tech/explorer

## 🌐 Live Public Testnet

The public testnet is **active and available** for testing:

### 🚀 Quick Access
- 🌐 **Dashboard**: [https://testnet.allianza.tech](https://testnet.allianza.tech)
- 🔍 **Explorer**: [https://testnet.allianza.tech/explorer](https://testnet.allianza.tech/explorer)
- 🚰 **Faucet**: [https://testnet.allianza.tech/faucet](https://testnet.allianza.tech/faucet)
- 🔐 **QRS-3 Verifier**: [https://testnet.allianza.tech/qrs3-verifier](https://testnet.allianza.tech/qrs3-verifier)

### ✨ Features
- ✅ Real-time dashboard with live statistics
- ✅ Block and transaction explorer
- ✅ Automatic faucet (1000 ALZ per request)
- ✅ QSS Dashboard (Quantum Security Service)
- ✅ Proof verifier for transaction proofs
- ✅ Cross-chain interoperability testing

### 📊 Testnet Statistics
- **Status**: ✅ Online and Operational
- **Network**: Allianza Testnet
- **Consensus**: ALZ-NIEV Protocol (Adaptive)
- **Security**: QRS-3 (Post-Quantum Cryptography)

## 🤝 Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for details on how to contribute.

## 📄 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) for details.

## 🔗 Quick Links

### 🌐 Official Resources
- **Website**: https://allianza.tech
- **Testnet**: https://testnet.allianza.tech
- **GitHub**: https://github.com/dieisonmaach-lang/allianzablockchain

### 📖 Documentation
- **Whitepaper**: [docs/WHITEPAPER.md](docs/WHITEPAPER.md)
- **Roadmap**: [ROADMAP.md](ROADMAP.md)
- **Changelog**: [CHANGELOG.md](CHANGELOG.md)

### 📧 Contact
- **Security Issues**: See [SECURITY.md](SECURITY.md)
- **General Inquiries**: Contact via GitHub Issues
- **Partnerships**: Contact via website

## 🎯 Key Features

### 🔐 Quantum Security
- **QRS-3**: Post-quantum cryptography (ML-DSA, SPHINCS+)
- **Quantum-Resistant**: Protection against quantum computing attacks
- **Batch Verification**: Efficient signature verification

### 🌉 Interoperability
- **Bridge-Free**: No traditional bridges or custody
- **Cross-Chain**: Seamless transfers between blockchains
- **ZK Proofs**: Zero-knowledge proofs for validation

### ⚙️ Consensus
- **ALZ-NIEV Protocol**: Adaptive consensus mechanism
- **High Throughput**: Optimized for performance
- **Scalable**: Automatic scaling based on network conditions

## ⚠️ Disclaimer

This is a project under development. Use only on testnet. Do not use real private keys or real funds during testing.

---

**Made with ❤️ by Allianza Team**
