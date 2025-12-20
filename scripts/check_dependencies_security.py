#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para verificar vulnerabilidades de segurança nas dependências
Usa pip-audit ou safety check
"""

import subprocess
import sys
import os

def check_with_pip_audit():
    """Verificar com pip-audit"""
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pip", "audit"],
            capture_output=True,
            text=True,
            timeout=120
        )
        return result.returncode == 0, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return False, "", "Timeout ao executar pip-audit"
    except FileNotFoundError:
        return None, "", "pip-audit não encontrado. Instale com: pip install pip-audit"

def check_with_safety():
    """Verificar com safety check"""
    try:
        result = subprocess.run(
            ["safety", "check", "--json"],
            capture_output=True,
            text=True,
            timeout=120
        )
        return result.returncode == 0, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return False, "", "Timeout ao executar safety check"
    except FileNotFoundError:
        return None, "", "safety não encontrado. Instale com: pip install safety"

def main():
    print("🔒 Verificando vulnerabilidades de segurança nas dependências...\n")
    
    # Tentar pip-audit primeiro
    print("1️⃣ Tentando pip-audit...")
    pip_audit_result = check_with_pip_audit()
    
    if pip_audit_result[0] is None:
        print(f"   ⚠️  {pip_audit_result[2]}")
        print("   💡 Instale: pip install pip-audit\n")
    elif pip_audit_result[0]:
        print("   ✅ pip-audit executado com sucesso!")
        if pip_audit_result[1]:
            print("   📋 Resultados:")
            print(pip_audit_result[1])
        if pip_audit_result[2]:
            print("   ⚠️  Avisos:")
            print(pip_audit_result[2])
        return
    else:
        print("   ⚠️  pip-audit encontrou problemas:")
        if pip_audit_result[1]:
            print(pip_audit_result[1])
        if pip_audit_result[2]:
            print(pip_audit_result[2])
    
    # Tentar safety check como alternativa
    print("\n2️⃣ Tentando safety check...")
    safety_result = check_with_safety()
    
    if safety_result[0] is None:
        print(f"   ⚠️  {safety_result[2]}")
        print("   💡 Instale: pip install safety\n")
    elif safety_result[0]:
        print("   ✅ safety check executado com sucesso!")
        if safety_result[1]:
            print("   📋 Resultados:")
            print(safety_result[1])
        if safety_result[2]:
            print("   ⚠️  Avisos:")
            print(safety_result[2])
    else:
        print("   ⚠️  safety check encontrou problemas:")
        if safety_result[1]:
            print(safety_result[1])
        if safety_result[2]:
            print(safety_result[2])
    
    # Se nenhum estiver disponível, dar instruções
    if (pip_audit_result[0] is None and safety_result[0] is None):
        print("\n📝 Nenhuma ferramenta de verificação disponível.")
        print("   Instale uma das opções:")
        print("   • pip install pip-audit")
        print("   • pip install safety")
        print("\n   Ou verifique manualmente em:")
        print("   • https://pypi.org/project/pip-audit/")
        print("   • https://github.com/pyupio/safety")

if __name__ == "__main__":
    main()

