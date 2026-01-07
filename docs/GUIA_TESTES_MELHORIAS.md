# 🧪 Guia de Testes - Melhorias de Interoperabilidade

**Data:** 2026-01-03  
**Versão:** 1.0

---

## 📋 Índice

1. [Pré-requisitos](#pré-requisitos)
2. [Configuração Inicial](#configuração-inicial)
3. [Testes no CMD/Terminal](#testes-no-cmdterminal)
4. [Testes no Localhost](#testes-no-localhost)
5. [Verificação no Explorer](#verificação-no-explorer)
6. [Troubleshooting](#troubleshooting)

---

## 🔧 Pré-requisitos

### Software Necessário

- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)
- Conta em testnet (Polygon Amoy ou Ethereum Sepolia)
- Tokens de teste (MATIC ou ETH)

### Dependências Python

```bash
pip install web3 py-solc-x python-dotenv
```

### Contratos Deployados

Os contratos já estão deployados nas seguintes testnets:

- **Polygon Amoy:** `0x0b5AB34be0f5734161E608885e139AE2b72a07AE`
- **Ethereum Sepolia:** `0x00077a4bF0d73f398C808fe8e5e9763Bf59915fb`

---

## ⚙️ Configuração Inicial

### 1. Criar/Editar arquivo `.env`

Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis:

```env
# RPC URLs
POLYGON_RPC_URL=https://rpc-amoy.polygon.technology
ETH_RPC_URL=https://sepolia.infura.io/v3/YOUR_INFURA_KEY

# Private Keys (OBRIGATÓRIO - Use uma conta de teste!)
POLYGON_PRIVATE_KEY=0xSEU_PRIVATE_KEY_AQUI
ETH_PRIVATE_KEY=0xSEU_PRIVATE_KEY_AQUI

# Contract Addresses (já configurados)
POLYGON_COMMITMENT_CONTRACT=0x0b5AB34be0f5734161E608885e139AE2b72a07AE
ETH_COMMITMENT_CONTRACT=0x00077a4bF0d73f398C808fe8e5e9763Bf59915fb
```

### 2. Obter Tokens de Teste

#### Polygon Amoy
- Faucet: https://faucet.polygon.technology/
- Adicione a rede Amoy no MetaMask
- Solicite tokens MATIC

#### Ethereum Sepolia
- Faucet: https://sepoliafaucet.com/
- Adicione a rede Sepolia no MetaMask
- Solicite tokens ETH

---

## 💻 Testes no CMD/Terminal

### Opção 1: Script de Teste Automatizado

O script `test_commitment_improvements.py` executa todos os testes automaticamente.

#### Executar todos os testes:

```bash
# Windows (CMD)
python test_commitment_improvements.py

# Windows (PowerShell)
python test_commitment_improvements.py

# Linux/Mac
python3 test_commitment_improvements.py
```

#### Executar testes específicos:

```bash
# Apenas testes do CommitmentManager
python test_commitment_improvements.py --test commitment --chain polygon

# Apenas testes de integração
python test_commitment_improvements.py --test integration --chain polygon

# Teste completo
python test_commitment_improvements.py --test full --chain polygon
```

### Opção 2: Teste Manual via Python Interativo

#### 1. Testar Conexão

```python
# Abrir Python
python

# No Python:
import os
from dotenv import load_dotenv
from commercial_repo.adapters.commitment_integration import CommitmentManager

load_dotenv()

# Configurar
rpc_url = "https://rpc-amoy.polygon.technology"
private_key = os.getenv('POLYGON_PRIVATE_KEY')
contract_address = "0x0b5AB34be0f5734161E608885e139AE2b72a07AE"

# Inicializar
manager = CommitmentManager(
    rpc_url=rpc_url,
    private_key=private_key,
    commitment_contract_address=contract_address
)

# Testar conexão
from web3 import Web3
print(f"Conectado: {manager.w3.is_connected()}")
print(f"Block atual: {manager.w3.eth.block_number}")
```

#### 2. Criar Commitment

```python
# Criar commitment
result = manager.create_commitment(
    target_chain="bitcoin",
    target_recipient="0x0000000000000000000000000000000000000000",
    amount=1000000000000000,  # 0.001 ETH em wei
    nonce=None
)

print(f"Sucesso: {result.get('success')}")
print(f"Commitment Hash: {result.get('commitment_hash')}")
print(f"UChainID: {result.get('uchain_id')}")
print(f"TX Hash: {result.get('tx_hash')}")
```

#### 3. Consultar Commitment

```python
# Consultar commitment (use o hash do passo anterior)
commitment_hash = result.get('commitment_hash')
commitment_data = manager.get_commitment(commitment_hash)

print(f"Commitment: {commitment_data.get('commitment')}")
```

### Opção 3: Teste de Integração Completa

```python
# Teste completo de transferência cross-chain
from commercial_repo.adapters.real_cross_chain_bridge import RealCrossChainBridge
import os
from dotenv import load_dotenv

load_dotenv()

# Inicializar bridge
bridge = RealCrossChainBridge()

# Executar transferência
result = bridge.real_cross_chain_transfer(
    source_chain="polygon",
    target_chain="bitcoin",
    amount=0.001,
    token_symbol="MATIC",
    recipient="bc1qxy2kgdygjrsqtzq2n0yrf2493p83kkfjhx0wlh",
    source_private_key=os.getenv('POLYGON_PRIVATE_KEY')
)

print(f"Sucesso: {result.get('success')}")
print(f"Commitment: {result.get('commitment')}")
print(f"Source TX: {result.get('source_transaction', {}).get('tx_hash')}")
```

---

## 🌐 Testes no Localhost

### Opção 1: Via API (se disponível)

Se você tiver o servidor Flask rodando:

```bash
# Iniciar servidor
python commercial_repo/production/allianza_blockchain.py

# Em outro terminal, testar via curl
curl -X POST http://localhost:5000/cross-chain/transfer \
  -H "Content-Type: application/json" \
  -d '{
    "source_chain": "polygon",
    "target_chain": "bitcoin",
    "amount": 0.001,
    "token_symbol": "MATIC",
    "recipient": "bc1qxy2kgdygjrsqtzq2n0yrf2493p83kkfjhx0wlh"
  }'
```

### Opção 2: Via Python Script Local

Crie um arquivo `test_local.py`:

```python
#!/usr/bin/env python3
import sys
from pathlib import Path

# Adicionar ao path
sys.path.insert(0, str(Path(__file__).parent))

from test_commitment_improvements import CommitmentTester

# Executar testes
tester = CommitmentTester()
tester.test_connection("polygon")
tester.test_create_commitment("polygon")
```

Execute:

```bash
python test_local.py
```

---

## 🔍 Verificação no Explorer

### Polygon Amoy

1. Acesse: https://amoy.polygonscan.com/
2. Cole o TX Hash da transação
3. Verifique:
   - Status da transação (Success)
   - Eventos emitidos (CommitmentCreated)
   - Gas usado
   - Block number

### Ethereum Sepolia

1. Acesse: https://sepolia.etherscan.io/
2. Cole o TX Hash da transação
3. Verifique:
   - Status da transação (Success)
   - Eventos emitidos (CommitmentCreated)
   - Gas usado
   - Block number

### Verificar Evento CommitmentCreated

No explorer, na aba "Logs" ou "Events", procure por:

- **Event Name:** `CommitmentCreated`
- **Topics:**
  - `commitmentHash` (indexed)
  - `sourceAddress` (indexed)
  - `uchainId` (indexed)
- **Data:**
  - `targetChain`
  - `targetRecipient`
  - `amount`
  - `nonce`

---

## 🐛 Troubleshooting

### Erro: "Private key não configurada"

**Solução:**
- Verifique se o arquivo `.env` existe na raiz do projeto
- Verifique se `POLYGON_PRIVATE_KEY` ou `ETH_PRIVATE_KEY` está configurado
- Certifique-se de que a private key começa com `0x`

### Erro: "Não foi possível conectar à blockchain"

**Solução:**
- Verifique a RPC URL no `.env`
- Teste a conexão manualmente:
  ```python
  from web3 import Web3
  w3 = Web3(Web3.HTTPProvider("https://rpc-amoy.polygon.technology"))
  print(w3.is_connected())
  ```
- Se usar Infura, verifique se a chave está correta

### Erro: "Saldo insuficiente"

**Solução:**
- Obtenha tokens de teste no faucet
- Verifique o saldo:
  ```python
  balance = manager.w3.eth.get_balance(manager.account.address)
  print(f"Saldo: {manager.w3.from_wei(balance, 'ether')} ETH")
  ```

### Erro: "Commitment contract not loaded"

**Solução:**
- Verifique se o endereço do contrato está correto no `.env`
- Verifique se o contrato está deployado na testnet correta
- Teste a conexão com o contrato:
  ```python
  from web3 import Web3
  w3 = Web3(Web3.HTTPProvider(rpc_url))
  code = w3.eth.get_code(contract_address)
  print(f"Contract code length: {len(code)}")
  # Se for 0, o contrato não existe nesse endereço
  ```

### Erro: "Gas estimation failed"

**Solução:**
- Verifique se tem saldo suficiente para gas
- Tente aumentar o gas limit manualmente
- Verifique se o contrato está no endereço correto

### Erro de Importação

**Solução:**
- Certifique-se de estar no diretório raiz do projeto
- Verifique se os módulos estão no path:
  ```python
  import sys
  sys.path.insert(0, 'commercial_repo/adapters')
  ```

---

## 📊 Checklist de Testes

### Testes Básicos

- [ ] Conexão com blockchain funciona
- [ ] Saldo da conta é suficiente
- [ ] Commitment pode ser criado
- [ ] Commitment pode ser consultado
- [ ] TX Hash é retornado corretamente

### Testes de Integração

- [ ] Transferência cross-chain funciona
- [ ] Commitment é criado automaticamente
- [ ] Commitment data está no resultado
- [ ] Source transaction é executada
- [ ] Target transaction é executada

### Testes de Verificação

- [ ] TX aparece no explorer
- [ ] Evento CommitmentCreated é emitido
- [ ] Dados do evento estão corretos
- [ ] Commitment pode ser consultado on-chain

---

## 🎯 Exemplos de Saída Esperada

### Teste de Conexão

```
✅ Conectado! Block atual: 31778029
ℹ️  Endereço: 0x86AE40869EB6ACb9477b42BfC9150c0A2Cc21f5E
ℹ️  Saldo: 0.5 ETH
```

### Teste de Criação de Commitment

```
✅ Commitment criado com sucesso!
ℹ️  Commitment Hash: 0xabc123def456...
ℹ️  UChainID: 0xdef456abc123...
ℹ️  TX Hash: 0x789ghi012jkl...
ℹ️  Block Number: 31778030
ℹ️  Explorer: https://amoy.polygonscan.com/tx/0x789ghi012jkl...
```

### Teste de Consulta

```
✅ Commitment encontrado!
ℹ️  Source Address: 0x86AE40869EB6ACb9477b42BfC9150c0A2Cc21f5E
ℹ️  Target Chain: bitcoin
ℹ️  Amount: 1000000000000000 wei
ℹ️  UChainID: 0xdef456abc123...
ℹ️  Executed: False
ℹ️  Block Number: 31778030
```

---

## 📝 Notas Importantes

1. **Testes usam tokens REAIS** - Mesmo em testnet, você precisa de tokens de teste
2. **Gas fees são reais** - Cada transação consome gas
3. **Contratos já estão deployados** - Não precisa fazer deploy novamente
4. **Private keys são sensíveis** - Nunca compartilhe ou commite no git
5. **Use apenas testnets** - Não use mainnet para testes

---

## 🔗 Links Úteis

- **Polygon Amoy Explorer:** https://amoy.polygonscan.com/
- **Ethereum Sepolia Explorer:** https://sepolia.etherscan.io/
- **Polygon Faucet:** https://faucet.polygon.technology/
- **Sepolia Faucet:** https://sepoliafaucet.com/
- **Documentação Completa:** `docs/MELHORIAS_INTEROPERABILIDADE_COMPLETA.md`

---

**Versão:** 1.0  
**Última Atualização:** 2026-01-03

