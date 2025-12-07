#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔐 MULTI-SIG QUÂNTICO
Sistema de multi-assinatura usando PQC (Post-Quantum Cryptography)
"""

import hashlib
import json
import time
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from datetime import datetime

# Placeholder para quantum_security
try:
    from quantum_security import QuantumSecuritySystem
except ImportError:
    class QuantumSecuritySystem:
        def sign_ml_dsa(self, keypair_id, data): 
            return {"success": True, "signature": f"mock_sig_{data.hex()[:20]}"}
        def verify_ml_dsa(self, public_key, data, signature): 
            return {"success": True}
        def generate_ml_dsa_keypair(self, security_level): 
            return {"keypair_id": "mock_keypair", "public_key": "mock_pubkey"}

@dataclass
class Signer:
    """Signatário no multi-sig"""
    signer_id: str
    public_key: str
    algorithm: str  # "ML-DSA-128" | "SLH-DSA-SHA2-128s"
    keypair_id: Optional[str] = None
    weight: int = 1  # Peso do signatário (para threshold)

@dataclass
class MultisigPolicy:
    """Política de multi-sig"""
    policy_id: str
    threshold: int  # m-of-n
    signers: List[Signer]
    algorithm_preference: str = "ML-DSA-128"
    require_dual_algorithm: bool = False  # Exigir 2 algoritmos diferentes

@dataclass
class MultisigSignature:
    """Assinatura individual de um signatário"""
    signer_id: str
    public_key: str
    algorithm: str
    signature: str
    timestamp: str
    signed_data_hash: str

class QuantumMultisig:
    """
    Sistema de Multi-Sig Quântico
    
    Suporta:
    - Threshold signatures (m-of-n)
    - Múltiplos algoritmos PQC
    - Agregação de assinaturas
    - Verificação individual e agregada
    """
    
    def __init__(self, quantum_security: Optional[QuantumSecuritySystem] = None):
        self.quantum_security = quantum_security
        self.policies: Dict[str, MultisigPolicy] = {}
        self.signers: Dict[str, Signer] = {}
        self.signatures: Dict[str, List[MultisigSignature]] = {}  # transaction_id -> signatures
    
    def create_policy(
        self,
        policy_id: str,
        threshold: int,
        signers: List[Signer],
        algorithm_preference: str = "ML-DSA-128",
        require_dual_algorithm: bool = False
    ) -> MultisigPolicy:
        """Criar política de multi-sig"""
        if threshold > len(signers):
            raise ValueError(f"Threshold ({threshold}) cannot exceed number of signers ({len(signers)})")
        
        policy = MultisigPolicy(
            policy_id=policy_id,
            threshold=threshold,
            signers=signers,
            algorithm_preference=algorithm_preference,
            require_dual_algorithm=require_dual_algorithm
        )
        
        self.policies[policy_id] = policy
        
        # Registrar signers
        for signer in signers:
            self.signers[signer.signer_id] = signer
        
        return policy
    
    def add_signer(
        self,
        signer_id: str,
        public_key: str,
        algorithm: str = "ML-DSA-128",
        keypair_id: Optional[str] = None,
        weight: int = 1
    ) -> Signer:
        """Adicionar signatário"""
        signer = Signer(
            signer_id=signer_id,
            public_key=public_key,
            algorithm=algorithm,
            keypair_id=keypair_id,
            weight=weight
        )
        self.signers[signer_id] = signer
        return signer
    
    def sign_transaction(
        self,
        transaction_id: str,
        data_to_sign: bytes,
        signer_id: str,
        keypair_id: Optional[str] = None
    ) -> Optional[MultisigSignature]:
        """
        Assinar transação com PQC
        
        Args:
            transaction_id: ID único da transação
            data_to_sign: Dados a assinar (geralmente hash)
            signer_id: ID do signatário
            keypair_id: ID do keypair (se não fornecido, busca do signer)
        
        Returns:
            MultisigSignature ou None se falhar
        """
        if signer_id not in self.signers:
            return None
        
        signer = self.signers[signer_id]
        
        if not self.quantum_security:
            # Modo mock
            signature_data = f"mock_sig_{signer_id}_{data_to_sign.hex()[:20]}"
            algorithm = signer.algorithm
        else:
            # Assinar com PQC real
            kp_id = keypair_id or signer.keypair_id
            if not kp_id:
                return None
            
            result = self.quantum_security.sign_ml_dsa(kp_id, data_to_sign)
            if not result.get("success"):
                return None
            
            signature_data = result.get("signature")
            algorithm = signer.algorithm
        
        data_hash = hashlib.sha256(data_to_sign).hexdigest()
        
        multisig_sig = MultisigSignature(
            signer_id=signer_id,
            public_key=signer.public_key,
            algorithm=algorithm,
            signature=signature_data,
            timestamp=datetime.utcnow().isoformat() + "Z",
            signed_data_hash=data_hash
        )
        
        # Armazenar assinatura
        if transaction_id not in self.signatures:
            self.signatures[transaction_id] = []
        self.signatures[transaction_id].append(multisig_sig)
        
        return multisig_sig
    
    def verify_signature(
        self,
        signature: MultisigSignature,
        data_to_verify: bytes
    ) -> bool:
        """Verificar assinatura individual"""
        if not self.quantum_security:
            # Modo mock - sempre retorna True
            return True
        
        data_hash = hashlib.sha256(data_to_verify).hexdigest()
        if signature.signed_data_hash != data_hash:
            return False
        
        try:
            result = self.quantum_security.verify_ml_dsa(
                signature.public_key,
                data_to_verify,
                signature.signature
            )
            return result.get("success", False)
        except:
            return False
    
    def verify_multisig(
        self,
        transaction_id: str,
        policy_id: str,
        data_to_verify: bytes
    ) -> Dict[str, Any]:
        """
        Verificar multi-sig completo
        
        Returns:
            Dict com resultado da verificação
        """
        if policy_id not in self.policies:
            return {
                "verified": False,
                "error": "Policy not found"
            }
        
        policy = self.policies[policy_id]
        
        if transaction_id not in self.signatures:
            return {
                "verified": False,
                "error": "No signatures found for transaction",
                "signatures_count": 0,
                "required": policy.threshold
            }
        
        signatures = self.signatures[transaction_id]
        
        # Verificar cada assinatura
        valid_signatures = []
        invalid_signatures = []
        algorithms_used = set()
        
        for sig in signatures:
            if self.verify_signature(sig, data_to_verify):
                valid_signatures.append(sig)
                algorithms_used.add(sig.algorithm)
            else:
                invalid_signatures.append(sig.signer_id)
        
        # Verificar threshold
        total_weight = sum(s.weight for s in policy.signers if s.signer_id in [vs.signer_id for vs in valid_signatures])
        threshold_met = total_weight >= policy.threshold
        
        # Verificar dual algorithm (se exigido)
        dual_algorithm_met = True
        if policy.require_dual_algorithm:
            dual_algorithm_met = len(algorithms_used) >= 2
        
        verified = threshold_met and dual_algorithm_met
        
        return {
            "verified": verified,
            "transaction_id": transaction_id,
            "policy_id": policy_id,
            "threshold_met": threshold_met,
            "dual_algorithm_met": dual_algorithm_met,
            "valid_signatures_count": len(valid_signatures),
            "invalid_signatures_count": len(invalid_signatures),
            "total_weight": total_weight,
            "required_threshold": policy.threshold,
            "algorithms_used": list(algorithms_used),
            "valid_signers": [s.signer_id for s in valid_signatures],
            "invalid_signers": invalid_signatures,
            "signatures": [asdict(s) for s in valid_signatures]
        }
    
    def aggregate_signatures(
        self,
        transaction_id: str
    ) -> Dict[str, Any]:
        """
        Agregar assinaturas em formato compacto
        
        Returns:
            Dict com assinaturas agregadas
        """
        if transaction_id not in self.signatures:
            return {
                "error": "No signatures found"
            }
        
        signatures = self.signatures[transaction_id]
        
        aggregated = {
            "transaction_id": transaction_id,
            "signatures_count": len(signatures),
            "algorithms": list(set(s.algorithm for s in signatures)),
            "signers": [s.signer_id for s in signatures],
            "aggregated_at": datetime.utcnow().isoformat() + "Z",
            "signatures": [asdict(s) for s in signatures]
        }
        
        return aggregated
    
    def export_policy(self, policy_id: str) -> Dict[str, Any]:
        """Exportar política para JSON"""
        if policy_id not in self.policies:
            return {"error": "Policy not found"}
        
        policy = self.policies[policy_id]
        return {
            "policy_id": policy.policy_id,
            "threshold": policy.threshold,
            "algorithm_preference": policy.algorithm_preference,
            "require_dual_algorithm": policy.require_dual_algorithm,
            "signers": [asdict(s) for s in policy.signers],
            "exported_at": datetime.utcnow().isoformat() + "Z"
        }
















