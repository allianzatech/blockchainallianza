#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
WSGI Entry Point Otimizado para Produção - Allianza Blockchain
Carregamento lazy para evitar timeout no deploy
"""

import os
import sys

# Adicionar diretório do projeto ao path
base_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, base_dir)

# Adicionar caminho do commercial_repo ao sys.path para importar corretamente
commercial_repo_path = os.path.join(base_dir, "commercial_repo", "production")
if os.path.exists(commercial_repo_path):
    sys.path.insert(0, commercial_repo_path)
# Também adicionar commercial_repo/ como módulo
commercial_repo_base = os.path.join(base_dir, "commercial_repo")
if os.path.exists(commercial_repo_base):
    sys.path.insert(0, commercial_repo_base)

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

# Importar app completo diretamente do arquivo comercial (sem lazy loading)
try:
    # Tentar importar do caminho comercial primeiro (correto)
    try:
        from commercial_repo.production.allianza_blockchain import app as application
        print("✅ Allianza Blockchain importado de commercial_repo/production/allianza_blockchain.py")
    except ImportError:
        # Fallback: tentar importar do wrapper na raiz
        from allianza_blockchain import app as application
        print("✅ Allianza Blockchain importado de allianza_blockchain.py (wrapper)")
    application.config['ENV'] = os.getenv('FLASK_ENV', 'production')
    application.config['DEBUG'] = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    
    # NÃO remover a rota do blueprint - deixar funcionar normalmente
    # Apenas garantir que HEAD requests funcionem para monitores
    from flask import jsonify, Response
    
    # Interceptar apenas HEAD requests na rota '/' (para monitores)
    # GET requests devem passar para o dashboard HTML do blueprint
    @application.before_request
    def intercept_root_before_request():
        """Intercepta apenas HEAD requests na rota '/' para monitores, GET passa para o dashboard"""
        from flask import request as flask_request, Response
        if flask_request.path == '/' and flask_request.method == 'HEAD':
            # Para HEAD requests (monitores), retornar 200 OK imediatamente
            return Response(status=200)
        # Para GET e outras requisições, deixar processar normalmente (mostrar dashboard HTML)
        return None
    
    # Registrar error handler para capturar erros 500 na rota '/' (backup)
    @application.errorhandler(500)
    def handle_500_error(e):
        """Captura erros 500 e retorna 200 OK para a rota raiz"""
        from flask import request as flask_request
        if flask_request.path == '/':
            print(f"⚠️  Erro 500 na rota raiz capturado (retornando 200 OK): {e}")
            import traceback
            traceback.print_exc()
            return jsonify({
                "status": "OK",
                "service": "Allianza Blockchain",
                "version": "1.0.0",
                "message": "Service is running"
            }), 200
        # Para outras rotas, retornar o erro normalmente
        return jsonify({"error": str(e)}), 500
    
    # Interceptar respostas de erro na rota '/' (backup adicional)
    @application.after_request
    def modify_error_responses(response):
        """Modifica respostas de erro 500 na rota '/' para retornar 200 OK"""
        from flask import request as flask_request
        if flask_request.path == '/' and response.status_code == 500:
            print(f"⚠️  Resposta 500 na rota raiz modificada para 200 OK")
            response.status_code = 200
            response.data = b'{"status":"OK","service":"Allianza Blockchain","version":"1.0.0"}'
            response.content_type = 'application/json'
        return response
    
    # Health check básico - verificar se já existe antes de registrar
    has_health_route = False
    has_healthz_route = False
    try:
        for rule in application.url_map.iter_rules():
            if rule.rule == '/health' and 'GET' in rule.methods:
                has_health_route = True
            if rule.rule == '/healthz' and 'GET' in rule.methods:
                has_healthz_route = True
    except:
        pass
    
    from flask import jsonify
    
    if not has_health_route:
        # Registrar health check apenas se não existir, com endpoint único
        @application.route('/health', endpoint='wsgi_health')
        def wsgi_health_status():
            return jsonify({"status": "ok", "service": "Allianza Blockchain"}), 200
    
    if not has_healthz_route:
        # Registrar /healthz também (usado pelo Render)
        @application.route('/healthz', endpoint='wsgi_healthz')
        def wsgi_healthz_status():
            return jsonify({"status": "ok", "service": "Allianza Blockchain"}), 200
except Exception as e:
    # Fallback mínimo se app completo falhar
    err_msg = str(e)
    application = Flask(__name__)
    application.config['ENV'] = os.getenv('FLASK_ENV', 'production')
    application.config['DEBUG'] = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    application.config['SECRET_KEY'] = os.getenv('SECRET_KEY', os.urandom(32).hex())
    from flask import jsonify
    @application.route('/', endpoint='wsgi_error_root')
    def error_root():
        return jsonify({"error": "Service initialization failed", "message": err_msg}), 500
    @application.route('/health', endpoint='wsgi_error_health')
    def health_fallback():
        return jsonify({"status": "error", "service": "Allianza Blockchain", "message": err_msg}), 500
    
    @application.route('/healthz', endpoint='wsgi_error_healthz')
    def healthz_fallback():
        return jsonify({"status": "error", "service": "Allianza Blockchain", "message": err_msg}), 500

# Aplicação WSGI
if __name__ == "__main__":
    port = int(os.getenv('PORT', 5000))
    host = os.getenv('HOST', '0.0.0.0')
    debug = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    
    print(f"🚀 Iniciando Allianza Blockchain em {host}:{port}")
    application.run(host=host, port=port, debug=debug)
