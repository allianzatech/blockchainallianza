# 📋 Lista de Arquivos para Atualizar no GitHub

## ✅ Arquivos Modificados

### 1. `backend/admin_routes.py` ✅
**Status:** Modificado (aparece no `git status`)

**Mudanças:**
- Adicionado endpoint de debug público: `/debug-token-info` (linha 593)

**URL no GitHub:**
- https://github.com/brunosmaach-spec/allianza-wallet-backend/blob/main/backend/admin_routes.py

---

### 2. `backend/backend_wallet_integration.py` ⚠️
**Status:** Modificado localmente (pode não aparecer no git se já estava modificado)

**Mudanças:**
- Linha 272: Prefixo do blueprint alterado de `/admin` para `/api/site`
- Linha 207: Adicionado OPTIONS para `/api/site/admin/debug-token-info`

**URL no GitHub:**
- https://github.com/brunosmaach-spec/allianza-wallet-backend/blob/main/backend/backend_wallet_integration.py

---

## 🚀 Como Atualizar

### Opção 1: Commit e Push (Mais Rápido)

```powershell
cd "C:\Users\notebook\Downloads\allianza-wallet1\backend"
git add admin_routes.py backend_wallet_integration.py
git commit -m "fix: corrigir prefixo do blueprint admin e adicionar endpoint de debug"
git push origin main
```

### Opção 2: Atualizar Manualmente no GitHub

#### Arquivo 1: `admin_routes.py`

1. Acesse: https://github.com/brunosmaach-spec/allianza-wallet-backend/blob/main/backend/admin_routes.py
2. Clique em "Edit" (ícone de lápis)
3. Após a linha 590, adicione:

```python
# ✅ DEBUG CORRIGIDO - Endpoint público para verificar token configurado
@admin_bp.route('/debug-token-info', methods=['GET'])
def debug_token_info():
    """Endpoint público para debug - mostra qual token o backend está esperando"""
    env_token = os.getenv('VITE_SITE_ADMIN_TOKEN', 'NOT_FOUND')
    return jsonify({
        "token_from_env": env_token[:20] + "..." if len(env_token) > 20 else env_token,
        "token_length": len(env_token) if env_token != 'NOT_FOUND' else 0,
        "token_first_10": env_token[:10] if env_token != 'NOT_FOUND' else "NOT_FOUND",
        "token_last_10": env_token[-10:] if env_token != 'NOT_FOUND' and len(env_token) > 10 else "NOT_FOUND",
        "env_var_exists": env_token != 'NOT_FOUND',
        "site_admin_token_used": SITE_ADMIN_TOKEN[:20] + "..." if len(SITE_ADMIN_TOKEN) > 20 else SITE_ADMIN_TOKEN,
        "site_admin_token_length": len(SITE_ADMIN_TOKEN),
        "message": "Debug de token - verifique se VITE_SITE_ADMIN_TOKEN está configurado"
    }), 200
```

4. Commit message: `fix: adicionar endpoint de debug para token`
5. Clique em "Commit changes"

---

#### Arquivo 2: `backend_wallet_integration.py`

1. Acesse: https://github.com/brunosmaach-spec/allianza-wallet-backend/blob/main/backend/backend_wallet_integration.py
2. Clique em "Edit" (ícone de lápis)

**Mudança 1 - Linha 272:**
- **De:**
  ```python
  app.register_blueprint(admin_bp, url_prefix="/admin")
  ```
- **Para:**
  ```python
  app.register_blueprint(admin_bp, url_prefix="/api/site")
  ```

**Mudança 2 - Linha 207:**
- Adicione após a linha existente:
  ```python
  @app.route('/api/site/admin/debug-token-info', methods=['OPTIONS', 'GET'])
  ```

3. Commit message: `fix: corrigir prefixo do blueprint admin`
4. Clique em "Commit changes"

---

## ⚠️ IMPORTANTE

Após atualizar no GitHub:
1. O Render pode detectar automaticamente (se auto-deploy estiver ativo)
2. **OU** faça deploy manual:
   - Render Dashboard → `allianza-wallet-backend-1` → `Manual Deploy`
   - Clique em: **"Deploy latest commit"**
   - Aguarde 2-5 minutos

---

## ✅ Verificação

Após o deploy, teste:
- Endpoint de debug: `https://allianza-wallet-backend-1.onrender.com/api/site/admin/debug-token-info`
- Admin panel: http://localhost:5173/admin

---

**Resumo:** 2 arquivos precisam ser atualizados:
1. `backend/admin_routes.py`
2. `backend/backend_wallet_integration.py`



