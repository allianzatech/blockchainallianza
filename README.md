# Allianza Blockchain - Universal Execution Chain (UEC)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Testnet Status](https://img.shields.io/badge/Testnet-Active-success)](https://testnet.allianza.tech)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

> **Blockchain pós-quântica e interoperável** com segurança quântica (QRS-3), interoperabilidade bridge-free e consenso adaptativo (ALZ-NIEV Protocol).

## 🚀 Quick Start

### Para Desenvolvedores

1. **Clone o repositório**
   ```bash
   git clone https://github.com/dieisonmaach-lang/allianzablockchain.git
   cd allianzablockchain
   ```

2. **Instale as dependências**
   ```bash
   pip install -r requirements.txt
   ```

3. **Execute os testes de verificação**
   ```bash
   python tests/public/run_verification_tests.py
   ```

4. **Acesse a Testnet Pública**
   - 🌐 **Dashboard**: https://testnet.allianza.tech
   - 🔍 **Explorer**: https://testnet.allianza.tech/explorer
   - 🚰 **Faucet**: https://testnet.allianza.tech/faucet

### Para Auditores e Verificadores

📋 **Leia primeiro**: [VERIFICATION.md](VERIFICATION.md) - Guia completo de verificação independente

🧪 **Execute testes**: [TESTING.md](TESTING.md) - Como executar e reproduzir os testes

## 📊 Comprovação Técnica

### Provas Técnicas Publicadas

- ✅ **Provas Completas**: [`PROVAS_TECNICAS_COMPLETAS_FINAL.json`](PROVAS_TECNICAS_COMPLETAS_FINAL.json)
- ✅ **Scripts de Teste**: [`tests/public/`](tests/public/) - Todos os scripts que geraram as provas
- ✅ **Testnet Ativa**: https://testnet.allianza.tech - Teste em tempo real

### Tecnologias Validadas

| Tecnologia | Status | Prova |
|------------|--------|------|
| **QRS-3 (PQC)** | ✅ Validado | ML-DSA, SPHINCS+ implementados |
| **Interoperabilidade Bridge-Free** | ✅ Validado | Transferências reais cross-chain |
| **ALZ-NIEV Protocol** | ✅ Validado | Consenso adaptativo funcional |
| **Quantum Security Service** | ✅ Validado | QSS Dashboard ativo |

## 🏗️ Arquitetura

```
allianzablockchain/
├── core/                    # Código-fonte principal
│   ├── consensus/          # ALZ-NIEV Protocol
│   ├── crypto/             # QRS-3, PQC algorithms
│   └── interoperability/   # Bridge-free interop
├── contracts/              # Smart contracts
│   ├── evm/               # Solidity contracts
│   └── proof-of-lock/     # Proof-of-Lock implementation
├── sdk/                    # SDKs públicos
│   ├── qss-sdk/          # Quantum Security Service SDK
│   └── qss-verifier/     # QSS Verifier
├── tests/                  # Testes públicos
│   └── public/           # Scripts de verificação
├── docs/                   # Documentação técnica
└── proofs/                 # Provas técnicas e relatórios
```

## 🔐 Segurança

- 🔒 **Chaves Privadas**: Nunca commitadas (protegidas por `.gitignore`)
- 🛡️ **Segredos**: Gerenciados via variáveis de ambiente
- 📋 **Política de Segurança**: [SECURITY.md](SECURITY.md)

**⚠️ IMPORTANTE**: Este repositório contém código-fonte público. Nunca exponha:
- Chaves privadas
- Seeds de wallets
- Tokens de API
- Credenciais de banco de dados

## 📚 Documentação

- 📖 [Whitepaper Técnico](docs/WHITEPAPER.md)
- 🔍 [API Reference](docs/API_REFERENCE.md)
- 🚀 [Quick Start Guide](docs/QUICK_START.md)
- 🧪 [Testing Guide](TESTING.md)
- ✅ [Verification Guide](VERIFICATION.md)

## 🧪 Testes e Verificação

### Executar Testes Públicos

```bash
# Testes de verificação básicos
python tests/public/run_verification_tests.py

# Testes completos (reproduzir provas técnicas)
python EXECUTAR_TODOS_TESTES_INVESTIDORES.py

# Testes específicos
python tests/public/test_qrs3_verification.py
python tests/public/test_interoperability.py
python tests/public/test_consensus.py
```

### Verificar Provas Técnicas

1. Execute os scripts em [`tests/public/`](tests/public/)
2. Compare os resultados com [`PROVAS_TECNICAS_COMPLETAS_FINAL.json`](PROVAS_TECNICAS_COMPLETAS_FINAL.json)
3. Verifique transações na testnet: https://testnet.allianza.tech/explorer

## 🌐 Testnet Pública

A testnet pública está **ativa e disponível** para testes:

- **URL**: https://testnet.allianza.tech
- **Status**: ✅ Online
- **Features**:
  - Dashboard em tempo real
  - Explorer de blocos e transações
  - Faucet automático
  - QSS Dashboard
  - Verificador de provas

## 🤝 Contribuindo

Veja [CONTRIBUTING.md](CONTRIBUTING.md) para detalhes sobre como contribuir.

## 📄 Licença

Este projeto está licenciado sob a Licença MIT - veja [LICENSE](LICENSE) para detalhes.

## 🔗 Links

- 🌐 **Website**: https://allianza.tech
- 📖 **Whitepaper**: [docs/WHITEPAPER.md](docs/WHITEPAPER.md)
- 🧪 **Testnet**: https://testnet.allianza.tech
- 📧 **Contato**: [Ver SECURITY.md](SECURITY.md) para relatar vulnerabilidades

## ⚠️ Disclaimer

Este é um projeto em desenvolvimento. Use apenas em testnet. Não use chaves privadas reais ou fundos reais durante os testes.

---

**Made with ❤️ by Allianza Team**

