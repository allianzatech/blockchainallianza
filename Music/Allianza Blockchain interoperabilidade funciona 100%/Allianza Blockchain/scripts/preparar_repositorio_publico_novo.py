#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🚀 Preparar Novo Repositório Público
Cria e configura o repositório público na mesma conta
"""

import os
import subprocess
from pathlib import Path

REPO_PRIVADO = Path(".")
REPO_PUBLICO = Path("../allianzablockchainpublic")
GIT_REPO_PUBLICO = "https://github.com/dieisonmaach-lang/allianzablockchainpublic.git"

def main():
    print("=" * 70)
    print("🚀 PREPARAR NOVO REPOSITÓRIO PÚBLICO")
    print("=" * 70)
    print()
    print(f"📁 Repositório privado: {REPO_PRIVADO.absolute()}")
    print(f"📁 Repositório público: {REPO_PUBLICO.absolute()}")
    print(f"🔗 URL Git: {GIT_REPO_PUBLICO}")
    print()
    
    # Criar diretório se não existir
    if not REPO_PUBLICO.exists():
        print("📦 Criando diretório do repositório público...")
        REPO_PUBLICO.mkdir(parents=True, exist_ok=True)
        print("✅ Diretório criado")
    else:
        print("ℹ️  Diretório já existe")
    
    # Inicializar Git
    if not (REPO_PUBLICO / ".git").exists():
        print()
        print("🔧 Inicializando Git...")
        subprocess.run(["git", "init"], cwd=REPO_PUBLICO, check=True)
        print("✅ Git inicializado")
    else:
        print("ℹ️  Git já inicializado")
    
    # Configurar remote
    print()
    print("🔗 Configurando remote...")
    result = subprocess.run(
        ["git", "remote", "-v"],
        cwd=REPO_PUBLICO,
        capture_output=True,
        text=True
    )
    
    if "origin" not in result.stdout:
        subprocess.run(
            ["git", "remote", "add", "origin", GIT_REPO_PUBLICO],
            cwd=REPO_PUBLICO,
            check=True
        )
        print("✅ Remote configurado")
    else:
        # Atualizar remote
        subprocess.run(
            ["git", "remote", "set-url", "origin", GIT_REPO_PUBLICO],
            cwd=REPO_PUBLICO,
            check=True
        )
        print("✅ Remote atualizado")
    
    print()
    print("=" * 70)
    print("✅ REPOSITÓRIO PÚBLICO PREPARADO!")
    print("=" * 70)
    print()
    print("📋 Próximos passos:")
    print("   1. Execute: python sincronizar_repositorio_publico.py")
    print("   2. O script vai copiar arquivos seguros e fazer push")
    print()
    print(f"🔗 Repositório: {GIT_REPO_PUBLICO}")
    print()

if __name__ == "__main__":
    main()

