#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧪 TESTE DO QaaS ENTERPRISE
"""

import requests
import hashlib
import time

def test_enterprise_service():
    """Testar serviço enterprise"""
    base_url = "http://localhost:5010"
    
    print("="*70)
    print("🧪 TESTE DO QUANTUM SECURITY AS A SERVICE - ENTERPRISE")
    print("="*70)
    
    # Teste 1: Health Check
    print("\n📋 TESTE 1: Health Check")
    print("-" * 70)
    try:
        response = requests.get(f"{base_url}/api/v1/health", timeout=5)
        print(f"✅ Status: {response.json().get('status')}")
        print(f"   Service: {response.json().get('service')}")
    except Exception as e:
        print(f"❌ Erro: {e}")
        print("⚠️  Serviço não está rodando. Inicie com: python qaas_enterprise.py")
        return
    
    # Teste 2: Gerar API Key
    print("\n📋 TESTE 2: Gerar API Key")
    print("-" * 70)
    response = requests.post(f"{base_url}/api/v1/auth/generate-key", json={
        "user_id": "test_user_123",
        "blockchain": "ethereum",
        "permissions": ["sign", "verify"],
        "rate_limit": 1000
    })
    
    if response.status_code == 200:
        api_data = response.json()
        api_key = api_data["api_key"]
        print(f"✅ API Key gerada: {api_key[:30]}...")
        print(f"   Key ID: {api_data['key_id']}")
        print(f"   User ID: {api_data['user_id']}")
        print(f"   Rate Limit: {api_data['rate_limit']}")
    else:
        print(f"❌ Erro: {response.json()}")
        return
    
    # Teste 3: Gerar Keypair (com autenticação)
    print("\n📋 TESTE 3: Gerar Keypair (com autenticação)")
    print("-" * 70)
    headers = {"X-API-Key": api_key}
    response = requests.post(f"{base_url}/api/v1/keypair/generate", json={
        "blockchain": "ethereum",
        "algorithm": "ML-DSA-128",
        "security_level": 3
    }, headers=headers)
    
    if response.status_code == 200:
        keypair = response.json()
        print(f"✅ Keypair gerado: {keypair['keypair_id'][:50]}...")
        print(f"   Real: {keypair.get('real', False)}")
        keypair_id = keypair["keypair_id"]
        public_key = keypair["public_key"]
    else:
        print(f"❌ Erro: {response.json()}")
        return
    
    # Teste 4: Assinar Transação
    print("\n📋 TESTE 4: Assinar Transação")
    print("-" * 70)
    tx_hash = "0x" + hashlib.sha256(f"test_{time.time()}".encode()).hexdigest()
    response = requests.post(f"{base_url}/api/v1/signature/sign", json={
        "blockchain": "ethereum",
        "transaction_hash": tx_hash,
        "keypair_id": keypair_id,
        "algorithm": "ML-DSA-128"
    }, headers=headers)
    
    if response.status_code == 200:
        signature = response.json()
        print(f"✅ Assinatura criada: {signature['signature'][:50]}...")
        print(f"   Request ID: {signature.get('request_id', 'N/A')}")
        sig_value = signature["signature"]
    else:
        print(f"❌ Erro: {response.json()}")
        return
    
    # Teste 5: Verificar Assinatura
    print("\n📋 TESTE 5: Verificar Assinatura")
    print("-" * 70)
    response = requests.post(f"{base_url}/api/v1/signature/verify", json={
        "blockchain": "ethereum",
        "transaction_hash": tx_hash,
        "signature": sig_value,
        "public_key": public_key,
        "algorithm": "ML-DSA-128"
    }, headers=headers)
    
    if response.status_code == 200:
        verification = response.json()
        print(f"✅ Verificação: {'Válida' if verification.get('valid') else 'Inválida'}")
        print(f"   Real: {verification.get('real', False)}")
    else:
        print(f"❌ Erro: {response.json()}")
    
    # Teste 6: Métricas
    print("\n📋 TESTE 6: Métricas de Monitoramento")
    print("-" * 70)
    response = requests.get(f"{base_url}/api/v1/monitoring/metrics", headers=headers)
    if response.status_code == 200:
        metrics = response.json()
        print(f"✅ Métricas obtidas:")
        print(f"   Requests/min: {metrics.get('requests_per_minute', 0)}")
        print(f"   Errors/min: {metrics.get('errors_per_minute', 0)}")
        print(f"   Avg Latency: {metrics.get('average_latency_ms', 0):.2f}ms")
        print(f"   P95 Latency: {metrics.get('p95_latency_ms', 0):.2f}ms")
    
    # Teste 7: Logs de Auditoria
    print("\n📋 TESTE 7: Logs de Auditoria")
    print("-" * 70)
    response = requests.get(f"{base_url}/api/v1/audit/logs?limit=5", headers=headers)
    if response.status_code == 200:
        logs = response.json()
        print(f"✅ Logs obtidos: {len(logs.get('logs', []))} entradas")
        for log in logs.get("logs", [])[:3]:
            print(f"   • {log.get('action')} - {log.get('blockchain')} - {log.get('success')}")
    
    print("\n" + "="*70)
    print("✅ TODOS OS TESTES CONCLUÍDOS!")
    print("="*70)

if __name__ == '__main__':
    test_enterprise_service()



