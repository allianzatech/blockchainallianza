#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
📊 DASHBOARD UNIFICADO EM TEMPO REAL
Dashboard completo com todas as métricas do sistema
"""

import time
import json
from typing import Dict, List, Optional
from datetime import datetime, timedelta
from collections import defaultdict, deque
from flask import Blueprint, render_template, jsonify, request
from flask_socketio import SocketIO, emit

class UnifiedDashboard:
    """Dashboard Unificado em Tempo Real"""
    
    def __init__(
        self,
        blockchain_instance=None,
        quantum_security_instance=None,
        bridge_instance=None,
        socketio: Optional[SocketIO] = None
    ):
        self.blockchain = blockchain_instance
        self.quantum_security = quantum_security_instance
        self.bridge = bridge_instance
        self.socketio = socketio
        
        # Histórico de métricas (últimas 24 horas)
        self.metrics_history = {
            "quantum": deque(maxlen=1440),  # 1 ponto por minuto
            "bridge": deque(maxlen=1440),
            "performance": deque(maxlen=1440),
            "security": deque(maxlen=1440)
        }
        
        # Estatísticas em tempo real
        self.real_time_stats = {
            "quantum": {},
            "bridge": {},
            "performance": {},
            "security": {}
        }
        
        # Alertas ativos
        self.active_alerts = []
        
    def get_quantum_metrics(self) -> Dict:
        """Obter métricas de segurança quântica"""
        if not self.quantum_security:
            return {
                "available": False,
                "message": "Quantum Security não disponível"
            }
        
        stats = getattr(self.quantum_security, 'stats', {})
        
        return {
            "available": True,
            "keys_generated": stats.get("keys_generated", 0),
            "signatures_created": stats.get("signatures_created", 0),
            "encryptions_performed": stats.get("encryptions_performed", 0),
            "quantum_keys_exchanged": stats.get("quantum_keys_exchanged", 0),
            "algorithms": {
                "ml_dsa": getattr(self.quantum_security, 'algorithms', {}).get("ml_dsa", False),
                "ml_kem": getattr(self.quantum_security, 'algorithms', {}).get("ml_kem", False),
                "sphincs": getattr(self.quantum_security, 'algorithms', {}).get("sphincs", False)
            },
            "cache_stats": getattr(self.quantum_security, '_cache_stats', {})
        }
    
    def get_bridge_metrics(self) -> Dict:
        """Obter métricas do bridge cross-chain"""
        if not self.bridge:
            return {
                "available": False,
                "message": "Bridge não disponível"
            }
        
        # Contar transferências
        pending = len(getattr(self.bridge, 'pending_bridges', {}))
        reserves = getattr(self.bridge, 'bridge_reserves', {})
        
        # Estatísticas de chains
        chains_status = {}
        for chain in ["bitcoin", "polygon", "ethereum", "bsc", "solana"]:
            if chain in reserves:
                chains_status[chain] = {
                    "available": True,
                    "reserves": reserves[chain]
                }
            else:
                chains_status[chain] = {
                    "available": False
                }
        
        return {
            "available": True,
            "pending_transfers": pending,
            "chains_status": chains_status,
            "async_enabled": getattr(self.bridge, 'async_enabled', False),
            "quantum_enabled": getattr(self.bridge, 'quantum_enabled', False),
            "improvements_available": getattr(self.bridge, 'improvements_available', False)
        }
    
    def get_performance_metrics(self) -> Dict:
        """Obter métricas de performance"""
        metrics = {
            "throughput": {
                "current_tps": 0,
                "avg_tps_1h": 0,
                "avg_tps_24h": 0,
                "peak_tps": 0
            },
            "latency": {
                "avg_ms": 0,
                "p95_ms": 0,
                "p99_ms": 0
            },
            "cache": {
                "hit_rate": 0,
                "miss_rate": 0,
                "total_requests": 0
            },
            "connections": {
                "active": 0,
                "pooled": 0,
                "failed": 0
            }
        }
        
        # Se bridge disponível, obter métricas
        if self.bridge:
            # Connection pooling stats
            pools = getattr(self.bridge, 'web3_pools', {})
            metrics["connections"]["pooled"] = len(pools)
            
            # Cache stats (se disponível)
            try:
                from cache_manager import global_cache
                if hasattr(global_cache, 'stats'):
                    cache_stats = global_cache.stats
                    metrics["cache"] = cache_stats
            except:
                pass
        
        return metrics
    
    def get_security_metrics(self) -> Dict:
        """Obter métricas de segurança"""
        metrics = {
            "anomaly_detection": {
                "enabled": False,
                "suspicious_patterns": 0,
                "blocked_transactions": 0
            },
            "rate_limiting": {
                "enabled": False,
                "blocked_requests": 0
            },
            "quantum_security": {
                "enabled": False,
                "transactions_protected": 0
            }
        }
        
        # Anomaly detection
        if self.bridge and hasattr(self.bridge, 'anomaly_detector'):
            detector = self.bridge.anomaly_detector
            if detector:
                suspicious = detector.get_suspicious_patterns(limit=100)
                metrics["anomaly_detection"] = {
                    "enabled": True,
                    "suspicious_patterns": len(suspicious),
                    "recent_patterns": suspicious[:10]
                }
        
        # Rate limiting
        if self.bridge and hasattr(self.bridge, 'intelligent_rate_limiter'):
            limiter = self.bridge.intelligent_rate_limiter
            if limiter:
                metrics["rate_limiting"]["enabled"] = True
        
        # Quantum security
        if self.quantum_security:
            stats = getattr(self.quantum_security, 'stats', {})
            metrics["quantum_security"] = {
                "enabled": True,
                "transactions_protected": stats.get("signatures_created", 0)
            }
        
        return metrics
    
    def get_all_metrics(self) -> Dict:
        """Obter todas as métricas"""
        timestamp = time.time()
        
        metrics = {
            "timestamp": timestamp,
            "datetime": datetime.now().isoformat(),
            "quantum": self.get_quantum_metrics(),
            "bridge": self.get_bridge_metrics(),
            "performance": self.get_performance_metrics(),
            "security": self.get_security_metrics(),
            "alerts": {
                "active": len(self.active_alerts),
                "critical": sum(1 for a in self.active_alerts if a.get("level") == "critical"),
                "warnings": sum(1 for a in self.active_alerts if a.get("level") == "warning"),
                "list": self.active_alerts[-10:]  # Últimos 10 alertas
            }
        }
        
        # Adicionar ao histórico
        self.metrics_history["quantum"].append({
            "timestamp": timestamp,
            "data": metrics["quantum"]
        })
        self.metrics_history["bridge"].append({
            "timestamp": timestamp,
            "data": metrics["bridge"]
        })
        self.metrics_history["performance"].append({
            "timestamp": timestamp,
            "data": metrics["performance"]
        })
        self.metrics_history["security"].append({
            "timestamp": timestamp,
            "data": metrics["security"]
        })
        
        # Atualizar stats em tempo real
        self.real_time_stats = {
            "quantum": metrics["quantum"],
            "bridge": metrics["bridge"],
            "performance": metrics["performance"],
            "security": metrics["security"]
        }
        
        return metrics
    
    def add_alert(
        self,
        level: str,  # "info", "warning", "critical"
        title: str,
        message: str,
        component: str = "system"
    ):
        """Adicionar alerta"""
        alert = {
            "id": f"alert_{int(time.time())}_{len(self.active_alerts)}",
            "level": level,
            "title": title,
            "message": message,
            "component": component,
            "timestamp": time.time(),
            "datetime": datetime.now().isoformat()
        }
        
        self.active_alerts.append(alert)
        
        # Manter apenas últimos 100 alertas
        if len(self.active_alerts) > 100:
            self.active_alerts = self.active_alerts[-100:]
        
        # Emitir via WebSocket se disponível
        if self.socketio:
            self.socketio.emit('new_alert', alert)
        
        return alert
    
    def get_metrics_history(
        self,
        metric_type: str,
        hours: int = 24
    ) -> List[Dict]:
        """Obter histórico de métricas"""
        if metric_type not in self.metrics_history:
            return []
        
        cutoff_time = time.time() - (hours * 3600)
        history = self.metrics_history[metric_type]
        
        return [
            point for point in history
            if point["timestamp"] >= cutoff_time
        ]
    
    def broadcast_metrics(self):
        """Broadcast métricas via WebSocket"""
        if not self.socketio:
            return
        
        metrics = self.get_all_metrics()
        self.socketio.emit('metrics_update', metrics)

def create_dashboard_blueprint(
    dashboard: UnifiedDashboard,
    socketio: Optional[SocketIO] = None
) -> Blueprint:
    """Criar blueprint Flask para dashboard"""
    dashboard_bp = Blueprint('unified_dashboard', __name__)
    
    @dashboard_bp.route('/')
    def dashboard_page():
        """Página principal do dashboard"""
        # Verificar se template existe, senão criar página simples com botão
        try:
            return render_template('unified_dashboard.html')
        except:
            # Página simples com botão para simulador
            return f"""
            <!DOCTYPE html>
            <html>
            <head>
                <title>Allianza Blockchain Dashboard</title>
                <style>
                    body {{
                        font-family: Arial, sans-serif;
                        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                        color: white;
                        padding: 50px;
                        text-align: center;
                    }}
                    .container {{
                        max-width: 800px;
                        margin: 0 auto;
                    }}
                    .btn {{
                        background: white;
                        color: #667eea;
                        border: none;
                        padding: 20px 40px;
                        font-size: 1.5em;
                        border-radius: 10px;
                        cursor: pointer;
                        text-decoration: none;
                        display: inline-block;
                        margin: 20px;
                        transition: transform 0.2s;
                    }}
                    .btn:hover {{
                        transform: scale(1.05);
                    }}
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>🚀 Allianza Blockchain Dashboard</h1>
                    <p>Bem-vindo ao sistema de interoperabilidade cross-chain com segurança quântica</p>
                    <a href="/dashboard/quantum-attack-simulator" class="btn">
                        🔬 Testar Ataque Quântico
                    </a>
                    <br>
                    <a href="/dashboard/api/metrics" class="btn">📊 Métricas</a>
                    <a href="/api/v1/docs/" class="btn">📚 API Docs</a>
                </div>
            </body>
            </html>
            """
    
    @dashboard_bp.route('/api/metrics')
    def get_metrics():
        """API para obter métricas"""
        return jsonify(dashboard.get_all_metrics())
    
    @dashboard_bp.route('/api/metrics/quantum')
    def get_quantum_metrics():
        """API para métricas quânticas"""
        return jsonify(dashboard.get_quantum_metrics())
    
    @dashboard_bp.route('/api/metrics/bridge')
    def get_bridge_metrics():
        """API para métricas do bridge"""
        return jsonify(dashboard.get_bridge_metrics())
    
    @dashboard_bp.route('/api/metrics/performance')
    def get_performance_metrics():
        """API para métricas de performance"""
        return jsonify(dashboard.get_performance_metrics())
    
    @dashboard_bp.route('/api/metrics/security')
    def get_security_metrics():
        """API para métricas de segurança"""
        return jsonify(dashboard.get_security_metrics())
    
    @dashboard_bp.route('/api/alerts')
    def get_alerts():
        """API para alertas"""
        return jsonify({
            "alerts": dashboard.active_alerts[-50:],  # Últimos 50
            "count": len(dashboard.active_alerts)
        })
    
    @dashboard_bp.route('/api/history/<metric_type>')
    def get_history(metric_type: str):
        """API para histórico de métricas"""
        hours = int(request.args.get('hours', 24))
        return jsonify(dashboard.get_metrics_history(metric_type, hours))
    
    @dashboard_bp.route('/api/quantum-attack-simulator/run')
    def run_quantum_attack_simulation():
        """Executar simulação de ataque quântico"""
        try:
            from quantum_attack_simulator import QuantumAttackSimulator
            
            quantum_security = getattr(dashboard, 'quantum_security_instance', None)
            simulator = QuantumAttackSimulator(quantum_security)
            
            # Executar simulação e salvar JSON
            result = simulator.run_comparison_demo(save_json=True)
            
            return jsonify({
                "success": True,
                "simulation": result,
                "json_file": result.get("json_file"),
                "timestamp": time.time()
            })
        except Exception as e:
            import traceback
            return jsonify({
                "success": False,
                "error": str(e),
                "traceback": traceback.format_exc()
            }), 500
    
    @dashboard_bp.route('/api/quantum-attack-simulator/statistics')
    def get_attack_statistics():
        """Obter estatísticas de simulações"""
        try:
            from quantum_attack_simulator import QuantumAttackSimulator
            
            quantum_security = getattr(dashboard, 'quantum_security_instance', None)
            simulator = QuantumAttackSimulator(quantum_security)
            
            stats = simulator.get_attack_statistics()
            return jsonify(stats)
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    @dashboard_bp.route('/quantum-attack-simulator')
    def quantum_attack_simulator_page():
        """Página do simulador de ataque quântico"""
        try:
            return render_template('quantum_attack_simulator.html')
        except Exception as e:
            return f"<h1>Erro ao carregar página</h1><p>{str(e)}</p><p>Certifique-se de que o arquivo templates/quantum_attack_simulator.html existe.</p>", 500
    
    @dashboard_bp.route('/api/quantum-attack-simulator/download')
    def download_quantum_attack_json():
        """Download do JSON detalhado da simulação"""
        try:
            from flask import send_file
            import os
            
            file_path = request.args.get('file')
            if not file_path:
                return jsonify({"error": "Parâmetro 'file' não fornecido"}), 400
            
            # Verificar se arquivo existe
            if not os.path.exists(file_path):
                return jsonify({"error": "Arquivo não encontrado"}), 404
            
            # Verificar se está no diretório permitido
            if not file_path.startswith('quantum_attack_simulations'):
                return jsonify({"error": "Acesso negado"}), 403
            
            return send_file(file_path, as_attachment=True, mimetype='application/json')
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    @dashboard_bp.route('/api/quantum-attack-simulator/verify')
    def verify_quantum_proof():
        """Verificar prova de segurança quântica"""
        try:
            from quantum_proof_verifier import QuantumProofVerifier
            import os
            
            proof_id = request.args.get('proof_id')
            if not proof_id:
                return jsonify({"error": "Parâmetro 'proof_id' não fornecido"}), 400
            
            quantum_security = getattr(dashboard, 'quantum_security_instance', None)
            verifier = QuantumProofVerifier(quantum_security)
            
            proof_dir = "quantum_attack_simulations"
            verification = verifier.verify_proof(proof_dir, proof_id)
            
            return jsonify({
                "success": True,
                "verification": verification
            })
        except Exception as e:
            import traceback
            return jsonify({
                "success": False,
                "error": str(e),
                "traceback": traceback.format_exc()
            }), 500
    
    # WebSocket events
    if socketio:
        @socketio.on('connect', namespace='/dashboard')
        def handle_connect():
            """Cliente conectado ao dashboard"""
            emit('connected', {'status': 'ok'})
            # Enviar métricas iniciais
            emit('metrics_update', dashboard.get_all_metrics())
        
        @socketio.on('request_metrics', namespace='/dashboard')
        def handle_request_metrics():
            """Cliente solicitou métricas"""
            emit('metrics_update', dashboard.get_all_metrics())
    
    return dashboard_bp

