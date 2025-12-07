# ⚡ Ação Imediata: Resolver Erro 401

## ✅ O que já está feito:
- Frontend `.env` tem `VITE_SITE_ADMIN_TOKEN` ✅

## ⚠️ O que precisa ser verificado:

### 1. **Reiniciar Servidor Frontend** (CRÍTICO)

O Vite só carrega variáveis do `.env` na inicialização. Se você adicionou o token depois de iniciar o servidor, precisa reiniciar:

```powershell
# Pare o servidor (Ctrl+C no terminal onde está rodando)
# Depois inicie novamente:
cd "C:\Users\notebook\Downloads\Site New Mindset - Cursor\Site"
npm run dev
```

---

### 2. **Verificar Backend no Render**

**Acesse:** https://dashboard.render.com

1. Vá em: `allianza-wallet-backend-1` → `Environment`
2. **Verifique se existe:**
   - Key: `VITE_SITE_ADMIN_TOKEN`
   - Value: `vNFkVqGDZ4QOcrMLdEKPSx3upInRaTAstogl6Ch8HmYJyB5eb1wiWXf270z9jU`

3. **Se NÃO existir ou estiver diferente:**
   - Adicione/Edite a variável
   - **IMPORTANTE:** Clique em "Save Changes"
   - Vá em: `Manual Deploy` → `Clear build cache & deploy`
   - **Aguarde 2-5 minutos** para o deploy completar

---

### 3. **Verificar URL do Backend**

No código do AdminDashboard, verifique se está usando:

**✅ CORRETO:**
```
https://allianza-wallet-backend-1.onrender.com
```

**❌ ERRADO:**
```
https://allianza-wallet-backend.onrender.com
```

Se estiver usando a URL errada (sem o `-1`), precisa atualizar o código.

---

### 4. **Verificar Código do Backend**

O arquivo `backend/admin_routes.py` precisa ter na linha 28:

```python
SITE_ADMIN_TOKEN = os.getenv('VITE_SITE_ADMIN_TOKEN', 'allianza_super_admin_2024_CdE25$$$')
```

**Verifique no GitHub:**
- https://github.com/brunosmaach-spec/allianza-wallet-backend/blob/main/backend/admin_routes.py

Se não estiver atualizado, atualize manualmente no GitHub.

---

## 🎯 Ordem de Ação Recomendada:

1. **Pare e reinicie o servidor frontend** (mais provável de resolver)
2. **Verifique se o backend no Render tem a variável**
3. **Se não tiver, adicione e faça deploy**
4. **Teste novamente**

---

## 🔍 Como Testar:

1. Limpe o cache do navegador: `Ctrl + Shift + Delete`
2. Acesse: http://localhost:5173/admin
3. Use senha: `AllianzaAdmin2025!`
4. Verifique se o erro `401 - Token inválido` desapareceu

---

## 📞 Se ainda não funcionar:

1. Verifique os logs do backend no Render (aba "Logs")
2. Verifique o console do navegador (F12) para ver erros detalhados
3. Veja `TROUBLESHOOTING_TOKEN_401.md` para mais detalhes

