# test_bitcoin_bridge.py
import requests
import json
import time

BASE_URL = "http://localhost:5008"

def test_bitcoin_bridge():
    print("🎯 TESTANDO BRIDGE BITCOIN UEC")
    print("=" * 50)
    
    # 1. Criar wallet UEC
    print("1. 🎯 Criando Wallet UEC...")
    response = requests.post(f"{BASE_URL}/uec/create_wallet", json={})
    wallet = response.json()
    print(f"✅ Wallet: {wallet['address'][:15]}...")
    print(f"✅ Bitcoin: {wallet['bitcoin_address']}")
    
    # 2. Validar endereço Bitcoin
    print("\n2. 🔍 Validando Endereço Bitcoin...")
    validate_data = {
        "address": "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa",  # Endereço do Satoshi!
        "chain": "bitcoin"
    }
    validate_response = requests.post(f"{BASE_URL}/uec/validate_address", json=validate_data)
    validation = validate_response.json()
    print(f"✅ Endereço Bitcoin válido: {validation['is_valid']}")
    
    # 3. Testar Bridge BTCa → Bitcoin
    print("\n3. 🌉 Bridge BTCa → Bitcoin...")
    bridge_data = {
        "token_id": "BTCa",
        "amount": 0.1,
        "external_address": "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa",
        "target_chain": "bitcoin",
        "private_key": wallet['private_key']
    }
    
    bridge_response = requests.post(f"{BASE_URL}/uec/bridge/transfer", json=bridge_data)
    if bridge_response.status_code == 200:
        result = bridge_response.json()
        bridge_id = result['bridge_transaction']['bridge_id']
        print(f"✅ Bridge Bitcoin criada!")
        print(f"📋 Bridge ID: {bridge_id}")
        
        # 4. Ver status
        print("\n4. 📊 Status da Bridge Bitcoin...")
        time.sleep(2)
        status_response = requests.get(f"{BASE_URL}/uec/bridge/status/{bridge_id}")
        status = status_response.json()
        print(f"✅ Status: {status['status']['status']}")
        
        # 5. Completar
        print("\n5. ✅ Completando Bridge Bitcoin...")
        complete_response = requests.post(f"{BASE_URL}/uec/bridge/complete/{bridge_id}")
        if complete_response.status_code == 200:
            print("🎉 Bridge Bitcoin completada!")
            final_result = complete_response.json()
            print(f"💰 TX Final: {final_result['completed_transaction']['completion_tx']}")
    
    print("\n" + "=" * 50)
    print("✅ TESTE BITCOIN CONCLUÍDO!")

if __name__ == "__main__":
    test_bitcoin_bridge()