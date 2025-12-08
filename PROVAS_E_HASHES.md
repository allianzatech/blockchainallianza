# 📋 Provas e Hashes - Guia Rápido

**Acesso rápido a todas as provas e hashes verificáveis**

---

## 🎯 Acesso Mais Rápido

### 🌐 Via Testnet (Recomendado)
- **Prova Individual:** https://testnet.allianza.tech/proof/<PROOF_ID>
- **Exemplos:**
  - https://testnet.allianza.tech/proof/PILAR_1_INTEROPERABILIDADE
  - https://testnet.allianza.tech/proof/PILAR_2_SEGURANCA_QUANTICA

### 📄 Arquivos Principais
- **Todas as 41 Provas:** [`COMPLETE_TECHNICAL_PROOFS_FINAL.json`](COMPLETE_TECHNICAL_PROOFS_FINAL.json)
- **Hashes On-Chain:** [`VERIFIABLE_ON_CHAIN_PROOFS.md`](VERIFIABLE_ON_CHAIN_PROOFS.md)
- **Índice de Provas:** [`proofs/INDEX.md`](proofs/INDEX.md)
- **Índice de Hashes:** [`proofs/HASHES_INDEX.md`](proofs/HASHES_INDEX.md)

---

## 🔐 Provas de Segurança Quântica

### QRS-3 (Triple Redundancy)
- **ID:** `PILAR_2_SEGURANCA_QUANTICA`
- **Acesso:** https://testnet.allianza.tech/proof/PILAR_2_SEGURANCA_QUANTICA
- **Arquivo:** [`proofs/pilar_2_seguranca_quantica/quantum_security_proof.json`](proofs/pilar_2_seguranca_quantica/quantum_security_proof.json)

### ML-DSA, ML-KEM, SPHINCS+
- **Arquivos:** [`proofs/pqc_complete/`](proofs/pqc_complete/)
- **Verificação:** Execute `python tests/public/run_verification_tests.py`

---

## 🌐 Provas de Interoperabilidade

### ALZ-NIEV Protocol
- **ID:** `PILAR_1_INTEROPERABILIDADE`
- **Acesso:** https://testnet.allianza.tech/proof/PILAR_1_INTEROPERABILIDADE
- **Arquivo:** [`proofs/pilar_1_interoperabilidade/`](proofs/pilar_1_interoperabilidade/)

### Cross-Chain Transfers
- **Polygon→Bitcoin:** [`proofs/real_transfer_polygon_bitcoin.json`](proofs/real_transfer_polygon_bitcoin.json)
- **Real Interop:** [`proofs/interoperability_real/`](proofs/interoperability_real/)

---

## 🔗 Hashes On-Chain Verificáveis

### Bitcoin Testnet
```
842f01a3302b6b19981204c96f377be1ec1dfc51e995f68b3a1563e6750d06e8
```
**Verificar:** https://blockstream.info/testnet/tx/842f01a3302b6b19981204c96f377be1ec1dfc51e995f68b3a1563e6750d06e8

### Ethereum Sepolia
```
0x9a75d8edd1af2f7239db94d799abbdec30c42870899cbdcb5d9d8df4daf27110
```
**Verificar:** https://sepolia.etherscan.io/tx/0x9a75d8edd1af2f7239db94d799abbdec30c42870899cbdcb5d9d8df4daf27110

### Polygon Amoy
```
0x78d157229865c682ad152f22fa56b80707528fbd2bbbf89d7be9f5c2a67313e2
```
**Verificar:** https://amoy.polygonscan.com/tx/0x78d157229865c682ad152f22fa56b80707528fbd2bbbf89d7be9f5c2a67313e2

**📄 Lista Completa:** [`VERIFIABLE_ON_CHAIN_PROOFS.md`](VERIFIABLE_ON_CHAIN_PROOFS.md)

---

## 🧪 Scripts de Teste

### Testes Básicos
```bash
python tests/public/run_verification_tests.py
```

### Testes Completos
```bash
python tests/public/run_all_tests.py
```

### Teste Simples
```bash
python test_simple.py
```

---

## 📊 Estrutura Organizada

```
allianzablockchain/
├── PROVAS_E_HASHES.md              # Este arquivo (guia rápido)
├── COMPLETE_TECHNICAL_PROOFS_FINAL.json  # 41 provas completas
├── VERIFIABLE_ON_CHAIN_PROOFS.md   # Hashes on-chain
│
└── proofs/
    ├── INDEX.md                     # Índice completo de provas
    ├── HASHES_INDEX.md              # Índice de hashes
    ├── README.md                    # Documentação
    │
    ├── pilar_1_interoperabilidade/ # Provas de interoperabilidade
    ├── pilar_2_seguranca_quantica/ # Provas de segurança quântica
    ├── interoperability_real/       # Provas reais
    ├── pqc_complete/               # Provas PQC
    ├── performance_pqc/            # Provas de performance
    └── testnet/                     # Provas da testnet
```

---

## ✅ Verificação Rápida

### 1. Verificar Prova
```bash
# Via testnet
curl https://testnet.allianza.tech/proof/PILAR_1_INTEROPERABILIDADE?format=json

# Via arquivo
cat proofs/pilar_1_interoperabilidade/ethereum_validation_proof.json
```

### 2. Verificar Hash
```bash
# Ver documento
cat VERIFIABLE_ON_CHAIN_PROOFS.md

# Verificar no explorer (links acima)
```

### 3. Executar Testes
```bash
python tests/public/run_verification_tests.py
```

---

**Última atualização:** 2025-12-08

