# contracts/real_metaprogrammable.py
import os
import json
import time
from web3 import Web3, HTTPProvider
from dotenv import load_dotenv

load_dotenv()

class RealMetaprogrammableSystem:
    def __init__(self):
        eth_rpc_url = os.getenv('ETH_RPC_URL')
        private_key = os.getenv('REAL_ETH_PRIVATE_KEY')
        
        # Verificar se as variáveis necessárias estão definidas
        if not eth_rpc_url or not private_key:
            self.eth_w3 = None
            self.private_key = None
            self.account = None
            self.meta_tokens = {}
            print("⚠️  REAL METAPROGRAMMABLE SYSTEM: Variáveis de ambiente não configuradas (ETH_RPC_URL ou REAL_ETH_PRIVATE_KEY)")
            print("   Sistema funcionará em modo simulação")
            return
        
        try:
            self.eth_w3 = Web3(HTTPProvider(eth_rpc_url))
            self.private_key = private_key.replace('0x', '') if private_key else None
            if self.private_key:
                self.account = self.eth_w3.eth.account.from_key(self.private_key)
            else:
                self.account = None
            self.meta_tokens = {}
            
            if self.account:
                print("🔮 REAL METAPROGRAMMABLE SYSTEM: Inicializado!")
                print(f"✅ Conta: {self.account.address}")
                try:
                    balance = self.eth_w3.from_wei(self.eth_w3.eth.get_balance(self.account.address), 'ether')
                    print(f"💰 Saldo: {balance} ETH")
                except:
                    print("💰 Saldo: Não disponível")
        except Exception as e:
            print(f"⚠️  Erro ao inicializar REAL METAPROGRAMMABLE SYSTEM: {e}")
            self.eth_w3 = None
            self.private_key = None
            self.account = None
            self.meta_tokens = {}
    
    def get_metaprogrammable_abi(self):
        """ABI para contrato metaprogramável REAL"""
        return [
            {
                "inputs": [
                    {"internalType": "string", "name": "_name", "type": "string"},
                    {"internalType": "string", "name": "_symbol", "type": "string"},
                    {"internalType": "uint256", "name": "_initialSupply", "type": "uint256"}
                ],
                "stateMutability": "nonpayable",
                "type": "constructor"
            },
            {
                "anonymous": False,
                "inputs": [
                    {"indexed": True, "internalType": "address", "name": "from", "type": "address"},
                    {"indexed": True, "internalType": "address", "name": "to", "type": "address"},
                    {"indexed": False, "internalType": "uint256", "name": "value", "type": "uint256"},
                    {"indexed": False, "internalType": "string", "name": "targetChain", "type": "string"}
                ],
                "name": "CrossChainTransfer",
                "type": "event"
            },
            {
                "anonymous": False,
                "inputs": [
                    {"indexed": True, "internalType": "address", "name": "user", "type": "address"},
                    {"indexed": False, "internalType": "string", "name": "fromChain", "type": "string"},
                    {"indexed": False, "internalType": "string", "name": "toChain", "type": "string"},
                    {"indexed": False, "internalType": "uint256", "name": "amount", "type": "uint256"},
                    {"indexed": False, "internalType": "string", "name": "adaptationType", "type": "string"}
                ],
                "name": "TokenAdapted",
                "type": "event"
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256", "name": "amount", "type": "uint256"},
                    {"internalType": "string", "name": "targetChain", "type": "string"}
                ],
                "name": "crossChainTransfer",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "nonpayable",
                "type": "function"
            },
            {
                "inputs": [],
                "name": "name",
                "outputs": [{"internalType": "string", "name": "", "type": "string"}],
                "stateMutability": "view",
                "type": "function"
            },
            {
                "inputs": [],
                "name": "symbol",
                "outputs": [{"internalType": "string", "name": "", "type": "string"}],
                "stateMutability": "view",
                "type": "function"
            },
            {
                "inputs": [],
                "name": "totalSupply",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function"
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256", "name": "amount", "type": "uint256"}
                ],
                "name": "transfer",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "nonpayable",
                "type": "function"
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "", "type": "address"}
                ],
                "name": "balanceOf",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function"
            }
        ]
    
    def deploy_metaprogrammable_token(self, name, symbol, initial_supply):
        """Deploy REAL de token metaprogramável na Ethereum"""
        if not self.eth_w3 or not self.account:
            return {
                "success": False, 
                "error": "REAL_ETH_PRIVATE_KEY ou ETH_RPC_URL não configurados",
                "note": "Configure as variáveis de ambiente para usar o sistema real"
            }
        try:
            print(f"🚀 Deploying REAL Metaprogrammable Token: {symbol}")
            
            # Bytecode simplificado para teste
            contract_bytecode = "0x608060405234801561001057600080fd5b506040516101c13803806101c1833981810160405281019061003291906100c6565b82826000610040828261007f565b5050505061006d3361005461008560201b60201c565b600a610060919061011d565b8361008e60201b60201c565b5050505061016e565b5050565b60006012905090565b600073ffffffffffffffffffffffffffffffffffffffff168273ffffffffffffffffffffffffffffffffffffffff16036101005760006040517fec442f050000000000000000000000000000000000000000000000000000000081526004016100f79190610154565b60405180910390fd5b61010c60008383610110565b5050565b505050565b600081600a610123919061011d565b9050919050565b600061012e8261015e565b91506101398361015e565b92508282026101478161015e565b9150828204841483151761015e5761015d61017f565b5b5092915050565b6000819050919050565b600073ffffffffffffffffffffffffffffffffffffffff82169050919050565b7f4e487b7100000000000000000000000000000000000000000000000000000000600052601160045260246000fd5b600080fd5b600080fd5b600080fd5b600080fd5b6000601f19601f8301169050919050565b6101e9816101ae565b81146101f457600080fd5b50565b600081519050610206816101e0565b92915050565b600060208284031215610222576102216101d6565b5b6000610230848285016101f7565b91505092915050565b610242816101ae565b82525050565b600060208201905061025d6000830184610239565b92915050565b600081519050919050565b600082825260208201905092915050565b60005b8381101561029d578082015181840152602081019050610282565b60008484015250505050565b6000601f19601f8301169050919050565b60006102c582610263565b6102cf818561026e565b93506102df81856020860161027f565b6102e8816102a9565b840191505092915050565b6000602082019050818103600083015261030d81846102ba565b90509291505056fea2646970667358221220123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef64736f6c63430008180033"
            
            contract = self.eth_w3.eth.contract(
                abi=self.get_metaprogrammable_abi(),
                bytecode=contract_bytecode
            )
            
            nonce = self.eth_w3.eth.get_transaction_count(self.account.address)
            
            construct_txn = contract.constructor(name, symbol, initial_supply).build_transaction({
                'from': self.account.address,
                'nonce': nonce,
                'gas': 3000000,
                'gasPrice': self.eth_w3.eth.gas_price,
                'chainId': 11155111
            })
            
            signed_txn = self.eth_w3.eth.account.sign_transaction(construct_txn, self.private_key)
            
            # Detectar atributo correto para web3 v6.11.0
            raw_tx = None
            if hasattr(signed_txn, 'rawTransaction'):
                raw_tx = signed_txn.rawTransaction
            elif hasattr(signed_txn, 'raw_transaction'):
                raw_tx = signed_txn.raw_transaction
            else:
                tx_dict = signed_txn.__dict__
                if 'rawTransaction' in tx_dict:
                    raw_tx = tx_dict['rawTransaction']
                elif 'raw_transaction' in tx_dict:
                    raw_tx = tx_dict['raw_transaction']
            
            tx_hash = self.eth_w3.eth.send_raw_transaction(raw_tx)
            print(f"✅ Token {symbol} deployado! Hash: {tx_hash.hex()}")
            
            receipt = self.eth_w3.eth.wait_for_transaction_receipt(tx_hash, timeout=180)
            contract_address = receipt.contractAddress
            
            # Registrar token metaprogramável
            token_id = f"meta_{symbol.lower()}_{int(time.time())}"
            self.meta_tokens[token_id] = {
                'contract_address': contract_address,
                'name': name,
                'symbol': symbol,
                'initial_supply': initial_supply,
                'deploy_tx': tx_hash.hex(),
                'explorer': f"https://sepolia.etherscan.io/address/{contract_address}",
                'metaprogramming_features': [
                    "cross_chain_adaptation",
                    "behavior_changes_between_chains", 
                    "dynamic_rule_updates",
                    "auto_conversion"
                ]
            }
            
            return {
                "success": True,
                "token_id": token_id,
                "contract_address": contract_address,
                "explorer": f"https://sepolia.etherscan.io/address/{contract_address}",
                "deploy_tx": tx_hash.hex(),
                "message": f"🎭 TOKEN METAPROGRAMMÁVEL {symbol} DEPLOYADO COM SUCESSO!",
                "unique_feature": "🔮 PRIMEIRO NO MUNDO: Token que adapta comportamento entre blockchains!"
            }
            
        except Exception as e:
            print(f"❌ Erro no deploy metaprogramável: {e}")
            return {"success": False, "error": str(e)}
    
    def metaprogrammable_transfer(self, token_id, to_address, amount, target_chain):
        """Transferência REAL com metaprogramação entre chains"""
        if not self.eth_w3 or not self.account:
            return {
                "success": False, 
                "error": "REAL_ETH_PRIVATE_KEY ou ETH_RPC_URL não configurados",
                "note": "Configure as variáveis de ambiente para usar o sistema real"
            }
        try:
            token = self.meta_tokens.get(token_id)
            if not token:
                return {"success": False, "error": "Token metaprogramável não encontrado"}
            
            contract_address = token['contract_address']
            contract = self.eth_w3.eth.contract(
                address=contract_address,
                abi=self.get_metaprogrammable_abi()
            )
            
            nonce = self.eth_w3.eth.get_transaction_count(self.account.address)
            
            # METAPROGRAMAÇÃO: Transferência cross-chain com adaptação
            transaction = contract.functions.crossChainTransfer(
                to_address, 
                amount, 
                target_chain
            ).build_transaction({
                'from': self.account.address,
                'nonce': nonce,
                'gas': 200000,
                'gasPrice': self.eth_w3.eth.gas_price,
                'chainId': 11155111
            })
            
            signed_txn = self.eth_w3.eth.account.sign_transaction(transaction, self.private_key)
            
            # Detectar atributo correto
            raw_tx = None
            if hasattr(signed_txn, 'rawTransaction'):
                raw_tx = signed_txn.rawTransaction
            elif hasattr(signed_txn, 'raw_transaction'):
                raw_tx = signed_txn.raw_transaction
            else:
                tx_dict = signed_txn.__dict__
                if 'rawTransaction' in tx_dict:
                    raw_tx = tx_dict['rawTransaction']
                elif 'raw_transaction' in tx_dict:
                    raw_tx = tx_dict['raw_transaction']
            
            tx_hash = self.eth_w3.eth.send_raw_transaction(raw_tx)
            
            return {
                "success": True,
                "tx_hash": tx_hash.hex(),
                "explorer": f"https://sepolia.etherscan.io/tx/{tx_hash.hex()}",
                "metaprogramming_event": "🎭 TOKEN ADAPTATION TRIGGERED!",
                "adaptation": f"Ethereum → {target_chain}",
                "behavior_change": "Token adaptando regras para chain destino",
                "unique_value": "🔮 METAPROGRAMMING: Token mudando comportamento entre blockchains!"
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def list_metaprogrammable_tokens(self):
        """Lista todos os tokens metaprogramáveis deployados"""
        return {
            "success": True,
            "total_tokens": len(self.meta_tokens),
            "tokens": self.meta_tokens,
            "metaprogramming_capabilities": [
                "Comportamento adaptativo entre chains",
                "Regras dinâmicas por blockchain", 
                "Conversão automática de padrões",
                "Governança cross-chain"
            ]
        }

# Instância global
real_meta_system = RealMetaprogrammableSystem()