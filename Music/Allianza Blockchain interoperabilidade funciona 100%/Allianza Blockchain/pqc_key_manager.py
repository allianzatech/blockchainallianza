#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔐 GERENCIADOR DE CHAVES PQC
Gera e gerencia chaves PQC reais (ML-DSA, SPHINCS+) e assinaturas
"""

import os
import json
import base64
from typing import Dict, Optional, Tuple, Any
from datetime import datetime

class PQCKeyManager:
    """
    Gerenciador de chaves PQC para assinaturas reais
    
    Tenta usar bibliotecas reais (liboqs, cryptography) se disponíveis,
    caso contrário usa implementação mock mas documentada
    """
    
    def __init__(self):
        self.keys_dir = "pqc_keys"
        os.makedirs(self.keys_dir, exist_ok=True)
        self._check_libraries()
    
    def _check_libraries(self):
        """Verificar quais bibliotecas PQC estão disponíveis"""
        self.has_liboqs = False
        self.has_cryptography = False
        
        # Tentar importar liboqs (Open Quantum Safe)
        try:
            import oqs
            self.has_liboqs = True
            self.oqs = oqs
            print("✅ Open Quantum Safe (liboqs) disponível - usando assinaturas PQC reais")
        except ImportError:
            print("⚠️  Open Quantum Safe (liboqs) não disponível - usando modo mock documentado")
        
        # Tentar importar cryptography (pode ter suporte PQC)
        try:
            from cryptography.hazmat.primitives.asymmetric import padding
            from cryptography.hazmat.primitives import hashes
            self.has_cryptography = True
        except ImportError:
            pass
    
    def generate_ml_dsa_keypair(self, key_id: str) -> Dict[str, Any]:
        """
        Gerar par de chaves ML-DSA-128 (Dilithium2)
        
        Returns:
            {
                "keypair_id": str,
                "public_key": str (base64),
                "public_key_pem": str,
                "algorithm": "ML-DSA-128",
                "standard": "FIPS 204",
                "security_level": 3
            }
        """
        if self.has_liboqs:
            try:
                # Usar liboqs real
                sigalg = "Dilithium2"  # ML-DSA-128
                with self.oqs.Signature(sigalg) as signer:
                    public_key = signer.generate_keypair()
                    private_key = signer.export_secret_key()
                    
                # Salvar chaves
                pub_key_path = os.path.join(self.keys_dir, f"{key_id}_ml_dsa_public_key.pem")
                priv_key_path = os.path.join(self.keys_dir, f"{key_id}_ml_dsa_private_key.pem")
                
                # Converter para formato PEM (base64)
                pub_key_b64 = base64.b64encode(public_key).decode('utf-8')
                priv_key_b64 = base64.b64encode(private_key).decode('utf-8')
                
                # Salvar em formato PEM
                with open(pub_key_path, 'w') as f:
                    f.write(f"-----BEGIN ML-DSA PUBLIC KEY-----\n")
                    f.write(f"{pub_key_b64}\n")
                    f.write(f"-----END ML-DSA PUBLIC KEY-----\n")
                
                with open(priv_key_path, 'w') as f:
                    f.write(f"-----BEGIN ML-DSA PRIVATE KEY-----\n")
                    f.write(f"{priv_key_b64}\n")
                    f.write(f"-----END ML-DSA PRIVATE KEY-----\n")
                
                return {
                    "keypair_id": key_id,
                    "public_key": pub_key_b64,
                    "public_key_pem": pub_key_path,
                    "private_key_pem": priv_key_path,
                    "algorithm": "ML-DSA-128",
                    "standard": "FIPS 204",
                    "security_level": 3,
                    "implementation": "Open Quantum Safe (liboqs)",
                    "real": True
                }
            except Exception as e:
                print(f"⚠️  Erro ao gerar chave ML-DSA com liboqs: {e}")
                return self._generate_mock_keypair(key_id, "ML-DSA-128")
        else:
            return self._generate_mock_keypair(key_id, "ML-DSA-128")
    
    def sign_ml_dsa(self, key_id: str, data: bytes) -> Dict[str, Any]:
        """
        Assinar dados com ML-DSA-128
        
        Args:
            key_id: ID do keypair
            data: Dados para assinar (hash SHA-256)
        
        Returns:
            {
                "signature": str (base64),
                "signature_bin": str (caminho do arquivo .bin),
                "algorithm": "ML-DSA-128",
                "signed_data_hash": str (hex)
            }
        """
        if self.has_liboqs:
            try:
                # Tentar usar signer já criado
                if hasattr(self, '_signers') and key_id in self._signers:
                    signer = self._signers[key_id]
                    signature = signer.sign(data)
                else:
                    # Carregar chave privada
                    priv_key_path = os.path.join(self.keys_dir, f"{key_id}_ml_dsa_private_key.pem")
                    if not os.path.exists(priv_key_path):
                        raise FileNotFoundError(f"Chave privada não encontrada: {priv_key_path}")
                    
                    with open(priv_key_path, 'r') as f:
                        lines = f.readlines()
                        priv_key_b64 = ''.join([l.strip() for l in lines if '-----' not in l])
                        private_key = base64.b64decode(priv_key_b64)
                    
                    # Assinar - liboqs Signature aceita secret_key no construtor
                    sigalg = "Dilithium2"
                    # Criar signer com secret_key (private_key)
                    signer = self.oqs.Signature(sigalg, private_key)
                    signature = signer.sign(data)
                    
                    # Armazenar signer para reutilização
                    if not hasattr(self, '_signers'):
                        self._signers = {}
                    self._signers[key_id] = self.oqs.Signature(sigalg, private_key)
                
                # Salvar assinatura binária
                sig_bin_path = os.path.join(self.keys_dir, f"{key_id}_ml_dsa_signature.bin")
                with open(sig_bin_path, 'wb') as f:
                    f.write(signature)
                
                sig_b64 = base64.b64encode(signature).decode('utf-8')
                
                # Obter chave pública PEM
                pub_key_path = os.path.join(self.keys_dir, f"{key_id}_ml_dsa_public_key.pem")
                
                return {
                    "signature": sig_b64,
                    "signature_bin": sig_bin_path,
                    "algorithm": "ML-DSA-128",
                    "standard": "FIPS 204",
                    "signed_data_hash": data.hex() if isinstance(data, bytes) else data,
                    "public_key_pem": pub_key_path if os.path.exists(pub_key_path) else None,
                    "real": True,
                    "implementation": "Open Quantum Safe (liboqs)"
                }
            except Exception as e:
                print(f"⚠️  Erro ao assinar com ML-DSA (liboqs): {e}")
                import traceback
                traceback.print_exc()
                return self._sign_mock(key_id, data, "ML-DSA-128")
        else:
            return self._sign_mock(key_id, data, "ML-DSA-128")
    
    def verify_ml_dsa(self, public_key: str, data: bytes, signature: str) -> Dict[str, Any]:
        """Verificar assinatura ML-DSA"""
        if self.has_liboqs:
            try:
                pub_key_bytes = base64.b64decode(public_key)
                sig_bytes = base64.b64decode(signature)
                
                sigalg = "Dilithium2"
                # liboqs: verify(message, signature, public_key) - método estático ou de instância
                # Criar verifier sem secret_key
                verifier = self.oqs.Signature(sigalg)
                # liboqs verify() recebe: verify(message, signature, public_key)
                is_valid = verifier.verify(data, sig_bytes, pub_key_bytes)
                
                return {
                    "success": is_valid,
                    "algorithm": "ML-DSA-128",
                    "real": True
                }
            except Exception as e:
                import traceback
                print(f"⚠️  Erro ao verificar ML-DSA: {e}")
                traceback.print_exc()
                return {"success": False, "error": str(e), "real": False}
        else:
            return {"success": True, "note": "Mock verification", "real": False}
    
    def _generate_mock_keypair(self, key_id: str, algorithm: str) -> Dict[str, Any]:
        """Gerar keypair mock (documentado)"""
        import hashlib
        import secrets
        
        # Gerar chave mock determinística baseada no key_id
        seed = hashlib.sha256(f"{key_id}_{algorithm}".encode()).digest()
        pub_key = hashlib.sha256(seed).hexdigest()
        priv_key = hashlib.sha256(seed + b"private").hexdigest()
        
        pub_key_path = os.path.join(self.keys_dir, f"{key_id}_ml_dsa_public_key.pem")
        priv_key_path = os.path.join(self.keys_dir, f"{key_id}_ml_dsa_private_key.pem")
        
        # Salvar em formato PEM mock
        with open(pub_key_path, 'w') as f:
            f.write(f"-----BEGIN ML-DSA PUBLIC KEY (MOCK)-----\n")
            f.write(f"{pub_key}\n")
            f.write(f"-----END ML-DSA PUBLIC KEY (MOCK)-----\n")
            f.write(f"# NOTE: This is a MOCK key for demonstration.\n")
            f.write(f"# For real PQC signatures, install: pip install oqs-python\n")
        
        return {
            "keypair_id": key_id,
            "public_key": pub_key,
            "public_key_pem": pub_key_path,
            "private_key_pem": priv_key_path,
            "algorithm": algorithm,
            "standard": "FIPS 204",
            "security_level": 3,
            "implementation": "Mock (documented)",
            "real": False,
            "note": "Install 'oqs-python' for real PQC signatures"
        }
    
    def _sign_mock(self, key_id: str, data: bytes, algorithm: str) -> Dict[str, Any]:
        """Assinar mock (documentado)"""
        import hashlib
        
        # Assinatura mock determinística
        sig_data = hashlib.sha256(f"{key_id}_{data.hex() if isinstance(data, bytes) else data}".encode()).hexdigest()
        
        sig_bin_path = os.path.join(self.keys_dir, f"{key_id}_ml_dsa_signature.bin")
        with open(sig_bin_path, 'wb') as f:
            f.write(sig_data.encode())
        
        return {
            "signature": sig_data,
            "signature_bin": sig_bin_path,
            "algorithm": algorithm,
            "standard": "FIPS 204",
            "signed_data_hash": data.hex() if isinstance(data, bytes) else data,
            "real": False,
            "implementation": "Mock (documented)",
            "note": "Install 'oqs-python' for real PQC signatures"
        }

