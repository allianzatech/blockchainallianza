# 🚰 Endereços e Faucets - Guia Rápido

**Data:** 2025-12-08

---

## 📋 Endereços Configurados

### ✅ Endereços em Uso no Sistema:

```
Bitcoin (Testnet):  mjQMvYHE5Bpqze4ifq6NLP9BthNJgxWRud
Ethereum (Sepolia): 0x86AE40869EB6ACb9477b42BfC9150c0A2Cc21f5E
Polygon (Amoy):     0x86AE40869EB6ACb9477b42BfC9150c0A2Cc21f5E
BSC (Testnet):      0x86AE40869EB6ACb9477b42BfC9150c0A2Cc21f5E
```

**Nota:** Ethereum, Polygon e BSC usam o mesmo endereço (formato EVM).

---

## 🚰 Faucets por Blockchain

### 1. ₿ Bitcoin Testnet

**Endereço:** `mjQMvYHE5Bpqze4ifq6NLP9BthNJgxWRud`

**Faucets:**
1. https://bitcoinfaucet.uo1.net/
2. https://testnet-faucet.mempool.co/
3. https://live.blockcypher.com/btc-testnet/faucet/
4. https://testnet-faucet.com/btc-testnet/

**Explorer:** https://blockstream.info/testnet/address/mjQMvYHE5Bpqze4ifq6NLP9BthNJgxWRud

---

### 2. 🔷 Ethereum Sepolia

**Endereço:** `0x86AE40869EB6ACb9477b42BfC9150c0A2Cc21f5E`

**Faucets:**
1. https://sepoliafaucet.com/ (0.5 ETH)
2. https://www.alchemy.com/faucets/ethereum-sepolia (0.5 ETH)
3. https://faucet.quicknode.com/ethereum/sepolia (0.1 ETH)
4. https://sepolia-faucet.pk910.de/ (0.5 ETH - PoW)

**Explorer:** https://sepolia.etherscan.io/address/0x86AE40869EB6ACb9477b42BfC9150c0A2Cc21f5E

---

### 3. 🔷 Polygon Amoy

**Endereço:** `0x86AE40869EB6ACb9477b42BfC9150c0A2Cc21f5E`

**Faucets:**
1. https://faucet.polygon.technology/ (0.1 MATIC)
2. https://www.alchemy.com/faucets/polygon-amoy (0.1 MATIC)
3. https://faucet.quicknode.com/polygon/amoy (0.1 MATIC)

**Explorer:** https://amoy.polygonscan.com/address/0x86AE40869EB6ACb9477b42BfC9150c0A2Cc21f5E

---

### 4. 🔷 BSC Testnet

**Endereço:** `0x86AE40869EB6ACb9477b42BfC9150c0A2Cc21f5E`

**Faucets:**
1. https://testnet.binance.org/faucet-smart (1 BNB)
2. https://faucet.quicknode.com/binance/bnb-testnet (0.1 BNB)

**Explorer:** https://testnet.bscscan.com/address/0x86AE40869EB6ACb9477b42BfC9150c0A2Cc21f5E

---

## 💰 Saldos Mínimos para Testes

| Blockchain | Mínimo Recomendado | Gas Estimado |
|------------|-------------------|--------------|
| Bitcoin | 0.001 BTC | ~0.00001 BTC |
| Ethereum | 0.1 ETH | ~0.000041 ETH |
| Polygon | 0.1 MATIC | ~0.0001 MATIC |
| BSC | 0.1 BNB | ~0.0001 BNB |

---

## 🎯 Como Obter Tokens

### Método 1: Manual (Recomendado)

1. Acesse o faucet desejado
2. Cole o endereço correspondente
3. Siga as instruções (login, CAPTCHA, etc.)
4. Aguarde confirmação (1-5 minutos)

### Método 2: Automático

O sistema já tem gerenciador automático que verifica saldos a cada 12 horas.

**Configurar no `.env`:**
```env
BITCOIN_TESTNET_ADDRESS=mjQMvYHE5Bpqze4ifq6NLP9BthNJgxWRud
ETHEREUM_ADDRESS=0x86AE40869EB6ACb9477b42BfC9150c0A2Cc21f5E
POLYGON_ADDRESS=0x86AE40869EB6ACb9477b42BfC9150c0A2Cc21f5E
BSC_ADDRESS=0x86AE40869EB6ACb9477b42BfC9150c0A2Cc21f5E
```

---

## ⚠️ Nota sobre Bitcoin

Bitcoin foi adicionado nas opções do formulário, mas requer implementação específica com `OP_RETURN`. Por enquanto, use EVM chains (Ethereum, Polygon, BSC) para testes completos.

**Bitcoin será suportado em versão futura!**

---

**Última atualização:** 2025-12-08

