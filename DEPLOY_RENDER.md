# 🎨 DEPLOY NO RENDER.COM - ALLIANZA BLOCKCHAIN

**Render.com** oferece free tier generoso e é excelente para Python/Flask.

---

## ✅ VANTAGENS

- ✅ **Free tier disponível**
- ✅ **Deploy automático via Git**
- ✅ **SSL automático**
- ✅ **Muito fácil de usar**
- ✅ **Suporte a Python/Flask nativo**

---

## 📦 PASSO 1: PREPARAR O PROJETO

### 1.1. Criar arquivo `render.yaml` (opcional)

Crie `render.yaml` na raiz:

```yaml
services:
  - type: web
    name: allianza-blockchain
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: gunicorn -w 4 -b 0.0.0.0:$PORT --timeout 120 wsgi:application
    envVars:
      - key: FLASK_ENV
        value: production
      - key: FLASK_DEBUG
        value: "False"
      - key: SECRET_KEY
        generateValue: true
```

### 1.2. Criar arquivo `Procfile`

```
web: gunicorn -w 4 -b 0.0.0.0:$PORT --timeout 120 wsgi:application
```

---

## 🚀 PASSO 2: CRIAR CONTA NO RENDER

1. Acesse: https://render.com
2. Clique em **"Get Started for Free"**
3. Faça login com GitHub (recomendado)

---

## 📤 PASSO 3: CONECTAR REPOSITÓRIO

1. No Render, clique em **"New +"** → **"Web Service"**
2. Conecte seu repositório GitHub
3. Render detectará automaticamente que é Python

---

## ⚙️ PASSO 4: CONFIGURAR SERVIÇO

### 4.1. Configurações Básicas:

- **Name:** `allianza-blockchain`
- **Environment:** `Python 3`
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `gunicorn -w 4 -b 0.0.0.0:$PORT --timeout 120 wsgi:application`

### 4.2. Variáveis de Ambiente:

Clique em **"Environment"** e adicione:

```env
FLASK_ENV=production
FLASK_DEBUG=False
SECRET_KEY=sua_chave_secreta_aqui
PORT=5000
HOST=0.0.0.0
```

---

## 🌐 PASSO 5: CONFIGURAR DOMÍNIO

1. No Render, vá em **"Settings"** → **"Custom Domains"**
2. Render fornece domínio gratuito: `seu-app.onrender.com`
3. Para domínio customizado:
   - Adicione seu domínio
   - Configure DNS conforme instruções

---

## ✅ PASSO 6: DEPLOY

1. Clique em **"Create Web Service"**
2. Render fará build e deploy automaticamente
3. Acompanhe os logs em tempo real
4. Aguarde alguns minutos (primeiro deploy é mais lento)

---

## 🔧 CONFIGURAÇÕES AVANÇADAS

### Auto-Deploy

- Render faz deploy automático a cada push no Git
- Ou configure para deploy manual

### Health Checks

- Render verifica automaticamente se o serviço está rodando
- Configure endpoint `/health` para melhor monitoramento

---

## 💰 PLANOS E LIMITES

**Free Tier:**
- Serviços "spin down" após 15min de inatividade
- 750 horas/mês
- SSL gratuito

**Starter Plan:**
- $7/mês
- Sem spin down
- Melhor performance

---

## 📋 CHECKLIST

- [ ] Conta Render criada
- [ ] Repositório conectado
- [ ] `Procfile` criado
- [ ] `render.yaml` criado (opcional)
- [ ] Variáveis de ambiente configuradas
- [ ] Deploy realizado
- [ ] Domínio configurado
- [ ] Testes funcionando

---

**Render é excelente e tem free tier! 🎨**

