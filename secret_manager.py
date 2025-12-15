#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔐 SECRET MANAGER - ALLIANZA BLOCKCHAIN
Gerenciamento seguro de secrets (chaves privadas, API keys, etc.)
"""

import os
import json
import base64
import time
from typing import Optional, Dict, Any
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
import hashlib

# Tentar importar bibliotecas de key vault
try:
    import boto3
    AWS_AVAILABLE = True
except ImportError:
    AWS_AVAILABLE = False

try:
    import hvac
    VAULT_AVAILABLE = True
except ImportError:
    VAULT_AVAILABLE = False

class SecretManager:
    """
    Gerenciador de Secrets Seguro
    
    Suporta:
    - Criptografia local (Fernet)
    - AWS Secrets Manager (opcional)
    - HashiCorp Vault (opcional)
    - Rotação automática de chaves
    """
    
    def __init__(
        self,
        master_key: Optional[str] = None,
        use_aws: bool = False,
        use_vault: bool = False,
        vault_url: Optional[str] = None,
        vault_token: Optional[str] = None
    ):
        # Gerar ou usar master key
        if master_key is None:
            master_key = os.getenv("ALLIANZA_MASTER_KEY")
            if master_key is None:
                # Em produção, falhar explicitamente se não houver master key configurada
                if os.getenv("FLASK_ENV") == "production" or os.getenv("ALLIANZA_ENV") == "production":
                    raise RuntimeError(
                        "ALLIANZA_MASTER_KEY não configurada em produção. "
                        "Defina a variável de ambiente ALLIANZA_MASTER_KEY ou passe master_key explicitamente."
                    )
                # Em ambientes de desenvolvimento/teste, ainda podemos gerar automaticamente
                master_key = Fernet.generate_key().decode()
                print("⚠️  Master key gerada automaticamente (DEV) - configure ALLIANZA_MASTER_KEY em produção!")
        
        # Inicializar criptografia local
        self.fernet = Fernet(master_key.encode() if isinstance(master_key, str) else master_key)
        
        # AWS Secrets Manager
        self.use_aws = use_aws and AWS_AVAILABLE
        self.aws_client = None
        if self.use_aws:
            try:
                self.aws_client = boto3.client('secretsmanager')
                print("✅ AWS Secrets Manager: Conectado!")
            except Exception as e:
                print(f"⚠️  AWS Secrets Manager: Não disponível - {e}")
                self.use_aws = False
        
        # HashiCorp Vault
        self.use_vault = use_vault and VAULT_AVAILABLE
        self.vault_client = None
        if self.use_vault:
            try:
                self.vault_client = hvac.Client(url=vault_url, token=vault_token)
                if self.vault_client.is_authenticated():
                    print("✅ HashiCorp Vault: Conectado!")
                else:
                    print("⚠️  HashiCorp Vault: Não autenticado")
                    self.use_vault = False
            except Exception as e:
                print(f"⚠️  HashiCorp Vault: Não disponível - {e}")
                self.use_vault = False
        
        # Cache local de secrets descriptografados
        self.secret_cache = {}
        
        print("🔐 Secret Manager: Inicializado!")
        print(f"   Local encryption: ✅")
        print(f"   AWS Secrets Manager: {'✅' if self.use_aws else '❌'}")
        print(f"   HashiCorp Vault: {'✅' if self.use_vault else '❌'}")
    
    def store_secret(
        self,
        key: str,
        value: str,
        secret_type: str = "private_key",
        rotate: bool = False
    ) -> bool:
        """
        Armazenar secret de forma segura
        
        Args:
            key: Nome da chave
            value: Valor do secret
            secret_type: Tipo (private_key, api_key, password, etc.)
            rotate: Se True, rotacionar chave existente
        """
        try:
            # Criptografar valor
            encrypted_value = self.fernet.encrypt(value.encode())
            encrypted_b64 = base64.b64encode(encrypted_value).decode()
            
            # Armazenar metadata
            metadata = {
                "key": key,
                "type": secret_type,
                "encrypted": True,
                "created_at": str(time.time()),
                "rotated": rotate
            }
            
            # Tentar armazenar em AWS/Vault primeiro
            if self.use_aws:
                try:
                    secret_name = f"allianza/{key}"
                    if rotate:
                        # Rotacionar secret existente
                        self.aws_client.update_secret(
                            SecretId=secret_name,
                            SecretString=encrypted_b64
                        )
                    else:
                        # Criar novo secret
                        self.aws_client.create_secret(
                            Name=secret_name,
                            SecretString=encrypted_b64,
                            Description=f"Allianza {secret_type}"
                        )
                    return True
                except Exception as e:
                    print(f"⚠️  Erro ao armazenar em AWS: {e}")
            
            if self.use_vault:
                try:
                    vault_path = f"secret/data/allianza/{key}"
                    self.vault_client.secrets.kv.v2.create_or_update_secret(
                        path=vault_path,
                        secret={"value": encrypted_b64, "metadata": metadata}
                    )
                    return True
                except Exception as e:
                    print(f"⚠️  Erro ao armazenar em Vault: {e}")
            
            # Fallback: armazenar localmente (criptografado)
            secret_file = f"secrets/{key}.enc"
            os.makedirs("secrets", exist_ok=True)
            
            with open(secret_file, "w") as f:
                json.dump({
                    "encrypted_value": encrypted_b64,
                    "metadata": metadata
                }, f)
            
            return True
            
        except Exception as e:
            print(f"❌ Erro ao armazenar secret: {e}")
            return False
    
    def get_secret(self, key: str, use_cache: bool = True) -> Optional[str]:
        """
        Obter secret descriptografado
        
        Args:
            key: Nome da chave
            use_cache: Se True, usar cache local
        """
        # Verificar cache primeiro
        if use_cache and key in self.secret_cache:
            return self.secret_cache[key]
        
        try:
            encrypted_b64 = None
            
            # Tentar buscar de AWS/Vault primeiro
            if self.use_aws:
                try:
                    secret_name = f"allianza/{key}"
                    response = self.aws_client.get_secret_value(SecretId=secret_name)
                    encrypted_b64 = response['SecretString']
                except Exception as e:
                    if "ResourceNotFoundException" not in str(e):
                        print(f"⚠️  Erro ao buscar de AWS: {e}")
            
            if encrypted_b64 is None and self.use_vault:
                try:
                    vault_path = f"secret/data/allianza/{key}"
                    response = self.vault_client.secrets.kv.v2.read_secret_version(path=vault_path)
                    encrypted_b64 = response['data']['data']['value']
                except Exception as e:
                    if "not found" not in str(e).lower():
                        print(f"⚠️  Erro ao buscar de Vault: {e}")
            
            # Fallback: buscar localmente
            if encrypted_b64 is None:
                secret_file = f"secrets/{key}.enc"
                if os.path.exists(secret_file):
                    with open(secret_file, "r") as f:
                        data = json.load(f)
                        encrypted_b64 = data["encrypted_value"]
                else:
                    # Tentar variável de ambiente como fallback
                    env_key = key.upper().replace("-", "_")
                    env_value = os.getenv(env_key)
                    if env_value:
                        # Assumir que já está descriptografado (de .env)
                        self.secret_cache[key] = env_value
                        return env_value
                    return None
            
            # Descriptografar
            encrypted_value = base64.b64decode(encrypted_b64.encode())
            decrypted_value = self.fernet.decrypt(encrypted_value).decode()
            
            # Armazenar em cache
            if use_cache:
                self.secret_cache[key] = decrypted_value
            
            return decrypted_value
            
        except Exception as e:
            print(f"❌ Erro ao obter secret: {e}")
            return None
    
    def rotate_secret(self, key: str, new_value: Optional[str] = None) -> bool:
        """
        Rotacionar secret (gerar novo valor ou usar fornecido)
        
        Args:
            key: Nome da chave
            new_value: Novo valor (se None, gerar automaticamente)
        """
        # Se não fornecido, gerar novo valor (exemplo: nova chave privada)
        if new_value is None:
            # Gerar novo secret (exemplo)
            new_value = Fernet.generate_key().decode()
        
        # Armazenar com rotate=True
        return self.store_secret(key, new_value, rotate=True)
    
    def delete_secret(self, key: str) -> bool:
        """Deletar secret"""
        try:
            # Remover de AWS/Vault
            if self.use_aws:
                try:
                    secret_name = f"allianza/{key}"
                    self.aws_client.delete_secret(SecretId=secret_name, ForceDeleteWithoutRecovery=True)
                except:
                    pass
            
            if self.use_vault:
                try:
                    vault_path = f"secret/data/allianza/{key}"
                    self.vault_client.secrets.kv.v2.delete_metadata_and_all_versions(path=vault_path)
                except:
                    pass
            
            # Remover localmente
            secret_file = f"secrets/{key}.enc"
            if os.path.exists(secret_file):
                os.remove(secret_file)
            
            # Remover do cache
            if key in self.secret_cache:
                del self.secret_cache[key]
            
            return True
            
        except Exception as e:
            print(f"❌ Erro ao deletar secret: {e}")
            return False
    
    def clear_cache(self):
        """Limpar cache de secrets"""
        self.secret_cache.clear()

# Instância global
_global_secret_manager = None

def get_secret_manager() -> SecretManager:
    """Obter instância global do secret manager"""
    global _global_secret_manager
    if _global_secret_manager is None:
        _global_secret_manager = SecretManager()
    return _global_secret_manager

if __name__ == '__main__':
    import time
    
    print("="*70)
    print("🔐 SECRET MANAGER - TESTE")
    print("="*70)
    
    manager = SecretManager()
    
    # Teste básico
    print("\n📝 Teste 1: Armazenar e recuperar secret")
    manager.store_secret("test_key", "test_value_123")
    value = manager.get_secret("test_key")
    print(f"   ✅ Valor recuperado: {value}")
    
    # Teste de rotação
    print("\n📝 Teste 2: Rotacionar secret")
    manager.rotate_secret("test_key", "new_value_456")
    new_value = manager.get_secret("test_key")
    print(f"   ✅ Novo valor: {new_value}")

