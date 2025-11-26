#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sistema de Tratamento de Erros Robusto
Códigos de erro específicos, retry logic, e error tracking
"""

import time
import logging
from typing import Dict, Optional, Callable, Any
from functools import wraps
from enum import Enum

class ErrorCode(Enum):
    """Códigos de erro específicos"""
    # Validação
    INVALID_ADDRESS = "E001"
    INVALID_AMOUNT = "E002"
    INVALID_NONCE = "E003"
    INVALID_TIMESTAMP = "E004"
    INVALID_INPUT = "E005"
    
    # Blockchain
    NETWORK_ERROR = "E101"
    TRANSACTION_FAILED = "E102"
    INSUFFICIENT_BALANCE = "E103"
    GAS_ESTIMATION_FAILED = "E104"
    TRANSACTION_TIMEOUT = "E105"
    
    # Bridge
    BRIDGE_NOT_AVAILABLE = "E201"
    INSUFFICIENT_RESERVES = "E202"
    CROSS_CHAIN_FAILED = "E203"
    VALIDATION_FAILED = "E204"
    
    # Segurança
    RATE_LIMIT_EXCEEDED = "E301"
    UNAUTHORIZED = "E302"
    INVALID_SIGNATURE = "E303"
    REPLAY_ATTACK = "E304"
    
    # Sistema
    INTERNAL_ERROR = "E401"
    CONFIGURATION_ERROR = "E402"
    DEPENDENCY_ERROR = "E403"
    TIMEOUT = "E404"

class ErrorHandler:
    """Handler centralizado de erros"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.error_tracking = {}  # Para analytics
        
    def handle_error(
        self,
        error_code: ErrorCode,
        message: str,
        details: Optional[Dict] = None,
        exception: Optional[Exception] = None
    ) -> Dict:
        """
        Trata erro de forma padronizada
        
        Returns:
            {
                "success": False,
                "error_code": str,
                "message": str,
                "details": Dict,
                "timestamp": int
            }
        """
        error_data = {
            "success": False,
            "error_code": error_code.value,
            "message": message,
            "details": details or {},
            "timestamp": int(time.time())
        }
        
        # Log do erro
        log_message = f"[{error_code.value}] {message}"
        if details:
            log_message += f" | Details: {details}"
        if exception:
            log_message += f" | Exception: {str(exception)}"
        
        self.logger.error(log_message, exc_info=exception)
        
        # Tracking para analytics
        self._track_error(error_code, message, details)
        
        return error_data
    
    def _track_error(self, error_code: ErrorCode, message: str, details: Dict):
        """Track erro para analytics"""
        code = error_code.value
        if code not in self.error_tracking:
            self.error_tracking[code] = {
                "count": 0,
                "last_occurrence": None,
                "messages": []
            }
        
        self.error_tracking[code]["count"] += 1
        self.error_tracking[code]["last_occurrence"] = time.time()
        if message not in self.error_tracking[code]["messages"]:
            self.error_tracking[code]["messages"].append(message)
    
    def get_error_stats(self) -> Dict:
        """Retorna estatísticas de erros"""
        return {
            "total_errors": sum(v["count"] for v in self.error_tracking.values()),
            "error_types": {
                code: {
                    "count": data["count"],
                    "last_occurrence": data["last_occurrence"],
                    "sample_messages": data["messages"][:5]
                }
                for code, data in self.error_tracking.items()
            }
        }

def retry_with_backoff(
    max_retries: int = 3,
    initial_delay: float = 1.0,
    max_delay: float = 60.0,
    exponential_base: float = 2.0,
    exceptions: tuple = (Exception,)
):
    """
    Decorator para retry com exponential backoff
    
    Args:
        max_retries: Número máximo de tentativas
        initial_delay: Delay inicial em segundos
        max_delay: Delay máximo em segundos
        exponential_base: Base para cálculo exponencial
        exceptions: Tupla de exceções que devem ser retryadas
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            delay = initial_delay
            last_exception = None
            
            for attempt in range(max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    if attempt < max_retries:
                        time.sleep(min(delay, max_delay))
                        delay *= exponential_base
                    else:
                        raise
            
            if last_exception:
                raise last_exception
        
        return wrapper
    return decorator

def handle_errors(error_code: ErrorCode, default_message: str = "An error occurred"):
    """
    Decorator para capturar e tratar erros automaticamente
    
    Usage:
        @handle_errors(ErrorCode.INTERNAL_ERROR, "Failed to process request")
        def my_function():
            ...
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Dict:
            handler = ErrorHandler()
            try:
                result = func(*args, **kwargs)
                # Se resultado já é um dict com success, retornar como está
                if isinstance(result, dict) and "success" in result:
                    return result
                # Caso contrário, wrappar em formato padrão
                return {"success": True, "data": result}
            except Exception as e:
                return handler.handle_error(
                    error_code,
                    default_message,
                    {"function": func.__name__, "args": str(args), "kwargs": str(kwargs)},
                    e
                )
        return wrapper
    return decorator







