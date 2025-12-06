#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
💾 DATABASE OPTIMIZER - ALLIANZA BLOCKCHAIN
Otimizações de database (índices, connection pooling, batch operations)
"""

import sqlite3
import time
from typing import Dict, List, Optional, Any, Tuple
from contextlib import contextmanager
from threading import local
import threading

# Tentar importar bibliotecas de database
try:
    import psycopg2
    from psycopg2 import pool
    POSTGRES_AVAILABLE = True
except ImportError:
    POSTGRES_AVAILABLE = False

class DatabaseOptimizer:
    """
    Otimizador de Database
    
    Características:
    - Connection pooling
    - Índices otimizados
    - Batch operations
    - Query optimization
    """
    
    def __init__(
        self,
        db_path: str = "allianza_blockchain.db",
        use_pooling: bool = True,
        pool_size: int = 10
    ):
        self.db_path = db_path
        self.use_pooling = use_pooling
        self.pool_size = pool_size
        
        # Connection pool (thread-local)
        self.thread_local = local()
        self.pool = None
        
        # Estatísticas
        self.stats = {
            "queries": 0,
            "batch_queries": 0,
            "avg_query_time": 0.0,
            "pool_hits": 0,
            "pool_misses": 0
        }
        
        # Criar índices se necessário
        self._create_indexes()
        
        print("💾 Database Optimizer: Inicializado!")
        print(f"   Connection pooling: {'✅' if use_pooling else '❌'}")
        print(f"   Pool size: {pool_size}")
    
    def _get_connection(self):
        """Obter conexão do pool (thread-local)"""
        if not hasattr(self.thread_local, 'connection'):
            self.thread_local.connection = sqlite3.connect(
                self.db_path,
                check_same_thread=False,
                timeout=10.0
            )
            self.thread_local.connection.row_factory = sqlite3.Row
            self.stats["pool_misses"] += 1
        else:
            self.stats["pool_hits"] += 1
        
        return self.thread_local.connection
    
    @contextmanager
    def get_cursor(self):
        """Context manager para cursor"""
        conn = self._get_connection()
        cursor = conn.cursor()
        try:
            yield cursor
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            cursor.close()
    
    def _create_indexes(self):
        """Criar índices otimizados"""
        indexes = [
            "CREATE INDEX IF NOT EXISTS idx_wallets_address ON wallets(address)",
            "CREATE INDEX IF NOT EXISTS idx_transactions_sender ON transactions_history(sender)",
            "CREATE INDEX IF NOT EXISTS idx_transactions_receiver ON transactions_history(receiver)",
            "CREATE INDEX IF NOT EXISTS idx_transactions_timestamp ON transactions_history(timestamp)",
            "CREATE INDEX IF NOT EXISTS idx_transactions_type ON transactions_history(type)",
            "CREATE INDEX IF NOT EXISTS idx_transactions_network ON transactions_history(network)"
        ]
        
        try:
            with self.get_cursor() as cursor:
                for index_sql in indexes:
                    try:
                        cursor.execute(index_sql)
                    except Exception as e:
                        print(f"⚠️  Erro ao criar índice: {e}")
        except Exception as e:
            print(f"⚠️  Erro ao criar índices: {e}")
    
    def execute_query(
        self,
        query: str,
        params: Tuple = (),
        fetch: bool = True
    ) -> Optional[List[Dict]]:
        """
        Executar query otimizada
        
        Args:
            query: SQL query
            params: Parâmetros da query
            fetch: Se True, retornar resultados
        
        Returns:
            Lista de resultados ou None
        """
        start_time = time.time()
        
        try:
            with self.get_cursor() as cursor:
                cursor.execute(query, params)
                
                if fetch:
                    rows = cursor.fetchall()
                    results = [dict(row) for row in rows]
                else:
                    results = None
                
                elapsed = time.time() - start_time
                self._update_stats(elapsed)
                
                return results
                
        except Exception as e:
            print(f"❌ Erro na query: {e}")
            raise
    
    def execute_batch(
        self,
        query: str,
        params_list: List[Tuple],
        batch_size: int = 100
    ) -> int:
        """
        Executar batch de queries (muito mais rápido)
        
        Args:
            query: SQL query com placeholders
            params_list: Lista de parâmetros
            batch_size: Tamanho do batch
        
        Returns:
            Número de linhas afetadas
        """
        start_time = time.time()
        total_affected = 0
        
        try:
            with self.get_cursor() as cursor:
                # Executar em batches
                for i in range(0, len(params_list), batch_size):
                    batch = params_list[i:i + batch_size]
                    cursor.executemany(query, batch)
                    total_affected += len(batch)
                
                elapsed = time.time() - start_time
                self._update_stats(elapsed, is_batch=True)
                
                return total_affected
                
        except Exception as e:
            print(f"❌ Erro no batch: {e}")
            raise
    
    def _update_stats(self, elapsed: float, is_batch: bool = False):
        """Atualizar estatísticas"""
        if is_batch:
            self.stats["batch_queries"] += 1
        else:
            self.stats["queries"] += 1
        
        # Calcular média
        total_queries = self.stats["queries"] + self.stats["batch_queries"]
        if total_queries > 0:
            total_time = self.stats["avg_query_time"] * (total_queries - 1)
            self.stats["avg_query_time"] = (total_time + elapsed) / total_queries
    
    def get_stats(self) -> Dict:
        """Obter estatísticas"""
        pool_hit_rate = 0.0
        total_pool_ops = self.stats["pool_hits"] + self.stats["pool_misses"]
        if total_pool_ops > 0:
            pool_hit_rate = self.stats["pool_hits"] / total_pool_ops
        
        return {
            **self.stats,
            "pool_hit_rate": pool_hit_rate
        }
    
    def optimize_query(self, query: str) -> str:
        """
        Otimizar query SQL (simplificado)
        
        Em produção, usar EXPLAIN para análise
        """
        # Remover espaços extras
        query = " ".join(query.split())
        
        # Adicionar hints se necessário
        # (SQLite não suporta hints, mas PostgreSQL sim)
        
        return query

# Instância global
_global_db_optimizer = None

def get_database_optimizer(db_path: str = "allianza_blockchain.db") -> DatabaseOptimizer:
    """Obter instância global do database optimizer"""
    global _global_db_optimizer
    if _global_db_optimizer is None:
        _global_db_optimizer = DatabaseOptimizer(db_path=db_path)
    return _global_db_optimizer

if __name__ == '__main__':
    print("="*70)
    print("💾 DATABASE OPTIMIZER - TESTE")
    print("="*70)
    
    optimizer = DatabaseOptimizer()
    
    # Teste de query
    print("\n📝 Teste 1: Query simples")
    results = optimizer.execute_query(
        "SELECT COUNT(*) as count FROM wallets",
        fetch=True
    )
    print(f"   ✅ Resultado: {results}")
    
    # Estatísticas
    print("\n📊 Estatísticas:")
    stats = optimizer.get_stats()
    print(f"   Queries: {stats['queries']}")
    print(f"   Pool hit rate: {stats['pool_hit_rate']*100:.1f}%")







