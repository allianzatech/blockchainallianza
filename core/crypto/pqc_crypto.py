# pqc_crypto.py
import json
import hashlib
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.backends import default_backend
import base58

class PQCrypto:
    """CRIPTOGRAFIA PÓS-QUÂNTICA - IMPLEMENTAÇÃO DE EMERGÊNCIA"""
    
    @staticmethod
    def generate_keypair():
        """Gera par de chaves usando ECDSA (transição para ML-DSA)"""
        # Usando SECP256K1 para padronização com o core da blockchain
        private_key = ec.generate_private_key(ec.SECP256K1(), default_backend())
        public_key = private_key.public_key()
        return private_key, public_key

    @staticmethod
    def sign_transaction(private_key, transaction):
        """Assina transação usando ECDSA (transição para ML-DSA)"""
        message = json.dumps(transaction, sort_keys=True).encode()
        
        # Assinatura ECDSA (SECP256K1)
        signature = private_key.sign(
            message,
            ec.ECDSA(hashes.SHA256())
        )
        
        # Retorna apenas a assinatura ECDSA, removendo a simulação PQC
        return signature.hex()

    @staticmethod
    def verify_signature(public_key, transaction, signature):
        """Verifica assinatura ECDSA (transição para ML-DSA)"""
        try:
            message = json.dumps(transaction, sort_keys=True).encode()
            
            # Verificar assinatura ECDSA (SECP256K1)
            public_key.verify(
                bytes.fromhex(signature),
                message,
                ec.ECDSA(hashes.SHA256())
            )
            
            return True
            
        except Exception as e:
            # O erro mais comum é InvalidSignature, mas capturamos todos para robustez
            print(f"Erro verificação ECDSA: {e}")
            return False

    @staticmethod
    def generate_secure_hash(data):
        """Gera hash seguro (SHA-256) para endereços"""
        if isinstance(data, str):
            data = data.encode()
        
        # Padronizando para SHA-256 para consistência com o core
        return hashlib.sha256(data).hexdigest()

    @staticmethod
    def private_key_to_pem(private_key):
        """Converte chave privada para PEM"""
        return private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        ).decode()

    @staticmethod
    def public_key_to_pem(public_key):
        """Converte chave pública para PEM"""
        return public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ).decode()

    @staticmethod
    def pem_to_private_key(pem_data):
        """Converte PEM para chave privada"""
        return serialization.load_pem_private_key(
            pem_data.encode(), 
            password=None, 
            backend=default_backend()
        )

    @staticmethod
    def pem_to_public_key(pem_data):
        """Converte PEM para chave pública"""
        return serialization.load_pem_public_key(
            pem_data.encode(), 
            backend=default_backend()
        )