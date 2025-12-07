# ⚠️ Problema: Token GitHub sem Permissão de Escrita

## 📊 Status Atual

✅ **O que funciona:**
- Token consegue **ler** o repositório (`git fetch`, `git ls-remote`)
- Arquivo `backend/admin_routes.py` está **correto localmente**:
  ```python
  SITE_ADMIN_TOKEN = os.getenv('VITE_SITE_ADMIN_TOKEN', 'allianza_super_admin_2024_CdE25$$$')
  ```
- Commit local criado: `1deff7b`

❌ **O que não funciona:**
- Token **não consegue escrever** (`git push` falha com erro 403)
- Erro: `Permission to brunosmaach-spec/allianza-wallet-backend.git denied`

## 🔍 Causa Provável

O Personal Access Token foi gerado **sem permissão de escrita** ou o repositório tem **proteções de branch** que impedem push direto.

## ✅ Soluções

### Opção 1: Regenerar Token com Permissões Corretas (Recomendado)

1. Acesse: https://github.com/settings/tokens
2. **Delete o token atual** (ou gere um novo)
3. Clique em **"Generate new token (classic)"**
4. Configure:
   - **Note:** `allianza-wallet-backend-write`
   - **Expiration:** Escolha uma data (ou "No expiration")
   - **Scopes:** Marque **TODAS** as opções em `repo`:
     - ✅ `repo:status`
     - ✅ `repo_deployment`
     - ✅ `public_repo`
     - ✅ `repo:invite`
     - ✅ `security_events`
5. Clique em **"Generate token"**
6. **COPIE O NOVO TOKEN**

Depois, execute:
```powershell
cd "C:\Users\notebook\Downloads\allianza-wallet1"
$novoToken = "SEU_NOVO_TOKEN_AQUI"
git remote set-url origin "https://$novoToken@github.com/brunosmaach-spec/allianza-wallet-backend.git"
git push origin main
git remote set-url origin "https://github.com/brunosmaach-spec/allianza-wallet-backend.git"
```

---

### Opção 2: Verificar Proteções de Branch

O branch `main` pode estar protegido. Verifique:

1. Acesse: https://github.com/brunosmaach-spec/allianza-wallet-backend/settings/branches
2. Veja se há regras de proteção no branch `main`
3. Se houver, você pode:
   - **Desabilitar temporariamente** a proteção
   - **Criar um Pull Request** ao invés de push direto
   - **Adicionar seu usuário** como exceção

---

### Opção 3: Push Manual via GitHub Web Interface

Se o push continuar falhando:

1. Acesse: https://github.com/brunosmaach-spec/allianza-wallet-backend
2. Vá em: `backend/admin_routes.py` (ou crie o arquivo se não existir)
3. Clique em **"Edit"** (lápis)
4. Verifique/atualize a linha 28:
   ```python
   SITE_ADMIN_TOKEN = os.getenv('VITE_SITE_ADMIN_TOKEN', 'allianza_super_admin_2024_CdE25$$$')
   ```
5. **Commit:** "chore: atualizar admin_routes.py para usar VITE_SITE_ADMIN_TOKEN"

---

### Opção 4: Usar Pull Request (Se Branch Protegido)

```powershell
cd "C:\Users\notebook\Downloads\allianza-wallet1"
git checkout -b fix/admin-token-env-var
git push origin fix/admin-token-env-var
```

Depois, crie um Pull Request no GitHub:
- https://github.com/brunosmaach-spec/allianza-wallet-backend/compare/main...fix/admin-token-env-var

---

## 📝 Verificação Final

Após qualquer solução, verifique:
- URL: https://github.com/brunosmaach-spec/allianza-wallet-backend/blob/main/backend/admin_routes.py
- Linha 28 deve conter: `VITE_SITE_ADMIN_TOKEN`

---

## 🎯 Recomendação

**Use a Opção 1** (regenerar token com permissões completas). É a solução mais rápida e permite push direto no futuro.

