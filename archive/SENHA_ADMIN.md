# 🔐 Senha do Admin

## 📋 Senhas Configuradas

### 1. **Frontend (Local) - Para acessar `/admin`**

**Senha:** `AllianzaAdmin2025!`

**Variável:** `VITE_ADMIN_PASSWORD`  
**Arquivo:** `.env` (frontend)

**Uso:** Esta é a senha que você usa para fazer login no painel admin em `http://localhost:5173/admin`

---

### 2. **Backend (Render) - Para autenticação no backend**

**Senha:** `H91fed103$$`

**Variável:** `ADMIN_PASSWORD_1`  
**Configurado em:** Render Dashboard → `allianza-wallet-backend-1` → Environment

**Uso:** Esta senha é usada internamente pelo backend para autenticação de rotas administrativas.

---

## 🎯 Qual Senha Usar?

### Para acessar o painel admin no navegador:

**URL:** http://localhost:5173/admin  
**Senha:** `AllianzaAdmin2025!`

---

## 📝 Verificar/Atualizar Senhas

### Frontend (Local)

**Arquivo:** `Site/.env`

```env
VITE_ADMIN_PASSWORD=AllianzaAdmin2025!
```

**Para mudar:** Edite o arquivo `.env` e reinicie o servidor frontend.

---

### Backend (Render)

**Dashboard:** https://dashboard.render.com  
**Serviço:** `allianza-wallet-backend-1` → `Environment`

**Variável:** `ADMIN_PASSWORD_1`  
**Valor atual:** `H91fed103$$`

**Para mudar:** Edite a variável no Render Dashboard e faça deploy.

---

## ⚠️ Importante

- A senha do **frontend** (`AllianzaAdmin2025!`) é usada para fazer login no painel admin
- A senha do **backend** (`H91fed103$$`) é usada internamente pelo backend
- Ambas são diferentes e servem propósitos diferentes

---

**Última atualização:** 2025-01-XX

