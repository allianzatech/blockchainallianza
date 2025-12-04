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
from flask import Flask

# Criar app mínimo inicialmente
application = Flask(__name__)
application.config['ENV'] = os.getenv('FLASK_ENV', 'production')
application.config['DEBUG'] = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
application.config['SECRET_KEY'] = os.getenv('SECRET_KEY', os.urandom(32).hex())

# Health check básico (deve responder imediatamente)
@application.route('/health')
def health_check():
    """Health check rápido para evitar timeout"""
    import socket
    try:
        # Verificar se a porta está sendo escutada
        port = int(os.getenv('PORT', 5000))
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex(('0.0.0.0', port))
        sock.close()
        port_status = "open" if result == 0 else "closed"
    except:
        port_status = "unknown"
    
    return {
        "status": "ok" if _app_loaded else "initializing",
        "service": "Allianza Blockchain",
        "port": os.getenv('PORT', '5000'),
        "port_status": port_status
    }, 200

# Carregar app completo de forma lazy
_app_loaded = False
_full_app = None

def _load_full_app():
    """Carregar aplicação completa de forma lazy"""
    global _app_loaded, _full_app
    
    if _app_loaded:
        return _full_app
    
    try:
        print("🔄 Carregando Allianza Blockchain (isso pode levar alguns segundos)...")
        
        # Importar app completo
        from allianza_blockchain import app as full_app
        
        # Configurar para produção
        full_app.config['ENV'] = os.getenv('FLASK_ENV', 'production')
        full_app.config['DEBUG'] = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
        
        _full_app = full_app
        _app_loaded = True
        
        print("✅ Allianza Blockchain carregado com sucesso!")
        return full_app
        
    except Exception as e:
        error_message = str(e)
        print(f"❌ Erro ao carregar Allianza Blockchain: {error_message}")
        import traceback
        traceback.print_exc()
        
        # Retornar app mínimo com mensagem de erro
        @application.route('/')
        def error():
            return {"error": "Service initialization failed", "message": error_message}, 500
        
        return application

# Middleware para carregar app completo na primeira requisição real
@application.before_request
def load_app_if_needed():
    """Carregar app completo na primeira requisição"""
    global application
    from flask import request
    
    # Se não for health check e app não foi carregado, carregar
    if request.path != '/health' and not _app_loaded:
        application = _load_full_app()

# Aplicação WSGI
if __name__ == "__main__":
    port = int(os.getenv('PORT', 5000))
    host = os.getenv('HOST', '0.0.0.0')
    debug = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    
    print(f"🚀 Iniciando Allianza Blockchain em {host}:{port}")
    application.run(host=host, port=port, debug=debug)

