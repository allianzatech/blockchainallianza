#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🆔 QR-DID - QUANTUM-RESISTANT DECENTRALIZED IDENTITY
Sistema de Identidade Descentralizada Resistente a Quântica
PRIMEIRO NO MUNDO
"""

import json
import hashlib
import time
from datetime import datetime, timezone
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
import base64

try:
    from quantum_security import QuantumSecuritySystem
    from pqc_key_manager import PQCKeyManager
    PQC_AVAILABLE = True
except ImportError:
    PQC_AVAILABLE = False
    QuantumSecuritySystem = None
    PQCKeyManager = None

@dataclass
class QR_DIDDocument:
    """Documento DID quântico-resistente"""
    did: str  # did:allianza:...
    context: List[str]  # ["https://www.w3.org/ns/did/v1"]
    created: str  # ISO 8601
    updated: str  # ISO 8601
    verification_methods: List[Dict]  # Chaves PQC
    authentication: List[str]  # Referências a verification methods
    assertion_method: List[str]  # Para assinaturas
    key_agreement: List[str]  # Para ML-KEM
    service_endpoints: List[Dict]  # Serviços associados
    quantum_signature: Optional[Dict] = None  # Assinatura PQC do documento

class QR_DIDManager:
    """
    Gerenciador de Identidade Descentralizada Quântico-Resistente
    
    Baseado em W3C DID spec com assinaturas PQC (ML-DSA)
    """
    
    def __init__(self, quantum_security: Optional[QuantumSecuritySystem] = None):
        self.quantum_security = quantum_security
        self.pqc_key_manager = None
        
        if PQC_AVAILABLE:
            try:
                if quantum_security:
                    self.quantum_security = quantum_security
                else:
                    self.quantum_security = QuantumSecuritySystem()
                
                self.pqc_key_manager = PQCKeyManager()
                print("✅ QR-DID: PQC disponível")
            except Exception as e:
                print(f"⚠️  QR-DID: PQC não disponível: {e}")
                self.quantum_security = None
                self.pqc_key_manager = None
        
        self.did_registry = {}  # did -> DIDDocument
        self.did_resolver_cache = {}
        
    def generate_did(self, subject: str = None) -> Tuple[str, Dict]:
        """
        Gerar novo DID quântico-resistente
        
        Args:
            subject: Identificador do sujeito (opcional)
            
        Returns:
            (did, keypair_dict)
        """
        # Gerar ID único
        timestamp = int(time.time() * 1000)
        random_part = hashlib.sha256(f"{subject}_{timestamp}_{time.time()}".encode()).hexdigest()[:16]
        did = f"did:allianza:{timestamp}:{random_part}"
        
        # Gerar chaves PQC
        if self.pqc_key_manager:
            try:
                # Gerar par de chaves ML-DSA
                key_id = f"did_key_{timestamp}_{random_part[:8]}"
                keypair_result = self.pqc_key_manager.generate_ml_dsa_keypair(key_id=key_id)
                
                if keypair_result.get("success"):
                    public_key_pem = keypair_result.get("public_key_pem", "")
                    private_key_pem = keypair_result.get("private_key_pem", "")
                    keypair_id = keypair_result.get("keypair_id", key_id)
                    
                    # Criar verification method
                    verification_method_id = f"{did}#keys-1"
                    verification_method = {
                        "id": verification_method_id,
                        "type": "ML-DSA-128",  # NIST PQC
                        "controller": did,
                        "publicKeyPem": public_key_pem,
                        "algorithm": "ML-DSA-128",
                        "nist_standard": True,
                        "quantum_resistant": True
                    }
                    
                    # Criar documento DID
                    now = datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')
                    did_document = QR_DIDDocument(
                        did=did,
                        context=["https://www.w3.org/ns/did/v1"],
                        created=now,
                        updated=now,
                        verification_methods=[verification_method],
                        authentication=[verification_method_id],
                        assertion_method=[verification_method_id],
                        key_agreement=[],  # ML-KEM pode ser adicionado depois
                        service_endpoints=[]
                    )
                    
                    # Assinar documento com PQC
                    signed_doc = self._sign_did_document(did_document)
                    
                    # Registrar
                    self.did_registry[did] = signed_doc
                    
                    return did, {
                        "did": did,
                        "keypair_id": keypair_id,
                        "public_key_pem": public_key_pem,
                        "private_key_pem": private_key_pem,
                        "verification_method_id": verification_method_id,
                        "did_document": asdict(signed_doc),
                        "quantum_resistant": True
                    }
            except Exception as e:
                print(f"⚠️  Erro ao gerar chaves PQC: {e}")
        
        # Fallback: DID sem PQC (não recomendado)
        print("⚠️  Gerando DID sem PQC (fallback)")
        now = datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')
        did_document = QR_DIDDocument(
            did=did,
            context=["https://www.w3.org/ns/did/v1"],
            created=now,
            updated=now,
            verification_methods=[],
            authentication=[],
            assertion_method=[],
            key_agreement=[],
            service_endpoints=[]
        )
        
        self.did_registry[did] = did_document
        
        return did, {
            "did": did,
            "did_document": asdict(did_document),
            "warning": "DID gerado sem PQC - não é quantum-resistant"
        }
    
    def _sign_did_document(self, doc: QR_DIDDocument) -> QR_DIDDocument:
        """Assinar documento DID com PQC"""
        if not self.pqc_key_manager:
            return doc
        
        try:
            # Serializar documento (sem assinatura)
            doc_dict = asdict(doc)
            doc_dict.pop("quantum_signature", None)
            doc_json = json.dumps(doc_dict, sort_keys=True)
            doc_hash = hashlib.sha256(doc_json.encode()).digest()
            
            # Assinar com ML-DSA
            # Nota: Em produção, usar a chave privada do DID
            # Por agora, assinamos com chave temporária para demonstração
            signature_result = self.pqc_key_manager.sign_ml_dsa(
                data=doc_hash,
                private_key_path=None  # Em produção, usar chave do DID
            )
            
            if signature_result.get("success"):
                doc.quantum_signature = {
                    "algorithm": "ML-DSA-128",
                    "signature": signature_result.get("signature_base64"),
                    "created": datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z'),
                    "nist_standard": True
                }
        except Exception as e:
            print(f"⚠️  Erro ao assinar DID: {e}")
        
        return doc
    
    def resolve_did(self, did: str) -> Optional[Dict]:
        """
        Resolver DID para documento
        
        Args:
            did: DID a ser resolvido
            
        Returns:
            DID Document ou None
        """
        # Verificar cache
        if did in self.did_resolver_cache:
            return self.did_resolver_cache[did]
        
        # Resolver do registry
        if did in self.did_registry:
            doc = self.did_registry[did]
            doc_dict = asdict(doc)
            self.did_resolver_cache[did] = doc_dict
            return doc_dict
        
        return None
    
    def verify_did_signature(self, did: str, message: bytes, signature: str) -> bool:
        """
        Verificar assinatura usando chaves do DID
        
        Args:
            did: DID do signatário
            message: Mensagem assinada
            signature: Assinatura (base64)
            
        Returns:
            True se válida
        """
        doc = self.resolve_did(did)
        if not doc:
            return False
        
        # Obter chave pública do DID
        verification_methods = doc.get("verification_methods", [])
        if not verification_methods:
            return False
        
        # Usar primeira chave
        public_key_pem = verification_methods[0].get("publicKeyPem")
        if not public_key_pem:
            return False
        
        # Verificar com PQC
        if self.pqc_key_manager:
            try:
                verify_result = self.pqc_key_manager.verify_ml_dsa(
                    public_key=public_key_pem,
                    data=message,
                    signature_base64=signature
                )
                return verify_result
            except Exception as e:
                print(f"⚠️  Erro ao verificar assinatura: {e}")
                return False
        
        return False
    
    def add_service_endpoint(self, did: str, service_type: str, endpoint: str) -> bool:
        """Adicionar service endpoint ao DID"""
        if did not in self.did_registry:
            return False
        
        doc = self.did_registry[did]
        service = {
            "id": f"{did}#{service_type}",
            "type": service_type,
            "serviceEndpoint": endpoint
        }
        
        doc.service_endpoints.append(service)
        doc.updated = datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')
        
        # Re-assinar
        doc = self._sign_did_document(doc)
        self.did_registry[did] = doc
        
        return True
    
    def export_did_document(self, did: str) -> Optional[str]:
        """Exportar DID document como JSON"""
        doc = self.resolve_did(did)
        if not doc:
            return None
        
        return json.dumps(doc, indent=2, ensure_ascii=False)
    
    def get_all_dids(self) -> List[str]:
        """Listar todos os DIDs registrados"""
        return list(self.did_registry.keys())

if __name__ == '__main__':
    print("="*70)
    print("🆔 QR-DID - QUANTUM-RESISTANT DECENTRALIZED IDENTITY")
    print("="*70)
    
    # Inicializar
    manager = QR_DIDManager()
    
    # Gerar DID
    print("\n📋 Gerando QR-DID...")
    did, keypair = manager.generate_did(subject="test_user")
    print(f"✅ DID gerado: {did}")
    print(f"✅ Chaves PQC: {'Sim' if keypair.get('public_key_pem') else 'Não'}")
    
    # Resolver DID
    print("\n📋 Resolvendo DID...")
    doc = manager.resolve_did(did)
    if doc:
        print(f"✅ DID resolvido: {doc['did']}")
        print(f"✅ Verification methods: {len(doc.get('verification_methods', []))}")
        print(f"✅ Quantum signature: {'Sim' if doc.get('quantum_signature') else 'Não'}")
    
    # Exportar
    print("\n📋 Exportando DID document...")
    json_doc = manager.export_did_document(did)
    if json_doc:
        print("✅ DID document exportado:")
        print(json_doc[:500] + "..." if len(json_doc) > 500 else json_doc)

