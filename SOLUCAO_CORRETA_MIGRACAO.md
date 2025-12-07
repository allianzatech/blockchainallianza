# ✅ Solução Correta: Adicionar Colunas no Banco (NÃO Remover do Código)

## 🚨 Problema Identificado

O banco PostgreSQL (Neon) está **incompleto** comparado ao SQLite. As colunas existem no código, mas não no banco.

## ❌ Solução ERRADA (que foi revertida)

- ❌ Remover colunas do código
- ❌ Isso quebra funcionalidades importantes

## ✅ Solução CORRETA

- ✅ **Manter as colunas no código** (já revertido)
- ✅ **Adicionar as colunas no banco PostgreSQL**

---

## 📋 Colunas Faltantes Identificadas

### Tabela `stakes`:
- ✅ `days_remaining` INTEGER
- ✅ `early_withdrawal_penalty` NUMERIC(20,8)
- ✅ `duration` INTEGER (verificar se existe)
- ✅ `estimated_reward` NUMERIC(20,8) (verificar se existe)
- ✅ `accrued_reward` NUMERIC(20,8) (verificar se existe)
- ✅ `auto_compound` BOOLEAN (verificar se existe)

### Tabela `payments`:
- ✅ `wallet_address` VARCHAR(255)

---

## 🔧 Como Executar a Migração

### Opção 1: Executar o Script Python (Recomendado)

```powershell
cd "C:\Users\notebook\Downloads\allianza-wallet1\backend"
python migrate_add_missing_columns.py
```

O script:
- ✅ Verifica se cada coluna existe
- ✅ Adiciona apenas as que faltam
- ✅ É seguro executar múltiplas vezes (idempotente)

### Opção 2: Executar SQL Manualmente no Neon

Acesse o console do Neon e execute:

```sql
-- Tabela stakes
ALTER TABLE stakes ADD COLUMN IF NOT EXISTS days_remaining INTEGER;
ALTER TABLE stakes ADD COLUMN IF NOT EXISTS early_withdrawal_penalty NUMERIC(20,8);
ALTER TABLE stakes ADD COLUMN IF NOT EXISTS duration INTEGER;
ALTER TABLE stakes ADD COLUMN IF NOT EXISTS estimated_reward NUMERIC(20,8);
ALTER TABLE stakes ADD COLUMN IF NOT EXISTS accrued_reward NUMERIC(20,8) DEFAULT 0.0;
ALTER TABLE stakes ADD COLUMN IF NOT EXISTS auto_compound BOOLEAN DEFAULT FALSE;

-- Tabela payments
ALTER TABLE payments ADD COLUMN IF NOT EXISTS wallet_address VARCHAR(255);
```

---

## ✅ Após Executar a Migração

1. **Fazer deploy no Render** (se necessário)
2. **Testar as rotas `/admin/payments` e `/admin/stakes`**
3. **Verificar que não há mais erros 500**

---

## 📁 Arquivos Criados

1. **`migrate_add_missing_columns.py`** - Script de migração automática
2. **`check_sqlite_schema.py`** - Script para verificar schema do SQLite

---

## 🎯 Resumo

- ✅ **Código revertido** - colunas mantidas
- ✅ **Script de migração criado** - adiciona colunas no banco
- ✅ **Solução profissional** - não quebra funcionalidades

---

**Última atualização:** 2025-01-XX

