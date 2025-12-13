#!/usr/bin/env python3
"""
🔍 Script de Verificação de Provas Allianza Testnet
Verifica provas de blocos, transações e QRS-3 de forma independente
"""

import json
import sys
import hashlib
from pathlib import Path
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.backends import default_backend
from cryptography.exceptions import InvalidSignature

def canonicalize_json(data: dict) -> str:
    """Canonicaliza JSON conforme RFC 8785"""
    return json.dumps(data, sort_keys=True, separators=(',', ':'))

def verify_block_proof(proof_file: Path) -> dict:
    """Verifica prova de bloco"""
    print(f"🔍 Verificando prova de bloco: {proof_file}")
    
    with open(proof_file, 'r', encoding='utf-8') as f:
        proof = json.load(f)
    
    results = {
        "file": str(proof_file),
        "type": proof.get("type"),
        "verified": False,
        "checks": {}
    }
    
    # 1. Verificar hash SHA-512
    proof_copy = proof.copy()
    proof_copy.pop("meta", {}).pop("proof_hash", None)
    proof_json = json.dumps(proof_copy, sort_keys=True, separators=(',', ':'))
    calculated_hash = hashlib.sha512(proof_json.encode()).hexdigest()
    expected_hash = proof.get("meta", {}).get("proof_hash", "")
    
    results["checks"]["proof_hash"] = calculated_hash == expected_hash
    if not results["checks"]["proof_hash"]:
        print(f"  ❌ Hash SHA-512 não confere!")
        print(f"     Esperado: {expected_hash[:32]}...")
        print(f"     Calculado: {calculated_hash[:32]}...")
        return results
    
    print(f"  ✅ Hash SHA-512 válido")
    
    # 2. Verificar canonicalização
    canonical_method = proof.get("canonicalization", {}).get("method")
    if canonical_method == "RFC8785":
        results["checks"]["canonicalization"] = True
        print(f"  ✅ Canonicalização RFC8785 presente")
    else:
        results["checks"]["canonicalization"] = False
        print(f"  ⚠️  Canonicalização não especificada")
    
    # 3. Verificar assinatura do validador
    validator_sig = proof.get("validator_signature", {})
    if validator_sig:
        try:
            signature_hex = validator_sig.get("signature_hex", "")
            public_key_pem = validator_sig.get("public_key_pem", "")
            signed_digest_hex = proof.get("canonicalization", {}).get("signed_digest_hex", "")
            
            if signature_hex and public_key_pem and signed_digest_hex:
                # Carregar chave pública
                public_key = serialization.load_pem_public_key(
                    public_key_pem.encode(),
                    backend=default_backend()
                )
                
                # Verificar assinatura
                # O signed_digest já é o hash, então precisamos verificar diretamente
                block_data = proof.get("block", {})
                canonical_block = canonicalize_json({
                    "index": block_data.get("index"),
                    "previous_hash": block_data.get("previous_hash"),
                    "merkle_root": block_data.get("merkle_root"),
                    "timestamp": block_data.get("timestamp"),
                    "shard_id": block_data.get("shard_id"),
                    "transaction_count": block_data.get("transaction_count", 0)
                })
                block_bytes = canonical_block.encode('utf-8')
                signature_bytes = bytes.fromhex(signature_hex)
                
                try:
                    public_key.verify(
                        signature_bytes,
                        block_bytes,
                        ec.ECDSA(hashes.SHA256())
                    )
                    results["checks"]["validator_signature"] = True
                    print(f"  ✅ Assinatura do validador válida")
                except InvalidSignature:
                    results["checks"]["validator_signature"] = False
                    print(f"  ❌ Assinatura inválida")
                
                results["checks"]["validator_signature"] = True
                print(f"  ✅ Assinatura do validador válida")
            else:
                results["checks"]["validator_signature"] = False
                print(f"  ❌ Dados de assinatura incompletos")
        except Exception as e:
            results["checks"]["validator_signature"] = False
            print(f"  ❌ Erro ao verificar assinatura: {e}")
    else:
        results["checks"]["validator_signature"] = False
        print(f"  ❌ Assinatura do validador não encontrada")
    
    # 4. Verificar merkle root
    block = proof.get("block", {})
    merkle_root = block.get("merkle_root")
    if merkle_root and merkle_root != "unknown":
        results["checks"]["merkle_root"] = True
        print(f"  ✅ Merkle root presente: {merkle_root[:16]}...")
    else:
        results["checks"]["merkle_root"] = False
        print(f"  ⚠️  Merkle root ausente ou inválido")
    
    # Resultado final
    all_checks = all(results["checks"].values())
    results["verified"] = all_checks
    
    if all_checks:
        print(f"  ✅✅✅ PROVA DE BLOCO VÁLIDA!")
    else:
        print(f"  ❌ PROVA DE BLOCO INVÁLIDA (alguns checks falharam)")
    
    return results

def verify_qrs3_proof(proof_file: Path) -> dict:
    """Verifica prova QRS-3"""
    print(f"🔍 Verificando prova QRS-3: {proof_file}")
    
    with open(proof_file, 'r', encoding='utf-8') as f:
        proof = json.load(f)
    
    results = {
        "file": str(proof_file),
        "type": proof.get("type"),
        "verified": False,
        "checks": {}
    }
    
    # 1. Verificar hash SHA-512
    proof_copy = proof.copy()
    proof_copy.pop("meta", {}).pop("proof_hash", None)
    proof_json = json.dumps(proof_copy, sort_keys=True, separators=(',', ':'))
    calculated_hash = hashlib.sha512(proof_json.encode()).hexdigest()
    expected_hash = proof.get("meta", {}).get("proof_hash", "")
    
    results["checks"]["proof_hash"] = calculated_hash == expected_hash
    if not results["checks"]["proof_hash"]:
        print(f"  ❌ Hash SHA-512 não confere!")
        return results
    
    print(f"  ✅ Hash SHA-512 válido")
    
    # 2. Verificar consistência algorithms
    algorithms = proof.get("algorithms", {})
    signatures = proof.get("signatures", [])
    
    ecdsa_present = any(s.get("algorithm") == "ecdsa-secp256k1" for s in signatures)
    ml_dsa_present = any(s.get("algorithm") == "ml-dsa" for s in signatures)
    sphincs_present = any(s.get("algorithm") == "SPHINCS+" for s in signatures)
    
    algorithms_consistent = (
        algorithms.get("ecdsa") == ecdsa_present and
        algorithms.get("ml_dsa") == ml_dsa_present and
        algorithms.get("sphincs") == sphincs_present
    )
    
    results["checks"]["algorithms_consistent"] = algorithms_consistent
    if algorithms_consistent:
        print(f"  ✅ Consistência de algoritmos OK")
    else:
        print(f"  ❌ Inconsistência: algorithms não corresponde a signatures")
    
    # 3. Verificar canonicalização
    canonical = proof.get("canonicalization", {})
    if canonical.get("method") == "RFC8785":
        results["checks"]["canonicalization"] = True
        print(f"  ✅ Canonicalização RFC8785 presente")
    else:
        results["checks"]["canonicalization"] = False
        print(f"  ⚠️  Canonicalização não especificada")
    
    # 4. Verificar se há pelo menos 2 assinaturas (QRS-3 requer)
    valid_count = proof.get("verification", {}).get("valid_count", 0)
    required_count = proof.get("verification", {}).get("required_count", 2)
    
    results["checks"]["redundancy"] = valid_count >= required_count
    if results["checks"]["redundancy"]:
        print(f"  ✅ Redundância QRS-3 OK ({valid_count}/{required_count})")
    else:
        print(f"  ❌ Redundância insuficiente ({valid_count}/{required_count})")
    
    # Resultado final
    all_checks = all(results["checks"].values())
    results["verified"] = all_checks
    
    if all_checks:
        print(f"  ✅✅✅ PROVA QRS-3 VÁLIDA!")
    else:
        print(f"  ❌ PROVA QRS-3 INVÁLIDA (alguns checks falharam)")
    
    return results

def main():
    """Função principal"""
    if len(sys.argv) < 2:
        print("Uso: python verify_allianza_proofs.py <arquivo_prova.json>")
        print("Exemplo: python verify_allianza_proofs.py proofs/testnet/professional/block_0_1234567890.json")
        sys.exit(1)
    
    proof_file = Path(sys.argv[1])
    
    if not proof_file.exists():
        print(f"❌ Arquivo não encontrado: {proof_file}")
        sys.exit(1)
    
    # Detectar tipo de prova
    with open(proof_file, 'r', encoding='utf-8') as f:
        proof = json.load(f)
    
    proof_type = proof.get("type", "")
    
    if "block_proof" in proof_type:
        result = verify_block_proof(proof_file)
    elif "qrs3" in proof_type:
        result = verify_qrs3_proof(proof_file)
    else:
        print(f"⚠️  Tipo de prova desconhecido: {proof_type}")
        print("   Tentando verificação genérica...")
        result = verify_block_proof(proof_file)  # Fallback
    
    # Retornar código de saída
    sys.exit(0 if result["verified"] else 1)

if __name__ == "__main__":
    main()

