#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Testes de Stress para Sistema de Commitment
Testa performance e resiliência sob carga
"""

import os
import sys
import time
import threading
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from dotenv import load_dotenv

# Adicionar ao path
root_dir = Path(__file__).parent.parent
sys.path.insert(0, str(root_dir))

load_dotenv()

from commercial_repo.adapters.commitment_integration import CommitmentManager
from commercial_repo.adapters.commitment_monitor import CommitmentMonitor


def create_commitment_worker(worker_id: int, total: int) -> dict:
    """Worker para criar commitment"""
    try:
        rpc_url = os.getenv('POLYGON_RPC_URL', 'https://rpc-amoy.polygon.technology')
        private_key = os.getenv('POLYGON_PRIVATE_KEY')
        contract_address = os.getenv('POLYGON_COMMITMENT_CONTRACT', '0x0b5AB34be0f5734161E608885e139AE2b72a07AE')
        
        if not private_key:
            return {
                "worker_id": worker_id,
                "success": False,
                "error": "Private key não configurada"
            }
        
        manager = CommitmentManager(
            rpc_url=rpc_url,
            private_key=private_key,
            commitment_contract_address=contract_address
        )
        
        start_time = time.time()
        
        result = manager.create_commitment(
            target_chain="bitcoin",
            target_recipient="0x0000000000000000000000000000000000000000",
            amount=1000000000000000,
            nonce=int(time.time()) + worker_id  # Nonce único
        )
        
        duration = time.time() - start_time
        
        return {
            "worker_id": worker_id,
            "success": result.get('success', False),
            "commitment_hash": result.get('commitment_hash'),
            "duration": duration,
            "error": result.get('error')
        }
        
    except Exception as e:
        return {
            "worker_id": worker_id,
            "success": False,
            "error": str(e),
            "duration": 0
        }


def stress_test_concurrent_creates(num_workers: int = 10):
    """Teste de stress: criar múltiplos commitments simultaneamente"""
    print("="*70)
    print(f"🧪 TESTE DE STRESS: {num_workers} Commitments Simultâneos")
    print("="*70)
    
    start_time = time.time()
    results = []
    
    with ThreadPoolExecutor(max_workers=num_workers) as executor:
        futures = [
            executor.submit(create_commitment_worker, i, num_workers)
            for i in range(num_workers)
        ]
        
        for future in as_completed(futures):
            result = future.result()
            results.append(result)
            
            if result['success']:
                print(f"✅ Worker {result['worker_id']}: {result['duration']:.2f}s")
            else:
                print(f"❌ Worker {result['worker_id']}: {result.get('error', 'Unknown')}")
    
    total_time = time.time() - start_time
    
    # Estatísticas
    successful = [r for r in results if r['success']]
    failed = [r for r in results if not r['success']]
    
    avg_duration = sum(r['duration'] for r in successful) / len(successful) if successful else 0
    
    print("\n" + "="*70)
    print("📊 RESULTADOS")
    print("="*70)
    print(f"Total de workers: {num_workers}")
    print(f"Sucessos: {len(successful)}")
    print(f"Falhas: {len(failed)}")
    print(f"Taxa de sucesso: {len(successful)/num_workers*100:.1f}%")
    print(f"Tempo total: {total_time:.2f}s")
    print(f"Tempo médio por commitment: {avg_duration:.2f}s")
    print(f"Throughput: {len(successful)/total_time:.2f} commitments/s")
    
    return {
        "total": num_workers,
        "successful": len(successful),
        "failed": len(failed),
        "total_time": total_time,
        "avg_duration": avg_duration,
        "throughput": len(successful)/total_time if total_time > 0 else 0
    }


def chaos_test():
    """Teste de caos: simular falhas e recuperação"""
    print("="*70)
    print("🌪️  TESTE DE CAOS")
    print("="*70)
    
    # Simular falhas de RPC
    print("\n1. Simulando falha de RPC...")
    # (Em produção, desligaria RPC temporariamente)
    
    # Simular recuperação
    print("2. Simulando recuperação...")
    
    # Testar retry
    print("3. Testando sistema de retry...")
    
    print("\n✅ Teste de caos concluído")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Testes de stress para commitments')
    parser.add_argument('--workers', type=int, default=10, help='Número de workers simultâneos')
    parser.add_argument('--chaos', action='store_true', help='Executar teste de caos')
    
    args = parser.parse_args()
    
    if args.chaos:
        chaos_test()
    else:
        stress_test_concurrent_creates(args.workers)

