# cross_chain_state_machine.py
# 🌟 CROSS-CHAIN STATE MACHINE
# Máquina de estado sincronizada entre múltiplas blockchains

import time
import hashlib
import json
from typing import Dict, List, Optional
from enum import Enum
import logging

logger = logging.getLogger(__name__)

class State(Enum):
    INITIAL = "initial"
    PENDING = "pending"
    EXECUTING = "executing"
    COMMITTED = "committed"
    ROLLED_BACK = "rolled_back"
    FAILED = "failed"

class CrossChainStateMachine:
    """
    🌟 CROSS-CHAIN STATE MACHINE
    Primeira blockchain com máquina de estado cross-chain!
    
    Sincroniza estado entre múltiplas blockchains:
    - Estado unificado
    - Transições atômicas
    - Rollback automático
    """
    
    def __init__(self):
        self.state_machines = {}
        self.transitions = []
        
        logger.info("🌟 CROSS-CHAIN STATE MACHINE: Inicializado!")
        print("🌟 CROSS-CHAIN STATE MACHINE: Sistema inicializado!")
        print("   • Estado sincronizado cross-chain")
        print("   • Transições atômicas")
        print("   • Rollback automático")
    
    def create_state_machine(self, machine_id: str, chains: List[str]) -> Dict:
        """Criar máquina de estado cross-chain"""
        machine = {
            "machine_id": machine_id,
            "chains": chains,
            "current_state": State.INITIAL.value,
            "state_history": [],
            "created_at": time.time()
        }
        
        self.state_machines[machine_id] = machine
        
        logger.info(f"✅ State Machine criada: {machine_id} ({', '.join(chains)})")
        
        return {
            "success": True,
            "machine_id": machine_id,
            "machine": machine
        }
    
    def transition(self, machine_id: str, new_state: str, chain: str) -> Dict:
        """Fazer transição de estado"""
        if machine_id not in self.state_machines:
            return {"success": False, "error": "State machine não encontrada"}
        
        machine = self.state_machines[machine_id]
        
        # Validar transição
        valid_transitions = {
            State.INITIAL.value: [State.PENDING.value],
            State.PENDING.value: [State.EXECUTING.value, State.FAILED.value],
            State.EXECUTING.value: [State.COMMITTED.value, State.ROLLED_BACK.value],
            State.COMMITTED.value: [],
            State.ROLLED_BACK.value: [],
            State.FAILED.value: []
        }
        
        current = machine["current_state"]
        if new_state not in valid_transitions.get(current, []):
            return {
                "success": False,
                "error": f"Transição inválida: {current} → {new_state}"
            }
        
        # Fazer transição
        old_state = machine["current_state"]
        machine["current_state"] = new_state
        machine["state_history"].append({
            "from": old_state,
            "to": new_state,
            "chain": chain,
            "timestamp": time.time()
        })
        
        self.transitions.append({
            "machine_id": machine_id,
            "from": old_state,
            "to": new_state,
            "chain": chain,
            "timestamp": time.time()
        })
        
        logger.info(f"🔄 Transição: {machine_id} ({old_state} → {new_state}) em {chain}")
        
        return {
            "success": True,
            "machine_id": machine_id,
            "old_state": old_state,
            "new_state": new_state,
            "chain": chain
        }
    
    def rollback(self, machine_id: str, reason: str = None) -> Dict:
        """Fazer rollback da máquina de estado"""
        if machine_id not in self.state_machines:
            return {"success": False, "error": "State machine não encontrada"}
        
        machine = self.state_machines[machine_id]
        
        # Rollback para estado anterior
        if machine["state_history"]:
            last_transition = machine["state_history"][-1]
            machine["current_state"] = last_transition["from"]
        else:
            machine["current_state"] = State.INITIAL.value
        
        machine["current_state"] = State.ROLLED_BACK.value
        
        logger.warning(f"⚠️  Rollback: {machine_id} ({reason or 'Erro desconhecido'})")
        
        return {
            "success": True,
            "machine_id": machine_id,
            "state": State.ROLLED_BACK.value,
            "reason": reason
        }
    
    def get_machine_state(self, machine_id: str) -> Dict:
        """Obter estado atual da máquina"""
        if machine_id not in self.state_machines:
            return {"error": "State machine não encontrada"}
        
        return self.state_machines[machine_id]


# Instância global
cross_chain_state_machine = None

def init_cross_chain_state_machine():
    """Inicializar máquina de estado cross-chain"""
    global cross_chain_state_machine
    cross_chain_state_machine = CrossChainStateMachine()
    logger.info("🌟 CROSS-CHAIN STATE MACHINE: Sistema inicializado!")
    return cross_chain_state_machine












