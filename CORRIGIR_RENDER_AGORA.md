# 🚨 CORREÇÃO URGENTE - Render detectando como Elixir

## ⚠️ PROBLEMA ATUAL
O Render está:
- ❌ Detectando como **Elixir/Erlang** (não Python!)
- ❌ Usando comando antigo com `--worker-class gevent`
- ❌ Não encontrando `gunicorn` porque está no ambiente errado

## ✅ SOLUÇÃO PASSO A PASSO

### PASSO 1: Acesse o Dashboard do Render
1. Vá para https://dashboard.render.com
2. Clique no seu serviço **allianza-blockchain**

### PASSO 2: Vá em Settings → Environment

### PASSO 3: ALTERE ESTAS CONFIGURAÇÕES:

#### 3.1. Environment Type
**MUDE DE:** `Elixir` ou `Auto-detect`  
**PARA:** `Python 3` (selecione explicitamente!)

#### 3.2. Python Version
**SELECIONE:** `3.10` ou `3.11` (NÃO 3.13!)

#### 3.3. Build Command
**COLE EXATAMENTE:**
```
pip install --upgrade pip && pip install -r requirements.txt
```

#### 3.4. Start Command ⚠️ CRÍTICO!
**REMOVA** `--worker-class gevent` do comando!

**COMANDO CORRETO:**
```
gunicorn -w 4 -b 0.0.0.0:$PORT --timeout 120 wsgi:application
```

**NÃO USE:**
```
gunicorn -w 4 -b 0.0.0.0:$PORT --timeout 120 --worker-class gevent wsgi:application
```

### PASSO 4: Salve as Configurações
Clique em **"Save Changes"**

### PASSO 5: Faça um Novo Deploy
1. Vá em **"Manual Deploy"** (menu superior)
2. Selecione **"Deploy latest commit"**
3. Aguarde o deploy

## 📋 CHECKLIST ANTES DE SALVAR

- [ ] Environment Type = **Python 3** (não Elixir!)
- [ ] Python Version = **3.10** ou **3.11**
- [ ] Build Command = `pip install --upgrade pip && pip install -r requirements.txt`
- [ ] Start Command = `gunicorn -w 4 -b 0.0.0.0:$PORT --timeout 120 wsgi:application`
- [ ] Start Command **NÃO contém** `--worker-class gevent`

## 🔍 COMO VERIFICAR SE ESTÁ CORRETO

Após salvar, o log deve mostrar:
```
==> Using Python version 3.10.x
==> Installing dependencies...
==> Build successful 🎉
==> Running 'gunicorn -w 4 -b 0.0.0.0:$PORT --timeout 120 wsgi:application'
```

**NÃO deve mostrar:**
```
==> Using Erlang version...
==> Using Elixir version...
```

## 🆘 SE AINDA NÃO FUNCIONAR

### Opção: Recriar o Serviço

1. **Delete o serviço atual:**
   - Settings → Danger Zone → Delete Service

2. **Crie um novo:**
   - New → Web Service
   - Conecte seu repositório GitHub
   - Configure manualmente como mostrado acima

3. **OU use Blueprint:**
   - New → Blueprint
   - Conecte o repositório
   - O `render.yaml` deve ser detectado automaticamente

## 📝 NOTA IMPORTANTE

O **build já está funcionando** (todas as dependências foram instaladas com sucesso).  
O problema é apenas o **ambiente de execução** que está errado.

Depois de corrigir o Environment Type para Python 3, tudo deve funcionar! ✅

