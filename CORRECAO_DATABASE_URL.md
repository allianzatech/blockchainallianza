# 🔧 Correção: DATABASE_URL vs NEON_DATABASE_URL

## ❌ Problema Identificado

O backend está procurando por `DATABASE_URL`, mas no Render só existe `NEON_DATABASE_URL`.

**Erro:**
```
ValueError: DATABASE_URL não configurada
```

## ✅ Solução Aplicada

Adicionado **fallback** em `admin_routes.py` para usar `NEON_DATABASE_URL` se `DATABASE_URL` não existir.

### Mudança em `admin_routes.py`

**Antes:**
```python
def get_db_connection():
    """Conexão única com o banco para evitar conflitos"""
    DATABASE_URL = os.getenv('DATABASE_URL')
    if not DATABASE_URL:
        raise ValueError("DATABASE_URL não configurada")
    
    conn = psycopg2.connect(DATABASE_URL)
    conn.autocommit = False
    return conn
```

**Depois:**
```python
def get_db_connection():
    """Conexão única com o banco para evitar conflitos"""
    # ✅ FALLBACK: Usar NEON_DATABASE_URL se DATABASE_URL não existir
    DATABASE_URL = os.getenv('DATABASE_URL') or os.getenv('NEON_DATABASE_URL')
    if not DATABASE_URL:
        raise ValueError("DATABASE_URL ou NEON_DATABASE_URL não configurada")
    
    print(f"🔗 Conectando ao banco usando: {'DATABASE_URL' if os.getenv('DATABASE_URL') else 'NEON_DATABASE_URL (fallback)'}")
    conn = psycopg2.connect(DATABASE_URL)
    conn.autocommit = False
    return conn
```

## 📁 Arquivo para Atualizar no GitHub

### `backend/admin_routes.py`

**Linhas 20-29:** Adicionar fallback para `NEON_DATABASE_URL`

**URL:** https://github.com/brunosmaach-spec/allianza-wallet-backend/blob/main/backend/admin_routes.py

---

## 🔍 Verificar Outros Arquivos

Outros arquivos que podem precisar da mesma correção:

1. **`backend_staking_routes.py`** - Verificar se usa `get_db_connection()` ou `DATABASE_URL` diretamente
2. **`balance_ledger_routes.py`** - Verificar se usa `get_db_connection()` ou `DATABASE_URL` diretamente
3. **`backend_reports_routes.py`** - Verificar se usa `get_db_connection()` ou `DATABASE_URL` diretamente

---

## ⚙️ Opção Alternativa: Adicionar DATABASE_URL no Render

Se preferir, você pode adicionar `DATABASE_URL` diretamente no Render:

1. Render Dashboard → `allianza-wallet-backend-1` → Environment
2. Adicionar nova variável:
   - **Key:** `DATABASE_URL`
   - **Value:** `postgresql://neondb_owner:npg_eK0UFHTc4wAJ@ep-lively-cell-af0g1vc1-pooler.c-2.us-west-2.aws.neon.tech/neondb?sslmode=require&channel_binding=require`
3. Salvar e fazer **"Manual Deploy"**

Mas a solução com fallback é **mais robusta** e funciona em ambos os casos.

---

## ✅ Após Atualizar

1. **Fazer deploy no Render**
2. **Verificar logs** - deve aparecer:
   ```
   🔗 Conectando ao banco usando: NEON_DATABASE_URL (fallback)
   ```
3. **Erro 500 deve desaparecer**

---

**Última atualização:** 2025-01-XX

