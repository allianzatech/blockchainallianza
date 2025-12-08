# 🏗️ Arquitetura - Allianza Blockchain

## 📋 Visão Geral

A Allianza Blockchain é uma blockchain pós-quântica e interoperável que combina:
- **QRS-3** (Quantum-Resistant Signature v3) - Segurança pós-quântica
- **ALZ-NIEV Protocol** - Consenso adaptativo
- **Bridge-Free Interoperability** - Interoperabilidade sem pontes

## 🏛️ Arquitetura em Camadas

```
┌─────────────────────────────────────────────────────────┐
│                    Application Layer                      │
│  (Smart Contracts, DApps, APIs)                          │
└─────────────────────────────────────────────────────────┘
                          │
┌─────────────────────────────────────────────────────────┐
│                  Interoperability Layer                  │
│  (Bridge-Free Interop, Proof-of-Lock, ZK Proofs)       │
└─────────────────────────────────────────────────────────┘
                          │
┌─────────────────────────────────────────────────────────┐
│                    Consensus Layer                        │
│  (ALZ-NIEV Protocol, Adaptive Consensus)                 │
└─────────────────────────────────────────────────────────┘
                          │
┌─────────────────────────────────────────────────────────┐
│                    Security Layer                        │
│  (QRS-3, PQC Algorithms, Quantum Security)             │
└─────────────────────────────────────────────────────────┘
                          │
┌─────────────────────────────────────────────────────────┐
│                    Core Blockchain                        │
│  (Blocks, Transactions, Wallets, State)                 │
└─────────────────────────────────────────────────────────┘
```

## 🔐 Camada de Segurança (QRS-3)

### Algoritmos PQC

- **ML-DSA** (Module-Lattice-based Digital Signature Algorithm)
  - Geração de chaves
  - Assinatura de transações
  - Verificação de assinaturas

- **SPHINCS+** (Stateless Hash-Based Signatures)
  - Assinaturas hash-based
  - Resistência quântica garantida
  - Batch verification

### Implementação

- **Arquivos**: `core/crypto/pqc_crypto.py`, `core/crypto/quantum_security.py`
- **Biblioteca**: liboqs-python (Open Quantum Safe)
- **Fallback**: Simulação funcional se liboqs não estiver disponível

## ⚙️ Camada de Consenso (ALZ-NIEV)

### Protocolo ALZ-NIEV

**ALZ-NIEV** = Non-Intermediate Execution Validation

- **Adaptativo**: Muda automaticamente baseado em condições da rede
- **Eficiente**: Otimiza performance e segurança
- **Escalável**: Escala automaticamente

### Tipos de Consenso

1. **PoS** (Proof of Stake) - Normal
2. **PoA** (Proof of Authority) - Alta carga
3. **PoH** (Proof of History) - Urgente
4. **Hybrid** - Combinação dinâmica

### Implementação

- **Arquivos**: `core/consensus/adaptive_consensus.py`, `core/consensus/alz_niev_interoperability.py`

## 🌉 Camada de Interoperabilidade

### Bridge-Free Interoperability

- **Sem custódia**: Tokens não ficam bloqueados em bridges
- **Sem pontes tradicionais**: Usa ZK Proofs e State Commitments
- **Sem wrapped tokens**: Transferências diretas

### Componentes

1. **Proof-of-Lock**
   - Prova criptográfica de lock
   - Validação on-chain
   - Atomicidade garantida

2. **ZK Proofs**
   - Validação sem revelar dados
   - Eficiência computacional
   - Segurança criptográfica

3. **State Commitments**
   - Compromissos de estado
   - Verificação cross-chain
   - Garantia de atomicidade

### Implementação

- **Arquivos**: `core/interoperability/bridge_free_interop.py`, `core/interoperability/proof_of_lock.py`

## 📦 Estrutura de Dados

### Bloco

```python
{
    "index": int,
    "timestamp": float,
    "transactions": List[Transaction],
    "previous_hash": str,
    "hash": str,
    "validator": str,
    "shard_id": int,
    "consensus_type": str
}
```

### Transação

```python
{
    "id": str,
    "sender": str,
    "receiver": str,
    "amount": float,
    "token": str,
    "signature": str,
    "qrs3_signature": str,  # Assinatura PQC
    "timestamp": float,
    "is_cross_chain": bool,
    "source_chain": str,
    "target_chain": str
}
```

## 🔄 Fluxo de Transação

```
1. Usuário cria transação
   ↓
2. Assina com QRS-3 (PQC)
   ↓
3. Transação adicionada à pool
   ↓
4. Validadores verificam (ALZ-NIEV)
   ↓
5. Bloco criado e adicionado à chain
   ↓
6. (Se cross-chain) Proof-of-Lock criado
   ↓
7. Estado atualizado
```

## 🌐 Interoperabilidade Cross-Chain

### Fluxo Bridge-Free

```
Chain A (Source)          Allianza          Chain B (Target)
    │                       │                    │
    │── Lock Tokens ───────>│                    │
    │                       │                    │
    │<── Proof-of-Lock ─────│                    │
    │                       │                    │
    │                       │── Verify Proof ────>│
    │                       │                    │
    │                       │<── Unlock Tokens ──│
    │                       │                    │
```

## 🔗 Links

- [README Principal](../../README.md)
- [TESTING.md](../../TESTING.md)
- [VERIFICATION.md](../../VERIFICATION.md)

---

**Última atualização**: 2025-12-07

