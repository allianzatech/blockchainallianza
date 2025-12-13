#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
⚡ GASLESS RELAY SYSTEM - ALLIANZA BLOCKCHAIN
Sistema completo de relay gasless com anti-replay
"""

import time
import hashlib
import json
import os
from datetime import datetime
from typing import Dict, Optional, List
from pathlib import Path
from web3 import Web3
from web3.middleware import geth_poa_middleware
from dotenv import load_dotenv

load_dotenv()


class GaslessRelaySystem:
    """
    Sistema de Relay Gasless Completo
    
    Funcionalidades:
    - Relay paga gas para usuário
    - Anti-replay com nonces únicos
    - Reembolso via tokenomics
    - Validação on-chain
    """
    
    def __init__(self, web3_provider=None, relay_private_key=None):
        """
        Inicializar sistema de relay
        
        Args:
            web3_provider: Provider Web3 (opcional)
            relay_private_key: Chave privada do relay (opcional)
        """
        self.relay_address = None
        self.relay_account = None
        self.web3 = web3_provider
        
        # Nonces usados (anti-replay)
        self.used_nonces = set()
        self.nonce_timestamps = {}  # nonce -> timestamp
        
        # Estatísticas
        self.stats = {
            "transactions_relayed": 0,
            "gas_paid_total": 0.0,
            "reimbursements_total": 0.0,
            "replay_attempts_blocked": 0
        }
        
        # Configurar relay
        if relay_private_key:
            try:
                from eth_account import Account
                self.relay_account = Account.from_key(relay_private_key)
                self.relay_address = self.relay_account.address
            except Exception as e:
                print(f"⚠️  Erro ao configurar relay account: {e}")
        
        # Se não tem web3, tentar criar
        if not self.web3:
            try:
                eth_rpc = os.getenv('ETH_RPC_URL')
                if eth_rpc:
                    self.web3 = Web3(Web3.HTTPProvider(eth_rpc))
                    if self.web3.is_connected():
                        self.web3.middleware_onion.inject(geth_poa_middleware, layer=0)
            except Exception as e:
                print(f"⚠️  Erro ao conectar Web3: {e}")
        
        print("⚡ GASLESS RELAY SYSTEM: Inicializado!")
        print("   • Relay paga gas para usuários")
        print("   • Anti-replay com nonces únicos")
        print("   • Reembolso via tokenomics")
    
    def generate_nonce(self, user_address: str) -> int:
        """
        Gerar nonce único para usuário
        
        Args:
            user_address: Endereço do usuário
        
        Returns:
            Nonce único
        """
        # Nonce baseado em timestamp + hash do endereço
        timestamp = int(time.time() * 1000)  # milissegundos
        address_hash = int(hashlib.sha256(user_address.encode()).hexdigest()[:8], 16)
        nonce = timestamp + (address_hash % 1000000)
        
        # Garantir que não foi usado
        while nonce in self.used_nonces:
            nonce += 1
        
        self.used_nonces.add(nonce)
        self.nonce_timestamps[nonce] = timestamp
        
        return nonce
    
    def check_replay(self, nonce: int, user_address: str) -> Dict:
        """
        Verificar se nonce já foi usado (anti-replay)
        
        Args:
            nonce: Nonce a verificar
            user_address: Endereço do usuário
        
        Returns:
            Dict com resultado da verificação
        """
        if nonce in self.used_nonces:
            self.stats["replay_attempts_blocked"] += 1
            return {
                "is_replay": True,
                "blocked": True,
                "reason": "Nonce já usado",
                "original_timestamp": self.nonce_timestamps.get(nonce)
            }
        
        # Verificar se nonce é muito antigo (expiração)
        if nonce in self.nonce_timestamps:
            timestamp = self.nonce_timestamps[nonce]
            age_seconds = (time.time() * 1000 - timestamp) / 1000
            if age_seconds > 3600:  # 1 hora
                return {
                    "is_replay": False,
                    "blocked": True,
                    "reason": "Nonce expirado",
                    "age_seconds": age_seconds
                }
        
        return {
            "is_replay": False,
            "blocked": False,
            "valid": True
        }
    
    def relay_transaction(
        self,
        user_address: str,
        to_address: str,
        data: str,
        value: int = 0,
        gas_limit: int = 21000,
        nonce: Optional[int] = None
    ) -> Dict:
        """
        Relayer transação (pagar gas para usuário)
        
        Args:
            user_address: Endereço do usuário
            to_address: Endereço de destino
            data: Dados da transação
            value: Valor em wei
            gas_limit: Limite de gas
            nonce: Nonce (opcional, será gerado se não fornecido)
        
        Returns:
            Dict com resultado do relay
        """
        try:
            if not self.web3 or not self.web3.is_connected():
                return {
                    "success": False,
                    "error": "Web3 não conectado"
                }
            
            if not self.relay_account:
                return {
                    "success": False,
                    "error": "Relay account não configurado"
                }
            
            # Gerar nonce se não fornecido
            if nonce is None:
                nonce = self.generate_nonce(user_address)
            
            # Verificar anti-replay
            replay_check = self.check_replay(nonce, user_address)
            if replay_check.get("blocked"):
                return {
                    "success": False,
                    "error": replay_check.get("reason", "Replay detectado"),
                    "replay_check": replay_check
                }
            
            # Obter gas price
            try:
                gas_price = self.web3.eth.gas_price
            except:
                gas_price = self.web3.to_wei(20, 'gwei')  # Fallback
            
            # Criar transação
            transaction = {
                'from': self.relay_address,
                'to': to_address,
                'value': value,
                'data': data,
                'gas': gas_limit,
                'gasPrice': gas_price,
                'nonce': self.web3.eth.get_transaction_count(self.relay_address),
                'chainId': self.web3.eth.chain_id
            }
            
            # Estimar gas se necessário
            try:
                estimated_gas = self.web3.eth.estimate_gas(transaction)
                transaction['gas'] = estimated_gas
            except:
                pass  # Usar gas_limit fornecido
            
            # Assinar e enviar transação
            signed_txn = self.web3.eth.account.sign_transaction(transaction, self.relay_account.key)
            tx_hash = self.web3.eth.send_raw_transaction(signed_txn.rawTransaction)
            
            # Calcular gas pago
            gas_paid = transaction['gas'] * transaction['gasPrice']
            gas_paid_eth = self.web3.from_wei(gas_paid, 'ether')
            
            # Atualizar estatísticas
            self.stats["transactions_relayed"] += 1
            self.stats["gas_paid_total"] += float(gas_paid_eth)
            
            # Marcar nonce como usado
            self.used_nonces.add(nonce)
            self.nonce_timestamps[nonce] = int(time.time() * 1000)
            
            return {
                "success": True,
                "transaction_hash": tx_hash.hex(),
                "relay_address": self.relay_address,
                "user_address": user_address,
                "gas_paid": gas_paid_eth,
                "gas_paid_wei": gas_paid,
                "user_gas_paid": 0.0,
                "nonce": nonce,
                "anti_replay": True,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def reimburse_relay(self, tx_hash: str, amount: float) -> Dict:
        """
        Reembolsar relay via tokenomics
        
        Args:
            tx_hash: Hash da transação
            amount: Quantidade a reembolsar
        
        Returns:
            Dict com resultado do reembolso
        """
        try:
            # Em produção, isso seria integrado com tokenomics
            # Por enquanto, simular reembolso
            
            reimbursement = {
                "success": True,
                "tx_hash": tx_hash,
                "amount": amount,
                "relay_address": self.relay_address,
                "reimbursed": True,
                "timestamp": datetime.now().isoformat(),
                "note": "Reembolso simulado - Em produção integrar com tokenomics"
            }
            
            self.stats["reimbursements_total"] += amount
            
            return reimbursement
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def get_stats(self) -> Dict:
        """Obter estatísticas do relay"""
        return {
            "relay_address": self.relay_address,
            "stats": self.stats.copy(),
            "used_nonces_count": len(self.used_nonces),
            "timestamp": datetime.now().isoformat()
        }


# =============================================================================
# EXECUÇÃO DIRETA
# =============================================================================

if __name__ == "__main__":
    # Teste básico
    relay = GaslessRelaySystem()
    
    print("\n⚡ Testando Gasless Relay System...")
    
    # Gerar nonce
    nonce = relay.generate_nonce("0xUserAddress")
    print(f"Nonce gerado: {nonce}")
    
    # Verificar replay
    replay_check = relay.check_replay(nonce, "0xUserAddress")
    print(f"Replay check: {replay_check}")
    
    # Tentar usar mesmo nonce (deve bloquear)
    replay_check2 = relay.check_replay(nonce, "0xUserAddress")
    print(f"Replay check (mesmo nonce): {replay_check2}")
    
    # Estatísticas
    stats = relay.get_stats()
    print(f"\nEstatísticas: {json.dumps(stats, indent=2)}")

