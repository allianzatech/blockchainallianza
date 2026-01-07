# Allianza Blockchain

> **Quantum-Safe, Bridge-Free Interoperability Protocol**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

## 🎯 Executive Summary

**Allianza Blockchain** is a next-generation interoperability protocol that enables secure, bridge-free cross-chain transfers using quantum-safe cryptography and zero-knowledge proofs. Unlike traditional bridge solutions, Allianza uses the **ALZ-NIEV protocol** to achieve trustless interoperability without requiring locked assets or centralized bridges.

### Key Differentiators

- 🔐 **Quantum-Safe Cryptography** - NIST PQC standards (ML-DSA, ML-KEM, SPHINCS+)
- 🌉 **Bridge-Free Interoperability** - No locked assets, no centralized bridges
- 🔗 **Universal Chain ID (UChainID)** - Unified addressing across all blockchains
- 🔒 **Zero-Knowledge Proofs** - Privacy-preserving transaction verification
- ⚡ **Multi-Chain Support** - Bitcoin, Ethereum, Polygon, Solana, BSC, and more

---

## 👥 Who is this for?

### For Developers
- Study the open-core protocol implementation
- Understand bridge-free interoperability architecture
- Review quantum-safe cryptography integration
- Explore ZK proof generation and verification
- Access code examples and technical documentation

### For Investors
- Review auditable protocol code
- Verify on-chain proofs of functionality
- Understand the open-core business model
- Evaluate technical differentiation
- Contact for commercial licensing opportunities

### For Enterprises (Banks, Exchanges, Institutions)
- Audit the protocol for security and compliance
- Evaluate quantum-safe cryptography implementation
- Review interoperability architecture
- Understand commercial licensing options
- Contact for enterprise deployment

---

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Installation

```bash
# Clone the repository
git clone https://github.com/allianzatech/blockchainallianza.git
cd blockchainallianza

# Install dependencies
pip install -r requirements.txt
```

### Basic Usage

```python
from core.interoperability.alz_niev_interoperability import ALZ_NIEVProtocol

# Initialize protocol
protocol = ALZ_NIEVProtocol()

# Create cross-chain transfer
result = protocol.create_transfer(
    source_chain="ethereum",
    target_chain="bitcoin",
    amount=1000000,  # in smallest unit
    recipient_address="bc1q..."
)
```

---

## 📚 Documentation

- **[Technical Documentation](./docs/README.md)** - Complete technical specifications
- **[Security Policy](./SECURITY.md)** - Security reporting and features
- **[Roadmap](./ROADMAP.md)** - Development roadmap and planned features
- **[Open Core Strategy](./OPEN_CORE_STRATEGY.md)** - Understanding our open-core model
- **[Contributing Guide](./CONTRIBUTING.md)** - How to contribute to the project
- **[Audit Guide](./AUDIT_GUIDE.md)** - Guide for developers, investors, and auditors
- **[Proof of Functionality](./PROOF_OF_FUNCTIONALITY.md)** - Verifiable proof that the technology works

---

## 🔍 What's Included (Open Core)

This repository contains the **open-core** implementation of Allianza Blockchain:

### ✅ Included

- **Core Protocol** - Complete ALZ-NIEV protocol implementation
- **Quantum-Safe Cryptography** - NIST PQC standards integration
- **UChainID System** - Universal Chain ID implementation
- **ZK Proof System** - Zero-knowledge proof generation and verification
- **Multi-Chain Adapters** - Support for Bitcoin, Ethereum, Polygon, Solana, BSC
- **Technical Documentation** - Complete API and architecture docs
- **Code Examples** - Working examples and demos
- **On-Chain Proofs** - Verifiable proof of functionality

### ❌ Not Included (Commercial License Required)

- **Production Testnet** - Fully functional testnet deployment
- **Production Bridge** - Real cross-chain bridge implementation
- **Enterprise Features** - Advanced monitoring, analytics, and management
- **Commercial Adapters** - Production-ready blockchain adapters
- **Deployment Infrastructure** - Production deployment configurations
- **Support & SLA** - Commercial support and service level agreements

> **Note:** The testnet runs on our private infrastructure. The protocol code in this repository is fully functional and can be audited, but production deployment requires a commercial license.

---

## 🎯 Proof of Functionality

### Live Testnet
- **Testnet URL:** [https://testnet.allianza.tech](https://testnet.allianza.tech)
- **Status:** Fully operational with real transactions
- **Supported Chains:** Bitcoin, Ethereum, Polygon, Solana, BSC

### On-Chain Proofs
- **Verifiable Transactions:** See [proofs/](./proofs/) directory
- **UChainID Examples:** Working examples of universal chain IDs
- **ZK Proof Verification:** On-chain verifiable proofs
- **Proof Documentation:** See [PROOF_OF_FUNCTIONALITY.md](./PROOF_OF_FUNCTIONALITY.md) for complete proof details

### For Auditors and Investors
- **[Audit Guide](./AUDIT_GUIDE.md)** - Complete guide for auditing the codebase
- **[Proof of Functionality](./PROOF_OF_FUNCTIONALITY.md)** - Detailed proof documentation
- **Verification:** All proofs are verifiable and on-chain

---

## 📖 Architecture Overview

```
Allianza Blockchain
├── core/
│   ├── consensus/        # Consensus mechanisms
│   ├── crypto/           # Quantum-safe cryptography
│   └── interoperability/ # ALZ-NIEV protocol
├── contracts/            # Smart contracts
├── proofs/              # ZK proofs and verification
├── docs/                # Technical documentation
└── examples/            # Code examples
```

### Key Components

1. **ALZ-NIEV Protocol** - Bridge-free interoperability protocol
2. **UChainID** - Universal Chain ID system for cross-chain addressing
3. **Quantum-Safe Crypto** - Post-quantum cryptography implementation
4. **ZK Proof System** - Zero-knowledge proof generation and verification

---

## 🔐 Security

Allianza Blockchain implements multiple layers of security:

- ✅ **Quantum-Safe Cryptography** - NIST PQC standards
- ✅ **Zero-Knowledge Proofs** - Privacy-preserving verification
- ✅ **No Bridge Risk** - No locked assets or centralized bridges
- ✅ **Auditable Protocol** - Open-core code for security audits
- ✅ **Security Policy** - See [SECURITY.md](./SECURITY.md)

---

## 💼 Commercial Licensing

This repository contains the **open-core** protocol. For production deployment, enterprise features, and commercial use, a **commercial license** is required.

### Commercial License Includes:
- Production testnet access
- Production bridge implementation
- Enterprise features and monitoring
- Commercial support and SLA
- Deployment infrastructure
- Priority updates and features

### Contact for Commercial Licensing:
- **Email:** commercial@allianza.tech
- **Website:** [https://allianza.tech](https://allianza.tech)

See [COMMERCIAL_LICENSE.md](./COMMERCIAL_LICENSE.md) for more information.

---

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](./CONTRIBUTING.md) for guidelines.

### How to Contribute:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

---

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](./LICENSE) file for details.

**Note:** Commercial use requires a separate commercial license. See [COMMERCIAL_LICENSE.md](./COMMERCIAL_LICENSE.md).

---

## 🔗 Links

- **Website:** [https://allianza.tech](https://allianza.tech)
- **Testnet:** [https://testnet.allianza.tech](https://testnet.allianza.tech)
- **Documentation:** [./docs/README.md](./docs/README.md)
- **Security:** [./SECURITY.md](./SECURITY.md)
- **Roadmap:** [./ROADMAP.md](./ROADMAP.md)

---

## 🚫 What's NOT in This Repository

This is the **open-core** repository. Production/commercial files are in the private repository:

- ❌ Production testnet infrastructure
- ❌ Commercial bridge implementation
- ❌ Production deployment files
- ❌ Commercial adapters and configurations

See [PUBLIC_REPO_EXCLUSIONS.md](./PUBLIC_REPO_EXCLUSIONS.md) for a complete list of excluded files.

---

## 📧 Contact

- **Commercial Inquiries:** commercial@allianza.tech
- **Security Issues:** security@allianza.tech
- **General Questions:** info@allianza.tech

---

## ⭐ Why Choose Allianza?

### For Developers
- **Open Core** - Study and understand the protocol
- **Well Documented** - Complete technical documentation
- **Modern Stack** - Python 3.8+, clean architecture
- **Extensible** - Easy to extend and customize

### For Enterprises
- **Quantum-Safe** - Future-proof cryptography
- **Bridge-Free** - No bridge risk or locked assets
- **Auditable** - Open-core code for security audits
- **Production-Ready** - Commercial license available

### For Investors
- **Proven Technology** - Working testnet with real transactions
- **Clear Business Model** - Open-core with commercial licensing
- **Technical Differentiation** - Unique bridge-free approach
- **Market Opportunity** - Growing interoperability market

---

**Built with ❤️ by the Allianza Team**

