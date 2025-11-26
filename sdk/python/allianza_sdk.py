#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Allianza Blockchain SDK - Python
Baseado em web3.py para compatibilidade máxima
"""

from web3 import Web3
from typing import Dict, Optional, Union
from eth_account import Account
import json

class AllianzaWeb3(Web3):
    """
    Cliente Web3 customizado para Allianza Blockchain
    Extende Web3 com funcionalidades específicas da Allianza
    """
    
    def __init__(self, rpc_url: str = "http://localhost:8545"):
        super().__init__(Web3.HTTPProvider(rpc_url))
        self.chain_id = 12345  # Allianza Chain ID
        self.chain_name = "Allianza Blockchain"
    
    def send_cross_chain_transaction(
        self,
        target_chain: str,
        recipient: str,
        amount: Union[float, str],
        private_key: Optional[str] = None
    ) -> Dict:
        """
        Envia transação cross-chain
        
        Args:
            target_chain: Chain de destino (bitcoin, ethereum, polygon, etc.)
            recipient: Endereço de destino
            amount: Quantidade (em wei ou unidades nativas)
            private_key: Chave privada (opcional, se já tiver wallet conectada)
        
        Returns:
            Resultado da transação
        """
        method = "allianza_sendCrossChain"
        params = [target_chain, recipient, str(amount)]
        
        return self.manager.request_blocking(method, params)
    
    def get_cross_chain_status(self, tx_hash: str) -> Dict:
        """
        Verifica status de transferência cross-chain
        
        Args:
            tx_hash: Hash da transação
        
        Returns:
            Status da transferência
        """
        method = "allianza_getCrossChainStatus"
        params = [tx_hash]
        
        return self.manager.request_blocking(method, params)
    
    def get_cross_chain_balance(
        self,
        address: str,
        chain: str
    ) -> Dict:
        """
        Obtém saldo cross-chain
        
        Args:
            address: Endereço
            chain: Chain (bitcoin, ethereum, etc.)
        
        Returns:
            Saldo
        """
        method = "allianza_getCrossChainBalance"
        params = [address, chain]
        
        return self.manager.request_blocking(method, params)
    
    def stake(self, address: str, amount: Union[float, str]) -> Dict:
        """
        Stake tokens para validação
        
        Args:
            address: Endereço do validador
            amount: Quantidade para stake
        
        Returns:
            Resultado do stake
        """
        method = "allianza_stake"
        params = [address, str(amount)]
        
        return self.manager.request_blocking(method, params)
    
    def unstake(self, address: str, amount: Union[float, str]) -> Dict:
        """
        Unstake tokens
        
        Args:
            address: Endereço do validador
            amount: Quantidade para unstake
        
        Returns:
            Resultado do unstake
        """
        method = "allianza_unstake"
        params = [address, str(amount)]
        
        return self.manager.request_blocking(method, params)
    
    def get_validators(self) -> Dict:
        """
        Obtém lista de validadores
        
        Returns:
            Lista de validadores
        """
        method = "allianza_getValidators"
        return self.manager.request_blocking(method, [])
    
    def get_validator_info(self, address: str) -> Dict:
        """
        Obtém informações de um validador
        
        Args:
            address: Endereço do validador
        
        Returns:
            Informações do validador
        """
        method = "allianza_getValidatorInfo"
        return self.manager.request_blocking(method, [address])
    
    def get_network_info(self) -> Dict:
        """
        Obtém informações da rede
        
        Returns:
            Informações da rede
        """
        method = "allianza_getNetworkInfo"
        return self.manager.request_blocking(method, [])


class AllianzaWallet:
    """
    Wallet para Allianza Blockchain
    """
    
    def __init__(self, private_key: Optional[str] = None, web3: Optional[AllianzaWeb3] = None):
        if private_key:
            self.account = Account.from_key(private_key)
        else:
            self.account = Account.create()
        
        self.web3 = web3 or AllianzaWeb3()
        self.address = self.account.address
    
    def send_transaction(
        self,
        to: str,
        value: Union[float, str],
        data: Optional[str] = None
    ) -> Dict:
        """
        Envia transação normal
        
        Args:
            to: Endereço de destino
            value: Valor
            data: Dados opcionais
        
        Returns:
            Hash da transação
        """
        try:
            # Converter endereço para checksum
            to_checksummed = self.web3.to_checksum_address(to)
            
            # Tentar obter gas price e nonce do RPC
            try:
                gas_price = self.web3.eth.gas_price
            except:
                gas_price = self.web3.to_wei(20, "gwei")  # Fallback: 20 gwei
            
            try:
                nonce = self.web3.eth.get_transaction_count(self.address)
            except:
                nonce = 0  # Fallback: nonce 0
            
            # Validar endereço antes de criar transação
            if not self.web3.is_address(to_checksummed):
                return {
                    "success": False,
                    "error": "Endereço de destino inválido",
                    "message": f"Endereço '{to}' não é válido"
                }
            
            # Criar transação (SEM campo 'from' - sign_transaction não aceita)
            transaction = {
                "to": to_checksummed,
                "value": self.web3.to_wei(str(value), "ether"),
                "gas": 21000,
                "gasPrice": int(gas_price),
                "nonce": int(nonce),
                "chainId": int(self.web3.chain_id)
            }
            
            if data:
                transaction["data"] = data
            
            # Assinar transação
            signed_txn = self.account.sign_transaction(transaction)
            
            # Obter rawTransaction (pode ser rawTransaction ou raw_transaction dependendo da versão)
            raw_tx = getattr(signed_txn, 'rawTransaction', None) or getattr(signed_txn, 'raw_transaction', None)
            
            if raw_tx is None:
                # Se não encontrar, tentar acessar diretamente
                if hasattr(signed_txn, 'rawTransaction'):
                    raw_tx = signed_txn.rawTransaction
                elif hasattr(signed_txn, 'raw_transaction'):
                    raw_tx = signed_txn.raw_transaction
                else:
                    # Último recurso: tentar serializar
                    raw_tx = bytes(signed_txn)
            
            # Enviar transação
            tx_hash = self.web3.eth.send_raw_transaction(raw_tx)
            
            return tx_hash
        except ValueError as e:
            # Erro de validação
            return {
                "success": False,
                "error": "Erro de validação",
                "message": str(e)
            }
        except Exception as e:
            # Se falhar, retornar erro estruturado
            return {
                "success": False,
                "error": str(e),
                "message": "Erro ao enviar transação. Verifique se o RPC server está rodando."
            }
    
    def send_cross_chain(
        self,
        target_chain: str,
        recipient: str,
        amount: Union[float, str]
    ) -> Dict:
        """
        Envia transação cross-chain
        
        Args:
            target_chain: Chain de destino
            recipient: Endereço de destino
            amount: Quantidade
        
        Returns:
            Resultado da transação
        """
        return self.web3.send_cross_chain_transaction(
            target_chain,
            recipient,
            amount,
            self.account.key.hex()
        )
    
    def stake(self, amount: Union[float, str]) -> Dict:
        """
        Stake tokens
        
        Args:
            amount: Quantidade
        
        Returns:
            Resultado do stake
        """
        return self.web3.stake(self.address, amount)
    
    def unstake(self, amount: Union[float, str]) -> Dict:
        """
        Unstake tokens
        
        Args:
            amount: Quantidade
        
        Returns:
            Resultado do unstake
        """
        return self.web3.unstake(self.address, amount)
    
    def get_balance(self) -> int:
        """
        Obtém saldo da wallet
        
        Returns:
            Saldo em wei
        """
        return self.web3.eth.get_balance(self.address)


# Funções de conveniência
def create_wallet() -> AllianzaWallet:
    """Cria nova wallet"""
    return AllianzaWallet()


def connect_wallet(private_key: str, rpc_url: str = "http://localhost:8545") -> AllianzaWallet:
    """Conecta wallet existente"""
    web3 = AllianzaWeb3(rpc_url)
    return AllianzaWallet(private_key, web3)


def connect_to_network(rpc_url: str = "http://localhost:8545") -> AllianzaWeb3:
    """Conecta à rede Allianza"""
    return AllianzaWeb3(rpc_url)

