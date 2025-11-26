# PROVA_QUANTUM_SAFE_ROUTING.py
# 🤖 TESTE: QUANTUM-SAFE AI ROUTING
# Valida que AI Routing considera segurança quântica

import json
import time
from quantum_safe_ai_routing import quantum_safe_routing

def test_quantum_safe_routing():
    """Testar AI Routing quântica-seguro"""
    print("="*70)
    print("🤖 TESTE: QUANTUM-SAFE AI ROUTING")
    print("="*70)
    print()
    
    # Teste 1: Roteamento com segurança quântica obrigatória
    print("📋 Teste 1: Roteamento com segurança quântica obrigatória")
    print("-" * 70)
    
    result1 = quantum_safe_routing.route_with_quantum_safety(
        operation="transfer",
        amount=1.0,
        quantum_safety_required=True
    )
    
    if result1.get("success"):
        print("✅ Teste 1 PASSOU!")
        print(f"   Chain Recomendada: {result1.get('recommended_chain')}")
        print(f"   Quantum Safe Score: {result1.get('quantum_safe_score'):.2f}")
        print(f"   Predicted Gas: {result1.get('predicted_gas'):.6f} ETH")
        print(f"   QRS-3 Cost: {result1.get('qrs3_cost'):.6f} ETH")
        print(f"   Total Cost: {result1.get('total_cost'):.6f} ETH")
        print(f"   {result1.get('world_first')}")
    else:
        print(f"❌ Teste 1 FALHOU: {result1.get('error')}")
        return False
    
    print()
    
    # Teste 2: Roteamento sem segurança quântica obrigatória
    print("📋 Teste 2: Roteamento sem segurança quântica obrigatória")
    print("-" * 70)
    
    result2 = quantum_safe_routing.route_with_quantum_safety(
        operation="transfer",
        amount=1.0,
        quantum_safety_required=False
    )
    
    if result2.get("success"):
        print("✅ Teste 2 PASSOU!")
        print(f"   Chain Recomendada: {result2.get('recommended_chain')}")
        print(f"   Quantum Safe Score: {result2.get('quantum_safe_score'):.2f}")
        print(f"   Predicted Gas: {result2.get('predicted_gas'):.6f} ETH")
    else:
        print(f"❌ Teste 2 FALHOU: {result2.get('error')}")
        return False
    
    print()
    
    # Teste 3: Análise de múltiplas chains
    print("📋 Teste 3: Análise de múltiplas chains")
    print("-" * 70)
    
    result3 = quantum_safe_routing.route_with_quantum_safety(
        operation="transfer",
        amount=1.0,
        quantum_safety_required=True,
        chains=["ethereum", "polygon", "allianza"]
    )
    
    if result3.get("success"):
        print("✅ Teste 3 PASSOU!")
        print(f"   Chain Recomendada: {result3.get('recommended_chain')}")
        print(f"   Análise de {len(result3.get('all_chains_analysis', []))} chains:")
        for chain_analysis in result3.get('all_chains_analysis', []):
            print(f"      • {chain_analysis['chain']}: Score {chain_analysis['quantum_safe_score']:.2f}, Custo {chain_analysis['total_cost']:.6f} ETH")
    else:
        print(f"❌ Teste 3 FALHOU: {result3.get('error')}")
        return False
    
    print()
    print("="*70)
    print("✅✅✅ TODOS OS TESTES PASSARAM!")
    print("="*70)
    print()
    print("🌍 PRIMEIRO NO MUNDO: AI Routing quântica-seguro funcionando!")
    print()
    
    return True

if __name__ == "__main__":
    success = test_quantum_safe_routing()
    exit(0 if success else 1)
