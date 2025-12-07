# 🔧 Correção: Colunas Inexistentes no Banco de Dados

## ❌ Erros Identificados

### 1. Tabela `payments`
```
column "wallet_address" does not exist
```

### 2. Tabela `stakes`
```
column "early_withdrawal_penalty" does not exist
```

## ✅ Correções Aplicadas

### 1. Query de `payments` - Removida coluna `wallet_address`

**Antes:**
```sql
SELECT id, email, amount, method, status, created_at, 
       processed_at, tx_hash, metadata, wallet_address
FROM payments 
ORDER BY created_at DESC
```

**Depois:**
```sql
SELECT id, email, amount, method, status, created_at, 
       processed_at, tx_hash, metadata
FROM payments 
ORDER BY created_at DESC
```

### 2. Query de `stakes` - Removidas colunas inexistentes

**Antes:**
```sql
SELECT id, user_id, asset, amount, duration, apy, start_date, end_date, 
       estimated_reward, accrued_reward, status, auto_compound, last_reward_claim, 
       days_remaining, early_withdrawal_penalty, actual_return, penalty_applied, 
       withdrawn_at, metadata
FROM stakes 
ORDER BY created_at DESC
```

**Depois:**
```sql
SELECT id, user_id, asset, amount, duration, apy, start_date, end_date, 
       estimated_reward, accrued_reward, status, auto_compound, last_reward_claim, 
       actual_return, penalty_applied, withdrawn_at, metadata
FROM stakes 
ORDER BY created_at DESC
```

### 3. Formatação de `stakes` - Removido `early_withdrawal_penalty`

**Antes:**
```python
for key in ['amount', 'apy', 'estimated_reward', 'accrued_reward', 'early_withdrawal_penalty', 'actual_return', 'penalty_applied']:
```

**Depois:**
```python
for key in ['amount', 'apy', 'estimated_reward', 'accrued_reward', 'actual_return', 'penalty_applied']:
```

## 📁 Arquivo para Atualizar no GitHub

### `backend/admin_routes.py`

**Mudanças:**
- Linha 119-123: Remover `wallet_address` da query de `payments`
- Linha 177-182: Remover `days_remaining` e `early_withdrawal_penalty` da query de `stakes`
- Linha 200: Remover `early_withdrawal_penalty` da lista de chaves numéricas

**URL:** https://github.com/brunosmaach-spec/allianza-wallet-backend/blob/main/backend/admin_routes.py

---

## 🔍 Por que isso aconteceu?

As queries estavam tentando acessar colunas que:
1. **Não foram criadas** no schema inicial do banco
2. **Foram removidas** em alguma migração
3. **Têm nomes diferentes** no banco de produção

## ✅ Após Atualizar

1. **Fazer deploy no Render**
2. **Verificar logs** - não deve aparecer erros de colunas inexistentes
3. **Rotas `/admin/payments` e `/admin/stakes` devem funcionar**

---

**Última atualização:** 2025-01-XX

