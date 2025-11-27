# 🔄 RECRIAR SERVIÇO NO RENDER (Solução Definitiva)

## ⚠️ Problema
O Render detectou seu serviço como **Elixir** e não há opção para mudar manualmente.

## ✅ SOLUÇÃO: Recriar usando Blueprint

### PASSO 1: Anotar Configurações Atuais
Antes de deletar, anote:
- **Health Check Path**: `/healthz` (ou `/health`)
- **Custom Domain**: (se tiver algum)
- **Environment Variables**: (se tiver alguma configurada)

### PASSO 2: Deletar o Serviço Atual

1. No Render Dashboard, vá até seu serviço
2. Role até o final da página
3. Clique em **"Delete Web Service"**
4. Confirme a exclusão

### PASSO 3: Criar Novo Serviço via Blueprint

1. No Dashboard do Render, clique em **"New +"** (canto superior direito)
2. Selecione **"Blueprint"**
3. Conecte seu repositório GitHub:
   - Selecione: `dieisonmaach-lang / allianzablockchain`
   - Clique em **"Connect"**
4. O Render vai detectar automaticamente o arquivo `render.yaml`
5. Clique em **"Apply"** ou **"Create"**

### PASSO 4: Verificar Configurações

Após criar, verifique se:
- ✅ Environment Type = **Python 3** (não Elixir!)
- ✅ Python Version = **3.10**
- ✅ Build Command = `pip install --upgrade pip && pip install -r requirements.txt`
- ✅ Start Command = `gunicorn -w 4 -b 0.0.0.0:$PORT --timeout 120 wsgi:application`
- ✅ Health Check Path = `/health` (ou `/healthz` se preferir)

### PASSO 5: Configurar Health Check (se necessário)

1. Vá em **Settings → Health Checks**
2. Altere **Health Check Path** para `/health` ou `/healthz`
3. Salve

### PASSO 6: Aguardar Deploy

O deploy deve iniciar automaticamente e agora deve funcionar corretamente!

## 📋 O que o render.yaml vai configurar automaticamente:

- ✅ Environment: Python 3
- ✅ Python Version: 3.10
- ✅ Build Command: Correto
- ✅ Start Command: Correto (sem gevent)
- ✅ Environment Variables: FLASK_ENV, FLASK_DEBUG, SECRET_KEY, PORT, HOST
- ✅ Health Check: /health
- ✅ Auto-Deploy: Ativado

## 🎯 Por que isso funciona?

O `render.yaml` força o Render a criar o serviço como **Python** desde o início, em vez de tentar detectar automaticamente (que falhou e detectou como Elixir).

## ⚠️ IMPORTANTE

Se você tiver um **Custom Domain** configurado:
1. Anote o domínio antes de deletar
2. Após recriar, vá em **Settings → Custom Domains**
3. Adicione o domínio novamente
4. Configure o DNS conforme as instruções do Render

---

**Depois de recriar, o serviço deve funcionar perfeitamente!** ✅

