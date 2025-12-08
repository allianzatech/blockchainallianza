# 🔧 Migração: Adicionar Coluna `expires_at`

## ❌ Problema

O backend está falhando com erro:
```
column "expires_at" does not exist
LINE 3: ... processed_at, tx_hash, metadata, wallet_address, expires_at
```

A coluna `expires_at` não existe na tabela `payments` do banco de dados PostgreSQL.

---

## ✅ Solução Implementada

### 1. **Verificação Automática na Inicialização**

O `admin_routes.py` agora verifica e cria a coluna automaticamente:

```python
# ✅ GARANTIR QUE A COLUNA EXISTS NA INICIALIZAÇÃO
try:
    add_expires_at_column()
    print("✅ Coluna 'expires_at' verificada/criada com sucesso")
except Exception as e:
    print(f"⚠️  Aviso ao verificar coluna expires_at: {e}")
```

### 2. **SELECT Dinâmico**

O código agora verifica se a coluna existe antes de usá-la:

```python
# Verificar se coluna existe
cursor.execute("""
    SELECT column_name 
    FROM information_schema.columns 
    WHERE table_name='payments' AND column_name='expires_at'
""")
has_expires_at = cursor.fetchone() is not None

# SELECT baseado na existência
if has_expires_at:
    # SELECT com expires_at
else:
    # SELECT sem expires_at ou tentar criar
```

### 3. **SQL de Migração Manual (Opcional)**

Se preferir executar manualmente no banco:

```sql
-- Adicionar coluna expires_at
ALTER TABLE payments 
ADD COLUMN IF NOT EXISTS expires_at TIMESTAMPTZ;

-- Atualizar pagamentos pendentes existentes
UPDATE payments 
SET expires_at = created_at + INTERVAL '10 days'
WHERE status = 'pending' AND expires_at IS NULL;
```

---

## 📋 Arquivos Atualizados

1. **`backend/admin_routes.py`**
   - Verificação automática na inicialização
   - SELECT dinâmico baseado na existência da coluna
   - Fallback se coluna não existir

2. **`backend/payment_expiration.py`** (já existia)
   - Função `add_expires_at_column()` para criar a coluna

---

## 🚀 Como Funciona

1. **Na inicialização do backend:**
   - Tenta importar `payment_expiration`
   - Chama `add_expires_at_column()` automaticamente
   - Se falhar, continua sem quebrar

2. **Nas queries:**
   - Verifica se coluna existe antes de usar
   - Se não existir, tenta criar
   - Se não conseguir criar, usa SELECT sem `expires_at`

---

## ✅ Resultado Esperado

- ✅ Backend não quebra se coluna não existir
- ✅ Coluna é criada automaticamente na primeira execução
- ✅ Queries funcionam com ou sem a coluna
- ✅ Sistema de expiração funciona corretamente

---

**Última atualização:** 2025-01-XX

