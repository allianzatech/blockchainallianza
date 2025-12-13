# test_bridge_fixed.py - TESTE DA BRIDGE CORRIGIDA
import requests
import json

def test_uec_bridge():
    """Testa a bridge UEC após correções"""
    
    base_url = "http://localhost:5008"
    
    print("🚀 TESTANDO BRIDGE UEC CORRIGIDA...")
    
    # 1. Criar wallet UEC
    print("1. Criando wallet UEC...")
    wallet_data = {
        "blockchain_source": "allianza"
    }
    
    try:
        response = requests.post(f"{base_url}/uec/create_wallet", json=wallet_data)
        if response.status_code == 200:
            wallet = response.json()
            print(f"✅ Wallet criada: {wallet['address']}")
            print(f"✅ Bitcoin Address: {wallet['bitcoin_address']}")
            
            # 2. Testar bridge transfer
            print("2. Testando bridge transfer...")
            bridge_data = {
                "token_id": "BTCa",
                "amount": 0.001,
                "external_address": "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa",
                "target_chain": "bitcoin",
                "private_key": wallet["private_key"]
            }
            
            bridge_response = requests.post(f"{base_url}/uec/bridge/transfer", json=bridge_data)
            print(f"🔧 Status Code: {bridge_response.status_code}")
            print(f"🔧 Response: {bridge_response.text}")
            
            if bridge_response.status_code == 200:
                bridge_result = bridge_response.json()
                print(f"✅ Bridge criada com sucesso!")
                print(f"📋 Bridge ID: {bridge_result['bridge_transaction']['bridge_id']}")
            else:
                print(f"❌ Erro na bridge: {bridge_response.json()}")
                
        else:
            print(f"❌ Erro ao criar wallet: {response.text}")
            
    except Exception as e:
        print(f"❌ Erro no teste: {e}")

if __name__ == "__main__":
    test_uec_bridge()