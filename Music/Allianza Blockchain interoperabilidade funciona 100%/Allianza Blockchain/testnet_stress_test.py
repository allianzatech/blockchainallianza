#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔥 Teste de Estresse para Testnet - Gerar Muitas Transações
Resolve problema de números zero no dashboard
"""

import time
import random
import threading
from typing import Dict, List
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class TestnetStressTest:
    """Gera muitas transações rapidamente para teste de estresse"""
    
    def __init__(self, blockchain_instance, quantum_security_instance=None):
        self.blockchain = blockchain_instance
        self.quantum_security = quantum_security_instance
        self.running = False
        self.thread = None
        self.transactions_generated = 0
        
        # Endereços de teste
        self.test_addresses = [
            "ALZ1Test0000000000000000000000000000000000",
            "ALZ1Test0000000000000000000000000000000001",
            "ALZ1Test0000000000000000000000000000000002",
            "ALZ1Test0000000000000000000000000000000003",
            "ALZ1Test0000000000000000000000000000000004",
            "ALZ1Test0000000000000000000000000000000005",
            "ALZ1Test0000000000000000000000000000000006",
            "ALZ1Test0000000000000000000000000000000007",
            "ALZ1Test0000000000000000000000000000000008",
            "ALZ1Test0000000000000000000000000000000009",
        ]
        
        self._initialize_addresses()
    
    def _initialize_addresses(self):
        """Garantir que todos os endereços tenham saldo"""
        try:
            if not hasattr(self.blockchain, 'wallets'):
                self.blockchain.wallets = {}
            
            for address in self.test_addresses:
                if address not in self.blockchain.wallets:
                    self.blockchain.wallets[address] = {
                        "ALZ": 10000.0,  # Saldo alto para testes
                        "staked": 0,
                        "blockchain_source": "allianza",
                        "external_address": None
                    }
                else:
                    # Garantir saldo mínimo
                    if self.blockchain.wallets[address]["ALZ"] < 1000:
                        self.blockchain.wallets[address]["ALZ"] = 10000.0
        except Exception as e:
            logger.warning(f"⚠️  Erro ao inicializar endereços: {e}")
    
    def generate_transaction(self) -> Dict:
        """Gera uma transação de teste"""
        try:
            sender = random.choice(self.test_addresses)
            receiver = random.choice([addr for addr in self.test_addresses if addr != sender])
            
            sender_balance = self.blockchain.wallets.get(sender, {}).get("ALZ", 0)
            if sender_balance < 0.001:
                self.blockchain.wallets[sender]["ALZ"] = 10000.0
                sender_balance = 10000.0
            
            amount = round(random.uniform(0.001, min(100.0, sender_balance * 0.1)), 6)
            
            # Criar transação manualmente (mais rápido)
            import hashlib
            import uuid
            
            tx_id = str(uuid.uuid4())
            timestamp = time.time()
            
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
                "signature": f"stress_test_{tx_hash[:32]}",
                "stress_test": True
            }
            
            # Adicionar às transações pendentes
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
                if receiver not in self.blockchain.wallets:
                    self.blockchain.wallets[receiver] = {"ALZ": 0, "staked": 0, "blockchain_source": "allianza", "external_address": None}
                self.blockchain.wallets[receiver]["ALZ"] = self.blockchain.wallets[receiver].get("ALZ", 0) + amount
            
            self.transactions_generated += 1
            return transaction
            
        except Exception as e:
            logger.error(f"❌ Erro ao gerar transação: {e}")
            return None
    
    def run_stress_test(self, count: int = 100, delay: float = 0.1):
        """
        Executa teste de estresse gerando muitas transações
        
        Args:
            count: Número de transações a gerar
            delay: Delay entre transações (segundos)
        """
        logger.info(f"🔥 Iniciando teste de estresse: {count} transações")
        print(f"🔥 Teste de estresse: Gerando {count} transações...")
        
        start_time = time.time()
        successful = 0
        failed = 0
        
        for i in range(count):
            try:
                tx = self.generate_transaction()
                if tx:
                    successful += 1
                    if (i + 1) % 10 == 0:
                        print(f"   ✅ {i + 1}/{count} transações geradas...")
                else:
                    failed += 1
                
                if delay > 0:
                    time.sleep(delay)
            except Exception as e:
                failed += 1
                logger.error(f"❌ Erro na transação {i+1}: {e}")
        
        duration = time.time() - start_time
        tps = successful / duration if duration > 0 else 0
        
        result = {
            "success": True,
            "total": count,
            "successful": successful,
            "failed": failed,
            "duration": round(duration, 2),
            "transactions_per_second": round(tps, 2),
            "message": f"✅ Teste de estresse concluído: {successful} transações em {duration:.2f}s ({tps:.2f} TPS)"
        }
        
        logger.info(result["message"])
        print(result["message"])
        
        return result
    
    def run_continuous_stress(self, tps: float = 10.0, duration: int = 60):
        """
        Executa teste de estresse contínuo
        
        Args:
            tps: Transações por segundo
            duration: Duração em segundos
        """
        logger.info(f"🔥 Teste de estresse contínuo: {tps} TPS por {duration}s")
        print(f"🔥 Teste contínuo: {tps} TPS por {duration} segundos...")
        
        start_time = time.time()
        successful = 0
        delay = 1.0 / tps if tps > 0 else 0.1
        
        while (time.time() - start_time) < duration:
            try:
                tx = self.generate_transaction()
                if tx:
                    successful += 1
                time.sleep(delay)
            except Exception as e:
                logger.error(f"❌ Erro: {e}")
        
        actual_duration = time.time() - start_time
        actual_tps = successful / actual_duration if actual_duration > 0 else 0
        
        result = {
            "success": True,
            "duration": round(actual_duration, 2),
            "transactions_generated": successful,
            "target_tps": tps,
            "actual_tps": round(actual_tps, 2),
            "message": f"✅ Teste contínuo concluído: {successful} transações em {actual_duration:.2f}s ({actual_tps:.2f} TPS)"
        }
        
        logger.info(result["message"])
        print(result["message"])
        
        return result

