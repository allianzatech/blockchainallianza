# adaptive_consensus.py
# 🌟 ADAPTIVE CONSENSUS MECHANISM
# Consenso que se adapta automaticamente baseado em condições da rede

import time
from typing import Dict, Optional
from collections import deque
import logging

logger = logging.getLogger(__name__)

class AdaptiveConsensus:
    """
    🌟 ADAPTIVE CONSENSUS MECHANISM
    Primeira blockchain com consenso adaptativo!
    
    Algoritmos:
    - PoS (Proof of Stake) - Normal
    - PoA (Proof of Authority) - Alta carga
    - PoH (Proof of History) - Urgente
    - Hybrid - Combinação dinâmica
    """
    
    def __init__(self):
        self.current_consensus = "PoS"
        self.consensus_history = deque(maxlen=100)
        self.network_state = {
            "load": 0.0,  # 0-1
            "validators": 0,
            "pending_txs": 0,
            "urgent_txs": 0,
            "block_time": 0.0
        }
        
        logger.info("🌟 ADAPTIVE CONSENSUS: Inicializado!")
        print("🌟 ADAPTIVE CONSENSUS: Sistema inicializado!")
        print("   • Adapta consenso automaticamente")
        print("   • Otimiza performance e segurança")
        print("   • Escala automaticamente")
    
    def update_network_state(self, state: Dict):
        """Atualizar estado da rede"""
        self.network_state.update(state)
        self._adapt_consensus()
    
    def _adapt_consensus(self):
        """Adaptar consenso baseado no estado da rede"""
        load = self.network_state.get("load", 0)
        urgent_txs = self.network_state.get("urgent_txs", 0)
        validators = self.network_state.get("validators", 0)
        
        new_consensus = None
        
        # Alta carga (>80%) -> PoA (mais rápido)
        if load > 0.8:
            new_consensus = "PoA"
            reason = "Alta carga da rede"
        
        # Muitas transações urgentes (>10) -> PoH (mais rápido ainda)
        elif urgent_txs > 10:
            new_consensus = "PoH"
            reason = "Muitas transações urgentes"
        
        # Poucos validadores (<5) -> PoA (mais seguro com poucos)
        elif validators < 5:
            new_consensus = "PoA"
            reason = "Poucos validadores"
        
        # Normal -> PoS (mais seguro)
        else:
            new_consensus = "PoS"
            reason = "Condições normais"
        
        # Mudar consenso se necessário
        if new_consensus != self.current_consensus:
            old_consensus = self.current_consensus
            self.current_consensus = new_consensus
            
            self.consensus_history.append({
                "timestamp": time.time(),
                "from": old_consensus,
                "to": new_consensus,
                "reason": reason,
                "network_state": self.network_state.copy()
            })
            
            logger.info(f"🔄 Consenso adaptado: {old_consensus} → {new_consensus} ({reason})")
    
    def select_consensus(self, network_state: Dict = None) -> str:
        """Selecionar melhor consenso para estado atual"""
        if network_state:
            self.update_network_state(network_state)
        
        return self.current_consensus
    
    def get_consensus_info(self) -> Dict:
        """Obter informações do consenso atual"""
        return {
            "current_consensus": self.current_consensus,
            "network_state": self.network_state,
            "adaptations_count": len(self.consensus_history),
            "recent_adaptations": list(self.consensus_history)[-5:]
        }


# Instância global
adaptive_consensus = None

def init_adaptive_consensus():
    """Inicializar consenso adaptativo"""
    global adaptive_consensus
    adaptive_consensus = AdaptiveConsensus()
    logger.info("🌟 ADAPTIVE CONSENSUS: Sistema inicializado!")
    return adaptive_consensus





















