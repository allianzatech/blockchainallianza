# 📚 API Reference - Allianza Blockchain

Complete reference for Allianza Blockchain RPC API.

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

## 📡 RPC Methods

### Standard Ethereum Methods

#### `eth_blockNumber`

Returns the number of the most recent block.

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

Returns the balance of an account.

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

Sends a transaction.

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

### Allianza Custom Methods

#### `allianza_getNetworkInfo`

Returns network information.

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

Returns list of validators.

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

Returns information about a specific validator.

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

Sends a cross-chain transaction.

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
    "message": "Cross-chain transaction initiated"
  },
  "id": 1
}
```

---

#### `allianza_getCrossChainStatus`

Checks the status of a cross-chain transfer.

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

Stakes tokens.

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

Removes staked tokens.

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

## 🔐 Error Codes

| Code | Description |
|------|-------------|
| -32700 | Parse error |
| -32600 | Invalid Request |
| -32601 | Method not found |
| -32602 | Invalid params |
| -32603 | Internal error |

---

## 📖 Examples

### Python

```python
import requests

url = "http://localhost:8545"
headers = {"Content-Type": "application/json"}

# Get network information
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

// Get network information
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

**For more information, see the complete documentation at [docs.allianza.io](https://docs.allianza.io)**
