#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gerenciador de Configuração Centralizado
Validação de configuração e suporte a múltiplos ambientes
"""

import os
from typing import Dict, Optional, Any
from dotenv import load_dotenv
import json

class ConfigManager:
    """Gerenciador centralizado de configuração"""
    
    def __init__(self, env_file: str = ".env"):
        self.env_file = env_file
        self.config = {}
        self.required_vars = []
        self.optional_vars = []
        
        # Carregar variáveis de ambiente
        load_dotenv(env_file)
        
        # Carregar configuração padrão
        self._load_default_config()
    
    def _load_default_config(self):
        """Carrega configuração padrão"""
        self.config = {
            # Ambiente
            "ENV": os.getenv("ENV", "development"),
            "DEBUG": os.getenv("DEBUG", "False").lower() == "true",
            
            # Blockchain
            "POLYGON_RPC": os.getenv("POLYGON_RPC", "https://rpc-amoy.polygon.technology/"),
            "ETHEREUM_RPC": os.getenv("ETHEREUM_RPC", "https://sepolia.infura.io/v3/"),
            "BSC_RPC": os.getenv("BSC_RPC", "https://data-seed-prebsc-1-s1.binance.org:8545/"),
            "BASE_RPC": os.getenv("BASE_RPC", "https://sepolia.base.org"),
            
            # APIs
            "BLOCKCYPHER_API_TOKEN": os.getenv("BLOCKCYPHER_API_TOKEN", ""),
            "INFURA_PROJECT_ID": os.getenv("INFURA_PROJECT_ID", ""),
            
            # Segurança
            "RATE_LIMIT_ENABLED": os.getenv("RATE_LIMIT_ENABLED", "True").lower() == "true",
            "RATE_LIMIT_PER_MINUTE": int(os.getenv("RATE_LIMIT_PER_MINUTE", "60")),
            
            # Performance
            "CACHE_ENABLED": os.getenv("CACHE_ENABLED", "False").lower() == "true",
            "CACHE_TTL": int(os.getenv("CACHE_TTL", "300")),
            
            # Logging
            "LOG_LEVEL": os.getenv("LOG_LEVEL", "INFO"),
            "LOG_FILE": os.getenv("LOG_FILE", "allianza_blockchain.log"),
            "STRUCTURED_LOGGING": os.getenv("STRUCTURED_LOGGING", "True").lower() == "true",
        }
    
    def get(self, key: str, default: Any = None) -> Any:
        """Obtém valor de configuração"""
        return self.config.get(key, os.getenv(key, default))
    
    def set(self, key: str, value: Any):
        """Define valor de configuração"""
        self.config[key] = value
        os.environ[key] = str(value)
    
    def require(self, *keys: str):
        """Marca variáveis como obrigatórias"""
        self.required_vars.extend(keys)
    
    def validate(self) -> tuple[bool, list[str]]:
        """
        Valida configuração
        
        Returns:
            (is_valid, errors)
        """
        errors = []
        
        # Verificar variáveis obrigatórias
        for key in self.required_vars:
            if key not in self.config or not self.config[key]:
                errors.append(f"Variável obrigatória não configurada: {key}")
        
        # Validações específicas
        if self.config.get("ENV") not in ["development", "staging", "production"]:
            errors.append("ENV deve ser: development, staging ou production")
        
        if self.config.get("RATE_LIMIT_PER_MINUTE", 0) <= 0:
            errors.append("RATE_LIMIT_PER_MINUTE deve ser maior que 0")
        
        return len(errors) == 0, errors
    
    def get_for_environment(self, env: Optional[str] = None) -> Dict:
        """Retorna configuração para ambiente específico"""
        env = env or self.config.get("ENV", "development")
        
        base_config = self.config.copy()
        
        # Ajustes por ambiente
        if env == "production":
            base_config["DEBUG"] = False
            base_config["LOG_LEVEL"] = "WARNING"
            base_config["RATE_LIMIT_ENABLED"] = True
        elif env == "staging":
            base_config["DEBUG"] = False
            base_config["LOG_LEVEL"] = "INFO"
        else:  # development
            base_config["DEBUG"] = True
            base_config["LOG_LEVEL"] = "DEBUG"
        
        return base_config
    
    def save_to_file(self, filepath: str):
        """Salva configuração em arquivo JSON"""
        with open(filepath, 'w') as f:
            json.dump(self.config, f, indent=2)
    
    def load_from_file(self, filepath: str):
        """Carrega configuração de arquivo JSON"""
        with open(filepath, 'r') as f:
            self.config.update(json.load(f))

# Instância global
config = ConfigManager()









