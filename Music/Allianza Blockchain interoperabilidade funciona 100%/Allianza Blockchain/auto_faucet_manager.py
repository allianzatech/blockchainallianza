#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🚰 GERENCIADOR AUTOMÁTICO DE FAUCET
Solicita fundos automaticamente a cada 12 horas para endereços configurados
"""

import os
import json
import time
import requests
import threading
from datetime import datetime, timedelta
from typing import Dict, List, Optional

# Tornar schedule opcional
try:
    import schedule
    SCHEDULE_AVAILABLE = True
except ImportError:
    SCHEDULE_AVAILABLE = False
    schedule = None
    print("⚠️  schedule não disponível - gerenciador automático de faucet desabilitado")

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

class AutoFaucetManager:
    """
    Gerenciador automático de faucets para testnet
    Verifica saldos e solicita fundos automaticamente a cada 12 horas
    """
    
    def __init__(self):
        self.addresses_config = self._load_addresses_config()
        self.last_request_file = "faucet_last_requests.json"
        self.min_balance_threshold = {
            "bitcoin": 0.0001,  # 0.0001 BTC mínimo
            "polygon": 0.01,    # 0.01 MATIC mínimo
            "ethereum": 0.001,  # 0.001 ETH mínimo
            "bsc": 0.01         # 0.01 BNB mínimo
        }
        self.faucet_apis = {
            "bitcoin": [
                {
                    "name": "Bitcoin Testnet Faucet (uo1.net)",
                    "url": "https://bitcoinfaucet.uo1.net/send",
                    "method": "POST",
                    "params": {"address": "{address}"},
                    "headers": {"Content-Type": "application/x-www-form-urlencoded"},
                    "check_balance": True
                },
                {
                    "name": "Bitcoin Testnet Faucet (alternativo)",
                    "url": "https://testnet-faucet.com/btc-testnet/",
                    "method": "POST",
                    "params": {"address": "{address}"},
                    "headers": {"Content-Type": "application/json"},
                    "check_balance": False
                }
            ],
            "polygon": [
                {
                    "name": "Polygon Faucet (Official - Amoy)",
                    "url": "https://faucet.polygon.technology/",
                    "method": "POST",
                    "params": {
                        "network": "amoy",  # Atualizado: usar Amoy, não Mumbai
                        "address": "{address}"
                    },
                    "headers": {"Content-Type": "application/json"},
                    "check_balance": True
                },
                {
                    "name": "Alchemy Polygon Faucet",
                    "url": "https://www.alchemy.com/faucets/polygon-amoy",
                    "method": "GET",
                    "params": {"address": "{address}"},
                    "headers": {"Content-Type": "application/json"},
                    "check_balance": False
                },
                {
                    "name": "QuickNode Polygon Faucet (Amoy)",
                    "url": "https://faucet.quicknode.com/polygon/amoy",
                    "method": "POST",
                    "params": {"address": "{address}"},
                    "headers": {"Content-Type": "application/json"},
                    "check_balance": False
                }
            ],
            "ethereum": [
                {
                    "name": "Sepolia Faucet (Official)",
                    "url": "https://faucet.sepolia.dev/",
                    "method": "POST",
                    "params": {"address": "{address}"},
                    "headers": {"Content-Type": "application/json"},
                    "check_balance": True
                },
                {
                    "name": "QuickNode Sepolia Faucet",
                    "url": "https://faucet.quicknode.com/ethereum/sepolia",
                    "method": "POST",
                    "params": {"address": "{address}"},
                    "headers": {"Content-Type": "application/json"},
                    "check_balance": False
                },
                {
                    "name": "Alchemy Sepolia Faucet",
                    "url": "https://sepoliafaucet.com/",
                    "method": "POST",
                    "params": {"address": "{address}"},
                    "headers": {"Content-Type": "application/json"},
                    "check_balance": False
                }
            ],
            "bsc": [
                {
                    "name": "BSC Testnet Faucet (Official)",
                    "url": "https://testnet.binance.org/faucet-smart",
                    "method": "POST",
                    "params": {"address": "{address}"},
                    "headers": {"Content-Type": "application/json"},
                    "check_balance": True
                },
                {
                    "name": "QuickNode BSC Faucet",
                    "url": "https://faucet.quicknode.com/binance/bnb-testnet",
                    "method": "POST",
                    "params": {"address": "{address}"},
                    "headers": {"Content-Type": "application/json"},
                    "check_balance": False
                }
            ]
        }
    
    def _load_addresses_config(self) -> Dict:
        """Carrega configuração de endereços do .env"""
        config = {}
        
        # Bitcoin
        btc_address = os.getenv('BITCOIN_TESTNET_ADDRESS') or os.getenv('BITCOIN_ADDRESS')
        if btc_address:
            config["bitcoin"] = {
                "address": btc_address,
                "enabled": True
            }
        
        # Ethereum
        eth_address = os.getenv('ETHEREUM_ADDRESS') or os.getenv('ETHEREUM_TESTNET_ADDRESS')
        # Se não tiver ETHEREUM_ADDRESS, tentar obter da conta Web3
        if not eth_address:
            try:
                from contracts.ethereum_bridge import RealEthereumBridge
                bridge = RealEthereumBridge()
                if bridge.account:
                    eth_address = bridge.account.address
            except:
                pass
        
        if eth_address:
            config["ethereum"] = {
                "address": eth_address,
                "enabled": True
            }
        
        # Polygon (EVM-compatible, pode usar mesmo endereço Ethereum)
        polygon_address = os.getenv('POLYGON_ADDRESS') or os.getenv('POLYGON_TESTNET_ADDRESS')
        # Se não tiver POLYGON_ADDRESS configurado, usar o mesmo endereço Ethereum
        if not polygon_address and eth_address:
            polygon_address = eth_address
        
        if polygon_address:
            config["polygon"] = {
                "address": polygon_address,
                "enabled": True
            }
        
        # BSC (EVM-compatible, pode usar mesmo endereço Ethereum)
        bsc_address = os.getenv('BSC_ADDRESS') or os.getenv('BSC_TESTNET_ADDRESS')
        # Se não tiver BSC_ADDRESS configurado, usar o mesmo endereço Ethereum
        if not bsc_address and eth_address:
            bsc_address = eth_address
        
        if bsc_address:
            config["bsc"] = {
                "address": bsc_address,
                "enabled": True
            }
        
        return config
    
    def _load_last_requests(self) -> Dict:
        """Carrega histórico de últimas solicitações"""
        if os.path.exists(self.last_request_file):
            try:
                with open(self.last_request_file, 'r', encoding='utf-8') as f:
                    data = f.read().strip()
                    # Se arquivo está vazio, retornar dict vazio
                    if not data or data == "":
                        return {}
                    return json.loads(data)
            except (json.JSONDecodeError, ValueError, IOError):
                # Se falhar, retornar dict vazio
                return {}
        return {}
    
    def _save_last_request(self, chain: str, address: str, success: bool):
        """Salva última solicitação de faucet"""
        last_requests = self._load_last_requests()
        last_requests[f"{chain}:{address}"] = {
            "timestamp": datetime.now().isoformat(),
            "success": success,
            "chain": chain,
            "address": address
        }
        try:
            with open(self.last_request_file, 'w', encoding='utf-8') as f:
                json.dump(last_requests, f, indent=2, ensure_ascii=False)
        except (IOError, OSError) as e:
            print(f"⚠️  Erro ao salvar last_requests: {e}")
    
    def _can_request_faucet(self, chain: str, address: str) -> bool:
        """Verifica se pode solicitar faucet (respeitando intervalo de 12 horas)"""
        last_requests = self._load_last_requests()
        key = f"{chain}:{address}"
        
        if key not in last_requests:
            return True
        
        last_request_time = datetime.fromisoformat(last_requests[key]["timestamp"])
        time_since_last = datetime.now() - last_request_time
        
        # Verificar se passaram pelo menos 12 horas
        return time_since_last >= timedelta(hours=12)
    
    def get_balance(self, chain: str, address: str) -> Optional[float]:
        """Obtém saldo do endereço"""
        try:
            if chain == "bitcoin":
                # Usar BlockCypher ou Blockstream
                url = f"https://blockstream.info/testnet/api/address/{address}"
                response = requests.get(url, timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    # Blockstream retorna chain_stats com funded_txo_sum
                    funded = data.get('chain_stats', {}).get('funded_txo_sum', 0)
                    spent = data.get('chain_stats', {}).get('spent_txo_sum', 0)
                    balance_satoshis = funded - spent
                    return balance_satoshis / 100000000  # Converter para BTC
            
            elif chain in ["polygon", "ethereum", "bsc"]:
                # Usar APIs de explorer
                if chain == "polygon":
                    # Usar Amoy testnet (novo testnet do Polygon)
                    url = f"https://api-amoy.polygonscan.com/api?module=account&action=balance&address={address}&tag=latest&apikey=YourApiKeyToken"
                elif chain == "ethereum":
                    url = f"https://api-sepolia.etherscan.io/api?module=account&action=balance&address={address}&tag=latest&apikey=YourApiKeyToken"
                elif chain == "bsc":
                    url = f"https://api-testnet.bscscan.com/api?module=account&action=balance&address={address}&tag=latest&apikey=YourApiKeyToken"
                
                response = requests.get(url, timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    if data.get('status') == '1':
                        balance_wei = int(data.get('result', 0))
                        # Converter para unidades nativas
                        if chain == "polygon":
                            return balance_wei / 1e18  # MATIC
                        elif chain == "ethereum":
                            return balance_wei / 1e18  # ETH
                        elif chain == "bsc":
                            return balance_wei / 1e18  # BNB
        
        except Exception as e:
            print(f"⚠️  Erro ao obter saldo de {chain}: {e}")
        
        return None
    
    def request_faucet(self, chain: str, address: str) -> Dict:
        """Solicita fundos do faucet"""
        if chain not in self.faucet_apis:
            return {
                "success": False,
                "error": f"Faucet não configurado para {chain}"
            }
        
        faucets = self.faucet_apis[chain]
        
        for faucet in faucets:
            try:
                url = faucet["url"]
                method = faucet.get("method", "POST")
                params = faucet.get("params", {})
                headers = faucet.get("headers", {})
                
                # Substituir {address} nos parâmetros
                formatted_params = {}
                for key, value in params.items():
                    if isinstance(value, str):
                        formatted_params[key] = value.format(address=address)
                    else:
                        formatted_params[key] = value
                
                print(f"🚰 Tentando faucet: {faucet['name']} para {chain}")
                
                if method.upper() == "POST":
                    if headers.get("Content-Type") == "application/json":
                        response = requests.post(url, json=formatted_params, headers=headers, timeout=30)
                    else:
                        response = requests.post(url, data=formatted_params, headers=headers, timeout=30)
                else:
                    response = requests.get(url, params=formatted_params, headers=headers, timeout=30)
                
                if response.status_code in [200, 201]:
                    print(f"✅ Solicitação enviada para {faucet['name']}")
                    return {
                        "success": True,
                        "faucet": faucet['name'],
                        "message": f"Solicitação enviada com sucesso para {faucet['name']}"
                    }
                elif response.status_code in [403, 429]:
                    # Rate limit ou bloqueio - tentar próximo faucet
                    print(f"⚠️  {faucet['name']} retornou status {response.status_code} (rate limit/bloqueio) - tentando próximo...")
                    continue
                elif response.status_code in [500, 502, 503]:
                    # Erro do servidor - tentar próximo faucet
                    print(f"⚠️  {faucet['name']} retornou status {response.status_code} (erro do servidor) - tentando próximo...")
                    continue
                else:
                    print(f"⚠️  {faucet['name']} retornou status {response.status_code} - tentando próximo...")
            
            except Exception as e:
                print(f"⚠️  Erro ao solicitar de {faucet['name']}: {e}")
                continue
        
        return {
            "success": False,
            "error": "Todos os faucets falharam"
        }
    
    def check_and_request(self, chain: str, address: str) -> Dict:
        """Verifica saldo e solicita faucet se necessário"""
        print(f"\n🔍 Verificando {chain.upper()} - {address}")
        
        # Verificar se pode solicitar (respeitando intervalo de 12h)
        if not self._can_request_faucet(chain, address):
            last_requests = self._load_last_requests()
            key = f"{chain}:{address}"
            last_time = datetime.fromisoformat(last_requests[key]["timestamp"])
            next_time = last_time + timedelta(hours=12)
            time_remaining = next_time - datetime.now()
            
            print(f"⏳ Próxima solicitação disponível em: {time_remaining}")
            return {
                "success": False,
                "skipped": True,
                "reason": f"Intervalo de 12h não passou. Próxima solicitação em {time_remaining}",
                "next_request": next_time.isoformat()
            }
        
        # Verificar saldo
        balance = self.get_balance(chain, address)
        
        if balance is None:
            print(f"⚠️  Não foi possível verificar saldo. Tentando solicitar faucet mesmo assim...")
            result = self.request_faucet(chain, address)
            self._save_last_request(chain, address, result.get("success", False))
            return result
        
        min_balance = self.min_balance_threshold.get(chain, 0.001)
        
        print(f"💰 Saldo atual: {balance} {chain.upper()}")
        print(f"📊 Mínimo necessário: {min_balance} {chain.upper()}")
        
        if balance < min_balance:
            print(f"🚰 Saldo baixo! Solicitando faucet...")
            result = self.request_faucet(chain, address)
            self._save_last_request(chain, address, result.get("success", False))
            return result
        else:
            print(f"✅ Saldo suficiente. Não é necessário solicitar faucet.")
            return {
                "success": True,
                "skipped": True,
                "reason": f"Saldo suficiente: {balance} {chain.upper()}",
                "balance": balance
            }
    
    def check_all_addresses(self):
        """Verifica e solicita faucet para todos os endereços configurados"""
        print(f"\n{'='*60}")
        print(f"🚰 VERIFICAÇÃO AUTOMÁTICA DE FAUCETS - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*60}")
        
        results = {}
        
        for chain, config in self.addresses_config.items():
            if not config.get("enabled", True):
                continue
            
            address = config["address"]
            result = self.check_and_request(chain, address)
            results[chain] = result
        
        print(f"\n{'='*60}")
        print(f"✅ Verificação concluída!")
        print(f"{'='*60}\n")
        
        return results
    
    def start_scheduler(self, interval_hours: int = 12):
        """Inicia agendador para verificar a cada X horas"""
        # Verificar se schedule está disponível - tentar importar diretamente
        try:
            import schedule as schedule_module
        except ImportError:
            print("⚠️  schedule não disponível - gerenciador automático não pode ser iniciado")
            print("   Para habilitar, instale: pip install schedule")
            return None
        
        print(f"🚀 Iniciando gerenciador automático de faucets...")
        print(f"   Intervalo: {interval_hours} horas")
        print(f"   Endereços configurados: {len(self.addresses_config)}")
        
        # Executar imediatamente
        self.check_all_addresses()
        
        # Agendar execuções periódicas
        schedule_module.every(interval_hours).hours.do(self.check_all_addresses)
        
        print(f"✅ Agendador iniciado! Próxima verificação em {interval_hours} horas")
        
        # Executar em thread separada
        def run_scheduler():
            while True:
                schedule_module.run_pending()
                time.sleep(60)  # Verificar a cada minuto
        
        scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
        scheduler_thread.start()
        
        return scheduler_thread

def main():
    """Função principal para executar manualmente"""
    manager = AutoFaucetManager()
    manager.check_all_addresses()

if __name__ == "__main__":
    main()

