# 🔐 Guia Completo: QSS para Outras Blockchains

## 📋 Índice

1. [Como o QSS Funciona](#como-o-qss-funciona)
2. [Como Obter Hashes de Transações](#como-obter-hashes-de-transações)
3. [Como Testar com Diferentes Blockchains](#como-testar-com-diferentes-blockchains)
4. [Exemplos Práticos](#exemplos-práticos)
5. [Ancoragem de Provas](#ancoragem-de-provas)
6. [FAQ](#faq)

---

## 🎯 Como o QSS Funciona

### O Que é o QSS?

O **Quantum Security Service (QSS)** é um serviço que permite que **qualquer blockchain** (Bitcoin, Ethereum, Polygon, Solana, etc.) use a segurança quântica da Allianza Blockchain **sem precisar modificar seu código ou consenso**.

### Como Funciona na Prática?

```
┌─────────────────────────────────────────────────────────────┐
│ 1. Você tem uma transação em qualquer blockchain            │
│    Exemplo: Bitcoin TX: 842f01a3302b6b19981204c96f377be1... │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│ 2. Você envia o hash da transação para o QSS               │
│    POST /api/qss/generate-proof                             │
│    {                                                        │
│      "chain": "bitcoin",                                    │
│      "tx_hash": "842f01a3302b6b19981204c96f377be1..."       │
│    }                                                        │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│ 3. Allianza gera uma PROVA QUÂNTICA verificável            │
│    - Assinatura ML-DSA (pós-quântica)                      │
│    - Merkle Proof (prova de inclusão)                       │
│    - Consensus Proof (prova de finalidade)                  │
│    - Proof Hash (hash canônico RFC8785)                     │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│ 4. Você recebe um JSON com a prova completa                │
│    {                                                        │
│      "proof_hash": "ac0036b1f993fb202923eb77f686b660...",  │
│      "quantum_signature": "Base64...",                      │
│      "merkle_proof": {...},                                 │
│      "valid": true                                          │
│    }                                                        │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│ 5. Você pode:                                               │
│    ✅ Verificar a prova em /verify-proof                     │
│    ✅ Ancorar no Bitcoin (OP_RETURN)                        │
│    ✅ Ancorar no Ethereum (Smart Contract)                 │
│    ✅ Usar como certificado de segurança                    │
└─────────────────────────────────────────────────────────────┘
```

### Por Que Isso é Revolucionário?

1. **Bitcoin não suporta PQC nativamente** → Mas você pode provar que uma TX Bitcoin foi validada por uma rede PQC
2. **Ethereum não tem segurança quântica** → Mas você pode ancorar provas QSS em contratos inteligentes
3. **Qualquer blockchain** → Pode usar segurança quântica sem modificar o código

---

## 🔍 Como Obter Hashes de Transações

### ✅ SIM, você pode pegar hashes direto dos explorers!

Os explorers são **públicos e confiáveis**. Qualquer hash de transação que você vê em um explorer é válido para gerar uma prova QSS.

### 📍 Onde Encontrar Hashes?

#### **Bitcoin (Testnet)**
- **BlockCypher**: https://www.blockcypher.com/dev/bitcoin/#blockchain
- **Blockstream**: https://blockstream.info/testnet/
- **Blockchain.com**: https://www.blockchain.com/explorer

**Como pegar:**
1. Acesse https://www.blockcypher.com/dev/bitcoin/#blockchain
2. Procure por uma transação recente
3. Copie o **TX Hash** (ex: `842f01a3302b6b19981204c96f377be1ec1dfc51e995f68b3a1563e6750d06e8`)

#### **Ethereum (Sepolia Testnet)**
- **Etherscan**: https://sepolia.etherscan.io/
- **Blockscout**: https://sepolia.blockscout.com/

**Como pegar:**
1. Acesse https://sepolia.etherscan.io/
2. Procure por uma transação
3. Copie o **TxHash** (ex: `0x286d8d6e9985ea1b423cf60bd902c850073574343694d8ccac1cca0c5e76edd6`)

#### **Polygon (Amoy Testnet)**
- **Polygonscan**: https://amoy.polygonscan.com/
- **Blockscout**: https://polygon-amoy.blockscout.com/

**Como pegar:**
1. Acesse https://amoy.polygonscan.com/
2. Procure por uma transação
3. Copie o **TxHash** (ex: `0x03008e09df2465e5ce67c179cf8b86b6f533a14ddfef643612a91d833dad4008`)

#### **BSC (Testnet)**
- **BscScan**: https://testnet.bscscan.com/

#### **Solana (Testnet)**
- **Solscan**: https://solscan.io/?cluster=testnet
- **Solana Explorer**: https://explorer.solana.com/?cluster=testnet

---

## 🧪 Como Testar com Diferentes Blockchains

### Método 1: Via Dashboard QSS (Mais Fácil)

1. **Acesse**: https://testnet.allianza.tech/qss
2. **Selecione a blockchain**: Bitcoin, Ethereum, Polygon, etc.
3. **Cole o hash da transação** (copiado do explorer)
4. **Clique em "Gerar Prova"**
5. **Verifique o resultado** clicando em "Verificar Prova"

### Método 2: Via API REST (Para Desenvolvedores)

#### **Exemplo: Bitcoin**

```bash
curl -X POST https://testnet.allianza.tech/api/qss/generate-proof \
  -H "Content-Type: application/json" \
  -d '{
    "chain": "bitcoin",
    "tx_hash": "842f01a3302b6b19981204c96f377be1ec1dfc51e995f68b3a1563e6750d06e8"
  }'
```

#### **Exemplo: Ethereum**

```bash
curl -X POST https://testnet.allianza.tech/api/qss/generate-proof \
  -H "Content-Type: application/json" \
  -d '{
    "chain": "ethereum",
    "tx_hash": "0x286d8d6e9985ea1b423cf60bd902c850073574343694d8ccac1cca0c5e76edd6"
  }'
```

#### **Exemplo: Polygon**

```bash
curl -X POST https://testnet.allianza.tech/api/qss/generate-proof \
  -H "Content-Type: application/json" \
  -d '{
    "chain": "polygon",
    "tx_hash": "0x03008e09df2465e5ce67c179cf8b86b6f533a14ddfef643612a91d833dad4008"
  }'
```

### Método 3: Via SDK JavaScript

```typescript
import { QSSClient } from '@allianza/qss-js';

const qss = new QSSClient({
  apiUrl: 'https://testnet.allianza.tech/api/qss'
});

// Bitcoin
const bitcoinProof = await qss.generateProof(
  'bitcoin',
  '842f01a3302b6b19981204c96f377be1ec1dfc51e995f68b3a1563e6750d06e8'
);

// Ethereum
const ethereumProof = await qss.generateProof(
  'ethereum',
  '0x286d8d6e9985ea1b423cf60bd902c850073574343694d8ccac1cca0c5e76edd6'
);

// Verificar
const result = await qss.verifyProof(bitcoinProof);
console.log('Prova válida?', result.valid);
```

---

## 💡 Exemplos Práticos

### Exemplo 1: Provar Segurança de uma Transação Bitcoin

**Cenário**: Você quer provar que uma transação Bitcoin foi validada por segurança quântica.

**Passo a Passo:**

1. **Encontre uma transação Bitcoin no BlockCypher**
   - Acesse: https://www.blockcypher.com/dev/bitcoin/#blockchain
   - Copie o hash: `842f01a3302b6b19981204c96f377be1ec1dfc51e995f68b3a1563e6750d06e8`

2. **Gere a prova QSS**
   ```bash
   POST /api/qss/generate-proof
   {
     "chain": "bitcoin",
     "tx_hash": "842f01a3302b6b19981204c96f377be1ec1dfc51e995f68b3a1563e6750d06e8"
   }
   ```

3. **Receba a prova**
   ```json
   {
     "proof_hash": "ac0036b1f993fb202923eb77f686b66081b4f570fdb0ca531d48e81818d9d088",
     "quantum_signature": "bDlHdmZ0MU9VQ3pTcFBuR3NNR0dnUWJBQ3IycWtXNzF3UElSOFRzTXQwU2NGMTV3dXZyaUlaRUk2REZPMkVzTlYrcGl6OUVpT1FLK1BXR0E4TFBHSmc9PQ==",
     "valid": true
   }
   ```

4. **Verifique a prova**
   - Acesse: https://testnet.allianza.tech/verify-proof
   - Cole o JSON da prova
   - Veja: ✅ **Prova válida!**

### Exemplo 2: Provar Segurança de uma Transação Ethereum

**Cenário**: Você quer provar que uma transação Ethereum foi validada por segurança quântica.

**Passo a Passo:**

1. **Encontre uma transação Ethereum no Etherscan**
   - Acesse: https://sepolia.etherscan.io/
   - Copie o hash: `0x286d8d6e9985ea1b423cf60bd902c850073574343694d8ccac1cca0c5e76edd6`

2. **Gere a prova QSS**
   ```bash
   POST /api/qss/generate-proof
   {
     "chain": "ethereum",
     "tx_hash": "0x286d8d6e9985ea1b423cf60bd902c850073574343694d8ccac1cca0c5e76edd6"
   }
   ```

3. **Ancore a prova em um Smart Contract**
   ```typescript
   const { transactionData } = await qss.anchorOnEVM(
     proof,
     '0x...', // Endereço do contrato QuantumSecurityAdapter
     'ethereum'
   );
   ```

### Exemplo 3: Provar Segurança de uma Transação Polygon

**Cenário**: Você quer provar que uma transação Polygon foi validada por segurança quântica.

**Passo a Passo:**

1. **Encontre uma transação Polygon no Polygonscan**
   - Acesse: https://amoy.polygonscan.com/
   - Copie o hash: `0x03008e09df2465e5ce67c179cf8b86b6f533a14ddfef643612a91d833dad4008`

2. **Gere a prova QSS**
   ```bash
   POST /api/qss/generate-proof
   {
     "chain": "polygon",
     "tx_hash": "0x03008e09df2465e5ce67c179cf8b86b6f533a14ddfef643612a91d833dad4008"
   }
   ```

3. **Use a prova como certificado de segurança**
   - A prova pode ser usada para validar a integridade da transação
   - Pode ser ancorada no Polygon via Smart Contract
   - Pode ser verificada publicamente

---

## 🔗 Ancoragem de Provas

### O Que é Ancoragem?

**Ancoragem** é o processo de registrar a prova QSS **diretamente na blockchain de destino**, criando um link imutável entre a transação original e a prova quântica.

### Como Funciona?

#### **Bitcoin (via OP_RETURN)**

```json
{
  "method": "OP_RETURN",
  "data": "ac0036b1f993fb202923eb77f686b66081b4f570fdb0ca531d48e81818d9d088",
  "instructions": "Incluir este hash no OP_RETURN da próxima transação Bitcoin"
}
```

**Nota**: OP_RETURN está temporariamente desabilitado, mas a prova ainda é válida e verificável.

#### **Ethereum/Polygon (via Smart Contract)**

```typescript
// Contrato QuantumSecurityAdapter
contract QuantumSecurityAdapter {
    function anchorProof(
        bytes32 proofHash,
        bytes calldata quantumSignature,
        bytes32 merkleRoot
    ) external {
        // Armazena a prova on-chain
        proofs[proofHash] = Proof({
            hash: proofHash,
            signature: quantumSignature,
            merkleRoot: merkleRoot,
            timestamp: block.timestamp
        });
    }
}
```

---

## ❓ FAQ

### 1. **Posso usar qualquer hash de transação?**

✅ **SIM!** Qualquer hash de transação válido de qualquer blockchain pode ser usado para gerar uma prova QSS.

### 2. **Preciso ter a transação na minha carteira?**

❌ **NÃO!** Você só precisa do **hash da transação**. Não precisa ser o dono da transação.

### 3. **A prova é válida mesmo se eu pegar o hash de um explorer?**

✅ **SIM!** Os explorers mostram dados públicos da blockchain. Qualquer hash válido pode ser usado.

### 4. **Como sei se a prova é confiável?**

✅ **Verifique em**: https://testnet.allianza.tech/verify-proof
- A prova é verificada criptograficamente
- A assinatura ML-DSA é validada
- O Merkle Proof é verificado
- O Proof Hash é recalculado

### 5. **Posso usar provas de Mainnet?**

⚠️ **ATENÇÃO**: Atualmente o QSS está em **Testnet**. Para Mainnet, você precisará:
- Usar a API da Mainnet (quando disponível)
- Ter tokens reais para ancoragem
- Verificar os custos de gas

### 6. **Quais blockchains são suportadas?**

✅ **Suportadas atualmente:**
- Bitcoin (Testnet)
- Ethereum (Sepolia Testnet)
- Polygon (Amoy Testnet)
- BSC (Testnet)
- Solana (Testnet)
- Qualquer blockchain (via hash genérico)

### 7. **Como testar profissionalmente?**

📋 **Checklist de Teste Profissional:**

1. ✅ **Bitcoin Testnet**
   - Pegue um hash do BlockCypher
   - Gere a prova QSS
   - Verifique em /verify-proof
   - Documente o resultado

2. ✅ **Ethereum Sepolia**
   - Pegue um hash do Etherscan
   - Gere a prova QSS
   - Verifique em /verify-proof
   - Teste ancoragem em Smart Contract

3. ✅ **Polygon Amoy**
   - Pegue um hash do Polygonscan
   - Gere a prova QSS
   - Verifique em /verify-proof
   - Teste ancoragem em Smart Contract

4. ✅ **Validação Independente**
   - Use o verificador open-source: https://github.com/allianza-blockchain/qss-verifier
   - Verifique a assinatura ML-DSA
   - Valide o Merkle Proof
   - Confirme o Proof Hash

---

## 🎯 Resumo: Como Dar Segurança Quântica para Outras Blockchains

### **Passo 1: Obter Hash da Transação**
- Acesse qualquer explorer (BlockCypher, Etherscan, Polygonscan, etc.)
- Copie o hash da transação

### **Passo 2: Gerar Prova QSS**
- Use o Dashboard: https://testnet.allianza.tech/qss
- Ou use a API: `POST /api/qss/generate-proof`
- Ou use o SDK: `qss.generateProof(chain, txHash)`

### **Passo 3: Verificar a Prova**
- Acesse: https://testnet.allianza.tech/verify-proof
- Cole o JSON da prova
- Confirme: ✅ **Prova válida!**

### **Passo 4: Ancorar (Opcional)**
- **Bitcoin**: Incluir `proof_hash` no OP_RETURN
- **Ethereum/Polygon**: Chamar `anchorProof()` no Smart Contract
- **Outras**: Usar método específico da blockchain

---

## 📚 Recursos Adicionais

- **Dashboard QSS**: https://testnet.allianza.tech/qss
- **Verificador de Provas**: https://testnet.allianza.tech/verify-proof
- **API Status**: https://testnet.allianza.tech/api/qss/status
- **SDK JavaScript**: https://github.com/allianza-blockchain/qss-sdk
- **Verificador Open-Source**: https://github.com/allianza-blockchain/qss-verifier

---

## 🚀 Próximos Passos

1. **Teste com Bitcoin**: Pegue um hash do BlockCypher e gere uma prova
2. **Teste com Ethereum**: Pegue um hash do Etherscan e gere uma prova
3. **Teste com Polygon**: Pegue um hash do Polygonscan e gere uma prova
4. **Valide Independentemente**: Use o verificador open-source
5. **Documente os Resultados**: Crie um relatório de testes

---

**🎉 Agora você sabe como dar segurança quântica para qualquer blockchain!**

Qualquer dúvida, consulte este documento ou acesse o dashboard QSS.



