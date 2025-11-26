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
    
    # Verificar hash
    bundle_json = json.dumps(bundle, sort_keys=True)
    bundle_hash = hashlib.sha256(bundle_json.encode()).hexdigest()
    
    expected_hash = bundle.get("components", {}).get("qrs3_signature", {}).get("bundle_hash")
    
    if expected_hash and bundle_hash == expected_hash:
        print("✅ Bundle hash verificado!")
        return True
    else:
        print("❌ Bundle hash não confere!")
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
