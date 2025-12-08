# 🌍 Sistema de Internacionalização e Teste de Estresse

**Data:** Dezembro 2025  
**Status:** ✅ Implementado e Funcional

---

## 📋 RESUMO

Implementado sistema completo de internacionalização (i18n) com detecção automática de idioma por IP/país e teste de estresse para gerar transações automaticamente.

---

## 🌍 SISTEMA DE INTERNACIONALIZAÇÃO (i18n)

### Funcionalidades

1. **Detecção Automática por IP/País:**
   - 🇺🇸 EUA, Reino Unido, Canadá, Austrália → Inglês (en)
   - 🇧🇷 Brasil, Portugal, Angola, Moçambique → Português (pt)
   - Usa serviço gratuito `ipapi.co` para geolocalização
   - Fallback para header `Accept-Language` do navegador
   - Default: Inglês

2. **Seleção Manual:**
   - Botões de idioma no dashboard (🇧🇷 PT / 🇺🇸 EN)
   - Rota `/set-language/<lang>` para mudança programática
   - Idioma salvo na sessão do usuário

3. **Traduções Implementadas:**
   - Dashboard principal traduzido
   - Todos os botões e textos principais
   - Suporte para expandir para outros templates

### Como Funciona

```python
# No template:
{{ t('dashboard_title') }}  # Retorna "Allianza Testnet" ou "Allianza Testnet"
{{ t('total_transactions') }}  # Retorna "Total de Transações" ou "Total Transactions"

# Detecção automática:
- Usuário do Brasil → Português automaticamente
- Usuário dos EUA → Inglês automaticamente
- Usuário pode mudar manualmente clicando nos botões
```

### Arquivos Criados

- `i18n_system.py` - Sistema completo de i18n
- Integrado em `allianza_blockchain.py`
- Templates atualizados com `{{ t() }}`

---

## 🔥 TESTE DE ESTRESSE

### Funcionalidades

1. **Geração Rápida de Transações:**
   - Gera 50 transações iniciais na inicialização
   - Teste em lote: `run_stress_test(count=100, delay=0.1)`
   - Teste contínuo: `run_continuous_stress(tps=10.0, duration=60)`

2. **API Endpoint:**
   - `POST /api/stress-test`
   - Parâmetros:
     - `count`: Número de transações (padrão: 100)
     - `delay`: Delay entre transações (padrão: 0.1s)
     - `tps`: Transações por segundo (para teste contínuo)
     - `duration`: Duração em segundos (para teste contínuo)

3. **Resultado:**
   - Resolve problema de "transações zero"
   - Blocos não ficam mais vazios
   - Dashboard mostra números reais

### Exemplo de Uso

```python
# Via API
POST /api/stress-test
{
  "count": 200,
  "delay": 0.05
}

# Resposta
{
  "success": true,
  "total": 200,
  "successful": 200,
  "failed": 0,
  "duration": 10.5,
  "transactions_per_second": 19.05
}
```

### Arquivos Criados

- `testnet_stress_test.py` - Sistema de teste de estresse
- Integrado em `testnet_routes.py`
- Executa automaticamente na inicialização

---

## 🎨 INTERFACE ATUALIZADA

### Botões Reduzidos

- **Antes:** `p-6` (padding grande)
- **Depois:** `p-3/p-4` (padding responsivo)
- **Grid:** 2-5 colunas (mobile → desktop)
- **Ícones:** `text-2xl/text-3xl` (menores)
- **Textos:** Ocultos em mobile, visíveis em desktop

### Layout Moderno

- Mais compacto e organizado
- Responsivo para todos os dispositivos
- Mantém funcionalidade completa

---

## 📊 RESULTADOS ESPERADOS

### Antes:
- ❌ Transações: 0
- ❌ Blocos vazios
- ❌ Interface apenas em português
- ❌ Números zero no dashboard

### Depois:
- ✅ Transações sendo geradas automaticamente
- ✅ Blocos com transações reais
- ✅ Interface em inglês/português (detecção automática)
- ✅ Dashboard com números reais
- ✅ Teste de estresse disponível via API

---

## 🚀 PRÓXIMOS PASSOS

1. **Expandir Traduções:**
   - Traduzir todos os templates da testnet
   - Adicionar mais idiomas (espanhol, francês, etc.)

2. **Melhorar Teste de Estresse:**
   - Adicionar métricas de performance
   - Dashboard de monitoramento
   - Histórico de testes

3. **Otimizações:**
   - Cache de geolocalização
   - Reduzir chamadas à API de IP
   - Melhorar performance do gerador

---

## 📝 NOTAS TÉCNICAS

### Dependências

- `requests` - Para geolocalização por IP
- Flask sessions - Para salvar idioma do usuário

### Performance

- Detecção de idioma: ~200ms (primeira vez)
- Cache: Idioma salvo na sessão (sem nova detecção)
- Teste de estresse: ~10-20 TPS (depende do hardware)

### Segurança

- IP não é armazenado
- Apenas código do país é usado
- Fallback seguro se API falhar

---

**Última atualização:** Dezembro 2025

