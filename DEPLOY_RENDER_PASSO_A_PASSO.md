# 🎨 DEPLOY NO RENDER - PASSO A PASSO COMPLETO

**Tudo pronto para deploy no Render.com!** 🚀

---

## ✅ ARQUIVOS JÁ PRONTOS

Todos os arquivos necessários já foram criados:

- ✅ `Procfile` - Comando de inicialização
- ✅ `render.yaml` - Configuração do Render
- ✅ `wsgi.py` - Entry point WSGI
- ✅ `requirements.txt` - Dependências completas
- ✅ `.gitignore` - Arquivos a ignorar

---

## 🚀 PASSO 1: CRIAR CONTA NO RENDER

1. Acesse: **https://render.com**
2. Clique em **"Get Started for Free"**
3. Faça login com **GitHub** (recomendado) ou email

---

## 📤 PASSO 2: PREPARAR REPOSITÓRIO GIT

### 2.1. Se você já tem repositório Git:

```bash
# Verificar se está no Git
git status

# Se não estiver, inicializar
git init
git add .
git commit -m "Allianza Blockchain - Ready for Render"
```

### 2.2. Criar repositório no GitHub (se não tiver):

1. Acesse: **https://github.com**
2. Clique em **"New repository"**
3. Nome: `allianza-blockchain` (ou o que preferir)
4. **NÃO** marque "Initialize with README"
5. Clique em **"Create repository"**

### 2.3. Conectar repositório local ao GitHub:

```bash
# Adicionar remote (substitua SEU_USUARIO)
git remote add origin https://github.com/SEU_USUARIO/allianza-blockchain.git

# Fazer push
git branch -M main
git push -u origin main
```

---

## 🎯 PASSO 3: CRIAR SERVIÇO NO RENDER

1. No Render, clique em **"New +"** → **"Web Service"**

2. **Conectar repositório:**
   - Se já conectou GitHub, selecione o repositório
   - Se não, clique em **"Connect account"** e autorize

3. **Selecionar repositório:**
   - Escolha `allianza-blockchain` (ou o nome que você usou)

---

## ⚙️ PASSO 4: CONFIGURAR SERVIÇO

### 4.1. Configurações Básicas:

- **Name:** `allianza-blockchain` (ou o nome que preferir)
- **Environment:** `Python 3`
- **Region:** Escolha mais próximo (ex: `Oregon (US West)`)
- **Branch:** `main` (ou `master`)

### 4.2. Build & Deploy:

O Render detectará automaticamente:
- **Build Command:** `pip install -r requirements.txt` ✅
- **Start Command:** Lê do `Procfile` ✅

**OU configure manualmente:**

- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `gunicorn -w 4 -b 0.0.0.0:$PORT --timeout 120 wsgi:application`

### 4.3. Variáveis de Ambiente:

Clique em **"Environment"** e adicione:

```env
FLASK_ENV=production
FLASK_DEBUG=False
SECRET_KEY=GERE_UMA_CHAVE_SECRETA_ALEATORIA_AQUI
PORT=5000
HOST=0.0.0.0
```

**Para gerar SECRET_KEY:**
```python
import secrets
print(secrets.token_hex(32))
```

Ou use este gerador online: https://randomkeygen.com/

---

## 🌐 PASSO 5: CONFIGURAR DOMÍNIO

1. No Render, vá em **"Settings"** → **"Custom Domains"**

2. **Domínio gratuito do Render:**
   - Render fornece automaticamente: `allianza-blockchain.onrender.com`
   - Já está configurado e funcionando!

3. **Domínio customizado (opcional):**
   - Clique em **"Add Custom Domain"**
   - Digite seu domínio (ex: `seu-dominio.com`)
   - Configure DNS conforme instruções do Render

---

## 🚀 PASSO 6: FAZER DEPLOY

1. Clique em **"Create Web Service"**

2. **Render fará automaticamente:**
   - Clone do repositório
   - Instalação de dependências (`pip install -r requirements.txt`)
   - Build da aplicação
   - Deploy

3. **Acompanhe os logs:**
   - Você verá o progresso em tempo real
   - Primeiro deploy pode levar 5-10 minutos

4. **Aguarde até ver:**
   ```
   ✅ Your service is live!
   ```

---

## ✅ PASSO 7: VERIFICAR SE ESTÁ FUNCIONANDO

1. **Acesse o domínio:**
   - `https://allianza-blockchain.onrender.com`
   - Ou seu domínio customizado

2. **Teste os endpoints:**
   - `https://allianza-blockchain.onrender.com/health`
   - `https://allianza-blockchain.onrender.com/testnet/professional-tests/`
   - `https://allianza-blockchain.onrender.com/dashboard`

3. **Você deve ver:**
   - Interface da Allianza Blockchain funcionando! ✅

---

## 🔧 CONFIGURAÇÕES AVANÇADAS

### Auto-Deploy

- ✅ **Automático:** Render faz deploy a cada push no Git
- Para desabilitar: Settings → Auto-Deploy → Off

### Health Checks

- Render verifica automaticamente se o serviço está rodando
- Endpoint `/health` é usado automaticamente

### Logs

- Acesse **"Logs"** no dashboard do Render
- Logs em tempo real
- Histórico disponível

---

## 💰 PLANOS E LIMITES

### Free Tier:
- ✅ **750 horas/mês** de execução
- ⚠️ **Spin down:** Serviço "dorme" após 15min de inatividade
- ✅ **SSL gratuito**
- ✅ **Deploy ilimitado**

### Starter Plan ($7/mês):
- ✅ **Sem spin down** (sempre online)
- ✅ **Melhor performance**
- ✅ **Mais recursos**

---

## 🔍 TROUBLESHOOTING

### ❌ Erro no Build

**Verifique:**
1. Logs do build no Render
2. Se `requirements.txt` está correto
3. Se todas as dependências estão listadas

**Solução:**
- Verifique os logs em tempo real
- Procure por erros específicos
- Adicione dependências faltantes ao `requirements.txt`

### ❌ Erro 500

**Verifique:**
1. Logs do serviço no Render
2. Se `wsgi.py` está correto
3. Se variáveis de ambiente estão configuradas

**Solução:**
- Acesse **"Logs"** no Render
- Procure por erros específicos
- Verifique se `SECRET_KEY` está configurada

### ❌ Serviço "Spinning Down"

**Isso é normal no Free Tier:**
- Após 15min de inatividade, o serviço "dorme"
- Primeira requisição após spin down pode levar 30-60s
- Para evitar: Upgrade para Starter Plan ($7/mês)

---

## 📋 CHECKLIST FINAL

Antes de considerar completo:

- [ ] Conta Render criada
- [ ] Repositório Git configurado
- [ ] Código enviado para GitHub
- [ ] Serviço criado no Render
- [ ] Repositório conectado
- [ ] Variáveis de ambiente configuradas
- [ ] Deploy realizado com sucesso
- [ ] Site acessível no navegador
- [ ] Endpoint `/health` funcionando
- [ ] Dashboard acessível

---

## 🎯 PRÓXIMOS PASSOS APÓS DEPLOY

1. **Configurar domínio customizado** (se tiver)
2. **Monitorar logs** regularmente
3. **Configurar backups** (se necessário)
4. **Otimizar performance** conforme necessário

---

## ✅ PRONTO!

Sua Allianza Blockchain Testnet está online no Render! 🚀

**URL:** `https://allianza-blockchain.onrender.com`

---

**Última Atualização:** 2025-11-26

