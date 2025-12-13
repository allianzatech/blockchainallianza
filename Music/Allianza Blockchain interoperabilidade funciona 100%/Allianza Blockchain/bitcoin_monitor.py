# bitcoin_monitor.py - SISTEMA DE DETECÇÃO AUTOMÁTICA BTC
import requests
import time
import json
import os
import secrets
from datetime import datetime

class BitcoinTransactionMonitor:
    def __init__(self):
        self.api_key = os.getenv('BLOCKCYPHER_API_TOKEN', '17766314e49c439e85cec883969614ac')
        self.base_url = "https://api.blockcypher.com/v1/btc/test3"
        self.pending_swaps = {}
        self.eth_bridge = None
        
        print("🔍 BITCOIN TRANSACTION MONITOR: Inicializado")
        
    def setup_ethereum_bridge(self):
        """Configurar ponte Ethereum para quando BTC for detectado"""
        try:
            from contracts.ethereum_bridge import RealEthereumBridge
            self.eth_bridge = RealEthereumBridge()
            if self.eth_bridge.eth_w3 and self.eth_bridge.account:
                print("✅ Ponte Ethereum configurada para swaps BTC→ETH")
            else:
                print("⚠️  Ponte Ethereum em modo simulação (variáveis não configuradas)")
        except (ImportError, Exception) as e:
            print(f"⚠️  Ponte Ethereum não disponível - usando modo simulação: {e}")
            self.eth_bridge = None
    
    def generate_btc_address(self):
        """Gerar endereço Bitcoin único para depósito"""
        try:
            # Usar BlockCypher para gerar endereço
            url = f"{self.base_url}/addrs?token={self.api_key}"
            response = requests.post(url)
            
            if response.status_code == 201:
                data = response.json()
                return {
                    "address": data['address'],
                    "private": data['private'],
                    "public": data['public'],
                    "wif": data['wif']
                }
            else:
                # Fallback: gerar endereço deterministicamente
                return self.generate_deterministic_address()
                
        except Exception as e:
            print(f"❌ Erro ao gerar endereço BTC: {e}")
            return self.generate_deterministic_address()
    
    def generate_deterministic_address(self):
        """Gerar endereço deterministicamente como fallback"""
        import hashlib
        from base58_utils import generate_allianza_address
        
        timestamp = str(int(time.time()))
        seed = f"btc_swap_{timestamp}_{secrets.token_hex(8)}"
        address_hash = hashlib.sha256(seed.encode()).digest()
        
        return {
            "address": generate_allianza_address(address_hash),
            "private": "simulated_private_key",
            "public": "simulated_public_key", 
            "wif": "simulated_wif"
        }
    
    def check_btc_balance(self, btc_address):
        """Verificar saldo de um endereço Bitcoin"""
        try:
            url = f"{self.base_url}/addrs/{btc_address}/balance"
            response = requests.get(url)
            
            if response.status_code == 200:
                data = response.json()
                balance_satoshis = data['balance']
                balance_btc = balance_satoshis / 100000000  # Converter para BTC
                
                return {
                    "success": True,
                    "address": btc_address,
                    "balance_btc": balance_btc,
                    "balance_satoshis": balance_satoshis,
                    "total_received": data['total_received'] / 100000000,
                    "total_sent": data['total_sent'] / 100000000,
                    "unconfirmed_balance": data['unconfirmed_balance'] / 100000000
                }
            else:
                return {
                    "success": False,
                    "error": f"Erro API: {response.status_code}",
                    "balance_btc": 0
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "balance_btc": 0
            }
    
    def create_btc_to_eth_swap(self, btc_amount, eth_recipient, user_data=None):
        """Criar swap Bitcoin → Ethereum"""
        try:
            # 1. Gerar endereço Bitcoin único
            btc_address_data = self.generate_btc_address()
            btc_deposit_address = btc_address_data['address']
            
            # 2. Criar ID único para o swap
            swap_id = f"btc_eth_swap_{int(time.time())}_{secrets.token_hex(4)}"
            
            # 3. Registrar swap pendente
            self.pending_swaps[swap_id] = {
                "btc_deposit_address": btc_deposit_address,
                "required_btc": btc_amount,
                "eth_recipient": eth_recipient,
                "created_at": datetime.now().isoformat(),
                "status": "waiting_for_btc",
                "user_data": user_data or {},
                "btc_address_data": btc_address_data
            }
            
            # 4. Iniciar monitoramento em background
            self.start_monitoring_swap(swap_id)
            
            return {
                "success": True,
                "swap_id": swap_id,
                "bitcoin_deposit_address": btc_deposit_address,
                "required_btc": btc_amount,
                "eth_recipient": eth_recipient,
                "estimated_btca_tokens": btc_amount * 45000,  # 1 BTC = ~$45k em BTCa
                "instructions": {
                    "1": f"💰 Envie exatamente {btc_amount} BTC para:",
                    "2": f"📍 {btc_deposit_address}",
                    "3": "⏰ O sistema detectará automaticamente em ~30 segundos",
                    "4": f"🎁 Você receberá {btc_amount * 45000:.2f} BTCa tokens em:",
                    "5": f"📬 {eth_recipient}",
                    "6": "🔮 BTCa é Bitcoin metaprogramável na Ethereum!"
                },
                "explorers": {
                    "bitcoin": f"https://live.blockcypher.com/btc-testnet/address/{btc_deposit_address}/",
                    "ethereum": f"https://sepolia.etherscan.io/address/{eth_recipient}"
                },
                "note": "Use Bitcoin TESTNET para demonstrações"
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def start_monitoring_swap(self, swap_id):
        """Iniciar monitoramento de um swap em background"""
        import threading
        
        def monitor_swap():
            swap_data = self.pending_swaps[swap_id]
            btc_address = swap_data['btc_deposit_address']
            required_amount = swap_data['required_btc']
            
            print(f"🔍 Monitorando BTC address: {btc_address} para {required_amount} BTC")
            
            max_attempts = 60  # 30 minutos (30 segundos × 60)
            attempts = 0
            
            while attempts < max_attempts and self.pending_swaps.get(swap_id):
                try:
                    # Verificar saldo
                    balance_info = self.check_btc_balance(btc_address)
                    
                    if balance_info['success']:
                        current_balance = balance_info['balance_btc']
                        
                        print(f"💰 Saldo atual: {current_balance} BTC | Necessário: {required_amount} BTC")
                        
                        # Se saldo suficiente foi recebido
                        if current_balance >= required_amount:
                            print(f"🎉 BTC detectado! Executando swap {swap_id}")
                            
                            # Executar swap
                            self.execute_btc_to_btca_swap(swap_id, swap_data)
                            break
                    
                    # Aguardar antes da próxima verificação
                    time.sleep(30)
                    attempts += 1
                    
                except Exception as e:
                    print(f"❌ Erro no monitoramento: {e}")
                    time.sleep(30)
                    attempts += 1
            
            # Se acabou o tempo
            if attempts >= max_attempts:
                print(f"⏰ Timeout no swap {swap_id}")
                self.pending_swaps[swap_id]['status'] = 'timeout'
        
        # Iniciar thread de monitoramento
        thread = threading.Thread(target=monitor_swap)
        thread.daemon = True
        thread.start()
    
    def execute_btc_to_btca_swap(self, swap_id, swap_data):
        """Executar swap BTC → BTCa (Bitcoin metaprogramável)"""
        try:
            btc_amount = swap_data['required_btc']
            eth_recipient = swap_data['eth_recipient']
            
            print(f"🚀 Executando swap: {btc_amount} BTC → BTCa para {eth_recipient}")
            
            # 1. Calcular quantidade de BTCa (1 BTC = 45,000 BTCa para demo)
            btca_amount = int(btc_amount * 45000 * 10**8)  # 8 decimais como BTC
            
            # 2. Se temos ponte Ethereum real, usar
            if self.eth_bridge:
                # Usar sistema de metaprogramação existente
                from contracts.real_metaprogrammable import real_meta_system
                
                # Criar ou usar token BTCa existente
                btca_token_id = self.get_or_create_btca_token()
                
                # Transferir BTCa para o usuário
                result = real_meta_system.metaprogrammable_transfer(
                    btca_token_id,
                    eth_recipient,
                    btca_amount,
                    "ethereum"  # Já está na Ethereum
                )
                
                if result['success']:
                    self.pending_swaps[swap_id].update({
                        'status': 'completed',
                        'completion_time': datetime.now().isoformat(),
                        'btca_amount': btca_amount,
                        'transaction_hash': result['tx_hash'],
                        'explorer_url': result['explorer']
                    })
                    
                    print(f"✅ Swap completado! TX: {result['tx_hash']}")
                    
                    # Emitir evento WebSocket se disponível
                    self.emit_swap_completed(swap_id, self.pending_swaps[swap_id])
                    
                else:
                    raise Exception(f"Erro na transferência: {result.get('error')}")
                    
            else:
                # Modo simulação
                self.pending_swaps[swap_id].update({
                    'status': 'completed_simulation',
                    'completion_time': datetime.now().isoformat(),
                    'btca_amount': btca_amount,
                    'transaction_hash': f"0x_simulated_{secrets.token_hex(20)}",
                    'explorer_url': "https://sepolia.etherscan.io/tx/0x_simulated",
                    'note': 'Modo simulação - Sem ponte Ethereum real'
                })
                
                print("✅ Swap simulado completado!")
                self.emit_swap_completed(swap_id, self.pending_swaps[swap_id])
            
        except Exception as e:
            print(f"❌ Erro no swap: {e}")
            self.pending_swaps[swap_id]['status'] = 'failed'
            self.pending_swaps[swap_id]['error'] = str(e)
    
    def get_or_create_btca_token(self):
        """Obter ou criar token BTCa metaprogramável"""
        try:
            from contracts.real_metaprogrammable import real_meta_system
            
            # Verificar se BTCa já existe
            tokens = real_meta_system.list_metaprogrammable_tokens()
            for token_id, token_data in tokens.get('tokens', {}).items():
                if token_data.get('symbol') == 'BTCa':
                    return token_id
            
            # Se não existe, criar
            result = real_meta_system.deploy_metaprogrammable_token(
                "Bitcoin Allianza",
                "BTCa",
                21000000 * 10**8  # 21M BTC com 8 decimais
            )
            
            if result['success']:
                return result['token_id']
            else:
                raise Exception(f"Erro ao criar BTCa: {result.get('error')}")
                
        except Exception as e:
            print(f"❌ Erro com BTCa: {e}")
            return "btca_fallback_token"
    
    def emit_swap_completed(self, swap_id, swap_data):
        """Emitir evento de swap completado"""
        try:
            from flask_socketio import emit
            emit('btc_swap_completed', {
                'swap_id': swap_id,
                'status': swap_data['status'],
                'btc_amount': swap_data['required_btc'],
                'btca_amount': swap_data.get('btca_amount'),
                'eth_recipient': swap_data['eth_recipient'],
                'transaction_hash': swap_data.get('transaction_hash'),
                'explorer_url': swap_data.get('explorer_url'),
                'completion_time': swap_data.get('completion_time')
            })
        except:
            pass  # WebSocket não disponível
    
    def get_swap_status(self, swap_id):
        """Obter status de um swap"""
        swap_data = self.pending_swaps.get(swap_id)
        if not swap_data:
            return {"success": False, "error": "Swap não encontrado"}
        
        # Verificar saldo atual se ainda está esperando
        if swap_data['status'] == 'waiting_for_btc':
            balance_info = self.check_btc_balance(swap_data['btc_deposit_address'])
            swap_data['current_balance'] = balance_info.get('balance_btc', 0)
        
        return {
            "success": True,
            "swap_id": swap_id,
            "status": swap_data['status'],
            "bitcoin_deposit_address": swap_data['btc_deposit_address'],
            "required_btc": swap_data['required_btc'],
            "current_balance": swap_data.get('current_balance', 0),
            "eth_recipient": swap_data['eth_recipient'],
            "created_at": swap_data['created_at'],
            "completion_time": swap_data.get('completion_time'),
            "transaction_hash": swap_data.get('transaction_hash'),
            "explorer_url": swap_data.get('explorer_url'),
            "error": swap_data.get('error')
        }
    
    def list_active_swaps(self):
        """Listar todos os swaps ativos"""
        return {
            "success": True,
            "total_swaps": len(self.pending_swaps),
            "active_swaps": {
                swap_id: {
                    "status": data['status'],
                    "btc_address": data['btc_deposit_address'],
                    "required_btc": data['required_btc'],
                    "eth_recipient": data['eth_recipient'],
                    "created_at": data['created_at']
                }
                for swap_id, data in self.pending_swaps.items()
            }
        }

# Instância global
btc_monitor = BitcoinTransactionMonitor()
btc_monitor.setup_ethereum_bridge()

def start_btc_monitoring_service():
    """Iniciar serviço de monitoramento BTC"""
    print("🔍 SERVIÇO DE MONITORAMENTO BTC INICIADO")
    print("💰 Pronto para swaps Bitcoin → Ethereum!")
    return btc_monitor

# Iniciar automaticamente
start_btc_monitoring_service()