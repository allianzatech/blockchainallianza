# 🔧 Correção: backend_reports_routes.py - Database

## ❌ Problema Identificado

O arquivo `backend_reports_routes.py` estava usando:
- `from database import get_db_connection` (SQLite)
- Queries com `?` (sintaxe SQLite)

Mas o backend usa **PostgreSQL (Neon)**, não SQLite!

## ✅ Correções Aplicadas

### 1. Import Corrigido

**Antes:**
```python
from database import get_db_connection
```

**Depois:**
```python
# ✅ CORRIGIDO: Usar database_neon (PostgreSQL) em vez de database (SQLite)
from database_neon import get_db_connection
```

### 2. Query SQL Corrigida

**Antes:**
```python
cursor.execute("SELECT email, nickname, wallet_address FROM users WHERE id = ?", (user_id,))
```

**Depois:**
```python
# ✅ CORRIGIDO: Usar %s (PostgreSQL) em vez de ? (SQLite)
cursor.execute("SELECT email, nickname, wallet_address FROM users WHERE id = %s", (user_id,))
```

## 📁 Arquivo para Atualizar no GitHub

### `backend/backend_reports_routes.py`

**Mudanças:**
- Linha 15: Mudar import de `database` para `database_neon`
- Linha 116: Mudar `?` para `%s` na query SQL

**URL:** https://github.com/brunosmaach-spec/allianza-wallet-backend/blob/main/backend/backend_reports_routes.py

---

## 📋 Sobre o `.env`

### ✅ **NÃO precisa adicionar `DATABASE_URL` no `.env`!**

**Por quê?**
- Já temos `NEON_DATABASE_URL` configurado
- A função `get_db_connection()` em `admin_routes.py` agora tem **fallback**:
  ```python
  DATABASE_URL = os.getenv('DATABASE_URL') or os.getenv('NEON_DATABASE_URL')
  ```
- Funciona automaticamente com `NEON_DATABASE_URL`

### ⚙️ Opção Alternativa (Opcional)

Se quiser, pode adicionar `DATABASE_URL` também (mas não é necessário):

```env
DATABASE_URL=postgresql://neondb_owner:npg_eK0UFHTc4wAJ@ep-lively-cell-af0g1vc1-pooler.c-2.us-west-2.aws.neon.tech/neondb?sslmode=require&channel_binding=require
NEON_DATABASE_URL=postgresql://neondb_owner:npg_eK0UFHTc4wAJ@ep-lively-cell-af0g1vc1-pooler.c-2.us-west-2.aws.neon.tech/neondb?sslmode=require&channel_binding=require
```

**Mas não é necessário!** O fallback já resolve.

---

## ✅ Após Atualizar

1. **Fazer deploy no Render**
2. **Verificar logs** - não deve aparecer erros de SQLite
3. **Rotas de relatórios devem funcionar**

---

**Última atualização:** 2025-01-XX



