#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧪 TESTE COMPLETO DO QaaS SERVICE
"""

import time
import hashlib
from qaas_integration_sdk import QaaSSDK

def test_qaas_service():
    """Testar todos os endpoints do QaaS"""
    print("="*70)
    print("🧪 TESTE COMPLETO DO QUANTUM SECURITY AS A SERVICE")
    print("="*70)
    
    # Inicializar SDK
    sdk = QaaSSDK(api_url="http://localhost:5009")
    
    # Teste 1: Health Check
    print("\n📋 TESTE 1: Health Check")
    print("-" * 70)
    try:
        health = sdk.health_check()
        print(f"✅ Status: {health.get('status', 'unknown')}")
        print(f"   Service: {health.get('service', 'N/A')}")
        print(f"   Version: {health.get('version', 'N/A')}")
    except Exception as e:
        print(f"❌ Erro: {e}")
        print("⚠️  Serviço não está rodando. Inicie com: python quantum_security_service.py")
        return
    
    # Teste 2: Gerar Keypair
    print("\n📋 TESTE 2: Gerar Keypair para Ethereum")
    print("-" * 70)
    keypair = sdk.generate_keypair("ethereum", algorithm="ML-DSA-128")
    if keypair.get("success"):
        print(f"✅ Keypair gerado com sucesso!")
        print(f"   Keypair ID: {keypair['keypair_id']}")
        print(f"   Algorithm: {keypair['algorithm']}")
        print(f"   Real: {keypair.get('real', False)}")
        print(f"   Public Key: {keypair['public_key'][:50]}...")
        keypair_id = keypair["keypair_id"]
        public_key = keypair["public_key"]
    else:
        print(f"❌ Erro ao gerar keypair: {keypair.get('error', 'Unknown')}")
        return
    
    # Teste 3: Assinar Transação
    print("\n📋 TESTE 3: Assinar Transação")
    print("-" * 70)
    tx_hash = "0x" + hashlib.sha256(f"test_transaction_{time.time()}".encode()).hexdigest()
    print(f"   Transaction Hash: {tx_hash[:50]}...")
    
    signature = sdk.sign_transaction("ethereum", tx_hash, keypair_id)
    if signature.get("success"):
        print(f"✅ Assinatura criada com sucesso!")
        print(f"   Signature: {signature['signature'][:50]}...")
        print(f"   Real: {signature.get('real', False)}")
        print(f"   From Cache: {signature.get('from_cache', False)}")
        sig_value = signature["signature"]
    else:
        print(f"❌ Erro ao assinar: {signature.get('error', 'Unknown')}")
        return
    
    # Teste 4: Verificar Assinatura
    print("\n📋 TESTE 4: Verificar Assinatura")
    print("-" * 70)
    verification = sdk.verify_signature("ethereum", tx_hash, sig_value, public_key)
    if verification.get("valid"):
        print(f"✅ Assinatura válida!")
        print(f"   Algorithm: {verification.get('algorithm', 'N/A')}")
        print(f"   Real: {verification.get('real', False)}")
    else:
        print(f"❌ Assinatura inválida: {verification.get('error', 'Unknown')}")
    
    # Teste 5: Batch Sign
    print("\n📋 TESTE 5: Batch Sign (Múltiplas Transações)")
    print("-" * 70)
    transactions = [
        {"transaction_hash": "0x" + hashlib.sha256(f"tx1_{i}".encode()).hexdigest()}
        for i in range(5)
    ]
    print(f"   Assinando {len(transactions)} transações...")
    
    batch_result = sdk.batch_sign("ethereum", transactions, keypair_id)
    if batch_result.get("signatures"):
        print(f"✅ Batch sign concluído!")
        print(f"   Total: {batch_result.get('total', 0)}")
        print(f"   Successful: {batch_result.get('successful', 0)}")
        print(f"   Failed: {batch_result.get('failed', 0)}")
    
    # Teste 6: Estatísticas
    print("\n📋 TESTE 6: Estatísticas do Serviço")
    print("-" * 70)
    stats = sdk.get_statistics()
    print(f"✅ Estatísticas obtidas:")
    print(f"   Keys Generated: {stats.get('keys_generated', 0)}")
    print(f"   Signatures Created: {stats.get('signatures_created', 0)}")
    print(f"   Verifications: {stats.get('verifications', 0)}")
    print(f"   Blockchains: {', '.join(stats.get('blockchains_supported', []))}")
    print(f"   Total Requests: {stats.get('total_requests', 0)}")
    print(f"   Cache Size: {stats.get('cache_size', 0)}")
    
    # Teste 7: Blockchains Suportadas
    print("\n📋 TESTE 7: Blockchains Suportadas")
    print("-" * 70)
    supported = sdk.get_supported_blockchains()
    print(f"✅ Blockchains suportadas:")
    for bc in supported.get("blockchains", []):
        print(f"   • {bc}")
    print(f"\n   Algorithms: {', '.join(supported.get('algorithms', []))}")
    
    print("\n" + "="*70)
    print("✅ TODOS OS TESTES CONCLUÍDOS!")
    print("="*70)

if __name__ == '__main__':
    test_qaas_service()



