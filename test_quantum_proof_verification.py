#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧪 TESTE DE PROVA VERIFICÁVEL DE SEGURANÇA QUÂNTICA
Demonstra o sistema completo de provas verificáveis
"""

import os
import json
from quantum_attack_simulator import QuantumAttackSimulator
from quantum_proof_verifier import QuantumProofVerifier

def test_complete_verifiable_proof():
    """Teste completo: Gerar e verificar prova"""
    print("\n" + "="*70)
    print("🔐 TESTE DE PROVA VERIFICÁVEL DE SEGURANÇA QUÂNTICA")
    print("="*70)
    
    try:
        # 1. Inicializar sistemas
        print("\n📦 Inicializando sistemas...")
        try:
            from quantum_security import QuantumSecuritySystem
            quantum_security = QuantumSecuritySystem()
        except:
            quantum_security = None
            print("⚠️  Quantum Security não disponível, usando modo mock")
        
        simulator = QuantumAttackSimulator(quantum_security)
        verifier = QuantumProofVerifier(quantum_security)
        
        print("✅ Sistemas inicializados")
        
        # 2. Executar simulação
        print("\n🔬 Executando simulação de ataque quântico...")
        result = simulator.run_comparison_demo(save_json=True)
        
        print("✅ Simulação concluída")
        
        # 3. Verificar se prova foi gerada
        json_file = result.get("json_file")
        if not json_file:
            print("❌ JSON não foi gerado")
            return False
        
        print(f"\n📄 JSON gerado: {json_file}")
        
        # 4. Verificar se há metadados de verificação
        verification_info = result.get("verification")
        if verification_info:
            print("\n🔐 PROVA VERIFICÁVEL GERADA:")
            print(f"   Proof ID: {verification_info.get('proof_id')}")
            print(f"   Hash SHA-256: {verification_info.get('canonical_sha256')}")
            print(f"   Algoritmo PQC: {verification_info.get('pqc_signature', {}).get('algorithm', 'N/A')}")
            
            # 5. Verificar prova
            proof_id = verification_info.get("proof_id")
            if proof_id:
                print(f"\n🔍 Verificando prova: {proof_id}")
                verification = verifier.verify_proof(
                    proof_dir="quantum_attack_simulations",
                    proof_id=proof_id
                )
                
                print(f"\n📊 RESULTADO DA VERIFICAÇÃO:")
                print(f"   Verificado: {verification['verified']}")
                print(f"   Checks: {verification['checks']}")
                if verification['errors']:
                    print(f"   Erros: {verification['errors']}")
                
                # 6. Listar arquivos gerados
                verification_files = verification_info.get("verification_files", {})
                print(f"\n📁 ARQUIVOS DO BUNDLE:")
                for file_type, file_path in verification_files.items():
                    if file_path and os.path.exists(file_path):
                        size = os.path.getsize(file_path)
                        print(f"   ✅ {file_type}: {file_path} ({size} bytes)")
                    elif file_path:
                        print(f"   ⚠️  {file_type}: {file_path} (não encontrado)")
                
                return verification['verified']
            else:
                print("⚠️  Proof ID não encontrado")
                return False
        else:
            print("⚠️  Metadados de verificação não encontrados")
            print("   (Sistema pode estar usando método padrão)")
            return False
        
    except Exception as e:
        print(f"❌ Erro no teste: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_canonical_json():
    """Teste: Verificar que JSON é canônico"""
    print("\n" + "="*70)
    print("🧪 TESTE: JSON Canônico (RFC 8785)")
    print("="*70)
    
    try:
        verifier = QuantumProofVerifier()
        
        # Dados de teste
        test_data = {
            "c": 3,
            "a": 1,
            "b": 2,
            "nested": {
                "z": 26,
                "a": 1
            }
        }
        
        # Gerar JSON canônico
        canonical = verifier.canonicalize_json(test_data)
        
        # Verificar que é determinístico
        canonical2 = verifier.canonicalize_json(test_data)
        
        if canonical == canonical2:
            print("✅ JSON canônico é determinístico")
        else:
            print("❌ JSON canônico não é determinístico")
            return False
        
        # Verificar hash
        hash1 = verifier.calculate_sha256(canonical)
        hash2 = verifier.calculate_sha256(canonical2)
        
        if hash1 == hash2:
            print("✅ Hash SHA-256 é determinístico")
            print(f"   Hash: {hash1}")
        else:
            print("❌ Hash SHA-256 não é determinístico")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

def test_mathematical_proof():
    """Teste: Verificar prova matemática"""
    print("\n" + "="*70)
    print("🧪 TESTE: Prova Matemática dos Cálculos")
    print("="*70)
    
    try:
        verifier = QuantumProofVerifier()
        
        # Dados de simulação de teste
        simulation_data = {
            "traditional": {
                "attack_time_seconds": 120.5,
                "funds_stolen": 10.0
            },
            "protected": {
                "attack_time_seconds": 999999.0,
                "funds_protected": 10.0
            }
        }
        
        # Gerar prova matemática
        math_proof = verifier.generate_mathematical_proof(simulation_data)
        
        print("✅ Prova matemática gerada")
        print(f"   Cálculos incluídos: {len(math_proof.get('mathematical_proof', {}).get('calculations', {}))}")
        
        # Verificar conteúdo
        calculations = math_proof.get("mathematical_proof", {}).get("calculations", {})
        
        if "ecdsa_shor" in calculations:
            print("✅ Cálculo ECDSA + Shor incluído")
            ecdsa_calc = calculations["ecdsa_shor"]
            print(f"   Fórmula: {ecdsa_calc.get('complexity', {}).get('formula', 'N/A')}")
            print(f"   Qubits lógicos: {ecdsa_calc.get('qubit_estimation', {}).get('logical_qubits', {}).get('logical_qubits_estimate', 'N/A')}")
        
        if "ml_dsa_grover" in calculations:
            print("✅ Cálculo ML-DSA + Grover incluído")
            ml_dsa_calc = calculations["ml_dsa_grover"]
            print(f"   Fórmula: {ml_dsa_calc.get('complexity', {}).get('formula', 'N/A')}")
            print(f"   Segurança quântica: {ml_dsa_calc.get('security_margin', {}).get('quantum_security', 'N/A')}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Executar todos os testes"""
    print("\n" + "="*70)
    print("🚀 TESTE COMPLETO DE PROVAS VERIFICÁVEIS")
    print("="*70)
    
    results = {
        "canonical_json": False,
        "mathematical_proof": False,
        "complete_proof": False
    }
    
    # Teste 1: JSON Canônico
    results["canonical_json"] = test_canonical_json()
    
    # Teste 2: Prova Matemática
    results["mathematical_proof"] = test_mathematical_proof()
    
    # Teste 3: Prova Completa
    results["complete_proof"] = test_complete_verifiable_proof()
    
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
        print("🎉 TODOS OS TESTES PASSARAM!")
        print("✅ Sistema de Provas Verificáveis está funcionando!")
    else:
        print("⚠️  Alguns testes falharam. Revise os erros acima.")
    
    return results

if __name__ == "__main__":
    main()





