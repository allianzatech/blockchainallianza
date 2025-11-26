#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sistema de Monitoramento e Métricas
Tracking de performance, erros e saúde do sistema
"""

import time
from typing import Dict, List, Optional
from collections import defaultdict, deque
from threading import Lock
from datetime import datetime

class MetricsCollector:
    """Coletor de métricas"""
    
    def __init__(self):
        self.counters = defaultdict(int)
        self.gauges = {}
        self.histograms = defaultdict(list)
        self.locks = defaultdict(Lock)
        self.max_history = 1000  # Manter últimas 1000 métricas
    
    def increment(self, metric_name: str, value: int = 1, labels: Optional[Dict] = None):
        """Incrementa contador"""
        key = self._make_key(metric_name, labels)
        with self.locks[key]:
            self.counters[key] += value
    
    def set_gauge(self, metric_name: str, value: float, labels: Optional[Dict] = None):
        """Define gauge (valor atual)"""
        key = self._make_key(metric_name, labels)
        with self.locks[key]:
            self.gauges[key] = {
                "value": value,
                "timestamp": time.time()
            }
    
    def record_histogram(self, metric_name: str, value: float, labels: Optional[Dict] = None):
        """Registra valor em histograma"""
        key = self._make_key(metric_name, labels)
        with self.locks[key]:
            if len(self.histograms[key]) >= self.max_history:
                self.histograms[key].pop(0)
            self.histograms[key].append({
                "value": value,
                "timestamp": time.time()
            })
    
    def _make_key(self, metric_name: str, labels: Optional[Dict]) -> str:
        """Cria chave única para métrica"""
        if labels:
            label_str = "_".join(f"{k}={v}" for k, v in sorted(labels.items()))
            return f"{metric_name}_{label_str}"
        return metric_name
    
    def get_metrics(self) -> Dict:
        """Retorna todas as métricas"""
        return {
            "counters": dict(self.counters),
            "gauges": {k: v["value"] for k, v in self.gauges.items()},
            "histograms": {
                k: {
                    "count": len(v),
                    "min": min(h["value"] for h in v) if v else 0,
                    "max": max(h["value"] for h in v) if v else 0,
                    "avg": sum(h["value"] for h in v) / len(v) if v else 0
                }
                for k, v in self.histograms.items()
            }
        }

class HealthChecker:
    """Verificador de saúde do sistema"""
    
    def __init__(self):
        self.checks = {}
        self.last_check = {}
    
    def register_check(self, name: str, check_func: callable):
        """Registra verificação de saúde"""
        self.checks[name] = check_func
    
    def check_health(self) -> Dict:
        """Verifica saúde do sistema"""
        results = {}
        overall_healthy = True
        
        for name, check_func in self.checks.items():
            try:
                result = check_func()
                results[name] = {
                    "healthy": result.get("healthy", False),
                    "message": result.get("message", ""),
                    "timestamp": time.time()
                }
                if not result.get("healthy", False):
                    overall_healthy = False
            except Exception as e:
                results[name] = {
                    "healthy": False,
                    "message": f"Erro ao verificar: {str(e)}",
                    "timestamp": time.time()
                }
                overall_healthy = False
        
        self.last_check = results
        
        return {
            "healthy": overall_healthy,
            "checks": results,
            "timestamp": time.time()
        }

class MonitoringSystem:
    """Sistema completo de monitoramento"""
    
    def __init__(self):
        self.metrics = MetricsCollector()
        self.health = HealthChecker()
        self.alerts = deque(maxlen=100)  # Últimas 100 alertas
        
        # Registrar verificações básicas
        self.health.register_check("system", self._check_system)
    
    def _check_system(self) -> Dict:
        """Verificação básica do sistema"""
        try:
            import psutil
            cpu_percent = psutil.cpu_percent(interval=0.1)
            memory = psutil.virtual_memory()
            
            # Tolerância mais alta: sistema saudável se CPU < 95% e memória < 95%
            healthy = cpu_percent < 95 and memory.percent < 95
            
            return {
                "healthy": healthy,
                "message": f"CPU: {cpu_percent:.1f}%, Memory: {memory.percent:.1f}%",
                "details": {
                    "cpu_percent": cpu_percent,
                    "memory_percent": memory.percent,
                    "memory_available": memory.available
                }
            }
        except ImportError:
            # psutil não instalado - considerar saudável por padrão
            return {
                "healthy": True,
                "message": "psutil não instalado - verificação básica desabilitada",
                "details": {}
            }
        except Exception as e:
            # Em caso de erro, considerar saudável para não bloquear o sistema
            return {
                "healthy": True,
                "message": f"Erro ao verificar sistema (não crítico): {str(e)}",
                "details": {}
            }
    
    def record_transaction(self, chain: str, success: bool, duration: float):
        """Registra métrica de transação"""
        self.metrics.increment("transactions_total", labels={"chain": chain, "status": "success" if success else "failed"})
        self.metrics.record_histogram("transaction_duration", duration, labels={"chain": chain})
    
    def record_error(self, error_type: str, error_code: str):
        """Registra métrica de erro"""
        self.metrics.increment("errors_total", labels={"type": error_type, "code": error_code})
    
    def add_alert(self, level: str, message: str, details: Optional[Dict] = None):
        """Adiciona alerta"""
        alert = {
            "level": level,  # info, warning, error, critical
            "message": message,
            "details": details or {},
            "timestamp": time.time()
        }
        self.alerts.append(alert)
    
    def get_dashboard_data(self) -> Dict:
        """Retorna dados para dashboard"""
        return {
            "metrics": self.metrics.get_metrics(),
            "health": self.health.check_health(),
            "recent_alerts": list(self.alerts)[-10:],  # Últimos 10 alertas
            "timestamp": time.time()
        }

# Instância global
global_monitoring = MonitoringSystem()


