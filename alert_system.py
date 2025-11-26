#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🚨 SISTEMA DE ALERTAS E NOTIFICAÇÕES INTELIGENTES
Sistema completo de alertas com múltiplos canais de notificação
"""

import time
import json
import smtplib
import requests
from typing import Dict, List, Optional, Callable
from datetime import datetime, timedelta
from collections import defaultdict, deque
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from enum import Enum

class AlertLevel(Enum):
    """Níveis de alerta"""
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"
    EMERGENCY = "emergency"

class AlertChannel(Enum):
    """Canais de notificação"""
    EMAIL = "email"
    SMS = "sms"
    WEBHOOK = "webhook"
    DASHBOARD = "dashboard"
    SLACK = "slack"
    TELEGRAM = "telegram"

class AlertSystem:
    """Sistema de Alertas e Notificações Inteligentes"""
    
    def __init__(self):
        self.alerts = deque(maxlen=1000)  # Últimos 1000 alertas
        self.active_alerts = {}  # alert_id -> alert_data
        self.alert_rules = []  # Regras de alerta
        self.notification_channels = {
            AlertChannel.DASHBOARD: True,  # Sempre ativo
            AlertChannel.EMAIL: False,
            AlertChannel.SMS: False,
            AlertChannel.WEBHOOK: False,
            AlertChannel.SLACK: False,
            AlertChannel.TELEGRAM: False
        }
        
        # Configurações de canais
        self.channel_config = {
            AlertChannel.EMAIL: {
                "smtp_server": None,
                "smtp_port": 587,
                "username": None,
                "password": None,
                "from_email": None,
                "to_emails": []
            },
            AlertChannel.WEBHOOK: {
                "urls": []
            },
            AlertChannel.SLACK: {
                "webhook_url": None
            },
            AlertChannel.TELEGRAM: {
                "bot_token": None,
                "chat_ids": []
            }
        }
        
        # Thresholds adaptativos
        self.adaptive_thresholds = defaultdict(lambda: {
            "base_value": 0,
            "current_value": 0,
            "adjustment_factor": 1.0
        })
        
        # Agrupamento de alertas
        self.alert_groups = defaultdict(list)
        
    def add_alert_rule(
        self,
        rule_id: str,
        condition: Callable,
        level: AlertLevel,
        channels: List[AlertChannel],
        cooldown: int = 300  # 5 minutos
    ):
        """
        Adicionar regra de alerta
        
        Args:
            rule_id: ID único da regra
            condition: Função que retorna True se alerta deve ser disparado
            level: Nível do alerta
            channels: Canais de notificação
            cooldown: Tempo mínimo entre alertas (segundos)
        """
        self.alert_rules.append({
            "rule_id": rule_id,
            "condition": condition,
            "level": level,
            "channels": channels,
            "cooldown": cooldown,
            "last_triggered": 0
        })
    
    def create_alert(
        self,
        level: AlertLevel,
        title: str,
        message: str,
        component: str = "system",
        metadata: Optional[Dict] = None,
        channels: Optional[List[AlertChannel]] = None
    ) -> Dict:
        """
        Criar e disparar alerta
        
        Returns:
            {
                "success": bool,
                "alert_id": str,
                "notified_channels": List[str]
            }
        """
        alert_id = f"alert_{int(time.time())}_{len(self.alerts)}"
        
        alert_data = {
            "alert_id": alert_id,
            "level": level.value,
            "title": title,
            "message": message,
            "component": component,
            "metadata": metadata or {},
            "timestamp": time.time(),
            "datetime": datetime.now().isoformat(),
            "acknowledged": False,
            "resolved": False
        }
        
        # Adicionar aos alertas
        self.alerts.append(alert_data)
        self.active_alerts[alert_id] = alert_data
        
        # Agrupar alertas similares
        group_key = f"{component}_{level.value}"
        self.alert_groups[group_key].append(alert_id)
        
        # Determinar canais de notificação
        if channels is None:
            # Usar canais padrão baseado no nível
            if level == AlertLevel.CRITICAL or level == AlertLevel.EMERGENCY:
                channels = [AlertChannel.DASHBOARD, AlertChannel.EMAIL, AlertChannel.WEBHOOK]
            elif level == AlertLevel.WARNING:
                channels = [AlertChannel.DASHBOARD, AlertChannel.EMAIL]
            else:
                channels = [AlertChannel.DASHBOARD]
        
        # Enviar notificações
        notified_channels = []
        for channel in channels:
            if self.notification_channels.get(channel, False):
                try:
                    if self._send_notification(channel, alert_data):
                        notified_channels.append(channel.value)
                except Exception as e:
                    print(f"⚠️  Erro ao enviar notificação via {channel.value}: {e}")
        
        # Sempre notificar no dashboard
        if AlertChannel.DASHBOARD not in channels:
            notified_channels.append(AlertChannel.DASHBOARD.value)
        
        return {
            "success": True,
            "alert_id": alert_id,
            "notified_channels": notified_channels
        }
    
    def _send_notification(self, channel: AlertChannel, alert_data: Dict) -> bool:
        """Enviar notificação via canal específico"""
        if channel == AlertChannel.EMAIL:
            return self._send_email(alert_data)
        elif channel == AlertChannel.WEBHOOK:
            return self._send_webhook(alert_data)
        elif channel == AlertChannel.SLACK:
            return self._send_slack(alert_data)
        elif channel == AlertChannel.TELEGRAM:
            return self._send_telegram(alert_data)
        elif channel == AlertChannel.SMS:
            return self._send_sms(alert_data)
        return False
    
    def _send_email(self, alert_data: Dict) -> bool:
        """Enviar alerta por email"""
        config = self.channel_config[AlertChannel.EMAIL]
        
        if not config.get("smtp_server") or not config.get("to_emails"):
            return False
        
        try:
            msg = MIMEMultipart()
            msg['From'] = config["from_email"]
            msg['To'] = ", ".join(config["to_emails"])
            msg['Subject'] = f"[{alert_data['level'].upper()}] {alert_data['title']}"
            
            body = f"""
            Alerta do Sistema Allianza Blockchain
            
            Nível: {alert_data['level'].upper()}
            Componente: {alert_data['component']}
            Título: {alert_data['title']}
            Mensagem: {alert_data['message']}
            Data/Hora: {alert_data['datetime']}
            
            Metadata: {json.dumps(alert_data.get('metadata', {}), indent=2)}
            """
            
            msg.attach(MIMEText(body, 'plain'))
            
            server = smtplib.SMTP(config["smtp_server"], config["smtp_port"])
            server.starttls()
            if config.get("username") and config.get("password"):
                server.login(config["username"], config["password"])
            server.send_message(msg)
            server.quit()
            
            return True
        except Exception as e:
            print(f"Erro ao enviar email: {e}")
            return False
    
    def _send_webhook(self, alert_data: Dict) -> bool:
        """Enviar alerta via webhook"""
        config = self.channel_config[AlertChannel.WEBHOOK]
        
        if not config.get("urls"):
            return False
        
        success = True
        for url in config["urls"]:
            try:
                response = requests.post(
                    url,
                    json=alert_data,
                    timeout=5
                )
                if response.status_code not in [200, 201, 202]:
                    success = False
            except Exception as e:
                print(f"Erro ao enviar webhook para {url}: {e}")
                success = False
        
        return success
    
    def _send_slack(self, alert_data: Dict) -> bool:
        """Enviar alerta para Slack"""
        config = self.channel_config[AlertChannel.SLACK]
        
        if not config.get("webhook_url"):
            return False
        
        try:
            # Formatar mensagem para Slack
            color_map = {
                "info": "#36a64f",
                "warning": "#ff9900",
                "critical": "#ff0000",
                "emergency": "#8b0000"
            }
            
            slack_message = {
                "attachments": [{
                    "color": color_map.get(alert_data["level"], "#808080"),
                    "title": alert_data["title"],
                    "text": alert_data["message"],
                    "fields": [
                        {
                            "title": "Componente",
                            "value": alert_data["component"],
                            "short": True
                        },
                        {
                            "title": "Nível",
                            "value": alert_data["level"].upper(),
                            "short": True
                        },
                        {
                            "title": "Data/Hora",
                            "value": alert_data["datetime"],
                            "short": False
                        }
                    ]
                }]
            }
            
            response = requests.post(
                config["webhook_url"],
                json=slack_message,
                timeout=5
            )
            
            return response.status_code in [200, 201, 202]
        except Exception as e:
            print(f"Erro ao enviar para Slack: {e}")
            return False
    
    def _send_telegram(self, alert_data: Dict) -> bool:
        """Enviar alerta para Telegram"""
        config = self.channel_config[AlertChannel.TELEGRAM]
        
        if not config.get("bot_token") or not config.get("chat_ids"):
            return False
        
        try:
            message = f"""
🔔 *Alerta: {alert_data['title']}*

*Nível:* {alert_data['level'].upper()}
*Componente:* {alert_data['component']}
*Mensagem:* {alert_data['message']}
*Data/Hora:* {alert_data['datetime']}
            """
            
            for chat_id in config["chat_ids"]:
                url = f"https://api.telegram.org/bot{config['bot_token']}/sendMessage"
                response = requests.post(
                    url,
                    json={
                        "chat_id": chat_id,
                        "text": message,
                        "parse_mode": "Markdown"
                    },
                    timeout=5
                )
                if response.status_code not in [200, 201]:
                    return False
            
            return True
        except Exception as e:
            print(f"Erro ao enviar para Telegram: {e}")
            return False
    
    def _send_sms(self, alert_data: Dict) -> bool:
        """Enviar alerta por SMS (requer serviço externo)"""
        # Implementação depende de serviço SMS (Twilio, etc.)
        # Por enquanto, retorna False
        return False
    
    def configure_channel(
        self,
        channel: AlertChannel,
        config: Dict
    ) -> Dict:
        """Configurar canal de notificação"""
        if channel not in self.channel_config:
            return {
                "success": False,
                "error": f"Canal {channel.value} não suportado"
            }
        
        self.channel_config[channel].update(config)
        self.notification_channels[channel] = True
        
        return {
            "success": True,
            "channel": channel.value,
            "configured": True
        }
    
    def enable_channel(self, channel: AlertChannel):
        """Habilitar canal de notificação"""
        self.notification_channels[channel] = True
    
    def disable_channel(self, channel: AlertChannel):
        """Desabilitar canal de notificação"""
        self.notification_channels[channel] = False
    
    def acknowledge_alert(self, alert_id: str) -> Dict:
        """Reconhecer alerta"""
        if alert_id not in self.active_alerts:
            return {
                "success": False,
                "error": "Alerta não encontrado"
            }
        
        self.active_alerts[alert_id]["acknowledged"] = True
        self.active_alerts[alert_id]["acknowledged_at"] = time.time()
        
        return {
            "success": True,
            "alert_id": alert_id
        }
    
    def resolve_alert(self, alert_id: str) -> Dict:
        """Resolver alerta"""
        if alert_id not in self.active_alerts:
            return {
                "success": False,
                "error": "Alerta não encontrado"
            }
        
        self.active_alerts[alert_id]["resolved"] = True
        self.active_alerts[alert_id]["resolved_at"] = time.time()
        
        # Remover de alertas ativos após 1 hora
        # (manter no histórico)
        
        return {
            "success": True,
            "alert_id": alert_id
        }
    
    def get_active_alerts(
        self,
        level: Optional[AlertLevel] = None,
        component: Optional[str] = None
    ) -> List[Dict]:
        """Obter alertas ativos com filtros"""
        alerts = []
        for alert_id, alert_data in self.active_alerts.items():
            if alert_data.get("resolved"):
                continue
            if level and alert_data["level"] != level.value:
                continue
            if component and alert_data["component"] != component:
                continue
            alerts.append(alert_data)
        
        return sorted(alerts, key=lambda x: x["timestamp"], reverse=True)
    
    def get_alert_statistics(self) -> Dict:
        """Obter estatísticas de alertas"""
        total = len(self.alerts)
        active = len([a for a in self.active_alerts.values() if not a.get("resolved")])
        
        by_level = defaultdict(int)
        by_component = defaultdict(int)
        
        for alert in self.alerts:
            by_level[alert["level"]] += 1
            by_component[alert["component"]] += 1
        
        return {
            "total_alerts": total,
            "active_alerts": active,
            "resolved_alerts": total - active,
            "by_level": dict(by_level),
            "by_component": dict(by_component),
            "channels_enabled": {
                ch.value: enabled
                for ch, enabled in self.notification_channels.items()
                if enabled
            }
        }



