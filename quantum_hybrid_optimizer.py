#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧠 OTIMIZADOR HÍBRIDO INTELIGENTE DE SEGURANÇA QUÂNTICA
Escolhe automaticamente o melhor algoritmo PQC baseado na chain e custo de gas
Resolve o problema de custos altos de QRS-3 no Ethereum
"""

import os
from typing import Dict, Optional, List
from datetime import datetime

class QuantumHybridOptimizer:
    """
    Otimizador híbrido inteligente que escolhe o melhor algoritmo PQC
    baseado na chain de destino e custos de gas
    """
    
    def __init__(self, gas_analyzer=None):
        self.gas_analyzer = gas_analyzer
        
        # Configurações de chains e seus custos de gas
        # Valores em USD por verificação (atualizados do gas_cost_analyzer)
        self.chain_costs = {
            "polygon": {
                "ml_dsa": 0.0076,
                "sphincs": 0.0199,
                "qrs3": 0.0244,
                "recommended": "qrs3",  # QRS-3 é viável em Polygon
                "max_cost_threshold": 0.10  # Máximo aceitável em USD
            },
            "polygon_testnet": {
                "ml_dsa": 0.001,
                "sphincs": 0.002,
                "qrs3": 0.003,
                "recommended": "qrs3",
                "max_cost_threshold": 0.10
            },
            "ethereum": {
                "ml_dsa": 0.0011,
                "sphincs": 0.0028,
                "qrs3": 61.0700,  # MUITO CARO!
                "recommended": "ml_dsa",  # Usar apenas ML-DSA no Ethereum
                "max_cost_threshold": 0.10
            },
            "ethereum_sepolia": {
                "ml_dsa": 0.0001,
                "sphincs": 0.0002,
                "qrs3": 0.0003,
                "recommended": "qrs3",  # Testnet é barato
                "max_cost_threshold": 0.10
            },
            "bsc": {
                "ml_dsa": 0.001,
                "sphincs": 0.002,
                "qrs3": 0.003,
                "recommended": "qrs3",  # BSC é barato
                "max_cost_threshold": 0.10
            },
            "bsc_testnet": {
                "ml_dsa": 0.0001,
                "sphincs": 0.0002,
                "qrs3": 0.0003,
                "recommended": "qrs3",
                "max_cost_threshold": 0.10
            },
            "base": {
                "ml_dsa": 0.001,
                "sphincs": 0.002,
                "qrs3": 0.003,
                "recommended": "qrs3",
                "max_cost_threshold": 0.10
            },
            "arbitrum": {
                "ml_dsa": 0.001,
                "sphincs": 0.002,
                "qrs3": 0.003,
                "recommended": "qrs3",
                "max_cost_threshold": 0.10
            },
            "optimism": {
                "ml_dsa": 0.001,
                "sphincs": 0.002,
                "qrs3": 0.003,
                "recommended": "qrs3",
                "max_cost_threshold": 0.10
            }
        }
        
        # Estratégias de seleção
        self.strategies = {
            "cost_optimized": self._select_by_cost,
            "security_max": self._select_max_security,
            "balanced": self._select_balanced,
            "chain_specific": self._select_chain_specific
        }
        
        # Estatísticas
        self.stats = {
            "total_selections": 0,
            "qrs3_selections": 0,
            "ml_dsa_selections": 0,
            "sphincs_selections": 0,
            "cost_savings_usd": 0.0
        }
    
    def select_algorithm(
        self,
        target_chain: str,
        transaction_value: float = 0.0,
        strategy: str = "cost_optimized",
        force_algorithm: Optional[str] = None
    ) -> Dict:
        """
        Selecionar o melhor algoritmo PQC baseado na chain e estratégia
        
        Args:
            target_chain: Chain de destino (polygon, ethereum, bsc, etc.)
            transaction_value: Valor da transação em USD (opcional)
            strategy: Estratégia de seleção (cost_optimized, security_max, balanced, chain_specific)
            force_algorithm: Forçar uso de algoritmo específico (opcional)
        
        Returns:
            Dict com algoritmo selecionado e justificativa
        """
        self.stats["total_selections"] += 1
        
        # Normalizar nome da chain
        chain_normalized = target_chain.lower().replace("_testnet", "").replace("_mainnet", "")
        
        # Se forçar algoritmo, usar diretamente
        if force_algorithm:
            return {
                "algorithm": force_algorithm,
                "chain": target_chain,
                "strategy": "forced",
                "cost_usd": self.chain_costs.get(chain_normalized, {}).get(force_algorithm, 0),
                "reason": f"Algoritmo forçado: {force_algorithm}",
                "recommended": True
            }
        
        # Verificar se chain está configurada
        if chain_normalized not in self.chain_costs:
            # Chain desconhecida - usar ML-DSA como padrão seguro
            return {
                "algorithm": "ml_dsa",
                "chain": target_chain,
                "strategy": "default",
                "cost_usd": 0.001,
                "reason": f"Chain {target_chain} não configurada - usando ML-DSA como padrão",
                "recommended": True
            }
        
        chain_config = self.chain_costs[chain_normalized]
        
        # Selecionar algoritmo baseado na estratégia
        if strategy in self.strategies:
            result = self.strategies[strategy](chain_normalized, chain_config, transaction_value)
        else:
            # Estratégia padrão: cost_optimized
            result = self.strategies["cost_optimized"](chain_normalized, chain_config, transaction_value)
        
        # Atualizar estatísticas
        if result["algorithm"] == "qrs3":
            self.stats["qrs3_selections"] += 1
        elif result["algorithm"] == "ml_dsa":
            self.stats["ml_dsa_selections"] += 1
        elif result["algorithm"] == "sphincs":
            self.stats["sphincs_selections"] += 1
        
        return result
    
    def _select_by_cost(
        self,
        chain: str,
        chain_config: Dict,
        transaction_value: float
    ) -> Dict:
        """
        Selecionar algoritmo baseado apenas no custo (mais barato)
        """
        costs = {
            "ml_dsa": chain_config["ml_dsa"],
            "sphincs": chain_config["sphincs"],
            "qrs3": chain_config["qrs3"]
        }
        
        # Encontrar algoritmo mais barato
        cheapest = min(costs.items(), key=lambda x: x[1])
        algorithm = cheapest[0]
        cost = cheapest[1]
        
        # Verificar se está dentro do threshold
        if cost > chain_config["max_cost_threshold"]:
            # Se o mais barato ainda é caro, usar ML-DSA (sempre seguro)
            algorithm = "ml_dsa"
            cost = chain_config["ml_dsa"]
            reason = f"Custo mínimo ({cheapest[0]}: ${cost:.4f}) excede threshold (${chain_config['max_cost_threshold']:.2f}). Usando ML-DSA."
        else:
            reason = f"Algoritmo mais barato: {algorithm} (${cost:.4f} USD)"
        
        return {
            "algorithm": algorithm,
            "chain": chain,
            "strategy": "cost_optimized",
            "cost_usd": cost,
            "reason": reason,
            "recommended": True,
            "cost_comparison": costs
        }
    
    def _select_max_security(
        self,
        chain: str,
        chain_config: Dict,
        transaction_value: float
    ) -> Dict:
        """
        Selecionar algoritmo com máxima segurança (QRS-3 se viável)
        """
        # Verificar se QRS-3 é viável (dentro do threshold)
        if chain_config["qrs3"] <= chain_config["max_cost_threshold"]:
            return {
                "algorithm": "qrs3",
                "chain": chain,
                "strategy": "security_max",
                "cost_usd": chain_config["qrs3"],
                "reason": f"Máxima segurança: QRS-3 (${chain_config['qrs3']:.4f} USD) - viável nesta chain",
                "recommended": True,
                "security_level": "maximum"
            }
        else:
            # QRS-3 muito caro, usar ML-DSA (ainda é quantum-safe)
            return {
                "algorithm": "ml_dsa",
                "chain": chain,
                "strategy": "security_max",
                "cost_usd": chain_config["ml_dsa"],
                "reason": f"QRS-3 muito caro (${chain_config['qrs3']:.4f} USD). Usando ML-DSA para segurança quântica viável.",
                "recommended": True,
                "security_level": "high",
                "warning": "QRS-3 não viável nesta chain devido ao custo"
            }
    
    def _select_balanced(
        self,
        chain: str,
        chain_config: Dict,
        transaction_value: float
    ) -> Dict:
        """
        Selecionar algoritmo balanceado (segurança vs custo)
        """
        # Se transação é crítica (>$10,000), priorizar segurança
        if transaction_value > 10000:
            return self._select_max_security(chain, chain_config, transaction_value)
        
        # Se transação é normal ($1,000-$10,000), usar recomendação da chain
        elif transaction_value > 1000:
            recommended = chain_config["recommended"]
            cost = chain_config[recommended]
            
            # Verificar se recomendado é viável
            if cost <= chain_config["max_cost_threshold"]:
                return {
                    "algorithm": recommended,
                    "chain": chain,
                    "strategy": "balanced",
                    "cost_usd": cost,
                    "reason": f"Transação normal: usando {recommended} recomendado para esta chain (${cost:.4f} USD)",
                    "recommended": True
                }
            else:
                # Recomendado não viável, usar ML-DSA
                return {
                    "algorithm": "ml_dsa",
                    "chain": chain,
                    "strategy": "balanced",
                    "cost_usd": chain_config["ml_dsa"],
                    "reason": f"Recomendado ({recommended}) não viável. Usando ML-DSA.",
                    "recommended": True
                }
        
        # Microtransações (<$1,000), usar mais barato
        else:
            return self._select_by_cost(chain, chain_config, transaction_value)
    
    def _select_chain_specific(
        self,
        chain: str,
        chain_config: Dict,
        transaction_value: float
    ) -> Dict:
        """
        Usar algoritmo específico recomendado para a chain
        """
        recommended = chain_config["recommended"]
        cost = chain_config[recommended]
        
        # Verificar se recomendado é viável
        if cost <= chain_config["max_cost_threshold"]:
            return {
                "algorithm": recommended,
                "chain": chain,
                "strategy": "chain_specific",
                "cost_usd": cost,
                "reason": f"Usando algoritmo recomendado para {chain}: {recommended} (${cost:.4f} USD)",
                "recommended": True
            }
        else:
            # Recomendado não viável, usar ML-DSA
            return {
                "algorithm": "ml_dsa",
                "chain": chain,
                "strategy": "chain_specific",
                "cost_usd": chain_config["ml_dsa"],
                "reason": f"Recomendado ({recommended}) não viável (${cost:.4f} USD). Usando ML-DSA (${chain_config['ml_dsa']:.4f} USD).",
                "recommended": True,
                "warning": f"QRS-3 custa ${cost:.2f} USD nesta chain - muito alto!"
            }
    
    def get_chain_recommendation(self, target_chain: str) -> Dict:
        """
        Obter recomendação para uma chain específica
        
        Returns:
            Dict com recomendação e justificativa
        """
        chain_normalized = target_chain.lower().replace("_testnet", "").replace("_mainnet", "")
        
        if chain_normalized not in self.chain_costs:
            return {
                "chain": target_chain,
                "recommended_algorithm": "ml_dsa",
                "reason": "Chain não configurada - usando ML-DSA como padrão",
                "cost_usd": 0.001
            }
        
        config = self.chain_costs[chain_normalized]
        recommended = config["recommended"]
        cost = config[recommended]
        
        # Verificar viabilidade
        is_viable = cost <= config["max_cost_threshold"]
        
        return {
            "chain": target_chain,
            "recommended_algorithm": recommended if is_viable else "ml_dsa",
            "cost_usd": cost if is_viable else config["ml_dsa"],
            "is_viable": is_viable,
            "reason": f"Recomendado: {recommended} (${cost:.4f} USD)" if is_viable else f"{recommended} não viável (${cost:.4f} USD). Usar ML-DSA (${config['ml_dsa']:.4f} USD).",
            "all_costs": {
                "ml_dsa": config["ml_dsa"],
                "sphincs": config["sphincs"],
                "qrs3": config["qrs3"]
            }
        }
    
    def update_chain_costs(self, chain: str, costs: Dict):
        """
        Atualizar custos de gas para uma chain (útil para atualizações em tempo real)
        """
        chain_normalized = chain.lower().replace("_testnet", "").replace("_mainnet", "")
        
        if chain_normalized in self.chain_costs:
            self.chain_costs[chain_normalized].update(costs)
            return True
        else:
            # Adicionar nova chain
            self.chain_costs[chain_normalized] = {
                "ml_dsa": costs.get("ml_dsa", 0.001),
                "sphincs": costs.get("sphincs", 0.002),
                "qrs3": costs.get("qrs3", 0.003),
                "recommended": costs.get("recommended", "ml_dsa"),
                "max_cost_threshold": costs.get("max_cost_threshold", 0.10)
            }
            return True
    
    def get_statistics(self) -> Dict:
        """
        Obter estatísticas de uso do otimizador
        """
        total = self.stats["total_selections"]
        if total == 0:
            return {
                "total_selections": 0,
                "message": "Nenhuma seleção realizada ainda"
            }
        
        return {
            "total_selections": total,
            "qrs3_percentage": (self.stats["qrs3_selections"] / total * 100) if total > 0 else 0,
            "ml_dsa_percentage": (self.stats["ml_dsa_selections"] / total * 100) if total > 0 else 0,
            "sphincs_percentage": (self.stats["sphincs_selections"] / total * 100) if total > 0 else 0,
            "cost_savings_usd": self.stats["cost_savings_usd"],
            "average_cost_per_tx": self.stats["cost_savings_usd"] / total if total > 0 else 0
        }
    
    def analyze_all_chains(self) -> Dict:
        """
        Analisar todas as chains e gerar recomendações
        """
        recommendations = {}
        
        for chain, config in self.chain_costs.items():
            recommendations[chain] = self.get_chain_recommendation(chain)
        
        return {
            "timestamp": datetime.now().isoformat(),
            "recommendations": recommendations,
            "summary": {
                "chains_with_qrs3": sum(1 for r in recommendations.values() if r["recommended_algorithm"] == "qrs3"),
                "chains_with_ml_dsa": sum(1 for r in recommendations.values() if r["recommended_algorithm"] == "ml_dsa"),
                "total_chains": len(recommendations)
            }
        }

# Instância global
quantum_hybrid_optimizer = QuantumHybridOptimizer()

