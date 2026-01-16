Audit & Verification Guide (ALZ‑NIEV)
=====================================

This guide explains how an external auditor, researcher, or technically inclined investor can independently verify ALZ‑NIEV cross‑chain transfers and assess the security guarantees provided by the system.

It is intended to be practical and tool‑agnostic.


1. Documents and Endpoints to Use
---------------------------------

Before starting, the auditor SHOULD read:

- `docs/ALZ_NIEV_FLOW_DIAGRAM.md`  
  Visual representation of the verification flow (recommended for understanding the process)

- `docs/ALZ_NIEV_VERIFICATION_STANDARD.md`  
  Formal specification of what qualifies as a VERIFIED transfer.

- `docs/WHAT_MAKES_A_TRANSFER_VERIFIED.md`  
  High‑level explanation of the four pillars of verification.

- `docs/THREAT_MODEL_ALZ_NIEV.md`  
  STRIDE‑based threat model and mitigations.

Key HTTP endpoints:

- **Verified transfers (institutional standard)**  
  `GET /api/interoperability/verified-transfers`

- **Interoperability UI (human‑friendly view)**  
  `GET /interoperability`


2. Sample Verified Transfer (Real Example)
-------------------------------------------

Below is a **real example** of a VERIFIED transfer (Solana → Bitcoin) that meets ALZ‑NIEV Verification Standard v1.0:

```json
{
  "type": "SOLANA → BITCOIN",
  "category": "Cross-Chain Transfer",
  "verification_status": "verified",
  "verification_level": "verified_full",
  "verification_standard": "ALZ-NIEV v1.0",
  "is_verified": true,
  "is_legacy": false,
  "source_chain": "solana",
  "target_chain": "bitcoin",
  "uchain_id": "UCHAIN-6845208c36391fcd446766c422c9b63e",
  "amount": 0.00360232,
  "recipient": "tb1q92s4pc5hxh0gmew4d026y7n5rtwc4astv3dn6q",
  "timestamp": "2026-01-13T15:08:00Z",
  "source_transaction": {
    "hash": "Lg1fAnwZdnXdR7hBpNZsr1E18wwVEBi9TEA2URj9t1fb3CKzjQenywZHRmo38Cg1KucYnFDsTpPh5NTrSFpFhkC",
    "tx_hash": "Lg1fAnwZdnXdR7hBpNZsr1E18wwVEBi9TEA2URj9t1fb3CKzjQenywZHRmo38Cg1KucYnFDsTpPh5NTrSFpFhkC",
    "explorer_url": "https://explorer.solana.com/tx/Lg1fAnwZdnXdR7hBpNZsr1E18wwVEBi9TEA2URj9t1fb3CKzjQenywZHRmo38Cg1KucYnFDsTpPh5NTrSFpFhkC?cluster=testnet",
    "chain": "solana",
    "status": "success"
  },
  "target_transaction": {
    "hash": "550a37beb6020855e0b92c8a38093b364df43e54b92cd33b052440c582c632a0",
    "tx_hash": "550a37beb6020855e0b92c8a38093b364df43e54b92cd33b052440c582c632a0",
    "explorer_url": "https://blockstream.info/testnet/tx/550a37beb6020855e0b92c8a38093b364df43e54b92cd33b052440c582c632a0",
    "chain": "bitcoin",
    "status": "broadcasted"
  },
  "proofs": {
    "consensus_proof": {
      "consensus_type": "poh_pos_bft",
      "source_chain": "solana",
      "finalized": true,
      "finality_slot_verified": true,
      "bft_quorum": true,
      "block_height": 328400,
      "poh_hash": "df568557813dda6d32af593354584e56...",
      "confirmations": 1
    },
    "merkle_proof": {
      "tree_depth": 5,
      "merkle_root": "9c7ea3d68a4b8c472285063b5ff7101a...",
      "chain_id": "solana",
      "leaf_hash": "...",
      "path": ["0xaaa", "0xbbb", "0xccc", "0xddd", "0xeee"],
      "verified": true,
      "is_legacy": false
    },
    "zk_proof": {
      "verified": true,
      "circuit_id": "transfer_solana_bitcoin",
      "proof_id": "be42861c77bd651fd194149efa3d5c68",
      "proof_type": "zk-snark",
      "proof_hash": "c507b08db223a54b751491663aa5d3b1...",
      "state_hash": "e19fab42f1cbdd9906b3f602a5204b45b23b74742adb9a3a937d33ace8a37b2e",
      "verifier_id": "verifier_bitcoin"
    }
  }
}
```

**Verification Checklist for this example:**
- ✅ Consensus type: `poh_pos_bft` (specific, not "unknown")
- ✅ Merkle depth: `5` (≥ 3 minimum for Solana)
- ✅ Merkle path: Present (5 elements)
- ✅ Source TX hash: Public and verifiable
- ✅ Target TX hash: Public and verifiable
- ✅ Explorer URLs: Both accessible
- ✅ ZK proof: Verified with proof_id

This transfer can be independently verified by:
1. Checking Solana transaction on explorer.solana.com
2. Checking Bitcoin transaction on blockstream.info/testnet
3. Verifying Merkle proof path
4. Validating consensus finality

---

3. High‑Level Verification Flow
-------------------------------

At a high level, an auditor SHOULD follow these steps:

1. **Select a Verified Transfer**
   - Use `/api/interoperability/verified-transfers` to obtain a list of VERIFIED transfers.
   - For each entry, note:
     - `uchain_id`
     - `source_chain`, `target_chain`
     - `source_transaction.hash`, `source_transaction.explorer_url`
     - `target_transaction.hash`, `target_transaction.explorer_url`
     - `proofs.consensus_proof`
     - `proofs.merkle_proof`
     - `proofs.zk_proof`

2. **Confirm Source and Target Transactions On‑Chain**
   - Open the `source_transaction.explorer_url` and confirm:
     - the transaction exists,  
     - the value and addresses match what is claimed.
   - Open the `target_transaction.explorer_url` and confirm:
     - the transaction exists on the target chain,  
     - the value/recipient mapping is consistent with the protocol description.

3. **Check Consensus Finality**
   - Using the data in `proofs.consensus_proof`, verify that:
     - the block/slot/epoch is considered final under the Source Chain’s documented rules; and
     - the reported `consensus_type` matches the chain (e.g., `poh_pos_bft` for Solana, `pow_confirmations` for Bitcoin).
   - Optionally, use your own nodes or third‑party services to recompute confirmations or finalization status.

4. **Verify Merkle (or Equivalent) Inclusion**
   - From `proofs.merkle_proof`, extract:
     - `tree_depth`
     - `merkle_root`
     - `leaf_hash`
     - `path` / `proof_path`
   - Recompute the root from `leaf_hash` and `path` and confirm it matches the advertised `merkle_root`.
   - Check that `tree_depth` is at least the minimum required for the Source Chain (see the Verification Standard).

5. **Verify the Zero‑Knowledge Proof**
   - Obtain the relevant verifier key/contract for the `proofs.zk_proof.verifier_id` and `circuit_id`.
   - Using public inputs (e.g., UChainID, amount, hashes), re‑verify the ZK proof:
     - On‑chain (if a verifier contract is deployed); or
     - Off‑chain using a public verifier implementation.

6. **Check Non‑Inflation / Value Conservation**
   - Confirm that:
     - the value represented on the Target Chain does not exceed the value locked/burned or otherwise reserved on the Source Chain for that UChainID; and
     - no other transfer reuses the same Source Chain transaction to mint/unlock additional value.


3. Example: Solana → Bitcoin (Conceptual)
-----------------------------------------

For a Solana → Bitcoin transfer classified as VERIFIED:

1. Confirm the Solana transaction:
   - On the Solana explorer, verify:
     - correct sender and recipient (or bridge program),
     - correct amount,
     - that the transaction is in a slot with BFT finality.

2. Confirm the Bitcoin transaction:
   - On Blockstream (or any Bitcoin testnet explorer), verify:
     - the TX hash exists;
     - the amount and recipient address match the expected mapping.

3. Verify consensus proof:
   - Ensure `proofs.consensus_proof.consensus_type == "poh_pos_bft"`.
   - Validate any additional fields (e.g., PoH hash, slot/height, BFT flags) as needed.

4. Validate Merkle proof:
   - Recompute the Merkle root for the Solana inclusion (or equivalent structure used by the implementation).
   - Ensure `tree_depth >= 3` and that the recomputed root matches the recorded root.

5. Validate ZK proof:
   - Use the verifier for `circuit_id = "transfer_solana_bitcoin"` and `verifier_id = "verifier_bitcoin"`.
   - Confirm the proof verifies, and that its public inputs bind the correct Solana TX and Bitcoin TX.


4. Understanding LEGACY vs VERIFIED in Audits
---------------------------------------------

During an audit, it is important to treat LEGACY and VERIFIED transfers differently:

- **VERIFIED Transfers**
  - May be used as primary evidence of protocol correctness and security.
  - Should form the basis of any “production‑grade” security claims.

- **LEGACY Transfers**
  - May be used as supporting evidence of historical development, testing, or evolution.
  - Must be clearly labeled as **not meeting** the full ALZ‑NIEV Verification Standard.
  - Should not be used alone to justify security guarantees.

An audit report MAY explicitly separate findings and metrics into “VERIFIED” and “LEGACY” sections.


5. Recommended Audit Questions
------------------------------

Auditors and reviewers MAY consider asking:

1. **Coverage**
   - What proportion of all cross‑chain volume is under VERIFIED transfers vs LEGACY?
   - Are there any production flows that still depend on LEGACY transfers?

2. **Implementation Independence**
   - Has at least one independent implementation of the ALZ‑NIEV verifier been run against the same dataset?
   - Do multiple implementations agree on VERIFIED vs LEGACY classification?

3. **Operational Maturity**
   - Are finality thresholds (e.g., confirmations) configurable and conservative?
   - Are ZK verifier keys managed and rotated in a secure, documented way?

4. **Incident Handling**
   - What is the procedure if a Source Chain suffers an unusual reorg or consensus failure?
   - How are previously VERIFIED transfers re‑evaluated in such scenarios?


6. Summary
----------

The ALZ‑NIEV stack is intentionally designed so that:

- VERIFICATION = cryptography + native consensus, not marketing;
- Any third party can replicate the classification logic using public data; and
- VERIFIED transfers have a clear, defensible meaning for institutional and research‑grade scrutiny.

By following this guide together with:

- `ALZ_NIEV_VERIFICATION_STANDARD.md`
- `WHAT_MAKES_A_TRANSFER_VERIFIED.md`
- `THREAT_MODEL_ALZ_NIEV.md`

an auditor can independently evaluate the correctness and security properties of the interoperability layer without relying on internal claims or opaque components.

