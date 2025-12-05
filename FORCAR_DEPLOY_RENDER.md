# 🔄 Forçar Deploy no Render

## ✅ Status Atual

**Commits enviados para GitHub:**
- ✅ `dc29f5a` - chore: adicionar node_modules e output.css ao .gitignore
- ✅ `00e1746` - fix: Melhorias críticas para testnet

**Repositório:** `dieisonmaach-lang/allianzablockchain`  
**Branch:** `main`

---

## 🚀 Como Forçar Deploy no Render

### Método 1: Deploy Manual (Recomendado)

1. **Acesse o Dashboard do Render:**
   - Vá para: https://dashboard.render.com
   - Faça login

2. **Encontre seu serviço:**
   - Procure por `allianza-blockchain` ou o nome do seu serviço
   - Clique no serviço

3. **Forçar Deploy:**
   - Clique na aba **"Manual Deploy"** (ou "Deploys")
   - Clique em **"Deploy latest commit"** ou **"Clear build cache & deploy"**
   - Aguarde o build completar (5-10 minutos)

### Método 2: Verificar Auto-Deploy

1. **Verificar Configuração:**
   - No dashboard do serviço, vá em **"Settings"**
   - Procure por **"Auto-Deploy"**
   - Certifique-se de que está **habilitado** e configurado para a branch `main`

2. **Verificar Webhook:**
   - Em **"Settings"** → **"Build & Deploy"**
   - Verifique se o webhook do GitHub está configurado
   - Se não estiver, clique em **"Connect GitHub"** novamente

### Método 3: Fazer Push Vazio (Trigger)

Se o auto-deploy não estiver funcionando, você pode forçar um novo deploy fazendo um commit vazio:

```bash
git commit --allow-empty -m "trigger: forçar deploy no Render"
git push origin main
```

---

## 🔍 Verificar se o Render Está Recebendo Atualizações

### 1. Verificar Logs do Render

1. No dashboard do Render, vá para **"Logs"**
2. Procure por mensagens como:
   - `"New commit detected"`
   - `"Building..."`
   - `"Deploying..."`

### 2. Verificar Último Deploy

1. Vá para a aba **"Deploys"**
2. Verifique a data/hora do último deploy
3. Compare com a data do último commit no GitHub

### 3. Verificar Webhook do GitHub

1. No GitHub, vá para: `Settings` → `Webhooks`
2. Procure por webhooks do Render
3. Verifique se há erros recentes

---

## ⚙️ Configurações Importantes no Render

### Build Command
```bash
pip install --upgrade pip && pip install -r requirements.txt
```

### Start Command
```bash
gunicorn -w 2 -b 0.0.0.0:$PORT --timeout 300 --keep-alive 5 --preload wsgi_optimized:application
```

### Variáveis de Ambiente Necessárias
- `FLASK_ENV=production`
- `FLASK_DEBUG=False`
- `SECRET_KEY=<sua-chave>`
- `PYTHONUNBUFFERED=1`

---

## 🐛 Problemas Comuns

### Render não detecta mudanças

**Solução:**
1. Verifique se está fazendo push para a branch correta (`main`)
2. Verifique se o auto-deploy está habilitado
3. Faça um deploy manual

### Build falha

**Solução:**
1. Verifique os logs do build no Render
2. Certifique-se de que `requirements.txt` está atualizado
3. Verifique se todas as dependências estão corretas

### Serviço não inicia

**Solução:**
1. Verifique os logs de runtime
2. Certifique-se de que `wsgi_optimized.py` existe
3. Verifique as variáveis de ambiente

---

## 📝 Checklist para Deploy

- [ ] Commits enviados para GitHub (`git push origin main`)
- [ ] Render conectado ao repositório correto
- [ ] Auto-deploy habilitado para branch `main`
- [ ] Variáveis de ambiente configuradas
- [ ] Build command correto
- [ ] Start command correto
- [ ] Webhook do GitHub funcionando

---

## 🚀 Próximos Passos

1. **Acesse o Render Dashboard**
2. **Verifique o último deploy**
3. **Se necessário, faça deploy manual**
4. **Aguarde o build completar**
5. **Teste a aplicação**

---

**Última atualização:** 2025-12-05  
**Commits no GitHub:** ✅ Enviados

