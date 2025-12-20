# Smart Contracts

This directory contains smart contracts and bridge implementations for Allianza Blockchain.

## 📁 Structure

```
contracts/
├── evm/                          # EVM-compatible contracts
│   └── QuantumProofVerifier.sol  # ZK proof verifier contract
│
├── proof-of-lock/                # Proof-of-Lock contracts
│
├── advanced_interoperability.py  # Advanced interoperability logic
├── bitcoin_bridge.py            # Bitcoin bridge implementation
├── ethereum_bridge.py           # Ethereum bridge implementation
├── polygon_bridge.py            # Polygon bridge implementation
├── QuantumProofVerifier.sol     # Main proof verifier
└── real_metaprogrammable.py     # Metaprogrammable token contracts
```

## 🔧 Components

### EVM Contracts (`evm/`)

- **QuantumProofVerifier.sol** - Solidity contract for verifying ZK proofs on EVM chains

### Bridge Implementations

- **Bitcoin Bridge** - Bitcoin blockchain integration
- **Ethereum Bridge** - Ethereum blockchain integration
- **Polygon Bridge** - Polygon blockchain integration

### Advanced Features

- **Advanced Interoperability** - Enhanced cross-chain functionality
- **Metaprogrammable Tokens** - Tokens with adaptive behavior

## 📚 Usage

### Deploying Contracts

```bash
# Deploy to Ethereum testnet
python contracts/ethereum_bridge.py

# Deploy to Polygon testnet
python contracts/polygon_bridge.py
```

### Verifying Contracts

Contracts can be verified on block explorers (Etherscan, Polygonscan) using the source code in this directory.

## 🔗 Related

- [Main README](../README.md)
- [Architecture Documentation](../docs/ARCHITECTURE.md)
- [Core Interoperability](../core/interoperability/)

