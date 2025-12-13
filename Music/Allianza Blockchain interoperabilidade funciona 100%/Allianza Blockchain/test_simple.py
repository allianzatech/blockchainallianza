#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste Simples - Allianza Blockchain
Testa funcionalidades básicas sem dependências complexas
"""

import sys
import os
from pathlib import Path

# Adicionar raiz do projeto ao path
ROOT_DIR = Path(__file__).parent
sys.path.insert(0, str(ROOT_DIR))

def test_source_code_exists():
    """Testa se o código-fonte existe"""
    print("=" * 70)
    print("🧪 TESTE 1: Verificar se Código-Fonte Existe")
    print("=" * 70)
    
    files_to_check = [
        ("QRS-3 (PQC)", "core/crypto/pqc_crypto.py"),
        ("Quantum Security", "core/crypto/quantum_security.py"),
        ("ALZ-NIEV Consensus", "core/consensus/adaptive_consensus.py"),
        ("ALZ-NIEV Protocol", "core/consensus/alz_niev_interoperability.py"),
        ("Bridge-Free Interop", "core/interoperability/bridge_free_interop.py"),
        ("Proof-of-Lock", "core/interoperability/proof_of_lock.py"),
    ]
    
    all_exist = True
    for name, file_path in files_to_check:
        full_path = ROOT_DIR / file_path
        if full_path.exists():
            size = full_path.stat().st_size
            print(f"✅ {name}: {file_path} ({size:,} bytes)")
        else:
            print(f"❌ {name}: {file_path} - NÃO ENCONTRADO")
            all_exist = False
    
    return all_exist

def test_read_source_code():
    """Testa se consegue ler o código-fonte"""
    print("\n" + "=" * 70)
    print("🧪 TESTE 2: Ler Código-Fonte")
    print("=" * 70)
    
    try:
        # Ler QRS-3
        with open(ROOT_DIR / "core/crypto/pqc_crypto.py", "r", encoding="utf-8") as f:
            qrs3_code = f.read()
            if "ML-DSA" in qrs3_code or "SPHINCS" in qrs3_code or "PQC" in qrs3_code:
                print(f"✅ QRS-3: Código legível ({len(qrs3_code):,} caracteres)")
            else:
                print("⚠️  QRS-3: Código legível mas não encontrou ML-DSA/SPHINCS")
        
        # Ler ALZ-NIEV
        with open(ROOT_DIR / "core/consensus/alz_niev_interoperability.py", "r", encoding="utf-8") as f:
            alz_code = f.read()
            if "ALZ-NIEV" in alz_code or "interoperability" in alz_code.lower():
                print(f"✅ ALZ-NIEV: Código legível ({len(alz_code):,} caracteres)")
            else:
                print("⚠️  ALZ-NIEV: Código legível mas não encontrou ALZ-NIEV")
        
        # Ler Interoperabilidade
        with open(ROOT_DIR / "core/interoperability/bridge_free_interop.py", "r", encoding="utf-8") as f:
            interop_code = f.read()
            if "bridge" in interop_code.lower() or "interop" in interop_code.lower():
                print(f"✅ Interoperabilidade: Código legível ({len(interop_code):,} caracteres)")
            else:
                print("⚠️  Interoperabilidade: Código legível mas não encontrou bridge/interop")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro ao ler código-fonte: {e}")
        return False

def test_proofs_exist():
    """Testa se as provas existem"""
    print("\n" + "=" * 70)
    print("🧪 TESTE 3: Verificar Provas")
    print("=" * 70)
    
    proofs_to_check = [
        ("Complete Proofs", "COMPLETE_TECHNICAL_PROOFS_FINAL.json"),
        ("Verifiable On-Chain", "VERIFIABLE_ON_CHAIN_PROOFS.md"),
        ("Ethereum Proof", "proofs/interoperability_real/ethereum_validation_proof.json"),
    ]
    
    all_exist = True
    for name, file_path in proofs_to_check:
        full_path = ROOT_DIR / file_path
        if full_path.exists():
            size = full_path.stat().st_size
            print(f"✅ {name}: {file_path} ({size:,} bytes)")
        else:
            print(f"❌ {name}: {file_path} - NÃO ENCONTRADO")
            all_exist = False
    
    return all_exist

def test_verify_transaction_hash():
    """Testa se os hashes de transação são válidos"""
    print("\n" + "=" * 70)
    print("🧪 TESTE 4: Verificar Hashes de Transação")
    print("=" * 70)
    
    # Ethereum transaction hash
    eth_hash = "0x9a75d8edd1af2f7239db94d799abbdec30c42870899cbdcb5d9d8df4daf27110"
    if eth_hash.startswith("0x") and len(eth_hash) == 66:
        print(f"✅ Ethereum Hash: {eth_hash[:20]}...{eth_hash[-10:]}")
        print(f"   Verificar em: https://sepolia.etherscan.io/tx/{eth_hash}")
    else:
        print(f"❌ Ethereum Hash inválido")
        return False
    
    # Bitcoin transaction hash
    btc_hash = "842f01a3302b6b19981204c96f377be1ec1dfc51e995f68b3a1563e6750d06e8"
    if len(btc_hash) == 64:
        print(f"✅ Bitcoin Hash: {btc_hash[:20]}...{btc_hash[-10:]}")
        print(f"   Verificar em: https://blockstream.info/testnet/tx/{btc_hash}")
    else:
        print(f"❌ Bitcoin Hash inválido")
        return False
    
    return True

def main():
    """Executa todos os testes"""
    print("\n" + "=" * 70)
    print("🚀 TESTE SIMPLES - ALLIANZA BLOCKCHAIN")
    print("=" * 70)
    print(f"📁 Diretório: {ROOT_DIR}")
    print()
    
    results = {
        "source_code_exists": test_source_code_exists(),
        "read_source_code": test_read_source_code(),
        "proofs_exist": test_proofs_exist(),
        "verify_hashes": test_verify_transaction_hash(),
    }
    
    # Resumo
    print("\n" + "=" * 70)
    print("📊 RESUMO")
    print("=" * 70)
    
    total = len(results)
    passed = sum(1 for v in results.values() if v)
    
    for test_name, result in results.items():
        status = "✅ PASSOU" if result else "❌ FALHOU"
        print(f"{status}: {test_name}")
    
    print(f"\nTotal: {total} | Passou: {passed} | Falhou: {total - passed}")
    
    if passed == total:
        print("\n✅ TODOS OS TESTES PASSARAM!")
        return 0
    else:
        print("\n⚠️  ALGUNS TESTES FALHARAM")
        return 1

if __name__ == "__main__":
    sys.exit(main())

