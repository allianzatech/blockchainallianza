# bridge_lock_verifier.py
# 🔒 VERIFICADOR DE LOCK ON-CHAIN - MELHORIA DE INTEROPERABILIDADE
# Verifica se locks foram confirmados on-chain antes de fazer unlock

import os
import time
import requests
from typing import Dict, Optional
from web3 import Web3
from web3.middleware import geth_poa_middleware
from dotenv import load_dotenv

load_dotenv()

class BridgeLockVerifier:
    """
    Verificador de Lock On-Chain
    MELHORIA: Verifica se locks foram confirmados on-chain antes de unlock
    """
    
    def __init__(self):
        self.setup_connections()
        print("🔒 BRIDGE LOCK VERIFIER: Inicializado!")
        print("   • Verificação on-chain de locks")
        print("   • Suporte a múltiplas blockchains")
    
    def setup_connections(self):
        """Configurar conexões com blockchains"""
        try:
            # BlockCypher API para Bitcoin
            self.blockcypher_token = os.getenv('BLOCKCYPHER_API_TOKEN', '17766314e49c439e85cec883969614ac')
            self.btc_api_base = "https://api.blockcypher.com/v1/btc/test3"
            
            # Web3 para EVM chains
            infura_id = os.getenv('INFURA_PROJECT_ID', '4622f8123b1a4cf7a3e30098d9120d7f')
            
            # Polygon
            polygon_rpcs = [
                os.getenv('POLYGON_RPC_URL') or 'https://rpc-amoy.polygon.technology/',
                'https://polygon-amoy.drpc.org',
                'https://rpc.ankr.com/polygon_amoy'
            ]
            self.polygon_w3 = None
            for rpc in polygon_rpcs:
                try:
                    test_w3 = Web3(Web3.HTTPProvider(rpc, request_kwargs={'timeout': 30}))
                    test_w3.middleware_onion.inject(geth_poa_middleware, layer=0)
                    if test_w3.is_connected():
                        self.polygon_w3 = test_w3
                        break
                except:
                    continue
            
            # Ethereum
            eth_rpcs = [
                os.getenv('ETH_RPC_URL', f'https://sepolia.infura.io/v3/{infura_id}'),
                'https://ethereum-sepolia-rpc.publicnode.com'
            ]
            self.eth_w3 = None
            for rpc in eth_rpcs:
                try:
                    test_w3 = Web3(Web3.HTTPProvider(rpc, request_kwargs={'timeout': 30}))
                    if test_w3.is_connected():
                        self.eth_w3 = test_w3
                        break
                except:
                    continue
            
            # BSC
            bsc_rpcs = [
                os.getenv('BSC_RPC_URL', 'https://data-seed-prebsc-1-s1.binance.org:8545'),
                'https://bsc-testnet-rpc.publicnode.com'
            ]
            self.bsc_w3 = None
            for rpc in bsc_rpcs:
                try:
                    test_w3 = Web3(Web3.HTTPProvider(rpc, request_kwargs={'timeout': 30}))
                    if test_w3.is_connected():
                        self.bsc_w3 = test_w3
                        break
                except:
                    continue
                    
        except Exception as e:
            print(f"⚠️  Erro ao configurar conexões: {e}")
    
    def verify_lock_on_chain(self, source_chain: str, lock_id: str, min_confirmations: int = 6) -> Dict:
        """
        Verificar se lock existe e está válido on-chain
        
        Args:
            source_chain: Blockchain de origem (bitcoin, polygon, ethereum, bsc)
            lock_id: ID do lock (pode ser tx_hash ou lock_id)
            min_confirmations: Número mínimo de confirmações necessárias
        
        Returns:
            Dict com success, confirmed, confirmations, etc.
        """
        try:
            source_chain_lower = source_chain.lower()
            
            # Para EVM chains (Polygon, Ethereum, BSC, Base)
            if source_chain_lower in ['polygon', 'ethereum', 'bsc', 'base']:
                return self._verify_lock_evm(source_chain_lower, lock_id, min_confirmations)
            
            # Para Bitcoin
            elif source_chain_lower == 'bitcoin':
                return self._verify_lock_bitcoin(lock_id, min_confirmations)
            
            else:
                return {
                    "success": False,
                    "error": f"Chain {source_chain} não suportada para verificação"
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": f"Erro ao verificar lock: {str(e)}"
            }
    
    def _verify_lock_evm(self, chain: str, tx_hash: str, min_confirmations: int) -> Dict:
        """Verificar lock em blockchain EVM"""
        try:
            # Obter Web3 instance
            w3 = None
            if chain == 'polygon':
                w3 = self.polygon_w3
            elif chain == 'ethereum':
                w3 = self.eth_w3
            elif chain == 'bsc':
                w3 = self.bsc_w3
            
            if not w3 or not w3.is_connected():
                return {
                    "success": False,
                    "error": f"Não foi possível conectar a {chain}"
                }
            
            # Buscar transação
            try:
                tx = w3.eth.get_transaction(tx_hash)
                tx_receipt = w3.eth.get_transaction_receipt(tx_hash)
            except Exception as e:
                return {
                    "success": False,
                    "error": f"Transação não encontrada: {str(e)}"
                }
            
            # Verificar confirmações
            current_block = w3.eth.block_number
            confirmations = current_block - tx_receipt.blockNumber if tx_receipt else 0
            
            # Verificar status
            is_confirmed = confirmations >= min_confirmations
            status = tx_receipt.status if tx_receipt else 0
            
            return {
                "success": True,
                "confirmed": is_confirmed,
                "confirmations": confirmations,
                "min_confirmations": min_confirmations,
                "tx_hash": tx_hash,
                "block_number": tx_receipt.blockNumber if tx_receipt else None,
                "status": "success" if status == 1 else "failed",
                "from_address": tx['from'] if tx else None,
                "to_address": tx['to'] if tx else None,
                "value": tx['value'] if tx else 0
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Erro ao verificar lock EVM: {str(e)}"
            }
    
    def _verify_lock_bitcoin(self, tx_hash: str, min_confirmations: int) -> Dict:
        """Verificar lock em Bitcoin"""
        try:
            # Usar BlockCypher API
            url = f"{self.btc_api_base}/txs/{tx_hash}"
            headers = {"token": self.blockcypher_token}
            
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code != 200:
                return {
                    "success": False,
                    "error": f"Transação não encontrada: {response.status_code}"
                }
            
            tx_data = response.json()
            confirmations = tx_data.get('confirmations', 0)
            is_confirmed = confirmations >= min_confirmations
            
            return {
                "success": True,
                "confirmed": is_confirmed,
                "confirmations": confirmations,
                "min_confirmations": min_confirmations,
                "tx_hash": tx_hash,
                "block_height": tx_data.get('block_height'),
                "status": "confirmed" if is_confirmed else "pending"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Erro ao verificar lock Bitcoin: {str(e)}"
            }
    
    def wait_for_confirmations(
        self, 
        source_chain: str, 
        lock_id: str, 
        min_confirmations: int = 6,
        max_wait_time: int = 300,
        check_interval: int = 5
    ) -> Dict:
        """
        Aguardar até que lock tenha confirmações suficientes
        
        Args:
            source_chain: Blockchain de origem
            lock_id: ID do lock
            min_confirmations: Número mínimo de confirmações
            max_wait_time: Tempo máximo de espera (segundos)
            check_interval: Intervalo entre verificações (segundos)
        
        Returns:
            Dict com resultado da verificação
        """
        start_time = time.time()
        
        while time.time() - start_time < max_wait_time:
            result = self.verify_lock_on_chain(source_chain, lock_id, min_confirmations)
            
            if result.get("success") and result.get("confirmed"):
                return {
                    "success": True,
                    "confirmed": True,
                    "confirmations": result.get("confirmations"),
                    "wait_time": time.time() - start_time
                }
            
            # Aguardar antes de verificar novamente
            time.sleep(check_interval)
        
        # Timeout
        return {
            "success": False,
            "error": f"Timeout: Lock não confirmado após {max_wait_time} segundos",
            "wait_time": time.time() - start_time
        }

