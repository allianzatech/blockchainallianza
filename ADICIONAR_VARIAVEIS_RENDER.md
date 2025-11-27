# ⚙️ ADICIONAR VARIÁVEIS DE AMBIENTE NO RENDER

## 🎯 OBJETIVO

Configurar todas as variáveis do seu `.env` no Render para habilitar transferências reais cross-chain.

---

## 📋 VARIÁVEIS PARA ADICIONAR NO RENDER

### 🔐 Chaves Privadas (ESSENCIAIS para transferências):

#### 1. POLYGON_PRIVATE_KEY
- **KEY:** `POLYGON_PRIVATE_KEY`
- **VALUE:** `a2b050a9ff78efabced4fd16bf5e51d204fd9a1bdab4b56418a5148fe70b4c28`
- **Sync:** ✅

#### 2. ETH_PRIVATE_KEY (ou REAL_ETH_PRIVATE_KEY)
- **KEY:** `ETH_PRIVATE_KEY`
- **VALUE:** `0xa2b050a9ff78efabced4fd16bf5e51d204fd9a1bdab4b56418a5148fe70b4c28`
- **Sync:** ✅

#### 3. BASE_PRIVATE_KEY
- **KEY:** `BASE_PRIVATE_KEY`
- **VALUE:** `a2b050a9ff78efabced4fd16bf5e51d204fd9a1bdab4b56418a5148fe70b4c28`
- **Sync:** ✅

#### 4. SOLANA_PRIVATE_KEY
- **KEY:** `SOLANA_PRIVATE_KEY`
- **VALUE:** `3VLK1GhCx6o7PimEPb5dgn6qUdtf7Ykxc1RmEH7ToVtUycvMmUH1cQj7GSajjZW9xuvSjco19YUqtrqat9kohHHx`
- **Sync:** ✅

#### 5. BITCOIN_PRIVATE_KEY
- **KEY:** `BITCOIN_PRIVATE_KEY`
- **VALUE:** `cSamqcRz79BCXe5LWhqVSMhKo1bkxZA3EE6PTpy8hkYVVmofUXfJ`
- **Sync:** ✅

---

### 🌐 RPCs (Já tem padrões, mas pode personalizar):

#### 6. ETH_RPC_URL
- **KEY:** `ETH_RPC_URL`
- **VALUE:** `https://sepolia.infura.io/v3/4622f8123b1a4cf7a3e30098d9120d7f`
- **Sync:** ✅

#### 7. POLYGON_RPC_URL
- **KEY:** `POLYGON_RPC_URL`
- **VALUE:** `https://rpc-amoy.polygon.technology/`
- **Sync:** ✅

#### 8. BASE_RPC_URL
- **KEY:** `BASE_RPC_URL`
- **VALUE:** `https://base-sepolia-rpc.publicnode.com`
- **Sync:** ✅

#### 9. SOLANA_RPC_URL
- **KEY:** `SOLANA_RPC_URL`
- **VALUE:** `https://api.testnet.solana.com`
- **Sync:** ✅

---

### 🔑 APIs e Tokens:

#### 10. BLOCKCYPHER_API_TOKEN
- **KEY:** `BLOCKCYPHER_API_TOKEN`
- **VALUE:** `17766314e49c439e85cec883969614ac`
- **Sync:** ✅

#### 11. INFURA_PROJECT_ID
- **KEY:** `INFURA_PROJECT_ID`
- **VALUE:** `4622f8123b1a4cf7a3e30098d9120d7f`
- **Sync:** ✅

#### 12. INFURA_PROJECT_SECRET
- **KEY:** `INFURA_PROJECT_SECRET`
- **VALUE:** `17766314e49c439e85cec883969614ac`
- **Sync:** ✅

---

### ⚙️ Configurações:

#### 13. BLOCKCHAIN_MODE
- **KEY:** `BLOCKCHAIN_MODE`
- **VALUE:** `testnet`
- **Sync:** ✅

#### 14. REAL_BRIDGE_OWNER
- **KEY:** `REAL_BRIDGE_OWNER`
- **VALUE:** `0x86AE40869EB6ACb9477b42BfC9150c0A2Cc21f5E`
- **Sync:** ✅

---

## 🚀 PASSO A PASSO NO RENDER

### 1. Acesse o Render Dashboard
- Vá em: https://dashboard.render.com
- Clique no seu serviço: **allianzablockchain**

### 2. Vá em Settings → Environment

### 3. Adicione cada variável

Para cada variável acima:
1. Clique em **"Add Environment Variable"**
2. Cole o **KEY** (nome da variável)
3. Cole o **VALUE** (valor)
4. Marque **"Sync"** se disponível
5. Clique em **"Save"**

### 4. Repita para todas as variáveis

Adicione todas as 14 variáveis listadas acima.

---

## 📋 LISTA RÁPIDA (Copiar e Colar)

### Chaves Privadas:
```
POLYGON_PRIVATE_KEY=a2b050a9ff78efabced4fd16bf5e51d204fd9a1bdab4b56418a5148fe70b4c28
ETH_PRIVATE_KEY=0xa2b050a9ff78efabced4fd16bf5e51d204fd9a1bdab4b56418a5148fe70b4c28
BASE_PRIVATE_KEY=a2b050a9ff78efabced4fd16bf5e51d204fd9a1bdab4b56418a5148fe70b4c28
SOLANA_PRIVATE_KEY=3VLK1GhCx6o7PimEPb5dgn6qUdtf7Ykxc1RmEH7ToVtUycvMmUH1cQj7GSajjZW9xuvSjco19YUqtrqat9kohHHx
BITCOIN_PRIVATE_KEY=cSamqcRz79BCXe5LWhqVSMhKo1bkxZA3EE6PTpy8hkYVVmofUXfJ
```

### RPCs:
```
ETH_RPC_URL=https://sepolia.infura.io/v3/4622f8123b1a4cf7a3e30098d9120d7f
POLYGON_RPC_URL=https://rpc-amoy.polygon.technology/
BASE_RPC_URL=https://base-sepolia-rpc.publicnode.com
SOLANA_RPC_URL=https://api.testnet.solana.com
```

### APIs:
```
BLOCKCYPHER_API_TOKEN=17766314e49c439e85cec883969614ac
INFURA_PROJECT_ID=4622f8123b1a4cf7a3e30098d9120d7f
INFURA_PROJECT_SECRET=17766314e49c439e85cec883969614ac
```

### Configurações:
```
BLOCKCHAIN_MODE=testnet
REAL_BRIDGE_OWNER=0x86AE40869EB6ACb9477b42BfC9150c0A2Cc21f5E
```

---

## ✅ APÓS ADICIONAR TODAS

1. **Salve todas as configurações**
2. **O Render fará deploy automático** (ou clique em "Manual Deploy")
3. **Aguarde 5-10 minutos**
4. **Teste transferências reais!** 🚀

---

## 🧪 TESTAR

Após o deploy, teste:

1. Acesse: `https://testnet.allianza.tech/testnet/interoperability`
2. Tente transferências:
   - Polygon → Ethereum ✅
   - Polygon → BSC ✅
   - Ethereum → Polygon ✅
   - Polygon → Bitcoin ✅

**Deve funcionar perfeitamente!** ✅

---

## 📝 NOTA

Algumas variáveis podem ter nomes diferentes no código. Se alguma não funcionar, tente também:
- `REAL_ETH_PRIVATE_KEY` (além de `ETH_PRIVATE_KEY`)
- `REAL_POLY_PRIVATE_KEY` (além de `POLYGON_PRIVATE_KEY`)
- `POLYGON_MASTER_PRIVATE_KEY` (além de `POLYGON_PRIVATE_KEY`)

---

**Adicione todas essas variáveis no Render e as transferências reais funcionarão!** 🎉

