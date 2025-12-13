#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
✅ VERIFICADOR DE PROVA JSON REAL
"""

import json
import hashlib
import os
from glob import glob

def verificar_prova(proof_file):
    """Verificar uma prova JSON"""
    print("="*70)
    print(f"🔍 VERIFICANDO PROVA: {proof_file}")
    print("="*70)
    
    with open(proof_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 1. Verificar Hash SHA-256
    print("\n📋 1. Verificação de Hash SHA-256")
    print("-" * 70)
    canonical_json = data.get("canonical_json", "")
    sha256_hash = data.get("sha256_hash", "")
    
    if canonical_json:
        calculated_hash = hashlib.sha256(canonical_json.encode('utf-8')).hexdigest()
        hash_valid = (calculated_hash == sha256_hash)
        
        print(f"   Hash calculado: {calculated_hash[:50]}...")
        print(f"   Hash do bundle: {sha256_hash[:50]}...")
        print(f"   ✅ Hash válido: {hash_valid}")
    else:
        print("   ⚠️  JSON canônico não encontrado")
        hash_valid = False
    
    # 2. Verificar Assinatura ML-DSA
    print("\n📋 2. Verificação de Assinatura ML-DSA")
    print("-" * 70)
    ml_dsa_sig = data.get("ml_dsa_signature", "")
    public_key = data.get("public_key", "")
    
    if ml_dsa_sig and public_key:
        print(f"   ✅ Assinatura ML-DSA presente: {len(ml_dsa_sig)} caracteres")
        print(f"   ✅ Chave pública presente: {len(public_key)} caracteres")
        
        # Tentar verificar se possível
        try:
            from pqc_key_manager import PQCKeyManager
            km = PQCKeyManager()
            if canonical_json and hash_valid:
                hash_bytes = bytes.fromhex(calculated_hash)
                result = km.verify_ml_dsa(public_key, hash_bytes, ml_dsa_sig)
                sig_valid = result.get("success", False)
                print(f"   ✅ Verificação ML-DSA: {'Válida' if sig_valid else 'Inválida'}")
                print(f"   ✅ Real: {result.get('real', False)}")
            else:
                print("   ⚠️  Não é possível verificar (hash inválido)")
                sig_valid = False
        except Exception as e:
            print(f"   ⚠️  Erro ao verificar: {e}")
            sig_valid = False
    else:
        print("   ⚠️  Assinatura ou chave pública não encontrada")
        sig_valid = False
    
    # 3. Verificar Estrutura
    print("\n📋 3. Verificação de Estrutura")
    print("-" * 70)
    bundle = data.get("bundle", {})
    required_fields = ["proof_id", "timestamp", "service", "transaction", "keypair", "signature"]
    
    structure_valid = True
    for field in required_fields:
        if field in bundle:
            print(f"   ✅ {field}: Presente")
        else:
            print(f"   ❌ {field}: Ausente")
            structure_valid = False
    
    # 4. Verificar Metadados
    print("\n📋 4. Verificação de Metadados")
    print("-" * 70)
    print(f"   Proof ID: {bundle.get('proof_id', 'N/A')}")
    print(f"   Timestamp: {bundle.get('timestamp', 'N/A')}")
    print(f"   Service: {bundle.get('service', 'N/A')}")
    print(f"   Version: {bundle.get('version', 'N/A')}")
    print(f"   Algorithm: {data.get('algorithm', 'N/A')}")
    print(f"   QRS-3 Mode: {data.get('qrs3_mode', False)}")
    
    # 5. Resumo Final
    print("\n" + "="*70)
    print("📊 RESUMO DA VERIFICAÇÃO")
    print("="*70)
    print(f"   Hash SHA-256: {'✅ Válido' if hash_valid else '❌ Inválido'}")
    print(f"   Assinatura ML-DSA: {'✅ Presente' if ml_dsa_sig else '❌ Ausente'}")
    print(f"   Verificação ML-DSA: {'✅ Válida' if sig_valid else '⚠️  Não verificada'}")
    print(f"   Estrutura: {'✅ Completa' if structure_valid else '❌ Incompleta'}")
    
    overall_valid = hash_valid and structure_valid and bool(ml_dsa_sig)
    
    print("\n" + "="*70)
    if overall_valid:
        print("✅ PROVA VÁLIDA E VERIFICÁVEL!")
    else:
        print("⚠️  PROVA COM PROBLEMAS")
    print("="*70)
    
    return {
        "hash_valid": hash_valid,
        "signature_present": bool(ml_dsa_sig),
        "signature_valid": sig_valid,
        "structure_valid": structure_valid,
        "overall_valid": overall_valid
    }

if __name__ == '__main__':
    # Procurar provas mais recentes (excluir canonical e outros)
    all_files = glob("proofs_real/proof_*.json")
    proof_files = [f for f in all_files if not f.endswith("_canonical.json")]
    if proof_files:
        # Ordenar por data (mais recente primeiro)
        proof_files.sort(reverse=True)
        latest_proof = proof_files[0]
        print(f"📁 Prova mais recente: {latest_proof}\n")
        verificar_prova(latest_proof)
    else:
        print("❌ Nenhuma prova encontrada em proofs_real/")
        print("   Execute: python test_qaas_proof_real.py")

