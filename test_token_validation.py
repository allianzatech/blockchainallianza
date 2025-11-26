# test_token_validation_fixed.py - TESTE COM REGRAS ATUALIZADAS
import requests
import time

BASE_URL = "http://localhost:5008"

def test_token_validation_fixed():
    print("🎯 TESTE DE VALIDAÇÃO - REGRAS ATUALIZADAS")
    print("=" * 50)
    
    try:
        # Criar wallet
        print("1. 🎯 Criando Wallet UEC...")
        wallet_response = requests.post(f"{BASE_URL}/uec/create_wallet", json={})
        if wallet_response.status_code != 200:
            print(f"❌ Erro ao criar wallet: {wallet_response.text}")
            return
            
        wallet = wallet_response.json()
        print(f"✅ Wallet: {wallet['address'][:15]}...")
        
        # 🔧 CORREÇÃO: Regras atualizadas baseadas no diagnóstico
        test_cases = [
            # (token, chain, should_work, description)
            ("BTCa", "bitcoin", True, "BTCa → Bitcoin (VÁLIDO)"),
            ("BTCa", "ethereum", False, "BTCa → Ethereum (INVÁLIDO)"),
            ("ETHa", "ethereum", True, "ETHa → Ethereum (VÁLIDO)"),
            ("ETHa", "polygon", True, "ETHa → Polygon (VÁLIDO)"), 
            ("ETHa", "bsc", True, "ETHa → BSC (VÁLIDO)"),
            ("USDa", "ethereum", True, "USDa → Ethereum (VÁLIDO)"),
            ("USDa", "polygon", True, "USDa → Polygon (VÁLIDO)"),
            ("USDa", "bsc", True, "USDa → BSC (VÁLIDO)"),
            ("BTCa", "solana", False, "BTCa → Solana (INVÁLIDO)"),
        ]
        
        print("\n2. 🧪 Testando com regras atualizadas...\n")
        
        results = []
        for token, chain, should_work, description in test_cases:
            external_address = (
                "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa" if chain == "bitcoin"
                else "0x742d35Cc6634C0532925a3b844Bc454e4438f44e"
            )
            
            bridge_data = {
                "token_id": token,
                "amount": 0.1,
                "external_address": external_address,
                "target_chain": chain,
                "private_key": wallet['private_key']
            }
            
            response = requests.post(f"{BASE_URL}/uec/bridge/transfer", json=bridge_data)
            
            if should_work:
                if response.status_code == 200:
                    print(f"✅ {description} - FUNCIONOU")
                    results.append("PASS")
                else:
                    error = response.json().get('error', 'Erro desconhecido')
                    print(f"❌ {description} - FALHOU: {error}")
                    results.append("FAIL")
            else:
                if response.status_code != 200:
                    print(f"✅ {description} - BLOQUEADO (correto)")
                    results.append("PASS")
                else:
                    print(f"❌ {description} - DEVERIA BLOQUEAR")
                    results.append("FAIL")
            
            time.sleep(0.3)
        
        # Resultado
        passed = results.count("PASS")
        total = len(results)
        print(f"\n📊 Resultado: {passed}/{total} testes passaram")
        
        if passed == total:
            print("🎉 TODOS OS TESTES PASSARAM!")
        else:
            print(f"💡 {total - passed} testes falharam - verifique as regras dos tokens")
            
    except Exception as e:
        print(f"❌ Erro no teste: {e}")

if __name__ == "__main__":
    test_token_validation_fixed()