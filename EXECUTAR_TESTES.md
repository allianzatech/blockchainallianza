# 🧪 Como Executar os Testes - Allianza Blockchain

Este guia fornece comandos prontos para executar todos os testes e verificar se funcionam.

## 📋 Pré-requisitos

### 1. Verificar Python

```bash
python --version
# Deve ser Python 3.8 ou superior
```

### 2. Instalar Dependências

```bash
# Navegar para o diretório do projeto
cd "C:\Users\notebook\Downloads\Allianza Blockchain"

# Instalar dependências básicas
pip install -r requirements.txt

# (Opcional) Instalar liboqs-python para testes PQC completos
# pip install liboqs-python
```

## 🚀 Comandos para Executar os Testes

### Teste 0: Teste Simples (Recomendado Primeiro)

**Comando:**
```bash
python test_simple.py
```

**O que testa:**
- ✅ Se o código-fonte existe
- ✅ Se consegue ler o código-fonte
- ✅ Se as provas existem
- ✅ Se os hashes de transação são válidos

**Este teste NÃO requer dependências complexas!**

### Teste 1: Testes Básicos de Verificação

**Comando:**
```bash
python tests/public/run_verification_tests.py
```

**O que testa:**
- ✅ QRS-3 (ML-DSA e SPHINCS+)
- ✅ Funcionalidades básicas da blockchain
- ✅ Interoperabilidade básica

**Resultado esperado:**
```
🚀 VERIFICAÇÃO PÚBLICA - ALLIANZA BLOCKCHAIN
======================================================================
📅 Data: 2025-12-07T...
📁 Diretório: C:\Users\notebook\Downloads\Allianza Blockchain

======================================================================
🧪 TESTE 1: Verificação QRS-3 (PQC)
======================================================================
📝 Testando ML-DSA...
✅ ML-DSA: Assinatura e verificação OK
📝 Testando SPHINCS+...
✅ SPHINCS+: Assinatura e verificação OK
✅ TESTE 1: PASSOU

======================================================================
🧪 TESTE 2: Funcionalidades Básicas da Blockchain
======================================================================
📝 Inicializando blockchain...
✅ Blockchain inicializada: X blocos
📝 Testando criação de wallet...
✅ Wallet criada: ALZ1...
✅ TESTE 2: PASSOU

======================================================================
📊 RESUMO
======================================================================
Total de testes: 3
✅ Passou: 3
❌ Falhou: 0
```

### Teste 2: Suite Completa de Testes

**Comando:**
```bash
python tests/public/run_all_tests.py
```

**O que testa:**
- ✅ Todos os testes básicos
- ✅ QRS-3 público
- ✅ Blockchain pública
- ✅ Gera relatório consolidado

**Resultado esperado:**
```
🚀 TESTES PÚBLICOS - ALLIANZA BLOCKCHAIN
======================================================================
📅 Data: 2025-12-07T...
📁 Diretório: C:\Users\notebook\Downloads\Allianza Blockchain

======================================================================
🧪 TESTE: QRS-3 (PQC)
======================================================================
📝 Testando ML-DSA...
✅ ML-DSA: OK
📝 Testando SPHINCS+...
✅ SPHINCS+: OK
✅ TESTE QRS-3: PASSOU

======================================================================
🧪 TESTE: Blockchain
======================================================================
📝 Inicializando blockchain...
✅ Blockchain: OK
📝 Testando wallet...
✅ Wallet: OK
✅ TESTE BLOCKCHAIN: PASSOU

✅ TODOS OS TESTES PASSARAM!
```

## 🔍 Verificar Código-Fonte

### Verificar QRS-3 (PQC)

```bash
# Ver código-fonte QRS-3
cat core/crypto/pqc_crypto.py

# Ou no Windows PowerShell:
Get-Content core/crypto/pqc_crypto.py
```

### Verificar ALZ-NIEV Protocol

```bash
# Ver código-fonte ALZ-NIEV
cat core/consensus/alz_niev_interoperability.py

# Ou no Windows PowerShell:
Get-Content core/consensus/alz_niev_interoperability.py
```

### Verificar Interoperabilidade

```bash
# Ver código-fonte Bridge-Free
cat core/interoperability/bridge_free_interop.py

# Ou no Windows PowerShell:
Get-Content core/interoperability/bridge_free_interop.py
```

## 🌐 Verificar Testnet

### Acessar Testnet

1. **Dashboard**: https://testnet.allianza.tech
2. **Explorer**: https://testnet.allianza.tech/explorer
3. **Faucet**: https://testnet.allianza.tech/faucet
4. **QRS-3 Verifier**: https://testnet.allianza.tech/qrs3-verifier

### Verificar Transações Reais

**Ethereum Transaction:**
- Hash: `0x9a75d8edd1af2f7239db94d799abbdec30c42870899cbdcb5d9d8df4daf27110`
- Verificar em: https://sepolia.etherscan.io/tx/0x9a75d8edd1af2f7239db94d799abbdec30c42870899cbdcb5d9d8df4daf27110

**Bitcoin Transaction:**
- Hash: `842f01a3302b6b19981204c96f377be1ec1dfc51e995f68b3a1563e6750d06e8`
- Verificar em: https://blockstream.info/testnet/tx/842f01a3302b6b19981204c96f377be1ec1dfc51e995f68b3a1563e6750d06e8

## 📊 Verificar Resultados dos Testes

Os resultados são salvos em:
```
proofs/testnet/verification_YYYYMMDD_HHMMSS.json
```

**Ver último resultado:**
```bash
# Listar arquivos de resultados
dir proofs\testnet\verification_*.json

# Ver último resultado (PowerShell)
Get-Content (Get-ChildItem proofs\testnet\verification_*.json | Sort-Object LastWriteTime -Descending | Select-Object -First 1)
```

## ⚠️ Solução de Problemas

### Erro: "ModuleNotFoundError: No module named 'pqc_crypto'"

**Solução:**
```bash
# Verificar se está no diretório correto
cd "C:\Users\notebook\Downloads\Allianza Blockchain"

# Verificar se o arquivo existe
dir pqc_crypto.py
```

### Erro: "liboqs-python não instalado"

**Solução:**
```bash
# Instalar liboqs-python (opcional, mas recomendado)
pip install liboqs-python

# Se não conseguir instalar, os testes ainda funcionam com simulação
```

### Erro: "No module named 'allianza_blockchain'"

**Solução:**
```bash
# Verificar se está no diretório correto
cd "C:\Users\notebook\Downloads\Allianza Blockchain"

# Verificar se o arquivo existe
dir allianza_blockchain.py
```

## ✅ Checklist de Verificação

Execute estes comandos na ordem:

```bash
# 1. Verificar Python
python --version

# 2. Instalar dependências
pip install -r requirements.txt

# 3. Executar testes básicos
python tests/public/run_verification_tests.py

# 4. Executar suite completa
python tests/public/run_all_tests.py

# 5. Verificar código-fonte
Get-Content core/crypto/pqc_crypto.py | Select-Object -First 50

# 6. Acessar testnet
# Abrir no navegador: https://testnet.allianza.tech
```

## 📝 Exemplo de Execução Completa

```powershell
# Navegar para o diretório
cd "C:\Users\notebook\Downloads\Allianza Blockchain"

# Verificar Python
python --version

# Instalar dependências (se necessário)
pip install -r requirements.txt

# Executar testes básicos
python tests/public/run_verification_tests.py

# Executar suite completa
python tests/public/run_all_tests.py

# Verificar resultados
Get-ChildItem proofs\testnet\verification_*.json | Sort-Object LastWriteTime -Descending | Select-Object -First 1 | Get-Content
```

## 🎯 Resultado Esperado

Se tudo estiver funcionando, você deve ver:

1. ✅ **Testes passando** - Todos os testes devem passar
2. ✅ **Código-fonte visível** - Arquivos em `core/` devem estar acessíveis
3. ✅ **Testnet online** - https://testnet.allianza.tech deve estar acessível
4. ✅ **Transações verificáveis** - Links para explorers devem funcionar

---

**Última atualização**: 2025-12-07

**Dúvidas?** Consulte:
- [TESTING.md](TESTING.md) - Guia completo de testes
- [VERIFICATION.md](VERIFICATION.md) - Guia de verificação
- [QUICK_VERIFICATION_GUIDE.md](QUICK_VERIFICATION_GUIDE.md) - Guia rápido

