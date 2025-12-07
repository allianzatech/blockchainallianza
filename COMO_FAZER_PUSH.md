# 🚀 Como Fazer Push para GitHub

## Opção 1: Usar Personal Access Token (Recomendado)

### Passo 1: Gerar Token no GitHub

1. Acesse: https://github.com/settings/tokens
2. Clique em **"Generate new token"** → **"Generate new token (classic)"**
3. Dê um nome: `allianza-wallet-backend`
4. Selecione as permissões:
   - ✅ `repo` (todas as permissões de repositório)
5. Clique em **"Generate token"**
6. **COPIE O TOKEN** (você só verá uma vez!)

### Passo 2: Fazer Push

Quando o Git pedir credenciais:
- **Username:** `brunosmaach-spec` (ou seu username do GitHub)
- **Password:** Cole o **Personal Access Token** (não use sua senha normal!)

```powershell
cd "C:\Users\notebook\Downloads\allianza-wallet1"
git push origin main
```

---

## Opção 2: Configurar Token no URL (Mais Rápido)

Se você já tem o token, pode configurar diretamente:

```powershell
cd "C:\Users\notebook\Downloads\allianza-wallet1"
$token = "SEU_TOKEN_AQUI"
git remote set-url origin https://$token@github.com/brunosmaach-spec/allianza-wallet-backend.git
git push origin main
```

**⚠️ Atenção:** Isso salva o token no URL. Para remover depois:
```powershell
git remote set-url origin https://github.com/brunosmaach-spec/allianza-wallet-backend.git
```

---

## Opção 3: Usar Git Credential Manager (Windows)

O Windows pode salvar suas credenciais automaticamente:

```powershell
cd "C:\Users\notebook\Downloads\allianza-wallet1"
git push origin main
```

Quando pedir credenciais:
- Username: `brunosmaach-spec`
- Password: Seu **Personal Access Token**

O Windows salvará para próximas vezes.

---

## ✅ Verificar se Funcionou

Após o push, verifique:
- https://github.com/brunosmaach-spec/allianza-wallet-backend/commits/main
- O commit `chore: atualizar admin_routes.py para usar VITE_SITE_ADMIN_TOKEN` deve aparecer

---

## 🔧 Se Der Erro

### Erro: "Authentication failed"
- Verifique se o token está correto
- Verifique se o token tem permissão `repo`
- Tente gerar um novo token

### Erro: "Permission denied"
- Verifique se você tem acesso ao repositório `brunosmaach-spec/allianza-wallet-backend`
- Verifique se está usando o username correto

### Erro: "Updates were rejected"
```powershell
git pull origin main --rebase
git push origin main
```

