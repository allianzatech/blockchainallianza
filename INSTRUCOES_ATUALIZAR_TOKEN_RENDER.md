# 🔐 Instruções para Atualizar Token no Render

## 📋 Informações do Serviço

**URL:** https://allianza-wallet-backend-1.onrender.com  
**Service ID:** srv-d3qp4mu3jp1c738pams0  
**Repositório GitHub:** https://github.com/brunosmaach-spec/allianza-wallet-backend

---

## ✅ Token que Precisa ser Adicionado

**Variável de Ambiente:** `VITE_SITE_ADMIN_TOKEN`  
**Valor:** `vNFkVqGDZ4QOcrMLdEKPSx3upInRaTAstogl6Ch8HmYJyB5eb1wiWXf270z9jU`

---

## 🚀 Passo a Passo Detalhado

### 1️⃣ Acessar o Dashboard do Render

1. Abra seu navegador
2. Vá para: **https://dashboard.render.com**
3. Faça login na sua conta

### 2️⃣ Encontrar o Serviço

1. No dashboard, procure por: **`allianza-wallet-backend-1`**
2. Ou procure pelo Service ID: **`srv-d3qp4mu3jp1c738pams0`**
3. Clique no serviço para abrir

### 3️⃣ Adicionar a Variável de Ambiente

1. No menu lateral esquerdo, clique em **"Environment"**
   - Ou vá em **"Settings"** → **"Environment"**

2. **Verificar se já existe:**
   - Procure na lista por `VITE_SITE_ADMIN_TOKEN`
   - Se encontrar:
     - Clique no ícone de **editar (✏️)** ao lado
     - Substitua o valor antigo pelo novo
     - Clique em **"Save Changes"**

3. **Se não existir:**
   - Clique no botão **"Add Environment Variable"** (ou **"+ Add"**)
   - No campo **"Key"**, digite: `VITE_SITE_ADMIN_TOKEN`
   - No campo **"Value"**, cole: `vNFkVqGDZ4QOcrMLdEKPSx3upInRaTAstogl6Ch8HmYJyB5eb1wiWXf270z9jU`
   - Clique em **"Save Changes"**

### 4️⃣ Reiniciar o Serviço

Após adicionar/atualizar a variável, você precisa reiniciar o serviço:

1. Vá para a aba **"Manual Deploy"** (ou **"Deploys"**)
2. Clique em **"Deploy latest commit"**
   - Ou **"Clear build cache & deploy"** (recomendado na primeira vez)
3. Aguarde o deploy completar (2-5 minutos)
4. Você verá os logs do build em tempo real

---

## ✅ Verificação Após o Deploy

### 1. Verificar Health Check
Acesse no navegador:
```
https://allianza-wallet-backend-1.onrender.com/health
```

Deve retornar algo como:
```json
{
  "status": "healthy",
  "database": "connected",
  ...
}
```

### 2. Testar o Painel Admin
1. Acesse: `http://localhost:5173/admin`
2. Use a senha: `AllianzaAdmin2025!`
3. O erro `401 - Token inválido` deve desaparecer
4. Os dados devem carregar normalmente

---

## 📝 Checklist Completo

- [ ] Acessei o dashboard do Render
- [ ] Encontrei o serviço `allianza-wallet-backend-1`
- [ ] Adicionei/atualizei a variável `VITE_SITE_ADMIN_TOKEN`
- [ ] Valor do token está correto (sem espaços extras)
- [ ] Salvei as alterações
- [ ] Iniciei um novo deploy
- [ ] Deploy completou com sucesso
- [ ] Testei o health check
- [ ] Testei o painel admin localmente

---

## 🔍 Troubleshooting

### ❌ Erro: "Token inválido" ainda aparece

**Possíveis causas:**
1. Token não foi salvo corretamente
   - **Solução:** Verifique se não há espaços antes/depois do valor
   - Verifique se o nome da variável está exatamente: `VITE_SITE_ADMIN_TOKEN`

2. Serviço não foi reiniciado
   - **Solução:** Faça um novo deploy manual

3. Cache do navegador
   - **Solução:** Limpe o cache (Ctrl+Shift+Delete) ou use modo anônimo

### ❌ Deploy falha

**Verifique:**
1. Logs do build no Render
2. Se todas as dependências estão instaladas
3. Se o `requirements.txt` está atualizado

### ❌ Serviço não inicia

**Verifique:**
1. Logs de runtime no Render
2. Se `DATABASE_URL` está configurada
3. Se todas as variáveis obrigatórias estão presentes

---

## 🔗 Links Úteis

- **Dashboard Render:** https://dashboard.render.com
- **Repositório GitHub:** https://github.com/brunosmaach-spec/allianza-wallet-backend
- **URL do Serviço:** https://allianza-wallet-backend-1.onrender.com

---

## 📞 Informações de Suporte

Se precisar de ajuda adicional:
1. Verifique os logs no Render (aba "Logs")
2. Verifique os logs do console do navegador (F12)
3. Compare o token no frontend e backend

---

**Última atualização:** 2025-01-XX  
**Status:** ⏳ Aguardando atualização manual no Render

