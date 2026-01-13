# ✅ Verifiable On-Chain Proofs - Allianza Blockchain

This document contains **real, verifiable transaction hashes** from public blockchains that demonstrate Allianza's interoperability and quantum security capabilities. All hashes can be verified on public blockchain explorers.

## 🎯 Purpose

These proofs demonstrate:
1. **Real cross-chain interoperability** - Actual transactions on Bitcoin, Ethereum, Polygon testnets
2. **Quantum security validation** - QRS-3 proofs for real transactions
3. **Bridge-free transfers** - No traditional bridges or wrapped tokens
4. **Independent verification** - Anyone can verify these transactions on public explorers

## 📋 How to Verify

### Step 1: Check Transaction on Public Explorer
Each proof includes a link to the public blockchain explorer where you can verify the transaction.

### Step 2: Generate QRS-3 Proof
Use the Allianza testnet to generate a quantum-proof signature for the transaction:
- **Testnet QSS**: https://testnet.allianza.tech/qrs3-verifier
- **API**: `POST /api/qss/generate-proof`

### Step 3: Verify Proof
Verify the generated proof on the testnet verifier.

## ₿ Bitcoin Testnet Proofs

### Proof 1: Bitcoin Transaction Validation

**Transaction Hash:**
```
842f01a3302b6b19981204c96f377be1ec1dfc51e995f68b3a1563e6750d06e8
```

**Public Explorer:**
- **Blockstream**: https://blockstream.info/testnet/tx/842f01a3302b6b19981204c96f377be1ec1dfc51e995f68b3a1563e6750d06e8
- **BlockCypher**: https://live.blockcypher.com/btc-testnet/tx/842f01a3302b6b19981204c96f377be1ec1dfc51e995f68b3a1563e6750d06e8

**Verification:**
1. Open the explorer link above
2. Verify transaction exists and is confirmed
3. Generate QRS-3 proof using the hash above
4. Verify proof on testnet: https://testnet.allianza.tech/qrs3-verifier

### Proof 2: Bitcoin Transaction

**Transaction Hash:**
```
89b6d1b46c2a1f93bd1d9ccc95dd25b46a81c7f37cb7b2a11abbebd29ddafaeb
```

**Public Explorer:**
- **Blockstream**: https://blockstream.info/testnet/tx/89b6d1b46c2a1f93bd1d9ccc95dd25b46a81c7f37cb7b2a11abbebd29ddafaeb

## ⛽ Ethereum Sepolia Testnet Proofs

### Proof 1: Ethereum Transaction Validation

**Transaction Hash:**
```
0x9a75d8edd1af2f7239db94d799abbdec30c42870899cbdcb5d9d8df4daf27110
```

**Public Explorer:**
- **Etherscan**: https://sepolia.etherscan.io/tx/0x9a75d8edd1af2f7239db94d799abbdec30c42870899cbdcb5d9d8df4daf27110
- **Blockscout**: https://sepolia.blockscout.com/tx/0x9a75d8edd1af2f7239db94d799abbdec30c42870899cbdcb5d9d8df4daf27110

**Transaction Details:**
- **Block**: 9671202
- **From**: 0x2CdA41645F2dBffB852a605E92B185501801FC28
- **To**: 0x091382ad7490FDd0F73D2c8697Fd15aA76F218d7
- **Value**: 0.5 ETH
- **Status**: ✅ Success

**Verification:**
1. Open Etherscan link above
2. Verify transaction details match
3. Generate QRS-3 proof using the hash
4. Verify proof on testnet

### Proof 2: Ethereum Transaction

**Transaction Hash:**
```
0x286d8d6e9985ea1b423cf60bd902c850073574343694d8ccac1cca0c5e76edd6
```

**Public Explorer:**
- **Etherscan**: https://sepolia.etherscan.io/tx/0x286d8d6e9985ea1b423cf60bd902c850073574343694d8ccac1cca0c5e76edd6

## 🔷 Polygon Amoy Testnet Proofs

### Proof 1: Polygon Transaction

**Transaction Hash:**
```
0x03008e09df2465e5ce67c179cf8b86b6f533a14ddfef643612a91d833dad4008
```

**Public Explorer:**
- **Polygonscan**: https://amoy.polygonscan.com/tx/0x03008e09df2465e5ce67c179cf8b86b6f533a14ddfef643612a91d833dad4008

## 🔗 Allianza Testnet Proofs

### Faucet Transactions

All faucet transactions are visible on the Allianza testnet explorer:
- **Explorer**: https://testnet.allianza.tech/explorer
- **Faucet**: https://testnet.allianza.tech/faucet

**How to verify:**
1. Request tokens from faucet
2. Note the transaction hash returned
3. Search for the hash in the explorer
4. Verify transaction details

## 🧪 Testing Instructions

### Test 1: Verify Bitcoin Transaction

```bash
# 1. Verify on Blockstream
# Open: https://blockstream.info/testnet/tx/842f01a3302b6b19981204c96f377be1ec1dfc51e995f68b3a1563e6750d06e8

# 2. Generate QRS-3 proof
curl -X POST https://testnet.allianza.tech/api/qss/generate-proof \
  -H "Content-Type: application/json" \
  -d '{
    "chain": "bitcoin",
    "tx_hash": "842f01a3302b6b19981204c96f377be1ec1dfc51e995f68b3a1563e6750d06e8"
  }'

# 3. Verify proof on testnet
# Open: https://testnet.allianza.tech/qrs3-verifier
```

### Test 2: Verify Ethereum Transaction

```bash
# 1. Verify on Etherscan
# Open: https://sepolia.etherscan.io/tx/0x9a75d8edd1af2f7239db94d799abbdec30c42870899cbdcb5d9d8df4daf27110

# 2. Generate QRS-3 proof
curl -X POST https://testnet.allianza.tech/api/qss/generate-proof \
  -H "Content-Type: application/json" \
  -d '{
    "chain": "ethereum",
    "tx_hash": "0x9a75d8edd1af2f7239db94d799abbdec30c42870899cbdcb5d9d8df4daf27110"
  }'

# 3. Verify proof on testnet
# Open: https://testnet.allianza.tech/qrs3-verifier
```

## 📊 Proof Summary

| Chain | Transaction Hash | Explorer Link | Status |
|-------|-----------------|---------------|--------|
| Bitcoin | `842f01a3...` | [Blockstream](https://blockstream.info/testnet/tx/842f01a3302b6b19981204c96f377be1ec1dfc51e995f68b3a1563e6750d06e8) | ✅ Verified |
| Ethereum | `0x9a75d8ed...` | [Etherscan](https://sepolia.etherscan.io/tx/0x9a75d8edd1af2f7239db94d799abbdec30c42870899cbdcb5d9d8df4daf27110) | ✅ Verified |
| Polygon | `0x03008e09...` | [Polygonscan](https://amoy.polygonscan.com/tx/0x03008e09df2465e5ce67c179cf8b86b6f533a14ddfef643612a91d833dad4008) | ✅ Verified |

## 🔍 Independent Verification

### For Auditors

1. **Verify Transactions**: Use the explorer links to verify each transaction exists
2. **Check Details**: Verify transaction details (amount, addresses, block number)
3. **Generate Proofs**: Use Allianza testnet to generate QRS-3 proofs
4. **Verify Proofs**: Verify proofs on the testnet verifier
5. **Cross-Reference**: Compare with `COMPLETE_TECHNICAL_PROOFS_FINAL.json`

### For Developers

1. **Clone Repository**: `git clone https://github.com/dieisonmaach-lang/allianzablockchain.git`
2. **Run Tests**: `python tests/public/run_verification_tests.py`
3. **Check Source Code**: Review `core/` directory for implementation
4. **Verify Algorithms**: Check `core/crypto/` for PQC implementations

## 📝 Notes

- All proofs use **testnet** transactions for safety
- All transaction hashes are **publicly verifiable** on blockchain explorers
- QRS-3 proofs can be generated and verified on the Allianza testnet
- Source code for core implementations is available in `core/` directory

## 🔗 Related Documentation

- [VERIFICATION.md](VERIFICATION.md) - Complete verification guide
- [TESTING.md](TESTING.md) - Testing instructions
- [COMPLETE_TECHNICAL_PROOFS_FINAL.json](COMPLETE_TECHNICAL_PROOFS_FINAL.json) - Complete technical proofs

---

**Last updated**: 2025-12-07

**Note**: This document is updated regularly with new verifiable proofs. Check the repository for the latest version.

