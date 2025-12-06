#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
✅ INPUT VALIDATOR - ALLIANZA BLOCKCHAIN
Validação rigorosa de inputs com sanitização
"""

import re
import hashlib
from typing import Any, Dict, Optional, List, Tuple
from web3 import Web3

class InputValidator:
    """
    Validador de Inputs Rigoroso
    
    Valida:
    - Endereços blockchain (EVM, Bitcoin, Solana)
    - Valores numéricos
    - Strings e formatos
    - Proteção contra injection
    """
    
    def __init__(self):
        # Padrões de validação
        self.patterns = {
            "evm_address": re.compile(r"^0x[a-fA-F0-9]{40}$"),
            "bitcoin_address": re.compile(r"^[13mn][a-km-zA-HJ-NP-Z1-9]{25,34}$|^bc1[a-z0-9]{39,59}$|^tb1[a-z0-9]{39,59}$"),
            "solana_address": re.compile(r"^[1-9A-HJ-NP-Za-km-z]{32,44}$"),
            "tx_hash": re.compile(r"^0x[a-fA-F0-9]{64}$"),
            "hex_string": re.compile(r"^0x[a-fA-F0-9]+$"),
            "private_key": re.compile(r"^0x[a-fA-F0-9]{64}$|^[a-fA-F0-9]{64}$")
        }
        
        print("✅ Input Validator: Inicializado!")
    
    def validate_address(
        self,
        address: str,
        chain: str = "evm"
    ) -> Tuple[bool, Optional[str]]:
        """
        Validar endereço blockchain
        
        Args:
            address: Endereço a validar
            chain: Tipo de chain (evm, bitcoin, solana)
        
        Returns:
            (is_valid, error_message)
        """
        if not address or not isinstance(address, str):
            return False, "Endereço inválido: deve ser string não vazia"
        
        address = address.strip()
        
        # Sanitizar (remover caracteres perigosos)
        if not self._is_safe_string(address):
            return False, "Endereço contém caracteres inválidos"
        
        # Validar formato baseado na chain
        if chain.lower() == "evm":
            if not self.patterns["evm_address"].match(address):
                return False, "Endereço EVM inválido: deve ser 0x seguido de 40 hex chars"
            
            # Validar checksum
            try:
                checksum_address = Web3.to_checksum_address(address)
                if checksum_address != address:
                    return False, f"Endereço com checksum incorreto. Use: {checksum_address}"
            except:
                return False, "Endereço EVM inválido"
        
        elif chain.lower() == "bitcoin":
            if not self.patterns["bitcoin_address"].match(address):
                return False, "Endereço Bitcoin inválido"
        
        elif chain.lower() == "solana":
            if not self.patterns["solana_address"].match(address):
                return False, "Endereço Solana inválido"
        
        else:
            return False, f"Chain não suportada: {chain}"
        
        return True, None
    
    def validate_amount(
        self,
        amount: Any,
        min_value: float = 0.0,
        max_value: Optional[float] = None,
        decimals: int = 18
    ) -> Tuple[bool, Optional[str]]:
        """
        Validar valor numérico
        
        Args:
            amount: Valor a validar
            min_value: Valor mínimo
            max_value: Valor máximo (None = sem limite)
            decimals: Casas decimais permitidas
        
        Returns:
            (is_valid, error_message)
        """
        # Converter para float
        try:
            amount_float = float(amount)
        except (ValueError, TypeError):
            return False, f"Valor inválido: deve ser numérico"
        
        # Verificar NaN e Infinity
        if not (amount_float == amount_float):  # NaN check
            return False, "Valor não pode ser NaN"
        
        if abs(amount_float) == float('inf'):
            return False, "Valor não pode ser infinito"
        
        # Verificar range
        if amount_float < min_value:
            return False, f"Valor muito pequeno: mínimo {min_value}"
        
        if max_value is not None and amount_float > max_value:
            return False, f"Valor muito grande: máximo {max_value}"
        
        # Verificar casas decimais
        if decimals > 0:
            decimal_places = len(str(amount_float).split('.')[-1]) if '.' in str(amount_float) else 0
            if decimal_places > decimals:
                return False, f"Muitas casas decimais: máximo {decimals}"
        
        return True, None
    
    def validate_tx_hash(self, tx_hash: str) -> Tuple[bool, Optional[str]]:
        """Validar hash de transação"""
        if not tx_hash or not isinstance(tx_hash, str):
            return False, "Hash de transação inválido"
        
        tx_hash = tx_hash.strip()
        
        if not self.patterns["tx_hash"].match(tx_hash):
            return False, "Hash de transação inválido: deve ser 0x seguido de 64 hex chars"
        
        return True, None
    
    def validate_private_key(
        self,
        private_key: str,
        chain: str = "evm"
    ) -> Tuple[bool, Optional[str]]:
        """
        Validar chave privada (sem expor valor real)
        
        Args:
            private_key: Chave privada
            chain: Tipo de chain
        
        Returns:
            (is_valid, error_message)
        """
        if not private_key or not isinstance(private_key, str):
            return False, "Chave privada inválida"
        
        private_key = private_key.strip()
        
        # Remover 0x se presente
        if private_key.startswith("0x"):
            private_key = private_key[2:]
        
        # Validar formato
        if not self.patterns["private_key"].match(f"0x{private_key}"):
            return False, "Chave privada inválida: deve ser 64 hex chars"
        
        # Validar comprimento
        if len(private_key) != 64:
            return False, "Chave privada deve ter 64 caracteres hexadecimais"
        
        return True, None
    
    def validate_string(
        self,
        value: str,
        min_length: int = 0,
        max_length: Optional[int] = None,
        allowed_chars: Optional[str] = None,
        sanitize: bool = True
    ) -> Tuple[bool, Optional[str], Optional[str]]:
        """
        Validar e sanitizar string
        
        Args:
            value: String a validar
            min_length: Comprimento mínimo
            max_length: Comprimento máximo
            allowed_chars: Caracteres permitidos (regex)
            sanitize: Se True, retornar versão sanitizada
        
        Returns:
            (is_valid, error_message, sanitized_value)
        """
        if not isinstance(value, str):
            return False, "Valor deve ser string", None
        
        # Sanitizar
        sanitized = value.strip()
        
        if sanitize:
            # Remover caracteres perigosos
            sanitized = re.sub(r'[<>"\']', '', sanitized)
            sanitized = re.sub(r'[^\w\s\-_.,!?@#$%&*()+=]', '', sanitized)
        
        # Validar comprimento
        if len(sanitized) < min_length:
            return False, f"String muito curta: mínimo {min_length} caracteres", None
        
        if max_length is not None and len(sanitized) > max_length:
            return False, f"String muito longa: máximo {max_length} caracteres", None
        
        # Validar caracteres permitidos
        if allowed_chars:
            pattern = re.compile(allowed_chars)
            if not pattern.match(sanitized):
                return False, f"String contém caracteres não permitidos", None
        
        return True, None, sanitized if sanitize else value
    
    def _is_safe_string(self, value: str) -> bool:
        """Verificar se string é segura (sem injection)"""
        # Verificar caracteres perigosos
        dangerous_chars = ['<', '>', '"', "'", ';', '--', '/*', '*/', 'xp_', 'exec', 'union', 'select']
        value_lower = value.lower()
        
        for char in dangerous_chars:
            if char in value_lower:
                return False
        
        return True
    
    def validate_transaction_data(self, data: Dict) -> Tuple[bool, Optional[str], Optional[Dict]]:
        """
        Validar dados completos de transação
        
        Args:
            data: Dados da transação
        
        Returns:
            (is_valid, error_message, sanitized_data)
        """
        sanitized = {}
        
        # Validar campos obrigatórios
        required_fields = ["from_address", "to_address", "amount"]
        for field in required_fields:
            if field not in data:
                return False, f"Campo obrigatório ausente: {field}", None
        
        # Validar endereços
        from_chain = data.get("from_chain", "evm")
        to_chain = data.get("to_chain", "evm")
        
        is_valid, error = self.validate_address(data["from_address"], from_chain)
        if not is_valid:
            return False, f"from_address inválido: {error}", None
        sanitized["from_address"] = data["from_address"].strip()
        
        is_valid, error = self.validate_address(data["to_address"], to_chain)
        if not is_valid:
            return False, f"to_address inválido: {error}", None
        sanitized["to_address"] = data["to_address"].strip()
        
        # Validar amount
        is_valid, error = self.validate_amount(
            data["amount"],
            min_value=0.0,
            decimals=18
        )
        if not is_valid:
            return False, f"amount inválido: {error}", None
        sanitized["amount"] = float(data["amount"])
        
        # Validar campos opcionais
        if "tx_hash" in data:
            is_valid, error = self.validate_tx_hash(data["tx_hash"])
            if not is_valid:
                return False, f"tx_hash inválido: {error}", None
            sanitized["tx_hash"] = data["tx_hash"].strip()
        
        # Copiar outros campos (sanitizados)
        for key, value in data.items():
            if key not in sanitized:
                if isinstance(value, str):
                    is_valid, error, sanitized_value = self.validate_string(value, sanitize=True)
                    if is_valid:
                        sanitized[key] = sanitized_value
                    else:
                        sanitized[key] = value  # Manter original se sanitização falhar
                else:
                    sanitized[key] = value
        
        return True, None, sanitized

# Instância global
_global_input_validator = None

def get_input_validator() -> InputValidator:
    """Obter instância global do input validator"""
    global _global_input_validator
    if _global_input_validator is None:
        _global_input_validator = InputValidator()
    return _global_input_validator

if __name__ == '__main__':
    print("="*70)
    print("✅ INPUT VALIDATOR - TESTE")
    print("="*70)
    
    validator = InputValidator()
    
    # Teste de endereço
    print("\n📝 Teste 1: Validar endereço EVM")
    is_valid, error = validator.validate_address("0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb", "evm")
    print(f"   {'✅' if is_valid else '❌'} {error or 'Válido'}")
    
    # Teste de amount
    print("\n📝 Teste 2: Validar amount")
    is_valid, error = validator.validate_amount(100.5, min_value=0.0, decimals=18)
    print(f"   {'✅' if is_valid else '❌'} {error or 'Válido'}")







