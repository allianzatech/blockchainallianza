# 🔧 Troubleshooting: Erro 401 - Token Inválido

## ❌ Problema

Após atualizar manualmente no Render, o erro `401 - Token inválido` ainda persiste.

## 🔍 Verificações Necessárias

### 1. Verificar se o Frontend está usando o token correto

O frontend precisa ter a variável `VITE_SITE_ADMIN_TOKEN` configurada no arquivo `.env`:

**Arquivo:** `Site/.env`

```env
VITE_SITE_ADMIN_TOKEN=vNFkVqGDZ4QOcrMLdEKPSx3upInRaTAstogl6Ch8HmYJyB5eb1wiWXf270z9jU
```

**⚠️ IMPORTANTE:**
- Após adicionar/atualizar o `.env`, **reinicie o servidor de desenvolvimento**
- No Vite, pare o servidor (Ctrl+C) e inicie novamente: `npm run dev`

---

### 2. Verificar se o Backend no Render tem a variável

**No Render Dashboard:**

1. Acesse: https://dashboard.render.com
2. Vá em: `allianza-wallet-backend-1` → `Environment`
3. Verifique se existe:
   - **Key:** `VITE_SITE_ADMIN_TOKEN`
   - **Value:** `vNFkVqGDZ4QOcrMLdEKPSx3upInRaTAstogl6Ch8HmYJyB5eb1wiWXf270z9jU`

**⚠️ ATENÇÃO:**
- Verifique se **NÃO há espaços** antes ou depois do valor
- Verifique se o nome está **exatamente** `VITE_SITE_ADMIN_TOKEN` (case-sensitive)

---

### 3. Verificar se o Backend foi reiniciado

**Após adicionar/atualizar a variável:**

1. Vá em: `Manual Deploy` (ou `Deploys`)
2. Clique em: **"Clear build cache & deploy"**
3. Aguarde o deploy completar (2-5 minutos)
4. Verifique os logs para garantir que não houve erros

**⚠️ IMPORTANTE:**
- Apenas salvar a variável **NÃO é suficiente**
- É necessário fazer um **novo deploy** para o backend pegar a nova variável

---

### 4. Verificar a URL do Backend

O frontend pode estar usando uma URL diferente. Verifique:

**No código do AdminDashboard, procure por:**
- `allianza-wallet-backend.onrender.com` (sem o `-1`)
- `allianza-wallet-backend-1.onrender.com` (com o `-1`)

**A URL correta é:**
```
https://allianza-wallet-backend-1.onrender.com
```

Se estiver usando `allianza-wallet-backend.onrender.com` (sem o `-1`), você precisa atualizar para `allianza-wallet-backend-1.onrender.com`.

---

### 5. Verificar se o código do backend está atualizado

O arquivo `backend/admin_routes.py` precisa ter:

```python
SITE_ADMIN_TOKEN = os.getenv('VITE_SITE_ADMIN_TOKEN', 'allianza_super_admin_2024_CdE25$$$')
```

**Verifique no GitHub:**
- https://github.com/brunosmaach-spec/allianza-wallet-backend/blob/main/backend/admin_routes.py
- Linha 28 deve conter: `VITE_SITE_ADMIN_TOKEN`

**Se não estiver atualizado:**
- Atualize manualmente no GitHub (veja `SOLUCAO_FINAL_PUSH.md`)
- Faça um novo deploy no Render

---

### 6. Limpar Cache do Navegador

Às vezes o navegador pode estar usando dados em cache:

1. Pressione `Ctrl + Shift + Delete`
2. Selecione "Cookies e dados de sites" e "Imagens e arquivos em cache"
3. Clique em "Limpar dados"
4. Recarregue a página: `Ctrl + Shift + R` (hard refresh)

---

### 7. Testar o Backend Diretamente

Teste se o backend está funcionando:

**Health Check:**
```bash
curl https://allianza-wallet-backend-1.onrender.com/health
```

**Teste de Token (substitua TOKEN pelo valor real):**
```bash
curl -H "X-Admin-Token: vNFkVqGDZ4QOcrMLdEKPSx3upInRaTAstogl6Ch8HmYJyB5eb1wiWXf270z9jU" \
     https://allianza-wallet-backend-1.onrender.com/api/site/admin/payments
```

Se retornar `401`, o problema está no backend.
Se retornar dados, o problema está no frontend.

---

## ✅ Checklist Completo

- [ ] Frontend `.env` tem `VITE_SITE_ADMIN_TOKEN` configurado
- [ ] Frontend servidor foi reiniciado após atualizar `.env`
- [ ] Backend no Render tem `VITE_SITE_ADMIN_TOKEN` configurado
- [ ] Backend no Render foi reiniciado (deploy feito)
- [ ] URL do backend está correta (`allianza-wallet-backend-1.onrender.com`)
- [ ] Código do backend está atualizado (linha 28 com `VITE_SITE_ADMIN_TOKEN`)
- [ ] Cache do navegador foi limpo
- [ ] Teste direto do backend funcionou

---

## 🎯 Solução Rápida (Passo a Passo)

1. **Frontend:**
   ```powershell
   cd "C:\Users\notebook\Downloads\Site New Mindset - Cursor\Site"
   # Verificar se .env tem VITE_SITE_ADMIN_TOKEN
   # Se não tiver, adicionar:
   # VITE_SITE_ADMIN_TOKEN=vNFkVqGDZ4QOcrMLdEKPSx3upInRaTAstogl6Ch8HmYJyB5eb1wiWXf270z9jU
   # Reiniciar servidor: npm run dev
   ```

2. **Backend no Render:**
   - Acesse: https://dashboard.render.com
   - Vá em: `allianza-wallet-backend-1` → `Environment`
   - Adicione/Atualize: `VITE_SITE_ADMIN_TOKEN` = `vNFkVqGDZ4QOcrMLdEKPSx3upInRaTAstogl6Ch8HmYJyB5eb1wiWXf270z9jU`
   - Salve
   - Vá em: `Manual Deploy` → `Clear build cache & deploy`
   - Aguarde 2-5 minutos

3. **Teste:**
   - Limpe cache do navegador
   - Acesse: http://localhost:5173/admin
   - Use senha: `AllianzaAdmin2025!`

---

## 📞 Se Ainda Não Funcionar

1. Verifique os logs do backend no Render (aba "Logs")
2. Verifique o console do navegador (F12) para ver erros detalhados
3. Verifique se há outros serviços/backends rodando que possam estar interferindo

