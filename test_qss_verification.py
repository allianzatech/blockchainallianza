#!/usr/bin/env python3
"""
Teste real de verificação QSS
Testa a verificação de uma prova gerada
"""

import requests
import json
import hashlib
import base64

# URL da API QSS
API_URL = "https://testnet.allianza.tech/api/qss"

def test_generate_and_verify():
    """Testa geração e verificação de prova"""
    
    print("🔐 Teste de Geração e Verificação QSS\n")
    print("=" * 60)
    
    # 1. Gerar prova
    print("\n1️⃣ Gerando prova quântica...")
    generate_data = {
        "chain": "bitcoin",
        "tx_hash": "89b6d1b46c2a1f93bd1d9ccc95dd25b46a81c7f37cb7b2a11abbebd29ddafaeb",
        "metadata": {
            "block_height": 0,
            "amount": "0.01"
        }
    }
    
    try:
        response = requests.post(f"{API_URL}/generate-proof", json=generate_data, timeout=30)
        response.raise_for_status()
        result = response.json()
        
        if not result.get('success'):
            print(f"❌ Erro ao gerar prova: {result.get('error')}")
            return
        
        proof = result['quantum_proof']
        print(f"✅ Prova gerada!")
        print(f"   Proof ID: {proof.get('proof_id')}")
        print(f"   Proof Hash: {proof.get('proof_hash')}")
        print(f"   Keypair ID: {proof.get('keypair_id')}")
        
        # 2. Verificar prova
        print("\n2️⃣ Verificando prova...")
        verify_data = {
            "quantum_proof": proof
        }
        
        response = requests.post(f"{API_URL}/verify-proof", json=verify_data, timeout=30)
        response.raise_for_status()
        verify_result = response.json()
        
        print(f"\n📊 Resultado da Verificação:")
        print(f"   Success: {verify_result.get('success')}")
        print(f"   Valid: {verify_result.get('valid')}")
        
        if verify_result.get('verification_details'):
            details = verify_result['verification_details']
            print(f"\n   Detalhes:")
            print(f"   - Signature Valid: {details.get('signature_valid')}")
            print(f"   - Proof Hash Valid: {details.get('proof_hash_valid')}")
            print(f"   - Timestamp Valid: {details.get('timestamp_valid')}")
            print(f"   - Merkle Proof Valid: {details.get('merkle_proof_valid')}")
        
        # 3. Verificar proof_hash manualmente
        print("\n3️⃣ Verificando proof_hash manualmente...")
        if proof.get('canonicalization') and proof.get('canonical_json'):
            canonical_json = proof['canonicalization']['canonical_json']
            computed_hash = hashlib.sha256(canonical_json.encode()).hexdigest()
            expected_hash = proof.get('proof_hash')
            
            print(f"   Canonical JSON: {canonical_json[:100]}...")
            print(f"   Computed Hash: {computed_hash}")
            print(f"   Expected Hash: {expected_hash}")
            print(f"   Match: {computed_hash == expected_hash}")
        
        # 4. Verificar chave pública
        print("\n4️⃣ Verificando chave pública...")
        keypair_id = proof.get('keypair_id')
        if keypair_id:
            try:
                response = requests.get(f"{API_URL}/key/{keypair_id}", timeout=10)
                if response.status_code == 200:
                    key_data = response.json()
                    print(f"   ✅ Chave pública encontrada!")
                    print(f"   Algorithm: {key_data.get('algorithm')}")
                    print(f"   Implementation: {key_data.get('implementation')}")
                else:
                    print(f"   ⚠️  Chave não encontrada (status: {response.status_code})")
            except Exception as e:
                print(f"   ⚠️  Erro ao buscar chave: {e}")
        
        print("\n" + "=" * 60)
        if verify_result.get('valid'):
            print("✅ TESTE PASSOU - Prova válida!")
        else:
            print("❌ TESTE FALHOU - Prova inválida")
            print(f"   Erro: {verify_result.get('error', 'Unknown')}")
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Erro de conexão: {e}")
    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_generate_and_verify()

