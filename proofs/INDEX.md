# 📋 Índice de Provas - Allianza Blockchain

**Última atualização:** 2025-12-08

---

## 🎯 Acesso Rápido

### 🌐 Provas via Testnet (Recomendado)
- **Dashboard:** https://testnet.allianza.tech/proof/<PROOF_ID>
- **API JSON:** https://testnet.allianza.tech/proof/<PROOF_ID>?format=json

### 📄 Arquivos Locais
- **Provas Completas:** [`../COMPLETE_TECHNICAL_PROOFS_FINAL.json`](../COMPLETE_TECHNICAL_PROOFS_FINAL.json)
- **Provas On-Chain:** [`../VERIFIABLE_ON_CHAIN_PROOFS.md`](../VERIFIABLE_ON_CHAIN_PROOFS.md)

---

## 📊 Provas por Categoria

### 1. 🔐 Segurança Quântica (QRS-3)

#### Provas Principais
- **PILAR_2_SEGURANCA_QUANTICA** - Prova completa de segurança quântica
  - Web: https://testnet.allianza.tech/proof/PILAR_2_SEGURANCA_QUANTICA
  - Arquivo: [`pilar_2_seguranca_quantica/quantum_security_proof.json`](pilar_2_seguranca_quantica/quantum_security_proof.json)

#### Provas Detalhadas
- **QRS-3 Verification:** [`qrs3_verification_proof.json`](qrs3_verification_proof.json)
- **PQC Complete:** [`pqc_complete/`](pqc_complete/)
- **QSS Quantum Proof:** [`qss_quantum_proof.json`](qss_quantum_proof.json)

---

### 2. 🌐 Interoperabilidade (ALZ-NIEV)

#### Provas Principais
- **PILAR_1_INTEROPERABILIDADE** - Prova completa de interoperabilidade
  - Web: https://testnet.allianza.tech/proof/PILAR_1_INTEROPERABILIDADE
  - Arquivo: [`pilar_1_interoperabilidade/`](pilar_1_interoperabilidade/)

#### Provas Detalhadas
- **Real Interoperability:** [`interoperability_real/`](interoperability_real/)
- **Cross-Chain Execution:** [`alz_niev_cross_chain_execution.json`](alz_niev_cross_chain_execution.json)
- **Atomic Execution:** [`alz_niev_atomic_execution.json`](alz_niev_atomic_execution.json)
- **Real Transfer Polygon→Bitcoin:** [`real_transfer_polygon_bitcoin.json`](real_transfer_polygon_bitcoin.json)

---

### 3. ⚡ Performance

#### Provas de Performance
- **Performance PQC:** [`performance_pqc/`](performance_pqc/)
- **50 Melhorias:** [`teste_real_50_melhorias_*.json`](teste_real_50_melhorias_*.json)

---

### 4. 🔗 Transações On-Chain Reais

#### Hashes Verificáveis
**📄 Documento Completo:** [`../VERIFIABLE_ON_CHAIN_PROOFS.md`](../VERIFIABLE_ON_CHAIN_PROOFS.md)

**Bitcoin Testnet:**
- Hash: `842f01a3302b6b19981204c96f377be1ec1dfc51e995f68b3a1563e6750d06e8`
- Explorer: https://blockstream.info/testnet/tx/842f01a3302b6b19981204c96f377be1ec1dfc51e995f68b3a1563e6750d06e8

**Ethereum Sepolia:**
- Hash: `0x9a75d8edd1af2f7239db94d799abbdec30c42870899cbdcb5d9d8df4daf27110`
- Explorer: https://sepolia.etherscan.io/tx/0x9a75d8edd1af2f7239db94d799abbdec30c42870899cbdcb5d9d8df4daf27110

**Polygon Amoy:**
- Verificar em: https://amoy.polygonscan.com/

---

## 📁 Estrutura de Diretórios

```
proofs/
├── INDEX.md                          # Este arquivo
├── README.md                         # Documentação geral
│
├── pilar_1_interoperabilidade/      # Provas de interoperabilidade
│   ├── bitcoin_validation_proof.json
│   ├── ethereum_validation_proof.json
│   └── polygon_validation_proof.json
│
├── pilar_2_seguranca_quantica/      # Provas de segurança quântica
│   └── quantum_security_proof.json
│
├── interoperability_real/           # Provas reais de interoperabilidade
│   ├── ethereum_validation_proof.json
│   └── polygon_validation_proof.json
│
├── pqc_complete/                    # Provas PQC completas
│   └── PROVA_PQC_COMPLETA_*.json
│
├── performance_pqc/                 # Provas de performance
│   └── performance_test_*.json
│
├── testnet/                         # Provas da testnet
│   ├── public_tests/               # Testes públicos
│   └── verification_*.json          # Verificações
│
└── relatorio_investidores/         # Relatórios para investidores
    └── RELATORIO_PROVAS_INVESTIDORES_*.md
```

---

## 🔍 Como Encontrar Provas Específicas

### Por ID de Prova
```bash
# Via testnet (recomendado)
curl https://testnet.allianza.tech/proof/<PROOF_ID>?format=json

# Via arquivo local
grep -r "<PROOF_ID>" proofs/
```

### Por Tipo
```bash
# Segurança quântica
ls proofs/pilar_2_seguranca_quantica/
ls proofs/pqc_complete/

# Interoperabilidade
ls proofs/pilar_1_interoperabilidade/
ls proofs/interoperability_real/

# Performance
ls proofs/performance_pqc/
```

### Por Hash de Transação
```bash
# Verificar hash em VERIFIABLE_ON_CHAIN_PROOFS.md
grep "<HASH>" VERIFIABLE_ON_CHAIN_PROOFS.md
```

---

## ✅ Verificação Rápida

### 1. Verificar Prova Individual
```bash
# Via testnet
curl https://testnet.allianza.tech/proof/PILAR_1_INTEROPERABILIDADE?format=json

# Via arquivo
cat proofs/pilar_1_interoperabilidade/ethereum_validation_proof.json
```

### 2. Verificar Hash On-Chain
```bash
# Ver documento completo
cat VERIFIABLE_ON_CHAIN_PROOFS.md

# Verificar no explorer
# Bitcoin: https://blockstream.info/testnet/tx/<HASH>
# Ethereum: https://sepolia.etherscan.io/tx/<HASH>
```

### 3. Executar Testes
```bash
# Testes básicos
python tests/public/run_verification_tests.py

# Testes completos
python tests/public/run_all_tests.py
```

---

## 📊 Estatísticas

- **Total de Provas:** 41 (conforme `COMPLETE_TECHNICAL_PROOFS_FINAL.json`)
- **Provas On-Chain:** 10+ (verificáveis em explorers públicos)
- **Provas de Performance:** 5+
- **Provas de Interoperabilidade:** 15+

---

**Última atualização:** 2025-12-08

