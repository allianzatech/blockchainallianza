# 📚 Usage Examples - Allianza Blockchain

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
python examples\qss_demo.py
python examples\qrs3_demo.py
python examples\alz_niev_demo.py
python examples\interoperability_demo.py

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
