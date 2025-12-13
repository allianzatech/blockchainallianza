# test_uec_complete.py - VERSÃO CORRIGIDA
import requests
import json
import time

BASE_URL = "http://localhost:5008"

def test_uec_complete():
    print("🚀 TESTE COMPLETO DA UEC - UNIVERSAL EXECUTION CHAIN")
    print("=" * 60)
    
    # 1. Criar wallet UEC
    print("1. 🎯 Criando Wallet UEC...")
    wallet_data = {"blockchain_source": "allianza"}
    
    response = requests.post(f"{BASE_URL}/uec/create_wallet", json=wallet_data)
    if response.status_code == 200:
        wallet = response.json()
        print(f"   ✅ Wallet UEC criada: {wallet['address'][:20]}...")
        print(f"   ✅ Bitcoin Address: {wallet['bitcoin_address']}")
        print(f"   ✅ UEC Enabled: {wallet['uec_enabled']}")
        
        # 2. Ver status do sistema
        print("\n2. 📊 Status do Sistema UEC...")
        status_response = requests.get(f"{BASE_URL}/uec/system/status")
        if status_response.status_code == 200:
            status = status_response.json()
            print(f"   ✅ UEC Version: {status['uec_version']}")
            print(f"   ✅ Tokens Suportados: {', '.join(status['supported_tokens'])}")
            print(f"   ✅ Chains Suportadas: {', '.join(status['supported_chains'])}")
        
        # 3. Listar tokens (CORRIGIDO)
        print("\n3. 🎯 Tokens Metaprogramáveis...")
        tokens_response = requests.get(f"{BASE_URL}/uec/tokens")
        if tokens_response.status_code == 200:
            tokens = tokens_response.json()
            for token_id, metadata in tokens['tokens'].items():
                print(f"   ✅ {token_id}: {metadata.get('name', 'N/A')}")
                
                # 🔧 CORREÇÃO: Verificar estrutura dos metadados
                cross_logic = metadata.get('cross_logic_metadata', {})
                if 'allowed_chains' in cross_logic:
                    print(f"      Chains: {', '.join(cross_logic['allowed_chains'])}")
                else:
                    # Tentar outras chaves possíveis
                    chains = cross_logic.get('supported_chains', cross_logic.get('chains', ['N/A']))
                    print(f"      Chains: {', '.join(chains) if isinstance(chains, list) else chains}")
        
        # 4. Validar endereço
        print("\n4. 🔍 Validando Endereço Ethereum...")
        validate_data = {
            "address": "0x48Ec8b17B7af735AB329fA07075247FAf3a09599",
            "chain": "ethereum"
        }
        validate_response = requests.post(f"{BASE_URL}/uec/validate_address", json=validate_data)
        if validate_response.status_code == 200:
            validation = validate_response.json()
            print(f"   ✅ Endereço {validation['address']} é válido para {validation['chain']}: {validation['is_valid']}")
        
        # 5. Testar Bridge
        print("\n5. 🌉 Testando Bridge UEC...")
        bridge_data = {
            "token_id": "ETHa",
            "amount": 2.0,
            "external_address": "0x48Ec8b17B7af735AB329fA07075247FAf3a09599",
            "target_chain": "ethereum",
            "private_key": wallet['private_key']
        }
        
        bridge_response = requests.post(f"{BASE_URL}/uec/bridge/transfer", json=bridge_data)
        if bridge_response.status_code == 200:
            bridge_result = bridge_response.json()
            bridge_id = bridge_result['bridge_transaction']['bridge_id']
            print(f"   ✅ Bridge criada com sucesso!")
            print(f"   📋 Bridge ID: {bridge_id}")
            print(f"   💰 Token: {bridge_result['bridge_transaction']['token']}")
            print(f"   🔗 Para: {bridge_result['bridge_transaction']['to_chain']}")
            
            # 6. Ver status da bridge
            print("\n6. 📈 Verificando Status da Bridge...")
            time.sleep(2)
            status_response = requests.get(f"{BASE_URL}/uec/bridge/status/{bridge_id}")
            if status_response.status_code == 200:
                bridge_status = status_response.json()
                print(f"   ✅ Status: {bridge_status['status']['status']}")
                print(f"   ⏱️  Estimado: {bridge_status['status']['estimated_completion']}")
            
            # 7. Completar bridge (opcional)
            print("\n7. ✅ Completando Bridge...")
            complete_response = requests.post(f"{BASE_URL}/uec/bridge/complete/{bridge_id}")
            if complete_response.status_code == 200:
                complete_result = complete_response.json()
                print(f"   🎉 Bridge completada!")
                print(f"   ✅ Status final: {complete_result['completed_transaction']['status']}")
        
        else:
            print(f"   ❌ Erro na bridge: {bridge_response.json()}")
    
    else:
        print(f"   ❌ Erro ao criar wallet: {response.text}")
    
    print("\n" + "=" * 60)
    print("🎊 TESTE COMPLETO DA UEC FINALIZADO!")

if __name__ == "__main__":
    test_uec_complete()