#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MELHORIAS DO BRIDGE CROSS-CHAIN
Implementações das melhorias sugeridas para o sistema de bridge
"""

import time
import json
import hashlib
from typing import Dict, List, Optional, Tuple, Callable
from concurrent.futures import ThreadPoolExecutor, as_completed
from collections import defaultdict, deque
from datetime import datetime, timedelta
import threading

# =============================================================================
# 1. PROCESSAMENTO ASSÍNCRONO COMPLETO
# =============================================================================

class AsyncBridgeProcessor:
    """Processador assíncrono completo para transações cross-chain"""
    
    def __init__(self, bridge_instance, max_workers: int = 5):
        self.bridge = bridge_instance
        self.max_workers = max_workers
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
        self.pending_tasks = {}
        self.completed_tasks = {}
        self.lock = threading.Lock()
        
    def process_transfer_async(
        self,
        source_chain: str,
        target_chain: str,
        amount: float,
        token_symbol: str,
        recipient: str,
        source_private_key: Optional[str] = None,
        priority: int = 5  # 1-10, maior = mais prioritário
    ) -> str:
        """
        Processar transferência cross-chain de forma assíncrona
        
        Returns:
            task_id: ID da tarefa para acompanhar status
        """
        import secrets
        task_id = f"async_transfer_{int(time.time())}_{secrets.token_hex(8)}"
        
        # Criar função wrapper para processar
        def process_wrapper():
            try:
                result = self.bridge.real_cross_chain_transfer(
                    source_chain=source_chain,
                    target_chain=target_chain,
                    amount=amount,
                    token_symbol=token_symbol,
                    recipient=recipient,
                    source_private_key=source_private_key
                )
                return result
            except Exception as e:
                return {
                    "success": False,
                    "error": str(e),
                    "task_id": task_id
                }
        
        # Registrar tarefa
        with self.lock:
            self.pending_tasks[task_id] = {
                "task_id": task_id,
                "source_chain": source_chain,
                "target_chain": target_chain,
                "amount": amount,
                "token_symbol": token_symbol,
                "recipient": recipient,
                "priority": priority,
                "status": "pending",
                "created_at": time.time(),
                "future": None
            }
        
        # Submeter para processamento assíncrono
        future = self.executor.submit(process_wrapper)
        
        with self.lock:
            self.pending_tasks[task_id]["future"] = future
            self.pending_tasks[task_id]["status"] = "processing"
        
        # MELHORIA: Monitoramento otimizado - usar callback do future ao invés de thread separada
        # Isso reduz overhead e locks desnecessários
        def monitor_completion(fut, tid):
            try:
                result = fut.result()
                # Usar lock apenas quando necessário (atualizar status)
                with self.lock:
                    if tid in self.pending_tasks:
                        task = self.pending_tasks.pop(tid)
                        task["status"] = "completed" if result.get("success") else "failed"
                        task["result"] = result
                        task["completed_at"] = time.time()
                        self.completed_tasks[tid] = task
            except Exception as e:
                with self.lock:
                    if tid in self.pending_tasks:
                        task = self.pending_tasks.pop(tid)
                        task["status"] = "failed"
                        task["error"] = str(e)
                        task["completed_at"] = time.time()
                        self.completed_tasks[tid] = task
        
        # MELHORIA: Usar add_done_callback ao invés de thread separada (menos overhead)
        future.add_done_callback(lambda f: monitor_completion(f, task_id))
        
        return task_id
    
    def get_task_status(self, task_id: str) -> Dict:
        """Obter status de uma tarefa"""
        with self.lock:
            if task_id in self.pending_tasks:
                task = self.pending_tasks[task_id]
                if task["future"] and task["future"].done():
                    try:
                        result = task["future"].result()
                        return {
                            "task_id": task_id,
                            "status": "completed" if result.get("success") else "failed",
                            "result": result
                        }
                    except Exception as e:
                        return {
                            "task_id": task_id,
                            "status": "failed",
                            "error": str(e)
                        }
                else:
                    return {
                        "task_id": task_id,
                        "status": task["status"],
                        "progress": "processing"
                    }
            elif task_id in self.completed_tasks:
                return {
                    "task_id": task_id,
                    "status": self.completed_tasks[task_id]["status"],
                    "result": self.completed_tasks[task_id].get("result")
                }
            else:
                return {
                    "task_id": task_id,
                    "status": "not_found"
                }
    
    def get_pending_tasks(self) -> List[Dict]:
        """Obter lista de tarefas pendentes"""
        with self.lock:
            return [
                {
                    "task_id": tid,
                    "source_chain": task["source_chain"],
                    "target_chain": task["target_chain"],
                    "amount": task["amount"],
                    "status": task["status"],
                    "created_at": task["created_at"]
                }
                for tid, task in self.pending_tasks.items()
            ]


# =============================================================================
# 2. QUANTUM-SAFE LOCK VERIFICATION
# =============================================================================

class QuantumSafeLockVerifier:
    """Verificador de locks com assinatura quântica"""
    
    def __init__(self, quantum_security=None):
        self.quantum_security = quantum_security
        self.verified_locks = {}
        
    def create_quantum_safe_lock(
        self,
        chain: str,
        tx_hash: str,
        amount: float,
        token_symbol: str,
        recipient: str
    ) -> Dict:
        """
        Criar lock com assinatura quântica
        """
        lock_data = {
            "chain": chain,
            "tx_hash": tx_hash,
            "amount": amount,
            "token_symbol": token_symbol,
            "recipient": recipient,
            "timestamp": time.time(),
            "lock_id": f"lock_{chain}_{tx_hash[:16]}"
        }
        
        # Adicionar assinatura quântica se disponível
        if self.quantum_security:
            try:
                # Criar hash do lock
                lock_hash = hashlib.sha256(
                    json.dumps(lock_data, sort_keys=True).encode()
                ).digest()
                
                # Assinar com ML-DSA
                if hasattr(self.quantum_security, 'sign_ml_dsa'):
                    signature_result = self.quantum_security.sign_ml_dsa(
                        keypair_id=None,  # Usar keypair padrão
                        message=lock_hash
                    )
                    
                    if signature_result.get("success"):
                        lock_data["quantum_signature"] = {
                            "algorithm": "ML-DSA",
                            "signature": signature_result.get("signature"),
                            "public_key": signature_result.get("public_key"),
                            "nist_standard": True
                        }
            except Exception as e:
                print(f"⚠️  Erro ao adicionar assinatura quântica ao lock: {e}")
        
        return lock_data
    
    def verify_quantum_lock(
        self,
        lock_data: Dict,
        expected_chain: str,
        expected_tx_hash: str
    ) -> Tuple[bool, Optional[str]]:
        """
        Verificar lock com assinatura quântica
        """
        # Verificar dados básicos
        if lock_data.get("chain") != expected_chain:
            return False, f"Chain mismatch: {lock_data.get('chain')} != {expected_chain}"
        
        if lock_data.get("tx_hash") != expected_tx_hash:
            return False, f"TX hash mismatch: {lock_data.get('tx_hash')} != {expected_tx_hash}"
        
        # Verificar assinatura quântica se presente
        if "quantum_signature" in lock_data and self.quantum_security:
            try:
                # Recriar hash do lock (sem assinatura)
                lock_data_copy = lock_data.copy()
                lock_data_copy.pop("quantum_signature", None)
                lock_hash = hashlib.sha256(
                    json.dumps(lock_data_copy, sort_keys=True).encode()
                ).digest()
                
                # Verificar assinatura
                sig_data = lock_data["quantum_signature"]
                if hasattr(self.quantum_security, 'verify_ml_dsa'):
                    verify_result = self.quantum_security.verify_ml_dsa(
                        public_key=sig_data.get("public_key"),
                        message=lock_hash,
                        signature=sig_data.get("signature")
                    )
                    
                    if not verify_result.get("success"):
                        return False, "Assinatura quântica inválida"
            except Exception as e:
                return False, f"Erro ao verificar assinatura quântica: {e}"
        
        # Lock válido
        lock_id = lock_data.get("lock_id")
        if lock_id:
            self.verified_locks[lock_id] = {
                "verified_at": time.time(),
                "lock_data": lock_data
            }
        
        return True, None


# =============================================================================
# 3. BATCH PROCESSING DE TRANSAÇÕES
# =============================================================================

class BatchTransactionProcessor:
    """Processador de transações em batch"""
    
    def __init__(self, bridge_instance):
        self.bridge = bridge_instance
        self.batch_queue = defaultdict(list)  # Agrupar por chain
        self.batch_size = 10  # Máximo de transações por batch
        self.batch_timeout = 5.0  # Segundos para agrupar transações
        
    def add_to_batch(
        self,
        chain: str,
        from_private_key: str,
        to_address: str,
        amount: float,
        token_symbol: str = None
    ) -> Dict:
        """
        Adicionar transação ao batch
        """
        transaction = {
            "from_private_key": from_private_key,
            "to_address": to_address,
            "amount": amount,
            "token_symbol": token_symbol,
            "added_at": time.time()
        }
        
        self.batch_queue[chain].append(transaction)
        
        # Se batch está cheio, processar imediatamente
        if len(self.batch_queue[chain]) >= self.batch_size:
            return self.process_batch(chain)
        
        return {
            "success": True,
            "status": "queued",
            "batch_size": len(self.batch_queue[chain]),
            "chain": chain
        }
    
    def process_batch(self, chain: str) -> Dict:
        """
        Processar batch de transações para uma chain (PARALELIZADO)
        """
        if chain not in self.batch_queue or not self.batch_queue[chain]:
            return {
                "success": False,
                "error": f"Nenhuma transação em batch para {chain}"
            }
        
        transactions = self.batch_queue[chain]
        self.batch_queue[chain] = []  # Limpar fila
        
        # MELHORIA: Processar em paralelo usando ThreadPoolExecutor
        from concurrent.futures import ThreadPoolExecutor, as_completed
        
        def process_single_tx(tx):
            try:
                result = self.bridge.send_evm_transaction(
                    chain=chain,
                    from_private_key=tx["from_private_key"],
                    to_address=tx["to_address"],
                    amount=tx["amount"],
                    token_symbol=tx.get("token_symbol")
                )
                return result
            except Exception as e:
                return {
                    "success": False,
                    "error": str(e),
                    "transaction": tx
                }
        
        # Processar até 5 transações em paralelo
        results = []
        max_workers = min(5, len(transactions))
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {executor.submit(process_single_tx, tx): tx for tx in transactions}
            
            for future in as_completed(futures):
                try:
                    result = future.result(timeout=60)  # 60s timeout por transação
                    results.append(result)
                except Exception as e:
                    tx = futures[future]
                    results.append({
                        "success": False,
                        "error": str(e),
                        "transaction": tx
                    })
        
        successful = sum(1 for r in results if r.get("success"))
        
        return {
            "success": True,
            "processed": len(transactions),
            "successful": successful,
            "failed": len(transactions) - successful,
            "results": results,
            "chain": chain
        }
    
    def process_all_batches(self) -> Dict:
        """Processar todos os batches pendentes"""
        all_results = {}
        for chain in list(self.batch_queue.keys()):
            if self.batch_queue[chain]:
                all_results[chain] = self.process_batch(chain)
        
        return {
            "success": True,
            "chains_processed": list(all_results.keys()),
            "results": all_results
        }


# =============================================================================
# 4. VALIDAÇÃO PARALELA DE MÚLTIPLAS CHAINS
# =============================================================================

class ParallelChainValidator:
    """Validador paralelo de múltiplas chains"""
    
    def __init__(self, bridge_instance, max_workers: int = 5):
        self.bridge = bridge_instance
        self.max_workers = max_workers
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
    
    def validate_transactions_parallel(
        self,
        validations: List[Dict]  # [{"chain": "...", "tx_hash": "...", "min_confirmations": ...}]
    ) -> Dict:
        """
        Validar múltiplas transações em paralelo
        """
        def validate_single(validation):
            chain = validation["chain"]
            tx_hash = validation["tx_hash"]
            min_confirmations = validation.get("min_confirmations", 12)
            
            try:
                result = self.bridge.wait_for_confirmations(
                    chain=chain,
                    tx_hash=tx_hash,
                    min_confirmations=min_confirmations
                )
                return {
                    "chain": chain,
                    "tx_hash": tx_hash,
                    "success": result.get("success", False),
                    "confirmations": result.get("confirmations", 0),
                    "result": result
                }
            except Exception as e:
                return {
                    "chain": chain,
                    "tx_hash": tx_hash,
                    "success": False,
                    "error": str(e)
                }
        
        # Executar validações em paralelo
        futures = {
            self.executor.submit(validate_single, v): v
            for v in validations
        }
        
        results = []
        for future in as_completed(futures):
            try:
                result = future.result(timeout=300)  # 5 minutos timeout
                results.append(result)
            except Exception as e:
                validation = futures[future]
                results.append({
                    "chain": validation["chain"],
                    "tx_hash": validation["tx_hash"],
                    "success": False,
                    "error": f"Timeout ou erro: {str(e)}"
                })
        
        successful = sum(1 for r in results if r.get("success"))
        
        return {
            "success": successful == len(validations),
            "total": len(validations),
            "successful": successful,
            "failed": len(validations) - successful,
            "results": results
        }


# =============================================================================
# 5. RATE LIMITING INTELIGENTE
# =============================================================================

class IntelligentRateLimiter:
    """Rate limiter adaptativo baseado em comportamento"""
    
    def __init__(self):
        self.requests = defaultdict(lambda: deque())  # Por identificador
        self.whitelist = set()  # Endereços/IPs confiáveis
        self.limits = {
            "default": {"max_requests": 100, "window": 60},  # 100 req/min
            "transfer": {"max_requests": 10, "window": 60},   # 10 transfers/min
            "query": {"max_requests": 200, "window": 60}      # 200 queries/min
        }
        self.behavior_scores = defaultdict(lambda: 1.0)  # Score de comportamento (0-1)
        self.lock = threading.Lock()
    
    def add_to_whitelist(self, identifier: str):
        """Adicionar identificador à whitelist"""
        self.whitelist.add(identifier)
    
    def is_allowed(
        self,
        identifier: str,
        operation_type: str = "default"
    ) -> Tuple[bool, Optional[str]]:
        """
        Verificar se requisição é permitida
        
        Returns:
            (is_allowed, error_message)
        """
        with self.lock:
            # Whitelist sempre permitido
            if identifier in self.whitelist:
                return True, None
            
            # Obter limites para tipo de operação
            limits = self.limits.get(operation_type, self.limits["default"])
            max_requests = limits["max_requests"]
            window = limits["window"]
            
            # Ajustar limite baseado em comportamento
            behavior_multiplier = self.behavior_scores.get(identifier, 1.0)
            adjusted_limit = int(max_requests * behavior_multiplier)
            
            # Limpar requisições antigas
            now = time.time()
            request_times = self.requests[identifier]
            while request_times and (now - request_times[0]) > window:
                request_times.popleft()
            
            # Verificar se excedeu limite
            if len(request_times) >= adjusted_limit:
                return False, f"Rate limit excedido: {len(request_times)}/{adjusted_limit} requisições em {window}s"
            
            # Registrar requisição
            request_times.append(now)
            
            return True, None
    
    def update_behavior_score(self, identifier: str, success: bool):
        """Atualizar score de comportamento baseado em sucesso/falha"""
        with self.lock:
            current_score = self.behavior_scores[identifier]
            if success:
                # Aumentar score (máximo 1.0)
                self.behavior_scores[identifier] = min(1.0, current_score + 0.01)
            else:
                # Diminuir score (mínimo 0.1)
                self.behavior_scores[identifier] = max(0.1, current_score - 0.05)


# =============================================================================
# 6. ANOMALY DETECTION
# =============================================================================

class AnomalyDetector:
    """Detector de anomalias em transações cross-chain"""
    
    def __init__(self):
        self.transaction_history = deque(maxlen=1000)  # Últimas 1000 transações
        self.suspicious_patterns = []
        self.lock = threading.Lock()
        
        # Thresholds para detecção
        self.thresholds = {
            "max_amount_multiplier": 10.0,  # 10x maior que média
            "max_frequency": 5,  # 5 transações por minuto
            "max_total_daily": 100  # 100 transações por dia
        }
    
    def analyze_transaction(
        self,
        source_chain: str,
        target_chain: str,
        amount: float,
        token_symbol: str,
        sender: str,
        recipient: str
    ) -> Dict:
        """
        Analisar transação para detectar anomalias
        
        Returns:
            {
                "is_suspicious": bool,
                "risk_score": float,  # 0-1
                "reasons": List[str],
                "should_block": bool
            }
        """
        with self.lock:
            now = time.time()
            
            # Registrar transação
            transaction = {
                "timestamp": now,
                "source_chain": source_chain,
                "target_chain": target_chain,
                "amount": amount,
                "token_symbol": token_symbol,
                "sender": sender,
                "recipient": recipient
            }
            self.transaction_history.append(transaction)
            
            # Análises
            reasons = []
            risk_score = 0.0
            
            # 1. Verificar valor muito alto
            recent_amounts = [
                tx["amount"] for tx in self.transaction_history
                if tx.get("token_symbol") == token_symbol
                and (now - tx["timestamp"]) < 3600  # Última hora
            ]
            
            if recent_amounts:
                avg_amount = sum(recent_amounts) / len(recent_amounts)
                if amount > avg_amount * self.thresholds["max_amount_multiplier"]:
                    reasons.append(f"Valor muito alto: {amount} vs média {avg_amount:.2f}")
                    risk_score += 0.3
            
            # 2. Verificar frequência muito alta
            recent_from_sender = [
                tx for tx in self.transaction_history
                if tx.get("sender") == sender
                and (now - tx["timestamp"]) < 60  # Último minuto
            ]
            
            if len(recent_from_sender) > self.thresholds["max_frequency"]:
                reasons.append(f"Frequência muito alta: {len(recent_from_sender)} transações/minuto")
                risk_score += 0.4
            
            # 3. Verificar total diário
            today_start = now - (now % 86400)  # Início do dia
            today_transactions = [
                tx for tx in self.transaction_history
                if tx["timestamp"] >= today_start
            ]
            
            if len(today_transactions) > self.thresholds["max_total_daily"]:
                reasons.append(f"Muitas transações hoje: {len(today_transactions)}")
                risk_score += 0.2
            
            # 4. Verificar padrões suspeitos (mesmo destinatário repetido)
            recent_to_recipient = [
                tx for tx in self.transaction_history
                if tx.get("recipient") == recipient
                and (now - tx["timestamp"]) < 300  # Últimos 5 minutos
            ]
            
            if len(recent_to_recipient) > 10:
                reasons.append(f"Muitas transações para mesmo destinatário: {len(recent_to_recipient)}")
                risk_score += 0.1
            
            # Decisão
            is_suspicious = risk_score > 0.5
            should_block = risk_score > 0.8
            
            if is_suspicious:
                self.suspicious_patterns.append({
                    "timestamp": now,
                    "transaction": transaction,
                    "risk_score": risk_score,
                    "reasons": reasons
                })
            
            return {
                "is_suspicious": is_suspicious,
                "risk_score": risk_score,
                "reasons": reasons,
                "should_block": should_block
            }
    
    def get_suspicious_patterns(self, limit: int = 10) -> List[Dict]:
        """Obter padrões suspeitos recentes"""
        with self.lock:
            return list(self.suspicious_patterns[-limit:])

