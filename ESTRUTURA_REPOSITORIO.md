# 📁 Estrutura do Repositório - Allianza Blockchain

## 🎯 Estrutura Profissional

```
allianzablockchain/
├── 📄 README.md                    # Documentação principal
├── 📄 LICENSE                       # Licença MIT
├── 📄 CHANGELOG.md                 # Histórico de mudanças
├── 📄 CONTRIBUTING.md              # Guia para contribuidores
├── 📄 CODE_OF_CONDUCT.md           # Código de conduta
├── 📄 SECURITY.md                  # Política de segurança
├── 📄 ROADMAP.md                   # Roadmap do projeto
│
├── 🔐 core/                        # Código-fonte principal (PUBLIC)
│   ├── crypto/                    # QRS-3, PQC
│   │   ├── quantum_security.py
│   │   ├── pqc_crypto.py
│   │   └── README.md
│   ├── consensus/                 # ALZ-NIEV Protocol
│   │   ├── adaptive_consensus.py
│   │   ├── alz_niev_interoperability.py
│   │   └── README.md
│   └── interoperability/         # Bridge-Free Interop
│       ├── bridge_free_interop.py
│       ├── proof_of_lock.py
│       └── README.md
│
├── 📜 contracts/                   # Smart Contracts
│   ├── evm/                       # Solidity contracts
│   └── README.md
│
├── 🧪 tests/                       # Testes públicos
│   └── public/                    # Scripts de verificação
│       ├── run_verification_tests.py
│       ├── run_all_tests.py
│       └── README.md
│
├── 📚 docs/                        # Documentação técnica
│   ├── ARCHITECTURE.md
│   ├── API_REFERENCE.md
│   └── QUICK_START.md
│
├── 💡 examples/                    # Exemplos de código
│   ├── basic_wallet.py
│   ├── qrs3_signature.py
│   └── cross_chain_transfer.py
│
├── 🔧 scripts/                     # Scripts auxiliares
│   ├── fix_encryption_key.py
│   └── keep_alive.py
│
├── 📊 proofs/                      # Provas técnicas
│   └── testnet/                   # Provas da testnet
│
├── 📦 sdk/                         # SDKs públicos
│   ├── qss-sdk/                   # Quantum Security Service SDK
│   └── qss-verifier/              # QSS Verifier
│
├── 🗄️ archive/                     # Documentação histórica
│   └── (arquivos antigos de documentação)
│
├── 🌐 templates/                   # Templates HTML
│   └── testnet/
│
├── 🎨 static/                      # Arquivos estáticos
│   ├── css/
│   └── js/
│
└── 🔒 secrets/                     # NUNCA commitado (gitignore)
    └── encryption_key.key
```

## 📋 Arquivos Principais na Raiz

### Documentação Essencial
- `README.md` - Ponto de entrada principal
- `LICENSE` - Licença MIT
- `CHANGELOG.md` - Histórico de versões
- `CONTRIBUTING.md` - Como contribuir
- `CODE_OF_CONDUCT.md` - Código de conduta
- `SECURITY.md` - Política de segurança
- `ROADMAP.md` - Roadmap do projeto

### Documentação Técnica
- `TESTING.md` - Guia de testes
- `VERIFICATION.md` - Guia de verificação
- `QUICK_VERIFICATION_GUIDE.md` - Guia rápido
- `RESPONSE_TO_ANALYSIS.md` - Respostas a análises
- `WHAT_IS_REAL.md` - O que é real vs simulado
- `RWA_TOKENIZATION.md` - Tokenização RWA

### Provas Técnicas
- `COMPLETE_TECHNICAL_PROOFS_FINAL.json` - 41 provas técnicas
- `VERIFIABLE_ON_CHAIN_PROOFS.md` - Provas on-chain verificáveis

### Configuração
- `.gitignore` - Arquivos ignorados
- `requirements.txt` - Dependências Python
- `package.json` - Dependências Node.js
- `Procfile` - Configuração Render
- `runtime.txt` - Versão Python

## 🔒 Arquivos Protegidos (não commitados)

- `secrets/` - Chaves privadas e segredos
- `pqc_keys/` - Chaves PQC privadas
- `.env` - Variáveis de ambiente
- `*.db`, `*.sqlite` - Bancos de dados
- `*.log` - Logs
- `__pycache__/` - Cache Python

## 📊 Organização por Tipo

### Código-Fonte
- `core/` - Implementações principais
- `allianza_blockchain.py` - Classe principal da blockchain
- `testnet_routes.py` - Rotas da testnet
- `db_manager.py` - Gerenciador de banco de dados

### Testes
- `tests/public/` - Testes públicos e verificáveis
- `tests/` - Testes internos (se houver)

### Documentação
- `docs/` - Documentação técnica detalhada
- `archive/` - Documentação histórica/antiga

### Scripts
- `scripts/` - Scripts auxiliares e utilitários

---

**Última atualização:** 2025-12-08

