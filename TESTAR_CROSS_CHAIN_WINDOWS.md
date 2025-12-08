# 🧪 Como Testar Cross-Chain no Windows

**Data:** 2025-12-08

---

## ✅ Interface Web no Dashboard

**URL:** https://testnet.allianza.tech/cross-chain-test

Acesse essa URL no navegador para testar via interface visual!

---

## 🐍 Opção 1: Script Python (Recomendado)

### 1. Execute o script:

```powershell
python test_cross_chain_windows.py
```

O script testa automaticamente:
- ✅ Criar transferência cross-chain
- ✅ Buscar prova por UChainID
- ✅ Listar todas as provas
- ✅ Status do sistema

---

## 💻 Opção 2: PowerShell (Comandos Corretos)

### Criar Transferência

```powershell
$body = @{
    source_chain = "polygon"
    target_chain = "ethereum"
    amount = 0.1
    recipient = "0x86AE40869EB6ACb9477b42BfC9150c0A2Cc21f5E"
    token_symbol = "ETH"
    send_real = $false
} | ConvertTo-Json

Invoke-RestMethod -Uri "https://testnet.allianza.tech/api/cross-chain/transfer" `
    -Method POST `
    -ContentType "application/json" `
    -Body $body
```

### Buscar Prova por UChainID

```powershell
$uchainId = "UCHAIN-abc123..."
Invoke-RestMethod -Uri "https://testnet.allianza.tech/api/cross-chain/proof/$uchainId" `
    -Method GET
```

### Listar Todas as Provas

```powershell
Invoke-RestMethod -Uri "https://testnet.allianza.tech/api/cross-chain/proofs?limit=50" `
    -Method GET
```

### Status do Sistema

```powershell
Invoke-RestMethod -Uri "https://testnet.allianza.tech/api/cross-chain/status" `
    -Method GET
```

---

## 🌐 Opção 3: Interface Web

1. **Acesse:** https://testnet.allianza.tech/cross-chain-test
2. **Preencha o formulário:**
   - Source Chain: Polygon
   - Target Chain: Ethereum
   - Amount: 0.1
   - Recipient: 0x86AE40869EB6ACb9477b42BfC9150c0A2Cc21f5E
3. **Clique em:** "Criar Transferência Cross-Chain"
4. **Veja o resultado:**
   - UChainID gerado
   - ZK Proof (se disponível)
   - Link para explorer (se send_real=true)

---

## 📋 Endpoints Disponíveis

| Endpoint | Método | Descrição |
|----------|--------|-----------|
| `/api/cross-chain/transfer` | POST | Criar transferência |
| `/api/cross-chain/proof/<uchain_id>` | GET | Buscar prova |
| `/api/cross-chain/proofs` | GET | Listar provas |
| `/api/cross-chain/status` | GET | Status do sistema |
| `/cross-chain-test` | GET | Interface web |

---

## ✅ Checklist de Teste

- [ ] Acessar interface web: `/cross-chain-test`
- [ ] Criar 1 transferência cross-chain
- [ ] Verificar que UChainID foi gerado
- [ ] Buscar prova por UChainID
- [ ] Listar todas as provas
- [ ] Verificar status do sistema

---

**Última atualização:** 2025-12-08

