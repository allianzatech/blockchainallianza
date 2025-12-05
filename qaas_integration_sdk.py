#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔐 SDK DE INTEGRAÇÃO QaaS
SDK para outras blockchains integrarem o Quantum Security Service
"""

import requests
import json
from typing import Dict, Optional, List, Any
from datetime import datetime

class QaaSSDK:
    """
    SDK para integração com Quantum Security as a Service
    
    Exemplo de uso:
        sdk = QaaSSDK(api_url="http://localhost:5009")
        keypair = sdk.generate_keypair("ethereum")
        signature = sdk.sign_transaction("ethereum", tx_hash, keypair["keypair_id"])
    """
    
    def __init__(self, api_url: str = "http://localhost:5009", api_key: Optional[str] = None):
        self.api_url = api_url.rstrip('/')
        self.api_key = api_key
        self.session = requests.Session()
        
        if api_key:
            self.session.headers.update({"Authorization": f"Bearer {api_key}"})
        
        self.session.headers.update({
            "Content-Type": "application/json",
            "User-Agent": "QaaS-SDK/1.0"
        })
    
    def health_check(self) -> Dict[str, Any]:
        """Verificar se o serviço está online"""
        try:
            response = self.session.get(f"{self.api_url}/api/v1/health", timeout=5)
            return response.json()
        except Exception as e:
            return {"status": "error", "error": str(e)}
    
    def generate_keypair(
        self,
        blockchain: str,
        algorithm: str = "ML-DSA-128",
        security_level: int = 3
    ) -> Dict[str, Any]:
        """
        Gerar par de chaves PQC
        
        Args:
            blockchain: Nome da blockchain
            algorithm: Algoritmo PQC
            security_level: Nível de segurança
        
        Returns:
            Dict com keypair_id, public_key, etc.
        """
        payload = {
            "blockchain": blockchain,
            "algorithm": algorithm,
            "security_level": security_level
        }
        
        try:
            response = self.session.post(
                f"{self.api_url}/api/v1/keypair/generate",
                json=payload,
                timeout=30
            )
            return response.json()
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def sign_transaction(
        self,
        blockchain: str,
        transaction_hash: str,
        keypair_id: str,
        algorithm: str = "ML-DSA-128"
    ) -> Dict[str, Any]:
        """
        Assinar hash de transação
        
        Args:
            blockchain: Nome da blockchain
            transaction_hash: Hash SHA-256 da transação
            keypair_id: ID do keypair PQC
            algorithm: Algoritmo PQC
        
        Returns:
            Dict com signature, etc.
        """
        payload = {
            "blockchain": blockchain,
            "transaction_hash": transaction_hash,
            "keypair_id": keypair_id,
            "algorithm": algorithm
        }
        
        try:
            response = self.session.post(
                f"{self.api_url}/api/v1/signature/sign",
                json=payload,
                timeout=30
            )
            return response.json()
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def verify_signature(
        self,
        blockchain: str,
        transaction_hash: str,
        signature: str,
        public_key: str,
        algorithm: str = "ML-DSA-128"
    ) -> Dict[str, Any]:
        """
        Verificar assinatura PQC
        
        Args:
            blockchain: Nome da blockchain
            transaction_hash: Hash SHA-256 da transação
            signature: Assinatura PQC (base64)
            public_key: Chave pública PQC (base64)
            algorithm: Algoritmo PQC
        
        Returns:
            Dict com valid: bool
        """
        payload = {
            "blockchain": blockchain,
            "transaction_hash": transaction_hash,
            "signature": signature,
            "public_key": public_key,
            "algorithm": algorithm
        }
        
        try:
            response = self.session.post(
                f"{self.api_url}/api/v1/signature/verify",
                json=payload,
                timeout=30
            )
            return response.json()
        except Exception as e:
            return {"valid": False, "error": str(e)}
    
    def batch_sign(
        self,
        blockchain: str,
        transactions: List[Dict[str, Any]],
        keypair_id: str,
        algorithm: str = "ML-DSA-128"
    ) -> Dict[str, Any]:
        """
        Assinar múltiplas transações em lote
        
        Args:
            blockchain: Nome da blockchain
            transactions: Lista de {transaction_hash, ...}
            keypair_id: ID do keypair PQC
            algorithm: Algoritmo PQC
        
        Returns:
            Dict com signatures, total, successful, failed
        """
        payload = {
            "blockchain": blockchain,
            "transactions": transactions,
            "keypair_id": keypair_id,
            "algorithm": algorithm
        }
        
        try:
            response = self.session.post(
                f"{self.api_url}/api/v1/signature/batch",
                json=payload,
                timeout=60
            )
            return response.json()
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def get_statistics(self) -> Dict[str, Any]:
        """Obter estatísticas do serviço"""
        try:
            response = self.session.get(f"{self.api_url}/api/v1/statistics", timeout=10)
            return response.json()
        except Exception as e:
            return {"error": str(e)}
    
    def get_supported_blockchains(self) -> Dict[str, Any]:
        """Listar blockchains suportadas"""
        try:
            response = self.session.get(f"{self.api_url}/api/v1/supported/blockchains", timeout=10)
            return response.json()
        except Exception as e:
            return {"error": str(e)}


# ============================================================================
# Exemplo de Integração para Ethereum
# ============================================================================

class EthereumQaaSIntegration:
    """
    Exemplo de integração QaaS para Ethereum
    
    Adiciona assinaturas PQC a transações Ethereum
    """
    
    def __init__(self, qaas_sdk: QaaSSDK, private_key: str):
        self.qaas = qaas_sdk
        self.private_key = private_key
        self.keypair_id = None
        self.blockchain = "ethereum"
    
    def initialize(self) -> bool:
        """Inicializar e gerar keypair PQC"""
        result = self.qaas.generate_keypair(self.blockchain)
        if result.get("success"):
            self.keypair_id = result["keypair_id"]
            return True
        return False
    
    def sign_ethereum_transaction(self, tx_hash: str) -> Dict[str, Any]:
        """
        Assinar transação Ethereum com PQC
        
        Args:
            tx_hash: Hash da transação Ethereum
        
        Returns:
            Dict com signature PQC
        """
        if not self.keypair_id:
            if not self.initialize():
                return {"success": False, "error": "Failed to initialize keypair"}
        
        return self.qaas.sign_transaction(
            self.blockchain,
            tx_hash,
            self.keypair_id
        )
    
    def verify_ethereum_transaction(
        self,
        tx_hash: str,
        pqc_signature: str,
        public_key: str
    ) -> bool:
        """Verificar assinatura PQC de transação Ethereum"""
        result = self.qaas.verify_signature(
            self.blockchain,
            tx_hash,
            pqc_signature,
            public_key
        )
        return result.get("valid", False)


# ============================================================================
# Exemplo de Integração para Polygon
# ============================================================================

class PolygonQaaSIntegration:
    """Exemplo de integração QaaS para Polygon"""
    
    def __init__(self, qaas_sdk: QaaSSDK):
        self.qaas = qaas_sdk
        self.blockchain = "polygon"
        self.keypair_id = None
    
    def initialize(self) -> bool:
        """Inicializar e gerar keypair PQC"""
        result = self.qaas.generate_keypair(self.blockchain)
        if result.get("success"):
            self.keypair_id = result["keypair_id"]
            return True
        return False
    
    def sign_polygon_transaction(self, tx_hash: str) -> Dict[str, Any]:
        """Assinar transação Polygon com PQC"""
        if not self.keypair_id:
            if not self.initialize():
                return {"success": False, "error": "Failed to initialize keypair"}
        
        return self.qaas.sign_transaction(
            self.blockchain,
            tx_hash,
            self.keypair_id
        )


# ============================================================================
# Exemplo de Uso
# ============================================================================

if __name__ == '__main__':
    print("="*70)
    print("🔐 QaaS SDK - Exemplo de Uso")
    print("="*70)
    
    # Inicializar SDK
    sdk = QaaSSDK(api_url="http://localhost:5009")
    
    # Health check
    health = sdk.health_check()
    print(f"✅ Serviço: {health.get('status', 'unknown')}")
    
    # Gerar keypair para Ethereum
    print("\n📝 Gerando keypair para Ethereum...")
    keypair = sdk.generate_keypair("ethereum")
    if keypair.get("success"):
        print(f"✅ Keypair gerado: {keypair['keypair_id']}")
        print(f"   Algorithm: {keypair['algorithm']}")
        print(f"   Real: {keypair.get('real', False)}")
    
    # Assinar transação de exemplo
    if keypair.get("success"):
        print("\n📝 Assinando transação de exemplo...")
        tx_hash = "0x" + "a" * 64  # Hash de exemplo
        signature = sdk.sign_transaction(
            "ethereum",
            tx_hash,
            keypair["keypair_id"]
        )
        if signature.get("success"):
            print(f"✅ Assinatura criada: {signature['signature'][:50]}...")
            print(f"   Real: {signature.get('real', False)}")
    
    # Estatísticas
    print("\n📊 Estatísticas do serviço:")
    stats = sdk.get_statistics()
    print(json.dumps(stats, indent=2))





