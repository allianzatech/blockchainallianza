#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🛡️ Security Middleware - Allianza Blockchain
Headers de segurança e validações adicionais
"""

from flask import request, jsonify, g
from functools import wraps
import os
import secrets
import hashlib

def setup_security_headers(app):
    """Configurar headers de segurança"""
    
    @app.after_request
    def set_security_headers(response):
        """Adicionar headers de segurança a todas as respostas"""
        
        # Gerar nonce único para esta requisição (para scripts inline seguros)
        nonce = secrets.token_urlsafe(16)
        g.csp_nonce = nonce
        
        # Content Security Policy
        # Nota: Mantendo 'unsafe-inline' temporariamente para compatibilidade
        # Ideal: Migrar todos os scripts inline para arquivos externos ou usar nonces
        csp = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline' cdn.tailwindcss.com cdnjs.cloudflare.com cdn.jsdelivr.net; "
            "style-src 'self' 'unsafe-inline' cdn.tailwindcss.com cdnjs.cloudflare.com; "
            "img-src 'self' data: https:; "
            "font-src 'self' data: cdnjs.cloudflare.com; "
            "connect-src 'self' https://testnet.allianza.tech wss://testnet.allianza.tech; "
            "frame-ancestors 'none'; "
            "base-uri 'self'; "
            "form-action 'self'; "
            "object-src 'none'; "
            "upgrade-insecure-requests"
        )
        response.headers['Content-Security-Policy'] = csp
        
        # Cross-Origin-Embedder-Policy (COEP) - Adicionado conforme recomendação
        # Nota: 'require-corp' pode quebrar alguns recursos externos
        # Usando 'credentialless' como alternativa mais permissiva
        response.headers['Cross-Origin-Embedder-Policy'] = 'credentialless'
        
        # Cross-Origin-Opener-Policy (COOP) - Adicionado conforme recomendação
        response.headers['Cross-Origin-Opener-Policy'] = 'same-origin'
        
        # Cross-Origin-Resource-Policy (CORP) - Adicionado conforme recomendação
        response.headers['Cross-Origin-Resource-Policy'] = 'same-origin'
        
        # X-Content-Type-Options
        response.headers['X-Content-Type-Options'] = 'nosniff'
        
        # X-Frame-Options
        response.headers['X-Frame-Options'] = 'DENY'
        
        # X-XSS-Protection
        response.headers['X-XSS-Protection'] = '1; mode=block'
        
        # Referrer Policy
        response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        
        # Permissions Policy
        response.headers['Permissions-Policy'] = (
            'geolocation=(), microphone=(), camera=(), payment=()'
        )
        
        # HSTS (apenas em HTTPS)
        if request.is_secure or request.headers.get('X-Forwarded-Proto') == 'https':
            response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains; preload'
        
        # Remove server header (se possível)
        if 'Server' in response.headers:
            del response.headers['Server']
        
        return response
    
    # Limitar tamanho de request
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB
    
    @app.errorhandler(413)
    def request_entity_too_large(error):
        """Handler para requests muito grandes"""
        return jsonify({
            "error": "Request too large",
            "message": "Maximum request size is 16MB"
        }), 413

def require_https(f):
    """Decorator para forçar HTTPS em produção"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if os.getenv('FLASK_ENV') == 'production':
            if not request.is_secure and request.headers.get('X-Forwarded-Proto') != 'https':
                from flask import redirect
                return redirect(request.url.replace('http://', 'https://'), code=301)
        return f(*args, **kwargs)
    return decorated_function

def validate_request_size():
    """Validar tamanho do request"""
    if request.content_length and request.content_length > 16 * 1024 * 1024:
        return jsonify({
            "error": "Request too large",
            "message": "Maximum request size is 16MB"
        }), 413
    return None

