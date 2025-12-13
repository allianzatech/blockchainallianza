#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔐 Utilitários de Segurança - Allianza Blockchain
Sanitização, validação e proteção contra vulnerabilidades
"""

import html
import re
import json
from typing import Any, Dict, Optional
from urllib.parse import quote, unquote


class SecurityUtils:
    """Utilitários de segurança para prevenir vulnerabilidades"""
    
    @staticmethod
    def escape_html(text: str) -> str:
        """
        Escapa HTML para prevenir XSS
        
        Args:
            text: Texto a ser escapado
            
        Returns:
            Texto escapado
        """
        if not isinstance(text, str):
            text = str(text)
        return html.escape(text, quote=True)
    
    @staticmethod
    def sanitize_for_json(data: Any) -> Any:
        """
        Sanitiza dados para uso seguro em JSON
        
        Args:
            data: Dados a serem sanitizados
            
        Returns:
            Dados sanitizados
        """
        if isinstance(data, str):
            # Remover caracteres de controle
            data = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', data)
            # Limitar tamanho
            if len(data) > 10000:
                data = data[:10000]
            return data
        elif isinstance(data, dict):
            return {k: SecurityUtils.sanitize_for_json(v) for k, v in data.items()}
        elif isinstance(data, list):
            return [SecurityUtils.sanitize_for_json(item) for item in data]
        else:
            return data
    
    @staticmethod
    def sanitize_address(address: str) -> Optional[str]:
        """
        Sanitiza endereço de blockchain
        
        Args:
            address: Endereço a ser sanitizado
            
        Returns:
            Endereço sanitizado ou None se inválido
        """
        if not isinstance(address, str):
            return None
        
        # Remover espaços e converter para minúsculas
        address = address.strip().lower()
        
        # Validar formato básico (hexadecimal)
        if not re.match(r'^[0-9a-f]{40,42}$', address):
            return None
        
        return address
    
    @staticmethod
    def sanitize_tx_hash(tx_hash: str) -> Optional[str]:
        """
        Sanitiza hash de transação
        
        Args:
            tx_hash: Hash a ser sanitizado
            
        Returns:
            Hash sanitizado ou None se inválido
        """
        if not isinstance(tx_hash, str):
            return None
        
        # Remover espaços e converter para minúsculas
        tx_hash = tx_hash.strip().lower()
        
        # Validar formato (hexadecimal, 64 caracteres)
        if not re.match(r'^[0-9a-f]{64}$', tx_hash):
            return None
        
        return tx_hash
    
    @staticmethod
    def validate_input_length(text: str, max_length: int = 1000) -> bool:
        """
        Valida comprimento de input
        
        Args:
            text: Texto a ser validado
            max_length: Comprimento máximo permitido
            
        Returns:
            True se válido, False caso contrário
        """
        if not isinstance(text, str):
            return False
        return len(text) <= max_length
    
    @staticmethod
    def detect_sql_injection(text: str) -> bool:
        """
        Detecta tentativas de SQL injection
        
        Args:
            text: Texto a ser verificado
            
        Returns:
            True se suspeito de SQL injection, False caso contrário
        """
        if not isinstance(text, str):
            return False
        
        text_lower = text.lower()
        
        # Padrões suspeitos
        suspicious_patterns = [
            r"(\bunion\b.*\bselect\b)",
            r"(\bselect\b.*\bfrom\b)",
            r"(\binsert\b.*\binto\b)",
            r"(\bupdate\b.*\bset\b)",
            r"(\bdelete\b.*\bfrom\b)",
            r"(\bdrop\b.*\btable\b)",
            r"(\bexec\b|\bexecute\b)",
            r"(\bxp_\w+)",
            r"(--|\#|\/\*|\*\/)",
            r"(\bor\b.*=.*)",
            r"(\band\b.*=.*)",
            r"('.*'|".*")",
        ]
        
        for pattern in suspicious_patterns:
            if re.search(pattern, text_lower):
                return True
        
        return False
    
    @staticmethod
    def detect_xss(text: str) -> bool:
        """
        Detecta tentativas de XSS
        
        Args:
            text: Texto a ser verificado
            
        Returns:
            True se suspeito de XSS, False caso contrário
        """
        if not isinstance(text, str):
            return False
        
        text_lower = text.lower()
        
        # Padrões suspeitos
        suspicious_patterns = [
            r"<script[^>]*>",
            r"javascript:",
            r"on\w+\s*=",
            r"<iframe[^>]*>",
            r"<img[^>]*src\s*=",
            r"<svg[^>]*onload",
            r"eval\s*\(",
            r"expression\s*\(",
        ]
        
        for pattern in suspicious_patterns:
            if re.search(pattern, text_lower):
                return True
        
        return False
    
    @staticmethod
    def safe_json_stringify(data: Any) -> str:
        """
        Converte dados para JSON de forma segura
        
        Args:
            data: Dados a serem convertidos
            
        Returns:
            String JSON sanitizada
        """
        try:
            sanitized = SecurityUtils.sanitize_for_json(data)
            return json.dumps(sanitized, ensure_ascii=False)
        except Exception:
            return "{}"


# Instância global
security_utils = SecurityUtils()

