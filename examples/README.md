# 💡 Code Examples - Allianza Blockchain

This directory contains practical code examples demonstrating how to use Allianza Blockchain.

## 📋 Available Examples

### Basic Examples

#### 1. Create Wallet and Generate Address

```python
from allianza_blockchain import AllianzaBlockchain

# Initialize blockchain
blockchain = AllianzaBlockchain()

# Create a new wallet
address, private_key = blockchain.create_wallet()

print(f"Address: {address}")
print(f"Private Key: {private_key}")
```

#### 2. Create Transaction

```python
from allianza_blockchain import AllianzaBlockchain

blockchain = AllianzaBlockchain()

# Create transaction
transaction = blockchain.create_transaction(
    sender="ALZ1SenderAddress...",
    receiver="ALZ1ReceiverAddress...",
    amount=1000.0,
    private_key="your_private_key_here",
    is_public=True,
    network="allianza"
)

print(f"Transaction ID: {transaction['id']}")
print(f"Status: {transaction.get('status', 'pending')}")
```

#### 3. Query Transaction

```python
from allianza_blockchain import AllianzaBlockchain

blockchain = AllianzaBlockchain()

# Get transaction by hash
tx_hash = "your_transaction_hash"
transaction = blockchain.get_transaction(tx_hash)

if transaction:
    print(f"From: {transaction['sender']}")
    print(f"To: {transaction['receiver']}")
    print(f"Amount: {transaction['amount']} ALZ")
else:
    print("Transaction not found")
```

### QRS-3 (Post-Quantum Cryptography) Examples

#### 4. Generate QRS-3 Key Pair

```python
from core.crypto.pqc_crypto import MLDSAKeyPair, SPHINCSPlusKeyPair

# Generate ML-DSA key pair
mldsa = MLDSAKeyPair()
public_key = mldsa.get_public_key()

print(f"ML-DSA Public Key: {public_key}")
```

#### 5. Sign and Verify with QRS-3

```python
from core.crypto.pqc_crypto import MLDSAKeyPair

# Generate key pair
mldsa = MLDSAKeyPair()

# Message to sign
message = b"Hello, Allianza Blockchain!"

# Sign message
signature = mldsa.sign(message)

# Verify signature
is_valid = mldsa.verify(message, signature)

print(f"Signature valid: {is_valid}")
```

### Interoperability Examples

#### 6. Cross-Chain Transfer

```python
from core.interoperability.bridge_free_interop import BridgeFreeInterop

interop = BridgeFreeInterop()

# Transfer from Bitcoin to Ethereum
result = interop.transfer_cross_chain(
    source_chain="bitcoin",
    target_chain="ethereum",
    amount=0.01,
    recipient="0x...",
    source_private_key="your_btc_private_key"
)

print(f"Transfer ID: {result['transfer_id']}")
print(f"Status: {result['status']}")
```

#### 7. Create Proof-of-Lock

```python
from core.interoperability.proof_of_lock import ProofOfLock

proof_lock = ProofOfLock()

# Create lock proof
proof = proof_lock.create_lock_proof(
    source_chain="polygon",
    tx_hash="0x...",
    amount=100.0,
    token_symbol="MATIC",
    target_chain="ethereum",
    recipient_address="0x..."
)

print(f"Proof ID: {proof['proof_id']}")
print(f"Lock Hash: {proof['lock_hash']}")
```

### Testnet Examples

#### 8. Request Tokens from Faucet

```python
import requests

# Testnet faucet endpoint
url = "https://testnet.allianza.tech/api/faucet/request"

# Your testnet address
data = {
    "address": "ALZ1YourTestnetAddress..."
}

response = requests.post(url, json=data)
result = response.json()

if result.get("success"):
    print(f"✅ {result['amount']} ALZ sent!")
    print(f"Transaction: {result['tx_hash']}")
else:
    print(f"❌ Error: {result.get('error')}")
```

#### 9. Query Testnet Explorer

```python
import requests

# Get recent transactions
url = "https://testnet.allianza.tech/api/transactions"
response = requests.get(url)
transactions = response.json()

for tx in transactions[:5]:
    print(f"TX: {tx['id'][:20]}... | {tx['amount']} ALZ")
```

## 🔗 More Examples

- **SDK Examples**: See [sdk/](sdk/) directory
- **Test Scripts**: See [tests/public/](tests/public/) directory
- **API Reference**: See [docs/API_REFERENCE.md](docs/API_REFERENCE.md)

## 📚 Documentation

- [Quick Start Guide](../docs/QUICK_START.md)
- [API Reference](../docs/API_REFERENCE.md)
- [Architecture](../docs/ARCHITECTURE.md)

---

**Note**: All examples use testnet. Never use real private keys or funds in examples.

