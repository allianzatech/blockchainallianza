# 🔍 Debug: Verificar Token no Backend

## ❌ Problema

A variável `VITE_SITE_ADMIN_TOKEN` está configurada no Render, mas o erro `401 - Token inválido` persiste.

## 🔍 Possíveis Causas

1. **Backend não foi reiniciado** após adicionar a variável
2. **Espaços extras** no valor da variável no Render
3. **Cache do Python** pode estar usando valor antigo
4. **Encoding** do token pode estar diferente

---

## ✅ Solução: Verificar Token no Backend

### Opção 1: Verificar Logs do Render

1. Acesse: https://dashboard.render.com
2. Vá em: `allianza-wallet-backend-1` → `Logs`
3. Procure por mensagens que mostram o token:
   - `SITE_ADMIN_TOKEN`
   - `Token inválido`
   - `expected:`

### Opção 2: Criar Endpoint de Debug (Temporário)

Adicione este endpoint temporário no `admin_routes.py` para verificar o token:

```python
@admin_bp.route('/api/site/admin/debug-token-info', methods=['GET'])
def debug_token_info():
    """Endpoint temporário para debug do token"""
    return jsonify({
        "token_from_env": SITE_ADMIN_TOKEN,
        "token_length": len(SITE_ADMIN_TOKEN),
        "token_first_10": SITE_ADMIN_TOKEN[:10],
        "token_last_10": SITE_ADMIN_TOKEN[-10:],
        "env_var_exists": os.getenv('VITE_SITE_ADMIN_TOKEN') is not None,
        "env_var_value": os.getenv('VITE_SITE_ADMIN_TOKEN', 'NOT_FOUND')[:20] + "..."
    }), 200
```

Depois acesse: `https://allianza-wallet-backend-1.onrender.com/api/site/admin/debug-token-info`

---

## 🔧 Ações Imediatas

### 1. Verificar se há Espaços no Render

No Render Dashboard:
1. Vá em: `allianza-wallet-backend-1` → `Environment`
2. Clique em editar `VITE_SITE_ADMIN_TOKEN`
3. **Copie o valor completo** e verifique se há espaços antes/depois
4. Se houver, remova e salve novamente

### 2. Forçar Reinício do Backend

1. Vá em: `Manual Deploy`
2. Clique em: **"Clear build cache & deploy"**
3. Aguarde 2-5 minutos
4. Verifique os logs para garantir que iniciou corretamente

### 3. Verificar se o Código está Atualizado

O arquivo `backend/admin_routes.py` deve ter na linha 28:
```python
SITE_ADMIN_TOKEN = os.getenv('VITE_SITE_ADMIN_TOKEN', 'allianza_super_admin_2024_CdE25$$$')
```

**Verifique no GitHub:**
- https://github.com/brunosmaach-spec/allianza-wallet-backend/blob/main/backend/admin_routes.py

Se não estiver atualizado, atualize manualmente no GitHub e faça deploy.

---

## 🧪 Teste Manual do Token

Você pode testar diretamente com curl:

```bash
curl -X GET "https://allianza-wallet-backend-1.onrender.com/api/site/admin/payments" \
  -H "Authorization: Bearer vNFkVqGDZ4QOcrMLdEKPSx3upInRaTAstogl6Ch8HmYJyB5eb1wiWXf270z9jU" \
  -H "Content-Type: application/json"
```

Se retornar `401`, o problema está no backend.
Se retornar dados, o problema está no frontend.

---

## 📋 Checklist de Verificação

- [ ] Variável `VITE_SITE_ADMIN_TOKEN` existe no Render
- [ ] Valor está correto (sem espaços)
- [ ] Deploy foi feito após adicionar/atualizar
- [ ] Código `admin_routes.py` está atualizado
- [ ] Logs do backend não mostram erros
- [ ] Teste manual com curl funcionou

---

## ⚠️ Importante

- O backend **DEVE** ser reiniciado após adicionar variáveis de ambiente
- Verifique os **logs do Render** para ver se há erros
- O token **NÃO pode ter espaços** antes ou depois

---

**Última atualização:** 2025-01-XX

