# bitcoin_clm.py
import hashlib
import base58
import bech32
import re

class BitcoinCLM:
    """CROSS-LOGIC MODULE PARA BITCOIN"""
    
    @staticmethod
    def validate_bitcoin_address(address):
        """Valida endereços Bitcoin (Legacy, SegWit, Native SegWit)"""
        if not address or not isinstance(address, str):
            return False
            
        address = address.strip()
        
        # Legacy (P2PKH) - começa com 1
        if address.startswith('1'):
            return BitcoinCLM._validate_base58_address(address)
        
        # SegWit (P2SH) - começa com 3  
        elif address.startswith('3'):
            return BitcoinCLM._validate_base58_address(address)
        
        # Native SegWit (Bech32) - começa com bc1
        elif address.startswith('bc1'):
            return BitcoinCLM._validate_bech32_address(address)
        
        # Testnet
        elif address.startswith('tb1') or address.startswith('2') or address.startswith('m') or address.startswith('n'):
            return True  # Aceitar testnet para desenvolvimento
        
        return False

    @staticmethod
    def _validate_base58_address(address):
        """Valida endereços Base58Check"""
        try:
            decoded = base58.b58decode_check(address)
            return len(decoded) == 21  # 1 byte version + 20 bytes hash
        except Exception:
            return False

    @staticmethod
    def _validate_bech32_address(address):
        """Valida endereços Bech32"""
        try:
            # Verificar formato básico
            if not re.match(r'^bc1[ac-hj-np-z02-9]+$', address.lower()):
                return False
                
            # Decodificar Bech32
            decoded = bech32.decode('bc', address)
            return decoded is not None and len(decoded[1]) in [20, 32]  # 20 bytes para P2WPKH, 32 para P2WSH
        except Exception:
            return False

    @staticmethod
    def create_bitcoin_metadata():
        """Retorna metadados padrão para token BTCa"""
        return {
            "bitcoin": {
                "name": "Bitcoin",
                "address_format": "Base58Check/Bech32",
                "vm_type": "UTXO",
                "signature_algo": "secp256k1",
                "script_types": ["P2PKH", "P2SH", "P2WPKH", "P2WSH"],
                "decimals": 8,
                "confirmation_blocks": 6,
                "network": "mainnet",
                "supports": ["multisig", "timelock", "hashlock"]
            }
        }

    @staticmethod
    def generate_bitcoin_compatible_address(public_key_bytes):
        """Gera endereço compatível com Bitcoin a partir de chave pública"""
        # SHA-256 da chave pública
        sha_hash = hashlib.sha256(public_key_bytes).digest()
        
        # RIPEMD-160 do SHA-256
        ripemd_hash = hashlib.new('ripemd160', sha_hash).digest()
        
        # Add version byte (0x00 for mainnet)
        versioned_hash = b'\x00' + ripemd_hash
        
        # Checksum
        checksum = hashlib.sha256(hashlib.sha256(versioned_hash).digest()).digest()[:4]
        
        # Base58Check encoding
        binary_addr = versioned_hash + checksum
        bitcoin_address = base58.b58encode(binary_addr).decode('utf-8')
        
        return bitcoin_address

    @staticmethod
    def simulate_bitcoin_transaction(from_address, to_address, amount):
        """Simula transação Bitcoin para testes"""
        return {
            "txid": f"simulated_btc_tx_{hashlib.sha256((from_address + to_address + str(amount)).encode()).hexdigest()[:16]}",
            "from": from_address,
            "to": to_address,
            "amount": amount,
            "fee": 0.0001,
            "confirmations": 1,
            "block_height": 999999,
            "timestamp": time.time(),
            "status": "confirmed"
        }