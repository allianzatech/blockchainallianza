ALZ-NIEV Verification Standard v1.0
===================================

Abstract
--------

This document defines the ALZ-NIEV Verification Standard v1.0, a unified, chain-agnostic model for verifying REAL cross-chain transfers.  
The goal is to provide a minimal, precise set of cryptographic requirements that allow independent verifiers to determine whether a cross-chain transfer is considered **VERIFIED** or must be classified as **LEGACY**.  
The standard is designed to support heterogeneous consensus systems, including Bitcoin, Solana, Polygon, Ethereum, and future blockchains.


Motivation
----------

Traditional bridges and interoperability systems frequently rely on trusted relayers, multisigs, or opaque off-chain services.  
These models are vulnerable to:

- message forgery by compromised relayers;
- misreporting of source-chain state;
- inflation of synthetic assets not fully backed on the origin chain;
- censorship or rollback of cross-chain transfers during reorganizations.

To mitigate these risks, a cross-chain verification standard MUST:

1. Rely on **native consensus finality** of the source chain, not on external assumptions;
2. Provide **cryptographic inclusion proofs** (Merkle or equivalent) that the relevant state/transaction is part of a finalized block;
3. Use **zero-knowledge proofs** (or equivalent) to prove the correctness of state transitions and value flows; and
4. Ensure **public verifiability** of all claims, without relying on trusted relayers.

The ALZ-NIEV Verification Standard defines such a model.


Definitions
-----------

- **Source Chain**: The blockchain from which value, state, or information originates in a cross-chain transfer.
- **Target Chain**: The blockchain to which value, state, or information is delivered in a cross-chain transfer.
- **UChainID**: A unique, chain-agnostic identifier that binds a specific cross-chain transfer across all chains involved.
- **State Transition**: The change in state on the source chain associated with the cross-chain transfer (e.g., debit of funds, lock, burn).
- **Finality**: The property that, under the consensus rules of the Source Chain, a block and its contained state transitions are economically or probabilistically irreversible.
- **Verified Transfer**: A cross-chain transfer that satisfies all mandatory verification requirements in this standard.
- **Legacy Transfer**: A cross-chain transfer that does not meet one or more mandatory verification requirements and therefore MUST NOT be classified as VERIFIED.


Verification Requirements (Chain-Agnostic)
------------------------------------------

A cross-chain transfer **MUST** satisfy all of the following conditions to be classified as a **Verified Transfer**:

1. **State Transition Proof**
   - There MUST exist a cryptographic proof that the relevant state transition occurred on the Source Chain.
   - The proof MUST include at least:
     - the UChainID;
     - the amount or value transferred;
     - the recipient (or recipient binding on the Target Chain);
     - the Source Chain transaction hash.

2. **Merkle (or Equivalent) Inclusion Proof**
   - There MUST exist a Merkle or equivalent inclusion proof that the Source Chain transaction (or relevant leaf) is included in a block.
   - The proof MUST:
     - reference a specific block hash and height;
     - contain the leaf hash and a path (set of sibling hashes) sufficient to recompute the block root; and
     - satisfy a **minimum tree depth** requirement for the Source Chain (see “Merkle Proof Requirements”).

3. **Consensus Finality Proof**
   - There MUST exist evidence that the block containing the state transition has reached finality under the native consensus of the Source Chain.
   - The finality proof MUST:
     - be expressed in a chain-specific module (see “Chain-Specific Finality Modules”);
     - include block height and/or epoch/slot identifiers; and
     - include a finality confirmation metric (e.g., number of confirmations, finalized checkpoint, or finalized slot).

4. **Zero-Knowledge Proof of Correctness**
   - A zero-knowledge proof system (e.g., zk-SNARK, zk-STARK, or equivalent) MUST be used to prove that:
     - the state transition satisfies the protocol’s value-conservation rules;
     - the mapping from Source Chain state to Target Chain effect is correct; and
     - no additional value is minted or unlocked beyond what is locked/burned on the Source Chain.
   - The proof MUST be verifiable by a public verifier key or contract on at least one chain.

5. **Non-Inflation Guarantee**
   - The verification procedure MUST guarantee that the aggregate value represented on all Target Chains does not exceed the value locked, burned, or otherwise provably reserved on the Source Chains.

6. **Public Verifiability**
   - All artifacts necessary for verification (transaction hashes, block identifiers, Merkle roots, proof hashes, and ZK verification keys) MUST be:
     - derivable from public data; and
     - accessible without trust in proprietary relayers or closed databases.

If **any** of the above requirements is not satisfied, the transfer **MUST** be classified as a **Legacy Transfer**.


Chain-Specific Finality Modules
-------------------------------

The consensus finality requirement is satisfied via chain-specific modules which implement the generic “Finality Proof” interface. The following reference mappings are RECOMMENDED:

- **Bitcoin**
  - Type: Proof-of-Work longest-chain rule.
  - Finality condition: a transaction is considered final when it is included in a block with at least *N* descendant blocks (confirmations).
  - The verifier MUST:
    - validate block headers and proof-of-work;
    - ensure that the chain of headers is consistent and has the greatest cumulative work; and
    - enforce a minimum confirmation threshold (e.g., N ≥ 6 for production environments).

- **Solana**
  - Type: Proof-of-History (PoH) + Tower BFT.
  - Finality condition: a transaction is considered final when it is included in a slot that has reached BFT finality under the Tower algorithm.
  - The verifier SHOULD:
    - validate the PoH sequence and Tower votes for the finalized slot;
    - ensure the slot cannot be reverted without violating the BFT assumptions.

- **Polygon (PoS)**
  - Type: PoS with BOR + Ethereum checkpointing.
  - Finality condition: a transaction is considered final when it is included in a block that is part of an epoch for which a checkpoint has been committed to Ethereum L1.
  - The verifier SHOULD:
    - verify the BOR chain and its validator signatures; and
    - verify that the checkpoint corresponding to the epoch is anchored on Ethereum and finalized under Ethereum’s PoS rules.

- **Ethereum**
  - Type: PoS with Casper FFG.
  - Finality condition: a transaction is considered final when it is included in a block that is part of a finalized checkpoint.
  - The verifier SHOULD:
    - validate the beacon chain finality checkpoints; and
    - ensure the block lies in the finalized part of the chain.

New blockchains MAY be added by defining a compatible finality module with:
  - a clear definition of finality;
  - the cryptographic objects that constitute a finality proof; and
  - explicit assumptions on validator or miner behaviour.


Zero-Knowledge Proof Requirements
---------------------------------

The zero-knowledge proof system used in ALZ-NIEV **MUST** satisfy:

- Soundness: it MUST be computationally infeasible for a prover to convince a verifier of a false state transition.
- Completeness: valid state transitions MUST always be accepted by an honest verifier.
- Public Verifiability: verification keys and public inputs MUST be publicly available.

The ZK proof for a Verified Transfer MUST at minimum attest that:

1. The Source Chain transaction corresponds to the claimed UChainID, amount, and recipient mapping.
2. The Target Chain effect (e.g., mint, unlock, accounting entry) does not exceed the value locked/burned on the Source Chain for that UChainID.
3. No additional hidden state allows double-minting or replay of the same Source Chain transaction for multiple Target Chain effects.


Merkle Proof Requirements
-------------------------

Merkle (or equivalent) inclusion proofs for Verified Transfers MUST satisfy:

- The leaf MUST encode, at minimum: UChainID, Source Chain transaction hash, and block/slot identifier.
- The path MUST contain enough sibling hashes to recompute the advertised Merkle root.
- The Merkle root MUST be bound to a specific finalized block via the consensus finality module.

Minimum depth requirements (RECOMMENDED defaults):

- EVM chains (Polygon, Ethereum, BSC, Base, Avalanche): depth ≥ 2.
- Solana: depth ≥ 3.
- Bitcoin: depth ≥ 6 (or equivalent UTXO inclusion path).

Implementations MAY use deeper trees; they MUST NOT classify as VERIFIED any transfer whose effective depth is below the chain-specific minimum.


Classification Rules
--------------------

A transfer MUST be classified as **Verified Transfer** if and only if:

1. All Verification Requirements (chain-agnostic) are satisfied; and
2. The corresponding chain-specific finality module confirms finality for the Source Chain state; and
3. The Merkle proof meets or exceeds the minimum depth and includes a non-empty path; and
4. Both Source Chain and Target Chain transaction hashes are publicly available and resolvable on-chain or via canonical explorers.

Any transfer that fails one or more of these conditions MUST be classified as a **Legacy Transfer**.

Legacy Transfers MAY be:
  - displayed in user interfaces with explicit warnings; and
  - used for internal testing, development, or historical purposes.

Legacy Transfers MUST NOT be marketed or reported as meeting the ALZ-NIEV Verification Standard.


Security Considerations
-----------------------

Implementations SHOULD explicitly consider and document mitigations against:

- **Replay Attacks**: UChainIDs MUST be unique per cross-chain transfer and bound to specific Source Chain transactions.
- **Double-Spend / Double-Mint**: ZK proofs and accounting MUST ensure that no more value is created on Target Chains than is provably locked/burned on Source Chains.
- **Reorganizations**: Finality modules MUST use conservative thresholds such that normal reorgs cannot invalidate a previously Verified Transfer.
- **Relayer Compromise**: Verifiers MUST NOT rely solely on relayer claims; all critical properties MUST be derivable from public data and proofs.
- **Verifier Independence**: Any third party with access to public chain data and verification keys MUST be able to re-verify a transfer independently.


Versioning
----------

This document defines **ALZ-NIEV Verification Standard v1.0**.

Subsequent versions (v1.1, v2.0, etc.) MAY:

- add new chain-specific finality modules;
- tighten minimum depth or confirmation parameters;
- extend the ZK proof requirements.

Breaking changes to the classification rules (e.g., relaxing mandatory conditions) SHOULD be avoided and, if necessary, MUST be clearly versioned and documented.

# ALZ-NIEV Verification Standard v1.0

**Status:** Draft  
**Type:** Standards Track  
**Category:** Cross-Chain Interoperability  
**Created:** 2026-01-13

---

## Abstract

This document defines a unified, chain-agnostic verification standard for cross-chain transfers. The ALZ-NIEV (Native Interoperability Execution Verification) standard establishes cryptographic requirements that MUST be satisfied for a cross-chain transfer to be considered VERIFIED. Transfers that do not meet these requirements are classified as LEGACY and MUST be clearly distinguished.

The standard is designed to be chain-agnostic, supporting Proof-of-Work (Bitcoin), Proof-of-Stake with BFT (Solana, Polygon), and other consensus mechanisms without modification to the core verification logic.

---

## Motivation

Cross-chain interoperability protocols face fundamental security challenges:

1. **Relayer Trust**: Traditional bridges require trusted relayers that can censor, freeze, or misrepresent state transitions.

2. **State Verification**: Without cryptographic proof of source chain state, target chains cannot independently verify the validity of incoming transfers.

3. **Finality Ambiguity**: Different blockchains achieve finality through different mechanisms (PoW confirmations, PoS epochs, BFT slots). A unified standard must accommodate all without compromising security.

4. **Inflation Risk**: Without cryptographic guarantees, malicious actors could create assets on target chains without corresponding locks on source chains.

This standard addresses these challenges by requiring cryptographic proofs that enable trustless verification across heterogeneous blockchain networks.

---

## Definitions

### Verified Transfer

A cross-chain transfer that satisfies ALL mandatory verification requirements defined in Section 4. A verified transfer provides cryptographic guarantees that:

- The state transition occurred on the source chain
- The source chain consensus finalized the transaction
- The transfer amount is correct and non-inflated
- The transfer can be verified without trusted intermediaries

### Legacy Transfer

A cross-chain transfer that does NOT satisfy all mandatory verification requirements. Legacy transfers MAY be functional but lack cryptographic guarantees and MUST be clearly labeled as such.

### Source Chain

The blockchain network where the original state transition (lock, burn, or transfer) occurs.

### Target Chain

The blockchain network where the corresponding state transition (mint, unlock, or transfer) occurs.

### UChainID

A unique identifier linking source and target transactions cryptographically. The UChainID MUST be deterministic and verifiable.

### State Transition

A change in blockchain state resulting from a transaction. For cross-chain transfers, this typically involves locking assets on the source chain and unlocking equivalent assets on the target chain.

### Finality

The property that a transaction or block cannot be reversed under the consensus rules of its blockchain. Finality mechanisms vary by chain (PoW confirmations, PoS epochs, BFT slots).

---

## Verification Requirements

A transfer MUST be classified as VERIFIED only if ALL of the following conditions are satisfied:

### 4.1 Cryptographic Proof of State Transition

A zero-knowledge proof (ZK-SNARK, ZK-STARK, or equivalent) MUST verify:

- The state transition is valid under the source chain's rules
- The amount transferred is correct
- The recipient address is correct
- No double-mint or replay attack occurred
- The transition respects non-inflation guarantees

**Verification:** The proof MUST be verifiable by a public verification key without requiring access to the source chain.

### 4.2 Merkle Inclusion Proof

A Merkle proof MUST demonstrate that the source transaction is included in a finalized block on the source chain.

**Requirements:**

- The proof MUST include the transaction hash
- The proof MUST include the Merkle path from leaf to root
- The proof MUST include the block header hash containing the root
- The proof depth MUST meet chain-specific minimums (see Section 5)

**Minimum Depths:**

- EVM chains (Polygon, Ethereum, BSC, Base): depth ≥ 2
- Solana: depth ≥ 3
- Bitcoin (UTXO): depth ≥ 6
- Other chains: depth ≥ 2 (unless chain-specific analysis requires higher)

### 4.3 Consensus Finality Proof

Proof that the source chain's consensus mechanism has finalized the transaction. The finality proof MUST be chain-specific (see Section 5) and MUST demonstrate:

- The transaction is included in a finalized block
- The finality cannot be reversed under normal consensus operation
- The finality meets the chain's security threshold

### 4.4 Public Transaction Hashes

Both source and target transaction hashes MUST be publicly accessible and verifiable:

- Source transaction hash MUST be verifiable on the source chain's explorer or RPC
- Target transaction hash MUST be verifiable on the target chain's explorer or RPC
- Explorer URLs or RPC endpoints MUST be provided

### 4.5 Non-Inflation Guarantee

The verification system MUST cryptographically guarantee that:

- Assets cannot be created on the target chain without corresponding locks/burns on the source chain
- The same source transaction cannot be used to create assets multiple times
- Replay attacks are prevented

### 4.6 Verifier Independence

The verification MUST be performable by any third party without:

- Trusted relayers
- Centralized oracles
- Off-chain services
- Private keys or credentials

---

## Chain-Specific Finality Modules

The consensus finality requirement (Section 4.3) is satisfied differently for each blockchain type. This section defines the finality modules without modifying the global standard.

### 5.1 Bitcoin (Proof-of-Work)

**Finality Type:** `pow_confirmations`

**Requirements:**

- Transaction MUST be included in a block
- Block MUST have ≥ 6 confirmations (testnet) or ≥ 6 confirmations (mainnet)
- Block header MUST be valid under Bitcoin's difficulty adjustment
- Block MUST be part of the longest valid chain

**Verification:**

- Verify block header hash meets difficulty target
- Verify block is in the longest chain (via block height comparison)
- Verify transaction is in the block's Merkle tree
- Count confirmations: `current_height - block_height + 1`

### 5.2 Solana (Proof-of-History + PoS BFT)

**Finality Type:** `poh_pos_bft`

**Requirements:**

- Transaction MUST be in a finalized slot
- Slot MUST be finalized by Tower BFT consensus
- PoH hash MUST be valid for the slot
- BFT quorum MUST have voted on finality

**Verification:**

- Verify slot is finalized (not just confirmed)
- Verify PoH hash chain integrity
- Verify BFT quorum signatures
- Verify transaction is included in the slot

**Minimum Confirmations:** 1 finalized slot (Solana finality is probabilistic but fast)

### 5.3 Polygon (PoS with BOR Checkpoint)

**Finality Type:** `pos_bor_checkpoint`

**Requirements:**

- Transaction MUST be in a BOR (Block Producer) block
- BOR block MUST be checkpointed to Ethereum L1
- Checkpoint MUST be finalized on Ethereum
- Validator quorum MUST have signed the checkpoint

**Verification:**

- Verify checkpoint exists on Ethereum L1
- Verify checkpoint is finalized (Ethereum PoS finality)
- Verify validator signatures meet quorum threshold
- Verify transaction is in the checkpointed BOR block

**Minimum Confirmations:** Checkpoint finalized on Ethereum (typically 2 epochs = 64 blocks)

### 5.4 Ethereum (PoS Finality)

**Finality Type:** `pos_finality`

**Requirements:**

- Transaction MUST be in a finalized epoch
- Epoch MUST be finalized by Casper FFG
- Finality checkpoint MUST be verified
- Validator set MUST be correct

**Verification:**

- Verify epoch is finalized (not just justified)
- Verify Casper FFG checkpoint signatures
- Verify validator set matches epoch
- Verify transaction is in a finalized block

**Minimum Confirmations:** 2 epochs (64 blocks) for full finality

### 5.5 Adding New Chains

To add support for a new blockchain:

1. Define the finality type string (e.g., `pos_avalanche`, `pow_litecoin`)
2. Specify the finality verification requirements
3. Define the minimum confirmation threshold
4. Document the Merkle proof structure (if applicable)
5. Submit as an extension to this standard

---

## Zero-Knowledge Proof Requirements

### 6.1 Proof System

The ZK proof system MUST be:

- **Sound**: Invalid state transitions cannot produce valid proofs
- **Complete**: Valid state transitions can produce valid proofs
- **Succinct**: Proof size is sublinear in computation size
- **Publicly Verifiable**: Verification requires only public inputs

### 6.2 Proof Content

The ZK proof MUST verify:

```
∀ (source_tx, target_tx, amount, recipient):
  ValidStateTransition(source_tx) ∧
  CorrectAmount(source_tx, amount) ∧
  CorrectRecipient(source_tx, recipient) ∧
  NoDoubleMint(source_tx, target_tx) ∧
  NoReplay(source_tx)
```

### 6.3 Circuit Specification

The verification circuit MUST be:

- Publicly auditable
- Deterministic
- Chain-agnostic (supports multiple source/target pairs)
- Versioned (circuit_id includes version)

**Circuit ID Format:** `transfer_{source_chain}_{target_chain}_v{version}`

Example: `transfer_solana_bitcoin_v1`

---

## Merkle Proof Requirements

### 7.1 Proof Structure

A Merkle proof MUST include:

- **Leaf Hash**: Hash of the transaction or transaction ID
- **Merkle Path**: Array of sibling hashes from leaf to root
- **Root Hash**: The Merkle root of the block
- **Block Header Hash**: Hash of the block containing the root

### 7.2 Verification Algorithm

```
function verify_merkle_proof(leaf, path, root):
    current = leaf
    for sibling in path:
        current = hash(concat(current, sibling))  // or hash(concat(sibling, current)) depending on path direction
    return current == root
```

### 7.3 Depth Requirements

The proof depth MUST meet chain-specific minimums (Section 4.2). Depth 0 or missing path indicates LEGACY transfer.

---

## Classification Rules

### 8.1 VERIFIED Classification

A transfer is VERIFIED if and only if:

```
is_verified = (
    has_zk_proof AND
    has_merkle_proof AND
    merkle_depth >= chain_minimum AND
    has_merkle_path AND
    has_consensus_finality AND
    consensus_type != "unknown" AND
    has_source_tx_hash AND
    has_target_tx_hash AND
    has_source_explorer AND
    has_target_explorer AND
    non_inflation_guaranteed
)
```

### 8.2 LEGACY Classification

A transfer is LEGACY if:

- Any requirement in Section 8.1 is not met
- Merkle depth is 0 or missing
- Consensus type is "unknown" or missing
- Transaction hashes are not publicly accessible
- Proof path is missing or incomplete

### 8.3 Display Requirements

- VERIFIED transfers MUST be clearly labeled with "✅ Verified" badge
- LEGACY transfers MUST be clearly labeled with "⚠️ Legacy" badge
- LEGACY transfers MUST include warning: "This transfer does not include complete consensus or Merkle proofs"
- VERIFIED and LEGACY transfers MUST be separated in API responses

---

## Security Considerations

### 9.1 Replay Attacks

The UChainID MUST be unique and deterministic. The same source transaction MUST NOT be used to create multiple target transactions.

**Mitigation:** Include source transaction hash, block height, and chain ID in UChainID generation.

### 9.2 Double-Spend Prevention

The verification system MUST prevent:

- Using the same UTXO/account balance multiple times
- Creating assets on target chain without locking on source chain
- Reversing source transaction after target transaction

**Mitigation:** ZK proof verifies non-inflation, Merkle proof verifies inclusion, consensus proof verifies finality.

### 9.3 Reorg Resistance

The system MUST handle blockchain reorganizations:

- PoW chains: Require sufficient confirmations (≥ 6 for Bitcoin)
- PoS chains: Require finalized epochs/slots
- If reorg occurs, target transaction MUST be reversible or invalidated

**Mitigation:** Only accept transactions from finalized blocks.

### 9.4 Verifier Independence

The verification MUST be performable by any third party without:

- Access to private keys
- Trusted relayers or oracles
- Centralized services
- Off-chain coordination

**Mitigation:** All proofs are public, verification is deterministic, no secrets required.

### 9.5 Inflation Attacks

Malicious actors MUST NOT be able to:

- Create assets on target chain without source chain lock
- Multiply assets through replay
- Forge state transitions

**Mitigation:** ZK proof cryptographically guarantees non-inflation.

---

## Versioning

### 10.1 Version Format

Versions follow semantic versioning: `v{MAJOR}.{MINOR}.{PATCH}`

- **MAJOR**: Breaking changes to verification requirements
- **MINOR**: New chain support or optional features
- **PATCH**: Clarifications or bug fixes

### 10.2 Current Version

**v1.0** (2026-01-13)

- Initial specification
- Support for Bitcoin, Solana, Polygon, Ethereum
- Core verification requirements defined

### 10.3 Backward Compatibility

- v1.x transfers MUST be verifiable by v1.0+ verifiers
- v2.0+ MAY introduce breaking changes with migration path
- Legacy transfers from older versions remain LEGACY

---

## References

- Bitcoin: [BIP-141](https://github.com/bitcoin/bips/blob/master/bip-0141.mediawiki) (Segregated Witness)
- Ethereum: [EIP-4844](https://eips.ethereum.org/EIPS/eip-4844) (Shard Blob Transactions)
- Solana: [Proof of History](https://docs.solana.com/developing/programming-model/runtime#proof-of-history)
- Zero-Knowledge Proofs: [zk-SNARKs](https://z.cash/technology/zksnarks/)

---

## Copyright

This document is released into the public domain.

---

**Authors:** ALZ-NIEV Protocol Contributors  
**Last Updated:** 2026-01-13
