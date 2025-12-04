# 🔄 Guia de Keep-Alive para Allianza Testnet

## 📋 Problema

O Render (plano gratuito) coloca serviços em **sleep mode** após **15 minutos de inatividade**. Este guia mostra como manter o serviço sempre ativo fazendo ping a cada **14 minutos**.

## ✅ Soluções Disponíveis

### Opção 1: Script Python Local (Recomendado para Testes)

**Arquivo:** `keep_alive.py`

**Como usar:**
```bash
# Instalar dependências
pip install requests python-dotenv

# Executar
python keep_alive.py
```

**Vantagens:**
- ✅ Simples de usar
- ✅ Logs detalhados
- ✅ Estatísticas em tempo real

**Desvantagens:**
- ❌ Precisa estar rodando 24/7 no seu computador
- ❌ Para quando você desliga o PC

---

### Opção 2: GitHub Actions (Recomendado - Gratuito)

**Arquivo:** `.github/workflows/keep_alive_github_actions.yml`

**Como configurar:**

1. **Criar diretório:**
   ```bash
   mkdir -p .github/workflows
   ```

2. **Copiar arquivo:**
   ```bash
   cp keep_alive_github_actions.yml .github/workflows/keep-alive.yml
   ```

3. **Commit e push:**
   ```bash
   git add .github/workflows/keep-alive.yml
   git commit -m "Adicionar GitHub Actions para keep-alive"
   git push
   ```

4. **Ativar no GitHub:**
   - Vá em **Settings → Actions → General**
   - Ative **"Allow all actions and reusable workflows"**
   - Salve

**Vantagens:**
- ✅ **100% gratuito**
- ✅ **Roda 24/7** automaticamente
- ✅ **Não precisa manter seu PC ligado**
- ✅ **Executa a cada 14 minutos** automaticamente

**Desvantagens:**
- ⚠️ GitHub Actions tem limite de 2000 minutos/mês (mas ping leva <1 segundo, então é suficiente)

---

### Opção 3: UptimeRobot (Recomendado - Gratuito)

**Como configurar:**

1. **Criar conta:** https://uptimerobot.com (gratuito)

2. **Adicionar Monitor:**
   - **Monitor Type:** HTTP(s)
   - **Friendly Name:** Allianza Testnet Keep-Alive
   - **URL:** `https://testnet.allianza.tech/health`
   - **Monitoring Interval:** 5 minutos (máximo no plano gratuito)
   - **Alert Contacts:** (opcional)

3. **Salvar**

**Vantagens:**
- ✅ **100% gratuito** (até 50 monitors)
- ✅ **Roda 24/7** automaticamente
- ✅ **Interface web** para monitoramento
- ✅ **Alertas** se o serviço cair

**Desvantagens:**
- ⚠️ Intervalo mínimo é 5 minutos (não 14 minutos, mas ainda funciona)

---

### Opção 4: PythonAnywhere (Gratuito)

**Como configurar:**

1. **Criar conta:** https://www.pythonanywhere.com (gratuito)

2. **Upload do script:**
   - Faça upload de `keep_alive_simple.py`

3. **Configurar Scheduled Task:**
   - Vá em **Tasks**
   - Clique em **"Create a new scheduled task"**
   - **Command:** `python3.10 /home/seu_usuario/keep_alive_simple.py`
   - **Hour:** `*` (todos)
   - **Minute:** `*/14` (a cada 14 minutos)

**Vantagens:**
- ✅ **Gratuito** (com limitações)
- ✅ **Roda automaticamente**
- ✅ **Interface web**

**Desvantagens:**
- ⚠️ Plano gratuito tem limitações de CPU

---

### Opção 5: Render Cron Job (Pago)

Se você tiver plano pago no Render, pode criar um **Cron Job**:

**Arquivo:** `render.yaml` (adicionar):
```yaml
services:
  - type: cron
    name: keep-alive
    schedule: "*/14 * * * *"  # A cada 14 minutos
    buildCommand: pip install requests
    startCommand: python keep_alive_simple.py
```

**Vantagens:**
- ✅ Integrado com Render
- ✅ Mesma infraestrutura

**Desvantagens:**
- ❌ Requer plano pago

---

## 🎯 Recomendação

**Para uso gratuito e automático:**
1. **GitHub Actions** (melhor opção - totalmente automático)
2. **UptimeRobot** (segunda melhor - interface web)

**Para testes locais:**
- **Script Python** (`keep_alive.py`)

---

## 📊 Como Verificar se Está Funcionando

### 1. Verificar Logs do Render
- Acesse o dashboard do Render
- Vá em **"Logs"**
- Procure por requisições ao `/health` a cada 14 minutos

### 2. Testar Manualmente
```bash
curl https://testnet.allianza.tech/health
```

### 3. Monitorar Uptime
- Use UptimeRobot ou similar
- Configure alertas se o serviço não responder

---

## ⚙️ Configuração Avançada

### Variáveis de Ambiente

Crie um arquivo `.env`:
```env
TESTNET_URL=https://testnet.allianza.tech
INTERVAL_MINUTES=14
```

### Personalizar Intervalo

No script `keep_alive.py`, altere:
```python
INTERVAL_MINUTES = 14  # Mude para o valor desejado (máximo 14 para evitar sleep)
```

---

## 🚨 Troubleshooting

### Problema: Script para de funcionar
**Solução:** Verifique se o processo está rodando:
```bash
ps aux | grep keep_alive
```

### Problema: GitHub Actions não executa
**Solução:** 
1. Verifique se Actions estão ativadas no repositório
2. Verifique se o arquivo está em `.github/workflows/`
3. Veja os logs em **Actions → Keep-Alive**

### Problema: UptimeRobot não detecta
**Solução:**
1. Verifique se a URL está correta
2. Teste manualmente: `curl https://testnet.allianza.tech/health`
3. Verifique se o monitor está ativo

---

## 📝 Notas Importantes

- ⏰ **Intervalo ideal:** 14 minutos (antes dos 15min de sleep)
- 🔄 **Primeira requisição** após sleep ainda pode levar 30-60 segundos
- 💰 **Plano pago** do Render elimina completamente o problema
- ✅ **Keep-alive** reduz drasticamente a frequência de sleep mode

---

## 🎉 Resultado Esperado

Com o keep-alive funcionando:
- ✅ Serviço **sempre ativo** (sem sleep mode)
- ✅ **Resposta instantânea** nas requisições
- ✅ **Sem tela de carregamento** do Render
- ✅ **Melhor experiência** para usuários

