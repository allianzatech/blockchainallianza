#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script auxiliar para criar start_server.sh
Evita problemas com caracteres especiais no batch
"""

import os

start_server_content = """#!/bin/bash
cd "$(dirname "$0")"
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi
source venv/bin/activate
pip install -r requirements.txt
pip install gunicorn gevent
gunicorn -w 4 -b 127.0.0.1:5000 --timeout 120 wsgi:application
"""

deploy_dir = "deploy"
if os.path.exists(deploy_dir):
    start_server_path = os.path.join(deploy_dir, "start_server.sh")
    with open(start_server_path, "w", encoding="utf-8") as f:
        f.write(start_server_content)
    print(f"✅ start_server.sh criado em {start_server_path}")
else:
    print(f"❌ Diretório {deploy_dir} não existe")

