#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🌐 API RESTFUL COMPLETA - ALLIANZA BLOCKCHAIN
API completa e documentada com OpenAPI/Swagger
"""

from flask import Blueprint, request, jsonify
from flask_restx import Api, Resource, fields, Namespace
from functools import wraps
import time
from typing import Dict, Optional

# Tentar importar Flask-RESTX
try:
    from flask_restx import Api, Resource, fields, Namespace
    RESTX_AVAILABLE = True
except ImportError:
    RESTX_AVAILABLE = False
    print("⚠️  Flask-RESTX não disponível. Instale com: pip install flask-restx")

def create_rest_api(
    blockchain_instance=None,
    quantum_security_instance=None,
    bridge_instance=None,
    multi_sig_instance=None,
    alert_system_instance=None
) -> Optional[Blueprint]:
    """Criar API RESTful completa"""
    
    if not RESTX_AVAILABLE:
        # Fallback: API básica sem Swagger
        api_bp = Blueprint('rest_api', __name__)
        
        @api_bp.route('/api/v1/health')
        def health():
            return jsonify({"status": "ok", "version": "1.0"})
        
        return api_bp
    
    # API com Flask-RESTX e Swagger
    api_bp = Blueprint('rest_api', __name__, url_prefix='/api/v1')
    api = Api(
        api_bp,
        version='1.0',
        title='Allianza Blockchain API',
        description='API RESTful completa para Allianza Blockchain',
        doc='/docs/',  # Swagger UI em /api/v1/docs/
        prefix='/api/v1'
    )
    
    # Namespaces
    ns_quantum = Namespace('quantum', description='Operações de Segurança Quântica')
    ns_bridge = Namespace('bridge', description='Operações Cross-Chain Bridge')
    ns_multisig = Namespace('multisig', description='Operações Multi-Signature')
    ns_alerts = Namespace('alerts', description='Sistema de Alertas')
    ns_metrics = Namespace('metrics', description='Métricas e Monitoramento')
    
    api.add_namespace(ns_quantum)
    api.add_namespace(ns_bridge)
    api.add_namespace(ns_multisig)
    api.add_namespace(ns_alerts)
    api.add_namespace(ns_metrics)
    
    # =============================================================================
    # MODELOS DE DADOS (Swagger)
    # =============================================================================
    
    quantum_signature_model = api.model('QuantumSignature', {
        'algorithm': fields.String(required=True, description='Algoritmo PQC usado'),
        'signature': fields.String(required=True, description='Assinatura quântica'),
        'public_key': fields.String(required=True, description='Chave pública'),
        'nist_standard': fields.Boolean(description='Conforme padrão NIST')
    })
    
    transfer_request_model = api.model('TransferRequest', {
        'source_chain': fields.String(required=True, description='Chain de origem', example='polygon'),
        'target_chain': fields.String(required=True, description='Chain de destino', example='bitcoin'),
        'amount': fields.Float(required=True, description='Quantidade', example=0.0001),
        'token_symbol': fields.String(required=True, description='Símbolo do token', example='MATIC'),
        'recipient': fields.String(required=True, description='Endereço do destinatário'),
        'source_private_key': fields.String(description='Chave privada (opcional se configurada)')
    })
    
    multisig_operation_model = api.model('MultiSigOperation', {
        'operation_type': fields.String(required=True, description='Tipo de operação'),
        'data': fields.Raw(required=True, description='Dados da operação'),
        'required_signatures': fields.Integer(required=True, description='Número mínimo de assinaturas'),
        'signer_ids': fields.List(fields.String, required=True, description='IDs dos signatários'),
        'expires_in': fields.Integer(description='Tempo de expiração em segundos', default=3600)
    })
    
    # =============================================================================
    # ENDPOINTS - QUANTUM SECURITY
    # =============================================================================
    
    @ns_quantum.route('/status')
    class QuantumStatus(Resource):
        @api.doc('quantum_status')
        def get(self):
            """Obter status do sistema de segurança quântica"""
            if not quantum_security_instance:
                return {"available": False}, 404
            
            stats = getattr(quantum_security_instance, 'stats', {})
            return {
                "available": True,
                "keys_generated": stats.get("keys_generated", 0),
                "signatures_created": stats.get("signatures_created", 0),
                "algorithms": getattr(quantum_security_instance, 'algorithms', {})
            }
    
    @ns_quantum.route('/generate-keypair')
    class GenerateKeypair(Resource):
        @api.doc('generate_quantum_keypair')
        def post(self):
            """Gerar par de chaves PQC"""
            if not quantum_security_instance:
                return {"error": "Quantum Security não disponível"}, 503
            
            try:
                keypair = quantum_security_instance.generate_ml_dsa_keypair(security_level=3)
                return {
                    "success": True,
                    "keypair_id": keypair.get("keypair_id"),
                    "public_key": keypair.get("public_key")
                }
            except Exception as e:
                return {"error": str(e)}, 500
    
    # =============================================================================
    # ENDPOINTS - BRIDGE
    # =============================================================================
    
    @ns_bridge.route('/transfer')
    class BridgeTransfer(Resource):
        @api.doc('bridge_transfer')
        @api.expect(transfer_request_model)
        def post(self):
            """Realizar transferência cross-chain"""
            if not bridge_instance:
                return {"error": "Bridge não disponível"}, 503
            
            data = request.json
            
            try:
                result = bridge_instance.real_cross_chain_transfer(
                    source_chain=data.get('source_chain'),
                    target_chain=data.get('target_chain'),
                    amount=data.get('amount'),
                    token_symbol=data.get('token_symbol'),
                    recipient=data.get('recipient'),
                    source_private_key=data.get('source_private_key')
                )
                
                if result.get('success'):
                    return result, 200
                else:
                    return result, 400
            except Exception as e:
                return {"error": str(e)}, 500
    
    @ns_bridge.route('/transfer/async')
    class BridgeTransferAsync(Resource):
        @api.doc('bridge_transfer_async')
        @api.expect(transfer_request_model)
        def post(self):
            """Realizar transferência cross-chain assíncrona"""
            if not bridge_instance:
                return {"error": "Bridge não disponível"}, 503
            
            data = request.json
            
            try:
                result = bridge_instance.real_cross_chain_transfer_async(
                    source_chain=data.get('source_chain'),
                    target_chain=data.get('target_chain'),
                    amount=data.get('amount'),
                    token_symbol=data.get('token_symbol'),
                    recipient=data.get('recipient'),
                    source_private_key=data.get('source_private_key'),
                    priority=data.get('priority', 5)
                )
                
                return result, 202  # Accepted
            except Exception as e:
                return {"error": str(e)}, 500
    
    @ns_bridge.route('/status')
    class BridgeStatus(Resource):
        @api.doc('bridge_status')
        def get(self):
            """Obter status do bridge"""
            if not bridge_instance:
                return {"error": "Bridge não disponível"}, 503
            
            return bridge_instance.get_reserves_status()
    
    @ns_bridge.route('/chains')
    class SupportedChains(Resource):
        @api.doc('supported_chains')
        def get(self):
            """Listar chains suportadas"""
            chains = [
                {"name": "Bitcoin", "id": "bitcoin", "status": "operational"},
                {"name": "Ethereum", "id": "ethereum", "status": "operational"},
                {"name": "Polygon", "id": "polygon", "status": "operational"},
                {"name": "BSC", "id": "bsc", "status": "operational"},
                {"name": "Solana", "id": "solana", "status": "development"},
                {"name": "Base", "id": "base", "status": "planned"}
            ]
            return {"chains": chains}
    
    # =============================================================================
    # ENDPOINTS - MULTI-SIG
    # =============================================================================
    
    @ns_multisig.route('/operation')
    class CreateMultiSigOperation(Resource):
        @api.doc('create_multisig_operation')
        @api.expect(multisig_operation_model)
        def post(self):
            """Criar operação multi-signature"""
            if not multi_sig_instance:
                return {"error": "Multi-Sig não disponível"}, 503
            
            data = request.json
            
            try:
                result = multi_sig_instance.create_operation(
                    operation_type=data.get('operation_type'),
                    data=data.get('data'),
                    required_signatures=data.get('required_signatures'),
                    signer_ids=data.get('signer_ids'),
                    expires_in=data.get('expires_in', 3600)
                )
                
                return result, 201
            except Exception as e:
                return {"error": str(e)}, 500
    
    @ns_multisig.route('/operation/<operation_id>/sign')
    class SignMultiSigOperation(Resource):
        @api.doc('sign_multisig_operation')
        def post(self, operation_id):
            """Assinar operação multi-signature"""
            if not multi_sig_instance:
                return {"error": "Multi-Sig não disponível"}, 503
            
            data = request.json
            signer_id = data.get('signer_id')
            
            if not signer_id:
                return {"error": "signer_id é obrigatório"}, 400
            
            try:
                result = multi_sig_instance.sign_operation(
                    operation_id=operation_id,
                    signer_id=signer_id
                )
                
                return result, 200
            except Exception as e:
                return {"error": str(e)}, 500
    
    @ns_multisig.route('/operation/<operation_id>')
    class GetMultiSigOperation(Resource):
        @api.doc('get_multisig_operation')
        def get(self, operation_id):
            """Obter status de operação multi-signature"""
            if not multi_sig_instance:
                return {"error": "Multi-Sig não disponível"}, 503
            
            result = multi_sig_instance.verify_operation(operation_id)
            return result, 200
    
    # =============================================================================
    # ENDPOINTS - ALERTS
    # =============================================================================
    
    @ns_alerts.route('/')
    class ListAlerts(Resource):
        @api.doc('list_alerts')
        def get(self):
            """Listar alertas ativos"""
            if not alert_system_instance:
                return {"error": "Sistema de alertas não disponível"}, 503
            
            level = request.args.get('level')
            component = request.args.get('component')
            
            alerts = alert_system_instance.get_active_alerts(
                level=level,
                component=component
            )
            
            return {"alerts": alerts, "count": len(alerts)}, 200
    
    @ns_alerts.route('/statistics')
    class AlertStatistics(Resource):
        @api.doc('alert_statistics')
        def get(self):
            """Obter estatísticas de alertas"""
            if not alert_system_instance:
                return {"error": "Sistema de alertas não disponível"}, 503
            
            stats = alert_system_instance.get_alert_statistics()
            return stats, 200
    
    # =============================================================================
    # ENDPOINTS - METRICS
    # =============================================================================
    
    @ns_metrics.route('/')
    class GetAllMetrics(Resource):
        @api.doc('get_all_metrics')
        def get(self):
            """Obter todas as métricas"""
            # Se unified_dashboard disponível, usar
            try:
                from unified_dashboard import UnifiedDashboard
                # Dashboard seria inicializado externamente
                return {"message": "Use /dashboard/api/metrics"}, 200
            except:
                return {"message": "Dashboard não disponível"}, 503
    
    return api_bp
















