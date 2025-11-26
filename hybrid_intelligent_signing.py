# hybrid_intelligent_signing.py
# 🧠 MODO HÍBRIDO INTELIGENTE AVANÇADO
# Assinatura adaptativa baseada em valor e tipo de transação

from typing import Dict, Optional
import time

class HybridIntelligentSigning:
    """
    Sistema de Assinatura Híbrida Inteligente
    Adapta o algoritmo de assinatura baseado em:
    - Valor da transação
    - Tipo de transação
    - Urgência
    - Nível de segurança requerido
    """
    
    def __init__(self, quantum_security):
        self.quantum_security = quantum_security
        
        # Limites de valor para diferentes níveis de segurança
        self.thresholds = {
            "critical": 10000.0,  # > $10,000: QRS-3 completo
            "normal": 1000.0,      # $1,000 - $10,000: QRS-2
            "micro": 0.0           # < $1,000: ML-DSA apenas
        }
        
        print("🧠 HYBRID INTELLIGENT SIGNING: Inicializado!")
        print("   • Adaptação automática baseada em valor")
        print("   • QRS-3 para transações críticas")
        print("   • QRS-2 para transações normais")
        print("   • ML-DSA para microtransações")
    
    def sign_intelligent(
        self,
        message: bytes,
        transaction_value: float,
        transaction_type: str = "normal",
        urgency: str = "normal",
        qrs3_keypair_id: Optional[str] = None,
        qrs2_keypair_id: Optional[str] = None,
        ml_dsa_keypair_id: Optional[str] = None
    ) -> Dict:
        """
        Assinar com modo híbrido inteligente
        
        Args:
            message: Mensagem para assinar
            transaction_value: Valor da transação em USD/ALZ
            transaction_type: Tipo de transação (normal, contract, nft, etc)
            urgency: Urgência (low, normal, high, critical)
            qrs3_keypair_id: ID do keypair QRS-3 (se disponível)
            qrs2_keypair_id: ID do keypair QRS-2 (se disponível)
            ml_dsa_keypair_id: ID do keypair ML-DSA (se disponível)
        
        Returns:
            Resultado da assinatura com algoritmo escolhido
        """
        start_time = time.time()
        
        # Decidir algoritmo baseado em valor e tipo
        algorithm_choice = self._choose_algorithm(
            transaction_value,
            transaction_type,
            urgency
        )
        
        # Assinar com algoritmo escolhido
        if algorithm_choice == "qrs3":
            if not qrs3_keypair_id:
                return {
                    "success": False,
                    "error": "QRS-3 keypair não fornecido"
                }
            
            result = self.quantum_security.sign_qrs3(
                qrs3_keypair_id,
                message,
                optimized=True,
                parallel=True
            )
            result["algorithm_used"] = "QRS-3"
            result["reason"] = f"Transação crítica (${transaction_value:,.2f})"
            
        elif algorithm_choice == "qrs2":
            if not qrs2_keypair_id:
                # Tentar gerar QRS-2 se não fornecido
                qrs2_result = self.quantum_security.generate_qrs2_keypair()
                if qrs2_result.get("success"):
                    qrs2_keypair_id = qrs2_result["keypair_id"]
                else:
                    return {
                        "success": False,
                        "error": "Não foi possível gerar QRS-2 keypair"
                    }
            
            # QRS-2 = ECDSA + ML-DSA (sem SPHINCS+)
            result = self._sign_qrs2(qrs2_keypair_id, message)
            result["algorithm_used"] = "QRS-2"
            result["reason"] = f"Transação normal (${transaction_value:,.2f})"
            
        else:  # ml_dsa
            if not ml_dsa_keypair_id:
                # Tentar gerar ML-DSA se não fornecido
                ml_dsa_result = self.quantum_security.generate_ml_dsa_keypair()
                if ml_dsa_result.get("success"):
                    ml_dsa_keypair_id = ml_dsa_result["keypair_id"]
                else:
                    return {
                        "success": False,
                        "error": "Não foi possível gerar ML-DSA keypair"
                    }
            
            result = self.quantum_security.sign_with_ml_dsa(ml_dsa_keypair_id, message)
            result["algorithm_used"] = "ML-DSA"
            result["reason"] = f"Microtransação (${transaction_value:,.2f})"
        
        result["signing_time_ms"] = (time.time() - start_time) * 1000
        result["transaction_value"] = transaction_value
        result["hybrid_mode"] = True
        
        return result
    
    def _choose_algorithm(
        self,
        transaction_value: float,
        transaction_type: str,
        urgency: str
    ) -> str:
        """
        Escolher algoritmo baseado em critérios inteligentes
        """
        # Transações críticas: sempre QRS-3
        if transaction_value >= self.thresholds["critical"]:
            return "qrs3"
        
        # Transações de contrato: QRS-3 (maior segurança)
        if transaction_type in ["contract", "smart_contract", "governance"]:
            return "qrs3"
        
        # Urgência crítica: QRS-3
        if urgency == "critical":
            return "qrs3"
        
        # Transações normais: QRS-2
        if transaction_value >= self.thresholds["normal"]:
            return "qrs2"
        
        # Microtransações: ML-DSA (quantum-safe, rápido)
        return "ml_dsa"
    
    def _sign_qrs2(self, qrs2_keypair_id: str, message: bytes) -> Dict:
        """
        Assinar com QRS-2 (ECDSA + ML-DSA, sem SPHINCS+)
        Mais rápido que QRS-3, mas ainda quantum-safe
        """
        from concurrent.futures import ThreadPoolExecutor
        
        try:
            if qrs2_keypair_id not in self.quantum_security.pqc_keypairs:
                return {"success": False, "error": "QRS-2 keypair não encontrado"}
            
            qrs2 = self.quantum_security.pqc_keypairs[qrs2_keypair_id]
            
            # Processar ECDSA e ML-DSA em paralelo
            from cryptography.hazmat.primitives import serialization
            from cryptography.hazmat.backends import default_backend
            
            # Carregar chave privada clássica
            classic_private = serialization.load_pem_private_key(
                qrs2["classic_private_key"].encode(),
                password=None,
                backend=default_backend()
            )
            
            with ThreadPoolExecutor(max_workers=2) as executor:
                ecdsa_future = executor.submit(
                    self.quantum_security._sign_ecdsa_internal,
                    classic_private,
                    message
                )
                ml_dsa_future = executor.submit(
                    self.quantum_security._sign_ml_dsa_internal,
                    qrs2["ml_dsa_keypair_id"],
                    message
                )
                
                ecdsa_signature = ecdsa_future.result()
                ml_dsa_result = ml_dsa_future.result()
            
            if not ml_dsa_result.get("success"):
                return {"success": False, "error": "Falha ao assinar com ML-DSA"}
            
            return {
                "success": True,
                "qrs2_signature": {
                    "ecdsa": ecdsa_signature.hex() if isinstance(ecdsa_signature, bytes) else str(ecdsa_signature),
                    "ml_dsa": ml_dsa_result.get("signature")
                },
                "keypair_id": qrs2_keypair_id,
                "redundancy_level": 2
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

