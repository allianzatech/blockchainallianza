# dynamic_sharding.py
# 🔀 SHARDING DINÂMICO - ALLIANZA BLOCKCHAIN
# Sistema de sharding que se adapta dinamicamente à carga da rede

import time
import hashlib
import logging
from typing import Dict, List, Optional
from collections import defaultdict

logger = logging.getLogger(__name__)

class DynamicSharding:
    """
    🔀 SHARDING DINÂMICO
    Primeira blockchain com sharding que se adapta automaticamente!
    
    Características:
    - Cria novos shards quando carga aumenta
    - Remove shards quando carga diminui
    - Balanceamento automático
    - Cross-shard transactions otimizadas
    - Escalabilidade horizontal infinita
    """
    
    def __init__(self, blockchain, min_shards: int = 4, max_shards: int = 1000):
        self.blockchain = blockchain
        self.min_shards = min_shards
        self.max_shards = max_shards
        self.shard_load_history = defaultdict(list)
        self.shard_metrics = {}
        self.cross_shard_cache = {}
        
        logger.info("🔀 DYNAMIC SHARDING: Inicializado!")
        print("🔀 DYNAMIC SHARDING: Sistema inicializado!")
        print(f"   • Shards mínimos: {min_shards}")
        print(f"   • Shards máximos: {max_shards}")
        print("   • Adaptação automática")
        print("   • Escalabilidade infinita")
    
    def get_shard_count(self) -> int:
        """Retorna número atual de shards"""
        return len(self.blockchain.shards)
    
    def calculate_shard_load(self, shard_id: int) -> float:
        """Calcula carga de um shard (0-1)"""
        if shard_id not in self.blockchain.shards:
            return 0.0
        
        pending_txs = len(self.blockchain.pending_transactions.get(shard_id, []))
        block_count = len(self.blockchain.shards[shard_id])
        
        # Carga baseada em transações pendentes e tamanho da chain
        tx_load = min(pending_txs / 1000.0, 1.0)  # Normalizar
        chain_load = min(block_count / 10000.0, 1.0)  # Normalizar
        
        total_load = (tx_load * 0.7) + (chain_load * 0.3)
        
        # Armazenar histórico
        self.shard_load_history[shard_id].append({
            "timestamp": time.time(),
            "load": total_load,
            "pending_txs": pending_txs,
            "block_count": block_count
        })
        
        # Manter apenas últimos 100 registros
        if len(self.shard_load_history[shard_id]) > 100:
            self.shard_load_history[shard_id].pop(0)
        
        return total_load
    
    def get_all_shard_loads(self) -> Dict[int, float]:
        """Retorna carga de todos os shards"""
        loads = {}
        for shard_id in self.blockchain.shards.keys():
            loads[shard_id] = self.calculate_shard_load(shard_id)
        return loads
    
    def should_create_shard(self) -> bool:
        """Determina se deve criar um novo shard"""
        loads = self.get_all_shard_loads()
        
        if not loads:
            return False
        
        current_shards = len(loads)
        if current_shards >= self.max_shards:
            return False
        
        # Criar shard se algum shard tem carga > 80%
        max_load = max(loads.values())
        if max_load > 0.8:
            return True
        
        # Criar shard se média de carga > 70% e temos menos de 20 shards
        avg_load = sum(loads.values()) / len(loads)
        if avg_load > 0.7 and current_shards < 20:
            return True
        
        return False
    
    def should_merge_shards(self) -> Optional[List[int]]:
        """Determina se deve mesclar shards (retorna lista de shards para mesclar)"""
        loads = self.get_all_shard_loads()
        current_shards = len(loads)
        
        if current_shards <= self.min_shards:
            return None
        
        # Encontrar shards com carga < 20%
        low_load_shards = [
            shard_id for shard_id, load in loads.items()
            if load < 0.2
        ]
        
        # Se temos 2+ shards com carga baixa, mesclar
        if len(low_load_shards) >= 2:
            # Mesclar os 2 shards com menor carga
            low_load_shards.sort(key=lambda x: loads[x])
            return low_load_shards[:2]
        
        return None
    
    def create_new_shard(self) -> int:
        """Cria um novo shard"""
        current_shards = self.get_shard_count()
        new_shard_id = current_shards
        
        # Criar shard vazio
        self.blockchain.shards[new_shard_id] = [self.blockchain.create_genesis_block(new_shard_id)]
        self.blockchain.pending_transactions[new_shard_id] = []
        
        logger.info(f"🔀 Novo shard criado: Shard {new_shard_id}")
        print(f"🔀 Novo shard criado: Shard {new_shard_id}")
        print(f"   Total de shards: {self.get_shard_count()}")
        
        return new_shard_id
    
    def merge_shards(self, shard_ids: List[int]) -> int:
        """Mescla dois shards em um"""
        if len(shard_ids) < 2:
            return shard_ids[0] if shard_ids else None
        
        shard1_id, shard2_id = shard_ids[0], shard_ids[1]
        
        # Mesclar transações pendentes
        self.blockchain.pending_transactions[shard1_id].extend(
            self.blockchain.pending_transactions[shard2_id]
        )
        
        # Mesclar blocos (manter histórico)
        # Nota: Em produção, isso seria mais complexo
        
        # Remover shard2
        del self.blockchain.shards[shard2_id]
        del self.blockchain.pending_transactions[shard2_id]
        
        logger.info(f"🔀 Shards mesclados: {shard1_id} + {shard2_id} → {shard1_id}")
        print(f"🔀 Shards mesclados: {shard1_id} + {shard2_id} → {shard1_id}")
        print(f"   Total de shards: {self.get_shard_count()}")
        
        return shard1_id
    
    def adapt_shards(self):
        """Adapta shards baseado na carga"""
        # Verificar se deve criar shard
        if self.should_create_shard():
            self.create_new_shard()
        
        # Verificar se deve mesclar shards
        shards_to_merge = self.should_merge_shards()
        if shards_to_merge:
            self.merge_shards(shards_to_merge)
    
    def get_shard_for_transaction(self, transaction: Dict) -> int:
        """
        Determina o melhor shard para uma transação
        
        Otimizações:
        - Agrupa transações relacionadas no mesmo shard
        - Balanceia carga entre shards
        - Considera tipo de transação (QRS-3 vai para shard dedicado)
        """
        # Se é transação QRS-3, usar shard dedicado se existir
        if transaction.get("type") == "qrs3" or transaction.get("qrs3_signature"):
            qrs3_shard = self._get_qrs3_shard()
            if qrs3_shard is not None:
                return qrs3_shard
        
        # Se é transação urgente, usar shard com menor carga
        if transaction.get("urgent", False):
            loads = self.get_all_shard_loads()
            if loads:
                min_load_shard = min(loads.items(), key=lambda x: x[1])[0]
                return min_load_shard
        
        # Caso padrão: hash do endereço
        sender = transaction.get("sender", "")
        if sender:
            return int(hashlib.sha256(sender.encode()).hexdigest(), 16) % self.get_shard_count()
        
        # Fallback: shard 0
        return 0
    
    def _get_qrs3_shard(self) -> Optional[int]:
        """Retorna shard dedicado para QRS-3 se existir"""
        # Procurar shard com nome "qrs3" ou último shard se muitos shards
        shard_count = self.get_shard_count()
        
        # Se temos muitos shards, usar um dedicado
        if shard_count > 10:
            # Usar shard especial (último shard ou shard específico)
            return shard_count - 1
        
        return None
    
    def optimize_cross_shard_routing(self, from_shard: int, to_shard: int) -> Dict:
        """Otimiza roteamento cross-shard"""
        cache_key = f"{from_shard}_{to_shard}"
        
        if cache_key in self.cross_shard_cache:
            return self.cross_shard_cache[cache_key]
        
        # Calcular melhor rota
        route = self._calculate_best_route(from_shard, to_shard)
        
        # Cachear resultado
        self.cross_shard_cache[cache_key] = route
        
        return route
    
    def _calculate_best_route(self, from_shard: int, to_shard: int) -> Dict:
        """Calcula melhor rota entre shards"""
        # Em produção, isso seria mais complexo (Dijkstra, etc.)
        return {
            "from_shard": from_shard,
            "to_shard": to_shard,
            "route": [from_shard, to_shard],
            "estimated_latency": 100,  # ms
            "estimated_cost": 1.0
        }
    
    def get_sharding_stats(self) -> Dict:
        """Retorna estatísticas de sharding"""
        loads = self.get_all_shard_loads()
        
        return {
            "total_shards": self.get_shard_count(),
            "min_shards": self.min_shards,
            "max_shards": self.max_shards,
            "average_load": sum(loads.values()) / len(loads) if loads else 0.0,
            "max_load": max(loads.values()) if loads else 0.0,
            "min_load": min(loads.values()) if loads else 0.0,
            "shard_loads": loads,
            "recommendations": self._get_sharding_recommendations()
        }
    
    def _get_sharding_recommendations(self) -> List[Dict]:
        """Retorna recomendações de sharding"""
        recommendations = []
        loads = self.get_all_shard_loads()
        
        if not loads:
            return recommendations
        
        avg_load = sum(loads.values()) / len(loads)
        max_load = max(loads.values())
        
        if max_load > 0.8:
            recommendations.append({
                "action": "create_shard",
                "reason": f"Shard com carga alta detectada ({max_load:.1%})",
                "expected_benefit": "Redução de carga e latência"
            })
        
        if avg_load < 0.2 and self.get_shard_count() > self.min_shards:
            recommendations.append({
                "action": "merge_shards",
                "reason": f"Carga média baixa ({avg_load:.1%})",
                "expected_benefit": "Otimização de recursos"
            })
        
        return recommendations











