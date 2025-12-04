#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🛡️ Proteção CSRF - Allianza Blockchain
Implementa proteção contra Cross-Site Request Forgery
"""

import secrets
import hashlib
from functools import wraps
from flask import request, session, jsonify, g
from typing import Optional, Callable


class CSRFProtection:
    """Sistema de proteção CSRF"""
    
    def __init__(self, app=None):
        self.app = app
        if app:
            self.init_app(app)
    
    def init_app(self, app):
        """Inicializar proteção CSRF no app Flask"""
        app.config.setdefault('CSRF_ENABLED', True)
        app.config.setdefault('CSRF_SECRET_KEY', secrets.token_hex(32))
        app.config.setdefault('CSRF_TOKEN_LENGTH', 32)
        
        # Adicionar token CSRF à sessão se não existir
        @app.before_request
        def ensure_csrf_token():
            if 'csrf_token' not in session:
                session['csrf_token'] = self.generate_token()
    
    @staticmethod
    def generate_token() -> str:
        """Gerar token CSRF"""
        return secrets.token_urlsafe(32)
    
    @staticmethod
    def get_token() -> Optional[str]:
        """Obter token CSRF da sessão"""
        return session.get('csrf_token')
    
    @staticmethod
    def validate_token(token: Optional[str]) -> bool:
        """Validar token CSRF"""
        if not token:
            return False
        
        session_token = session.get('csrf_token')
        if not session_token:
            return False
        
        # Comparação segura
        return secrets.compare_digest(token, session_token)
    
    @staticmethod
    def require_csrf(f: Callable) -> Callable:
        """
        Decorator para proteger rotas contra CSRF
        
        Uso:
            @csrf_protection.require_csrf
            @app.route('/api/transfer', methods=['POST'])
            def transfer():
                ...
        """
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Métodos seguros não precisam de CSRF
            if request.method in ['GET', 'HEAD', 'OPTIONS']:
                return f(*args, **kwargs)
            
            # Verificar token CSRF
            token = None
            
            # Tentar obter do header
            token = request.headers.get('X-CSRF-Token')
            
            # Tentar obter do form
            if not token:
                token = request.form.get('csrf_token')
            
            # Tentar obter do JSON
            if not token and request.is_json:
                data = request.get_json(silent=True)
                if data:
                    token = data.get('csrf_token')
            
            # Validar token
            if not CSRFProtection.validate_token(token):
                return jsonify({
                    "error": "CSRF token inválido ou ausente",
                    "message": "Por favor, recarregue a página e tente novamente."
                }), 403
            
            return f(*args, **kwargs)
        
        return decorated_function


# Instância global
csrf_protection = CSRFProtection()

