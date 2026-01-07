#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔍 Script para Verificar Repositório Público Antes de Push
Verifica se arquivos comerciais/produção não estão sendo incluídos
"""

import os
import sys
from pathlib import Path
from typing import List, Tuple

# Cores para output
RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'

# Arquivos/diretórios que NÃO devem estar no público
EXCLUDED_PATTERNS = [
    # Diretórios comerciais
    'commercial_repo/',
    'deploy/',
    
    # Arquivos comerciais
    'real_cross_chain_bridge.py',
    'allianza_bridge_config.py',
    'db_manager.py',
    'bridge_free_interop.py',
    
    # Arquivos testnet
    'testnet_*.py',
    
    # Arquivos de deploy
    'wsgi.py',
    'wsgi_optimized.py',
    'gunicorn_config.py',
    'Procfile',
    'render.yaml',
    'docker-compose.yml',
    'Dockerfile',
    'runtime.txt',
    '.htaccess',
    'start_server.sh',
    'nginx_*.conf',
    
    # Bancos de dados
    '*.db',
    '*.sqlite',
    '*.sqlite3',
    
    # Logs
    '*.log',
    'logs/',
    
    # Secrets
    'secrets/',
    '*.key',
    '*.pem',
    '.env',
    '.env.production',
    '.env.local',
    'exposed_keys_report.json',
    
    # Dados de produção
    'data/faucet_last_requests.json',
    'data/pending_commitments.json',
    'data/commitment_metrics.json',
]

def check_git_status() -> List[str]:
    """Verifica arquivos staged para commit"""
    import subprocess
    result = subprocess.run(
        ['git', 'status', '--porcelain'],
        capture_output=True,
        text=True
    )
    return result.stdout.strip().split('\n') if result.stdout.strip() else []

def check_file_exists(pattern: str) -> bool:
    """Verifica se arquivo/diretório existe"""
    path = Path(pattern.replace('*', ''))
    if '*' in pattern:
        # Pattern matching
        return any(Path('.').glob(pattern))
    return path.exists()

def verify_exclusions() -> Tuple[bool, List[str]]:
    """Verifica se arquivos excluídos estão no repositório"""
    issues = []
    all_ok = True
    
    print(f"{BLUE}🔍 Verificando exclusões...{RESET}\n")
    
    for pattern in EXCLUDED_PATTERNS:
        if check_file_exists(pattern):
            issues.append(f"❌ {pattern} encontrado (não deve estar no público)")
            all_ok = False
    
    return all_ok, issues

def verify_git_status() -> Tuple[bool, List[str]]:
    """Verifica arquivos staged para commit"""
    issues = []
    all_ok = True
    
    print(f"{BLUE}🔍 Verificando arquivos staged...{RESET}\n")
    
    staged_files = check_git_status()
    
    for line in staged_files:
        if not line.strip():
            continue
        
        status = line[:2]
        filename = line[3:].strip()
        
        # Verificar se arquivo excluído está staged
        for pattern in EXCLUDED_PATTERNS:
            if pattern.replace('*', '') in filename or filename.startswith(pattern.replace('*', '')):
                issues.append(f"❌ {filename} está staged (não deve estar no público)")
                all_ok = False
                break
    
    return all_ok, issues

def verify_gitignore() -> Tuple[bool, List[str]]:
    """Verifica se .gitignore está atualizado"""
    issues = []
    all_ok = True
    
    print(f"{BLUE}🔍 Verificando .gitignore...{RESET}\n")
    
    gitignore_path = Path('.gitignore')
    if not gitignore_path.exists():
        issues.append("❌ .gitignore não encontrado")
        all_ok = False
        return all_ok, issues
    
    gitignore_content = gitignore_path.read_text()
    
    # Verificar se padrões importantes estão no .gitignore
    important_patterns = [
        'commercial_repo/',
        'deploy/',
        'testnet_*.py',
        'real_cross_chain_bridge.py',
        'wsgi.py',
        '*.db',
        '*.log',
    ]
    
    for pattern in important_patterns:
        if pattern not in gitignore_content:
            issues.append(f"⚠️  {pattern} não está no .gitignore")
            # Não falha, apenas avisa
    
    return all_ok, issues

def main():
    """Função principal"""
    print("=" * 70)
    print(f"{BLUE}🔍 VERIFICAÇÃO DO REPOSITÓRIO PÚBLICO{RESET}")
    print("=" * 70)
    print()
    
    all_checks_passed = True
    all_issues = []
    
    # Verificar exclusões
    ok, issues = verify_exclusions()
    all_checks_passed = all_checks_passed and ok
    all_issues.extend(issues)
    
    # Verificar git status
    ok, issues = verify_git_status()
    all_checks_passed = all_checks_passed and ok
    all_issues.extend(issues)
    
    # Verificar .gitignore
    ok, issues = verify_gitignore()
    # .gitignore warnings não falham o check
    all_issues.extend(issues)
    
    # Resultado
    print()
    print("=" * 70)
    if all_checks_passed:
        print(f"{GREEN}✅ VERIFICAÇÃO PASSOU{RESET}")
        print(f"{GREEN}O repositório está pronto para push público.{RESET}")
        if all_issues:
            print(f"\n{YELLOW}⚠️  Avisos:{RESET}")
            for issue in all_issues:
                print(f"  {issue}")
        return 0
    else:
        print(f"{RED}❌ VERIFICAÇÃO FALHOU{RESET}")
        print(f"{RED}Arquivos comerciais/produção encontrados!{RESET}\n")
        print(f"{YELLOW}Problemas encontrados:{RESET}")
        for issue in all_issues:
            if issue.startswith('❌'):
                print(f"  {issue}")
        print()
        print(f"{YELLOW}Por favor, remova esses arquivos antes de fazer push.{RESET}")
        print(f"{YELLOW}Veja PUBLIC_REPO_EXCLUSIONS.md para mais informações.{RESET}")
        return 1

if __name__ == '__main__':
    sys.exit(main())

