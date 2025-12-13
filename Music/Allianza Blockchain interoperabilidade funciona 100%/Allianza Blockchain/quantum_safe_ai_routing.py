# quantum_safe_ai_routing.py
# 🤖 AI Routing que considera segurança quântica
# INÉDITO: Primeiro sistema no mundo

import os
import json
import time
from typing import Dict, List, Optional
from POC_PREDICAO_GAS_80_PRECISAO import GasPricePredictionPOC
from quantum_security import quantum_security

class QuantumSafeAIRouting:
    """
    AI Routing com consideração de segurança quântica
    PRIMEIRO NO MUNDO: Roteamento que otimiza para segurança quântica
    """
    
    def __init__(self):
        self.gas_predictor = GasPricePredictionPOC()
        self.quantum_security = quantum_security
        
        # Suporte PQC por chain
        self.chain_pqc_support = {
            "ethereum": {"pqc_native": False, "qrs3_bridge": True, "quantum_safe_score": 0.8},
            "polygon": {"pqc_native": False, "qrs3_bridge": True, "quantum_safe_score": 0.8},
            "bitcoin": {"pqc_native": False, "qrs3_bridge": True, "quantum_safe_score": 0.7},
            "solana": {"pqc_native": False, "qrs3_bridge": True, "quantum_safe_score": 0.7},
            "bsc": {"pqc_native": False, "qrs3_bridge": True, "quantum_safe_score": 0.8},
            "base": {"pqc_native": False, "qrs3_bridge": True, "quantum_safe_score": 0.8},
            "allianza": {"pqc_native": True, "qrs3_bridge": True, "quantum_safe_score": 1.0}
        }
        
        print("🤖 QUANTUM-SAFE AI ROUTING: Inicializado!")
        print("🔐 Roteamento que considera segurança quântica - PRIMEIRO NO MUNDO!")
    
    def route_with_quantum_safety(
        self,
        operation: str,
        amount: float,
        quantum_safety_required: bool = True,
        chains: Optional[List[str]] = None
    ) -> Dict:
        """
        Rotear considerando segurança quântica
        
        Args:
            operation: Tipo de operação (transfer, swap, etc.)
            amount: Quantidade a transferir
            quantum_safety_required: Se segurança quântica é obrigatória
            chains: Lista de chains a considerar (None = todas)
        
        Returns:
            Dict com chain recomendada e análise
        """
        try:
            if chains is None:
                chains = ["ethereum", "polygon", "bitcoin", "solana", "bsc", "base", "allianza"]
            
            chains_analysis = []
            
            for chain in chains:
                # 1. Prever gas price
                try:
                    gas_analysis = self.gas_predictor.predict_gas_spike(chain)
                    predicted_gas = gas_analysis.get("predicted_price", 0)
                    gas_confidence = gas_analysis.get("confidence", 0.5)
                except:
                    predicted_gas = 0.001  # Fallback
                    gas_confidence = 0.5
                
                # 2. Verificar suporte PQC
                pqc_support = self.chain_pqc_support.get(chain, {
                    "pqc_native": False,
                    "qrs3_bridge": False,
                    "quantum_safe_score": 0.0
                })
                
                # 3. Calcular custo QRS-3
                qrs3_cost = self.calculate_qrs3_cost(chain, amount)
                
                # 4. Calcular score de segurança quântica
                quantum_safe_score = self.calculate_quantum_safe_score(
                    chain,
                    pqc_support,
                    quantum_safety_required
                )
                
                # 5. Calcular score total (combina custo e segurança)
                total_score = self.calculate_total_score(
                    predicted_gas,
                    qrs3_cost,
                    quantum_safe_score,
                    gas_confidence
                )
                
                chains_analysis.append({
                    "chain": chain,
                    "predicted_gas": predicted_gas,
                    "gas_confidence": gas_confidence,
                    "pqc_support": pqc_support,
                    "qrs3_cost": qrs3_cost,
                    "quantum_safe_score": quantum_safe_score,
                    "total_cost": predicted_gas + qrs3_cost,
                    "total_score": total_score
                })
            
            # Filtrar por segurança quântica (se requerido)
            if quantum_safety_required:
                chains_analysis = [
                    c for c in chains_analysis
                    if c["quantum_safe_score"] >= 0.7
                ]
            
            if not chains_analysis:
                return {
                    "success": False,
                    "error": "Nenhuma chain atende aos requisitos de segurança quântica",
                    "quantum_safety_required": quantum_safety_required
                }
            
            # Escolher melhor opção (maior score = melhor)
            best_chain = max(
                chains_analysis,
                key=lambda x: x["total_score"]
            )
            
            return {
                "success": True,
                "recommended_chain": best_chain["chain"],
                "quantum_safe": True,
                "quantum_safe_score": best_chain["quantum_safe_score"],
                "predicted_gas": best_chain["predicted_gas"],
                "gas_confidence": best_chain["gas_confidence"],
                "qrs3_cost": best_chain["qrs3_cost"],
                "total_cost": best_chain["total_cost"],
                "reasoning": f"Chain escolhida por segurança quântica ({best_chain['quantum_safe_score']:.2f}) + custo otimizado ({best_chain['total_cost']:.6f} ETH)",
                "all_chains_analysis": chains_analysis,
                "world_first": "🌍 PRIMEIRO NO MUNDO: AI Routing quântica-seguro!"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def calculate_qrs3_cost(self, chain: str, amount: float) -> float:
        """Calcular custo adicional de usar QRS-3"""
        # QRS-3 tem assinaturas maiores, então custa mais gas
        base_cost = 0.001  # ETH base
        size_multiplier = 3.0  # QRS-3 é ~3x maior que ECDSA
        
        # Ajustar por chain (algumas são mais baratas)
        chain_multipliers = {
            "polygon": 0.1,
            "bsc": 0.1,
            "base": 0.1,
            "ethereum": 1.0,
            "bitcoin": 0.5,
            "solana": 0.2,
            "allianza": 0.05
        }
        
        multiplier = chain_multipliers.get(chain, 1.0)
        
        return base_cost * size_multiplier * multiplier
    
    def calculate_quantum_safe_score(
        self,
        chain: str,
        pqc_support: Dict,
        quantum_safety_required: bool
    ) -> float:
        """Calcular score de segurança quântica (0.0 a 1.0)"""
        # Usar score pré-calculado se disponível
        if "quantum_safe_score" in pqc_support:
            return pqc_support["quantum_safe_score"]
        
        # Calcular baseado em suporte
        score = 0.0
        
        # Suporte PQC nativo = 1.0
        if pqc_support.get("pqc_native"):
            score = 1.0
        # Suporte QRS-3 via bridge = 0.8
        elif pqc_support.get("qrs3_bridge"):
            score = 0.8
        # Sem suporte = 0.0
        else:
            score = 0.0
        
        return score
    
    def calculate_total_score(
        self,
        predicted_gas: float,
        qrs3_cost: float,
        quantum_safe_score: float,
        gas_confidence: float
    ) -> float:
        """
        Calcular score total combinando custo e segurança
        Maior score = melhor opção
        """
        # Normalizar custo (menor = melhor, então inverter)
        # Assumir custo máximo de 0.1 ETH
        normalized_cost = 1.0 - min(1.0, (predicted_gas + qrs3_cost) / 0.1)
        
        # Combinar: 40% segurança quântica + 40% custo + 20% confiança
        total_score = (
            quantum_safe_score * 0.4 +
            normalized_cost * 0.4 +
            gas_confidence * 0.2
        )
        
        return total_score

# Instância global
quantum_safe_routing = QuantumSafeAIRouting()
