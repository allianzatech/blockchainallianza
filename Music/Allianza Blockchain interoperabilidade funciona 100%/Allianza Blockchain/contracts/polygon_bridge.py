# contracts/polygon_bridge.py - CORRIGIDO PARA WEB3 v6.11.0
import json
import os
from web3 import Web3, HTTPProvider
from web3.middleware import geth_poa_middleware
from dotenv import load_dotenv

# 🔥 CARREGAR VARIÁVEIS DO .env
load_dotenv()

class RealPolygonBridge:
    def __init__(self):
        self.poly_w3 = None
        self.account = None
        self.private_key = None
        self.setup_web3()
        
    def setup_web3(self):
        """Configurar conexão Web3 com Polygon - CORRIGIDO PARA WEB3 v6.11.0"""
        try:
            print("🔧 Inicializando Polygon Bridge...")
            
            poly_rpc = os.getenv('POLY_RPC_URL')
            private_key = os.getenv('REAL_POLY_PRIVATE_KEY')
            
            print(f"📡 Polygon RPC: {'✅ Configurada' if poly_rpc else '❌ Faltando'}")
            print(f"🔑 Polygon Private Key: {'✅ Configurada' if private_key else '❌ Faltando'}")
            
            if not poly_rpc:
                # Usar RPC pública como fallback
                poly_rpc = "https://polygon-amoy.infura.io/v3/4622f8123b1a4cf7a3e30098d9120d7f"
                print("⚠️  Usando RPC pública como fallback")
            
            if not private_key:
                # Usar a mesma private key do Ethereum como fallback para testes
                private_key = os.getenv('REAL_ETH_PRIVATE_KEY')
                if private_key:
                    print("⚠️  Usando ETH private key para Polygon (TESTES)")
                else:
                    raise Exception("Nenhuma private key configurada")
            
            self.poly_w3 = Web3(HTTPProvider(poly_rpc))
            
            if self.poly_w3.is_connected():
                # Polygon Amoy é POA, precisa do middleware
                self.poly_w3.middleware_onion.inject(geth_poa_middleware, layer=0)
                print("✅ Polygon: Conectado com sucesso")
            else:
                print("❌ Polygon: Não foi possível conectar")
                self.poly_w3 = None
                return
                
            self.private_key = private_key
            if self.private_key.startswith('0x'):
                self.private_key = self.private_key[2:]
                
            self.account = self.poly_w3.eth.account.from_key(self.private_key)
            print(f"✅ Polygon Bridge: Conectado - {self.account.address}")
            
            # Verificar saldo
            balance = self.poly_w3.eth.get_balance(self.account.address)
            balance_matic = self.poly_w3.from_wei(balance, 'ether')
            print(f"💰 Saldo Polygon: {balance_matic} MATIC")
            
            # Se saldo for 0, sugerir faucet
            if balance_matic == 0:
                print("💡 Dica: Use o faucet do Polygon Amoy: https://faucet.polygon.technology/")
                
        except Exception as e:
            print(f"❌ Erro ao conectar Polygon: {e}")
            self.poly_w3 = None
            self.account = None
    
    def get_contract_abi(self):
        """ABI do contrato Polygon Bridge"""
        return [
            {
                "inputs": [
                    {"internalType": "address", "name": "user", "type": "address"},
                    {"internalType": "uint256", "name": "amount", "type": "uint256"},
                    {"internalType": "bytes32", "name": "proof", "type": "bytes32"}
                ],
                "name": "unlockTokens",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function"
            },
            {
                "anonymous": False,
                "inputs": [
                    {"indexed": True, "internalType": "address", "name": "user", "type": "address"},
                    {"indexed": False, "internalType": "uint256", "name": "amount", "type": "uint256"},
                    {"indexed": False, "internalType": "bytes32", "name": "proof", "type": "bytes32"}
                ],
                "name": "TokensUnlocked",
                "type": "event"
            }
        ]
    
    def deploy_contract(self):
        """Deploy do contrato REAL na Polygon - CORRIGIDO PARA WEB3 v6.11.0"""
        if not self.poly_w3 or not self.poly_w3.is_connected():
            raise Exception("❌ Não conectado à Polygon")
            
        if not self.account:
            raise Exception("❌ Conta Polygon não configurada")
            
        # Bytecode simplificado para teste
        contract_bytecode = "0x6080604052348015600f57600080fd5b5060008054600160a060020a0319163317905561011c806100316000396000f3fe608060405260043610603f576000357c010000000000000000000000000000000000000000000000000000000090048063e6c2c5c5146044575b600080fd5b348015604f57600080fd5b5060566068565b60408051918252519081900360200190f35b6000548156fea2646970667358221220123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef64736f6c63430006000033"
        
        contract = self.poly_w3.eth.contract(
            abi=self.get_contract_abi(),
            bytecode=contract_bytecode
        )
        
        nonce = self.poly_w3.eth.get_transaction_count(self.account.address)
        
        construct_txn = contract.constructor().build_transaction({
            'from': self.account.address,
            'nonce': nonce,
            'gas': 2000000,
            'gasPrice': self.poly_w3.eth.gas_price,
            'chainId': 80002  # Polygon Amoy
        })
        
        # 🔥 CORREÇÃO: signed_txn.raw_transaction em v6.11.0
        signed_txn = self.poly_w3.eth.account.sign_transaction(construct_txn, self.private_key)
        tx_hash = self.poly_w3.eth.send_raw_transaction(signed_txn.raw_transaction)
        
        print(f"🚀 Contrato Polygon Bridge deployado!")
        print(f"📝 Tx Hash: {tx_hash.hex()}")
        
        receipt = self.poly_w3.eth.wait_for_transaction_receipt(tx_hash, timeout=120)
        contract_address = receipt.contractAddress
        
        print(f"✅ Contrato deployado em: {contract_address}")
        return contract_address
    
    def unlock_tokens(self, user_address, amount_wei, proof):
        """Fazer unlock REAL de tokens na Polygon - CORRIGIDO PARA WEB3 v6.11.0"""
        try:
            contract_address = os.getenv('BRIDGE_CONTRACT_POLY')
            if not contract_address or contract_address == "0x...":
                raise Exception("Contrato Polygon não deployado ainda")
                
            print(f"🔓 Fazendo unlock de {self.poly_w3.from_wei(amount_wei, 'ether')} ETH para {user_address}...")
            
            contract = self.poly_w3.eth.contract(
                address=contract_address,
                abi=self.get_contract_abi()
            )
            
            nonce = self.poly_w3.eth.get_transaction_count(self.account.address)
            
            transaction = contract.functions.unlockTokens(user_address, amount_wei, proof).build_transaction({
                'from': self.account.address,
                'nonce': nonce,
                'gas': 200000,
                'gasPrice': self.poly_w3.eth.gas_price,
                'chainId': 80002  # Polygon Amoy
            })
            
            # 🔥 CORREÇÃO: signed_txn.raw_transaction em v6.11.0
            signed_txn = self.poly_w3.eth.account.sign_transaction(transaction, self.private_key)
            tx_hash = self.poly_w3.eth.send_raw_transaction(signed_txn.raw_transaction)
            
            print(f"🔓 Tokens unlocked na Polygon!")
            print(f"📝 Tx Hash: {tx_hash.hex()}")
            
            return tx_hash.hex()
            
        except Exception as e:
            print(f"❌ Erro no unlock: {e}")
            raise e

# Função auxiliar para teste rápido
def quick_test_polygon():
    """Teste rápido da Polygon bridge"""
    try:
        bridge = RealPolygonBridge()
        if bridge.poly_w3 and bridge.account:
            print("✅ Polygon Bridge inicializada com sucesso!")
            
            # Testar saldo
            balance = bridge.poly_w3.eth.get_balance(bridge.account.address)
            balance_matic = bridge.poly_w3.from_wei(balance, 'ether')
            print(f"💰 Saldo Polygon: {balance_matic} MATIC")
            
            return {
                "success": True,
                "address": bridge.account.address,
                "balance_matic": float(balance_matic),
                "connected": bridge.poly_w3.is_connected()
            }
        else:
            return {"success": False, "error": "Polygon não conectado"}
        
    except Exception as e:
        print(f"❌ Erro no teste rápido Polygon: {e}")
        return {"success": False, "error": str(e)}

if __name__ == "__main__":
    # Teste rápido quando executado diretamente
    result = quick_test_polygon()
    print("Resultado do teste Polygon:", result)