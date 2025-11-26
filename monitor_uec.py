# monitor_uec.py
import requests
import time
import os

BASE_URL = "http://localhost:5008"

def monitor_uec():
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("📡 MONITOR UEC - TEMPO REAL")
        print("=" * 40)
        
        try:
            # Status UEC
            uec_status = requests.get(f"{BASE_URL}/uec/system/status").json()
            print(f"🌌 UEC Version: {uec_status['uec_version']}")
            print(f"🔄 Pendentes: {uec_status['pending_transfers']}")
            print(f"✅ Completadas: {uec_status['completed_transfers']}")
            print(f"👛 Wallets: {uec_status['total_wallets_uec']}")
            
            # Status Rede
            network_status = requests.get(f"{BASE_URL}/network/status").json()
            print(f"\n📊 REDE ALLIANZA")
            print(f"🔢 Shards: {network_status['shards']}")
            print(f"🧱 Blocos: {network_status['total_blocks']}")
            print(f"💼 Wallets: {network_status['total_wallets']}")
            print(f"🔗 UEC Ativa: {network_status['uec_enabled']}")
            
        except Exception as e:
            print(f"❌ Erro: {e}")
        
        print(f"\n⏰ Última atualização: {time.strftime('%H:%M:%S')}")
        print("Press CTRL+C para parar...")
        time.sleep(5)

if __name__ == "__main__":
    monitor_uec()