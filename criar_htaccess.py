#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script auxiliar para criar .htaccess
Evita problemas com caracteres especiais no batch
"""

import os

htaccess_content = """RewriteEngine On
RewriteCond %{REQUEST_FILENAME} !-f
RewriteCond %{REQUEST_FILENAME} !-d
RewriteRule ^(.*)$ wsgi.py/$1 [QSA,L]
"""

deploy_dir = "deploy"
if os.path.exists(deploy_dir):
    htaccess_path = os.path.join(deploy_dir, ".htaccess")
    with open(htaccess_path, "w", encoding="utf-8") as f:
        f.write(htaccess_content)
    print(f"✅ .htaccess criado em {htaccess_path}")
else:
    print(f"❌ Diretório {deploy_dir} não existe")

