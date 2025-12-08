# 💻 CLI Usage Guide - Windows

Specific guide for using Allianza Blockchain CLI on Windows PowerShell.

---

## ⚠️ IMPORTANT: Do not use `<` and `>`

In Windows PowerShell, `<` and `>` are redirectors. **DO NOT use** these characters in commands!

**❌ WRONG:**
```powershell
python cli/allianza_cli.py wallet balance <0xBeEd0E7001daA6E72146A5BA74Ace7D958037af5>
```

**✅ CORRECT:**
```powershell
python cli/allianza_cli.py wallet balance 0xBeEd0E7001daA6E72146A5BA74Ace7D958037af5
```

---

## 📋 Basic Commands

### 1. Create Wallet

```powershell
python cli/allianza_cli.py wallet create
```

**Output:**
```
✅ Wallet created!
Address: 0xBeEd0E7001daA6E72146A5BA74Ace7D958037af5
Private key: 287cd4c45d3232c67919337e6d6c095e8db0fd40062ff92bf49422306c6dc955

⚠️  KEEP YOUR PRIVATE KEY SAFE!
```

---

### 2. Check Balance

```powershell
python cli/allianza_cli.py wallet balance 0xBeEd0E7001daA6E72146A5BA74Ace7D958037af5
```

**Replace** `0xBeEd0E7001daA6E72146A5BA74Ace7D958037af5` with the actual address.

---

### 3. Send Transaction

```powershell
python cli/allianza_cli.py transaction send 0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb0 0.1 --private-key 287cd4c45d3232c67919337e6d6c095e8db0fd40062ff92bf49422306c6dc955
```

**Where:**
- `0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb0` = destination address
- `0.1` = amount in ALZ
- `287cd4c45d3232c67919337e6d6c095e8db0fd40062ff92bf49422306c6dc955` = your private key

---

### 4. Cross-Chain Transaction

```powershell
python cli/allianza_cli.py transaction cross-chain bitcoin 1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa 0.001 --private-key 287cd4c45d3232c67919337e6d6c095e8db0fd40062ff92bf49422306c6dc955
```

**Where:**
- `bitcoin` = destination chain (bitcoin, ethereum, polygon, etc.)
- `1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa` = destination address
- `0.001` = amount

---

### 5. List Validators

```powershell
python cli/allianza_cli.py validator list
```

---

### 6. Validator Information

```powershell
python cli/allianza_cli.py validator info 0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb0
```

---

### 7. Network Information

```powershell
python cli/allianza_cli.py network-info
```

---

## 🔗 Useful Links

- **Testnet**: https://testnet.allianza.tech
- **Developer Hub**: https://testnet.allianza.tech/developer-hub
- **API Documentation**: [API_REFERENCE.md](API_REFERENCE.md)
- **Quick Start**: [QUICK_START.md](QUICK_START.md)

---

**Note:** This CLI is for demonstration purposes. The core blockchain implementation remains private.
