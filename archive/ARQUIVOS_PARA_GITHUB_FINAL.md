# 📋 Arquivos para Atualizar no GitHub (Deploy Automático no Render)

## ✅ Status Atual

- ✅ **Coluna `metadata` adicionada no banco** (já feito via script)
- ✅ **Código corrigido localmente** (precisa atualizar no GitHub)

## 📁 Arquivos que PRECISAM ser Atualizados no GitHub

### 1. `backend/database_neon.py` ⚠️ **CRÍTICO**
**Mudança:** Aceitar `DATABASE_URL` ou `NEON_DATABASE_URL`
- Linha 11: `self.database_url = os.getenv('NEON_DATABASE_URL') or os.getenv('DATABASE_URL')`
- Linha 20: Mensagem de erro atualizada
- Linha 25: Mensagem de erro atualizada

**URL:** https://github.com/brunosmaach-spec/allianza-wallet-backend/blob/main/backend/database_neon.py

---

### 2. `backend/admin_routes.py` ✅ **Já tem fallback**
**Status:** Já está correto (tem fallback)
- Linha 24: `DATABASE_URL = os.getenv('DATABASE_URL') or os.getenv('NEON_DATABASE_URL')`

**URL:** https://github.com/brunosmaach-spec/allianza-wallet-backend/blob/main/backend/admin_routes.py

---

### 3. `backend/backend_wallet_integration.py` ⚠️ **IMPORTANTE**
**Mudança:** Importação opcional de `balance_ledger_routes`
- Linhas 279-285: Tornar importação opcional com try/except

**URL:** https://github.com/brunosmaach-spec/allianza-wallet-backend/blob/main/backend/backend_wallet_integration.py

---

### 4. `backend/backend_reports_routes.py` ⚠️ **IMPORTANTE**
**Mudança:** Usar `database_neon` em vez de `database`
- Linha 15: `from database_neon import get_db_connection`
- Linhas 116, 124, 138, 151: Queries SQL corrigidas (`?` → `%s`)

**URL:** https://github.com/brunosmaach-spec/allianza-wallet-backend/blob/main/backend/backend_reports_routes.py

---

### 5. `backend/requirements.txt` ⚠️ **CRÍTICO**
**Mudança:** Adicionar `psycopg2-binary`
- Linha 8: `psycopg2-binary==2.9.9`

**URL:** https://github.com/brunosmaach-spec/allianza-wallet-backend/blob/main/backend/requirements.txt

---

## 🚀 Ordem de Prioridade

### 🔴 **CRÍTICO (Fazer Primeiro):**
1. `backend/database_neon.py` - Fallback DATABASE_URL
2. `backend/requirements.txt` - psycopg2-binary

### 🟡 **IMPORTANTE:**
3. `backend/backend_wallet_integration.py` - Importação opcional
4. `backend/backend_reports_routes.py` - Database correto

### 🟢 **JÁ ESTÁ OK:**
5. `backend/admin_routes.py` - Já tem fallback

---

## 📝 Como Atualizar

### Opção 1: Commit e Push (Recomendado)

```powershell
cd "C:\Users\notebook\Downloads\allianza-wallet1\backend"
git add database_neon.py requirements.txt backend_wallet_integration.py backend_reports_routes.py
git commit -m "fix: adicionar fallback DATABASE_URL, psycopg2-binary, corrigir imports"
git push origin main
```

### Opção 2: Atualizar Manualmente no GitHub

1. Acesse cada URL acima
2. Clique no ícone de lápis (Edit)
3. Faça as mudanças
4. Commit changes

---

## ⚠️ IMPORTANTE

### ❌ NÃO precisa atualizar no Render:
- Variáveis de ambiente (já estão configuradas)
- Configurações do serviço

### ✅ O Render faz deploy automaticamente:
- Quando você faz push no GitHub
- Ou pode fazer "Manual Deploy" após o push

---

## ✅ Após Atualizar no GitHub

1. **Render detecta automaticamente** (se auto-deploy estiver ativo)
2. **OU faça Manual Deploy:**
   - Render Dashboard → `allianza-wallet-backend-1`
   - Clique em "Manual Deploy"
   - Aguarde 2-5 minutos

---

## 🎯 Resumo

- ✅ **Banco atualizado** - coluna metadata adicionada
- ⚠️ **Código precisa atualizar no GitHub** - 4 arquivos principais
- ✅ **Render faz deploy automaticamente** - após push no GitHub

---

**Última atualização:** 2025-01-XX



