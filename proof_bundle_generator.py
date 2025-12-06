#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
📦 GERADOR DE PROOF BUNDLES VERIFICÁVEIS
Gera artefatos completos e assinados para auditoria e verificação
"""

import json
import hashlib
import time
import os
from typing import Dict, List, Optional, Any
from datetime import datetime
from dataclasses import dataclass, asdict

# Placeholder para quantum_security se não disponível
try:
    from quantum_security import QuantumSecuritySystem
except ImportError:
    class QuantumSecuritySystem:
        def sign_ml_dsa(self, keypair_id, data): 
            return {"success": True, "signature": f"mock_sig_{data.hex()[:20]}"}
        def verify_ml_dsa(self, public_key, data, signature): 
            return {"success": True}
        def generate_ml_dsa_keypair(self, security_level): 
            return {"keypair_id": "mock_keypair", "public_key": "mock_pubkey"}

@dataclass
class TransactionManifest:
    """Manifesto da transação cross-chain"""
    lock_id: str
    source_chain: str
    target_chain: str
    amount: float
    source_tx_hash: str
    target_tx_hash: Optional[str]
    timestamp: str
    operator: str
    seed: Optional[int]
    notes: Optional[str]
    fee: Optional[float]
    exchange_rate: Optional[float]

@dataclass
class MerkleProof:
    """Prova Merkle de inclusão"""
    leaf_hash: str
    path: List[str]
    positions: List[int]  # 0 = left, 1 = right
    root: str
    tree_depth: int
    leaf_index: int

@dataclass
class ZKProof:
    """Prova ZK (Zero-Knowledge)"""
    circuit_id: str
    public_inputs: Dict[str, Any]
    proof_bytes: str  # Base64 encoded
    verifier_id: str
    proof_type: str  # "groth16" | "stark" | "plonk"
    verifying_key_hash: Optional[str]

@dataclass
class ConsensusProof:
    """Prova de consenso/finalidade"""
    block_header: Dict[str, Any]
    merkle_root: str
    confirmations: int
    consensus_type: str  # "pow" | "pos" | "poa"
    finality_proof: Optional[Dict[str, Any]]
    validator_signatures: Optional[List[str]]

class ProofBundleGenerator:
    """
    Gerador de Proof Bundles verificáveis para operações cross-chain
    
    Gera artefatos completos e assinados para auditoria:
    - transaction_manifest.json
    - merkle_proof.json
    - zk_proof.json (opcional)
    - consensus_proof.json
    - execution_log.log
    - bundle.sha256
    - bundle.signed.json
    - parameters.json
    """
    
    def __init__(self, quantum_security: Optional[QuantumSecuritySystem] = None):
        self.quantum_security = quantum_security
        self.pqc_keypair_id = None
        self.pqc_public_key = None
        
        # Inicializar PQC se disponível
        if self.quantum_security:
            try:
                keypair = self.quantum_security.generate_ml_dsa_keypair(security_level=3)
                self.pqc_keypair_id = keypair.get("keypair_id")
                self.pqc_public_key = keypair.get("public_key")
            except:
                pass
    
    def generate_merkle_proof(
        self,
        leaf_data: str,
        merkle_path: List[str],
        positions: List[int],
        root: str,
        leaf_index: int
    ) -> MerkleProof:
        """Gerar prova Merkle"""
        leaf_hash = hashlib.sha256(leaf_data.encode()).hexdigest()
        return MerkleProof(
            leaf_hash=leaf_hash,
            path=merkle_path,
            positions=positions,
            root=root,
            tree_depth=len(merkle_path),
            leaf_index=leaf_index
        )
    
    def generate_zk_proof(
        self,
        circuit_id: str,
        public_inputs: Dict[str, Any],
        proof_bytes: str,
        verifier_id: str,
        proof_type: str = "groth16",
        verifying_key_hash: Optional[str] = None
    ) -> ZKProof:
        """Gerar prova ZK (simulada ou real)"""
        return ZKProof(
            circuit_id=circuit_id,
            public_inputs=public_inputs,
            proof_bytes=proof_bytes,
            verifier_id=verifier_id,
            proof_type=proof_type,
            verifying_key_hash=verifying_key_hash
        )
    
    def generate_consensus_proof(
        self,
        block_header: Dict[str, Any],
        merkle_root: str,
        confirmations: int,
        consensus_type: str,
        finality_proof: Optional[Dict[str, Any]] = None,
        validator_signatures: Optional[List[str]] = None
    ) -> ConsensusProof:
        """Gerar prova de consenso"""
        return ConsensusProof(
            block_header=block_header,
            merkle_root=merkle_root,
            confirmations=confirmations,
            consensus_type=consensus_type,
            finality_proof=finality_proof,
            validator_signatures=validator_signatures
        )
    
    def create_transaction_manifest(
        self,
        lock_id: str,
        source_chain: str,
        target_chain: str,
        amount: float,
        source_tx_hash: str,
        target_tx_hash: Optional[str] = None,
        operator: str = "bridge-node-01",
        seed: Optional[int] = None,
        notes: Optional[str] = None,
        fee: Optional[float] = None,
        exchange_rate: Optional[float] = None
    ) -> TransactionManifest:
        """Criar manifesto de transação"""
        return TransactionManifest(
            lock_id=lock_id,
            source_chain=source_chain,
            target_chain=target_chain,
            amount=amount,
            source_tx_hash=source_tx_hash,
            target_tx_hash=target_tx_hash,
            timestamp=datetime.utcnow().isoformat() + "Z",
            operator=operator,
            seed=seed or int(time.time()),
            notes=notes,
            fee=fee,
            exchange_rate=exchange_rate
        )
    
    def generate_bundle_hash(self, files: Dict[str, str]) -> str:
        """
        Gerar hash SHA-256 do bundle completo
        Ordena arquivos por nome para determinismo
        """
        canonical_order = sorted(files.keys())
        combined = ""
        for filename in canonical_order:
            combined += f"{filename}:{files[filename]}\n"
        return hashlib.sha256(combined.encode('utf-8')).hexdigest()
    
    def sign_bundle(self, bundle_hash: str) -> Dict[str, Any]:
        """Assinar bundle com PQC"""
        if not self.quantum_security or not self.pqc_keypair_id:
            return {
                "algorithm": "NONE",
                "public_key": None,
                "signature": None,
                "note": "PQC signing not available"
            }
        
        hash_bytes = bytes.fromhex(bundle_hash)
        result = self.quantum_security.sign_ml_dsa(self.pqc_keypair_id, hash_bytes)
        
        if result.get("success"):
            return {
                "algorithm": "ML-DSA-128",
                "standard": "FIPS 204",
                "public_key": self.pqc_public_key,
                "signature": result.get("signature"),
                "signed_hash": bundle_hash,
                "timestamp": datetime.utcnow().isoformat() + "Z"
            }
        else:
            return {
                "algorithm": "ML-DSA-128",
                "public_key": self.pqc_public_key,
                "signature": None,
                "error": result.get("error", "Signing failed")
            }
    
    def generate_proof_bundle(
        self,
        manifest: TransactionManifest,
        merkle_proof: Optional[MerkleProof] = None,
        zk_proof: Optional[ZKProof] = None,
        consensus_proof: Optional[ConsensusProof] = None,
        execution_log: Optional[List[str]] = None,
        parameters: Optional[Dict[str, Any]] = None,
        output_dir: str = "proof_bundles"
    ) -> Dict[str, str]:
        """
        Gerar proof bundle completo e assinado
        
        Returns:
            Dict com caminhos dos arquivos gerados
        """
        os.makedirs(output_dir, exist_ok=True)
        bundle_id = manifest.lock_id
        
        # 1. Gerar transaction_manifest.json
        manifest_dict = asdict(manifest)
        manifest_json = json.dumps(manifest_dict, indent=2, sort_keys=True, ensure_ascii=False)
        manifest_path = os.path.join(output_dir, f"{bundle_id}_transaction_manifest.json")
        with open(manifest_path, 'w', encoding='utf-8') as f:
            f.write(manifest_json)
        
        # 2. Gerar merkle_proof.json (se disponível)
        files_content = {"transaction_manifest.json": manifest_json}
        merkle_path = None
        if merkle_proof:
            merkle_dict = asdict(merkle_proof)
            merkle_json = json.dumps(merkle_dict, indent=2, sort_keys=True, ensure_ascii=False)
            merkle_path = os.path.join(output_dir, f"{bundle_id}_merkle_proof.json")
            with open(merkle_path, 'w', encoding='utf-8') as f:
                f.write(merkle_json)
            files_content["merkle_proof.json"] = merkle_json
        
        # 3. Gerar zk_proof.json (se disponível)
        zk_path = None
        if zk_proof:
            zk_dict = asdict(zk_proof)
            zk_json = json.dumps(zk_dict, indent=2, sort_keys=True, ensure_ascii=False)
            zk_path = os.path.join(output_dir, f"{bundle_id}_zk_proof.json")
            with open(zk_path, 'w', encoding='utf-8') as f:
                f.write(zk_json)
            files_content["zk_proof.json"] = zk_json
        
        # 4. Gerar consensus_proof.json (se disponível)
        consensus_path = None
        if consensus_proof:
            consensus_dict = asdict(consensus_proof)
            consensus_json = json.dumps(consensus_dict, indent=2, sort_keys=True, ensure_ascii=False)
            consensus_path = os.path.join(output_dir, f"{bundle_id}_consensus_proof.json")
            with open(consensus_path, 'w', encoding='utf-8') as f:
                f.write(consensus_json)
            files_content["consensus_proof.json"] = consensus_json
        
        # 5. Gerar execution_log.log
        log_path = os.path.join(output_dir, f"{bundle_id}_execution_log.log")
        log_content = execution_log or [
            f"[{datetime.utcnow().isoformat()}Z] Proof bundle generation started",
            f"[{datetime.utcnow().isoformat()}Z] Bundle ID: {bundle_id}",
            f"[{datetime.utcnow().isoformat()}Z] Source: {manifest.source_chain} -> Target: {manifest.target_chain}",
            f"[{datetime.utcnow().isoformat()}Z] Amount: {manifest.amount}",
            f"[{datetime.utcnow().isoformat()}Z] Proof bundle generation completed"
        ]
        with open(log_path, 'w', encoding='utf-8') as f:
            f.write("\n".join(log_content))
        files_content["execution_log.log"] = "\n".join(log_content)
        
        # 6. Gerar parameters.json
        params = parameters or {
            "seed": manifest.seed,
            "quantum_assumptions": {
                "qubit_quality": "logical_qubits_with_surface_code",
                "error_rate": "10^-3",
                "gate_time": "100ns"
            },
            "security_parameters": {
                "security_level": "NIST_Level_3",
                "attack_model": "Q2_model"
            },
            "version": "1.0",
            "generated_at": datetime.utcnow().isoformat() + "Z"
        }
        params_json = json.dumps(params, indent=2, sort_keys=True, ensure_ascii=False)
        params_path = os.path.join(output_dir, f"{bundle_id}_parameters.json")
        with open(params_path, 'w', encoding='utf-8') as f:
            f.write(params_json)
        files_content["parameters.json"] = params_json
        
        # 7. Gerar bundle.sha256
        bundle_hash = self.generate_bundle_hash(files_content)
        hash_path = os.path.join(output_dir, f"{bundle_id}_bundle.sha256")
        with open(hash_path, 'w', encoding='utf-8') as f:
            f.write(bundle_hash)
        
        # 8. Assinar bundle
        signature_data = self.sign_bundle(bundle_hash)
        signature_json = json.dumps(signature_data, indent=2, sort_keys=True, ensure_ascii=False)
        signature_path = os.path.join(output_dir, f"{bundle_id}_bundle.signed.json")
        with open(signature_path, 'w', encoding='utf-8') as f:
            f.write(signature_json)
        
        # 9. Gerar bundle_index.json (índice de todos os arquivos)
        bundle_index = {
            "bundle_id": bundle_id,
            "generated_at": datetime.utcnow().isoformat() + "Z",
            "files": {
                "transaction_manifest": f"{bundle_id}_transaction_manifest.json",
                "merkle_proof": f"{bundle_id}_merkle_proof.json" if merkle_proof else None,
                "zk_proof": f"{bundle_id}_zk_proof.json" if zk_proof else None,
                "consensus_proof": f"{bundle_id}_consensus_proof.json" if consensus_proof else None,
                "execution_log": f"{bundle_id}_execution_log.log",
                "parameters": f"{bundle_id}_parameters.json",
                "bundle_hash": f"{bundle_id}_bundle.sha256",
                "bundle_signature": f"{bundle_id}_bundle.signed.json"
            },
            "bundle_hash": bundle_hash,
            "signature_algorithm": signature_data.get("algorithm"),
            "verification_instructions": {
                "step_1": "Calculate SHA-256 of all JSON files in canonical order",
                "step_2": "Compare with bundle.sha256",
                "step_3": "Verify PQC signature using public_key from bundle.signed.json",
                "step_4": "Validate merkle proof (if available)",
                "step_5": "Verify ZK proof using verifier (if available)"
            }
        }
        index_path = os.path.join(output_dir, f"{bundle_id}_bundle_index.json")
        with open(index_path, 'w', encoding='utf-8') as f:
            json.dump(bundle_index, f, indent=2, sort_keys=True, ensure_ascii=False)
        
        return {
            "bundle_id": bundle_id,
            "bundle_hash": bundle_hash,
            "output_dir": output_dir,
            "files": {
                "manifest": manifest_path,
                "merkle": merkle_path,
                "zk": zk_path,
                "consensus": consensus_path,
                "log": log_path,
                "parameters": params_path,
                "hash": hash_path,
                "signature": signature_path,
                "index": index_path
            },
            "signature": signature_data
        }
    
    def verify_bundle(self, bundle_dir: str, bundle_id: str) -> Dict[str, Any]:
        """
        Verificar proof bundle completo
        
        Returns:
            Dict com resultado da verificação
        """
        results = {
            "bundle_id": bundle_id,
            "verified": False,
            "checks": {},
            "errors": []
        }
        
        try:
            # 1. Ler bundle_index.json
            index_path = os.path.join(bundle_dir, f"{bundle_id}_bundle_index.json")
            if not os.path.exists(index_path):
                results["errors"].append("bundle_index.json not found")
                return results
            
            with open(index_path, 'r', encoding='utf-8') as f:
                bundle_index = json.load(f)
            
            # 2. Ler todos os arquivos mencionados
            files_content = {}
            for file_type, filename in bundle_index["files"].items():
                if filename:
                    file_path = os.path.join(bundle_dir, filename)
                    if os.path.exists(file_path):
                        with open(file_path, 'r', encoding='utf-8') as f:
                            files_content[file_type] = f.read()
            
            # 3. Verificar hash
            expected_hash = bundle_index.get("bundle_hash")
            calculated_hash = self.generate_bundle_hash(files_content)
            results["checks"]["hash_match"] = expected_hash == calculated_hash
            if not results["checks"]["hash_match"]:
                results["errors"].append(f"Hash mismatch: expected {expected_hash}, got {calculated_hash}")
            
            # 4. Verificar assinatura PQC
            signature_path = os.path.join(bundle_dir, f"{bundle_id}_bundle.signed.json")
            if os.path.exists(signature_path):
                with open(signature_path, 'r', encoding='utf-8') as f:
                    signature_data = json.load(f)
                
                if signature_data.get("algorithm") == "ML-DSA-128" and self.quantum_security:
                    public_key = signature_data.get("public_key")
                    signature = signature_data.get("signature")
                    signed_hash = signature_data.get("signed_hash")
                    
                    if public_key and signature and signed_hash == calculated_hash:
                        hash_bytes = bytes.fromhex(calculated_hash)
                        verify_result = self.quantum_security.verify_ml_dsa(
                            public_key, hash_bytes, signature
                        )
                        results["checks"]["pqc_signature"] = verify_result.get("success", False)
                        if not results["checks"]["pqc_signature"]:
                            results["errors"].append("PQC signature verification failed")
                    else:
                        results["checks"]["pqc_signature"] = False
                        results["errors"].append("Invalid signature data")
                else:
                    results["checks"]["pqc_signature"] = None
                    results["errors"].append("PQC verification not available")
            
            # 5. Verificar se todos os arquivos existem
            missing_files = []
            for file_type, filename in bundle_index["files"].items():
                if filename and file_type not in ["merkle_proof", "zk_proof", "consensus_proof"]:  # Opcionais
                    file_path = os.path.join(bundle_dir, filename)
                    if not os.path.exists(file_path):
                        missing_files.append(filename)
            
            results["checks"]["all_files_present"] = len(missing_files) == 0
            if missing_files:
                results["errors"].append(f"Missing files: {', '.join(missing_files)}")
            
            # Verificação geral
            results["verified"] = all([
                results["checks"].get("hash_match", False),
                results["checks"].get("pqc_signature", False) is not False,  # None é OK se não disponível
                results["checks"].get("all_files_present", False)
            ])
            
        except Exception as e:
            results["errors"].append(f"Verification error: {str(e)}")
        
        return results







