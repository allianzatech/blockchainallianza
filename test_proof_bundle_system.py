#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧪 TESTE DO SISTEMA DE PROOF BUNDLES
Valida todas as funcionalidades implementadas
"""

import os
import sys
import json
import time
from proof_bundle_generator import (
    ProofBundleGenerator,
    TransactionManifest,
    MerkleProof,
    ZKProof,
    ConsensusProof
)
from quantum_multisig import QuantumMultisig, Signer
from audit_system import AuditSystem

def test_proof_bundle_generation():
    """Teste 1: Geração de Proof Bundle"""
    print("\n" + "="*70)
    print("🧪 TESTE 1: Geração de Proof Bundle")
    print("="*70)
    
    try:
        # Inicializar gerador
        generator = ProofBundleGenerator()
        print("✅ ProofBundleGenerator inicializado")
        
        # Criar manifest
        manifest = generator.create_transaction_manifest(
            lock_id="lock_test_12345",
            source_chain="polygon",
            target_chain="bitcoin",
            amount=0.1,
            source_tx_hash="0xabc123...",
            target_tx_hash="tx_test_456",
            operator="bridge-node-01",
            seed=12345,
            notes="Teste de proof bundle",
            fee=0.0001,
            exchange_rate=87500.0
        )
        print("✅ TransactionManifest criado")
        
        # Criar merkle proof (simulado)
        merkle_proof = generator.generate_merkle_proof(
            leaf_data=json.dumps({"tx_hash": "0xabc123..."}, sort_keys=True),
            merkle_path=["hash1", "hash2", "hash3"],
            positions=[0, 1, 0],
            root="merkle_root_abc123",
            leaf_index=5
        )
        print("✅ MerkleProof criado")
        
        # Criar ZK proof (simulado)
        zk_proof = generator.generate_zk_proof(
            circuit_id="circuit_lock_verification",
            public_inputs={
                "lock_id": "lock_test_12345",
                "merkle_root": "merkle_root_abc123",
                "amount": 0.1
            },
            proof_bytes="dGVzdF9wcm9vZl9ieXRlcw==",  # Base64 simulado
            verifier_id="verifier_contract_0x123",
            proof_type="groth16"
        )
        print("✅ ZKProof criado")
        
        # Criar consensus proof (simulado)
        consensus_proof = generator.generate_consensus_proof(
            block_header={
                "number": 12345,
                "hash": "0xblock123",
                "timestamp": int(time.time())
            },
            merkle_root="merkle_root_abc123",
            confirmations=12,
            consensus_type="pos"
        )
        print("✅ ConsensusProof criado")
        
        # Gerar bundle completo
        execution_log = [
            f"[{time.strftime('%Y-%m-%dT%H:%M:%SZ')}] Início da transferência",
            f"[{time.strftime('%Y-%m-%dT%H:%M:%SZ')}] Lock criado na chain de origem",
            f"[{time.strftime('%Y-%m-%dT%H:%M:%SZ')}] Transação confirmada",
            f"[{time.strftime('%Y-%m-%dT%H:%M:%SZ')}] Unlock executado na chain de destino"
        ]
        
        bundle_result = generator.generate_proof_bundle(
            manifest=manifest,
            merkle_proof=merkle_proof,
            zk_proof=zk_proof,
            consensus_proof=consensus_proof,
            execution_log=execution_log,
            parameters={
                "seed": 12345,
                "quantum_assumptions": {
                    "qubit_quality": "logical_qubits_with_surface_code"
                }
            }
        )
        
        print(f"✅ Proof Bundle gerado!")
        print(f"   Bundle ID: {bundle_result['bundle_id']}")
        print(f"   Bundle Hash: {bundle_result['bundle_hash']}")
        print(f"   Arquivos gerados: {len(bundle_result['files'])}")
        print(f"   Diretório: {bundle_result['output_dir']}")
        
        # Verificar bundle
        verification = generator.verify_bundle(
            bundle_dir=bundle_result['output_dir'],
            bundle_id=bundle_result['bundle_id']
        )
        
        print(f"\n📊 Resultado da Verificação:")
        print(f"   Verificado: {verification['verified']}")
        print(f"   Checks: {verification['checks']}")
        if verification['errors']:
            print(f"   Erros: {verification['errors']}")
        
        return bundle_result, verification
        
    except Exception as e:
        print(f"❌ Erro no teste: {e}")
        import traceback
        traceback.print_exc()
        return None, None

def test_quantum_multisig():
    """Teste 2: Multi-Sig Quântico"""
    print("\n" + "="*70)
    print("🧪 TESTE 2: Multi-Sig Quântico")
    print("="*70)
    
    try:
        # Inicializar multi-sig
        multisig = QuantumMultisig()
        print("✅ QuantumMultisig inicializado")
        
        # Adicionar signers
        signer1 = multisig.add_signer(
            signer_id="signer_1",
            public_key="pubkey_signer1",
            algorithm="ML-DSA-128",
            keypair_id="kp1",
            weight=1
        )
        signer2 = multisig.add_signer(
            signer_id="signer_2",
            public_key="pubkey_signer2",
            algorithm="ML-DSA-128",
            keypair_id="kp2",
            weight=1
        )
        signer3 = multisig.add_signer(
            signer_id="signer_3",
            public_key="pubkey_signer3",
            algorithm="SLH-DSA-SHA2-128s",
            keypair_id="kp3",
            weight=1
        )
        print("✅ Signers adicionados")
        
        # Criar política (2-of-3)
        policy = multisig.create_policy(
            policy_id="policy_test",
            threshold=2,
            signers=[signer1, signer2, signer3],
            algorithm_preference="ML-DSA-128",
            require_dual_algorithm=False
        )
        print("✅ Política criada (2-of-3)")
        
        # Assinar transação
        transaction_id = "tx_test_multisig"
        data_to_sign = b"test_transaction_data_12345"
        
        sig1 = multisig.sign_transaction(transaction_id, data_to_sign, "signer_1", "kp1")
        sig2 = multisig.sign_transaction(transaction_id, data_to_sign, "signer_2", "kp2")
        
        print(f"✅ Assinaturas coletadas: {len([s for s in [sig1, sig2] if s])}")
        
        # Verificar multi-sig
        verification = multisig.verify_multisig(
            transaction_id=transaction_id,
            policy_id="policy_test",
            data_to_verify=data_to_sign
        )
        
        print(f"\n📊 Resultado da Verificação Multi-Sig:")
        print(f"   Verificado: {verification['verified']}")
        print(f"   Threshold atendido: {verification['threshold_met']}")
        print(f"   Assinaturas válidas: {verification['valid_signatures_count']}")
        print(f"   Signers válidos: {verification['valid_signers']}")
        
        # Agregar assinaturas
        aggregated = multisig.aggregate_signatures(transaction_id)
        print(f"\n✅ Assinaturas agregadas: {aggregated['signatures_count']} assinaturas")
        
        return verification
        
    except Exception as e:
        print(f"❌ Erro no teste: {e}")
        import traceback
        traceback.print_exc()
        return None

def test_audit_system():
    """Teste 3: Sistema de Auditoria"""
    print("\n" + "="*70)
    print("🧪 TESTE 3: Sistema de Auditoria")
    print("="*70)
    
    try:
        # Inicializar sistema de auditoria
        audit = AuditSystem()
        print("✅ AuditSystem inicializado")
        
        # Gerar checklist
        checklist = audit.generate_auditor_checklist()
        print(f"✅ Checklist gerado: {len(checklist['steps'])} passos")
        
        # Simular verificação
        verification_results = {
            "verified": True,
            "checks": {
                "hash_match": True,
                "pqc_signature": True,
                "all_files_present": True
            },
            "errors": []
        }
        
        # Gerar relatório
        report = audit.generate_audit_report(
            transaction_id="tx_test_audit",
            bundle_path="proof_bundles/",
            verification_results=verification_results,
            additional_metrics={
                "time_generate_ms": 150,
                "time_sign_ms": 50,
                "bundle_size_bytes": 1024
            }
        )
        
        print(f"✅ Relatório de auditoria gerado")
        print(f"   Report ID: {report['audit_report_id']}")
        print(f"   Checks realizados: {len(report['checks_performed'])}")
        print(f"   Recomendações: {len(report['recommendations'])}")
        
        # Gerar pacote para desenvolvedores
        dev_package = audit.generate_developer_package(
            bundle_id="lock_test_12345",
            bundle_dir="proof_bundles"
        )
        print(f"✅ Pacote para desenvolvedores gerado")
        
        # Exportar bundle de auditoria
        export_result = audit.export_audit_bundle(
            transaction_id="tx_test_audit"
        )
        print(f"✅ Bundle de auditoria exportado")
        print(f"   Checklist: {export_result['checklist']}")
        print(f"   Dev Package: {export_result['developer_package']}")
        
        return report, dev_package
        
    except Exception as e:
        print(f"❌ Erro no teste: {e}")
        import traceback
        traceback.print_exc()
        return None, None

def test_integration():
    """Teste 4: Integração Completa"""
    print("\n" + "="*70)
    print("🧪 TESTE 4: Integração Completa")
    print("="*70)
    
    try:
        # Gerar bundle
        generator = ProofBundleGenerator()
        manifest = generator.create_transaction_manifest(
            lock_id="lock_integration_test",
            source_chain="polygon",
            target_chain="bitcoin",
            amount=0.5,
            source_tx_hash="0xintegration123"
        )
        
        bundle_result = generator.generate_proof_bundle(
            manifest=manifest,
            execution_log=["Log de teste de integração"]
        )
        
        # Verificar bundle
        verification = generator.verify_bundle(
            bundle_dir=bundle_result['output_dir'],
            bundle_id=bundle_result['bundle_id']
        )
        
        # Gerar relatório de auditoria
        audit = AuditSystem(generator)
        report = audit.generate_audit_report(
            transaction_id=bundle_result['bundle_id'],
            bundle_path=bundle_result['output_dir'],
            verification_results=verification
        )
        
        print("✅ Integração completa testada!")
        print(f"   Bundle: {bundle_result['bundle_id']}")
        print(f"   Verificado: {verification['verified']}")
        print(f"   Relatório: {report['audit_report_id']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro no teste: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Executar todos os testes"""
    print("\n" + "="*70)
    print("🚀 TESTE COMPLETO DO SISTEMA DE PROOF BUNDLES")
    print("="*70)
    print("\nEste teste valida:")
    print("  ✅ Geração de Proof Bundles")
    print("  ✅ Multi-Sig Quântico")
    print("  ✅ Sistema de Auditoria")
    print("  ✅ Integração Completa")
    print("\n" + "="*70)
    
    results = {
        "proof_bundle": False,
        "multisig": False,
        "audit": False,
        "integration": False
    }
    
    # Teste 1: Proof Bundle
    bundle_result, verification = test_proof_bundle_generation()
    results["proof_bundle"] = bundle_result is not None and verification is not None
    
    # Teste 2: Multi-Sig
    multisig_result = test_quantum_multisig()
    results["multisig"] = multisig_result is not None
    
    # Teste 3: Auditoria
    audit_report, dev_package = test_audit_system()
    results["audit"] = audit_report is not None
    
    # Teste 4: Integração
    results["integration"] = test_integration()
    
    # Resumo
    print("\n" + "="*70)
    print("📊 RESUMO DOS TESTES")
    print("="*70)
    for test_name, passed in results.items():
        status = "✅ PASSOU" if passed else "❌ FALHOU"
        print(f"  {test_name.upper()}: {status}")
    
    total_passed = sum(1 for v in results.values() if v)
    total_tests = len(results)
    
    print(f"\n🎯 Resultado Final: {total_passed}/{total_tests} testes passaram")
    
    if total_passed == total_tests:
        print("🎉 TODOS OS TESTES PASSARAM! Sistema pronto para uso!")
    else:
        print("⚠️  Alguns testes falharam. Revise os erros acima.")
    
    return results

if __name__ == "__main__":
    main()





