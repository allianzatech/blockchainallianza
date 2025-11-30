# 🔐 Teste Profissional - Quantum Security Service (QSS)

## 📋 Guia de Testes para Bitcoin e Ethereum

Este documento descreve como testar profissionalmente a segurança quântica para Bitcoin e Ethereum usando o QSS.

---

## 🎯 Objetivo

Demonstrar que a Allianza pode fornecer segurança quântica (PQC) para blockchains que não suportam nativamente, como Bitcoin e Ethereum.

---

## 🧪 Teste 1: Segurança Quântica para Bitcoin

### **Passo 1: Acessar Dashboard QSS**

1. Acesse: `https://testnet.allianza.tech/qss`
2. Verifique se o serviço está **Online** (badge verde)

### **Passo 2: Gerar Prova Quântica para TX Bitcoin**

1. Na seção **"Teste de Segurança Quântica - Bitcoin"**:
   - Insira um TX Hash Bitcoin real (ex: de um explorer testnet)
   - Opcionalmente, insira o Block Height
   - Clique em **"Gerar Prova Quântica Bitcoin"**

2. **O que acontece:**
   - Sistema gera assinatura ML-DSA (PQC) para a transação
   - Cria Merkle Proof na Allianza
   - Gera Consensus Proof
   - Retorna Quantum Proof Object (JSON)

### **Passo 3: Verificar Prova**

1. Clique em **"Verificar Prova"**
2. Sistema verifica:
   - ✅ Assinatura ML-DSA válida
   - ✅ Merkle Proof válido
   - ✅ Proof Hash correto
   - ✅ Timestamp válido

### **Passo 4: Instruções de Ancoragem**

1. Sistema mostra instruções para ancorar no Bitcoin:
   - **Método**: OP_RETURN
   - **Data**: `ALZ-QSS:{proof_hash}`
   - **Formato**: Hash da prova quântica

2. **Como ancorar:**
   - Criar transação Bitcoin com OP_RETURN contendo o hash
   - Isso prova que a transação Bitcoin foi atestada pela Allianza

### **Resultado Esperado:**

```json
{
  "success": true,
  "quantum_proof": {
    "asset_chain": "bitcoin",
    "asset_tx": "abc123...",
    "quantum_signature": "Base64(ML-DSA signature)",
    "quantum_signature_scheme": "ML-DSA",
    "proof_hash": "sha256(tx_hash + signature + merkle_root)",
    "valid": true
  },
  "anchor_instructions": {
    "method": "OP_RETURN",
    "data": "ALZ-QSS:{proof_hash}",
    "proof_hash": "..."
  }
}
```

---

## 🧪 Teste 2: Segurança Quântica para Ethereum

### **Passo 1: Gerar Prova Quântica para TX Ethereum**

1. Na seção **"Teste de Segurança Quântica - Ethereum"**:
   - Insira um TX Hash Ethereum (ex: de Polygon/Amoy)
   - Opcionalmente, insira o Block Height
   - Clique em **"Gerar Prova Quântica Ethereum"**

### **Passo 2: Verificar Prova**

1. Clique em **"Verificar Prova"**
2. Sistema verifica todas as camadas de segurança

### **Passo 3: Instruções de Ancoragem**

1. Sistema mostra instruções para ancorar via Smart Contract:
   - **Método**: Smart Contract Call
   - **Função**: `anchorQuantumProof(bytes32 proofHash)`
   - **Gas Estimate**: ~50,000 gas
   - **Transaction Data**: Hex encoded

2. **Como ancorar:**
   - Chamar `QuantumSecurityAdapter.anchorQuantumProof(proofHash)`
   - Isso registra a prova on-chain na Ethereum

### **Resultado Esperado:**

```json
{
  "success": true,
  "quantum_proof": {
    "asset_chain": "ethereum",
    "asset_tx": "0xabc123...",
    "quantum_signature": "Base64(ML-DSA signature)",
    "quantum_signature_scheme": "ML-DSA",
    "proof_hash": "...",
    "valid": true
  },
  "anchor_instructions": {
    "method": "Smart Contract Call",
    "contract_function": "anchorQuantumProof(bytes32 proofHash)",
    "proof_hash": "...",
    "gas_estimate": 50000
  }
}
```

---

## 📊 Métricas de Profissionalismo

### **1. Verificação Criptográfica**

✅ **Assinatura ML-DSA**: Verificada matematicamente
✅ **Merkle Proof**: Verificado na Allianza
✅ **Proof Hash**: SHA-256 imutável
✅ **Timestamp**: Validado (não muito antigo)

### **2. Ancoragem Cross-Chain**

✅ **Bitcoin**: OP_RETURN com hash da prova
✅ **Ethereum**: Smart Contract com registro on-chain
✅ **Verificação Reversa**: Qualquer um pode verificar

### **3. Transparência**

✅ **JSON Público**: Prova pode ser verificada por qualquer um
✅ **Explorer**: Prova aparece no explorer da Allianza
✅ **Open Source**: Código verificável

---

## 🎬 Demonstração Profissional

### **Cenário 1: Exchange quer proteger saques Bitcoin**

1. Exchange recebe solicitação de saque Bitcoin
2. Exchange gera prova quântica via QSS API
3. Exchange ancore prova no OP_RETURN da transação Bitcoin
4. Cliente pode verificar que saque foi atestado quânticamente

### **Cenário 2: DeFi Protocol quer proteger swaps**

1. Protocol executa swap na Polygon
2. Protocol gera prova quântica via QSS API
3. Protocol ancore prova via Smart Contract
4. Usuários podem verificar segurança quântica on-chain

---

## 🔗 Links Úteis

- **Dashboard QSS**: `https://testnet.allianza.tech/qss`
- **API Status**: `https://testnet.allianza.tech/api/qss/status`
- **Verificar Prova**: `https://testnet.allianza.tech/verify-proof`
- **Explorer**: `https://testnet.allianza.tech/explorer`

---

## ✅ Checklist de Teste Profissional

- [ ] Serviço QSS está online
- [ ] Prova Bitcoin gerada com sucesso
- [ ] Prova Bitcoin verificada com sucesso
- [ ] Instruções de ancoragem Bitcoin recebidas
- [ ] Prova Ethereum gerada com sucesso
- [ ] Prova Ethereum verificada com sucesso
- [ ] Instruções de ancoragem Ethereum recebidas
- [ ] JSON da prova pode ser copiado/baixado
- [ ] Prova pode ser verificada publicamente
- [ ] Todas as métricas de segurança estão OK

---

## 🎯 Conclusão

O QSS permite que **qualquer blockchain** (Bitcoin, Ethereum, etc.) use segurança quântica sem precisar implementar PQC nativamente.

Isso é **revolucionário** porque:
1. ✅ Bitcoin não precisa mudar seu código
2. ✅ Ethereum não precisa hard fork
3. ✅ Qualquer blockchain pode usar segurança quântica
4. ✅ Provas são verificáveis publicamente
5. ✅ Ancoragem é imutável

**A Allianza se torna o "Chainlink da Segurança Quântica"** - uma camada de infraestrutura essencial para toda a Web3.

