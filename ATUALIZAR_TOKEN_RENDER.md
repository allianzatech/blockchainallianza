# 🔐 Atualizar Token no Render

## 📋 Informações do Serviço

**URL do Serviço:** https://allianza-wallet-backend-1.onrender.com  
**Service ID:** srv-d3qp4mu3jp1c738pams0  
**Dashboard:** https://dashboard.render.com

---

## ✅ Token para Adicionar

**Variável:** `VITE_SITE_ADMIN_TOKEN`  
**Valor:** `vNFkVqGDZ4QOcrMLdEKPSx3upInRaTAstogl6Ch8HmYJyB5eb1wiWXf270z9jU`

---

## 🚀 Passo a Passo para Atualizar

### 1. Acessar o Dashboard
1. Vá para: https://dashboard.render.com
2. Faça login na sua conta

### 2. Encontrar o Serviço
1. Procure pelo serviço: `allianza-wallet-backend-1`
2. Ou use o Service ID: `srv-d3qp4mu3jp1c738pams0`
3. Clique no serviço para abrir

### 3. Adicionar/Atualizar Variável de Ambiente
1. No menu lateral, clique em **"Environment"** (ou vá em **Settings** → **Environment**)
2. Procure pela variável `VITE_SITE_ADMIN_TOKEN`
3. Se já existir:
   - Clique no botão de editar (✏️) ao lado da variável
   - Substitua o valor pelo novo token
   - Clique em **"Save Changes"**
4. Se não existir:
   - Clique em **"Add Environment Variable"**
   - **Key:** `VITE_SITE_ADMIN_TOKEN`
   - **Value:** `vNFkVqGDZ4QOcrMLdEKPSx3upInRaTAstogl6Ch8HmYJyB5eb1wiWXf270z9jU`
   - Clique em **"Save Changes"**

### 4. Reiniciar o Serviço
1. Vá para a aba **"Manual Deploy"** (ou **"Deploys"**)
2. Clique em **"Deploy latest commit"** ou **"Clear build cache & deploy"**
3. Aguarde o deploy completar (2-5 minutos)

---

## ✅ Verificação

Após o deploy, teste se está funcionando:

1. Acesse: https://allianza-wallet-backend-1.onrender.com/health
2. Deve retornar: `{"status": "healthy", ...}`

3. Teste o painel admin:
   - Acesse: http://localhost:5173/admin
   - Use a senha: `AllianzaAdmin2025!`
   - O erro `401 - Token inválido` deve desaparecer

---

## 📝 Variáveis de Ambiente Necessárias

Certifique-se de que estas variáveis estão configuradas no Render:

### Obrigatórias:
- ✅ `VITE_SITE_ADMIN_TOKEN` = `vNFkVqGDZ4QOcrMLdEKPSx3upInRaTAstogl6Ch8HmYJyB5eb1wiWXf270z9jU`
- ✅ `DATABASE_URL` = (sua URL do banco de dados)

### Opcionais (mas recomendadas):
- `FLASK_ENV` = `production`
- `FLASK_DEBUG` = `False`
- `PYTHONUNBUFFERED` = `1`

---

## 🔍 Troubleshooting

### Erro: "Token inválido" ainda aparece
- Verifique se o token foi salvo corretamente (sem espaços extras)
- Certifique-se de que o serviço foi reiniciado após adicionar a variável
- Verifique os logs do Render para ver se há erros

### Serviço não inicia
- Verifique os logs em **"Logs"** no dashboard
- Certifique-se de que `DATABASE_URL` está configurada
- Verifique se todas as dependências estão instaladas

### Como verificar se a variável foi salva
1. No dashboard, vá em **Environment**
2. Procure por `VITE_SITE_ADMIN_TOKEN`
3. O valor deve aparecer (parcialmente mascarado por segurança)

---

**Última atualização:** 2025-01-XX  
**Status:** ⏳ Aguardando atualização no Render

