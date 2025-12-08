# 🚀 Quick Start - Allianza Blockchain

Guia rápido para começar a usar a Allianza Blockchain.

---

## 📋 Pré-requisitos

- Python 3.8+
- Node.js 14+ (para SDK JavaScript)
- Git

---

## 🔧 Instalação

### 1. Clone o repositório

```bash
git clone https://github.com/allianza/blockchain.git
cd blockchain
```

### 2. Instale dependências Python

```bash
pip install -r requirements.txt
```

### 3. Instale dependências JavaScript (opcional)

```bash
cd sdk/javascript
npm install
```

---

## 🏃 Iniciando a Blockchain

### Opção 1: RPC Server (Recomendado)

```bash
python rpc_server.py
```

O servidor RPC estará disponível em:
- **RPC Endpoint:** `http://localhost:8545`
- **Health Check:** `http://localhost:8545/health`
- **Network Info:** `http://localhost:8545/network`

### Opção 2: Blockchain Completa

```bash
python allianza_blockchain.py
```

---

## 💻 Usando o CLI

### Criar Wallet

```bash
python cli/allianza_cli.py wallet create
```

### Ver Saldo

```bash
python cli/allianza_cli.py wallet balance <endereço>
```

### Enviar Transação

```bash
python cli/allianza_cli.py transaction send <destino> <quantidade> --private-key <chave>
```

### Transação Cross-Chain

```bash
python cli/allianza_cli.py transaction cross-chain bitcoin <destino> <quantidade> --private-key <chave>
```

### Listar Validadores

```bash
python cli/allianza_cli.py validator list
```

---

## 📚 Usando os SDKs

### Python SDK

```python
from sdk.python.allianza_sdk import AllianzaWeb3, create_wallet

# Conectar à rede
web3 = AllianzaWeb3("http://localhost:8545")

# Criar wallet
wallet = create_wallet()
print(f"Endereço: {wallet.address}")

# Obter informações da rede
info = web3.get_network_info()
print(info)

# Enviar transação cross-chain
result = wallet.send_cross_chain("bitcoin", "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa", 0.001)
print(result)
```

### JavaScript SDK

```javascript
const { AllianzaSDK } = require('./sdk/javascript/allianza-sdk');

// Conectar à rede
const sdk = new AllianzaSDK('http://localhost:8545');

// Criar wallet
const wallet = sdk.createWallet();
console.log(`Endereço: ${wallet.address}`);

// Obter informações da rede
const info = await sdk.getNetworkInfo();
console.log(info);

// Enviar transação cross-chain
const result = await wallet.sendCrossChainTransaction(
    'bitcoin',
    '1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa',
    '0.001'
);
console.log(result);
```

---

## 🏛️ DAO (Governança)

### Criar Proposta

```python
from dao_system import get_dao_system, initialize_dao_system

dao = initialize_dao_system()

result = dao.create_proposal(
    proposer="0x...",
    title="Aumentar recompensa de bloco",
    description="Proposta para aumentar recompensa de 1.0 para 1.5 ALZ",
    action={"type": "update_block_reward", "value": 1.5},
    deposit=100.0
)

print(f"Proposta criada: {result['proposal_id']}")
```

### Votar

```python
from dao_system import VoteOption

dao.vote(
    proposal_id="...",
    voter="0x...",
    vote_option=VoteOption.YES,
    vote_weight=1000.0  # Baseado em stake
)
```

---

## ⚖️ Validadores

### Registrar Validador

```python
from validators_manager import initialize_validators_manager

validators = initialize_validators_manager()

result = validators.register_validator(
    address="0x...",
    staked_amount=10000.0,
    commission_rate=0.1
)

print(f"Validador registrado: {result['validator']['address']}")
```

### Stake

```python
validators.stake("0x...", 5000.0)
```

---

## 🌐 P2P Network

### Inicializar Rede

```python
from p2p_network import initialize_p2p_network, NodeType

p2p = initialize_p2p_network("node_1", NodeType.FULL_NODE)

# Adicionar bootstrap node
p2p.add_bootstrap_node("192.168.1.100", 30333)

# Obter informações
info = p2p.get_network_info()
print(info)
```

---

## 📖 Próximos Passos

1. **Leia a documentação completa:** `docs/API_REFERENCE.md`
2. **Explore exemplos:** `examples/`
3. **Participe da comunidade:** [Discord](https://discord.gg/allianza)
4. **Contribua:** [GitHub](https://github.com/allianza/blockchain)

---

## 🆘 Suporte

- **Documentação:** [docs.allianza.io](https://docs.allianza.io)
- **Discord:** [discord.gg/allianza](https://discord.gg/allianza)
- **GitHub Issues:** [github.com/allianza/blockchain/issues](https://github.com/allianza/blockchain/issues)

---

**Bem-vindo à Allianza Blockchain! 🚀**



















