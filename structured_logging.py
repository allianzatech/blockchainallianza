#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sistema de Logging Estruturado (JSON)
Auditoria e tracking de operações críticas
"""

import json
import logging
import time
from datetime import datetime
from typing import Dict, Optional, Any
from enum import Enum

class LogLevel(Enum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"

class AuditEvent(Enum):
    """Eventos que devem ser auditados"""
    TRANSACTION_CREATED = "transaction_created"
    TRANSACTION_CONFIRMED = "transaction_confirmed"
    TRANSACTION_FAILED = "transaction_failed"
    CROSS_CHAIN_INITIATED = "cross_chain_initiated"
    CROSS_CHAIN_COMPLETED = "cross_chain_completed"
    BRIDGE_OPERATION = "bridge_operation"
    KEY_GENERATED = "key_generated"
    SIGNATURE_CREATED = "signature_created"
    VALIDATION_PERFORMED = "validation_performed"
    SECURITY_EVENT = "security_event"

class StructuredLogger:
    """Logger estruturado com suporte a auditoria"""
    
    def __init__(self, name: str, log_file: Optional[str] = None):
        self.name = name
        self.logger = logging.getLogger(name)
        self.log_file = log_file
        
        # Configurar handler para arquivo se especificado
        if log_file:
            file_handler = logging.FileHandler(log_file)
            file_handler.setFormatter(logging.Formatter('%(message)s'))
            self.logger.addHandler(file_handler)
        
        # Handler para console
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(logging.Formatter('%(message)s'))
        self.logger.addHandler(console_handler)
        
        self.logger.setLevel(logging.INFO)
    
    def _log_structured(
        self,
        level: LogLevel,
        message: str,
        data: Optional[Dict] = None,
        audit: bool = False,
        audit_event: Optional[AuditEvent] = None
    ):
        """Log estruturado em formato JSON"""
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": level.value,
            "logger": self.name,
            "message": message,
            "data": data or {}
        }
        
        # Adicionar informações de auditoria se necessário
        if audit:
            log_entry["audit"] = True
            if audit_event:
                log_entry["audit_event"] = audit_event.value
        
        # Converter para JSON
        log_json = json.dumps(log_entry, ensure_ascii=False)
        
        # Log usando nível apropriado
        if level == LogLevel.DEBUG:
            self.logger.debug(log_json)
        elif level == LogLevel.INFO:
            self.logger.info(log_json)
        elif level == LogLevel.WARNING:
            self.logger.warning(log_json)
        elif level == LogLevel.ERROR:
            self.logger.error(log_json)
        elif level == LogLevel.CRITICAL:
            self.logger.critical(log_json)
    
    def debug(self, message: str, data: Optional[Dict] = None):
        """Log de debug"""
        self._log_structured(LogLevel.DEBUG, message, data)
    
    def info(self, message: str, data: Optional[Dict] = None, audit: bool = False, audit_event: Optional[AuditEvent] = None):
        """Log de informação"""
        self._log_structured(LogLevel.INFO, message, data, audit, audit_event)
    
    def warning(self, message: str, data: Optional[Dict] = None):
        """Log de aviso"""
        self._log_structured(LogLevel.WARNING, message, data)
    
    def error(self, message: str, data: Optional[Dict] = None, audit: bool = True, audit_event: Optional[AuditEvent] = None):
        """Log de erro"""
        self._log_structured(LogLevel.ERROR, message, data, audit, audit_event)
    
    def critical(self, message: str, data: Optional[Dict] = None, audit: bool = True, audit_event: Optional[AuditEvent] = None):
        """Log crítico"""
        self._log_structured(LogLevel.CRITICAL, message, data, audit, audit_event)
    
    def audit(
        self,
        event: AuditEvent,
        message: str,
        data: Optional[Dict] = None
    ):
        """Log de auditoria"""
        self._log_structured(
            LogLevel.INFO,
            message,
            data,
            audit=True,
            audit_event=event
        )

# Instância global
default_logger = StructuredLogger("allianza_blockchain", "allianza_blockchain_structured.log")











