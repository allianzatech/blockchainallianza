#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔮 INTELLIGENT PREFETCH - ALLIANZA BLOCKCHAIN
Prefetching inteligente de dados prováveis
"""

import time
from typing import Dict, List, Optional, Callable, Set
from collections import defaultdict, deque
from dataclasses import dataclass
from datetime import datetime, timedelta

@dataclass
class PrefetchPattern:
    """Padrão de prefetch"""
    trigger: str  # Evento que dispara prefetch
    keys_to_prefetch: List[str]  # Chaves para prefetch
    fetch_func: Callable  # Função para buscar dados
    priority: int = 5  # Prioridade (1-10)

class IntelligentPrefetch:
    """
    Sistema de Prefetch Inteligente
    
    Características:
    - Aprende padrões de uso
    - Prefetch baseado em contexto
    - Prefetch paralelo
    - Cache de padrões
    """
    
    def __init__(self, cache=None):
        self.cache = cache
        
        # Padrões de prefetch
        self.patterns: Dict[str, PrefetchPattern] = {}
        
        # Histórico de uso (para aprender padrões)
        self.usage_history = defaultdict(lambda: deque(maxlen=100))
        
        # Estatísticas
        self.stats = {
            "prefetches": 0,
            "hits": 0,
            "misses": 0,
            "time_saved": 0.0
        }
        
        print("🔮 Intelligent Prefetch: Inicializado!")
    
    def register_pattern(
        self,
        pattern_id: str,
        trigger: str,
        keys_to_prefetch: List[str],
        fetch_func: Callable,
        priority: int = 5
    ):
        """Registrar padrão de prefetch"""
        pattern = PrefetchPattern(
            trigger=trigger,
            keys_to_prefetch=keys_to_prefetch,
            fetch_func=fetch_func,
            priority=priority
        )
        self.patterns[pattern_id] = pattern
        print(f"   ✅ Padrão registrado: {pattern_id}")
    
    def on_event(self, event: str, context: Dict = None):
        """
        Disparar prefetch baseado em evento
        
        Args:
            event: Tipo de evento (ex: "cross_chain_transfer", "balance_check")
            context: Contexto do evento (ex: {"from_chain": "polygon", "to_chain": "bitcoin"})
        """
        context = context or {}
        
        # Encontrar padrões que correspondem ao evento
        matching_patterns = []
        for pattern_id, pattern in self.patterns.items():
            if pattern.trigger == event or event.startswith(pattern.trigger):
                matching_patterns.append((pattern.priority, pattern))
        
        # Ordenar por prioridade
        matching_patterns.sort(key=lambda x: x[0], reverse=True)
        
        # Executar prefetch para cada padrão
        for priority, pattern in matching_patterns:
            self._execute_prefetch(pattern, context)
    
    def _execute_prefetch(self, pattern: PrefetchPattern, context: Dict):
        """Executar prefetch para um padrão"""
        try:
            # Gerar chaves baseadas no contexto
            keys_to_fetch = []
            for key_template in pattern.keys_to_prefetch:
                # Substituir placeholders no template
                key = key_template
                for placeholder, value in context.items():
                    key = key.replace(f"{{{placeholder}}}", str(value))
                keys_to_fetch.append(key)
            
            # Verificar quais chaves não estão no cache
            if self.cache:
                missing_keys = []
                for key in keys_to_fetch:
                    if self.cache.get(key) is None:
                        missing_keys.append(key)
                
                if not missing_keys:
                    self.stats["hits"] += 1
                    return  # Todas já estão no cache
            else:
                missing_keys = keys_to_fetch
            
            # Executar fetch
            start_time = time.time()
            try:
                fetched_data = pattern.fetch_func(missing_keys, context)
                
                # Armazenar no cache
                if self.cache and fetched_data:
                    for key, value in fetched_data.items():
                        if value is not None:
                            self.cache.set(key, value)
                
                elapsed = time.time() - start_time
                self.stats["prefetches"] += 1
                self.stats["time_saved"] += elapsed
                
            except Exception as e:
                print(f"⚠️  Erro no prefetch: {e}")
                self.stats["misses"] += 1
                
        except Exception as e:
            print(f"⚠️  Erro ao executar prefetch: {e}")
    
    def learn_from_usage(self, event: str, keys_accessed: List[str]):
        """Aprender padrões de uso"""
        # Registrar no histórico
        self.usage_history[event].extend(keys_accessed)
        
        # Analisar padrões (simplificado)
        # Em produção, usar ML para detectar padrões
    
    def get_stats(self) -> Dict:
        """Obter estatísticas"""
        avg_time_saved = 0.0
        if self.stats["prefetches"] > 0:
            avg_time_saved = self.stats["time_saved"] / self.stats["prefetches"]
        
        hit_rate = 0.0
        total_attempts = self.stats["hits"] + self.stats["misses"]
        if total_attempts > 0:
            hit_rate = self.stats["hits"] / total_attempts
        
        return {
            **self.stats,
            "avg_time_saved": avg_time_saved,
            "hit_rate": hit_rate,
            "patterns_registered": len(self.patterns)
        }

# Instância global
_global_prefetch = None

def get_intelligent_prefetch(cache=None) -> IntelligentPrefetch:
    """Obter instância global do prefetch"""
    global _global_prefetch
    if _global_prefetch is None:
        _global_prefetch = IntelligentPrefetch(cache=cache)
    return _global_prefetch

if __name__ == '__main__':
    print("="*70)
    print("🔮 INTELLIGENT PREFETCH - TESTE")
    print("="*70)
    
    from hierarchical_cache import HierarchicalCache
    
    cache = HierarchicalCache()
    prefetch = IntelligentPrefetch(cache=cache)
    
    # Registrar padrão
    def fetch_balance_data(keys, context):
        return {key: 100.0 for key in keys}
    
    prefetch.register_pattern(
        pattern_id="cross_chain_balance",
        trigger="cross_chain_transfer",
        keys_to_prefetch=["balance_{from_chain}", "balance_{to_chain}"],
        fetch_func=fetch_balance_data
    )
    
    # Disparar prefetch
    prefetch.on_event("cross_chain_transfer", {
        "from_chain": "polygon",
        "to_chain": "bitcoin"
    })
    
    # Estatísticas
    print("\n📊 Estatísticas:")
    stats = prefetch.get_stats()
    print(f"   Prefetches: {stats['prefetches']}")
    print(f"   Hit rate: {stats['hit_rate']*100:.1f}%")

