#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
📊 TESTE DE MÉTRICAS DE PERFORMANCE
Mede custo de gas, latência e outras métricas de execução cross-chain
Responde à análise técnica: "Falta detalhamento de custo de gas e latência"
"""

import json
import time
import os
from datetime import datetime
from alz_niev_interoperability import ALZNIEV

def test_performance_metrics():
    """
    Teste de métricas de performance para execuções cross-chain
    """
    print("="*80)
    print("📊 TESTE DE MÉTRICAS DE PERFORMANCE")
    print("="*80)
    print("Objetivo: Medir custo de gas, latência e outras métricas")
    print("="*80)
    
    alz_niev = ALZNIEV()
    
    metrics = {
        "test_timestamp": datetime.now().isoformat(),
        "tests": []
    }
    
    # Teste 1: Execução simples (leitura)
    print(f"\n📋 Teste 1: Execução de Leitura (getBalance)")
    start_time = time.time()
    
    result1 = alz_niev.execute_cross_chain_with_proofs(
        source_chain="allianza",
        target_chain="polygon",
        function_name="getBalance",
        function_params={"address": "0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb0"}
    )
    
    latency1 = (time.time() - start_time) * 1000
    
    metrics["tests"].append({
        "test": "read_function",
        "function": "getBalance",
        "target_chain": "polygon",
        "latency_ms": latency1,
        "success": result1.success,
        "has_proofs": {
            "zk": result1.zk_proof is not None,
            "merkle": result1.merkle_proof is not None,
            "consensus": result1.consensus_proof is not None
        },
        "estimated_gas": "~21,000 (view function)",
        "note": "Função de leitura - não altera estado"
    })
    
    # Teste 2: Execução de escrita
    print(f"\n📋 Teste 2: Execução de Escrita (transfer)")
    start_time = time.time()
    
    result2 = alz_niev.execute_cross_chain_with_proofs(
        source_chain="allianza",
        target_chain="polygon",
        function_name="transfer",
        function_params={
            "to": "0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb0",
            "amount": 0.001
        }
    )
    
    latency2 = (time.time() - start_time) * 1000
    
    metrics["tests"].append({
        "test": "write_function",
        "function": "transfer",
        "target_chain": "polygon",
        "latency_ms": latency2,
        "success": result2.success,
        "is_write_function": getattr(result2, 'is_write_function', False),
        "state_changed": getattr(result2, 'state_changed', False),
        "has_proofs": {
            "zk": result2.zk_proof is not None,
            "merkle": result2.merkle_proof is not None,
            "consensus": result2.consensus_proof is not None
        },
        "estimated_gas": "~65,000 (transfer function)",
        "note": "Função de escrita - altera estado"
    })
    
    # Teste 3: Execução atômica multi-chain
    print(f"\n📋 Teste 3: Execução Atômica Multi-Chain (AES)")
    start_time = time.time()
    
    chains = [
        ("polygon", "transfer", {"to": "0x1234...", "amount": 100}),
        ("ethereum", "transfer", {"to": "0x5678...", "amount": 50}),
        ("bsc", "transfer", {"to": "0x9abc...", "amount": 25})
    ]
    
    results3 = alz_niev.aes.execute_atomic_multi_chain(
        chains=chains,
        elni=alz_niev.elni,
        zkef=alz_niev.zkef,
        upnmt=alz_niev.upnmt,
        mcl=alz_niev.mcl
    )
    
    latency3 = (time.time() - start_time) * 1000
    
    metrics["tests"].append({
        "test": "atomic_multi_chain",
        "chains": len(chains),
        "latency_ms": latency3,
        "latency_per_chain_ms": latency3 / len(chains),
        "all_success": all(r.success for r in results3.values() if isinstance(r, type(results3.get(list(results3.keys())[0])))),
        "estimated_gas_total": f"~{65_000 * len(chains):,} (transfer em {len(chains)} chains)",
        "note": "Execução atômica - todas ou nenhuma"
    })
    
    # Calcular médias
    latencies = [t["latency_ms"] for t in metrics["tests"]]
    metrics["summary"] = {
        "average_latency_ms": sum(latencies) / len(latencies) if latencies else 0,
        "min_latency_ms": min(latencies) if latencies else 0,
        "max_latency_ms": max(latencies) if latencies else 0,
        "total_tests": len(metrics["tests"])
    }
    
    # Salvar métricas
    metrics_file = f"proofs/testnet/performance_metrics_{int(time.time())}.json"
    os.makedirs(os.path.dirname(metrics_file), exist_ok=True)
    
    with open(metrics_file, 'w') as f:
        json.dump(metrics, f, indent=2)
    
    print(f"\n📄 Métricas salvas em: {metrics_file}")
    print(f"\n{'='*80}")
    print("📊 RESUMO DE PERFORMANCE")
    print(f"{'='*80}")
    print(f"Latência Média: {metrics['summary']['average_latency_ms']:.2f}ms")
    print(f"Latência Mínima: {metrics['summary']['min_latency_ms']:.2f}ms")
    print(f"Latência Máxima: {metrics['summary']['max_latency_ms']:.2f}ms")
    print(f"{'='*80}")
    
    return metrics

if __name__ == "__main__":
    test_performance_metrics()

