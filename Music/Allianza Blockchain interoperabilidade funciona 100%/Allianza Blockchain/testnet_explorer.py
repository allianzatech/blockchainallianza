"""
🔍 Explorer da Allianza Testnet
Visualização de blocos, transações e estatísticas da rede
Versão melhorada com informações detalhadas de cross-chain, PQC e métricas avançadas
"""

from typing import Dict, List, Optional
from datetime import datetime, timedelta
import time

class TestnetExplorer:
    def __init__(self, blockchain_instance):
        self.blockchain = blockchain_instance
    
    def get_recent_blocks(self, limit: int = 20) -> List[Dict]:
        """Retorna blocos recentes"""
        try:
            blocks = []
            
            # Tentar obter blocos dos shards
            if hasattr(self.blockchain, 'shards'):
                # Coletar blocos de todos os shards
                for shard_id, shard_blocks in self.blockchain.shards.items():
                    if shard_blocks:
                        # Pegar os últimos blocos de cada shard
                        for block in shard_blocks[-limit:]:
                            blocks.append(block)
                
                # Ordenar por índice (mais recente primeiro)
                blocks.sort(key=lambda b: self._get_block_index(b), reverse=True)
                blocks = blocks[:limit]
            
            # Fallback: tentar chain direto
            elif hasattr(self.blockchain, 'chain'):
                blocks = self.blockchain.chain[-limit:] if len(self.blockchain.chain) > limit else self.blockchain.chain
            
            # Formatar blocos
            formatted_blocks = []
            for block in blocks:
                formatted_blocks.append(self._format_block(block))
            
            return formatted_blocks
        except Exception as e:
            import traceback
            traceback.print_exc()
            return []
    
    def _get_block_index(self, block) -> int:
        """Extrai o índice de um bloco"""
        if isinstance(block, dict):
            return block.get("index", 0)
        elif hasattr(block, 'index'):
            return block.index
        return 0
    
    def get_block_by_hash(self, block_hash: str) -> Optional[Dict]:
        """Retorna um bloco específico pelo hash"""
        try:
            if hasattr(self.blockchain, 'chain'):
                for block in self.blockchain.chain:
                    if isinstance(block, dict):
                        if block.get("hash") == block_hash:
                            return self._format_block(block)
                    elif hasattr(block, 'hash'):
                        if block.hash == block_hash:
                            return self._format_block(block)
            return None
        except Exception:
            return None
    
    def get_recent_transactions(self, limit: int = 50) -> List[Dict]:
        """Retorna transações recentes"""
        try:
            transactions = []
            
            # 1. Obter transações pendentes de TODOS os shards
            if hasattr(self.blockchain, 'pending_transactions'):
                if isinstance(self.blockchain.pending_transactions, dict):
                    # pending_transactions é um dicionário por shard: {0: [], 1: [], ...}
                    for shard_id, shard_pending in self.blockchain.pending_transactions.items():
                        if isinstance(shard_pending, list):
                            transactions.extend(shard_pending)
                elif isinstance(self.blockchain.pending_transactions, list):
                    # Fallback: se for lista (compatibilidade)
                    transactions.extend(self.blockchain.pending_transactions)
            
            # 2. Obter transações do banco de dados (transactions_history)
            try:
                from db_manager import DBManager
                db_manager = DBManager()
                db_txs = db_manager.execute_query(
                    "SELECT id, sender, receiver, amount, type, timestamp, network, is_public FROM transactions_history ORDER BY timestamp DESC LIMIT ?",
                    (limit * 2,)  # Buscar mais para ter opções
                )
                
                for tx_row in db_txs:
                    tx_id, sender, receiver, amount, tx_type, timestamp, network, is_public = tx_row
                    transactions.append({
                        "id": tx_id,
                        "sender": sender,
                        "receiver": receiver,
                        "amount": amount,
                        "type": tx_type,
                        "timestamp": timestamp,
                        "network": network or "allianza",
                        "is_public": bool(is_public) if is_public is not None else True
                    })
            except Exception as db_err:
                # Se falhar ao buscar do banco, continuar sem essas transações
                pass
            
            # 3. Obter transações dos blocos recentes
            blocks = self.get_recent_blocks(limit=10)
            for block in blocks:
                block_txs = block.get("transactions", [])
                if isinstance(block_txs, list):
                    transactions.extend(block_txs)
            
            # 4. Remover duplicatas (por id) e formatar
            seen_ids = set()
            formatted_txs = []
            for tx in transactions:
                tx_id = tx.get("id") or tx.get("tx_hash") or str(tx.get("hash", ""))
                if tx_id and tx_id not in seen_ids:
                    seen_ids.add(tx_id)
                    formatted_tx = self._format_transaction(tx)
                    if formatted_tx:
                        formatted_txs.append(formatted_tx)
            
            # 5. Ordenar por timestamp (mais recente primeiro)
            formatted_txs.sort(key=lambda x: x.get("timestamp", 0), reverse=True)
            
            return formatted_txs[:limit]
        except Exception as e:
            import traceback
            traceback.print_exc()
            return []
    
    def get_transaction_by_hash(self, tx_hash: str) -> Optional[Dict]:
        """Retorna uma transação específica pelo hash"""
        try:
            # Procurar em transações pendentes
            if hasattr(self.blockchain, 'pending_transactions'):
                for tx in self.blockchain.pending_transactions:
                    if isinstance(tx, dict):
                        if tx.get("tx_hash") == tx_hash or tx.get("hash") == tx_hash:
                            return self._format_transaction(tx)
            
            # Procurar nos blocos
            blocks = self.get_recent_blocks(limit=100)
            for block in blocks:
                transactions = block.get("transactions", [])
                for tx in transactions:
                    if isinstance(tx, dict):
                        if tx.get("tx_hash") == tx_hash or tx.get("hash") == tx_hash:
                            return self._format_transaction(tx)
            
            return None
        except Exception:
            return None
    
    def get_network_stats(self) -> Dict:
        """Retorna estatísticas detalhadas da rede"""
        try:
            blocks = self.get_recent_blocks(limit=1000)
            transactions = self.get_recent_transactions(limit=1000)
            
            # Calcular TPS (transações por segundo)
            now = datetime.utcnow().timestamp()
            last_24h_txs = [tx for tx in transactions if tx.get("timestamp", 0) > (now - 86400)]
            tps_24h = len(last_24h_txs) / 86400 if last_24h_txs else 0
            
            # TPS atual (última hora)
            last_hour_txs = [tx for tx in transactions if tx.get("timestamp", 0) > (now - 3600)]
            tps_current = len(last_hour_txs) / 3600 if last_hour_txs else 0
            
            # Calcular latência média (tempo entre blocos)
            block_times = []
            for i in range(1, len(blocks)):
                if blocks[i].get("timestamp") and blocks[i-1].get("timestamp"):
                    block_time = blocks[i].get("timestamp") - blocks[i-1].get("timestamp")
                    if block_time > 0:
                        block_times.append(block_time)
            
            avg_latency = sum(block_times) / len(block_times) if block_times else 0
            
            # Contar shards ativos
            shards = set()
            for block in blocks:
                shard_id = block.get("shard_id")
                if shard_id is not None:
                    shards.add(shard_id)
            
            # Estatísticas de cross-chain
            cross_chain_txs = [tx for tx in transactions if tx.get("is_cross_chain") or tx.get("source_chain")]
            cross_chain_count = len(cross_chain_txs)
            cross_chain_volume = sum(tx.get("amount", 0) for tx in cross_chain_txs)
            
            # Estatísticas de PQC
            quantum_signed_txs = [tx for tx in transactions if tx.get("qrs3_signature") or tx.get("quantum_signature")]
            quantum_signed_count = len(quantum_signed_txs)
            quantum_percentage = (quantum_signed_count / len(transactions) * 100) if transactions else 0
            
            # Validators
            validators = set()
            for block in blocks:
                validator = block.get("validator")
                if validator and validator != "unknown":
                    validators.add(validator)
            
            return {
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
                    "percentage": round((cross_chain_count / len(transactions) * 100) if transactions else 0, 2)
                },
                "quantum_security": {
                    "quantum_signed_count": quantum_signed_count,
                    "quantum_percentage": round(quantum_percentage, 2),
                    "qrs3_verified_count": sum(1 for tx in transactions if tx.get("qrs3_verified"))
                },
                "chains_supported": ["Allianza", "Polygon", "Bitcoin", "Ethereum", "BSC", "Solana", "Base", "Avalanche"],
                "last_block_time": blocks[0].get("timestamp_readable") if blocks else "N/A",
                "last_block_index": blocks[0].get("index") if blocks else 0
            }
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
    
    def _format_block(self, block) -> Dict:
        """Formata um bloco para exibição"""
        try:
            if isinstance(block, dict):
                transactions = block.get("transactions", [])
                timestamp = block.get("timestamp", 0)
            else:
                # Se for um objeto Block
                transactions = getattr(block, 'transactions', [])
                timestamp = getattr(block, 'timestamp', 0)
            
            # Formatar transações
            formatted_txs = []
            for tx in transactions:
                if tx:  # Ignorar None ou vazios
                    formatted_txs.append(self._format_transaction(tx))
            
            # Calcular estatísticas do bloco
            total_amount = 0.0
            cross_chain_count = 0
            quantum_signed_count = 0
            
            for tx in formatted_txs:
                # Total amount
                tx_amount = tx.get("amount", 0)
                if isinstance(tx_amount, (int, float)):
                    total_amount += float(tx_amount)
                
                # Cross-chain count
                if tx.get("is_cross_chain") or tx.get("source_chain"):
                    cross_chain_count += 1
                
                # Quantum signed count
                if tx.get("qrs3_signature") or tx.get("quantum_signature") or tx.get("qrs3_verified"):
                    quantum_signed_count += 1
            
            # Criar objeto statistics
            statistics = {
                "total_amount": total_amount,
                "cross_chain_count": cross_chain_count,
                "quantum_signed_count": quantum_signed_count,
                "avg_amount": total_amount / len(formatted_txs) if formatted_txs else 0
            }
            
            # Estimar tamanho do bloco
            size_bytes = 256  # Tamanho base do bloco
            size_bytes += len(formatted_txs) * 200  # ~200 bytes por transação
            
            if isinstance(block, dict):
                return {
                    "index": block.get("index", 0),
                    "hash": block.get("hash", "unknown"),
                    "previous_hash": block.get("previous_hash", "unknown"),
                    "timestamp": timestamp,
                    "timestamp_readable": datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S") if timestamp else "unknown",
                    "merkle_root": block.get("merkle_root", "unknown"),
                    "shard_id": block.get("shard_id", 0),
                    "validator": block.get("validator", "unknown"),
                    "transaction_count": len(formatted_txs),
                    "transactions": formatted_txs,
                    "signature": block.get("signature", {}),
                    "qrs3_verified": self._check_qrs3_signature(block.get("signature", {})),
                    "statistics": statistics,
                    "size_bytes": size_bytes
                }
            else:
                # Se for um objeto Block
                # Calcular estatísticas (mesmo cálculo acima)
                total_amount = 0.0
                cross_chain_count = 0
                quantum_signed_count = 0
                
                for tx in formatted_txs:
                    tx_amount = tx.get("amount", 0)
                    if isinstance(tx_amount, (int, float)):
                        total_amount += float(tx_amount)
                    if tx.get("is_cross_chain") or tx.get("source_chain"):
                        cross_chain_count += 1
                    if tx.get("qrs3_signature") or tx.get("quantum_signature") or tx.get("qrs3_verified"):
                        quantum_signed_count += 1
                
                statistics = {
                    "total_amount": total_amount,
                    "cross_chain_count": cross_chain_count,
                    "quantum_signed_count": quantum_signed_count,
                    "avg_amount": total_amount / len(formatted_txs) if formatted_txs else 0
                }
                
                size_bytes = 256 + (len(formatted_txs) * 200)
                
                return {
                    "index": getattr(block, 'index', 0),
                    "hash": getattr(block, 'hash', 'unknown'),
                    "previous_hash": getattr(block, 'previous_hash', 'unknown'),
                    "timestamp": timestamp,
                    "timestamp_readable": datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S") if timestamp else "unknown",
                    "merkle_root": getattr(block, 'merkle_root', 'unknown'),
                    "shard_id": getattr(block, 'shard_id', 0),
                    "validator": getattr(block, 'validator', 'unknown'),
                    "transaction_count": len(formatted_txs),
                    "transactions": formatted_txs,
                    "signature": getattr(block, 'signature', {}),
                    "qrs3_verified": self._check_qrs3_signature(getattr(block, 'signature', {})),
                    "statistics": statistics,
                    "size_bytes": size_bytes
                }
        except Exception as e:
            # Em caso de erro, retornar bloco básico
            import traceback
            traceback.print_exc()
            return {
                "index": 0,
                "hash": "error",
                "previous_hash": "unknown",
                "timestamp": 0,
                "timestamp_readable": "unknown",
                "merkle_root": "unknown",
                "shard_id": 0,
                "validator": "unknown",
                "transaction_count": 0,
                "transactions": [],
                "signature": {},
                "qrs3_verified": False,
                "statistics": {
                    "total_amount": 0.0,
                    "cross_chain_count": 0,
                    "quantum_signed_count": 0,
                    "avg_amount": 0.0
                },
                "size_bytes": 256
            }
    
    def _format_transaction(self, tx: Dict) -> Dict:
        """Formata uma transação para exibição com informações detalhadas"""
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
                
                # Formatar timestamp
                timestamp_readable = datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S") if timestamp else "unknown"
                timestamp_relative = self._get_relative_time(timestamp)
                
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
                    "signature": tx.get("signature", {}),
                    "qrs3_signature": quantum_signature_info,
                    "qrs3_verified": self._check_qrs3_signature(quantum_signature_info),
                    
                    # NOVAS INFORMAÇÕES
                    "is_cross_chain": is_cross_chain,
                    "source_chain": source_chain,
                    "target_chain": target_chain,
                    "has_quantum_signature": has_quantum_signature,
                    "quantum_algorithm": quantum_signature_info.get("algorithm", "N/A") if isinstance(quantum_signature_info, dict) else "N/A",
                    "gas_used": tx.get("gas_used", 0),
                    "gas_price": tx.get("gas_price", 0),
                    "gas_cost": (tx.get("gas_used", 0) * tx.get("gas_price", 0)) if tx.get("gas_used") and tx.get("gas_price") else 0,
                    "confirmations": tx.get("confirmations", 0),
                    "block_number": tx.get("block_number"),
                    "explorer_url": self._get_explorer_url(tx_hash, source_chain) if is_cross_chain else None,
                    "fee": tx.get("fee", 0),
                    "nonce": tx.get("nonce", 0)
                }
            else:
                return {
                    "tx_hash": getattr(tx, 'tx_hash', 'unknown'),
                    "from": getattr(tx, 'sender', 'unknown'),
                    "to": getattr(tx, 'receiver', 'unknown'),
                    "amount": getattr(tx, 'amount', 0),
                    "timestamp": getattr(tx, 'timestamp', 0),
                    "status": "pending",
                    "signature": {},
                    "qrs3_signature": {},
                    "qrs3_verified": False,
                    "is_cross_chain": False,
                    "has_quantum_signature": False
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
    
    def _check_qrs3_signature(self, signature: Dict) -> bool:
        """Verifica se uma assinatura QRS-3 é válida"""
        if not signature or not isinstance(signature, dict):
            return False
        
        # Verificar se tem pelo menos 2 assinaturas válidas
        valid_count = 0
        if signature.get("ecdsa"):
            valid_count += 1
        if signature.get("ml_dsa", {}).get("valid", False):
            valid_count += 1
        if signature.get("sphincs", {}).get("valid", False):
            valid_count += 1
        
        return valid_count >= 2
    
    def _get_blocks_from_db(self, limit: int) -> List[Dict]:
        """Tenta obter blocos do banco de dados"""
        try:
            if hasattr(self.blockchain, 'db_manager'):
                # Implementar query ao banco
                return []
        except Exception:
            pass
        return []

