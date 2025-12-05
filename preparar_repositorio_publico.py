#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔒 Script para Preparar Repositório Público de Validação
Copia apenas arquivos seguros, excluindo chaves privadas e código proprietário
"""

import os
import shutil
import json
from pathlib import Path

# Diretório de origem
SOURCE_DIR = Path(".")
# Diretório de destino (repositório público)
PUBLIC_DIR = Path("../allianzablockchain-public")

# Arquivos e diretórios SEGUROS para copiar
SAFE_FILES = [
    # Documentação
    "WHITEPAPER_ALLIANZA_BLOCKCHAIN.md",
    "README.md",
    "LICENSE",
    ".gitignore",
    
    # Provas Técnicas
    "PROVAS_TECNICAS_COMPLETAS_FINAL.json",
    "PROVAS_TECNICAS_COMPLETAS_FINAL_EN.json",
    
    # Documentação Técnica
    "docs/API_REFERENCE.md",
    "docs/QUICK_START.md",
    "docs/GUIA_CLI_WINDOWS.md",
    "GUIA_QSS_PARA_OUTRAS_BLOCKCHAINS.md",
    
    # SDK (completo)
    "qss-sdk/",
    
    # Templates (apenas UI)
    "templates/testnet/",
    
    # Configuração
    "render.yaml",
    "Procfile",
    "wsgi_optimized.py",
]

# Diretórios SEGUROS para copiar
SAFE_DIRS = [
    "docs/",
    "qss-sdk/",
    "templates/testnet/",
    "proofs/testnet/critical_tests/",  # Apenas resultados JSON
]

# Arquivos e padrões a EXCLUIR (segurança)
EXCLUDE_PATTERNS = [
    # Chaves privadas
    "*_PRIVATE_KEY*",
    "*private_key*",
    "*PRIVATE_KEY*",
    
    # Arquivos de ambiente
    ".env",
    ".env.*",
    "*_VARIAVEIS_RENDER*",
    "env_limpo_para_render.txt",
    "VARIAVEIS_RENDER_COPIAR_COLAR.txt",
    
    # Segredos
    "*secret*",
    "*password*",
    "*SECRET*",
    "*PASSWORD*",
    
    # API Keys
    "*API_TOKEN*",
    "*API_KEY*",
    "*INFURA*",
    "*BLOCKCYPHER*",
    
    # Core proprietário
    "alz_niev_interoperability.py",
    "quantum_security.py",
    "quantum_security_REAL.py",
    "real_cross_chain_bridge.py",
    "allianza_blockchain.py",
    
    # Chaves PQC
    "pqc_keys/",
    "*.bin",  # Arquivos binários de chaves
    
    # Configurações sensíveis
    "secrets/",
    "secret_manager.py",
    
    # Banco de dados
    "*.db",
    "*.sqlite",
    "*.sqlite3",
    
    # Logs
    "*.log",
    "logs/",
    
    # Cache
    "__pycache__/",
    ".pytest_cache/",
    ".cache/",
    
    # Node modules
    "node_modules/",
    
    # Build
    "dist/",
    "build/",
    "*.egg-info/",
]

def should_exclude(file_path):
    """Verifica se arquivo deve ser excluído"""
    file_str = str(file_path)
    file_name = file_path.name
    
    # Verificar padrões de exclusão
    for pattern in EXCLUDE_PATTERNS:
        if pattern in file_str or pattern in file_name:
            return True
    
    # Verificar se contém chaves privadas no conteúdo
    if file_path.is_file() and file_path.suffix in ['.py', '.txt', '.md', '.json', '.yaml', '.yml']:
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read().lower()
                dangerous_keywords = [
                    'private_key',
                    'api_key',
                    'api_token',
                    'secret',
                    'password',
                    'infura',
                    'blockcypher',
                ]
                for keyword in dangerous_keywords:
                    if keyword in content and 'test' not in file_str.lower():
                        # Verificar se não é apenas documentação
                        if not any(doc in file_str for doc in ['README', 'DOC', 'GUIA', 'EXEMPLO']):
                            return True
        except:
            pass
    
    return False

def copy_safe_file(source, dest):
    """Copia arquivo se for seguro"""
    if should_exclude(source):
        print(f"⚠️  EXCLUÍDO (segurança): {source}")
        return False
    
    try:
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, dest)
        print(f"✅ Copiado: {source} -> {dest}")
        return True
    except Exception as e:
        print(f"❌ Erro ao copiar {source}: {e}")
        return False

def copy_safe_directory(source_dir, dest_dir):
    """Copia diretório recursivamente, excluindo arquivos perigosos"""
    if not source_dir.exists():
        print(f"⚠️  Diretório não existe: {source_dir}")
        return
    
    for item in source_dir.rglob('*'):
        if item.is_file():
            # Calcular caminho relativo
            rel_path = item.relative_to(source_dir)
            dest_path = dest_dir / rel_path
            
            # Verificar se deve excluir
            if not should_exclude(item):
                copy_safe_file(item, dest_path)
            else:
                print(f"⚠️  EXCLUÍDO: {item}")

def create_public_readme():
    """Cria README profissional para repositório público"""
    readme_content = """# 🔐 Allianza Blockchain - Quantum-Safe Blockchain

[![npm version](https://img.shields.io/npm/v/allianza-qss-js)](https://www.npmjs.com/package/allianza-qss-js)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Testnet](https://img.shields.io/badge/Testnet-Active-green)](https://testnet.allianza.tech)

## 🌟 Sobre

Allianza Blockchain é uma blockchain pós-quântica com interoperabilidade cross-chain e segurança quântica integrada.

### ✨ Características Principais

- 🔐 **Segurança Pós-Quântica**: Proteção contra computadores quânticos
- 🌉 **Interoperabilidade Cross-Chain**: Conecta Bitcoin, Ethereum, Polygon e mais
- 🚀 **Quantum Security Service (QSS)**: API pública para outras blockchains
- ✅ **41 Provas Técnicas**: Validação completa de todas as funcionalidades

## 🚀 Quick Start

### Instalar SDK

```bash
npm install allianza-qss-js
```

### Gerar Prova Quântica

```javascript
import QSS from 'allianza-qss-js';

const proof = await QSS.generateProof('bitcoin', txHash);
console.log('Proof Hash:', proof.proof_hash);
```

## 📚 Documentação

- [API Reference](docs/API_REFERENCE.md)
- [Quick Start Guide](docs/QUICK_START.md)
- [QSS para Outras Blockchains](GUIA_QSS_PARA_OUTRAS_BLOCKCHAINS.md)

## 🧪 Testnet

Acesse nossa testnet pública: **https://testnet.allianza.tech**

- ✅ Faucet para testar
- ✅ Explorer de blocos
- ✅ API QSS funcional
- ✅ 41 testes técnicos disponíveis

## 📊 Provas Técnicas

Este repositório contém as **41 provas técnicas** que validam todas as funcionalidades da Allianza Blockchain:

- ✅ Geração e verificação de assinaturas ML-DSA
- ✅ Interoperabilidade cross-chain
- ✅ Quantum Security Service (QSS)
- ✅ Validação de provas quânticas
- ✅ E muito mais...

Veja os resultados completos em: `proofs/PROVAS_TECNICAS_COMPLETAS_FINAL.json`

## 🔗 Links Úteis

- **Testnet**: https://testnet.allianza.tech
- **npm SDK**: https://www.npmjs.com/package/allianza-qss-js
- **Developer Hub**: https://testnet.allianza.tech/developer-hub
- **Leaderboard**: https://testnet.allianza.tech/leaderboard

## 📦 Estrutura do Repositório

```
allianzablockchain/
├── docs/              # Documentação técnica
├── proofs/            # 41 provas técnicas
├── qss-sdk/          # SDK JavaScript/TypeScript
├── templates/        # Templates frontend
└── examples/          # Exemplos de uso
```

## 🤝 Contribuindo

Contribuições são bem-vindas! Veja [CONTRIBUTING.md](CONTRIBUTING.md) para mais detalhes.

## 📄 Licença

Este projeto está licenciado sob a MIT License - veja [LICENSE](LICENSE) para detalhes.

## ⚠️ Aviso

Este repositório contém apenas código público e documentação. O core da blockchain e algoritmos proprietários permanecem privados.

---

**Desenvolvido com ❤️ pela equipe Allianza Blockchain**
"""
    
    readme_path = PUBLIC_DIR / "README.md"
    readme_path.parent.mkdir(parents=True, exist_ok=True)
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(readme_content)
    print(f"✅ README criado: {readme_path}")

def main():
    """Função principal"""
    print("=" * 70)
    print("🔒 PREPARANDO REPOSITÓRIO PÚBLICO DE VALIDAÇÃO")
    print("=" * 70)
    print()
    
    # Criar diretório público
    PUBLIC_DIR.mkdir(parents=True, exist_ok=True)
    print(f"📁 Diretório público: {PUBLIC_DIR}")
    print()
    
    # Copiar arquivos seguros
    print("📋 Copiando arquivos seguros...")
    print()
    
    for item in SAFE_FILES:
        source = SOURCE_DIR / item
        if source.exists():
            if source.is_file():
                dest = PUBLIC_DIR / item
                copy_safe_file(source, dest)
            elif source.is_dir():
                dest = PUBLIC_DIR / item
                copy_safe_directory(source, dest)
        else:
            print(f"⚠️  Não encontrado: {source}")
    
    print()
    print("📋 Copiando diretórios seguros...")
    print()
    
    for dir_path in SAFE_DIRS:
        source = SOURCE_DIR / dir_path
        if source.exists():
            dest = PUBLIC_DIR / dir_path
            copy_safe_directory(source, dest)
        else:
            print(f"⚠️  Diretório não encontrado: {source}")
    
    # Criar README profissional
    print()
    print("📝 Criando README profissional...")
    create_public_readme()
    
    # Criar .gitignore para repositório público
    gitignore_content = """# Python
__pycache__/
*.py[cod]
*.so

# Environment
.env
.env.*

# IDE
.vscode/
.idea/

# Logs
*.log

# Database
*.db
*.sqlite

# Node
node_modules/

# Build
dist/
build/
"""
    gitignore_path = PUBLIC_DIR / ".gitignore"
    with open(gitignore_path, 'w', encoding='utf-8') as f:
        f.write(gitignore_content)
    print(f"✅ .gitignore criado: {gitignore_path}")
    
    print()
    print("=" * 70)
    print("✅ REPOSITÓRIO PÚBLICO PREPARADO COM SUCESSO!")
    print("=" * 70)
    print()
    print(f"📁 Localização: {PUBLIC_DIR.absolute()}")
    print()
    print("⚠️  PRÓXIMOS PASSOS:")
    print("1. Revisar manualmente os arquivos copiados")
    print("2. Verificar que nenhum segredo foi incluído")
    print("3. Fazer commit e push para o repositório público")
    print()
    print("🔗 Repositório: https://github.com/allianzatoken-png/allianzablockchain.git")
    print()

if __name__ == "__main__":
    main()

