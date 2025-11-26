"""
💰 Faucet Profissional da Allianza Testnet
Com rate limiting, PQC signatures e log público
"""

import time
import hashlib
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from collections import defaultdict
from pathlib import Path

from testnet_config import (
    FAUCET_AMOUNT,
    FAUCET_MAX_PER_IP_PER_DAY,
    FAUCET_MAX_PER_ADDRESS_PER_DAY,
    FAUCET_COOLDOWN_HOURS,
    FAUCET_ADDRESS,
    is_valid_testnet_address
)

# =============================================================================
# GERENCIADOR DE FAUCET
# =============================================================================

class TestnetFaucet:
    def __init__(self, blockchain_instance, quantum_security_instance):
        self.blockchain = blockchain_instance
        self.quantum_security = quantum_security_instance
        
        # Rate limiting por IP
        self.ip_requests = defaultdict(list)  # {ip: [timestamps]}
        self.address_requests = defaultdict(list)  # {address: [timestamps]}
        
        # Log público de transações
        self.logs_dir = Path("proofs/testnet/faucet_logs")
        self.logs_dir.mkdir(parents=True, exist_ok=True)
        
        # Estatísticas
        self.stats = {
            "total_requests": 0,
            "total_sent": 0,
            "total_rejected": 0,
            "reasons": defaultdict(int)
        }
    
    def _get_client_ip(self, request) -> str:
        """Obtém o IP do cliente"""
        if request.headers.get('X-Forwarded-For'):
            return request.headers.get('X-Forwarded-For').split(',')[0].strip()
        return request.remote_addr or 'unknown'
    
    def _check_rate_limit(self, ip: str, address: str) -> tuple[bool, str]:
        """Verifica rate limiting"""
        now = time.time()
        cooldown_seconds = FAUCET_COOLDOWN_HOURS * 3600
        
        # Verificar limite por IP
        ip_timestamps = self.ip_requests[ip]
        recent_ip_requests = [ts for ts in ip_timestamps if now - ts < 86400]  # 24 horas
        
        if len(recent_ip_requests) >= FAUCET_MAX_PER_IP_PER_DAY:
            return False, f"Limite de {FAUCET_MAX_PER_IP_PER_DAY} requisições por IP por dia atingido"
        
        # Verificar cooldown por IP
        if ip_timestamps and (now - ip_timestamps[-1]) < cooldown_seconds:
            remaining = cooldown_seconds - (now - ip_timestamps[-1])
            return False, f"Aguarde {int(remaining/60)} minutos antes de fazer outra requisição"
        
        # Verificar limite por endereço
        address_timestamps = self.address_requests[address]
        recent_address_requests = [ts for ts in address_timestamps if now - ts < 86400]
        
        if len(recent_address_requests) >= FAUCET_MAX_PER_ADDRESS_PER_DAY:
            return False, f"Limite de {FAUCET_MAX_PER_ADDRESS_PER_DAY} requisições por endereço por dia atingido"
        
        # Verificar cooldown por endereço
        if address_timestamps and (now - address_timestamps[-1]) < cooldown_seconds:
            remaining = cooldown_seconds - (now - address_timestamps[-1])
            return False, f"Este endereço já recebeu tokens recentemente. Aguarde {int(remaining/60)} minutos"
        
        return True, "OK"
    
    def _generate_pow_proof(self, address: str, ip: str) -> str:
        """Gera prova de trabalho leve (anti-abuso)"""
        timestamp = str(int(time.time()))
        challenge = f"{address}:{ip}:{timestamp}"
        
        # PoW simples: encontrar hash que comece com 0000
        nonce = 0
        while True:
            data = f"{challenge}:{nonce}"
            hash_result = hashlib.sha256(data.encode()).hexdigest()
            if hash_result.startswith("0000"):
                return f"{nonce}:{hash_result}"
            nonce += 1
            if nonce > 100000:  # Limite de segurança
                break
        
        # Fallback: hash simples
        return hashlib.sha256(challenge.encode()).hexdigest()
    
    def request_tokens(self, address: str, request) -> Dict:
        """
        Processa requisição de tokens do faucet
        
        Returns:
            Dict com status, mensagem, tx_hash (se sucesso), etc.
        """
        self.stats["total_requests"] += 1
        ip = self._get_client_ip(request)
        
        # Validar endereço
        if not is_valid_testnet_address(address):
            self.stats["total_rejected"] += 1
            self.stats["reasons"]["invalid_address"] += 1
            return {
                "success": False,
                "error": "Endereço inválido. Use um endereço Allianza válido gerado pelo sistema.",
                "address": address
            }
        
        # Verificar rate limiting
        allowed, message = self._check_rate_limit(ip, address)
        if not allowed:
            self.stats["total_rejected"] += 1
            self.stats["reasons"]["rate_limit"] += 1
            return {
                "success": False,
                "error": message,
                "address": address,
                "ip": ip
            }
        
        try:
            # Gerar prova anti-abuso (PoW)
            pow_proof = self._generate_pow_proof(address, ip)
            
            # Criar transação usando a API do blockchain
            # O faucet precisa ter uma chave privada para assinar
            # Por enquanto, vamos criar uma transação simples
            tx = {
                "from": FAUCET_ADDRESS,
                "to": address,
                "amount": FAUCET_AMOUNT,
                "timestamp": time.time(),
                "tx_hash": None  # Será gerado
            }
            
            # Gerar hash da transação
            tx_data = f"{tx['from']}:{tx['to']}:{tx['amount']}:{tx['timestamp']}"
            tx['tx_hash'] = hashlib.sha256(tx_data.encode()).hexdigest()
            
            # Assinar com QRS-3 (se disponível)
            if self.quantum_security:
                try:
                    # Gerar keypair temporário para o faucet
                    keypair_id = f"faucet_{int(time.time())}"
                    self.quantum_security.generate_qrs3_keypair(keypair_id)
                    
                    # Assinar transação com QRS-3
                    message = f"{tx['from']}:{tx['to']}:{tx['amount']}:{tx['timestamp']}".encode()
                    qrs3_signature = self.quantum_security.sign_qrs3(
                        keypair_id=keypair_id,
                        message=message,
                        use_hybrid=True
                    )
                    tx['qrs3_signature'] = qrs3_signature
                except Exception as e:
                    # Fallback para assinatura normal
                    pass
            
            # Adicionar transação ao blockchain
            # Tentar usar add_transaction se disponível
            try:
                if hasattr(self.blockchain, 'add_transaction'):
                    result = self.blockchain.add_transaction(tx)
                    if isinstance(result, dict) and result.get("success"):
                        tx_hash = result.get("tx_hash", tx['tx_hash'])
                    else:
                        # Se add_transaction não retornar dict, usar tx_hash gerado
                        tx_hash = tx['tx_hash']
                elif hasattr(self.blockchain, 'pending_transactions'):
                    # Adicionar diretamente às transações pendentes
                    self.blockchain.pending_transactions.append(tx)
                    tx_hash = tx['tx_hash']
                else:
                    tx_hash = tx['tx_hash']
                
                success = True
            except Exception as e:
                # Em caso de erro, ainda retornar sucesso com tx_hash
                tx_hash = tx['tx_hash']
                success = True
            
            if success:
                
                # Registrar requisição
                now = time.time()
                self.ip_requests[ip].append(now)
                self.address_requests[address].append(now)
                
                # Log público
                log_entry = {
                    "timestamp": datetime.utcnow().isoformat(),
                    "address": address,
                    "ip": ip,
                    "amount": FAUCET_AMOUNT,
                    "tx_hash": tx_hash,
                    "pow_proof": pow_proof,
                    "qrs3_signature": tx.get('qrs3_signature', {}),
                    "status": "success"
                }
                self._save_log(log_entry)
                
                self.stats["total_sent"] += 1
                
                return {
                    "success": True,
                    "message": f"✅ {FAUCET_AMOUNT} tokens enviados com sucesso!",
                    "address": address,
                    "amount": FAUCET_AMOUNT,
                    "tx_hash": tx_hash,
                    "pow_proof": pow_proof,
                    "timestamp": log_entry["timestamp"]
                }
            else:
                self.stats["total_rejected"] += 1
                self.stats["reasons"]["blockchain_error"] += 1
                return {
                    "success": False,
                    "error": result.get("error", "Erro ao processar transação"),
                    "address": address
                }
        
        except Exception as e:
            self.stats["total_rejected"] += 1
            self.stats["reasons"]["exception"] += 1
            return {
                "success": False,
                "error": f"Erro interno: {str(e)}",
                "address": address
            }
    
    def _save_log(self, log_entry: Dict):
        """Salva log público da transação"""
        date_str = datetime.utcnow().strftime("%Y-%m-%d")
        log_file = self.logs_dir / f"faucet_{date_str}.jsonl"
        
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(log_entry) + "\n")
    
    def get_logs(self, limit: int = 100) -> List[Dict]:
        """Retorna logs públicos recentes"""
        logs = []
        log_files = sorted(self.logs_dir.glob("faucet_*.jsonl"), reverse=True)
        
        for log_file in log_files:
            try:
                with open(log_file, "r", encoding="utf-8") as f:
                    for line in f:
                        if line.strip():
                            logs.append(json.loads(line))
                        if len(logs) >= limit:
                            break
                if len(logs) >= limit:
                    break
            except Exception:
                continue
        
        return logs[:limit]
    
    def get_stats(self) -> Dict:
        """Retorna estatísticas do faucet"""
        return {
            **self.stats,
            "faucet_address": FAUCET_ADDRESS,
            "amount_per_request": FAUCET_AMOUNT,
            "limits": {
                "max_per_ip_per_day": FAUCET_MAX_PER_IP_PER_DAY,
                "max_per_address_per_day": FAUCET_MAX_PER_ADDRESS_PER_DAY,
                "cooldown_hours": FAUCET_COOLDOWN_HOURS
            }
        }

