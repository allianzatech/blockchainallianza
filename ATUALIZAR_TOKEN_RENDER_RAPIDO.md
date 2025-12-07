# 🚀 Atualizar Token no Render - Método Rápido

## ⚡ Opção 1: Script Automatizado (Recomendado)

### Pré-requisitos
1. **Obter API Key do Render:**
   - Acesse: https://dashboard.render.com/account/api-keys
   - Clique em "New API Key"
   - Copie a chave gerada

2. **Instalar dependências:**
   ```bash
   pip install requests
   ```

### Executar o Script

**Windows PowerShell:**
```powershell
cd "C:\Users\notebook\Downloads\Allianza Blockchain"
$env:RENDER_API_KEY="sua_api_key_aqui"
python atualizar_token_render.py
```

**Linux/Mac:**
```bash
cd ~/Downloads/Allianza\ Blockchain
export RENDER_API_KEY="sua_api_key_aqui"
python3 atualizar_token_render.py
```

---

## ⚡ Opção 2: Atualização Manual (Mais Rápido)

### Passos Rápidos:

1. **Acesse:** https://dashboard.render.com
2. **Procure por:** `allianza-wallet-backend-1` ou `srv-d3qp4mu3jp1c738pams0`
3. **Clique no serviço**
4. **Vá em:** `Environment` (menu lateral)
5. **Procure por:** `VITE_SITE_ADMIN_TOKEN`
   - Se existir: Clique em editar (✏️) → Cole o novo valor → Salvar
   - Se não existir: Clique em "Add" → Key: `VITE_SITE_ADMIN_TOKEN` → Value: `vNFkVqGDZ4QOcrMLdEKPSx3upInRaTAstogl6Ch8HmYJyB5eb1wiWXf270z9jU` → Salvar
6. **Vá em:** `Manual Deploy` → `Deploy latest commit`
7. **Aguarde 2-5 minutos**

---

## ✅ Token para Copiar e Colar

```
vNFkVqGDZ4QOcrMLdEKPSx3upInRaTAstogl6Ch8HmYJyB5eb1wiWXf270z9jU
```

---

## 🔍 Verificação Rápida

Após o deploy, teste:
- Health: https://allianza-wallet-backend-1.onrender.com/health
- Admin: http://localhost:5173/admin (senha: `AllianzaAdmin2025!`)

---

**Tempo estimado:** 3-5 minutos (método manual)

