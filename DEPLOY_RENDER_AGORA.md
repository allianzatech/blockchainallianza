# ⚡ DEPLOY NO RENDER - AGORA MESMO!

**Tudo está pronto! Siga estes 5 passos simples:**

---

## 🚀 PASSO 1: PREPARAR GIT (2 minutos)

```bash
# Se ainda não tem Git inicializado
git init
git add .
git commit -m "Allianza Blockchain - Ready for Render"

# Criar repositório no GitHub e conectar
git remote add origin https://github.com/SEU_USUARIO/allianza-blockchain.git
git branch -M main
git push -u origin main
```

---

## 🎯 PASSO 2: CRIAR CONTA RENDER (1 minuto)

1. Acesse: **https://render.com**
2. Clique em **"Get Started for Free"**
3. Faça login com **GitHub**

---

## 📤 PASSO 3: CRIAR SERVIÇO (2 minutos)

1. No Render: **"New +"** → **"Web Service"**
2. Conecte seu repositório GitHub
3. Selecione `allianza-blockchain`
4. Render detecta automaticamente Python ✅

---

## ⚙️ PASSO 4: CONFIGURAR (1 minuto)

### Variáveis de Ambiente:

Clique em **"Environment"** e adicione:

```env
FLASK_ENV=production
FLASK_DEBUG=False
SECRET_KEY=GERE_UMA_CHAVE_AQUI
```

**Gerar SECRET_KEY:**
```python
python -c "import secrets; print(secrets.token_hex(32))"
```

### Build & Start:

✅ **Já está configurado automaticamente!**
- Build: `pip install -r requirements.txt`
- Start: Lê do `Procfile`

---

## 🚀 PASSO 5: DEPLOY (5-10 minutos)

1. Clique em **"Create Web Service"**
2. Aguarde o build (5-10 minutos)
3. Pronto! ✅

**URL:** `https://allianza-blockchain.onrender.com`

---

## ✅ TESTAR

Acesse:
- `https://allianza-blockchain.onrender.com/health`
- `https://allianza-blockchain.onrender.com/testnet/professional-tests/`

---

## 🎉 PRONTO!

Sua Allianza Blockchain está online! 🚀

**Tempo total:** ~10 minutos

---

**Dúvidas?** Veja `DEPLOY_RENDER_PASSO_A_PASSO.md` para guia completo.

