# test_performance.py - TESTE DE PERFORMANCE MÁSSICO
import requests
import threading
import time
import json
from datetime import datetime

BASE_URL = "http://localhost:5008"

class PerformanceTester:
    def __init__(self):
        self.results = {
            "wallets_created": 0,
            "transactions_sent": 0,
            "bridges_created": 0,
            "errors": 0,
            "start_time": None,
            "end_time": None
        }
        self.lock = threading.Lock()
    
    def create_wallet_batch(self, count=10):
        """Cria um lote de wallets"""
        wallets = []
        for i in range(count):
            try:
                response = requests.post(f"{BASE_URL}/uec/create_wallet", json={}, timeout=10)
                if response.status_code == 200:
                    wallet = response.json()
                    wallets.append(wallet)
                    with self.lock:
                        self.results["wallets_created"] += 1
                    print(f"👛 Wallet {i+1}/{count} criada")
                else:
                    with self.lock:
                        self.results["errors"] += 1
            except Exception as e:
                with self.lock:
                    self.results["errors"] += 1
                print(f"❌ Erro ao criar wallet: {e}")
        return wallets
    
    def stress_bridge_transfers(self, wallets, transfers_per_wallet=5):
        """Teste de estresse na bridge"""
        def make_transfer(wallet, transfer_id):
            try:
                # Alternar entre tokens e chains
                tokens_chains = [
                    ("ETHa", "ethereum"),
                    ("BTCa", "bitcoin"), 
                    ("USDa", "bsc"),
                    ("ETHa", "polygon")
                ]
                token, chain = tokens_chains[transfer_id % len(tokens_chains)]
                
                external_address = (
                    "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa" if chain == "bitcoin"
                    else "0x742d35Cc6634C0532925a3b844Bc454e4438f44e"
                )
                
                bridge_data = {
                    "token_id": token,
                    "amount": 0.01,
                    "external_address": external_address,
                    "target_chain": chain,
                    "private_key": wallet['private_key']
                }
                
                response = requests.post(f"{BASE_URL}/uec/bridge/transfer", 
                                       json=bridge_data, timeout=10)
                
                if response.status_code == 200:
                    with self.lock:
                        self.results["bridges_created"] += 1
                    print(f"🌉 Transferência {transfer_id} criada")
                else:
                    with self.lock:
                        self.results["errors"] += 1
                    
            except Exception as e:
                with self.lock:
                    self.results["errors"] += 1
                print(f"❌ Erro na transferência: {e}")
        
        threads = []
        for i, wallet in enumerate(wallets):
            for j in range(transfers_per_wallet):
                t = threading.Thread(target=make_transfer, args=(wallet, i*transfers_per_wallet + j))
                threads.append(t)
                t.start()
        
        for t in threads:
            t.join()
    
    def run_performance_test(self, wallet_count=20, transfers_per_wallet=3):
        """Executa teste de performance completo"""
        print("🚀 INICIANDO TESTE DE PERFORMANCE MÁSSICO")
        print("=" * 60)
        
        self.results["start_time"] = datetime.now()
        
        # 1. Criar wallets em lote
        print(f"1. 🎯 Criando {wallet_count} wallets...")
        wallets = self.create_wallet_batch(wallet_count)
        print(f"✅ {len(wallets)} wallets criadas com sucesso")
        
        # 2. Teste de estresse na bridge
        print(f"\n2. 🌉 Executando {transfers_per_wallet} transferências por wallet...")
        total_transfers = len(wallets) * transfers_per_wallet
        print(f"📊 Total de transferências: {total_transfers}")
        
        self.stress_bridge_transfers(wallets, transfers_per_wallet)
        
        # 3. Resultados
        self.results["end_time"] = datetime.now()
        duration = (self.results["end_time"] - self.results["start_time"]).total_seconds()
        
        print("\n" + "=" * 60)
        print("📊 RESULTADOS DO TESTE DE PERFORMANCE")
        print("=" * 60)
        print(f"⏱️  Duração: {duration:.2f} segundos")
        print(f"👛 Wallets criadas: {self.results['wallets_created']}")
        print(f"🌉 Bridges criadas: {self.results['bridges_created']}")
        print(f"❌ Erros: {self.results['errors']}")
        print(f"⚡ Performance: {self.results['bridges_created']/duration:.2f} transações/segundo")
        
        # 4. Status do sistema
        try:
            status = requests.get(f"{BASE_URL}/uec/system/status").json()
            network = requests.get(f"{BASE_URL}/network/status").json()
            
            print(f"\n📈 STATUS DO SISTEMA:")
            print(f"🔄 Bridges pendentes: {status['pending_transfers']}")
            print(f"✅ Bridges completadas: {status['completed_transfers']}") 
            print(f"👛 Wallets UEC totais: {status['total_wallets_uec']}")
            print(f"🧱 Blocos na rede: {network['total_blocks']}")
            print(f"💼 Wallets totais: {network['total_wallets']}")
            
        except Exception as e:
            print(f"❌ Erro ao obter status: {e}")
        
        return self.results

def main():
    tester = PerformanceTester()
    tester.run_performance_test(
        wallet_count=15,      # Número de wallets para criar
        transfers_per_wallet=4 # Transferências por wallet
    )

if __name__ == "__main__":
    main()