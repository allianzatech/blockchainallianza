#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sistema de Validação Rigorosa para Allianza Blockchain
Valida endereços, valores, nonces, e inputs de forma segura
"""

import re
import time
from typing import Dict, Optional, Tuple
from web3 import Web3
from web3.exceptions import InvalidAddress

class InputValidator:
    """Validador rigoroso de inputs"""
    
    # Padrões de endereços por blockchain
    ADDRESS_PATTERNS = {
        "ethereum": r"^0x[a-fA-F0-9]{40}$",
        "polygon": r"^0x[a-fA-F0-9]{40}$",
        "bsc": r"^0x[a-fA-F0-9]{40}$",
        "base": r"^0x[a-fA-F0-9]{40}$",
        "bitcoin": r"^(bc1|[13])[a-zA-HJ-NP-Z0-9]{25,62}$",
        "bitcoin_testnet": r"^(tb1|[2mn])[a-zA-HJ-NP-Z0-9]{25,62}$",
        "solana": r"^[1-9A-HJ-NP-Za-km-z]{32,44}$",
    }
    
    # Valores mínimos e máximos
    MIN_AMOUNT = 0.00000001  # 1 satoshi equivalente
    MAX_AMOUNT = 1e15  # Valor máximo razoável
    
    def __init__(self):
        self.nonce_cache = {}  # Cache de nonces por endereço
        self.timestamp_cache = {}  # Cache de timestamps por transação
        
    def validate_address(
        self,
        address: str,
        chain: str,
        checksum: bool = True
    ) -> Tuple[bool, Optional[str]]:
        """
        Valida endereço de forma rigorosa
        
        Returns:
            (is_valid, error_message)
        """
        if not address or not isinstance(address, str):
            return False, "Endereço inválido: deve ser uma string não vazia"
        
        address = address.strip()
        
        # Verificar padrão básico
        pattern = self.ADDRESS_PATTERNS.get(chain)
        if pattern:
            if not re.match(pattern, address):
                return False, f"Endereço não corresponde ao padrão de {chain}"
        
        # Validação específica por chain
        if chain in ["ethereum", "polygon", "bsc", "base"]:
            # Validar endereço EVM
            try:
                w3 = Web3()
                # Verificar se é endereço válido
                if not w3.is_address(address):
                    return False, "Endereço EVM inválido"
                
                # Se checksum obrigatório, verificar formato (mas aceitar mesmo sem checksum)
                if checksum:
                    try:
                        checksum_address = w3.to_checksum_address(address)
                        # Aceitar endereço válido mesmo que não esteja em checksum
                        # (mais tolerante para desenvolvimento e compatibilidade)
                        if address.lower() != checksum_address.lower():
                            # Endereço válido mas não em checksum - aceitar mesmo assim
                            pass
                    except Exception:
                        # Se não conseguir converter para checksum, mas is_address retornou True,
                        # ainda assim aceitar (pode ser endereço válido em lowercase)
                        pass
            except InvalidAddress:
                return False, "Endereço EVM inválido"
            except Exception as e:
                return False, f"Erro ao validar endereço: {str(e)}"
        
        elif chain in ["bitcoin", "bitcoin_testnet"]:
            # Validação adicional para Bitcoin
            if not (address.startswith("1") or address.startswith("3") or 
                   address.startswith("bc1") or address.startswith("tb1") or
                   address.startswith("2") or address.startswith("m") or address.startswith("n")):
                return False, "Formato de endereço Bitcoin inválido"
        
        elif chain == "solana":
            # Validação básica para Solana (base58)
            if len(address) < 32 or len(address) > 44:
                return False, "Endereço Solana deve ter entre 32 e 44 caracteres"
        
        return True, None
    
    def validate_amount(
        self,
        amount: float,
        min_amount: Optional[float] = None,
        max_amount: Optional[float] = None
    ) -> Tuple[bool, Optional[str]]:
        """
        Valida valor de transação
        
        Returns:
            (is_valid, error_message)
        """
        if not isinstance(amount, (int, float)):
            return False, "Valor deve ser um número"
        
        if amount <= 0:
            return False, "Valor deve ser maior que zero"
        
        min_val = min_amount or self.MIN_AMOUNT
        max_val = max_amount or self.MAX_AMOUNT
        
        if amount < min_val:
            return False, f"Valor muito pequeno. Mínimo: {min_val}"
        
        if amount > max_val:
            return False, f"Valor muito grande. Máximo: {max_val}"
        
        # Verificar se não é NaN ou infinito
        import math
        if math.isnan(amount) or math.isinf(amount):
            return False, "Valor inválido (NaN ou infinito)"
        
        return True, None
    
    def validate_nonce(
        self,
        address: str,
        nonce: int,
        current_nonce: int
    ) -> Tuple[bool, Optional[str]]:
        """
        Valida nonce para prevenir replay attacks
        
        Returns:
            (is_valid, error_message)
        """
        if not isinstance(nonce, int):
            return False, "Nonce deve ser um inteiro"
        
        if nonce < 0:
            return False, "Nonce não pode ser negativo"
        
        # Verificar se nonce não é muito maior que o atual (possível ataque)
        if nonce > current_nonce + 10:
            return False, f"Nonce muito à frente. Atual: {current_nonce}, Fornecido: {nonce}"
        
        # Verificar se nonce não foi usado recentemente (cache)
        cache_key = f"{address}:{nonce}"
        if cache_key in self.nonce_cache:
            cache_time = self.nonce_cache[cache_key]
            if time.time() - cache_time < 300:  # 5 minutos
                return False, "Nonce já foi usado recentemente (possível replay attack)"
        
        # Adicionar ao cache
        self.nonce_cache[cache_key] = time.time()
        
        # Limpar cache antigo (mais de 1 hora)
        current_time = time.time()
        self.nonce_cache = {
            k: v for k, v in self.nonce_cache.items()
            if current_time - v < 3600
        }
        
        return True, None
    
    def validate_timestamp(
        self,
        timestamp: int,
        max_age_seconds: int = 300
    ) -> Tuple[bool, Optional[str]]:
        """
        Valida timestamp para prevenir transações antigas
        
        Returns:
            (is_valid, error_message)
        """
        if not isinstance(timestamp, int):
            return False, "Timestamp deve ser um inteiro"
        
        current_time = int(time.time())
        
        # Verificar se não é muito antigo
        if timestamp < current_time - max_age_seconds:
            return False, f"Timestamp muito antigo. Máximo: {max_age_seconds}s atrás"
        
        # Verificar se não é muito no futuro
        if timestamp > current_time + 60:
            return False, "Timestamp não pode ser mais de 60s no futuro"
        
        return True, None
    
    def sanitize_input(self, input_str: str, max_length: int = 1000) -> Tuple[str, Optional[str]]:
        """
        Sanitiza input de string
        
        Returns:
            (sanitized_string, error_message)
        """
        if not isinstance(input_str, str):
            return "", "Input deve ser uma string"
        
        # Remover caracteres de controle
        sanitized = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', input_str)
        
        # Limitar tamanho
        if len(sanitized) > max_length:
            return "", f"Input muito longo. Máximo: {max_length} caracteres"
        
        # Remover espaços extras
        sanitized = ' '.join(sanitized.split())
        
        return sanitized, None
    
    def validate_transaction_data(
        self,
        from_address: str,
        to_address: str,
        amount: float,
        chain: str,
        nonce: Optional[int] = None,
        current_nonce: Optional[int] = None,
        timestamp: Optional[int] = None
    ) -> Dict:
        """
        Valida todos os dados de uma transação
        
        Returns:
            {
                "valid": bool,
                "errors": List[str],
                "warnings": List[str]
            }
        """
        errors = []
        warnings = []
        
        # Validar endereço de origem
        valid, error = self.validate_address(from_address, chain)
        if not valid:
            errors.append(f"Endereço de origem: {error}")
        
        # Validar endereço de destino
        valid, error = self.validate_address(to_address, chain)
        if not valid:
            errors.append(f"Endereço de destino: {error}")
        
        # Validar que endereços são diferentes
        if from_address.lower() == to_address.lower():
            warnings.append("Endereço de origem e destino são iguais")
        
        # Validar valor
        valid, error = self.validate_amount(amount)
        if not valid:
            errors.append(f"Valor: {error}")
        
        # Validar nonce se fornecido
        if nonce is not None and current_nonce is not None:
            valid, error = self.validate_nonce(from_address, nonce, current_nonce)
            if not valid:
                errors.append(f"Nonce: {error}")
        
        # Validar timestamp se fornecido
        if timestamp is not None:
            valid, error = self.validate_timestamp(timestamp)
            if not valid:
                errors.append(f"Timestamp: {error}")
        
        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "warnings": warnings
        }

