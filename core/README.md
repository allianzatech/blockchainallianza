# Core Module

This directory contains the core functionality of Allianza Blockchain.

## 📁 Structure

```
core/
├── consensus/           # Consensus algorithms
│   ├── adaptive_consensus.py      # Adaptive consensus mechanism
│   └── alz_niev_interoperability.py  # ALZ-NIEV protocol
│
├── crypto/              # Cryptography modules
│   ├── pqc_crypto.py    # Post-quantum cryptography
│   └── quantum_security.py  # Quantum security system
│
└── interoperability/    # Cross-chain interoperability
    ├── bridge_free_interop.py  # Bridge-free interoperability
    ├── proof_of_lock.py  # Proof-of-Lock mechanism
    └── solana_bridge.py  # Solana bridge integration
```

## 🔧 Modules

### Consensus (`consensus/`)

- **Adaptive Consensus** - Dynamic consensus mechanism that adapts to network conditions
- **ALZ-NIEV Protocol** - Non-Intermediate Execution Validation protocol

### Cryptography (`crypto/`)

- **PQC Crypto** - Post-quantum cryptography implementations (NIST PQC standards)
- **Quantum Security** - Quantum-safe security system with QRS-3

### Interoperability (`interoperability/`)

- **Bridge-Free Interop** - Core bridge-free interoperability logic
- **Proof-of-Lock** - Cryptographic proof-of-lock mechanism
- **Solana Bridge** - Solana blockchain integration

## 📚 Documentation

For detailed architecture information, see [docs/ARCHITECTURE.md](../docs/ARCHITECTURE.md).

## 🔗 Related

- [Main README](../README.md)
- [Architecture Documentation](../docs/ARCHITECTURE.md)
- [Contributing Guide](../CONTRIBUTING.md)

