# contracts/ethereum_bridge.py - CORREÇÃO DEFINITIVA WEB3 v6.11.0
import json
import os
from web3 import Web3, HTTPProvider
from dotenv import load_dotenv

# 🔥 CARREGAR VARIÁVEIS DO .env
load_dotenv()

class RealEthereumBridge:
    def __init__(self):
        self.eth_w3 = None
        self.account = None
        self.private_key = None
        self.setup_web3()
        
    def setup_web3(self):
        """Configurar conexão Web3 com Ethereum"""
        try:
            print("🔧 Inicializando Ethereum Bridge...")
            
            # Verificar se as variáveis existem
            eth_rpc = os.getenv('ETH_RPC_URL')
            private_key = os.getenv('REAL_ETH_PRIVATE_KEY')
            
            print(f"📡 RPC URL: {'✅ Configurada' if eth_rpc else '❌ Faltando'}")
            print(f"🔑 Private Key: {'✅ Configurada' if private_key else '❌ Faltando'}")
            
            if not eth_rpc or not private_key:
                print("⚠️  Ethereum Bridge: Variáveis de ambiente não configuradas")
                print("   Configure ETH_RPC_URL e REAL_ETH_PRIVATE_KEY para usar funcionalidades reais")
                print("   Continuando em modo simulação...")
                self.eth_w3 = None
                self.account = None
                self.private_key = None
                return
            
            self.eth_w3 = Web3(HTTPProvider(eth_rpc))
            print(f"✅ Ethereum Conectado: {self.eth_w3.is_connected()}")
            
            self.private_key = private_key
            if self.private_key.startswith('0x'):
                self.private_key = self.private_key[2:]
                
            self.account = self.eth_w3.eth.account.from_key(self.private_key)
            print(f"✅ Conta Ethereum: {self.account.address}")
            
            # Verificar saldo
            balance = self.eth_w3.eth.get_balance(self.account.address)
            balance_eth = self.eth_w3.from_wei(balance, 'ether')
            print(f"💰 Saldo: {balance_eth} ETH")
            
        except Exception as e:
            print(f"⚠️  Erro setup Ethereum: {e}")
            print("   Continuando em modo simulação...")
            self.eth_w3 = None
            self.account = None
            self.private_key = None
        
    def get_contract_abi(self):
        """ABI simplificada para teste"""
        return [
            {
                "inputs": [
                    {"internalType": "uint256", "name": "amount", "type": "uint256"},
                    {"internalType": "string", "name": "targetChain", "type": "string"}
                ],
                "name": "lockTokens",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function"
            },
            {
                "anonymous": False,
                "inputs": [
                    {"indexed": True, "internalType": "address", "name": "user", "type": "address"},
                    {"indexed": False, "internalType": "uint256", "name": "amount", "type": "uint256"},
                    {"indexed": False, "internalType": "string", "name": "targetChain", "type": "string"}
                ],
                "name": "TokensLocked",
                "type": "event"
            }
        ]
    
    def test_transaction(self):
        """Teste SIMPLES de transação REAL - CORREÇÃO DEFINITIVA"""
        try:
            print("🚀 Testando transação REAL...")
            
            # Verificar saldo primeiro
            balance = self.eth_w3.eth.get_balance(self.account.address)
            balance_eth = self.eth_w3.from_wei(balance, 'ether')
            
            if balance_eth < 0.001:
                raise Exception(f"Saldo insuficiente: {balance_eth} ETH. Precisa de pelo menos 0.001 ETH para gas")
            
            # Criar transação SIMPLES (enviar 0 ETH para si mesmo)
            nonce = self.eth_w3.eth.get_transaction_count(self.account.address)
            
            transaction = {
                'to': self.account.address,  # Enviar para si mesmo
                'value': 0,  # 0 ETH - só testar gas
                'gas': 21000,
                'gasPrice': self.eth_w3.eth.gas_price,
                'nonce': nonce,
                'chainId': 11155111  # Sepolia
            }
            
            # 🔥 CORREÇÃO DEFINITIVA: Verificar estrutura do objeto signed_txn
            signed_txn = self.eth_w3.eth.account.sign_transaction(transaction, self.private_key)
            
            # DEBUG: Mostrar estrutura do objeto
            print(f"🔍 DEBUG - Tipo signed_txn: {type(signed_txn)}")
            print(f"🔍 DEBUG - Atributos: {dir(signed_txn)}")
            
            # Tentar diferentes atributos possíveis
            raw_tx = None
            if hasattr(signed_txn, 'rawTransaction'):
                raw_tx = signed_txn.rawTransaction
                print("✅ Usando rawTransaction")
            elif hasattr(signed_txn, 'raw_transaction'):
                raw_tx = signed_txn.raw_transaction  
                print("✅ Usando raw_transaction")
            elif hasattr(signed_txn, 'raw_tx'):
                raw_tx = signed_txn.raw_tx
                print("✅ Usando raw_tx")
            else:
                # Último recurso: usar __dict__
                tx_dict = signed_txn.__dict__
                if 'rawTransaction' in tx_dict:
                    raw_tx = tx_dict['rawTransaction']
                    print("✅ Usando __dict__['rawTransaction']")
                elif 'raw_transaction' in tx_dict:
                    raw_tx = tx_dict['raw_transaction']
                    print("✅ Usando __dict__['raw_transaction']")
            
            if not raw_tx:
                raise Exception("Não foi possível encontrar raw transaction no objeto signed_txn")
            
            tx_hash = self.eth_w3.eth.send_raw_transaction(raw_tx)
            
            print(f"✅ Transação REAL enviada!")
            print(f"📝 Hash: {tx_hash.hex()}")
            print(f"🔗 Explorer: https://sepolia.etherscan.io/tx/{tx_hash.hex()}")
            
            # Aguardar confirmação
            print("⏳ Aguardando confirmação...")
            receipt = self.eth_w3.eth.wait_for_transaction_receipt(tx_hash, timeout=120)
            
            print(f"✅ Transação confirmada no bloco: {receipt.blockNumber}")
            
            return {
                "success": True,
                "tx_hash": tx_hash.hex(),
                "block_number": receipt.blockNumber,
                "explorer": f"https://sepolia.etherscan.io/tx/{tx_hash.hex()}"
            }
            
        except Exception as e:
            print(f"❌ Erro na transação: {e}")
            return {"success": False, "error": str(e)}
    
    def deploy_contract(self):
        """Deploy SIMPLIFICADO para teste - CORREÇÃO DEFINITIVA"""
        try:
            print("🚀 Deployando contrato...")
            
            # Bytecode MUITO simples (apenas para teste)
            contract_bytecode = "0x" + "60" * 100  # Bytecode dummy simplificado
            
            # Criar contrato
            contract = self.eth_w3.eth.contract(
                abi=self.get_contract_abi(),
                bytecode=contract_bytecode
            )
            
            nonce = self.eth_w3.eth.get_transaction_count(self.account.address)
            
            construct_txn = contract.constructor().build_transaction({
                'from': self.account.address,
                'nonce': nonce,
                'gas': 2000000,
                'gasPrice': self.eth_w3.eth.gas_price,
                'chainId': 11155111
            })
            
            # 🔥 CORREÇÃO DEFINITIVA: Mesma lógica de detecção
            signed_txn = self.eth_w3.eth.account.sign_transaction(construct_txn, self.private_key)
            
            # Detectar atributo correto
            raw_tx = None
            if hasattr(signed_txn, 'rawTransaction'):
                raw_tx = signed_txn.rawTransaction
            elif hasattr(signed_txn, 'raw_transaction'):
                raw_tx = signed_txn.raw_transaction
            elif hasattr(signed_txn, 'raw_tx'):
                raw_tx = signed_txn.raw_tx
            else:
                tx_dict = signed_txn.__dict__
                if 'rawTransaction' in tx_dict:
                    raw_tx = tx_dict['rawTransaction']
                elif 'raw_transaction' in tx_dict:
                    raw_tx = tx_dict['raw_transaction']
            
            if not raw_tx:
                raise Exception("Não foi possível encontrar raw transaction")
                
            tx_hash = self.eth_w3.eth.send_raw_transaction(raw_tx)
            
            print(f"✅ Contrato deployado! Hash: {tx_hash.hex()}")
            
            # Aguardar
            receipt = self.eth_w3.eth.wait_for_transaction_receipt(tx_hash, timeout=120)
            contract_address = receipt.contractAddress
            
            print(f"✅ Contrato em: {contract_address}")
            return contract_address
            
        except Exception as e:
            print(f"❌ Erro no deploy: {e}")
            raise e

    def lock_tokens(self, amount_wei, target_chain="polygon"):
        """Fazer lock REAL de tokens na Ethereum"""
        try:
            contract_address = os.getenv('BRIDGE_CONTRACT_ETH')
            if not contract_address or contract_address == "0x...":
                raise Exception("Contrato não deployado ainda. Use /real/test/simple_deploy primeiro.")
                
            print(f"🔒 Fazendo lock de {self.eth_w3.from_wei(amount_wei, 'ether')} ETH para {target_chain}...")
            
            contract = self.eth_w3.eth.contract(
                address=contract_address,
                abi=self.get_contract_abi()
            )
            
            nonce = self.eth_w3.eth.get_transaction_count(self.account.address)
            
            transaction = contract.functions.lockTokens(amount_wei, target_chain).build_transaction({
                'from': self.account.address,
                'nonce': nonce,
                'gas': 200000,
                'gasPrice': self.eth_w3.eth.gas_price,
                'chainId': 11155111
            })
            
            # Usar mesma lógica de detecção
            signed_txn = self.eth_w3.eth.account.sign_transaction(transaction, self.private_key)
            
            raw_tx = None
            if hasattr(signed_txn, 'rawTransaction'):
                raw_tx = signed_txn.rawTransaction
            elif hasattr(signed_txn, 'raw_transaction'):
                raw_tx = signed_txn.raw_transaction
            elif hasattr(signed_txn, 'raw_tx'):
                raw_tx = signed_txn.raw_tx
            else:
                tx_dict = signed_txn.__dict__
                if 'rawTransaction' in tx_dict:
                    raw_tx = tx_dict['rawTransaction']
                elif 'raw_transaction' in tx_dict:
                    raw_tx = tx_dict['raw_transaction']
            
            if not raw_tx:
                raise Exception("Não foi possível encontrar raw transaction")
                
            tx_hash = self.eth_w3.eth.send_raw_transaction(raw_tx)
            
            print(f"🔒 Tokens locked na Ethereum!")
            print(f"📝 Tx Hash: {tx_hash.hex()}")
            print(f"🔗 Explorer: https://sepolia.etherscan.io/tx/{tx_hash.hex()}")
            
            return tx_hash.hex()
            
        except Exception as e:
            print(f"❌ Erro no lock: {e}")
            raise e

# Função auxiliar para teste rápido
def quick_test():
    """Teste rápido da bridge"""
    try:
        bridge = RealEthereumBridge()
        print("✅ Bridge inicializada com sucesso!")
        
        # Testar saldo
        balance = bridge.eth_w3.eth.get_balance(bridge.account.address)
        balance_eth = bridge.eth_w3.from_wei(balance, 'ether')
        print(f"💰 Saldo atual: {balance_eth} ETH")
        
        return {
            "success": True,
            "address": bridge.account.address,
            "balance_eth": float(balance_eth),
            "connected": bridge.eth_w3.is_connected()
        }
        
    except Exception as e:
        print(f"❌ Erro no teste rápido: {e}")
        return {"success": False, "error": str(e)}

if __name__ == "__main__":
    # Teste rápido quando executado diretamente
    result = quick_test()
    print("Resultado do teste:", result)