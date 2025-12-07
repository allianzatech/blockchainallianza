#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧪 Script de Teste para Suite Profissional
Testa se todos os módulos podem ser importados corretamente
"""

import sys
import os

print("="*70)
print("🧪 TESTE DE IMPORTAÇÃO - SUITE PROFISSIONAL")
print("="*70)
print()

# Testar importações
try:
    print("1️⃣  Testando importação de real_cross_chain_bridge...")
    from real_cross_chain_bridge import RealCrossChainBridge
    print("   ✅ real_cross_chain_bridge importado com sucesso!")
except SyntaxError as e:
    print(f"   ❌ Erro de sintaxe: {e}")
    sys.exit(1)
except Exception as e:
    print(f"   ⚠️  Erro de importação (pode ser normal se dependências faltarem): {e}")

try:
    print("\n2️⃣  Testando importação de testnet_professional_test_suite...")
    from testnet_professional_test_suite import ProfessionalTestSuite
    print("   ✅ testnet_professional_test_suite importado com sucesso!")
except SyntaxError as e:
    print(f"   ❌ Erro de sintaxe: {e}")
    sys.exit(1)
except Exception as e:
    print(f"   ⚠️  Erro de importação (pode ser normal se dependências faltarem): {e}")

try:
    print("\n3️⃣  Testando importação de quantum_security...")
    from quantum_security import QuantumSecuritySystem
    print("   ✅ quantum_security importado com sucesso!")
except SyntaxError as e:
    print(f"   ❌ Erro de sintaxe: {e}")
    sys.exit(1)
except Exception as e:
    print(f"   ⚠️  Erro de importação (pode ser normal se dependências faltarem): {e}")

try:
    print("\n4️⃣  Testando importação de pqc_key_manager...")
    from pqc_key_manager import PQCKeyManager
    print("   ✅ pqc_key_manager importado com sucesso!")
except SyntaxError as e:
    print(f"   ❌ Erro de sintaxe: {e}")
    sys.exit(1)
except Exception as e:
    print(f"   ⚠️  Erro de importação (pode ser normal se dependências faltarem): {e}")

print("\n" + "="*70)
print("✅ TESTE DE SINTAXE CONCLUÍDO!")
print("="*70)
print("\n📋 Próximos passos:")
print("   1. Iniciar o servidor Flask: python allianza_blockchain.py")
print("   2. Acessar: http://localhost:5000/testnet/professional-tests/")
print("   3. Executar testes individuais ou todos os testes")
















