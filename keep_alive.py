#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Keep-Alive Service para Allianza Testnet
Faz ping a cada 14 minutos para evitar sleep mode do Render
"""

import requests
import time
import os
from datetime import datetime
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# URL da testnet
TESTNET_URL = os.getenv('TESTNET_URL', 'https://testnet.allianza.tech')
HEALTH_ENDPOINT = f"{TESTNET_URL}/health"
INTERVAL_MINUTES = 14  # Ping a cada 14 minutos (antes dos 15min de sleep)
INTERVAL_SECONDS = INTERVAL_MINUTES * 60

def ping_testnet():
    """Faz ping no health check da testnet"""
    try:
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 🔄 Enviando ping...")
        response = requests.get(HEALTH_ENDPOINT, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Ping bem-sucedido! Status: {data.get('status', 'unknown')}")
            return True
        else:
            print(f"⚠️  Ping retornou status {response.status_code}")
            return False
            
    except requests.exceptions.Timeout:
        print(f"⏱️  Timeout ao fazer ping (serviço pode estar em sleep mode)")
        return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Erro ao fazer ping: {e}")
        return False

def main():
    """Loop principal do keep-alive"""
    print("=" * 60)
    print("🔄 Keep-Alive Service para Allianza Testnet")
    print("=" * 60)
    print(f"🌐 URL: {TESTNET_URL}")
    print(f"⏰ Intervalo: {INTERVAL_MINUTES} minutos")
    print(f"💚 Endpoint: {HEALTH_ENDPOINT}")
    print("=" * 60)
    print("🚀 Iniciando serviço...")
    print("💡 Pressione Ctrl+C para parar\n")
    
    ping_count = 0
    success_count = 0
    
    try:
        while True:
            # Fazer ping
            if ping_testnet():
                success_count += 1
            ping_count += 1
            
            # Estatísticas
            success_rate = (success_count / ping_count * 100) if ping_count > 0 else 0
            print(f"📊 Estatísticas: {success_count}/{ping_count} pings bem-sucedidos ({success_rate:.1f}%)")
            
            # Aguardar próximo ping
            print(f"⏳ Próximo ping em {INTERVAL_MINUTES} minutos...\n")
            time.sleep(INTERVAL_SECONDS)
            
    except KeyboardInterrupt:
        print("\n\n" + "=" * 60)
        print("🛑 Keep-Alive Service interrompido pelo usuário")
        print("=" * 60)
        print(f"📊 Estatísticas finais:")
        print(f"   Total de pings: {ping_count}")
        print(f"   Pings bem-sucedidos: {success_count}")
        if ping_count > 0:
            print(f"   Taxa de sucesso: {success_count/ping_count*100:.1f}%")
        print("=" * 60)

if __name__ == "__main__":
    main()

