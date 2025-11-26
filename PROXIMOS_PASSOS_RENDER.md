# 🚀 PRÓXIMOS PASSOS - DEPLOY NO RENDER

**Repositório GitHub:** `dieisonmaach-lang/allianzablockchain` ✅

---

## ✅ PASSO 1: VERIFICAR GIT (JÁ FEZ)

Você já executou:
```bash
git remote add origin https://github.com/dieisonmaach-lang/allianzablockchain.git
git branch -M main
git push -u origin main
```

**Se o push foi bem-sucedido, continue!** ✅

---

## 🎯 PASSO 2: CRIAR CONTA NO RENDER

1. Acesse: **https://render.com**
2. Clique em **"Get Started for Free"**
3. Faça login com **GitHub** (mesma conta: `dieisonmaach-lang`)

---

## 📤 PASSO 3: CRIAR WEB SERVICE

1. No Render, clique em **"New +"** → **"Web Service"**

2. **Conectar GitHub:**
   - Se ainda não conectou, clique em **"Connect GitHub"**
   - Autorize o Render a acessar seus repositórios
   - Selecione **"All repositories"** ou apenas `allianzablockchain`

3. **Selecionar repositório:**
   - Escolha: `dieisonmaach-lang/allianzablockchain`
   - Render detectará automaticamente que é Python ✅

---

## ⚙️ PASSO 4: CONFIGURAR SERVIÇO

### 4.1. Configurações Básicas (já detectadas automaticamente):

- **Name:** `allianza-blockchain` (ou deixe o padrão)
- **Environment:** `Python 3` ✅
- **Region:** Escolha mais próximo (ex: `Oregon (US West)`)
- **Branch:** `main` ✅

### 4.2. Build & Start (já configurado):

✅ **Render detecta automaticamente:**
- **Build Command:** `pip install -r requirements.txt` ✅
- **Start Command:** Lê do `Procfile` ✅

**NÃO precisa alterar nada!** Está tudo configurado.

### 4.3. Variáveis de Ambiente:

Clique em **"Environment"** e adicione estas variáveis:

```env
FLASK_ENV=production
FLASK_DEBUG=False
SECRET_KEY=<COLE_AQUI_A_CHAVE_GERADA>
```

**Para gerar SECRET_KEY, execute:**
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

Copie a chave gerada e cole no campo `SECRET_KEY` no Render.

---

## 🚀 PASSO 5: FAZER DEPLOY

1. Clique em **"Create Web Service"**

2. **Render fará automaticamente:**
   - ✅ Clone do repositório
   - ✅ Instalação de dependências
   - ✅ Build da aplicação
   - ✅ Deploy

3. **Acompanhe os logs:**
   - Você verá o progresso em tempo real
   - Primeiro deploy pode levar **5-10 minutos**

4. **Aguarde até ver:**
   ```
   ✅ Your service is live!
   ```

---

## ✅ PASSO 6: VERIFICAR SE ESTÁ FUNCIONANDO

1. **Render fornece URL automática:**
   - `https://allianza-blockchain.onrender.com`
   - Ou outro nome se você escolheu diferente

2. **Teste os endpoints:**
   - `https://allianza-blockchain.onrender.com/health`
   - `https://allianza-blockchain.onrender.com/testnet/professional-tests/`
   - `https://allianza-blockchain.onrender.com/dashboard`

3. **Você deve ver:**
   - Interface da Allianza Blockchain funcionando! ✅

---

## 🔧 CONFIGURAÇÕES OPCIONAIS

### Domínio Customizado:

1. No Render: **Settings** → **Custom Domains**
2. Clique em **"Add Custom Domain"**
3. Digite seu domínio
4. Configure DNS conforme instruções

### Auto-Deploy:

- ✅ **Já está ativado!** Cada push no Git faz deploy automático
- Para desabilitar: Settings → Auto-Deploy → Off

---

## 📋 CHECKLIST

- [x] Repositório Git configurado
- [x] Código enviado para GitHub
- [ ] Conta Render criada
- [ ] Serviço criado no Render
- [ ] Repositório conectado
- [ ] Variáveis de ambiente configuradas
- [ ] Deploy realizado
- [ ] Site acessível
- [ ] Testes funcionando

---

## 🆘 SE TIVER PROBLEMAS

### Erro no Build:

1. **Verifique os logs no Render:**
   - Dashboard → Logs
   - Procure por erros específicos

2. **Verifique requirements.txt:**
   - Confirme que todas as dependências estão listadas

### Erro 500:

1. **Verifique logs:**
   - Dashboard → Logs
   - Procure por erros de importação

2. **Verifique SECRET_KEY:**
   - Confirme que está configurada
   - Deve ser uma string longa (64 caracteres hex)

### Serviço não inicia:

1. **Verifique Procfile:**
   - Deve estar na raiz do projeto
   - Conteúdo: `web: gunicorn -w 4 -b 0.0.0.0:$PORT --timeout 120 --worker-class gevent wsgi:application`

2. **Verifique wsgi.py:**
   - Deve estar na raiz
   - Deve ter variável `application` definida

---

## 🎉 PRONTO!

Após seguir estes passos, sua Allianza Blockchain estará online no Render! 🚀

**URL:** `https://allianza-blockchain.onrender.com`

---

**Última Atualização:** 2025-11-26

