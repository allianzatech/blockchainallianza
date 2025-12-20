#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script to check security vulnerabilities in dependencies
Uses pip-audit or safety check
"""

import subprocess
import sys
import os

def check_with_pip_audit():
    """Check with pip-audit"""
    try:
        # Tentar primeiro como comando direto (pip-audit)
        result = subprocess.run(
            ["pip-audit"],
            capture_output=True,
            text=True,
            timeout=120
        )
        return result.returncode == 0, result.stdout, result.stderr
    except FileNotFoundError:
        # Se não encontrar como comando direto, tentar como módulo Python
        try:
            result = subprocess.run(
                [sys.executable, "-m", "pip_audit"],
                capture_output=True,
                text=True,
                timeout=120
            )
            return result.returncode == 0, result.stdout, result.stderr
        except FileNotFoundError:
            return None, "", "pip-audit not found. Install with: pip install pip-audit"
    except subprocess.TimeoutExpired:
        return False, "", "Timeout executing pip-audit"

def check_with_safety():
    """Check with safety check"""
    try:
        result = subprocess.run(
            ["safety", "check", "--json"],
            capture_output=True,
            text=True,
            timeout=120
        )
        return result.returncode == 0, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return False, "", "Timeout executing safety check"
    except FileNotFoundError:
        return None, "", "safety not found. Install with: pip install safety"

def main():
    print("🔒 Checking security vulnerabilities in dependencies...\n")
    
    # Try pip-audit first
    print("1️⃣ Trying pip-audit...")
    pip_audit_result = check_with_pip_audit()
    
    if pip_audit_result[0] is None:
        print(f"   ⚠️  {pip_audit_result[2]}")
        print("   💡 Install: pip install pip-audit\n")
    elif pip_audit_result[0]:
        print("   ✅ pip-audit executed successfully!")
        print("   ℹ️  No vulnerabilities found.\n")
        if pip_audit_result[1]:
            print("   📋 Results:")
            print(pip_audit_result[1])
        if pip_audit_result[2]:
            print("   ⚠️  Warnings:")
            print(pip_audit_result[2])
        return
    else:
        print("   ⚠️  pip-audit found vulnerabilities:")
        print("   📋 Details:")
        if pip_audit_result[1]:
            print(pip_audit_result[1])
        if pip_audit_result[2]:
            print(pip_audit_result[2])
        print("\n   💡 See docs/DEPENDENCY_VULNERABILITIES_REPORT.md for details and fixes")
    
    # Try safety check as alternative
    print("\n2️⃣ Trying safety check...")
    safety_result = check_with_safety()
    
    if safety_result[0] is None:
        print(f"   ⚠️  {safety_result[2]}")
        print("   💡 Install: pip install safety\n")
    elif safety_result[0]:
        print("   ✅ safety check executed successfully!")
        if safety_result[1]:
            print("   📋 Results:")
            print(safety_result[1])
        if safety_result[2]:
            print("   ⚠️  Warnings:")
            print(safety_result[2])
    else:
        print("   ⚠️  safety check found issues:")
        if safety_result[1]:
            print(safety_result[1])
        if safety_result[2]:
            print(safety_result[2])
    
    # If none available, provide instructions
    if (pip_audit_result[0] is None and safety_result[0] is None):
        print("\n📝 No verification tool available.")
        print("   Install one of the options:")
        print("   • pip install pip-audit")
        print("   • pip install safety")
        print("\n   Or check manually at:")
        print("   • https://pypi.org/project/pip-audit/")
        print("   • https://github.com/pyupio/safety")

if __name__ == "__main__":
    main()

