# Allianza Blockchain - Project One Pager

**Version:** 1.0 | **Date:** January 2026

---

## 🎯 Elevator Pitch

Allianza is a **post-quantum blockchain infrastructure** that enables **bridge-free, trustless cross-chain interoperability** between heterogeneous blockchains (EVM, non-EVM, UTXO) using cryptographic proofs and zero-knowledge verification. Unlike traditional bridges that require custody and wrapped tokens, Allianza provides direct transfers with **institutional-grade verification standards**.

---

## 🔥 Problem → Solution → Differential

### The Problem

- **Bridge Vulnerabilities**: Over $2.5B lost in bridge hacks due to custodial models and trusted relayers
- **Quantum Threats**: Current blockchain cryptography is vulnerable to future quantum computers
- **Fragmented Ecosystems**: Users need multiple wallets, bridges, and wrapped tokens to move assets between chains

### The Solution

**ALZ-NIEV Protocol** - A 5-layer interoperability system that:
- ✅ Eliminates custody (no locked funds)
- ✅ Removes wrapped tokens (direct transfers)
- ✅ Uses cryptographic proofs (consensus, Merkle, ZK)
- ✅ Supports heterogeneous chains (Bitcoin ↔ Ethereum ↔ Solana)

### The Differential

| Feature | Industry Standard | Allianza |
|---------|------------------|----------|
| **Custody** | ✅ Yes (vulnerable) | ❌ No (bridge-free) |
| **Consensus Verification** | ❌ No | ✅ Yes (ALZ-NIEV v1.0) |
| **Quantum-Safe** | ❌ No | ✅ Yes (QRS-3: ML-DSA, ML-KEM, SPHINCS+) |
| **EVM ↔ Bitcoin** | ❌ No | ✅ Yes (heterogeneous) |
| **Trustless Level** | ⚠️ Trust-minimized | ✅ 100% Trustless |

---

## 🏗️ Components & Integrations

### Core Components

1. **ALZ-NIEV Protocol** (`core/consensus/alz_niev_interoperability.py`)
   - Cross-chain interoperability with 5 proof layers
   - Chain-agnostic finality verification
   - Merkle inclusion proofs

2. **Quantum Security (QRS-3)** (`core/crypto/`)
   - ML-DSA (signatures)
   - ML-KEM (key exchange)
   - SPHINCS+ (hash-based signatures)

3. **ZK Proof System** (`core/zk/`)
   - State transition verification
   - Circuit-based proofs
   - On-chain verification

### Supported Chains

- **EVM**: Ethereum, Polygon, BSC, Base
- **Non-EVM**: Solana (PoH+PoS+BFT)
- **UTXO**: Bitcoin (PoW)
- **Sovereign**: Allianza (Custom PoS+BFT)

### Integration Points

- **APIs**: RESTful APIs for cross-chain transfers
- **SDK**: Python SDK for developers
- **CLI**: Command-line tools for testing
- **Testnet**: Public testnet at https://testnet.allianza.tech

---

## 🧪 Where to Test Now

### Live Testnet

- **Dashboard**: [https://testnet.allianza.tech](https://testnet.allianza.tech)
- **Interoperability Explorer**: [https://testnet.allianza.tech/interoperability](https://testnet.allianza.tech/interoperability)
- **Verified Transfers API**: [https://testnet.allianza.tech/api/interoperability/verified-transfers](https://testnet.allianza.tech/api/interoperability/verified-transfers)

### Quick Verification

```bash
# Clone and run (1 command)
git clone https://github.com/allianzatech/blockchainallianza.git && cd blockchainallianza && docker-compose -f docker-compose.public.yml up

# Or verify proofs directly
python scripts/verify_technical_proofs.py
python scripts/verify_on_chain_transactions.py
```

### Technical Proofs

- **41 Technical Validations**: 100% success rate
- **On-Chain Transactions**: Verifiable on Bitcoin, Ethereum, Polygon testnets
- **Quantum Security**: QRS-3 implementation verified
- **Cross-Chain Transfers**: Real transfers with cryptographic proofs

**See**: [PROOFS_README.md](../PROOFS_README.md) | [Complete Technical Proofs](../COMPLETE_TECHNICAL_PROOFS_FINAL.json)

---

## 📊 Technical Specifications

### Verification Standard

**ALZ-NIEV Verification Standard v1.0** defines:
- ✅ Consensus finality (chain-specific)
- ✅ Merkle inclusion proofs (depth ≥ minimum)
- ✅ Zero-knowledge proofs (state transitions)
- ✅ Public transaction hashes (verifiable)

**See**: [ALZ_NIEV_VERIFICATION_STANDARD.md](ALZ_NIEV_VERIFICATION_STANDARD.md)

### Security Model

- **Threat Model**: STRIDE-based analysis
- **Security Architecture**: 6-layer protection
- **Audit-Ready**: Complete documentation for external auditors

**See**: [THREAT_MODEL_ALZ_NIEV.md](THREAT_MODEL_ALZ_NIEV.md) | [AUDIT_AND_VERIFICATION.md](AUDIT_AND_VERIFICATION.md)

---

## 🧩 Open Core Strategy

### Open Source (MIT License)

- ✅ Core protocols and specifications
- ✅ Testnet implementation
- ✅ SDK and developer tools
- ✅ Complete documentation
- ✅ Verification scripts

### Commercial / Enterprise

- 🔒 Production-optimized implementations
- 🔒 Custom integrations and SLA
- 🔒 Dedicated audits and support
- 🔒 Enterprise features

**See**: [OPEN_CORE_STRATEGY.md](../OPEN_CORE_STRATEGY.md)

---

## 📞 Contact

**Enterprise, Partnerships, or Integrations:**
- 📧 **Email**: contact@allianza.tech
- 🌐 **Website**: https://allianza.tech

**Community:**
- 📚 **Documentation**: [docs/](docs/)
- 🧪 **Testnet**: [https://testnet.allianza.tech](https://testnet.allianza.tech)
- 💬 **GitHub**: [github.com/allianzatech/blockchainallianza](https://github.com/allianzatech/blockchainallianza)

---

## 📈 Roadmap Highlights

### ✅ Completed (Q4 2025)

- Quantum-Safe Cryptography (QRS-3)
- Bridge-Free Interoperability (ALZ-NIEV)
- Multi-Chain Support (Bitcoin, Ethereum, Polygon, Solana)
- Public Testnet Deployment
- Institutional-Grade Verification Standard

### 🚧 In Progress (Q1 2026)

- Mainnet Deployment
- Performance Optimizations
- Enhanced Documentation
- Mobile SDK

### 📅 Planned (Q2-Q4 2026)

- Additional Blockchain Support (Avalanche, Cosmos, Polkadot)
- Enterprise Features (Multi-sig, Compliance, KYC/AML)
- Advanced Analytics Dashboard
- Governance System

**See**: [ROADMAP.md](../ROADMAP.md)

---

## 🎯 Key Metrics

- **Technical Validations**: 41 tests, 100% success rate
- **Supported Chains**: 5+ (Bitcoin, Ethereum, Polygon, Solana, BSC)
- **Testnet Status**: ✅ Active
- **Verification Standard**: ALZ-NIEV v1.0 (institutional-grade)
- **License**: MIT (open core)

---

## 🔗 Quick Links

- **GitHub**: [github.com/allianzatech/blockchainallianza](https://github.com/allianzatech/blockchainallianza)
- **Testnet**: [testnet.allianza.tech](https://testnet.allianza.tech)
- **Documentation**: [docs/](docs/)
- **Verification Standard**: [docs/ALZ_NIEV_VERIFICATION_STANDARD.md](docs/ALZ_NIEV_VERIFICATION_STANDARD.md)
- **Open Core Strategy**: [OPEN_CORE_STRATEGY.md](../OPEN_CORE_STRATEGY.md)

---

**Last Updated**: January 2026  
**Status**: ✅ Active Development | Testnet Live | Production-Ready Architecture
