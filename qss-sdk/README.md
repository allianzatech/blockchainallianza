# @allianza/qss-js

🔐 **Quantum Security Service SDK** - Bring quantum-resistant security to any blockchain

[![npm version](https://img.shields.io/npm/v/@allianza/qss-js)](https://www.npmjs.com/package/@allianza/qss-js)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

The **first SDK in the world** that enables any blockchain to use quantum-resistant cryptography (PQC) without native support.

## 🚀 Quick Start

```bash
npm install @allianza/qss-js
```

```typescript
import QSS from '@allianza/qss-js';

// Generate quantum proof for any blockchain transaction
const proof = await QSS.generateProof('bitcoin', txid);

// Verify the proof
const result = await QSS.verifyProof(proof);
console.log('Valid:', result.valid);

// Anchor proof on Bitcoin
const instructions = await QSS.anchorOnBitcoin(proof, 'tb1q...');
```

## 📖 Documentation

### Basic Usage

#### Generate Quantum Proof

```typescript
import QSS from '@allianza/qss-js';

// Generate proof for Bitcoin transaction
const proof = await QSS.generateProof('bitcoin', 'abc123...', {
  block_height: 12345,
  amount: '0.01'
});

console.log('Proof Hash:', proof.proof_hash);
console.log('Signature Scheme:', proof.quantum_signature_scheme);
```

#### Verify Proof

```typescript
const result = await QSS.verifyProof(proof);

if (result.valid) {
  console.log('✅ Proof is valid!');
  console.log('Signature valid:', result.verification_details?.signature_valid);
  console.log('Merkle proof valid:', result.verification_details?.merkle_proof_valid);
} else {
  console.log('❌ Proof is invalid');
}
```

#### Anchor on Bitcoin

```typescript
// Get anchor instructions
const instructions = await QSS.anchorOnBitcoin(proof, 'tb1q...');

// instructions.data contains OP_RETURN data
// Use with your Bitcoin library (e.g., bitcoinjs-lib)
console.log('OP_RETURN data:', instructions.data);
```

#### Anchor on Ethereum/Polygon

```typescript
import { ethers } from 'ethers';

const { instructions, transactionData } = await QSS.anchorOnEVM(
  proof,
  '0x...', // QuantumSecurityAdapter contract address
  'ethereum'
);

// Sign and send transaction
const signer = new ethers.Wallet(privateKey, provider);
const tx = await signer.sendTransaction(transactionData);
await tx.wait();
```

### Advanced Usage

#### Custom Configuration

```typescript
import { QSSClient } from '@allianza/qss-js';

const client = new QSSClient({
  apiUrl: 'https://api.allianza.tech/qss',
  timeout: 60000,
  apiKey: 'your-api-key'
});

const proof = await client.generateProof('ethereum', txHash);
```

#### Using Blockchain Helpers

```typescript
import { BitcoinAnchor, EVMAnchor } from '@allianza/qss-js';

// Create OP_RETURN data
const opReturnData = BitcoinAnchor.createOPReturnData(proofHash);

// Extract proof hash from OP_RETURN
const extractedHash = BitcoinAnchor.extractProofHash(opReturnData);

// Create EVM transaction
const txData = EVMAnchor.createAnchorTransaction(contractAddress, proofHash);
```

## 🌐 Supported Blockchains

- ✅ **Bitcoin** (via OP_RETURN)
- ✅ **Ethereum** (via Smart Contracts)
- ✅ **Polygon** (via Smart Contracts)
- ✅ **BSC** (via Smart Contracts)
- ✅ **Solana** (via Account Data)
- ✅ **Cosmos** (via IBC)
- ✅ **Avalanche** (via Smart Contracts)
- ✅ **Any EVM-compatible chain**

## 🔐 Security Features

- **ML-DSA** (Dilithium) - NIST PQC Standard
- **SPHINCS+** - Hash-based signatures
- **QRS-3** - Triple redundancy (ECDSA + ML-DSA + SPHINCS+)
- **Merkle Proofs** - Verifiable inclusion proofs
- **Consensus Proofs** - Blockchain finality verification

## 📚 API Reference

### `QSS.generateProof(chain, txHash, metadata?)`

Generate a quantum proof for a transaction.

**Parameters:**
- `chain` (string): Blockchain name (bitcoin, ethereum, polygon, etc.)
- `txHash` (string): Transaction hash
- `metadata` (object, optional): Transaction metadata

**Returns:** `Promise<QuantumProof>`

### `QSS.verifyProof(proof)`

Verify a quantum proof.

**Parameters:**
- `proof` (QuantumProof): Quantum proof object

**Returns:** `Promise<VerificationResult>`

### `QSS.anchorOnBitcoin(proof, targetAddress?)`

Get anchor instructions for Bitcoin.

**Parameters:**
- `proof` (QuantumProof): Quantum proof object
- `targetAddress` (string, optional): Bitcoin address

**Returns:** `Promise<AnchorInstructions>`

### `QSS.anchorOnEVM(proof, contractAddress, targetChain?)`

Get anchor instructions and transaction data for EVM chains.

**Parameters:**
- `proof` (QuantumProof): Quantum proof object
- `contractAddress` (string): QuantumSecurityAdapter contract address
- `targetChain` (string, optional): Target chain (default: 'ethereum')

**Returns:** `Promise<{instructions, transactionData}>`

## 🎯 Use Cases

### 1. Cross-Chain Bridges

```typescript
// Bridge transaction from Polygon to Bitcoin
const polygonTx = '0x...';
const proof = await QSS.generateProof('polygon', polygonTx);

// Anchor proof on Bitcoin
await QSS.anchorOnBitcoin(proof);
```

### 2. Exchange Security

```typescript
// Generate proof for exchange withdrawal
const withdrawalTx = '0x...';
const proof = await QSS.generateProof('ethereum', withdrawalTx);

// Verify before processing
const result = await QSS.verifyProof(proof);
if (result.valid) {
  // Process withdrawal
}
```

### 3. DeFi Protocol Protection

```typescript
// Protect smart contract interactions
const swapTx = '0x...';
const proof = await QSS.generateProof('polygon', swapTx);

// Anchor on-chain for verification
const { transactionData } = await QSS.anchorOnEVM(proof, contractAddress);
```

## 🔗 Links

- **Documentation**: [https://docs.allianza.tech/qss](https://docs.allianza.tech/qss)
- **API Status**: [https://testnet.allianza.tech/api/qss/status](https://testnet.allianza.tech/api/qss/status)
- **Explorer**: [https://testnet.allianza.tech/verify-proof](https://testnet.allianza.tech/verify-proof)
- **GitHub**: [https://github.com/allianza-blockchain/qss-sdk-js](https://github.com/allianza-blockchain/qss-sdk-js)

## 📄 License

MIT

## 🤝 Contributing

Contributions are welcome! Please read our [Contributing Guide](CONTRIBUTING.md) first.

## ⚠️ Disclaimer

This SDK is in active development. Use at your own risk in production environments.

---

**Made with ❤️ by Allianza Blockchain**

🔐 **The Chainlink of Quantum Security**

