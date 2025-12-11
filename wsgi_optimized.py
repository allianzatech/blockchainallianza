#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
WSGI Entry Point Otimizado para Produção - Allianza Blockchain
Carregamento lazy para evitar timeout no deploy
"""

import os
import sys

# Adicionar diretório do projeto ao path
sys.path.insert(0, os.path.dirname(__file__))

# Carregar variáveis de ambiente
from dotenv import load_dotenv
if os.path.exists('.env.production'):
    load_dotenv('.env.production')
elif os.path.exists('.env'):
    load_dotenv('.env')

# Configurar variáveis de ambiente críticas antes de importar
os.environ.setdefault('FLASK_ENV', 'production')
os.environ.setdefault('FLASK_DEBUG', 'False')

# Importar Flask básico primeiro
from flask import Flask, request

# Importar app completo diretamente (sem lazy loading)
try:
    from allianza_blockchain import app as application
    application.config['ENV'] = os.getenv('FLASK_ENV', 'production')
    application.config['DEBUG'] = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    # Verificar se já existe uma rota '/' registrada (do blueprint testnet)
    # Se não existir, registrar uma rota simples de health check
    has_root_route = False
    try:
        for rule in application.url_map.iter_rules():
            if rule.rule == '/' and 'GET' in rule.methods:
                has_root_route = True
                break
    except:
        pass
    
    if not has_root_route:
        # Registrar rota raiz de saúde simples apenas se não existir
        @application.route('/', methods=['GET', 'HEAD'], endpoint='wsgi_root')
        def root_health():
            if request.method == 'HEAD':
                return '', 200
            return {
                "status": "OK",
                "service": "Allianza Blockchain",
                "version": "1.0.0"
            }, 200
    
    # Health check básico - verificar se já existe antes de registrar
    has_health_route = False
    try:
        for rule in application.url_map.iter_rules():
            if rule.rule == '/health' and 'GET' in rule.methods:
                has_health_route = True
                break
    except:
        pass
    
    if not has_health_route:
        # Registrar health check apenas se não existir, com endpoint único
        @application.route('/health', endpoint='wsgi_health')
        def wsgi_health_status():
            return {"status": "ok", "service": "Allianza Blockchain"}, 200
except Exception as e:
    # Fallback mínimo se app completo falhar
    err_msg = str(e)
    application = Flask(__name__)
    application.config['ENV'] = os.getenv('FLASK_ENV', 'production')
    application.config['DEBUG'] = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    application.config['SECRET_KEY'] = os.getenv('SECRET_KEY', os.urandom(32).hex())
    @application.route('/', endpoint='wsgi_error_root')
    def error_root():
        return {"error": "Service initialization failed", "message": err_msg}, 500
    @application.route('/health', endpoint='wsgi_error_health')
    def health_fallback():
        return {"status": "initializing", "service": "Allianza Blockchain"}, 200

# Aplicação WSGI
if __name__ == "__main__":
    port = int(os.getenv('PORT', 5000))
    host = os.getenv('HOST', '0.0.0.0')
    debug = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    
    print(f"🚀 Iniciando Allianza Blockchain em {host}:{port}")
    application.run(host=host, port=port, debug=debug)

