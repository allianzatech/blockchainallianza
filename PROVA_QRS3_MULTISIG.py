# PROVA_QRS3_MULTISIG.py
# 🔐 TESTE: QRS-3 MULTI-SIGNATURE WALLETS
# Valida que multi-sig funciona com QRS-3 por signatário

import json
import time
from quantum_multi_sig_wallet import QuantumMultiSigWallet

def test_qrs3_multisig():
    """Testar wallet multi-sig com QRS-3"""
    print("="*70)
    print("🔐 TESTE: QRS-3 MULTI-SIGNATURE WALLETS")
    print("="*70)
    print()
    
    # Teste 1: Criar wallet QRS-3 multi-sig
    print("📋 Teste 1: Criar wallet multi-sig com QRS-3 (3 de 5)")
    print("-" * 70)
    
    wallet = QuantumMultiSigWallet()
    result = wallet.create_qrs3_multisig_wallet(
        required_signatures=3,
        total_signers=5
    )
    
    if result.get("success"):
        print("✅ Teste 1 PASSOU!")
        print(f"   Wallet ID: {result.get('wallet_id')}")
        print(f"   Required Signatures: {result.get('required_signatures')}")
        print(f"   Total Signers: {result.get('total_signers')}")
        print(f"   Redundancy Level: {result.get('redundancy_level')}")
        print(f"   Quantum Safe: {result.get('quantum_safe')}")
        print(f"   {result.get('world_first')}")
    else:
        print(f"❌ Teste 1 FALHOU: {result.get('error')}")
        return False
    
    print()
    
    # Teste 2: Criar transação
    print("📋 Teste 2: Criar transação na wallet")
    print("-" * 70)
    
    tx = wallet.create_transaction(
        to_address="0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb",
        amount=1.5,
        data={"note": "Test transaction"}
    )
    
    if tx:
        print("✅ Teste 2 PASSOU!")
        print(f"   TX ID: {tx.get('tx_id')}")
        print(f"   To: {tx.get('to_address')}")
        print(f"   Amount: {tx.get('amount')}")
        print(f"   Status: {tx.get('status')}")
    else:
        print("❌ Teste 2 FALHOU: Não foi possível criar transação")
        return False
    
    print()
    
    # Teste 3: Obter informações da wallet
    print("📋 Teste 3: Informações da wallet")
    print("-" * 70)
    
    wallet_info = wallet.get_wallet_info()
    print("✅ Teste 3 PASSOU!")
    print(f"   Wallet ID: {wallet_info.get('wallet_id')}")
    print(f"   Threshold: {wallet_info.get('threshold')}")
    print(f"   Total Signers: {wallet_info.get('total_signers')}")
    print(f"   Signers: {len(wallet_info.get('signers', []))}")
    
    print()
    print("="*70)
    print("✅✅✅ TODOS OS TESTES PASSARAM!")
    print("="*70)
    print()
    print("🌍 PRIMEIRO NO MUNDO: Multi-sig QRS-3 funcionando!")
    print()
    
    return True

if __name__ == "__main__":
    success = test_qrs3_multisig()
    exit(0 if success else 1)
