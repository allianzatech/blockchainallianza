#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔄 Gerador Automático de Transações para Testnet
Resolve o problema de blocos vazios e transações zero
"""

import time
import secrets
import random
from typing import Dict, List, Optional
from datetime import datetime
import threading
import logging

logger = logging.getLogger(__name__)

class TestnetAutoTransactionGenerator:
    """Gera transações automaticamente para manter a testnet ativa"""
    
    def __init__(self, blockchain_instance, quantum_security_instance=None):
        self.blockchain = blockchain_instance
        self.quantum_security = quantum_security_instance
        self.running = False
        self.thread = None
        self.interval = 30  # Gerar transação a cada 30 segundos
        self.min_amount = 0.001
        self.max_amount = 10.0
        
        # Endereços de teste para gerar transações
        self.test_addresses = [
            "ALZ1Test0000000000000000000000000000000000",
            "ALZ1Test0000000000000000000000000000000001",
            "ALZ1Test0000000000000000000000000000000002",
            "ALZ1Test0000000000000000000000000000000003",
            "ALZ1Test0000000000000000000000000000000004",
            "ALZ1Test0000000000000000000000000000000005",
        ]
        
        # Garantir que os endereços de teste existam
        self._initialize_test_addresses()
    
    def _initialize_test_addresses(self):
        """Inicializar endereços de teste com saldos"""
        try:
            # Garantir que wallets existe
            if not hasattr(self.blockchain, 'wallets'):
                self.blockchain.wallets = {}
            
            for address in self.test_addresses:
                if address not in self.blockchain.wallets:
                    # Criar carteira manualmente
                    self.blockchain.wallets[address] = {
                        "ALZ": 1000.0,  # Saldo inicial de 1000 ALZ
                        "staked": 0,
                        "blockchain_source": "allianza",
                        "external_address": None
                    }
                else:
                    # Garantir saldo mínimo
                    if self.blockchain.wallets[address].get("ALZ", 0) < 100:
                        self.blockchain.wallets[address]["ALZ"] = 1000.0
        except Exception as e:
            logger.warning(f"⚠️  Erro ao inicializar endereços de teste: {e}")
            import traceback
            logger.debug(traceback.format_exc())
    
    def generate_test_transaction(self) -> Optional[Dict]:
        """Gera uma transação de teste"""
        try:
            # Selecionar endereços aleatórios
            sender = random.choice(self.test_addresses)
            receiver = random.choice([addr for addr in self.test_addresses if addr != sender])
            
            # Garantir que wallets existe e endereços estão inicializados
            if not hasattr(self.blockchain, 'wallets'):
                self.blockchain.wallets = {}
            
            if sender not in self.blockchain.wallets:
                self._initialize_test_addresses()
            
            # Verificar se ainda não existe após inicialização
            if sender not in self.blockchain.wallets:
                self.blockchain.wallets[sender] = {
                    "ALZ": 1000.0,
                    "staked": 0,
                    "blockchain_source": "allianza",
                    "external_address": None
                }
            
            sender_balance = self.blockchain.wallets.get(sender, {}).get("ALZ", 0)
            
            if sender_balance < self.min_amount:
                # Recarregar saldo se necessário
                self.blockchain.wallets[sender]["ALZ"] = 1000.0
                sender_balance = 1000.0
            
            # Gerar valor aleatório
            amount = round(random.uniform(self.min_amount, min(self.max_amount, sender_balance * 0.1)), 6)
            
            # Criar chave privada de teste (simulada)
            # Em produção, usar chaves reais, mas para testnet podemos usar uma chave fixa de teste
            from cryptography.hazmat.primitives.asymmetric import ec
            from cryptography.hazmat.backends import default_backend
            
            # Gerar chave privada de teste (ou usar uma fixa)
            try:
                private_key = ec.generate_private_key(ec.SECP256K1(), default_backend())
            except:
                # Fallback: criar transação sem assinatura real (para testnet)
                private_key = None
            
            # Criar transação
            if hasattr(self.blockchain, 'create_transaction'):
                try:
                    if private_key:
                        tx = self.blockchain.create_transaction(
                            sender=sender,
                            receiver=receiver,
                            amount=amount,
                            private_key=private_key,
                            is_public=True,
                            network="allianza"
                        )
                    else:
                        # Criar transação manualmente se não tiver chave
                        tx = self._create_transaction_manual(sender, receiver, amount)
                    
                    logger.info(f"✅ Transação gerada: {sender[:10]}... → {receiver[:10]}... ({amount} ALZ)")
                    return tx
                except Exception as e:
                    logger.warning(f"⚠️  Erro ao criar transação: {e}")
                    # Fallback: criar transação manual
                    return self._create_transaction_manual(sender, receiver, amount)
            else:
                return self._create_transaction_manual(sender, receiver, amount)
                
        except Exception as e:
            logger.error(f"❌ Erro ao gerar transação de teste: {e}")
            return None
    
    def _create_transaction_manual(self, sender: str, receiver: str, amount: float) -> Dict:
        """Cria transação manualmente (fallback)"""
        import hashlib
        import uuid
        
        tx_id = str(uuid.uuid4())
        timestamp = time.time()
        
        # Gerar hash da transação
        tx_data = f"{tx_id}{sender}{receiver}{amount}{timestamp}"
        tx_hash = hashlib.sha256(tx_data.encode()).hexdigest()
        
        transaction = {
            "id": tx_id,
            "tx_hash": f"0x{tx_hash}",
            "sender": sender,
            "receiver": receiver,
            "amount": amount,
            "timestamp": timestamp,
            "type": "transfer",
            "network": "allianza",
            "is_public": True,
            "signature": f"test_signature_{tx_hash[:32]}",
            "auto_generated": True  # Marca como gerada automaticamente
        }
        
        # Adicionar à lista de transações pendentes
        if hasattr(self.blockchain, 'pending_transactions'):
            shard_id = self.blockchain.get_shard(sender) if hasattr(self.blockchain, 'get_shard') else 0
            if isinstance(self.blockchain.pending_transactions, dict):
                if shard_id not in self.blockchain.pending_transactions:
                    self.blockchain.pending_transactions[shard_id] = []
                self.blockchain.pending_transactions[shard_id].append(transaction)
            elif isinstance(self.blockchain.pending_transactions, list):
                self.blockchain.pending_transactions.append(transaction)
        
        # Atualizar saldos
        if hasattr(self.blockchain, 'wallets'):
            if sender in self.blockchain.wallets:
                self.blockchain.wallets[sender]["ALZ"] = max(0, self.blockchain.wallets[sender]["ALZ"] - amount)
            if receiver in self.blockchain.wallets:
                if receiver not in self.blockchain.wallets:
                    self.blockchain.wallets[receiver] = {"ALZ": 0, "staked": 0, "blockchain_source": "allianza", "external_address": None}
                self.blockchain.wallets[receiver]["ALZ"] = self.blockchain.wallets[receiver].get("ALZ", 0) + amount
        
        return transaction
    
    def start(self, interval: int = 30):
        """Inicia o gerador automático de transações"""
        if self.running:
            logger.warning("⚠️  Gerador já está rodando")
            return
        
        self.interval = interval
        self.running = True
        self.thread = threading.Thread(target=self._run, daemon=True)
        self.thread.start()
        logger.info(f"🔄 Gerador automático de transações iniciado (intervalo: {interval}s)")
    
    def stop(self):
        """Para o gerador automático"""
        self.running = False
        if self.thread:
            self.thread.join(timeout=5)
        logger.info("⏹️  Gerador automático de transações parado")
    
    def _run(self):
        """Loop principal do gerador"""
        while self.running:
            try:
                # Gerar transação
                tx = self.generate_test_transaction()
                
                if tx:
                    logger.debug(f"📝 Transação gerada: {tx.get('tx_hash', 'N/A')[:16]}...")
                
                # Aguardar intervalo
                time.sleep(self.interval)
                
            except Exception as e:
                logger.error(f"❌ Erro no loop do gerador: {e}")
                time.sleep(self.interval)
    
    def generate_batch(self, count: int = 10) -> List[Dict]:
        """Gera um lote de transações de uma vez"""
        transactions = []
        for _ in range(count):
            tx = self.generate_test_transaction()
            if tx:
                transactions.append(tx)
            time.sleep(0.1)  # Pequeno delay entre transações
        return transactions

