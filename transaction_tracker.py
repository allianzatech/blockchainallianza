#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
📊 TRANSACTION STATUS TRACKING AVANÇADO
Rastreamento em tempo real de transações cross-chain
"""

import time
import json
from typing import Dict, List, Optional
from datetime import datetime, timedelta
from enum import Enum
from dataclasses import dataclass, asdict
from collections import defaultdict, deque

class TransactionStatus(Enum):
    """Status de uma transação"""
    PENDING = "pending"
    BROADCASTED = "broadcasted"
    CONFIRMED = "confirmed"
    FINALIZED = "finalized"
    FAILED = "failed"
    CANCELLED = "cancelled"

@dataclass
class TransactionState:
    """Estado de uma transação"""
    tx_id: str
    source_chain: str
    target_chain: str
    status: TransactionStatus
    source_tx_hash: Optional[str] = None
    target_tx_hash: Optional[str] = None
    amount: float = 0.0
    token_symbol: str = ""
    created_at: float = 0.0
    updated_at: float = 0.0
    confirmations: int = 0
    required_confirmations: int = 0
    estimated_completion: Optional[float] = None
    error: Optional[str] = None
    metadata: Dict = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}
        if self.created_at == 0.0:
            self.created_at = time.time()
        if self.updated_at == 0.0:
            self.updated_at = time.time()

class TransactionTracker:
    """Rastreador de transações cross-chain"""
    
    def __init__(self):
        self.transactions = {}  # tx_id -> TransactionState
        self.transactions_by_hash = {}  # tx_hash -> tx_id
        self.history = deque(maxlen=10000)  # Histórico de mudanças
        self.subscribers = defaultdict(list)  # tx_id -> List[callbacks]
        self.chain_stats = defaultdict(lambda: {
            "total": 0,
            "pending": 0,
            "confirmed": 0,
            "failed": 0,
            "avg_time": 0.0
        })
    
    def create_transaction(
        self,
        tx_id: str,
        source_chain: str,
        target_chain: str,
        amount: float,
        token_symbol: str,
        required_confirmations: Optional[int] = None
    ) -> TransactionState:
        """Criar nova transação para rastreamento"""
        if required_confirmations is None:
            # Valores padrão por chain
            required_confirmations = {
                "bitcoin": 6,
                "ethereum": 12,
                "polygon": 12,
                "bsc": 12,
                "solana": 1
            }.get(source_chain.lower(), 12)
        
        state = TransactionState(
            tx_id=tx_id,
            source_chain=source_chain,
            target_chain=target_chain,
            status=TransactionStatus.PENDING,
            amount=amount,
            token_symbol=token_symbol,
            required_confirmations=required_confirmations
        )
        
        self.transactions[tx_id] = state
        self.chain_stats[source_chain]["total"] += 1
        self.chain_stats[source_chain]["pending"] += 1
        
        self._log_change(state, "created")
        
        return state
    
    def update_status(
        self,
        tx_id: str,
        status: TransactionStatus,
        tx_hash: Optional[str] = None,
        confirmations: Optional[int] = None,
        error: Optional[str] = None,
        metadata: Optional[Dict] = None
    ) -> bool:
        """Atualizar status de uma transação"""
        if tx_id not in self.transactions:
            return False
        
        state = self.transactions[tx_id]
        old_status = state.status
        
        state.status = status
        state.updated_at = time.time()
        
        if tx_hash:
            if not state.source_tx_hash:
                state.source_tx_hash = tx_hash
                self.transactions_by_hash[tx_hash] = tx_id
            elif not state.target_tx_hash and status == TransactionStatus.CONFIRMED:
                state.target_tx_hash = tx_hash
                self.transactions_by_hash[tx_hash] = tx_id
        
        if confirmations is not None:
            state.confirmations = confirmations
        
        if error:
            state.error = error
        
        if metadata:
            state.metadata.update(metadata)
        
        # Atualizar estatísticas
        self._update_stats(old_status, state.status, state.source_chain)
        
        # Calcular estimativa de conclusão
        if status == TransactionStatus.BROADCASTED:
            # Estimar baseado em histórico
            avg_time = self.chain_stats[state.source_chain].get("avg_time", 60)
            state.estimated_completion = time.time() + avg_time
        
        self._log_change(state, f"status_changed: {old_status.value} -> {status.value}")
        
        # Notificar subscribers
        self._notify_subscribers(tx_id, state)
        
        return True
    
    def get_transaction(self, tx_id: str) -> Optional[TransactionState]:
        """Obter estado de uma transação"""
        return self.transactions.get(tx_id)
    
    def get_transaction_by_hash(self, tx_hash: str) -> Optional[TransactionState]:
        """Obter transação por hash"""
        tx_id = self.transactions_by_hash.get(tx_hash)
        if tx_id:
            return self.transactions.get(tx_id)
        return None
    
    def subscribe(self, tx_id: str, callback: callable):
        """Inscrever-se em atualizações de uma transação"""
        self.subscribers[tx_id].append(callback)
    
    def unsubscribe(self, tx_id: str, callback: callable):
        """Cancelar inscrição"""
        if tx_id in self.subscribers:
            self.subscribers[tx_id] = [cb for cb in self.subscribers[tx_id] if cb != callback]
    
    def _notify_subscribers(self, tx_id: str, state: TransactionState):
        """Notificar subscribers"""
        for callback in self.subscribers.get(tx_id, []):
            try:
                callback(state)
            except Exception as e:
                print(f"⚠️  Erro ao notificar subscriber: {e}")
    
    def _update_stats(self, old_status: TransactionStatus, new_status: TransactionStatus, chain: str):
        """Atualizar estatísticas"""
        stats = self.chain_stats[chain]
        
        # Remover do status antigo
        if old_status == TransactionStatus.PENDING:
            stats["pending"] = max(0, stats["pending"] - 1)
        elif old_status == TransactionStatus.CONFIRMED:
            stats["confirmed"] = max(0, stats["confirmed"] - 1)
        elif old_status == TransactionStatus.FAILED:
            stats["failed"] = max(0, stats["failed"] - 1)
        
        # Adicionar ao novo status
        if new_status == TransactionStatus.PENDING:
            stats["pending"] += 1
        elif new_status == TransactionStatus.CONFIRMED:
            stats["confirmed"] += 1
            # Calcular tempo médio
            if tx_id in self.transactions:
                state = self.transactions[tx_id]
                elapsed = state.updated_at - state.created_at
                # Média móvel
                if stats["avg_time"] == 0:
                    stats["avg_time"] = elapsed
                else:
                    stats["avg_time"] = (stats["avg_time"] * 0.9) + (elapsed * 0.1)
        elif new_status == TransactionStatus.FAILED:
            stats["failed"] += 1
    
    def _log_change(self, state: TransactionState, event: str):
        """Registrar mudança no histórico"""
        self.history.append({
            "timestamp": time.time(),
            "tx_id": state.tx_id,
            "event": event,
            "status": state.status.value,
            "confirmations": state.confirmations
        })
    
    def get_status_summary(self, tx_id: str) -> Dict:
        """Obter resumo de status de uma transação"""
        state = self.get_transaction(tx_id)
        if not state:
            return {"error": "Transaction not found"}
        
        elapsed = time.time() - state.created_at
        progress = 0.0
        
        if state.status == TransactionStatus.PENDING:
            progress = 10.0
        elif state.status == TransactionStatus.BROADCASTED:
            if state.required_confirmations > 0:
                progress = 30.0 + (state.confirmations / state.required_confirmations * 50.0)
            else:
                progress = 50.0
        elif state.status == TransactionStatus.CONFIRMED:
            progress = 90.0
        elif state.status == TransactionStatus.FINALIZED:
            progress = 100.0
        elif state.status == TransactionStatus.FAILED:
            progress = 0.0
        
        return {
            "tx_id": tx_id,
            "status": state.status.value,
            "progress_percent": round(progress, 1),
            "elapsed_seconds": round(elapsed, 1),
            "confirmations": f"{state.confirmations}/{state.required_confirmations}",
            "source_tx_hash": state.source_tx_hash,
            "target_tx_hash": state.target_tx_hash,
            "estimated_completion": datetime.fromtimestamp(state.estimated_completion).isoformat() if state.estimated_completion else None,
            "error": state.error
        }
    
    def get_chain_statistics(self, chain: str) -> Dict:
        """Obter estatísticas de uma chain"""
        return dict(self.chain_stats.get(chain, {}))
    
    def get_all_statistics(self) -> Dict:
        """Obter todas as estatísticas"""
        return {
            "total_transactions": len(self.transactions),
            "by_chain": dict(self.chain_stats),
            "recent_history": list(self.history)[-100:]  # Últimas 100 mudanças
        }

# Instância global
global_transaction_tracker = TransactionTracker()



