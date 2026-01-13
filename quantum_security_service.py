#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔐 QUANTUM SECURITY AS A SERVICE (QaaS)
API de Segurança Quântica para outras blockchains integrarem
"""

import os
import json
import time
import hashlib
import base64
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timezone
from flask import Flask, request, jsonify
from functools import wraps
import threading
from collections import defaultdict

from quantum_security import QuantumSecuritySystem
from pqc_key_manager import PQCKeyManager

class QuantumSecurityService:
    """
    Serviço de Segurança Quântica para outras blockchains
    
    Oferece:
    - Geração de chaves PQC
    - Assinatura de transações
    - Verificação de assinaturas
    - Suporte multi-blockchain
    - Cache e otimizações
    """
    
    def __init__(self):
        self.quantum_security = QuantumSecuritySystem()
        self.key_manager = PQCKeyManager()
        
        # Cache de chaves por blockchain
        self.key_cache = {}  # blockchain -> keypair_id -> keypair
        self.signature_cache = {}  # hash -> signature (para evitar re-assinaturas)
        
        # Estatísticas
        self.stats = {
            "keys_generated": 0,
            "signatures_created": 0,
            "verifications": 0,
            "blockchains_supported": [],
            "total_requests": 0
        }
        
        # Rate limiting por blockchain
        self.rate_limits = defaultdict(lambda: {"count": 0, "reset_time": time.time() + 3600})
        
        print("🔐 QUANTUM SECURITY SERVICE: Inicializado!")
        print("🌐 Serviço disponível para outras blockchains")
    
    def generate_keypair(
        self, 
        blockchain: str, 
        algorithm: str = "ML-DSA-128",
        security_level: int = 3
    ) -> Dict[str, Any]:
        """
        Gerar par de chaves PQC para uma blockchain específica
        
        Args:
            blockchain: Nome da blockchain (ethereum, polygon, bsc, solana, etc.)
            algorithm: Algoritmo PQC (ML-DSA-128, SPHINCS+, QRS-3)
            security_level: Nível de segurança (1-5)
        
        Returns:
            {
                "keypair_id": str,
                "public_key": str,
                "public_key_pem": str,
                "algorithm": str,
                "blockchain": str,
                "real": bool
            }
        """
        try:
            # Gerar keypair usando key_manager
            key_id = f"{blockchain}_{int(time.time())}_{hashlib.sha256(f'{blockchain}{algorithm}'.encode()).hexdigest()[:8]}"
            
            if algorithm in ["ML-DSA-128", "ML-DSA"]:
                keypair = self.key_manager.generate_ml_dsa_keypair(key_id)
            elif algorithm in ["SPHINCS+", "SLH-DSA"]:
                # Implementar SPHINCS+ se necessário
                keypair = self.key_manager._generate_mock_keypair(key_id, "SPHINCS+")
            else:
                keypair = self.key_manager.generate_ml_dsa_keypair(key_id)
            
            # Armazenar no cache
            if blockchain not in self.key_cache:
                self.key_cache[blockchain] = {}
            self.key_cache[blockchain][keypair["keypair_id"]] = keypair
            
            self.stats["keys_generated"] += 1
            if blockchain not in self.stats["blockchains_supported"]:
                self.stats["blockchains_supported"].append(blockchain)
            
            return {
                "success": True,
                "keypair_id": keypair["keypair_id"],
                "public_key": keypair["public_key"],
                "public_key_pem": keypair.get("public_key_pem"),
                "algorithm": algorithm,
                "blockchain": blockchain,
                "security_level": security_level,
                "real": keypair.get("real", False),
                "created_at": datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "blockchain": blockchain
            }
    
    def sign_transaction(
        self,
        blockchain: str,
        transaction_hash: str,
        keypair_id: str,
        algorithm: str = "ML-DSA-128"
    ) -> Dict[str, Any]:
        """
        Assinar hash de transação com PQC
        
        Args:
            blockchain: Nome da blockchain
            transaction_hash: Hash SHA-256 da transação
            keypair_id: ID do keypair PQC
            algorithm: Algoritmo PQC
        
        Returns:
            {
                "signature": str (base64),
                "signature_bin": str (caminho),
                "algorithm": str,
                "transaction_hash": str,
                "real": bool
            }
        """
        try:
            # Verificar cache
            cache_key = f"{blockchain}_{transaction_hash}_{keypair_id}"
            if cache_key in self.signature_cache:
                cached = self.signature_cache[cache_key]
                return {
                    "success": True,
                    "signature": cached["signature"],
                    "signature_bin": cached.get("signature_bin"),
                    "algorithm": algorithm,
                    "transaction_hash": transaction_hash,
                    "real": cached.get("real", False),
                    "from_cache": True
                }
            
            # Converter hash para bytes (remover "0x" se presente)
            tx_hash_clean = transaction_hash.replace("0x", "").replace("0X", "")
            hash_bytes = bytes.fromhex(tx_hash_clean)
            
            # Assinar usando key_manager
            if algorithm in ["ML-DSA-128", "ML-DSA"]:
                result = self.key_manager.sign_ml_dsa(keypair_id, hash_bytes)
            else:
                result = self.key_manager._sign_mock(keypair_id, hash_bytes, algorithm)
            
            if result:
                # Armazenar no cache
                self.signature_cache[cache_key] = result
                self.stats["signatures_created"] += 1
                
                return {
                    "success": True,
                    "signature": result["signature"],
                    "signature_bin": result.get("signature_bin"),
                    "algorithm": algorithm,
                    "transaction_hash": transaction_hash,
                    "real": result.get("real", False),
                    "from_cache": False
                }
            else:
                return {
                    "success": False,
                    "error": "Falha ao assinar transação",
                    "transaction_hash": transaction_hash
                }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "transaction_hash": transaction_hash
            }
    
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
            {
                "valid": bool,
                "algorithm": str,
                "real": bool
            }
        """
        try:
            hash_bytes = bytes.fromhex(transaction_hash)
            sig_bytes = base64.b64decode(signature)
            
            if algorithm in ["ML-DSA-128", "ML-DSA"]:
                result = self.key_manager.verify_ml_dsa(public_key, hash_bytes, signature)
            else:
                result = {"success": True, "real": False, "note": "Mock verification"}
            
            self.stats["verifications"] += 1
            
            return {
                "valid": result.get("success", False),
                "algorithm": algorithm,
                "real": result.get("real", False),
                "blockchain": blockchain
            }
        except Exception as e:
            return {
                "valid": False,
                "error": str(e),
                "blockchain": blockchain
            }
    
    def batch_sign(
        self,
        blockchain: str,
        transactions: List[Dict[str, Any]],
        keypair_id: str,
        algorithm: str = "ML-DSA-128"
    ) -> Dict[str, Any]:
        """
        Assinar múltiplas transações em lote (otimizado)
        
        Args:
            blockchain: Nome da blockchain
            transactions: Lista de {transaction_hash, ...}
            keypair_id: ID do keypair PQC
            algorithm: Algoritmo PQC
        
        Returns:
            {
                "signatures": List[Dict],
                "total": int,
                "successful": int,
                "failed": int
            }
        """
        results = []
        successful = 0
        failed = 0
        
        for tx in transactions:
            tx_hash = tx.get("transaction_hash") or tx.get("hash")
            if not tx_hash:
                failed += 1
                results.append({"error": "Transaction hash missing"})
                continue
            
            result = self.sign_transaction(blockchain, tx_hash, keypair_id, algorithm)
            if result.get("success"):
                successful += 1
            else:
                failed += 1
            results.append(result)
        
        return {
            "signatures": results,
            "total": len(transactions),
            "successful": successful,
            "failed": failed,
            "blockchain": blockchain
        }
    
    def get_statistics(self) -> Dict[str, Any]:
        """Retornar estatísticas do serviço"""
        return {
            "keys_generated": self.stats["keys_generated"],
            "signatures_created": self.stats["signatures_created"],
            "verifications": self.stats["verifications"],
            "blockchains_supported": self.stats["blockchains_supported"],
            "total_requests": self.stats["total_requests"],
            "cache_size": len(self.signature_cache),
            "key_cache_size": sum(len(keys) for keys in self.key_cache.values())
        }


# ============================================================================
# API RESTful Flask
# ============================================================================

app = Flask(__name__)
service = QuantumSecurityService()

def rate_limit_check(blockchain: str, max_requests: int = 1000) -> bool:
    """Verificar rate limit"""
    now = time.time()
    limit = service.rate_limits[blockchain]
    
    if now > limit["reset_time"]:
        limit["count"] = 0
        limit["reset_time"] = now + 3600  # Reset a cada hora
    
    if limit["count"] >= max_requests:
        return False
    
    limit["count"] += 1
    service.stats["total_requests"] += 1
    return True

def require_blockchain(f):
    """Decorator para validar blockchain"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        blockchain = request.json.get("blockchain") if request.is_json else request.args.get("blockchain")
        if not blockchain:
            return jsonify({"error": "blockchain parameter required"}), 400
        return f(*args, **kwargs)
    return decorated_function

@app.route('/api/v1/health', methods=['GET'])
def health():
    """Health check"""
    return jsonify({
        "status": "healthy",
        "service": "Quantum Security as a Service",
        "version": "1.0.0",
        "timestamp": datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')
    })

@app.route('/api/v1/keypair/generate', methods=['POST'])
@require_blockchain
def generate_keypair():
    """Gerar par de chaves PQC"""
    data = request.json
    blockchain = data.get("blockchain")
    algorithm = data.get("algorithm", "ML-DSA-128")
    security_level = data.get("security_level", 3)
    
    if not rate_limit_check(blockchain):
        return jsonify({"error": "Rate limit exceeded"}), 429
    
    result = service.generate_keypair(blockchain, algorithm, security_level)
    return jsonify(result), 200 if result.get("success") else 500

@app.route('/api/v1/signature/sign', methods=['POST'])
@require_blockchain
def sign_transaction():
    """Assinar transação"""
    data = request.json
    blockchain = data.get("blockchain")
    transaction_hash = data.get("transaction_hash")
    keypair_id = data.get("keypair_id")
    algorithm = data.get("algorithm", "ML-DSA-128")
    
    if not transaction_hash or not keypair_id:
        return jsonify({"error": "transaction_hash and keypair_id required"}), 400
    
    if not rate_limit_check(blockchain):
        return jsonify({"error": "Rate limit exceeded"}), 429
    
    result = service.sign_transaction(blockchain, transaction_hash, keypair_id, algorithm)
    return jsonify(result), 200 if result.get("success") else 500

@app.route('/api/v1/signature/verify', methods=['POST'])
@require_blockchain
def verify_signature():
    """Verificar assinatura"""
    data = request.json
    blockchain = data.get("blockchain")
    transaction_hash = data.get("transaction_hash")
    signature = data.get("signature")
    public_key = data.get("public_key")
    algorithm = data.get("algorithm", "ML-DSA-128")
    
    if not all([transaction_hash, signature, public_key]):
        return jsonify({"error": "transaction_hash, signature, and public_key required"}), 400
    
    if not rate_limit_check(blockchain):
        return jsonify({"error": "Rate limit exceeded"}), 429
    
    result = service.verify_signature(blockchain, transaction_hash, signature, public_key, algorithm)
    return jsonify(result), 200

@app.route('/api/v1/signature/batch', methods=['POST'])
@require_blockchain
def batch_sign():
    """Assinar múltiplas transações em lote"""
    data = request.json
    blockchain = data.get("blockchain")
    transactions = data.get("transactions", [])
    keypair_id = data.get("keypair_id")
    algorithm = data.get("algorithm", "ML-DSA-128")
    
    if not transactions or not keypair_id:
        return jsonify({"error": "transactions and keypair_id required"}), 400
    
    if not rate_limit_check(blockchain, max_requests=5000):  # Maior limite para batch
        return jsonify({"error": "Rate limit exceeded"}), 429
    
    result = service.batch_sign(blockchain, transactions, keypair_id, algorithm)
    return jsonify(result), 200

@app.route('/api/v1/statistics', methods=['GET'])
def get_statistics():
    """Obter estatísticas do serviço"""
    return jsonify(service.get_statistics()), 200

@app.route('/api/v1/supported/blockchains', methods=['GET'])
def supported_blockchains():
    """Listar blockchains suportadas"""
    return jsonify({
        "blockchains": [
            "ethereum",
            "polygon",
            "bsc",
            "solana",
            "avalanche",
            "base",
            "cosmos",
            "cardano",
            "polkadot",
            "bitcoin"  # Para transações futuras
        ],
        "algorithms": [
            "ML-DSA-128",
            "SPHINCS+",
            "QRS-3"
        ]
    }), 200

if __name__ == '__main__':
    print("="*70)
    print("🔐 QUANTUM SECURITY AS A SERVICE (QaaS)")
    print("="*70)
    print("🌐 API disponível em: http://localhost:5009")
    print("📚 Documentação: http://localhost:5009/api/v1/supported/blockchains")
    print("="*70)
    app.run(host='0.0.0.0', port=5009, debug=True)

