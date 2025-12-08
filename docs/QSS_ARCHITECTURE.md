# 🔐 QSS (Quantum Security Service) - Arquitetura Completa

**Versão:** 1.0  
**Data:** 03 de Dezembro de 2025  
**Status:** Documentação Técnica Completa

---

## 📋 Índice

1. [Visão Geral](#visão-geral)
2. [Arquitetura do Sistema](#arquitetura-do-sistema)
3. [Componentes Principais](#componentes-principais)
4. [Fluxo de Funcionamento](#fluxo-de-funcionamento)
5. [Integração com Outras Blockchains](#integração-com-outras-blockchains)
6. [APIs e Endpoints](#apis-e-endpoints)
7. [Segurança e Verificação](#segurança-e-verificação)
8. [Exemplos Práticos](#exemplos-práticos)
9. [FAQ](#faq)

---

## 🎯 Visão Geral

### O Que é o QSS?

O **Quantum Security Service (QSS)** é um serviço B2B que permite que **qualquer blockchain** (Bitcoin, Ethereum, Polygon, Solana, etc.) use a segurança quântica da Allianza Blockchain **sem precisar modificar seu código ou consenso**.

### Por Que é Revolucionário?

1. **Primeiro no Mundo**: Nenhuma blockchain oferece segurança quântica como serviço para outras blockchains
2. **Sem Modificações**: Blockchains existentes podem usar QSS sem mudanças no código
3. **Proteção Futura**: Prepara blockchains para a era pós-quântica
4. **Modelo Escalável**: Receita recorrente por validação

### Casos de Uso

- **Exchanges**: Proteção de fundos e transações críticas
- **DeFi Protocols**: Proteção de smart contracts e liquidações
- **NFTs**: Certificação quântica de autenticidade
- **Supply Chain**: Rastreamento seguro de produtos
- **Governo/Enterprise**: Documentos e contratos críticos

---

## 🏗️ Arquitetura do Sistema

### Diagrama de Alto Nível

```
┌─────────────────────────────────────────────────────────────────┐
│                    BLOCKCHAINS EXTERNAS                        │
│  Bitcoin │ Ethereum │ Polygon │ Solana │ BSC │ Outras...      │
└──────────┬──────────┬──────────┬──────────┬──────────┬─────────┘
           │          │          │          │          │
           │          │          │          │          │
           │  Envia TX Hash + Metadata para QSS API               │
           │                                                      │
           ▼                                                      │
┌─────────────────────────────────────────────────────────────────┐
│              QSS API GATEWAY (Flask/FastAPI)                   │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  /api/qss/generate-proof                                 │  │
│  │  /api/qss/verify-proof                                   │  │
│  │  /api/qss/anchor-proof                                   │  │
│  │  /api/qss/get-proof-status                                │  │
│  └──────────────────────────────────────────────────────────┘  │
└──────────┬──────────────────────────────────────────────────────┘
           │
           ▼
┌─────────────────────────────────────────────────────────────────┐
│              QSS CORE ENGINE                                    │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │ Quantum      │  │ Proof        │  │ Merkle       │         │
│  │ Signature    │  │ Generator    │  │ Tree         │         │
│  │ (ML-DSA)     │  │              │  │ Manager      │         │
│  └──────────────┘  └──────────────┘  └──────────────┘         │
│                                                                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │ Consensus    │  │ Anchor      │  │ Verification │         │
│  │ Proof        │  │ Service     │  │ Engine       │         │
│  │ Generator    │  │             │  │              │         │
│  └──────────────┘  └──────────────┘  └──────────────┘         │
└──────────┬──────────────────────────────────────────────────────┘
           │
           ▼
┌─────────────────────────────────────────────────────────────────┐
│              ALLIANZA BLOCKCHAIN                                │
│  - Armazena provas quânticas                                    │
│  - Mantém Merkle Tree de todas as provas                        │
│  - Fornece consenso distribuído                                 │
│  - Ancoragem permanente no Bitcoin                              │
└─────────────────────────────────────────────────────────────────┘
```

### Camadas do Sistema

#### **Camada 1: API Gateway**
- Recebe requisições de blockchains externas
- Valida inputs
- Rate limiting e autenticação
- Retorna provas quânticas

#### **Camada 2: QSS Core Engine**
- Gera assinaturas quânticas (ML-DSA, SPHINCS+)
- Cria Merkle Proofs
- Gera Consensus Proofs
- Gerencia ancoragem

#### **Camada 3: Allianza Blockchain**
- Armazena provas permanentemente
- Mantém Merkle Tree global
- Fornece consenso distribuído
- Ancoragem no Bitcoin

---

## 🔧 Componentes Principais

### 1. Quantum Proof Generator

**Função**: Gera provas quânticas verificáveis para transações de outras blockchains

**Input**:
```json
{
  "chain": "bitcoin",
  "tx_hash": "842f01a3302b6b19981204c96f377be1...",
  "metadata": {
    "block_height": 12345,
    "timestamp": "2025-12-03T10:00:00Z"
  }
}
```

**Output**:
```json
{
  "proof_hash": "ac0036b1f993fb202923eb77f686b660...",
  "quantum_signature": "Base64...",
  "merkle_proof": {
    "root": "...",
    "path": [...],
    "leaf": "..."
  },
  "consensus_proof": {
    "block_height": 12345,
    "validators": [...],
    "signatures": [...]
  },
  "valid": true,
  "timestamp": "2025-12-03T10:00:00Z"
}
```

### 2. Proof Verifier

**Função**: Verifica se uma prova quântica é válida

**Processo**:
1. Verifica assinatura quântica (ML-DSA)
2. Valida Merkle Proof
3. Verifica Consensus Proof
4. Confirma ancoragem no Bitcoin (se aplicável)

### 3. Anchor Service

**Função**: Ancora provas quânticas em blockchains externas

**Métodos de Ancoragem**:

| Blockchain | Método | Descrição |
|------------|--------|-----------|
| **Bitcoin** | OP_RETURN | Hash da prova em OP_RETURN |
| **Ethereum/Polygon** | Smart Contract | Contrato `QuantumProofAnchor` |
| **Solana** | Account Data | Dados armazenados em account |
| **BSC** | Smart Contract | Similar ao Ethereum |

### 4. Merkle Tree Manager

**Função**: Mantém árvore Merkle de todas as provas geradas

**Características**:
- Inserção O(log n)
- Verificação O(log n)
- Root hash atualizado a cada bloco
- Ancoragem periódica no Bitcoin

---

## 🔄 Fluxo de Funcionamento

### Fluxo Completo: Geração de Prova

```
1. Cliente envia TX hash
   ↓
2. QSS API valida input
   ↓
3. QSS Core gera assinatura quântica (ML-DSA)
   ↓
4. QSS Core cria Merkle Proof
   ↓
5. QSS Core gera Consensus Proof
   ↓
6. Allianza Blockchain armazena prova
   ↓
7. Merkle Tree atualizado
   ↓
8. Prova ancorada no Bitcoin (opcional)
   ↓
9. QSS API retorna prova completa
   ↓
10. Cliente pode verificar/ancorar em sua blockchain
```

### Fluxo: Verificação de Prova

```
1. Cliente envia prova quântica
   ↓
2. QSS API recebe prova
   ↓
3. Proof Verifier valida assinatura quântica
   ↓
4. Proof Verifier valida Merkle Proof
   ↓
5. Proof Verifier valida Consensus Proof
   ↓
6. Proof Verifier verifica ancoragem (se aplicável)
   ↓
7. QSS API retorna resultado da verificação
```

### Fluxo: Ancoragem

```
1. Cliente solicita ancoragem
   ↓
2. QSS API recebe solicitação
   ↓
3. Anchor Service prepara ancoragem
   ↓
4. Anchor Service cria transação na blockchain destino
   ↓
5. Transação é broadcastada
   ↓
6. Confirmação aguardada
   ↓
7. QSS API retorna TX hash da ancoragem
```

---

## 🔗 Integração com Outras Blockchains

### Bitcoin

**Método**: OP_RETURN

```python
# Exemplo de ancoragem no Bitcoin
def anchor_to_bitcoin(proof_hash: str) -> str:
    # Criar transação Bitcoin com OP_RETURN
    tx = create_bitcoin_tx(
        outputs=[
            {"address": "burn_address", "amount": 0},
            {"op_return": proof_hash}  # Hash da prova
        ]
    )
    return broadcast_tx(tx)
```

### Ethereum / Polygon

**Método**: Smart Contract

```solidity
// Contrato para ancorar provas
contract QuantumProofAnchor {
    mapping(bytes32 => bool) public proofs;
    
    function anchorProof(bytes32 proofHash) external {
        proofs[proofHash] = true;
        emit ProofAnchored(proofHash, msg.sender, block.timestamp);
    }
    
    function verifyProof(bytes32 proofHash) external view returns (bool) {
        return proofs[proofHash];
    }
}
```

### Solana

**Método**: Account Data

```rust
// Programa Solana para ancorar provas
pub fn anchor_proof(
    ctx: Context<AnchorProof>,
    proof_hash: [u8; 32]
) -> Result<()> {
    let proof_account = &mut ctx.accounts.proof_account;
    proof_account.proof_hash = proof_hash;
    proof_account.timestamp = Clock::get()?.unix_timestamp;
    Ok(())
}
```

---

## 🌐 APIs e Endpoints

### POST `/api/qss/generate-proof`

Gera uma prova quântica para uma transação de outra blockchain.

**Request**:
```json
{
  "chain": "bitcoin",
  "tx_hash": "842f01a3302b6b19981204c96f377be1...",
  "metadata": {
    "block_height": 12345,
    "timestamp": "2025-12-03T10:00:00Z"
  }
}
```

**Response**:
```json
{
  "success": true,
  "proof": {
    "proof_hash": "ac0036b1f993fb202923eb77f686b660...",
    "quantum_signature": "Base64...",
    "merkle_proof": {...},
    "consensus_proof": {...},
    "valid": true
  },
  "timestamp": "2025-12-03T10:00:00Z"
}
```

### POST `/api/qss/verify-proof`

Verifica se uma prova quântica é válida.

**Request**:
```json
{
  "proof": {
    "proof_hash": "ac0036b1f993fb202923eb77f686b660...",
    "quantum_signature": "Base64...",
    "merkle_proof": {...},
    "consensus_proof": {...}
  }
}
```

**Response**:
```json
{
  "valid": true,
  "verification_details": {
    "signature_valid": true,
    "merkle_proof_valid": true,
    "consensus_proof_valid": true,
    "anchored": true
  }
}
```

### POST `/api/qss/anchor-proof`

Ancora uma prova quântica em uma blockchain externa.

**Request**:
```json
{
  "proof_hash": "ac0036b1f993fb202923eb77f686b660...",
  "target_chain": "bitcoin",
  "options": {
    "priority": "high"
  }
}
```

**Response**:
```json
{
  "success": true,
  "anchor_tx_hash": "bitcoin_tx_hash...",
  "status": "pending",
  "estimated_confirmation_time": 600
}
```

### GET `/api/qss/get-proof-status`

Obtém o status de uma prova quântica.

**Request**:
```
GET /api/qss/get-proof-status?proof_hash=ac0036b1f993fb202923eb77f686b660...
```

**Response**:
```json
{
  "proof_hash": "ac0036b1f993fb202923eb77f686b660...",
  "status": "verified",
  "anchored": true,
  "anchor_tx_hash": "bitcoin_tx_hash...",
  "created_at": "2025-12-03T10:00:00Z",
  "verified_at": "2025-12-03T10:01:00Z"
}
```

---

## 🔒 Segurança e Verificação

### Algoritmos PQC Utilizados

1. **ML-DSA (Module-Lattice-based Digital Signature Algorithm)**
   - Padrão NIST PQC
   - Nível de segurança 3
   - Resistente a ataques quânticos

2. **SPHINCS+**
   - Assinatura baseada em hash
   - Nível de segurança 5
   - Backup para ML-DSA

3. **QRS-3 (Quantum-Resistant Signature 3)**
   - Combinação de 3 algoritmos
   - Máxima segurança
   - Usado para transações críticas

### Verificação de Provas

**Processo de Verificação**:

1. **Verificação de Assinatura Quântica**
   - Valida assinatura ML-DSA
   - Verifica chave pública
   - Confirma integridade

2. **Verificação de Merkle Proof**
   - Valida caminho na árvore
   - Verifica root hash
   - Confirma inclusão

3. **Verificação de Consensus Proof**
   - Valida assinaturas de validadores
   - Verifica quorum
   - Confirma finalidade

4. **Verificação de Ancoragem**
   - Confirma ancoragem no Bitcoin
   - Verifica TX hash
   - Valida timestamp

### Proteções Implementadas

- **Rate Limiting**: Previne abuso da API
- **Autenticação**: API keys para clientes
- **Criptografia**: Todas as comunicações criptografadas
- **Auditoria**: Logs de todas as operações
- **Backup**: Múltiplas cópias das provas

---

## 💡 Exemplos Práticos

### Exemplo 1: Proteger Transação Bitcoin

```python
import requests

# 1. Obter hash de transação Bitcoin
bitcoin_tx_hash = "842f01a3302b6b19981204c96f377be1..."

# 2. Gerar prova quântica
response = requests.post(
    "https://testnet.allianza.tech/api/qss/generate-proof",
    json={
        "chain": "bitcoin",
        "tx_hash": bitcoin_tx_hash
    }
)

proof = response.json()["proof"]

# 3. Verificar prova
verify_response = requests.post(
    "https://testnet.allianza.tech/api/qss/verify-proof",
    json={"proof": proof}
)

print(f"Prova válida: {verify_response.json()['valid']}")

# 4. Ancorar no Bitcoin (opcional)
anchor_response = requests.post(
    "https://testnet.allianza.tech/api/qss/anchor-proof",
    json={
        "proof_hash": proof["proof_hash"],
        "target_chain": "bitcoin"
    }
)

print(f"TX de ancoragem: {anchor_response.json()['anchor_tx_hash']}")
```

### Exemplo 2: Integração com Smart Contract Ethereum

```solidity
// Contrato que usa QSS para proteger transações
contract ProtectedContract {
    address public qssVerifier;
    
    function executeProtectedTransaction(
        bytes32 txHash,
        bytes memory quantumProof
    ) external {
        // Verificar prova quântica
        require(
            QuantumProofVerifier(qssVerifier).verifyProof(
                txHash,
                quantumProof
            ),
            "Invalid quantum proof"
        );
        
        // Executar transação protegida
        // ...
    }
}
```

### Exemplo 3: SDK JavaScript

```javascript
import { QSSClient } from '@allianza/qss-sdk';

const client = new QSSClient({
  apiUrl: 'https://testnet.allianza.tech/api/qss',
  apiKey: 'your-api-key'
});

// Gerar prova
const proof = await client.generateProof({
  chain: 'bitcoin',
  txHash: '842f01a3302b6b19981204c96f377be1...'
});

// Verificar prova
const isValid = await client.verifyProof(proof);

// Ancorar prova
const anchorTx = await client.anchorProof({
  proofHash: proof.proof_hash,
  targetChain: 'bitcoin'
});
```

---

## ❓ FAQ

### 1. O QSS modifica a blockchain original?

**Não.** O QSS funciona como um serviço externo. A blockchain original não precisa ser modificada.

### 2. Como o QSS protege transações de outras blockchains?

O QSS gera provas quânticas que podem ser verificadas independentemente. Essas provas são ancoradas permanentemente no Bitcoin e podem ser verificadas por qualquer pessoa.

### 3. O QSS é necessário para todas as transações?

**Não.** O QSS é opcional e pode ser usado para transações críticas que precisam de proteção quântica adicional.

### 4. Quanto custa usar o QSS?

O modelo de preços varia:
- **Por prova**: $0.01 - $0.10
- **Por ancoragem**: $0.05 - $0.50
- **Pacote empresarial**: $500 - $5000/mês

### 5. O QSS funciona em mainnet?

Atualmente, o QSS está disponível em testnet. A versão mainnet será lançada após auditorias de segurança.

### 6. Quais blockchains são suportadas?

Atualmente suportadas:
- Bitcoin (Testnet)
- Ethereum (Sepolia)
- Polygon (Amoy)
- BSC (Testnet)

Em desenvolvimento:
- Solana
- Cosmos
- Avalanche

### 7. Como verificar uma prova quântica?

Você pode verificar uma prova usando:
- API REST: `POST /api/qss/verify-proof`
- SDK JavaScript/Python
- Smart Contract (Ethereum/Polygon)

### 8. As provas são armazenadas permanentemente?

**Sim.** Todas as provas são armazenadas permanentemente na Allianza Blockchain e ancoradas no Bitcoin.

---

## 📚 Referências

- [GUIA_QSS_PARA_OUTRAS_BLOCKCHAINS.md](../GUIA_QSS_PARA_OUTRAS_BLOCKCHAINS.md)
- [QUANTUM_SECURITY_SERVICE_LAYER.md](../QUANTUM_SECURITY_SERVICE_LAYER.md)
- [QSS SDK Documentation](../qss-sdk/README.md)
- [NIST PQC Standards](https://csrc.nist.gov/projects/post-quantum-cryptography)

---

## 📝 Changelog

### Versão 1.0 (03/12/2025)
- Documentação inicial completa
- Arquitetura detalhada
- Exemplos práticos
- FAQ completo

---

**Última Atualização:** 03 de Dezembro de 2025  
**Mantido por:** Allianza Blockchain Team


