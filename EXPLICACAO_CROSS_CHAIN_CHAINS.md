# 🌉 Explicação: Cross-Chain Transfer - Quais Blockchains?

**Data:** 2025-12-08

---

## 📋 Resumo

O **Cross-Chain Test** atualmente suporta transferências entre **blockchains EVM-compatíveis**:
- ✅ Ethereum (Sepolia Testnet)
- ✅ Polygon (Amoy Testnet)
- ✅ BSC (BSC Testnet)

**Bitcoin** não está incluído porque requer uma implementação diferente.

---

## 🔍 Por Que Apenas EVM Chains?

### 1. **Tecnologia Diferente**
- **EVM Chains** (Ethereum, Polygon, BSC): Usam `Web3.py` e transações com `data` field
- **Bitcoin**: Usa protocolo UTXO diferente, requer `OP_RETURN` para dados

### 2. **Implementação Atual**
O código atual usa:
```python
from web3 import Web3
# Funciona para Ethereum, Polygon, BSC
```

Para Bitcoin seria necessário:
```python
from bitcoinlib import Transaction
# Ou usar APIs REST do Bitcoin
```

---

## 🚀 Como Funciona Atualmente

### Transferências Suportadas:
1. **Polygon → Ethereum** ✅
2. **Ethereum → Polygon** ✅
3. **BSC → Ethereum** ✅
4. **Ethereum → BSC** ✅
5. **Polygon → BSC** ✅
6. **BSC → Polygon** ✅

### O Que Acontece:
1. Cria **State Commitment** na chain de origem
2. Gera **ZK Proof** da transição de estado
3. Aplica estado na chain de destino usando a prova
4. Inclui **UChainID e ZK Proof** no memo da transação

---

## 💡 Para Adicionar Bitcoin

Seria necessário:

1. **Biblioteca Bitcoin:**
   - `python-bitcoinlib` ou
   - APIs REST (BlockCypher, Blockstream)

2. **Modificar `send_real_transaction()`:**
   - Detectar se é Bitcoin
   - Usar `OP_RETURN` para incluir memo
   - Assinar transação Bitcoin

3. **Exemplo:**
```python
if target_chain == "bitcoin":
    # Criar transação Bitcoin com OP_RETURN
    tx = create_bitcoin_tx_with_op_return(memo_data)
    # Assinar e enviar
else:
    # Usar Web3.py (atual)
    transaction = w3.eth.account.sign_transaction(...)
```

---

## ✅ Conclusão

**Atualmente:** Apenas EVM chains (Ethereum, Polygon, BSC)  
**Futuro:** Bitcoin pode ser adicionado com implementação específica

O sistema **ALZ-NIEV** é projetado para funcionar com **qualquer blockchain**, mas a implementação atual foca em EVM para simplificar.

---

**Última atualização:** 2025-12-08

