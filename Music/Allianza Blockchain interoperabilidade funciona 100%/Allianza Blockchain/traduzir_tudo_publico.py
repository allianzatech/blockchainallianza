#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🌐 Traduzir TUDO para Inglês - Repositório Público
Traduz nomes de arquivos, títulos e conteúdo completo
"""

import os
import shutil
import subprocess
from pathlib import Path

REPO_PUBLICO = Path("../allianzablockchainpublic")

# Mapeamento de arquivos para renomear
RENAME_FILES = {
    "GUIA_QSS_PARA_OUTRAS_BLOCKCHAINS.md": "QSS_FOR_OTHER_BLOCKCHAINS.md",
    "docs/GUIA_CLI_WINDOWS.md": "docs/CLI_USAGE_GUIDE_WINDOWS.md",
}

# Traduções de conteúdo
TRANSLATIONS = {
    "# 💻 Guia de Uso do CLI - Windows": "# 💻 CLI Usage Guide - Windows",
    "Guia específico para usar o CLI da Allianza Blockchain no Windows PowerShell.": "Specific guide for using Allianza Blockchain CLI on Windows PowerShell.",
    "# 🚀 Quick Start - Allianza Blockchain": "# 🚀 Quick Start - Allianza Blockchain",
    "Guia rápido para começar a usar a Allianza Blockchain.": "Quick guide to get started with Allianza Blockchain.",
    "## 📋 Pré-requisitos": "## 📋 Prerequisites",
    "Python 3.8+": "Python 3.8+",
    "Node.js 14+ (para SDK JavaScript)": "Node.js 14+ (for JavaScript SDK)",
    "Git": "Git",
    "## 🔧 Instalação": "## 🔧 Installation",
    "1. Clone o repositório": "1. Clone the repository",
}

def traduzir_quick_start():
    """Traduz docs/QUICK_START.md completamente"""
    arquivo = REPO_PUBLICO / "docs" / "QUICK_START.md"
    if not arquivo.exists():
        print("⚠️  QUICK_START.md não encontrado")
        return
    
    with open(arquivo, 'r', encoding='utf-8') as f:
        conteudo = f.read()
    
    # Traduções específicas
    traducoes = {
        "# 🚀 Quick Start - Allianza Blockchain": "# 🚀 Quick Start - Allianza Blockchain",
        "Guia rápido para começar a usar a Allianza Blockchain.": "Quick guide to get started with Allianza Blockchain.",
        "## 📋 Pré-requisitos": "## 📋 Prerequisites",
        "Python 3.8+": "Python 3.8+",
        "Node.js 14+ (para SDK JavaScript)": "Node.js 14+ (for JavaScript SDK)",
        "Git": "Git",
        "## 🔧 Instalação": "## 🔧 Installation",
        "1. Clone o repositório": "1. Clone the repository",
        "```bash": "```bash",
        "git clone": "git clone",
        "2. Instale as dependências": "2. Install dependencies",
        "```bash": "```bash",
        "pip install -r requirements.txt": "pip install -r requirements.txt",
        "3. Execute os exemplos": "3. Run examples",
        "```bash": "```bash",
        "python examples/qss_demo.py": "python examples/qss_demo.py",
    }
    
    # Aplicar traduções
    for pt, en in traducoes.items():
        conteudo = conteudo.replace(pt, en)
    
    # Traduções mais genéricas
    conteudo = conteudo.replace("Guia", "Guide")
    conteudo = conteudo.replace("guia", "guide")
    conteudo = conteudo.replace("Instalação", "Installation")
    conteudo = conteudo.replace("instalação", "installation")
    conteudo = conteudo.replace("Pré-requisitos", "Prerequisites")
    conteudo = conteudo.replace("pré-requisitos", "prerequisites")
    conteudo = conteudo.replace("Clone", "Clone")
    conteudo = conteudo.replace("clone", "clone")
    conteudo = conteudo.replace("dependências", "dependencies")
    conteudo = conteudo.replace("Execute", "Run")
    conteudo = conteudo.replace("execute", "run")
    conteudo = conteudo.replace("exemplos", "examples")
    
    with open(arquivo, 'w', encoding='utf-8') as f:
        f.write(conteudo)
    
    print("✅ QUICK_START.md traduzido")

def traduzir_cli_guide():
    """Traduz e renomeia docs/GUIA_CLI_WINDOWS.md"""
    arquivo_antigo = REPO_PUBLICO / "docs" / "GUIA_CLI_WINDOWS.md"
    arquivo_novo = REPO_PUBLICO / "docs" / "CLI_USAGE_GUIDE_WINDOWS.md"
    
    if not arquivo_antigo.exists():
        print("⚠️  GUIA_CLI_WINDOWS.md não encontrado")
        return
    
    with open(arquivo_antigo, 'r', encoding='utf-8') as f:
        conteudo = f.read()
    
    # Traduções
    traducoes = {
        "# 💻 Guia de Uso do CLI - Windows": "# 💻 CLI Usage Guide - Windows",
        "Guia específico para usar o CLI da Allianza Blockchain no Windows PowerShell.": "Specific guide for using Allianza Blockchain CLI on Windows PowerShell.",
        "## ⚠️ IMPORTANTE: Não use `<` e `>`": "## ⚠️ IMPORTANT: Do not use `<` and `>`",
        "No Windows PowerShell, `<` e `>` são redirecionadores.": "In Windows PowerShell, `<` and `>` are redirectors.",
        "**NÃO use** esses caracteres nos comandos!": "**DO NOT use** these characters in commands!",
        "**❌ ERRADO:**": "**❌ WRONG:**",
        "**✅ CORRETO:**": "**✅ CORRECT:**",
    }
    
    for pt, en in traducoes.items():
        conteudo = conteudo.replace(pt, en)
    
    # Salvar com novo nome
    with open(arquivo_novo, 'w', encoding='utf-8') as f:
        f.write(conteudo)
    
    # Remover arquivo antigo
    if arquivo_antigo.exists():
        arquivo_antigo.unlink()
    
    print("✅ GUIA_CLI_WINDOWS.md traduzido e renomeado para CLI_USAGE_GUIDE_WINDOWS.md")

def renomear_arquivos():
    """Renomeia arquivos com nomes em português"""
    print("\n📝 Renomeando arquivos...")
    
    for antigo, novo in RENAME_FILES.items():
        arquivo_antigo = REPO_PUBLICO / antigo
        arquivo_novo = REPO_PUBLICO / novo
        
        if arquivo_antigo.exists() and not arquivo_novo.exists():
            arquivo_antigo.rename(arquivo_novo)
            print(f"✅ {antigo} → {novo}")
        elif arquivo_antigo.exists():
            print(f"⚠️  {novo} já existe, mantendo ambos")

def atualizar_referencias():
    """Atualiza referências a arquivos renomeados"""
    print("\n🔗 Atualizando referências...")
    
    # Arquivos para atualizar
    arquivos_para_atualizar = [
        "README.md",
        "docs/QUICK_START.md",
        "examples/README.md",
    ]
    
    atualizacoes = {
        "GUIA_QSS_PARA_OUTRAS_BLOCKCHAINS.md": "QSS_FOR_OTHER_BLOCKCHAINS.md",
        "docs/GUIA_CLI_WINDOWS.md": "docs/CLI_USAGE_GUIDE_WINDOWS.md",
        "GUIA_CLI_WINDOWS.md": "CLI_USAGE_GUIDE_WINDOWS.md",
    }
    
    for arquivo_nome in arquivos_para_atualizar:
        arquivo = REPO_PUBLICO / arquivo_nome
        if arquivo.exists():
            with open(arquivo, 'r', encoding='utf-8') as f:
                conteudo = f.read()
            
            conteudo_original = conteudo
            for antigo, novo in atualizacoes.items():
                conteudo = conteudo.replace(antigo, novo)
            
            if conteudo != conteudo_original:
                with open(arquivo, 'w', encoding='utf-8') as f:
                    f.write(conteudo)
                print(f"✅ Referências atualizadas em {arquivo_nome}")

def verificar_pastas_faltantes():
    """Verifica se há pastas faltando"""
    print("\n📁 Verificando pastas...")
    
    pastas_esperadas = [
        "examples",
        "tests",
        "docs",
        "qss-sdk",
        "templates/testnet",
        ".github",
    ]
    
    for pasta in pastas_esperadas:
        caminho = REPO_PUBLICO / pasta
        if caminho.exists():
            print(f"✅ {pasta}/ existe")
        else:
            print(f"⚠️  {pasta}/ NÃO encontrado")

def main():
    print("=" * 70)
    print("🌐 TRADUZIR TUDO PARA INGLÊS - REPOSITÓRIO PÚBLICO")
    print("=" * 70)
    print()
    
    if not REPO_PUBLICO.exists():
        print(f"❌ Repositório público não encontrado: {REPO_PUBLICO}")
        return
    
    # Executar tarefas
    traduzir_quick_start()
    traduzir_cli_guide()
    renomear_arquivos()
    atualizar_referencias()
    verificar_pastas_faltantes()
    
    print()
    print("=" * 70)
    print("✅ TRADUÇÃO COMPLETA CONCLUÍDA!")
    print("=" * 70)
    print()
    print("📋 Próximos passos:")
    print("   1. Execute: cd ../allianzablockchainpublic")
    print("   2. Execute: git add .")
    print("   3. Execute: git commit -m 'docs: translate all files to English'")
    print("   4. Execute: git push origin master")
    print()

if __name__ == "__main__":
    main()

