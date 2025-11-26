"""
👛 Gerador de Wallets para Allianza Testnet
Cria wallets e endereços para usuários testarem
"""

from typing import Dict, Tuple
from testnet_config import is_valid_testnet_address, ADDRESS_PREFIX
from cryptography.hazmat.primitives import serialization

class TestnetWalletGenerator:
    def __init__(self, blockchain_instance):
        self.blockchain = blockchain_instance
    
    def generate_wallet(self) -> Dict:
        """Gera uma nova wallet para a testnet"""
        try:
            # Usar o método create_wallet do blockchain
            if hasattr(self.blockchain, 'create_wallet'):
                address, private_key = self.blockchain.create_wallet()
                
                # Serializar a chave privada para string PEM (JSON serializable)
                private_key_pem = private_key.private_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PrivateFormat.PKCS8,
                    encryption_algorithm=serialization.NoEncryption()
                ).decode('utf-8')
                
                return {
                    "success": True,
                    "address": address,
                    "private_key": private_key_pem,  # ⚠️ Apenas para testnet!
                    "message": "⚠️ ATENÇÃO: Esta é uma testnet. NUNCA use esta chave privada na mainnet!",
                    "instructions": [
                        "1. Copie o endereço acima",
                        "2. Use no faucet para obter tokens",
                        "3. Guarde a chave privada com segurança (apenas para testes)",
                        "4. NUNCA compartilhe sua chave privada"
                    ]
                }
            else:
                return {
                    "success": False,
                    "error": "Método create_wallet não disponível no blockchain"
                }
        except Exception as e:
            return {
                "success": False,
                "error": f"Erro ao gerar wallet: {str(e)}"
            }
    
    def validate_address(self, address: str) -> Dict:
        """Valida um endereço da testnet"""
        is_valid = is_valid_testnet_address(address)
        
        return {
            "valid": is_valid,
            "address": address,
            "message": "Endereço válido" if is_valid else "Endereço inválido. Deve começar com ALZ1 e ter 42 caracteres."
        }
