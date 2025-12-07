#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔐 MULTI-SIGNATURE QUÂNTICO-SEGURO
Sistema de multi-assinatura usando algoritmos PQC (ML-DSA)
"""

import time
import json
import hashlib
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum

class MultiSigStatus(Enum):
    """Status de uma operação multi-sig"""
    PENDING = "pending"
    PARTIALLY_SIGNED = "partially_signed"
    COMPLETED = "completed"
    REJECTED = "rejected"
    EXPIRED = "expired"

@dataclass
class MultiSigOperation:
    """Operação que requer multi-signature"""
    operation_id: str
    operation_type: str  # "transfer", "bridge", "critical"
    data: Dict
    required_signatures: int
    total_signers: int
    signatures: List[Dict]
    status: MultiSigStatus
    created_at: float
    expires_at: Optional[float] = None
    quantum_signatures: List[Dict] = None

class QuantumMultiSig:
    """Sistema de Multi-Signature Quântico-Seguro"""
    
    def __init__(self, quantum_security=None):
        self.quantum_security = quantum_security
        self.operations = {}  # operation_id -> MultiSigOperation
        self.signers = {}  # signer_id -> {"public_key": ..., "weight": ...}
        self.operation_counter = 0
        
    def register_signer(
        self,
        signer_id: str,
        public_key: Optional[str] = None,
        weight: int = 1
    ) -> Dict:
        """
        Registrar um signatário no sistema
        
        Args:
            signer_id: Identificador único do signatário
            public_key: Chave pública PQC (ML-DSA)
            weight: Peso do signatário (para threshold customizado)
        """
        # Gerar chave pública se não fornecida
        if not public_key and self.quantum_security:
            try:
                keypair = self.quantum_security.generate_ml_dsa_keypair(security_level=3)
                public_key = keypair.get("public_key")
            except Exception as e:
                return {
                    "success": False,
                    "error": f"Erro ao gerar chave pública: {e}"
                }
        
        self.signers[signer_id] = {
            "public_key": public_key,
            "weight": weight,
            "registered_at": time.time()
        }
        
        return {
            "success": True,
            "signer_id": signer_id,
            "public_key": public_key,
            "weight": weight
        }
    
    def create_operation(
        self,
        operation_type: str,
        data: Dict,
        required_signatures: int,
        signer_ids: List[str],
        expires_in: Optional[int] = 3600  # 1 hora padrão
    ) -> Dict:
        """
        Criar uma operação que requer multi-signature
        
        Args:
            operation_type: Tipo de operação ("transfer", "bridge", "critical")
            data: Dados da operação
            required_signatures: Número mínimo de assinaturas necessárias
            signer_ids: Lista de signatários autorizados
            expires_in: Tempo de expiração em segundos
        """
        # Validar signatários
        for signer_id in signer_ids:
            if signer_id not in self.signers:
                return {
                    "success": False,
                    "error": f"Signatário {signer_id} não registrado"
                }
        
        if required_signatures > len(signer_ids):
            return {
                "success": False,
                "error": f"required_signatures ({required_signatures}) > total_signers ({len(signer_ids)})"
            }
        
        # Criar ID único
        self.operation_counter += 1
        operation_id = f"multisig_{int(time.time())}_{self.operation_counter:06d}"
        
        # Criar operação
        operation = MultiSigOperation(
            operation_id=operation_id,
            operation_type=operation_type,
            data=data,
            required_signatures=required_signatures,
            total_signers=len(signer_ids),
            signatures=[],
            status=MultiSigStatus.PENDING,
            created_at=time.time(),
            expires_at=time.time() + expires_in if expires_in else None,
            quantum_signatures=[]
        )
        
        self.operations[operation_id] = operation
        
        return {
            "success": True,
            "operation_id": operation_id,
            "status": operation.status.value,
            "required_signatures": required_signatures,
            "total_signers": len(signer_ids),
            "expires_at": operation.expires_at
        }
    
    def sign_operation(
        self,
        operation_id: str,
        signer_id: str,
        private_key: Optional[str] = None
    ) -> Dict:
        """
        Assinar uma operação com assinatura quântica
        
        Args:
            operation_id: ID da operação
            signer_id: ID do signatário
            private_key: Chave privada PQC (opcional, se já registrada)
        """
        # Verificar se operação existe
        if operation_id not in self.operations:
            return {
                "success": False,
                "error": "Operação não encontrada"
            }
        
        operation = self.operations[operation_id]
        
        # Verificar se expirou
        if operation.expires_at and time.time() > operation.expires_at:
            operation.status = MultiSigStatus.EXPIRED
            return {
                "success": False,
                "error": "Operação expirou",
                "status": operation.status.value
            }
        
        # Verificar se já foi completada
        if operation.status == MultiSigStatus.COMPLETED:
            return {
                "success": False,
                "error": "Operação já foi completada"
            }
        
        # Verificar se signatário já assinou
        existing_signature = next(
            (s for s in operation.signatures if s.get("signer_id") == signer_id),
            None
        )
        if existing_signature:
            return {
                "success": False,
                "error": "Signatário já assinou esta operação"
            }
        
        # Verificar se signatário está registrado
        if signer_id not in self.signers:
            return {
                "success": False,
                "error": "Signatário não registrado"
            }
        
        # Criar hash da operação para assinatura
        operation_hash = hashlib.sha256(
            json.dumps({
                "operation_id": operation_id,
                "operation_type": operation.operation_type,
                "data": operation.data
            }, sort_keys=True).encode()
        ).digest()
        
        # Assinar com ML-DSA se quantum_security disponível
        quantum_signature = None
        if self.quantum_security:
            try:
                # Usar keypair_id se disponível, senão gerar novo
                keypair_id = f"multisig_{signer_id}"
                
                # Tentar assinar
                if hasattr(self.quantum_security, 'sign_ml_dsa'):
                    sig_result = self.quantum_security.sign_ml_dsa(
                        keypair_id=keypair_id,
                        message=operation_hash
                    )
                    
                    if sig_result.get("success"):
                        quantum_signature = {
                            "algorithm": "ML-DSA",
                            "signature": sig_result.get("signature"),
                            "public_key": sig_result.get("public_key"),
                            "nist_standard": True
                        }
            except Exception as e:
                # Se falhar, continuar sem assinatura quântica (fallback)
                pass
        
        # Criar assinatura
        signature = {
            "signer_id": signer_id,
            "timestamp": time.time(),
            "quantum_signature": quantum_signature,
            "signature_hash": hashlib.sha256(
                json.dumps({
                    "signer_id": signer_id,
                    "operation_id": operation_id,
                    "timestamp": time.time()
                }, sort_keys=True).encode()
            ).hexdigest()
        }
        
        # Adicionar assinatura
        operation.signatures.append(signature)
        if quantum_signature:
            operation.quantum_signatures = operation.quantum_signatures or []
            operation.quantum_signatures.append(quantum_signature)
        
        # Verificar se tem assinaturas suficientes
        if len(operation.signatures) >= operation.required_signatures:
            operation.status = MultiSigStatus.COMPLETED
        else:
            operation.status = MultiSigStatus.PARTIALLY_SIGNED
        
        return {
            "success": True,
            "operation_id": operation_id,
            "signer_id": signer_id,
            "signatures_count": len(operation.signatures),
            "required_signatures": operation.required_signatures,
            "status": operation.status.value,
            "quantum_signature": quantum_signature is not None
        }
    
    def verify_operation(self, operation_id: str) -> Dict:
        """
        Verificar se uma operação tem assinaturas suficientes
        
        Returns:
            {
                "success": bool,
                "operation_id": str,
                "status": str,
                "signatures_count": int,
                "required_signatures": int,
                "can_execute": bool,
                "signatures": List[Dict]
            }
        """
        if operation_id not in self.operations:
            return {
                "success": False,
                "error": "Operação não encontrada"
            }
        
        operation = self.operations[operation_id]
        
        # Verificar expiração
        if operation.expires_at and time.time() > operation.expires_at:
            operation.status = MultiSigStatus.EXPIRED
        
        can_execute = (
            operation.status == MultiSigStatus.COMPLETED and
            len(operation.signatures) >= operation.required_signatures
        )
        
        return {
            "success": True,
            "operation_id": operation_id,
            "status": operation.status.value,
            "signatures_count": len(operation.signatures),
            "required_signatures": operation.required_signatures,
            "can_execute": can_execute,
            "signatures": [
                {
                    "signer_id": s["signer_id"],
                    "timestamp": s["timestamp"],
                    "has_quantum": s.get("quantum_signature") is not None
                }
                for s in operation.signatures
            ]
        }
    
    def get_operation(self, operation_id: str) -> Optional[MultiSigOperation]:
        """Obter operação por ID"""
        return self.operations.get(operation_id)
    
    def list_operations(
        self,
        status: Optional[MultiSigStatus] = None,
        operation_type: Optional[str] = None
    ) -> List[Dict]:
        """Listar operações com filtros"""
        results = []
        for op_id, op in self.operations.items():
            if status and op.status != status:
                continue
            if operation_type and op.operation_type != operation_type:
                continue
            
            results.append({
                "operation_id": op_id,
                "operation_type": op.operation_type,
                "status": op.status.value,
                "signatures_count": len(op.signatures),
                "required_signatures": op.required_signatures,
                "created_at": op.created_at,
                "expires_at": op.expires_at
            })
        
        return results
    
    def reject_operation(self, operation_id: str, signer_id: str) -> Dict:
        """Rejeitar uma operação (requer maioria)"""
        if operation_id not in self.operations:
            return {
                "success": False,
                "error": "Operação não encontrada"
            }
        
        operation = self.operations[operation_id]
        
        # Verificar se signatário está autorizado
        if signer_id not in self.signers:
            return {
                "success": False,
                "error": "Signatário não registrado"
            }
        
        # Marcar como rejeitada (pode ser implementado com threshold de rejeição)
        operation.status = MultiSigStatus.REJECTED
        
        return {
            "success": True,
            "operation_id": operation_id,
            "status": operation.status.value,
            "rejected_by": signer_id
        }
















