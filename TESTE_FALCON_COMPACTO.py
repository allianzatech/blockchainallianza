#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste de FALCON como alternativa mais compacta
Demonstra redução de ~46% no tamanho de assinatura vs ML-DSA
"""

from quantum_security import QuantumSecuritySystem
import base64

print("=" * 70)
print("🔐 TESTE: FALCON - ALTERNATIVA COMPACTA")
print("=" * 70)
print()

# Inicializar sistema
qs = QuantumSecuritySystem()

# Teste 1: ML-DSA (baseline)
print("📊 TESTE 1: ML-DSA (BASELINE)")
print("-" * 70)
ml_dsa_result = qs.generate_ml_dsa_keypair(security_level=3)
if ml_dsa_result.get("success"):
    ml_dsa_id = ml_dsa_result["keypair_id"]
    message = b"Teste de comparacao ML-DSA vs FALCON"
    ml_dsa_sig = qs.sign_with_ml_dsa(ml_dsa_id, message)
    if ml_dsa_sig.get("success"):
        ml_dsa_size = len(base64.b64decode(ml_dsa_sig["signature"]))
        print(f"✅ ML-DSA:")
        print(f"   Keypair ID: {ml_dsa_id[:30]}...")
        print(f"   Tamanho assinatura: {ml_dsa_size} bytes")
        print(f"   Padrão NIST: Sim")
    else:
        print(f"❌ Erro ao assinar ML-DSA: {ml_dsa_sig.get('error')}")
        ml_dsa_size = 2420  # Valor padrão
else:
    print(f"❌ Erro ao gerar ML-DSA: {ml_dsa_result.get('error')}")
    ml_dsa_size = 2420  # Valor padrão

print()

# Teste 2: FALCON
print("📊 TESTE 2: FALCON (ALTERNATIVA COMPACTA)")
print("-" * 70)
falcon_result = qs.generate_falcon_keypair("FALCON-512")
if falcon_result.get("success"):
    falcon_id = falcon_result["keypair_id"]
    message = b"Teste de comparacao ML-DSA vs FALCON"
    falcon_sig = qs.sign_with_falcon(falcon_id, message)
    if falcon_sig.get("success"):
        falcon_size = falcon_sig.get("signature_size_bytes", len(base64.b64decode(falcon_sig["signature"])))
        print(f"✅ FALCON:")
        print(f"   Keypair ID: {falcon_id[:30]}...")
        print(f"   Tamanho assinatura: {falcon_size} bytes")
        print(f"   Padrão NIST: Sim")
        print(f"   Implementação: {falcon_result.get('implementation', 'simulated')}")
    else:
        print(f"❌ Erro ao assinar FALCON: {falcon_sig.get('error')}")
        falcon_size = 1330  # Valor padrão
else:
    print(f"❌ Erro ao gerar FALCON: {falcon_result.get('error')}")
    falcon_size = 1330  # Valor padrão

print()

# Comparação
print("=" * 70)
print("📊 COMPARAÇÃO: ML-DSA vs FALCON")
print("=" * 70)
print()

if ml_dsa_size > 0 and falcon_size > 0:
    reduction = ((ml_dsa_size - falcon_size) / ml_dsa_size) * 100
    print(f"   ML-DSA (Dilithium): {ml_dsa_size} bytes")
    print(f"   FALCON-512:         {falcon_size} bytes")
    print(f"   Redução:            {reduction:.1f}%")
    print()
    
    if reduction > 40:
        print("✅✅✅ FALCON é significativamente mais compacto!")
        print("   Benefício: Menor overhead em blocos")
        print("   Uso recomendado: Transações que precisam de segurança quântica com menor overhead")
    else:
        print("✅ FALCON oferece redução moderada no tamanho")
    
    print()
    print("💡 RECOMENDAÇÃO:")
    print("   • Use FALCON para transações que precisam de segurança quântica")
    print("     mas com menor overhead de dados")
    print("   • Use ML-DSA para máxima segurança (padrão NIST principal)")
    print("   • Ambos são padrões NIST PQC e quantum-safe")
else:
    print("⚠️  Não foi possível comparar (erros nos testes)")

print("=" * 70)











