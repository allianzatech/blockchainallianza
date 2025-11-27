# ⚙️ CONFIGURAR RENDER MANUALMENTE - VALORES CORRETOS

## 📋 CAMPOS PARA PREENCHER

### ✅ Campos já corretos:
- **Name:** `allianzablockchain` ✅
- **Language:** `Python 3` ✅
- **Branch:** `main` ✅
- **Region:** `Oregon (US West)` ✅
- **Instance Type:** `Free` ✅

### 🔧 Campos que PRECISAM ser alterados:

#### 1. Build Command
**MUDE DE:**
```
pip install -r requirements.txt
```

**PARA:**
```
pip install --upgrade pip && pip install -r requirements.txt
```

#### 2. Start Command ⚠️ CRÍTICO!
**MUDE DE:**
```
gunicorn app:app
```

**PARA:**
```
gunicorn -w 4 -b 0.0.0.0:$PORT --timeout 120 wsgi:application
```

### 🔑 Environment Variables (Adicionar 3 variáveis):

Clique em **"Add Environment Variable"** e adicione:

#### Variável 1:
- **NAME:** `FLASK_ENV`
- **VALUE:** `production`

#### Variável 2:
- **NAME:** `FLASK_DEBUG`
- **VALUE:** `False`

#### Variável 3:
- **NAME:** `SECRET_KEY`
- **VALUE:** (gere uma chave - veja abaixo)

**Para gerar SECRET_KEY:**
Execute no terminal:
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

Ou use esta chave de exemplo (substitua por uma gerada):
```
a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v2w3x4y5z6
```

---

## ✅ CHECKLIST ANTES DE CRIAR

- [ ] Build Command = `pip install --upgrade pip && pip install -r requirements.txt`
- [ ] Start Command = `gunicorn -w 4 -b 0.0.0.0:$PORT --timeout 120 wsgi:application`
- [ ] Instance Type = **Free** (já selecionado)
- [ ] Environment Variable: `FLASK_ENV` = `production`
- [ ] Environment Variable: `FLASK_DEBUG` = `False`
- [ ] Environment Variable: `SECRET_KEY` = (chave gerada)

---

## 🚀 DEPOIS DE CRIAR

1. Clique em **"Deploy web service"**
2. Aguarde o build (5-10 minutos)
3. Após o deploy, vá em **Settings → Health Checks**
4. Configure **Health Check Path:** `/health`

---

## 📝 RESUMO DOS VALORES

```
Name: allianzablockchain
Language: Python 3
Branch: main
Region: Oregon (US West)
Root Directory: (deixe vazio)
Build Command: pip install --upgrade pip && pip install -r requirements.txt
Start Command: gunicorn -w 4 -b 0.0.0.0:$PORT --timeout 120 wsgi:application
Instance Type: Free

Environment Variables:
  FLASK_ENV=production
  FLASK_DEBUG=False
  SECRET_KEY=<sua_chave_gerada>
```

---

**Preencha esses campos e clique em "Deploy web service"!** 🚀

