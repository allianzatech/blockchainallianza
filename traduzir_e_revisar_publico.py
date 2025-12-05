#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🌐 Traduzir e Revisar Repositório Público
Traduz títulos e conteúdo para inglês, adiciona arquivos faltantes
"""

import os
import shutil
import subprocess
from pathlib import Path

REPO_PRIVADO = Path(".")
REPO_PUBLICO = Path("../allianzablockchainpublic")

def traduzir_guia_qss():
    """Traduz GUIA_QSS_PARA_OUTRAS_BLOCKCHAINS.md para inglês"""
    print("📝 Traduzindo GUIA_QSS_PARA_OUTRAS_BLOCKCHAINS.md...")
    
    # Ler arquivo original
    arquivo_original = REPO_PRIVADO / "GUIA_QSS_PARA_OUTRAS_BLOCKCHAINS.md"
    if not arquivo_original.exists():
        print("⚠️  Arquivo não encontrado")
        return
    
    # Criar versão traduzida
    arquivo_traduzido = REPO_PUBLICO / "QSS_FOR_OTHER_BLOCKCHAINS.md"
    arquivo_traduzido.parent.mkdir(parents=True, exist_ok=True)
    
    # Traduzir conteúdo básico (títulos principais)
    with open(arquivo_original, 'r', encoding='utf-8') as f:
        conteudo = f.read()
    
    # Traduções básicas
    traducoes = {
        "# 🔐 Guia Completo: QSS para Outras Blockchains": "# 🔐 Complete Guide: QSS for Other Blockchains",
        "## 📋 Índice": "## 📋 Index",
        "## 🎯 Como o QSS Funciona": "## 🎯 How QSS Works",
        "### O Que é o QSS?": "### What is QSS?",
        "### Como Funciona na Prática?": "### How Does It Work in Practice?",
        "## 📋 Como Obter Hashes de Transações": "## 📋 How to Get Transaction Hashes",
        "## 🧪 Como Testar com Diferentes Blockchains": "## 🧪 How to Test with Different Blockchains",
        "## 💡 Exemplos Práticos": "## 💡 Practical Examples",
        "## 🔗 Ancoragem de Provas": "## 🔗 Proof Anchoring",
        "## ❓ FAQ": "## ❓ FAQ",
    }
    
    for pt, en in traducoes.items():
        conteudo = conteudo.replace(pt, en)
    
    with open(arquivo_traduzido, 'w', encoding='utf-8') as f:
        f.write(conteudo)
    
    print("✅ GUIA_QSS_PARA_OUTRAS_BLOCKCHAINS.md traduzido para QSS_FOR_OTHER_BLOCKCHAINS.md")

def copiar_examples_e_tests():
    """Copia diretórios examples/ e tests/ se existirem"""
    print("\n📦 Verificando examples/ e tests/...")
    
    # Verificar examples/
    examples_privado = REPO_PRIVADO / "examples"
    examples_publico = REPO_PUBLICO / "examples"
    
    if examples_privado.exists():
        print("✅ Copiando examples/...")
        if examples_publico.exists():
            shutil.rmtree(examples_publico)
        shutil.copytree(examples_privado, examples_publico, ignore=shutil.ignore_patterns('__pycache__', '*.pyc', '.git'))
        print("✅ examples/ copiado")
    else:
        print("⚠️  examples/ não encontrado no privado")
    
    # Verificar tests/
    tests_privado = REPO_PRIVADO / "tests"
    tests_publico = REPO_PUBLICO / "tests"
    
    if tests_privado.exists():
        print("✅ Copiando tests/...")
        if tests_publico.exists():
            shutil.rmtree(tests_publico)
        shutil.copytree(tests_privado, tests_publico, ignore=shutil.ignore_patterns('__pycache__', '*.pyc', '.git'))
        print("✅ tests/ copiado")
    else:
        print("⚠️  tests/ não encontrado no privado")

def traduzir_docs():
    """Traduz títulos em arquivos docs/"""
    print("\n📚 Traduzindo títulos em docs/...")
    
    docs_publico = REPO_PUBLICO / "docs"
    if not docs_publico.exists():
        print("⚠️  docs/ não encontrado")
        return
    
    # Traduzir GUIA_CLI_WINDOWS.md
    guia_cli = docs_publico / "GUIA_CLI_WINDOWS.md"
    if guia_cli.exists():
        with open(guia_cli, 'r', encoding='utf-8') as f:
            conteudo = f.read()
        
        # Traduzir título
        conteudo = conteudo.replace(
            "# 💻 Guia de Uso do CLI - Windows",
            "# 💻 CLI Usage Guide - Windows"
        )
        
        with open(guia_cli, 'w', encoding='utf-8') as f:
            f.write(conteudo)
        
        print("✅ GUIA_CLI_WINDOWS.md traduzido")

def atualizar_readme():
    """Atualiza README.md com referências em inglês"""
    print("\n📝 Atualizando README.md...")
    
    readme = REPO_PUBLICO / "README.md"
    if not readme.exists():
        print("⚠️  README.md não encontrado")
        return
    
    with open(readme, 'r', encoding='utf-8') as f:
        conteudo = f.read()
    
    # Atualizar referências
    conteudo = conteudo.replace(
        "- **QSS Integration:** `GUIA_QSS_PARA_OUTRAS_BLOCKCHAINS.md`",
        "- **QSS Integration:** `QSS_FOR_OTHER_BLOCKCHAINS.md`"
    )
    
    with open(readme, 'w', encoding='utf-8') as f:
        f.write(conteudo)
    
    print("✅ README.md atualizado")

def criar_license():
    """Cria LICENSE se não existir"""
    print("\n📄 Verificando LICENSE...")
    
    license_file = REPO_PUBLICO / "LICENSE"
    if not license_file.exists():
        mit_license = """MIT License

Copyright (c) 2025 Allianza Blockchain

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
        with open(license_file, 'w', encoding='utf-8') as f:
            f.write(mit_license)
        print("✅ LICENSE criado")
    else:
        print("ℹ️  LICENSE já existe")

def criar_changelog():
    """Cria CHANGELOG.md se não existir"""
    print("\n📋 Verificando CHANGELOG.md...")
    
    changelog = REPO_PUBLICO / "CHANGELOG.md"
    if not changelog.exists():
        conteudo = """# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-12-05

### Added
- Initial public repository release
- QSS SDK (TypeScript) published to npm
- 41 technical proofs documentation
- Testnet infrastructure
- Developer Hub and Leaderboard
- Cross-chain interoperability examples
- Post-quantum cryptography implementation (ML-DSA, SPHINCS+, QRS-3)

### Security
- Core blockchain implementation remains private
- All sensitive data excluded from public repository
"""
        with open(changelog, 'w', encoding='utf-8') as f:
            f.write(conteudo)
        print("✅ CHANGELOG.md criado")
    else:
        print("ℹ️  CHANGELOG.md já existe")

def main():
    print("=" * 70)
    print("🌐 TRADUZIR E REVISAR REPOSITÓRIO PÚBLICO")
    print("=" * 70)
    print()
    
    # Verificar se repositório público existe
    if not REPO_PUBLICO.exists():
        print(f"❌ Repositório público não encontrado: {REPO_PUBLICO}")
        return
    
    # Executar tarefas
    traduzir_guia_qss()
    copiar_examples_e_tests()
    traduzir_docs()
    atualizar_readme()
    criar_license()
    criar_changelog()
    
    print()
    print("=" * 70)
    print("✅ REVISÃO E TRADUÇÃO CONCLUÍDA!")
    print("=" * 70)
    print()
    print("📋 Próximos passos:")
    print("   1. Execute: python sincronizar_repositorio_publico.py")
    print("   2. O script vai fazer commit e push automático")
    print()

if __name__ == "__main__":
    main()

