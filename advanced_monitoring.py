# advanced_monitoring.py
# 📊 ADVANCED MONITORING - ALLIANZA BLOCKCHAIN
# Sistema de monitoramento avançado

import time
import logging
from typing import Dict, List, Optional
from collections import deque, defaultdict

logger = logging.getLogger(__name__)

class AdvancedMonitoring:
    """
    📊 ADVANCED MONITORING
    Sistema de monitoramento avançado
    
    Características:
    - Métricas em tempo real
    - Alertas automáticos
    - Dashboards interativos
    - Análise de performance
    - Detecção de anomalias (IA)
    """
    
    def __init__(self):
        self.metrics = defaultdict(deque)
        self.alerts = deque(maxlen=1000)
        self.anomalies = deque(maxlen=100)
        self.metric_history = {}
        
        logger.info("📊 ADVANCED MONITORING: Inicializado!")
        print("📊 ADVANCED MONITORING: Sistema inicializado!")
        print("   • Métricas em tempo real")
        print("   • Alertas automáticos")
        print("   • Detecção de anomalias")
    
    def record_metric(self, metric_name: str, value: float, tags: Dict = None):
        """
        Registra métrica
        
        Args:
            metric_name: Nome da métrica
            value: Valor
            tags: Tags opcionais
        """
        timestamp = time.time()
        
        metric_data = {
            "name": metric_name,
            "value": value,
            "timestamp": timestamp,
            "tags": tags or {}
        }
        
        self.metrics[metric_name].append(metric_data)
        
        # Manter apenas últimos 1000 valores
        if len(self.metrics[metric_name]) > 1000:
            self.metrics[metric_name].popleft()
        
        # Verificar alertas
        self._check_alerts(metric_name, value)
        
        # Detectar anomalias
        self._detect_anomalies(metric_name, value)
    
    def _check_alerts(self, metric_name: str, value: float):
        """Verifica alertas"""
        # Alertas básicos
        if metric_name == "transaction_latency" and value > 1000:  # > 1s
            self.alerts.append({
                "type": "high_latency",
                "metric": metric_name,
                "value": value,
                "timestamp": time.time(),
                "severity": "warning"
            })
        
        if metric_name == "error_rate" and value > 0.1:  # > 10%
            self.alerts.append({
                "type": "high_error_rate",
                "metric": metric_name,
                "value": value,
                "timestamp": time.time(),
                "severity": "critical"
            })
    
    def _detect_anomalies(self, metric_name: str, value: float):
        """Detecta anomalias usando IA simples"""
        if metric_name not in self.metrics or len(self.metrics[metric_name]) < 10:
            return
        
        # Calcular média e desvio padrão
        values = [m["value"] for m in list(self.metrics[metric_name])[-10:]]
        avg = sum(values) / len(values)
        std = (sum((v - avg) ** 2 for v in values) / len(values)) ** 0.5
        
        # Anomalia se valor está > 3 desvios padrão
        if abs(value - avg) > 3 * std:
            self.anomalies.append({
                "metric": metric_name,
                "value": value,
                "expected": avg,
                "deviation": abs(value - avg),
                "timestamp": time.time()
            })
    
    def get_metrics(self, metric_name: Optional[str] = None) -> Dict:
        """Retorna métricas"""
        if metric_name:
            return {
                "metric": metric_name,
                "values": list(self.metrics.get(metric_name, [])),
                "count": len(self.metrics.get(metric_name, []))
            }
        else:
            return {
                "metrics": {name: len(values) for name, values in self.metrics.items()},
                "total_metrics": len(self.metrics)
            }
    
    def get_alerts(self, limit: int = 10) -> List[Dict]:
        """Retorna alertas recentes"""
        return list(self.alerts)[-limit:]
    
    def get_anomalies(self, limit: int = 10) -> List[Dict]:
        """Retorna anomalias recentes"""
        return list(self.anomalies)[-limit:]
    
    def get_dashboard_data(self) -> Dict:
        """Retorna dados para dashboard"""
        return {
            "metrics": {name: len(values) for name, values in self.metrics.items()},
            "recent_alerts": list(self.alerts)[-10:],
            "recent_anomalies": list(self.anomalies)[-10:],
            "timestamp": time.time()
        }









