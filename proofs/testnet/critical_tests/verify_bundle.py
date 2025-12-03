#!/usr/bin/env python3
# Script de Verificação de Bundle - Allianza Blockchain
# Bundle ID: test_6_audit_reproducible_bundle
# Timestamp: 2025-11-26T00:53:54.126719

import json
import hashlib
import sys

def verify_bundle(bundle_path):
    """Verificar bundle de prova"""
    with open(bundle_path, 'r') as f:
        bundle = json.load(f)
    
    # Obter hash esperado ANTES de remover do bundle
    expected_hash = bundle.get("components", {}).get("qrs3_signature", {}).get("bundle_hash")
    
    # Calcular hash SEM incluir o bundle_hash, signature_hash, keypair_id e timestamp (para evitar circularidade e variações)
    bundle_for_hash = json.loads(json.dumps(bundle))
    # Remover timestamp que varia a cada execução
    bundle_for_hash.pop("timestamp", None)
    if "components" in bundle_for_hash and "qrs3_signature" in bundle_for_hash["components"]:
        bundle_for_hash["components"]["qrs3_signature"].pop("bundle_hash", None)
        bundle_for_hash["components"]["qrs3_signature"].pop("signature_hash", None)
        bundle_for_hash["components"]["qrs3_signature"].pop("keypair_id", None)
    
    # Usar ensure_ascii=False e separators consistentes para garantir hash idêntico
    bundle_json_for_hash = json.dumps(bundle_for_hash, sort_keys=True, ensure_ascii=False, separators=(',', ':'))
    bundle_hash = hashlib.sha256(bundle_json_for_hash.encode('utf-8')).hexdigest()
    
    if expected_hash and bundle_hash == expected_hash:
        print("✅ Bundle hash verificado!")
        return True
    else:
        print(f"❌ Bundle hash não confere!")
        print(f"   Esperado: {expected_hash}")
        print(f"   Calculado: {bundle_hash}")
        return False

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python verify_bundle.py <bundle_path>")
        sys.exit(1)
    
    bundle_path = sys.argv[1]
    if verify_bundle(bundle_path):
        print("✅ Bundle verificado com sucesso!")
        sys.exit(0)
    else:
        print("❌ Falha na verificação do bundle!")
        sys.exit(1)
