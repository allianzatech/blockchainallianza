# native_credit_system.py
# 💎 SISTEMA DE CRÉDITOS NATIVOS
# INÉDITO: Créditos nativos (não sintéticos, não wrapped) baseados em provas criptográficas

import os
import json
import time
import hashlib
from typing import Dict, List, Optional
from datetime import datetime
from universal_signature_validator import universal_validator
from dotenv import load_dotenv

load_dotenv()

class NativeCredit:
    """
    CRÉDITO NATIVO - Representação real de tokens sem wrapped
    Baseado em prova criptográfica de transação original
    """
    
    def __init__(
        self,
        source_chain: str,
        tx_hash: str,
        amount: float,
        token_symbol: str,
        signature_proof: Dict,
        recipient_address: str
    ):
        self.source_chain = source_chain  # "bitcoin", "ethereum", etc.
        self.tx_hash = tx_hash  # Hash da transação original
        self.amount = amount  # Quantidade
        self.token_symbol = token_symbol  # "BTC", "ETH", "MATIC", etc.
        self.signature_proof = signature_proof  # Prova criptográfica
        self.recipient_address = recipient_address  # Endereço do destinatário
        self.is_native = True  # Não é wrapped!
        self.created_at = time.time()
        self.credit_id = self._generate_credit_id()
        self.status = "active"  # active, burned, withdrawn
    
    def _generate_credit_id(self) -> str:
        """Gera ID único para o crédito"""
        data = f"{self.source_chain}:{self.tx_hash}:{self.amount}:{time.time()}"
        return hashlib.sha256(data.encode()).hexdigest()[:16]
    
    def verify(self) -> Dict:
        """
        Verifica se o crédito é válido
        Valida assinatura original e confirma transação na blockchain
        """
        try:
            # Validar assinatura usando UniversalSignatureValidator
            validation_result = universal_validator.validate_universal(
                chain=self.source_chain,
                tx_hash=self.tx_hash,
                signature=self.signature_proof.get("signature"),
                public_key=self.signature_proof.get("public_key")
            )
            
            if not validation_result.get("valid"):
                return {
                    "valid": False,
                    "error": validation_result.get("error", "Validação falhou"),
                    "credit_id": self.credit_id
                }
            
            # Verificar se quantidade confere
            if validation_result.get("amount") and abs(validation_result["amount"] - self.amount) > 0.0001:
                return {
                    "valid": False,
                    "error": "Quantidade não confere com transação original",
                    "credit_id": self.credit_id,
                    "expected": validation_result.get("amount"),
                    "actual": self.amount
                }
            
            return {
                "valid": True,
                "credit_id": self.credit_id,
                "source_chain": self.source_chain,
                "tx_hash": self.tx_hash,
                "amount": self.amount,
                "token_symbol": self.token_symbol,
                "confirmations": validation_result.get("confirmations", 0),
                "block_height": validation_result.get("block_height")
            }
            
        except Exception as e:
            return {
                "valid": False,
                "error": f"Erro ao verificar crédito: {str(e)}",
                "credit_id": self.credit_id
            }
    
    def to_dict(self) -> Dict:
        """Converte crédito para dicionário"""
        return {
            "credit_id": self.credit_id,
            "source_chain": self.source_chain,
            "tx_hash": self.tx_hash,
            "amount": self.amount,
            "token_symbol": self.token_symbol,
            "recipient_address": self.recipient_address,
            "is_native": self.is_native,
            "status": self.status,
            "created_at": self.created_at,
            "signature_proof": self.signature_proof
        }


class NativeCreditSystem:
    """
    SISTEMA DE CRÉDITOS NATIVOS
    Gerencia créditos nativos baseados em provas criptográficas
    """
    
    def __init__(self):
        self.credits = {}  # credit_id -> NativeCredit
        self.credits_by_address = {}  # address -> [credit_ids]
        self.credits_by_chain = {}  # chain -> [credit_ids]
        print("💎 NATIVE CREDIT SYSTEM: Inicializado!")
        print("✅ Créditos nativos (não sintéticos)")
        print("✅ Prova criptográfica de cada depósito")
        print("✅ Validação on-chain")
    
    def create_native_credit(
        self,
        source_chain: str,
        tx_hash: str,
        amount: float,
        token_symbol: str,
        recipient_address: str,
        signature_proof: Optional[Dict] = None
    ) -> Dict:
        """
        Cria um crédito nativo baseado em transação real
        
        Args:
            source_chain: Blockchain de origem (bitcoin, ethereum, etc.)
            tx_hash: Hash da transação original
            amount: Quantidade
            token_symbol: Símbolo do token (BTC, ETH, etc.)
            recipient_address: Endereço do destinatário na Allianza
            signature_proof: Prova de assinatura (opcional, pode buscar da tx)
        
        Returns:
            Dict com resultado
        """
        try:
            # Validar transação na blockchain original
            validation_result = universal_validator.validate_universal(
                chain=source_chain,
                tx_hash=tx_hash,
                signature=signature_proof.get("signature") if signature_proof else None,
                public_key=signature_proof.get("public_key") if signature_proof else None
            )
            
            if not validation_result.get("valid"):
                return {
                    "success": False,
                    "error": f"Transação não válida: {validation_result.get('error')}",
                    "chain": source_chain,
                    "tx_hash": tx_hash
                }
            
            # Usar quantidade da validação se disponível
            validated_amount = validation_result.get("amount", amount)
            
            # Criar crédito nativo
            credit = NativeCredit(
                source_chain=source_chain,
                tx_hash=tx_hash,
                amount=validated_amount,
                token_symbol=token_symbol,
                signature_proof=signature_proof or validation_result,
                recipient_address=recipient_address
            )
            
            # Verificar crédito
            verification = credit.verify()
            if not verification.get("valid"):
                return {
                    "success": False,
                    "error": f"Crédito não válido: {verification.get('error')}",
                    "credit_id": credit.credit_id
                }
            
            # Armazenar crédito
            self.credits[credit.credit_id] = credit
            
            # Indexar por endereço
            if recipient_address not in self.credits_by_address:
                self.credits_by_address[recipient_address] = []
            self.credits_by_address[recipient_address].append(credit.credit_id)
            
            # Indexar por chain
            if source_chain not in self.credits_by_chain:
                self.credits_by_chain[source_chain] = []
            self.credits_by_chain[source_chain].append(credit.credit_id)
            
            return {
                "success": True,
                "credit_id": credit.credit_id,
                "credit": credit.to_dict(),
                "message": f"✅ Crédito nativo {token_symbol} criado!",
                "world_first": "🌍 PRIMEIRO NO MUNDO: Crédito nativo sem wrapped token!"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Erro ao criar crédito nativo: {str(e)}"
            }
    
    def get_credits_by_address(self, address: str) -> List[Dict]:
        """Retorna todos os créditos de um endereço"""
        credit_ids = self.credits_by_address.get(address, [])
        return [self.credits[cid].to_dict() for cid in credit_ids if cid in self.credits]
    
    def get_credits_by_chain(self, chain: str) -> List[Dict]:
        """Retorna todos os créditos de uma chain"""
        credit_ids = self.credits_by_chain.get(chain, [])
        return [self.credits[cid].to_dict() for cid in credit_ids if cid in self.credits]
    
    def get_credit(self, credit_id: str) -> Optional[Dict]:
        """Retorna um crédito específico"""
        credit = self.credits.get(credit_id)
        if credit:
            return credit.to_dict()
        return None
    
    def burn_credit(self, credit_id: str, reason: str = "withdrawn") -> Dict:
        """
        Queima um crédito (quando é sacado ou usado)
        
        Args:
            credit_id: ID do crédito
            reason: Razão (withdrawn, expired, etc.)
        
        Returns:
            Dict com resultado
        """
        if credit_id not in self.credits:
            return {
                "success": False,
                "error": "Crédito não encontrado"
            }
        
        credit = self.credits[credit_id]
        credit.status = "burned"
        
        return {
            "success": True,
            "credit_id": credit_id,
            "reason": reason,
            "message": f"Crédito {credit_id} queimado: {reason}"
        }
    
    def verify_credit(self, credit_id: str) -> Dict:
        """Verifica se um crédito ainda é válido"""
        if credit_id not in self.credits:
            return {
                "valid": False,
                "error": "Crédito não encontrado"
            }
        
        credit = self.credits[credit_id]
        return credit.verify()
    
    def get_system_status(self) -> Dict:
        """Retorna status do sistema"""
        total_credits = len(self.credits)
        active_credits = sum(1 for c in self.credits.values() if c.status == "active")
        burned_credits = total_credits - active_credits
        
        credits_by_chain = {}
        for chain, credit_ids in self.credits_by_chain.items():
            credits_by_chain[chain] = len(credit_ids)
        
        return {
            "total_credits": total_credits,
            "active_credits": active_credits,
            "burned_credits": burned_credits,
            "credits_by_chain": credits_by_chain,
            "supported_chains": ["bitcoin", "ethereum", "polygon", "bsc", "base", "solana"]
        }

# Instância global
native_credit_system = NativeCreditSystem()












