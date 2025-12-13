# blockchain_connector.py - CONEXÃO REAL COM SUAS APIS
import os
from web3 import Web3
import requests
import json
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

class RealBlockchainConnector:
    def __init__(self, mode="testnet"):
        self.mode = mode
        self.setup_providers()
        
    def setup_providers(self):
        """Configura providers com SUAS chaves"""
        
        # SUAS CHAVES INFURA
        infura_project_id = os.getenv('INFURA_PROJECT_ID', '4622f8123b1a4cf7a3e30098d9120d7f')
        infura_secret = os.getenv('INFURA_PROJECT_SECRET', '17766314e49c439e85cec883969614ac')
        
        # SUA CHAVE BLOCKCYPHER
        self.blockcypher_token = os.getenv('BLOCKCYPHER_API_TOKEN', '17766314e49c439e85cec883969614ac')
        
        if self.mode == "mainnet":
            # MAINNET - SUA CONEXÃO REAL
            self.eth_provider = f"https://mainnet.infura.io/v3/{infura_project_id}"
            self.btc_api = "https://api.blockcypher.com/v1/btc/main"
        else:
            # TESTNET - PARA DESENVOLVIMENTO SEGURO
            self.eth_provider = f"https://sepolia.infura.io/v3/{infura_project_id}"
            self.btc_api = "https://api.blockcypher.com/v1/btc/test3"  # Bitcoin testnet
        
        self.w3 = Web3(Web3.HTTPProvider(self.eth_provider))
        
        print(f"🔗 Real Blockchain Connector: {self.mode.upper()} mode")
        print(f"⬨ Ethereum Connected: {self.w3.is_connected()}")
        print(f"₿ Bitcoin API: BlockCypher")
    
    # =========================================================================
    # ETHEREUM REAL - COM SUA INFURA
    # =========================================================================
    
    def get_eth_balance(self, address):
        """Consulta saldo REAL de Ethereum usando SUA Infura"""
        try:
            if not self.w3.is_connected():
                return {"error": "Ethereum provider not connected"}
            
            # Validar endereço
            if not self.w3.is_address(address):
                return {"error": "Invalid Ethereum address"}
            
            balance_wei = self.w3.eth.get_balance(address)
            balance_eth = self.w3.from_wei(balance_wei, 'ether')
            
            # Obter informações extras do bloco
            block_number = self.w3.eth.block_number
            
            return {
                "success": True,
                "address": address,
                "balance": float(balance_eth),
                "balance_wei": balance_wei,
                "unit": "ETH",
                "network": "ethereum",
                "block_number": block_number,
                "provider": "infura"
            }
            
        except Exception as e:
            return {"error": f"Erro ao consultar saldo ETH: {str(e)}"}
    
    def get_eth_transactions(self, address, limit=10):
        """Obtém transações Ethereum recentes (apenas mainnet)"""
        try:
            if self.mode != "mainnet":
                return {"error": "Transaction history only available on mainnet"}
            
            # Usar API Etherscan-like (precisa de API key separada)
            # Por enquanto, retornar transação atual
            return {
                "success": True,
                "address": address,
                "transactions": [],
                "note": "Full transaction history requires Etherscan API"
            }
        except Exception as e:
            return {"error": f"Erro ao obter transações: {str(e)}"}
    
    def send_real_eth(self, from_private_key, to_address, amount_eth):
        """Envia Ethereum REAL (apenas testnet para segurança)"""
        try:
            if self.mode == "mainnet":
                return {"error": "Mainnet transactions disabled for safety - use testnet"}
            
            if not self.w3.is_connected():
                return {"error": "Ethereum provider not connected"}
            
            # Validar endereço de destino
            if not self.w3.is_address(to_address):
                return {"error": "Invalid destination address"}
            
            # Obter conta da private key
            account = self.w3.eth.account.from_key(from_private_key)
            
            # Verificar saldo primeiro
            balance = self.w3.eth.get_balance(account.address)
            amount_wei = self.w3.to_wei(amount_eth, 'ether')
            
            if balance < amount_wei:
                return {"error": f"Saldo insuficiente. Disponível: {self.w3.from_wei(balance, 'ether')} ETH"}
            
            # Preparar transação
            transaction = {
                'to': to_address,
                'value': amount_wei,
                'gas': 21000,
                'gasPrice': self.w3.eth.gas_price,
                'nonce': self.w3.eth.get_transaction_count(account.address),
                'chainId': 11155111  # Sepolia testnet
            }
            
            # Estimar gas (pode ser mais que 21000 para contratos)
            try:
                transaction['gas'] = self.w3.eth.estimate_gas(transaction)
            except:
                transaction['gas'] = 21000  # Fallback para transferência simples
            
            # Assinar e enviar
            signed_txn = self.w3.eth.account.sign_transaction(transaction, from_private_key)
            tx_hash = self.w3.eth.send_raw_transaction(signed_txn.rawTransaction)
            
            # Obter informações da transação
            tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash, timeout=120)
            
            return {
                "success": True,
                "txid": tx_hash.hex(),
                "from": account.address,
                "to": to_address,
                "amount": amount_eth,
                "network": "ethereum testnet",
                "status": "confirmed" if tx_receipt.status == 1 else "failed",
                "block_number": tx_receipt.blockNumber,
                "gas_used": tx_receipt.gasUsed,
                "provider": "infura"
            }
            
        except Exception as e:
            return {"error": f"Erro ao enviar ETH: {str(e)}"}
    
    # =========================================================================
    # BITCOIN REAL - COM SEU BLOCKCYPHER
    # =========================================================================
    
    def get_btc_balance(self, address):
        """Consulta saldo REAL de Bitcoin usando SEU BlockCypher"""
        try:
            url = f"{self.btc_api}/addrs/{address}/balance"
            params = {"token": self.blockcypher_token}
            
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                balance_satoshis = data['balance']
                balance_btc = balance_satoshis / 100000000
                
                return {
                    "success": True,
                    "address": address,
                    "balance": balance_btc,
                    "balance_satoshis": balance_satoshis,
                    "unit": "BTC",
                    "network": "bitcoin",
                    "total_received": data['total_received'] / 100000000,
                    "total_sent": data['total_sent'] / 100000000,
                    "transaction_count": data['n_tx'],
                    "unconfirmed_balance": data['unconfirmed_balance'] / 100000000,
                    "final_balance": data['final_balance'] / 100000000,
                    "provider": "blockcypher"
                }
            else:
                return {"error": f"API error: {response.status_code} - {response.text}"}
                
        except Exception as e:
            return {"error": f"Erro ao consultar saldo BTC: {str(e)}"}
    
    def get_btc_transactions(self, address, limit=10):
        """Obtém transações Bitcoin recentes"""
        try:
            url = f"{self.btc_api}/addrs/{address}/full"
            params = {"token": self.blockcypher_token, "limit": limit}
            
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                transactions = []
                
                for tx in data.get('txs', [])[:limit]:
                    transactions.append({
                        "txid": tx['hash'],
                        "block_height": tx.get('block_height', 'pending'),
                        "confirmations": tx.get('confirmations', 0),
                        "time": tx['received'],
                        "total": tx['total'] / 100000000,
                        "fees": tx['fees'] / 100000000
                    })
                
                return {
                    "success": True,
                    "address": address,
                    "transactions": transactions,
                    "provider": "blockcypher"
                }
            else:
                return {"error": f"API error: {response.status_code}"}
                
        except Exception as e:
            return {"error": f"Erro ao obter transações BTC: {str(e)}"}
    
    def get_btc_price(self):
        """Obtém preço atual do Bitcoin"""
        try:
            # Usar API alternativa para preço (BlockCypher não tem preço)
            response = requests.get("https://blockchain.info/ticker", timeout=10)
            if response.status_code == 200:
                data = response.json()
                return {
                    "success": True,
                    "price_usd": data['USD']['last'],
                    "currency": "USD",
                    "timestamp": data['USD']['timestamp'],
                    "provider": "blockchain.info"
                }
            return {"error": "Failed to get BTC price"}
        except Exception as e:
            return {"error": f"Erro ao obter preço BTC: {str(e)}"}
    
    def send_real_btc(self, from_private_key, to_address, amount_btc):
        """Envia Bitcoin REAL (simulação - BlockCypher tem API de transações)"""
        try:
            # EM PRODUÇÃO: Implementar com BlockCypher Transaction API
            # https://www.blockcypher.com/dev/bitcoin/#creating-transactions
            
            return {
                "success": True,
                "txid": f"real_btc_tx_blockcypher_{os.urandom(4).hex()}",
                "from": "implement_with_blockcypher_api",
                "to": to_address,
                "amount": amount_btc,
                "network": "bitcoin",
                "status": "pending",
                "simulated": True,
                "note": "Real BTC transactions require BlockCypher transaction API implementation"
            }
            
        except Exception as e:
            return {"error": f"Erro ao enviar BTC: {str(e)}"}
    
    # =========================================================================
    # UTILITÁRIOS AVANÇADOS
    # =========================================================================
    
    def validate_eth_address(self, address):
        """Valida endereço Ethereum"""
        return self.w3.is_address(address)
    
    def validate_btc_address(self, address):
        """Valida endereço Bitcoin"""
        if not address or len(address) < 26 or len(address) > 62:
            return False
        
        # Prefixos válidos para Bitcoin
        valid_prefixes = ['1', '3', 'bc1']
        return any(address.startswith(prefix) for prefix in valid_prefixes)
    
    def get_network_status(self):
        """Retorna status completo das redes"""
        eth_connected = self.w3.is_connected()
        latest_block = self.w3.eth.block_number if eth_connected else None
        
        # Testar Bitcoin API
        btc_test = self.get_btc_balance("1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa")
        btc_connected = btc_test.get('success', False)
        
        return {
            "ethereum": {
                "connected": eth_connected,
                "network": "mainnet" if self.mode == "mainnet" else "sepolia testnet",
                "latest_block": latest_block,
                "provider": "infura",
                "your_project_id": "4622f8123b1a4cf7a3e30098d9120d7f"[:8] + "..."  # Mostrar apenas parte
            },
            "bitcoin": {
                "connected": btc_connected,
                "network": "mainnet" if self.mode == "mainnet" else "testnet3",
                "provider": "blockcypher",
                "your_token": self.blockcypher_token[:8] + "..."  # Mostrar apenas parte
            },
            "mode": self.mode,
            "status": "fully_operational" if (eth_connected and btc_connected) else "partial"
        }
    
    def get_gas_price(self):
        """Obtém preço do gas Ethereum"""
        try:
            gas_price = self.w3.eth.gas_price
            return {
                "success": True,
                "gas_price_wei": gas_price,
                "gas_price_gwei": self.w3.from_wei(gas_price, 'gwei'),
                "gas_price_eth": self.w3.from_wei(gas_price, 'ether')
            }
        except Exception as e:
            return {"error": f"Erro ao obter gas price: {str(e)}"}

# Instância global para uso
real_connector = RealBlockchainConnector(mode="testnet")

# Teste rápido das SUAS conexões
if __name__ == "__main__":
    print("🚀 TESTANDO SUAS CONEXÕES BLOCKCHAIN REAL...")
    print("=" * 60)
    
    connector = RealBlockchainConnector()
    
    # Testar status das redes
    status = connector.get_network_status()
    print("🔗 STATUS DAS REDES:")
    print(json.dumps(status, indent=2))
    
    # Testar saldo Ethereum (endereço conhecido)
    print("\n💰 TESTE ETHEREUM:")
    eth_balance = connector.get_eth_balance("0x742d35Cc6634C0532925a3b8Df6B5e5B5C5b5E5e")
    print(json.dumps(eth_balance, indent=2))
    
    # Testar saldo Bitcoin (Genesis address)
    print("\n₿ TESTE BITCOIN:")
    btc_balance = connector.get_btc_balance("1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa")
    print(json.dumps(btc_balance, indent=2))
    
    # Testar preço Bitcoin
    print("\n💵 PREÇO BITCOIN:")
    btc_price = connector.get_btc_price()
    print(json.dumps(btc_price, indent=2))
    
    # Testar gas price
    print("\n⛽ GAS PRICE ETHEREUM:")
    gas_price = connector.get_gas_price()
    print(json.dumps(gas_price, indent=2))