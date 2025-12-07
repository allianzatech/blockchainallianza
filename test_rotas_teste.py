# test_rotas_teste.py
# 🧪 TESTE RÁPIDO: Verificar se rotas de teste estão funcionando

import requests
import json

BASE_URL = "http://localhost:5008"

def test_route(name, method, endpoint, data=None):
    """Testar uma rota"""
    print(f"\n🔍 Testando: {name}")
    try:
        if method == "GET":
            response = requests.get(f"{BASE_URL}{endpoint}", timeout=5)
        else:
            response = requests.post(
                f"{BASE_URL}{endpoint}",
                json=data,
                headers={"Content-Type": "application/json"},
                timeout=10
            )
        
        if response.status_code == 200:
            print(f"   ✅ Sucesso (200)")
            result = response.json()
            if isinstance(result, dict):
                print(f"   📊 Resultado: {json.dumps(result, indent=2)[:200]}...")
            return True
        elif response.status_code == 429:
            print(f"   ⚠️  Rate limit atingido (429) - Isso é bom! Rate limiting funcionando!")
            return True
        else:
            print(f"   ❌ Erro ({response.status_code}): {response.text[:100]}")
            return False
    except requests.exceptions.ConnectionError:
        print(f"   ❌ Servidor não está rodando. Inicie com: python allianza_blockchain.py")
        return False
    except Exception as e:
        print(f"   ❌ Erro: {str(e)}")
        return False

def main():
    print("="*70)
    print("🧪 TESTE RÁPIDO: ROTAS DE TESTE")
    print("="*70)
    print("\n⚠️  Certifique-se de que o servidor está rodando!")
    print("   Execute: python allianza_blockchain.py")
    print("\n" + "="*70)
    
    tests = [
        ("Página de Testes", "GET", "/test"),
        ("Health Check", "GET", "/health"),
        ("Gas Atual", "GET", "/test/gas/current"),
        ("Validação Bitcoin (hash inválido)", "POST", "/test/validation/bitcoin", {
            "tx_hash": "invalid_hash_test"
        }),
        ("Validação Solana (assinatura inválida)", "POST", "/test/validation/solana", {
            "signature": "invalid_signature_test"
        }),
        ("Proof-of-Lock (dados válidos)", "POST", "/test/proof-of-lock", {
            "source_chain": "polygon",
            "target_chain": "ethereum",
            "amount": 0.1,
            "token_symbol": "MATIC",
            "recipient_address": "0x48Ec8b17B7af735AB329fA07075247FAf3a09599"
        }),
    ]
    
    results = []
    for name, method, endpoint, *args in tests:
        data = args[0] if args else None
        success = test_route(name, method, endpoint, data)
        results.append((name, success))
    
    print("\n" + "="*70)
    print("📊 RESUMO")
    print("="*70)
    
    passed = sum(1 for _, s in results if s)
    total = len(results)
    
    for name, success in results:
        status = "✅" if success else "❌"
        print(f"{status} {name}")
    
    print(f"\n✅ Passou: {passed}/{total}")
    print(f"Taxa de sucesso: {(passed/total*100):.1f}%")
    print("="*70)
    
    if passed == total:
        print("\n🎉 TODAS AS ROTAS ESTÃO FUNCIONANDO!")
        print("✅ Acesse: http://localhost:5008/test")
    else:
        print("\n⚠️  Algumas rotas falharam. Verifique os erros acima.")

if __name__ == "__main__":
    main()





















