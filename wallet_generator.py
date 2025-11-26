# wallet_generator_fixed.py - VERSÃO CORRIGIDA
import json
import secrets
from web3 import Web3
import base58

class UniversalWalletGenerator:
    def __init__(self):
        self.wallets = {}
    
    def generate_ethereum_wallet(self):
        """Gera wallet Ethereum com private key"""
        w3 = Web3()
        account = w3.eth.account.create(secrets.token_hex(32))
        
        return {
            "chain": "ethereum",
            "address": account.address,
            "private_key": account.key.hex()
        }
    
    def generate_solana_wallet(self):
        """Gera wallet Solana"""
        private_key = secrets.token_hex(32)
        address = base58.b58encode(bytes.fromhex(private_key)).decode()[:44]
        
        return {
            "chain": "solana", 
            "address": address,
            "private_key": private_key
        }
    
    def generate_bitcoin_wallet_simulated(self):
        """Gera wallet Bitcoin simulada"""
        private_key = secrets.token_hex(32)
        address = f"1{secrets.token_hex(20)}"  # Simulação de address Bitcoin
        
        return {
            "chain": "bitcoin",
            "address": address,
            "private_key": private_key,
            "note": "Address Bitcoin simulado"
        }
    
    def generate_test_wallets(self):
        """Gera wallets de teste"""
        print("🔐 GERANDO WALLETS DE TESTE")
        print("=" * 50)
        
        # Ethereum
        eth_wallet = self.generate_ethereum_wallet()
        self.wallets['ethereum'] = eth_wallet
        print(f"⬨ Ethereum: {eth_wallet['address']}")
        print(f"   Private Key: {eth_wallet['private_key']}")
        
        # Solana 
        sol_wallet = self.generate_solana_wallet()
        self.wallets['solana'] = sol_wallet
        print(f"⚡ Solana: {sol_wallet['address']}")
        print(f"   Private Key: {sol_wallet['private_key']}")
        
        # Bitcoin
        btc_wallet = self.generate_bitcoin_wallet_simulated()
        self.wallets['bitcoin'] = btc_wallet
        print(f"₿ Bitcoin: {btc_wallet['address']}")
        print(f"   Private Key: {btc_wallet['private_key']}")
        
        print("=" * 50)
        print("🎯 VOCÊ JÁ TEM KEYS REAIS - Use as que recebeu!")
        
        return self.wallets

if __name__ == "__main__":
    generator = UniversalWalletGenerator()
    wallets = generator.generate_test_wallets()