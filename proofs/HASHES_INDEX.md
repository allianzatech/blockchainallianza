# 🔗 Índice de Hashes - Allianza Blockchain

**Última atualização:** 2025-12-08

Este documento lista **todos os hashes de transações reais** que podem ser verificados em explorers públicos.

---

## 📋 Documento Principal

**📄 Ver Hashes Completos:** [`../VERIFIABLE_ON_CHAIN_PROOFS.md`](../VERIFIABLE_ON_CHAIN_PROOFS.md)

---

## ₿ Bitcoin Testnet

### Hash 1
```
842f01a3302b6b19981204c96f377be1ec1dfc51e995f68b3a1563e6750d06e8
```
- **Explorer:** https://blockstream.info/testnet/tx/842f01a3302b6b19981204c96f377be1ec1dfc51e995f68b3a1563e6750d06e8
- **Status:** ✅ Verificável

### Hash 2
```
89b6d1b46c2a1f93bd1d9ccc95dd25b46a81c7f37cb7b2a11abbebd29ddafaeb
```
- **Explorer:** https://blockstream.info/testnet/tx/89b6d1b46c2a1f93bd1d9ccc95dd25b46a81c7f37cb7b2a11abbebd29ddafaeb
- **Status:** ✅ Verificável

---

## 🔷 Ethereum Sepolia

### Hash 1
```
0x9a75d8edd1af2f7239db94d799abbdec30c42870899cbdcb5d9d8df4daf27110
```
- **Explorer:** https://sepolia.etherscan.io/tx/0x9a75d8edd1af2f7239db94d799abbdec30c42870899cbdcb5d9d8df4daf27110
- **Status:** ✅ Verificável

### Hash 2
```
0x797ed08087074ccbf134d3a26a0fd3daa1cb541aa1494b253db80ba73501c477
```
- **Explorer:** https://sepolia.etherscan.io/tx/0x797ed08087074ccbf134d3a26a0fd3daa1cb541aa1494b253db80ba73501c477
- **Status:** ✅ Verificável

---

## 🔷 Polygon Amoy

### Hash 1
```
0x78d157229865c682ad152f22fa56b80707528fbd2bbbf89d7be9f5c2a67313e2
```
- **Explorer:** https://amoy.polygonscan.com/tx/0x78d157229865c682ad152f22fa56b80707528fbd2bbbf89d7be9f5c2a67313e2
- **Status:** ✅ Verificável

---

## 🔍 Como Verificar

### Método 1: Via Explorer
1. Copie o hash acima
2. Acesse o explorer correspondente
3. Cole o hash na busca
4. Verifique que a transação existe

### Método 2: Via Testnet Allianza
1. Acesse: https://testnet.allianza.tech/qrs3-verifier
2. Cole o hash
3. Gere prova QRS-3
4. Verifique a prova

### Método 3: Via API
```bash
# Gerar prova para hash
curl -X POST https://testnet.allianza.tech/api/qss/generate-proof \
  -H "Content-Type: application/json" \
  -d '{"transaction_hash": "<HASH_AQUI>"}'
```

---

## 📊 Estatísticas

- **Bitcoin Testnet:** 2+ hashes verificáveis
- **Ethereum Sepolia:** 2+ hashes verificáveis
- **Polygon Amoy:** 1+ hashes verificáveis
- **Total:** 5+ hashes on-chain verificáveis

---

**Para lista completa, veja:** [`VERIFIABLE_ON_CHAIN_PROOFS.md`](../VERIFIABLE_ON_CHAIN_PROOFS.md)

