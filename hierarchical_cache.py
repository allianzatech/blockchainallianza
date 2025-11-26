#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
💾 HIERARCHICAL CACHE SYSTEM - ALLIANZA BLOCKCHAIN
Cache hierárquico L1 (in-memory), L2 (Redis), L3 (Database)
"""

import json
import time
import hashlib
from typing import Optional, Any, Dict, List
from functools import wraps
from collections import OrderedDict
from datetime import datetime, timedelta

# Tentar importar Redis
try:
    import redis
    REDIS_AVAILABLE = True
except ImportError:
    REDIS_AVAILABLE = False

class HierarchicalCache:
    """
    Sistema de Cache Hierárquico
    
    L1: In-memory (ultra-rápido, < 1ms)
    L2: Redis (rápido, compartilhado, < 5ms)
    L3: Database (persistente, < 50ms)
    """
    
    def __init__(
        self,
        l1_max_size: int = 10000,
        l1_default_ttl: int = 60,
        redis_host: str = "localhost",
        redis_port: int = 6379,
        redis_db: int = 0,
        enable_l2: bool = True,
        enable_l3: bool = False
    ):
        # L1: In-memory cache (LRU)
        self.l1_cache = OrderedDict()
        self.l1_max_size = l1_max_size
        self.l1_default_ttl = l1_default_ttl
        self.l1_stats = {
            "hits": 0,
            "misses": 0,
            "sets": 0,
            "evictions": 0
        }
        
        # L2: Redis cache
        self.l2_enabled = enable_l2 and REDIS_AVAILABLE
        self.l2_client = None
        self.l2_stats = {
            "hits": 0,
            "misses": 0,
            "sets": 0,
            "errors": 0
        }
        
        if self.l2_enabled:
            try:
                self.l2_client = redis.Redis(
                    host=redis_host,
                    port=redis_port,
                    db=redis_db,
                    decode_responses=True,
                    socket_connect_timeout=2,
                    socket_timeout=2
                )
                self.l2_client.ping()
                print("✅ L2 Cache (Redis): Conectado!")
            except Exception as e:
                print(f"⚠️  L2 Cache (Redis): Não disponível - {e}")
                self.l2_enabled = False
        
        # L3: Database cache (opcional, para dados persistentes)
        self.l3_enabled = enable_l3
        self.l3_stats = {
            "hits": 0,
            "misses": 0,
            "sets": 0
        }
        
        print("💾 Hierarchical Cache: Inicializado!")
        print(f"   L1 (Memory): {l1_max_size} itens, TTL {l1_default_ttl}s")
        print(f"   L2 (Redis): {'✅' if self.l2_enabled else '❌'}")
        print(f"   L3 (Database): {'✅' if self.l3_enabled else '❌'}")
    
    def _calculate_adaptive_ttl(self, key: str, data_type: str = "default") -> int:
        """
        Calcular TTL adaptativo baseado no tipo de dado
        
        Dados que mudam pouco: TTL longo
        Dados que mudam muito: TTL curto
        """
        ttl_map = {
            "balance": 30,  # Saldos mudam frequentemente
            "gas_price": 10,  # Gas prices mudam muito
            "nonce": 5,  # Nonces mudam a cada transação
            "exchange_rate": 300,  # Exchange rates mudam pouco
            "block_number": 2,  # Block numbers mudam constantemente
            "transaction": 3600,  # Transações confirmadas não mudam
            "utxo": 60,  # UTXOs podem mudar
            "default": self.l1_default_ttl
        }
        
        # Detectar tipo pela chave
        key_lower = key.lower()
        for data_type_key, ttl in ttl_map.items():
            if data_type_key in key_lower:
                return ttl
        
        return ttl_map.get(data_type, self.l1_default_ttl)
    
    def get(self, key: str, default: Any = None) -> Optional[Any]:
        """Obter valor do cache (tenta L1, L2, L3)"""
        # Tentar L1 primeiro (mais rápido)
        if key in self.l1_cache:
            item = self.l1_cache[key]
            if time.time() < item["expires_at"]:
                # Hit em L1 - mover para o final (LRU)
                self.l1_cache.move_to_end(key)
                self.l1_stats["hits"] += 1
                return item["value"]
            else:
                # Expirou - remover
                del self.l1_cache[key]
        
        self.l1_stats["misses"] += 1
        
        # Tentar L2 (Redis)
        if self.l2_enabled and self.l2_client:
            try:
                value = self.l2_client.get(f"cache:{key}")
                if value:
                    data = json.loads(value)
                    # Promover para L1
                    self._set_l1(key, data["value"], data.get("ttl", self.l1_default_ttl))
                    self.l2_stats["hits"] += 1
                    return data["value"]
                self.l2_stats["misses"] += 1
            except Exception as e:
                self.l2_stats["errors"] += 1
                if self.l2_stats["errors"] % 100 == 0:
                    print(f"⚠️  L2 Cache error: {e}")
        
        # Tentar L3 (Database) - se habilitado
        if self.l3_enabled:
            # Implementar busca em database se necessário
            pass
        
        return default
    
    def set(self, key: str, value: Any, ttl: Optional[int] = None, data_type: str = "default"):
        """Armazenar valor no cache (L1, L2, L3)"""
        # Calcular TTL adaptativo se não fornecido
        if ttl is None:
            ttl = self._calculate_adaptive_ttl(key, data_type)
        
        # Armazenar em L1
        self._set_l1(key, value, ttl)
        
        # Armazenar em L2 (Redis)
        if self.l2_enabled and self.l2_client:
            try:
                cache_data = {
                    "value": value,
                    "ttl": ttl,
                    "timestamp": time.time()
                }
                self.l2_client.setex(
                    f"cache:{key}",
                    ttl,
                    json.dumps(cache_data)
                )
                self.l2_stats["sets"] += 1
            except Exception as e:
                self.l2_stats["errors"] += 1
                if self.l2_stats["errors"] % 100 == 0:
                    print(f"⚠️  L2 Cache set error: {e}")
        
        # Armazenar em L3 (Database) - se habilitado
        if self.l3_enabled:
            # Implementar armazenamento em database se necessário
            pass
    
    def _set_l1(self, key: str, value: Any, ttl: int):
        """Armazenar em L1 (in-memory) com LRU eviction"""
        expires_at = time.time() + ttl
        
        # Se já existe, atualizar
        if key in self.l1_cache:
            self.l1_cache[key] = {
                "value": value,
                "expires_at": expires_at
            }
            self.l1_cache.move_to_end(key)
        else:
            # Adicionar novo item
            self.l1_cache[key] = {
                "value": value,
                "expires_at": expires_at
            }
            
            # Se excedeu tamanho máximo, remover LRU
            if len(self.l1_cache) > self.l1_max_size:
                oldest_key = next(iter(self.l1_cache))
                del self.l1_cache[oldest_key]
                self.l1_stats["evictions"] += 1
        
        self.l1_stats["sets"] += 1
    
    def delete(self, key: str):
        """Remover do cache (L1, L2, L3)"""
        # Remover de L1
        if key in self.l1_cache:
            del self.l1_cache[key]
        
        # Remover de L2
        if self.l2_enabled and self.l2_client:
            try:
                self.l2_client.delete(f"cache:{key}")
            except:
                pass
        
        # Remover de L3 - se habilitado
        if self.l3_enabled:
            pass
    
    def clear(self, level: Optional[str] = None):
        """Limpar cache (todos os níveis ou nível específico)"""
        if level is None or level == "l1":
            self.l1_cache.clear()
            self.l1_stats = {"hits": 0, "misses": 0, "sets": 0, "evictions": 0}
        
        if (level is None or level == "l2") and self.l2_enabled and self.l2_client:
            try:
                # Limpar todas as chaves de cache
                keys = self.l2_client.keys("cache:*")
                if keys:
                    self.l2_client.delete(*keys)
            except:
                pass
        
        if level is None or level == "l3":
            # Limpar L3 se habilitado
            pass
    
    def get_stats(self) -> Dict:
        """Obter estatísticas do cache"""
        l1_hit_rate = 0.0
        if self.l1_stats["hits"] + self.l1_stats["misses"] > 0:
            l1_hit_rate = self.l1_stats["hits"] / (self.l1_stats["hits"] + self.l1_stats["misses"])
        
        l2_hit_rate = 0.0
        if self.l2_stats["hits"] + self.l2_stats["misses"] > 0:
            l2_hit_rate = self.l2_stats["hits"] / (self.l2_stats["hits"] + self.l2_stats["misses"])
        
        return {
            "l1": {
                **self.l1_stats,
                "size": len(self.l1_cache),
                "max_size": self.l1_max_size,
                "hit_rate": l1_hit_rate
            },
            "l2": {
                **self.l2_stats,
                "enabled": self.l2_enabled,
                "hit_rate": l2_hit_rate
            },
            "l3": {
                **self.l3_stats,
                "enabled": self.l3_enabled
            }
        }
    
    def prefetch(self, keys: List[str], fetch_func: callable):
        """
        Prefetch inteligente de múltiplas chaves
        
        Args:
            keys: Lista de chaves para prefetch
            fetch_func: Função para buscar dados (recebe lista de keys, retorna dict)
        """
        # Identificar chaves que não estão no cache
        missing_keys = [key for key in keys if key not in self.l1_cache]
        
        if not missing_keys:
            return  # Todas já estão no cache
        
        # Buscar dados faltantes
        try:
            fetched_data = fetch_func(missing_keys)
            
            # Armazenar no cache
            for key, value in fetched_data.items():
                if value is not None:
                    self.set(key, value)
        except Exception as e:
            print(f"⚠️  Erro no prefetch: {e}")

# Instância global
_global_hierarchical_cache = None

def get_hierarchical_cache() -> HierarchicalCache:
    """Obter instância global do cache hierárquico"""
    global _global_hierarchical_cache
    if _global_hierarchical_cache is None:
        _global_hierarchical_cache = HierarchicalCache()
    return _global_hierarchical_cache

def cached_hierarchical(ttl: Optional[int] = None, data_type: str = "default"):
    """
    Decorator para cachear resultados usando cache hierárquico
    
    Args:
        ttl: Time to live em segundos (None = adaptativo)
        data_type: Tipo de dado para TTL adaptativo
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            cache = get_hierarchical_cache()
            
            # Criar chave do cache
            cache_key = f"{func.__name__}_{hashlib.sha256(str(args).encode() + str(kwargs).encode()).hexdigest()[:16]}"
            
            # Tentar buscar do cache
            cached_result = cache.get(cache_key)
            if cached_result is not None:
                return cached_result
            
            # Executar função
            result = func(*args, **kwargs)
            
            # Armazenar no cache
            cache.set(cache_key, result, ttl=ttl, data_type=data_type)
            
            return result
        return wrapper
    return decorator

if __name__ == '__main__':
    print("="*70)
    print("💾 HIERARCHICAL CACHE - TESTE")
    print("="*70)
    
    cache = HierarchicalCache()
    
    # Teste básico
    print("\n📝 Teste 1: Set e Get")
    cache.set("test_key", {"data": "test"}, ttl=60)
    result = cache.get("test_key")
    print(f"   ✅ Resultado: {result}")
    
    # Teste de TTL adaptativo
    print("\n📝 Teste 2: TTL Adaptativo")
    cache.set("balance_0x123", 100.0, data_type="balance")
    cache.set("gas_price_polygon", 30.0, data_type="gas_price")
    cache.set("exchange_rate_BTC", 50000.0, data_type="exchange_rate")
    
    # Estatísticas
    print("\n📊 Estatísticas:")
    stats = cache.get_stats()
    print(json.dumps(stats, indent=2, ensure_ascii=False))



