# 🏗️ Architecture Diagrams - Allianza Blockchain

## 📊 System Overview

```mermaid
graph TB
    subgraph "Allianza Blockchain Core"
        A[AllianzaBlockchain] --> B[Quantum Security System]
        A --> C[ALZ-NIEV Consensus]
        A --> D[Bridge-Free Interop]
        
        B --> E[ML-DSA]
        B --> F[ML-KEM]
        B --> G[SPHINCS+]
        
        C --> H[Adaptive Consensus]
        C --> I[Sharding]
        
        D --> J[Proof-of-Lock]
        D --> K[ZK Proofs]
    end
    
    subgraph "External Blockchains"
        L[Bitcoin]
        M[Ethereum]
        N[Polygon]
        O[Solana]
    end
    
    D -.->|Validate Signatures| L
    D -.->|Validate Signatures| M
    D -.->|Validate Signatures| N
    D -.->|Validate Signatures| O
    
    style B fill:#2ecc71
    style C fill:#3498db
    style D fill:#9b59b6
```

## 🔐 QRS-3 Signature System

```mermaid
graph LR
    A[Transaction] --> B[QRS-3 Signer]
    
    B --> C[ECDSA Signature]
    B --> D[ML-DSA Signature]
    B --> E[SPHINCS+ Signature]
    
    C --> F[Combined Signature]
    D --> F
    E --> F
    
    F --> G[Transaction with QRS-3]
    
    style B fill:#e74c3c
    style F fill:#2ecc71
```

## 🌐 ALZ-NIEV Interoperability Flow

```mermaid
sequenceDiagram
    participant User
    participant Allianza
    participant External as External Chain
    participant Verifier as QSS Verifier
    
    User->>Allianza: Request Cross-Chain Transfer
    Allianza->>External: Lock Tokens
    External-->>Allianza: Lock Proof
    Allianza->>Allianza: Generate ZK Proof
    Allianza->>Verifier: Verify Proof
    Verifier-->>Allianza: Proof Valid
    Allianza->>Allianza: Mint Equivalent Tokens
    Allianza-->>User: Transfer Complete
```

## 🏛️ Consensus Architecture

```mermaid
graph TB
    subgraph "ALZ-NIEV Consensus"
        A[Network State] --> B{Consensus Mode}
        
        B -->|Low Load| C[PoS]
        B -->|Medium Load| D[PoA]
        B -->|High Load| E[PoH]
        B -->|Mixed| F[Hybrid]
        
        C --> G[Block Creation]
        D --> G
        E --> G
        F --> G
        
        G --> H[Shard Distribution]
        H --> I[Validation]
        I --> J[Final Block]
    end
    
    style B fill:#f39c12
    style G fill:#3498db
```

## 🔄 Transaction Flow

```mermaid
sequenceDiagram
    participant User
    participant Wallet
    participant QSS as Quantum Security
    participant Consensus
    participant Shard
    participant DB as Database
    
    User->>Wallet: Create Transaction
    Wallet->>QSS: Sign with QRS-3
    QSS-->>Wallet: Signed Transaction
    Wallet->>Consensus: Submit Transaction
    Consensus->>Shard: Route to Shard
    Shard->>Shard: Validate Transaction
    Shard->>DB: Store Transaction
    Shard-->>Consensus: Transaction Confirmed
    Consensus-->>User: Transaction Complete
```

## 📦 Component Architecture

```mermaid
graph TB
    subgraph "Core Components"
        A[allianza_blockchain.py] --> B[QuantumSecuritySystem]
        A --> C[DBManager]
        A --> D[TestnetExplorer]
        A --> E[TestnetFaucet]
    end
    
    subgraph "Core Modules"
        F[core/crypto/] --> G[quantum_security.py]
        F --> H[pqc_crypto.py]
        
        I[core/consensus/] --> J[adaptive_consensus.py]
        I --> K[alz_niev_interoperability.py]
        
        L[core/interoperability/] --> M[bridge_free_interop.py]
        L --> N[proof_of_lock.py]
    end
    
    B --> G
    A --> I
    A --> L
    
    style A fill:#e74c3c
    style F fill:#2ecc71
    style I fill:#3498db
    style L fill:#9b59b6
```

## 🔗 Interoperability Architecture

```mermaid
graph TB
    subgraph "Allianza Blockchain"
        A[User Request] --> B[ALZ-NIEV Protocol]
        B --> C[Signature Validator]
        B --> D[Proof Generator]
    end
    
    subgraph "External Chains"
        E[Bitcoin]
        F[Ethereum]
        G[Polygon]
        H[Solana]
    end
    
    C -->|Validate| E
    C -->|Validate| F
    C -->|Validate| G
    C -->|Validate| H
    
    D --> I[ZK Proof]
    I --> J[On-Chain Verification]
    
    style B fill:#9b59b6
    style C fill:#3498db
    style I fill:#2ecc71
```

## 🧪 Test Architecture

```mermaid
graph TB
    A[Test Suite] --> B[Unit Tests]
    A --> C[Integration Tests]
    A --> D[Public Verification Tests]
    
    B --> E[QRS-3 Tests]
    B --> F[Consensus Tests]
    B --> G[Interop Tests]
    
    C --> H[End-to-End Tests]
    C --> I[Performance Tests]
    
    D --> J[Reproducible Tests]
    D --> K[On-Chain Verification]
    
    style A fill:#e74c3c
    style D fill:#2ecc71
```

---

**Nota:** Estes diagramas são renderizados usando Mermaid. Para visualizar:
- GitHub: Renderiza automaticamente em arquivos `.md`
- VS Code: Instale extensão "Markdown Preview Mermaid Support"
- Online: https://mermaid.live/

