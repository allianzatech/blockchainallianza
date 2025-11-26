#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
⚡ OTIMIZAÇÕES DE PERFORMANCE
Implementa todas as otimizações de alta e média prioridade
"""

import time
import json
import hashlib
from typing import Dict, List, Optional, Tuple
from concurrent.futures import ThreadPoolExecutor, as_completed
from collections import defaultdict, deque
from dataclasses import dataclass
from datetime import datetime, timedelta

# =============================================================================
# 1. ASSINATURA INTELIGENTE INTEGRADA
# =============================================================================

class IntelligentSigningIntegration:
    """Integra assinatura inteligente no bridge"""
    
    def __init__(self, quantum_security=None):
        self.quantum_security = quantum_security
        self.hybrid_signing = None
        
        # Tentar importar hybrid_intelligent_signing
        try:
            from hybrid_intelligent_signing import HybridIntelligentSigning
            if quantum_security:
                self.hybrid_signing = HybridIntelligentSigning(quantum_security)
                print("✅ Assinatura Inteligente: Integrada!")
        except ImportError:
            print("⚠️  Hybrid Intelligent Signing não disponível")
    
    def sign_transaction_intelligent(
        self,
        transaction_data: Dict,
        transaction_value_usd: float = 0.0,
        transaction_type: str = "normal"
    ) -> Dict:
        """
        Assinar transação com estratégia inteligente
        
        Args:
            transaction_data: Dados da transação
            transaction_value_usd: Valor em USD (para decidir algoritmo)
            transaction_type: Tipo de transação
        
        Returns:
            transaction_data com assinatura quântica apropriada
        """
        if not self.hybrid_signing or not self.quantum_security:
            # Fallback: usar ML-DSA simples
            return self._fallback_ml_dsa_signature(transaction_data)
        
        try:
            # Criar hash da transação
            tx_hash = hashlib.sha256(
                json.dumps(transaction_data, sort_keys=True).encode()
            ).digest()
            
            # Obter keypairs se necessário
            qrs3_keypair_id = getattr(self, '_qrs3_keypair_id', None)
            qrs2_keypair_id = getattr(self, '_qrs2_keypair_id', None)
            ml_dsa_keypair_id = getattr(self, '_ml_dsa_keypair_id', None)
            
            # Gerar keypairs se não existirem
            if not qrs3_keypair_id:
                qrs3_result = self.quantum_security.generate_qrs3_keypair()
                if qrs3_result.get("success"):
                    self._qrs3_keypair_id = qrs3_result["keypair_id"]
                    qrs3_keypair_id = self._qrs3_keypair_id
            
            if not qrs2_keypair_id:
                qrs2_result = self.quantum_security.generate_qrs2_keypair()
                if qrs2_result.get("success"):
                    self._qrs2_keypair_id = qrs2_result["keypair_id"]
                    qrs2_keypair_id = self._qrs2_keypair_id
            
            if not ml_dsa_keypair_id:
                ml_dsa_result = self.quantum_security.generate_ml_dsa_keypair(security_level=3)
                if ml_dsa_result.get("success"):
                    self._ml_dsa_keypair_id = ml_dsa_result["keypair_id"]
                    ml_dsa_keypair_id = self._ml_dsa_keypair_id
            
            # Assinar com estratégia inteligente
            result = self.hybrid_signing.sign_intelligent(
                message=tx_hash,
                transaction_value=transaction_value_usd,
                transaction_type=transaction_type,
                urgency="normal",
                qrs3_keypair_id=qrs3_keypair_id,
                qrs2_keypair_id=qrs2_keypair_id,
                ml_dsa_keypair_id=ml_dsa_keypair_id
            )
            
            if result.get("success"):
                # Armazenar assinatura quântica (será removida antes de enviar para blockchain)
                transaction_data["quantum_signature"] = {
                    "algorithm": result.get("algorithm_used", "ML-DSA"),
                    "signature": result.get("signature") or result.get("ml_dsa_signature"),
                    "reason": result.get("reason", "Assinatura inteligente"),
                    "quantum_resistant": True,
                    "nist_standard": True
                }
                
                # Adicionar informações de performance
                if "signing_time_ms" in result:
                    transaction_data["quantum_signature"]["signing_time_ms"] = result["signing_time_ms"]
            
            # NOTA: O campo quantum_signature será removido antes de enviar para blockchain
            # pois transações EVM não aceitam campos não reconhecidos
            return transaction_data
            
        except Exception as e:
            # Fallback em caso de erro
            return self._fallback_ml_dsa_signature(transaction_data)
    
    def _fallback_ml_dsa_signature(self, transaction_data: Dict) -> Dict:
        """Fallback: assinatura ML-DSA simples"""
        if not self.quantum_security:
            return transaction_data
        
        try:
            tx_hash = hashlib.sha256(
                json.dumps(transaction_data, sort_keys=True).encode()
            ).digest()
            
            if not hasattr(self, '_ml_dsa_keypair_id'):
                keypair = self.quantum_security.generate_ml_dsa_keypair(security_level=3)
                self._ml_dsa_keypair_id = keypair.get("keypair_id")
            
            signature_result = self.quantum_security.sign_with_ml_dsa(
                self._ml_dsa_keypair_id,
                tx_hash
            )
            
            if signature_result.get("success"):
                transaction_data["quantum_signature"] = {
                    "algorithm": "ML-DSA",
                    "signature": signature_result.get("signature"),
                    "public_key": signature_result.get("public_key"),
                    "quantum_resistant": True
                }
        except:
            pass
        
        return transaction_data

# =============================================================================
# 2. PARALELIZAÇÃO ENTRE TRANSAÇÕES
# =============================================================================

class ParallelTransactionProcessor:
    """Processa múltiplas transações em paralelo"""
    
    def __init__(self, max_workers: int = 5):
        self.max_workers = max_workers
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
        self.active_tasks = {}
        self.completed_tasks = deque(maxlen=1000)
    
    def process_transactions_parallel(
        self,
        transactions: List[Dict],
        process_func: callable
    ) -> List[Dict]:
        """
        Processar múltiplas transações em paralelo
        
        Args:
            transactions: Lista de transações
            process_func: Função para processar cada transação
        
        Returns:
            Lista de resultados
        """
        if not transactions:
            return []
        
        # Submeter todas as tarefas
        futures = {}
        for i, tx in enumerate(transactions):
            future = self.executor.submit(process_func, tx)
            futures[future] = (i, tx)
        
        # Coletar resultados na ordem de conclusão
        results = [None] * len(transactions)
        for future in as_completed(futures):
            i, tx = futures[future]
            try:
                result = future.result()
                results[i] = result
            except Exception as e:
                results[i] = {
                    "success": False,
                    "error": str(e),
                    "transaction": tx
                }
        
        return results
    
    def process_batch_async(
        self,
        transactions: List[Dict],
        process_func: callable
    ) -> Dict:
        """
        Processar batch de transações de forma assíncrona
        
        Returns:
            {
                "task_id": str,
                "status": "processing",
                "total": len(transactions)
            }
        """
        task_id = f"batch_{int(time.time())}_{hashlib.sha256(str(transactions).encode()).hexdigest()[:8]}"
        
        def process_batch():
            return self.process_transactions_parallel(transactions, process_func)
        
        future = self.executor.submit(process_batch)
        self.active_tasks[task_id] = {
            "future": future,
            "status": "processing",
            "created_at": time.time(),
            "total": len(transactions)
        }
        
        return {
            "task_id": task_id,
            "status": "processing",
            "total": len(transactions)
        }
    
    def get_task_status(self, task_id: str) -> Dict:
        """Obter status de uma tarefa"""
        if task_id not in self.active_tasks:
            return {"status": "not_found"}
        
        task = self.active_tasks[task_id]
        future = task["future"]
        
        if future.done():
            try:
                result = future.result()
                task["status"] = "completed"
                task["result"] = result
                self.completed_tasks.append(task)
                del self.active_tasks[task_id]
                return {
                    "status": "completed",
                    "result": result
                }
            except Exception as e:
                task["status"] = "failed"
                task["error"] = str(e)
                return {
                    "status": "failed",
                    "error": str(e)
                }
        else:
            return {
                "status": "processing",
                "elapsed": time.time() - task["created_at"]
            }

# =============================================================================
# 3. CONNECTION POOL INTELIGENTE
# =============================================================================

@dataclass
class ConnectionMetrics:
    """Métricas de uma conexão"""
    chain: str
    url: str
    latency_ms: float
    success_count: int = 0
    failure_count: int = 0
    last_used: float = 0
    last_success: float = 0
    health_score: float = 1.0  # 0.0 a 1.0

class IntelligentConnectionPool:
    """Connection pool inteligente com métricas"""
    
    def __init__(self):
        self.connections = {}  # chain -> List[ConnectionMetrics]
        self.connection_cache = {}  # chain -> Web3 instance
        self.metrics_history = defaultdict(deque)  # chain -> deque de latências
    
    def add_connection(self, chain: str, url: str, w3_instance=None):
        """Adicionar conexão ao pool"""
        if chain not in self.connections:
            self.connections[chain] = []
        
        metrics = ConnectionMetrics(
            chain=chain,
            url=url,
            latency_ms=0.0,
            last_used=time.time()
        )
        
        self.connections[chain].append(metrics)
        
        if w3_instance:
            self.connection_cache[chain] = w3_instance
    
    def get_optimal_connection(self, chain: str) -> Optional[ConnectionMetrics]:
        """Obter conexão mais rápida e saudável"""
        if chain not in self.connections or not self.connections[chain]:
            return None
        
        # Calcular health score para cada conexão
        for conn in self.connections[chain]:
            # Health score baseado em:
            # - Taxa de sucesso
            # - Latência recente
            # - Último uso
            
            total_requests = conn.success_count + conn.failure_count
            if total_requests > 0:
                success_rate = conn.success_count / total_requests
            else:
                success_rate = 1.0
            
            # Latência normalizada (assumindo 1000ms = 0.0, 0ms = 1.0)
            latency_score = max(0.0, 1.0 - (conn.latency_ms / 1000.0))
            
            # Recency score (últimas 5 minutos = 1.0, mais antigo = menor)
            time_since_use = time.time() - conn.last_used
            recency_score = max(0.0, 1.0 - (time_since_use / 300.0))
            
            # Health score combinado
            conn.health_score = (success_rate * 0.5) + (latency_score * 0.3) + (recency_score * 0.2)
        
        # Retornar conexão com maior health score
        best_connection = max(self.connections[chain], key=lambda c: c.health_score)
        return best_connection
    
    def record_success(self, chain: str, url: str, latency_ms: float):
        """Registrar sucesso de uma conexão"""
        for conn in self.connections.get(chain, []):
            if conn.url == url:
                conn.success_count += 1
                conn.latency_ms = latency_ms
                conn.last_used = time.time()
                conn.last_success = time.time()
                self.metrics_history[chain].append(latency_ms)
                # Manter apenas últimas 100 métricas
                if len(self.metrics_history[chain]) > 100:
                    self.metrics_history[chain].popleft()
                break
    
    def record_failure(self, chain: str, url: str):
        """Registrar falha de uma conexão"""
        for conn in self.connections.get(chain, []):
            if conn.url == url:
                conn.failure_count += 1
                conn.last_used = time.time()
                break
    
    def get_average_latency(self, chain: str) -> float:
        """Obter latência média de uma chain"""
        if chain not in self.metrics_history or not self.metrics_history[chain]:
            return 0.0
        return sum(self.metrics_history[chain]) / len(self.metrics_history[chain])
    
    def get_connection_stats(self, chain: str) -> Dict:
        """Obter estatísticas de conexões"""
        if chain not in self.connections:
            return {"error": "Chain não encontrada"}
        
        stats = {
            "chain": chain,
            "total_connections": len(self.connections[chain]),
            "connections": []
        }
        
        for conn in self.connections[chain]:
            total = conn.success_count + conn.failure_count
            success_rate = (conn.success_count / total * 100) if total > 0 else 0
            
            stats["connections"].append({
                "url": conn.url,
                "latency_ms": conn.latency_ms,
                "success_rate": f"{success_rate:.1f}%",
                "health_score": f"{conn.health_score:.2f}",
                "requests": total
            })
        
        stats["average_latency_ms"] = self.get_average_latency(chain)
        
        return stats

# =============================================================================
# 4. COMPACT SERIALIZATION
# =============================================================================

class CompactSerialization:
    """Serialização compacta de proofs e transações"""
    
    def __init__(self):
        self.use_protobuf = False
        # Tentar importar protobuf
        try:
            import google.protobuf.message
            self.use_protobuf = True
            print("✅ Protobuf disponível para serialização compacta")
        except ImportError:
            print("⚠️  Protobuf não disponível, usando JSON compacto")
    
    def serialize_proof(self, proof_data: Dict) -> bytes:
        """Serializar proof de forma compacta"""
        if self.use_protobuf:
            # TODO: Implementar schema Protobuf
            # Por enquanto, usar JSON compacto
            return json.dumps(proof_data, separators=(',', ':')).encode()
        else:
            # JSON compacto (sem espaços)
            return json.dumps(proof_data, separators=(',', ':')).encode()
    
    def deserialize_proof(self, data: bytes) -> Dict:
        """Deserializar proof"""
        return json.loads(data.decode())
    
    def serialize_transaction(self, tx_data: Dict) -> bytes:
        """Serializar transação de forma compacta"""
        # Remover campos opcionais vazios
        compact_tx = {
            "from": tx_data.get("from"),
            "to": tx_data.get("to"),
            "value": tx_data.get("value"),
            "nonce": tx_data.get("nonce"),
            "gas": tx_data.get("gas"),
            "gasPrice": tx_data.get("gasPrice"),
            "data": tx_data.get("data", ""),
            "chainId": tx_data.get("chainId")
        }
        
        # Remover campos None ou vazios
        compact_tx = {k: v for k, v in compact_tx.items() if v is not None and v != ""}
        
        return json.dumps(compact_tx, separators=(',', ':')).encode()
    
    def get_size_reduction(self, original_data: Dict, serialized: bytes) -> Dict:
        """Calcular redução de tamanho"""
        original_json = json.dumps(original_data, indent=2).encode()
        original_size = len(original_json)
        compact_size = len(serialized)
        
        reduction = ((original_size - compact_size) / original_size) * 100
        
        return {
            "original_size_bytes": original_size,
            "compact_size_bytes": compact_size,
            "reduction_percent": round(reduction, 2),
            "reduction_bytes": original_size - compact_size
        }

# =============================================================================
# 5. OTIMIZAÇÃO SPHINCS+
# =============================================================================

class SPHINCSOptimizer:
    """Otimizações para SPHINCS+"""
    
    def __init__(self, quantum_security=None):
        self.quantum_security = quantum_security
        self.merkle_tree_cache = {}  # message_hash -> precomputed_tree
        self.signature_cache = {}  # message_hash -> signature
        self.cache_hits = 0
        self.cache_misses = 0
    
    def get_cached_signature(self, message_hash: bytes) -> Optional[Dict]:
        """Obter assinatura do cache"""
        hash_str = message_hash.hex()
        if hash_str in self.signature_cache:
            self.cache_hits += 1
            return self.signature_cache[hash_str]
        self.cache_misses += 1
        return None
    
    def cache_signature(self, message_hash: bytes, signature: Dict):
        """Armazenar assinatura no cache"""
        hash_str = message_hash.hex()
        self.signature_cache[hash_str] = signature
        
        # Limitar tamanho do cache (LRU)
        if len(self.signature_cache) > 1000:
            # Remover entrada mais antiga (simples)
            oldest_key = next(iter(self.signature_cache))
            del self.signature_cache[oldest_key]
    
    def get_cache_stats(self) -> Dict:
        """Obter estatísticas do cache"""
        total = self.cache_hits + self.cache_misses
        hit_rate = (self.cache_hits / total * 100) if total > 0 else 0
        
        return {
            "cache_hits": self.cache_hits,
            "cache_misses": self.cache_misses,
            "hit_rate_percent": round(hit_rate, 2),
            "cached_signatures": len(self.signature_cache),
            "cached_trees": len(self.merkle_tree_cache)
        }

