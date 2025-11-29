# 🚰 Sistema Automático de Faucet

Sistema que verifica saldos e solicita fundos automaticamente a cada 12 horas para endereços configurados em testnet.

## 📋 Funcionalidades

- ✅ Verifica saldos automaticamente a cada 12 horas
- ✅ Solicita faucet quando saldo está abaixo do mínimo
- ✅ Respeita intervalo de 12 horas entre solicitações
- ✅ Suporta múltiplas chains: Bitcoin, Polygon, Ethereum, BSC
- ✅ Logs detalhados de todas as solicitações
- ✅ API REST para verificar status e forçar solicitações

## 🔧 Configuração

### 1. Configurar Endereços no `.env`

Adicione os endereços que deseja monitorar:

```env
# Bitcoin Testnet
BITCOIN_TESTNET_ADDRESS=mjQMvYHE5Bpqze4ifq6NLP9BthNJgxWRud

# Polygon Testnet (Amoy)
POLYGON_ADDRESS=0x86AE40869EB6ACb9477b42BfC9150c0A2Cc21f5E

# Ethereum Testnet (Sepolia)
ETHEREUM_ADDRESS=0x86AE40869EB6ACb9477b42BfC9150c0A2Cc21f5E

# BSC Testnet
BSC_ADDRESS=0x86AE40869EB6ACb9477b42BfC9150c0A2Cc21f5E
```

### 2. Saldos Mínimos

O sistema solicita faucet quando o saldo está abaixo de:

- **Bitcoin**: 0.0001 BTC
- **Polygon**: 0.01 MATIC
- **Ethereum**: 0.001 ETH
- **BSC**: 0.01 BNB

## 🚀 Como Funciona

### Inicialização Automática

O sistema inicia automaticamente quando o app Flask é iniciado:

```python
# Em allianza_blockchain.py
from auto_faucet_manager import AutoFaucetManager

auto_faucet = AutoFaucetManager()
auto_faucet.start_scheduler(interval_hours=12)
```

### Fluxo de Verificação

1. **A cada 12 horas**, o sistema:
   - Verifica saldo de cada endereço configurado
   - Compara com o saldo mínimo necessário
   - Se saldo < mínimo E passaram 12h desde última solicitação:
     - Solicita faucet de múltiplas fontes
     - Registra resultado no arquivo `faucet_last_requests.json`

2. **Respeita intervalo de 12 horas**:
   - Não solicita se última solicitação foi há menos de 12 horas
   - Mostra tempo restante até próxima solicitação disponível

## 📡 API Endpoints

### Verificar Status

```bash
GET /api/auto-faucet/status
```

Retorna:
- Endereços configurados
- Saldos atuais
- Status de cada endereço
- Histórico de últimas solicitações

### Forçar Verificação

```bash
POST /api/auto-faucet/check
```

Força verificação e solicitação para todos os endereços (respeitando intervalo de 12h)

### Solicitar para Chain Específica

```bash
POST /api/auto-faucet/request/<chain>
```

Exemplo:
```bash
POST /api/auto-faucet/request/bitcoin
POST /api/auto-faucet/request/polygon
```

## 🔍 Verificação Manual

Você pode executar manualmente:

```bash
python auto_faucet_manager.py
```

Ou importar no Python:

```python
from auto_faucet_manager import AutoFaucetManager

manager = AutoFaucetManager()
results = manager.check_all_addresses()
print(results)
```

## 📊 Logs e Histórico

### Arquivo de Histórico

O sistema salva histórico em `faucet_last_requests.json`:

```json
{
  "bitcoin:mjQMvYHE5Bpqze4ifq6NLP9BthNJgxWRud": {
    "timestamp": "2025-11-28T22:00:00",
    "success": true,
    "chain": "bitcoin",
    "address": "mjQMvYHE5Bpqze4ifq6NLP9BthNJgxWRud"
  }
}
```

### Logs no Console

O sistema imprime logs detalhados:

```
🚰 VERIFICAÇÃO AUTOMÁTICA DE FAUCETS - 2025-11-28 22:00:00
🔍 Verificando BITCOIN - mjQMvYHE5Bpqze4ifq6NLP9BthNJgxWRud
💰 Saldo atual: 0.00005 BTC
📊 Mínimo necessário: 0.0001 BTC
🚰 Saldo baixo! Solicitando faucet...
✅ Solicitação enviada para Bitcoin Testnet Faucet
```

## 🛠️ Faucets Suportados

### Bitcoin Testnet
- Bitcoin Testnet Faucet (https://bitcoinfaucet.uo1.net/)
- Mempool Faucet (https://testnet-faucet.mempool.co/)

### Polygon Testnet
- Polygon Faucet (https://faucet.polygon.technology/)
- QuickNode Polygon Faucet

### Ethereum Sepolia
- Sepolia Faucet (https://sepoliafaucet.com/)

### BSC Testnet
- BSC Testnet Faucet (https://testnet.binance.org/faucet-smart)

## ⚙️ Personalização

### Alterar Intervalo

No código, altere o intervalo:

```python
# Em allianza_blockchain.py
auto_faucet.start_scheduler(interval_hours=12)  # Altere para 6, 24, etc.
```

### Alterar Saldos Mínimos

Em `auto_faucet_manager.py`:

```python
self.min_balance_threshold = {
    "bitcoin": 0.0001,   # Altere aqui
    "polygon": 0.01,     # Altere aqui
    "ethereum": 0.001,   # Altere aqui
    "bsc": 0.01          # Altere aqui
}
```

### Adicionar Novos Faucets

Em `auto_faucet_manager.py`, adicione na lista `self.faucet_apis`:

```python
"bitcoin": [
    {
        "name": "Novo Faucet",
        "url": "https://novo-faucet.com/",
        "method": "POST",
        "params": {"address": "{address}"},
        "headers": {"Content-Type": "application/json"}
    }
]
```

## 🔒 Segurança

- ✅ Não armazena chaves privadas
- ✅ Apenas lê endereços do `.env`
- ✅ Respeita rate limits dos faucets
- ✅ Logs não contêm informações sensíveis

## 📝 Notas

- O sistema funciona em **thread separada** (não bloqueia o app Flask)
- Se um faucet falhar, tenta o próximo automaticamente
- Se todos os faucets falharem, registra erro mas continua funcionando
- O sistema verifica saldos via APIs públicas (Blockstream, Polygonscan, etc.)

## 🐛 Troubleshooting

### Sistema não está verificando

1. Verifique se os endereços estão no `.env`
2. Verifique logs do console ao iniciar o app
3. Verifique se a biblioteca `schedule` está instalada: `pip install schedule`

### Faucets não estão funcionando

1. Alguns faucets podem estar temporariamente indisponíveis
2. Verifique se os endereços são válidos para testnet
3. Alguns faucets podem ter rate limits mais restritivos

### Saldo não está sendo detectado

1. Verifique se o endereço está correto
2. Verifique se há transações confirmadas no explorer
3. Algumas APIs podem ter delay na atualização

## 📞 Suporte

Para problemas ou dúvidas, verifique:
- Logs do console
- Arquivo `faucet_last_requests.json`
- Status via API: `GET /api/auto-faucet/status`

