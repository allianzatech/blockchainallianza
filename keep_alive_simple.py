#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Keep-Alive Simples - Versão Minimalista
Para rodar em qualquer lugar (local, servidor, GitHub Actions, etc.)
"""

import requests
import time
from datetime import datetime

TESTNET_URL = "https://testnet.allianza.tech"
HEALTH_ENDPOINT = f"{TESTNET_URL}/health"
INTERVAL_SECONDS = 14 * 60  # 14 minutos

def ping():
    try:
        response = requests.get(HEALTH_ENDPOINT, timeout=10)
        status = "✅" if response.status_code == 200 else "⚠️"
        print(f"{status} [{datetime.now().strftime('%H:%M:%S')}] Ping enviado - Status: {response.status_code}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ [{datetime.now().strftime('%H:%M:%S')}] Erro: {e}")
        return False

if __name__ == "__main__":
    print("🔄 Keep-Alive iniciado - Ping a cada 14 minutos")
    while True:
        ping()
        time.sleep(INTERVAL_SECONDS)

