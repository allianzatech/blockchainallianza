#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔄 Script de Sincronização Automática - Repositório Público
Sincroniza arquivos seguros do repositório privado para o público
"""

import os
import shutil
import subprocess
from pathlib import Path
from datetime import datetime

# Configuração
REPO_PRIVADO = Path(".")  # Repositório atual (privado)
REPO_PUBLICO = Path("../allianzablockchainpublic")  # Repositório público
GIT_REPO_PUBLICO = "https://github.com/dieisonmaach-lang/allianzablockchainpublic.git"

# Arquivos e diretórios SEGUROS para copiar
SAFE_FILES = [
    # Documentação
    "WHITEPAPER_ALLIANZA_BLOCKCHAIN.md",
    "README.md",
    "LICENSE",
    ".gitignore",
    "CHANGELOG.md",
    "CONTRIBUTING.md",
    "CODE_OF_CONDUCT.md",
    
    # Provas Técnicas
    "PROVAS_TECNICAS_COMPLETAS_FINAL.json",
    "PROVAS_TECNICAS_COMPLETAS_FINAL_EN.json",
    
    # Documentação Técnica
    "docs/",
    "GUIA_QSS_PARA_OUTRAS_BLOCKCHAINS.md",
    "QSS_FOR_OTHER_BLOCKCHAINS.md",  # Versão traduzida
    
    # SDK (completo)
    "qss-sdk/",
    
    # Templates (apenas UI)
    "templates/testnet/",
    
    # Exemplos
    "examples/",
    
    # Testes
    "tests/",
    
    # Provas Reais
    "proofs/",
    
    # Configuração
    "Procfile",
    ".github/",
]

# Arquivos a EXCLUIR (segurança)
EXCLUDE_PATTERNS = [
    "*_PRIVATE_KEY*",
    "*private_key*",
    ".env",
    ".env.*",
    "*secret*",
    "*password*",
    "*API_KEY*",
    "*API_TOKEN*",
    "*HASH*",
    "*hash*",
    "*HASHES*",
    "*hashes*",
    "HASH_*.txt",
    "HASHES_*.txt",
    "HASH_*.json",
    "HASHES_*.json",
    "alz_niev_interoperability.py",
    "quantum_security.py",
    "real_cross_chain_bridge.py",
    "allianza_blockchain.py",
    "*.db",
    "*.sqlite",
    "__pycache__/",
    "node_modules/",
    "dist/",
    "build/",
    "*.log",
    "logs/",
]

def should_exclude(file_path):
    """Verifica se arquivo deve ser excluído"""
    file_str = str(file_path)
    for pattern in EXCLUDE_PATTERNS:
        if pattern in file_str:
            return True
    return False

def copy_safe_files():
    """Copia arquivos seguros para repositório público"""
    print("=" * 70)
    print("🔄 SINCRONIZANDO REPOSITÓRIO PÚBLICO")
    print("=" * 70)
    print()
    
    if not REPO_PUBLICO.exists():
        print(f"❌ Repositório público não encontrado: {REPO_PUBLICO}")
        print(f"💡 Execute primeiro: preparar_repositorio_publico.py")
        return False
    
    print(f"📁 Repositório privado: {REPO_PRIVADO.absolute()}")
    print(f"📁 Repositório público: {REPO_PUBLICO.absolute()}")
    print()
    
    copied = 0
    skipped = 0
    
    for item in SAFE_FILES:
        source = REPO_PRIVADO / item
        dest = REPO_PUBLICO / item
        
        if not source.exists():
            print(f"⚠️  Não encontrado: {source}")
            continue
        
        try:
            if source.is_file():
                if should_exclude(source):
                    print(f"🚫 EXCLUÍDO: {source.name}")
                    skipped += 1
                    continue
                
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(source, dest)
                print(f"✅ Copiado: {source.name}")
                copied += 1
                
            elif source.is_dir():
                # Copiar diretório recursivamente
                for file_path in source.rglob('*'):
                    if file_path.is_file():
                        if should_exclude(file_path):
                            continue
                        
                        rel_path = file_path.relative_to(source)
                        dest_file = dest / rel_path
                        dest_file.parent.mkdir(parents=True, exist_ok=True)
                        shutil.copy2(file_path, dest_file)
                
                print(f"✅ Copiado diretório: {item}")
                copied += 1
                
        except Exception as e:
            print(f"❌ Erro ao copiar {item}: {e}")
            skipped += 1
    
    print()
    print("=" * 70)
    print(f"✅ Sincronização concluída!")
    print(f"   Copiados: {copied}")
    print(f"   Ignorados: {skipped}")
    print("=" * 70)
    
    return True

def git_commit_and_push(use_token=False, token=None):
    """Faz commit e push para o repositório público"""
    print()
    print("=" * 70)
    print("📤 FAZENDO COMMIT E PUSH")
    print("=" * 70)
    print()
    
    os.chdir(REPO_PUBLICO)
    
    try:
        # Configurar remote com token se fornecido
        if use_token and token:
            remote_url = f"https://{token}@github.com/dieisonmaach-lang/allianzablockchainpublic.git"
            subprocess.run(
                ["git", "remote", "set-url", "origin", remote_url],
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            print("✅ Remote configurado com token")
        
        # Verificar se há mudanças
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            capture_output=True,
            text=True,
            check=True
        )
        
        if not result.stdout.strip():
            print("ℹ️  Nenhuma mudança para commitar")
            return True
        
        # Adicionar todos os arquivos
        subprocess.run(["git", "add", "."], check=True)
        print("✅ Arquivos adicionados ao staging")
        
        # Commit
        commit_message = f"chore: sync from private repo - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        subprocess.run(
            ["git", "commit", "-m", commit_message],
            check=True
        )
        print(f"✅ Commit criado: {commit_message}")
        
        # Verificar qual branch existe
        branch_result = subprocess.run(
            ["git", "branch", "--show-current"],
            capture_output=True,
            text=True
        )
        branch = branch_result.stdout.strip() or "master"
        
        # Push
        push_result = subprocess.run(
            ["git", "push", "origin", branch],
            capture_output=True,
            text=True
        )
        
        if push_result.returncode == 0:
            print("✅ Push realizado com sucesso!")
            print()
            print("🔗 Verifique em: https://github.com/dieisonmaach-lang/allianzablockchainpublic")
            return True
        else:
            print("❌ Erro no push:")
            print(push_result.stderr)
            print()
            print("💡 Solução: Configure um token ou use GitHub Desktop")
            return False
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro no Git: {e}")
        return False
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False
    finally:
        os.chdir(REPO_PRIVADO)

def main():
    """Função principal"""
    print("=" * 70)
    print("🔄 SINCRONIZAÇÃO AUTOMÁTICA - REPOSITÓRIO PÚBLICO")
    print("=" * 70)
    print()
    
    # Copiar arquivos
    if not copy_safe_files():
        return
    
    # Tentar fazer commit e push automaticamente
    print("\n📤 Tentando fazer commit e push automático...")
    
    # Verificar se há token configurado
    token = os.getenv('GITHUB_TOKEN_PUBLIC')
    
    if token:
        print("✅ Token encontrado nas variáveis de ambiente")
        success = git_commit_and_push(use_token=True, token=token)
    else:
        print("ℹ️  Nenhum token configurado")
        print("   Tentando push normal (pode falhar se credenciais incorretas)...")
        success = git_commit_and_push()
        
        if not success:
            print("\n" + "=" * 70)
            print("💡 PUSH FALHOU - CONFIGURE UM TOKEN")
            print("=" * 70)
            print("\nPara push automático, configure um token:")
            print("\n1. Crie token da conta allianzatoken-png:")
            print("   https://github.com/settings/tokens")
            print("\n2. Configure variável de ambiente:")
            print("   setx GITHUB_TOKEN_PUBLIC \"seu_token_aqui\"")
            print("\n3. Reinicie o terminal e execute o script novamente")
            print("\nOU use GitHub Desktop para fazer push manualmente")
            print("   (mais fácil e não precisa de token)")
    
    print()
    print("=" * 70)
    print("✅ SINCRONIZAÇÃO CONCLUÍDA!")
    print("=" * 70)

if __name__ == "__main__":
    main()

