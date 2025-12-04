# 🔄 Solução para Sleep Mode do Render

## 📋 Problema

O Render (plano gratuito) coloca serviços em **"sleep mode"** após **15 minutos de inatividade**. Quando isso acontece:

1. ⏱️ **Primeira requisição** após sleep leva **30-60 segundos** para "acordar" o serviço
2. 🖥️ **Tela de carregamento** do Render aparece durante esse tempo
3. ⚠️ **Usuário vê** mensagens como "SERVIÇO SENDO ATIVADO" e "ALOCANDO RECURSOS"

## ✅ Soluções Implementadas

### 1. Otimização do Gunicorn

**Antes:**
```bash
gunicorn -w 4 -b 0.0.0.0:$PORT --timeout 120 wsgi:application
```

**Depois:**
```bash
gunicorn -w 2 -b 0.0.0.0:$PORT --timeout 180 --keep-alive 5 --preload wsgi:application
```

**Melhorias:**
- ✅ **`-w 2`**: Reduz workers de 4 para 2 (economiza memória, inicia mais rápido)
- ✅ **`--timeout 180`**: Aumenta timeout de 120s para 180s (mais tempo para inicializar)
- ✅ **`--keep-alive 5`**: Mantém conexões HTTP abertas por 5 segundos (reduz latência)
- ✅ **`--preload`**: Carrega o app antes de iniciar workers (inicialização mais rápida)

### 2. Health Check Otimizado

**Configuração no `render.yaml`:**
```yaml
healthCheckPath: /health
healthCheckGracePeriod: 120  # Aumentado de 60 para 120 segundos
```

**Por quê:**
- ✅ Dá mais tempo para o app inicializar antes do health check falhar
- ✅ Evita que o Render marque o serviço como "unhealthy" durante inicialização

### 3. Variáveis de Ambiente

**Adicionado:**
```yaml
- key: PYTHONUNBUFFERED
  value: "1"
```

**Por quê:**
- ✅ Logs aparecem imediatamente (sem buffer)
- ✅ Facilita debug durante inicialização

## 🎯 Resultados Esperados

### Antes:
- ⏱️ Tempo de inicialização: **30-60 segundos** após sleep
- 🖥️ Tela de carregamento: **Sempre aparece** após 15min de inatividade

### Depois:
- ⏱️ Tempo de inicialização: **15-30 segundos** (reduzido pela metade)
- 🖥️ Tela de carregamento: **Ainda aparece**, mas por menos tempo

## ⚠️ Limitações do Plano Gratuito

**O Render Free Tier tem limitações:**
- ❌ **Não pode desabilitar** sleep mode (é uma limitação do plano gratuito)
- ❌ **15 minutos** de inatividade = sleep automático
- ❌ **Primeira requisição** sempre leva tempo para "acordar"

## 💡 Soluções Alternativas

### Opção 1: Upgrade para Plano Pago
- 💰 **$7/mês** (Starter Plan)
- ✅ **Sem sleep mode**
- ✅ **Sempre online**
- ✅ **Melhor performance**

### Opção 2: Ping Automático (Keep-Alive)
Criar um serviço externo que faz ping a cada 10 minutos:

```python
# keep_alive.py (executar em outro servidor/cron)
import requests
import time

while True:
    try:
        requests.get("https://testnet.allianza.tech/health", timeout=5)
        print("✅ Ping enviado")
    except:
        print("⚠️ Erro ao enviar ping")
    time.sleep(600)  # 10 minutos
```

### Opção 3: Mensagem Amigável na UI
Adicionar uma mensagem na página inicial explicando o delay:

```html
<div id="render-loading" style="display: none;">
    <p>⏳ Serviço sendo ativado... Isso leva cerca de 30 segundos após inatividade.</p>
</div>
```

## 📊 Monitoramento

### Verificar Status:
```bash
curl https://testnet.allianza.tech/health
```

### Verificar Logs no Render:
1. Acesse o dashboard do Render
2. Vá em **"Logs"**
3. Procure por mensagens de inicialização

## 🔍 Como Identificar se Está em Sleep Mode

**Sinais:**
- ⏱️ Primeira requisição leva 30-60 segundos
- 🖥️ Tela de carregamento do Render aparece
- 📝 Logs mostram "SERVIÇO SENDO ATIVADO"

**Soluções Imediatas:**
- ⏳ **Aguarde 30-60 segundos** na primeira requisição
- 🔄 **Recarregue a página** após o carregamento inicial
- ✅ **Próximas requisições** serão instantâneas (serviço já está ativo)

## 📝 Notas Finais

- ✅ **Configurações otimizadas** foram aplicadas
- ✅ **Health check** está funcionando corretamente
- ⚠️ **Sleep mode** é uma limitação do plano gratuito do Render
- 💡 **Upgrade para plano pago** elimina completamente o problema

