#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔌 CIRCUIT BREAKER PATTERN
Protege contra falhas repetidas de APIs e serviços externos
"""

import time
from typing import Dict, Optional, Callable
from enum import Enum
from dataclasses import dataclass
from datetime import datetime, timedelta

class CircuitState(Enum):
    """Estados do circuit breaker"""
    CLOSED = "closed"      # Normal, permitindo requisições
    OPEN = "open"          # Bloqueando requisições (muitas falhas)
    HALF_OPEN = "half_open"  # Testando se serviço recuperou

@dataclass
class CircuitBreakerConfig:
    """Configuração do circuit breaker"""
    failure_threshold: int = 5  # Número de falhas para abrir circuito
    success_threshold: int = 2  # Número de sucessos para fechar (half-open)
    timeout_seconds: int = 60  # Tempo antes de tentar reabrir
    timeout_window: int = 300  # Janela de tempo para contar falhas (5 min)

class CircuitBreaker:
    """Circuit Breaker para proteger contra falhas repetidas"""
    
    def __init__(self, name: str, config: Optional[CircuitBreakerConfig] = None):
        self.name = name
        self.config = config or CircuitBreakerConfig()
        
        self.state = CircuitState.CLOSED
        self.failure_count = 0
        self.success_count = 0
        self.last_failure_time = None
        self.last_success_time = None
        self.opened_at = None
        
        # Histórico de falhas (para janela de tempo)
        self.failure_history = []  # Lista de timestamps de falhas
    
    def call(self, func: Callable, *args, **kwargs) -> Dict:
        """
        Executar função protegida pelo circuit breaker
        
        Returns:
            {
                "success": bool,
                "result": Any,
                "error": str,
                "circuit_state": str
            }
        """
        # Verificar se circuito está aberto
        if self.state == CircuitState.OPEN:
            # Verificar se timeout expirou
            if self.opened_at and (time.time() - self.opened_at) >= self.config.timeout_seconds:
                # Tentar reabrir (half-open)
                self.state = CircuitState.HALF_OPEN
                self.success_count = 0
                print(f"🔄 Circuit Breaker '{self.name}': Tentando reabrir (half-open)")
            else:
                # Circuito ainda aberto, rejeitar imediatamente
                return {
                    "success": False,
                    "error": f"Circuit breaker '{self.name}' is OPEN. Service unavailable.",
                    "circuit_state": self.state.value,
                    "retry_after": self.config.timeout_seconds - (time.time() - self.opened_at) if self.opened_at else self.config.timeout_seconds
                }
        
        # Executar função
        try:
            result = func(*args, **kwargs)
            
            # Sucesso!
            self._record_success()
            
            return {
                "success": True,
                "result": result,
                "circuit_state": self.state.value
            }
            
        except Exception as e:
            # Falha!
            self._record_failure()
            
            return {
                "success": False,
                "error": str(e),
                "circuit_state": self.state.value,
                "failure_count": self.failure_count
            }
    
    def _record_success(self):
        """Registrar sucesso"""
        self.last_success_time = time.time()
        
        if self.state == CircuitState.HALF_OPEN:
            self.success_count += 1
            if self.success_count >= self.config.success_threshold:
                # Fechar circuito (serviço recuperou)
                self.state = CircuitState.CLOSED
                self.failure_count = 0
                self.success_count = 0
                self.opened_at = None
                print(f"✅ Circuit Breaker '{self.name}': Fechado (serviço recuperou)")
        elif self.state == CircuitState.CLOSED:
            # Resetar contador de falhas se teve sucesso recente
            if self.failure_count > 0:
                self.failure_count = max(0, self.failure_count - 1)
    
    def _record_failure(self):
        """Registrar falha"""
        self.last_failure_time = time.time()
        self.failure_count += 1
        
        # Adicionar ao histórico (com janela de tempo)
        now = time.time()
        self.failure_history.append(now)
        
        # Remover falhas antigas (fora da janela)
        cutoff = now - self.config.timeout_window
        self.failure_history = [f for f in self.failure_history if f > cutoff]
        
        # Contar falhas na janela
        failures_in_window = len(self.failure_history)
        
        if self.state == CircuitState.HALF_OPEN:
            # Se falhar em half-open, abrir novamente
            self.state = CircuitState.OPEN
            self.opened_at = time.time()
            self.success_count = 0
            print(f"❌ Circuit Breaker '{self.name}': Aberto novamente (falhou em half-open)")
        elif self.state == CircuitState.CLOSED:
            # Verificar se deve abrir circuito
            if failures_in_window >= self.config.failure_threshold:
                self.state = CircuitState.OPEN
                self.opened_at = time.time()
                print(f"🔴 Circuit Breaker '{self.name}': ABERTO ({failures_in_window} falhas em {self.config.timeout_window}s)")
    
    def get_status(self) -> Dict:
        """Obter status do circuit breaker"""
        return {
            "name": self.name,
            "state": self.state.value,
            "failure_count": self.failure_count,
            "success_count": self.success_count,
            "failures_in_window": len(self.failure_history),
            "last_failure": datetime.fromtimestamp(self.last_failure_time).isoformat() if self.last_failure_time else None,
            "last_success": datetime.fromtimestamp(self.last_success_time).isoformat() if self.last_success_time else None,
            "opened_at": datetime.fromtimestamp(self.opened_at).isoformat() if self.opened_at else None,
            "time_until_retry": max(0, self.config.timeout_seconds - (time.time() - self.opened_at)) if self.opened_at and self.state == CircuitState.OPEN else None
        }
    
    def reset(self):
        """Resetar circuit breaker manualmente"""
        self.state = CircuitState.CLOSED
        self.failure_count = 0
        self.success_count = 0
        self.failure_history = []
        self.opened_at = None
        print(f"🔄 Circuit Breaker '{self.name}': Resetado manualmente")

class CircuitBreakerManager:
    """Gerenciador de múltiplos circuit breakers"""
    
    def __init__(self):
        self.breakers = {}  # name -> CircuitBreaker
    
    def get_breaker(self, name: str, config: Optional[CircuitBreakerConfig] = None) -> CircuitBreaker:
        """Obter ou criar circuit breaker"""
        if name not in self.breakers:
            self.breakers[name] = CircuitBreaker(name, config)
        return self.breakers[name]
    
    def get_all_status(self) -> Dict:
        """Obter status de todos os circuit breakers"""
        return {
            name: breaker.get_status()
            for name, breaker in self.breakers.items()
        }
    
    def reset_all(self):
        """Resetar todos os circuit breakers"""
        for breaker in self.breakers.values():
            breaker.reset()

# Instância global
global_circuit_breaker_manager = CircuitBreakerManager()







