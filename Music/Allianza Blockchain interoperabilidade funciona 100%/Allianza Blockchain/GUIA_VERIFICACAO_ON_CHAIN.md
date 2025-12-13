# 🔍 Guia Completo: Verificação On-Chain de Transferências Cross-Chain

**Data:** 2025-12-08

---

## 📋 Objetivo

Este guia mostra como verificar transferências cross-chain **diretamente nos explorers de blockchain**, provando que as transações são **reais e verificáveis**.

---

## 🎯 Pré-requisitos

### 1. Saldo Suficiente

**Para Polygon → Ethereum:**
- **Polygon (Amoy):** >0.1 MATIC + gas (~0.001 MATIC)
- **Ethereum (Sepolia):** >0.1 ETH + gas (~0.000041 ETH)

**Faucets:**
- Polygon: https://faucet.polygon.technology
- Ethereum: https://sepoliafaucet.com

### 2. Endereço de Destino

Use um endereço que você controla:
```
0x86AE40869EB6ACb9477b42BfC9150c0A2Cc21f5E
```

---

## 🚀 Passo a Passo

### Passo 1: Criar Transferência Real

1. Acesse: https://testnet.allianza.tech/cross-chain-test
2. Preencha o formulário:
   ```
   Source Chain: Polygon
   Target Chain: Ethereum
   Amount: 0.1
   Recipient: 0x86AE40869EB6ACb9477b42BfC9150c0A2Cc21f5E
   Token Symbol: ETH
   ✅ Send REAL transaction (marcar)
   ```
3. Clique em "Create Cross-Chain Transfer"
4. **Copie o `tx_hash` retornado**

### Passo 2: Verificar no Polygon Explorer (Source)

1. Acesse: https://amoy.polygonscan.com
2. Cole o `tx_hash` no campo de busca
3. Clique na transação
4. Procure por:
   - **"Input Data"** ou **"Data"**
   - Clique em **"Click to see more"**
   - Selecione **"View Input As"** → **"UTF-8"** ou **"Text"**

**O que você verá:**
```json
{
  "alz_niev_version": "1.0",
  "amount": 0.1,
  "source_chain": "polygon",
  "target_chain": "ethereum",
  "timestamp": "2025-12-08T18:30:11.914248",
  "type": "cross_chain_transfer",
  "uchain_id": "UCHAIN-bee7ff2415e0934463387914219c89aa",
  "zk_proof": {
    "proof_id": "zk_proof_1765218611_7c60f438878dd596",
    "state_hash": "d47a09681949ba916e2c1fe4fdf35817afec8057ba9278e485b0e12e31058b72",
    "verified": true
  }
}
```

### Passo 3: Verificar no Ethereum Explorer (Target)

1. Acesse: https://sepolia.etherscan.io
2. Cole o `tx_hash` retornado (da transação Ethereum)
3. Clique na transação
4. Procure por:
   - **"Input Data"**
   - Clique em **"Decode Input Data"**
   - Ou copie o hex e decodifique manualmente

**O que você verá:**
- Mesmo memo JSON com UChainID e ZK Proof
- Confirmação de que a transferência foi aplicada

---

## 🔧 Decodificação Manual do Hex

### Se o Explorer Não Decodificar Automaticamente:

**Python:**
```python
import json

# Hex do data field (sem 0x)
memo_hex = "7b22616c7a5f6e6965765f76657273696f6e223a22312e30222c..."

# Converter hex para bytes
memo_bytes = bytes.fromhex(memo_hex)

# Decodificar UTF-8
memo_text = memo_bytes.decode('utf-8')

# Parse JSON
memo_json = json.loads(memo_text)

# Imprimir formatado
print(json.dumps(memo_json, indent=2))
```

**JavaScript (Node.js):**
```javascript
const memoHex = "7b22616c7a5f6e6965765f76657273696f6e223a22312e30222c...";
const memoBytes = Buffer.from(memoHex, 'hex');
const memoText = memoBytes.toString('utf-8');
const memoJson = JSON.parse(memoText);
console.log(JSON.stringify(memoJson, null, 2));
```

**Online Tools:**
- https://www.rapidtables.com/convert/number/hex-to-ascii.html
- https://www.hexdictionary.com/hexdecoder/
- Cole o hex (sem 0x) e converta para ASCII/UTF-8

---

## 📊 O Que Verificar

### ✅ Checklist de Verificação:

1. **UChainID Presente:**
   - Deve começar com `UCHAIN-`
   - 32 caracteres após o prefixo
   - Exemplo: `UCHAIN-bee7ff2415e0934463387914219c89aa`

2. **ZK Proof ID Presente:**
   - Deve começar com `zk_proof_`
   - Exemplo: `zk_proof_1765218611_7c60f438878dd596`

3. **State Hash Presente:**
   - Hash SHA-256 (64 caracteres hex)
   - Exemplo: `d47a09681949ba916e2c1fe4fdf35817afec8057ba9278e485b0e12e31058b72`

4. **Timestamp Válido:**
   - Formato ISO 8601
   - Exemplo: `2025-12-08T18:30:11.914248`

5. **Chains Corretas:**
   - `source_chain`: Polygon
   - `target_chain`: Ethereum

6. **Amount Correto:**
   - Deve corresponder ao valor enviado
   - Exemplo: `0.1`

---

## 🔍 Buscar UChainID na Interface

1. Acesse: https://testnet.allianza.tech/cross-chain-test
2. Role até "Search Proof by UChainID"
3. Cole o UChainID: `UCHAIN-bee7ff2415e0934463387914219c89aa`
4. Clique em "Search Proof"
5. **Resultado:** Deve mostrar o memo completo e ZK Proof

---

## 📡 Verificação via API

### Buscar por UChainID:

```bash
curl https://testnet.allianza.tech/api/cross-chain/proof/UCHAIN-bee7ff2415e0934463387914219c89aa
```

**Resposta:**
```json
{
  "success": true,
  "uchain_id": "UCHAIN-bee7ff2415e0934463387914219c89aa",
  "amount": 0.1,
  "source_chain": "polygon",
  "target_chain": "ethereum",
  "memo": { ... },
  "zk_proof": { ... }
}
```

### Listar Todas as Provas:

```bash
curl https://testnet.allianza.tech/api/cross-chain/proofs?limit=50
```

---

## 🎯 Exemplo Completo

### 1. Criar Transferência:
```
POST /api/cross-chain/transfer
{
  "source_chain": "polygon",
  "target_chain": "ethereum",
  "amount": 0.1,
  "recipient": "0x86AE40869EB6ACb9477b42BfC9150c0A2Cc21f5E",
  "send_real": true
}
```

### 2. Resposta:
```json
{
  "success": true,
  "uchain_id": "UCHAIN-bee7ff2415e0934463387914219c89aa",
  "tx_hash": "0x1234...5678",
  "explorer_url": "https://amoy.polygonscan.com/tx/0x1234...5678"
}
```

### 3. Verificar no Explorer:
- Acesse: https://amoy.polygonscan.com/tx/0x1234...5678
- Veja o `data` field
- Decodifique para ver UChainID e ZK Proof

### 4. Buscar UChainID:
- Use a interface web ou API
- Confirme que os dados correspondem

---

## ✅ Conclusão

Com este guia, você pode:
1. ✅ Criar transferências reais
2. ✅ Verificar on-chain nos explorers
3. ✅ Decodificar memos hex
4. ✅ Confirmar UChainID e ZK Proof
5. ✅ Provar que é interoperabilidade REAL

**Isso prova que o ALZ-NIEV Protocol funciona e é verificável!**

---

**Última atualização:** 2025-12-08

