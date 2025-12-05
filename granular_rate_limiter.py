#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🚦 GRANULAR RATE LIMITER - ALLIANZA BLOCKCHAIN
Rate limiting granular por endereço, tipo de operação, valor, etc.
"""

import time
from typing import Dict, Optional, List, Tuple
from collections import defaultdict, deque
from dataclasses import dataclass
from enum import Enum

class RateLimitType(Enum):
    """Tipo de rate limit"""
    ADDRESS = "address"
    IP = "ip"
    OPERATION = "operation"
    VALUE = "value"
    COMBINED = "combined"

@dataclass
class RateLimitRule:
    """Regra de rate limit"""
    limit_type: RateLimitType
    identifier: str  # Endereço, IP, operação, etc.
    max_requests: int
    window_seconds: int
    priority: int = 5  # 1-10, 10 = maior prioridade

class GranularRateLimiter:
    """
    Rate Limiter Granular
    
    Características:
    - Rate limiting por endereço/IP
    - Rate limiting por tipo de operação
    - Rate limiting por valor da transação
    - Rate limiting combinado
    - Whitelist/Blacklist
    - Reputação
    """
    
    def __init__(self):
        # Histórico de requests
        self.request_history = defaultdict(lambda: deque(maxlen=1000))
        
        # Regras de rate limit
        self.rules: List[RateLimitRule] = []
        
        # Whitelist/Blacklist
        self.whitelist = set()
        self.blacklist = set()
        
        # Reputação (score 0-100)
        self.reputation = defaultdict(lambda: 50.0)
        
        # Estatísticas
        self.stats = {
            "total_requests": 0,
            "allowed": 0,
            "blocked": 0,
            "blocked_by_address": 0,
            "blocked_by_ip": 0,
            "blocked_by_operation": 0,
            "blocked_by_value": 0
        }
        
        # Configurar regras padrão
        self._setup_default_rules()
        
        print("🚦 Granular Rate Limiter: Inicializado!")
    
    def _setup_default_rules(self):
        """Configurar regras padrão"""
        # Rate limit por endereço
        self.add_rule(RateLimitRule(
            limit_type=RateLimitType.ADDRESS,
            identifier="*",  # Todos os endereços
            max_requests=100,
            window_seconds=60,
            priority=5
        ))
        
        # Rate limit por operação
        self.add_rule(RateLimitRule(
            limit_type=RateLimitType.OPERATION,
            identifier="cross_chain_transfer",
            max_requests=10,
            window_seconds=60,
            priority=8
        ))
        
        # Rate limit por valor (transações grandes)
        self.add_rule(RateLimitRule(
            limit_type=RateLimitType.VALUE,
            identifier="high_value",
            max_requests=5,
            window_seconds=300,
            priority=9
        ))
    
    def add_rule(self, rule: RateLimitRule):
        """Adicionar regra de rate limit"""
        self.rules.append(rule)
        # Ordenar por prioridade
        self.rules.sort(key=lambda r: r.priority, reverse=True)
    
    def check_rate_limit(
        self,
        address: Optional[str] = None,
        ip: Optional[str] = None,
        operation: Optional[str] = None,
        value: Optional[float] = None
    ) -> Tuple[bool, Optional[str]]:
        """
        Verificar rate limit
        
        Args:
            address: Endereço blockchain
            ip: Endereço IP
            operation: Tipo de operação
            value: Valor da transação
        
        Returns:
            (is_allowed, error_message)
        """
        self.stats["total_requests"] += 1
        
        # Verificar blacklist
        if address and address in self.blacklist:
            self.stats["blocked"] += 1
            return False, "Endereço está na blacklist"
        
        if ip and ip in self.blacklist:
            self.stats["blocked"] += 1
            return False, "IP está na blacklist"
        
        # Verificar whitelist (bypass rate limit)
        if address and address in self.whitelist:
            self.stats["allowed"] += 1
            return True, None
        
        if ip and ip in self.whitelist:
            self.stats["allowed"] += 1
            return True, None
        
        # Verificar regras de rate limit
        now = time.time()
        
        for rule in self.rules:
            identifier = None
            
            if rule.limit_type == RateLimitType.ADDRESS:
                identifier = address
            elif rule.limit_type == RateLimitType.IP:
                identifier = ip
            elif rule.limit_type == RateLimitType.OPERATION:
                identifier = operation
            elif rule.limit_type == RateLimitType.VALUE:
                if value and value > 10000:  # High value threshold
                    identifier = "high_value"
                else:
                    continue
            
            if identifier is None:
                continue
            
            # Verificar se regra se aplica
            if rule.identifier != "*" and rule.identifier != identifier:
                continue
            
            # Verificar histórico
            key = f"{rule.limit_type.value}:{identifier}"
            history = self.request_history[key]
            
            # Remover requests antigos
            cutoff_time = now - rule.window_seconds
            while history and history[0] < cutoff_time:
                history.popleft()
            
            # Verificar limite
            if len(history) >= rule.max_requests:
                # Bloquear
                self.stats["blocked"] += 1
                
                if rule.limit_type == RateLimitType.ADDRESS:
                    self.stats["blocked_by_address"] += 1
                elif rule.limit_type == RateLimitType.IP:
                    self.stats["blocked_by_ip"] += 1
                elif rule.limit_type == RateLimitType.OPERATION:
                    self.stats["blocked_by_operation"] += 1
                elif rule.limit_type == RateLimitType.VALUE:
                    self.stats["blocked_by_value"] += 1
                
                return False, f"Rate limit excedido: {rule.limit_type.value} ({len(history)}/{rule.max_requests})"
            
            # Registrar request
            history.append(now)
        
        # Permitir
        self.stats["allowed"] += 1
        return True, None
    
    def add_to_whitelist(self, identifier: str, limit_type: RateLimitType = RateLimitType.ADDRESS):
        """Adicionar à whitelist"""
        self.whitelist.add(f"{limit_type.value}:{identifier}")
    
    def add_to_blacklist(self, identifier: str, limit_type: RateLimitType = RateLimitType.ADDRESS):
        """Adicionar à blacklist"""
        self.blacklist.add(f"{limit_type.value}:{identifier}")
    
    def update_reputation(self, identifier: str, score_delta: float):
        """Atualizar reputação"""
        current_score = self.reputation[identifier]
        new_score = max(0, min(100, current_score + score_delta))
        self.reputation[identifier] = new_score
    
    def get_stats(self) -> Dict:
        """Obter estatísticas"""
        block_rate = 0.0
        if self.stats["total_requests"] > 0:
            block_rate = self.stats["blocked"] / self.stats["total_requests"]
        
        return {
            **self.stats,
            "block_rate": block_rate,
            "allow_rate": 1.0 - block_rate
        }

# Instância global
_global_granular_rate_limiter = None

def get_granular_rate_limiter() -> GranularRateLimiter:
    """Obter instância global do rate limiter"""
    global _global_granular_rate_limiter
    if _global_granular_rate_limiter is None:
        _global_granular_rate_limiter = GranularRateLimiter()
    return _global_granular_rate_limiter

if __name__ == '__main__':
    print("="*70)
    print("🚦 GRANULAR RATE LIMITER - TESTE")
    print("="*70)
    
    limiter = GranularRateLimiter()
    
    # Teste básico
    print("\n📝 Teste 1: Verificar rate limit")
    for i in range(15):
        allowed, error = limiter.check_rate_limit(
            address="0x1234...",
            operation="cross_chain_transfer"
        )
        if not allowed:
            print(f"   ⚠️  Bloqueado: {error}")
            break
    
    # Estatísticas
    print("\n📊 Estatísticas:")
    stats = limiter.get_stats()
    print(f"   Total requests: {stats['total_requests']}")
    print(f"   Block rate: {stats['block_rate']*100:.1f}%")





