# 🔐 Allianza Blockchain - Public Repository

[![npm version](https://img.shields.io/npm/v/allianza-qss-js)](https://www.npmjs.com/package/allianza-qss-js)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Testnet](https://img.shields.io/badge/Testnet-Active-green)](https://testnet.allianza.tech)
[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.0+-blue.svg)](https://www.typescriptlang.org/)
[![CI](https://github.com/dieisonmaach-lang/allianzablockchainpublic/workflows/CI/badge.svg)](https://github.com/dieisonmaach-lang/allianzablockchainpublic/actions)
[![Tests](https://img.shields.io/badge/Tests-Passing-brightgreen)](https://github.com/dieisonmaach-lang/allianzablockchainpublic/actions)

> **Post-Quantum Blockchain for Real-World Assets (RWA)**

This is the **public repository** for developers and investors to validate Allianza Blockchain technology. The core blockchain implementation remains private for security reasons.

---

## 🚀 Quick Start

### **For Developers**

1. **Install the QSS SDK:**
   ```bash
   npm install allianza-qss-js
   ```

2. **Try the API:**
   ```javascript
   const response = await fetch('https://testnet.allianza.tech/api/qss/generate-proof', {
       method: 'POST',
       headers: { 'Content-Type': 'application/json' },
       body: JSON.stringify({
           chain: 'bitcoin',
           tx_hash: 'your_tx_hash'
       })
   });
   const proof = await response.json();
   ```

3. **Visit the Testnet:**
   - 🌐 **Testnet:** https://testnet.allianza.tech
   - 📚 **Developer Hub:** https://testnet.allianza.tech/developer-hub
   - 🏆 **Leaderboard:** https://testnet.allianza.tech/leaderboard

---

## 📦 What's Included

### ✅ **Available in This Repository:**

- **QSS SDK** (`qss-sdk/`) - TypeScript SDK for quantum security
- **Documentation** (`docs/`) - API reference, guides, and technical docs
- **Templates** (`templates/testnet/`) - UI templates for testnet
- **Technical Proofs** (`TECHNICAL_PROOFS_COMPLETE_FINAL.json`) - 41 technical proofs
- **Real Proofs** (`proofs/`) - Verifiable real-world proofs (transfers, QRS-3, ALZ-NIEV, QSS)
- **Whitepaper** (`WHITEPAPER_ALLIANZA_BLOCKCHAIN.md`) - Complete technical documentation

### 🔒 **Not Included (Private Repository):**

- Core blockchain implementation (ALZ-NIEV, QRS-3)
- Private keys, passwords, and sensitive configuration
- Database files and logs
- Internal security mechanisms

---

## 🛠️ Technologies

- **Post-Quantum Cryptography:** ML-DSA, ML-KEM, SPHINCS+, QRS-3
- **Blockchain:** Custom consensus, cross-chain interoperability
- **SDK:** TypeScript/JavaScript
- **Testnet:** Live at https://testnet.allianza.tech

---

## 📚 Documentation

- **API Reference:** `docs/API_REFERENCE.md`
- **Quick Start Guide:** `docs/QUICK_START.md`
- **QSS Integration:** `QSS_FOR_OTHER_BLOCKCHAINS.md`
- **Whitepaper:** `WHITEPAPER_ALLIANZA_BLOCKCHAIN.md`
- **Audit Readiness:** `docs/AUDIT_READINESS.md`
- **Contributing:** `CONTRIBUTING.md`

---

## 🔗 Links

- 🌐 **Testnet:** https://testnet.allianza.tech
- 📦 **npm Package:** https://www.npmjs.com/package/allianza-qss-js
- 📄 **Technical Proofs:** See `TECHNICAL_PROOFS_COMPLETE_FINAL.json`
- 🔐 **Real Proofs:** See `proofs/` directory for verifiable real-world proofs

---

## ⚠️ Security Notice

This repository contains **public-facing code and documentation only**. The core blockchain implementation, private keys, and sensitive data are kept in a private repository for security reasons.

---

## 📄 License

MIT License - See `LICENSE` file (if included)

---

**Built with ❤️ for the post-quantum future**

