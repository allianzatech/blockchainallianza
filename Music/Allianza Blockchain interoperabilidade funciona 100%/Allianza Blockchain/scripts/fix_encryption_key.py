#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para corrigir ENCRYPTION_KEY
"""

import os
from pathlib import Path
from cryptography.fernet import Fernet

ENCRYPTION_KEY_FILE = "secrets/encryption_key.key"

# Garantir que o diretório existe
os.makedirs(os.path.dirname(ENCRYPTION_KEY_FILE), exist_ok=True)

# Gerar nova chave válida
new_key = Fernet.generate_key()

# Salvar
with open(ENCRYPTION_KEY_FILE, "wb") as f:
    f.write(new_key)

print(f"✅ ENCRYPTION_KEY gerada e salva em {ENCRYPTION_KEY_FILE}")
print(f"   Tamanho: {len(new_key)} bytes")
print(f"   Base64: {new_key.decode()}")

