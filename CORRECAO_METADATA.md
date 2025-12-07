# 🔧 Correção: Coluna `metadata` Faltante na Tabela `stakes`

## ❌ Erro Identificado

```
column "metadata" does not exist
LINE 5: withdrawn_at, metadata
```

## 🔍 Causa

O código em `admin_routes.py` busca a coluna `metadata` na tabela `stakes`, mas essa coluna não existe no banco PostgreSQL (Neon).

## ✅ Solução Aplicada

### Script Criado: `add_metadata_column.py`

Executa automaticamente:
```sql
ALTER TABLE stakes ADD COLUMN IF NOT EXISTS metadata JSONB;
```

## 🚀 Como Executar

### Opção 1: Script Python (Recomendado)

```powershell
cd "C:\Users\notebook\Downloads\allianza-wallet1\backend"
python add_metadata_column.py
```

### Opção 2: SQL Manual no Neon

Execute no console do Neon:
```sql
ALTER TABLE stakes ADD COLUMN IF NOT EXISTS metadata JSONB;
```

## 📁 Arquivos Atualizados

1. **`add_metadata_column.py`** - Script específico para adicionar metadata
2. **`migrate_add_missing_columns.py`** - Atualizado para incluir metadata

## ✅ Após Executar

1. **Coluna `metadata` será adicionada**
2. **Erro 500 deve desaparecer**
3. **Rota `/admin/stakes` deve funcionar**

---

**Última atualização:** 2025-01-XX

