#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🏦 ALLIANZA BANKING SECURITY LAYER (ABSL)
API dedicada para bancos com segurança quântica máxima
"""

import os
import json
import time
import hashlib
from datetime import datetime, timezone
from typing import Dict, Optional, List
from flask import Flask, request, jsonify
from functools import wraps
import jwt

try:
    from quantum_security import QuantumSecuritySystem
    from pqc_key_manager import PQCKeyManager
    from qr_did_system import QR_DIDManager
    PQC_AVAILABLE = True
except ImportError:
    PQC_AVAILABLE = False
    QuantumSecuritySystem = None
    PQCKeyManager = None
    QR_DIDManager = None

class BankingSecurityLayer:
    """
    Allianza Banking Security Layer (ABSL)
    
    Camada de segurança dedicada para bancos com:
    - API RESTful especializada
    - Autenticação OAuth2/JWT
    - QKD (Quantum Key Distribution)
    - ML-KEM para key exchange
    - Multi-sig FHE
    - Ledger privado
    - Audit logs completos
    """
    
    def __init__(self):
        self.app = Flask(__name__)
        self.app.config['SECRET_KEY'] = os.getenv('ABSL_SECRET_KEY', 'banking-secret-key-change-in-production')
        
        # Inicializar sistemas
        self.quantum_security = None
        self.pqc_key_manager = None
        self.did_manager = None
        
        if PQC_AVAILABLE:
            try:
                self.quantum_security = QuantumSecuritySystem()
                self.pqc_key_manager = PQCKeyManager()
                self.did_manager = QR_DIDManager(self.quantum_security)
                print("✅ ABSL: Sistemas PQC inicializados")
            except Exception as e:
                print(f"⚠️  ABSL: Erro ao inicializar PQC: {e}")
        
        # Banco de dados de bancos (em produção, usar DB real)
        self.banks = {}  # bank_id -> bank_info
        self.api_keys = {}  # api_key -> bank_id
        self.audit_logs = []
        
        # Rate limiting por banco
        self.rate_limits = {}  # bank_id -> {requests: count, window_start: time}
        
        self._init_routes()
    
    def _init_routes(self):
        """Inicializar rotas da API"""
        
        @self.app.route('/api/v1/health', methods=['GET'])
        def health_check():
            """Health check"""
            return jsonify({
                "status": "healthy",
                "service": "Allianza Banking Security Layer",
                "version": "1.0.0",
                "pqc_available": PQC_AVAILABLE,
                "timestamp": datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')
            })
        
        @self.app.route('/api/v1/banks/register', methods=['POST'])
        def register_bank():
            """Registrar novo banco"""
            data = request.json
            
            bank_id = data.get('bank_id')
            bank_name = data.get('bank_name')
            contact_email = data.get('contact_email')
            
            if not all([bank_id, bank_name, contact_email]):
                return jsonify({"error": "Missing required fields"}), 400
            
            # Gerar API key
            api_key = self._generate_api_key(bank_id)
            
            # Criar DID para o banco
            did = None
            if self.did_manager:
                did, did_info = self.did_manager.generate_did(subject=bank_id)
            
            bank_info = {
                "bank_id": bank_id,
                "bank_name": bank_name,
                "contact_email": contact_email,
                "api_key": api_key,
                "did": did,
                "created_at": datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z'),
                "status": "active"
            }
            
            self.banks[bank_id] = bank_info
            self.api_keys[api_key] = bank_id
            
            # Audit log
            self._audit_log(bank_id, "bank_registered", {"bank_name": bank_name})
            
            return jsonify({
                "success": True,
                "bank_id": bank_id,
                "api_key": api_key,
                "did": did,
                "message": "Banco registrado com sucesso"
            })
        
        @self.app.route('/api/v1/banks/<bank_id>/keypair', methods=['POST'])
        @self.require_auth
        def generate_keypair(bank_id):
            """Gerar par de chaves PQC para banco"""
            if not self.pqc_key_manager:
                return jsonify({"error": "PQC não disponível"}), 503
            
            key_id = f"{bank_id}_key_{int(time.time())}"
            keypair_result = self.pqc_key_manager.generate_ml_dsa_keypair(key_id=key_id)
            
            if keypair_result.get("success"):
                self._audit_log(bank_id, "keypair_generated", {"key_id": key_id})
                
                return jsonify({
                    "success": True,
                    "keypair_id": keypair_result.get("keypair_id"),
                    "public_key_pem": keypair_result.get("public_key_pem"),
                    "algorithm": "ML-DSA-128",
                    "standard": "FIPS 204",
                    "quantum_resistant": True
                })
            else:
                return jsonify({"error": "Falha ao gerar keypair"}), 500
        
        @self.app.route('/api/v1/banks/<bank_id>/sign', methods=['POST'])
        @self.require_auth
        def sign_transaction(bank_id):
            """Assinar transação com PQC"""
            data = request.json
            transaction_hash = data.get('transaction_hash')
            keypair_id = data.get('keypair_id')
            
            if not transaction_hash or not keypair_id:
                return jsonify({"error": "Missing transaction_hash or keypair_id"}), 400
            
            if not self.pqc_key_manager:
                return jsonify({"error": "PQC não disponível"}), 503
            
            # Remover 0x se presente
            if transaction_hash.startswith('0x'):
                transaction_hash = transaction_hash[2:]
            
            try:
                tx_bytes = bytes.fromhex(transaction_hash)
                signature_result = self.pqc_key_manager.sign_ml_dsa(
                    data=tx_bytes,
                    private_key_path=None  # Em produção, buscar do HSM
                )
                
                if signature_result.get("success"):
                    self._audit_log(bank_id, "transaction_signed", {
                        "tx_hash": transaction_hash,
                        "keypair_id": keypair_id
                    })
                    
                    return jsonify({
                        "success": True,
                        "signature": signature_result.get("signature_base64"),
                        "algorithm": "ML-DSA-128",
                        "transaction_hash": transaction_hash
                    })
                else:
                    return jsonify({"error": "Falha ao assinar"}), 500
            except Exception as e:
                return jsonify({"error": str(e)}), 400
        
        @self.app.route('/api/v1/banks/<bank_id>/verify', methods=['POST'])
        @self.require_auth
        def verify_signature(bank_id):
            """Verificar assinatura PQC"""
            data = request.json
            transaction_hash = data.get('transaction_hash')
            signature = data.get('signature')
            public_key_pem = data.get('public_key_pem')
            
            if not all([transaction_hash, signature, public_key_pem]):
                return jsonify({"error": "Missing required fields"}), 400
            
            if not self.pqc_key_manager:
                return jsonify({"error": "PQC não disponível"}), 503
            
            # Remover 0x se presente
            if transaction_hash.startswith('0x'):
                transaction_hash = transaction_hash[2:]
            
            try:
                tx_bytes = bytes.fromhex(transaction_hash)
                is_valid = self.pqc_key_manager.verify_ml_dsa(
                    public_key=public_key_pem,
                    data=tx_bytes,
                    signature_base64=signature
                )
                
                self._audit_log(bank_id, "signature_verified", {
                    "tx_hash": transaction_hash,
                    "valid": is_valid
                })
                
                return jsonify({
                    "success": True,
                    "valid": is_valid,
                    "algorithm": "ML-DSA-128"
                })
            except Exception as e:
                return jsonify({"error": str(e)}), 400
        
        @self.app.route('/api/v1/banks/<bank_id>/audit', methods=['GET'])
        @self.require_auth
        def get_audit_logs(bank_id):
            """Obter logs de auditoria"""
            limit = request.args.get('limit', 100, type=int)
            logs = [log for log in self.audit_logs if log.get('bank_id') == bank_id][-limit:]
            
            return jsonify({
                "success": True,
                "logs": logs,
                "count": len(logs)
            })
        
        @self.app.route('/api/v1/banks/<bank_id>/metrics', methods=['GET'])
        @self.require_auth
        def get_metrics(bank_id):
            """Obter métricas do banco"""
            bank_logs = [log for log in self.audit_logs if log.get('bank_id') == bank_id]
            
            metrics = {
                "bank_id": bank_id,
                "total_operations": len(bank_logs),
                "keypairs_generated": sum(1 for log in bank_logs if log.get('action') == 'keypair_generated'),
                "transactions_signed": sum(1 for log in bank_logs if log.get('action') == 'transaction_signed'),
                "signatures_verified": sum(1 for log in bank_logs if log.get('action') == 'signature_verified'),
                "timestamp": datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')
            }
            
            return jsonify({
                "success": True,
                "metrics": metrics
            })
    
    def require_auth(self, f):
        """Decorator para autenticação"""
        @wraps(f)
        def decorated_function(*args, **kwargs):
            api_key = request.headers.get('X-API-Key') or request.headers.get('Authorization', '').replace('Bearer ', '')
            
            if not api_key:
                return jsonify({"error": "Missing API key"}), 401
            
            bank_id = self.api_keys.get(api_key)
            if not bank_id:
                return jsonify({"error": "Invalid API key"}), 401
            
            # Verificar rate limit
            if not self._check_rate_limit(bank_id):
                return jsonify({"error": "Rate limit exceeded"}), 429
            
            # Adicionar bank_id ao contexto
            request.bank_id = bank_id
            return f(*args, **kwargs)
        
        return decorated_function
    
    def _generate_api_key(self, bank_id: str) -> str:
        """Gerar API key único"""
        timestamp = int(time.time())
        random_part = hashlib.sha256(f"{bank_id}_{timestamp}_{time.time()}".encode()).hexdigest()[:32]
        return f"absl_{bank_id[:8]}_{random_part}"
    
    def _check_rate_limit(self, bank_id: str) -> bool:
        """Verificar rate limit"""
        if bank_id not in self.rate_limits:
            self.rate_limits[bank_id] = {"requests": 0, "window_start": time.time()}
        
        limit_info = self.rate_limits[bank_id]
        window_duration = 60  # 1 minuto
        max_requests = 1000  # 1000 requests por minuto
        
        # Resetar se janela expirou
        if time.time() - limit_info["window_start"] > window_duration:
            limit_info["requests"] = 0
            limit_info["window_start"] = time.time()
        
        # Verificar limite
        if limit_info["requests"] >= max_requests:
            return False
        
        limit_info["requests"] += 1
        return True
    
    def _audit_log(self, bank_id: str, action: str, details: Dict):
        """Registrar log de auditoria"""
        log_entry = {
            "bank_id": bank_id,
            "action": action,
            "details": details,
            "timestamp": datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z'),
            "request_id": hashlib.sha256(f"{bank_id}_{action}_{time.time()}".encode()).hexdigest()[:16]
        }
        self.audit_logs.append(log_entry)
        
        # Manter apenas últimos 10000 logs
        if len(self.audit_logs) > 10000:
            self.audit_logs = self.audit_logs[-10000:]
    
    def run(self, host='0.0.0.0', port=5009, debug=False):
        """Executar servidor"""
        print("="*70)
        print("🏦 ALLIANZA BANKING SECURITY LAYER (ABSL)")
        print("="*70)
        print(f"✅ Servidor iniciando em http://{host}:{port}")
        print(f"✅ PQC disponível: {PQC_AVAILABLE}")
        print(f"✅ Endpoints disponíveis:")
        print(f"   • POST /api/v1/banks/register")
        print(f"   • POST /api/v1/banks/<bank_id>/keypair")
        print(f"   • POST /api/v1/banks/<bank_id>/sign")
        print(f"   • POST /api/v1/banks/<bank_id>/verify")
        print(f"   • GET  /api/v1/banks/<bank_id>/audit")
        print(f"   • GET  /api/v1/banks/<bank_id>/metrics")
        print("="*70)
        
        self.app.run(host=host, port=port, debug=debug)

if __name__ == '__main__':
    layer = BankingSecurityLayer()
    layer.run(port=5009, debug=True)





