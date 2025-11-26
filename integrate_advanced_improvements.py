#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔧 INTEGRAÇÃO DE MELHORIAS AVANÇADAS
Integra todas as melhorias avançadas no sistema principal
"""

import time
from flask import request

def integrate_advanced_improvements(app, blockchain_instance, quantum_security_instance, bridge_instance):
    """
    Integrar todas as melhorias avançadas no sistema
    
    Args:
        app: Instância Flask
        blockchain_instance: Instância AllianzaBlockchain
        quantum_security_instance: Instância QuantumSecuritySystem
        bridge_instance: Instância RealCrossChainBridge
    """
    print("\n" + "="*60)
    print("🚀 INTEGRANDO MELHORIAS AVANÇADAS")
    print("="*60)
    
    # =============================================================================
    # 1. MULTI-SIGNATURE QUÂNTICO-SEGURO
    # =============================================================================
    try:
        from quantum_multi_sig import QuantumMultiSig
        multi_sig = QuantumMultiSig(quantum_security_instance)
        print("✅ Multi-Signature Quântico-Seguro: Integrado!")
        
        # Adicionar ao bridge se disponível
        if bridge_instance:
            bridge_instance.multi_sig = multi_sig
    except ImportError as e:
        print(f"⚠️  Multi-Sig não disponível: {e}")
        multi_sig = None
    
    # =============================================================================
    # 2. DASHBOARD UNIFICADO
    # =============================================================================
    try:
        from flask_socketio import SocketIO
        from unified_dashboard import UnifiedDashboard, create_dashboard_blueprint
        
        # Inicializar SocketIO se não existir
        socketio = None
        if hasattr(app, 'socketio'):
            socketio = app.socketio
        else:
            try:
                socketio = SocketIO(app, cors_allowed_origins="*")
                app.socketio = socketio
            except:
                pass
        
        # Criar dashboard
        dashboard = UnifiedDashboard(
            blockchain_instance=blockchain_instance,
            quantum_security_instance=quantum_security_instance,
            bridge_instance=bridge_instance,
            socketio=socketio
        )
        
        # Registrar blueprint
        dashboard_bp = create_dashboard_blueprint(dashboard, socketio)
        app.register_blueprint(dashboard_bp, url_prefix='/dashboard')
        
        print("✅ Dashboard Unificado: Integrado!")
        print("   📊 Acesse em: http://localhost:5008/dashboard/")
        
        # Broadcast periódico de métricas
        def broadcast_metrics_periodically():
            import threading
            def broadcast():
                while True:
                    try:
                        time.sleep(5)  # A cada 5 segundos
                        dashboard.broadcast_metrics()
                    except:
                        pass
            
            thread = threading.Thread(target=broadcast, daemon=True)
            thread.start()
        
        broadcast_metrics_periodically()
        
    except ImportError as e:
        print(f"⚠️  Dashboard não disponível: {e}")
        dashboard = None
    
    # =============================================================================
    # 3. SISTEMA DE ALERTAS
    # =============================================================================
    try:
        from alert_system import AlertSystem, AlertLevel, AlertChannel
        
        alert_system = AlertSystem()
        print("✅ Sistema de Alertas: Integrado!")
        
        # Configurar canais básicos
        alert_system.enable_channel(AlertChannel.DASHBOARD)
        
        # Adicionar ao bridge
        if bridge_instance:
            bridge_instance.alert_system = alert_system
        
        # Adicionar ao dashboard
        if dashboard:
            dashboard.alert_system = alert_system
        
    except ImportError as e:
        print(f"⚠️  Sistema de Alertas não disponível: {e}")
        alert_system = None
    
    # =============================================================================
    # 4. SOLANA BRIDGE
    # =============================================================================
    try:
        from solana_bridge import SolanaBridge
        
        solana_bridge = SolanaBridge()
        print("✅ Solana Bridge: Integrado!")
        
        # Adicionar ao bridge principal
        if bridge_instance:
            bridge_instance.solana_bridge = solana_bridge
            # Adicionar Solana às reservas
            if "solana" not in bridge_instance.bridge_reserves:
                bridge_instance.bridge_reserves["solana"] = {}
            bridge_instance.bridge_reserves["solana"]["SOL"] = 1000.0  # Reserva inicial
            
            # Adicionar taxa de câmbio
            bridge_instance.exchange_rates_usd["SOL"] = 100.0
            bridge_instance.coingecko_ids["SOL"] = "solana"
        
    except ImportError as e:
        print(f"⚠️  Solana Bridge não disponível: {e}")
        solana_bridge = None
    
    # =============================================================================
    # 5. API RESTFUL
    # =============================================================================
    try:
        from rest_api import create_rest_api
        
        api_bp = create_rest_api(
            blockchain_instance=blockchain_instance,
            quantum_security_instance=quantum_security_instance,
            bridge_instance=bridge_instance,
            multi_sig_instance=multi_sig,
            alert_system_instance=alert_system
        )
        
        if api_bp:
            app.register_blueprint(api_bp)
            print("✅ API RESTful: Integrada!")
            print("   📚 Documentação: http://localhost:5008/api/v1/docs/")
            print("   🔗 Health Check: http://localhost:5008/api/v1/health")
        
    except ImportError as e:
        print(f"⚠️  API RESTful não disponível: {e}")
    
    # =============================================================================
    # 6. ROTAS ADICIONAIS
    # =============================================================================
    
    @app.route('/api/v1/improvements/status')
    def improvements_status():
        """Status de todas as melhorias"""
        return {
            "multi_sig": multi_sig is not None,
            "dashboard": dashboard is not None,
            "alert_system": alert_system is not None,
            "solana_bridge": solana_bridge is not None,
            "rest_api": api_bp is not None if 'api_bp' in locals() else False
        }
    
    @app.route('/api/v1/multisig/register', methods=['POST'])
    def register_multisig_signer():
        """Registrar signatário multi-sig"""
        if not multi_sig:
            return {"error": "Multi-Sig não disponível"}, 503
        
        data = request.json
        result = multi_sig.register_signer(
            signer_id=data.get('signer_id'),
            public_key=data.get('public_key'),
            weight=data.get('weight', 1)
        )
        
        return result, 200 if result.get('success') else 400
    
    @app.route('/api/v1/alerts/create', methods=['POST'])
    def create_alert():
        """Criar alerta"""
        if not alert_system:
            return {"error": "Sistema de alertas não disponível"}, 503
        
        data = request.json
        from alert_system import AlertLevel, AlertChannel
        
        level = AlertLevel(data.get('level', 'info'))
        channels = [AlertChannel(c) for c in data.get('channels', ['dashboard'])]
        
        result = alert_system.create_alert(
            level=level,
            title=data.get('title'),
            message=data.get('message'),
            component=data.get('component', 'system'),
            metadata=data.get('metadata'),
            channels=channels
        )
        
        return result, 201 if result.get('success') else 400
    
    print("\n" + "="*60)
    print("✅ TODAS AS MELHORIAS INTEGRADAS!")
    print("="*60)
    print("\n📋 Endpoints Disponíveis:")
    print("   • Dashboard: http://localhost:5008/dashboard/")
    print("   • API Docs: http://localhost:5008/api/v1/docs/")
    print("   • Health: http://localhost:5008/api/v1/health")
    print("   • Status: http://localhost:5008/api/v1/improvements/status")
    print("\n")
    
    return {
        "multi_sig": multi_sig,
        "dashboard": dashboard,
        "alert_system": alert_system,
        "solana_bridge": solana_bridge
    }

