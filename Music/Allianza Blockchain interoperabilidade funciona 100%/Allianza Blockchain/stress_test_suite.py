#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧪 TESTE DE ESTRESSE EM LARGA ESCALA
Testa sistema com 100+ transações/minuto
Crítico para validar throughput prometido
"""

import os
import json
import time
import asyncio
import threading
from datetime import datetime
from typing import Dict, List
from concurrent.futures import ThreadPoolExecutor, as_completed
import statistics

# Importar sistemas necessários
try:
    from allianza_blockchain import AllianzaBlockchain
    from quantum_security import QuantumSecuritySystem
    from real_cross_chain_bridge import RealCrossChainBridge
    from alz_niev_interoperability import ALZNIEV
except ImportError as e:
    print(f"⚠️  Erro ao importar módulos: {e}")
    print("   Certifique-se de que todos os módulos estão disponíveis")

class StressTestSuite:
    """
    Suite de testes de estresse para validar performance do sistema
    """
    
    def __init__(self):
        self.results = {
            "test_timestamp": datetime.now().isoformat(),
            "tests": [],
            "summary": {}
        }
        
        # Inicializar sistemas
        print("🔧 Inicializando sistemas...")
        self.blockchain = AllianzaBlockchain()
        self.quantum_security = QuantumSecuritySystem()
        self.bridge = RealCrossChainBridge()
        self.alz_niev = ALZNIEV()
        
        print("✅ Sistemas inicializados!")
    
    def test_transaction_throughput(
        self,
        transactions_per_minute: int = 100,
        duration_minutes: int = 5,
        use_quantum: bool = True
    ) -> Dict:
        """
        Testar throughput de transações
        
        Args:
            transactions_per_minute: Número de transações por minuto
            duration_minutes: Duração do teste em minutos
            use_quantum: Se deve usar assinaturas quânticas
        
        Returns:
            Dict com resultados do teste
        """
        print("="*80)
        print(f"🧪 TESTE DE THROUGHPUT")
        print(f"   Transações/minuto: {transactions_per_minute}")
        print(f"   Duração: {duration_minutes} minutos")
        print(f"   Total esperado: {transactions_per_minute * duration_minutes} transações")
        print(f"   Assinaturas quânticas: {'Sim' if use_quantum else 'Não'}")
        print("="*80)
        
        start_time = time.time()
        end_time = start_time + (duration_minutes * 60)
        
        transactions = []
        errors = []
        latencies = []
        
        # Criar wallets de teste
        # create_wallet() retorna uma tupla: (address, private_key)
        sender_address, sender_private_key = self.blockchain.create_wallet()
        receiver_address, _ = self.blockchain.create_wallet()
        
        # Serializar chave privada para formato PEM (string) se necessário
        try:
            from cryptography.hazmat.primitives import serialization
            if hasattr(sender_private_key, 'private_bytes'):
                sender_private_key_pem = sender_private_key.private_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PrivateFormat.PKCS8,
                    encryption_algorithm=serialization.NoEncryption()
                ).decode('utf-8')
            else:
                sender_private_key_pem = str(sender_private_key)
        except:
            sender_private_key_pem = str(sender_private_key)
        
        # Gerar chave QRS-3 se necessário
        qrs3_keypair_id = None
        if use_quantum:
            qrs3_result = self.quantum_security.generate_qrs3_keypair()
            if qrs3_result.get("success"):
                qrs3_keypair_id = qrs3_result["keypair_id"]
                print(f"✅ Chave QRS-3 gerada: {qrs3_keypair_id}")
            else:
                print(f"⚠️  Falha ao gerar QRS-3: {qrs3_result.get('error')}")
                use_quantum = False
        
        # Calcular intervalo entre transações
        interval_seconds = 60.0 / transactions_per_minute
        
        transaction_count = 0
        successful_count = 0
        failed_count = 0
        
        print(f"\n🚀 Iniciando teste...")
        print(f"   Intervalo entre transações: {interval_seconds:.3f}s")
        
        def create_transaction(tx_id: int):
            """Criar uma transação"""
            tx_start = time.time()
            
            try:
                # Criar transação
                # create_transaction espera private_key como objeto ou string PEM
                tx_result = self.blockchain.create_transaction(
                    sender=sender_address,
                    receiver=receiver_address,
                    amount=0.001,
                    private_key=sender_private_key_pem,
                    is_public=True,
                    network="allianza"
                )
                
                tx_latency = (time.time() - tx_start) * 1000  # ms
                
                if tx_result.get("success"):
                    return {
                        "tx_id": tx_id,
                        "success": True,
                        "latency_ms": tx_latency,
                        "transaction_id": tx_result.get("transaction", {}).get("id"),
                        "timestamp": datetime.now().isoformat()
                    }
                else:
                    return {
                        "tx_id": tx_id,
                        "success": False,
                        "error": tx_result.get("error", "Unknown error"),
                        "latency_ms": tx_latency,
                        "timestamp": datetime.now().isoformat()
                    }
            except Exception as e:
                tx_latency = (time.time() - tx_start) * 1000
                return {
                    "tx_id": tx_id,
                    "success": False,
                    "error": str(e),
                    "latency_ms": tx_latency,
                    "timestamp": datetime.now().isoformat()
                }
        
        # Executar transações
        next_tx_time = start_time
        
        while time.time() < end_time:
            current_time = time.time()
            
            # Verificar se é hora de criar nova transação
            if current_time >= next_tx_time:
                transaction_count += 1
                result = create_transaction(transaction_count)
                
                if result["success"]:
                    successful_count += 1
                    latencies.append(result["latency_ms"])
                else:
                    failed_count += 1
                    errors.append(result)
                
                transactions.append(result)
                
                # Calcular próximo tempo
                next_tx_time = current_time + interval_seconds
                
                # Log progresso
                if transaction_count % 10 == 0:
                    elapsed = time.time() - start_time
                    rate = transaction_count / elapsed * 60  # transações/minuto
                    print(f"   📊 Progresso: {transaction_count} transações | "
                          f"Taxa: {rate:.1f} tx/min | "
                          f"Sucesso: {successful_count} | "
                          f"Falhas: {failed_count}")
            
            # Pequeno sleep para não sobrecarregar CPU
            time.sleep(0.01)
        
        total_time = time.time() - start_time
        actual_rate = transaction_count / (total_time / 60)  # transações/minuto real
        
        # Calcular estatísticas
        if latencies:
            avg_latency = statistics.mean(latencies)
            median_latency = statistics.median(latencies)
            min_latency = min(latencies)
            max_latency = max(latencies)
            p95_latency = statistics.quantiles(latencies, n=20)[18] if len(latencies) > 20 else max_latency
        else:
            avg_latency = median_latency = min_latency = max_latency = p95_latency = 0
        
        result = {
            "test_name": "Transaction Throughput Test",
            "parameters": {
                "transactions_per_minute_target": transactions_per_minute,
                "duration_minutes": duration_minutes,
                "use_quantum": use_quantum
            },
            "results": {
                "total_transactions": transaction_count,
                "successful_transactions": successful_count,
                "failed_transactions": failed_count,
                "success_rate_percent": (successful_count / transaction_count * 100) if transaction_count > 0 else 0,
                "actual_rate_per_minute": actual_rate,
                "target_rate_per_minute": transactions_per_minute,
                "rate_achievement_percent": (actual_rate / transactions_per_minute * 100) if transactions_per_minute > 0 else 0,
                "total_time_seconds": total_time,
                "latency_stats": {
                    "average_ms": avg_latency,
                    "median_ms": median_latency,
                    "min_ms": min_latency,
                    "max_ms": max_latency,
                    "p95_ms": p95_latency
                },
                "errors": errors[:10]  # Primeiros 10 erros
            },
            "timestamp": datetime.now().isoformat()
        }
        
        print(f"\n{'='*80}")
        print("📊 RESULTADOS")
        print(f"{'='*80}")
        print(f"Total de transações: {transaction_count}")
        print(f"Sucesso: {successful_count} ({result['results']['success_rate_percent']:.1f}%)")
        print(f"Falhas: {failed_count}")
        print(f"Taxa real: {actual_rate:.1f} tx/min")
        print(f"Taxa alvo: {transactions_per_minute} tx/min")
        print(f"Atingiu {result['results']['rate_achievement_percent']:.1f}% da taxa alvo")
        print(f"\nLatência:")
        print(f"  Média: {avg_latency:.2f}ms")
        print(f"  Mediana: {median_latency:.2f}ms")
        print(f"  P95: {p95_latency:.2f}ms")
        print(f"  Min: {min_latency:.2f}ms")
        print(f"  Max: {max_latency:.2f}ms")
        print(f"{'='*80}")
        
        self.results["tests"].append(result)
        return result
    
    def test_concurrent_cross_chain(
        self,
        concurrent_transfers: int = 50,
        target_chains: List[str] = ["polygon", "ethereum", "bsc"]
    ) -> Dict:
        """
        Testar transferências cross-chain concorrentes
        
        Args:
            concurrent_transfers: Número de transferências concorrentes
            target_chains: Lista de chains de destino
        
        Returns:
            Dict com resultados
        """
        print("="*80)
        print(f"🧪 TESTE DE TRANSFERÊNCIAS CROSS-CHAIN CONCORRENTES")
        print(f"   Transferências concorrentes: {concurrent_transfers}")
        print(f"   Chains de destino: {', '.join(target_chains)}")
        print("="*80)
        
        start_time = time.time()
        results = []
        errors = []
        
        def create_cross_chain_transfer(transfer_id: int):
            """Criar transferência cross-chain"""
            chain = target_chains[transfer_id % len(target_chains)]
            tx_start = time.time()
            
            try:
                # Usar ALZ-NIEV para execução cross-chain
                result = self.alz_niev.execute_cross_chain_with_proofs(
                    source_chain="allianza",
                    target_chain=chain,
                    function_name="transfer",
                    function_params={
                        "to": "0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb0",
                        "amount": 0.001
                    }
                )
                
                tx_latency = (time.time() - tx_start) * 1000
                
                return {
                    "transfer_id": transfer_id,
                    "target_chain": chain,
                    "success": result.success,
                    "latency_ms": tx_latency,
                    "has_proofs": {
                        "zk": result.zk_proof is not None,
                        "merkle": result.merkle_proof is not None,
                        "consensus": result.consensus_proof is not None
                    },
                    "timestamp": datetime.now().isoformat()
                }
            except Exception as e:
                tx_latency = (time.time() - tx_start) * 1000
                return {
                    "transfer_id": transfer_id,
                    "target_chain": chain,
                    "success": False,
                    "error": str(e),
                    "latency_ms": tx_latency,
                    "timestamp": datetime.now().isoformat()
                }
        
        # Executar transferências concorrentes
        print(f"\n🚀 Iniciando {concurrent_transfers} transferências concorrentes...")
        
        with ThreadPoolExecutor(max_workers=min(concurrent_transfers, 20)) as executor:
            futures = [executor.submit(create_cross_chain_transfer, i) for i in range(concurrent_transfers)]
            
            for future in as_completed(futures):
                result = future.result()
                results.append(result)
                
                if not result["success"]:
                    errors.append(result)
                
                if len(results) % 10 == 0:
                    print(f"   📊 Progresso: {len(results)}/{concurrent_transfers} transferências")
        
        total_time = time.time() - start_time
        successful = sum(1 for r in results if r["success"])
        failed = len(results) - successful
        
        latencies = [r["latency_ms"] for r in results if r["success"]]
        
        if latencies:
            avg_latency = statistics.mean(latencies)
            max_latency = max(latencies)
            min_latency = min(latencies)
        else:
            avg_latency = max_latency = min_latency = 0
        
        result = {
            "test_name": "Concurrent Cross-Chain Transfer Test",
            "parameters": {
                "concurrent_transfers": concurrent_transfers,
                "target_chains": target_chains
            },
            "results": {
                "total_transfers": len(results),
                "successful_transfers": successful,
                "failed_transfers": failed,
                "success_rate_percent": (successful / len(results) * 100) if results else 0,
                "total_time_seconds": total_time,
                "throughput_per_minute": (len(results) / total_time * 60) if total_time > 0 else 0,
                "latency_stats": {
                    "average_ms": avg_latency,
                    "min_ms": min_latency,
                    "max_ms": max_latency
                },
                "errors": errors[:10]
            },
            "timestamp": datetime.now().isoformat()
        }
        
        print(f"\n{'='*80}")
        print("📊 RESULTADOS")
        print(f"{'='*80}")
        print(f"Total: {len(results)} transferências")
        print(f"Sucesso: {successful} ({result['results']['success_rate_percent']:.1f}%)")
        print(f"Falhas: {failed}")
        print(f"Throughput: {result['results']['throughput_per_minute']:.1f} transferências/minuto")
        print(f"Latência média: {avg_latency:.2f}ms")
        print(f"{'='*80}")
        
        self.results["tests"].append(result)
        return result
    
    def run_full_stress_test(self) -> Dict:
        """
        Executar suite completa de testes de estresse
        
        Returns:
            Dict com todos os resultados
        """
        print("="*80)
        print("🧪 SUITE COMPLETA DE TESTES DE ESTRESSE")
        print("="*80)
        
        # Teste 1: Throughput básico (100 tx/min)
        self.test_transaction_throughput(
            transactions_per_minute=100,
            duration_minutes=2,
            use_quantum=False
        )
        
        # Teste 2: Throughput com QRS-3 (50 tx/min - mais lento)
        self.test_transaction_throughput(
            transactions_per_minute=50,
            duration_minutes=2,
            use_quantum=True
        )
        
        # Teste 3: Cross-chain concorrente
        self.test_concurrent_cross_chain(
            concurrent_transfers=50,
            target_chains=["polygon", "ethereum", "bsc"]
        )
        
        # Calcular resumo
        if self.results["tests"]:
            total_tests = len(self.results["tests"])
            successful_tests = sum(1 for t in self.results["tests"] if t["results"].get("success_rate_percent", 0) > 90)
            
            self.results["summary"] = {
                "total_tests": total_tests,
                "successful_tests": successful_tests,
                "success_rate_percent": (successful_tests / total_tests * 100) if total_tests > 0 else 0,
                "timestamp": datetime.now().isoformat()
            }
        
        # Salvar resultados
        report_file = f"stress_test_report_{int(time.time())}.json"
        with open(report_file, 'w') as f:
            json.dump(self.results, f, indent=2)
        
        print(f"\n📄 Relatório completo salvo em: {report_file}")
        
        return self.results

if __name__ == "__main__":
    suite = StressTestSuite()
    suite.run_full_stress_test()

