What Makes a Transfer VERIFIED?
===============================

This document explains, in practical terms, what it means for a cross-chain transfer to be **VERIFIED** under the ALZ‑NIEV Verification Standard v1.0, and how this differs from a **LEGACY** transfer.

It is intended for engineers, auditors, and technically inclined investors who want a clear, high‑level view without reading the full formal specification.


1. Two Classes of Transfers
---------------------------

Under ALZ‑NIEV there are only two categories:

- **VERIFIED Transfer**
  - Meets all cryptographic and consensus requirements.
  - Can be independently re‑verified by any third party.
  - Suitable for institutional due diligence and security‑critical flows.

- **LEGACY Transfer**
  - Does **not** meet at least one requirement (e.g. missing Merkle proof, incomplete consensus data, or no public TX hashes).
  - May be useful for testing, early versions, or historical exploration.
  - MUST NOT be treated as having the same security guarantees as VERIFIED transfers.

The system and UI MUST always make this distinction explicit. There is **no "half‑verified" state**.

### Verification Levels

- **`verified_full`**: All 4 pillars present and valid (meets ALZ-NIEV v1.0 standard)
- **`verified_l2_only`**: L2-specific verification (future: e.g., Polygon without L1 anchor)
- **`legacy_partial`**: Incomplete proofs (missing consensus type, Merkle path, or TX hashes)

All verified transfers include `"verification_standard": "ALZ-NIEV v1.0"` in their JSON metadata.


2. The Four Pillars of a VERIFIED Transfer
------------------------------------------

A transfer is considered VERIFIED only when **all four** of the following are true.

### 2.1 Consensus Finality (Source Chain)

The Source Chain MUST have finalized the transaction that initiates the cross‑chain transfer, under its **native** consensus rules.

Examples:

- **Bitcoin**: the transaction is in a block with at least *N* confirmations (typically ≥ 6), and the block headers and proof‑of‑work are valid.
- **Ethereum**: the transaction is in a block that lies within a **finalized checkpoint** according to Casper FFG.
- **Solana**: the transaction is in a slot that has reached BFT finality under Tower.
- **Polygon (PoS)**: the transaction’s block is part of an epoch whose checkpoint is anchored and finalized on Ethereum L1.

If finality is not demonstrable from publicly verifiable data, the transfer CANNOT be classified as VERIFIED.


### 2.2 Merkle (or Equivalent) Inclusion Proof

There MUST be a cryptographic proof that the relevant transaction or state leaf is included in a specific block.

This proof:

- Contains a leaf hash (encoding UChainID, transaction hash, etc.);
- Contains a path of sibling hashes sufficient to recompute the block’s Merkle (or equivalent) root; and
- Is bound to a block that is itself proven finalized by the consensus module.

Minimum depth requirements (guideline values):

- EVM chains (Polygon, Ethereum, BSC, Base, Avalanche): depth ≥ 2.
- Solana: depth ≥ 3.
- Bitcoin: depth ≥ 6 (or UTXO‑equivalent path length).

If the depth is 0 or the path is missing/empty, the proof is considered **insufficient** for VERIFIED classification.


### 2.3 Zero‑Knowledge Proof of Correctness

A ZK proof (zk‑SNARK, zk‑STARK, or equivalent) MUST prove that:

1. The Source Chain transaction and its state changes match the claimed:
   - UChainID,
   - amount,
   - sender/recipient mapping.
2. The Target Chain effect (e.g. credit, unlock, mint) does not exceed the value provably locked or burned on the Source Chain.
3. No double‑mint or replay is possible from the same Source Chain transaction.

This proof MUST be verifiable using a public verifier key or contract.  
Anyone with public chain data and the verifier key MUST be able to validate the proof independently.


### 2.4 Public TX Hashes and Explorers

Both sides of the transfer MUST be independently auditable:

- **Source transaction**: public transaction hash + canonical explorer URL.
- **Target transaction**: public transaction hash + canonical explorer URL.

If a user, auditor, or indexer cannot click through to both transactions and see them on public infrastructure (or reproduce the view from raw RPC data), the transfer is NOT fully auditable and MUST NOT be labeled VERIFIED.


3. How the System Decides: VERIFIED vs LEGACY
---------------------------------------------

Internally, the system evaluates a transfer against a small set of boolean conditions:

```python
is_verified = (
    consensus_type != "unknown" and
    merkle_depth >= min_depth_for_chain and
    has_merkle_path and
    has_source_tx_hash and
    has_target_tx_hash and
    has_source_explorer_url and
    has_target_explorer_url and
    zk_proof_verified
)
```

If `is_verified` is `True`, the transfer is classified as **VERIFIED**.  
Otherwise, it is classified as **LEGACY**.

The UI and APIs MUST expose this classification explicitly via fields such as:

- `verification_status: "verified" | "legacy"`
- `is_verified: true/false`
- `is_legacy: true/false`


4. How to Read VERIFIED Transfers in the UI
-------------------------------------------

In a typical implementation:

- The **“Live Verified Cross‑Chain Transfers”** view:
  - Shows only transfers where `is_verified == true`;
  - Displays a green “Verified” badge;
  - Shows both Source and Target TX hashes and explorer links.

- Legacy transfers:
  - Either do not appear in that list, or
  - Are clearly labeled with a yellow “Legacy” badge and an explicit warning:
    - e.g. “This transfer does not include complete consensus or Merkle proofs.”

This makes it impossible to confuse a test/legacy entry with a fully verified transfer.


5. When to Use VERIFIED vs LEGACY
---------------------------------

- Use **VERIFIED**:
  - In any security‑critical flow involving value or user funds;
  - In documentation, demos, or dashboards presented to auditors or institutional partners;
  - As the baseline for all external reporting (e.g. “X cross‑chain transfers, Y VERIFIED under ALZ‑NIEV v1.0”).

- Use **LEGACY**:
  - For historical compatibility with earlier test runs;
  - For development, QA, or stress‑test data;
  - With explicit warnings, never as evidence of full cryptographic security.


6. Summary
----------

A transfer is **VERIFIED** when:

- The Source Chain state is **final** under its native consensus;
- There is a **Merkle (or equivalent) inclusion proof** with sufficient depth and path;
- A **ZK proof** attests to correct, non‑inflationary state transition; and
- Both Source and Target sides are **publicly auditable** via transaction hashes and explorers.

Any transfer that fails one or more of these conditions is **LEGACY** by design.

The ALZ‑NIEV Verification Standard v1.0, together with this document, provides a clear and defensible line between “appears to work” and “cryptographically proven and independently verifiable”.

What Makes a Transfer VERIFIED?
===============================

Context
-------

This document explains, in practical and precise terms, what it means for a cross-chain transfer to be classified as **VERIFIED** under the **ALZ-NIEV Verification Standard v1.0**.
It is intended for engineers, auditors, and technically minded investors who want a clear mental model of the guarantees provided by a VERIFIED transfer versus a LEGACY one.


High-Level Intuition
--------------------

A VERIFIED transfer is **not** “a transaction that went through without errors”.  
It is a transfer for which the system can prove, to any independent verifier, that:

1. The transaction **really happened** on the Source Chain.
2. The Source Chain has **finalized** that transaction under its native consensus rules.
3. The Target Chain effect (mint/unlock/accounting) **exactly matches** the locked/burned amount on the Source Chain.
4. No additional value was created or double-counted elsewhere.
5. All of the above can be checked **independently from public data**, without trusting a specific relayer or server.


Formal Criteria (Operational View)
----------------------------------

A cross-chain transfer is considered **VERIFIED** if and only if **all** of the following are true:

1. **Consensus Type is Specific and Valid**
   - The transfer is tagged with a concrete `consensus_type` that corresponds to the Source Chain:
     - `pos_bor_checkpoint` (Polygon)
     - `pos_finality` (Ethereum)
     - `poh_pos_bft` (Solana)
     - `pow_confirmations` (Bitcoin)
     - `pos_bsc`, `pos_op_stack`, `pos_avalanche`, etc.
   - `consensus_type` must **never** be `unknown` for a VERIFIED transfer.

2. **Merkle Proof Has Sufficient Depth and a Real Path**
   - The Merkle (or equivalent) proof has:
     - A non-zero `tree_depth`; and
     - A non-empty `path` (or `proof_path`) of sibling hashes.
   - The effective depth must be at least the chain-specific minimum:
     - EVM chains (Polygon, Ethereum, BSC, Base, Avalanche): depth ≥ 2
     - Solana: depth ≥ 3
     - Bitcoin: depth ≥ 6
   - Depth `0` or an empty path implies **no real inclusion proof**, therefore the transfer cannot be VERIFIED.

3. **Native Finality Is Proven**
   - The block that contains the Source Chain transaction is shown to be finalized according to that chain’s consensus rules.
   - Example conditions:
     - Bitcoin: transaction included in a block with ≥ 6 confirmations and valid PoW chain.
     - Solana: transaction included in a slot that has reached Tower BFT finality.
     - Polygon: transaction in an epoch that has a checkpoint anchored on Ethereum.
     - Ethereum: transaction in a block that is part of a finalized checkpoint.

4. **Zero-Knowledge Proof of Correctness**
   - A ZK proof (e.g., zk-SNARK) links:
     - The Source Chain transaction (UChainID, amount, recipient mapping); and
     - The Target Chain effect (mint/unlock/accounting).
   - The proof ensures:
     - No extra value is minted/unlocked.
     - No double-mint/double-spend is possible from the same Source event.
     - The state transition follows the protocol’s rules.

5. **Public TX Hashes and Explorer Links**
   - The JSON representation of the transfer includes:
     - `source_transaction.hash` (or `tx_hash`) and an `explorer_url` for the Source Chain.
     - `target_transaction.hash` (or `tx_hash`) and an `explorer_url` for the Target Chain.
   - Anyone can click the links or query the explorers directly to confirm the on-chain reality.

6. **No Hidden Trust Assumptions**
   - The verification procedure does **not** rely on:
     - a single trusted relayer,
     - a proprietary database,
     - or opaque, unverifiable off-chain logic.
   - All critical data can be reconstructed from:
     - public chain data (nodes, explorers);
     - published verification keys;
     - and the proofs embedded in the system (ZK + Merkle + consensus metadata).


How VERIFIED vs LEGACY Appears in the System
--------------------------------------------

In the ALZ-NIEV-based implementation:

- Each transfer carries a classification:
  - `verified` / `is_verified: true` → all criteria met.
  - `legacy` / `is_legacy: true` → one or more criteria missing.

- The **Verified Transfers API** (e.g. `/api/interoperability/verified-transfers`) returns only transfers that:
  - have a specific `consensus_type` (not `unknown`);
  - have Merkle depth ≥ minimum and a non-empty proof path;
  - expose public TX hashes for both Source and Target;
  - have ZK and consensus metadata consistent with the standard.

- The UI:
  - Shows a green **Verified** badge for VERIFIED transfers.
  - Shows a yellow **Legacy** badge and an explicit warning for legacy entries.


Practical Interpretation for Auditors
-------------------------------------

When auditing a transfer labeled as **VERIFIED**, you can assume:

1. The Source Chain transaction can be independently located and confirmed on-chain.
2. The Target Chain effect is cryptographically linked to that Source transaction via ZK and Merkle proofs.
3. The Source Chain consensus has finalized the relevant block under its own rules.
4. No off-chain actor can, on their own, forge such a VERIFIED transfer without breaking:
   - the underlying consensus security assumptions; or
   - the cryptographic assumptions of the ZK/Merkle systems.

When auditing a **LEGACY** transfer, you should treat it as:

- a historical or testing artifact;
- not meeting the full ALZ-NIEV Verification Standard v1.0;
- unsuitable as primary evidence of secure interoperability.


Summary
-------

- **VERIFIED** means:  
  *“This transfer is fully backed by consensus, Merkle inclusion, and ZK proofs, and can be re-verified independently from public data, without trusting our infrastructure.”*

- **LEGACY** means:  
  *“This transfer exists in the system, but does not meet the full verification standard and MUST NOT be treated as a cryptographically strong proof of interoperability.”*

What Makes a Transfer VERIFIED (ALZ‑NIEV)
=========================================

Overview
--------

This document explains, in practical terms, what it means for a cross‑chain transfer to be classified as **VERIFIED** under the *ALZ‑NIEV Verification Standard v1.0*, and how this differs from a **LEGACY** transfer.

It is written for:
- security reviewers and auditors,
- protocol researchers,
- sophisticated investors and partners,
- engineers integrating with ALZ‑NIEV.

The normative, formal definition is given in `ALZ_NIEV_VERIFICATION_STANDARD.md`.  
This document is the human‑readable companion.


Core Idea
---------

A transfer is **VERIFIED** if an independent third party, with only public data, can reconstruct and validate all of the following, **without trusting any bridge operator, relayer, or centralized service**:

1. What happened on the **Source Chain** (state transition).
2. That this state is **final** under the Source Chain’s own consensus.
3. That the state is **correctly mapped** into the **Target Chain**.
4. That **no extra value** was created in the process.

If any of these elements is missing, incomplete, or opaque, the transfer is classified as **LEGACY**.


The Four Pillars of a VERIFIED Transfer
---------------------------------------

### 1. Consensus Finality (Source Chain)

**Question:**  
“How do I know this transaction will not be reverted on the Source Chain?”

**Requirement (high‑level):**
- There must be a machine‑checkable proof that the block containing the transfer has reached *finality* according to the Source Chain’s native consensus rules.

Examples:
- **Bitcoin:** block header chain + proof‑of‑work + ≥ 6 confirmations.
- **Ethereum:** inclusion in a finalized checkpoint (Casper FFG).
- **Solana:** inclusion in a slot finalized by Tower BFT.
- **Polygon PoS:** inclusion in a block belonging to an epoch that is checkpointed and finalized on Ethereum L1.

If finality cannot be proven under the native rules of the chain, the transfer **cannot** be considered VERIFIED.


### 2. Merkle Inclusion Proof (Source Chain)

**Question:**  
“How do I know this specific transaction or state is really inside that finalized block?”

**Requirement (high‑level):**
- A **Merkle (or equivalent) proof** must:
  - start from a leaf representing the transaction/state;
  - include a path of sibling hashes;
  - recompute the Merkle root of the finalized block header.

Minimum recommended depths:
- EVM (Polygon, Ethereum, BSC, Base, Avalanche): **depth ≥ 2**
- Solana: **depth ≥ 3**
- Bitcoin (UTXO inclusion): **depth ≥ 6**

If the depth is `0`, the path is missing, or the proof cannot reconstruct the root of a finalized block, the transfer is **LEGACY**.


### 3. Zero‑Knowledge Proof of Correctness

**Question:**  
“How do I know the cross‑chain logic itself is correct and non‑inflationary?”

**Requirement (high‑level):**
- A **ZK proof** (zk‑SNARK/zk‑STARK or equivalent) must attest that:
  - the Source Chain state transition is valid;
  - the amounts and recipients on the Target Chain match the “locked/burned” amounts on the Source Chain;
  - no duplicate or hidden state allows double‑mint or replay for the same UChainID.

Key properties:
- The proof is **succinct**: fast to verify.
- The verifier and public inputs are **publicly known**.
- Anyone can re‑verify the proof off‑chain or on‑chain.

If no ZK proof exists, or if it is not publicly verifiable, the transfer is **LEGACY**.


### 4. Public TX Hashes and Explorers

**Question:**  
“How can an auditor or outsider independently re‑check all of this?”

**Requirement (high‑level):**
- Both ends of the transfer must expose:
  - `source_tx_hash` + `source_explorer_url`
  - `target_tx_hash` + `target_explorer_url`

With these, anyone can:
- click through to the official explorers;
- check confirmations, block numbers, logs, and events;
- correlate on‑chain data with the Merkle and ZK proofs.

If hashes are hidden, absent, or only available via proprietary dashboards, the transfer is **not** considered VERIFIED under ALZ‑NIEV.


Verified vs Legacy – Quick Comparison
-------------------------------------

| Dimension                | VERIFIED                                           | LEGACY                                              |
|-------------------------|----------------------------------------------------|-----------------------------------------------------|
| Consensus finality      | Proved under native rules of Source Chain         | Missing / implicit / not machine‑checkable         |
| Merkle proof            | Depth ≥ minimum, path present, root matches block | Depth 0, no path, or not bound to finalized block  |
| ZK proof                | Exists, publicly verifiable                       | Missing, opaque, or informal                        |
| TX hashes               | Always present and clickable                      | Missing / hidden / only internal                    |
| Classification          | `verified`, institutional‑grade                   | `legacy`, for history/tests/early versions          |
| Use in claims           | Can be cited as cryptographically verified        | Must NOT be marketed as fully verified              |


How to Check a VERIFIED Transfer (Step‑by‑Step)
-----------------------------------------------

1. **Locate the UChainID** (e.g., via API or explorer).
2. **Fetch the transfer record**, including:
   - `source_transaction`, `target_transaction`,
   - `proofs.consensus_proof`, `proofs.merkle_proof`, `proofs.zk_proof`.
3. **Verify TX hashes on explorers**:
   - Confirm that the hashes exist and match the advertised chains and amounts.
4. **Verify consensus finality** using the appropriate chain‑specific module:
   - Bitcoin headers + confirmations,
   - Ethereum finalized checkpoint, etc.
5. **Verify the Merkle proof**:
   - Recompute the Merkle root and compare to the finalized block header.
6. **Verify the ZK proof**:
   - Use the public verifier contract or library to check proof validity.
7. **Check classification flags**:
   - `is_verified == true`,
   - `verification_level == "verified"`,
   - `proofs.merkle_proof.is_legacy == false`.

If all steps succeed, the transfer conforms to the ALZ‑NIEV Verification Standard v1.0.


When to Use LEGACY Transfers
----------------------------

LEGACY transfers remain useful for:
- early testnets and prototypes,
- load/stress testing,
- non‑critical demos and UX experiments,
- historical introspection of how the system evolved.

However:
- They MUST be clearly labeled as **LEGACY** in any UI.
- They MUST NOT be counted as “fully verified” in reports, audits, or marketing.


Summary
-------

In the ALZ‑NIEV model, “VERIFIED” is not a cosmetic label.  
It is a strict, cryptographic classification with:

- native consensus finality,
- Merkle inclusion with minimum depth,
- zero‑knowledge proofs of correctness,
- public transaction hashes and explorers.

Anything below this bar is explicitly and transparently classified as **LEGACY**.

