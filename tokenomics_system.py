#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
💰 TOKENOMICS SYSTEM - ALLIANZA BLOCKCHAIN
Sistema completo de Tokenomics e Governança
"""

import json
import time
import hashlib
from datetime import datetime, timezone
from typing import Dict, Optional, List
from dataclasses import dataclass, asdict
from collections import defaultdict

@dataclass
class TokenDistribution:
    """Distribuição de tokens"""
    team: float = 0.15  # 15%
    investors: float = 0.25  # 25%
    ecosystem: float = 0.30  # 30%
    public_sale: float = 0.20  # 20%
    reserve: float = 0.10  # 10%

@dataclass
class VestingSchedule:
    """Cronograma de vesting"""
    team_years: int = 4
    investors_years: int = 2
    ecosystem_years: int = 3
    public_sale_immediate: bool = True

@dataclass
class TokenUtility:
    """Utilidades do token"""
    gas_fee_discount: float = 0.20  # 20% desconto
    bridge_fee_discount: float = 0.30  # 30% desconto
    qaas_discount: float = 0.15  # 15% desconto
    staking_rewards: float = 0.10  # 10% APY
    governance_voting: bool = True
    validator_rewards: bool = True

class TokenomicsSystem:
    """
    Sistema completo de Tokenomics para Allianza Blockchain
    
    Características:
    - Token ALZ (Allianza Token)
    - Distribuição controlada
    - Vesting schedules
    - Utilidades múltiplas
    - Integração com governança
    """
    
    def __init__(self):
        self.total_supply = 1_000_000_000  # 1 bilhão de tokens
        self.token_symbol = "ALZ"
        self.token_name = "Allianza Token"
        self.decimals = 18
        
        # Distribuição
        self.distribution = TokenDistribution()
        
        # Vesting
        self.vesting = VestingSchedule()
        
        # Utilidades
        self.utilities = TokenUtility()
        
        # Balances (simulado - em produção usar blockchain)
        self.balances = defaultdict(float)
        
        # Vesting tracking
        self.vesting_schedules = {}  # address -> vesting_info
        
        # Staking
        self.staking_pools = {}  # pool_id -> staking_info
        
        # Governance
        self.governance_enabled = True
        
        print("💰 TOKENOMICS SYSTEM: Inicializado!")
        print(f"   Token: {self.token_name} ({self.token_symbol})")
        print(f"   Total Supply: {self.total_supply:,} {self.token_symbol}")
    
    def get_tokenomics_info(self) -> Dict:
        """Obter informações completas de tokenomics"""
        return {
            "token": {
                "name": self.token_name,
                "symbol": self.token_symbol,
                "total_supply": self.total_supply,
                "decimals": self.decimals
            },
            "distribution": asdict(self.distribution),
            "vesting": asdict(self.vesting),
            "utilities": asdict(self.utilities),
            "circulating_supply": self._calculate_circulating_supply(),
            "locked_supply": self._calculate_locked_supply()
        }
    
    def _calculate_circulating_supply(self) -> float:
        """Calcular supply em circulação"""
        # Em produção, calcular baseado em vesting releases
        # Por agora, simular 20% em circulação (public sale)
        return self.total_supply * self.distribution.public_sale
    
    def _calculate_locked_supply(self) -> float:
        """Calcular supply bloqueado (vesting)"""
        return self.total_supply * (
            self.distribution.team +
            self.distribution.investors +
            self.distribution.ecosystem
        )
    
    def calculate_distribution_amounts(self) -> Dict:
        """Calcular quantidades de distribuição"""
        return {
            "team": self.total_supply * self.distribution.team,
            "investors": self.total_supply * self.distribution.investors,
            "ecosystem": self.total_supply * self.distribution.ecosystem,
            "public_sale": self.total_supply * self.distribution.public_sale,
            "reserve": self.total_supply * self.distribution.reserve
        }
    
    def get_vesting_info(self, address: str) -> Optional[Dict]:
        """Obter informações de vesting para um endereço"""
        if address not in self.vesting_schedules:
            return None
        
        vesting = self.vesting_schedules[address]
        now = time.time()
        
        # Calcular tokens desbloqueados
        if now >= vesting["end_time"]:
            unlocked = vesting["total_amount"]
        else:
            elapsed = now - vesting["start_time"]
            total_duration = vesting["end_time"] - vesting["start_time"]
            unlocked = vesting["total_amount"] * (elapsed / total_duration)
        
        return {
            "address": address,
            "total_amount": vesting["total_amount"],
            "unlocked": unlocked,
            "locked": vesting["total_amount"] - unlocked,
            "start_time": vesting["start_time"],
            "end_time": vesting["end_time"],
            "vesting_type": vesting["type"]
        }
    
    def calculate_gas_fee_with_alz(self, base_fee: float, alz_balance: float) -> Dict:
        """Calcular taxa de gas com desconto ALZ"""
        # Desconto baseado em quantidade de ALZ
        if alz_balance >= 1_000_000:  # 1M ALZ
            discount = self.utilities.gas_fee_discount
        elif alz_balance >= 100_000:  # 100K ALZ
            discount = self.utilities.gas_fee_discount * 0.5
        else:
            discount = 0.0
        
        discounted_fee = base_fee * (1 - discount)
        
        return {
            "base_fee": base_fee,
            "discounted_fee": discounted_fee,
            "discount_percent": discount * 100,
            "savings": base_fee - discounted_fee,
            "alz_balance": alz_balance
        }
    
    def calculate_bridge_fee_with_alz(self, base_fee: float, alz_balance: float) -> Dict:
        """Calcular taxa de bridge com desconto ALZ"""
        # Desconto baseado em quantidade de ALZ
        if alz_balance >= 500_000:  # 500K ALZ
            discount = self.utilities.bridge_fee_discount
        elif alz_balance >= 50_000:  # 50K ALZ
            discount = self.utilities.bridge_fee_discount * 0.5
        else:
            discount = 0.0
        
        discounted_fee = base_fee * (1 - discount)
        
        return {
            "base_fee": base_fee,
            "discounted_fee": discounted_fee,
            "discount_percent": discount * 100,
            "savings": base_fee - discounted_fee,
            "alz_balance": alz_balance
        }
    
    def create_staking_pool(
        self,
        pool_id: str,
        apy: float,
        min_stake: float,
        lock_period_days: int = 0
    ) -> Dict:
        """Criar pool de staking"""
        pool = {
            "pool_id": pool_id,
            "apy": apy,
            "min_stake": min_stake,
            "lock_period_days": lock_period_days,
            "total_staked": 0.0,
            "stakers": {},
            "created_at": time.time()
        }
        
        self.staking_pools[pool_id] = pool
        
        return {
            "success": True,
            "pool": pool,
            "message": f"Pool de staking {pool_id} criado"
        }
    
    def stake_tokens(
        self,
        pool_id: str,
        address: str,
        amount: float
    ) -> Dict:
        """Stake tokens em um pool"""
        if pool_id not in self.staking_pools:
            return {"success": False, "error": "Pool não encontrado"}
        
        pool = self.staking_pools[pool_id]
        
        if amount < pool["min_stake"]:
            return {
                "success": False,
                "error": f"Quantidade mínima: {pool['min_stake']} ALZ"
            }
        
        if address not in pool["stakers"]:
            pool["stakers"][address] = {
                "amount": 0.0,
                "staked_at": time.time(),
                "rewards_earned": 0.0
            }
        
        pool["stakers"][address]["amount"] += amount
        pool["total_staked"] += amount
        
        return {
            "success": True,
            "pool_id": pool_id,
            "address": address,
            "amount_staked": amount,
            "total_staked": pool["stakers"][address]["amount"],
            "apy": pool["apy"],
            "estimated_rewards_per_year": amount * pool["apy"]
        }
    
    def calculate_staking_rewards(
        self,
        pool_id: str,
        address: str
    ) -> Dict:
        """Calcular recompensas de staking"""
        if pool_id not in self.staking_pools:
            return {"success": False, "error": "Pool não encontrado"}
        
        pool = self.staking_pools[pool_id]
        
        if address not in pool["stakers"]:
            return {"success": False, "error": "Endereço não está fazendo stake"}
        
        staker = pool["stakers"][address]
        staked_amount = staker["amount"]
        staked_time = time.time() - staker["staked_at"]
        staked_days = staked_time / (24 * 3600)
        
        # Calcular recompensas (APY anual)
        rewards = staked_amount * pool["apy"] * (staked_days / 365)
        
        return {
            "success": True,
            "pool_id": pool_id,
            "address": address,
            "staked_amount": staked_amount,
            "staked_days": staked_days,
            "apy": pool["apy"],
            "rewards_earned": rewards,
            "rewards_per_day": staked_amount * pool["apy"] / 365
        }
    
    def get_revenue_model(self) -> Dict:
        """Obter modelo de receita"""
        return {
            "bridge_fees": {
                "standard_rate": 0.001,  # 0.1%
                "with_alz_rate": 0.0005,  # 0.05% (50% desconto)
                "projected_annual": {
                    "low": 1_000_000,  # $1M (1000 transações/dia)
                    "high": 5_000_000  # $5M (5000 transações/dia)
                }
            },
            "qaas_enterprise": {
                "monthly_per_client": {
                    "low": 10_000,  # $10K/mês
                    "high": 50_000  # $50K/mês
                },
                "projected_annual": {
                    "low": 500_000,  # $500K (10 clientes)
                    "high": 2_000_000  # $2M (20 clientes)
                }
            },
            "api_premium": {
                "tiers": {
                    "tier_1": {"price": 1_000, "requests_per_min": 1000},
                    "tier_2": {"price": 5_000, "requests_per_min": 5000},
                    "tier_3": {"price": 10_000, "requests_per_min": -1}  # unlimited
                },
                "projected_annual": {
                    "low": 200_000,  # $200K (20 clientes)
                    "high": 1_000_000  # $1M (100 clientes)
                }
            },
            "governance_fees": {
                "proposal_fee": {"min": 100, "max": 1000},  # ALZ
                "execution_fee": {"min": 50, "max": 500},  # ALZ
                "projected_annual": {
                    "low": 50_000,  # $50K
                    "high": 200_000  # $200K
                }
            },
            "total_projected_annual": {
                "low": 1_750_000,  # $1.75M
                "high": 8_200_000  # $8.2M
            }
        }

if __name__ == '__main__':
    print("="*70)
    print("💰 TOKENOMICS SYSTEM - TESTE")
    print("="*70)
    
    tokenomics = TokenomicsSystem()
    
    # Informações de tokenomics
    print("\n📊 Informações de Tokenomics:")
    info = tokenomics.get_tokenomics_info()
    print(json.dumps(info, indent=2, ensure_ascii=False))
    
    # Distribuição
    print("\n📋 Distribuição de Tokens:")
    distribution = tokenomics.calculate_distribution_amounts()
    for category, amount in distribution.items():
        print(f"   {category.capitalize()}: {amount:,.0f} ALZ")
    
    # Modelo de receita
    print("\n💰 Modelo de Receita:")
    revenue = tokenomics.get_revenue_model()
    print(f"   Receita Anual Projetada: ${revenue['total_projected_annual']['low']:,} - ${revenue['total_projected_annual']['high']:,}")
    
    # Staking
    print("\n📈 Criando Pool de Staking...")
    staking_result = tokenomics.create_staking_pool(
        pool_id="main_pool",
        apy=0.10,  # 10% APY
        min_stake=1000.0,
        lock_period_days=30
    )
    print(f"   ✅ {staking_result['message']}")
    
    # Stake tokens
    print("\n📈 Fazendo Stake...")
    stake_result = tokenomics.stake_tokens(
        pool_id="main_pool",
        address="0x1234...",
        amount=10000.0
    )
    if stake_result.get("success"):
        print(f"   ✅ Stake realizado: {stake_result['amount_staked']:,.0f} ALZ")
        print(f"   ✅ APY: {stake_result['apy']*100:.1f}%")
        print(f"   ✅ Recompensas estimadas/ano: {stake_result['estimated_rewards_per_year']:,.0f} ALZ")
    
    # Calcular recompensas
    print("\n📈 Calculando Recompensas...")
    rewards = tokenomics.calculate_staking_rewards("main_pool", "0x1234...")
    if rewards.get("success"):
        print(f"   ✅ Recompensas acumuladas: {rewards['rewards_earned']:,.2f} ALZ")
        print(f"   ✅ Recompensas/dia: {rewards['rewards_per_day']:,.2f} ALZ")



