# 🔧 Corrigir Variáveis no Render

## ❌ Problemas Identificados

1. **Variável com nome errado:**
   - ❌ Atual: `SITE_ADMIN_TOKEN`
   - ✅ Correto: `VITE_SITE_ADMIN_TOKEN`

2. **Valor incorreto:**
   - ❌ Atual: `AllianzaToken2025!`
   - ✅ Correto: `vNFkVqGDZ4QOcrMLdEKPSx3upInRaTAstogl6Ch8HmYJyB5eb1wiWXf270z9jU`

3. **URL do backend incorreta no código:**
   - ❌ Atual: `allianza-wallet-backend.onrender.com` (sem o `-1`)
   - ✅ Correto: `allianza-wallet-backend-1.onrender.com` (com o `-1`)

---

## ✅ Solução: Atualizar no Render

### Passo 1: Acessar o Render Dashboard

1. Acesse: https://dashboard.render.com
2. Vá em: `allianza-wallet-backend-1` → `Environment`

### Passo 2: Adicionar a Variável Correta

1. Clique em **"Add Environment Variable"** (ou **"+ Add"**)
2. **Key:** `VITE_SITE_ADMIN_TOKEN`
3. **Value:** `vNFkVqGDZ4QOcrMLdEKPSx3upInRaTAstogl6Ch8HmYJyB5eb1wiWXf270z9jU`
4. Clique em **"Save Changes"**

### Passo 3: Remover a Variável Antiga (Opcional)

Se quiser limpar, pode remover a variável `SITE_ADMIN_TOKEN` antiga (ela não será mais usada).

### Passo 4: Reiniciar o Serviço

1. Vá em: `Manual Deploy` → `Clear build cache & deploy`
2. Aguarde 2-5 minutos para o deploy completar

---

## ✅ Variáveis que DEVEM estar no Render

### Para o Backend (`allianza-wallet-backend-1`):

- ✅ `VITE_SITE_ADMIN_TOKEN` = `vNFkVqGDZ4QOcrMLdEKPSx3upInRaTAstogl6Ch8HmYJyB5eb1wiWXf270z9jU`
- ✅ `ADMIN_JWT_SECRET` = `CdE25$$$` (já está)
- ✅ `ADMIN_PASSWORD_1` = `H91fed103$$$` (já está)
- ✅ `ADMIN_USER_1` = `admin` (já está)
- ✅ `NEON_DATABASE_URL` = (já está)
- ✅ `PYTHON_VERSION` = `3.11.0` (já está)

### Para o Frontend (se houver deploy no Render):

- ✅ `VITE_SITE_ADMIN_TOKEN` = `vNFkVqGDZ4QOcrMLdEKPSx3upInRaTAstogl6Ch8HmYJyB5eb1wiWXf270z9jU`
- ✅ `VITE_ADMIN_PASSWORD` = `AllianzaAdmin2025!`
- ✅ `VITE_WALLET_BACKEND_URL` = `https://allianza-wallet-backend-1.onrender.com`

---

## 📋 Checklist

- [ ] Adicionei `VITE_SITE_ADMIN_TOKEN` no Render
- [ ] Valor está correto (sem espaços)
- [ ] Fiz deploy do backend após adicionar
- [ ] Código do frontend foi atualizado (URL corrigida)
- [ ] Frontend `.env` tem `VITE_SITE_ADMIN_TOKEN`
- [ ] Servidor frontend foi reiniciado

---

## 🎯 Após Corrigir

1. **Backend no Render:**
   - Adicione `VITE_SITE_ADMIN_TOKEN`
   - Faça deploy

2. **Frontend local:**
   - Verifique se `.env` tem `VITE_SITE_ADMIN_TOKEN`
   - Reinicie o servidor (`npm run dev`)

3. **Teste:**
   - Acesse: http://localhost:5173/admin
   - Use senha: `AllianzaAdmin2025!`
   - O erro `401 - Token inválido` deve desaparecer

---

## ⚠️ Importante

- O nome da variável **DEVE** ser exatamente `VITE_SITE_ADMIN_TOKEN` (case-sensitive)
- O valor **NÃO pode ter espaços** antes ou depois
- Após adicionar, **sempre faça deploy** para o backend pegar a nova variável

