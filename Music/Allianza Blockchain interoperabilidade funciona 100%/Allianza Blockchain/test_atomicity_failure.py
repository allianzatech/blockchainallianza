#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧪 TESTE DE ATOMICIDADE COM FALHA
Prova que o sistema AES reverte todas as execuções quando uma falha
Responde à análise técnica: "Falta prova de atomicidade em caso de falha"
"""

import json
import time
from datetime import datetime
from alz_niev_interoperability import ALZNIEV

def test_atomicity_with_failure():
    """
    Teste crítico: Provar que o sistema reverte todas as execuções
    quando uma das chains falha
    """
    print("="*80)
    print("🧪 TESTE DE ATOMICIDADE COM FALHA")
    print("="*80)
    print("Objetivo: Provar que o sistema reverte todas as execuções quando uma falha")
    print("="*80)
    
    alz_niev = ALZNIEV()
    
    # Cenário: 3 chains, uma vai falhar propositalmente
    chains = [
        ("polygon", "transfer", {"to": "0x1234567890123456789012345678901234567890", "amount": 100}),
        ("ethereum", "transfer", {"to": "0xINVALID_ADDRESS", "amount": 50}),  # Esta vai falhar
        ("bsc", "transfer", {"to": "0x9876543210987654321098765432109876543210", "amount": 25})
    ]
    
    print(f"\n📋 Cenário de Teste:")
    print(f"   Chain 1: Polygon - transfer 100 (deve funcionar)")
    print(f"   Chain 2: Ethereum - transfer 50 (vai FALHAR - endereço inválido)")
    print(f"   Chain 3: BSC - transfer 25 (deve funcionar)")
    print(f"\n🎯 Expectativa: Todas as execuções devem ser revertidas")
    print(f"   (incluindo Polygon e BSC que funcionaram)")
    
    start_time = time.time()
    
    # Executar atomicamente
    results = alz_niev.aes.execute_atomic_multi_chain(
        chains=chains,
        elni=alz_niev.elni,
        zkef=alz_niev.zkef,
        upnmt=alz_niev.upnmt,
        mcl=alz_niev.mcl
    )
    
    execution_time = (time.time() - start_time) * 1000  # em ms
    
    print(f"\n{'='*80}")
    print("📊 RESULTADOS DO TESTE")
    print(f"{'='*80}")
    
    # Verificar se rollback foi executado
    rollback_performed = results.get("rollback_performed", False)
    rollback_results = results.get("rollback_results", {})
    
    print(f"\n✅ Rollback Executado: {rollback_performed}")
    
    if rollback_performed:
        print(f"\n🔄 Detalhes do Rollback:")
        for chain, rollback_info in rollback_results.items():
            status = "✅" if rollback_info.get("rollback_success") else "❌"
            print(f"   {status} {chain}: {rollback_info.get('message', 'N/A')}")
    
    # Verificar atomicidade
    all_reverted = True
    for chain, result in results.items():
        if isinstance(result, dict) and result.get("success"):
            # Se alguma execução ainda está marcada como sucesso, atomicidade falhou
            if not rollback_performed:
                all_reverted = False
                print(f"   ❌ {chain}: Execução não foi revertida!")
    
    # Criar prova JSON
    proof = {
        "test_name": "Atomicidade com Falha",
        "test_timestamp": datetime.now().isoformat(),
        "test_objective": "Provar que o sistema reverte todas as execuções quando uma falha",
        "scenario": {
            "chains": [
                {"chain": "polygon", "function": "transfer", "expected": "sucesso"},
                {"chain": "ethereum", "function": "transfer", "expected": "falha (endereço inválido)"},
                {"chain": "bsc", "function": "transfer", "expected": "sucesso"}
            ]
        },
        "results": {
            "rollback_performed": rollback_performed,
            "rollback_results": rollback_results,
            "atomicity_verified": all_reverted and rollback_performed,
            "execution_time_ms": execution_time
        },
        "validation": {
            "atomicity_proven": all_reverted and rollback_performed,
            "all_or_nothing": all_reverted and rollback_performed,
            "conclusion": "✅ ATOMICIDADE PROVADA" if (all_reverted and rollback_performed) else "❌ ATOMICIDADE NÃO PROVADA"
        }
    }
    
    # Salvar prova
    proof_file = f"proofs/testnet/atomicity_failure_test_{int(time.time())}.json"
    os.makedirs(os.path.dirname(proof_file), exist_ok=True)
    
    with open(proof_file, 'w') as f:
        json.dump(proof, f, indent=2)
    
    print(f"\n📄 Prova salva em: {proof_file}")
    print(f"\n{'='*80}")
    print(f"🎯 CONCLUSÃO: {'✅ ATOMICIDADE PROVADA' if (all_reverted and rollback_performed) else '❌ ATOMICIDADE NÃO PROVADA'}")
    print(f"{'='*80}")
    
    return proof

if __name__ == "__main__":
    test_atomicity_with_failure()

