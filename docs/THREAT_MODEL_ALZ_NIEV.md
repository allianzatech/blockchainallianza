ALZ‑NIEV Threat Model
=====================

This document summarizes the primary security threats relevant to ALZ‑NIEV‑based cross‑chain transfers and the corresponding mitigation strategies.  
It is intended as a concise companion to the ALZ‑NIEV Verification Standard v1.0, written for auditors, security engineers, and protocol designers.


1. Scope and Assumptions
------------------------

ALZ‑NIEV is designed for **non‑custodial, proof‑based interoperability** between heterogeneous blockchains (e.g., Bitcoin, Solana, Polygon, Ethereum).

The following assumptions are made:

- Each underlying blockchain’s **native consensus** (PoW, PoS, BFT, etc.) behaves within its documented security model.
- Public RPC endpoints, full nodes, or archival infrastructure are available for independent verification.
- Cryptographic primitives (hash functions, Merkle trees, ZK systems) are not broken.

The model explicitly **does not** attempt to defend against:

- Complete compromise of the majority of consensus participants on a Source Chain; or
- Catastrophic breaks in foundational cryptography (e.g., hash collisions under current parameters).


2. STRIDE Overview
------------------

We use the STRIDE framework (Spoofing, Tampering, Repudiation, Information Disclosure, Denial of Service, Elevation of Privilege) to structure the threat model.


2.1 Spoofing
------------

**Threat:**  
An attacker attempts to impersonate a valid cross‑chain transfer, UChainID, or transaction without the corresponding on‑chain state.

**Examples:**
- Presenting a fake Source Chain transaction hash that never existed.
- Claiming a UChainID that is not actually bound to the stated Source Chain transaction.

**Mitigations:**
- **Merkle Inclusion Proofs**: A VERIFIED transfer MUST include a Merkle (or equivalent) inclusion proof for the Source Chain state, bound to a finalized block.
- **Consensus Finality Modules**: The block containing the transaction MUST be proven final under the Source Chain’s native consensus rules.
- **ZK Proof of Correctness**: The ZK proof MUST bind UChainID, amount, and recipient to the genuine Source Chain transaction.
- **Public Verifiability**: All necessary data (TX hashes, block identifiers, roots) is derivable from public chain state; any independent verifier can detect spoofing.


2.2 Tampering
-------------

**Threat:**  
An attacker attempts to alter transaction data, Merkle paths, or proof artifacts in transit or at rest.

**Examples:**
- Modifying leaf or sibling hashes in the Merkle path.
- Changing amounts, recipients, or block heights in off‑chain storage.

**Mitigations:**
- **Cryptographic Binding**:
  - Merkle proofs are tied to specific block roots; any tampering yields a mismatch.
  - ZK proofs are generated over precise public inputs; any modification invalidates the proof.
- **End‑to‑End Verification**:
  - Verifiers recompute Merkle roots and verify ZK proofs directly.
  - No trust is placed in intermediate relayers or databases.


2.3 Repudiation
---------------

**Threat:**  
A participant (user, relayer, or verifier) later denies that a particular cross‑chain transfer or state transition occurred.

**Examples:**
- A sender claims a transfer never happened.
- A verifier claims a transfer was never considered VERIFIED.

**Mitigations:**
- **On‑Chain Evidence**:
  - Source and Target transaction hashes are immutable on their respective chains.
  - UChainIDs are deterministically derived or recorded and can be re‑derived.
- **Deterministic Classification**:
  - The VERIFIED vs LEGACY classification is derived from explicit, documented criteria.
  - Any independent implementation of the ALZ‑NIEV standard will reach the same classification given the same inputs.


2.4 Information Disclosure
--------------------------

**Threat:**  
Sensitive information is leaked through proofs, Merkle paths, or on‑chain metadata.

**Examples:**
- Embedding raw user identifiers in Merkle leaves.
- Exposing more state than necessary in ZK public inputs.

**Mitigations:**
- **Minimal Public Inputs**:
  - ZK circuits SHOULD minimize exposed information (e.g., reveal commitments instead of full state where appropriate).
  - Merkle leaves SHOULD contain only what is necessary to link UChainID, transaction hash, and relevant state.
- **Structured Metadata**:
  - Non‑essential metadata SHOULD be kept off‑chain or behind explicit consent.

Note: ALZ‑NIEV is primarily about correctness and integrity, not confidentiality; additional privacy layers MAY be applied on top.


2.5 Denial of Service (DoS)
---------------------------

**Threat:**  
An attacker attempts to prevent verification, either by overloading verification infrastructure or by exploiting worst‑case behavior in proof systems.

**Examples:**
- Submitting very large or malformed proofs to verifiers.
- Forcing repeated reorg checks by targeting borderline‑final blocks.

**Mitigations:**
- **Verification Cost Limits**:
  - Implementations SHOULD enforce time and size limits on Merkle proofs and ZK proofs.
  - RPC calls SHOULD use conservative timeouts and fallbacks.
- **Conservative Finality**:
  - Finality thresholds (e.g., number of confirmations) SHOULD be chosen to minimize reorg handling overhead.
- **Rate Limiting and Caching**:
  - Public verification endpoints MAY apply rate limiting and caching for repeated verification of the same UChainID.


2.6 Elevation of Privilege
--------------------------

**Threat:**  
An attacker attempts to gain capabilities not allowed by the protocol, such as minting unbacked assets or bypassing verification.

**Examples:**
- Minting Target Chain assets without a corresponding locked/burned amount on the Source Chain.
- Circumventing the VERIFIED requirements while still being treated as verified by downstream systems.

**Mitigations:**
- **Non‑Inflation Guarantees**:
  - ZK proofs MUST enforce that Target Chain effects do not exceed the provably reserved value on Source Chains.
  - Accounting MUST be strictly tied to UChainIDs, preventing replay or double‑use.
- **Strict Classification Rules**:
  - Only transfers satisfying all ALZ‑NIEV requirements may be labeled VERIFIED.
  - Systems consuming this data SHOULD treat LEGACY transfers as lower‑trust and display explicit warnings.


3. Reorganizations and Cross‑Chain Consistency
----------------------------------------------

**Threat:**  
Source Chain or Target Chain reorganizations (reorgs) invalidate previously observed state, potentially leading to inconsistent cross‑chain views.

**Mitigations:**
- **Conservative Finality Thresholds**:
  - Finality modules SHOULD use robust parameters (e.g., ≥ 6 confirmations for Bitcoin) to minimize the probability of reorg beyond the finalized point.
- **Re‑verification**:
  - Systems MAY periodically re‑verify Verified Transfers against the latest canonical chain state.
  - In the rare event of a deep reorg, affected transfers MUST be downgraded from VERIFIED until new proofs are established.


4. Verifier Independence
------------------------

An important security objective of ALZ‑NIEV is that **no single implementation or operator is a point of failure** for correctness.

To that end:

- Any third party with:
  - access to public chain data;
  - Merkle and ZK verification code; and
  - the ALZ‑NIEV Verification Standard
  
  MUST be able to reproduce the VERIFIED/LEGACY classification.

- UI and API layers MUST NOT hide the underlying classification or override it with marketing language.


5. Summary
----------

ALZ‑NIEV is designed to move interoperability from a **trust‑in‑relayers** model to a **trust‑in‑cryptography and native consensus** model.

By:

- enforcing consensus finality checks;
- requiring Merkle inclusion proofs with minimum depths;
- mandating ZK proofs of non‑inflationary, correct state transitions; and
- insisting on public, independently verifiable TX hashes;

the standard provides a clear, defensible line between:

- transfers that are **cryptographically proven and independently verifiable**; and
- transfers that are **legacy or best‑effort**, useful but not at the same security level.

This document should be read together with:

- `ALZ_NIEV_VERIFICATION_STANDARD.md`
- `WHAT_MAKES_A_TRANSFER_VERIFIED.md`

to obtain a complete view of the security and verification model.

ALZ-NIEV Threat Model (STRIDE-Oriented)
=======================================

Scope
-----

This document describes a high-level threat model for the ALZ-NIEV interoperability protocol.  
It focuses on the security of **Verified Transfers** as defined by the **ALZ-NIEV Verification Standard v1.0** and assumes honest-but-curious users, potentially malicious relayers, and an adversarial network environment.


Assets
------

The primary assets to protect are:

1. **Cross-Chain Value Integrity**
   - The aggregate value on Target Chains MUST NOT exceed the value provably locked, burned, or reserved on Source Chains.

2. **Cross-Chain State Consistency**
   - UChainID-bound state transitions across chains MUST be consistent and non-contradictory.

3. **Proof Integrity**
   - ZK proofs, Merkle proofs, and consensus metadata MUST be authentic, untampered, and verifiable from public data.

4. **Auditability**
   - External auditors MUST be able to re-verify transfers without trusting proprietary infrastructure.


Adversary Model
---------------

The adversary is assumed to:

- Control arbitrary network nodes and endpoints (including relayers).
- Attempt to forge or replay cross-chain transfers.
- Attempt to exploit consensus reorganizations.
- Attempt to inflate assets by breaking accounting invariants.
- Have access to public chain data and standard cryptographic tools.

We assume:

- Underlying consensus assumptions of Bitcoin, Solana, Ethereum, Polygon, etc. hold (no majority takeover).
- Standard cryptographic primitives (hashes, signatures, ZK systems) are not broken.


STRIDE Analysis
---------------

### S — Spoofing Identity

**Threats**
- An attacker pretends to be a legitimate relayer or bridge component.
- An attacker forges messages claiming a cross-chain transfer occurred.

**Mitigations**
- VERIFIED classification does not depend on relayer identity:
  - All critical properties (Source transaction, block, Merkle root, ZK proof) are derived from public data.
- Authentication of system components (e.g., API authentication, TLS) is required operationally but is **not** relied upon for correctness of VERIFIED transfers.


### T — Tampering with Data

**Threats**
- Modification of:
  - Merkle proofs;
  - ZK proofs or verification keys;
  - consensus metadata (block heights, hashes, confirmations);
  - JSON representations of transfers (TX hashes, UChainIDs).

**Mitigations**
- Merkle proofs:
  - Any change in the leaf, path, or root breaks the recomputation and verification.
- ZK proofs:
  - Soundness: invalid proofs are rejected by the verifier.
- Consensus metadata:
  - Block hashes and heights are cross-checked against public nodes or canonical explorers.
- JSON/API tampering:
  - External verifiers recompute and cross-check against on-chain data; inconsistencies are detectable.


### R — Repudiation

**Threats**
- A party denies having initiated or processed a cross-chain transfer.

**Mitigations**
- Source Chain:
  - Transactions are signed with private keys and recorded on-chain; standard non-repudiation of blockchain transactions applies.
- Cross-Chain:
  - UChainID binds the Source transaction to the Target effect.
  - Logs and proofs include cryptographic identifiers traceable to on-chain events.


### I — Information Disclosure

**Threats**
- Leakage of sensitive information through:
  - proofs;
  - memos / metadata;
  - internal logs.

**Mitigations**
- ZK proofs:
  - Reveal only the public inputs (amount, chains, hashes) necessary for verification.
- Memos:
  - SHOULD NOT contain secrets, private keys, or raw user identifiers.
- Logs:
  - SHOULD be scrubbed of sensitive data; only public hashes and high-level metadata SHOULD be stored for audit.


### D — Denial of Service (DoS)

**Threats**
- Overloading:
  - proof generation services;
  - verification endpoints;
  - RPC nodes.
- Targeted DoS to prevent verification or finality checks.

**Mitigations**
- Rate limiting:
  - Per-IP or per-API-key limits on verification endpoints.
- Caching:
  - Cache positive verification results to avoid recomputation for the same UChainID.
- Redundancy:
  - Use multiple RPC providers and explorers where possible.
- Degradation model:
  - Under DoS, new transfers MAY be delayed but previously VERIFIED transfers remain verifiable from public data.


### E — Elevation of Privilege

**Threats**
- An attacker gains the ability to:
  - mark transfers as VERIFIED without meeting criteria;
  - bypass ZK or Merkle verification logic;
  - tamper with classification logic (VERIFIED vs LEGACY).

**Mitigations**
- Verification logic:
  - MUST be deterministic, publicly documented (via the Verification Standard), and auditable in code.
- Classification:
  - MUST be derived from objective conditions:
    - consensus_type ≠ "unknown";
    - merkle_depth ≥ minimum;
    - non-empty proof path;
    - public TX hashes + explorers.
- Separation of concerns:
  - Operational roles (e.g., devops, relayer operators) MUST NOT be able to override cryptographic checks.


Cross-Chain Specific Threats
----------------------------

1. **Replay Across Chains**
   - Reusing a Source transaction to mint/unlock value multiple times on different Target Chains.
   - Mitigation:
     - UChainID is unique per logical transfer.
     - ZK and accounting logic MUST enforce one-to-one mapping between Source events and Target effects.

2. **Partial Finality Exploits**
   - Recognizing transfers before sufficient confirmation/finality.
   - Mitigation:
     - Chain-specific finality modules enforce conservative thresholds (e.g., Bitcoin 6+ confirmations).

3. **Bridge Inflation**
   - Creating more synthetic or wrapped assets than are locked or burned at the origin.
   - Mitigation:
     - Non-inflation constraint enforced by ZK proofs and ledger accounting.
     - Public verifiability of total locked vs. total minted.


Residual Risks
--------------

The following risks are out of scope or rely on external assumptions:

- Fundamental breaks in underlying consensus (e.g., 51% attacks).
- Cryptographic breaks in hash functions, signatures, or ZK systems.
- Operational misconfigurations (e.g., wrong RPC endpoints, faulty monitoring).

Implementers SHOULD document their operational assumptions and monitoring practices to minimize the impact of these residual risks.


Summary
-------

The ALZ-NIEV threat model assumes an adversarial environment but leverages:

- native consensus finality;
- Merkle inclusion proofs;
- zero-knowledge proofs; and
- public TX visibility

to ensure that VERIFIED transfers are:

- independent of trusted relayers,
- resistant to spoofing and inflation,
- robust against normal reorgs, and
- auditable by any third party with access to public blockchain data.

