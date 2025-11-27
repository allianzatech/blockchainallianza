#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
WSGI Entry Point para Produção - Allianza Blockchain
Configurado para Hostinger e outros servidores de produção
"""

import os
import sys

# Adicionar diretório do projeto ao path
sys.path.insert(0, os.path.dirname(__file__))

# Carregar variáveis de ambiente de produção
from dotenv import load_dotenv

# Tentar carregar .env.production primeiro, depois .env
if os.path.exists('.env.production'):
    load_dotenv('.env.production')
elif os.path.exists('.env'):
    load_dotenv('.env')

# Importar app Flask e instâncias
try:
    from allianza_blockchain import app, blockchain, quantum_security, bridge
    
    # Configurar para produção
    app.config['ENV'] = os.getenv('FLASK_ENV', 'production')
    app.config['DEBUG'] = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    
    # Aplicação WSGI
    application = app
    
    print("✅ Allianza Blockchain WSGI carregado com sucesso!")
    print(f"   Ambiente: {app.config['ENV']}")
    print(f"   Debug: {app.config['DEBUG']}")
    
except Exception as e:
    error_message = str(e)
    print(f"❌ Erro ao carregar Allianza Blockchain: {error_message}")
    import traceback
    traceback.print_exc()
    
    # Criar app mínimo para evitar erro 500
    from flask import Flask
    application = Flask(__name__)
    
    @application.route('/')
    def error():
        return f"Erro ao inicializar: {error_message}", 500

if __name__ == "__main__":
    # Executar diretamente (para testes)
    port = int(os.getenv('PORT', 5000))
    host = os.getenv('HOST', '0.0.0.0')
    debug = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    
    print(f"🚀 Iniciando Allianza Blockchain em {host}:{port}")
    application.run(host=host, port=port, debug=debug)

