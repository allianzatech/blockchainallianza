# 💳 OPÇÕES PARA RENDER - PAGAMENTO

## ⚠️ Situação
O Render exige cartão mesmo para usar o **free tier**, mas **NÃO COBRA NADA** se você ficar dentro dos limites gratuitos.

## ✅ OPÇÃO 1: Adicionar Cartão (RECOMENDADO)

### Por que é seguro:
- ✅ Render só faz **autorização de $1 USD** (não é cobrança real)
- ✅ **NÃO cobra nada** se você ficar no free tier
- ✅ Você pode **remover o cartão** depois se quiser
- ✅ Free tier inclui:
  - 750 horas/mês de serviço
  - 100 GB/mês de bandwidth
  - 500 minutos/mês de build

### Como adicionar:
1. Clique em **"Add Card"**
2. Preencha os dados do cartão
3. Confirme
4. O Blueprint será criado automaticamente

### Monitorar uso:
- Vá em **Billing** no dashboard
- Configure alertas se quiser
- Você pode suspender serviços a qualquer momento

---

## 🔧 OPÇÃO 2: Criar Serviço Manualmente (SEM BLUEPRINT)

Se preferir **NÃO adicionar cartão**, você pode criar o serviço manualmente:

### Passo 1: Cancelar o Blueprint
- Clique em **"Cancel"** na tela de pagamento

### Passo 2: Criar Web Service Manualmente
1. No Render Dashboard, clique em **"New +"** → **"Web Service"**
2. Conecte seu repositório: `dieisonmaach-lang/allianzablockchain`
3. Configure manualmente:

   **Name:** `allianza-blockchain`
   
   **Environment:** `Python 3`
   
   **Region:** `Oregon (US West)` (ou mais próximo)
   
   **Branch:** `main`
   
   **Root Directory:** (deixe vazio)
   
   **Build Command:**
   ```
   pip install --upgrade pip && pip install -r requirements.txt
   ```
   
   **Start Command:**
   ```
   gunicorn -w 4 -b 0.0.0.0:$PORT --timeout 120 wsgi:application
   ```
   
   **Instance Type:** `Free` (0.1 CPU, 512 MB)

### Passo 3: Adicionar Variáveis de Ambiente
Vá em **Environment** e adicione:

```
FLASK_ENV=production
FLASK_DEBUG=False
SECRET_KEY=<gere uma chave>
```

**Para gerar SECRET_KEY:**
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

### Passo 4: Health Check
Vá em **Settings → Health Checks**:
- **Health Check Path:** `/health`

### Passo 5: Criar Serviço
- Clique em **"Create Web Service"**
- Aguarde o deploy

---

## 📊 COMPARAÇÃO

| Aspecto | Opção 1 (Cartão) | Opção 2 (Manual) |
|---------|------------------|------------------|
| Facilidade | ⭐⭐⭐⭐⭐ Muito fácil | ⭐⭐⭐ Configuração manual |
| Blueprint | ✅ Usa render.yaml | ❌ Não usa |
| Atualizações | ✅ Automáticas | ⚠️ Manuais |
| Free Tier | ✅ Disponível | ✅ Disponível |
| Custo | 💰 $0 (dentro dos limites) | 💰 $0 (dentro dos limites) |

---

## 🎯 RECOMENDAÇÃO

**Use a Opção 1 (adicionar cartão)** porque:
- É mais fácil e rápido
- Usa o `render.yaml` (atualizações automáticas)
- Não cobra nada no free tier
- Você pode remover o cartão depois

**Use a Opção 2** apenas se:
- Não quiser adicionar cartão de forma alguma
- Preferir controle total manual

---

## ⚠️ IMPORTANTE

Mesmo com cartão, o Render **NÃO COBRA** se você:
- Usar menos de 750 horas/mês
- Usar menos de 100 GB/mês de bandwidth
- Usar menos de 500 minutos/mês de build

Você pode **suspender serviços** a qualquer momento para economizar horas gratuitas!

