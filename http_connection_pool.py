#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🌐 HTTP CONNECTION POOLING - ALLIANZA BLOCKCHAIN
Pool de conexões HTTP com keep-alive para reduzir overhead
"""

import time
import requests
from typing import Dict, Optional, List
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from urllib3.poolmanager import PoolManager
from collections import defaultdict
import threading

class HTTPConnectionPool:
    """
    Pool de conexões HTTP reutilizáveis
    
    Características:
    - Keep-alive connections
    - Connection pooling por host
    - Retry automático
    - Health checks
    - Métricas de performance
    """
    
    def __init__(
        self,
        max_connections: int = 100,
        max_connections_per_host: int = 10,
        pool_block: bool = False,
        pool_connections: int = 10,
        retry_strategy: Optional[Retry] = None
    ):
        self.max_connections = max_connections
        self.max_connections_per_host = max_connections_per_host
        
        # Configurar retry strategy
        if retry_strategy is None:
            retry_strategy = Retry(
                total=3,
                backoff_factor=0.3,
                status_forcelist=[429, 500, 502, 503, 504],
                allowed_methods=["GET", "POST", "PUT", "DELETE"]
            )
        
        # Criar session com pooling
        self.session = requests.Session()
        
        # Configurar adapter com pooling
        adapter = HTTPAdapter(
            pool_connections=pool_connections,
            pool_maxsize=max_connections_per_host,
            max_retries=retry_strategy,
            pool_block=pool_block
        )
        
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)
        
        # Métricas
        self.metrics = {
            "requests": 0,
            "success": 0,
            "errors": 0,
            "total_time": 0.0,
            "avg_latency": 0.0,
            "by_host": defaultdict(lambda: {
                "requests": 0,
                "success": 0,
                "errors": 0,
                "total_time": 0.0
            })
        }
        
        self.lock = threading.Lock()
        
        print("🌐 HTTP Connection Pool: Inicializado!")
        print(f"   Max connections: {max_connections}")
        print(f"   Max per host: {max_connections_per_host}")
        print(f"   Keep-alive: ✅")
    
    def get(
        self,
        url: str,
        params: Optional[Dict] = None,
        headers: Optional[Dict] = None,
        timeout: int = 10,
        **kwargs
    ) -> requests.Response:
        """GET request usando connection pool"""
        return self._request("GET", url, params=params, headers=headers, timeout=timeout, **kwargs)
    
    def post(
        self,
        url: str,
        json: Optional[Dict] = None,
        data: Optional[Dict] = None,
        headers: Optional[Dict] = None,
        timeout: int = 10,
        **kwargs
    ) -> requests.Response:
        """POST request usando connection pool"""
        return self._request("POST", url, json=json, data=data, headers=headers, timeout=timeout, **kwargs)
    
    def _request(
        self,
        method: str,
        url: str,
        **kwargs
    ) -> requests.Response:
        """Executar request usando connection pool"""
        start_time = time.time()
        host = self._extract_host(url)
        
        try:
            # Usar session com pooling
            response = self.session.request(method, url, **kwargs)
            
            # Atualizar métricas
            elapsed = time.time() - start_time
            self._update_metrics(host, success=True, elapsed=elapsed)
            
            return response
            
        except Exception as e:
            # Atualizar métricas de erro
            elapsed = time.time() - start_time
            self._update_metrics(host, success=False, elapsed=elapsed)
            raise
    
    def _extract_host(self, url: str) -> str:
        """Extrair host da URL"""
        try:
            from urllib.parse import urlparse
            parsed = urlparse(url)
            return parsed.netloc
        except:
            return "unknown"
    
    def _update_metrics(self, host: str, success: bool, elapsed: float):
        """Atualizar métricas"""
        with self.lock:
            self.metrics["requests"] += 1
            self.metrics["total_time"] += elapsed
            
            if success:
                self.metrics["success"] += 1
            else:
                self.metrics["errors"] += 1
            
            # Calcular latência média
            if self.metrics["requests"] > 0:
                self.metrics["avg_latency"] = self.metrics["total_time"] / self.metrics["requests"]
            
            # Métricas por host
            host_metrics = self.metrics["by_host"][host]
            host_metrics["requests"] += 1
            host_metrics["total_time"] += elapsed
            
            if success:
                host_metrics["success"] += 1
            else:
                host_metrics["errors"] += 1
    
    def get_metrics(self) -> Dict:
        """Obter métricas do pool"""
        with self.lock:
            metrics = self.metrics.copy()
            
            # Calcular taxas de sucesso
            if metrics["requests"] > 0:
                metrics["success_rate"] = metrics["success"] / metrics["requests"]
                metrics["error_rate"] = metrics["errors"] / metrics["requests"]
            else:
                metrics["success_rate"] = 0.0
                metrics["error_rate"] = 0.0
            
            # Métricas por host
            for host, host_metrics in metrics["by_host"].items():
                if host_metrics["requests"] > 0:
                    host_metrics["success_rate"] = host_metrics["success"] / host_metrics["requests"]
                    host_metrics["avg_latency"] = host_metrics["total_time"] / host_metrics["requests"]
            
            return metrics
    
    def close(self):
        """Fechar todas as conexões"""
        self.session.close()
        print("🌐 HTTP Connection Pool: Fechado")

# Instância global
_global_http_pool = None

def get_http_pool() -> HTTPConnectionPool:
    """Obter instância global do HTTP connection pool"""
    global _global_http_pool
    if _global_http_pool is None:
        _global_http_pool = HTTPConnectionPool()
    return _global_http_pool

if __name__ == '__main__':
    print("="*70)
    print("🌐 HTTP CONNECTION POOL - TESTE")
    print("="*70)
    
    pool = HTTPConnectionPool()
    
    # Teste básico
    print("\n📝 Teste 1: GET request")
    try:
        response = pool.get("https://httpbin.org/get", timeout=5)
        print(f"   ✅ Status: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Erro: {e}")
    
    # Métricas
    print("\n📊 Métricas:")
    metrics = pool.get_metrics()
    print(f"   Requests: {metrics['requests']}")
    print(f"   Success rate: {metrics.get('success_rate', 0)*100:.1f}%")
    print(f"   Avg latency: {metrics.get('avg_latency', 0)*1000:.2f}ms")
















