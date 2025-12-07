# 📋 Resumo: Arquivos para Atualizar no GitHub

## ✅ Total: 3 Arquivos

### 1. `backend/requirements.txt`
**Mudança:**
- Adicionar: `psycopg2-binary==2.9.9`

**URL:** https://github.com/brunosmaach-spec/allianza-wallet-backend/blob/main/backend/requirements.txt

---

### 2. `backend/admin_routes.py`
**Mudanças:**
- Linhas 10-12: Adicionar `load_dotenv()`
- Linha 33: Substituir carregamento do token com debug

**URL:** https://github.com/brunosmaach-spec/allianza-wallet-backend/blob/main/backend/admin_routes.py

---

### 3. `backend/backend_wallet_integration.py`
**Mudanças:**
- Linha 272: Mudar prefixo de `/admin` para `/api/site`
- Linha 208: Adicionar OPTIONS para debug-token-info

**URL:** https://github.com/brunosmaach-spec/allianza-wallet-backend/blob/main/backend/backend_wallet_integration.py

---

## 🚀 Como Atualizar

### Opção 1: Commit e Push

```powershell
cd "C:\Users\notebook\Downloads\allianza-wallet1\backend"
git add requirements.txt admin_routes.py backend_wallet_integration.py
git commit -m "fix: adicionar psycopg2-binary, corrigir carregamento de token e prefixo do blueprint"
git push origin main
```

### Opção 2: Atualizar Manualmente no GitHub

Veja `CORRECOES_DEPLOY_RENDER.md` para instruções detalhadas de cada arquivo.

---

## ⚠️ IMPORTANTE

Após atualizar no GitHub:
1. O Render pode detectar automaticamente (se auto-deploy estiver ativo)
2. **OU** faça deploy manual:
   - Render Dashboard → `allianza-wallet-backend-1` → `Manual Deploy`
   - Clique em: **"Clear build cache & deploy"**
   - Aguarde 2-5 minutos

---

## ✅ Verificação

Após o deploy, nos logs você deve ver:
```
✅ VITE_SITE_ADMIN_TOKEN carregado: vNFkVqGDZ4... (comprimento: 64)
```

**NÃO deve aparecer:**
```
⚠️  VITE_SITE_ADMIN_TOKEN não encontrado
```

---

**Última atualização:** 2025-01-XX

