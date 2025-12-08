# 📁 Arquivos para Atualizar no GitHub

## ✅ Arquivos Modificados no Backend

### 1. `backend/admin_routes.py`
**Mudanças:**
- Linha 28: Já estava usando `VITE_SITE_ADMIN_TOKEN` ✅
- Adicionado endpoint de debug: `/debug-token-info` (linha 593)

**O que fazer:**
- Atualizar no GitHub: https://github.com/brunosmaach-spec/allianza-wallet-backend/blob/main/backend/admin_routes.py
- Ou fazer commit e push

---

### 2. `backend/backend_wallet_integration.py`
**Mudanças:**
- Linha 272: Prefixo do blueprint alterado de `/admin` para `/api/site`
- Linha 207: Adicionado OPTIONS para `/api/site/admin/debug-token-info`

**O que fazer:**
- Atualizar no GitHub: https://github.com/brunosmaach-spec/allianza-wallet-backend/blob/main/backend/backend_wallet_integration.py
- Ou fazer commit e push

---

## 📋 Resumo das Mudanças

### `admin_routes.py`:
```python
# Linha 593 - Novo endpoint de debug (público)
@admin_bp.route('/debug-token-info', methods=['GET'])
def debug_token_info():
    # Mostra qual token o backend está usando
```

### `backend_wallet_integration.py`:
```python
# Linha 272 - Prefixo corrigido
app.register_blueprint(admin_bp, url_prefix="/api/site")  # Era "/admin"

# Linha 207 - Adicionado OPTIONS para debug
@app.route('/api/site/admin/debug-token-info', methods=['OPTIONS', 'GET'])
```

---

## 🚀 Como Atualizar

### Opção 1: Commit e Push (Recomendado)

```powershell
cd "C:\Users\notebook\Downloads\allianza-wallet1\backend"
git add admin_routes.py backend_wallet_integration.py
git commit -m "fix: corrigir prefixo do blueprint admin e adicionar endpoint de debug"
git push origin main
```

### Opção 2: Atualizar Manualmente no GitHub

1. **admin_routes.py:**
   - Acesse: https://github.com/brunosmaach-spec/allianza-wallet-backend/blob/main/backend/admin_routes.py
   - Clique em "Edit" (lápis)
   - Adicione o endpoint de debug após a linha 590:
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
   - Commit: "fix: adicionar endpoint de debug para token"

2. **backend_wallet_integration.py:**
   - Acesse: https://github.com/brunosmaach-spec/allianza-wallet-backend/blob/main/backend/backend_wallet_integration.py
   - Clique em "Edit" (lápis)
   - Linha 272: Mude de:
     ```python
     app.register_blueprint(admin_bp, url_prefix="/admin")
     ```
     Para:
     ```python
     app.register_blueprint(admin_bp, url_prefix="/api/site")
     ```
   - Linha 207: Adicione após a linha existente:
     ```python
     @app.route('/api/site/admin/debug-token-info', methods=['OPTIONS', 'GET'])
     ```
   - Commit: "fix: corrigir prefixo do blueprint admin"

---

## ⚠️ IMPORTANTE

Após atualizar no GitHub:
1. O Render detectará automaticamente a mudança (se auto-deploy estiver ativo)
2. **OU** faça deploy manual no Render:
   - Vá em: `Manual Deploy` → `Deploy latest commit`
   - Aguarde 2-5 minutos

---

## ✅ Verificação

Após o deploy, teste:
- Endpoint de debug: `https://allianza-wallet-backend-1.onrender.com/api/site/admin/debug-token-info`
- Admin panel: http://localhost:5173/admin

---

**Última atualização:** 2025-01-XX



