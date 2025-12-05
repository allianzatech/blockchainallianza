# 📚 API Reference - Allianza Blockchain

Referência completa da API RPC da Allianza Blockchain.

---

## 🌐 Endpoints

### RPC Endpoint

```
POST http://localhost:8545
Content-Type: application/json
```

### Health Check

```
GET http://localhost:8545/health
```

### Network Info

```
GET http://localhost:8545/network
```

---

## 📡 Métodos RPC

### Métodos Ethereum Padrão

#### `eth_blockNumber`

Retorna o número do bloco mais recente.

**Request:**
```json
{
  "jsonrpc": "2.0",
  "method": "eth_blockNumber",
  "params": [],
  "id": 1
}
```

**Response:**
```json
{
  "jsonrpc": "2.0",
  "result": "0x1a2b3c",
  "id": 1
}
```

---

#### `eth_getBalance`

Retorna o saldo de uma conta.

**Request:**
```json
{
  "jsonrpc": "2.0",
  "method": "eth_getBalance",
  "params": ["0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb0", "latest"],
  "id": 1
}
```

**Response:**
```json
{
  "jsonrpc": "2.0",
  "result": "0x2386f26fc10000",
  "id": 1
}
```

---

#### `eth_sendTransaction`

Envia uma transação.

**Request:**
```json
{
  "jsonrpc": "2.0",
  "method": "eth_sendTransaction",
  "params": [{
    "from": "0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb0",
    "to": "0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb0",
    "value": "0x2386f26fc10000"
  }],
  "id": 1
}
```

**Response:**
```json
{
  "jsonrpc": "2.0",
  "result": "0x1234567890abcdef...",
  "id": 1
}
```

---

### Métodos Allianza Customizados

#### `allianza_getNetworkInfo`

Retorna informações da rede.

**Request:**
```json
{
  "jsonrpc": "2.0",
  "method": "allianza_getNetworkInfo",
  "params": [],
  "id": 1
}
```

**Response:**
```json
{
  "jsonrpc": "2.0",
  "result": {
    "chain_id": 12345,
    "chain_name": "Allianza Blockchain",
    "network_info": {
      "node_id": "rpc_node_1",
      "node_type": "rpc_node",
      "total_peers": 5,
      "connected_peers": 3
    },
    "validators_stats": {
      "total_validators": 10,
      "active_validators": 8,
      "total_staked": 1000000.0
    }
  },
  "id": 1
}
```

---

#### `allianza_getValidators`

Retorna lista de validadores.

**Request:**
```json
{
  "jsonrpc": "2.0",
  "method": "allianza_getValidators",
  "params": [],
  "id": 1
}
```

**Response:**
```json
{
  "jsonrpc": "2.0",
  "result": [
    {
      "address": "0x...",
      "staked_amount": 10000.0,
      "status": "active",
      "uptime": 99.5
    }
  ],
  "id": 1
}
```

---

#### `allianza_getValidatorInfo`

Retorna informações de um validador específico.

**Request:**
```json
{
  "jsonrpc": "2.0",
  "method": "allianza_getValidatorInfo",
  "params": ["0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb0"],
  "id": 1
}
```

**Response:**
```json
{
  "jsonrpc": "2.0",
  "result": {
    "address": "0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb0",
    "staked_amount": 10000.0,
    "status": "active",
    "commission_rate": 0.1,
    "total_rewards": 500.0,
    "uptime": 99.5,
    "slashing_count": 0
  },
  "id": 1
}
```

---

#### `allianza_sendCrossChain`

Envia transação cross-chain.

**Request:**
```json
{
  "jsonrpc": "2.0",
  "method": "allianza_sendCrossChain",
  "params": [
    "bitcoin",
    "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa",
    "0.001"
  ],
  "id": 1
}
```

**Response:**
```json
{
  "jsonrpc": "2.0",
  "result": {
    "success": true,
    "tx_hash": "0x1234567890abcdef...",
    "message": "Transação cross-chain iniciada"
  },
  "id": 1
}
```

---

#### `allianza_getCrossChainStatus`

Verifica status de transferência cross-chain.

**Request:**
```json
{
  "jsonrpc": "2.0",
  "method": "allianza_getCrossChainStatus",
  "params": ["0x1234567890abcdef..."],
  "id": 1
}
```

**Response:**
```json
{
  "jsonrpc": "2.0",
  "result": {
    "status": "pending",
    "tx_hash": "0x1234567890abcdef...",
    "source_chain": "allianza",
    "target_chain": "bitcoin"
  },
  "id": 1
}
```

---

#### `allianza_stake`

Faz stake de tokens.

**Request:**
```json
{
  "jsonrpc": "2.0",
  "method": "allianza_stake",
  "params": [
    "0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb0",
    "1000.0"
  ],
  "id": 1
}
```

**Response:**
```json
{
  "jsonrpc": "2.0",
  "result": {
    "success": true,
    "new_stake": 11000.0
  },
  "id": 1
}
```

---

#### `allianza_unstake`

Remove stake de tokens.

**Request:**
```json
{
  "jsonrpc": "2.0",
  "method": "allianza_unstake",
  "params": [
    "0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb0",
    "1000.0"
  ],
  "id": 1
}
```

**Response:**
```json
{
  "jsonrpc": "2.0",
  "result": {
    "success": true,
    "new_stake": 10000.0
  },
  "id": 1
}
```

---

## 🔐 Códigos de Erro

| Código | Descrição |
|--------|-----------|
| -32700 | Parse error |
| -32600 | Invalid Request |
| -32601 | Method not found |
| -32602 | Invalid params |
| -32603 | Internal error |

---

## 📖 Exemplos

### Python

```python
import requests

url = "http://localhost:8545"
headers = {"Content-Type": "application/json"}

# Obter informações da rede
payload = {
    "jsonrpc": "2.0",
    "method": "allianza_getNetworkInfo",
    "params": [],
    "id": 1
}

response = requests.post(url, json=payload, headers=headers)
print(response.json())
```

### JavaScript

```javascript
const fetch = require('node-fetch');

const url = 'http://localhost:8545';

// Obter informações da rede
const payload = {
  jsonrpc: '2.0',
  method: 'allianza_getNetworkInfo',
  params: [],
  id: 1
};

fetch(url, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify(payload)
})
  .then(res => res.json())
  .then(data => console.log(data));
```

---

**Para mais informações, consulte a documentação completa em [docs.allianza.io](https://docs.allianza.io)**








