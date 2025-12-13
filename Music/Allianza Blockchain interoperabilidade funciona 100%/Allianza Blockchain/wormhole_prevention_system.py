#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🛡️ WORMHOLE PREVENTION SYSTEM - ALLIANZA BLOCKCHAIN
Sistema de prevenção de exploits tipo Wormhole
"""

import time
import hashlib
import json
from datetime import datetime
from typing import Dict, Optional, List, Set
from pathlib import Path


class WormholePreventionSystem:
    """
    Sistema de Prevenção de Exploits Wormhole
    
    Funcionalidades:
    - Validação de mensagens cross-chain
    - Prevenção de duplicação de mensagens
    - Verificação de sequência de mensagens
    - Detecção de mensagens maliciosas
    - Rate limiting por origem
    """
    
    def __init__(self):
        """Inicializar sistema de prevenção"""
        # Mensagens processadas (hash -> timestamp)
        self.processed_messages: Dict[str, float] = {}
        
        # Sequências por origem (chain -> last_sequence)
        self.sequence_tracker: Dict[str, int] = {}
        
        # Rate limiting (chain -> [timestamps])
        self.rate_limit_history: Dict[str, List[float]] = {}
        
        # Mensagens bloqueadas
        self.blocked_messages: Set[str] = set()
        
        # Estatísticas
        self.stats = {
            "messages_processed": 0,
            "messages_blocked": 0,
            "duplicate_detections": 0,
            "sequence_violations": 0,
            "rate_limit_hits": 0
        }
        
        print("🛡️ WORMHOLE PREVENTION SYSTEM: Inicializado!")
        print("   • Validação de mensagens cross-chain")
        print("   • Prevenção de duplicação")
        print("   • Verificação de sequência")
        print("   • Rate limiting")
    
    def generate_message_hash(self, source_chain: str, target_chain: str, message_data: Dict) -> str:
        """
        Gerar hash único da mensagem
        
        Args:
            source_chain: Chain de origem
            target_chain: Chain de destino
            message_data: Dados da mensagem
        
        Returns:
            Hash SHA-256 da mensagem
        """
        message_str = json.dumps({
            "source_chain": source_chain,
            "target_chain": target_chain,
            "data": message_data
        }, sort_keys=True)
        
        return hashlib.sha256(message_str.encode()).hexdigest()
    
    def validate_message_sequence(self, source_chain: str, sequence: int) -> Dict:
        """
        Validar sequência da mensagem
        
        Args:
            source_chain: Chain de origem
            sequence: Número de sequência
        
        Returns:
            Dict com resultado da validação
        """
        last_sequence = self.sequence_tracker.get(source_chain, -1)
        
        # Sequência deve ser maior que a última
        if sequence <= last_sequence:
            self.stats["sequence_violations"] += 1
            return {
                "valid": False,
                "reason": f"Sequência inválida: {sequence} <= {last_sequence}",
                "last_sequence": last_sequence,
                "current_sequence": sequence
            }
        
        # Atualizar sequência
        self.sequence_tracker[source_chain] = sequence
        
        return {
            "valid": True,
            "last_sequence": last_sequence,
            "current_sequence": sequence
        }
    
    def check_rate_limit(self, source_chain: str, max_per_minute: int = 10) -> Dict:
        """
        Verificar rate limiting
        
        Args:
            source_chain: Chain de origem
            max_per_minute: Máximo de mensagens por minuto
        
        Returns:
            Dict com resultado do rate limit
        """
        now = time.time()
        minute_ago = now - 60
        
        # Limpar histórico antigo
        if source_chain in self.rate_limit_history:
            self.rate_limit_history[source_chain] = [
                ts for ts in self.rate_limit_history[source_chain]
                if ts > minute_ago
            ]
        else:
            self.rate_limit_history[source_chain] = []
        
        # Verificar limite
        count = len(self.rate_limit_history[source_chain])
        
        if count >= max_per_minute:
            self.stats["rate_limit_hits"] += 1
            return {
                "allowed": False,
                "reason": f"Rate limit excedido: {count}/{max_per_minute} mensagens/min",
                "count": count,
                "limit": max_per_minute
            }
        
        # Adicionar timestamp
        self.rate_limit_history[source_chain].append(now)
        
        return {
            "allowed": True,
            "count": count + 1,
            "limit": max_per_minute
        }
    
    def validate_cross_chain_message(
        self,
        source_chain: str,
        target_chain: str,
        message_data: Dict,
        sequence: Optional[int] = None,
        message_hash: Optional[str] = None
    ) -> Dict:
        """
        Validar mensagem cross-chain completa
        
        Args:
            source_chain: Chain de origem
            target_chain: Chain de destino
            message_data: Dados da mensagem
            sequence: Número de sequência (opcional)
            message_hash: Hash da mensagem (opcional, será gerado se não fornecido)
        
        Returns:
            Dict com resultado da validação
        """
        # Gerar hash se não fornecido
        if not message_hash:
            message_hash = self.generate_message_hash(source_chain, target_chain, message_data)
        
        # Verificar se mensagem já foi processada (duplicação)
        if message_hash in self.processed_messages:
            self.stats["duplicate_detections"] += 1
            self.stats["messages_blocked"] += 1
            self.blocked_messages.add(message_hash)
            
            return {
                "valid": False,
                "reason": "Mensagem duplicada detectada",
                "message_hash": message_hash,
                "original_timestamp": self.processed_messages[message_hash],
                "blocked": True
            }
        
        # Verificar se mensagem foi bloqueada anteriormente
        if message_hash in self.blocked_messages:
            return {
                "valid": False,
                "reason": "Mensagem previamente bloqueada",
                "message_hash": message_hash,
                "blocked": True
            }
        
        # Validar sequência se fornecida
        sequence_valid = True
        if sequence is not None:
            seq_result = self.validate_message_sequence(source_chain, sequence)
            sequence_valid = seq_result.get("valid", False)
            if not sequence_valid:
                self.stats["messages_blocked"] += 1
                self.blocked_messages.add(message_hash)
                return {
                    "valid": False,
                    "reason": seq_result.get("reason", "Sequência inválida"),
                    "message_hash": message_hash,
                    "sequence_validation": seq_result,
                    "blocked": True
                }
        
        # Verificar rate limit
        rate_limit_result = self.check_rate_limit(source_chain)
        if not rate_limit_result.get("allowed", False):
            self.stats["messages_blocked"] += 1
            self.blocked_messages.add(message_hash)
            return {
                "valid": False,
                "reason": rate_limit_result.get("reason", "Rate limit excedido"),
                "message_hash": message_hash,
                "rate_limit": rate_limit_result,
                "blocked": True
            }
        
        # Mensagem válida - registrar
        self.processed_messages[message_hash] = time.time()
        self.stats["messages_processed"] += 1
        
        return {
            "valid": True,
            "message_hash": message_hash,
            "source_chain": source_chain,
            "target_chain": target_chain,
            "sequence": sequence,
            "timestamp": datetime.now().isoformat(),
            "rate_limit": rate_limit_result,
            "sequence_validation": seq_result if sequence is not None else None
        }
    
    def get_stats(self) -> Dict:
        """Obter estatísticas do sistema"""
        return {
            **self.stats,
            "processed_messages_count": len(self.processed_messages),
            "blocked_messages_count": len(self.blocked_messages),
            "tracked_chains": list(self.sequence_tracker.keys())
        }
    
    def reset_stats(self):
        """Resetar estatísticas"""
        self.stats = {
            "messages_processed": 0,
            "messages_blocked": 0,
            "duplicate_detections": 0,
            "sequence_violations": 0,
            "rate_limit_hits": 0
        }
        self.processed_messages.clear()
        self.blocked_messages.clear()
        self.sequence_tracker.clear()
        self.rate_limit_history.clear()


# =============================================================================
# TESTE DO SISTEMA
# =============================================================================

if __name__ == "__main__":
    print("\n" + "="*70)
    print("🛡️ TESTANDO WORMHOLE PREVENTION SYSTEM")
    print("="*70 + "\n")
    
    prevention = WormholePreventionSystem()
    
    # Teste 1: Mensagem válida
    print("📌 Teste 1: Mensagem válida")
    result1 = prevention.validate_cross_chain_message(
        source_chain="polygon",
        target_chain="ethereum",
        message_data={"amount": 100, "recipient": "0xRecipient"},
        sequence=1
    )
    print(f"   Resultado: {'✅ Válida' if result1.get('valid') else '❌ Inválida'}")
    print(f"   Hash: {result1.get('message_hash', 'N/A')[:16]}...")
    
    # Teste 2: Tentativa de duplicação
    print("\n📌 Teste 2: Tentativa de duplicação")
    result2 = prevention.validate_cross_chain_message(
        source_chain="polygon",
        target_chain="ethereum",
        message_data={"amount": 100, "recipient": "0xRecipient"},
        sequence=2
    )
    print(f"   Resultado: {'✅ Válida' if result2.get('valid') else '❌ Bloqueada (esperado)'}")
    print(f"   Razão: {result2.get('reason', 'N/A')}")
    
    # Teste 3: Sequência inválida
    print("\n📌 Teste 3: Sequência inválida")
    result3 = prevention.validate_cross_chain_message(
        source_chain="polygon",
        target_chain="ethereum",
        message_data={"amount": 200, "recipient": "0xRecipient2"},
        sequence=1  # Menor que a última (2)
    )
    print(f"   Resultado: {'✅ Válida' if result3.get('valid') else '❌ Bloqueada (esperado)'}")
    print(f"   Razão: {result3.get('reason', 'N/A')}")
    
    # Teste 4: Rate limiting
    print("\n📌 Teste 4: Rate limiting")
    for i in range(12):  # Exceder limite de 10/min
        result4 = prevention.validate_cross_chain_message(
            source_chain="bitcoin",
            target_chain="polygon",
            message_data={"amount": i, "recipient": f"0xRecipient{i}"},
            sequence=i + 1
        )
        if not result4.get("valid"):
            print(f"   Mensagem {i+1}: ❌ Bloqueada por rate limit")
            print(f"   Razão: {result4.get('reason', 'N/A')}")
            break
    
    # Estatísticas
    print("\n📊 Estatísticas:")
    stats = prevention.get_stats()
    for key, value in stats.items():
        print(f"   {key}: {value}")
    
    print("\n✅ Testes concluídos!")

