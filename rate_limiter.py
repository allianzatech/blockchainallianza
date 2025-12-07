#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sistema de Rate Limiting Robusto
Proteção contra DDoS e abuso
"""

import time
from typing import Dict, Optional
from collections import defaultdict
from threading import Lock

class RateLimiter:
    """Rate limiter com múltiplas estratégias"""
    
    def __init__(self):
        self.requests = defaultdict(list)  # IP/address -> [timestamps]
        self.locks = defaultdict(Lock)  # Lock por IP/address
        self.config = {
            "requests_per_minute": 60,
            "requests_per_hour": 1000,
            "requests_per_day": 10000,
            "burst_size": 10,
            "burst_window": 1  # segundos
        }
    
    def is_allowed(
        self,
        identifier: str,
        custom_limits: Optional[Dict] = None
    ) -> tuple[bool, Optional[str]]:
        """
        Verifica se requisição é permitida
        
        Returns:
            (is_allowed, error_message)
        """
        limits = custom_limits or self.config
        current_time = time.time()
        
        with self.locks[identifier]:
            # Limpar requisições antigas
            self._clean_old_requests(identifier, current_time)
            
            # Verificar limites
            requests = self.requests[identifier]
            
            # Limite por minuto
            recent_minute = [r for r in requests if current_time - r < 60]
            if len(recent_minute) >= limits["requests_per_minute"]:
                return False, f"Rate limit excedido: {limits['requests_per_minute']} requisições por minuto"
            
            # Limite por hora
            recent_hour = [r for r in requests if current_time - r < 3600]
            if len(recent_hour) >= limits["requests_per_hour"]:
                return False, f"Rate limit excedido: {limits['requests_per_hour']} requisições por hora"
            
            # Limite por dia
            recent_day = [r for r in requests if current_time - r < 86400]
            if len(recent_day) >= limits["requests_per_day"]:
                return False, f"Rate limit excedido: {limits['requests_per_day']} requisições por dia"
            
            # Verificar burst (muitas requisições em pouco tempo)
            recent_burst = [r for r in requests if current_time - r < limits["burst_window"]]
            if len(recent_burst) >= limits["burst_size"]:
                return False, f"Burst limit excedido: {limits['burst_size']} requisições em {limits['burst_window']}s"
            
            # Adicionar requisição atual
            requests.append(current_time)
            
            return True, None
    
    def _clean_old_requests(self, identifier: str, current_time: float):
        """Remove requisições antigas (mais de 24 horas)"""
        self.requests[identifier] = [
            r for r in self.requests[identifier]
            if current_time - r < 86400
        ]
    
    def get_stats(self, identifier: str) -> Dict:
        """Retorna estatísticas de rate limiting para um identificador"""
        current_time = time.time()
        
        with self.locks[identifier]:
            requests = self.requests[identifier]
            
            return {
                "total_requests_24h": len([r for r in requests if current_time - r < 86400]),
                "requests_last_hour": len([r for r in requests if current_time - r < 3600]),
                "requests_last_minute": len([r for r in requests if current_time - r < 60]),
                "limit_per_minute": self.config["requests_per_minute"],
                "limit_per_hour": self.config["requests_per_hour"],
                "limit_per_day": self.config["requests_per_day"]
            }

# Instância global
global_rate_limiter = RateLimiter()




















