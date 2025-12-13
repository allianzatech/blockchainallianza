#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sistema de Gerenciamento de Validadores
Gerencia validadores, staking, slashing e recompensas
"""

import time
import json
from typing import Dict, List, Optional, Set
from dataclasses import dataclass
from enum import Enum
import logging

logger = logging.getLogger(__name__)

class ValidatorStatus(Enum):
    """Status do validador"""
    ACTIVE = "active"
    INACTIVE = "inactive"
    JAILED = "jailed"
    UNBONDING = "unbonding"

@dataclass
class Validator:
    """Representa um validador"""
    address: str
    staked_amount: float
    status: ValidatorStatus
    commission_rate: float  # Taxa de comissão (0-1)
    created_at: float
    last_validation: Optional[float] = None
    total_rewards: float = 0.0
    slashing_count: int = 0
    uptime: float = 100.0  # Percentual de uptime

class ValidatorsManager:
    """
    Gerencia validadores, staking, slashing e recompensas
    """
    
    def __init__(self, min_stake: float = 1000.0):
        self.validators: Dict[str, Validator] = {}
        self.min_stake = min_stake
        self.total_staked = 0.0
        self.slashing_params = {
            "double_sign_penalty": 0.05,  # 5% do stake
            "downtime_penalty": 0.01,  # 1% do stake
            "jail_duration": 86400  # 24 horas em segundos
        }
        self.reward_params = {
            "block_reward": 1.0,  # Recompensa por bloco
            "validator_share": 0.8,  # 80% para validadores
            "delegator_share": 0.2  # 20% para delegadores
        }
        
        logger.info("⚖️  Validators Manager inicializado")
    
    def register_validator(
        self,
        address: str,
        staked_amount: float,
        commission_rate: float = 0.1
    ) -> Dict:
        """Registra novo validador"""
        if staked_amount < self.min_stake:
            return {
                "success": False,
                "error": f"Stake mínimo: {self.min_stake}"
            }
        
        if address in self.validators:
            return {
                "success": False,
                "error": "Validador já registrado"
            }
        
        validator = Validator(
            address=address,
            staked_amount=staked_amount,
            status=ValidatorStatus.ACTIVE,
            commission_rate=commission_rate,
            created_at=time.time()
        )
        
        self.validators[address] = validator
        self.total_staked += staked_amount
        
        logger.info(f"✅ Validador registrado: {address} (stake: {staked_amount})")
        
        return {
            "success": True,
            "validator": {
                "address": address,
                "staked_amount": staked_amount,
                "status": validator.status.value
            }
        }
    
    def stake(self, address: str, amount: float) -> Dict:
        """Adiciona stake a um validador"""
        if address not in self.validators:
            return {
                "success": False,
                "error": "Validador não encontrado"
            }
        
        validator = self.validators[address]
        validator.staked_amount += amount
        self.total_staked += amount
        
        logger.info(f"💰 Stake adicionado: {address} (+{amount})")
        
        return {
            "success": True,
            "new_stake": validator.staked_amount
        }
    
    def unstake(self, address: str, amount: float) -> Dict:
        """Remove stake de um validador"""
        if address not in self.validators:
            return {
                "success": False,
                "error": "Validador não encontrado"
            }
        
        validator = self.validators[address]
        
        if amount > validator.staked_amount:
            return {
                "success": False,
                "error": "Stake insuficiente"
            }
        
        if validator.staked_amount - amount < self.min_stake:
            return {
                "success": False,
                "error": f"Stake não pode ficar abaixo de {self.min_stake}"
            }
        
        validator.staked_amount -= amount
        self.total_staked -= amount
        
        logger.info(f"💸 Stake removido: {address} (-{amount})")
        
        return {
            "success": True,
            "new_stake": validator.staked_amount
        }
    
    def select_validator(self, block_index: int) -> Optional[str]:
        """Seleciona validador para próximo bloco (baseado em stake)"""
        active_validators = [
            (addr, v) for addr, v in self.validators.items()
            if v.status == ValidatorStatus.ACTIVE
        ]
        
        if not active_validators:
            return None
        
        # Seleção baseada em stake (weighted random)
        total_stake = sum(v.staked_amount for _, v in active_validators)
        
        # Por simplicidade, seleciona baseado em stake
        # Em produção, usaria algoritmo mais sofisticado
        import random
        random_value = random.random() * total_stake
        
        current = 0.0
        for address, validator in active_validators:
            current += validator.staked_amount
            if random_value <= current:
                validator.last_validation = time.time()
                return address
        
        # Fallback
        return active_validators[0][0]
    
    def record_validation(self, validator_address: str, success: bool):
        """Registra resultado de validação"""
        if validator_address not in self.validators:
            return
        
        validator = self.validators[validator_address]
        validator.last_validation = time.time()
        
        if success:
            # Atualizar uptime
            validator.uptime = min(validator.uptime + 0.1, 100.0)
        else:
            # Penalizar
            validator.uptime = max(validator.uptime - 1.0, 0.0)
            validator.slashing_count += 1
            
            # Se uptime muito baixo, jailing
            if validator.uptime < 50.0:
                self.jail_validator(validator_address)
    
    def jail_validator(self, address: str, reason: str = "downtime"):
        """Coloca validador em jail"""
        if address not in self.validators:
            return
        
        validator = self.validators[address]
        validator.status = ValidatorStatus.JAILED
        
        # Aplicar slashing
        penalty = validator.staked_amount * self.slashing_params["downtime_penalty"]
        validator.staked_amount -= penalty
        self.total_staked -= penalty
        
        logger.warning(f"🚨 Validador jailing: {address} (razão: {reason}, penalidade: {penalty})")
    
    def distribute_rewards(self, block_index: int, validator_address: str) -> Dict:
        """Distribui recompensas por bloco"""
        if validator_address not in self.validators:
            return {"success": False, "error": "Validador não encontrado"}
        
        validator = self.validators[validator_address]
        
        if validator.status != ValidatorStatus.ACTIVE:
            return {"success": False, "error": "Validador não está ativo"}
        
        # Calcular recompensa baseada em stake
        stake_ratio = validator.staked_amount / self.total_staked if self.total_staked > 0 else 0
        base_reward = self.reward_params["block_reward"] * self.reward_params["validator_share"]
        validator_reward = base_reward * stake_ratio
        
        # Aplicar comissão
        commission = validator_reward * validator.commission_rate
        delegator_reward = validator_reward - commission
        
        validator.total_rewards += validator_reward
        
        logger.info(f"🎁 Recompensa distribuída: {validator_address} ({validator_reward})")
        
        return {
            "success": True,
            "validator_reward": validator_reward,
            "commission": commission,
            "delegator_reward": delegator_reward
        }
    
    def get_validator_info(self, address: str) -> Optional[Dict]:
        """Retorna informações do validador"""
        if address not in self.validators:
            return None
        
        validator = self.validators[address]
        
        return {
            "address": address,
            "staked_amount": validator.staked_amount,
            "status": validator.status.value,
            "commission_rate": validator.commission_rate,
            "total_rewards": validator.total_rewards,
            "uptime": validator.uptime,
            "slashing_count": validator.slashing_count,
            "last_validation": validator.last_validation
        }
    
    def get_all_validators(self) -> List[Dict]:
        """Retorna lista de todos os validadores"""
        return [
            self.get_validator_info(addr)
            for addr in self.validators.keys()
        ]
    
    def get_network_stats(self) -> Dict:
        """Retorna estatísticas da rede"""
        active_count = sum(
            1 for v in self.validators.values()
            if v.status == ValidatorStatus.ACTIVE
        )
        
        return {
            "total_validators": len(self.validators),
            "active_validators": active_count,
            "total_staked": self.total_staked,
            "min_stake": self.min_stake,
            "jailed_validators": sum(
                1 for v in self.validators.values()
                if v.status == ValidatorStatus.JAILED
            )
        }

# Instância global
global_validators_manager: Optional[ValidatorsManager] = None

def initialize_validators_manager(min_stake: float = 1000.0) -> ValidatorsManager:
    """Inicializa gerenciador de validadores global"""
    global global_validators_manager
    global_validators_manager = ValidatorsManager(min_stake)
    return global_validators_manager

def get_validators_manager() -> Optional[ValidatorsManager]:
    """Retorna instância global do gerenciador de validadores"""
    return global_validators_manager



















