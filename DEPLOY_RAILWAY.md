# 🚂 DEPLOY NA RAILWAY.APP - ALLIANZA BLOCKCHAIN

**Railway.app** é uma das melhores opções para deploy de aplicações Python/Flask.

---

## ✅ VANTAGENS

- ✅ **Gratuito** (com limites generosos)
- ✅ **Deploy automático** via Git
- ✅ **Suporte nativo a Python/Flask**
- ✅ **SSL automático**
- ✅ **Muito fácil de usar**
- ✅ **Logs em tempo real**

---

## 📦 PASSO 1: PREPARAR O PROJETO

### 1.1. Criar arquivo `Procfile`

Crie um arquivo `Procfile` na raiz do projeto:

```
web: gunicorn -w 4 -b 0.0.0.0:$PORT --timeout 120 wsgi:application
```

### 1.2. Criar arquivo `runtime.txt` (opcional)

Para especificar a versão do Python:

```
python-3.10.12
```

### 1.3. Atualizar `requirements.txt`

Já está atualizado com `gunicorn` e `gevent`.

---

## 🚀 PASSO 2: CRIAR CONTA NA RAILWAY

1. Acesse: https://railway.app
2. Clique em **"Start a New Project"**
3. Faça login com GitHub (recomendado) ou email

---

## 📤 PASSO 3: CONECTAR REPOSITÓRIO GIT

### Opção A: Via GitHub (Recomendado)

1. **Criar repositório no GitHub:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit - Allianza Blockchain"
   git remote add origin https://github.com/seu-usuario/allianza-blockchain.git
   git push -u origin main
   ```

2. **No Railway:**
   - Clique em **"New Project"**
   - Selecione **"Deploy from GitHub repo"**
   - Escolha seu repositório
   - Railway detectará automaticamente que é Python

### Opção B: Upload Direto

1. No Railway, clique em **"New Project"**
2. Selecione **"Empty Project"**
3. Clique em **"Add Service"** → **"GitHub Repo"** ou **"Upload"**

---

## ⚙️ PASSO 4: CONFIGURAR VARIÁVEIS DE AMBIENTE

No Railway, vá em **"Variables"** e adicione:

```env
FLASK_ENV=production
FLASK_DEBUG=False
SECRET_KEY=sua_chave_secreta_aqui_gerada_aleatoriamente
PORT=5000
HOST=0.0.0.0
```

**Ou use o arquivo `.env`** (Railway carrega automaticamente).

---

## 🚀 PASSO 5: CONFIGURAR BUILD E DEPLOY

### 5.1. Railway detecta automaticamente:

- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** Lê do `Procfile`

### 5.2. Se necessário, configure manualmente:

No Railway, vá em **"Settings"** → **"Deploy"**:

- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `gunicorn -w 4 -b 0.0.0.0:$PORT --timeout 120 wsgi:application`

---

## 🌐 PASSO 6: CONFIGURAR DOMÍNIO

1. No Railway, vá em **"Settings"** → **"Networking"**
2. Clique em **"Generate Domain"** (domínio gratuito)
3. Ou configure domínio customizado:
   - Adicione seu domínio
   - Configure DNS conforme instruções

---

## ✅ PASSO 7: VERIFICAR DEPLOY

1. Railway fará deploy automaticamente
2. Acompanhe os logs em tempo real
3. Acesse o domínio gerado
4. Teste os endpoints:
   - `https://seu-app.railway.app/health`
   - `https://seu-app.railway.app/testnet/professional-tests/`

---

## 🔧 CONFIGURAÇÕES AVANÇADAS

### Usar PostgreSQL (se necessário)

1. No Railway, adicione **"PostgreSQL"** service
2. Railway fornecerá variável `DATABASE_URL` automaticamente
3. Use no seu `.env` ou código

### Configurar Logs

- Logs são exibidos automaticamente no dashboard
- Exporte para serviços externos se necessário

---

## 💰 PLANOS E LIMITES

**Free Tier:**
- $5 créditos/mês (suficiente para testes)
- 500 horas de execução
- 100GB de egress

**Pro Plan:**
- $20/mês
- Créditos ilimitados
- Melhor performance

---

## 📋 CHECKLIST

- [ ] Conta Railway criada
- [ ] Repositório Git configurado
- [ ] `Procfile` criado
- [ ] `requirements.txt` atualizado
- [ ] Variáveis de ambiente configuradas
- [ ] Deploy realizado
- [ ] Domínio configurado
- [ ] Testes funcionando

---

**Railway é a opção mais fácil e rápida! 🚀**

