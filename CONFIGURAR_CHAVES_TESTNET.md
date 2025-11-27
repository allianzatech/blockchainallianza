# 🔑 CONFIGURAR CHAVES PRIVADAS PARA TESTNET

## 🎯 OBJETIVO

Configurar chaves privadas de teste no Render para permitir transferências reais cross-chain na testnet.

---

## 📋 VARIÁVEIS DE AMBIENTE NECESSÁRIAS

### Chaves Principais (Mínimo para funcionar):

1. **POLYGON_PRIVATE_KEY** ⭐ (ESSENCIAL - pode ser usada como fallback)
2. **ETH_PRIVATE_KEY** (Opcional - se não tiver, usa POLYGON_PRIVATE_KEY)
3. **BSC_PRIVATE_KEY** (Opcional - se não tiver, usa POLYGON_PRIVATE_KEY)
4. **BASE_PRIVATE_KEY** (Opcional - se não tiver, usa POLYGON_PRIVATE_KEY)

### RPCs (Já configurados, mas pode personalizar):

- **POLYGON_RPC_URL** (já tem padrão)
- **ETH_RPC_URL** (já tem padrão)
- **BSC_RPC_URL** (já tem padrão)

---

## 🔐 PASSO 1: GERAR CHAVES DE TESTE

### Opção A: Usar MetaMask (Mais Fácil)

1. **Instale MetaMask** (se não tiver)
2. **Crie uma nova carteira** (ou use uma de teste)
3. **Configure as redes de teste:**
   - Polygon Amoy Testnet
   - Ethereum Sepolia Testnet
   - BSC Testnet
   - Base Sepolia Testnet

4. **Exporte a chave privada:**
   - Clique nos 3 pontos → "Detalhes da conta"
   - "Exportar chave privada"
   - Copie a chave (sem o `0x` inicial)

### Opção B: Gerar Programaticamente

Execute no terminal:

```python
from eth_account import Account
import secrets

# Gerar chave privada aleatória
private_key = "0x" + secrets.token_hex(32)
account = Account.from_key(private_key)

print(f"Chave Privada: {private_key}")
print(f"Endereço: {account.address}")
```

**⚠️ IMPORTANTE:** Use apenas para TESTNET! Nunca use chaves reais!

---

## 💰 PASSO 2: OBTER TOKENS DE TESTE

Depois de gerar as chaves, você precisa de tokens de teste:

### Polygon Amoy Testnet:
- **Faucet:** https://faucet.polygon.technology/
- **Cole o endereço** da sua carteira
- **Solicite MATIC**

### Ethereum Sepolia Testnet:
- **Faucet:** https://sepoliafaucet.com/
- **Ou:** https://faucet.quicknode.com/ethereum/sepolia
- **Solicite ETH**

### BSC Testnet:
- **Faucet:** https://testnet.bnbchain.org/faucet-smart
- **Solicite BNB**

### Base Sepolia Testnet:
- **Faucet:** https://www.coinbase.com/faucets/base-ethereum-goerli-faucet
- **Solicite ETH**

---

## ⚙️ PASSO 3: ADICIONAR NO RENDER

1. **Acesse:** https://dashboard.render.com
2. **Vá até:** Seu serviço → **Settings → Environment**
3. **Clique em:** **"Add Environment Variable"**

### Adicione estas variáveis:

#### Variável 1: POLYGON_PRIVATE_KEY
- **KEY:** `POLYGON_PRIVATE_KEY`
- **VALUE:** `sua_chave_privada_aqui` (com ou sem `0x`)
- **Sync:** ✅ (marcar)

#### Variável 2: ETH_PRIVATE_KEY (Opcional)
- **KEY:** `ETH_PRIVATE_KEY`
- **VALUE:** `sua_chave_privada_aqui` (pode ser a mesma do Polygon)
- **Sync:** ✅

#### Variável 3: BSC_PRIVATE_KEY (Opcional)
- **KEY:** `BSC_PRIVATE_KEY`
- **VALUE:** `sua_chave_privada_aqui` (pode ser a mesma do Polygon)
- **Sync:** ✅

#### Variável 4: BASE_PRIVATE_KEY (Opcional)
- **KEY:** `BASE_PRIVATE_KEY`
- **VALUE:** `sua_chave_privada_aqui` (pode ser a mesma do Polygon)
- **Sync:** ✅

---

## 📝 EXEMPLO DE CONFIGURAÇÃO MÍNIMA

**Mínimo necessário (só POLYGON_PRIVATE_KEY):**

```
POLYGON_PRIVATE_KEY=0x1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef
```

O sistema usará essa chave como fallback para outras chains também.

---

## ✅ PASSO 4: VERIFICAR

Após adicionar as variáveis:

1. **Salve as configurações**
2. **O Render fará deploy automático** (ou clique em "Manual Deploy")
3. **Aguarde o deploy** (5-10 minutos)
4. **Teste uma transferência** na testnet

---

## 🧪 PASSO 5: TESTAR

Após o deploy, teste:

1. Acesse: `https://testnet.allianza.tech/testnet/interoperability`
2. Tente fazer uma transferência:
   - Polygon → Ethereum
   - Polygon → BSC
   - Ethereum → Polygon

3. **Deve funcionar!** ✅

---

## ⚠️ SEGURANÇA

### ✅ SEGURO (Testnet):
- ✅ Chaves de teste (sem valor real)
- ✅ Tokens de testnet (sem valor real)
- ✅ Pode compartilhar (são só para teste)

### ❌ NUNCA FAÇA (Mainnet):
- ❌ Usar chaves de carteiras reais
- ❌ Usar tokens reais
- ❌ Expor chaves em código público

---

## 📋 CHECKLIST

- [ ] Gerar chave privada de teste
- [ ] Obter endereço da carteira
- [ ] Solicitar tokens de teste nos faucets
- [ ] Adicionar `POLYGON_PRIVATE_KEY` no Render
- [ ] (Opcional) Adicionar outras chaves
- [ ] Aguardar deploy
- [ ] Testar transferência

---

## 🎯 RESUMO

**Mínimo necessário:**
1. `POLYGON_PRIVATE_KEY` - Chave privada de teste
2. Tokens de teste na carteira (MATIC, ETH, etc.)

**No Render:**
- Settings → Environment → Add Environment Variable
- KEY: `POLYGON_PRIVATE_KEY`
- VALUE: `sua_chave_privada`

**Pronto!** As transferências reais funcionarão! 🚀

---

## 💡 DICA

Você pode usar a **mesma chave privada** para todas as chains de teste (Polygon, Ethereum, BSC, Base). O sistema aceita isso como fallback.

---

**Configure e seus usuários poderão testar transferências reais!** ✅

