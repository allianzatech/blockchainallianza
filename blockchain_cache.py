# blockchain_cache.py
# 💾 CACHE REDIS PARA BLOCKCHAIN
# Cache agressivo para dados frequentes

import json
import time
from typing import Optional, Dict, Any
from functools import wraps

# Tentar importar Redis
try:
    import redis
    REDIS_AVAILABLE = True
except ImportError:
    REDIS_AVAILABLE = False
    print("⚠️  Redis não disponível - usando cache em memória")

class BlockchainCache:
    """
    Sistema de Cache para Blockchain
    Usa Redis se disponível, senão cache em memória
    """
    
    def __init__(self, use_redis: bool = True):
        self.use_redis = use_redis and REDIS_AVAILABLE
        self.memory_cache = {}  # Fallback para cache em memória
        
        if self.use_redis:
            try:
                self.redis_client = redis.Redis(
                    host=os.getenv('REDIS_HOST', 'localhost'),
                    port=int(os.getenv('REDIS_PORT', 6379)),
                    db=0,
                    decode_responses=True,
                    socket_connect_timeout=2
                )
                # Testar conexão
                self.redis_client.ping()
                print("✅ Redis conectado - Cache ativo")
            except Exception as e:
                print(f"⚠️  Redis não disponível: {e} - usando cache em memória")
                self.use_redis = False
                self.redis_client = None
        else:
            self.redis_client = None
            print("💾 Cache em memória ativo")
    
    def get(self, key: str, default: Any = None) -> Any:
        """Buscar valor do cache"""
        try:
            if self.use_redis and self.redis_client:
                value = self.redis_client.get(key)
                if value:
                    return json.loads(value)
            else:
                if key in self.memory_cache:
                    cached = self.memory_cache[key]
                    # Verificar TTL
                    if cached.get("expires_at", 0) > time.time():
                        return cached["value"]
                    else:
                        del self.memory_cache[key]
        except Exception as e:
            print(f"Erro ao buscar cache: {e}")
        
        return default
    
    def set(self, key: str, value: Any, ttl: int = 60) -> bool:
        """Armazenar valor no cache"""
        try:
            if self.use_redis and self.redis_client:
                self.redis_client.setex(
                    key,
                    ttl,
                    json.dumps(value)
                )
            else:
                self.memory_cache[key] = {
                    "value": value,
                    "expires_at": time.time() + ttl
                }
                # Limitar tamanho do cache (LRU)
                if len(self.memory_cache) > 1000:
                    oldest = min(
                        self.memory_cache.keys(),
                        key=lambda k: self.memory_cache[k].get("expires_at", 0)
                    )
                    del self.memory_cache[oldest]
            return True
        except Exception as e:
            print(f"Erro ao armazenar cache: {e}")
            return False
    
    def delete(self, key: str) -> bool:
        """Remover valor do cache"""
        try:
            if self.use_redis and self.redis_client:
                self.redis_client.delete(key)
            else:
                if key in self.memory_cache:
                    del self.memory_cache[key]
            return True
        except Exception as e:
            print(f"Erro ao deletar cache: {e}")
            return False
    
    def clear(self):
        """Limpar todo o cache"""
        try:
            if self.use_redis and self.redis_client:
                self.redis_client.flushdb()
            else:
                self.memory_cache.clear()
        except Exception as e:
            print(f"Erro ao limpar cache: {e}")

# Instância global
_global_cache = None

def get_cache() -> BlockchainCache:
    """Obter instância global do cache"""
    global _global_cache
    if _global_cache is None:
        _global_cache = BlockchainCache()
    return _global_cache

def cached(ttl: int = 60):
    """
    Decorator para cachear resultados de funções
    
    Args:
        ttl: Time to live em segundos
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            cache = get_cache()
            
            # Criar chave do cache baseada em args e kwargs
            cache_key = f"{func.__name__}_{hash(str(args) + str(kwargs))}"
            
            # Tentar buscar do cache
            cached_result = cache.get(cache_key)
            if cached_result is not None:
                return cached_result
            
            # Executar função
            result = func(*args, **kwargs)
            
            # Armazenar no cache
            cache.set(cache_key, result, ttl)
            
            return result
        return wrapper
    return decorator

# Importar os para usar em getenv
import os

