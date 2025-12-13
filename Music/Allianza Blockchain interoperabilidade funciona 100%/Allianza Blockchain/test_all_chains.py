# test_all_chains.py
# Script para testar todas as conexões de blockchain
import requests
import json

BASE_URL = "http://localhost:5008"

def test_endpoint(endpoint, method="GET", data=None):
    """Testar um endpoint"""
    try:
        url = f"{BASE_URL}{endpoint}"
        if method == "GET":
            response = requests.get(url, timeout=10)
        else:
            response = requests.post(url, json=data, timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            return {"success": True, "data": result}
        else:
            return {"success": False, "error": f"Status {response.status_code}", "data": response.text}
    except Exception as e:
        return {"success": False, "error": str(e)}

def main():
    print("=" * 60)
    print("🧪 TESTE COMPLETO DE TODAS AS BLOCKCHAINS")
    print("=" * 60)
    
    tests = [
        ("Health Check", "/health", "GET"),
        ("Advanced Interop Status", "/advanced/interop/status", "GET"),
        ("Quantum Security Status", "/quantum/security/status", "GET"),
        ("Bitcoin Demo Swap", "/bitcoin/demo/swap", "POST"),
        ("Advanced Interop Demo", "/advanced/interop/demo", "POST"),
        ("Quantum Security Demo", "/quantum/security/demo", "POST"),
        ("Intelligent Route", "/advanced/interop/intelligent_route", "POST", {
            "operation": "swap",
            "amount": 1.0,
            "from_address": "0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb",
            "to_address": "0x86AE40869EB6ACb9477b42BfC9150c0A2Cc21f5E"
        }),
        ("DeFi Aggregator", "/advanced/interop/defi_aggregator", "POST", {
            "token": "ETH",
            "amount": 1.0,
            "operation": "swap"
        }),
        ("ML-DSA Keypair", "/quantum/security/ml_dsa/keypair", "POST", {
            "security_level": 3
        }),
        ("Hybrid Keypair", "/quantum/security/hybrid/keypair", "POST"),
    ]
    
    results = []
    for name, endpoint, method, *args in tests:
        data = args[0] if args else None
        print(f"\n🔍 Testando: {name}")
        result = test_endpoint(endpoint, method, data)
        results.append((name, result))
        
        if result["success"]:
            print(f"   ✅ Sucesso!")
            if "connected_chains" in result.get("data", {}):
                chains = result["data"]["connected_chains"]
                print(f"   📊 Chains conectadas: {len(chains)}")
                for chain in chains:
                    print(f"      - {chain}")
        else:
            print(f"   ❌ Erro: {result.get('error', 'Unknown')}")
    
    print("\n" + "=" * 60)
    print("📊 RESUMO DOS TESTES")
    print("=" * 60)
    
    success_count = sum(1 for _, r in results if r["success"])
    total_count = len(results)
    
    print(f"✅ Sucessos: {success_count}/{total_count}")
    print(f"❌ Falhas: {total_count - success_count}/{total_count}")
    
    for name, result in results:
        status = "✅" if result["success"] else "❌"
        print(f"{status} {name}")
    
    print("=" * 60)

if __name__ == "__main__":
    main()
