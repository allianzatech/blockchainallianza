#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔍 ANÁLISE DE PERFORMANCE FASE 2
Identifica gargalos e problemas de performance
"""

import time
import cProfile
import pstats
from io import StringIO
from bridge_improvements import AsyncBridgeProcessor, BatchTransactionProcessor

def analisar_async_processor():
    """Analisar performance do AsyncBridgeProcessor"""
    print("="*70)
    print("🔍 ANÁLISE: AsyncBridgeProcessor")
    print("="*70)
    
    # Criar instância mock
    class MockBridge:
        def real_cross_chain_transfer(self, **kwargs):
            # Simular processamento rápido (sem I/O real)
            time.sleep(0.1)  # 100ms de processamento
            return {"success": True, "tx_hash": "0xtest"}
    
    bridge = MockBridge()
    processor = AsyncBridgeProcessor(bridge, max_workers=5)
    
    # Teste de throughput
    print("\n📊 Teste de Throughput:")
    print("   Enviando 10 tarefas assíncronas...")
    
    start = time.time()
    task_ids = []
    
    for i in range(10):
        task_id = processor.process_transfer_async(
            source_chain="polygon",
            target_chain="bitcoin",
            amount=0.0001,
            token_symbol="MATIC",
            recipient="tb1qtest",
            priority=5
        )
        task_ids.append(task_id)
    
    creation_time = time.time() - start
    print(f"   ✅ Criação: {creation_time:.3f}s ({creation_time/10*1000:.1f}ms por tarefa)")
    
    # Aguardar conclusão
    print("\n   Aguardando conclusão...")
    completed = 0
    start_wait = time.time()
    
    while completed < 10 and (time.time() - start_wait) < 30:
        for tid in task_ids:
            status = processor.get_task_status(tid)
            if status.get("status") in ["completed", "failed"]:
                completed += 1
                task_ids.remove(tid)
                break
        time.sleep(0.1)
    
    total_time = time.time() - start
    print(f"   ✅ Total: {total_time:.3f}s")
    print(f"   ✅ Throughput: {10/total_time:.2f} tarefas/segundo")
    print(f"   ✅ Concluídas: {completed}/10")
    
    # Comparar com síncrono
    print("\n📊 Comparação com Síncrono:")
    start_sync = time.time()
    for i in range(10):
        bridge.real_cross_chain_transfer(
            source_chain="polygon",
            target_chain="bitcoin",
            amount=0.0001,
            token_symbol="MATIC",
            recipient="tb1qtest"
        )
    time_sync = time.time() - start_sync
    print(f"   ⏱️  Síncrono: {time_sync:.3f}s")
    print(f"   ⚡ Assíncrono: {total_time:.3f}s")
    print(f"   🚀 Speedup: {time_sync/total_time:.2f}x")
    
    return {
        "async_time": total_time,
        "sync_time": time_sync,
        "speedup": time_sync / total_time if total_time > 0 else 0,
        "throughput": 10 / total_time if total_time > 0 else 0
    }

def analisar_batch_processor():
    """Analisar performance do BatchTransactionProcessor"""
    print("\n" + "="*70)
    print("🔍 ANÁLISE: BatchTransactionProcessor")
    print("="*70)
    
    # Criar instância mock
    class MockBridge:
        def send_evm_transaction(self, **kwargs):
            # Simular processamento rápido
            time.sleep(0.05)  # 50ms por transação
            return {"success": True, "tx_hash": "0xtest"}
    
    bridge = MockBridge()
    processor = BatchTransactionProcessor(bridge)
    
    # Teste individual
    print("\n📊 Teste Individual (Baseline):")
    start_individual = time.time()
    for i in range(10):
        bridge.send_evm_transaction(
            chain="polygon",
            from_private_key="0xtest",
            to_address="0xtest",
            amount=0.001,
            token_symbol="MATIC"
        )
    time_individual = time.time() - start_individual
    print(f"   ⏱️  Tempo: {time_individual:.3f}s")
    print(f"   📈 Throughput: {10/time_individual:.2f} transações/segundo")
    
    # Teste batch
    print("\n📊 Teste Batch:")
    start_batch = time.time()
    for i in range(10):
        processor.add_to_batch(
            chain="polygon",
            from_private_key="0xtest",
            to_address="0xtest",
            amount=0.001,
            token_symbol="MATIC"
        )
    
    # Processar batch
    result = processor.process_batch("polygon")
    time_batch = time.time() - start_batch
    print(f"   ⏱️  Tempo: {time_batch:.3f}s")
    print(f"   📈 Throughput: {10/time_batch:.2f} transações/segundo")
    print(f"   ✅ Processadas: {result.get('processed', 0)}")
    
    # Comparação
    print("\n📊 Comparação:")
    print(f"   ⏱️  Individual: {time_individual:.3f}s")
    print(f"   📦 Batch: {time_batch:.3f}s")
    print(f"   🚀 Speedup: {time_individual/time_batch:.2f}x")
    
    return {
        "individual_time": time_individual,
        "batch_time": time_batch,
        "speedup": time_individual / time_batch if time_batch > 0 else 0
    }

def identificar_gargalos():
    """Identificar gargalos no código"""
    print("\n" + "="*70)
    print("🔍 IDENTIFICAÇÃO DE GARGALOS")
    print("="*70)
    
    gargalos = []
    
    # Ler código
    with open("bridge_improvements.py", "r", encoding="utf-8") as f:
        code = f.read()
    
    # Verificar problemas comuns
    if "time.sleep" in code:
        gargalos.append("⚠️  time.sleep() encontrado - pode causar bloqueio")
    
    if "ThreadPoolExecutor" in code:
        print("✅ ThreadPoolExecutor usado corretamente")
    else:
        gargalos.append("❌ ThreadPoolExecutor não encontrado")
    
    # Verificar se há locks excessivos
    lock_count = code.count("self.lock")
    if lock_count > 10:
        gargalos.append(f"⚠️  Muitos locks ({lock_count}) - pode causar contenção")
    
    # Verificar processamento sequencial em batch
    if "for tx in transactions:" in code:
        print("⚠️  Processamento sequencial em batch - pode ser paralelizado")
        gargalos.append("Processamento sequencial em batch pode ser otimizado")
    
    print("\n📋 Gargalos Identificados:")
    for g in gargalos:
        print(f"   {g}")
    
    return gargalos

if __name__ == '__main__':
    print("="*70)
    print("🔍 ANÁLISE COMPLETA DE PERFORMANCE FASE 2")
    print("="*70)
    
    # Análise assíncrona
    async_results = analisar_async_processor()
    
    # Análise batch
    batch_results = analisar_batch_processor()
    
    # Identificar gargalos
    gargalos = identificar_gargalos()
    
    # Resumo
    print("\n" + "="*70)
    print("📊 RESUMO DA ANÁLISE")
    print("="*70)
    print(f"\n⚡ Processamento Assíncrono:")
    print(f"   Speedup: {async_results['speedup']:.2f}x")
    print(f"   Throughput: {async_results['throughput']:.2f} tarefas/segundo")
    
    print(f"\n📦 Batch Processing:")
    print(f"   Speedup: {batch_results['speedup']:.2f}x")
    
    print(f"\n🔍 Gargalos: {len(gargalos)}")
    for g in gargalos:
        print(f"   • {g}")







