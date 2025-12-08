# 💻 Guia de Uso do CLI - Windows

Guia específico para usar o CLI da Allianza Blockchain no Windows PowerShell.

---

## ⚠️ IMPORTANTE: Não use `<` e `>`

No Windows PowerShell, `<` e `>` são redirecionadores. **NÃO use** esses caracteres nos comandos!

**❌ ERRADO:**
```powershell
python cli/allianza_cli.py wallet balance <0xBeEd0E7001daA6E72146A5BA74Ace7D958037af5>
```

**✅ CORRETO:**
```powershell
python cli/allianza_cli.py wallet balance 0xBeEd0E7001daA6E72146A5BA74Ace7D958037af5
```

---

## 📋 Comandos Básicos

### 1. Criar Wallet

```powershell
python cli/allianza_cli.py wallet create
```

**Saída:**
```
✅ Wallet criada!
Endereço: 0xBeEd0E7001daA6E72146A5BA74Ace7D958037af5
Chave privada: 287cd4c45d3232c67919337e6d6c095e8db0fd40062ff92bf49422306c6dc955

⚠️  GUARDE A CHAVE PRIVADA EM SEGURANÇA!
```

---

### 2. Ver Saldo

```powershell
python cli/allianza_cli.py wallet balance 0xBeEd0E7001daA6E72146A5BA74Ace7D958037af5
```

**Substitua** `0xBeEd0E7001daA6E72146A5BA74Ace7D958037af5` pelo endereço real.

---

### 3. Enviar Transação

```powershell
python cli/allianza_cli.py transaction send 0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb0 0.1 --private-key 287cd4c45d3232c67919337e6d6c095e8db0fd40062ff92bf49422306c6dc955
```

**Onde:**
- `0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb0` = endereço de destino
- `0.1` = quantidade em ALZ
- `287cd4c45d3232c67919337e6d6c095e8db0fd40062ff92bf49422306c6dc955` = sua chave privada

---

### 4. Transação Cross-Chain

```powershell
python cli/allianza_cli.py transaction cross-chain bitcoin 1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa 0.001 --private-key 287cd4c45d3232c67919337e6d6c095e8db0fd40062ff92bf49422306c6dc955
```

**Onde:**
- `bitcoin` = chain de destino (bitcoin, ethereum, polygon, etc.)
- `1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa` = endereço de destino
- `0.001` = quantidade

---

### 5. Listar Validadores

```powershell
python cli/allianza_cli.py validator list
```

---

### 6. Informações do Validador

```powershell
python cli/allianza_cli.py validator info 0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb0
```

---

### 7. Informações da Rede

```powershell
python cli/allianza_cli.py network-info
```

---

### 8. Versão do CLI

```powershell
python cli/allianza_cli.py version
```

---

## 🔧 Usando Variáveis no PowerShell

Para facilitar, você pode usar variáveis:

```powershell
# Definir variáveis
$endereco = "0xBeEd0E7001daA6E72146A5BA74Ace7D958037af5"
$chave = "287cd4c45d3232c67919337e6d6c095e8db0fd40062ff92bf49422306c6dc955"
$destino = "0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb0"

# Usar nas variáveis
python cli/allianza_cli.py wallet balance $endereco
python cli/allianza_cli.py transaction send $destino 0.1 --private-key $chave
```

---

## 📝 Exemplos Completos

### Exemplo 1: Criar wallet e ver saldo

```powershell
# 1. Criar wallet
python cli/allianza_cli.py wallet create

# 2. Copiar o endereço gerado e verificar saldo
python cli/allianza_cli.py wallet balance 0xBeEd0E7001daA6E72146A5BA74Ace7D958037af5
```

### Exemplo 2: Enviar transação

```powershell
# Substitua pelos seus valores reais
python cli/allianza_cli.py transaction send 0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb0 0.1 --private-key 287cd4c45d3232c67919337e6d6c095e8db0fd40062ff92bf49422306c6dc955
```

### Exemplo 3: Transação cross-chain para Bitcoin

```powershell
python cli/allianza_cli.py transaction cross-chain bitcoin 1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa 0.001 --private-key 287cd4c45d3232c67919337e6d6c095e8db0fd40062ff92bf49422306c6dc955
```

---

## 🆘 Solução de Problemas

### Erro: "A sintaxe do comando está incorreta"

**Causa:** Você usou `<` ou `>` nos argumentos.

**Solução:** Remova `<` e `>` e use os valores diretamente.

**❌ ERRADO:**
```powershell
python cli/allianza_cli.py wallet balance <0xBeEd0E7001daA6E72146A5BA74Ace7D958037af5>
```

**✅ CORRETO:**
```powershell
python cli/allianza_cli.py wallet balance 0xBeEd0E7001daA6E72146A5BA74Ace7D958037af5
```

---

### Erro: "Connection refused"

**Causa:** O RPC Server não está rodando.

**Solução:** Inicie o RPC Server primeiro:

```powershell
python rpc_server.py
```

Depois, em outro terminal, execute os comandos do CLI.

---

### Erro: "Module not found"

**Causa:** Dependências não instaladas.

**Solução:** Instale as dependências:

```powershell
pip install -r requirements.txt
pip install click
```

---

## 💡 Dicas

1. **Use aspas para endereços longos:**
   ```powershell
   python cli/allianza_cli.py wallet balance "0xBeEd0E7001daA6E72146A5BA74Ace7D958037af5"
   ```

2. **Use Tab para autocompletar** (se configurado)

3. **Salve comandos em um arquivo .ps1** para reutilizar:
   ```powershell
   # meu_script.ps1
   $chave = "287cd4c45d3232c67919337e6d6c095e8db0fd40062ff92bf49422306c6dc955"
   python cli/allianza_cli.py wallet balance 0xBeEd0E7001daA6E72146A5BA74Ace7D958037af5
   ```

---

## 📖 Ver Ajuda

Para ver todos os comandos disponíveis:

```powershell
python cli/allianza_cli.py --help
```

Para ver ajuda de um comando específico:

```powershell
python cli/allianza_cli.py wallet --help
python cli/allianza_cli.py transaction --help
python cli/allianza_cli.py validator --help
```

---

**Lembre-se: NUNCA use `<` e `>` nos comandos do PowerShell!** ✅



















