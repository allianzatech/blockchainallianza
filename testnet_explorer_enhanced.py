#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔍 EXPLORER MELHORADO - Allianza Testnet
Versão aprimorada com informações detalhadas de cross-chain, PQC, e métricas avançadas
"""

from typing import Dict, List, Optional
from datetime import datetime, timedelta
import time

class EnhancedTestnetExplorer:
    """Explorer melhorado com informações detalhadas"""
    
    def __init__(self, blockchain_instance, bridge_instance=None, quantum_security_instance=None):
        self.blockchain = blockchain_instance
        self.bridge = bridge_instance
        self.quantum_security = quantum_security_instance
        
        # Cache de estatísticas
        self._stats_cache = {}
        self._cache_timestamp = 0
        self._cache_ttl = 30  # 30 segundos
    
    # =========================================================================
    # MÉTODOS MELHORADOS DE BLOCOS
    # =========================================================================
    
    def get_recent_blocks(self, limit: int = 20) -> List[Dict]:
        """Retorna blocos recentes com informações detalhadas"""
        try:
            blocks = []
            
            # Tentar obter blocos dos shards
            if hasattr(self.blockchain, 'shards'):
                for shard_id, shard_blocks in self.blockchain.shards.items():
                    if shard_blocks:
                        for block in shard_blocks[-limit:]:
                            blocks.append(block)
                
                blocks.sort(key=lambda b: self._get_block_index(b), reverse=True)
                blocks = blocks[:limit]
            
            elif hasattr(self.blockchain, 'chain'):
                blocks = self.blockchain.chain[-limit:] if len(self.blockchain.chain) > limit else self.blockchain.chain
            
            # Formatar blocos com informações detalhadas
            formatted_blocks = []
            for block in blocks:
                formatted_blocks.append(self._format_block_enhanced(block))
            
            return formatted_blocks
        except Exception as e:
            import traceback
            traceback.print_exc()
            return []
    
    def _format_block_enhanced(self, block) -> Dict:
        """Formata bloco com informações detalhadas"""
        try:
            if isinstance(block, dict):
                transactions = block.get("transactions", [])
                timestamp = block.get("timestamp", 0)
                index = block.get("index", 0)
                hash_val = block.get("hash", "unknown")
            else:
                transactions = getattr(block, 'transactions', [])
                timestamp = getattr(block, 'timestamp', 0)
                index = getattr(block, 'index', 0)
                hash_val = getattr(block, 'hash', 'unknown')
            
            # Formatar transações
            formatted_txs = []
            cross_chain_count = 0
            quantum_signed_count = 0
            total_amount = 0
            
            for tx in transactions:
                if tx:
                    formatted_tx = self._format_transaction_enhanced(tx)
                    formatted_txs.append(formatted_tx)
                    
                    # Estatísticas
                    if formatted_tx.get("is_cross_chain"):
                        cross_chain_count += 1
                    if formatted_tx.get("has_quantum_signature"):
                        quantum_signed_count += 1
                    total_amount += formatted_tx.get("amount", 0)
            
            # Informações do bloco
            block_info = {
                "index": index,
                "hash": hash_val,
                "hash_short": hash_val[:16] + "..." + hash_val[-8:] if len(hash_val) > 24 else hash_val,
                "previous_hash": block.get("previous_hash", "unknown") if isinstance(block, dict) else getattr(block, 'previous_hash', 'unknown'),
                "timestamp": timestamp,
                "timestamp_readable": datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S") if timestamp else "unknown",
                "timestamp_relative": self._get_relative_time(timestamp),
                "merkle_root": block.get("merkle_root", "unknown") if isinstance(block, dict) else getattr(block, 'merkle_root', 'unknown'),
                "shard_id": block.get("shard_id", 0) if isinstance(block, dict) else getattr(block, 'shard_id', 0),
                "validator": block.get("validator", "unknown") if isinstance(block, dict) else getattr(block, 'validator', 'unknown'),
                "transaction_count": len(formatted_txs),
                "transactions": formatted_txs,
                "signature": block.get("signature", {}) if isinstance(block, dict) else getattr(block, 'signature', {}),
                "qrs3_verified": self._check_qrs3_signature(block.get("signature", {}) if isinstance(block, dict) else getattr(block, 'signature', {})),
                
                # NOVAS INFORMAÇÕES
                "statistics": {
                    "cross_chain_count": cross_chain_count,
                    "quantum_signed_count": quantum_signed_count,
                    "total_amount": total_amount,
                    "avg_amount": total_amount / len(formatted_txs) if formatted_txs else 0
                },
                "size_bytes": self._estimate_block_size(block, formatted_txs),
                "gas_used": block.get("gas_used", 0) if isinstance(block, dict) else getattr(block, 'gas_used', 0),
                "gas_limit": block.get("gas_limit", 0) if isinstance(block, dict) else getattr(block, 'gas_limit', 0),
                "difficulty": block.get("difficulty", 0) if isinstance(block, dict) else getattr(block, 'difficulty', 0),
                "nonce": block.get("nonce", 0) if isinstance(block, dict) else getattr(block, 'nonce', 0)
            }
            
            return block_info
        except Exception as e:
            return {
                "index": 0,
                "hash": "error",
                "error": str(e),
                "transaction_count": 0,
                "transactions": []
            }
    
    # =========================================================================
    # MÉTODOS MELHORADOS DE TRANSAÇÕES
    # =========================================================================
    
    def get_recent_transactions(self, limit: int = 50) -> List[Dict]:
        """Retorna transações recentes com informações detalhadas"""
        try:
            # Obter transações pendentes
            pending = []
            if hasattr(self.blockchain, 'pending_transactions'):
                pending = self.blockchain.pending_transactions[:limit]
            
            # Obter transações dos blocos
            blocks = self.get_recent_blocks(limit=10)
            transactions = []
            
            for block in blocks:
                block_txs = block.get("transactions", [])
                if isinstance(block_txs, list):
                    transactions.extend(block_txs)
            
            # Adicionar pendentes
            transactions.extend(pending)
            
            # Obter transações cross-chain do bridge
            if self.bridge:
                bridge_txs = self._get_bridge_transactions(limit=20)
                transactions.extend(bridge_txs)
            
            # Formatar
            formatted_txs = []
            for tx in transactions[:limit]:
                formatted_txs.append(self._format_transaction_enhanced(tx))
            
            # Ordenar por timestamp
            formatted_txs.sort(key=lambda x: x.get("timestamp", 0), reverse=True)
            
            return formatted_txs[:limit]
        except Exception as e:
            return []
    
    def _format_transaction_enhanced(self, tx) -> Dict:
        """Formata transação com informações detalhadas"""
        try:
            if isinstance(tx, dict):
                tx_hash = tx.get("tx_hash") or tx.get("hash", "unknown")
                from_addr = tx.get("from") or tx.get("sender", "unknown")
                to_addr = tx.get("to") or tx.get("receiver", "unknown")
                amount = tx.get("amount", 0)
                timestamp = tx.get("timestamp", 0)
                status = tx.get("status", "pending")
                
                # Verificar se é cross-chain
                is_cross_chain = tx.get("is_cross_chain", False) or tx.get("source_chain") is not None
                source_chain = tx.get("source_chain")
                target_chain = tx.get("target_chain")
                
                # Verificar assinatura quântica
                has_quantum_signature = bool(tx.get("quantum_signature") or tx.get("qrs3_signature"))
                quantum_signature_info = tx.get("quantum_signature") or tx.get("qrs3_signature", {})
                
                # Informações de gas
                gas_used = tx.get("gas_used", 0)
                gas_price = tx.get("gas_price", 0)
                gas_limit = tx.get("gas_limit", 0)
                
                # Informações de confirmações
                confirmations = tx.get("confirmations", 0)
                block_number = tx.get("block_number")
                
            else:
                tx_hash = getattr(tx, 'tx_hash', 'unknown')
                from_addr = getattr(tx, 'sender', 'unknown')
                to_addr = getattr(tx, 'receiver', 'unknown')
                amount = getattr(tx, 'amount', 0)
                timestamp = getattr(tx, 'timestamp', 0)
                status = "pending"
                is_cross_chain = False
                source_chain = None
                target_chain = None
                has_quantum_signature = False
                quantum_signature_info = {}
                gas_used = 0
                gas_price = 0
                gas_limit = 0
                confirmations = 0
                block_number = None
            
            # Formatar timestamp
            timestamp_readable = datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S") if timestamp else "unknown"
            timestamp_relative = self._get_relative_time(timestamp)
            
            # Verificar QRS-3
            qrs3_verified = self._check_qrs3_signature(quantum_signature_info)
            
            return {
                "tx_hash": tx_hash,
                "tx_hash_short": tx_hash[:16] + "..." + tx_hash[-8:] if len(tx_hash) > 24 else tx_hash,
                "from": from_addr,
                "from_short": from_addr[:10] + "..." + from_addr[-6:] if len(from_addr) > 16 else from_addr,
                "to": to_addr,
                "to_short": to_addr[:10] + "..." + to_addr[-6:] if len(to_addr) > 16 else to_addr,
                "amount": amount,
                "amount_formatted": self._format_amount(amount),
                "timestamp": timestamp,
                "timestamp_readable": timestamp_readable,
                "timestamp_relative": timestamp_relative,
                "status": status,
                "status_color": self._get_status_color(status),
                "signature": tx.get("signature", {}) if isinstance(tx, dict) else {},
                "qrs3_signature": quantum_signature_info,
                "qrs3_verified": qrs3_verified,
                
                # NOVAS INFORMAÇÕES
                "is_cross_chain": is_cross_chain,
                "source_chain": source_chain,
                "target_chain": target_chain,
                "has_quantum_signature": has_quantum_signature,
                "quantum_algorithm": quantum_signature_info.get("algorithm", "N/A") if isinstance(quantum_signature_info, dict) else "N/A",
                "gas_used": gas_used,
                "gas_price": gas_price,
                "gas_limit": gas_limit,
                "gas_cost": gas_used * gas_price if gas_used and gas_price else 0,
                "confirmations": confirmations,
                "block_number": block_number,
                "explorer_url": self._get_explorer_url(tx_hash, source_chain) if is_cross_chain else None,
                "fee": tx.get("fee", 0) if isinstance(tx, dict) else 0,
                "nonce": tx.get("nonce", 0) if isinstance(tx, dict) else 0
            }
        except Exception as e:
            return {
                "tx_hash": "error",
                "from": "unknown",
                "to": "unknown",
                "amount": 0,
                "timestamp": 0,
                "status": "error",
                "error": str(e)
            }
    
    # =========================================================================
    # ESTATÍSTICAS MELHORADAS
    # =========================================================================
    
    def get_network_stats(self) -> Dict:
        """Retorna estatísticas detalhadas da rede"""
        # Verificar cache
        now = time.time()
        if (now - self._cache_timestamp) < self._cache_ttl and self._stats_cache:
            return self._stats_cache
        
        try:
            blocks = self.get_recent_blocks(limit=1000)
            transactions = self.get_recent_transactions(limit=1000)
            
            # Calcular TPS
            now_ts = datetime.utcnow().timestamp()
            last_24h_txs = [tx for tx in transactions if tx.get("timestamp", 0) > (now_ts - 86400)]
            tps_24h = len(last_24h_txs) / 86400 if last_24h_txs else 0
            
            # TPS atual (última hora)
            last_hour_txs = [tx for tx in transactions if tx.get("timestamp", 0) > (now_ts - 3600)]
            tps_current = len(last_hour_txs) / 3600 if last_hour_txs else 0
            
            # Latência média
            block_times = []
            for i in range(1, len(blocks)):
                if blocks[i].get("timestamp") and blocks[i-1].get("timestamp"):
                    block_time = blocks[i].get("timestamp") - blocks[i-1].get("timestamp")
                    if block_time > 0:
                        block_times.append(block_time)
            
            avg_latency = sum(block_times) / len(block_times) if block_times else 0
            
            # Shards ativos
            shards = set()
            for block in blocks:
                shard_id = block.get("shard_id")
                if shard_id is not None:
                    shards.add(shard_id)
            
            # Estatísticas de cross-chain
            cross_chain_txs = [tx for tx in transactions if tx.get("is_cross_chain")]
            cross_chain_count = len(cross_chain_txs)
            cross_chain_volume = sum(tx.get("amount", 0) for tx in cross_chain_txs)
            
            # Estatísticas de PQC
            quantum_signed_txs = [tx for tx in transactions if tx.get("has_quantum_signature")]
            quantum_signed_count = len(quantum_signed_txs)
            quantum_percentage = (quantum_signed_count / len(transactions) * 100) if transactions else 0
            
            # Estatísticas de gas
            total_gas_used = sum(tx.get("gas_used", 0) for tx in transactions)
            avg_gas_per_tx = total_gas_used / len(transactions) if transactions else 0
            
            # Validators
            validators = set()
            for block in blocks:
                validator = block.get("validator")
                if validator and validator != "unknown":
                    validators.add(validator)
            
            stats = {
                "total_blocks": len(blocks) if blocks else 0,
                "total_transactions": len(transactions) if transactions else 0,
                "pending_transactions": len(self.blockchain.pending_transactions) if hasattr(self.blockchain, 'pending_transactions') else 0,
                "tps_current": round(tps_current, 2),
                "tps_24h_avg": round(tps_24h, 2),
                "latency_avg_ms": round(avg_latency * 1000, 2) if avg_latency else 0,
                "active_shards": len(shards),
                "validators_online": len(validators) if validators else 1,
                "network_status": "operational",
                
                # NOVAS ESTATÍSTICAS
                "cross_chain": {
                    "total_transactions": cross_chain_count,
                    "total_volume": cross_chain_volume,
                    "percentage": (cross_chain_count / len(transactions) * 100) if transactions else 0
                },
                "quantum_security": {
                    "quantum_signed_count": quantum_signed_count,
                    "quantum_percentage": round(quantum_percentage, 2),
                    "qrs3_verified_count": sum(1 for tx in transactions if tx.get("qrs3_verified"))
                },
                "gas": {
                    "total_gas_used": total_gas_used,
                    "avg_gas_per_tx": round(avg_gas_per_tx, 0),
                    "total_gas_cost": sum(tx.get("gas_cost", 0) for tx in transactions)
                },
                "chains_supported": self._get_supported_chains(),
                "last_block_time": blocks[0].get("timestamp_readable") if blocks else "N/A",
                "last_block_index": blocks[0].get("index") if blocks else 0
            }
            
            # Atualizar cache
            self._stats_cache = stats
            self._cache_timestamp = now
            
            return stats
        except Exception as e:
            return {
                "total_blocks": 0,
                "total_transactions": 0,
                "pending_transactions": 0,
                "tps_current": 0,
                "tps_24h_avg": 0,
                "latency_avg_ms": 0,
                "active_shards": 0,
                "validators_online": 0,
                "network_status": "unknown",
                "error": str(e)
            }
    
    # =========================================================================
    # MÉTODOS AUXILIARES
    # =========================================================================
    
    def _get_bridge_transactions(self, limit: int = 20) -> List[Dict]:
        """Obtém transações do bridge cross-chain"""
        transactions = []
        
        if not self.bridge:
            return transactions
        
        try:
            # Obter transações pendentes do bridge
            if hasattr(self.bridge, 'pending_bridges'):
                for bridge_id, bridge_data in list(self.bridge.pending_bridges.items())[:limit]:
                    transactions.append({
                        "tx_hash": bridge_id,
                        "hash": bridge_id,
                        "is_cross_chain": True,
                        "source_chain": bridge_data.get("source_chain"),
                        "target_chain": bridge_data.get("target_chain"),
                        "amount": bridge_data.get("amount", 0),
                        "status": bridge_data.get("status", "pending"),
                        "timestamp": bridge_data.get("timestamp", time.time())
                    })
            
            # Obter histórico do bridge
            if hasattr(self.bridge, 'bridge_history'):
                for bridge_tx in list(self.bridge.bridge_history)[-limit:]:
                    if isinstance(bridge_tx, dict):
                        transactions.append(bridge_tx)
        except Exception as e:
            pass
        
        return transactions
    
    def _get_supported_chains(self) -> List[str]:
        """Retorna lista de chains suportadas"""
        # Lista completa de todas as blockchains suportadas (11 total)
        chains = [
            "Bitcoin",
            "Ethereum", 
            "Polygon",
            "BSC",
            "Solana",
            "Cosmos",
            "Avalanche",
            "Base",
            "Cardano",
            "Polkadot",
            "Allianza"
        ]
        
        return chains
    
    def _get_relative_time(self, timestamp: float) -> str:
        """Retorna tempo relativo (ex: 'há 2 minutos')"""
        if not timestamp:
            return "unknown"
        
        try:
            delta = datetime.now() - datetime.fromtimestamp(timestamp)
            
            if delta.total_seconds() < 60:
                return f"há {int(delta.total_seconds())}s"
            elif delta.total_seconds() < 3600:
                return f"há {int(delta.total_seconds() / 60)}min"
            elif delta.total_seconds() < 86400:
                return f"há {int(delta.total_seconds() / 3600)}h"
            else:
                return f"há {int(delta.total_seconds() / 86400)}d"
        except:
            return "unknown"
    
    def _format_amount(self, amount: float) -> str:
        """Formata valor de forma legível"""
        if amount >= 1_000_000:
            return f"{amount / 1_000_000:.2f}M"
        elif amount >= 1_000:
            return f"{amount / 1_000:.2f}K"
        else:
            return f"{amount:.6f}"
    
    def _get_status_color(self, status: str) -> str:
        """Retorna cor do status"""
        colors = {
            "confirmed": "green",
            "pending": "yellow",
            "failed": "red",
            "error": "red"
        }
        return colors.get(status.lower(), "gray")
    
    def _get_explorer_url(self, tx_hash: str, chain: str = None) -> Optional[str]:
        """Retorna URL do explorer externo"""
        if not chain:
            return None
        
        explorers = {
            "polygon": f"https://amoy.polygonscan.com/tx/{tx_hash}",
            "ethereum": f"https://sepolia.etherscan.io/tx/{tx_hash}",
            "bsc": f"https://testnet.bscscan.com/tx/{tx_hash}",
            "bitcoin": f"https://blockstream.info/testnet/tx/{tx_hash}",
            "solana": f"https://explorer.solana.com/tx/{tx_hash}?cluster=testnet",
            "base": f"https://sepolia.basescan.org/tx/{tx_hash}",
            "avalanche": f"https://testnet.snowtrace.io/tx/{tx_hash}"
        }
        
        return explorers.get(chain.lower())
    
    def _estimate_block_size(self, block, transactions: List[Dict]) -> int:
        """Estima tamanho do bloco em bytes"""
        # Estimativa básica
        base_size = 256  # Header
        tx_size = len(transactions) * 128  # ~128 bytes por transação
        return base_size + tx_size
    
    def _get_block_index(self, block) -> int:
        """Extrai o índice de um bloco"""
        if isinstance(block, dict):
            return block.get("index", 0)
        elif hasattr(block, 'index'):
            return block.index
        return 0
    
    def _check_qrs3_signature(self, signature: Dict) -> bool:
        """Verifica se uma assinatura QRS-3 é válida"""
        if not signature or not isinstance(signature, dict):
            return False
        
        valid_count = 0
        if signature.get("ecdsa"):
            valid_count += 1
        if signature.get("ml_dsa", {}).get("valid", False):
            valid_count += 1
        if signature.get("sphincs", {}).get("valid", False):
            valid_count += 1
        
        return valid_count >= 2
    
    # =========================================================================
    # MÉTODOS DE BUSCA
    # =========================================================================
    
    def search_block(self, query: str) -> Optional[Dict]:
        """Busca bloco por hash ou índice"""
        try:
            # Tentar como índice
            if query.isdigit():
                index = int(query)
                blocks = self.get_recent_blocks(limit=10000)
                for block in blocks:
                    if block.get("index") == index:
                        return block
            
            # Tentar como hash
            blocks = self.get_recent_blocks(limit=10000)
            for block in blocks:
                if block.get("hash", "").startswith(query.lower()):
                    return block
            
            return None
        except:
            return None
    
    def search_transaction(self, query: str) -> Optional[Dict]:
        """Busca transação por hash"""
        try:
            transactions = self.get_recent_transactions(limit=10000)
            for tx in transactions:
                tx_hash = tx.get("tx_hash", "")
                if tx_hash.startswith(query.lower()):
                    return tx
            return None
        except:
            return None
    
    def get_address_info(self, address: str) -> Dict:
        """Retorna informações de um endereço"""
        try:
            transactions = self.get_recent_transactions(limit=10000)
            
            # Filtrar transações do endereço
            sent_txs = [tx for tx in transactions if tx.get("from", "").lower() == address.lower()]
            received_txs = [tx for tx in transactions if tx.get("to", "").lower() == address.lower()]
            
            # Calcular saldo (simulado)
            total_sent = sum(tx.get("amount", 0) for tx in sent_txs)
            total_received = sum(tx.get("amount", 0) for tx in received_txs)
            balance = total_received - total_sent
            
            return {
                "address": address,
                "balance": balance,
                "total_sent": total_sent,
                "total_received": total_received,
                "transaction_count": len(sent_txs) + len(received_txs),
                "sent_count": len(sent_txs),
                "received_count": len(received_txs),
                "first_seen": min([tx.get("timestamp", 0) for tx in sent_txs + received_txs]) if (sent_txs or received_txs) else 0,
                "last_seen": max([tx.get("timestamp", 0) for tx in sent_txs + received_txs]) if (sent_txs or received_txs) else 0
            }
        except Exception as e:
            return {
                "address": address,
                "error": str(e)
            }



