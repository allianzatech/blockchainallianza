#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Middleware de Melhorias para Allianza Blockchain
Rate limiting, validação e logging de requisições
"""

from flask import request, jsonify
from typing import Optional
import time
import logging

logger = logging.getLogger(__name__)

# Importar rate limiter global
try:
    from rate_limiter import global_rate_limiter
    RATE_LIMITER_AVAILABLE = True
except ImportError:
    RATE_LIMITER_AVAILABLE = False
    global_rate_limiter = None

# Importar structured logging se disponível
try:
    from structured_logging import StructuredLogger
    structured_logger = StructuredLogger("middleware")
    STRUCTURED_LOGGING_AVAILABLE = True
except ImportError:
    STRUCTURED_LOGGING_AVAILABLE = False
    structured_logger = None


def rate_limit_middleware() -> Optional[dict]:
    """
    Middleware de rate limiting
    Retorna resposta de erro se rate limit excedido, None caso contrário
    """
    if not RATE_LIMITER_AVAILABLE or not global_rate_limiter:
        return None
    
    try:
        # Obter identificador (IP do cliente)
        identifier = request.remote_addr or "unknown"
        
        # Verificar rate limit
        is_allowed, error_message = global_rate_limiter.is_allowed(identifier)
        
        if not is_allowed:
            if structured_logger:
                structured_logger.warning("Rate limit excedido", {
                    "ip": identifier,
                    "path": request.path,
                    "method": request.method
                })
            
            return jsonify({
                "success": False,
                "error": "Rate limit excedido",
                "message": error_message,
                "retry_after": 60  # segundos
            }), 429
        
        return None
    
    except Exception as e:
        logger.error(f"Erro no rate limit middleware: {e}")
        # Em caso de erro, permitir requisição (fail-open)
        return None


def validate_request() -> Optional[dict]:
    """
    Valida requisição básica
    Retorna resposta de erro se inválida, None caso contrário
    """
    try:
        # Validar método HTTP
        if request.method not in ['GET', 'POST', 'PUT', 'DELETE', 'PATCH']:
            return jsonify({
                "success": False,
                "error": "Método HTTP não permitido"
            }), 405
        
        # Validar tamanho do payload (máximo 10MB)
        if request.content_length and request.content_length > 10 * 1024 * 1024:
            return jsonify({
                "success": False,
                "error": "Payload muito grande (máximo 10MB)"
            }), 413
        
        return None
    
    except Exception as e:
        logger.error(f"Erro na validação de requisição: {e}")
        return None


def log_request():
    """
    Registra requisição para auditoria
    """
    try:
        log_data = {
            "ip": request.remote_addr,
            "method": request.method,
            "path": request.path,
            "user_agent": request.headers.get("User-Agent", "Unknown"),
            "timestamp": time.time()
        }
        
        if structured_logger:
            structured_logger.info("Requisição recebida", log_data)
        else:
            logger.info(f"Requisição: {request.method} {request.path} de {request.remote_addr}")
    
    except Exception as e:
        logger.error(f"Erro ao registrar requisição: {e}")
















