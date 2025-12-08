# 🧪 Como Testar UChainID e ZK Proofs no Dashboard

**Data:** 2025-12-08  
**Status:** ✅ **Código no GitHub - Pronto para Testar**

---

## ✅ Verificação: Código no GitHub

O código foi enviado para o GitHub nos commits:
- `54f421a` - feat: Implement UChainID and ZK Proofs in on-chain memos
- `990eaba` - docs: Add implementation documentation

**Repositório:** https://github.com/dieisonmaach-lang/allianzablockchain

---

## 🧪 Como Testar no Dashboard/Testnet

### Opção 1: Via API REST (Recomendado)

#### 1. Criar Transferência Cross-Chain com UChainID

**URL:** `https://testnet.allianza.tech/api/cross-chain/transfer`

**Método:** POST

**Body (JSON):**
```json
{
  "source_chain": "polygon",
  "target_chain": "ethereum",
  "amount": 0.1,
  "recipient": "0x86AE40869EB6ACb9477b42BfC9150c0A2Cc21f5E",
  "send_real": true,
  "token_symbol": "ETH"
}
```

**Exemplo com cURL:**
```bash
curl -X POST https://testnet.allianza.tech/api/cross-chain/transfer \
  -H "Content-Type: application/json" \
  -d '{
    "source_chain": "polygon",
    "target_chain": "ethereum",
    "amount": 0.1,
    "recipient": "0x86AE40869EB6ACb9477b42BfC9150c0A2Cc21f5E",
    "send_real": true
  }'
```

**Resposta Esperada:**
```json
{
  "success": true,
  "transfer_id": "bridge_free_...",
  "uchain_id": "UCHAIN-abc123...",
  "memo": {
    "uchain_id": "UCHAIN-abc123...",
    "alz_niev_version": "1.0",
    "zk_proof": {
      "proof_id": "...",
      "state_hash": "...",
      "verified": true
    },
    "source_chain": "polygon",
    "target_chain": "ethereum",
    "amount": 0.1
  },
  "tx_hash": "0x...",
  "explorer_url": "https://sepolia.etherscan.io/tx/0x...",
  "has_zk_proof": true
}
```

#### 2. Buscar Prova por UChainID

**URL:** `https://testnet.allianza.tech/api/cross-chain/proof/<UCHAIN_ID>`

**Método:** GET

**Exemplo:**
```bash
curl https://testnet.allianza.tech/api/cross-chain/proof/UCHAIN-abc123...
```

**Resposta Esperada:**
```json
{
  "success": true,
  "uchain_id": "UCHAIN-abc123...",
  "source_chain": "polygon",
  "target_chain": "ethereum",
  "recipient": "0x86AE40869EB6ACb9477b42BfC9150c0A2Cc21f5E",
  "amount": 0.1,
  "memo": {...},
  "zk_proof": {...}
}
```

#### 3. Listar Todas as Provas

**URL:** `https://testnet.allianza.tech/api/cross-chain/proofs?limit=50`

**Método:** GET

**Exemplo:**
```bash
curl https://testnet.allianza.tech/api/cross-chain/proofs?limit=50
```

**Resposta Esperada:**
```json
{
  "success": true,
  "total": 10,
  "returned": 10,
  "proofs": [
    {
      "uchain_id": "UCHAIN-abc123...",
      "source_chain": "polygon",
      "target_chain": "ethereum",
      "amount": 0.1,
      "timestamp": 1733688000,
      "has_zk_proof": true
    },
    ...
  ]
}
```

#### 4. Status do Sistema

**URL:** `https://testnet.allianza.tech/api/cross-chain/status`

**Método:** GET

**Exemplo:**
```bash
curl https://testnet.allianza.tech/api/cross-chain/status
```

---

### Opção 2: Via Interface Web (Se Implementada)

1. **Acesse:** `https://testnet.allianza.tech`
2. **Navegue para:** Seção de Interoperabilidade ou Cross-Chain
3. **Preencha o formulário:**
   - Source Chain: Polygon
   - Target Chain: Ethereum
   - Amount: 0.1
   - Recipient: 0x86AE40869EB6ACb9477b42BfC9150c0A2Cc21f5E
4. **Clique em:** "Transfer with UChainID"
5. **Veja o resultado:**
   - UChainID gerado
   - Link para explorer
   - Memo com ZK Proof

---

### Opção 3: Via Python (Local)

```python
from core.interoperability.bridge_free_interop import bridge_free_interop

# Criar transferência
result = bridge_free_interop.bridge_free_transfer(
    source_chain="polygon",
    target_chain="ethereum",
    amount=0.1,
    token_symbol="ETH",
    recipient="0x86AE40869EB6ACb9477b42BfC9150c0A2Cc21f5E",
    send_real=True
)

print(f"UChainID: {result.get('uchain_id')}")
print(f"TX Hash: {result.get('tx_hash')}")
print(f"Explorer: {result.get('explorer_url')}")

# Buscar prova
proof = bridge_free_interop.get_cross_chain_proof(
    uchain_id=result.get('uchain_id')
)
print(f"Prova: {proof}")
```

---

## 🔍 Como Verificar no Explorer

### 1. Acesse o Explorer

Use o `explorer_url` retornado na resposta, por exemplo:
- Ethereum Sepolia: `https://sepolia.etherscan.io/tx/0x...`
- Polygon Amoy: `https://amoy.polygonscan.com/tx/0x...`

### 2. Veja o Campo "Input Data"

1. Role até a seção "Input Data"
2. Você verá dados em hex (ex.: `0x7b22636861696e...`)
3. Clique em "Decode Input Data" ou use um decodificador online

### 3. Decodifique o Hex para JSON

O memo estará no formato:
```json
{
  "uchain_id": "UCHAIN-abc123...",
  "alz_niev_version": "1.0",
  "zk_proof": {
    "proof_id": "...",
    "state_hash": "...",
    "verified": true
  },
  "source_chain": "polygon",
  "target_chain": "ethereum",
  "amount": 0.1,
  "timestamp": "2025-12-08T..."
}
```

---

## 📊 Verificar Métricas

### Contar Transações com UChainID

```bash
# Listar todas e contar
curl https://testnet.allianza.tech/api/cross-chain/proofs | jq '.total'

# Ou via Python
import requests
response = requests.get('https://testnet.allianza.tech/api/cross-chain/proofs')
data = response.json()
print(f"Total de provas: {data['total']}")
```

### Contar Transações com ZK Proof

```bash
# Via API
curl https://testnet.allianza.tech/api/cross-chain/proofs | jq '.proofs[] | select(.has_zk_proof == true) | length'

# Ou via Python
import requests
response = requests.get('https://testnet.allianza.tech/api/cross-chain/proofs')
data = response.json()
zk_proofs = [p for p in data['proofs'] if p.get('has_zk_proof')]
print(f"Provas com ZK Proof: {len(zk_proofs)}")
```

---

## ✅ Checklist de Teste

- [ ] Criar 1 transferência cross-chain
- [ ] Verificar que UChainID foi gerado
- [ ] Verificar que memo foi incluído na transação
- [ ] Verificar que ZK Proof está no memo
- [ ] Acessar explorer e verificar "Input Data"
- [ ] Decodificar hex e verificar JSON do memo
- [ ] Buscar prova por UChainID via API
- [ ] Listar todas as provas via API
- [ ] Verificar status do sistema

**Meta:** 10+ transações com UChainID, 5+ com ZK Proofs

---

## 🐛 Troubleshooting

### Erro: "Private key não configurada"

**Solução:** Configure no `.env`:
```
POLYGON_PRIVATE_KEY=0x...
ETH_PRIVATE_KEY=0x...
BSC_PRIVATE_KEY=0x...
```

### Erro: "Saldo insuficiente"

**Solução:** 
- Solicite tokens no faucet
- Ou use `send_real=False` para simulação

### Erro: "Não conectado à chain"

**Solução:**
- Verifique RPC URLs no `.env`
- Ou use testnet público (não requer RPC local)

### Memo não aparece no explorer

**Possíveis causas:**
- Transação ainda não confirmada (aguarde alguns segundos)
- Explorer pode ter delay (tente novamente em 1-2 minutos)
- Memo muito grande (foi truncado para 24KB)

---

## 📝 Notas Importantes

1. **Testnet Real:** As transações aparecem nos explorers públicos
2. **Gas Fees:** Você precisa ter tokens para pagar gas
3. **Confirmação:** Aguarde confirmação antes de verificar no explorer
4. **Memos:** Limitados a ~24KB (EVM limit)

---

**Última atualização:** 2025-12-08  
**Status:** ✅ **PRONTO PARA TESTAR**

