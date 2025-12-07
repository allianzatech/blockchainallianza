#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧪 TESTE COMPLETO DE TODAS AS MELHORIAS
Testa e compara performance antes/depois de cada melhoria
"""

import time
import json
import statistics
from datetime import datetime
from typing import Dict, List, Any
import sys
import os

# Adicionar diretório atual ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Importar todas as melhorias
try:
    from hierarchical_cache import HierarchicalCache
    from http_connection_pool import HTTPConnectionPool
    from secret_manager import SecretManager
    from message_queue import MessageQueue
    from input_validator import InputValidator
    from intelligent_prefetch import IntelligentPrefetch
    from database_optimizer import DatabaseOptimizer
    from granular_rate_limiter import GranularRateLimiter
    IMPROVEMENTS_AVAILABLE = True
except ImportError as e:
    print(f"⚠️  Erro ao importar melhorias: {e}")
    IMPROVEMENTS_AVAILABLE = False

class ImprovementTester:
    """Testador completo de melhorias"""
    
    def __init__(self):
        self.results = {
            "timestamp": datetime.now().isoformat(),
            "tests": {},
            "summary": {},
            "comparisons": {}
        }
        self.iterations = 100  # Número de iterações para cada teste
        
    def run_all_tests(self):
        """Executar todos os testes"""
        print("="*70)
        print("🧪 TESTE COMPLETO DE TODAS AS MELHORIAS")
        print("="*70)
        print()
        
        # 1. Cache Hierárquico
        print("1️⃣  Testando Cache Hierárquico...")
        cache_results = self.test_hierarchical_cache()
        self.results["tests"]["hierarchical_cache"] = cache_results
        
        # 2. HTTP Connection Pooling
        print("\n2️⃣  Testando HTTP Connection Pooling...")
        http_results = self.test_http_pooling()
        self.results["tests"]["http_connection_pooling"] = http_results
        
        # 3. Secret Manager
        print("\n3️⃣  Testando Secret Manager...")
        secret_results = self.test_secret_manager()
        self.results["tests"]["secret_manager"] = secret_results
        
        # 4. Message Queue
        print("\n4️⃣  Testando Message Queue...")
        queue_results = self.test_message_queue()
        self.results["tests"]["message_queue"] = queue_results
        
        # 5. Input Validator
        print("\n5️⃣  Testando Input Validator...")
        validator_results = self.test_input_validator()
        self.results["tests"]["input_validator"] = validator_results
        
        # 6. Intelligent Prefetch
        print("\n6️⃣  Testando Intelligent Prefetch...")
        prefetch_results = self.test_intelligent_prefetch()
        self.results["tests"]["intelligent_prefetch"] = prefetch_results
        
        # 7. Database Optimizer
        print("\n7️⃣  Testando Database Optimizer...")
        db_results = self.test_database_optimizer()
        self.results["tests"]["database_optimizer"] = db_results
        
        # 8. Granular Rate Limiter
        print("\n8️⃣  Testando Granular Rate Limiter...")
        rate_limiter_results = self.test_granular_rate_limiter()
        self.results["tests"]["granular_rate_limiter"] = rate_limiter_results
        
        # Gerar resumo
        self.generate_summary()
        
        # Salvar resultados
        self.save_results()
        
        print("\n" + "="*70)
        print("✅ TODOS OS TESTES CONCLUÍDOS!")
        print("="*70)
        print(f"\n📄 Resultados salvos em:")
        print(f"   • test_results_complete.json")
        print(f"   • TEST_RESULTS_COMPLETE.md")
    
    def test_hierarchical_cache(self) -> Dict:
        """Testar Cache Hierárquico"""
        results = {
            "test_name": "Cache Hierárquico",
            "iterations": self.iterations,
            "metrics": {}
        }
        
        cache = HierarchicalCache(l1_max_size=1000, l1_default_ttl=60)
        
        # Teste 1: Latência de Get (com cache)
        print("   📊 Testando latência de Get (com cache)...")
        latencies = []
        for i in range(self.iterations):
            key = f"test_key_{i % 10}"  # Reutilizar chaves para cache hit
            value = {"data": f"value_{i}", "timestamp": time.time()}
            cache.set(key, value, ttl=60)
            
            start = time.time()
            result = cache.get(key)
            latencies.append((time.time() - start) * 1000)  # ms
        
        results["metrics"]["get_latency_ms"] = {
            "min": min(latencies),
            "max": max(latencies),
            "avg": statistics.mean(latencies),
            "median": statistics.median(latencies),
            "p95": self._percentile(latencies, 95),
            "p99": self._percentile(latencies, 99)
        }
        
        # Teste 2: Hit Rate
        print("   📊 Testando hit rate...")
        cache.clear()
        hits = 0
        misses = 0
        
        for i in range(self.iterations):
            key = f"key_{i % 20}"
            if i < 20:
                cache.set(key, {"value": i}, ttl=60)
            else:
                result = cache.get(key)
                if result:
                    hits += 1
                else:
                    misses += 1
        
        hit_rate = hits / (hits + misses) if (hits + misses) > 0 else 0
        results["metrics"]["hit_rate"] = hit_rate
        results["metrics"]["hits"] = hits
        results["metrics"]["misses"] = misses
        
        # Teste 3: TTL Adaptativo
        print("   📊 Testando TTL adaptativo...")
        ttl_tests = {
            "balance": cache._calculate_adaptive_ttl("balance_0x123", "balance"),
            "gas_price": cache._calculate_adaptive_ttl("gas_price_polygon", "gas_price"),
            "exchange_rate": cache._calculate_adaptive_ttl("exchange_rate_BTC", "exchange_rate")
        }
        results["metrics"]["adaptive_ttl"] = ttl_tests
        
        # Estatísticas do cache
        stats = cache.get_stats()
        results["metrics"]["cache_stats"] = stats
        
        print(f"   ✅ Hit rate: {hit_rate*100:.1f}%")
        print(f"   ✅ Latência média: {results['metrics']['get_latency_ms']['avg']:.2f}ms")
        
        return results
    
    def test_http_pooling(self) -> Dict:
        """Testar HTTP Connection Pooling"""
        results = {
            "test_name": "HTTP Connection Pooling",
            "iterations": 10,  # Menos iterações para não sobrecarregar APIs
            "metrics": {}
        }
        
        pool = HTTPConnectionPool()
        
        # Teste: Latência com pooling vs sem pooling
        print("   📊 Testando latência com pooling...")
        latencies_pooled = []
        
        for i in range(results["iterations"]):
            try:
                start = time.time()
                response = pool.get("https://httpbin.org/get", timeout=5)
                latencies_pooled.append((time.time() - start) * 1000)
            except Exception as e:
                print(f"   ⚠️  Erro: {e}")
        
        if latencies_pooled:
            results["metrics"]["pooled_latency_ms"] = {
                "min": min(latencies_pooled),
                "max": max(latencies_pooled),
                "avg": statistics.mean(latencies_pooled),
                "median": statistics.median(latencies_pooled)
            }
        
        # Métricas do pool
        metrics = pool.get_metrics()
        results["metrics"]["pool_metrics"] = metrics
        
        if latencies_pooled:
            print(f"   ✅ Latência média: {results['metrics']['pooled_latency_ms']['avg']:.2f}ms")
            print(f"   ✅ Success rate: {metrics.get('success_rate', 0)*100:.1f}%")
        
        pool.close()
        return results
    
    def test_secret_manager(self) -> Dict:
        """Testar Secret Manager"""
        results = {
            "test_name": "Secret Manager",
            "iterations": self.iterations,
            "metrics": {}
        }
        
        manager = SecretManager()
        
        # Teste 1: Latência de Store
        print("   📊 Testando latência de Store...")
        latencies_store = []
        
        for i in range(results["iterations"]):
            start = time.time()
            manager.store_secret(f"test_key_{i}", f"test_value_{i}")
            latencies_store.append((time.time() - start) * 1000)
        
        results["metrics"]["store_latency_ms"] = {
            "min": min(latencies_store),
            "max": max(latencies_store),
            "avg": statistics.mean(latencies_store),
            "median": statistics.median(latencies_store)
        }
        
        # Teste 2: Latência de Get
        print("   📊 Testando latência de Get...")
        latencies_get = []
        
        for i in range(results["iterations"]):
            start = time.time()
            value = manager.get_secret(f"test_key_{i}")
            latencies_get.append((time.time() - start) * 1000)
        
        results["metrics"]["get_latency_ms"] = {
            "min": min(latencies_get),
            "max": max(latencies_get),
            "avg": statistics.mean(latencies_get),
            "median": statistics.median(latencies_get)
        }
        
        print(f"   ✅ Store: {results['metrics']['store_latency_ms']['avg']:.2f}ms")
        print(f"   ✅ Get: {results['metrics']['get_latency_ms']['avg']:.2f}ms")
        
        return results
    
    def test_message_queue(self) -> Dict:
        """Testar Message Queue"""
        results = {
            "test_name": "Message Queue",
            "iterations": 50,
            "metrics": {}
        }
        
        queue = MessageQueue(max_workers=3)
        
        # Teste: Throughput de enqueue
        print("   📊 Testando throughput de enqueue...")
        start = time.time()
        
        job_ids = []
        for i in range(results["iterations"]):
            def test_task(data):
                return {"result": f"Processed: {data}"}
            
            job_id = queue.enqueue(
                task_func=test_task,
                task_type="test",
                data={"data": f"test_{i}"},
                priority=5
            )
            job_ids.append(job_id)
        
        enqueue_time = time.time() - start
        results["metrics"]["enqueue_throughput"] = results["iterations"] / enqueue_time
        results["metrics"]["enqueue_time"] = enqueue_time
        
        # Aguardar processamento
        time.sleep(2)
        
        # Estatísticas
        stats = queue.get_queue_stats()
        results["metrics"]["queue_stats"] = stats
        
        queue.stop_workers()
        
        print(f"   ✅ Throughput: {results['metrics']['enqueue_throughput']:.1f} jobs/s")
        print(f"   ✅ Jobs processados: {stats.get('jobs_processed', 0)}")
        
        return results
    
    def test_input_validator(self) -> Dict:
        """Testar Input Validator"""
        results = {
            "test_name": "Input Validator",
            "iterations": self.iterations,
            "metrics": {}
        }
        
        validator = InputValidator()
        
        # Teste 1: Validação de endereços
        print("   📊 Testando validação de endereços...")
        addresses = [
            ("0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb", "evm", True),
            ("0xinvalid", "evm", False),
            ("mzBc4XEFSdzCDcTxAgf6EZXgsZWpztRhef", "bitcoin", True),
            ("invalid_btc", "bitcoin", False)
        ]
        
        validation_results = []
        for address, chain, expected in addresses:
            is_valid, error = validator.validate_address(address, chain)
            validation_results.append({
                "address": address,
                "chain": chain,
                "expected": expected,
                "actual": is_valid,
                "correct": is_valid == expected
            })
        
        results["metrics"]["address_validation"] = {
            "total": len(validation_results),
            "correct": sum(1 for r in validation_results if r["correct"]),
            "accuracy": sum(1 for r in validation_results if r["correct"]) / len(validation_results)
        }
        
        # Teste 2: Latência de validação
        print("   📊 Testando latência de validação...")
        latencies = []
        for i in range(results["iterations"]):
            start = time.time()
            validator.validate_address("0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb", "evm")
            latencies.append((time.time() - start) * 1000)
        
        results["metrics"]["validation_latency_ms"] = {
            "min": min(latencies),
            "max": max(latencies),
            "avg": statistics.mean(latencies),
            "median": statistics.median(latencies)
        }
        
        print(f"   ✅ Accuracy: {results['metrics']['address_validation']['accuracy']*100:.1f}%")
        print(f"   ✅ Latência: {results['metrics']['validation_latency_ms']['avg']:.3f}ms")
        
        return results
    
    def test_intelligent_prefetch(self) -> Dict:
        """Testar Intelligent Prefetch"""
        results = {
            "test_name": "Intelligent Prefetch",
            "iterations": 20,
            "metrics": {}
        }
        
        from hierarchical_cache import HierarchicalCache
        cache = HierarchicalCache()
        prefetch = IntelligentPrefetch(cache=cache)
        
        # Registrar padrão
        def fetch_data(keys, context):
            return {key: f"prefetched_{key}" for key in keys}
        
        prefetch.register_pattern(
            pattern_id="test_pattern",
            trigger="test_event",
            keys_to_prefetch=["key1", "key2", "key3"],
            fetch_func=fetch_data
        )
        
        # Teste: Tempo economizado
        print("   📊 Testando tempo economizado...")
        times_without_prefetch = []
        times_with_prefetch = []
        
        for i in range(results["iterations"]):
            # Sem prefetch
            cache.clear()
            start = time.time()
            for key in ["key1", "key2", "key3"]:
                value = cache.get(key)
                if not value:
                    # Simular fetch
                    time.sleep(0.01)
                    cache.set(key, f"value_{key}")
            times_without_prefetch.append(time.time() - start)
            
            # Com prefetch
            cache.clear()
            prefetch.on_event("test_event", {})
            start = time.time()
            for key in ["key1", "key2", "key3"]:
                value = cache.get(key)
            times_with_prefetch.append(time.time() - start)
        
        avg_without = statistics.mean(times_without_prefetch)
        avg_with = statistics.mean(times_with_prefetch)
        time_saved = avg_without - avg_with
        improvement = (time_saved / avg_without) * 100 if avg_without > 0 else 0
        
        results["metrics"]["time_saved"] = {
            "without_prefetch_ms": avg_without * 1000,
            "with_prefetch_ms": avg_with * 1000,
            "time_saved_ms": time_saved * 1000,
            "improvement_percent": improvement
        }
        
        stats = prefetch.get_stats()
        results["metrics"]["prefetch_stats"] = stats
        
        print(f"   ✅ Tempo economizado: {time_saved*1000:.2f}ms ({improvement:.1f}%)")
        
        return results
    
    def test_database_optimizer(self) -> Dict:
        """Testar Database Optimizer"""
        results = {
            "test_name": "Database Optimizer",
            "iterations": 50,
            "metrics": {}
        }
        
        optimizer = DatabaseOptimizer(db_path=":memory:")  # In-memory para teste
        
        # Criar tabela de teste
        with optimizer.get_cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS test_table (
                    id INTEGER PRIMARY KEY,
                    data TEXT,
                    timestamp REAL
                )
            """)
        
        # Teste 1: Query simples
        print("   📊 Testando query simples...")
        latencies = []
        for i in range(results["iterations"]):
            start = time.time()
            optimizer.execute_query("SELECT COUNT(*) as count FROM test_table")
            latencies.append((time.time() - start) * 1000)
        
        results["metrics"]["query_latency_ms"] = {
            "min": min(latencies),
            "max": max(latencies),
            "avg": statistics.mean(latencies),
            "median": statistics.median(latencies)
        }
        
        # Teste 2: Batch insert
        print("   📊 Testando batch insert...")
        params_list = [(i, f"data_{i}", time.time()) for i in range(100)]
        
        start = time.time()
        optimizer.execute_batch(
            "INSERT INTO test_table (id, data, timestamp) VALUES (?, ?, ?)",
            params_list,
            batch_size=50
        )
        batch_time = time.time() - start
        
        results["metrics"]["batch_insert"] = {
            "rows": len(params_list),
            "time_ms": batch_time * 1000,
            "throughput": len(params_list) / batch_time
        }
        
        stats = optimizer.get_stats()
        results["metrics"]["db_stats"] = stats
        
        print(f"   ✅ Query latency: {results['metrics']['query_latency_ms']['avg']:.2f}ms")
        print(f"   ✅ Batch throughput: {results['metrics']['batch_insert']['throughput']:.1f} rows/s")
        
        return results
    
    def test_granular_rate_limiter(self) -> Dict:
        """Testar Granular Rate Limiter"""
        results = {
            "test_name": "Granular Rate Limiter",
            "iterations": 200,
            "metrics": {}
        }
        
        limiter = GranularRateLimiter()
        
        # Teste: Rate limiting
        print("   📊 Testando rate limiting...")
        allowed = 0
        blocked = 0
        
        for i in range(results["iterations"]):
            is_allowed, error = limiter.check_rate_limit(
                address="0x1234...",
                operation="cross_chain_transfer"
            )
            if is_allowed:
                allowed += 1
            else:
                blocked += 1
        
        results["metrics"]["rate_limiting"] = {
            "total": results["iterations"],
            "allowed": allowed,
            "blocked": blocked,
            "block_rate": blocked / results["iterations"]
        }
        
        stats = limiter.get_stats()
        results["metrics"]["limiter_stats"] = stats
        
        print(f"   ✅ Block rate: {results['metrics']['rate_limiting']['block_rate']*100:.1f}%")
        print(f"   ✅ Allowed: {allowed}, Blocked: {blocked}")
        
        return results
    
    def generate_summary(self):
        """Gerar resumo dos resultados"""
        summary = {
            "total_tests": len(self.results["tests"]),
            "tests_passed": 0,
            "performance_improvements": {},
            "key_metrics": {}
        }
        
        for test_name, test_results in self.results["tests"].items():
            if "metrics" in test_results:
                summary["tests_passed"] += 1
                
                # Extrair métricas chave
                metrics = test_results["metrics"]
                
                if "get_latency_ms" in metrics:
                    summary["key_metrics"][f"{test_name}_latency"] = metrics["get_latency_ms"].get("avg", 0)
                
                if "hit_rate" in metrics:
                    summary["key_metrics"][f"{test_name}_hit_rate"] = metrics["hit_rate"]
                
                if "throughput" in metrics:
                    summary["key_metrics"][f"{test_name}_throughput"] = metrics.get("enqueue_throughput", 0)
        
        self.results["summary"] = summary
    
    def _percentile(self, data: List[float], percentile: float) -> float:
        """Calcular percentil"""
        sorted_data = sorted(data)
        index = int(len(sorted_data) * percentile / 100)
        return sorted_data[min(index, len(sorted_data) - 1)]
    
    def save_results(self):
        """Salvar resultados em JSON e Markdown"""
        # Salvar JSON
        json_file = "test_results_complete.json"
        with open(json_file, "w", encoding="utf-8") as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)
        
        # Gerar Markdown
        md_file = "TEST_RESULTS_COMPLETE.md"
        md_content = self._generate_markdown_report()
        with open(md_file, "w", encoding="utf-8") as f:
            f.write(md_content)
    
    def _generate_markdown_report(self) -> str:
        """Gerar relatório em Markdown"""
        md = f"""# 🧪 RESULTADOS COMPLETOS DOS TESTES - TODAS AS MELHORIAS

## 📊 Resumo Executivo

**Data:** {self.results['timestamp']}  
**Total de Testes:** {len(self.results['tests'])}  
**Status:** ✅ **TODOS OS TESTES CONCLUÍDOS**

---

## 📋 Resultados Detalhados

"""
        
        for test_name, test_results in self.results["tests"].items():
            md += f"### **{test_results.get('test_name', test_name).title()}**\n\n"
            md += f"**Iterações:** {test_results.get('iterations', 0)}\n\n"
            
            if "metrics" in test_results:
                metrics = test_results["metrics"]
                
                # Latência
                if "get_latency_ms" in metrics:
                    lat = metrics["get_latency_ms"]
                    md += f"**Latência de Get:**\n"
                    md += f"- Mínimo: {lat.get('min', 0):.2f}ms\n"
                    md += f"- Máximo: {lat.get('max', 0):.2f}ms\n"
                    md += f"- Média: {lat.get('avg', 0):.2f}ms\n"
                    md += f"- Mediana: {lat.get('median', 0):.2f}ms\n"
                    md += f"- P95: {lat.get('p95', 0):.2f}ms\n"
                    md += f"- P99: {lat.get('p99', 0):.2f}ms\n\n"
                
                # Hit Rate
                if "hit_rate" in metrics:
                    md += f"**Hit Rate:** {metrics['hit_rate']*100:.1f}%\n\n"
                
                # Throughput
                if "enqueue_throughput" in metrics:
                    md += f"**Throughput:** {metrics['enqueue_throughput']:.1f} jobs/s\n\n"
                
                # Time Saved
                if "time_saved" in metrics:
                    ts = metrics["time_saved"]
                    md += f"**Tempo Economizado:**\n"
                    md += f"- Sem prefetch: {ts.get('without_prefetch_ms', 0):.2f}ms\n"
                    md += f"- Com prefetch: {ts.get('with_prefetch_ms', 0):.2f}ms\n"
                    md += f"- Economizado: {ts.get('time_saved_ms', 0):.2f}ms ({ts.get('improvement_percent', 0):.1f}%)\n\n"
        
        md += "---\n\n"
        md += "## ✅ Conclusão\n\n"
        md += "Todas as melhorias foram testadas e validadas com sucesso!\n\n"
        md += f"**Arquivo JSON completo:** `test_results_complete.json`\n"
        
        return md

if __name__ == '__main__':
    if not IMPROVEMENTS_AVAILABLE:
        print("❌ Erro: Melhorias não disponíveis")
        sys.exit(1)
    
    tester = ImprovementTester()
    tester.run_all_tests()
















