# ALZ-NIEV Cross-Chain Transfer Flow

## Visual Flow Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                    SOURCE CHAIN (e.g., Solana)                  │
│                                                                 │
│  ┌──────────────┐                                              │
│  │ Transaction  │  User initiates transfer                     │
│  │   Created    │  Amount: X tokens                            │
│  └──────┬───────┘  Recipient: Target chain address            │
│         │                                                       │
│         ▼                                                       │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │ 1. CONSENSUS PROOF                                        │ │
│  │    • Consensus Type: poh_pos_bft (Solana)                │ │
│  │    • Block Height: 328400                                │ │
│  │    • Finality Slot Verified: ✓                            │ │
│  │    • BFT Quorum: ✓                                        │ │
│  └──────────────────────────────────────────────────────────┘ │
│         │                                                       │
│         ▼                                                       │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │ 2. MERKLE INCLUSION PROOF                                 │ │
│  │    • Tree Depth: 5 (≥ minimum for Solana)               │ │
│  │    • Merkle Root: 9c7ea3d68a4b8c...                      │ │
│  │    • Proof Path: [0xaaa, 0xbbb, 0xccc, 0xddd, 0xeee]   │ │
│  │    • Leaf Hash: Transaction hash                         │ │
│  └──────────────────────────────────────────────────────────┘ │
│         │                                                       │
│         ▼                                                       │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │ 3. ZERO-KNOWLEDGE PROOF                                   │ │
│  │    • Circuit ID: transfer_solana_bitcoin                │ │
│  │    • Proof Type: zk-snark                                 │ │
│  │    • Verifier ID: verifier_bitcoin                        │ │
│  │    • State Hash: e19fab42f1cbdd...                       │ │
│  │    • Verified: ✓                                          │ │
│  └──────────────────────────────────────────────────────────┘ │
│         │                                                       │
│         ▼                                                       │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │ 4. PUBLIC TRANSACTION HASHES                              │ │
│  │    • Source TX: Lg1fAnwZdnXdR7hBpNZsr1E18wwVEBi9TEA2...  │ │
│  │    • Target TX: 550a37beb6020855e0b92c8a38093b364df43... │ │
│  │    • Explorer URLs: Publicly accessible                  │ │
│  └──────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                              │
                              │ ALZ-NIEV Protocol
                              │ (Bridge-Free, Trustless)
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                  TARGET CHAIN (e.g., Bitcoin)                   │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │ VERIFICATION ON TARGET CHAIN                             │ │
│  │                                                           │ │
│  │ ✓ Consensus proof validated                             │ │
│  │ ✓ Merkle proof verified                                 │ │
│  │ ✓ ZK proof checked                                      │ │
│  │ ✓ No double-spend detected                              │ │
│  │ ✓ Value conservation confirmed                          │ │
│  └──────────────────────────────────────────────────────────┘ │
│         │                                                       │
│         ▼                                                       │
│  ┌──────────────┐                                              │
│  │ Transaction  │  Transfer completed                          │
│  │  Broadcasted │  Amount: X tokens (converted)               │
│  └──────────────┘  Recipient: Target address                 │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Verification Levels

### `verified_full`
All 4 pillars present and valid:
- ✅ Consensus proof with specific type
- ✅ Merkle proof with depth ≥ minimum
- ✅ ZK proof verified
- ✅ Public TX hashes

### `verified_l2_only` (Future)
L2-specific verification (e.g., Polygon without L1 anchor):
- ✅ Consensus proof (L2-specific)
- ✅ Merkle proof
- ⚠️ No L1 checkpoint anchor

### `legacy_partial`
Incomplete proofs:
- ⚠️ Missing consensus type or Merkle path
- ⚠️ Depth 0 or insufficient
- ⚠️ Missing TX hashes

## Security Guarantees

Each step provides cryptographic guarantees:

1. **Consensus Proof** → Prevents reorg attacks
2. **Merkle Proof** → Proves inclusion in block
3. **ZK Proof** → Ensures correct state transition
4. **Public Hashes** → Enables independent verification

## Chain-Agnostic Design

The same flow works for:
- **Bitcoin** → PoW confirmations (6+)
- **Solana** → PoH + PoS BFT finalized slot
- **Polygon** → PoS BOR checkpoint
- **Ethereum** → PoS finality checkpoint
- **Future chains** → Define compatible finality module
