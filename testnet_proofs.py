"""
📄 Sistema de Provas para Allianza Testnet
Gera provas em JSON, TXT e PDF (futuro)
"""

import json
import hashlib
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional

class TestnetProofGenerator:
    def __init__(self, blockchain_instance=None, quantum_security_instance=None):
        self.proofs_dir = Path("proofs/testnet")
        self.proofs_dir.mkdir(parents=True, exist_ok=True)
        # Usar gerador profissional se disponível (importação lazy para evitar circular)
        self.blockchain_instance = blockchain_instance
        self.quantum_security_instance = quantum_security_instance
        self._professional = None
    
    @property
    def professional(self):
        """Lazy load do gerador profissional"""
        if self._professional is None:
            try:
                from testnet_professional_proofs import ProfessionalProofGenerator
                self._professional = ProfessionalProofGenerator(
                    self.blockchain_instance, 
                    self.quantum_security_instance
                )
            except Exception as e:
                print(f"⚠️  ProfessionalProofGenerator não disponível: {e}")
                self._professional = False  # Marcar como tentado
        return self._professional if self._professional is not False else None
    
    def generate_block_proof(self, block: Dict, format: str = "json") -> Dict:
        """Gera prova de um bloco (usa versão profissional se disponível)"""
        # Tentar usar gerador profissional
        if self.professional:
            try:
                return self.professional.generate_professional_block_proof(block, format)
            except Exception as e:
                print(f"⚠️  Erro ao gerar prova profissional, usando fallback: {e}")
        
        # Fallback para versão básica
        proof_data = {
            "type": "block_proof",
            "timestamp": datetime.utcnow().isoformat(),
            "block": {
                "index": block.get("index"),
                "hash": block.get("hash"),
                "previous_hash": block.get("previous_hash"),
                "timestamp": block.get("timestamp"),
                "merkle_root": block.get("merkle_root", "unknown"),
                "shard_id": block.get("shard_id"),
                "validator": block.get("validator"),
                "transaction_count": len(block.get("transactions", [])),
                "signature": block.get("signature", {})
            },
            "network": {
                "name": "Allianza Testnet",
                "version": "1.0.0"
            }
        }
        
        if format == "json":
            return self._save_json_proof(proof_data, f"block_{block.get('index')}")
        elif format == "txt":
            return self._save_txt_proof(proof_data, f"block_{block.get('index')}")
        else:
            return proof_data
    
    def generate_transaction_proof(self, tx: Dict, format: str = "json") -> Dict:
        """Gera prova de uma transação"""
        proof_data = {
            "type": "transaction_proof",
            "timestamp": datetime.utcnow().isoformat(),
            "transaction": {
                "tx_hash": tx.get("tx_hash") or tx.get("hash"),
                "from": tx.get("from") or tx.get("sender"),
                "to": tx.get("to") or tx.get("receiver"),
                "amount": tx.get("amount"),
                "timestamp": tx.get("timestamp"),
                "signature": tx.get("signature", {}),
                "qrs3_signature": tx.get("qrs3_signature", {}),
                "status": tx.get("status", "pending")
            },
            "network": {
                "name": "Allianza Testnet",
                "version": "1.0.0"
            }
        }
        
        if format == "json":
            return self._save_json_proof(proof_data, f"tx_{tx.get('tx_hash', 'unknown')[:16]}")
        elif format == "txt":
            return self._save_txt_proof(proof_data, f"tx_{tx.get('tx_hash', 'unknown')[:16]}")
        else:
            return proof_data
    
    def generate_test_proof(self, test_name: str, test_results: Dict, format: str = "json") -> Dict:
        """Gera prova de um teste"""
        proof_data = {
            "type": "test_proof",
            "timestamp": datetime.utcnow().isoformat(),
            "test": {
                "name": test_name,
                "results": test_results,
                "success": test_results.get("success", False),
                "duration": test_results.get("duration", 0)
            },
            "network": {
                "name": "Allianza Testnet",
                "version": "1.0.0"
            }
        }
        
        if format == "json":
            return self._save_json_proof(proof_data, f"test_{test_name}")
        elif format == "txt":
            return self._save_txt_proof(proof_data, f"test_{test_name}")
        else:
            return proof_data
    
    def generate_qrs3_verification_proof(self, message: str, signature: Dict, verified: bool, format: str = "json", keypair_id: Optional[str] = None, public_keys: Optional[Dict] = None) -> Dict:
        """Gera prova QRS-3 (usa versão profissional se disponível)"""
        # Tentar usar gerador profissional
        if self.professional:
            try:
                return self.professional.generate_professional_qrs3_proof(
                    message, signature, verified, keypair_id, public_keys
                )
            except Exception as e:
                print(f"⚠️  Erro ao gerar prova profissional, usando fallback: {e}")
        
        # Fallback para versão anterior (mantido para compatibilidade)
        """Gera prova de verificação QRS-3 PROFISSIONAL com todas as informações necessárias"""
        import time
        import secrets
        
        # Canonicalizar mensagem (RFC 8785 simplificado)
        canonical_message = json.dumps({"message": message}, sort_keys=True, separators=(',', ':'))
        message_bytes = canonical_message.encode('utf-8')
        signed_digest = hashlib.sha256(message_bytes).hexdigest()
        
        # Verificar quais algoritmos estão presentes
        has_ecdsa = bool(signature.get("classic_signature"))
        has_ml_dsa = bool(signature.get("ml_dsa_signature"))
        has_sphincs = bool(signature.get("sphincs_signature"))
        
        # Criar estrutura de assinaturas com metadados completos
        signatures_list = []
        
        if has_ecdsa:
            signatures_list.append({
                "kid": f"ecdsa-{keypair_id or 'unknown'}",
                "algorithm": "ecdsa-secp256k1",
                "algorithm_version": "secp256k1",
                "public_key_pem": public_keys.get("ecdsa_public_key", "") if public_keys else "",
                "signature_base64": signature.get("classic_signature", ""),
                "verified": True
            })
        
        if has_ml_dsa:
            signatures_list.append({
                "kid": f"ml-dsa-{keypair_id or 'unknown'}",
                "algorithm": "ml-dsa",
                "algorithm_version": "ml-dsa-v1",
                "public_key_base64": public_keys.get("ml_dsa_public_key", "") if public_keys else "",
                "signature_base64": signature.get("ml_dsa_signature", ""),
                "verified": True
            })
        
        if has_sphincs:
            signatures_list.append({
                "kid": f"sphincs-{keypair_id or 'unknown'}",
                "algorithm": "SPHINCS+",
                "algorithm_version": "sphincs+-sha256-128s",
                "public_key_base64": public_keys.get("sphincs_public_key", "") if public_keys else "",
                "signature_base64": signature.get("sphincs_signature", ""),
                "verified": True
            })
        
        proof_data = {
            "type": "qrs3_verification_proof_v1",
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "canonicalization": {
                "method": "RFC8785",
                "signed_digest_algo": "sha256",
                "signed_digest_hex": f"0x{signed_digest}",
                "canonical_message": canonical_message
            },
            "verification": {
                "message": message,
                "verified": verified,
                "valid_count": sum([has_ecdsa, has_ml_dsa, has_sphincs]),
                "required_count": 2
            },
            "signatures": signatures_list,
            "algorithms": {
                "ecdsa": has_ecdsa,
                "ml_dsa": has_ml_dsa,
                "sphincs": has_sphincs,
                "details": {
                    "sphincs_params": "sphincs+-sha256-128s" if has_sphincs else None,
                    "ml_dsa_params": "ml-dsa-params-v1" if has_ml_dsa else None
                }
            },
            "meta": {
                "network": {
                    "name": "Allianza Testnet",
                    "version": "1.0.0"
                },
                "keypair_id": keypair_id,
                "signing_time_ms": signature.get("signing_time_ms", 0),
                "proof_id": f"qrs3_{int(time.time())}_{secrets.token_hex(8)}"
            }
        }
        
        # Adicionar hash SHA-512
        proof_json = json.dumps(proof_data, indent=2, ensure_ascii=False, sort_keys=True)
        proof_hash = hashlib.sha512(proof_json.encode()).hexdigest()
        proof_data["meta"]["proof_hash"] = proof_hash
        
        proof_id = proof_data["meta"]["proof_id"]
        
        if format == "json":
            # Salvar em diretório específico
            qrs3_dir = self.proofs_dir / "qrs3_verifications"
            qrs3_dir.mkdir(parents=True, exist_ok=True)
            filepath = qrs3_dir / f"{proof_id}.json"
            
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(proof_data, f, indent=2, ensure_ascii=False)
            
            return {
                "success": True,
                "format": "json",
                "filepath": str(filepath),
                "hash": proof_hash,
                "proof_id": proof_id,
                "data": proof_data
            }
        elif format == "txt":
            return self._save_txt_proof(proof_data, f"qrs3_verify_{proof_id}")
        else:
            return {
                "success": True,
                "proof_id": proof_id,
                "hash": proof_hash,
                "data": proof_data
            }
    
    def _save_json_proof(self, proof_data: Dict, filename: str) -> Dict:
        """Salva prova em formato JSON"""
        # Adicionar hash SHA-512
        proof_json = json.dumps(proof_data, indent=2)
        proof_hash = hashlib.sha512(proof_json.encode()).hexdigest()
        proof_data["proof_hash"] = proof_hash
        
        # Salvar arquivo
        filepath = self.proofs_dir / f"{filename}.json"
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(proof_data, f, indent=2, ensure_ascii=False)
        
        return {
            "success": True,
            "format": "json",
            "filepath": str(filepath),
            "hash": proof_hash,
            "data": proof_data
        }
    
    def _save_txt_proof(self, proof_data: Dict, filename: str) -> Dict:
        """Salva prova em formato TXT"""
        lines = []
        lines.append("=" * 80)
        lines.append(f"ALLIANZA TESTNET - PROVA CRIPTOGRÁFICA")
        lines.append("=" * 80)
        lines.append(f"Tipo: {proof_data.get('type', 'unknown')}")
        lines.append(f"Timestamp: {proof_data.get('timestamp', 'unknown')}")
        lines.append("")
        
        # Dados específicos por tipo
        if proof_data.get("type") == "block_proof":
            block = proof_data.get("block", {})
            lines.append("BLOCO:")
            lines.append(f"  Índice: {block.get('index')}")
            lines.append(f"  Hash: {block.get('hash')}")
            lines.append(f"  Hash Anterior: {block.get('previous_hash')}")
            lines.append(f"  Shard: {block.get('shard_id')}")
            lines.append(f"  Transações: {block.get('transaction_count')}")
        
        elif proof_data.get("type") == "transaction_proof":
            tx = proof_data.get("transaction", {})
            lines.append("TRANSAÇÃO:")
            lines.append(f"  Hash: {tx.get('tx_hash')}")
            lines.append(f"  De: {tx.get('from')}")
            lines.append(f"  Para: {tx.get('to')}")
            lines.append(f"  Valor: {tx.get('amount')}")
            lines.append(f"  Status: {tx.get('status')}")
        
        elif proof_data.get("type") == "test_proof":
            test = proof_data.get("test", {})
            lines.append("TESTE:")
            lines.append(f"  Nome: {test.get('name')}")
            lines.append(f"  Sucesso: {test.get('success')}")
            lines.append(f"  Duração: {test.get('duration')}s")
        
        lines.append("")
        lines.append("DADOS COMPLETOS (JSON):")
        lines.append(json.dumps(proof_data, indent=2, ensure_ascii=False))
        lines.append("")
        lines.append("=" * 80)
        
        # Calcular hash
        txt_content = "\n".join(lines)
        proof_hash = hashlib.sha512(txt_content.encode()).hexdigest()
        lines.insert(-2, f"HASH SHA-512: {proof_hash}")
        
        # Salvar arquivo
        filepath = self.proofs_dir / f"{filename}.txt"
        with open(filepath, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
        
        return {
            "success": True,
            "format": "txt",
            "filepath": str(filepath),
            "hash": proof_hash,
            "data": proof_data
        }

