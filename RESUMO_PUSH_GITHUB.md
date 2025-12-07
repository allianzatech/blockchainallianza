# 📤 Resumo: Push para GitHub

## ✅ Status do Arquivo

O arquivo `backend/admin_routes.py` **já está atualizado** com:
```python
SITE_ADMIN_TOKEN = os.getenv('VITE_SITE_ADMIN_TOKEN', 'allianza_super_admin_2024_CdE25$$$')
```

## ⚠️ Problema de Permissão

O push falhou porque:
- **Usuário atual:** `dieisonmaach-lang`
- **Repositório remoto:** `brunosmaach-spec/allianza-wallet-backend`
- **Erro:** `Permission denied (403)`

## 🔧 Soluções

### Opção 1: Configurar Credenciais Corretas

Se você tem acesso ao repositório `brunosmaach-spec/allianza-wallet-backend`:

1. **Gerar Personal Access Token no GitHub:**
   - Acesse: https://github.com/settings/tokens
   - Clique em "Generate new token (classic)"
   - Dê permissões: `repo`
   - Copie o token

2. **Configurar Git com o token:**
   ```powershell
   cd "C:\Users\notebook\Downloads\allianza-wallet1"
   git remote set-url origin https://SEU_TOKEN@github.com/brunosmaach-spec/allianza-wallet-backend.git
   ```

3. **Fazer push:**
   ```powershell
   git add backend/admin_routes.py
   git commit -m "chore: atualizar admin_routes.py para usar VITE_SITE_ADMIN_TOKEN"
   git push origin main
   ```

### Opção 2: Push Manual via GitHub Web Interface

1. Acesse: https://github.com/brunosmaach-spec/allianza-wallet-backend
2. Vá em: `backend/admin_routes.py`
3. Clique em "Edit" (lápis)
4. Verifique se a linha 28 está assim:
   ```python
   SITE_ADMIN_TOKEN = os.getenv('VITE_SITE_ADMIN_TOKEN', 'allianza_super_admin_2024_CdE25$$$')
   ```
5. Se estiver diferente, atualize e salve
6. Commit: "chore: atualizar admin_routes.py para usar VITE_SITE_ADMIN_TOKEN"

### Opção 3: Usar SSH (se configurado)

```powershell
cd "C:\Users\notebook\Downloads\allianza-wallet1"
git remote set-url origin git@github.com:brunosmaach-spec/allianza-wallet-backend.git
git add backend/admin_routes.py
git commit -m "chore: atualizar admin_routes.py para usar VITE_SITE_ADMIN_TOKEN"
git push origin main
```

## 📝 Verificação

Após o push, verifique se o arquivo está atualizado no GitHub:
- URL: https://github.com/brunosmaach-spec/allianza-wallet-backend/blob/main/backend/admin_routes.py
- Linha 28 deve conter: `VITE_SITE_ADMIN_TOKEN`

## 🚀 Próximos Passos

Após o push bem-sucedido:
1. O Render detectará automaticamente a mudança (se auto-deploy estiver ativo)
2. Ou faça deploy manual no Render
3. Configure `VITE_SITE_ADMIN_TOKEN` no Render (se ainda não estiver)
4. Teste o admin panel: http://localhost:5173/admin

---

**Última atualização:** 2025-01-XX

