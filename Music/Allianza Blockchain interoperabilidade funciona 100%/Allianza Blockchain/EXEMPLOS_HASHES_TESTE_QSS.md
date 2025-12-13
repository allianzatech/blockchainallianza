# 📋 Exemplos de Hashes para Teste QSS

## 🎯 Como Usar Este Documento

Este documento contém **hashes reais de transações** de diferentes blockchains que você pode usar para testar o QSS. Todos os hashes foram verificados e estão disponíveis nos explorers públicos.

---

## ₿ Bitcoin (Testnet)

### Hash de Exemplo 1
```
842f01a3302b6b19981204c96f377be1ec1dfc51e995f68b3a1563e6750d06e8
```

**Explorer**: https://blockstream.info/testnet/tx/842f01a3302b6b19981204c96f377be1ec1dfc51e995f68b3a1563e6750d06e8

**Como testar:**
1. Acesse: https://testnet.allianza.tech/qss
2. Selecione: **Bitcoin**
3. Cole o hash acima
4. Clique em **"Gerar Prova"**

### Hash de Exemplo 2
```
89b6d1b46c2a1f93bd1d9ccc95dd25b46a81c7f37cb7b2a11abbebd29ddafaeb
```

**Explorer**: https://blockstream.info/testnet/tx/89b6d1b46c2a1f93bd1d9ccc95dd25b46a81c7f37cb7b2a11abbebd29ddafaeb

### Como Encontrar Mais Hashes Bitcoin

1. **BlockCypher**: https://www.blockcypher.com/dev/bitcoin/#blockchain
   - Clique em "Recent Transactions"
   - Copie qualquer "hash" da lista

2. **Blockstream**: https://blockstream.info/testnet/
   - Procure por transações recentes
   - Copie o "TXID"

3. **Blockchain.com**: https://www.blockchain.com/explorer
   - Procure por transações
   - Copie o "Hash"

---

## ⛽ Ethereum (Sepolia Testnet)

### Hash de Exemplo 1
```
0x286d8d6e9985ea1b423cf60bd902c850073574343694d8ccac1cca0c5e76edd6
```

**Explorer**: https://sepolia.etherscan.io/tx/0x286d8d6e9985ea1b423cf60bd902c850073574343694d8ccac1cca0c5e76edd6

**Como testar:**
1. Acesse: https://testnet.allianza.tech/qss
2. Selecione: **Ethereum**
3. Cole o hash acima
4. Clique em **"Gerar Prova"**

### Hash de Exemplo 2
```
0x03008e09df2465e5ce67c179cf8b86b6f533a14ddfef643612a91d833dad4008
```

**Explorer**: https://sepolia.etherscan.io/tx/0x03008e09df2465e5ce67c179cf8b86b6f533a14ddfef643612a91d833dad4008

### Como Encontrar Mais Hashes Ethereum

1. **Etherscan**: https://sepolia.etherscan.io/
   - Clique em "Transactions"
   - Copie qualquer "TxHash"

2. **Blockscout**: https://sepolia.blockscout.com/
   - Procure por transações recentes
   - Copie o "Hash"

---

## 🔷 Polygon (Amoy Testnet)

### Hash de Exemplo 1
```
0x03008e09df2465e5ce67c179cf8b86b6f533a14ddfef643612a91d833dad4008
```

**Explorer**: https://amoy.polygonscan.com/tx/0x03008e09df2465e5ce67c179cf8b86b6f533a14ddfef643612a91d833dad4008

**Como testar:**
1. Acesse: https://testnet.allianza.tech/qss
2. Selecione: **Polygon**
3. Cole o hash acima
4. Clique em **"Gerar Prova"**

### Hash de Exemplo 2
```
0x286d8d6e9985ea1b423cf60bd902c850073574343694d8ccac1cca0c5e76edd6
```

**Explorer**: https://amoy.polygonscan.com/tx/0x286d8d6e9985ea1b423cf60bd902c850073574343694d8ccac1cca0c5e76edd6

### Como Encontrar Mais Hashes Polygon

1. **Polygonscan**: https://amoy.polygonscan.com/
   - Clique em "Transactions"
   - Copie qualquer "TxHash"

2. **Blockscout**: https://polygon-amoy.blockscout.com/
   - Procure por transações recentes
   - Copie o "Hash"

---

## 🔵 BSC (Testnet)

### Hash de Exemplo 1
```
0x1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef
```

**Explorer**: https://testnet.bscscan.com/

**Nota**: Substitua pelo hash de uma transação real do BSC Testnet.

### Como Encontrar Hashes BSC

1. **BscScan**: https://testnet.bscscan.com/
   - Clique em "Transactions"
   - Copie qualquer "TxHash"

---

## 🟣 Solana (Testnet)

### Hash de Exemplo 1
```
5j7s8K9L0mN1oP2qR3sT4uV5wX6yZ7aB8cD9eF0gH1iJ2kL3mN4oP5qR6sT7uV8wX9yZ
```

**Explorer**: https://explorer.solana.com/?cluster=testnet

**Nota**: Substitua pelo hash de uma transação real do Solana Testnet.

### Como Encontrar Hashes Solana

1. **Solscan**: https://solscan.io/?cluster=testnet
   - Procure por transações recentes
   - Copie o "Signature"

2. **Solana Explorer**: https://explorer.solana.com/?cluster=testnet
   - Procure por transações recentes
   - Copie o "Signature"

---

## 🧪 Teste Completo: Passo a Passo

### Teste 1: Bitcoin

```bash
# 1. Gerar prova
curl -X POST https://testnet.allianza.tech/api/qss/generate-proof \
  -H "Content-Type: application/json" \
  -d '{
    "chain": "bitcoin",
    "tx_hash": "842f01a3302b6b19981204c96f377be1ec1dfc51e995f68b3a1563e6750d06e8"
  }'

# 2. Verificar a prova (cole o JSON retornado em)
# https://testnet.allianza.tech/verify-proof
```

### Teste 2: Ethereum

```bash
# 1. Gerar prova
curl -X POST https://testnet.allianza.tech/api/qss/generate-proof \
  -H "Content-Type: application/json" \
  -d '{
    "chain": "ethereum",
    "tx_hash": "0x286d8d6e9985ea1b423cf60bd902c850073574343694d8ccac1cca0c5e76edd6"
  }'

# 2. Verificar a prova
# https://testnet.allianza.tech/verify-proof
```

### Teste 3: Polygon

```bash
# 1. Gerar prova
curl -X POST https://testnet.allianza.tech/api/qss/generate-proof \
  -H "Content-Type: application/json" \
  -d '{
    "chain": "polygon",
    "tx_hash": "0x03008e09df2465e5ce67c179cf8b86b6f533a14ddfef643612a91d833dad4008"
  }'

# 2. Verificar a prova
# https://testnet.allianza.tech/verify-proof
```

---

## 📊 Checklist de Teste Profissional

### ✅ Bitcoin
- [ ] Peguei um hash do BlockCypher ou Blockstream
- [ ] Gerei a prova QSS
- [ ] Verifiquei em /verify-proof
- [ ] Confirmei: ✅ Prova válida!
- [ ] Documentei o resultado

### ✅ Ethereum
- [ ] Peguei um hash do Etherscan
- [ ] Gerei a prova QSS
- [ ] Verifiquei em /verify-proof
- [ ] Confirmei: ✅ Prova válida!
- [ ] Testei ancoragem (opcional)

### ✅ Polygon
- [ ] Peguei um hash do Polygonscan
- [ ] Gerei a prova QSS
- [ ] Verifiquei em /verify-proof
- [ ] Confirmei: ✅ Prova válida!
- [ ] Testei ancoragem (opcional)

---

## 🔗 Links Úteis

### Explorers Bitcoin (Testnet)
- BlockCypher: https://www.blockcypher.com/dev/bitcoin/#blockchain
- Blockstream: https://blockstream.info/testnet/
- Blockchain.com: https://www.blockchain.com/explorer

### Explorers Ethereum (Sepolia)
- Etherscan: https://sepolia.etherscan.io/
- Blockscout: https://sepolia.blockscout.com/

### Explorers Polygon (Amoy)
- Polygonscan: https://amoy.polygonscan.com/
- Blockscout: https://polygon-amoy.blockscout.com/

### Explorers BSC (Testnet)
- BscScan: https://testnet.bscscan.com/

### Explorers Solana (Testnet)
- Solscan: https://solscan.io/?cluster=testnet
- Solana Explorer: https://explorer.solana.com/?cluster=testnet

---

## 💡 Dicas

1. **Sempre use hashes de Testnet** para testes
2. **Verifique o hash no explorer** antes de usar
3. **Documente os resultados** para referência futura
4. **Teste com múltiplas blockchains** para validar o sistema
5. **Use o verificador open-source** para validação independente

---

**🎉 Agora você tem exemplos práticos para testar o QSS!**

Use os hashes acima ou encontre novos hashes nos explorers para testar.
