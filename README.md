# Allianza Blockchain - Universal Execution Chain (UEC)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Testnet Status](https://img.shields.io/badge/Testnet-Active-success)](https://testnet.allianza.tech)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![CI Status](https://img.shields.io/badge/CI-Passing-success)](https://github.com/dieisonmaach-lang/allianzablockchain/actions)
[![Security](https://img.shields.io/badge/Security-Audited-blue)](SECURITY.md)
[![Contributors Welcome](https://img.shields.io/badge/contributors-welcome-brightgreen)](CONTRIBUTING.md)
[![Documentation](https://img.shields.io/badge/docs-available-blue)](docs/)

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

⚡ **Quick Start**: [QUICK_VERIFICATION_GUIDE.md](QUICK_VERIFICATION_GUIDE.md) - Quick reference for finding source code and proofs

📋 **Read first**: [VERIFICATION.md](VERIFICATION.md) - Complete independent verification guide

🧪 **Run tests**: [TESTING.md](TESTING.md) - How to run and reproduce tests

📋 **Response to Analysis**: [RESPONSE_TO_ANALYSIS.md](RESPONSE_TO_ANALYSIS.md) - Direct response to technical analysis reports

## 📊 Technical Proof

### ✅ Source Code is Publicly Available

**⚠️ IMPORTANT: All core implementations are PUBLIC and auditable in this repository:**

- **QRS-3 (PQC)**: [`core/crypto/pqc_crypto.py`](core/crypto/pqc_crypto.py) - ML-DSA and SPHINCS+ implementations
- **Quantum Security**: [`core/crypto/quantum_security.py`](core/crypto/quantum_security.py) - Quantum security service
- **ALZ-NIEV Consensus**: [`core/consensus/adaptive_consensus.py`](core/consensus/adaptive_consensus.py) - Adaptive consensus mechanism
- **ALZ-NIEV Protocol**: [`core/consensus/alz_niev_interoperability.py`](core/consensus/alz_niev_interoperability.py) - **FULL PROTOCOL IMPLEMENTATION - PUBLIC**
- **Bridge-Free Interop**: [`core/interoperability/bridge_free_interop.py`](core/interoperability/bridge_free_interop.py) - Bridge-free interoperability
- **Proof-of-Lock**: [`core/interoperability/proof_of_lock.py`](core/interoperability/proof_of_lock.py) - Proof-of-Lock implementation

**🔍 Direct Links to Core Code:**
- [QRS-3 Implementation](https://github.com/dieisonmaach-lang/allianzablockchain/tree/main/core/crypto)
- [ALZ-NIEV Protocol](https://github.com/dieisonmaach-lang/allianzablockchain/tree/main/core/consensus)
- [Interoperability](https://github.com/dieisonmaach-lang/allianzablockchain/tree/main/core/interoperability)

**✅ All source code is in this public repository - no private repositories for core functionality.**

### Published Technical Proofs

- ✅ **Complete Proofs**: [`COMPLETE_TECHNICAL_PROOFS_FINAL.json`](COMPLETE_TECHNICAL_PROOFS_FINAL.json) - All 41 technical proofs
- ✅ **Individual Proof Access**: https://testnet.allianza.tech/proof/<PROOF_ID> - Access individual proofs (e.g., `/proof/QRS3-01`, `/proof/PILAR_1_INTEROPERABILIDADE`)
- ✅ **Verifiable On-Chain Proofs**: [`VERIFIABLE_ON_CHAIN_PROOFS.md`](VERIFIABLE_ON_CHAIN_PROOFS.md) - Real transaction hashes from Bitcoin, Ethereum, Polygon (verifiable on public explorers)
- ✅ **Test Scripts**: [`tests/public/`](tests/public/) - All scripts that generated the proofs
- ✅ **Active Testnet**: https://testnet.allianza.tech - Test in real-time
- ✅ **Response to Analysis**: [`RESPONSE_TO_ANALYSIS.md`](RESPONSE_TO_ANALYSIS.md) - Direct response to technical analysis reports

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
├── core/                    # ✅ PUBLISHED - Main source code
│   ├── consensus/          # ✅ ALZ-NIEV Protocol (adaptive consensus)
│   ├── crypto/             # ✅ QRS-3, PQC algorithms (ML-DSA, SPHINCS+)
│   └── interoperability/   # ✅ Bridge-free interop (Proof-of-Lock, ZK Proofs)
├── contracts/              # Smart contracts
│   ├── evm/               # Solidity contracts (QuantumProofVerifier.sol)
│   └── proof-of-lock/     # Proof-of-Lock implementation
├── sdk/                    # Public SDKs
│   ├── qss-sdk/          # Quantum Security Service SDK
│   └── qss-verifier/     # QSS Verifier
├── tests/                  # Public tests
│   └── public/           # ✅ Verification scripts (reproducible)
├── examples/               # ✅ Code examples
├── docs/                   # Technical documentation
└── proofs/                 # Technical proofs and reports
```

### ✅ Source Code Transparency

**All core implementations are publicly available:**

- **QRS-3 (PQC)**: [`core/crypto/`](core/crypto/) - Complete ML-DSA and SPHINCS+ implementations
- **ALZ-NIEV Protocol**: [`core/consensus/`](core/consensus/) - Adaptive consensus mechanism
- **Bridge-Free Interop**: [`core/interoperability/`](core/interoperability/) - Proof-of-Lock and ZK Proofs

**Verification:**
- ✅ Code is open source and auditable
- ✅ Test scripts are public and reproducible
- ✅ Real transaction hashes are verifiable on public explorers
- ✅ Testnet is live and accessible

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
- 📋 [Response to Analysis](RESPONSE_TO_ANALYSIS.md) - Direct response to technical analysis reports
- 🔐 [Security Policy](SECURITY.md)

### Project Information
- 🗺️ [Roadmap](ROADMAP.md) - Complete ecosystem roadmap
- 📝 [Changelog](CHANGELOG.md)
- 🤝 [Contributing](CONTRIBUTING.md)
- 📋 [Code of Conduct](CODE_OF_CONDUCT.md)
- 🏦 [RWA Tokenization](RWA_TOKENIZATION.md) - Real-World Asset tokenization strategy

## 💡 Code Examples

### Quick Examples

```python
# Create wallet
from allianza_blockchain import AllianzaBlockchain
blockchain = AllianzaBlockchain()
address, private_key = blockchain.create_wallet()

# Create transaction
transaction = blockchain.create_transaction(
    sender=address,
    receiver="ALZ1Receiver...",
    amount=1000.0,
    private_key=private_key
)

# QRS-3 signature
from core.crypto.pqc_crypto import MLDSAKeyPair
mldsa = MLDSAKeyPair()
signature = mldsa.sign(b"Hello, Allianza!")
is_valid = mldsa.verify(b"Hello, Allianza!", signature)
```

📖 **More Examples**: See [examples/](examples/) directory for complete code examples.

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

1. **Run Test Scripts**: Execute scripts in [`tests/public/`](tests/public/)
2. **Compare Results**: Compare with [`COMPLETE_TECHNICAL_PROOFS_FINAL.json`](COMPLETE_TECHNICAL_PROOFS_FINAL.json)
3. **Verify On-Chain**: Check real transaction hashes in [`VERIFIABLE_ON_CHAIN_PROOFS.md`](VERIFIABLE_ON_CHAIN_PROOFS.md)
4. **Testnet Explorer**: Verify transactions on https://testnet.allianza.tech/explorer
5. **Public Explorers**: Verify Bitcoin/Ethereum/Polygon transactions on their respective explorers

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

## 👥 Team & Contributors

### Core Team
- **Allianza Team** - Development and maintenance

### Contributors
We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for details.

### Acknowledgments
- Open Quantum Safe (OQS) for PQC algorithms
- Community contributors and testers

## 📸 Screenshots & Demo

> **Note**: Screenshots and demo GIF will be added here.
> 
> To add:
> - Dashboard screenshot
> - Explorer screenshot  
> - Faucet in action
> - QRS-3 Verifier
> - Demo GIF (15 seconds)

## ⚠️ Disclaimer

This is a project under development. Use only on testnet. Do not use real private keys or real funds during testing.

---

**Made with ❤️ by Allianza Team**
