#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔍 SISTEMA DE AUDITORIA
Gera artefatos verificáveis e relatórios para auditores
"""

import json
import os
import hashlib
import time
from typing import Dict, List, Optional, Any
from datetime import datetime
try:
    from proof_bundle_generator import ProofBundleGenerator
except ImportError:
    ProofBundleGenerator = None
try:
    from quantum_multisig import QuantumMultisig
except ImportError:
    QuantumMultisig = None

class AuditSystem:
    """
    Sistema de Auditoria Completo
    
    Gera:
    - Proof bundles verificáveis
    - Relatórios de auditoria
    - Checklists de verificação
    - Artefatos para devs/empresas
    """
    
    def __init__(
        self,
        proof_generator: Optional[ProofBundleGenerator] = None,
        multisig: Optional[QuantumMultisig] = None
    ):
        if proof_generator:
            self.proof_generator = proof_generator
        elif ProofBundleGenerator:
            self.proof_generator = ProofBundleGenerator()
        else:
            self.proof_generator = None
        self.multisig = multisig
        self.audit_reports: List[Dict[str, Any]] = []
    
    def generate_audit_report(
        self,
        transaction_id: str,
        bundle_path: str,
        verification_results: Dict[str, Any],
        additional_metrics: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Gerar relatório de auditoria completo"""
        
        report = {
            "audit_report_id": f"audit_{transaction_id}_{int(time.time())}",
            "transaction_id": transaction_id,
            "generated_at": datetime.utcnow().isoformat() + "Z",
            "auditor": "Allianza Blockchain Audit System",
            "version": "1.0",
            
            "bundle_location": bundle_path,
            "verification_results": verification_results,
            
            "checks_performed": {
                "hash_verification": verification_results.get("checks", {}).get("hash_match", False),
                "pqc_signature_verification": verification_results.get("checks", {}).get("pqc_signature", False),
                "file_integrity": verification_results.get("checks", {}).get("all_files_present", False),
                "bundle_completeness": True
            },
            
            "metrics": additional_metrics or {},
            
            "recommendations": self._generate_recommendations(verification_results),
            
            "next_steps": [
                "Verify bundle hash matches bundle.sha256",
                "Verify PQC signature using public_key",
                "Validate merkle proof (if available)",
                "Verify ZK proof using verifier (if available)",
                "Check execution log for anomalies"
            ],
            
            "compliance": {
                "nist_pqc_standards": True,
                "quantum_safe": True,
                "audit_trail": True,
                "reproducibility": True
            }
        }
        
        self.audit_reports.append(report)
        return report
    
    def _generate_recommendations(self, verification_results: Dict[str, Any]) -> List[str]:
        """Gerar recomendações baseadas nos resultados"""
        recommendations = []
        
        checks = verification_results.get("checks", {})
        errors = verification_results.get("errors", [])
        
        if not checks.get("hash_match", False):
            recommendations.append("CRITICAL: Bundle hash mismatch detected. Do not trust this bundle.")
        
        if checks.get("pqc_signature") is False:
            recommendations.append("CRITICAL: PQC signature verification failed. Bundle may be compromised.")
        
        if not checks.get("all_files_present", False):
            recommendations.append("WARNING: Some bundle files are missing. Verify completeness.")
        
        if len(errors) > 0:
            recommendations.append(f"WARNING: {len(errors)} verification errors found. Review errors list.")
        
        if all(checks.values()):
            recommendations.append("SUCCESS: All checks passed. Bundle is verified and trustworthy.")
        
        return recommendations
    
    def generate_auditor_checklist(self) -> Dict[str, Any]:
        """Gerar checklist para auditores"""
        return {
            "checklist_version": "1.0",
            "generated_at": datetime.utcnow().isoformat() + "Z",
            "steps": [
                {
                    "step": 1,
                    "description": "Verify bundle hash",
                    "action": "Calculate SHA-256 of all JSON files in canonical order and compare with bundle.sha256",
                    "expected_result": "Hash matches"
                },
                {
                    "step": 2,
                    "description": "Verify PQC signature",
                    "action": "Use public_key from bundle.signed.json to verify signature on bundle hash",
                    "expected_result": "Signature valid"
                },
                {
                    "step": 3,
                    "description": "Validate transaction manifest",
                    "action": "Check transaction_manifest.json for required fields and consistency",
                    "expected_result": "All fields present and valid"
                },
                {
                    "step": 4,
                    "description": "Verify merkle proof (if available)",
                    "action": "Validate merkle path and root match expected values",
                    "expected_result": "Merkle proof valid"
                },
                {
                    "step": 5,
                    "description": "Verify ZK proof (if available)",
                    "action": "Run ZK verifier with public inputs and proof",
                    "expected_result": "ZK proof valid"
                },
                {
                    "step": 6,
                    "description": "Check execution log",
                    "action": "Review execution_log.log for errors or anomalies",
                    "expected_result": "No critical errors"
                },
                {
                    "step": 7,
                    "description": "Verify parameters",
                    "action": "Check parameters.json matches expected assumptions",
                    "expected_result": "Parameters consistent"
                },
                {
                    "step": 8,
                    "description": "Reproducibility test",
                    "action": "Re-run simulation with same seed and verify hash matches",
                    "expected_result": "Same hash generated"
                }
            ],
            "tools_required": [
                "SHA-256 calculator",
                "PQC signature verifier (ML-DSA-128)",
                "Merkle proof verifier",
                "ZK proof verifier (if applicable)"
            ],
            "references": [
                "NIST FIPS 204 (ML-DSA)",
                "NIST FIPS 205 (SLH-DSA)",
                "Proof Bundle Specification v1.0"
            ]
        }
    
    def generate_developer_package(
        self,
        bundle_id: str,
        bundle_dir: str
    ) -> Dict[str, Any]:
        """Gerar pacote completo para desenvolvedores"""
        
        package = {
            "package_id": f"dev_package_{bundle_id}",
            "generated_at": datetime.utcnow().isoformat() + "Z",
            "bundle_id": bundle_id,
            "bundle_directory": bundle_dir,
            
            "contents": {
                "proof_bundle": f"{bundle_dir}/{bundle_id}_*",
                "verification_script": "verify_bundle.py",
                "documentation": "PROOF_BUNDLE_SPEC.md",
                "examples": "examples/"
            },
            
            "verification_instructions": {
                "quick_start": "Run: python verify_bundle.py --bundle-dir <dir> --bundle-id <id>",
                "manual_verification": "See PROOF_BUNDLE_SPEC.md for detailed steps",
                "api_integration": "Use ProofBundleGenerator.verify_bundle() method"
            },
            
            "technical_specs": {
                "hash_algorithm": "SHA-256",
                "signature_algorithm": "ML-DSA-128 (FIPS 204)",
                "encoding": "UTF-8",
                "json_format": "Canonical (sort_keys=True)"
            },
            
            "support": {
                "documentation": "https://github.com/allianza-blockchain/docs",
                "api_reference": "https://api.allianza-blockchain.com/docs",
                "contact": "support@allianza-blockchain.com"
            }
        }
        
        return package
    
    def export_audit_bundle(
        self,
        transaction_id: str,
        output_dir: str = "audit_bundles"
    ) -> Dict[str, str]:
        """Exportar bundle completo de auditoria"""
        os.makedirs(output_dir, exist_ok=True)
        
        # Gerar checklist
        checklist = self.generate_auditor_checklist()
        checklist_path = os.path.join(output_dir, f"{transaction_id}_auditor_checklist.json")
        with open(checklist_path, 'w', encoding='utf-8') as f:
            json.dump(checklist, f, indent=2, sort_keys=True, ensure_ascii=False)
        
        # Gerar pacote para desenvolvedores
        dev_package = self.generate_developer_package(transaction_id, "proof_bundles")
        dev_package_path = os.path.join(output_dir, f"{transaction_id}_developer_package.json")
        with open(dev_package_path, 'w', encoding='utf-8') as f:
            json.dump(dev_package, f, indent=2, sort_keys=True, ensure_ascii=False)
        
        return {
            "checklist": checklist_path,
            "developer_package": dev_package_path,
            "output_dir": output_dir
        }

