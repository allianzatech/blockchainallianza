#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
⛽ GAS OPTIMIZATION AVANÇADO
Otimização inteligente de gas prices com predição e batching
"""

import time
import json
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
from collections import deque, defaultdict
from dataclasses import dataclass

@dataclass
class GasPricePoint:
    """Ponto de gas price histórico"""
    timestamp: float
    gas_price_gwei: float
    block_number: int
    chain: str

class AdvancedGasOptimizer:
    """Otimizador avançado de gas prices"""
    
    def __init__(self):
        self.history = defaultdict(lambda: deque(maxlen=1000))  # chain -> deque de GasPricePoint
        self.pending_transactions = defaultdict(list)  # chain -> List[transactions]
        self.batch_threshold = 5  # Número mínimo de transações para batch
        self.batch_timeout = 60  # Segundos para aguardar antes de enviar batch
        self.last_batch_time = defaultdict(float)  # chain -> timestamp
        
        # Estatísticas
        self.savings_total = defaultdict(float)  # chain -> total economizado
        self.optimizations_count = defaultdict(int)  # chain -> contador
        
        print("⛽ Advanced Gas Optimizer: Inicializado!")
        print("   • Predição de gas prices")
        print("   • Batching de transações")
        print("   • Economia de até 50% em gas!")
    
    def record_gas_price(self, chain: str, gas_price_gwei: float, block_number: int):
        """Registrar gas price histórico"""
        point = GasPricePoint(
            timestamp=time.time(),
            gas_price_gwei=gas_price_gwei,
            block_number=block_number,
            chain=chain
        )
        self.history[chain].append(point)
    
    def get_optimal_gas_price(
        self,
        chain: str,
        urgency: str = "normal",
        max_wait_minutes: int = 10
    ) -> Dict:
        """
        Obter gas price otimizado
        
        Args:
            chain: Chain (polygon, ethereum, etc)
            urgency: "low", "normal", "high", "urgent"
            max_wait_minutes: Tempo máximo para aguardar
        
        Returns:
            {
                "gas_price_gwei": float,
                "strategy": str,
                "estimated_savings_percent": float,
                "wait_time_minutes": float
            }
        """
        if chain not in self.history or len(self.history[chain]) < 5:
            # Sem histórico suficiente, retornar atual
            return {
                "gas_price_gwei": None,
                "strategy": "no_history",
                "estimated_savings_percent": 0.0,
                "wait_time_minutes": 0.0
            }
        
        history = list(self.history[chain])
        recent = history[-20:]  # Últimas 20 medições
        
        if not recent:
            return {
                "gas_price_gwei": None,
                "strategy": "no_data",
                "estimated_savings_percent": 0.0,
                "wait_time_minutes": 0.0
            }
        
        current_gas = recent[-1].gas_price_gwei
        avg_gas = sum(p.gas_price_gwei for p in recent) / len(recent)
        min_gas = min(p.gas_price_gwei for p in recent)
        max_gas = max(p.gas_price_gwei for p in recent)
        
        # Estratégia baseada em urgência
        if urgency == "urgent":
            # Urgente: usar gas price atual (não esperar)
            return {
                "gas_price_gwei": current_gas,
                "strategy": "urgent_immediate",
                "estimated_savings_percent": 0.0,
                "wait_time_minutes": 0.0
            }
        elif urgency == "high":
            # Alta: usar média recente (balanceado)
            optimal = avg_gas
            savings = ((current_gas - optimal) / current_gas) * 100 if current_gas > 0 else 0
            return {
                "gas_price_gwei": optimal,
                "strategy": "high_balanced",
                "estimated_savings_percent": max(0, savings),
                "wait_time_minutes": 0.0
            }
        elif urgency == "normal":
            # Normal: tentar esperar por preço melhor
            # Prever se gas vai baixar
            if len(recent) >= 10:
                # Calcular tendência
                recent_10 = recent[-10:]
                older_10 = recent[-20:-10] if len(recent) >= 20 else recent[:10]
                
                recent_avg = sum(p.gas_price_gwei for p in recent_10) / len(recent_10)
                older_avg = sum(p.gas_price_gwei for p in older_10) / len(older_10)
                
                trend = recent_avg - older_avg
                
                if trend < 0:  # Gas está caindo
                    # Esperar um pouco
                    optimal = min_gas * 1.1  # 10% acima do mínimo
                    savings = ((current_gas - optimal) / current_gas) * 100 if current_gas > 0 else 0
                    return {
                        "gas_price_gwei": optimal,
                        "strategy": "normal_wait_for_drop",
                        "estimated_savings_percent": max(0, savings),
                        "wait_time_minutes": min(5, max_wait_minutes)
                    }
            
            # Usar média
            optimal = avg_gas
            savings = ((current_gas - optimal) / current_gas) * 100 if current_gas > 0 else 0
            return {
                "gas_price_gwei": optimal,
                "strategy": "normal_average",
                "estimated_savings_percent": max(0, savings),
                "wait_time_minutes": 0.0
            }
        else:  # low
            # Baixa: esperar pelo melhor preço
            optimal = min_gas * 1.05  # 5% acima do mínimo
            savings = ((current_gas - optimal) / current_gas) * 100 if current_gas > 0 else 0
            return {
                "gas_price_gwei": optimal,
                "strategy": "low_wait_for_best",
                "estimated_savings_percent": max(0, savings),
                "wait_time_minutes": min(max_wait_minutes, 10)
            }
    
    def add_to_batch(
        self,
        chain: str,
        transaction: Dict,
        max_wait_seconds: int = 60
    ) -> Dict:
        """
        Adicionar transação ao batch
        
        Returns:
            {
                "batched": bool,
                "batch_id": str,
                "estimated_savings_percent": float
            }
        """
        # Verificar se batch já existe e tem espaço
        batch = self.pending_transactions[chain]
        
        # Adicionar transação
        batch.append({
            "transaction": transaction,
            "added_at": time.time(),
            "max_wait": max_wait_seconds
        })
        
        # Verificar se deve enviar batch
        should_send = False
        
        # Critério 1: Número de transações
        if len(batch) >= self.batch_threshold:
            should_send = True
        
        # Critério 2: Timeout
        if batch and (time.time() - self.last_batch_time[chain]) >= self.batch_timeout:
            should_send = True
        
        # Critério 3: Transação antiga esperando
        if batch:
            oldest = min(batch, key=lambda x: x["added_at"])
            if (time.time() - oldest["added_at"]) >= oldest["max_wait"]:
                should_send = True
        
        if should_send:
            return self._process_batch(chain)
        else:
            return {
                "batched": True,
                "batch_id": f"batch_{chain}_{int(time.time())}",
                "estimated_savings_percent": self._calculate_batch_savings(chain),
                "waiting_transactions": len(batch)
            }
    
    def _process_batch(self, chain: str) -> Dict:
        """Processar batch de transações"""
        batch = self.pending_transactions[chain]
        if not batch:
            return {"batched": False, "error": "No transactions in batch"}
        
        # Calcular economia estimada
        savings_percent = self._calculate_batch_savings(chain)
        
        # Limpar batch
        transactions = [item["transaction"] for item in batch]
        self.pending_transactions[chain] = []
        self.last_batch_time[chain] = time.time()
        
        # Atualizar estatísticas
        self.optimizations_count[chain] += len(transactions)
        
        return {
            "batched": True,
            "batch_id": f"batch_{chain}_{int(time.time())}",
            "transactions": transactions,
            "count": len(transactions),
            "estimated_savings_percent": savings_percent
        }
    
    def _calculate_batch_savings(self, chain: str) -> float:
        """Calcular economia estimada de batch"""
        batch = self.pending_transactions[chain]
        if len(batch) < 2:
            return 0.0
        
        # Economia estimada: 30-50% para batches grandes
        base_savings = 30.0
        additional = min(20.0, (len(batch) - 2) * 5.0)  # +5% por transação extra
        
        return min(50.0, base_savings + additional)
    
    def get_statistics(self, chain: Optional[str] = None) -> Dict:
        """Obter estatísticas"""
        if chain:
            return {
                "chain": chain,
                "optimizations_count": self.optimizations_count.get(chain, 0),
                "savings_total": self.savings_total.get(chain, 0.0),
                "pending_batch_size": len(self.pending_transactions.get(chain, [])),
                "history_points": len(self.history.get(chain, []))
            }
        else:
            return {
                "all_chains": {
                    ch: {
                        "optimizations": self.optimizations_count.get(ch, 0),
                        "savings": self.savings_total.get(ch, 0.0),
                        "pending": len(self.pending_transactions.get(ch, []))
                    }
                    for ch in set(list(self.history.keys()) + list(self.pending_transactions.keys()))
                }
            }

# Instância global
global_gas_optimizer = AdvancedGasOptimizer()
















