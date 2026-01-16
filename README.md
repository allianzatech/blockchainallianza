# Allianza Blockchain

<div align="center">

![Allianza Blockchain](https://img.shields.io/badge/Allianza-Blockchain-blue)
![Python](https://img.shields.io/badge/Python-3.8+-green)
![License](https://img.shields.io/badge/License-Commercial-blue)
![Tests](https://img.shields.io/badge/Tests-41%20validations-success)
![Success Rate](https://img.shields.io/badge/Success%20Rate-100%25-brightgreen)
![Testnet](https://img.shields.io/badge/Testnet-Active-success)

**Advanced Blockchain Platform with Cross-Chain Interoperability**

[Features](#-features) • [Documentation](#-documentation) • [Quick Start](#-quick-start) • [Security](#-security) • [Getting Started](GETTING_STARTED.md) • [Testing](TESTING.md)

</div>

---

## 💰 Investment Opportunity - Seed Round Open

<div align="center">

**🌐 The First Quantum-Safe, Bridge-Free Cross-Chain Infrastructure**

Solving **$2.5B+ bridge hacks** and **$1T+ quantum risk** with proven technology

| Market Opportunity | Allianza Solution |
|-------------------|------------------|
| $50B+ Cross-Chain Volume | Bridge-Free Protocol (ALZ-NIEV) |
| $1T+ Quantum Risk | QRS-3 Triple Protection |
| 100% Success Rate | 41 Technical Validations |

**Quick Links:**
- 📄 [Full Investment Overview](docs/INVEST_IN_ALLIANZA.md) - Complete investor document
- 📋 [Investment One-Pager](docs/INVEST_IN_ALLIANZA_ONE_PAGER.md) - Executive summary
- 📧 **Contact Investors:** [contact@allianza.tech](mailto:contact@allianza.tech)

**Why Invest:**
- ✅ **Proven Technology** - Public testnet with real cross-chain transfers
- ✅ **No Competitors** - Only bridge-free + quantum-safe solution
- ✅ **Enterprise-Ready** - Institutional-grade audit guides and proofs
- ✅ **Open Core Model** - Sustainable revenue with transparent protocols

</div>

---

## 🌟 Features

- ✅ **Cross-Chain Interoperability**: Real transfers between EVM, non-EVM, and sovereign blockchains
- ✅ **ALZ-NIEV Protocol**: 5-layer interoperability system with ZK proofs
- ✅ **Quantum-Safe Security**: Post-quantum cryptography (ML-DSA, ML-KEM, SPHINCS+)
- ✅ **Bridge-Free Transfers**: No custody, no wrapped tokens
- ✅ **Multi-Consensus Support**: PoW, PoS, PoH+PoS+BFT, Custom BFT

## 📚 Documentation

| Document | Description |
|----------|-------------|
| [Complete README](docs/README_COMPLETO.md) | Complete system documentation |
| [Security Model](docs/SECURITY_MODEL_WHITEPAPER.md) | Security architecture and model |
| [Threat Model](docs/THREAT_MODEL.md) | Threat analysis and mitigation |
| [Audit Guide](AUDIT_GUIDE.md) | External audit guidelines |
| [Technical Proofs](PROOFS_README.md) | Technical proofs and verifications |
| [Roadmap](docs/ROADMAP_PUBLIC.md) | Development roadmap |

## 🔬 Technical Proofs

Allianza Blockchain provides **verifiable technical proofs** that can be independently audited:

- ✅ **41 Technical Validations** - 100% success rate
- ✅ **On-Chain Verifiable Transactions** - Real transactions on Bitcoin, Ethereum, Polygon testnets
- ✅ **Quantum Security Proofs** - QRS-3 implementation verified
- ✅ **Cross-Chain Interoperability Proofs** - Real transfers between blockchains
- ✅ **Public Testnet** - Fully functional testnet available at https://testnet.allianza.tech

**Quick Access:**
- [Technical Proofs Index](PROOFS_README.md) - Quick access to all proofs
- [Complete Technical Proofs](COMPLETE_TECHNICAL_PROOFS_FINAL.json) - Full technical validation (41 tests)
- [On-Chain Proofs](VERIFIABLE_ON_CHAIN_PROOFS.md) - Verifiable transaction hashes
- [Audit Guide](AUDIT_GUIDE.md) - Complete audit guide for external auditors

**Verification Scripts:**
```bash
# Verify all technical proofs
python scripts/verify_technical_proofs.py

# Verify on-chain transactions
python scripts/verify_on_chain_transactions.py

# Verify QRS-3 implementation
python scripts/verify_qrs3_implementation.py
```

## 🏗️ Project Structure

```
allianza-blockchain/
├── core/                    # Core blockchain components
│   ├── interoperability/    # Cross-chain interoperability
│   ├── consensus/          # Consensus mechanisms
│   └── quantum/            # Quantum-safe cryptography
├── testnet/                # Testnet infrastructure
├── scripts/                # Utility scripts
├── docs/                   # Documentation
├── config/                 # Configuration files
├── templates/              # Web templates
└── static/                 # Static assets
```

## 🛠️ Installation

### Quick Start (Docker - Recommended)

```bash
# Clone repository
git clone https://github.com/allianzatech/blockchainallianza.git
cd blockchainallianza

# Run with Docker (one command)
docker-compose -f docker-compose.public.yml up

# Or build and run
docker build -f Dockerfile.public -t allianza-public .
docker run -v $(pwd)/verification_reports:/app/verification_reports allianza-public
```

### Manual Installation

#### Requirements

- Python 3.8+
- Redis (optional, for caching)
- Node.js 16+ (for frontend assets)

#### Setup

```bash
# Clone repository
git clone https://github.com/allianzatech/blockchainallianza.git
cd blockchainallianza

# Install dependencies
pip install -r requirements.txt

# Install frontend dependencies (optional)
npm install
```

### GitHub Codespaces

Click the green "Code" button and select "Codespaces" to test the repository in your browser with one click!

## 📖 Quick Start

### Run All Demos

```bash
# Linux/Mac
./examples/run_all_demos.sh

# Windows
examples\run_all_demos.bat
```

### Docker Quick Test

```bash
docker-compose -f docker-compose.public.yml up
```

### 1. Clone and Install

```bash
git clone https://github.com/allianzatech/blockchainallianza.git
cd blockchainallianza
pip install -r requirements.txt
```

### 2. Run Examples

```bash
# QRS-3 Signature Demo
python examples/qrs3_demo.py

# ALZ-NIEV Protocol Demo
python examples/alz_niev_demo.py

# Cross-Chain Transfer Demo
python examples/cross_chain_transfer.py
```

### 3. Verify Technical Proofs

```bash
# Verify all proofs
python scripts/verify_technical_proofs.py

# Verify on-chain transactions
python scripts/verify_on_chain_transactions.py
```

**For detailed instructions, see [GETTING_STARTED.md](GETTING_STARTED.md)**

## 🔐 Security

This project implements quantum-safe cryptography and follows security best practices.

- **Post-Quantum Cryptography**: ML-DSA, ML-KEM, SPHINCS+
- **Zero-Knowledge Proofs**: ZK-SNARK verification
- **Multi-Layer Security**: 6 layers of security protection
- **Audit Logs**: Complete transaction and system audit trails

See [SECURITY.md](docs/README_SECURITY.md) for complete security documentation.

## 🌐 Cross-Chain Interoperability

Allianza supports real cross-chain transfers between:

- **EVM Chains**: Ethereum, Polygon, BSC, Base
- **Non-EVM**: Solana (PoH+PoS+BFT)
- **Sovereign**: Allianza (Custom PoS+BFT)
- **UTXO**: Bitcoin (PoW)

All transfers include:
- ✅ ZK Proofs (verified on-chain)
- ✅ Merkle Proofs (inclusion verification)
- ✅ Consensus Proofs (consensus-specific validation)
- ✅ State Transition Hashes
- ✅ No custody, no wrapped tokens

## 📄 License

This project uses a commercial license. See [LICENSE](LICENSE) for details.

## 🤝 Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## 🧪 Testing

Run tests and verify technical proofs:

```bash
# Run all public tests
python tests/public/run_all_tests.py

# Verify technical proofs
python scripts/verify_technical_proofs.py
```

See [TESTING.md](TESTING.md) for complete testing guide.

## 🌐 Links

- **Website**: https://allianza.tech
- **Documentation**: [docs/](docs/)
- **Testnet**: Available at `/testnet` endpoint
- **Contact**: contact@allianza.tech

---

<div align="center">

**Built with ❤️ by [Allianza Tech](https://allianza.tech)**

[Website](https://allianza.tech) • [Documentation](docs/) • [Security](docs/README_SECURITY.md)

</div>
