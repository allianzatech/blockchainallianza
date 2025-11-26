# bridge_smart_contract.py
# 🌉 SMART CONTRACT PARA BRIDGE DESCENTRALIZADO
# Implementação Python para interagir com contratos Solidity

import os
import json
import time
from typing import Dict, Optional
from web3 import Web3
from web3.middleware import geth_poa_middleware
from dotenv import load_dotenv

load_dotenv()

# ABI do contrato AllianzaBridge (simplificado)
BRIDGE_ABI = [
    {
        "inputs": [
            {"internalType": "address", "name": "token", "type": "address"},
            {"internalType": "uint256", "name": "amount", "type": "uint256"},
            {"internalType": "string", "name": "targetChain", "type": "string"},
            {"internalType": "address", "name": "recipient", "type": "address"}
        ],
        "name": "lockTokens",
        "outputs": [{"internalType": "bytes32", "name": "lockId", "type": "bytes32"}],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [{"internalType": "bytes32", "name": "lockId", "type": "bytes32"}],
        "name": "verifyLock",
        "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "anonymous": False,
        "inputs": [
            {"indexed": True, "internalType": "bytes32", "name": "lockId", "type": "bytes32"},
            {"indexed": True, "internalType": "address", "name": "sender", "type": "address"},
            {"indexed": False, "internalType": "uint256", "name": "amount", "type": "uint256"},
            {"indexed": False, "internalType": "string", "name": "targetChain", "type": "string"}
        ],
        "name": "TokensLocked",
        "type": "event"
    }
]

class BridgeSmartContract:
    """
    Interface Python para Smart Contract de Bridge
    Permite lock e verificação on-chain
    """
    
    def __init__(self, chain: str = "polygon"):
        self.chain = chain.lower()
        self.w3 = self._get_web3()
        self.contract_address = os.getenv(f'{self.chain.upper()}_BRIDGE_CONTRACT_ADDRESS')
        
        if self.contract_address and self.w3:
            self.contract = self.w3.eth.contract(
                address=Web3.to_checksum_address(self.contract_address),
                abi=BRIDGE_ABI
            )
            print(f"🌉 Bridge Smart Contract conectado em {chain}")
        else:
            self.contract = None
            print(f"⚠️  Bridge Smart Contract não configurado para {chain}")
    
    def _get_web3(self):
        """Obter conexão Web3 para a chain"""
        try:
            if self.chain == "polygon":
                rpc = os.getenv('POLYGON_RPC_URL', 'https://rpc-amoy.polygon.technology/')
            elif self.chain == "ethereum":
                infura_id = os.getenv('INFURA_PROJECT_ID', '4622f8123b1a4cf7a3e30098d9120d7f')
                rpc = f'https://sepolia.infura.io/v3/{infura_id}'
            elif self.chain == "bsc":
                rpc = os.getenv('BSC_RPC_URL', 'https://data-seed-prebsc-1-s1.binance.org:8545')
            else:
                return None
            
            w3 = Web3(Web3.HTTPProvider(rpc, request_kwargs={'timeout': 30}))
            if self.chain in ["polygon", "bsc"]:
                w3.middleware_onion.inject(geth_poa_middleware, layer=0)
            
            if w3.is_connected():
                return w3
            return None
        except Exception as e:
            print(f"Erro ao conectar: {e}")
            return None
    
    def lock_tokens(
        self,
        token_address: str,
        amount: int,
        target_chain: str,
        recipient: str,
        private_key: str
    ) -> Dict:
        """
        Fazer lock de tokens on-chain
        
        Args:
            token_address: Endereço do token ERC20
            amount: Quantidade (em wei/smallest unit)
            target_chain: Chain de destino
            recipient: Endereço do destinatário
            private_key: Chave privada do remetente
        
        Returns:
            Resultado do lock com lock_id
        """
        if not self.contract:
            return {
                "success": False,
                "error": "Contrato não configurado"
            }
        
        try:
            account = self.w3.eth.account.from_key(private_key)
            
            # Construir transação
            tx = self.contract.functions.lockTokens(
                Web3.to_checksum_address(token_address),
                amount,
                target_chain,
                Web3.to_checksum_address(recipient)
            ).build_transaction({
                'from': account.address,
                'nonce': self.w3.eth.get_transaction_count(account.address),
                'gas': 200000,
                'gasPrice': self.w3.eth.gas_price
            })
            
            # Assinar e enviar
            signed_tx = self.w3.eth.account.sign_transaction(tx, private_key)
            tx_hash = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction)
            
            # Aguardar confirmação
            receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash, timeout=120)
            
            # Buscar lock_id do evento
            lock_id = None
            if receipt.status == 1:
                # Buscar evento TokensLocked
                logs = self.contract.events.TokensLocked().process_receipt(receipt)
                if logs:
                    lock_id = logs[0]['args']['lockId'].hex()
            
            return {
                "success": receipt.status == 1,
                "lock_id": lock_id,
                "tx_hash": tx_hash.hex(),
                "block_number": receipt.blockNumber,
                "gas_used": receipt.gasUsed
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def verify_lock(self, lock_id: str) -> Dict:
        """
        Verificar se lock existe e está válido on-chain
        
        Args:
            lock_id: ID do lock (bytes32 em hex)
        
        Returns:
            Resultado da verificação
        """
        if not self.contract:
            return {
                "success": False,
                "error": "Contrato não configurado",
                "lock_valid": False
            }
        
        try:
            # Converter lock_id para bytes32
            if isinstance(lock_id, str) and lock_id.startswith('0x'):
                lock_id_bytes = bytes.fromhex(lock_id[2:])
            else:
                lock_id_bytes = bytes.fromhex(lock_id) if len(lock_id) == 64 else lock_id.encode()
            
            # Chamar função verifyLock
            is_valid = self.contract.functions.verifyLock(lock_id_bytes).call()
            
            return {
                "success": True,
                "lock_valid": is_valid,
                "lock_id": lock_id
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "lock_valid": False
            }
    
    def wait_for_confirmations(
        self,
        tx_hash: str,
        min_confirmations: int = 12
    ) -> Dict:
        """
        Aguardar confirmações suficientes
        
        Args:
            tx_hash: Hash da transação
            min_confirmations: Número mínimo de confirmações
        
        Returns:
            Status das confirmações
        """
        try:
            receipt = self.w3.eth.get_transaction_receipt(tx_hash)
            current_block = self.w3.eth.block_number
            
            confirmations = current_block - receipt.blockNumber
            
            if confirmations >= min_confirmations:
                return {
                    "success": True,
                    "confirmations": confirmations,
                    "sufficient": True
                }
            else:
                # Aguardar mais blocos
                needed = min_confirmations - confirmations
                print(f"⏳ Aguardando {needed} confirmações adicionais...")
                
                # Aguardar blocos (estimativa: 2s por bloco)
                wait_time = needed * 2
                time.sleep(min(wait_time, 60))  # Máximo 60 segundos
                
                # Verificar novamente
                current_block = self.w3.eth.block_number
                confirmations = current_block - receipt.blockNumber
                
                return {
                    "success": True,
                    "confirmations": confirmations,
                    "sufficient": confirmations >= min_confirmations
                }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "confirmations": 0,
                "sufficient": False
            }

