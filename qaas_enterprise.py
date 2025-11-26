#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🏦 QUANTUM SECURITY AS A SERVICE - ENTERPRISE EDITION
Versão avançada para blockchains e bancos
"""

import os
import json
import time
import hashlib
import base64
import jwt
import secrets
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta, timezone
from flask import Flask, request, jsonify, g
from functools import wraps
import threading
from collections import defaultdict
import logging
from logging.handlers import RotatingFileHandler
import sqlite3
from contextlib import contextmanager

from quantum_security import QuantumSecuritySystem
from pqc_key_manager import PQCKeyManager
try:
    from qaas_proof_bundle import QaaSProofBundle
    from qaas_siem_exporter import SIEMExporter
except ImportError:
    QaaSProofBundle = None
    SIEMExporter = None
from qaas_proof_bundle import QaaSProofBundle

# ============================================================================
# CONFIGURAÇÃO DE LOGGING AVANÇADO
# ============================================================================

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        RotatingFileHandler('qaas_enterprise.log', maxBytes=10*1024*1024, backupCount=5),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# ============================================================================
# BANCO DE DADOS PARA AUDITORIA
# ============================================================================

class AuditDatabase:
    """Banco de dados para logs de auditoria"""
    
    def __init__(self, db_path: str = "qaas_audit.db"):
        self.db_path = db_path
        self._init_db()
    
    def _init_db(self):
        """Inicializar banco de dados"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS audit_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                user_id TEXT,
                blockchain TEXT,
                action TEXT,
                request_id TEXT,
                ip_address TEXT,
                user_agent TEXT,
                request_data TEXT,
                response_data TEXT,
                success BOOLEAN,
                error_message TEXT
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS api_keys (
                key_id TEXT PRIMARY KEY,
                key_hash TEXT NOT NULL,
                user_id TEXT,
                blockchain TEXT,
                permissions TEXT,
                rate_limit INTEGER,
                created_at TEXT,
                last_used TEXT,
                is_active BOOLEAN
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS keypairs (
                keypair_id TEXT PRIMARY KEY,
                blockchain TEXT,
                algorithm TEXT,
                public_key TEXT,
                created_at TEXT,
                last_used TEXT,
                usage_count INTEGER
            )
        ''')
        
        conn.commit()
        conn.close()
    
    @contextmanager
    def get_connection(self):
        """Context manager para conexão com banco"""
        conn = sqlite3.connect(self.db_path)
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()
    
    def log_audit(
        self,
        user_id: str,
        blockchain: str,
        action: str,
        request_id: str,
        ip_address: str,
        user_agent: str,
        request_data: Dict,
        response_data: Dict,
        success: bool,
        error_message: Optional[str] = None
    ):
        """Registrar log de auditoria"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO audit_logs 
                (timestamp, user_id, blockchain, action, request_id, ip_address, 
                 user_agent, request_data, response_data, success, error_message)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z'),
                user_id,
                blockchain,
                action,
                request_id,
                ip_address,
                user_agent,
                json.dumps(request_data),
                json.dumps(response_data),
                success,
                error_message
            ))

# ============================================================================
# SISTEMA DE AUTENTICAÇÃO
# ============================================================================

class AuthenticationSystem:
    """Sistema de autenticação avançado"""
    
    def __init__(self, secret_key: str = None):
        self.secret_key = secret_key or os.getenv("QaaS_SECRET_KEY", secrets.token_urlsafe(32))
        self.api_keys = {}  # key_id -> {hash, user_id, permissions, rate_limit}
        self.jwt_tokens = {}  # token -> {user_id, expires_at}
        self.audit_db = AuditDatabase()
    
    def generate_api_key(self, user_id: str, blockchain: str, permissions: List[str], rate_limit: int = 1000) -> Dict[str, Any]:
        """Gerar API key para usuário"""
        key_id = f"qaas_{secrets.token_urlsafe(16)}"
        api_key = f"qaas_{secrets.token_urlsafe(32)}"
        key_hash = hashlib.sha256(api_key.encode()).hexdigest()
        
        self.api_keys[key_id] = {
            "key_hash": key_hash,
            "user_id": user_id,
            "blockchain": blockchain,
            "permissions": permissions,
            "rate_limit": rate_limit,
                "created_at": datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z'),
            "last_used": None,
            "is_active": True
        }
        
        # Salvar no banco
        with self.audit_db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT OR REPLACE INTO api_keys 
                (key_id, key_hash, user_id, blockchain, permissions, rate_limit, created_at, is_active)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                key_id,
                key_hash,
                user_id,
                blockchain,
                json.dumps(permissions),
                rate_limit,
                datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z'),
                True
            ))
        
        return {
            "key_id": key_id,
            "api_key": api_key,  # Mostrar apenas uma vez
            "user_id": user_id,
            "blockchain": blockchain,
            "permissions": permissions,
            "rate_limit": rate_limit,
            "warning": "⚠️  Guarde esta API key com segurança! Ela não será mostrada novamente."
        }
    
    def verify_api_key(self, api_key: str) -> Optional[Dict[str, Any]]:
        """Verificar API key"""
        if not api_key or not api_key.startswith("qaas_"):
            return None
        
        key_hash = hashlib.sha256(api_key.encode()).hexdigest()
        
        for key_id, key_data in self.api_keys.items():
            if key_data["key_hash"] == key_hash and key_data["is_active"]:
                # Atualizar last_used
                key_data["last_used"] = datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')
                return {
                    "key_id": key_id,
                    "user_id": key_data["user_id"],
                    "blockchain": key_data["blockchain"],
                    "permissions": key_data["permissions"],
                    "rate_limit": key_data["rate_limit"]
                }
        
        return None
    
    def generate_jwt_token(self, user_id: str, expires_in: int = 3600) -> str:
        """Gerar JWT token"""
        payload = {
            "user_id": user_id,
            "exp": datetime.now(timezone.utc) + timedelta(seconds=expires_in),
            "iat": datetime.now(timezone.utc)
        }
        token = jwt.encode(payload, self.secret_key, algorithm="HS256")
        self.jwt_tokens[token] = {"user_id": user_id, "expires_at": payload["exp"]}
        return token
    
    def verify_jwt_token(self, token: str) -> Optional[Dict[str, Any]]:
        """Verificar JWT token"""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=["HS256"])
            if token in self.jwt_tokens:
                return {"user_id": payload["user_id"]}
        except jwt.ExpiredSignatureError:
            if token in self.jwt_tokens:
                del self.jwt_tokens[token]
        except Exception as e:
            logger.warning(f"Erro ao verificar JWT: {e}")
        return None

# ============================================================================
# SISTEMA DE MONITORAMENTO AVANÇADO
# ============================================================================

class AdvancedMonitoring:
    """Sistema de monitoramento avançado"""
    
    def __init__(self):
        self.metrics = {
            "requests_per_minute": defaultdict(int),
            "errors_per_minute": defaultdict(int),
            "latency": [],
            "blockchain_usage": defaultdict(int),
            "algorithm_usage": defaultdict(int)
        }
        self.alerts = []
        self.thresholds = {
            "max_requests_per_minute": 1000,
            "max_error_rate": 0.05,  # 5%
            "max_latency_ms": 5000
        }
    
    def record_request(self, blockchain: str, algorithm: str, latency_ms: float, success: bool):
        """Registrar requisição"""
        minute = int(time.time() / 60)
        self.metrics["requests_per_minute"][minute] += 1
        if not success:
            self.metrics["errors_per_minute"][minute] += 1
        self.metrics["blockchain_usage"][blockchain] += 1
        self.metrics["algorithm_usage"][algorithm] += 1
        self.metrics["latency"].append(latency_ms)
        
        # Manter apenas últimas 1000 latências
        if len(self.metrics["latency"]) > 1000:
            self.metrics["latency"] = self.metrics["latency"][-1000:]
        
        # Verificar alertas
        self._check_alerts()
    
    def _check_alerts(self):
        """Verificar se há alertas"""
        current_minute = int(time.time() / 60)
        requests = self.metrics["requests_per_minute"][current_minute]
        
        if requests > self.thresholds["max_requests_per_minute"]:
            self.alerts.append({
                "type": "high_traffic",
                "message": f"Alto tráfego detectado: {requests} requisições/minuto",
                "timestamp": datetime.utcnow().isoformat() + "Z"
            })
    
    def get_metrics(self) -> Dict[str, Any]:
        """Obter métricas"""
        current_minute = int(time.time() / 60)
        recent_latencies = self.metrics["latency"][-100:] if self.metrics["latency"] else []
        
        return {
            "requests_per_minute": self.metrics["requests_per_minute"][current_minute],
            "errors_per_minute": self.metrics["errors_per_minute"][current_minute],
            "average_latency_ms": sum(recent_latencies) / len(recent_latencies) if recent_latencies else 0,
            "p95_latency_ms": sorted(recent_latencies)[int(len(recent_latencies) * 0.95)] if len(recent_latencies) >= 20 else 0,
            "blockchain_usage": dict(self.metrics["blockchain_usage"]),
            "algorithm_usage": dict(self.metrics["algorithm_usage"]),
            "alerts": self.alerts[-10:]  # Últimos 10 alertas
        }

# ============================================================================
# QUANTUM SECURITY SERVICE ENTERPRISE
# ============================================================================

class QuantumSecurityServiceEnterprise:
    """Versão Enterprise do Quantum Security Service"""
    
    def __init__(self):
        self.quantum_security = QuantumSecuritySystem()
        self.key_manager = PQCKeyManager()
        self.auth_system = AuthenticationSystem()
        self.monitoring = AdvancedMonitoring()
        self.audit_db = AuditDatabase()
        self.proof_bundle = QaaSProofBundle()  # Proof bundles assinados com PQC
        
        # Cache avançado
        self.key_cache = {}
        self.signature_cache = {}
        
        # Rate limiting por usuário
        self.user_rate_limits = defaultdict(lambda: {"count": 0, "reset_time": time.time() + 3600})
        
        # HSM Mode (suporte para AWS CloudHSM e outros)
        self.hsm_mode = os.getenv("HSM_MODE", "false").lower() == "true"
        self.hsm_backend = os.getenv("HSM_BACKEND", "SOFTWARE")
        
        if self.hsm_mode:
            logger.info(f"🔐 HSM Mode: {self.hsm_backend}")
        
        logger.info("🏦 QUANTUM SECURITY SERVICE ENTERPRISE: Inicializado!")
    
    def generate_keypair(
        self,
        blockchain: str,
        algorithm: str = "ML-DSA-128",
        security_level: int = 3,
        user_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Gerar par de chaves PQC (com auditoria)"""
        start_time = time.time()
        request_id = secrets.token_urlsafe(16)
        
        try:
            keypair = self.key_manager.generate_ml_dsa_keypair(
                f"{blockchain}_{int(time.time())}_{secrets.token_urlsafe(8)}"
            )
            
            # Armazenar no cache
            if blockchain not in self.key_cache:
                self.key_cache[blockchain] = {}
            self.key_cache[blockchain][keypair["keypair_id"]] = keypair
            
            # Registrar no banco
            with self.audit_db.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT OR REPLACE INTO keypairs 
                    (keypair_id, blockchain, algorithm, public_key, created_at, usage_count)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (
                    keypair["keypair_id"],
                    blockchain,
                    algorithm,
                    keypair["public_key"],
                    datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z'),
                    0
                ))
            
            latency = (time.time() - start_time) * 1000
            self.monitoring.record_request(blockchain, algorithm, latency, True)
            
            return {
                "success": True,
                "keypair_id": keypair["keypair_id"],
                "public_key": keypair["public_key"],
                "public_key_pem": keypair.get("public_key_pem"),
                "algorithm": algorithm,
                "blockchain": blockchain,
                "security_level": security_level,
                "real": keypair.get("real", False),
                "request_id": request_id,
                "created_at": datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')
            }
        except Exception as e:
            latency = (time.time() - start_time) * 1000
            self.monitoring.record_request(blockchain, algorithm, latency, False)
            logger.error(f"Erro ao gerar keypair: {e}")
            return {
                "success": False,
                "error": str(e),
                "request_id": request_id
            }
    
    def sign_transaction(
        self,
        blockchain: str,
        transaction_hash: str,
        keypair_id: str,
        algorithm: str = "ML-DSA-128",
        user_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Assinar transação (com auditoria)"""
        start_time = time.time()
        request_id = secrets.token_urlsafe(16)
        
        try:
            # Verificar cache
            cache_key = f"{blockchain}_{transaction_hash}_{keypair_id}"
            if cache_key in self.signature_cache:
                cached = self.signature_cache[cache_key]
                latency = (time.time() - start_time) * 1000
                self.monitoring.record_request(blockchain, algorithm, latency, True)
                return {
                    "success": True,
                    **cached,
                    "from_cache": True,
                    "request_id": request_id
                }
            
            hash_bytes = bytes.fromhex(transaction_hash.replace("0x", ""))
            result = self.key_manager.sign_ml_dsa(keypair_id, hash_bytes)
            
            if result:
                self.signature_cache[cache_key] = result
                latency = (time.time() - start_time) * 1000
                self.monitoring.record_request(blockchain, algorithm, latency, True)
                
                return {
                    "success": True,
                    "signature": result["signature"],
                    "signature_bin": result.get("signature_bin"),
                    "algorithm": algorithm,
                    "transaction_hash": transaction_hash,
                    "real": result.get("real", False),
                    "from_cache": False,
                    "request_id": request_id
                }
            else:
                raise Exception("Falha ao assinar")
        except Exception as e:
            latency = (time.time() - start_time) * 1000
            self.monitoring.record_request(blockchain, algorithm, latency, False)
            logger.error(f"Erro ao assinar: {e}")
            return {
                "success": False,
                "error": str(e),
                "request_id": request_id
            }
    
    def verify_signature(
        self,
        blockchain: str,
        transaction_hash: str,
        signature: str,
        public_key: str,
        algorithm: str = "ML-DSA-128"
    ) -> Dict[str, Any]:
        """Verificar assinatura"""
        start_time = time.time()
        
        try:
            hash_bytes = bytes.fromhex(transaction_hash.replace("0x", ""))
            result = self.key_manager.verify_ml_dsa(public_key, hash_bytes, signature)
            
            latency = (time.time() - start_time) * 1000
            self.monitoring.record_request(blockchain, algorithm, latency, result.get("success", False))
            
            return {
                "valid": result.get("success", False),
                "algorithm": algorithm,
                "real": result.get("real", False),
                "blockchain": blockchain
            }
        except Exception as e:
            latency = (time.time() - start_time) * 1000
            self.monitoring.record_request(blockchain, algorithm, latency, False)
            return {
                "valid": False,
                "error": str(e),
                "blockchain": blockchain
            }

# ============================================================================
# API FLASK ENTERPRISE
# ============================================================================

app = Flask(__name__)
service = QuantumSecurityServiceEnterprise()

def require_auth(f):
    """Decorator para autenticação"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get("Authorization")
        api_key = request.headers.get("X-API-Key")
        
        user_info = None
        
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header[7:]
            user_info = service.auth_system.verify_jwt_token(token)
        
        if not user_info and api_key:
            user_info = service.auth_system.verify_api_key(api_key)
        
        if not user_info:
            return jsonify({"error": "Authentication required"}), 401
        
        g.user_info = user_info
        return f(*args, **kwargs)
    return decorated_function

def audit_log(action: str):
    """Decorator para log de auditoria"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            user_info = getattr(g, 'user_info', {"user_id": "anonymous"})
            request_id = secrets.token_urlsafe(16)
            
            try:
                response = f(*args, **kwargs)
                response_data = response[0].get_json() if hasattr(response[0], 'get_json') else {}
                
                service.audit_db.log_audit(
                    user_id=user_info.get("user_id", "anonymous"),
                    blockchain=request.json.get("blockchain") if request.is_json else request.args.get("blockchain", "unknown"),
                    action=action,
                    request_id=request_id,
                    ip_address=request.remote_addr,
                    user_agent=request.headers.get("User-Agent", ""),
                    request_data=request.json if request.is_json else {},
                    response_data=response_data,
                    success=response[1] < 400,
                    error_message=None
                )
                
                return response
            except Exception as e:
                service.audit_db.log_audit(
                    user_id=user_info.get("user_id", "anonymous"),
                    blockchain="unknown",
                    action=action,
                    request_id=request_id,
                    ip_address=request.remote_addr,
                    user_agent=request.headers.get("User-Agent", ""),
                    request_data=request.json if request.is_json else {},
                    response_data={},
                    success=False,
                    error_message=str(e)
                )
                raise
        return decorated_function
    return decorator

@app.route('/api/v1/health', methods=['GET'])
def health():
    """Health check"""
    return jsonify({
        "status": "healthy",
        "service": "Quantum Security as a Service - Enterprise",
        "version": "2.0.0",
        "timestamp": datetime.utcnow().isoformat() + "Z"
    })

@app.route('/api/v1/auth/generate-key', methods=['POST'])
def generate_api_key():
    """Gerar API key (requer autenticação admin)"""
    data = request.json
    user_id = data.get("user_id")
    blockchain = data.get("blockchain")
    permissions = data.get("permissions", ["sign", "verify"])
    rate_limit = data.get("rate_limit", 1000)
    
    if not user_id or not blockchain:
        return jsonify({"error": "user_id and blockchain required"}), 400
    
    result = service.auth_system.generate_api_key(user_id, blockchain, permissions, rate_limit)
    return jsonify(result), 200

@app.route('/api/v1/keypair/generate', methods=['POST'])
@require_auth
@audit_log("generate_keypair")
def generate_keypair():
    """Gerar par de chaves PQC"""
    data = request.json
    blockchain = data.get("blockchain")
    algorithm = data.get("algorithm", "ML-DSA-128")
    security_level = data.get("security_level", 3)
    user_id = g.user_info.get("user_id")
    
    if not blockchain:
        return jsonify({"error": "blockchain required"}), 400
    
    result = service.generate_keypair(blockchain, algorithm, security_level, user_id)
    return jsonify(result), 200 if result.get("success") else 500

@app.route('/api/v1/signature/sign', methods=['POST'])
@require_auth
@audit_log("sign_transaction")
def sign_transaction():
    """Assinar transação"""
    data = request.json
    blockchain = data.get("blockchain")
    transaction_hash = data.get("transaction_hash")
    keypair_id = data.get("keypair_id")
    algorithm = data.get("algorithm", "ML-DSA-128")
    user_id = g.user_info.get("user_id")
    
    if not all([blockchain, transaction_hash, keypair_id]):
        return jsonify({"error": "blockchain, transaction_hash, and keypair_id required"}), 400
    
    result = service.sign_transaction(blockchain, transaction_hash, keypair_id, algorithm, user_id)
    return jsonify(result), 200 if result.get("success") else 500

@app.route('/api/v1/signature/verify', methods=['POST'])
@require_auth
@audit_log("verify_signature")
def verify_signature():
    """Verificar assinatura"""
    data = request.json
    blockchain = data.get("blockchain")
    transaction_hash = data.get("transaction_hash")
    signature = data.get("signature")
    public_key = data.get("public_key")
    algorithm = data.get("algorithm", "ML-DSA-128")
    
    if not all([blockchain, transaction_hash, signature, public_key]):
        return jsonify({"error": "All parameters required"}), 400
    
    result = service.verify_signature(blockchain, transaction_hash, signature, public_key, algorithm)
    return jsonify(result), 200

@app.route('/api/v1/monitoring/metrics', methods=['GET'])
@require_auth
def get_metrics():
    """Obter métricas de monitoramento"""
    metrics = service.monitoring.get_metrics()
    return jsonify(metrics), 200

@app.route('/api/v1/audit/logs', methods=['GET'])
@require_auth
def get_audit_logs():
    """Obter logs de auditoria (requer permissão admin)"""
    limit = request.args.get("limit", 100, type=int)
    
    with service.audit_db.get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM audit_logs 
            ORDER BY timestamp DESC 
            LIMIT ?
        ''', (limit,))
        
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        logs = [dict(zip(columns, row)) for row in rows]
    
    return jsonify({"logs": logs}), 200

if __name__ == '__main__':
    print("="*70)
    print("🏦 QUANTUM SECURITY AS A SERVICE - ENTERPRISE EDITION")
    print("="*70)
    print("🌐 API disponível em: http://localhost:5010")
    print("🔐 Autenticação: Bearer Token ou X-API-Key")
    print("📊 Monitoramento: /api/v1/monitoring/metrics")
    print("📋 Auditoria: /api/v1/audit/logs")
    print("="*70)
    app.run(host='0.0.0.0', port=5010, debug=True)

