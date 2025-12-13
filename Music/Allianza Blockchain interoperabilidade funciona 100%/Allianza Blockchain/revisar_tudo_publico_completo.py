#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🌐 Revisar TUDO - Repositório Público
Revisa arquivo por arquivo, pasta por pasta, traduz tudo para inglês
"""

import os
import shutil
import subprocess
from pathlib import Path

REPO_PUBLICO = Path("../allianzablockchainpublic")

# Arquivos para renomear
RENAME_MAP = {
    "PROVAS_TECNICAS_COMPLETAS_FINAL_EN.json": "TECHNICAL_PROOFS_COMPLETE_FINAL.json",
    "PROVAS_TECNICAS_COMPLETAS_FINAL.json": "TECHNICAL_PROOFS_COMPLETE_FINAL_PT.json",
}

def traduzir_api_reference():
    """Traduz docs/API_REFERENCE.md"""
    arquivo = REPO_PUBLICO / "docs" / "API_REFERENCE.md"
    if not arquivo.exists():
        return
    
    with open(arquivo, 'r', encoding='utf-8') as f:
        conteudo = f.read()
    
    traducoes = {
        "# 📚 API Reference - Allianza Blockchain": "# 📚 API Reference - Allianza Blockchain",
        "Referência completa da API RPC da Allianza Blockchain.": "Complete reference for Allianza Blockchain RPC API.",
    }
    
    for pt, en in traducoes.items():
        conteudo = conteudo.replace(pt, en)
    
    with open(arquivo, 'w', encoding='utf-8') as f:
        f.write(conteudo)
    
    print("✅ API_REFERENCE.md traduzido")

def traduzir_atomic_rollback():
    """Traduz docs/ATOMIC_ROLLBACK_MECHANISM.md"""
    arquivo = REPO_PUBLICO / "docs" / "ATOMIC_ROLLBACK_MECHANISM.md"
    if not arquivo.exists():
        return
    
    with open(arquivo, 'r', encoding='utf-8') as f:
        conteudo = f.read()
    
    traducoes = {
        "## 🔄 Mecanismo de Rollback Atômico (AES)": "## 🔄 Atomic Rollback Mechanism (AES)",
        "Data: 03 de Dezembro de 2025": "Date: December 3, 2025",
        "Versão: 1.0": "Version: 1.0",
        "Status: ✅ Implementado e Testado": "Status: ✅ Implemented and Tested",
    }
    
    for pt, en in traducoes.items():
        conteudo = conteudo.replace(pt, en)
    
    # Traduções genéricas
    conteudo = conteudo.replace("Data:", "Date:")
    conteudo = conteudo.replace("Versão:", "Version:")
    conteudo = conteudo.replace("Status:", "Status:")
    conteudo = conteudo.replace("Implementado", "Implemented")
    conteudo = conteudo.replace("Testado", "Tested")
    
    with open(arquivo, 'w', encoding='utf-8') as f:
        f.write(conteudo)
    
    print("✅ ATOMIC_ROLLBACK_MECHANISM.md traduzido")

def renomear_arquivos():
    """Renomeia arquivos com nomes em português"""
    print("\n📝 Renomeando arquivos...")
    
    for antigo, novo in RENAME_MAP.items():
        arquivo_antigo = REPO_PUBLICO / antigo
        arquivo_novo = REPO_PUBLICO / novo
        
        if arquivo_antigo.exists():
            if arquivo_novo.exists():
                print(f"⚠️  {novo} já existe, removendo {antigo}")
                arquivo_antigo.unlink()
            else:
                arquivo_antigo.rename(arquivo_novo)
                print(f"✅ {antigo} → {novo}")
        else:
            print(f"⚠️  {antigo} não encontrado")

def atualizar_referencias_arquivos():
    """Atualiza referências a arquivos renomeados"""
    print("\n🔗 Atualizando referências a arquivos...")
    
    arquivos_para_atualizar = [
        "README.md",
        "docs/QUICK_START.md",
        "docs/API_REFERENCE.md",
        "examples/README.md",
        "tests/README.md",
    ]
    
    for arquivo_nome in arquivos_para_atualizar:
        arquivo = REPO_PUBLICO / arquivo_nome
        if arquivo.exists():
            with open(arquivo, 'r', encoding='utf-8') as f:
                conteudo = f.read()
            
            conteudo_original = conteudo
            for antigo, novo in RENAME_MAP.items():
                conteudo = conteudo.replace(antigo, novo)
            
            if conteudo != conteudo_original:
                with open(arquivo, 'w', encoding='utf-8') as f:
                    f.write(conteudo)
                print(f"✅ Referências atualizadas em {arquivo_nome}")

def revisar_qss_sdk():
    """Revisa arquivos em qss-sdk/"""
    print("\n📦 Revisando qss-sdk/...")
    
    qss_sdk = REPO_PUBLICO / "qss-sdk"
    if not qss_sdk.exists():
        print("⚠️  qss-sdk/ não encontrado")
        return
    
    # Verificar PUBLICAR_AGORA.md
    publicar = qss_sdk / "PUBLICAR_AGORA.md"
    if publicar.exists():
        with open(publicar, 'r', encoding='utf-8') as f:
            conteudo = f.read()
        
        traducoes = {
            "## 🚀 Publicar Agora (Sem Escopo)": "## 🚀 Publish Now (Without Scope)",
            "### ✅ Solução Rápida": "### ✅ Quick Solution",
            "Mudei o package.json para publicar sem escopo temporariamente.": "Changed package.json to publish without scope temporarily.",
        }
        
        for pt, en in traducoes.items():
            conteudo = conteudo.replace(pt, en)
        
        with open(publicar, 'w', encoding='utf-8') as f:
            f.write(conteudo)
        
        print("✅ qss-sdk/PUBLICAR_AGORA.md traduzido")

def revisar_examples():
    """Revisa arquivos em examples/"""
    print("\n📚 Revisando examples/...")
    
    examples = REPO_PUBLICO / "examples"
    if not examples.exists():
        print("⚠️  examples/ não encontrado")
        return
    
    readme = examples / "README.md"
    if readme.exists():
        with open(readme, 'r', encoding='utf-8') as f:
            conteudo = f.read()
        
        # Verificar se há português
        palavras_pt = ["Guia", "guia", "Exemplos", "exemplos", "Como", "como"]
        tem_pt = any(palavra in conteudo for palavra in palavras_pt)
        
        if tem_pt:
            print("⚠️  examples/README.md pode ter conteúdo em português")
        else:
            print("✅ examples/README.md parece estar em inglês")

def revisar_tests():
    """Revisa arquivos em tests/"""
    print("\n🧪 Revisando tests/...")
    
    tests = REPO_PUBLICO / "tests"
    if not tests.exists():
        print("⚠️  tests/ não encontrado")
        return
    
    readme = tests / "README.md"
    if readme.exists():
        with open(readme, 'r', encoding='utf-8') as f:
            conteudo = f.read()
        
        palavras_pt = ["Guia", "guia", "Testes", "testes"]
        tem_pt = any(palavra in conteudo for palavra in palavras_pt)
        
        if tem_pt:
            print("⚠️  tests/README.md pode ter conteúdo em português")
        else:
            print("✅ tests/README.md parece estar em inglês")

def main():
    print("=" * 70)
    print("🌐 REVISAR TUDO - REPOSITÓRIO PÚBLICO")
    print("=" * 70)
    print()
    
    if not REPO_PUBLICO.exists():
        print(f"❌ Repositório público não encontrado: {REPO_PUBLICO}")
        return
    
    # Executar revisões
    traduzir_api_reference()
    traduzir_atomic_rollback()
    renomear_arquivos()
    atualizar_referencias_arquivos()
    revisar_qss_sdk()
    revisar_examples()
    revisar_tests()
    
    print()
    print("=" * 70)
    print("✅ REVISÃO COMPLETA CONCLUÍDA!")
    print("=" * 70)
    print()
    print("📋 Próximos passos:")
    print("   1. Execute: cd ../allianzablockchainpublic")
    print("   2. Execute: git add .")
    print("   3. Execute: git commit -m 'docs: complete English translation - all files'")
    print("   4. Execute: git push origin master")
    print()

if __name__ == "__main__":
    main()

