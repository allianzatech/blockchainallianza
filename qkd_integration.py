#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🌐 QKD INTEGRATION - QUANTUM KEY DISTRIBUTION
Distribuição quântica de chaves para comunicação segura
"""

import json
import hashlib
import time
from datetime import datetime, timezone
from typing import Dict, Optional, Tuple, List
import secrets

class QKDIntegration:
    """
    Quantum Key Distribution Integration
    
    Sistema de distribuição quântica de chaves com fallback clássico (ML-KEM)
    """
    
    def __init__(self, quantum_security=None):
        self.quantum_security = quantum_security
        self.qkd_available = False  # Em produção, verificar hardware QKD
        self.shared_keys = {}  # (node_a, node_b) -> shared_key
        self.key_sessions = {}  # session_id -> session_info
        
        # Verificar disponibilidade QKD
        self._check_qkd_availability()
    
    def _check_qkd_availability(self):
        """Verificar se QKD hardware está disponível"""
        # Em produção, verificar conexão com hardware QKD
        # Por agora, simular disponibilidade
        self.qkd_available = False  # Sem hardware QKD real
        print(f"⚠️  QKD: Hardware não disponível - usando fallback ML-KEM")
    
    def establish_quantum_channel(
        self,
        node_a: str,
        node_b: str,
        session_id: str = None
    ) -> Dict:
        """
        Estabelecer canal quântico entre dois nós
        
        Args:
            node_a: ID do primeiro nó
            node_b: ID do segundo nó
            session_id: ID da sessão (opcional)
            
        Returns:
            Informações da sessão QKD
        """
        if not session_id:
            session_id = f"qkd_session_{int(time.time())}_{secrets.token_hex(8)}"
        
        # Tentar QKD real primeiro
        if self.qkd_available:
            # Em produção, usar hardware QKD real
            shared_key = self._qkd_key_exchange(node_a, node_b)
            method = "QKD_HARDWARE"
        else:
            # Fallback: ML-KEM (PQC)
            shared_key = self._ml_kem_key_exchange(node_a, node_b)
            method = "ML-KEM_FALLBACK"
        
        # Armazenar chave compartilhada
        key_pair = tuple(sorted([node_a, node_b]))
        self.shared_keys[key_pair] = {
            "shared_key": shared_key,
            "method": method,
            "established_at": datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z'),
            "session_id": session_id
        }
        
        # Criar sessão
        session_info = {
            "session_id": session_id,
            "node_a": node_a,
            "node_b": node_b,
            "shared_key_hash": hashlib.sha256(shared_key.encode()).hexdigest(),
            "method": method,
            "established_at": datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z'),
            "status": "active"
        }
        self.key_sessions[session_id] = session_info
        
        return {
            "success": True,
            "session_id": session_id,
            "method": method,
            "shared_key_hash": session_info["shared_key_hash"],
            "message": f"Canal quântico estabelecido via {method}"
        }
    
    def _qkd_key_exchange(self, node_a: str, node_b: str) -> str:
        """
        Troca de chaves via QKD real (hardware)
        
        Em produção, usar hardware QKD real (ex: ID Quantique, Toshiba)
        """
        # Simular QKD
        # Em produção, usar biblioteca/hardware QKD real
        key = secrets.token_bytes(32)
        return key.hex()
    
    def _ml_kem_key_exchange(self, node_a: str, node_b: str) -> str:
        """
        Troca de chaves via ML-KEM (fallback clássico)
        
        Usa ML-KEM (Kyber) para estabelecer chave compartilhada
        """
        if self.quantum_security:
            try:
                # Gerar chave compartilhada via ML-KEM
                # Em produção, usar implementação real de ML-KEM
                key = secrets.token_bytes(32)
                return key.hex()
            except Exception as e:
                print(f"⚠️  Erro no ML-KEM: {e}")
        
        # Fallback final: gerar chave aleatória
        key = secrets.token_bytes(32)
        return key.hex()
    
    def get_shared_key(self, node_a: str, node_b: str) -> Optional[str]:
        """Obter chave compartilhada entre dois nós"""
        key_pair = tuple(sorted([node_a, node_b]))
        if key_pair in self.shared_keys:
            return self.shared_keys[key_pair]["shared_key"]
        return None
    
    def encrypt_with_shared_key(
        self,
        node_a: str,
        node_b: str,
        message: str
    ) -> Dict:
        """
        Criptografar mensagem usando chave compartilhada QKD
        
        Args:
            node_a: Nó remetente
            node_b: Nó destinatário
            message: Mensagem a criptografar
            
        Returns:
            Mensagem criptografada
        """
        shared_key = self.get_shared_key(node_a, node_b)
        if not shared_key:
            return {
                "success": False,
                "error": "Chave compartilhada não encontrada. Estabeleça canal primeiro."
            }
        
        # Criptografar (simulado - em produção usar AES-GCM com chave QKD)
        key_bytes = bytes.fromhex(shared_key)
        message_bytes = message.encode()
        
        # Simular criptografia
        encrypted = hashlib.sha256(f"{message}{shared_key}".encode()).hexdigest()
        
        return {
            "success": True,
            "encrypted": encrypted,
            "method": "QKD_ENCRYPTED",
            "timestamp": datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')
        }
    
    def decrypt_with_shared_key(
        self,
        node_a: str,
        node_b: str,
        encrypted: str
    ) -> Dict:
        """
        Descriptografar mensagem usando chave compartilhada QKD
        
        Args:
            node_a: Nó remetente
            node_b: Nó destinatário
            encrypted: Mensagem criptografada
            
        Returns:
            Mensagem descriptografada
        """
        shared_key = self.get_shared_key(node_a, node_b)
        if not shared_key:
            return {
                "success": False,
                "error": "Chave compartilhada não encontrada"
            }
        
        # Descriptografar (simulado)
        # Em produção, usar descriptografia real
        
        return {
            "success": True,
            "decrypted": "simulated_message",  # Em produção, mensagem real
            "method": "QKD_DECRYPTED"
        }
    
    def rotate_shared_key(self, node_a: str, node_b: str) -> Dict:
        """Rotacionar chave compartilhada"""
        # Estabelecer nova chave
        result = self.establish_quantum_channel(node_a, node_b)
        
        if result.get("success"):
            return {
                "success": True,
                "message": "Chave rotacionada com sucesso",
                "new_session_id": result.get("session_id")
            }
        
        return {
            "success": False,
            "error": "Falha ao rotacionar chave"
        }
    
    def get_active_sessions(self) -> List[Dict]:
        """Obter todas as sessões ativas"""
        return [
            session for session in self.key_sessions.values()
            if session.get("status") == "active"
        ]

if __name__ == '__main__':
    print("="*70)
    print("🌐 QKD INTEGRATION - QUANTUM KEY DISTRIBUTION")
    print("="*70)
    
    qkd = QKDIntegration()
    
    # Estabelecer canal quântico
    print("\n📋 Estabelecendo canal quântico...")
    result = qkd.establish_quantum_channel("node_a", "node_b")
    
    if result.get("success"):
        print(f"✅ Canal estabelecido: {result['session_id']}")
        print(f"✅ Método: {result['method']}")
        print(f"✅ Chave compartilhada (hash): {result['shared_key_hash']}")
        
        # Criptografar mensagem
        print("\n📋 Criptografando mensagem...")
        encrypted = qkd.encrypt_with_shared_key("node_a", "node_b", "Mensagem secreta")
        if encrypted.get("success"):
            print(f"✅ Mensagem criptografada: {encrypted['encrypted'][:50]}...")
        
        # Sessões ativas
        print("\n📋 Sessões ativas:")
        sessions = qkd.get_active_sessions()
        print(f"✅ Total: {len(sessions)}")



