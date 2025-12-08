# 📝 Como Adicionar Source Chain tx_hash

**Data:** 2025-12-08

---

## 🎯 Objetivo

Capturar `tx_hash` da **source chain** (Polygon) além do `tx_hash` da **target chain** (Ethereum) para provar o ciclo completo de lock/commitment → apply.

---

## 📋 Implementação Necessária

### 1. Modificar `bridge_free_transfer`

No método `bridge_free_transfer`, quando `send_real=True`:

```python
# ANTES de enviar transação na target chain:
# 1. Enviar transação na source chain (lock/commitment)
if send_real:
    # Criar transação na source chain com commitment
    source_tx_result = self.send_real_transaction(
        source_chain=source_chain,
        target_chain=source_chain,  # Mesma chain (lock local)
        amount=amount,
        recipient=recipient,  # Ou endereço de lock
        private_key=private_key,
        include_memo=True,
        zk_proof_id=None  # Ainda não tem proof
    )
    
    if source_tx_result.get("success"):
        source_tx_hash = source_tx_result.get("tx_hash")
        source_explorer_url = source_tx_result.get("explorer_url")
    else:
        source_tx_hash = None
        source_explorer_url = None
else:
    source_tx_hash = None
    source_explorer_url = None

# 2. Depois enviar transação na target chain (apply)
target_tx_result = self.send_real_transaction(
    source_chain=source_chain,
    target_chain=target_chain,
    amount=amount,
    recipient=recipient,
    private_key=private_key,
    include_memo=True,
    zk_proof_id=proof_id
)
```

### 2. Retornar Ambos os tx_hash

```python
result = {
    "success": True,
    "source_tx_hash": source_tx_hash,  # Polygon
    "target_tx_hash": target_tx_result.get("tx_hash"),  # Ethereum
    "source_explorer_url": source_explorer_url,
    "target_explorer_url": target_tx_result.get("explorer_url"),
    # ... resto dos dados
}
```

---

## ⚠️ Considerações

1. **Gas Costs:** Enviar 2 transações (source + target) dobra os custos
2. **Timing:** Source tx deve ser confirmada antes de enviar target tx
3. **Error Handling:** Se source tx falhar, não enviar target tx
4. **Atomicity:** Garantir que ambas as txs sejam bem-sucedidas ou nenhuma

---

## 🚀 Implementação Futura

Isso será implementado na próxima versão para:
- ✅ Provar lock completo na source chain
- ✅ Mostrar ambos os tx_hash lado a lado
- ✅ Links para ambos os explorers
- ✅ Verificação completa do ciclo

---

**Status:** Planejado para próxima versão

