# 📖 Glossário Técnico - Allianza Blockchain

Este documento define termos técnicos usados no projeto Allianza Blockchain.

## 🔐 Criptografia Pós-Quântica (PQC)

### ML-DSA (Module-Lattice-based Digital Signature Algorithm)
- **Também conhecido como:** Dilithium
- **Tipo:** Assinatura digital baseada em lattices
- **Padrão:** NIST PQC Standard (2024)
- **Uso:** Assinaturas quântico-seguras
- **Implementação:** Via `liboqs-python` (real) ou simulação funcional

### ML-KEM (Module-Lattice-based Key Encapsulation Mechanism)
- **Também conhecido como:** Kyber
- **Tipo:** Encapsulamento de chave baseado em lattices
- **Padrão:** NIST PQC Standard (2024)
- **Uso:** Troca de chaves quântico-segura
- **Implementação:** Via `liboqs-python` (real) ou simulação funcional

### SPHINCS+ (Stateless Hash-Based Signatures)
- **Tipo:** Assinatura baseada em hash (stateless)
- **Padrão:** NIST PQC Standard (2024)
- **Uso:** Assinaturas quântico-seguras de longo prazo
- **Característica:** Não requer estado (stateless)
- **Implementação:** Via `liboqs-python` (real) ou simulação funcional

### QRS-3 (Quantum-Resistant Signature v3)
- **Tipo:** Sistema de assinatura tripla redundante
- **Componentes:** ECDSA + ML-DSA + SPHINCS+
- **Uso:** Máxima segurança quântica
- **Implementação:** [`core/crypto/quantum_security.py`](core/crypto/quantum_security.py)

### ECDSA (Elliptic Curve Digital Signature Algorithm)
- **Tipo:** Assinatura digital clássica (não quântico-segura)
- **Uso:** Compatibilidade com blockchains existentes
- **Status:** Usado em QRS-3 para compatibilidade, mas não é quântico-seguro sozinho

## 🌐 Interoperabilidade

### ALZ-NIEV Protocol
- **Nome completo:** Adaptive Lattice Zero-Knowledge Native Interoperability Execution Verification
- **Tipo:** Protocolo de interoperabilidade bridge-free
- **Características:**
  - Validação nativa de assinaturas de outras blockchains
  - Sem necessidade de bridges custodiadas
  - Usa Zero-Knowledge Proofs
- **Implementação:** [`core/consensus/alz_niev_interoperability.py`](core/consensus/alz_niev_interoperability.py)

### Proof-of-Lock
- **Tipo:** Mecanismo de prova criptográfica
- **Uso:** Provar que tokens foram bloqueados em outra blockchain
- **Características:**
  - Verificável on-chain
  - Não requer bridge custodiada
  - Usa ZK Proofs
- **Implementação:** [`core/interoperability/proof_of_lock.py`](core/interoperability/proof_of_lock.py)

### Bridge-Free
- **Significado:** Interoperabilidade sem bridges custodiadas
- **Vantagem:** Sem ponto único de falha
- **Método:** Validação nativa de assinaturas + ZK Proofs

## 🔗 Blockchain

### Sharding
- **Significado:** Divisão da blockchain em fragmentos (shards)
- **Vantagem:** Escalabilidade horizontal
- **Uso:** Processar transações em paralelo

### Consensus
- **Tipos suportados:** PoS, PoA, PoH, Hybrid
- **Característica:** Adaptativo (ALZ-NIEV)
- **Implementação:** [`core/consensus/adaptive_consensus.py`](core/consensus/adaptive_consensus.py)

## 📊 Testes e Provas

### Testnet
- **URL:** https://testnet.allianza.tech
- **Tipo:** Rede de teste pública
- **Uso:** Testar funcionalidades sem risco

### On-Chain Proof
- **Significado:** Prova verificável em blockchain pública
- **Exemplo:** Hash de transação em Ethereum Sepolia
- **Verificação:** Via explorers públicos (Etherscan, Blockstream)

### Batch Verification
- **Significado:** Verificação de múltiplas assinaturas simultaneamente
- **Vantagem:** Performance melhorada
- **Uso:** Otimização de throughput

## 🛠️ Ferramentas

### liboqs-python
- **Tipo:** Biblioteca Python para criptografia pós-quântica
- **Fonte:** Open Quantum Safe (OQS)
- **Uso:** Implementação real de ML-DSA, ML-KEM, SPHINCS+
- **Instalação:** `pip install liboqs-python`

### Quantum Security System
- **Classe:** `QuantumSecuritySystem`
- **Arquivo:** [`core/crypto/quantum_security.py`](core/crypto/quantum_security.py)
- **Função:** Gerenciar criptografia quântico-segura
- **Característica:** Detecta automaticamente `liboqs-python` e usa implementação real quando disponível

## 📚 Documentação Relacionada

- [WHAT_IS_REAL.md](WHAT_IS_REAL.md) - O que é real vs simulado
- [RESPONSE_TO_ANALYSIS.md](RESPONSE_TO_ANALYSIS.md) - Respostas a análises
- [VERIFICATION.md](VERIFICATION.md) - Guia de verificação
- [TESTING.md](TESTING.md) - Guia de testes

---

**Última atualização:** 2025-12-08

