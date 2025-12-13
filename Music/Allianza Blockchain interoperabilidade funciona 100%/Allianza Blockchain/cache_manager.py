#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sistema de Cache com Redis
Cache de dados frequentes para melhorar performance
"""

import json
import time
from typing import Optional, Any, Dict
from functools import wraps

# Tentar importar Redis, mas funcionar sem ele
try:
    import redis
    REDIS_AVAILABLE = True
except ImportError:
    REDIS_AVAILABLE = False
    print("⚠️  Redis não disponível. Usando cache em memória.")

class CacheManager:
    """Gerenciador de cache com fallback para memória"""
    
    def __init__(self, redis_host: str = "localhost", redis_port: int = 6379, redis_db: int = 0):
        self.redis_client = None
        self.memory_cache = {}  # Fallback
        self.use_redis = False
        
        if REDIS_AVAILABLE:
            try:
                self.redis_client = redis.Redis(
                    host=redis_host,
                    port=redis_port,
                    db=redis_db,
                    decode_responses=True,
                    socket_connect_timeout=5
                )
                # Testar conexão
                self.redis_client.ping()
                self.use_redis = True
                print("✅ Redis conectado!")
            except Exception as e:
                print(f"⚠️  Redis não disponível: {e}. Usando cache em memória.")
                self.use_redis = False
    
    def get(self, key: str) -> Optional[Any]:
        """Obtém valor do cache"""
        if self.use_redis and self.redis_client:
            try:
                value = self.redis_client.get(key)
                if value:
                    return json.loads(value)
            except Exception:
                pass
        
        # Fallback para memória
        if key in self.memory_cache:
            data, expiry = self.memory_cache[key]
            if expiry is None or time.time() < expiry:
                return data
            else:
                del self.memory_cache[key]
        
        return None
    
    def set(self, key: str, value: Any, ttl: Optional[int] = None):
        """Define valor no cache"""
        if self.use_redis and self.redis_client:
            try:
                json_value = json.dumps(value)
                if ttl:
                    self.redis_client.setex(key, ttl, json_value)
                else:
                    self.redis_client.set(key, json_value)
                return
            except Exception:
                pass
        
        # Fallback para memória
        expiry = None
        if ttl:
            expiry = time.time() + ttl
        
        self.memory_cache[key] = (value, expiry)
        
        # Limpar cache expirado periodicamente
        if len(self.memory_cache) > 10000:
            self._clean_expired()
    
    def delete(self, key: str):
        """Remove valor do cache"""
        if self.use_redis and self.redis_client:
            try:
                self.redis_client.delete(key)
            except Exception:
                pass
        
        if key in self.memory_cache:
            del self.memory_cache[key]
    
    def clear(self):
        """Limpa todo o cache"""
        if self.use_redis and self.redis_client:
            try:
                self.redis_client.flushdb()
            except Exception:
                pass
        
        self.memory_cache.clear()
    
    def _clean_expired(self):
        """Remove entradas expiradas do cache em memória"""
        current_time = time.time()
        expired_keys = [
            key for key, (_, expiry) in self.memory_cache.items()
            if expiry and current_time >= expiry
        ]
        for key in expired_keys:
            del self.memory_cache[key]
    
    def get_stats(self) -> Dict:
        """Retorna estatísticas do cache"""
        if self.use_redis and self.redis_client:
            try:
                info = self.redis_client.info()
                return {
                    "type": "redis",
                    "keys": info.get("db0", {}).get("keys", 0),
                    "memory_used": info.get("used_memory_human", "N/A")
                }
            except Exception:
                pass
        
        return {
            "type": "memory",
            "keys": len(self.memory_cache),
            "memory_used": "N/A"
        }

def cached(ttl: int = 300, key_prefix: str = ""):
    """
    Decorator para cachear resultado de função
    
    Usage:
        @cached(ttl=600, key_prefix="balance")
        def get_balance(address):
            ...
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Criar chave de cache
            cache_key = f"{key_prefix}:{func.__name__}:{str(args)}:{str(kwargs)}"
            
            # Tentar obter do cache
            cache = CacheManager()
            cached_value = cache.get(cache_key)
            if cached_value is not None:
                return cached_value
            
            # Executar função e cachear resultado
            result = func(*args, **kwargs)
            cache.set(cache_key, result, ttl)
            
            return result
        return wrapper
    return decorator

# Instância global
global_cache = CacheManager()




















